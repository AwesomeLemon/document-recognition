# document-recognition
A program for document recognition. 
More info at https://awesomelemon.github.io/2017/01/15/Document-recognition-with-Python-OpenCV-and-Tesseract.html
## Usage
### Arguments
-i, --image, Path to the image to be scanned.

-o, --output, Path for the output text file.

-c, --check, Path to the file with reference text.

-s, --show, Show intermediate results [optional]

### Example
python .\recognize.py -i photos\chom4.jpg -c texts\chom.txt -o output.txt
## Dependencies
OpenCV, Scikit, Scipy, Numpy+mkl, Tesseract, pytesseract, jellyfish.
