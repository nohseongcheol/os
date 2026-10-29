#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from 命令実行 import 計画根

def 起動処理():
    結果データ=計画根/'build/verification/coding';結果データ.mkdir(parents=True,exist_ok=True)
    妥当性報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(計画根/'道具/公開SDK.py')])
        with tarfile.open(str(計画根/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 圧縮済み束:圧縮済み束.extractall(str(結果データ))
        開発道具一式=結果データ/'jkoros-native-sdk'
        記号一覧一覧=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(開発道具一式/'lib/libposix-kor-user.a')]).decode()
        for 名前 in ('通信端点作成','番地結合','データグラムデータ送信','データグラムデータ受取','ファイル開放','ファイルデータ読取','ファイルデータ書込'):
            assert ' T '+名前+'\n' in 記号一覧一覧, 名前
        (結果データ/'korean-function-symbols.txt').write_text(記号一覧一覧)
        妥当性報告['checks'].append('real-korean-c-function-symbols')
        def 命令実行(名前,経路,引数配列,期待):
            データ位置=subprocess.run(['python3',str(計画根/'道具/ファイル実行.py'),str(経路)]+引数配列,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (結果データ/(名前+'.log')).write_bytes(データ位置.stdout);assert データ位置.returncode==0,データ位置.stdout.decode('utf-8','replace')
            assert 期待.encode() in データ位置.stdout,データ位置.stdout;妥当性報告['checks'].append(名前)
        for 接尾辞値 in ('c','cpp'):
            実行形式ファイル=結果データ/('挨拶例-'+接尾辞値+'.elf')
            subprocess.check_call(['python3',str(開発道具一式/'compile.py'),str(開発道具一式/'examples'/('挨拶例.'+接尾辞値)),'-o',str(実行形式ファイル)])
            命令実行('korean-'+接尾辞値,実行形式ファイル,[],'posix-kor 呼出')
        実行形式ファイル=結果データ/'ストリーム値.elf'
        subprocess.check_call(['python3',str(開発道具一式/'compile.py'),str(開発道具一式/'examples/ストリーム値.c'),'-o',str(実行形式ファイル)])
        命令実行('c-stream-queues',実行形式ファイル,[],'C posix-kor 연결형 通信 PASS')
        命令実行('korean-python',計画根/'用例/ハングル符号化方式/挨拶例.py',['--include',str(計画根/'用例/ハングル符号化方式/日本語.py')],'안녕하세요 누리')
        命令実行('guest-korean-javac',計画根/'用例/ハングル符号化方式/挨拶例.java',[],'안녕하세요 · 合計値=42')
        妥当性報告['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(結果データ/'report.json').write_text(json.dumps(妥当性報告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':起動処理()
