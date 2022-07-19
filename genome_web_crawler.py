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

parser = argparse.ArgumentParser(description='Genome download from GCA/GCF Num using selenium !')
parser.add_argument('-i', '--input', required=True, type=str, help='input GCA or GCF num, such as: GCA_001599795.1')
parser.add_argument('-o', '--output',required=True, type=str, help='output dir')
args = parser.parse_args()

if not os.path.exists(args.output):
    os.mkdir(args.output)

## ---------------------------------------------------
## 参考基因组下载函数
## ---------------------------------------------------

def genome_download(acc_num:str,out_path:str):
    abs_path = os.path.abspath(out_path)
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
            'download.default_directory': abs_path
            }
    options.add_experimental_option('prefs', prefs)
    ncbi_web = 'https://www.ncbi.nlm.nih.gov/assembly/'
    genome_download_path = ncbi_web + acc_num
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(genome_download_path)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="download-asm"]').click()
    time.sleep(2)
    els = driver.find_element_by_xpath('//*[@id="dl_assembly_gbrs"]')
    time.sleep(2)
    options = Select(els).options
    # 切换数据库为GenBank【0,GenBank; 1,RefSeq】
    # 这里写的只针对了GCA genbank的基因组，后续再完善
    Select(els).select_by_index("0")
    now_option = Select(els).first_selected_option
    time.sleep(3)
    print("Now you changed source database to {}".format(now_option.text))
    driver.find_element_by_xpath('//*[@id="dl_assembly_download"]').click()
    time.sleep(5)
    if os.path.exists("{}/genome_assemblies_genome_fasta.tar.crdownload".format(abs_path)):
        driver.close()
        os.system("tar -xvf {}/genome_assemblies_genome_fasta.tar.crdownload".format(abs_path))
        os.system("cp ncbi-genomes*/*.fna.gz {}".format(abs_path))
        print("check the genome in {}".format(abs_path))
    else:
        driver.close()
        print("download failed")

if __name__ == '__main__':
    genome_download(args.input,args.output)

## ---------------------------------------------------
## 单个基因组GCA_001599795.1 写程序测试用的
## ---------------------------------------------------
# chrome中加入配置参数，处理连接不是私密连接的网站(https ssl 证书)；不加载图片等问题
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# # options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless')
# options.add_argument('blink-settings=imagesEnabled=false')
# options.add_argument('--disable-gpu')

# prefs = {'profile.default_content_settings.popups': 0, \
#          'profile.managed_default_content_settings.images': 2, \
#          'download.default_directory': args.output
#          }
# options.add_experimental_option('prefs', prefs)
# driver = webdriver.Chrome(chrome_options=options)
# driver.get('https://www.ncbi.nlm.nih.gov/assembly/GCA_001599795.1/')
# time.sleep(2)
# driver.find_element_by_xpath('//*[@id="download-asm"]').click()
# time.sleep(2)
# els = driver.find_element_by_xpath('//*[@id="dl_assembly_gbrs"]')
# time.sleep(2)
# options = Select(els).options
# # 切换数据库为GenBank【0,GenBank; 1,RefSeq】
# Select(els).select_by_index("0")
# now_option = Select(els).first_selected_option
# time.sleep(3)
# print("Now you changed source database to {}".format(now_option.text))
# driver.find_element_by_xpath('//*[@id="dl_assembly_download"]').click()
# time.sleep(5)
# file_name = "genome_assemblies_genome_fasta.tar.crdownload"
# if os.path.exists(file_name):
#     os.system("tar -xvf genome_assemblies_genome_fasta.tar.crdownload")
#     driver.close()
# os.system("cp ncbi-genomes*/*.fna.gz ../")