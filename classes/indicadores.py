"""
Essa classe possui os metodos para calcular indicadores de candlesticks dado um DataFrame.

Nenhuma das funções aqui deve alterar o DataFrame mas sim retornar o indicador
no formato series ou lista, ou ate mesmo um DataFrame cópia do original.
"""

import numpy as np

class Indicadores:
    def __init__(self):
        pass

    def calcula_medias_relativas(self,dados):
        """Retorna uma serie com o calculo de todas as medias móveis exponenciais.

        Média Móvel Exponencial é basicamente a media ponderada do preço de fechamento
        dos ultimos N fechamentos, dando mais peso para os fechamentos mais próximos.
        Aqui o N é chamado de periodo, e estamos utilizando um periodo de 20.
        Dependendo do dataset, 20 periodos pode ser 20 minutos, 20 horas, 20 dias ou 20 anos.

        :param dados: DataFrame
        :return: Serie
        """
        media = dados['Close'].ewm(span=20, adjust=False).mean()

        return media


    def calcula_indices_de_força_relativa(self, precos, n=14):
        """Retorna uma lista com os índices de força relativa dado uma Serie de preços

        O indice de força relativa (RSI em inglês) foi desenvolvido por J. Welles Wilder.
        É um indice com escala de variação fixa, entre 0 e 100.
        Basicamente, quanto maior o indice (>70) mais sobrevalorizada a ação esta
        e quanto menor o indice (<30) mais subvalorizada a ação esta.

        :param precos: Serie
        :param n: periodo
        :return: lista de rsi
        """
        # Qual que é a ideia
        # Calcular os deltas, que sao a diferença entre o preço[0] e o preço[1]
        # Calcular o rsi pros n primeiros deltas;
        # Esses n-rsi primeiros serao iguais obviamente;
        # Depois vou percorrer os deltas faltantes pra calcular os rsi faltantes
        # Dentro do for vou corrigindo os valores da media da taxa de cotação quando ela sobe e quando ela desce
        # Depois calculo o RSI usando a media da taxa de cotação corrigida

        
        # fazendo o calculo dos n primeiros pra inicializar a conta

        deltas = np.diff(precos)  # pegando a diferença preco[0]-preco[1] e guardando em deltas[0]
        primeiros = deltas[:n]  # pegando as diferença 14 primeiras diferenças

        ganho = primeiros[primeiros >= 0].sum() / n  # media das diferenças positivas dentre as 14 iniciais
        perda = -primeiros[primeiros < 0].sum() / n  # media das diferenças negativas dentre as 14 iniciais

        forca_relativa = ganho / perda  # calculando a força relativa

        rsi = np.zeros_like(precos)  # criando uma copia de precos só com zeros

        rsi[:n] = 100. - 100. / (1. + forca_relativa)  # calculando rsi para os 14 primeiros precos, serao iguais

        # print(deltas,primeiros,ganho,perda,rsi[:n+1], sep='\n')
        # print(deltas[:n+1])

        # for pra calcular o resto dos rsi
        for i in range(n, len(precos)):
            delta = deltas[i - 1]
            # tem que ser deltas[i-1] porque é a diferença do preço anterior com o preço atual
            # se fosse deltas[i] seria a diferença do preço atual com o proximo preço

            if (delta >= 0):
                ganho_variacao = delta
                perda_variacao = 0.
            else:
                ganho_variacao = 0.
                perda_variacao = -delta

            # corrigindo
            ganho = (ganho * (n - 1) + ganho_variacao) / n
            perda = (perda * (n - 1) + perda_variacao) / n

            forca_relativa = ganho / perda

            rsi[i] = 100. - 100. / (1. + forca_relativa)

        return rsi







