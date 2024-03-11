from setuptools import find_packages, setup  
setup(
    name = 'advanced_trdng_indicators',
    packages = find_packages(include=['advanced_trdng_indicators']),
    version = '0.1.0',
    description = 'Advanced Trading Indicators',
    author = 'Houssam Zak',
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest==4.4.1'],
    test_suite = 'tests',
    python_requires='>=3.8',
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
    ]
)