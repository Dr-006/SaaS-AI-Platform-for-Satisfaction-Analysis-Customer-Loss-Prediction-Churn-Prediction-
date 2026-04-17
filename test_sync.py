#!/usr/bin/env python3
"""
Script de test pour vérifier la synchronisation des clients
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_sync_client():
    """Test de l'endpoint de synchronisation"""
    
    # Données de test
    client_data = {
        "name": "Test Client Sync",
        "email": "test.sync@example.com",
        "tenure": 24,
        "monthlyCharges": 75.50,
        "churn_probability": 0.45,
        "churn_prediction": 0
    }
    
    print("🧪 Test de synchronisation client...")
    print(f"📤 Envoi des données: {json.dumps(client_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/clients/sync-from-app1",
            json=client_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"📥 Réponse: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Synchronisation réussie!")
        else:
            print(f"\n❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ Erreur de connexion: {e}")
        print("Assurez-vous que le backend ChurnGuard est démarré sur http://localhost:8000")

def test_get_clients():
    """Test de récupération des clients"""
    print("\n\n🧪 Test de récupération des clients...")
    
    try:
        response = requests.get(f"{BASE_URL}/clients/")
        print(f"✅ Status: {response.status_code}")
        clients = response.json()
        print(f"📊 Nombre de clients: {len(clients)}")
        
        if clients:
            print("\n👥 Clients enregistrés:")
            for client in clients:
                print(f"  - #{client['id']}: {client['name']} (Prob: {client.get('churn_probability', 'N/A')})")
        else:
            print("⚠️  Aucun client trouvé")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE SYNCHRONISATION CHURNGUARD")
    print("=" * 60)
    
    test_sync_client()
    test_get_clients()
    
    print("\n" + "=" * 60)
    print("Tests terminés")
    print("=" * 60)
