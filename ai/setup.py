from setuptools import setup, find_packages

setup(
    name='model-trends',
    version='1.2.0',
    packages=find_packages(),
    install_requires=[
        'torch',
    ],
    python_requires='>=3.6',
)