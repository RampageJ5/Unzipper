from setuptools import setup

setup(
    name='Assignment_Unzipper',
    version='0.1',  # Consider syncing this version with the metadata version inside the script
    description='Utility to unzip and organize the Canvas submissions download',
    author='Jay Annadurai',
    scripts=['Unzipper.py'],  # Assuming you've named the provided script as 'canvas_unzipper.py'
    install_requires=[ ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Educators',  # Update as appropriate
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',  # Choose an appropriate license or omit if not applicable
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
