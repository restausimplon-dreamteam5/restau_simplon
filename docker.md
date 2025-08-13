Créer le volume
```sh
docker volume create restau-simplon
```

Créer la base de donnée
```sh
docker run -d --name restau-simplon-db -p 5433:5432 -e POSTGRES_PASSWORD=admin -v restau-simplon:/var/lib/postgresql/data postgres:17-alpine3.22 
```

Comme on utilise un volume on pourrait créer un autre postgres qui utilise lui aussi ce volume.
Les 2 db auraient alors la même base de données. (A vos risques et périls)

Créer et Alimenter la base de donnée à la main

```sh
# Avoir un fichier .env avec l'URI de la DB 
alembic upgrade head
python app/database.py
```

Contruire l'image de l'api

```sh 
docker build -t ghcr.io/restausimplon-dreamteam5/restau-simplon-api:0.0.1 .
```

Lancer l'api

```sh
docker run -d --name api-restau -p 8000:8000 ghcr.io/restausimplon-dreamteam5/restau-simplon-api:0.0.1
```

Mettre l'image sur github

```sh
docker login ghcr.io -u thomas-lefloch -p {password}
docker build -t ghcr.io/restausimplon-dreamteam5/restausimplon-app:0.0.1 .
docker push ghcr.io/restausimplon-dreamteam5/restausimplon-app:0.0.1
docker pull ghcr.io/restausimplon-dreamteam5/restausimplon-app:0.0.1
```

Lancer docker compose (en précisant le fichier yaml à utiliser)
```sh
docker compose -f compose.test.yaml up
```

Faire communiquer les docker avec un network
```sh
docker network create bla
docker network connect bla {nom_conteneur}
docker run --network bla {nom_conteneur}
```
Profit $$$
