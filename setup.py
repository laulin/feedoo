from setuptools import setup, find_packages
 
setup(name='feedo',
    version='0.1.0',
    url='https://github.com/laulin/feedo',
    license='GPLV3',
    author='Laurent MOULIN',
    author_email='gignops@gmail.com',
    description='General purpose data processor',
    packages=find_packages(exclude=['tests']),
    install_requires=["rethinkdb", "chronyk", "inotify", "pyyaml", "fluentbit-server-py"],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: GNU GPL V3 License",
       "Operating System :: OS Independent",
    ],
    python_requires='>=3',
      entry_points={
            'console_scripts': [ 
            'feedo = feedo.feedo:main' 
            ] 
      }
)