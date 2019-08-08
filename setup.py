from setuptools import setup

setup(
    name='leviathan',
    version='0.1.0',
    description='A Minecraft: Bedrock Edition server software written in Python',
    url='https://github.com/snakedragondevs/leviathan',
    author='Clark Dwain Luna',
    author_email='lclarkdwain@outlook.com',
    license='MIT',
    packages=['leviathan', 'tests', 'leviathan.network'],
    install_requires=('enum34', 'protobuf', 'twisted'),
    tests_require=('coverage', 'nose', 'mock'),
    test_suite='nose.collector',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'leviathan = leviathan.__main__:main'
        ]
    }
)
