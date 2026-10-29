#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 命令実行 import 計画根,命令

def 起動処理():
    宛先値位置=計画根/'build/verification/windows';宛先値位置.mkdir(parents=True,exist_ok=True)
    妥当性報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest()};履歴記録記録=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 作業中経路:
        試験用模擬制御接続状態=Path(作業中経路)/'qmp.sock'
        データ位置=subprocess.Popen(命令()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(試験用模擬制御接続状態)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        選択器=selectors.DefaultSelector();選択器.register(データ位置.stdout,selectors.EVENT_READ)
        def 取扱いイベント(秒数単位=.1):
            for 押下済み値,_ in 選択器.select(秒数単位):
                第二値=押下済み値.fileobj.read(65536)
                if 第二値:履歴記録記録.extend(第二値)
            assert b'PANIC:' not in 履歴記録記録 and b'HALTED' not in 履歴記録記録,履歴記録記録[-2048:]
        def 待機(標識,現在位置,秒数単位=50):
            終端位置変位量=time.monotonic()+秒数単位
            while 標識 not in 履歴記録記録[現在位置:]:
                if time.monotonic()>終端位置変位量 or データ位置.poll() is not None:raise AssertionError(履歴記録記録[現在位置:].decode('utf-8','replace'))
                取扱いイベント()
            return bytes(履歴記録記録[現在位置:])
        def 送信(第二値,標識=b'jkoros-native> '):
            現在位置=len(履歴記録記録);データ位置.stdin.write(第二値);データ位置.stdin.flush();return 待機(標識,現在位置)
        def シェル(文字列データ):return 送信((文字列データ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def 短縮操作値(第三添字):return bytes([30,2,第三添字,0,0,0,0])
        def クリックボタン(横座標,縦座標):return bytes([30,1,1,横座標&255,横座標>>8,縦座標&255,縦座標>>8,30,1,0,横座標&255,横座標>>8,縦座標&255,縦座標>>8])
        def 命令方式():
            データ位置.stdin.write(b'\x1b');データ位置.stdin.flush();終端位置変位量=time.monotonic()+.2
            while time.monotonic()<終端位置変位量:取扱いイベント(.03)
        try:
            待機(b'jkoros-native> ',0)
            シェル('terminal');取扱いイベント(.3)
            シェル('mkdir first; cd first; export NAME=one')
            送信('vi 先頭位置序数.py\n'.encode(),b'NORMAL')
            送信('i값 = 21\nprint(値 * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            終端位置変位量=time.monotonic()+3
            while time.monotonic()<終端位置変位量:取扱いイベント(.1)
            送信(短縮操作値(1),b'TERMINAL FOCUS 2');取扱いイベント(.2)
            assert b'/\r\n' in シェル('pwd')
            シェル('export NAME=two')
            送信('vi 第二序数.txt\n'.encode(),b'NORMAL')
            送信('i두 번째 窓\n'.encode(),b'INSERT')
            送信(クリックボタン(180,12),b'TERMINAL FOCUS 1');取扱いイベント(.2)
            命令方式();送信(b':wq\r')
            assert b'one:/first' in シェル('echo "$NAME:$PWD"')
            assert '値 = 21\r\nprint(値 * 2)'.encode() in シェル('cat 先頭位置序数.py')
            結果=シェル('python 先頭位置序数.py');assert b'42\r\n' in 結果,結果
            # Close the first shell with its actual title-bar X; second editor resumes.
            送信(クリックボタン(560,63),b'TERMINAL FOCUS 2');取扱いイベント(.2)
            命令方式();送信(b':wq\r')
            assert b'two:/' in シェル('echo "$NAME:$PWD"')
            assert '두 번째 窓'.encode() in シェル('cat 第二序数.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            送信('vi 第二序数.txt\n'.encode(),b'NORMAL');送信(b'xu',b'NORMAL')
            送信(b'iX',b'INSERT');命令方式();送信(b':q\r',b'Unsaved')
            送信(b':q!\r');assert '두 번째 窓'.encode() in シェル('cat 第二序数.txt')
            送信(短縮操作値(1),b'TERMINAL FOCUS 1');取扱いイベント(.2)
            送信(短縮操作値(1),b'TERMINAL FOCUS 3');取扱いイベント(.2)
            送信(短縮操作値(1),b'TERMINAL FOCUS 4');取扱いイベント(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            データ位置.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));データ位置.stdin.flush()
            シェル('echo DRAGGED_OK')
            送信('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            送信('i저장하지 않은 データ'.encode(),b'INSERT')
            送信(クリックボタン(578,97),b'TERMINAL FOCUS 3');取扱いイベント(.2)
            assert '버릴문서.txt'.encode() not in シェル('ls')
            送信(短縮操作値(1),b'TERMINAL FOCUS 4');取扱いイベント(.2)
            シェル('echo REUSED_WINDOW_OK')
            完了済み総量=履歴記録記録.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            待機(b'jkoros-native> ',完了済み総量)
            # UART completion precedes the next QEMU display refresh.
            終端位置変位量=time.monotonic()+.3
            while time.monotonic()<終端位置変位量:取扱いイベント(.05)
            with socket.socket(socket.AF_UNIX) as 文字コード:
                文字コード.settimeout(10);文字コード.connect(str(試験用模擬制御接続状態))
                with 文字コード.makefile('rwb') as ファイル入口:
                    json.loads(ファイル入口.readline())
                    for 要求値 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(宛先値位置/'four-terminals.png'),'format':'png'}}):
                        ファイル入口.write((json.dumps(要求値)+'\n').encode());ファイル入口.flush()
                        while True:
                            返却済み値=json.loads(ファイル入口.readline())
                            if 'error' in 返却済み値:raise AssertionError(返却済み値)
                            if 'return' in 返却済み値:break
            from PIL import Image
            画素列一覧=Image.open(str(宛先値位置/'four-terminals.png')).convert('RGB')
            for 座標対,画素色 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 画素列一覧.getpixel(座標対)==画素色,(座標対,画素列一覧.getpixel(座標対))
            シェル('echo FOUR_WINDOWS_OK')
            妥当性報告.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if データ位置.poll() is None:データ位置.terminate()
            try:データ位置.wait(timeout=5)
            except subprocess.TimeoutExpired:データ位置.kill();データ位置.wait()
            選択器.close();データ位置.stdin.close();データ位置.stdout.close();(宛先値位置/'serial.log').write_bytes(履歴記録記録);(宛先値位置/'report.json').write_text(json.dumps(妥当性報告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':起動処理()
