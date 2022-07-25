#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'wanjin.hu'

import os
import re
import argparse
import gzip
import time

parser = argparse.ArgumentParser(description='Genomes download from GCA/GCF Num using esearch and ascp')
parser.add_argument('-l', '--list', dest='list', required=False,
                    type=str, help='genome assembly accessions list')
parser.add_argument('-o', '--outdir', dest='outDir',required=False,
                    type=str, help='output dir')
args = parser.parse_args()
if not os.path.exists(args.outDir):
    os.mkdir(args.outDir)
print('-'*8 + 'Preparing the genome download link, please wait!' + '-'*8 +'\n')

def genomes_download():
    with open(args.list, 'r') as list:
        for line in list:
            num = line.strip('\n')
            if num.startswith('GCF_'):
                res1 = os.popen('esearch -db assembly -query ' + num + ' | efetch -format docsum ').read()
                pr = re.findall('<FtpPath_RefSeq>(.*?)<', res1)
                pr1 = pr[0].split('/', 3)[3]
                pr2 = 'ascp -i .aspera/connect/etc/asperaweb_id_dsa.openssh -k1 -QTr -l100m anonftp@ftp.ncbi.nlm.nih.gov:' + pr1 + ' ' + args.outDir
                os.system(pr2)
                print('--------'+num+' is completed--------\n')
            elif num.startswith('GCA_'):
                res1 = os.popen('esearch -db assembly -query ' + num + ' | efetch -format docsum ').read()
                pr = re.findall('<FtpPath_GenBank>(.*?)<', res1)
                pr1 = pr[0].split('/', 3)[3]
                pr2 = 'ascp -i .aspera/connect/etc/asperaweb_id_dsa.openssh -k1 -QTr -l100m anonftp@ftp.ncbi.nlm.nih.gov:' + pr1 + ' ' + args.outDir
                os.system(pr2)
                print('--------'+num+' is completed--------\n')
            else:
                print(num + ' is not true genome number, please check')

if __name__ == '__main__':
    genomes_download()
