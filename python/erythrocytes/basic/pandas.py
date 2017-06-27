from pandas import Series, DataFrame
import pandas as pd


# A Series is a one-dimensional array-like object containing an array of data (of any NumPy data type) and an associated array of data labels, called its index. The simplest Series is formed from only an array of data:

s = Series([0.1,3.4,5.6,12])

s
# Out[52]: 
# 0     0.1
# 1     3.4
# 2     5.6
# 3    12.0
# dtype: float64

s.values
# Out[53]: array([  0.1,   3.4,   5.6,  12. ])

s.index
# Out[54]: RangeIndex(start=0, stop=4, step=1)

s2 = Series([0.1,3.4,5.6,12], index = ["a","b","c","d"])

s2.index
# Out[56]: Index([u'a', u'b', u'c', u'd'], dtype='object')

s
# Out[57]: 
# 0     0.1
# 1     3.4
# 2     5.6
# 3    12.0
# dtype: float64

s2
# Out[58]: 
# a     0.1
# b     3.4
# c     5.6
# d    12.0
# dtype: float64

s2[s2>3]
# Out[62]: 
# b     3.4
# c     5.6
# d    12.0
# dtype: float64

s2 * 2
# Out[63]: 
# a     0.2
# b     6.8
# c    11.2
# d    24.0
# dtype: float64

s2 ** 2
# Out[64]: 
# a      0.01
# b     11.56
# c     31.36
# d    144.00
# dtype: float64

np.exp(s2)
# Out[65]: 
# a         1.105171
# b        29.964100
# c       270.426407
# d    162754.791419
# dtype: float64


'b' in s
Out[66]: False

'b' in s2
Out[67]: True


sdata = {"Beijing":12, "Shanghai": 11, "Shenzhen":23}

s3 = Series(sdata)

s3
Out[71]: 
Beijing     12
Shanghai    11
Shenzhen    23
dtype: int64


citys=['Shenzhen', 'Nanjing', 'Beijing']

s4=Series(sdata, index=citys)

s4
Out[81]: 
Shenzhen    23.0
Nanjing      NaN
Beijing     12.0
dtype: float64




s4.isnull()
Out[85]: 
Shenzhen    False
Nanjing      True
Beijing     False
dtype: bool

pd.isnull(s4)
Out[87]: 
Shenzhen    False
Nanjing      True
Beijing     False
dtype: bool

# rename 
s4.index=["A","B","C"]

s4
Out[91]: 
A    23.0
B     NaN
C    12.0
dtype: float64


# Dataframe 
# A DataFrame represents a tabular, spreadsheet-like data structure containing an or- dered collection of columns, each of which can be a different value type (numeric, string, boolean, etc.). 

data = {'city':["BJ", "SH", "SZ"], 'fancy':[1,3,1],'year':['2016','2015','2011']}
data
Out[95]: 
{'city': ['BJ', 'SH', 'SZ'],
 'fancy': [1, 3, 1],
 'year': ['2016', '2015', '2011']}

frame=Dataframe(data)
frame
Out[98]: 
  city  fancy  year
0   BJ      1  2016
1   SH      3  2015
2   SZ      1  2011

#reorder columns
DataFrame(data, columns=['fancy','city','year'])
Out[104]: 
   fancy city  year
0      1   BJ  2016
1      3   SH  2015
2      1   SZ  2011

# frame property

frame.columns
Out[105]: Index([u'city', u'fancy', u'year'], dtype='object')

frame.year
Out[106]: 
0    2016
1    2015
2    2011
Name: year, dtype: object

frame.fancy
Out[107]: 
0    1
1    3
2    1
Name: fancy, dtype: int64

# frame index
frame.ix[1]
Out[113]: 
city       SH
fancy       3
year     2015
Name: 1, dtype: object


# add column with calculate
frame['older']= frame.year >= '2015'

frame
Out[119]: 
  city  fancy  year  older
0   BJ      1  2016   True
1   SH      3  2015   True
2   SZ      1  2011  False

# column <-> index
frame.T
Out[120]: 
          0     1      2
city     BJ    SH     SZ
fancy     1     3      1
year   2016  2015   2011
older  True  True  False

# series reindex
obj = Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])

obj
Out[123]: 
d    4.5
b    7.2
a   -5.3
c    3.6
dtype: float64

obj2 = obj.reindex(['a','b','c','d','e'])

obj2
Out[125]: 
a   -5.3
b    7.2
c    3.6
d    4.5
e    NaN
dtype: float64

obj.reindex(['a','b','c','d','e'], fill_value=0)
Out[126]: 
a   -5.3
b    7.2
c    3.6
d    4.5
e    0.0
dtype: float64

# dataframe reindex
frame2=DataFrame(np.arange(9).reshape(3,3), columns=['Ohio', 'Texas', 'California'],index=['a', 'c', 'd'])

frame2
Out[135]: 
   Ohio  Texas  California
a     0      1           2
c     3      4           5
d     6      7           8

frame3=frame2.reindex(['a','b','c','d'])

frame3
Out[137]: 
   Ohio  Texas  California
