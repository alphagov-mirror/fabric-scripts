from fabric.api import env, run, runs_once, task
from fabric.utils import abort


@task
@runs_once
def fastly_purge(*args):
    "Purge items from Fastly, eg \"/one,/two,/three\". Wildcards not supported."
    if env.environment == 'production':
        hostnames_to_purge = ['www.gov.uk', 'assets.publishing.service.gov.uk']
    elif env.environment == 'staging':
        hostnames_to_purge = ['www.staging.publishing.service.gov.uk', 'assets.staging.publishing.service.gov.uk']

    for path in args:
        if "*" in path:
            abort("Sorry, purging paths containing wildcards is not supported "
                  "(you requested to purge '%s'). "
                  "See https://github.gds/pages/gds/opsmanual/2nd-line/cache-flush.html?highlight=fastly#purging-a-page-from-fastly-with-fabric"
                  % path)
    for govuk_path in args:
        for hostname in hostnames_to_purge:
            run("curl -s -X PURGE {0}{1} | grep 'ok'".format(hostname, govuk_path.strip()))
