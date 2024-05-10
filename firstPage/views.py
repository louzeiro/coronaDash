from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import MyForm


import pandas as pd
import numpy as np

# informações dos paises
df3 = pd.read_json(
    'https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')

Posgrad = pd.read_csv('datasets/Perfil_Posgrad_26062023.csv')


def bkp_index(request):
    # Posgrad = pd.read_csv('datasets/Perfil_Posgrad_26062023.csv')

    unidades = Posgrad['unidade'].unique()
    lista_campus = Posgrad['campus'].unique()

    df = Posgrad

    if request.method == 'GET':
        unidade_filter = request.GET.get('unidade', 'all')
        ano_filter = request.GET.get('ano', 'all')

        filtered_df = Posgrad
        if unidade_filter != 'all':
            filtered_df = filtered_df[filtered_df['unidade'] == unidade_filter]

        if ano_filter != 'all':
            filtered_df = filtered_df[filtered_df['Ano'] == ano_filter]

        df = filtered_df

    # chamar as funções para gerar os gráficos

    teste = df['unidade'].unique()

    context = {
        'Posgrad': Posgrad, 'unidades': unidades, 'lista_campus': lista_campus,
        'df': df, 'teste': teste,
    }

    return render(request, 'index.html', context)

    # Renderiza o template com o DataFrame filtrado
    #    return render(request, 'index.html', {'df': filtered_df})
    # else:
    #    # Se a solicitação não for GET, redirecione para a mesma página
    #    return render(request, 'index.html', {'df': Posgrad})

    # contryNames, countsVal, logVals, overallCount, dataForMapGraph, maxVal = getBarData(
    #    confirmedGlobal, uniqueCountryNames)  # Dado mapa
    # dataForheatMap, dateCat = getHeatMapData(
    #    confirmedGlobal, contryNames)  # Dado mapa
    # datasetForLine, axisvalues = getLinebarGroupData(confirmedGlobal)
    # variavel que responde ao index.
    # context = {'dateCat': dateCat, 'dataForheatMap': dataForheatMap, 'maxVal': maxVal, 'dataForMapGraph': dataForMapGraph, 'axisvalues': axisvalues, 'datasetForLine': datasetForLine,
    #           'uniqueCountryNames': uniqueCountryNames, 'contryNames': contryNames, 'countsVal': countsVal, 'logVals': logVals, 'overallCount': overallCount}
    # context = {
    #    'Posgrad': Posgrad, 'unidades': unidades, 'anos': anos,
    # }

    # return render(request, 'index.html', context)


