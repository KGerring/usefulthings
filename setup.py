import setuptools

setuptools.setup(
    name="usefulthings",
    version="0.1.0",
    url="https://github.com/bKGerring/usefulthings",

    author="Kristen Gerring",
    author_email="kgerring@gmail.com",

    description="usefulthings I use frequently (meant for private use)",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
