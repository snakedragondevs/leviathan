from setuptools import setup

setup(
    name='leviathan',
    version='0.1.0',
    packages=['leviathan', 'leviathan.network'],
    entry_points={
        'console_scripts': [
            'leviathan = leviathan.__main__:main'
        ]
    }
)
