# PerfumeRecommendations

This project has been developed for the course Knowledge Technology Practical
at the University of Groningen. It is a perfume recommendation system created
together with the expert knowledge of the [Perfume Lounge](https://www.https://www.perfumelounge.nl/).

## Requirements
For the requirements, please take a look at the requirements.txt file.

In an IDE like PyCharm, you should be able to install all requirements in one go
by going to the file and clicking on the popup 'install requirements'.

If you are not using an IDE, you could try the following:

```
pip install -r requirements.txt --no-index
```

Note that cx-Freeze is only used by the standalone create_executable.py.
If you want to speed up the installation and are not
creating an executable, you could remove this package from the list.

## Executable
Create an executable on Windows by running: 

```
python create_executable.py build
```
