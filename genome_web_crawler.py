#! /usr/bin/python3
# -*- coding:utf-8 -*-
# Author：wanjin.hu

from cmath import exp
# from msilib.schema import File
from pathlib import Path
from xml.parsers import expat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import os
import argparse

# parser = argparse.ArgumentParser(description='Genome download from GCA/GCF Num')
# parser.add_argument('-i', '--input', required=True, type=str, help='input GCA or GCF num, such as: GCA_001599795.1')
# parser.add_argument('-o', '--output',required=True, type=str, help='output dir')

# chrome中加入配置参数，处理连接不是私密连接的网站(https ssl 证书)；不加载图片等问题
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
# options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-gpu')

prefs = {'profile.default_content_settings.popups': 0, \
         'profile.managed_default_content_settings.images': 2, \
         'download.default_directory': '/mnt/ilustre/users/wanjin.hu/test'
         }
options.add_experimental_option('prefs', prefs)

## -----------------------------------------------
## 单个基因组GCA_001599795.1 下载基因组fa文件
## -----------------------------------------------

driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.ncbi.nlm.nih.gov/assembly/GCA_001599795.1/')
time.sleep(2)
driver.find_element_by_xpath('//*[@id="download-asm"]').click()
time.sleep(2)
els = driver.find_element_by_xpath('//*[@id="dl_assembly_gbrs"]')
time.sleep(2)
options = Select(els).options
# 切换数据库为GenBank【0,GenBank; 1,RefSeq】
Select(els).select_by_index("0")
now_option = Select(els).first_selected_option
time.sleep(3)
print("Now you changed source database to {}".format(now_option.text))
driver.find_element_by_xpath('//*[@id="dl_assembly_download"]').click()
time.sleep(5)
file_name = "genome_assemblies_genome_fasta.tar.crdownload"
if os.path.exists(file_name):
    os.system("tar -xvf genome_assemblies_genome_fasta.tar.crdownload")
    driver.close()
os.system("cp ncbi-genomes*/*.fna.gz ../")