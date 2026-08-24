"""
Geração dos dados sintéticos da consultoria Mixed Comunicação e Marketing.

O script simula dados operacionais de uma pequena empresa de comunicação
para o período de janeiro de 2025 a junho de 2026.

Os dados contêm algumas inconsistências intencionais para permitir uma
etapa posterior de Data Quality.
"""

from pathlib import Path
import numpy as np
import pandas as pd

SEMENTE = 42
np.random.seed(SEMENTE)

RAIZ = Path(__file__).resolve().parents[1]
PASTA_DADOS = RAIZ / "data" / "raw"
PASTA_DADOS.mkdir(parents=True, exist_ok=True)

MESES = pd.date_range("2025-01-01", "2026-06-01", freq="MS")

EQUIPE = [
    ("Marcelo", "Diretor / Atendimento"),
    ("Fernanda", "Diretora / Comunicação"),
    ("Camila", "Assessora de Imprensa"),
    ("Rafael", "Social Media / Conteúdo"),
    ("Juliana", "Designer"),
]

SERVICOS_CLIENTES = {
    "C001": ["Assessoria de imprensa", "Conteúdo"],
    "C002": ["Assessoria de imprensa", "Comunicação corporativa"],
    "C003": ["Assessoria de imprensa", "Conteúdo"],
    "C004": ["Conteúdo", "Design"],
    "C005": ["Assessoria de imprensa", "Comunicação corporativa"],
    "C006": ["Assessoria de imprensa", "Conteúdo"],
    "C007": ["Assessoria de imprensa", "Conteúdo"],
    "C008": ["Assessoria de imprensa", "Conteúdo", "Design"],
    "C009": ["Assessoria de imprensa", "Conteúdo"],
    "C010": ["Assessoria de imprensa", "Design"],
    "C011": ["Conteúdo", "Design"],
    "C012": ["Assessoria de imprensa", "Comunicação corporativa"],
    "C013": ["Assessoria de imprensa"],
    "C014": ["Conteúdo", "Design"],
    "C015": ["Comunicação corporativa", "Design"],
}

VALOR_MENSAL = {
    "C001": 5200, "C002": 6500, "C003": 4800, "C004": 3900,
    "C005": 7800, "C006": 4300, "C007": 4600, "C008": 7200,
    "C009": 4100, "C010": 5000, "C011": 3600, "C012": 5900,
    "C013": 3500, "C014": 4700, "C015": 4200,
}

INICIO_CONTRATO = {
    "C001": "2024-01-01", "C002": "2024-01-01", "C003": "2024-02-01",
    "C004": "2024-05-20", "C005": "2024-08-12", "C006": "2025-01-15",
    "C007": "2025-03-10", "C008": "2025-05-05", "C009": "2025-08-01",
    "C010": "2025-10-15", "C011": "2026-02-02", "C012": "2026-04-06",
    "C013": "2022-09-01", "C014": "2024-03-01", "C015": "2025-02-10",
}

FIM_CONTRATO = {
    "C013": "2025-06-30",
    "C014": "2025-11-30",
    "C015": "2026-03-31",
}


