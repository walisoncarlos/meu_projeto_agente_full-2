import streamlit as st
import google.generativeai as genai

def _configure():
    try:
        GOOGLE_API_KEY = st.secrets["general"]["GOOGLE_API_KEY"]
        genai.configure(api_key=GOOGLE_API_KEY)
        return True, None
    except Exception as e:
        return False, e

def run():
    ok, err = _configure()
    if not ok:
        st.error(f"API key não encontrada ou erro ao configurar Gemini: {err}")
        return

    model = genai.GenerativeModel("gemini-1.5-pro")

    if "history" not in st.session_state:
        st.session_state.history = []

    st.subheader("Conversa com o agente")
    # display history
    for i, m in enumerate(st.session_state.history):
        role = m.get('role', 'user')
        content = m.get('content', '')
        if role == 'user':
            st.markdown(f"**Você:** {content}")
        else:
            st.markdown(f"**Agente:** {content}")

    user_input = st.text_area("💬 Digite sua pergunta:", key="user_input_area", height=120, placeholder="Ex: Quais são as colunas numéricas e quais são as mais correlacionadas?")

    cols = st.columns([1,1,1])
    if cols[0].button("Enviar"):
        if not user_input.strip():
            st.warning("Digite uma pergunta antes de enviar.")
        else:
            # append user message to history
            st.session_state.history.append({"role":"user", "content": user_input})
            with st.spinner("Gerando resposta com Gemini..."):
                try:
                    prompt = build_prompt(user_input)
                    response = model.generate_content(prompt)
                    text = response.text if hasattr(response, 'text') else str(response)
                    st.session_state.history.append({"role":"assistant", "content": text})
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {e}")
    if cols[1].button("Limpar histórico"):
        st.session_state.history = []
        st.experimental_rerun()

def build_prompt(user_question: str) -> str:
    # Provide a robust prompt wrapper so the model knows how to answer
    guidance = (
        "Você é um assistente especialista em análise de dados. Responda de forma objetiva, "
        "indique quando você estiver inferindo e, se for pedir cálculos, forneça código Python "
        "aplicável ao pandas. Sempre que possível, sugira um gráfico ou uma tabela."
    )
    return f"{guidance}\n\nPergunta do usuário:\n{user_question}\n\nResponda:"
