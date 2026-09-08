# 🔢 Conjectura de Collatz — App Streamlit

Aplicativo web feito com [Streamlit](https://streamlit.io/) que calcula e
visualiza a **Conjectura de Collatz** (também conhecida como *problema
3n + 1*) para qualquer número inteiro positivo informado pelo usuário.

## O que é a Conjectura de Collatz?

Dado um número inteiro positivo `n`:

- Se `n` é **par**, o próximo número é `n / 2`.
- Se `n` é **ímpar**, o próximo número é `3n + 1`.

Repetindo esse processo, a conjectura afirma que **sempre** se chega ao
número `1`, não importa o número inicial escolhido. Até hoje, isso nunca
foi provado matematicamente para todos os números, mas também nunca foi
encontrado um contraexemplo.

## Funcionalidades do app

- Campo para o usuário digitar qualquer número inteiro positivo.
- Cálculo completo da sequência de Collatz até chegar a 1.
- Métricas resumidas: total de passos, maior valor atingido, quantidade
  de passos pares e ímpares.
- Gráfico de linha mostrando a evolução da sequência (com destaque para
  o pico/maior valor).
- Gráfico opcional em escala logarítmica (útil para números com picos
  muito altos).
- Gráfico de barras comparando passos pares x ímpares.
- Tabela detalhada passo a passo, com a operação aplicada em cada etapa.
- Botão para baixar a sequência completa em CSV.
- Tema escuro customizado via `style.css` e `.streamlit/config.toml`.

## Estrutura do projeto

```
collatz_app/
├── app.py                  # Código principal do Streamlit
├── style.css               # Estilos customizados (CSS)
├── requirements.txt        # Dependências Python do projeto
├── README.md                # Este arquivo
└── .streamlit/
    └── config.toml         # Configuração de tema do Streamlit
```

## Como rodar o projeto

1. **Crie um ambiente virtual (recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o aplicativo:**

   ```bash
   streamlit run app.py
   ```

4. O Streamlit abrirá automaticamente no navegador, geralmente em
   `http://localhost:8501`.

## Exemplos de números para testar

| Número | Total de passos (aprox.) | Observação                        |
|--------|---------------------------|------------------------------------|
| 6      | 8                          | Sequência curta                    |
| 27     | 111                        | Clássico exemplo de sequência longa|
| 97     | 118                        | Também gera uma sequência longa    |
| 871    | 178                        | Bom exemplo de pico alto           |

## Licença

Projeto de uso livre para fins educacionais e de estudo.
