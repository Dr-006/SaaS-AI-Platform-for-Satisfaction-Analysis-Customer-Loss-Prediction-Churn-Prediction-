# Instructions de Vérification - Clients ChurnGuard

## ✅ Le backend fonctionne !

Votre test a montré que :
- ✅ La synchronisation fonctionne
- ✅ Le client est bien enregistré dans la base de données
- ✅ L'API retourne correctement les clients

## 🔍 Vérification Frontend

### Étape 1 : Tester avec authentification
```bash
cd ChurnGuard
python test_frontend.py
```

Ce test va :
1. Se connecter avec admin/admin
2. Récupérer les clients avec le token JWT
3. Afficher les statistiques du dashboard

### Étape 2 : Vérifier dans le navigateur

1. **Ouvrir ChurnGuard**
   - URL : http://localhost:3000
   - Ou le port où tourne votre frontend React

2. **Se connecter**
   - Username : `admin`
   - Password : `admin`

3. **Aller dans l'onglet Clients**
   - Cliquer sur "👥 Clients" dans la sidebar

4. **Vérifier la console du navigateur**
   - Appuyer sur F12
   - Aller dans l'onglet "Console"
   - Chercher des erreurs en rouge

5. **Vérifier l'onglet Network**
   - F12 → Network
   - Rafraîchir la page
   - Chercher la requête `GET /clients/`
   - Vérifier le status (devrait être 200)
   - Vérifier la réponse (devrait contenir vos clients)

## 🐛 Problèmes possibles

### 1. Token JWT expiré
**Symptôme** : Erreur 401 Unauthorized

**Solution** :
- Se déconnecter
- Se reconnecter
- Le token sera régénéré

### 2. CORS Error
**Symptôme** : Erreur CORS dans la console

**Solution** : Vérifier dans `ChurnGuard/backend/app/main.py` :
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:3030"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Frontend non connecté au bon backend
**Symptôme** : Erreur de connexion

**Solution** : Vérifier dans `ChurnGuard/frontend/src/api.js` :
```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000',  // ← Doit correspondre au port du backend
  headers: { 'Content-Type': 'application/json' },
});
```

### 4. Cache du navigateur
**Symptôme** : Anciennes données affichées

**Solution** :
- Ctrl + Shift + R (hard refresh)
- Ou vider le cache du navigateur

## 📋 Checklist de vérification

- [ ] Backend ChurnGuard démarré (port 8000)
- [ ] Frontend ChurnGuard démarré (port 3000 ou autre)
- [ ] Test `python test_sync.py` réussi ✅
- [ ] Test `python test_frontend.py` réussi
- [ ] Connexion au frontend réussie (admin/admin)
- [ ] Onglet Clients accessible
- [ ] Aucune erreur dans la console (F12)
- [ ] Requête GET /clients/ retourne 200
- [ ] Les clients sont visibles dans l'interface

## 🎯 Test complet

### 1. Ajouter un client manuellement dans ChurnGuard
1. Aller dans "Clients"
2. Cliquer sur "+ Ajouter client"
3. Remplir le formulaire :
   - Nom : "Test Manuel"
   - Email : "test@example.com"
   - Ancienneté : 12
   - Charges mensuelles : 50
4. Cliquer sur "Ajouter"
5. Le client devrait apparaître dans la liste

### 2. Analyser un client depuis app1-gestionnaire
1. Ouvrir app1-gestionnaire (http://localhost:3030)
2. Aller dans "Clients"
3. Sélectionner un client
4. Cliquer sur "Analyser App2"
5. Attendre le message de succès
6. Retourner dans ChurnGuard → Clients
7. Cliquer sur "↻ Rafraîchir"
8. Le client devrait apparaître

## 💡 Commandes utiles

### Voir les clients dans la base de données
```bash
cd ChurnGuard/backend
sqlite3 ai_saas.db "SELECT id, name, email, churn_probability FROM clients;"
```

### Supprimer tous les clients (reset)
```bash
cd ChurnGuard/backend
sqlite3 ai_saas.db "DELETE FROM clients;"
```

### Voir les logs du backend en temps réel
```bash
cd ChurnGuard/backend
python -m uvicorn app.main:app --reload --port 8000
```

### Redémarrer le frontend
```bash
cd ChurnGuard/frontend
npm start
```

## 📞 Si le problème persiste

1. **Vérifier les logs du backend**
   - Regarder le terminal où tourne le backend
   - Chercher des erreurs ou warnings

2. **Vérifier la console du navigateur**
   - F12 → Console
   - Noter toutes les erreurs

3. **Tester l'API directement**
   ```bash
   # Sans auth (devrait échouer avec 401)
   curl http://localhost:8000/clients/
   
   # Avec auth
   TOKEN=$(curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin"}' \
     | jq -r '.access_token')
   
   curl http://localhost:8000/clients/ \
     -H "Authorization: Bearer $TOKEN"
   ```

4. **Vérifier que le frontend charge bien les données**
   - Ouvrir F12 → Network
   - Aller dans Clients
   - Vérifier la requête GET /clients/
   - Status devrait être 200
   - Response devrait contenir les clients
