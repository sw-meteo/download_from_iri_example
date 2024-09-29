# IRI下载气候数据示例脚本

在CDS数据中心宕机的时候，我用这种方式在IRI补充了急用的C3S季节预测数据，这个仓库保存了当时的代码以供参考。

## 概述

IRI climate data library是哥大的气候数据下载中心，从这里可以下载多国机构的预测、观测数据，参见这个[目录](https://iridl.ldeo.columbia.edu/SOURCES/overview.html)（甚至有CMA的数据，不过都是一些比较老的模式了）。

部分数据下载受限，需要首先需要注册IRI的账户，并提交申请，所以需要预留一段审核的时间。

## expert mode选择数据

- [视频版教程](https://www.youtube.com/watch?v=QbnXl_F5Clo)

- [文字版教程](http://iridl.ldeo.columbia.edu/dochelp/Tutorial/)  

如果直接选择data files，access到的是整个数据集。如果需要选取特定的时段、空间范围等，则需要用data viewer交互式选择想要的数据，或者在页面上方选到exper mode，用脚本模式来设置。

脚本主要做的事情是给每个坐标轴，用RANGE, VALUE, VALUES等表示选择的范围或点。坐标轴名称在数据集说明页的“Independent Variables (Grids)”一节给出，RANGE VALUES等顾名思义，是选择范围或者单点。

例如，如果要从subX下载GEO-S2S的部分数据，脚本可以如下：

```text
 SOURCES .Models .SubX .GMAO .GEOS_V2p1 .forecast .pr
  M (1) VALUE
  S (01 Apr 2022) (10 Apr 2022) RANGE
  Y -10 10 RANGE
  X -70 -20 RANGE
```

## 下载数据

编辑好脚本后会自动生成数据的下载地址，例如上述脚本所对应的地址是

```text
http://iridl.ldeo.columbia.edu/SOURCES/.Models/.SubX/.GMAO/.GEOS_V2p1/.forecast/.pr/M/%281%29/VALUE/S/%2801%20Apr%202022%29/%2810%20Apr%202022%29/RANGE/Y/-10/10/RANGE/X/-70/-20/RANGE/dods
```

这个网址是有规律的，其实只是直接展开expert mode的文字。`%28`表示左括号`(`，`%29`表示右括号`)`，`%20`表示同一个字符串内部的分隔，没加括号的全部用`/`分隔，这里生成的是用于opendap协议的地址。

下载C3S数据时，用opendap协议进行了多种尝试都没有成功，经过排查，主要是数据集不公开，需要验证的原因。

最终成功的下载方式是用request库直接获取nc文件，这时网址的形式和opandap的地址类似但稍有不同，例如：

```text
https://iridl.ldeo.columbia.edu/SOURCES/.EU/.Copernicus/.CDS/.C3S/.ECMWF/.SEAS5/.hindcast/.va/S/(Jan%201993)/(Nov%202016)/RANGE/L/(2.5)/VALUE/P/(700)/VALUE/Y/(4S)/(60N)/RANGE/X/(64E)/(160E)/RANGE/data.nc
```

具体的操作步骤是：

- 注册验证iri的账户，申请访问所需的数据集，等IRI中心发来一个密码用于登录
- 打开Chrome（safari不行）在交互式页面尝试下载数据，扒出Chrome的cookie信息
- 输入给request，脚本如下，需要将url，path/to/file，Cookie，User-Agent这四项替换成自己的

```python
import requests
session = requests.Session()
headers = {
	'Cookie': xxxxx
	'User-Agent': xxxxx
}

response = session.get(url=url, headers=headers)
with open('/path/to/save/file.nc', 'wb') as f:
	f.write(response.content)
```

- 需要经常检查cookie有没有失效，然后手动换上新的（代码里虽然有我的cookie，但早已失效，仅提供形式上的参考）