a   0.0    1.0         2.0
b   NaN    NaN         NaN
c   3.0    4.0         5.0
d   6.0    7.0         8.0


#filter 
data = DataFrame(np.arange(16).reshape((4, 4)),index=['Ohio', 'Colorado', 'Utah', 'New York'],columns=['one', 'two', 'three', 'four'])

data
Out[145]: 
          one  two  three  four
Ohio        0    1      2     3
Colorado    4    5      6     7
Utah        8    9     10    11
New York   12   13     14    15





data <5
Out[146]: 
            one    two  three   four
Ohio       True   True   True   True
Colorado   True  False  False  False
Utah      False  False  False  False
New York  False  False  False  False

data[data['three']<5]
Out[147]: 
      one  two  three  four
Ohio    0    1      2     3

data[data['three']<8]
Out[148]: 
          one  two  three  four
Ohio        0    1      2     3
Colorado    4    5      6     7

## IMPORTANT: handle missing data

# remove na in series
from numpy import nan as NA

data = Series([1, NA, 3.5, NA, 7])

data.dropna()
Out[152]: 
0    1.0
2    3.5
4    7.0
dtype: float64

# another test
Series([[1, NA, 3.5, NA, 7],[2,3,4]]).dropna()
Out[161]: 
0    [1, nan, 3.5, nan, 7]
1                [2, 3, 4]
dtype: object

Series([[1, NA, 3.5, NA, 7],[2,3,4]]).dropna()[0]
Out[162]: [1, nan, 3.5, nan, 7]

Series([[1, NA, 3.5, NA, 7],[2,3,4]]).dropna()[1]
Out[163]: [2, 3, 4]


# dataframe dropna

data = DataFrame([[1., 6.5, 3.], [1., NA, NA], [NA, NA, NA], [NA, 6.5, 3.]])

data
Out[168]: 
     0    1    2
0  1.0  6.5  3.0
1  1.0  NaN  NaN
2  NaN  NaN  NaN
3  NaN  6.5  3.0

data.dropna()
Out[169]: 
     0    1    2
0  1.0  6.5  3.0
# only drop row which is all NA
data.dropna(how='all')
Out[170]: 
     0    1    2
0  1.0  6.5  3.0
1  1.0  NaN  NaN
3  NaN  6.5  3.0

# add a column which is all NA
data[4]=NA

data
Out[172]: 
     0    1    2   4
0  1.0  6.5  3.0 NaN
1  1.0  NaN  NaN NaN
2  NaN  NaN  NaN NaN
3  NaN  6.5  3.0 NaN
data.dropna(axis=1,how="all")
Out[174]: 
     0    1    2
0  1.0  6.5  3.0
1  1.0  NaN  NaN
2  NaN  NaN  NaN
3  NaN  6.5  3.0


#filling in empty data

 df = DataFrame(np.random.randn(7, 3))
 df.ix[:4,1]=NA
 df.ix[:2,2]=NA

df
Out[184]: 
          0         1         2
0  2.835825       NaN       NaN
1  0.222555       NaN       NaN
2 -2.233193       NaN       NaN
3  0.119567       NaN  0.181973
4 -1.132524       NaN -0.032814
5  0.159883 -0.481497 -0.446252
6 -0.209037  0.093733  1.256807


# fill with default value

df.fillna(0)
Out[187]: 
          0         1         2
0  2.835825  0.000000  0.000000
1  0.222555  0.000000  0.000000
2 -2.233193  0.000000  0.000000
3  0.119567  0.000000  0.181973
4 -1.132524  0.000000 -0.032814
5  0.159883 -0.481497 -0.446252
6 -0.209037  0.093733  1.256807


# use ffill
df.fillna(method='ffill')
Out[188]: 
          0         1         2
0  2.835825       NaN       NaN
1  0.222555       NaN       NaN
2 -2.233193       NaN       NaN
3  0.119567       NaN  0.181973
4 -1.132524       NaN -0.032814
5  0.159883 -0.481497 -0.446252
6 -0.209037  0.093733  1.256807

df.T
Out[189]: 
          0         1         2         3         4         5         6
0  2.835825  0.222555 -2.233193  0.119567 -1.132524  0.159883 -0.209037
1       NaN       NaN       NaN       NaN       NaN -0.481497  0.093733
2       NaN       NaN       NaN  0.181973 -0.032814 -0.446252  1.256807

df.T.fillna(method='ffill')
Out[190]: 
          0         1         2         3         4         5         6
0  2.835825  0.222555 -2.233193  0.119567 -1.132524  0.159883 -0.209037
1  2.835825  0.222555 -2.233193  0.119567 -1.132524 -0.481497  0.093733
2  2.835825  0.222555 -2.233193  0.181973 -0.032814 -0.446252  1.256807

df.T.fillna(method='ffill').T
Out[191]: 
          0         1         2
0  2.835825  2.835825  2.835825
1  0.222555  0.222555  0.222555
2 -2.233193 -2.233193 -2.233193
3  0.119567  0.119567  0.181973
4 -1.132524 -1.132524 -0.032814
5  0.159883 -0.481497 -0.446252
6 -0.209037  0.093733  1.256807

































