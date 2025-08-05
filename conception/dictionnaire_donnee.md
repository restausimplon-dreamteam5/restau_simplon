# Dictionnaire de Données - RestauSimplon
## Entité : user

| Champ            | Type          | Description|  Contraintes|  Exemple |
| --------------- |---------------| -----| -----|-----|
| id                |    uuid     |  Identification unique | PK   |  e582aa43347a4e7fa994510fdd0ad486 |
| email | string            |   Adresse email de connexion | unique, non nul, format email | use@gmail.com |
| nom | string         |    Nom de l'utilisateur | non nul | Maurel |
| prenom | string       |    Prenom de l'utilisateur| non nul | Julien |
| telephone | string         |    Numero de téléphone de l'utilisateur| non nul | 0612834822
| adresse | string       |    Adresse de l'utilisateur| optionnel| 12 rue des Plantes |
| mot_de_passe | string         |    Mot de passe hashé | non nul | $2bfkekk... |
| created_at  | datetime         |    Date de création du compte | auto     | 2025-06-02T12:30 |

## Entité : role
| Champ            | Type          | Description|  Contraintes|  Exemple |
| id                |    uuid     |  Identification unique | PK   |  e582aa43347a4e7fa994510fdd0ad486 |
| role  | string          |    Role de l'utilisateur | Enum (admin, employe, client) | admin |
## Entité : article

| Champ            | Type          | Description|  Contraintes|  Exemple |
| --------------- |---------------| -----| -----|-----|
| id                |    uuid     |  Identification unique | PK   |  e582aa43347a4e7fa994510fdd0ad486 |
| nom | string         |    Nom de l'article | non nul | Couscous  |
| prix | decimal       |    Prix TTC de l'article | > 0, non null, décimal (8,2)| Julien|
| categorie | string         |    Categorie du plat| non null | Dessert|
| description| text      |    Detail de l'article| facultatif | frites maison, légumes ...|
| stock | int         |    Quantité disponible en stock| >= 0, non nul | 50|

## Entité : commande
| Champ            | Type          | Description|  Contraintes|  Exemple|
| --------------- |---------------| -----| -----|-----|
| id                |    uuid     |  Identification unique | PK   |  e582aa43347a4e7fa994510fdd0ad486|
| Statut | string         |    Etat de la commande | Enum : en preparation, prête et servie | en preparation|
| date_commande | datetime       |    Date de la création de la commande | auto, non nul| 2025-06-02T12:30|

## Entité : detail_commande
| Champ            | Type          | Description|  Contraintes|  Exemple|
| --------------- |---------------| -----| -----|-----|
| id                |    uuid     |  Identification unique | PK   |  e582aa43347a4e7fa994510fdd0ad486|
| quantite commandé | string         |    Quantité commandé| >1, non nul| 2|
| prix_unitaire | float       |    prix unitaire de l'article à la date de commande | > 0, non null, décimal (8,2) | 12.5|
