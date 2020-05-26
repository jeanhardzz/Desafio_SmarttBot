"""
Testes Automatizados para a classe Dados.
"""

import pytest

from classes.dados import Dados

@pytest.fixture()
def dados():
  dados = Dados("data/coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv")
  dados.tratando_dados_faltantes()
  return dados

#testa se existem dados faltantes
def testa_se_existem_dados_faltantes(dados):
    """
    Confere se há dados nulos do tipo NaN.

    :param dados:
    :return:
    """
    assert (len(dados.dados) - dados.dados.count()).sum() == 0

#testa se data_inicio recebe datas compativeis
def testa_se_data_inicio_recebe_datas_compativeis(dados):
    """
    Confere se a classe dados recebe uma data inicio no formato ideal.

    :param dados:
    :return:
    """
    assert dados.preenche_data_inicio("12/05/1997 00:19") == True

#testa se data_fim recebe datas compativeis
def testa_se_data_fim_recebe_datas_compativeis(dados):
    """
    Confere se a classe dados recebe uma data fim no formato correto.

    :param dados:
    :return:
    """
    assert dados.preenche_data_inicio("13/05/1997 00:19") == True

#testa se data_inicio recebe datas incompativeis
def testa_se_data_inicio_recebe_datas_incompativeis(dados):
    """
    Confere se a classe dados recebe uma data inicio com o mes
    e o dia no formato correto.

    :param dados:
    :return:
    """
    assert dados.preenche_data_inicio("12/25/1997 4:19") == False
    assert dados.preenche_data_inicio("50/01/1997 4:19") == False

#testa se data_fim recebe datas incompativeis
def testa_se_data_fim_recebe_datas_incompativeis(dados):
    """
    Confere se a classe dados recebe uma data fim com o mes
    e o dia no formato correto.

    :param dados:
    :return:
    """
    assert dados.preenche_data_fim("12/25/1997 4:21") == False
    assert dados.preenche_data_fim("50/01/1997 4:21") == False

#testa se data_inicio recebe horas incompativeis
def testa_se_data_inicio_recebe_horas_incompativeis(dados):
    """
    Confere se a classe dados recebe as horas inicio no formato correto.

    :param dados:
    :return:
    """
    assert dados.preenche_data_inicio("12/06/1997 58:19") == False

#testa se data_fim recebe horas incompativeis
def testa_se_data_fim_recebe_horas_incompativeis(dados):
    """
    Confere se a classe dados recebe as horas fim no formato correto.

    :param dados:
    :return:
    """
    assert dados.preenche_data_fim("12/06/1997 58:19") == False

#testa se data_inicio recebe datas anterioes a 1970
def testa_se_data_inicio_recebe_datas_anterioes_a_1970(dados):
    """
    Confere se a classe dados recebe a data inicio anterior ao formato utilizado.

    :param dados:
    :return:
    """
    assert dados.preenche_data_inicio("12/01/1500 18:00") == False
    assert dados.preenche_data_inicio("12/01/150 18:00") == False

#testa se data_fim recebe datas anterioes a 1970
def testa_se_data_fim_recebe_datas_anterioes_a_1970(dados):
    """
    Confere se a classe dados recebe a data fim anterior ao formato utilizado.

    :param dados:
    :return:
    """
    assert dados.preenche_data_fim("12/01/1500 23:59") == False
    assert dados.preenche_data_fim("12/01/150 23:59") == False

#testa se retorna um data frame no intervalo
def testa_se_retorna_um_data_frame_no_intervalo(dados):
    """
    Confere se a funcao dado.pesquisa_no_dataframe retorna um dataframe no intervalo correto.

    :param dados:
    :return:
    """
    teste1 = dados.preenche_data_inicio("1/12/2014 2:33")
    teste2 = dados.preenche_data_fim("2/12/2014 2:29")
    if teste1 and teste2:
        df_intervalo=dados.pesquisa_no_dataframe_o_intervalo_datas(dados.dados)

        for i in range(df_intervalo.shape[0]):
            pesquisa_df = dados.dados[dados.dados["Timestamp"] == df_intervalo.iloc[i][0]]
            assert pesquisa_df.shape[0] == 1
    else:
        assert False==True

#testa se arquivo csv foi criado com sucesso
def testa_se_arquivo_csv_foi_criado_com_sucesso():
    """
    Confere se dados.gera_csv_indicadores gera um arquivo.csv.

    :return:
    """
    dados = Dados("data/coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv",1)
    teste1 = dados.preenche_data_inicio("1/12/2015 2:33")
    teste2 = dados.preenche_data_fim("1/12/2015 4:00")
    if teste1 and teste2:
        assert dados.gera_csv_indicadores == True
