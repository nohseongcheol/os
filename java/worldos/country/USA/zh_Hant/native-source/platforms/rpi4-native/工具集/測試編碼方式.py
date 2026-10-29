#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from 執行命令 import 項目根

def 運行():
    結果資料=項目根/'build/verification/coding';結果資料.mkdir(parents=True,exist_ok=True)
    有效性驗證報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(項目根/'工具集/導出SDK.py')])
        with tarfile.open(str(項目根/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 已壓縮捆綁:已壓縮捆綁.extractall(str(結果資料))
        開發工具套件=結果資料/'jkoros-native-sdk'
        符號列列表=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(開發工具套件/'lib/libposix-kor-user.a')]).decode()
        for 名稱 in ('創建端點','綁定地址','發送數據報資料','接收數據報資料','打開檔案','讀取檔案資料','寫入檔案資料'):
            assert ' T '+名稱+'\n' in 符號列列表, 名稱
        (結果資料/'korean-function-symbols.txt').write_text(符號列列表)
        有效性驗證報告['checks'].append('real-korean-c-function-symbols')
        def 執行命令(名稱,路徑,實際參數陣列,預期):
            資料位置=subprocess.run(['python3',str(項目根/'工具集/執行檔案.py'),str(路徑)]+實際參數陣列,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (結果資料/(名稱+'.log')).write_bytes(資料位置.stdout);assert 資料位置.returncode==0,資料位置.stdout.decode('utf-8','replace')
            assert 預期.encode() in 資料位置.stdout,資料位置.stdout;有效性驗證報告['checks'].append(名稱)
        for 後綴值 in ('c','cpp'):
            可執行文件檔案=結果資料/('問候例-'+後綴值+'.elf')
            subprocess.check_call(['python3',str(開發工具套件/'compile.py'),str(開發工具套件/'examples'/('問候例.'+後綴值)),'-o',str(可執行文件檔案)])
            執行命令('korean-'+後綴值,可執行文件檔案,[],'posix-kor 調用')
        可執行文件檔案=結果資料/'流值.elf'
        subprocess.check_call(['python3',str(開發工具套件/'compile.py'),str(開發工具套件/'examples/流值.c'),'-o',str(可執行文件檔案)])
        執行命令('c-stream-queues',可執行文件檔案,[],'C posix-kor 연결형 通信 PASS')
        執行命令('korean-python',項目根/'範例/韓文字母編碼方式/問候例.py',['--include',str(項目根/'範例/韓文字母編碼方式/中文.py')],'안녕하세요 누리')
        執行命令('guest-korean-javac',項目根/'範例/韓文字母編碼方式/問候例.java',[],'안녕하세요 · 總計值=42')
        有效性驗證報告['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(結果資料/'report.json').write_text(json.dumps(有效性驗證報告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':運行()
