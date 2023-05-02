import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="png2grm",
    version="0.2.0",
    author="tantanGH",
    author_email="tantanGH@github",
    license='MIT',
    description="PNG to X68k GVRAM format data converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tantanGH/png2grm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'png2grm=png2grm.png2grm:main'
        ]
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    setup_requires=["setuptools"],
    install_requires=["Pillow"],
)
