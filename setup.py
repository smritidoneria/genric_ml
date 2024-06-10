from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    '''
    this function reads the requirements.txt file and returns the list of requirements
    
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements=[req.replace('\n','') for req in requirements]

        if(HYPHEN_E_DOT in requirements):
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(

    name='mlgenralproject',
        version='0.0.1',
        packages=find_packages(),
        author='Smriti',
        author_email="smritidoneria@gmail.com",
        install_requires=get_requirements('requirements.txt'),
)