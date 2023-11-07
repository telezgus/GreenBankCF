from fabric.api import local, cd, run, env, prefix, sudo

env.user = 'gus'
env.hosts = ['146.190.175.201']


def make_deploy(commit=''):
    local('git add .')
    local(f'git commit -m "{commit}"')
    local('git push origin main')
    deploy()
    
    
def deploy():
    with cd('/home/gus/project/GreenBankCF'):
        run('git pull')
        with prefix('source env/bin/activate'):
            run('pip install -r requirements.txt')
            run('pyrhon manage.py migrate')
        sudo('sytemctl restart banco_cf')
        sudo('sytemctl restart nginx')
        sudo('sytemctl restart redis')
        sudo('sytemctl restart celery')
        sudo('sytemctl restart celerybeat')