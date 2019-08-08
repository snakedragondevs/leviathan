from setuptools import setup

setup(
    name='leviathan',
    version='0.1.0',
    packages=['leviathan', 'leviathan.network'],
    install_requires=('enum34', 'protobuf', 'twisted'),
    entry_points={
        'console_scripts': [
            'leviathan = leviathan.__main__:main'
        ]
    }
)
