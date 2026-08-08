from collections import Counter
import random
import statistics
import streamlit as st

# Configuração da página para ficar com visual agradável no celular
st.set_page_config(
    page_title="Analisador Mega-Sena IA", page_icon="🎲", layout="centered"
)


class AnalisadorMegaSena:

  def __init__(self, historico_concursos):
    self.historico = historico_concursos
    self.total_concursos = len(historico_concursos)
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

  def gerar_jogo_otimizado(self):
    atrasos = self.calcular_atrasos()
    pesos = []
    for num in range(1, 61):
      freq = self.frequencia.get(num, 1)
      atraso = atrasos[num]
      # Heurística: equilibra frequência e tempo de atraso
      score = (freq * 0.4) + (atraso * 0.6)
      pesos.append((num, max(score, 0.1)))

    numeros = [item[0] for item in pesos]
    probabilidades = [item[1] for item in pesos]

    jogo_sugerido = sorted(random.choices(numeros, weights=probabilidades, k=6))
    while len(set(jogo_sugerido)) < 6:
      jogo_sugerido = sorted(random.choices(numeros, weights=probabilidades, k=6))

    return jogo_sugerido


# Interface do Aplicativo no Celular
st.title("🎲 Gerador Estatístico Mega-Sena")
st.write(
    "Aplicativo de análise combinatória e estatística baseado no histórico de"
    " concursos."
)

# Simulando um banco de dados de concursos (ou você pode carregar um arquivo CSV real depois)
@st.cache_data
def carregar_dados():
  random.seed(42)
  return [sorted(random.sample(range(1, 61), 6)) for _ in range(500)]


historico = carregar_dados()
analisador = AnalisadorMegaSena(historico)

# Botão principal otimizado para toque em telas de celular
if st.button("Gerar Jogo Otimizado", type="primary", use_container_width=True):
  jogo = analisador.gerar_jogo_otimizado()
  jogo_formatado = " - ".join([f"{n:02d}" for n in jogo])

  st.success("### Aposta Gerada:")
  st.markdown(
      f"<h2 style='text-align: center; color: #4CAF50;'>{jogo_formatado}</h2>",
      unsafe_allow_html=True,
  )

  # Métricas rápidas da aposta gerada
  soma_jogo = sum(jogo)
  pares = len([n for n in jogo if n % 2 == 0])
  st.info(
      f"**Estatísticas deste jogo:** Soma total = {soma_jogo} | Pares:"
      f" {pares} | Ímpares: {6 - pares}"
  )

st.divider()
st.caption(
    "Dica: Para usar como um app de celular, você pode hospedar este código"
    " gratuitamente no **Streamlit Community Cloud** e acessar o link direto do"
    " seu smartphone."
)
