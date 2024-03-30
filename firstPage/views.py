from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
import numpy as np

# informações dos paises
df3 = pd.read_json(
    'https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')


def index(request):
    # confirmedGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8',na_values=None)
    # Posgrad = pd.read_csv('datasets/Perfil_Posgrad_26062023.csv')
    Posgrad = pd.DataFrame()

    # uniqueCountryNames = pd.unique(confirmedGlobal['Country/Region'])
    # contryNames, countsVal, logVals, overallCount, dataForMapGraph, maxVal = getBarData(
    #    confirmedGlobal, uniqueCountryNames)  # Dado mapa
    # dataForheatMap, dateCat = getHeatMapData(
    #    confirmedGlobal, contryNames)  # Dado mapa
    # datasetForLine, axisvalues = getLinebarGroupData(confirmedGlobal)
    # variavel que responde ao index.
    # context = {'dateCat': dateCat, 'dataForheatMap': dataForheatMap, 'maxVal': maxVal, 'dataForMapGraph': dataForMapGraph, 'axisvalues': axisvalues, 'datasetForLine': datasetForLine,
    #           'uniqueCountryNames': uniqueCountryNames, 'contryNames': contryNames, 'countsVal': countsVal, 'logVals': logVals, 'overallCount': overallCount}
    context = {
        'Posgrad': Posgrad
    }

    return render(request, 'index.html', context)


def getBarData(confirmedGlobal, uniqueCountryNames):
    df2 = confirmedGlobal[list(
        confirmedGlobal.columns[1:2])+list([confirmedGlobal.columns[-2]])]
    df2.columns = ['Country/Region', 'values']
    df2 = df2.sort_values(by='values', ascending=False)
    contryNames = list(df2['Country/Region'].values)
    countsVal = list(df2['values'].values)
    maxVal = max(countsVal)
    overallCount = sum(countsVal)
    logVals = list(np.log(ind) if ind != 0 else 0 for ind in countsVal)
    dataForMapGraph = getDataforMap(uniqueCountryNames, df2)
    # dictVal=[]
    # for i in range(df2.shape[0]):
    #     dictVal.append(dict(df2.ix[i]))
    return (contryNames, countsVal, logVals, overallCount, dataForMapGraph, maxVal)


def getLinebarGroupData(confirmedGlobal):
    colNames = confirmedGlobal.columns[4:-1]  # salvando os dias
    top10 = confirmedGlobal[['Country/Region', confirmedGlobal.columns[-2]]].groupby(
        'Country/Region').sum().sort_values(by=str(confirmedGlobal.columns[-2]), ascending=False)
    # exibindo a evolução da covid nos atuais 10 país com mais casos
    top10 = top10.iloc[0:10, :]
    # colNames=confirmedGlobal.columns[4:-1]
    top10 = top10.reset_index()
    top10Names = top10['Country/Region']
    datasetsForLine = []
    for i in top10Names:
        temp = {}  # inicializando o dicionário
        temp['label'] = i  # salvando o país
        temp['fill'] = 'false'
        temp['borderWidth'] = 2
        cores = list(np.random.choice(range(256), size=3))  # gerando as cores
        cores.append(0.85)  # add o parâmetro de transparencia
        cores = tuple(cores)  # transformando a lista em tuple
        temp['borderColor'] = 'rgba'+str(cores)
        temp['color'] = 'rgba'+str(cores)
        temp['backgroundColor'] = 'rgba'+str(cores)
        temp['data'] = confirmedGlobal[confirmedGlobal['Country/Region']
                                       == i][colNames].sum().values.tolist()
        datasetsForLine.append(temp)
    return datasetsForLine, list(colNames)  # list(range(len(colNames)))

# dados do mapa


def getDataforMap(uniqueCOuntryName, df2):
    dataForMap = []
    for i in uniqueCOuntryName:
        try:
            tempdf = df3[df3['name'] == i]
            temp = {}
            temp["code3"] = list(tempdf['code3'].values)[0]
            temp["name"] = i
            temp["value"] = df2[df2['Country/Region'] == i]['values'].sum()
            temp["code"] = list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    print(len(dataForMap))
    return dataForMap


def getHeatMapData(confirmedGlobal, contryNames):
    df3 = confirmedGlobal[list(
        confirmedGlobal.columns[1:2])+list(list(confirmedGlobal.columns.values)[-6:-1])]
    dataForheatMap = []
    for i in contryNames:
        try:
            tempdf = df3[df3['Country/Region'] == i]
            temp = {}
            temp["name"] = i
            temp["data"] = [{'x': j, 'y': k} for j, k in zip(
                tempdf[tempdf.columns[1:]].sum().index, tempdf[tempdf.columns[1:]].sum().values)]
            dataForheatMap.append(temp)
        except:
            pass
    dateCat = list(list(confirmedGlobal.columns.values)[-6:-1])
    return dataForheatMap, dateCat


@csrf_exempt
def drillDownACountry(request):
    if request.method == "POST":
        print(request.POST.dict())
        countryName = request.POST.get('countryName')
        confirmedGlobal = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', encoding='utf-8', na_values=None)
        countryDataSpe = pd.DataFrame(
            confirmedGlobal[confirmedGlobal['Country/Region'] == countryName][confirmedGlobal.columns[4:-1]].sum()).reset_index()
        countryDataSpe.columns = ['country', 'values']
        countryDataSpe['lagVal'] = countryDataSpe['values'].shift(1).fillna(0)
        countryDataSpe['incrementVal'] = countryDataSpe['values'] - \
            countryDataSpe['lagVal']
        countryDataSpe['rollingMean'] = countryDataSpe['incrementVal'].rolling(
            window=4).mean()
        countryDataSpe = countryDataSpe.fillna(0)
        datasetsForLine = [{'yAxisID': 'y-axis-1', 'label': 'Número acumulado de casos', 'data': countryDataSpe['values'].values.tolist(), 'borderColor': '#03a9fc', 'backgroundColor': '#03a9fc', 'fill': 'false'},
                           {'yAxisID': 'y-axis-2', 'label': 'Média móvel de 4 dias', 'data': countryDataSpe['rollingMean'].values.tolist(), 'borderColor': '#fc5203', 'backgroundColor': '#fc5203', 'fill': 'false'}]
        axisvalues = countryDataSpe['country'].tolist()
        uniqueCountryNames = pd.unique(confirmedGlobal['Country/Region'])
        contryNames, countsVal, logVals, overallCount, dataForMapGraph, maxVal = getBarData(
            confirmedGlobal, uniqueCountryNames)
        dataForheatMap, dateCat = getHeatMapData(confirmedGlobal, contryNames)

        context = context = {"countryName": countryName, 'axisvalues': axisvalues, 'datasetsForLine': datasetsForLine, 'dateCat': dateCat, 'dataForheatMap': dataForheatMap, 'maxVal': maxVal,
                             'dataForMapGraph': dataForMapGraph, 'uniqueCountryNames': uniqueCountryNames, 'contryNames': contryNames, 'countsVal': countsVal, 'logVals': logVals, 'overallCount': overallCount}

        return render(request, 'index2.html', context)
