"""
Programa principal
"""

from classes.dados import Dados
import sys


def main(args):
    """
    Onde são coletadas as datas: inicio e fim e chama as classes para
    o calculo dos indicadores e criação do saida.csv
    """
    dados = Dados("data/coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv")
    dados.tratando_dados_faltantes()
    if(len(args) == 5):
        data_inicio = args[1] +" "+args[2]
        test = dados.preenche_data_inicio(data_inicio)
    else:
        test = True

    while (not test):
        data_inicio = input("Digite uma Data Incio (dd/mm/yy H:M):")
        test = dados.preenche_data_inicio(data_inicio)
        if (not test): print("Data Inicio invalida tente novamente...")

    if (len(args) == 5):
        data_fim = args[3] + " " + args[4]
        test = dados.preenche_data_fim(data_fim)
    else:
        test = True

    while (not test):
        data_fim = input("Digite uma Data Fim (dd/mm/yy H:M):")
        test = dados.preenche_data_fim(data_fim)
        if (not test): print("Data Fim invalida tente novamente...")

    dados.gera_csv_indicadores
    dados.gera_data_set_em_mes()
    dados.grafico_exp(data_inicio,data_fim)



if __name__ == '__main__':
    sys.exit(main(sys.argv))


