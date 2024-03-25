from ..entities.stock import Stock
from ..entities.produit import Produit
from ...data.data_stock import Data_stock
from .ifonction_get import Ifonction_get


class Gestion_stock(Ifonction_get):

    def __init__(self):

        self.produit = Produit()
        self.stock = Stock()
        self._data_stock = Data_stock()


    def get_all(self):

        rows = self._data_stock.get_all_stocks()
        stocks=[]
        for row in rows:
            stock={
                'id_stock': row[0],
                'nom_stock': row[1],
            }
            stocks.append(stock)
            print("id:", row[0], "nom du stock:", row[1])
        return stocks

    def get_all_produit(self):

        rows = self._data_stock.get_all_produits()
        produits = []
        for row in rows:
            produit={
                'id_produit': row[0],
                'nom_produit': row[1],
            }
            produits.append(produit)
            print("id:", row[0], "nom du produit:", row[1])
        return produits

    def get_1(self):
        retour = self._data_stock.get_1_stock(self.stock.id)
        rows = retour[1]
        produits = []
        for row in rows:
            produit = {
                'nom_stock': row[1],
                'id_produit': row[2],
                'nom_produit': row[3],
                'quantite_stock': row[4],
            }
            produits.append(produit)
        print(produits)
        return produits

    def get_id(self):

        return self._data_stock.get_id_stock(self.stock.nom)[0]



    def get_stock_1_produit(self):

        row=self._data_stock.get_stock_1produit(self.produit.id)
        print("id_stock:", row[0], "nom_stock:", row[1], ":", "id_produit:", row[2], "nom_produit:", row[3],
              "quantite en stock:", row[4])

    def get_1_produit(self,premieres_lettres):

        rows=self._data_stock.get_1_produit(premieres_lettres)
        for row in rows:
            print("id:", row[0], "nom:", row[1])

    def ajouter_quantite_stock(self,nombre_ajoute):

        self._data_stock.ajouter_quantite_stock(nombre_ajoute,self.produit.id)

    def retirer_quantite_stock(self, nombre_retire,id_produit):

        self._data_stock.retirer_quantite_stock(nombre_retire,id_produit)


    def add_produit_stock(self):

        self._data_stock.add_produit_stock(self.produit.nom,self.stock.id,self.produit.quantite_en_stock)

    def delete_produit_stock(self):
        self._data_stock.delete_produit_stock(self.produit.id)



    def update_quantity(self):
        self._data_stock.update_quantity(self.produit.quantite_en_stock,self.produit.id)

