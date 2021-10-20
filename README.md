# Geospatial Data Exercise G5

This is a notebook for the fifth lesson of the kaggle course
["Geospatial Analysis"](https://www.kaggle.com/learn/geospatial-analysis)
offered by Alexis Cook and Jessica Li. The main goal of the lesson is
to get used to __Proximity Analysis__, using `geopandas` methods such as
`.distance`, `.contains` or `.within`. We also learn how to use
`.unary_union` to connect multiple `POLYGON`s into one.

------------------------------------------------------------------
## How to run the Demo

1. Load `proximity-analysis.ipynb` to Jupyter Notebook and run, or

2. `> python3 proximity-analysis.py'

------------------------------------------------------------------
## 1. Task

Every year certain amount of toxic chemicals are accidentally
released to the environment by industrial facilities and others. 
Check if at least one monitoring station exists
within 2 miles of such events, using the historical record.
The information will be used to make a decision where to set up next
monitoring stations to fully cover the potential emission events.

------------------------------------------------------------------
## Directory Tree
```
.
├── LICENSE
├── README.md
├── html
│   ├── m_1.html
│   ├── m_1b.html
│   ├── m_2.html
│   ├── m_2b.html
│   ├── p_1.html
│   ├── p_2.html
│   ├── p_3.html
│   └── p_4.html
├── kaggle_geospatial
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   └── kgsp.cpython-38.pyc
│   └── kgsp.py
├── proximity-analysis.ipynb
├── proximity-analysis.py
└── requirements.txt

```
* `html` directory in the repo is intentionally kept empty. It will be
   filled when the Python demo ran successfully. 
* kgsp is a python module that contains functions used in the exercise. 
------------------------------------------------------------------
END

