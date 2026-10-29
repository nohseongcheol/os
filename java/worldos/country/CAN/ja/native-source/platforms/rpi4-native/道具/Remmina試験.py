#!/usr/bin/env python3
"""Exercise the installed Remmina in an isolated X display and D-Bus session.

Needs Remmina's VNC plugin, xdotool, Xvfb (or the existing ARM64 Xvfb rootfs
and qemu-aarch64), dbus-run-session, and ImageMagick import. Never uses :0.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from 命令実行 import 計画根


def 起動処理():
    結果データ=計画根/'build/verification/remmina';結果データ.mkdir(parents=True,exist_ok=True)
    妥当性報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 作業中経路:
        作業中経路=Path(作業中経路);稼働状態プロセス一覧=[];準備監視器=selectors.DefaultSelector();直列入出力=bytearray()
        履歴記録記録一覧=[]
        try:
            仮想表示処理=shutil.which('Xvfb')
            if 仮想表示処理: サーバー値=[仮想表示処理]
            else:
                ルートファイル体系=計画根.parent/'rpi4/build/rootfs'
                サーバー値=['qemu-aarch64','-L',str(ルートファイル体系),str(ルートファイル体系/'usr/bin/Xvfb')]
            def 起動処理(引数配列,環境=None,**命名済み引数):
                履歴記録記録=(結果データ/('process-%d.log'%len(履歴記録記録一覧))).open('wb');履歴記録記録一覧.append(履歴記録記録)
                データ位置=subprocess.Popen(引数配列,env=環境,stdout=履歴記録記録,stderr=subprocess.STDOUT,**命名済み引数)
                稼働状態プロセス一覧.append(データ位置);return データ位置
            環境=dict(os.environ)
            for 名前 in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):環境.pop(名前,None)
            環境.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(作業中経路/'config'),XDG_DATA_HOME=str(作業中経路/'data'),XDG_CACHE_HOME=str(作業中経路/'cache'))
            数値値=next(項目個数 for 項目個数 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(項目個数)).exists() and not Path('/tmp/.X%d-lock'%項目個数).exists())
            環境['DISPLAY']=':'+str(数値値)
            表示処理装置=起動処理(サーバー値+[環境['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],環境=環境)
            期限時間=time.monotonic()+30
            while True:
                assert 表示処理装置.poll() is None and time.monotonic()<期限時間,'Xvfb failed; see process-0.log'
                用意状態完了=subprocess.run(['xdotool','getdisplaygeometry'],env=環境,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 用意状態完了.returncode==0:break
                time.sleep(.1)
            ゲスト=subprocess.Popen(['python3',str(計画根/'道具/命令実行.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            稼働状態プロセス一覧.append(ゲスト);準備監視器.register(ゲスト.stdout,selectors.EVENT_READ)
            def 待機(標識,変位量値=0):
                期限時間=time.monotonic()+45
                while 標識 not in 直列入出力[変位量値:]:
                    assert ゲスト.poll() is None and time.monotonic()<期限時間,直列入出力[変位量値:].decode('utf-8','replace')
                    for 押下済み値,_ in 準備監視器.select(.1):
                        データ=押下済み値.fileobj.read(65536)
                        if データ:直列入出力.extend(データ)
            待機(b'TERMINAL READY');待機(b'jkoros-native> ',直列入出力.rfind(b'TERMINAL READY'))
            ポート番号=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',直列入出力).group(1))
            動作設定=作業中経路/'test.remmina'
            動作設定.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%ポート番号)
            起動処理(['dbus-run-session','--','remmina','-c',str(動作設定)],環境=環境,start_new_session=True)
            def 仮想入力道具要素(*引数配列):return subprocess.check_output(['xdotool']+list(引数配列),env=環境,stderr=subprocess.STDOUT)
            期限時間=time.monotonic()+60;窓=None
            while time.monotonic()<期限時間:
                結果捜索=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=環境,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if 結果捜索.returncode==0:
                    候補=結果捜索.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    焦点対象=subprocess.run(['xdotool','windowfocus','--sync',候補],env=環境,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if 焦点対象.returncode==0:窓=候補;break
                time.sleep(.1)
            assert 窓,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            仮想入力道具要素('mousemove','--window',窓,'280','240','click','1')
            time.sleep(1)
            def 型付き文字(文):仮想入力道具要素('type','--clearmodifiers','--delay','50',文)
            def 押下済み値(*押下済みキー一覧):仮想入力道具要素('key','--clearmodifiers',*押下済みキー一覧)
            変位量値=len(直列入出力);型付き文字('echo ');押下済み値('F9');型付き文字('dkssudgktpdy gksrmf');押下済み値('F9','Return')
            待機('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),変位量値)
            変位量値=len(直列入出力);型付き文字('echo ');押下済み値('shift+space');型付き文字('rhk rkqtk');押下済み値('shift+space','Return')
            待機('\r\n과 갑사\r\njkoros-native> '.encode(),変位量値)
            変位量値=len(直列入出力);型付き文字('help ko');押下済み値('Return')
            待機('한/零被演算子 キー値, Shift+Space 또는 F9'.encode(),変位量値);待機(b'jkoros-native> ',変位量値)
            変位量値=len(直列入出力);型付き文字('echo ');押下済み値('F9');型付き文字('gksrmf dlfr')
            待機('읽'.encode(),変位量値)
            subprocess.check_call(['import','-display',環境['DISPLAY'],'-window',窓,str(結果データ/'remmina-korean.png')])
            押下済み値('F9','Return')
            待機(b'jkoros-native> ',変位量値)
            # 実際データ Remmina의 画面 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            描画=Image.open(str(結果データ/'remmina-korean.png')).convert('RGB')
            表題棒=None
            for 垂直位置 in range(描画.height):
                水平位置一覧=[水平位置 for 水平位置 in range(描画.width) if 描画.getpixel((水平位置,垂直位置))==(32,80,144)]
                if len(水平位置一覧)>=500:表題棒=(min(水平位置一覧),垂直位置);break
            assert 表題棒,'native terminal title bar not found'
            水平位置,垂直位置=表題棒[0]+564,表題棒[1]+356
            仮想入力道具要素('mousemove','--window',窓,str(水平位置),str(垂直位置))
            def 対象ビットマップ待合(名前,点一覧一覧):
                期限値=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',環境['DISPLAY'],'-window',窓,str(結果データ/名前)])
                    ビットマップイメージ=Image.open(str(結果データ/名前)).convert('RGB')
                    if all(ビットマップイメージ.getpixel(位置)==色 for 位置,色 in 点一覧一覧):return
                    assert time.monotonic()<期限値,'Remmina framebuffer did not settle: '+名前
                    time.sleep(.1)
            対象ビットマップ待合('remmina-resize-cursor.png',[
                ((水平位置-7,垂直位置-7),(255,255,255)),((水平位置+7,垂直位置+7),(255,255,255))])
            仮想入力道具要素('mousedown','1','mousemove','--window',窓,str(水平位置-120),str(垂直位置-80),'mouseup','1')
            time.sleep(.4)
            変位量値=len(直列入出力);型付き文字('terminal size');押下済み値('Return')
            待機(b'TERMINAL SIZE 53x14\r\n',変位量値)
            仮想入力道具要素('mousemove','--window',窓,'500','45')
            対象ビットマップ待合('remmina-resized.png',[
                ((表題棒[0]+447,表題棒[1]+279),(39,49,64)),((水平位置,垂直位置),(24,32,48))])
            if shutil.which('dpkg-query'):
                版番号=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                版番号=subprocess.check_output(['remmina','--version'],env=環境,stderr=subprocess.STDOUT).decode('utf-8','replace')
            妥当性報告.update(passed=True,display=環境['DISPLAY'],remmina_version=版番号,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not 妥当性報告['passed'] and '環境' in locals() and 環境.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',環境['DISPLAY'],'-window','root',str(結果データ/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for データ位置 in reversed(稼働状態プロセス一覧):
                if データ位置.poll() is None:
                    if データ位置.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(データ位置.pid,signal.SIGTERM)
                    else:データ位置.terminate()
                    try:データ位置.wait(timeout=5)
                    except subprocess.TimeoutExpired:データ位置.kill();データ位置.wait()
            準備監視器.close()
            for ファイル入口 in 履歴記録記録一覧:ファイル入口.close()
            (結果データ/'serial.log').write_bytes(直列入出力)
            (結果データ/'report.json').write_text(json.dumps(妥当性報告,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':起動処理()
