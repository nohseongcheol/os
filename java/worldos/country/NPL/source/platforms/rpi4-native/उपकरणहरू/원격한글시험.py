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
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट


def चलाउनुहोस्():
    मापन_लगत=परियोजना_रूट/'build/verification/remmina';मापन_लगत.mkdir(parents=True,exist_ok=True)
    वैधानिकता_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];चयनकर्ता=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            अवास्तविक_प्रदर्शन=shutil.which('Xvfb')
            if अवास्तविक_प्रदर्शन: सर्भर_मान=[अवास्तविक_प्रदर्शन]
            else:
                뿌리파일계층=परियोजना_रूट.parent/'rpi4/build/rootfs'
                सर्भर_मान=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def चलाउनुहोस्(तर्क_विन्यास,환경=None,**이름붙인인수):
                लग_रेकर्ड=(मापन_लगत/('process-%d.log'%len(기록들))).open('wb');기록들.append(लग_रेकर्ड)
                लगत_राख्नुहोस्=subprocess.Popen(तर्क_विन्यास,env=환경,stdout=लग_रेकर्ड,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(लगत_राख्नुहोस्);return लगत_राख्नुहोस्
            환경=dict(os.environ)
            for नाम in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(नाम,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            प्रदर्शन=चलाउनुहोस्(सर्भर_मान+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert प्रदर्शन.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            अतिथि=subprocess.Popen(['python3',str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(अतिथि);चयनकर्ता.register(अतिथि.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,अफसेट_मान=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[अफसेट_मान:]:
                    assert अतिथि.poll() is None and time.monotonic()<마감시각,직렬입출력[अफसेट_मान:].decode('utf-8','replace')
                    for 누름값,_ in चयनकर्ता.select(.1):
                        लगत=누름값.fileobj.read(65536)
                        if लगत:직렬입출력.extend(लगत)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            प्रोफाइल=작업경로/'test.remmina'
            प्रोफाइल.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            चलाउनुहोस्(['dbus-run-session','--','remmina','-c',str(प्रोफाइल)],환경=환경,start_new_session=True)
            def 가상입력도구(*तर्क_विन्यास):return subprocess.check_output(['xdotool']+list(तर्क_विन्यास),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;सन्झ्याल=None
            while time.monotonic()<마감시각:
                खोज_मापन=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if खोज_मापन.returncode==0:
                    후보=खोज_मापन.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    केन्द्रित=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if केन्द्रित.returncode==0:सन्झ्याल=후보;break
                time.sleep(.1)
            assert सन्झ्याल,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',सन्झ्याल,'280','240','click','1')
            time.sleep(1)
            def 글자입력(पाठ):가상입력도구('type','--clearmodifiers','--delay','50',पाठ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            अफसेट_मान=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),अफसेट_मान)
            अफसेट_मान=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),अफसेट_मान)
            अफसेट_मान=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 कुञ्जी_मान, Shift+Space 또는 F9'.encode(),अफसेट_मान);기다리기(b'jkoros-native> ',अफसेट_मान)
            अफसेट_मान=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),अफसेट_मान)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',सन्झ्याल,str(मापन_लगत/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',अफसेट_मान)
            # वास्तविक_लगत Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            चित्रकारी_मान=Image.open(str(मापन_लगत/'remmina-korean.png')).convert('RGB')
            शीर्षकपट्टी=None
            for ठाडो_राख्नुहोस् in range(चित्रकारी_मान.height):
                가로들=[가로 for 가로 in range(चित्रकारी_मान.width) if चित्रकारी_मान.getpixel((가로,ठाडो_राख्नुहोस्))==(32,80,144)]
                if len(가로들)>=500:शीर्षकपट्टी=(min(가로들),ठाडो_राख्नुहोस्);break
            assert शीर्षकपट्टी,'native terminal title bar not found'
            가로,ठाडो_राख्नुहोस्=शीर्षकपट्टी[0]+564,शीर्षकपट्टी[1]+356
            가상입력도구('mousemove','--window',सन्झ्याल,str(가로),str(ठाडो_राख्नुहोस्))
            def 화상기다리기(नाम,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',सन्झ्याल,str(मापन_लगत/नाम)])
                    बिटम्याप_छवि=Image.open(str(मापन_लगत/नाम)).convert('RGB')
                    if all(बिटम्याप_छवि.getpixel(स्थिति)==빛 for स्थिति,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+नाम
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,ठाडो_राख्नुहोस्-7),(255,255,255)),((가로+7,ठाडो_राख्नुहोस्+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',सन्झ्याल,str(가로-120),str(ठाडो_राख्नुहोस्-80),'mouseup','1')
            time.sleep(.4)
            अफसेट_मान=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',अफसेट_मान)
            가상입력도구('mousemove','--window',सन्झ्याल,'500','45')
            화상기다리기('remmina-resized.png',[
                ((शीर्षकपट्टी[0]+447,शीर्षकपट्टी[1]+279),(39,49,64)),((가로,ठाडो_राख्नुहोस्),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            वैधानिकता_रिपोर्ट.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not वैधानिकता_रिपोर्ट['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(मापन_लगत/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for लगत_राख्नुहोस् in reversed(실행과정들):
                if लगत_राख्नुहोस्.poll() is None:
                    if लगत_राख्नुहोस्.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(लगत_राख्नुहोस्.pid,signal.SIGTERM)
                    else:लगत_राख्नुहोस्.terminate()
                    try:लगत_राख्नुहोस्.wait(timeout=5)
                    except subprocess.TimeoutExpired:लगत_राख्नुहोस्.kill();लगत_राख्नुहोस्.wait()
            चयनकर्ता.close()
            for फाइल_प्रविष्टि in 기록들:फाइल_प्रविष्टि.close()
            (मापन_लगत/'serial.log').write_bytes(직렬입출력)
            (मापन_लगत/'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':चलाउनुहोस्()
