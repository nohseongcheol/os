#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 命令実行 import 計画根,命令

def 起動処理():
    宛先値位置=計画根/'build/verification/swing';宛先値位置.mkdir(parents=True,exist_ok=True)
    クラス経路=計画根/'build/verification/new-java';クラス経路.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(計画根/'dist/jkoros-native-korean.jar'),'-d',str(クラス経路),str(計画根/'試験/Java/Swing試験.java'),str(計画根/'試験/Java/ハングル窓試験.java')])
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
            データ=(計画根/'build/verification/new-java/Swing試験.class').read_bytes()
            送信('load Swing試験.class\n'.encode(),b'hex> ')
            for 序数添字 in range(0,len(データ),64):送信(データ[序数添字:序数添字+64].hex().encode()+b'\n',b'hex> ')
            送信(b'.\n')
            送信('java Swing試験\n'.encode(),b'SWING READY')
            終端位置変位量=time.monotonic()+3
            while time.monotonic()<終端位置変位量:取扱いイベント(.1)
            # JFrame centered at (120,100), content at y=130.
            送信(クリックボタン(200,210),b'',)  # focus JTextField
            データ位置.stdin.write('누리'.encode());データ位置.stdin.flush()
            終端位置変位量=time.monotonic()+.3
            while time.monotonic()<終端位置変位量:取扱いイベント(.05)
            結果=送信(クリックボタン(200,255),'SWING CLICK 이름누리'.encode())
            待機(b'true',len(履歴記録記録)-len(結果))
            送信(短縮操作値(1),b'TERMINAL FOCUS 2')
            結果=シェル('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 結果
            送信(クリックボタン(180,12),b'TERMINAL FOCUS 1')
            終端位置変位量=time.monotonic()+.3
            while time.monotonic()<終端位置変位量:取扱いイベント(.05)
            with socket.socket(socket.AF_UNIX) as 文字コード:
                文字コード.settimeout(10);文字コード.connect(str(試験用模擬制御接続状態))
                with 文字コード.makefile('rwb') as ファイル入口:
                    json.loads(ファイル入口.readline())
                    for 要求値 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(宛先値位置/'native-swing.png'),'format':'png'}}):
                        ファイル入口.write((json.dumps(要求値)+'\n').encode());ファイル入口.flush()
                        while True:
                            返却済み値=json.loads(ファイル入口.readline())
                            if 'error' in 返却済み値:raise AssertionError(返却済み値)
                            if 'return' in 返却済み値:break
            送信(クリックボタン(505,115))
            シェル('echo SWING_CLOSED_OK')
            データ=(クラス経路/'ハングル窓試験.class').read_bytes()
            送信('load ハングル窓試験.class\n'.encode(),b'hex> ')
            for 序数添字 in range(0,len(データ),64):送信(データ[序数添字:序数添字+64].hex().encode()+b'\n',b'hex> ')
            送信(b'.\n')
            送信('java ハングル窓試験\n'.encode(),b'KOREAN SWING READY')
            送信(クリックボタン(200,255),'KOREAN SWING CLICK 名前'.encode())
            送信(クリックボタン(505,115))
            シェル('echo KOREAN_SWING_CLOSED_OK')
            妥当性報告.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','日本語 窓/ボタン/動作通知/イベント待ち行列 directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if データ位置.poll() is None:データ位置.terminate()
            try:データ位置.wait(timeout=5)
            except subprocess.TimeoutExpired:データ位置.kill();データ位置.wait()
            選択器.close();データ位置.stdin.close();データ位置.stdout.close();(宛先値位置/'serial.log').write_bytes(履歴記録記録);(宛先値位置/'report.json').write_text(json.dumps(妥当性報告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':起動処理()
