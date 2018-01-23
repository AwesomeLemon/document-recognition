#!/usr/bin/env bash
# Dependencies: OpenCV 3, Scikit, Scipy, Numpy+mkl, Tesseract, pytesseract, jellyfish.
# PIL  <- no? wasn't mentioned in readme documentation
conda install numpy &
# cv2  # install 'opencv' instead
conda install opencv &
conda install -c conda-forge jellyfish &
# Scikit <-- scikit-learn
conda install scikit-learn &
# Scipy
conda install -c anaconda scipy &
# skimage  <- even though not listed in the readme documentation, it threw an error without this.
# hopefully the following installed the correct version:
pip install scikit-image &
# Tesseract
#conda install -c bioconda tesseract &  # DIDNT WORK
#conda install -c simonflueckiger tesserocr ?
# hopefully the following installed the correct version:
pip install tesseract &
# pytesseract
#conda install -c auto pytesseract &  # DIDNT WORK
# hopefully the following installed the correct version:
pip install pytesseract &
# Numpy+mkl
#conda install -c intel/label/deprecated mkl
conda install -c intel mkl