def index(request):
    df = Posgrad

    # melhorar, para exibir apenas as unidades do campus
    lista_campus = Posgrad['campus'].unique()

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            print('aaaaaaaqui -  recebeu forms')
            var_campus = request.POST.get('campus')

            if (var_campus != 'All'):  # or var_campus != 'all'):
                print('aaaaaaaqui -  recebeu campus')
                df = Posgrad[Posgrad['campus'] == var_campus]

            nome_campus, total_sim, total_geral_sim, total_nao, total_geral_nao, total_geral = contemplados_campus(
                df)
            tota_inscritos = sum(total_geral)
            total_sim_inscrito = sum(total_sim)
            total_nao_inscrito = sum(total_nao)

            campus_nome_raca, total_amarela, total_Branca, total_Indigena, total_nao_informada, total_Parda, total_Preta_negra = contemplados_raca_cor_por_campus(
                df)
            contemplado_sexo_campos, contemplado_sexo_F, contemplado_sexo_M = contemplados_sexo(
                df)
            menos_0_5_sm, entre_0_5_e_1_sm, entre_1_e_1_5_sm, acima_1_5 = contemplado_renda(
                df)
            geral_cor_raca, total_geral_cor_raca = contemplados_raca_cor_geral(
                df)

            context = {
                'form': form,
                'Posgrad': Posgrad,
                'lista_campus': lista_campus,
                'nome_campus': nome_campus,
                'total_sim': total_sim,
                'total_geral_sim': total_geral_sim,
                'total_nao': total_nao,
                'total_geral_nao': total_geral_nao,
                'campus_nome_raca': campus_nome_raca,
                'total_amarela': total_amarela,
                'total_Branca': total_Branca,
                'total_Indigena': total_Indigena,
                'total_nao_informada': total_nao_informada,
                'total_Parda': total_Parda,
                'total_Preta_negra': total_Preta_negra,
                'contemplado_sexo_campos': contemplado_sexo_campos,
                'contemplado_sexo_F': contemplado_sexo_F,
                'contemplado_sexo_M': contemplado_sexo_M,
                'menos_0_5_sm': menos_0_5_sm,
                'entre_0_5_e_1_sm': entre_0_5_e_1_sm,
                'entre_1_e_1_5_sm': entre_1_e_1_5_sm,
                'acima_1_5': acima_1_5,
                'geral_cor_raca': geral_cor_raca,
                'total_geral_cor_raca': total_geral_cor_raca,
                'total_geral': total_geral,
                'tota_inscritos': tota_inscritos,
                'total_sim_inscrito': total_sim_inscrito,
                'total_nao_inscrito': total_nao_inscrito
            }
            return render(request, 'index.html', context=context)

        else:
            print('Flaaaaa')

            nome_campus, total_sim, total_geral_sim, total_nao, total_geral_nao, total_geral = contemplados_campus(
                df)

            tota_inscritos = sum(total_geral)

            campus_nome_raca, total_amarela, total_Branca, total_Indigena, total_nao_informada, total_Parda, total_Preta_negra = contemplados_raca_cor_por_campus(
                df)
            contemplado_sexo_campos, contemplado_sexo_F, contemplado_sexo_M = contemplados_sexo(
                df)

            menos_0_5_sm, entre_0_5_e_1_sm, entre_1_e_1_5_sm, acima_1_5 = contemplado_renda(
                df)

            geral_cor_raca, total_geral_cor_raca = contemplados_raca_cor_geral(
                df)

            context = {
                'form': form,
                'Posgrad': Posgrad,
                'lista_campus': lista_campus,
                'nome_campus': nome_campus,
                'total_sim': total_sim,
                'total_geral_sim': total_geral_sim,
                'total_nao': total_nao,
                'total_geral_nao': total_geral_nao,
                'campus_nome_raca': campus_nome_raca,
                'total_amarela': total_amarela,
                'total_Branca': total_Branca,
                'total_Indigena': total_Indigena,
                'total_nao_informada': total_nao_informada,
                'total_Parda': total_Parda,
                'total_Preta_negra': total_Preta_negra,
                'contemplado_sexo_campos': contemplado_sexo_campos,
                'contemplado_sexo_F': contemplado_sexo_F,
                'contemplado_sexo_M': contemplado_sexo_M,
                'menos_0_5_sm': menos_0_5_sm,
                'entre_0_5_e_1_sm': entre_0_5_e_1_sm,
                'entre_1_e_1_5_sm': entre_1_e_1_5_sm,
                'acima_1_5': acima_1_5,
                'geral_cor_raca': geral_cor_raca,
                'total_geral_cor_raca': total_geral_cor_raca,
                'total_geral': total_geral,
                'tota_inscritos': tota_inscritos,
                'total_sim_inscrito': total_sim_inscrito,
                'total_nao_inscrito': total_nao_inscrito
            }

            return render(request, 'index.html', context=context)

    else:
        form = MyForm()
        nome_campus, total_sim, total_geral_sim, total_nao, total_geral_nao, total_geral = contemplados_campus(
            df)
        tota_inscritos = sum(total_geral)

        campus_nome_raca, total_amarela, total_Branca, total_Indigena, total_nao_informada, total_Parda, total_Preta_negra = contemplados_raca_cor_por_campus(
            df)
        contemplado_sexo_campos, contemplado_sexo_F, contemplado_sexo_M = contemplados_sexo(
            df)

        menos_0_5_sm, entre_0_5_e_1_sm, entre_1_e_1_5_sm, acima_1_5 = contemplado_renda(
            df)

        geral_cor_raca, total_geral_cor_raca = contemplados_raca_cor_geral(
            df)

        context = {
            'form': form,
            'Posgrad': Posgrad,
            'lista_campus': lista_campus,
            'nome_campus': nome_campus,
            'total_sim': total_sim,
            'total_geral_sim': total_geral_sim,
            'total_nao': total_nao,
            'total_geral_nao': total_geral_nao,
            'campus_nome_raca': campus_nome_raca,
            'total_amarela': total_amarela,
            'total_Branca': total_Branca,
            'total_Indigena': total_Indigena,
            'total_nao_informada': total_nao_informada,
            'total_Parda': total_Parda,
            'total_Preta_negra': total_Preta_negra,
            'contemplado_sexo_campos': contemplado_sexo_campos,
            'contemplado_sexo_F': contemplado_sexo_F,
            'contemplado_sexo_M': contemplado_sexo_M,
            'menos_0_5_sm': menos_0_5_sm,
            'entre_0_5_e_1_sm': entre_0_5_e_1_sm,
            'entre_1_e_1_5_sm': entre_1_e_1_5_sm,
            'acima_1_5': acima_1_5,
            'geral_cor_raca': geral_cor_raca,
            'total_geral_cor_raca': total_geral_cor_raca,
            'total_geral': total_geral,
            'tota_inscritos': tota_inscritos,
            'total_sim_inscrito': total_sim_inscrito,
            'total_nao_inscrito': total_nao_inscrito

        }

        return render(request, 'index.html', context=context)


