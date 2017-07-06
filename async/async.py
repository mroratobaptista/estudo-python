import asyncio
import os
from time import time

import aiohttp
from openpyxl import load_workbook

URL_BASE = 'https://api.mercadolibre.com/items/'
PASTA_DOWNLOADS = 'downloads'
PLANILHA_MLBS = 'mlbs.xlsx'


def gerar_url(mlb):
    return f'{URL_BASE}{mlb}'


async def pegar_titulo(mlb, session):
    url = gerar_url(mlb)

    resposta = await session.get(url)
    if resposta.status == 200:
        print(f'{mlb} - OK')
        json = await resposta.json()
        await salvar_titulo(mlb, json['title'])


async def salvar_titulo(mlb, titulo):
    with open(mlb + '.txt', 'w') as arquivo:
        arquivo.write(str(titulo))


def gerar_lista_mlbs(nome_planilha):
    arquivo = load_workbook(nome_planilha)
    planilha = arquivo.active

    mlbs = []

    for row in planilha.rows:
        for cell in row:
            mlbs.append(cell.value)

    return mlbs


def pegar_e_salvar_titulos():
    mlbs = gerar_lista_mlbs(PLANILHA_MLBS)
    os.chdir(PASTA_DOWNLOADS)

    loop = asyncio.get_event_loop()

    with aiohttp.ClientSession() as session:
        tarefas = [pegar_titulo(mlb, session) for mlb in mlbs]

        esperaveis = asyncio.wait(tarefas)

        resposta, _ = loop.run_until_complete(esperaveis)

    loop.close()

    return len(resposta)


if __name__ == '__main__':
    tempo_inicio = time()

    qtd = pegar_e_salvar_titulos()

    tempo_final = time() - tempo_inicio
    print(f'{qtd} títulos salvos em {round(tempo_final, 2)} segundos.')
