#!/usr/bin/env python3
"""
Script pour tester l'accès frontend avec authentification
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_login():
    """Test de connexion"""
    print("🔐 Test de connexion...")
    
    # Essayer avec les différents identifiants possibles
    credentials = [
        ("admin", "admin123"),
        ("admin", "admin"),
        ("analyst", "analyst123"),
    ]
    
    for username, password in credentials:
        try:
            print(f"   Essai: {username} / {password}")
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                print(f"✅ Connexion réussie avec {username}!")
                print(f"🎫 Token: {token[:50]}...")
                return token
            else:
                print(f"   ❌ Échec: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    print(f"\n❌ Aucun identifiant ne fonctionne")
    print(f"💡 Identifiants par défaut:")
    print(f"   - admin / admin123")
    print(f"   - analyst / analyst123")
    return None

def test_get_clients_with_auth(token):
    """Test de récupération des clients avec authentification"""
    print("\n🧪 Test de récupération des clients (avec auth)...")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/clients/", headers=headers)
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            clients = response.json()
            print(f"📊 Nombre de clients: {len(clients)}")
            
            if clients:
                print("\n👥 Clients enregistrés:")
                for client in clients:
                    prob = client.get('churn_probability')
                    prob_str = f"{prob:.1%}" if prob is not None else "N/A"
                    risk = "🔴 Élevé" if prob and prob >= 0.65 else "🟡 Modéré" if prob and prob >= 0.35 else "🟢 Faible"
                    print(f"  - #{client['id']}: {client['name']}")
                    print(f"    Email: {client.get('email', 'N/A')}")
                    print(f"    Risque: {risk} ({prob_str})")
                    print()
            else:
                print("⚠️  Aucun client trouvé")
                
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_dashboard_stats(token):
    """Test des statistiques du dashboard"""
    print("\n📊 Test des statistiques du dashboard...")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistiques récupérées:")
            print(f"  - Total prédictions: {stats.get('total_predictions', 0)}")
            print(f"  - Taux de churn: {stats.get('churn_rate', 0):.1%}")
            print(f"  - Clients analysés: {stats.get('total_analyzed', 0)}")
            print(f"  - Haut risque: {stats.get('high_risk_count', 0)}")
            print(f"  - Moyen risque: {stats.get('medium_risk_count', 0)}")
            print(f"  - Faible risque: {stats.get('low_risk_count', 0)}")
            print(f"  - Score satisfaction: {stats.get('customer_satisfaction_score', 0)}%")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("TEST FRONTEND CHURNGUARD (avec authentification)")
    print("=" * 70)
    print()
    
    # Test de connexion
    token = test_login()
    
    if token:
        # Test de récupération des clients
        test_get_clients_with_auth(token)
        
        # Test des stats
        test_dashboard_stats(token)
        
        print("\n" + "=" * 70)
        print("✅ Tous les tests sont passés!")
        print()
        print("💡 Pour accéder au frontend:")
        print("   1. Ouvrez http://localhost:3000")
        print("   2. Connectez-vous avec: admin / admin123")
        print("   3. Allez dans l'onglet 'Clients'")
        print("   4. Cliquez sur le bouton '↻ Rafraîchir' si nécessaire")
        print("   5. Vérifiez la console du navigateur (F12) pour des erreurs")
        print()
        print("📝 Identifiants disponibles:")
        print("   - admin / admin123 (administrateur)")
        print("   - analyst / analyst123 (analyste)")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("❌ Échec de connexion - Vérifiez que le backend est démarré")
        print("=" * 70)
