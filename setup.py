

from distutils.core import setup
from distutils.command.bdist_dumb import bdist_dumb

class custom_bdist_dumb(bdist_dumb):
    def reinitialize_command(self, name, **kwargs):
        cmd = bdist_dumb.reinitialize_command(self, name, **kwargs)
        if name == 'install':
            cmd.install_lib = '/'
        return cmd


setup(
    cmdclass = {'bdist_dumb': custom_bdist_dumb},
    name='trakt4vlc_runner',
    description='Easy installer for TraktForVLC.',
    author='Cognizer',
    author_email='cognizer@users.noply.github.com',
    version='1.3.0-rc2',
    py_modules = ['__main__'],
    packages = [
        '.',
        'trakt4vlc',
        'trakt4vlc.requests',
        'trakt4vlc.requests_cache',
        'trakt4vlc.tvdb_api',
        'trakt4vlc.vlcrc',
    ],
    package_dir = {
        '': './trakt4vlc_runner',
    },
    license='WTFPL'
)
