# Agente Autônomo - Projeto para Atividade Extra

Estrutura do projeto e instruções rápidas:

- `main.py`: painel principal (menu) do Streamlit.
- `agent.py`: módulo do agente conversacional (usa Gemini).
- `eda_tools.py`: funções utilitárias para EDA (carregar dados, gráficos, etc).
- `report_generator.py`: geração de relatório PDF com ReportLab.
- `insights.py`: geração de conclusões automáticas via Gemini.
- `.streamlit/secrets.toml`: arquivo de segredos (adicione sua chave do Google AI Studio aqui).
- `.devcontainer/`: configuração para VS Code Dev Container.

Para rodar localmente:
1. Preencha `.streamlit/secrets.toml` com sua chave do Google AI Studio.
2. Instale dependências: `pip install -r requirements.txt`
3. Rode: `streamlit run main.py`

Observações:
- Não inclua chaves reais ao enviar o .zip para avaliação pública.
