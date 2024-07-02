import setuptools


setuptools.setup(
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True,
)
