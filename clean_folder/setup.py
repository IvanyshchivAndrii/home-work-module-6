from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.0.2',
    description='This package can clen you folder',
    url='https://github.com/IvanyshchivAndrii/home-work-module-6/tree/master/clean_folder/clean_folder',
    author='Ivanyshchiv Andrii',
    author_email='belka04011993@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)