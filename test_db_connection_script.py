# from neo4j import GraphDatabase, basic_auth

# uri = "neo4j+s://b7de8794.databases.neo4j.io"
# user = "neo4j"
# password = "JmaYgn014lSdibCmA8J6vXRMIn5cFVALoRlEmzz_xps"

# driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

# try:
#     with driver.session(database="neo4j") as session:
#         result = session.run("RETURN '✅ Connected to Neo4j Aura!' AS msg")
#         print(result.single()[0])
# except Exception as e:
#     print("❌ Error:", e)
# finally:
#     driver.close()




from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "cefalo2025")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")