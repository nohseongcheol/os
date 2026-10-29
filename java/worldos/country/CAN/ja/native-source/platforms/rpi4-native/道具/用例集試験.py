#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from デスクトップ表示像 import 厳密値
from 復唱試験サーバー import 復唱サーバー一覧
from 命令実行 import 計画根


def 言語試験(言語,復唱サーバー入口,結果データ):
    with socket.socket() as 一時:
        一時.bind(('127.0.0.1',0));ファイル転送ポート番号=一時.getsockname()[1]
    プロセス=subprocess.Popen(['python3',str(計画根/'道具/命令実行.py'),'--desktop','--network','--port','0','--ftp-port',str(ファイル転送ポート番号)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    準備監視器=selectors.DefaultSelector();準備監視器.register(プロセス.stdout,selectors.EVENT_READ)
    実行記録=bytearray();接続元=None;ファイル転送接続状態=None
    def メッセージ受取(標識,起動処理=0):
        終端位置変位量=time.monotonic()+60
        while 標識 not in 実行記録[起動処理:]:
            if time.monotonic()>終端位置変位量 or プロセス.poll() is not None:raise AssertionError(実行記録[起動処理:].decode('utf-8','replace'))
            for 押下済み値,_ in 準備監視器.select(.1):
                データ=押下済み値.fileobj.read(65536)
                if データ:実行記録.extend(データ)
        return 実行記録[起動処理:].decode('utf-8','replace').replace('\r\n','\n')
    def 押下済み値(記号値,判定押下中=True):接続元.sendall(struct.pack('>BBHI',4,int(判定押下中),0,記号値))
    def 変位量開始処理(行):
        起動処理=len(実行記録)
        for 文字コード in 行+'\n':
            記号値=0xff0d if 文字コード=='\n' else ord(文字コード) if ord(文字コード)<256 else 0x1000000|ord(文字コード)
            押下済み値(記号値);押下済み値(記号値,False)
        return 起動処理
    def シェル(行):return メッセージ受取(b'jkoros-native> ',変位量開始処理(行))
    def 命令実行(行,期待):
        文=シェル(行);assert 期待 in 文 and 'exit 0' in 文,(行,文)
        return 文
    def 画素列一覧():
        接続元.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        RGB色=bytearray(640*480*3)
        while True:
            分類値=厳密値(接続元,1)[0]
            if 分類値==2:continue
            if 分類値==3:
                項目個数=struct.unpack('>I',厳密値(接続元,7)[3:])[0];厳密値(接続元,項目個数);continue
            assert 分類値==0,分類値
            入口個数=struct.unpack('>H',厳密値(接続元,3)[1:])[0]
            for _ in range(入口個数):
                横座標,縦座標,要求済み幅値,要求済み高さ値,文字設定=struct.unpack('>HHHHi',厳密値(接続元,12));assert 文字設定==0,文字設定
                データ=厳密値(接続元,要求済み幅値*要求済み高さ値*4)
                for 行番号位置 in range(要求済み高さ値):
                    for 列位置 in range(要求済み幅値):
                        原本データ=(行番号位置*要求済み幅値+列位置)*4;対象値=((縦座標+行番号位置)*640+横座標+列位置)*3
                        RGB色[対象値:対象値+3]=bytes((データ[原本データ+2],データ[原本データ+1],データ[原本データ]))
            if 入口個数:return RGB色
    try:
        メッセージ受取(b'TERMINAL READY');メッセージ受取(b'jkoros-native> ',実行記録.rfind(b'TERMINAL READY'))
        ポート番号=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',実行記録).group(1))
        接続元=socket.create_connection(('127.0.0.1',ポート番号),timeout=10)
        assert 厳密値(接続元,12)==b'RFB 003.008\n';接続元.sendall(b'RFB 003.008\n')
        assert 1 in 厳密値(接続元,厳密値(接続元,1)[0]);接続元.sendall(b'\x01');assert 厳密値(接続元,4)==b'\0'*4
        接続元.sendall(b'\x01');初期値=厳密値(接続元,24);厳密値(接続元,struct.unpack('>I',初期値[20:])[0])
        接続元.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        接続元.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in シェル('ftpd start')
        ファイル転送接続状態=ftplib.FTP();ファイル転送接続状態.encoding='utf-8';ファイル転送接続状態.connect('127.0.0.1',ファイル転送ポート番号,timeout=20);ファイル転送接続状態.login()
        本文データデータ=('GUI와 FTP 동시 使用値 '+言語+' 😀\n').encode()
        ファイル転送接続状態.storbinary('STOR 함께.txt',io.BytesIO(本文データデータ))
        assert 本文データデータ.decode().strip() in シェル('cat /함께.txt')
        受信済み個数=bytearray();ファイル転送接続状態.retrbinary('RETR 함께.txt',受信済み個数.extend);assert 受信済み個数==本文データデータ;ファイル転送接続状態.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        一覧送信=シェル('ls /example')
        assert all(名前 in 一覧送信 for 名前 in ('java/','c/','python/','README.md')),一覧送信
        if 言語=='java':
            束管理目録=json.loads((計画根/'build/examples/manifest.json').read_text())
            for 経路,入口点 in 束管理目録.items():
                シェル('cp '+経路+' /example-check.bin')
                内容物値=bytearray();ファイル転送接続状態.retrbinary('RETR example-check.bin',内容物値.extend)
                assert len(内容物値)==入口点['bytes'] and hashlib.sha256(内容物値).hexdigest()==入口点['sha256'],経路
            ファイル転送接続状態.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            二進=bytes(range(256))*64
            ファイル転送接続状態.storbinary('STOR boundary.bin',io.BytesIO(二進))
            内容物値=bytearray();ファイル転送接続状態.retrbinary('RETR boundary.bin',内容物値.extend)
            assert 内容物値==二進 and 'boundary.bin' in ファイル転送接続状態.nlst()
            シェル('cp /boundary.bin /boundary-copy.bin')
            内容物値=bytearray();ファイル転送接続状態.retrbinary('RETR boundary-copy.bin',内容物値.extend)
            assert 内容物値==二進
            ファイル転送接続状態.delete('boundary.bin');ファイル転送接続状態.delete('boundary-copy.bin')
        assert '出力例' in シェル('ls /example/'+言語)
        シェル('cd /example/'+言語)
        名前表={'java':'JAVA','c':'C','python':'PYTHON'}[言語]
        期待ファイル=名前表+' ファイル: 한글 データ 😀\n'
        if 言語=='java':
            命令実行('javac 出力例.java','Compiled:');命令実行('java 出力例','JAVA 出力: 안녕하세요 😀')
            命令実行('javac ファイル例.java','Compiled:');命令実行('java ファイル例',期待ファイル)
            命令実行('java 通信例 {} {}'.format(復唱サーバー入口.TCPポート,復唱サーバー入口.UDPポート),'JAVA 네트워크 検証: TCP UDP 한글')
            描画命令='java 描画例'
        elif 言語=='c':
            for 名前,転送済み値,期待 in [('出力','', 'C 出力: 안녕하세요 😀'),('ファイル','',期待ファイル),
                    ('네트워크',' '+str(復唱サーバー入口.UDPポート),'C 네트워크 検証: UDP 한글')]:
                命令実行('cc '+名前+'用例.c -o 命令実行','Compiled native ARM64 ELF:')
                命令実行('./命令実行'+転送済み値,期待)
            命令実行('cc 描画例.c -o 命令実行','Compiled native ARM64 ELF:');描画命令='./命令実行'
        else:
            for 名前,転送済み値,期待 in [('出力','','PYTHON 出力: 안녕하세요 😀'),('ファイル','',期待ファイル),
                    ('네트워크',' '+str(復唱サーバー入口.UDPポート),'PYTHON 네트워크 検証: UDP 한글')]:
                命令実行('python '+名前+'用例.py'+転送済み値,期待)
            描画命令='python 描画例.py'
        描画中開始処理=変位量開始処理(描画命令)
        文=メッセージ受取('그림을 확인한 後端値 Enter를 누르세요.\r\n'.encode(),描画中開始処理)
        assert 名前表+' 그래픽: 빨강 초록 파랑' in 文 and 'exit 0' not in 文,文
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ファイル転送接続状態.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        受信済み個数=bytearray();ファイル転送接続状態.retrbinary('RETR 도중.txt',受信済み個数.extend);assert 受信済み個数==b'FTP DURING GRAPHICS';ファイル転送接続状態.delete('도중.txt')
        RGB色=画素列一覧()
        for 縦座標,画素色 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            変位量値=(縦座標*640+610)*3;assert tuple(RGB色[変位量値:変位量値+3])==画素色,(言語,縦座標,tuple(RGB色[変位量値:変位量値+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(RGB色)).save(str(結果データ/(言語+'-graphics.png')))
        押下済み値(0xff0d);押下済み値(0xff0d,False)
        assert 'exit 0' in メッセージ受取(b'jkoros-native> ',描画中開始処理)
        if 言語=='java':
            窓開始処理=変位量開始処理('java 窓例')
            メッセージ受取('GUI 用例 用意: 窓例'.encode(),窓開始処理)
            def クリック値(水平位置,垂直位置):
                for ボタン in (1,0):接続元.sendall(struct.pack('>BBHH',5,ボタン,水平位置,垂直位置))
            time.sleep(.3)
            前回イメージ=Image.frombytes('RGB',(640,480),bytes(画素列一覧()))
            クリック値(160,196)
            for _ in range(2):押下済み値(0xff08);押下済み値(0xff08,False)
            for 文字値 in '한글':押下済み値(0x1000000|ord(文字値));押下済み値(0x1000000|ord(文字値),False)
            for 反復状態個数 in (1,2):
                起動処理=len(実行記録);クリック値(180,242)
                メッセージ受取(('GUI 挨拶例: 안녕하세요, 한글님! ('+str(反復状態個数)+')').encode(),起動処理)
            time.sleep(.3)
            窓描画中=Image.frombytes('RGB',(640,480),bytes(画素列一覧()))
            assert 前回イメージ.crop((110,272,530,300)).tobytes()!=窓描画中.crop((110,272,530,300)).tobytes()
            窓描画中.save(str(結果データ/'java-swing.png'))
            起動処理=len(実行記録);クリック値(535,105)
            assert 'exit 0' in メッセージ受取(b'jkoros-native> ',起動処理)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ファイル入口名前={'java':'java.txt','c':'c.txt','python':'python.txt'}[言語]
        シェル('cp '+ファイル入口名前+' /妥当性検査.txt')
        受信済み個数=bytearray();ファイル転送接続状態.retrbinary('RETR 妥当性検査.txt',受信済み個数.extend);assert 受信済み個数==期待ファイル.encode()
        シェル('echo preserved > 出力例.'+('py' if 言語=='python' else 言語))
        assert 'EXAMPLES READY' in シェル('example '+言語)
        assert '\npreserved\n' in シェル('cat 出力例.'+('py' if 言語=='python' else 言語))
        assert '한/零被演算子 キー値, Shift+Space 또는 F9' in シェル('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in シェル('echo GUI NETWORK TOGETHER')
        ファイル転送接続状態.quit();ファイル転送接続状態=None;assert 'FTP stopped' in シェル('ftpd stop')
        print('PASS '+言語+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ファイル転送接続状態:
            try:ファイル転送接続状態.close()
            except OSError:pass
        if 接続元:接続元.close()
        プロセス.terminate()
        try:プロセス.wait(timeout=8)
        except subprocess.TimeoutExpired:プロセス.kill();プロセス.wait()
        準備監視器.close();プロセス.stdout.close();(結果データ/(言語+'-serial.log')).write_bytes(実行記録)


def 起動処理():
    結果データ=計画根/'build/verification/examples';結果データ.mkdir(parents=True,exist_ok=True)
    妥当性報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 復唱サーバー一覧() as 復唱サーバー入口:
            for 言語 in ('java','c','python'):
                言語試験(言語,復唱サーバー入口,結果データ);妥当性報告['languages'].append(言語)
            期待=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 復唱サーバー入口.保有受信済み==[(分類値,データ.encode()) for 分類値,データ in 期待],復唱サーバー入口.保有受信済み
            妥当性報告['host_network_payloads']=[{'protocol':分類値,'text':データ.decode()} for 分類値,データ in 復唱サーバー入口.保有受信済み]
        妥当性報告.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(結果データ/'report.json').write_text(json.dumps(妥当性報告,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':起動処理()
