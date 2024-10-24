import pandas as pd
import openpyxl as openpy
import locale

df_meses = pd.DataFrame()

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
#PROCEDIMENTOS REALIZADOS PROTESES
df_proteses = pd.read_excel(r'\DadosSia\proteses.xlsx', skiprows=2)
df_long = pd.melt(df_proteses, id_vars=['Procedimentos realizados'], 
                  var_name='Mes', 
                  value_name='Quantidade')
df_long = df_long[df_long['Procedimentos realizados'] != 'Total']
df_long = df_long.drop(140)
df_long = df_long.drop(141)
df_long = df_long.drop(142)
df_long = df_long.drop(143)
meses_portugues = {
    "Janeiro": "January", "Fevereiro": "February", "Março": "March", "Abril": "April", 
    "Maio": "May", "Junho": "June", "Julho": "July", "Agosto": "August", 
    "Setembro": "September", "Outubro": "October", "Novembro": "November", "Dezembro": "December"
}
df_long['Mes'] = df_long['Mes'].replace(meses_portugues, regex=True)
df_long['Mes'] = pd.to_datetime(df_long['Mes'], format='mixed', errors='coerce')

df_long['Ano'] = df_long['Mes'].dt.year
df_long['Ano'] = df_long['Ano'].astype(str)
anos_extenso = {
    "2021.0": "2021", "2022.0": "2022", "2023.0": "2023", "2024.0": "2024"}
df_long['Ano'] = df_long['Ano'].replace(anos_extenso, regex=True)
df_long['Mes'] = df_long['Mes'].dt.month
df_long['Mes Extenso'] =  df_long['Mes']
df_long['Mes Extenso'] = df_long['Mes Extenso'].astype(str)
meses_extenso = {
    "1": "Janeiro", "2": "Fevereiro", "3": "Março", "4": "Abril", "5": "Maio","6": "Junho", "7": "Julho",
    "8": "Agosto", "9": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"}
df_long['Mes Extenso'] = df_long['Mes Extenso'].replace(meses_extenso, regex=True)
df_long['Mes Extenso'] = df_long['Mes Extenso'].replace('Janeiro0', 'Janeiro')
df_long['Mes Extenso'] = df_long['Mes Extenso'].replace('JaneiroJaneiro', 'Novembro')
df_long['Mes Extenso'] = df_long['Mes Extenso'].replace('JaneiroFevereiro', 'Dezembro')
df_long['Procedimentos realizados'] = df_long['Procedimentos realizados'].replace('0701070099 PROTESE PARCIAL MANDIBULAR REMOVIVEL', 'PROTESE PARCIAL MANDIBULAR REMOVIVEL')
df_long['Procedimentos realizados'] = df_long['Procedimentos realizados'].replace('0701070102 PROTESE PARCIAL MAXILAR REMOVIVEL', 'PROTESE PARCIAL MAXILAR REMOVIVEL')
df_long['Procedimentos realizados'] = df_long['Procedimentos realizados'].replace('0701070129 PROTESE TOTAL MANDIBULAR', 'PROTESE TOTAL MANDIBULAR')
df_long['Procedimentos realizados'] = df_long['Procedimentos realizados'].replace('0701070137 PROTESE TOTAL MAXILAR', 'PROTESE TOTAL MAXILAR')
df_long['Mes'] = df_long['Mes'].astype(str).str.rstrip('.0').astype('int64')

#DISTRIBUIÇÃO POR SEXO
df_proteses_sexo = pd.read_excel(r'\DadosSia\proteses_sexo.xlsx', skiprows=2)
df_proteses_sexo = pd.melt(df_proteses_sexo, id_vars=['Sexo'], 
                  var_name='Mes', 
                  value_name='Quantidade')
df_proteses_sexo = df_proteses_sexo[df_proteses_sexo['Sexo'] != 'Total']
df_proteses_sexo = df_proteses_sexo.drop(84)
df_proteses_sexo = df_proteses_sexo.drop(85)

meses_portugues = {
    "Janeiro": "January", "Fevereiro": "February", "Março": "March", "Abril": "April", 
    "Maio": "May", "Junho": "June", "Julho": "July", "Agosto": "August", 
    "Setembro": "September", "Outubro": "October", "Novembro": "November", "Dezembro": "December"
}
df_proteses_sexo['Mes'] = df_proteses_sexo['Mes'].replace(meses_portugues, regex=True)
df_proteses_sexo['Mes'] = pd.to_datetime(df_proteses_sexo ['Mes'], format='mixed', errors='coerce')

df_proteses_sexo['Ano'] = df_proteses_sexo['Mes'].dt.year
df_proteses_sexo['Ano'] = df_proteses_sexo['Ano'].astype(str)
df_proteses_sexo['Mes'] = df_proteses_sexo['Mes'].dt.month
df_proteses_sexo['Mes Extenso'] = df_proteses_sexo['Mes'].astype(str)
meses_extenso = {
    "1": "Janeiro", "2": "Fevereiro", "3": "Março", "4": "Abril", "5": "Maio","6": "Junho", "7": "Julho",
    "8": "Agosto", "9": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"}
df_proteses_sexo['Mes Extenso']=df_proteses_sexo['Mes Extenso'].replace(meses_extenso, regex=True)
df_proteses_sexo['Mes Extenso']=df_proteses_sexo['Mes Extenso'].replace('JaneiroJaneiro','Novembro')
df_proteses_sexo['Mes Extenso']=df_proteses_sexo['Mes Extenso'].replace('JaneiroFevereiro','Dezembro')
df_proteses_sexo = df_proteses_sexo.sort_values(['Mes'])