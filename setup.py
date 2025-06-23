from setuptools import setup, find_packages

setup(
    name="sympy-texinfo-patch",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["sphinx>=4.0"],
    python_requires=">=3.7",
)
