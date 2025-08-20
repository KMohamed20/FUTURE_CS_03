# 🔐 Security Overview - FUTURE_CS_03

## Architecture
Le système est un portail web simple permettant le téléversement et le téléchargement de fichiers, avec chiffrement côté serveur.

## Chiffrement
- **Algorithme** : AES-256 en mode GCM (authentifié)
- **Dérivation de clé** : PBKDF2 avec SHA-256, 100 000 itérations
- **Sel (salt)** : 16 octets aléatoires
- **Intégrité** : Tag d'authentification (16 octets)

## Sécurité
- Le fichier original n'est jamais stocké en clair
- Le fichier chiffré est supprimé après téléchargement
- Aucune sauvegarde ou journalisation du mot de passe
- Protection contre les attaques par dictionnaire grâce à PBKDF2

## Recommandations
- Utiliser des mots de passe forts
- Ne pas partager le lien de téléchargement
- Vérifier l'intégrité du fichier après déchiffrement
