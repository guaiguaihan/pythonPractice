from subprocess import call
from pip._internal.utils.misc import get_installed_distributions

call('pip list --outdated',shell=True)
for dist in get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
