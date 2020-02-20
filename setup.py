from setuptools import setup, find_packages
setup(
    name="Obelix",
    version="0.1",
    packages=find_packages(),
    scripts=["main.py"],

 
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.npy"]
    },

    # metadata to display on PyPI

    description="Camera Package",
    keywords="camera package",
 

)
