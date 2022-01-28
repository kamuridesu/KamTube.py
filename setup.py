from setuptools import setup, find_packages


setup(
    name='KamTube',
    version='0.1.1',
    license='MIT',
    author="Kamuri Amorim",
    author_email='myk.gata14@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/kamuridesu/KamTube.py',
    keywords='youtube ytbtrom downloader invidious api', 
    install_requires=[
          'requests',
          'beautifulsoup4',
    ],
)