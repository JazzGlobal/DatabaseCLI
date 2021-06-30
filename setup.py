from setuptools import setup
import src

setup(
    name='DatabaseCLI',
    version='0.0.1',
    py_modules=['DatabaseCLI'],
    install_requires=[
        'Click',
        'pythonnet'
    ],
    entry_points={
        'console_scripts': [
            'get_databases = src.database.database:get_databases',
            'backup = src.database.database:backup_databases',
        ],
    },
)