def criar_clientes():
    dados = [
        ("C001", "Casa Nativa", "Gastronomia", "Rio de Janeiro", "2023-03-15", "Ativo", "Marcelo"),
        ("C002", "Instituto Horizonte", "Educação", "Rio de Janeiro", "2023-06-10", "Ativo", "Fernanda"),
        ("C003", "RioFit", "Saúde e bem-estar", "Rio de Janeiro", "2024-02-01", "Ativo", "Marcelo"),
        ("C004", "Armazém Carioca", "Varejo", "Rio de Janeiro", "2024-05-20", "Ativo", "Marcelo"),
        ("C005", "Construtora Atlântica", "Construção", "Rio de Janeiro", "2024-08-12", "Ativo", "Fernanda"),
        ("C006", "Verde Vivo", "Sustentabilidade", "Niterói", "2025-01-15", "Ativo", "Fernanda"),
        ("C007", "Clínica Orla", "Saúde", "Rio de Janeiro", "2025-03-10", "Ativo", "Marcelo"),
        ("C008", "Nexo Tecnologia", "Tecnologia", "Rio de Janeiro", "2025-05-05", "Ativo", "Fernanda"),
        ("C009", "Vila Gourmet", "Gastronomia", "Rio de Janeiro", "2025-08-01", "Ativo", "Marcelo"),
        ("C010", "Instituto Arte Rio", "Cultura", "Rio de Janeiro", "2025-10-15", "Ativo", "Fernanda"),
        ("C011", "Ótica Central", "Varejo", "Rio de Janeiro", "2026-02-02", "Ativo", "Marcelo"),
        ("C012", "MobiCarioca", "Mobilidade", "Rio de Janeiro", "2026-04-06", "Ativo", "Fernanda"),
        ("C013", "Espaço Movimento", "Saúde", "Rio de Janeiro", "2022-09-01", "Encerrado", "Marcelo"),
        ("C014", "Grupo Lume", "Varejo", "Rio de Janeiro", "2024-03-01", "Encerrado", "Fernanda"),
        ("C015", "Ponto Sul Eventos", "Eventos", "Rio de Janeiro", "2025-02-10", "Encerrado", "Marcelo"),
    ]

    df = pd.DataFrame(dados, columns=[
        "cliente_id", "cliente", "segmento", "cidade",
        "data_entrada", "status", "responsavel"
    ])

    # Inconsistências intencionais para o exercício de qualidade.
    df.loc[5, "cidade"] = "Niteroi"
    df.loc[7, "cliente"] = "NEXO TECNOLOGIA"
    df.loc[11, "responsavel"] = "Fernanda "
    df = pd.concat([df, df.iloc[[3]].assign(cliente_id="C004_DUP")], ignore_index=True)

    return df


def criar_contratos(clientes):
    dados = []
    numero = 1

    for cliente_id, servicos in SERVICOS_CLIENTES.items():
        nome = clientes.loc[clientes["cliente_id"] == cliente_id, "cliente"].iloc[0]

        for servico in servicos:
            valor = round((VALOR_MENSAL[cliente_id] / len(servicos)) / 50) * 50
            dados.append((
                f"CTR{numero:03d}", cliente_id, nome, servico,
                INICIO_CONTRATO[cliente_id],
                FIM_CONTRATO.get(cliente_id, "2026-12-31"),
                valor,
                "Encerrado" if cliente_id in FIM_CONTRATO else "Ativo",
            ))
            numero += 1

    df = pd.DataFrame(dados, columns=[
        "contrato_id", "cliente_id", "cliente", "servico",
        "data_inicio", "data_fim", "valor_mensal", "status_contrato"
    ])

    df.loc[2, "cliente"] = "Rio Fit"
    df.loc[4, "valor_mensal"] += 100
    return df


def criar_faturamento(contratos):
    dados = []
    numero = 1

    for _, contrato in contratos.iterrows():
        inicio = pd.to_datetime(contrato["data_inicio"]).to_period("M").to_timestamp()
        fim = pd.to_datetime(contrato["data_fim"]).to_period("M").to_timestamp()

        for mes in MESES:
            if inicio <= mes <= fim:
                valor = float(contrato["valor_mensal"])

                if contrato["cliente_id"] == "C008" and mes >= pd.Timestamp("2026-01-01"):
                    valor *= 1.08

                status = "Pago" if np.random.rand() >= 0.07 else "Em aberto"
                dados.append((
                    f"F{numero:04d}", contrato["cliente_id"], mes,
                    mes + pd.Timedelta(days=3), round(valor, 2),
                    "Recorrente", status,
                ))
                numero += 1

    df = pd.DataFrame(dados, columns=[
        "fatura_id", "cliente_id", "competencia", "data_emissao",
        "valor_faturado", "tipo_receita", "status_pagamento"
    ])

    # Duplicidade e divergência de valor intencionais.
    df = pd.concat([df, df.iloc[[10]]], ignore_index=True)
    df.loc[5, "valor_faturado"] += 250
    return df


