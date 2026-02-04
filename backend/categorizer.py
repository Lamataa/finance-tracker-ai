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
            ("uber", "Transporte"),
            ("99", "Transporte"),
            ("taxi", "Transporte"),
            ("onibus", "Transporte"),
            ("metro", "Transporte"),
            ("gasolina", "Transporte"),
            ("combustivel", "Transporte"),
            ("ifood", "Alimentacao"),
            ("restaurante", "Alimentacao"),
            ("lanche", "Alimentação"),
            ("pizza", "Alimentação"),
            ("supermercado", "Alimentação"),
            ("padaria", "Alimentação"),
            ("mercado", "Alimentação"),
            ("netflix", "Assinaturas"),
            ("spotify", "Assinaturas"),
            ("amazon prime", "Assinaturas"),
            ("youtube premium", "Assinaturas"),
            ("disney", "Assinaturas"),
            ("farmacia", "Saúde"),
            ("droga", "Saúde"),
            ("medico", "Saúde"),
            ("hospital", "Saúde"),
            ("aluguel", "Moradia"),
            ("condominio", "Moradia"),
            ("luz", "Moradia"),
            ("agua", "Moradia"),
            ("internet", "Moradia"),
        ]

        descricoes = [d[0] for d in dados_treino]
        categorias = [d[1] for d in dados_treino]

        X = self.vectorizer.fit_transform(descricoes)
        self.modelo.fit(X, categorias)
        self.treinado = True

    def categorizar(self, descricao):
        if not self.treinado:
            self.treinar()

        descricao_lower = descricao.lower()
        X = self.vectorizer.transform([descricao_lower])
        categoria = self.modelo.predict(X)[0]

        return categoria

categorizador = CategorizadorIA()