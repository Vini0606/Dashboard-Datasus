import streamlit as st
import pandas as pd
import plotly.express as px

theme={
        "primaryColor": "#1f77b4",
        "backgroundColor": "#f0f0f5",
        "secondaryBackgroundColor": "#FFFFFF",
        "textColor": "#333333",
        "font": "sans serif"
    }

st.set_page_config(page_title="dataiesb", page_icon="👨‍🎓", layout="wide")

# Bases de Dados
qtd_datasus = pd.read_csv("qtd_datasus_pop.csv", sep=',')

qtd_datasus['01 Ações de promoção e prevenção em saúde'] = qtd_datasus['01 Ações de promoção e prevenção em saúde'].str.replace('-', '0').fillna(0).astype(int)
qtd_datasus['02 Procedimentos com finalidade diagnóstica'] = qtd_datasus['02 Procedimentos com finalidade diagnóstica'].str.replace('-', '0').fillna(0).astype(int)
qtd_datasus['03 Procedimentos clínicos'] = qtd_datasus['03 Procedimentos clínicos'].str.replace('-', '0').fillna(0).astype(int)
qtd_datasus['04 Procedimentos cirúrgicos'] = qtd_datasus['04 Procedimentos cirúrgicos'].str.replace('-', '0').astype(float).fillna(0).astype(int)
qtd_datasus['05 Transplantes de orgãos, tecidos e células'] = qtd_datasus['05 Transplantes de orgãos, tecidos e células'].str.replace('-', '0').astype(float).fillna(0).astype(int)
qtd_datasus['06 Medicamentos'] = qtd_datasus['06 Medicamentos'].str.replace('-', '0').astype(float).fillna(0).astype(int)
qtd_datasus['07 Órteses, próteses e materiais especiais'] = qtd_datasus['07 Órteses, próteses e materiais especiais'].str.replace('-', '0').astype(float).fillna(0).astype(int)
qtd_datasus['08 Ações complementares da atenção à saúde'] = qtd_datasus['08 Ações complementares da atenção à saúde'].str.replace('-', '0').astype(float).fillna(0).astype(int)
qtd_datasus['Total'] = qtd_datasus['Total'].str.replace('-', '0').astype(float).fillna(0).astype(int)

# Entrada de Dados
municipios = qtd_datasus["Nome_Município"].unique()
municipio = st.sidebar.selectbox("Municípios", ["Todos"] + list(municipios))
uf = st.sidebar.selectbox("Unidades da Federação", ["Todos"] + list(qtd_datasus["Nome_UF"].unique()))

# Filter based on municipio and uf
if municipio == "Todos" and uf == "Todos":
    df_filtered = qtd_datasus
elif municipio != "Todos" and uf != "Todos":
    df_filtered = qtd_datasus[(qtd_datasus["Nome_Município"] == municipio) & (qtd_datasus["Nome_UF"] == uf)]
elif municipio != "Todos":
    df_filtered = qtd_datasus[qtd_datasus["Nome_Município"] == municipio]
elif uf != "Todos":
    df_filtered = qtd_datasus[qtd_datasus["Nome_UF"] == uf]
else:
    df_filtered = qtd_datasus

# Radio buttons for nota and procedimento
captions = ['01 Ações de promoção e prevenção em saúde',
            '02 Procedimentos com finalidade diagnóstica',
            '03 Procedimentos clínicos', '04 Procedimentos cirúrgicos',
            '05 Transplantes de orgãos, tecidos e células', '06 Medicamentos',
            '07 Órteses, próteses e materiais especiais',
            '08 Ações complementares da atenção à saúde', 'Total']

procedimento = st.sidebar.radio("Procedimentos", captions, captions=captions)

# Saída de Dados
html_code = f"""
<div style="display: flex; justify-content: center; align-items: flex-start; height: 10vh;">
    <h2>Quantidades de procedimentos hospitalares nos hospitais vinculados ao SUS, 
    por municípios, nos últimos 16 anos</h2>
</div>
"""
st.markdown(html_code, unsafe_allow_html=True)

# Medidas
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Graficos de Linha e Barras
col7, col8 = st.columns([2, 1])

# Medidas

media_value = qtd_datasus[procedimento].mean()
col1.write(f"""
           ## Media
           ### {media_value:.2f}
           """)

moda_value = qtd_datasus[procedimento].astype(int).mode()[0]
col2.write(f"""
           ## Moda
           ### {moda_value}
           """)

mediana_value = qtd_datasus[procedimento].median()
col3.write(f"""
           ## Mediana
           ### {mediana_value:.2f}
           """)

min_value = qtd_datasus[procedimento].min()
col4.write(f"""
           ## Min
           ### {min_value:.2f}
           """)

max_value = qtd_datasus[procedimento].max()
col5.write(f"""
           ## Max
           ### {max_value:.2f}
           """)

desvio_padrao = qtd_datasus[procedimento].std()
col6.write(f"""
           ## Desvio
           ### {desvio_padrao:.2f}
           """)


# Gráfico com Top 10 Municípios Por Qtd de Procedimentos 

# Check and debug the filtered DataFrame
if not df_filtered.empty:
    top_municipios = df_filtered.groupby('Nome_Município')[[procedimento]].sum().sort_values(by=procedimento, ascending=True).tail(10).reset_index()
else:
    st.write("Filtered DataFrame is empty")
    top_municipios = pd.DataFrame()  # Create an empty DataFrame if the filtered data is empty

# Plot the bar chart if the DataFrame is not empty
if not top_municipios.empty:
    fig_top_mun = px.bar(
        top_municipios,
        x=procedimento,
        y='Nome_Município',
        orientation='h',
        text=procedimento
    )
    col8.plotly_chart(fig_top_mun, use_container_width=True)
else:
    col8.write("No data to display")

# Plotar Gráfico de Linhas

qtd_ano = df_filtered.groupby('Ano')[[procedimento]].sum().sort_values(by='Ano', ascending=True).reset_index()

fig_line = px.line(qtd_ano, x='Ano', y=procedimento, title='Procedimentos por Ano', markers=True)
col7.plotly_chart(fig_line, use_container_width=True)

# Plotar Gráfico de Árvore

qtd_uf = df_filtered.groupby('Nome_UF')[[procedimento]].sum().reset_index()

fig_map = px.treemap(
    qtd_uf,
    path=['Nome_UF'],  
    values=procedimento,  
)

st.plotly_chart(fig_map, use_container_width=True)

