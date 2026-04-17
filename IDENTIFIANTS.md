# 🔐 Identifiants ChurnGuard

## Identifiants par défaut

### Administrateur
- **Username** : `admin`
- **Password** : `admin123`
- **Rôle** : Administrateur (accès complet)

### Analyste
- **Username** : `analyst`
- **Password** : `analyst123`
- **Rôle** : Analyste (accès lecture/analyse)

## 🚀 Connexion

### Via le Frontend
1. Ouvrir http://localhost:3000
2. Entrer les identifiants
3. Cliquer sur "Se connecter"

### Via l'API (pour tests)
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Réponse :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 🔧 Modifier les identifiants

Les identifiants sont définis dans :
`ChurnGuard/backend/app/routes/auth.py`

```python
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "analyst": {"password": "analyst123", "role": "analyst"},
}
```

Pour ajouter un utilisateur :
```python
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "analyst": {"password": "analyst123", "role": "analyst"},
    "nouveau_user": {"password": "motdepasse", "role": "analyst"},
}
```

## 🔒 Sécurité

⚠️ **Important** : Ces identifiants sont pour le développement uniquement !

Pour la production :
1. Utiliser une base de données pour stocker les utilisateurs
2. Hasher les mots de passe (bcrypt, argon2)
3. Utiliser des mots de passe forts
4. Implémenter une gestion des rôles plus robuste
5. Ajouter une limitation des tentatives de connexion

## 🎫 Token JWT

- **Durée de validité** : 8 heures
- **Algorithme** : HS256
- **Secret** : Défini dans `SECRET_KEY` (variable d'environnement ou valeur par défaut)

Le token est automatiquement inclus dans toutes les requêtes API après connexion.

## 🧪 Test de connexion

```bash
cd ChurnGuard
python test_frontend.py
```

Ce script teste automatiquement les identifiants et affiche le token JWT.

## ❓ Problèmes courants

### "Incorrect username or password"
- Vérifier que vous utilisez `admin123` et non `admin`
- Vérifier qu'il n'y a pas d'espaces avant/après
- Vérifier que le backend est bien démarré

### Token expiré
- Se déconnecter et se reconnecter
- Le token est valide 8 heures

### 401 Unauthorized sur les requêtes
- Vérifier que le token est bien envoyé dans le header
- Format : `Authorization: Bearer <token>`
- Se reconnecter si le token a expiré
