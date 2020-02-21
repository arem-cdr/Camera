from setuptools import setup, find_packages
setup(
    name="obelix",
    version="0.1",
    packages=find_packages(),
    scripts=["main.py"],

 
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.yml", "*.npy", "*.txt"]
    },

    # metadata to display on PyPI

    description="Camera Package",
    keywords="camera package",
 

)
