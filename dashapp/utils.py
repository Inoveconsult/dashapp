from dashapp.df_tratados import df_meses, df_long

def opcoes_meses(ano_atual, df):
    if df_meses.empty or ano_atual not in df_meses['Ano'].unique():
        # Atualiza o DataFrame com o ano correspondente
        df_meses = df.loc[df['Ano'] == ano_atual, :]    
        # Gera a lista de meses únicos
    df_meses = df_meses.loc[df_meses['Ano'] == ano_atual, :]
    listar_meses = list(df_meses['Mes Extenso'].unique())
    listar_meses.append('TODOS')  # Adiciona a opção "TODOS"
    
    return listar_meses