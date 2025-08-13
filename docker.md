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
docker build -t restau-simplon-api:test .
```

Lancer l'api

```sh
docker run -d --name api-restau -p 8000:8000 restau-simplon-api:test
```


Profit $$$

TODO: network