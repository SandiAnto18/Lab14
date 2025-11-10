from database.DB_connect import DBConnect

from model.order import Order
class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct o.store_id as store from orders o"

        cursor.execute(query)

        for row in cursor:
            results.append(row["store"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllOrdersbyStore(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct * from orders o where o.store_id=%s"""

        cursor.execute(query, (store,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(store, k, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """Select DISTINCT 
    o1.order_id as id1,           -- Seleziona l'ID dell'ordine più recente e lo chiama 'id1'
    o2.order_id as id2,           -- Seleziona l'ID dell'ordine precedente e lo chiama 'id2'
    count(oi.quantity + oi2.quantity) as cnt  -- Conta la somma delle quantità degli articoli di entrambi gli ordini
from 
    orders o1,                    -- Prima tabella di ordini (più recente)
    orders o2,                    -- Seconda tabella di ordini (più vecchio)
    order_items oi,               -- Tabella dei dettagli degli articoli dell'ordine o1
    order_items oi2               -- Tabella dei dettagli degli articoli dell'ordine o2
where 
    o1.store_id=%s                -- Considera solo gli ordini del negozio specificato (%s è un placeholder)
    and o1.store_id=o2.store_id   -- Entrambi gli ordini devono appartenere allo stesso negozio
    and o1.order_date > o2.order_date   -- o1 è più recente di o2 (ordine cronologico)
    and oi.order_id = o1.order_id       -- Collega i dettagli degli articoli al primo ordine
    and oi2.order_id  = o2.order_id    -- Collega i dettagli degli articoli al secondo ordine
    and DATEDIFF(o1.order_Date, o2.order_date) < %s  -- Considera solo ordini entro un certo intervallo di giorni
group by 
    o1.order_id, o2.order_id      -- Raggruppa i risultati per coppia di ordini (o1, o2)
	"""

        cursor.execute(query, (store,k))

        for row in cursor:
            results.append((idMap[row["id1"]],idMap[row["id2"]], row["cnt"]))

        cursor.close()
        conn.close()
        return results