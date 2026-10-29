#!/usr/bin/env python3
"""実際データ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import selectors
from Crypto.Cipher import DES
from 命令実行 import 計画根, 命令
from 通信網橋渡し import 通信網橋渡し


def 起動処理():
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('--kernel', type=Path, default=計画根 / 'build/kernel8.img')
    構文解析器.add_argument('--access', type=Path, default=計画根 / 'build/remote/access.json')
    構文解析器.add_argument('--output', type=Path, default=計画根 / 'build/verification/native-remote')
    引数 = 構文解析器.parse_args()
    出力 = 引数.output
    出力.mkdir(parents=True, exist_ok=True)
    設定値 = json.loads(引数.access.read_text())
    報告値 = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(引数.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 空ポート():
        with socket.socket() as 接続:
            接続.bind(('127.0.0.5', 0))
            return 接続.getsockname()[1]
    シェルポート, 画面ポート, ファイルポート = 空ポート(), 空ポート(), 空ポート()
    履歴記録記録 = bytearray()
    プロセス値 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 一時値, 通信網橋渡し(ファイルポート,
                ['tcp:{}:22'.format(シェルポート), 'tcp:{}:5900'.format(画面ポート)], ホスト番地='127.0.0.5') as 橋渡し値:
            実行引数 = 命令()
            実行引数[実行引数.index('-kernel') + 1] = str(引数.kernel.resolve())
            プロセス値 = subprocess.Popen(実行引数 + ['-display','none','-monitor','none','-serial','stdio'] + 橋渡し値.転送済み引数(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 値一覧収集処理():
                while True:
                    データ = プロセス値.stdout.read(4096)
                    if not データ: break
                    履歴記録記録.extend(データ)
            スレッド値 = threading.Thread(target=値一覧収集処理, daemon=True)
            スレッド値.start()
            def 状況待合(語本文, 初期項目=0, 上限値=60):
                終端 = time.monotonic() + 上限値
                while 語本文 not in 履歴記録記録[初期項目:]:
                    if time.monotonic()>終端 or プロセス値.poll() is not None:
                        raise AssertionError('Missing '+repr(語本文)+'\n'+履歴記録記録[初期項目:].decode('utf-8','replace'))
                    time.sleep(.02)
            状況待合(b'jkoros-native> ')
            補助器値 = Path(一時値)/'askpass'
            補助器値.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            補助器値.chmod(0o700)
            環境 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(補助器値), SSH_ASKPASS_REQUIRE='force')
            def 保安シェル(合言葉値, 命令語値, 入口追記=()):
                環境['JKOROS_TEST_PASSWORD']=合言葉値
                引数=['ssh','-v']+list(入口追記)+['-p',str(シェルポート),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(一時値)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',命令語値]
                結果=subprocess.run(引数,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=環境,start_new_session=True,timeout=50)
                return 結果
            結果=保安シェル('!' + 設定値['ssh_password'], 'echo SHOULD_NOT_RUN')
            (出力/'ssh-rejected.log').write_bytes(結果.stderr)
            assert 結果.returncode!=0 and b'Permission denied' in 結果.stderr and b'SHOULD_NOT_RUN' not in 履歴記録記録, 結果.stderr
            報告値['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            結果=保安シェル(設定値['ssh_password'], 'echo SSH_NATIVE_PASS')
            (出力/'ssh.log').write_bytes(結果.stderr)
            (出力/'ssh-output.txt').write_bytes(結果.stdout)
            assert 結果.returncode==0 and b'SSH_NATIVE_PASS' in 結果.stdout, (結果.returncode,結果.stdout,結果.stderr)
            報告値['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 結果.stderr, 結果.stderr
            報告値['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            結果=保安シェル(設定値['ssh_password'], 'cd /example/java; java 出力例; cd /')
            assert 結果.returncode==0 and 'JAVA 出力: 안녕하세요 😀'.encode() in 結果.stdout,結果.stdout
            報告値['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            結果=保安シェル(設定値['ssh_password'], 'missing_remote_command')
            assert 結果.returncode==127,結果.returncode
            報告値['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            結果=保安シェル(設定値['ssh_password'], 'cat /example/java/窓例.java', ('-o', 'RekeyLimit=1K'))
            (出力/'ssh-rekey.log').write_bytes(結果.stderr)
            assert 結果.returncode==0 and 'class 窓例'.encode() in 結果.stdout, (結果.returncode,結果.stdout,結果.stderr)
            assert 結果.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 結果.stderr
            報告値['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            対話式引数列=['ssh','-tt','-p',str(シェルポート),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(一時値)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            対話式セッション=subprocess.Popen(対話式引数列,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=環境,start_new_session=True,bufsize=0)
            実行記録=bytearray();選択状態値=selectors.DefaultSelector();選択状態値.register(対話式セッション.stdout,selectors.EVENT_READ)
            def 対話式読取(値表示):
                期限値=time.monotonic()+30
                while 値表示 not in 実行記録:
                    if time.monotonic()>期限値 or 対話式セッション.poll() is not None:raise AssertionError('SSH interactive missing '+repr(値表示)+' '+repr(bytes(実行記録)))
                    for 入口値,_ in 選択状態値.select(.1):
                        断片値=入口値.fileobj.read(4096)
                        if 断片値:実行記録.extend(断片値)
            try:
                対話式読取(b'shared native console')
                対話式セッション.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');対話式セッション.stdin.flush();対話式読取(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                対話式セッション.stdin.write(b'\x04');対話式セッション.stdin.flush();剰余値,エラー=対話式セッション.communicate(timeout=15)
                assert 対話式セッション.returncode==0 and b'PTY allocation request failed' not in エラー,(対話式セッション.returncode,エラー)
                (出力/'ssh-interactive.txt').write_bytes(実行記録+剰余値)
            finally:
                選択状態値.close()
                if 対話式セッション.poll() is None:対話式セッション.kill();対話式セッション.wait()
            報告値['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 厳密に値(接続, 数):
                データ=bytearray()
                while len(データ)<数:
                    断片要素値=接続.recv(数-len(データ))
                    if not 断片要素値: raise AssertionError('RFB EOF')
                    データ.extend(断片要素値)
                return bytes(データ)
            def 画面認証(合言葉値):
                接続=socket.create_connection(('127.0.0.5',画面ポート),10);接続.settimeout(30)
                assert 厳密に値(接続,12)==b'RFB 003.008\n'
                接続.sendall(b'RFB 003.008\n');assert 厳密に値(接続,2)==b'\x01\x02'
                接続.sendall(b'\x02');検証課題値=厳密に値(接続,16)
                入力合言葉=合言葉値.encode('ascii')[:8].ljust(8, b'\0')
                キー素材=bytes(int('{:08b}'.format(数)[::-1],2) for 数 in 入力合言葉)
                接続.sendall(DES.new(キー素材,DES.MODE_ECB).encrypt(検証課題値))
                状況値=struct.unpack('!I',厳密に値(接続,4))[0]
                return 接続,状況値
            無効合言葉='!' if not 設定値['vnc_password'].startswith('!') else '?'
            接続,状況値=画面認証(無効合言葉);assert 状況値==1;接続.close();time.sleep(.6)
            報告値['checks'].append('VNC incorrect password rejected')
            接続,状況値=画面認証(設定値['vnc_password']);assert 状況値==0
            with 接続:
                接続.sendall(b'\x01');初期状況=厳密に値(接続,24);幅値,高さ値=struct.unpack('!HH',初期状況[:4]);名前=厳密に値(接続,struct.unpack('!I',初期状況[20:24])[0])
                assert (幅値,高さ値)==(640,480) and b'jkoros native'==名前
                def 画面(増分段階=0):
                    接続.sendall(struct.pack('!BBHHHH',3,増分段階,0,0,幅値,高さ値));先頭部値=厳密に値(接続,4);数=struct.unpack('!H',先頭部値[2:])[0];合計値=0
                    描画=bytearray(幅値*高さ値*4)
                    for _ in range(数):
                        横座標,縦座標,領域幅,領域高さ,メソッド方式=struct.unpack('!HHHHi',厳密に値(接続,12));assert メソッド方式==0 and 横座標+領域幅<=幅値 and 縦座標+領域高さ<=高さ値
                        画素=厳密に値(接続,領域幅*領域高さ*4);合計値+=len(画素)
                        for 行 in range(領域高さ):描画[((縦座標+行)*幅値+横座標)*4:((縦座標+行)*幅値+横座標+領域幅)*4]=画素[行*領域幅*4:(行+1)*領域幅*4]
                    if not 増分段階:
                        from PIL import Image
                        Image.frombytes('RGB',(幅値,高さ値),bytes(描画),'raw','BGRX').save(str(出力/'native-vnc.png'))
                    return 数,合計値
                数,合計値=画面();assert 数>0 and 合計値==幅値*高さ値*4
                報告値['checks'].append('Native framebuffer RFB full update {} bytes'.format(合計値))
                数,合計値=画面(1);assert 合計値<幅値*高さ値*4
                報告値['checks'].append('RFB incremental update')
                初期項目=len(履歴記録記録)
                for 文字値 in 'echo VNC_NATIVE_PASS\r':
                    記号=0xff0d if 文字値=='\r' else ord(文字値)
                    接続.sendall(struct.pack('!BBHI',4,1,0,記号));接続.sendall(struct.pack('!BBHI',4,0,0,記号))
                状況待合(b'VNC_NATIVE_PASS',初期項目)
                報告値['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def キー描線(記号,押下値=1):接続.sendall(struct.pack('!BBHI',4,押下値,0,記号))
                初期項目=len(履歴記録記録)
                for 文字値 in 'echo ':キー描線(ord(文字値))
                キー描線(0xffc6)
                for 文字値 in 'gksrmf':キー描線(ord(文字値))
                キー描線(0xffc6);キー描線(0xff0d)
                状況待合('\r\n한글\r\n'.encode(),初期項目)
                報告値['checks'].append('Native VNC F9 two-set Hangul composition')
                接続.sendall(struct.pack('!BBHH',5,0,120,100))
                報告値['checks'].append('VNC pointer input accepted')
            プロセス値.stdin.write(b'poweroff\n');プロセス値.stdin.flush();プロセス値.wait(timeout=15);assert プロセス値.returncode==0
            報告値['passed']=True
    finally:
        if プロセス値 and プロセス値.poll() is None:
            プロセス値.terminate()
            try: プロセス値.wait(timeout=5)
            except subprocess.TimeoutExpired: プロセス値.kill();プロセス値.wait()
        (出力/'serial.log').write_bytes(履歴記録記録)
        (出力/'report.json').write_text(json.dumps(報告値,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(報告値,ensure_ascii=False,indent=2))


if __name__=='__main__': 起動処理()
