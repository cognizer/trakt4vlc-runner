

from setuptools import setup


setup(
    name='trakt4vlc-runner',
    version='1.3.0rc2',
    description='Easy installer for TraktForVLC.',
    long_description='Easy installer for TraktForVLC.',
    author='Cognizer',
    author_email='cognizer@users.noply.github.com',
    url='http://example.org',
    py_modules = ['__main__'],
    zip_safe=True,
    scripts = ['scripts/trakt4vlc'],
    packages = [
        'trakt4vlc_runner',
        'trakt4vlc_runner.trakt4vlc',
        'trakt4vlc_runner.trakt4vlc.requests',
        'trakt4vlc_runner.trakt4vlc.requests_cache',
        'trakt4vlc_runner.trakt4vlc.tvdb_api',
        'trakt4vlc_runner.trakt4vlc.vlcrc',
    ],
    package_dir = {
        'trakt4vlc_runner': 'trakt4vlc_runner',
    },
    install_requires=[
        'requests_cache',
        'requests',
    ],
    license='WTFPL'
)
