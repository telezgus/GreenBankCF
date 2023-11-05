from fabric.api import task

@task(alias='hello')
def hello_world():
    print("Hola Mundo!!")