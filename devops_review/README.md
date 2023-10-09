# Documentación y ejecucion:

Proceso de creación de la imagen de docker:

### 
1. Para poder crear una imagen de docker, es necesario ejecutar este comando: 
```
docker build -t “image-name”:”tag” .
```
dónde “image-name” representa el nombre que le vamos a asignar a la imagen y “tag” es el tag con el cual la imagen se va a crear, luego el . al final indica, que para la creación de esta imagen, se tiene que usar el archivo Dockerfile del directorio actual. Es importante que al momento de ejecutar este comando, estemos posicionados en el directorio que contiene el Dockerfile, caso contrario, tendremos un error.
Para este caso, el comando es el siguiente:
```
docker build -f <path/to/Dockerfile> -t “image-name”:”tag” .
```

2. Una vez que creamos la imagen, podemos ejecutarlo de dos formas:
```
docker run -p 8080:8080 -d nombre-de-tu-imagen:etiqueta
```
Donde lo que hacemos con este comando es levantar un contenedor que tenga expuesto el puerto 8080, o bien:
```
docker-compose up -d
```
En este otro caso, estamos ejecutando el archivo docker-compose.yml, que va a levantar al igual que el comando anterior la aplicación exponiendo en puerto que se indica en su configuración.

3. El paso 2, nos sirve para poder probar la aplicación de manera local, ahora bien, queremos llevarla a k8s, entonces, tenemos que ejecutar el siguiente comando:
```
docker push “image-name”:”tag”
```
Con este comando, cargamos la imagen en el registro de contenedores.

4. Como último paso, ejecutamos el apply de kubectl para deployar en k8s.
```
kubectl apply -f deployment.yml
```
esto, es así si no encontramos dentro de la carpeta que contiene el archivo deployment.yml, de otra manera seria:
```
kubectl apply -f devops_review/deployment.yaml
```

Como se podrá ver, en el archivo deployment.yml se crean varios recursos, como ser el deployment, service, HPA (escalamiento horizontal de pods) y también el Ingress, que en el caso que implemnte es sencillo, pero en caso de ir a producción, el mismo debería tener una forma similar al ejemplo que dejo a continuación:
```
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: us-core-vmc-ingress
  annotations:
    kubernetes.io/ingress.global-static-ip-name: us-core-vmc-ip
    ingress.gcp.kubernetes.io/pre-shared-cert: "certificado" #este certificado, puede ser uno que se tenga de antemano, o bien uno que provee google.
spec:
  rules:
    - host: us-core-vmc.com.ar
      http:
        paths:
          - backend:
              service:
                name: us-core-vmc-service
                port:
                  number: 80
            path: /*
            pathType: ImplementationSpecific
---
```