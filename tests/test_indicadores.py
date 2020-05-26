"""
Testes Automatizados para a classe Indicadores.
"""

import pytest
import pandas as pd
from pandas._testing import assert_frame_equal

from classes.dados import Dados
from classes.indicadores import Indicadores

@pytest.fixture()
def dados():
  dados = Dados("data/coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv")
  dados.tratando_dados_faltantes()
  return dados

@pytest.fixture()
def indicadores():
  indicadores = Indicadores()
  return indicadores

#testa se o calculo dos indicadores esta correto
def testa_se_o_calculo_dos_indicadores_esta_correto(dados,indicadores):
    """
    Confere se o arquivo.csv gerado após os calculos dos indicadores esta correto.

    Essa conferencia é realizada a partir de um arquivo.csv com os calculos feitos previamente.

    A função cria uma saida.csv e depois chama esse arquivo para fazer a comparação de dados,
    isso teve que ser feito dessa forma porque há algum erro de comparação quando se compara
    um arquivo criado dentro do python e um arquivo externo chamado pelo python, mesmo garantindo
    que ambos sao identicos.

    :param dados:
    :param indicadores:
    :return:
    """
    data_confere = pd.read_csv("tests/testa_se_o_calculo_dos_indicadores_esta_correto.csv")

    teste1 = dados.preenche_data_inicio("1/12/2015 2:33")
    teste2 = dados.preenche_data_fim("1/12/2015 4:00")
    if teste1 and teste2:
        # Assumindo que dados apois data_fim nao serao utilizados
        dados_cortado = dados.corta_excesso(dados.dados)  # cortando o excesso de dados

        data_resposta = pd.DataFrame()
        data_resposta['Timestamp'] = dados_cortado['Timestamp']

        medias_relativas = indicadores.calcula_medias_relativas(dados_cortado)
        data_resposta['indicador-1'] = medias_relativas

        rsi = indicadores.calcula_indices_de_força_relativa(dados_cortado['Close'])
        data_resposta['indicador-2'] = rsi

        data_resposta = dados.pesquisa_no_dataframe_o_intervalo_datas(data_resposta)
        data_resposta.index = range(data_resposta.shape[0])
        data_resposta.to_csv("tests/save_auxiliar_testa_se_o_calculo_dos_indicadores_esta_correto.csv")
        data_resposta = pd.read_csv("tests/save_auxiliar_testa_se_o_calculo_dos_indicadores_esta_correto.csv")

        assert_frame_equal(data_resposta, data_confere)

