def predict_regression():

    # %%
    # Importando as bibliotecas
    import numpy as np
    import pandas as pd
    from pandas_profiling import ProfileReport
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    # %%
    # Importando a base
    dados = pd.read_excel('perfil_clientes_edits.xlsx')

    # %%
    ## criando coluna de targets
    dados['target_gestor'] = 0
    mente_aberta = dados['Caracteristica do Gestor'] == '"Cabeça aberta"'
    dados.loc[mente_aberta, 'target_gestor'] = 1

    dados['target_suporte'] = 0
    baixo_suporte = (dados['Frequencia Suporte'] == 'Menos de uma vez por semana') | (dados['Frequencia Suporte'] == 'Raramente')
    #baixo_suporte = dados['Frequencia Suporte'] == 'Raramente'
    dados.loc[baixo_suporte, 'target_suporte'] = 1

    # %%
    dados_y = dados['target_suporte']
    dados_x = dados.drop(dados[['Frequencia Suporte', 'Tipo de Suporte','Categoria Suporte','target_gestor','target_suporte']], axis=1)

    # %%
    # Convertendo valores de string para valores númericos para conseguirmos usar no modelo de Regressão.
    dummies = pd.get_dummies(dados_x)

    #print(dummies)

    # %%
    # Carregando os dados em um array numpy
    X = np.array(dummies.values)
    y = np.array(dados_y.values)

    # %%
    # Dividir os dados em conjunto de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=45)


    # %%
    # Para as variáveis de treino

    # normalizando e padronizando os dados
    # MinMaxScaler é usado para normalizar as variáveis, e StandardScaler é usado para padronizar
    from sklearn.preprocessing import MinMaxScaler, StandardScaler

    # dados x (features) normalizados
    # X = np.array(X)

    # normalizando
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    normalized_data = scaler.transform(X_train)
    #print(normalized_data)

    # Padronizando
    scaler = StandardScaler()
    scaler.fit(X_train)
    standardized_data = scaler.transform(X_train)
    #print(standardized_data)

    #print(standardized_data.shape)

    X_train = standardized_data

    # %%
    # Para as variáveis de teste

    # normalizando e padronizando os dados
    # MinMaxScaler é usado para normalizar as variáveis, e StandardScaler é usado para padronizar
    from sklearn.preprocessing import MinMaxScaler, StandardScaler

    # dados x (features) normalizados
    # X = np.array(X)

    # normalizando
    scaler = MinMaxScaler()
    scaler.fit(X_test)
    normalized_data = scaler.transform(X_test)
    #print(normalized_data)

    # Padronizando
    scaler = StandardScaler()
    scaler.fit(X_test)
    standardized_data = scaler.transform(X_test)
    #print(standardized_data)

    #print(standardized_data.shape)

    X_test = standardized_data

    # %%
    # Criando o modelo
    model = LogisticRegression(random_state=0,max_iter=1000)

    # Treinando o modelo
    model.fit(X_train, y_train)

    clf2 = LogisticRegression(random_state=45,max_iter=1000).fit(X_train, y_train)

    # %%
    # Fazendo a previsão das classes
    y_pred2 = clf2.predict(X_test)

    # %%
    # Avaliando o erro

    from sklearn.metrics import confusion_matrix

    confusion_matrix(y_test,y_pred2)

    # %%
    # Avaliando o modelo 
    # score = model.score(X_test, y_test)

    from sklearn import metrics

    score = metrics.accuracy_score(y_test, y_pred2)

    #print('Acurácia:', score)

    # Percentagem de acerto

    # %%
    # Usando o modelo para previsão
    predictions = model.predict(X_test)
    #print(predictions)

    # %%
    # Visualizando o gráfico

    import matplotlib.pyplot as plt
    from scipy.special import expit

    # x = np.linspace(X_train.min(), X_train.max(), 100)
    # y = expit(x)
    # plt.plot(x, y)
    # plt.grid()
    # plt.xlim(X_train.min(), X_train.max())
    # plt.xlabel('x')
    # plt.title('expit(x)')
    # plt.show()

    # # %%
    # # Comparando a previsão com o valor real
    # print('O valor de y teste é:')
    # print(y_test)

    # print('O valor do y_pred é:')
    # print(predictions)

    # %%
    # Fazendo a previsão das probabilidades
    proba = clf2.predict_proba(X_test)
    #print(proba)

    # Probabilidade de acionar o suporte até 1vez na semana é de:
    probabilidade_baixo_suporte = proba[:,1]

    #list(probabilidade_baixo_suporte)

    # %% [markdown]
    # ### Prevendo novos valores

    # %%
    dados_x_input = dados.drop(dados[['Frequencia Suporte', 'Tipo de Suporte','Categoria Suporte','target_gestor','target_suporte']], axis=1)
    dados_x_input['Input'] = 0

    dados_y = dados['target_suporte']

    dados_x_input

    # %%
    data = {}


    for item in dados_x_input.columns[:-1]:
        
    #  print(f'Para a coluna de {item}')

        options = set(dados_x_input[item])

        lista_len = len(options)

        c = 1
        opt = []


        for op in options:
            list_add_opt = []
            list_add_opt = [[c], [op]]
            opt.append(list_add_opt)
            c += 1

        data[item] = opt

    #print(data)


    # %%
    data_input = {}

    for k,v in data.items():
    # for i in k:
        print(f'Escolha o número da opção de {k}')

        opt_list = len(v)
        for i in range(0, opt_list):
            print(f'{v[i][0]} - {v[i][1]}')
            
        number = 0
        while number not in range(1, opt_list + 1):
            number = int(input(f'Digite o número da opção. Escolha valores entre {range(1, opt_list)}: '))
        print(f'Você escolheu a opção {v[number-1][1]}')
        
        data_input[k] = v[number-1][1]

    data_input['Input'] = [1]

    #print(data_input)

    # %%
    dados_input = pd.DataFrame(data_input)

    dados_input = pd.concat([dados_x_input, dados_input])

    #dados_input.tail(3)

    # %%
    ## Realizando a previsão:
    ## Adição manual

    # data = {
    #     'Atividade': ['COMÉRCIO'],
    #     'Ramo de atuação': ['PANIFICAÇÃO'],
    #     'Colaboradores': ['De 10 a 20'],
    #     'Faixa etária gestor': ['50+'],
    #     'Caracteristica do Gestor': ['"Cabeça aberta"'],
    #     'Faturamento estimado': ['Até R$ 50 mil'],
    #     'Input': [1]
    # }

    # dados_input = pd.DataFrame(data)

    # dados_input = pd.concat([dados_x_input, dados_input])

    # dados_input.tail(3)


    # %%
    # Convertendo valores de string para valores númericos para conseguirmos usar no modelo de Regressão.
    dummies = pd.get_dummies(dados_input)

    #print(dummies.columns)

    #print(dummies)


    # %%
    dummies_input = dummies[dummies['Input'] == 1]
    dummies_input = dummies_input.drop(dummies_input[['Input']], axis=1)
    dummies_input


    # %%
    # Carregando os dados em um array numpy
    X = np.array(dummies_input.values)

    # %%
    # Usando o modelo para previsão
    print('Prevendo classificação para o dado de entrada... \n 0 - Frequência de suporte + 1 Vez por Semana \n 1 - Frequência de suporte menor do que 1 vez por semana')

    print('')

    # Fazendo a previsão das probabilidades
    proba = clf2.predict_proba(X)


    print(f'Classificação 0 --> {(proba[0][0] * 100):.2f}% de probabilidade')
    print(f'Classificação 1 --> {(proba[0][1] * 100):.2f}% de probabilidade')

    print()


    predictions = model.predict(X)[-1]
    print('A classificação predita foi', predictions)


    # Performance do modelo:
    print('\nAcurácia do modelo:', round((score * 100),2), '%')


    # Probabilidade de acionar o suporte até 1 vez na semana é de:
    #probabilidade_baixo_suporte = proba[:,1]

    #list(probabilidade_baixo_suporte)


