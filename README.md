# reference_genome_download
这个仓库会陆续补充一些参考基因组自动化下载的方法

## **1. genome_web_crawler.py**
该程序利用selenium模块，模仿页面点击的方式来下载参考基因组的fasta文件。GCA编号下载获得的是GeneBank数据，GCF编号下载获得的是RefSeq数据。

该下载方法的使用效率取决于网络情况和其他会影响到selenium使用的因素，下载不成功可能是因为selenium连接浏览器失败等，你可以再尝试下载试试看。

### 使用方法：
```
$python3 genome_web_crawler.py -h
usage: genome_web_crawler.py [-h] -i INPUT -o OUTPUT

Genome download from GCA/GCF Num using selenium !

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input GCA or GCF num, such as: GCA_001599795.1
  -o OUTPUT, --output OUTPUT
                        output dir
```
## **2. genome_esearch_ascp.py**
该程序利用esearch + ascp的方式批量下载参考基因组。需要提供GCA/GCF的列表

### 使用方法：
```
$python3 genome_esearch_ascp.py -h
usage: genome_esearch_ascp.py [-h] [-l LIST] [-o OUTDIR]

Genomes download from GCA/GCF Num using esearch and ascp

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  genome assembly accessions list
  -o OUTDIR, --outdir OUTDIR
                        output dir

```