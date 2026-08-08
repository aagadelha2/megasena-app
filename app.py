from collections import Counter
import random
import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Mega-Sena: Caos e Teoria dos Jogos", page_icon="🧬", layout="centered")

@st.cache_data
def carregar_dados_reais():
    try:
        df = pd.read_csv('megasena.csv')
        colunas_bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
        historico = df[colunas_bolas].values.tolist()
        return historico, "Dados reais (megasena.csv)"
    except Exception:
        random.seed(42)
        historico_mock = [sorted(random.sample(range(1, 61), 6)) for _ in range(500)]
        return historico_mock, "Dados simulados (demonstração)"

class AnalisadorAvancadoMega:
    def __init__(self, historico):
        self.historico = historico
        self.total_concursos = len(historico)
        self.todos_numeros = [num for concurso in self.historico for num in concurso]
        self.frequencia = Counter(self.todos_numeros)

    def calcular_atrasos(self):
        atrasos_reais = {}
        for num in range(1, 61):
            atraso = 0
            for concurso in reversed(self.historico):
                if num in concurso:
                    break
                atraso += 1
            atrasos_reais[num] = atraso
        return atrasos_reais

    def calcular_indice_teoria_dos_jogos(self, numero):
        """
        Teoria dos Jogos aplicada: Pessoas tendem a apostar em datas (1 a 31).
        Números > 31 fogem do padrão comportamental humano coletivo, 
        reduzindo a chance de divisão de prêmio (Equilíbrio de Nash prático).
        """
        return 1.2 if numero > 31 else 0.8

    def calcular_fator_caos(self):
        """
        Teoria do Caos: Mede a volatilidade dos últimos sorteios (entropia simples).
        Simula a imprevisibilidade de curto prazo do sistema físico dos globos.
        """
        ultimos_concursos = self.historico[-10:] # Olha os últimos 10
        plana_ultimos = [num for c in ultimos_concursos for num in c]
        variabilidade = len(set(plana_ultimos)) / 60.0 # Razão de dispersão
        return variabilidade

    def gerar_jogo_multidisciplinar(self):
        atrasos = self.calcular_atrasos()
        fator_caos = self.calcular_fator_caos()
        dados_numeros = []

        for num in range(1, 61):
            freq = self.frequencia.get(num, 0)
            freq_relativa = freq / self.total_concursos
            atraso = atrasos[num]
            
            # Peso da Teoria dos Jogos (Evitar o comportamento coletivo previsível)
            peso_jogo = self.calcular_indice_teoria_dos_jogos(num)
            
            # Score unificado: Frequência + Atraso + Ajuste de Teoria dos Jogos + Perturbação do Caos
            # A perturbação do caos introduz um fator estocástico não-linear inspirado no Efeito Borboleta
            perturbacao_caos = random.uniform(0.9, 1.1) * fator_caos
            
            score = ((freq_relativa * 0.2) + (atraso * 0.5) + (peso_jogo * 0.3)) * perturbacao_caos
            
            dados_numeros.append({
                'numero': num,
                'frequencia': freq,
                'atraso': atraso,
                'fator_jogos': peso_jogo,
                'score': max(score, 0.01)
            })

        numeros = [d['numero'] for d in dados_numeros]
        pesos = [d['score'] for d in dados_numeros]

        jogo_escolhido = []
        while len(jogo_escolhido) < 6:
            candidato = random.choices(numeros, weights=pesos, k=1)[0]
            if candidato not in jogo_escolhido:
                jogo_escolhido.append(candidato)
        
        jogo_escolhido.sort()
        detalhes_escolhidos = [d for d in dados_numeros if d['numero'] in jogo_escolhido]
        return jogo_escolhido, detalhes_escolhidos, fator_caos

# --- Interface do Aplicativo ---
st.title("🧬 Analisador Multidisciplinar")
st.subheader("Estatística, Teoria do Caos e Teoria dos Jogos")

historico, origem_dados = carregar_dados_reais()
st.caption(f"ℹ️ **Fonte ativa:** {origem_dados} ({len(historico)} concursos processados).")

analisador = AnalisadorAvancadoMega(historico)

if st.button("Gerar Aposta com Análise Completa", type="primary", use_container_width=True):
    jogo, detalhes, caos = analisador.gerar_jogo_multidisciplinar()
    
    jogo_formatado = " - ".join([f"{n:02d}" for n in jogo])
    st.success("### 🎲 Jogo Sugerido:")
    st.markdown(f"<h2 style='text-align: center; color: #1B5E20;'>{jogo_formatado}</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🔬 Fundamentos Teóricos Aplicados a esta Aposta")
    st.info(f"🌪️ **Índice de Entropia (Teoria do Caos):** O fator de volatilidade recente calculado nos últimos sorteios foi de **{caos:.4f}**, injetando perturbações não-lineares na seleção para simular a imprevisibilidade física dos globos.")

    for d in detalhes:
        perfil_jogos = "Acima de 31 (Favorecido pela Teoria dos Jogos para fugir de datas de aniversário comuns)" if d['numero'] > 31 else "Abaixo de 32 (Faixa de alta densidade de escolha humana coletiva)"
        
        with st.expander(f"Número **{d['numero']:02d}** (Score Ponderado: {d['score']:.4f})"):
            st.write(f"- **Estatística Pura:** Apareceu {d['frequencia']} vezes e está com atraso de {d['atraso']} concursos.")
            st.write(f"- **Teoria dos Jogos (Comportamento):** {perfil_jogos}.")
            st.write(f"- **Teoria do Caos:** Influenciado pela matriz de perturbação estocástica não-linear do sistema.")