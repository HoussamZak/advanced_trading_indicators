from setuptools import setup, find_packages
setup(
name='advTradingIndicators',
version='0.1.0',
author='Houssam Zak',
author_email='houssamzak@gmail.com',
description='Not your usual trading indicators, use with in combination with other indicator, this is not financial advice.',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
install_requires=[
          'numpy',
          'pandas',
          'matplotlib',
      ],
python_requires='>=3.8',
)