def criar_projetos():
    dados = [
        ("P001", "C001", "Campanha de Verão", "Design", "2025-01-15", "2025-02-05", 6500, 30, 34, "Concluído"),
        ("P002", "C004", "Campanha Dia das Mães", "Conteúdo", "2025-04-10", "2025-05-10", 4800, 25, 31, "Concluído"),
        ("P003", "C005", "Relatório Institucional", "Design", "2025-06-01", "2025-06-25", 7200, 35, 39, "Concluído"),
        ("P004", "C008", "Lançamento de Produto", "Assessoria de imprensa", "2025-08-05", "2025-09-10", 9000, 40, 58, "Concluído"),
        ("P005", "C009", "Evento Gastronômico", "Comunicação corporativa", "2025-09-01", "2025-09-25", 5500, 28, 26, "Concluído"),
        ("P006", "C010", "Identidade Visual", "Design", "2025-11-01", "2025-12-05", 8000, 40, 47, "Concluído"),
        ("P007", "C002", "Campanha de Matrículas", "Conteúdo", "2026-01-10", "2026-02-15", 6200, 32, 37, "Concluído"),
        ("P008", "C011", "Campanha de Inverno", "Design", "2026-04-01", "2026-05-15", 4200, 24, 35, "Concluído"),
        ("P009", "C012", "Lançamento Institucional", "Comunicação corporativa", "2026-05-01", "2026-06-15", 7500, 36, 42, "Concluído"),
    ]

    df = pd.DataFrame(dados, columns=[
        "projeto_id", "cliente_id", "projeto", "servico",
        "data_inicio", "data_fim", "valor_contratado",
        "horas_estimadas", "horas_realizadas", "status"
    ])
    df.loc[3, "servico"] = "Assessoria imprensa"
    return df


def criar_horas(clientes):
    ativos = clientes.loc[clientes["status"] == "Ativo", "cliente_id"].tolist()
    atividades = {
        "Assessoria de imprensa": ["Release", "Follow-up", "Clipping", "Entrevista"],
        "Comunicação corporativa": ["Planejamento", "Newsletter", "Comunicação institucional"],
        "Conteúdo": ["Planejamento editorial", "Copy", "Social media"],
        "Design": ["Peça digital", "Apresentação", "Material institucional"],
    }

    dados = []
    numero = 1

    for mes in MESES:
        for nome, cargo in EQUIPE:
            quantidade = 28 if "Diretor" in cargo else 36

            for _ in range(quantidade):
                cliente_id = np.random.choice(ativos)
                servico = np.random.choice(SERVICOS_CLIENTES[cliente_id])
                horas = round(np.random.uniform(0.75, 3.5), 1)

                if cliente_id == "C008" and servico == "Assessoria de imprensa":
                    horas = round(np.random.uniform(2, 4.5), 1)

                dados.append((
                    f"H{numero:05d}",
                    mes + pd.Timedelta(days=np.random.randint(0, 27)),
                    nome, cargo, cliente_id, servico,
                    np.random.choice(atividades[servico]), horas,
                ))
                numero += 1

    df = pd.DataFrame(dados, columns=[
        "registro_id", "data", "profissional", "cargo",
        "cliente_id", "servico", "atividade", "horas"
    ])

    df.loc[20, "horas"] = np.nan
    df.loc[50, "servico"] = "Assessoria imprensa"
    return df


