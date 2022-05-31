from typing import List
from neo4j import GraphDatabase
import os

class Neo4jDB:
    
    def __init__(self) -> None:
        scheme      = os.getenv('scheme')
        host_name   = os.getenv('host_name')
        port        = os.getenv('port')
        url         = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
        self._database    = os.getenv('database')
        self._driver      = GraphDatabase.driver(url, auth=(os.getenv('user'), os.getenv('password')))

    def __del__(self):
        self._driver.close()
        
    def clean_up_anguix_database(self) -> None:
        delete_query = 'MATCH (n:SabioRKReaction)-[:kineticDatafor]-(k), (n)-[:generalReactionFor]-(r), (k)-[:parameterInfo]->(p) DETACH DELETE n, k, p'

        with self._driver.session() as session:
            session.run(delete_query)
    
    def insert(self, queries: List[str]) -> None:
        
        create = lambda tx, query: tx.run(query)

        with self._driver.session(database=self._database) as session:
            for query in queries:
                session.write_transaction(create, query)
    
    def close(self) -> None:
        self._driver.close()
        