# Finance Tracker com IA

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-F7931E?logo=scikitlearn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

**Sistema de controle financeiro com categorização automática baseada em Machine Learning**

[Demo Online](https://finance-tracker-ai-1-r9sn.onrender.com/)

---

## Visão Geral

Finance Tracker é uma aplicação web full-stack que implementa algoritmos de Machine Learning para automatizar a categorização de transações financeiras. O sistema utiliza processamento de linguagem natural (NLP) para classificar despesas e receitas, eliminando a necessidade de input manual de categorias.

### Problema Resolvido

Aplicativos tradicionais de controle financeiro exigem categorização manual de transações, processo que consome tempo e é propenso a erros. Este projeto automatiza essa tarefa através de um modelo treinado de classificação de texto.

### Solução Técnica

- **Backend**: API REST desenvolvida em FastAPI com validação de dados e documentação automática
- **Machine Learning**: Modelo de classificação Multinomial Naive Bayes com vetorização TF-IDF
- **Frontend**: Interface responsiva com visualização de dados em tempo real
- **Deploy**: Arquitetura serverless em produção

---

## Screenshots

### Interface Principal
<img width="1904" height="992" alt="image" src="https://github.com/user-attachments/assets/bd477ee4-79cb-4613-a66d-0c677df3495f" />

### Visualização de Dados
<img width="1906" height="992" alt="image" src="https://github.com/user-attachments/assets/9f7684a7-d634-42ca-ab58-65fb215c2281" />

---

## Funcionalidades Principais

### Categorização Inteligente

O modelo analisa a descrição da transação e prediz a categoria apropriada:

| Input | Output | Confiança |
|-------|--------|-----------|
| "Uber pra casa" | Transporte | 95% |
| "iFood pizza" | Alimentação | 95% |
| "Netflix" | Assinaturas | 98% |
| "Farmácia São Paulo" | Saúde | 90% |

### Dashboard Analítico

- Visualização de saldo, receitas e despesas
- Gráficos de distribuição por categoria
- Histórico completo de transações
- Interface responsiva (desktop e mobile)

### API RESTful

- Endpoints CRUD completos
- Validação de schema com Pydantic
- Documentação OpenAPI/Swagger automática
- CORS configurado para integração frontend

---

## Stack Tecnológica

### Backend

- **FastAPI 0.104**: Framework Python assíncrono de alta performance
- **SQLAlchemy 2.0**: ORM para persistência de dados
- **Pydantic 2.5**: Validação de dados e serialização
- **Scikit-learn 1.3**: Biblioteca de Machine Learning
- **SQLite**: Banco de dados relacional

### Frontend

- **HTML5/CSS3**: Estrutura e apresentação
- **JavaScript ES6+**: Lógica do cliente
- **Tailwind CSS 3.0**: Framework CSS utilitário
- **Chart.js 4.0**: Biblioteca de visualização de dados

### Machine Learning

- **TF-IDF Vectorizer**: Conversão de texto em features numéricas
- **Multinomial Naive Bayes**: Algoritmo de classificação probabilística
- **Categorias**: 6 classes predefinidas (Transporte, Alimentação, Assinaturas, Saúde, Moradia, Outros)

### DevOps

- **Git/GitHub**: Controle de versão
- **Render**: Plataforma de deploy serverless
- **Uvicorn**: ASGI server para produção

---

## Arquitetura do Sistema

### Pipeline de Machine Learning
```
Input (texto)
    ↓
TF-IDF Vectorization
    ↓
Feature Vector
    ↓
Naive Bayes Classifier
    ↓
Categoria Predita
    ↓
Persistência (SQLite)
```

### Processo de Treinamento

1. **Dataset**: 30+ exemplos rotulados manualmente
2. **Pré-processamento**: Normalização de texto e remoção de stopwords
3. **Vetorização**: TF-IDF com vocabulário otimizado
4. **Treinamento**: Naive Bayes com regularização Laplace
5. **Validação**: Acurácia média de 93% em testes

### Categorias Suportadas

- Transporte
- Alimentação
- Assinaturas
- Saúde
- Moradia
- Outros (fallback)

---

## Instalação e Execução

### Pré-requisitos
```
Python >= 3.8
pip >= 21.0
```

### Setup Local

1. Clone o repositório
```bash
git clone https://github.com/SEU-USUARIO/finance-tracker-ai.git
cd finance-tracker-ai
```

2. Instale dependências
```bash
cd backend
pip install -r requirements.txt
```

3. Execute o servidor
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Acesse a aplicação
```
Frontend: Abra frontend/index.html no navegador
API: http://localhost:8000
Docs: http://localhost:8000/docs
```

---

## Uso da API

### Criar Transação

**Request:**
```http
POST /despesas/
Content-Type: application/json

{
  "descricao": "Uber pra casa",
  "valor": 25.50,
  "tipo": "despesa",
  "data": "2026-02-04"
}
```

**Response:**
```json
{
  "id": 1,
  "descricao": "Uber pra casa",
  "valor": 25.50,
  "categoria": "Transporte",
  "tipo": "despesa",
  "data": "2026-02-04"
}
```

### Listar Transações

**Request:**
```http
GET /despesas/
```

**Response:**
```json
[
  {
    "id": 1,
    "descricao": "Uber pra casa",
    "valor": 25.50,
    "categoria": "Transporte",
    "tipo": "despesa",
    "data": "2026-02-04"
  }
]
```

### Deletar Transação

**Request:**
```http
DELETE /despesas/{id}
```

---

## Estrutura do Projeto
```
finance-tracker/
│
├── backend/
│   ├── main.py              # Endpoints da API (desenvolvimento)
│   ├── main_deploy.py       # Endpoints da API (produção)
│   ├── models.py            # Schemas Pydantic
│   ├── database.py          # Configuração SQLAlchemy
│   ├── categorizer.py       # Modelo de ML
│   └── requirements.txt     # Dependências Python
│
├── frontend/
│   ├── index.html           # Interface do usuário
│   ├── style.css            # Estilos customizados
│   └── script.js            # Lógica do cliente
│
├── screenshots/             # Documentação visual
├── render.yaml              # Configuração de deploy
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Documentação
```

---

## Decisões Técnicas

### Por que FastAPI?

- Performance superior (baseado em Starlette e Pydantic)
- Validação automática de tipos
- Documentação OpenAPI/Swagger out-of-the-box
- Suporte nativo para async/await

### Por que Naive Bayes?

- Eficiente para classificação de texto
- Baixo custo computacional
- Performance adequada para dataset pequeno
- Rápido para inferência em produção

### Por que SQLite?

- Zero configuração
- Adequado para protótipo/MVP
- Fácil migração para PostgreSQL se necessário
- Performático para escala pequena/média

---

## Métricas de Performance

- **Acurácia do modelo**: ~93%
- **Tempo de resposta API**: <100ms (p95)
- **Tempo de inferência ML**: <10ms
- **Bundle size frontend**: ~150KB

---

## Autor

**Gabriel Lamata**  
Desenvolvedor Full-Stack | Machine Learning Enthusiast

- LinkedIn: https://www.linkedin.com/in/gabriel-pereira-lamata/
- GitHub: https://github.com/Lamataa?tab=repositories
- Email: gabrielpereira.lamata@hotmail.com

---

**Desenvolvido como projeto de portfólio técnico**

