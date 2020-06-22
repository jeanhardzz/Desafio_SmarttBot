"""
Esta classe esta sendo usada para ler um arquivo.csv de candlestisck e gerar uma saida.csv com indicadores.

Essa classe se ultiliza da classe Indicadores para fazero calculos dos indicadores

O arquivo saida.csv contem dois indicadores, sao eles:
indicador-1: Representa as Médias Móveis Exponenciais
indicador-2: Representa os Índices de Forças Relativas
"""

from datetime import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt

from .indicadores import Indicadores



class Dados:
    def __init__(self,caminho_csv,pytest_val=0):
        """Construtor que recebe o caminho do arquivo.csv e uma varivel identificadora de pytest.

        A varivel pytest_val serve para identificar se o programa esta sendo executado
        por uma função pytest (a função pytest precisa enviar um parametro !=0 )

        Nesta classe a pytest_val esta sendo usada para salvar um saida.csv especifica
        para o teste do pytest

        :param caminho_csv: caminho/arquivo.csv
        :param pytest_val: varivael auxilio para testes pytest
        """
        self.dados = pd.read_csv(caminho_csv)
        self.pytest_val = pytest_val
        self.dados_mes = None

    def tratando_dados_faltantes(self):
        """Retira do DataFrame todos os dados invalidos (NaN).

        Pesquisa em todas as colunas se há um valor do tipo Nan.
        Se houver, remove essa linha do DataFrame.

        :return:
        """
        self.dados.dropna(subset=self.dados.columns,inplace=True)
        self.dados.index = range(self.dados.shape[0])

    def preenche_data_inicio(self,data_inicio):
        """Testa se o valor é valido para ser a data inicial.

        Primeiro faz um teste de ValueError para garantir que foi escrito
        uma data no formato exigido.

        E depois faz uma conversao de datetime para seconds since the epoch,
        que é um tipo de dado que conta a quantidade de segundos passados desde
        January 1, 1970, 00:00:00 (UTC).

        :param data_inicio: Inicio do intervalo.
        :return:
        """
        try:
            self.data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y %H:%M")
            try:
                self.data_inicio = time.mktime(self.data_inicio.timetuple())
                return True

            except OverflowError:
                return False

        except ValueError:
            return False


    def preenche_data_fim(self, data_fim):
        """Testa se o valor é valido para ser a data fim.

        Primeiro faz um teste de ValueError para garantir que foi escrito
        uma data no formato exigido.

        E depois faz uma conversao de datetime para seconds since the epoch,
        que é um tipo de dado que conta a quantidade de segundos passados desde
        January 1, 1970, 00:00:00 (UTC).

        E por ultimo testa se a data fim é menor que a data inicio.

        :param data_inicio: Inicio do intervalo.
        :return:
        """

        try:
            self.data_fim = datetime.strptime(data_fim, "%d/%m/%Y %H:%M")
            try:
                self.data_fim = time.mktime(self.data_fim.timetuple())
                if self.data_fim < self.data_inicio:
                    return False
                return True

            except OverflowError:
                return False

        except ValueError:
            return False


    def imprime_datas_inicio_fim(self):
        """Usa a função print() para imprimir as datas inicio e fim.

        :return:
        """
        print(self.data_inicio)
        print(self.data_fim)

    def pesquisa_no_dataframe_o_intervalo_datas(self,data):
        """Recebe um data frame e devolve um novo dataframe no intervalo.

        O dataframe retorno esta no intervalo data_inicio - data_fim.

        :param data: Dataframe.
        :return: data_intervalo
        """
        selecao = (data["Timestamp"] >= self.data_inicio) & (data["Timestamp"] <= self.data_fim)
        data_intervalo = data[selecao]


        return data_intervalo

    def corta_excesso(self,data):
        """Recebe um dataframe e retorna outro dataframe com datas inferiores a data_fim.

        :param data: Dataframe
        :return: data_cortado
        """
        selecao = (data["Timestamp"] <= self.data_fim)
        data_cortado = data[selecao]
        return data_cortado

    @property
    def gera_csv_indicadores(self):
        """Gera um arquivo.csv com dois indicadores.

        indicador-1: Medias Móveis Exponenciais.
        indicador-2: Indice de Força Relativa.

        Para otimizar, faço um corte nos Dados no data_fim.
        Assumindo que os indicadores nao usaram dados após data_fim para cálculo.

        Após os calculos efetua-se a criação do arquivo.csv e garanto a criação do mesmo.
        Retornando False caso nao tenho efetuado a criação e True caso tenha sucesso

        :return:
        """
        try:
            indicadores = Indicadores()

            # Assumindo que dados apois data_fim nao serao utilizados
            dados_cortado = self.corta_excesso(self.dados) # cortando o excesso de dados

            data_resposta = pd.DataFrame()
            data_resposta['Timestamp'] = dados_cortado['Timestamp']


            medias_relativas = indicadores.calcula_medias_relativas(dados_cortado)
            data_resposta['indicador-1'] = medias_relativas

            rsi = indicadores.calcula_indices_de_força_relativa(dados_cortado['Close'])
            data_resposta['indicador-2']=rsi

            data_resposta = self.pesquisa_no_dataframe_o_intervalo_datas(data_resposta)
            data_resposta.index = range(data_resposta.shape[0])

            if(self.pytest_val==0):
                caminho = "data/saida.csv"
            else:
                caminho = "tests/testa_se_arquivo_csv_foi_criado_com_sucesso.csv"

            data_resposta.to_csv(caminho)
            print("\nO arquivo saida.csv foi criado com sucesso.\n\nPreview:")
            print(data_resposta.info())
            return True
        except FileNotFoundError:
            erro = FileNotFoundError("Caminho do arquivo nao encontrado!")
            print(erro)
            return False
        except:
            print("Erro!")
            return False



    def converte_timestamp_datetime(self,x):
        """
        Pega uma data no formato timestamp e tranforma em datetime
        :return:
        """
        dt = datetime.utcfromtimestamp(x)
        return dt



    def gera_data_set_em_mes(self):
        """
        Gera um data set chamado self.dados_mes baseado no dataset em minutos mas
        com o periodo convertido para meses.

        :return:
        """
        #Primeiro criamos uma coluna de datetime em self.dados para trabalhar
        self.dados['Datetime'] = self.dados['Timestamp'].apply(self.converte_timestamp_datetime)

        #Criando novo Dataset em mes

        ultima_data = self.dados['Datetime'][-1:].values  # 2019-01-07 22:06:00
        ultima_data = ultima_data[0]
        ultima_data = pd.to_datetime(ultima_data)

        data_inicial = pd.to_datetime('12-01-2014 00:00')
        dic_mes = {}
        while (data_inicial < ultima_data):
            selecao = (self.dados['Datetime'] >= data_inicial) & (self.dados['Datetime'] < data_inicial + pd.DateOffset(1))
            aux = self.dados[selecao]

            dic_mes[data_inicial.date()] = aux['Close'].mean()

            data_inicial = data_inicial + pd.DateOffset(1)

        self.dados_mes = pd.Series(dic_mes).to_frame('Close')
        self.dados_mes.dropna(subset=self.dados_mes.columns, inplace=True)

    def grafico_exp(self,data_1,data_2):


        data_1 = pd.to_datetime(data_1)
        data_2 = pd.to_datetime(data_2)

        selecao = (self.dados_mes.index >= data_1) & (self.dados_mes.index <= data_2)
        df_mes = self.dados_mes[selecao]

        exp1 = df_mes['Close'].ewm(span=5, adjust=False).mean()
        exp2 = df_mes['Close'].ewm(span=20, adjust=False).mean()

        plt.plot(df_mes.index, df_mes['Close'], label='Fechamento')
        plt.plot(df_mes.index, exp1, label='exp 5')
        plt.plot(df_mes.index, exp2, label='exp 20')
        plt.legend(loc='upper left')
        plt.show()

    def __str__(self):
        """Propriedade __str__ que retorna o DataFrame carregado em dados

        :return: self.dados
        """
        return str(self.dados)




