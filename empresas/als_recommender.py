""" An example of using this library to calculate related artists
from the last.fm dataset. More details can be found
at http://www.benfrederickson.com/matrix-factorization/
"""

import time
import numpy
import logging
import pandas
from scipy.sparse import coo_matrix
import annoy
from implicit import alternating_least_squares
from .models import Empresa, RecommendedClients, RecommendedProviders

def read_data(transferencias, inv=False):
    """ Reads in the last.fm dataset, and returns a tuple of a pandas dataframe
    and a sparse matrix of artist/user/playcount """
    # read in triples of user/artist/playcount from the input dataset
    if inv:
        transfer_count = transferencias.groupby(["REFERENCIA_1", "REFERENCIA_ORIGEN"]).IMPORTE.count().reset_index()
    else:
        transfer_count = transferencias.groupby(["REFERENCIA_ORIGEN", "REFERENCIA_1"]).IMPORTE.count().reset_index()

    # for index, row in transfer_count.iterrows():
    #     cliente = Empresa.objects.get(fiscal_id=str(row['REFERENCIA_ORIGEN']))
    #     proveedor = Empresa.objects.get(fiscal_id=str(row['REFERENCIA_1']))
    #     proveedor.clients.add(cliente)
    #     cliente.providers.add(proveedor)

    print("clientes y proveedores cargados")

    data = pandas.DataFrame()
    data['user'] = transfer_count['REFERENCIA_ORIGEN'].astype("category")
    data['artist'] = transfer_count['REFERENCIA_1'].astype("category")
    data['transfers'] = transfer_count['IMPORTE'].astype("category")

    transfers = coo_matrix((data['transfers'].astype(float),
                       (data['artist'].cat.codes.copy(),
                        data['user'].cat.codes.copy())))

    return data, transfers

def bm25_weight(X, K1=100, B=0.8):
    """ Weighs each row of the sparse matrix of the data by BM25 weighting """
    # calculate idf per term (user)
    X = coo_matrix(X)
    N = X.shape[0]
    idf = numpy.log(float(N) / (1 + numpy.bincount(X.col)))

    # calculate length_norm per document (artist)
    row_sums = numpy.ravel(X.sum(axis=1))
    average_length = row_sums.mean()
    length_norm = (1.0 - B) + B * row_sums / average_length

    # weight matrix rows by bm25
    X.data = X.data * (K1 + 1.0) / (K1 * length_norm[X.row] + X.data) * idf[X.col]
    return X


class TopRelated(object):
    def __init__(self, artist_factors):
        # fully normalize artist_factors, so can compare with only the dot product
        norms = numpy.linalg.norm(artist_factors, axis=-1)
        self.factors = artist_factors / norms[:, numpy.newaxis]

    def get_related(self, artistid, N=50):
        scores = self.factors.dot(self.factors[artistid])
        best = numpy.argpartition(scores, -N)[-N:]
        return sorted(zip(best, scores[best]), key=lambda x: -x[1])


class ApproximateTopRelated(object):
    def __init__(self, artist_factors, treecount=20):
        index = annoy.AnnoyIndex(artist_factors.shape[1], 'angular')
        for i, row in enumerate(artist_factors):
            index.add_item(i, row)
        index.build(treecount)
        self.index = index

    def get_related(self, artistid, N=50):
        neighbours = self.index.get_nns_by_item(artistid, N)
        return sorted(((other, 1 - self.index.get_distance(artistid, other))
                      for other in neighbours), key=lambda x: -x[1])


def calculate_similar_artists(input_filename, output_filename,
                              factors=50, regularization=0.01,
                              iterations=15,
                              exact=False, trees=20,
                              use_native=True,
                              dtype=numpy.float64):

    # Calculo de clientes recomendados ---

    print("Calculating similar clients. This might take a while")
    print("reading data from %s", input_filename)
    start = time.time()
    df, transfers = read_data(input_filename, inv=False)
    print("read data file in %s", time.time() - start)

    print("weighting matrix by bm25")
    weighted = bm25_weight(transfers)

    print("calculating factors")
    start = time.time()
    artist_factors, user_factors = alternating_least_squares(weighted,
                                                             factors=factors,
                                                             regularization=regularization,
                                                             iterations=iterations,
                                                             use_native=use_native,
                                                             dtype=dtype)
    print("calculated factors in %s", time.time() - start)

    # write out artists by popularity
    print("calculating top clients")
    user_count = df.groupby('artist').size()
    artists = dict(enumerate(df['artist'].cat.categories))
    to_generate = sorted(list(artists), key=lambda x: -user_count[x])

    if exact:
        calc = TopRelated(artist_factors)
    else:
        calc = ApproximateTopRelated(artist_factors, trees)
    list_of_recommended_clients = []
    print("writing top related to %s", output_filename)
    for i, artistid in enumerate(to_generate):
        print(i)
        artist = artists[artistid]
        for other, score in calc.get_related(artistid):
            if (artist!=artists[other]):
                recommendedClients = RecommendedClients()
                recommendedClients.empresa = Empresa.objects.get(fiscal_id=artist)
                recommendedClients.clientes_recomendados = Empresa.objects.get(fiscal_id=artists[other])
                recommendedClients.similarity = score
                list_of_recommended_clients.append(recommendedClients)
    
    print('All clients recommendations have been stored in a list, saving them to DB')
    RecommendedClients.objects.bulk_create(list_of_recommended_clients, batch_size=20000)

    # Calculo de proveedores recomendados ---

    print("Calculating similar providers. This might take a while")
    print("reading data from %s", input_filename)
    start = time.time()
    df, transfers = read_data(input_filename, inv=True)
    print("read data file in %s", time.time() - start)

    print("weighting matrix by bm25")
    weighted = bm25_weight(transfers)

    print("calculating factors")
    start = time.time()
    artist_factors, user_factors = alternating_least_squares(weighted,
                                                             factors=factors,
                                                             regularization=regularization,
                                                             iterations=iterations,
                                                             use_native=use_native,
                                                             dtype=dtype)
    print("calculated factors in %s", time.time() - start)

    # write out artists by popularity
    print("calculating top providers")
    user_count = df.groupby('artist').size()
    artists = dict(enumerate(df['artist'].cat.categories))
    to_generate = sorted(list(artists), key=lambda x: -user_count[x])

    if exact:
        calc = TopRelated(artist_factors)
    else:
        calc = ApproximateTopRelated(artist_factors, trees)

    list_of_recommended_providers = []
    print("writing top related to %s", output_filename)
    for i, artistid in enumerate(to_generate):
        print(i)
        artist = artists[artistid]
        for other, score in calc.get_related(artistid):
            if (artist!=artists[other]):
                recommendedProviders = RecommendedProviders()
                recommendedProviders.empresa = Empresa.objects.get(fiscal_id=artist)
                recommendedProviders.clientes_recomendados = Empresa.objects.get(fiscal_id=artists[other])
                recommendedProviders.similarity = score
                list_of_recommended_providers.append(recommendedProviders)
    
    print('All providers recommendations have been stored in a list, saving them to DB')
    RecommendedProviders.objects.bulk_create(list_of_recommended_providers, batch_size=20000)