from django.shortcuts import render
import pandas as pd

# Exemplo de DataFrame (pode ser substituído pelos seus dados reais)
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'Gender': ['Female', 'Male', 'Male'],
    'City': ['City1', 'City2', 'City1'],
    'Education': ['High School', 'College', 'College']
}
df = pd.DataFrame(data)


def filter_data(request):
    if request.method == 'GET':
        # Obtém os valores dos filtros enviados pela solicitação GET
        gender_filter = request.GET.get('gender', 'all')
        city_filter = request.GET.get('city', 'all')
        education_filter = request.GET.get('education', 'all')

        # Aplica os filtros ao DataFrame
        filtered_df = df
        if gender_filter != 'all':
            filtered_df = filtered_df[filtered_df['Gender'] == gender_filter]
        if city_filter != 'all':
            filtered_df = filtered_df[filtered_df['City'] == city_filter]
        if education_filter != 'all':
            filtered_df = filtered_df[filtered_df['Education']
                                      == education_filter]

        # Renderiza o template com o DataFrame filtrado
        return render(request, 'teste_filtro_pd.html', {'df': filtered_df})
    else:
        # Se a solicitação não for GET, redirecione para a mesma página
        return render(request, 'teste_filtro_pd.html', {'df': df})