def contemplados_campus(df):
    if len(df['Campus'].unique()) > 1:

        data = round(pd.crosstab(
            df['Campus'], df['Contemplado'],
            margins='index', margins_name='Total'))
        data.sort_values(by='Total', inplace=True, ascending=False)
        total_geral = data['Total'].tolist()
        data.drop('Total', axis=0, inplace=True)  # linha
        data.drop('Total', axis=1, inplace=True)  # coluna
        total_geral_sim = data['Sim'].sum()
        total_geral_nao = data['Não'].sum()
        nome_campus = data.index.tolist()
        total_sim = data['Sim'].to_list()
        total_nao = data['Não'].to_list()

    else:
        data = df[['Campus', 'Contemplado']].value_counts().reset_index()
        total_geral = [sum(data['count'].tolist())]
        nome_campus = data.Campus.unique().tolist()
        total_sim = data.loc[data.Contemplado == 'Sim', 'count'].tolist()
        total_geral_sim = total_sim
        total_nao = data.loc[data.Contemplado == 'Não', 'count'].tolist()
        total_geral_nao = total_nao

    return (nome_campus, total_sim, total_geral_sim, total_nao,
            total_geral_nao, total_geral)


def contemplados_raca_cor_geral(df):
    geral_cor_raca = df['Raça / Cor'].value_counts().reset_index()[
        'Raça / Cor'].tolist()
    total_geral_cor_raca = df['Raça / Cor'].value_counts().reset_index()[
        'count'].tolist()

    return (geral_cor_raca, total_geral_cor_raca)


def contemplados_raca_cor_geral_(df):
    data = pd.crosstab(
        df['Campus'], df['Raça / Cor'])

    nome_raca_cor_geral = data.columns.tolist()

    if 'Amarela' in data.columns:
        total_amarela_geral = sum(data['Amarela'].tolist())
    else:
        total_amarela_geral = [0]

    if 'Indígena' in data.columns:
        total_Indigena_geral = sum(data['Indígena'].tolist())
    else:
        total_Indigena_geral = [0]

    if 'Parda' in data.columns:
        total_Parda_geral = sum(data['Parda'].tolist())
    else:
        total_Parda_geral = [0]

    if 'Preta / negra' in data.columns:
        total_Preta_negra_geral = sum(data['Preta / negra'].tolist())
    else:
        total_Preta_negra_geral = [0]

    total_Branca_geral = sum(data['Branca'].tolist())
    total_nao_informada_geral = sum(data['Não informada'].tolist())
    print(data)

    return (nome_raca_cor_geral, total_amarela_geral, total_Branca_geral, total_Indigena_geral,
            total_nao_informada_geral, total_Parda_geral, total_Preta_negra_geral)


def contemplados_raca_cor_por_campus(df):
    data = round(pd.crosstab(
        df['Campus'], df['Raça / Cor'], normalize='index') * 100)

    campus_nome = data.index.tolist()

    if 'Amarela' in data.columns:
        total_amarela = data['Amarela'].tolist()
    else:
        total_amarela = [0]

    if 'Indígena' in data.columns:
        total_Indigena = data['Indígena'].tolist()
    else:
        total_Indigena = [0]

    if 'Parda' in data.columns:
        total_Parda = data['Parda'].tolist()
    else:
        total_Parda = [0]

    if 'Preta / negra' in data.columns:
        total_Preta_negra = data['Preta / negra'].tolist()
    else:
        total_Preta_negra = [0]

    total_Branca = data['Branca'].tolist()
    total_nao_informada = data['Não informada'].tolist()

    return (campus_nome, total_amarela, total_Branca, total_Indigena,
            total_nao_informada, total_Parda, total_Preta_negra)


def contemplados_sexo(df):

    data = round((
        pd.crosstab(df['Campus'], df['Sexo'], normalize='index')*100)).reset_index()
    contemplado_sexo_campos = data['Campus'].tolist()
    contemplado_sexo_F = data['F'].tolist()
    contemplado_sexo_M = data['M'].tolist()

    return (contemplado_sexo_campos, contemplado_sexo_F, contemplado_sexo_M)


def contemplado_renda(df):
    menos_0_5_sm = 1
    entre_0_5_e_1_sm = 1
    entre_1_e_1_5_sm = 1
    acima_1_5 = 1

    return (menos_0_5_sm, entre_0_5_e_1_sm, entre_1_e_1_5_sm, acima_1_5)


def contemplado_renda_(df):
    df['Renda per capita'] = pd.to_numeric(
        df['Renda per capita'], errors='coerce')
    df['Renda per capita por salario minimo'] = round(
        df['Renda per capita']/1412, 1)

    menos_0_5_sm = df[df['Renda per capita por salario minimo']
                      < 0.5]['Renda per capita por salario minimo'].count()
    entre_0_5_e_1_sm = df.loc[(df['Renda per capita por salario minimo'] >= 0.5)
                              & (df['Renda per capita por salario minimo'] < 1)
                              ]['Renda per capita por salario minimo'].count()
    entre_1_e_1_5_sm = df.loc[(df['Renda per capita por salario minimo'] >= 1.0)
                              & (df['Renda per capita por salario minimo'] < 1.5)
                              ]['Renda per capita por salario minimo'].count()
    acima_1_5 = df.loc[(df['Renda per capita por salario minimo'] >= 1.5)
                       ]['Renda per capita por salario minimo'].count()
    return (menos_0_5_sm, entre_0_5_e_1_sm, entre_1_e_1_5_sm, acima_1_5)


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
