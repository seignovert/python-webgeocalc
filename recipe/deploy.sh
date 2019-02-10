#!/bin/bash

if [[ "$TRAVIS_OS_NAME" == "osx" ]]
then
    export OS=MacOSX
else
    export OS=Linux
fi

# Download Miniconda3 (latest)
wget https://repo.continuum.io/miniconda/Miniconda3-latest-$OS-x86_64.sh -q -O $HOME/miniconda.sh

# Install
bash $HOME/miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r

# Add conda-build and anaconda-client
conda install -q -y conda-build anaconda-client

# Build recipe and upload it to anaconda cloud
conda build recipe/ --token $CONDA_TOKEN --user $USERNAME
