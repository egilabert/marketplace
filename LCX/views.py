#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
import json
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

def HomeView(request):
	return render(request, "lcx_home.html", {})

def SegmentosView(request):
	eje1 = ["MAT postivo", "MAT negativo"]
	d1 = [0.25,0.75]
	eje2 = ["Trasformable", "No Trasformable"]
	d2 = [0.90,0.10]
	eje3 = ["Deuda inferior al VES - LTV Bajo", "Carga previa de terceros", "2a hipoteca"]
	d3 = [0.20,0.40,0.40]
	eje4 = ["LTV > 120%", "Importe de deuda > 600k€", "Maturity > 40%", "Resto"]
	d4 = [0.40,0.10,0.10,0.40]
	eje5 = ["Con voluntad de pago", "Sin voluntad de pago"]
	d5 = [0.60,0.40]
	eje6 = ["Con capacidad de pago", "Sin capacidad de pago"]
	d6 = [0.50,0.50]
	nodes_list = [{"name": "Cobro", "id": "NoMAT_score"}]
	nodes_list.append({"name": "Refinanciación", "id": "NoMAT_score"})
	nodes_list.append({"name": "Refinanciación agresiva", "id": "NoMAT_score"})
	nodes_list.append({"name": "Mandato de venta", "id": "NoMAT_score"})
	nodes_list.append({"name": "Dación", "id": "NoMAT_score"})
	nodes_list.append({"name": "Demanda", "id": "NoMAT_score"})

	nodes_list.append({"name": "Entrada en impago", "id": "final_score"})
	links_list = list()

	for i, n in enumerate(eje1):
		if n == eje1[1]:
			nodes_list.append({'name': n, "id": "NoMAT_score"})
			links_list.append({ "source": nodes_list.index({'name': "Entrada en impago", "id": "final_score"}), "value": d1[i], "target": len(nodes_list)-1 })
			for j, t in enumerate(eje2):
				nodes_list.append({'name': t, "id": "NoMAT_score"})
				links_list.append({ "source": nodes_list.index({'name': n, "id": "NoMAT_score"}), "value": d1[i]*d2[j], "target": len(nodes_list)-1 })
				for k, nt in enumerate(eje3):
					if j==1:
						nodes_list.append({'name': nt, "id": "NoMAT_score"})
						links_list.append({ "source": nodes_list.index({'name': "No Trasformable", "id": "NoMAT_score"}), "value": d1[i]*d2[j]*d3[k], "target": len(nodes_list)-1 })
						for p in range(0,1):
							links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d3[k]*0.85, "target": nodes_list.index({"name": "Refinanciación agresiva", "id": "NoMAT_score"}) })
							links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d3[k]*0.15, "target": nodes_list.index({"name": "Mandato de venta", "id": "NoMAT_score"}) })
				for k, nt in enumerate(eje4):
					if j==0:
						nodes_list.append({'name': nt, "id": "NoMAT_score"})
						links_list.append({ "source": nodes_list.index({'name': "Trasformable", "id": "NoMAT_score"}), "value": d1[i]*d2[j]*d4[k], "target": len(nodes_list)-1 })
						for s, v in enumerate(eje5):
							if k!=2:
								nodes_list.append({'name': v+' ('+str(k)+')', "id": "NoMAT_score"})
								links_list.append({ "source": nodes_list.index({'name': eje4[k], "id": "NoMAT_score"}), "value": d1[i]*d2[j]*d4[k]*d5[s], "target": len(nodes_list)-1 })
								for l, c in enumerate(eje6):
									if s==0:
										nodes_list.append({'name': c, "id": "NoMAT_score"})
										links_list.append({ "source": nodes_list.index({'name': eje5[s]+' ('+str(k)+')', "id": "NoMAT_score"}), "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l], "target": len(nodes_list)-1 })
										if l==0:
											links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.3, "target": nodes_list.index({"name": "Cobro", "id": "NoMAT_score"}) })
											links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.7, "target": nodes_list.index({"name": "Refinanciación", "id": "NoMAT_score"}) })
										else:
											links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.9, "target": nodes_list.index({"name": "Demanda", "id": "NoMAT_score"}) })
											links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.1, "target": nodes_list.index({"name": "Dación", "id": "NoMAT_score"}) })
									else:
										links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.9, "target": nodes_list.index({"name": "Demanda", "id": "NoMAT_score"}) })
										links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.1, "target": nodes_list.index({"name": "Dación", "id": "NoMAT_score"}) })
							else:
								for l, c in enumerate(eje6):
									if s==0:
										nodes_list.append({'name': c, "id": "NoMAT_score"})
										links_list.append({ "source": nodes_list.index({'name': eje4[k], "id": "NoMAT_score"}), "value": d1[i]*d2[j]*d4[k]*d6[l], "target": len(nodes_list)-1 })
										if l==0:
											links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.3, "target": nodes_list.index({"name": "Cobro", "id": "NoMAT_score"}) })
											links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.7, "target": nodes_list.index({"name": "Refinanciación", "id": "NoMAT_score"}) })
										else:
											links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.9, "target": nodes_list.index({"name": "Demanda", "id": "NoMAT_score"}) })
											links_list.append({ "source": len(nodes_list)-1, "value": d1[i]*d2[j]*d4[k]*d5[s]*d6[l]*0.1, "target": nodes_list.index({"name": "Dación", "id": "NoMAT_score"}) })
											
		else:
			nodes_list.append({'name': eje1[i], "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': "Entrada en impago", "id": "final_score"}), "value": d1[i], "target": len(nodes_list)-1 })

			nodes_list.append({'name': "Gran número de ciclos de impago", "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': eje1[i], "id": "MAT_score"}), "value": d1[i]*0.8, "target": len(nodes_list)-1 })

			nodes_list.append({'name': "_", "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': "Gran número de ciclos de impago", "id": "MAT_score"}), "value": d1[i]*0.8, "target": len(nodes_list)-1 })

			nodes_list.append({'name': "_a", "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': "_", "id": "MAT_score"}), "value": d1[i]*0.8, "target": len(nodes_list)-1 })

			nodes_list.append({'name': "_b", "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': "_a", "id": "MAT_score"}), "value": d1[i]*0.8, "target": len(nodes_list)-1 })

			nodes_list.append({'name': "Primer o pocos ciclos de impago", "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': eje1[i], "id": "MAT_score"}), "value": d1[i]*0.2, "target": len(nodes_list)-1 })

			nodes_list.append({'name': "_2", "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': "Primer o pocos ciclos de impago", "id": "MAT_score"}), "value": d1[i]*0.2, "target": len(nodes_list)-1 })

			nodes_list.append({'name': "_3", "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': "_2", "id": "MAT_score"}), "value": d1[i]*0.2, "target": len(nodes_list)-1 })

			nodes_list.append({'name': "_4", "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': "_3", "id": "MAT_score"}), "value": d1[i]*0.2, "target": len(nodes_list)-1 })

			nodes_list.append({'name': "Autcobro - No gestión", "id": "MAT_score"})
			links_list.append({ "source": nodes_list.index({'name': "_b", "id": "MAT_score"}), "value": d1[i]*0.8, "target": len(nodes_list)-1 })

			links_list.append({ "source": nodes_list.index({'name': "_4", "id": "MAT_score"}), "value": d1[i]*0.2, "target": nodes_list.index({"name": "Cobro", "id": "NoMAT_score"}) })

	segmentacion = {"nodes": nodes_list, "links": links_list}
	print(segmentacion)
	print(settings.DATA_FOLDER+'segmentacion3.json')

	with open(settings.DATA_FOLDER+'segmentacion3.json', 'w') as fp:
		json.dump(segmentacion, fp, indent=4, sort_keys=True, cls=DjangoJSONEncoder)

	return render(request, "lcx_segmentos.html", {})