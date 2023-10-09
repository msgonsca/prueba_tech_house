import subprocess

# comando para realizar el build de la imagen.
subprocess.run(["docker", "build", "-f", "Dockerfile", "-t", "us-core-vmc-image:us-core-vmc-app", "."])

# comando para subir la imagen al registro de contenedores.
subprocess.run(["docker", "push", "us-core-vmc-image:us-core-vmc-app"])

# aplico el manifiesto de k8s.
kubectl_apply = subprocess.run(["kubectl", "apply", "-f", "deployment.yml"])

# verifico que el manifiesto se aplico correctamente.
if kubectl_apply.returncode == 0:
    print("El manifiesto se aplico de manera correcta")
else:
    print("Hay un error en el archivo deployment.yml")