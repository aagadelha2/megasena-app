from collections import Counter
import random
import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Mega-Sena com Explicação Estatística", page_icon="📊", layout="centered")

@st.cache_data
def carregar_dados_reais():
    # Tenta carregar o CSV real; se não encontrar, gera dados simulados para teste
    try:
        df = pd.read_csv('megasena.csv')
        colunas_bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
        historico = df[colunas_bolas].values.tolist()
        return historico, "Dados reais (megasena.csv)"
    except Exception:
        # Fallback para simulação caso o CSV ainda não tenha sido enviado
        random.seed(42)
        historico_mock = [sorted(random.sample(range(1, 61), 6)) for _ in range(500)]
        return historico_mock, "Dados simulados (demonstração)"

class AnalisadorMegaSenaComMatematica:
    def __init__(self, historico):
        self.historico = historico
        self.total_concursos = len(historico)
        self.todos_numeros = [num for concurso in self.historico for num in concurso]
        self.frequencia = Counter(self.todos_numeros)

    def calcular_atrasos(self):
        """Calcula a inércia (quantos concursos atrás o número foi sorteado por último)."""
        atrasos_reais = {}
        for num in range(1, 61):
            atraso = 0
            for concurso in reversed(self.historico):
                if num in concurso:
                    break
                atraso += 1
            atrasos_reais[num] = atraso
        return atrasos_reais

    def gerar_jogo_com_detalhes(self):
        atrasos = self.calcular_atrasos()
        dados_numeros = []

        for num in range(1, 61):
            freq = self.frequencia.get(num, 0)
            # Probabilidade histórica relativa (frequência / total de aparições possíveis)
            freq_relativa = freq / self.total_concursos
            atraso = atrasos[num]
            
            # Heurística combinada: 30% peso na frequência histórica + 70% peso no atraso
            score = (freq_relativa * 0.3) + (atraso * 0.7)
            dados_numeros.append({
                'numero': num,
                'frequencia': freq,
                'atraso': atraso,
                'score': max(score, 0.01)
            })

        # Extrai listas para amostragem ponderada (Método de Monte Carlo)
        numeros = [d['numero'] for d in dados_numeros]
        pesos = [d['score'] for d in dados_numeros]

        # Sorteio ponderado garantindo 6 números únicos
        jogo_escolhido = []
        while len(jogo_escolhido) < 6:
            candidato = random.choices(numeros, weights=pesos, k=1)[0]
            if candidato not in jogo_escolhido:
                jogo_escolhido.append(candidato)
        
        jogo_escolhido.sort()

        # Mapeia os detalhes matemáticos apenas dos números escolhidos
        detalhes_escolhidos = [d for d in dados_numeros if d['numero'] in jogo_escolhido]
        return jogo_escolhido, detalhes_escolhidos

# --- Interface do Aplicativo ---
st.title("📊 Analisador Estatístico da Mega-Sena")
st.write("Aplicativo combinatório com transparência matemática dos modelos de escolha.")

historico, origem_dados = carregar_dados_reais()
st.caption(f"ℹ️ **Fonte ativa:** {origem_dados} ({len(historico)} concursos processados).")

analisador = AnalisadorMegaSenaComMatematica(historico)

if st.button("Gerar Aposta e Exibir Justificativa Matemática", type="primary", use_container_width=True):
    jogo, detalhes = analisador.gerar_jogo_com_detalhes()
    
    jogo_formatado = " - ".join([f"{n:02d}" for n in jogo])
    st.success("### 🎲 Jogo Sugerido:")
    st.markdown(f"<h2 style='text-align: center; color: #2E7D32;'>{jogo_formatado}</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📐 Memória de Cálculo e Explicação Estatística")
    st.write("Abaixo está a decomposição matemática do porquê cada dezena foi selecionada com base no histórico:")

    # Tabela detalhando a matemática por trás de cada número escolhido
    for d in detalhes:
        with st.expander(f"Número **{d['numero']:02d}** (Score Matemático: {d['score']:.4f})"):
            st.write(f"- **Frequência Histórica:** Apareceu **{d['frequencia']}** vezes no total de {len(historico)} concursos.")
            st.write(f"- **Tempo de Atraso (Inércia):** Está há **{d['atraso']}** concursos consecutivos sem ser sorteado.")
            st.write(f"- **Justificativa do Algoritmo:** O valor combinou a taxa de aparição com a métrica de atraso atual, resultando em uma pontuação de relevância estatística de `{d['score']:.4f}` dentro da amostra ponderada de Monte Carlo.")

    # Métricas gerais do bilhete
    soma = sum(jogo)
    pares = len([n for n in jogo if n % 2 == 0])
    st.info(f"**Panorama do Bilhete:** Soma total das dezenas = **{soma}** | Números Pares: **{pares}** | Números Ímpares: **{6 - pares}**")