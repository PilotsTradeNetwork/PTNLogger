import os
from pathlib import Path
import setuptools
from importlib import util

NAMESPACE = 'ptn'
PACKAGE = 'logger'

here = Path().absolute()
metadata_location = f'{NAMESPACE}.{PACKAGE}._metadata'
spec = util.spec_from_file_location(metadata_location, os.path.join(here, NAMESPACE, PACKAGE, '_metadata.py'))
metadata = util.module_from_spec(spec)
spec.loader.exec_module(metadata)

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name=f'{NAMESPACE}.{PACKAGE}',
    version=metadata.__version__,
    author='Graeme Cruickshank',
    packages=setuptools.find_packages(
        exclude='tests'
    ),
    include_package_data=True,
    install_requires=[],
    license='MIT',
    tests_require=[
        'pytest',
        'mock',
        'coverage'
    ],
    python_requires='>=3.8, <4'
)