def criar_comercial():
    origens = ["Indicação", "Instagram", "Google", "Networking", "Site"]
    segmentos = ["Gastronomia", "Saúde", "Varejo", "Tecnologia", "Educação", "Cultura", "Construção", "Serviços"]
    motivos = ["Preço", "Momento inadequado", "Escolheu concorrente", "Sem retorno", "Escopo"]

    dados = []
    numero = 1

    for mes in MESES:
        for _ in range(np.random.randint(5, 10)):
            etapa = np.random.choice(
                ["Contato", "Reunião", "Proposta", "Negociação", "Ganho", "Perdido"],
                p=[0.12, 0.18, 0.20, 0.12, 0.18, 0.20],
            )
            resultado = "Ganho" if etapa == "Ganho" else "Perdido" if etapa == "Perdido" else "Em andamento"

            dados.append((
                f"L{numero:04d}",
                mes + pd.Timedelta(days=np.random.randint(0, 27)),
                f"Prospect {numero:03d}",
                np.random.choice(segmentos),
                np.random.choice(origens, p=[0.30, 0.28, 0.18, 0.14, 0.10]),
                np.random.choice(["Marcelo", "Fernanda"]),
                etapa,
                np.random.choice([2500, 3500, 4500, 5500, 6500, 8000, 10000]),
                mes + pd.Timedelta(days=np.random.randint(3, 25)),
                resultado,
                np.random.choice(motivos) if resultado == "Perdido" else None,
            ))
            numero += 1

    df = pd.DataFrame(dados, columns=[
        "lead_id", "data_entrada", "empresa", "segmento", "origem",
        "responsavel", "etapa", "valor_proposta", "data_proposta",
        "resultado", "motivo_perda"
    ])

    df.loc[7, "origem"] = "Instagram "
    df.loc[18, "etapa"] = "proposta"
    df.loc[31, "valor_proposta"] = np.nan
    return df


def criar_entregas(clientes):
    ativos = clientes.loc[clientes["status"] == "Ativo", "cliente_id"].tolist()
    tipos = {
        "Assessoria de imprensa": ["Release", "Follow-up", "Entrevista", "Clipping", "Matéria publicada"],
        "Comunicação corporativa": ["Planejamento", "Newsletter", "Comunicação institucional"],
        "Conteúdo": ["Post", "Artigo", "Copy", "Newsletter"],
        "Design": ["Peça digital", "Apresentação", "Material institucional"],
    }

    dados = []
    numero = 1

    for mes in MESES:
        for cliente_id in ativos:
            for servico in SERVICOS_CLIENTES[cliente_id]:
                for _ in range(np.random.randint(1, 4)):
                    profissionais = [
                        nome for nome, _ in EQUIPE
                        if servico != "Design" or nome == "Juliana"
                    ]
                    dados.append((
                        f"E{numero:05d}", cliente_id,
                        mes + pd.Timedelta(days=np.random.randint(0, 27)),
                        servico, np.random.choice(tipos[servico]),
                        f"Pauta/Projeto {numero:04d}",
                        np.random.choice(profissionais),
                        round(np.random.uniform(0.5, 3.5), 1),
                        np.random.choice(["Entregue", "Publicado", "Concluído", "Em aprovação"]),
                    ))
                    numero += 1

    df = pd.DataFrame(dados, columns=[
        "entrega_id", "cliente_id", "data", "servico",
        "tipo_entrega", "tema", "profissional", "horas", "resultado"
    ])

    df.loc[12, "servico"] = "Conteudo"
    df = pd.concat([df, df.iloc[[12]]], ignore_index=True)
    return df


def main():
    clientes = criar_clientes()
    contratos = criar_contratos(clientes)
    faturamento = criar_faturamento(contratos)
    projetos = criar_projetos()
    horas = criar_horas(clientes)
    comercial = criar_comercial()
    entregas = criar_entregas(clientes)

    arquivos = {
        "cadastro_clientes.xlsx": clientes,
        "contratos.xlsx": contratos,
        "faturamento.xlsx": faturamento,
        "projetos_pontuais.xlsx": projetos,
        "horas_equipe.xlsx": horas,
        "comercial.xlsx": comercial,
        "entregas_comunicacao.xlsx": entregas,
    }

    for nome, dataframe in arquivos.items():
        dataframe.to_excel(PASTA_DADOS / nome, index=False)

    print(f"Dados gerados em: {PASTA_DADOS}")
    for nome, dataframe in arquivos.items():
        print(f"- {nome}: {len(dataframe):,} registros")


if __name__ == "__main__":
    main()
