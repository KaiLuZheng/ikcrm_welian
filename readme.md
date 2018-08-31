## welian ikcrm 批量查重小程序

写给微链小伙伴使用，使用 Python3.6.0 环境

使用爱客系统的，可自行更改源码。


* 20180831

    当前可通过终端在 Python3 的环境下运行 ikcrm_welian.py 进行登入；

    当前只读取 txt 中的手机号列表进行批量查重，输出文件名为 outfile.txt 和 outExcel.xlsx;

    当前若系统中有 openpyxl 库，则输出为 outExcel.xlsx ，否则为 outfile.txt；

    若输出为 outfile.txt 文件，可以将内容复制到 Excel 表格，可以按单元格正确复制；
    
    如果查重出了问题，可以清除cookie，重新登入一次；

