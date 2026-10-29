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
from לבצע_פקודה import לשקף_בסיס


def הפעלה():
    תוצאה_נתונים=לשקף_בסיס/'build/verification/remmina';תוצאה_נתונים.mkdir(parents=True,exist_ok=True)
    אימות_דוח={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];בורר=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            וירטואלי_צג=shutil.which('Xvfb')
            if וירטואלי_צג: שרת_ערך=[וירטואלי_צג]
            else:
                뿌리파일계층=לשקף_בסיס.parent/'rpi4/build/rootfs'
                שרת_ערך=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def הפעלה(ארגומנט_מערך,סביבה=None,**ארגומנט_בעל_שם):
                לרשום_שיא=(תוצאה_נתונים/('process-%d.log'%len(기록들))).open('wb');기록들.append(לרשום_שיא)
                נתונים_עמדה=subprocess.Popen(ארגומנט_מערך,env=סביבה,stdout=לרשום_שיא,stderr=subprocess.STDOUT,**ארגומנט_בעל_שם)
                실행과정들.append(נתונים_עמדה);return נתונים_עמדה
            סביבה=dict(os.environ)
            for שם in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):סביבה.pop(שם,None)
            סביבה.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            סביבה['DISPLAY']=':'+str(수치)
            צג=הפעלה(שרת_ערך+[סביבה['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],סביבה=סביבה)
            תאריך_יעד_זמן=time.monotonic()+30
            while True:
                assert צג.poll() is None and time.monotonic()<תאריך_יעד_זמן,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=סביבה,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            אורח=subprocess.Popen(['python3',str(לשקף_בסיס/'כלים/לבצע_פקודה.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(אורח);בורר.register(אורח.stdout,selectors.EVENT_READ)
            def 기다리기(סמן,היסט_ערך=0):
                תאריך_יעד_זמן=time.monotonic()+45
                while סמן not in 직렬입출력[היסט_ערך:]:
                    assert אורח.poll() is None and time.monotonic()<תאריך_יעד_זמן,직렬입출력[היסט_ערך:].decode('utf-8','replace')
                    for 누름값,_ in בורר.select(.1):
                        נתונים=누름값.fileobj.read(65536)
                        if נתונים:직렬입출력.extend(נתונים)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            מספר_יציאה=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            פרופיל=작업경로/'test.remmina'
            פרופיל.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%מספר_יציאה)
            הפעלה(['dbus-run-session','--','remmina','-c',str(פרופיל)],סביבה=סביבה,start_new_session=True)
            def וירטואלי_קלט_כלי(*ארגומנט_מערך):return subprocess.check_output(['xdotool']+list(ארגומנט_מערך),env=סביבה,stderr=subprocess.STDOUT)
            תאריך_יעד_זמן=time.monotonic()+60;חלון=None
            while time.monotonic()<תאריך_יעד_זמן:
                חפש_תוצאה=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=סביבה,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if חפש_תוצאה.returncode==0:
                    후보=חפש_תוצאה.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ממוקד=subprocess.run(['xdotool','windowfocus','--sync',후보],env=סביבה,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ממוקד.returncode==0:חלון=후보;break
                time.sleep(.1)
            assert חלון,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            וירטואלי_קלט_כלי('mousemove','--window',חלון,'280','240','click','1')
            time.sleep(1)
            def 글자입력(טקסט):וירטואלי_קלט_כלי('type','--clearmodifiers','--delay','50',טקסט)
            def 누름값(*누름열):וירטואלי_קלט_כלי('key','--clearmodifiers',*누름열)
            היסט_ערך=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),היסט_ערך)
            היסט_ערך=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),היסט_ערך)
            היסט_ערך=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/אפס_אופרנד מקש_ערך, Shift+Space 또는 F9'.encode(),היסט_ערך);기다리기(b'jkoros-native> ',היסט_ערך)
            היסט_ערך=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),היסט_ערך)
            subprocess.check_call(['import','-display',סביבה['DISPLAY'],'-window',חלון,str(תוצאה_נתונים/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',היסט_ערך)
            # בפועל_נתונים Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ציור_ערך=Image.open(str(תוצאה_נתונים/'remmina-korean.png')).convert('RGB')
            פס_כותרת=None
            for אנכי_עמדה in range(ציור_ערך.height):
                가로들=[가로 for 가로 in range(ציור_ערך.width) if ציור_ערך.getpixel((가로,אנכי_עמדה))==(32,80,144)]
                if len(가로들)>=500:פס_כותרת=(min(가로들),אנכי_עמדה);break
            assert פס_כותרת,'native terminal title bar not found'
            가로,אנכי_עמדה=פס_כותרת[0]+564,פס_כותרת[1]+356
            וירטואלי_קלט_כלי('mousemove','--window',חלון,str(가로),str(אנכי_עמדה))
            def 화상기다리기(שם,점들):
                תאריך_יעד_ערך=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',סביבה['DISPLAY'],'-window',חלון,str(תוצאה_נתונים/שם)])
                    מפת_סיביות_תמונה=Image.open(str(תוצאה_נתונים/שם)).convert('RGB')
                    if all(מפת_סיביות_תמונה.getpixel(מיקום)==빛 for מיקום,빛 in 점들):return
                    assert time.monotonic()<תאריך_יעד_ערך,'Remmina framebuffer did not settle: '+שם
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,אנכי_עמדה-7),(255,255,255)),((가로+7,אנכי_עמדה+7),(255,255,255))])
            וירטואלי_קלט_כלי('mousedown','1','mousemove','--window',חלון,str(가로-120),str(אנכי_עמדה-80),'mouseup','1')
            time.sleep(.4)
            היסט_ערך=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',היסט_ערך)
            וירטואלי_קלט_כלי('mousemove','--window',חלון,'500','45')
            화상기다리기('remmina-resized.png',[
                ((פס_כותרת[0]+447,פס_כותרת[1]+279),(39,49,64)),((가로,אנכי_עמדה),(24,32,48))])
            if shutil.which('dpkg-query'):
                מספר_גירסה=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                מספר_גירסה=subprocess.check_output(['remmina','--version'],env=סביבה,stderr=subprocess.STDOUT).decode('utf-8','replace')
            אימות_דוח.update(passed=True,display=סביבה['DISPLAY'],remmina_version=מספר_גירסה,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not אימות_דוח['passed'] and 'סביבה' in locals() and סביבה.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',סביבה['DISPLAY'],'-window','root',str(תוצאה_נתונים/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for נתונים_עמדה in reversed(실행과정들):
                if נתונים_עמדה.poll() is None:
                    if נתונים_עמדה.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(נתונים_עמדה.pid,signal.SIGTERM)
                    else:נתונים_עמדה.terminate()
                    try:נתונים_עמדה.wait(timeout=5)
                    except subprocess.TimeoutExpired:נתונים_עמדה.kill();נתונים_עמדה.wait()
            בורר.close()
            for קובץ_ערך in 기록들:קובץ_ערך.close()
            (תוצאה_נתונים/'serial.log').write_bytes(직렬입출력)
            (תוצאה_נתונים/'report.json').write_text(json.dumps(אימות_דוח,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':הפעלה()
