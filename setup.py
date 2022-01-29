from setuptools import setup, find_packages

with open("README.md","r") as ld:
    long_description = ld.read()

setup(
    name = "velocitycorrelation2D",
    version = "1.1.0",
    author = "Liam Bailey",
    author_email = "bailey.liam102@gmail.com",
    description = "Implementation of the velocity correlation algorithm used in ‘Self-concentration and Large-Scale Coherence in Bacterial Dynamics’, Dombrowski et al; ‘Cytoplasmic streaming in Drosophilia oocytes with kinesin activity and correlates with the microtubule cytoskeleton architecture’, Ganguly et al.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/LiamABailey/2DVelocityCorrelation",
    project_urls = {
        "Issues": "https://github.com/LiamABailey/2DVelocityCorrelation/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(exclude=('tests','READMEAssets')),
    install_requires = ["pandas>=1.1.*","numpy>=1.1.*"],
    python_requires = ">=3.7"
)
