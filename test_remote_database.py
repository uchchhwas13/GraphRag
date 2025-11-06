from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

uri = os.getenv("NEO4J_URL")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

print(f"Attempting to connect to: {uri}")
print(f"Username: {user}")
print(f"Password: {'*' * len(password) if password else 'NOT SET'}\n")

# Try alternative URI formats if the original fails
alternative_uris = []
if uri:
    base_host = None
    if "neo4j+s://" in uri:
        base_host = uri.replace("neo4j+s://", "")
    elif "neo4j+ssc://" in uri:
        base_host = uri.replace("neo4j+ssc://", "")
    elif "bolt+s://" in uri:
        base_host = uri.replace("bolt+s://", "")
    
    if base_host:
        # Remove port if present
        base_host = base_host.split(":")[0]
        # Try different schemes
        alternative_uris.append(f"neo4j+s://{base_host}")
        alternative_uris.append(f"neo4j+ssc://{base_host}")  # Self-signed cert
        alternative_uris.append(f"bolt+s://{base_host}")
    else:
        alternative_uris.append(uri)
else:
    alternative_uris = [uri]

success = False
driver = None

# Try each URI variant
for uri_variant in alternative_uris:
    if not uri_variant:
        continue
        
    print(f"\n{'='*60}")
    print(f"Trying URI: {uri_variant}")
    print(f"{'='*60}")
    
    # Determine connection config based on URI scheme
    if "+s://" in uri_variant or "+ssc://" in uri_variant:
        # Encrypted schemes handle encryption automatically
        configs = [{}]
    elif "://" in uri_variant:
        # Unencrypted schemes - try with encryption settings
        configs = [
            {"encrypted": True, "trust": "TRUST_SYSTEM_CA_SIGNED_CERTIFICATES"},
            {"encrypted": False},
        ]
    else:
        configs = [{}]
    
    for i, config in enumerate(configs, 1):
        print(f"\n  Attempt {i}/{len(configs)} with config: {config if config else 'default'}")
        
        try:
            driver = GraphDatabase.driver(uri_variant, auth=(user, password), **config)
            
            # Test connection with timeout
            driver.verify_connectivity()
            
            with driver.session() as session:
                result = session.run("RETURN '✅ Connected to Neo4j' AS msg")
                print(f"  {result.single()['msg']}")
                print(f"\n✅ Success! Use this URI in your .env file:")
                print(f"   NEO4J_URL={uri_variant}")
                success = True
                break
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ Failed: {error_msg}")
            if driver:
                try:
                    driver.close()
                except:
                    pass
                driver = None
    
    if success:
        break

if not success:
    print("\n" + "="*60)
    print("🔍 Troubleshooting Tips:")
    print("="*60)
    print("\n1. Check if your AuraDB instance is RUNNING:")
    print("   - Log into https://console.neo4j.io/")
    print("   - Verify your instance status is 'Running' (not Paused)")
    print("   - If paused, click 'Resume' to start the instance")
    print("\n2. Verify the Connection URI format:")
    print("   - For AuraDB: Should be 'neo4j+s://xxxxx.databases.neo4j.io'")
    print("   - NO port number for AuraDB (neo4j+s:// handles routing)")
    print("   - Get the URI from AuraDB console → Connection Details → 'Connection URI'")
    print("\n3. Check credentials:")
    print(f"   - URL: {uri}")
    print(f"   - Username: {user}")
    print(f"   - Password: {'SET (' + str(len(password)) + ' chars)' if password else 'NOT SET'}")
    print("   - Reset password in AuraDB console if needed")
    print("\n4. Network/Firewall issues:")
    print("   - Ensure your network allows outbound connections to *.databases.neo4j.io")
    print("   - Check corporate firewall/VPN settings")
    print("\n5. Try neo4j+ssc:// if having SSL issues:")
    print("   - This uses self-signed certificates")
    print("   - Example: neo4j+ssc://b7de8794.databases.neo4j.io")
    print("\n6. For local Neo4j:")
    print("   - Use: neo4j://localhost:7687 or bolt://localhost:7687")
    print("   - Ensure Neo4j is running: neo4j status")
