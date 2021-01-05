from setuptools import setup, find_packages
 
setup(name='feedoo_hash',
    version='1.0.0',
    url='https://github.com/laulin/feedoo',
    license='GPLV3',
    author='Laurent MOULIN',
    author_email='gignops@gmail.com',
    description='Plugins for feedoo to hash fields',
    packages=find_packages(exclude=['tests', "etc", "build", "dist", "feedoo.egg-info"]),
    install_requires=["feedoo"],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    python_requires='>=3',
    entry_points={'feedoo.plugins': 'package = feedoo_hash'}
)