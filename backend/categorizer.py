from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

class CategorizadorIA:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.modelo = MultinomialNB()
        self.treinado = False

    def treinar(self):
        dados_treino = [
            # Transporte
            ("uber", "Transporte"),
            ("99", "Transporte"),
            ("taxi", "Transporte"),
            ("onibus", "Transporte"),
            ("metro", "Transporte"),
            ("gasolina", "Transporte"),
            ("combustivel", "Transporte"),
            ("estacionamento", "Transporte"),
            
            # Alimentação
            ("ifood", "Alimentação"),
            ("rappi", "Alimentação"),
            ("restaurante", "Alimentação"),
            ("lanche", "Alimentação"),
            ("pizza", "Alimentação"),
            ("supermercado", "Alimentação"),
            ("padaria", "Alimentação"),
            ("mercado", "Alimentação"),
            ("almoço", "Alimentação"),
            ("jantar", "Alimentação"),
            ("café", "Alimentação"),
            
            # Assinaturas
            ("netflix", "Assinaturas"),
            ("spotify", "Assinaturas"),
            ("amazon prime", "Assinaturas"),
            ("youtube premium", "Assinaturas"),
            ("disney", "Assinaturas"),
            ("hbo", "Assinaturas"),
            ("apple music", "Assinaturas"),
            
            # Saúde
            ("farmacia", "Saúde"),
            ("drogaria", "Saúde"),
            ("remedio", "Saúde"),
            ("medico", "Saúde"),
            ("hospital", "Saúde"),
            ("consulta", "Saúde"),
            ("exame", "Saúde"),
            
            # Moradia
            ("aluguel", "Moradia"),
            ("condominio", "Moradia"),
            ("luz", "Moradia"),
            ("energia", "Moradia"),
            ("agua", "Moradia"),
            ("internet", "Moradia"),
            ("gas", "Moradia"),
            
            # Receitas
            ("salario", "Salário"),
            ("salário", "Salário"),
            ("vencimento", "Salário"),
            ("pagamento", "Salário"),
            ("freelance", "Freelance"),
            ("freela", "Freelance"),
            ("bico", "Freelance"),
            ("extra", "Freelance"),
            ("investimento", "Investimentos"),
            ("rendimento", "Investimentos"),
            ("dividendo", "Investimentos"),
        ]

        descricoes = [d[0] for d in dados_treino]
        categorias = [d[1] for d in dados_treino]

        X = self.vectorizer.fit_transform(descricoes)
        self.modelo.fit(X, categorias)
        self.treinado = True

    def categorizar(self, descricao: str) -> str:
        if not self.treinado:
            self.treinar()

        descricao_lower = descricao.lower()
        X = self.vectorizer.transform([descricao_lower])
        categoria = self.modelo.predict(X)[0]

        return categoria

categorizador = CategorizadorIA()