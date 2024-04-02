from setuptools import find_packages
from cx_Freeze import setup, Executable


options = {
    'build_exe': {
        'includes': [
            'cx_Logging', 'idna',
        ],
        'packages': [
            'asyncio', 'flask', 'jinja2', 'dash', 'waitress', 'dash_iconify', 'dash_bootstrap_components', 'dash_extensions'
        ],
        'excludes': ['tkinter']
    }
}

executables = [
    Executable('server.py',
               base='console')
]

setup(
    name='logistic_calculator',
    packages=find_packages(),
    version='0.0.1',
    description='alpha',
    executables=executables,
    options=options
)