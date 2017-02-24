# http://blog.untrod.com/2016/06/simple-similar-products-recommendation-engine-in-python.html
# http://blog.untrod.com/2017/02/recommendation-engine-for-trending-products-in-python.md.html

import time
import numpy
import logging
import pandas as pd
import category_encoders as ce 
from scipy.sparse import coo_matrix
from django.conf import settings
from .models import Empresa, RecommendedClients, RecommendedProviders
from sklearn.metrics.pairwise import linear_kernel

def create_label_encoding(data, encode='label', categorical_features=[], verbose=0):
    #Function that encodes the string values to numerical values.
    def label_encode(data, column_names):
        #Encoding the data, encoding the string values into numerical values.
        encoder = ce.OrdinalEncoder(column_names)
        data_transformed = encoder.fit_transform(data)
        return(data_transformed)

    def binary_encode(data, column_names):
        #Encoding the data, encoding the string values into numerical values, using binary method.
        encoder = ce.BinaryEncoder(column_names)
        data_transformed = encoder.fit_transform(data)
        return(data_transformed)

    def hashing_encode(data, column_names):
        #Encoding the data, encoding the string values into numerical values, using binary method.
        encoder = ce.HashingEncoder(column_names, n_components = 128)
        data_transformed = encoder.fit_transform(data)
        return(data_transformed)

    def one_hot(data, column_names):
        #Encoding the data, encoding the string values into numerical values, using binary method.
        encoder = ce.OneHotEncoder(column_names)
        data_transformed = encoder.fit_transform(data)
        return(data_transformed)

    def backward_difference_encode(data, column_names):
        #Encoding the data, encoding the string values into numerical values, using binary method.
        encoder = ce.BackwardDifferenceEncoder(column_names)
        data_transformed = encoder.fit_transform(data)
        return(data_transformed)

    def helmert_encode(data, column_names):
        #Encoding the data, encoding the string values into numerical values, using binary method.
        encoder = ce.HelmertEncoder(column_names)
        data_transformed = encoder.fit_transform(data)
        return(data_transformed)

    def sum_encode(data, column_names):
        #Encoding the data, encoding the string values into numerical values, using binary method.
        encoder = ce.SumEncoder(column_names)
        data_transformed = encoder.fit_transform(data)
        return(data_transformed)

    def polynomial_encode(data, column_names):
        #Encoding the data, encoding the string values into numerical values, using binary method.
        encoder = ce.PolynomialEncoder(column_names)
        data_transformed = encoder.fit_transform(data)
        return(data_transformed)

    if(encode != None):
        #Data will be encoded to the form that the user enters
        encoding = {'binary':binary_encode,'hashing':hashing_encode,'backward_difference'
                   :backward_difference_encode,'helmert':helmert_encode,'polynomial':
                   polynomial_encode,'sum':sum_encode,'label':label_encode, 'one_hot':one_hot}
        if verbose != 0:
            print ("Encoding categorical features...")
        #Once the above encoding techniques has been selected by the user, the appropriate encoding function is called
        #encoder = ce.OrdinalEncoder(categorical_features)
        data_transformed = encoding[encode](data, categorical_features) #data_transformed = encoder.fit_transform(data)
        return(data_transformed)

    return data

def create_dummies(data, verbose=0, categorical_features=[]):
    if verbose != 0:
        print ("Handling categorical features...")
    for feature in categorical_features: # Encode categorical features
		if feature in data.columns.values:
			print(feature)
			try:
				data = pd.concat([data, pd.get_dummies(data[feature]).rename(columns=lambda x: feature + '_' + x.encode('latin-1'))], axis=1)
				data = data.drop(feature, axis=1)
			except:
				data = pd.concat([data, pd.get_dummies(data[feature]).rename(columns=lambda x: feature[0] + '_' + str(x))], axis=1)
				data = data.drop(feature, axis=1)
    return data

def get_features_by_type(data, verbose=0):
    #Getting numerical and categorical variables
    numerical_features = data.select_dtypes(include=["float","int","bool"]).columns.values
    categorical_features=data.select_dtypes(include=["object"]).columns.values
    if verbose !=0:
        print'============================'
        print('Numerical_features:')
        print(numerical_features)
        print'============================'
        print("Categorical_features")
        print(categorical_features)
        print'============================'
    return numerical_features,categorical_features

def read_data(empresas):
	""" Reads in the last.fm dataset, and returns a tuple of a pandas dataframe
	and a sparse matrix of artist/user/playcount """
	# read in triples of user/artist/playcount from the input dataset
	empresas = empresas[['FECHA_NACIMIENTO', 'Sector', 'CNAE', 'CNAE_2', 'DE_CORTA_TERRITORIAL_GEST', 'NOMBRE_REGIONAL_GEST']]
	for index, row in empresas.iterrows():
		row['FECHA_NACIMIENTO'] = str(row['FECHA_NACIMIENTO'])[6:10]
	return empresas

def content_based_similarity():
	link = settings.DATA_FOLDER+'empresas_ok.csv'
	empresas = pd.read_csv(link, sep=';', decimal=',', encoding='latin1') # read empresas data
	print(empresas.columns.values)
	data = read_data(empresas)
	numerical_features, categorical_features = get_features_by_type(data)
	data = create_label_encoding(data, categorical_features=categorical_features, encode='one_hot', verbose=1)
	cosine_similarities = linear_kernel(data, data)
	for idx, row in data.iterrows():
		print(empresas['NOMBRE'][idx])
		print('============================')
		similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
		print(similar_indices)
		similar_items = [(cosine_similarities[idx][i], empresas['NOMBRE'][i]) for i in similar_indices]
		print(similar_items)
