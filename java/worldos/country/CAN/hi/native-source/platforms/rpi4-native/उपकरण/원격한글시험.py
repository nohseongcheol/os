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
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल


def चलाएँ():
    परिणाम_डेटा=प्रोजेक्ट_करें_मूल/'build/verification/remmina';परिणाम_डेटा.mkdir(parents=True,exist_ok=True)
    प्रमाणीकरण_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];सिलेक्टर=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: 서버=[가상표시장치]
            else:
                뿌리파일계층=प्रोजेक्ट_करें_मूल.parent/'rpi4/build/rootfs'
                서버=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def चलाएँ(तर्क_सरणी,환경=None,**नामित_तर्क):
                लॉग_रिकॉर्ड=(परिणाम_डेटा/('process-%d.log'%len(기록들))).open('wb');기록들.append(लॉग_रिकॉर्ड)
                डेटा_पद=subprocess.Popen(तर्क_सरणी,env=환경,stdout=लॉग_रिकॉर्ड,stderr=subprocess.STDOUT,**नामित_तर्क)
                실행과정들.append(डेटा_पद);return डेटा_पद
            환경=dict(os.environ)
            for नाम in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(नाम,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            डिस्प्ले=चलाएँ(서버+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            अंति_म_समय_सीमा_समय=time.monotonic()+30
            while True:
                assert डिस्प्ले.poll() is None and time.monotonic()<अंति_म_समय_सीमा_समय,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            अतिथि=subprocess.Popen(['python3',str(प्रोजेक्ट_करें_मूल/'उपकरण/निष्पादित_करें_आदेश.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(अतिथि);सिलेक्टर.register(अतिथि.stdout,selectors.EVENT_READ)
            def 기다리기(मार्कर,ऑफ़सेट_मान=0):
                अंति_म_समय_सीमा_समय=time.monotonic()+45
                while मार्कर not in 직렬입출력[ऑफ़सेट_मान:]:
                    assert अतिथि.poll() is None and time.monotonic()<अंति_म_समय_सीमा_समय,직렬입출력[ऑफ़सेट_मान:].decode('utf-8','replace')
                    for 누름값,_ in सिलेक्टर.select(.1):
                        आँकड़े=누름값.fileobj.read(65536)
                        if आँकड़े:직렬입출력.extend(आँकड़े)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            पोर्ट_संख्या=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            प्रोफ़ाइल=작업경로/'test.remmina'
            प्रोफ़ाइल.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%पोर्ट_संख्या)
            चलाएँ(['dbus-run-session','--','remmina','-c',str(प्रोफ़ाइल)],환경=환경,start_new_session=True)
            def 가상입력도구(*तर्क_सरणी):return subprocess.check_output(['xdotool']+list(तर्क_सरणी),env=환경,stderr=subprocess.STDOUT)
            अंति_म_समय_सीमा_समय=time.monotonic()+60;खिड़की=None
            while time.monotonic()<अंति_म_समय_सीमा_समय:
                खोज_परिणाम=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if खोज_परिणाम.returncode==0:
                    후보=खोज_परिणाम.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    केंद्रित=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if केंद्रित.returncode==0:खिड़की=후보;break
                time.sleep(.1)
            assert खिड़की,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',खिड़की,'280','240','click','1')
            time.sleep(1)
            def 글자입력(पाठ):가상입력도구('type','--clearmodifiers','--delay','50',पाठ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ऑफ़सेट_मान=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/शून्य_ऑपरेंड कुंजी_मान, Shift+Space 또는 F9'.encode(),ऑफ़सेट_मान);기다리기(b'jkoros-native> ',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ऑफ़सेट_मान)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',खिड़की,str(परिणाम_डेटा/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ऑफ़सेट_मान)
            # वास्तविक_डेटा Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ड्रॉइंग_मान=Image.open(str(परिणाम_डेटा/'remmina-korean.png')).convert('RGB')
            शीर्षक_बार=None
            for अनुलंब_पद in range(ड्रॉइंग_मान.height):
                가로들=[가로 for 가로 in range(ड्रॉइंग_मान.width) if ड्रॉइंग_मान.getpixel((가로,अनुलंब_पद))==(32,80,144)]
                if len(가로들)>=500:शीर्षक_बार=(min(가로들),अनुलंब_पद);break
            assert शीर्षक_बार,'native terminal title bar not found'
            가로,अनुलंब_पद=शीर्षक_बार[0]+564,शीर्षक_बार[1]+356
            가상입력도구('mousemove','--window',खिड़की,str(가로),str(अनुलंब_पद))
            def 화상기다리기(नाम,점들):
                अंति_म_समय_सीमा_मान=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',खिड़की,str(परिणाम_डेटा/नाम)])
                    बिटमैप_छवि=Image.open(str(परिणाम_डेटा/नाम)).convert('RGB')
                    if all(बिटमैप_छवि.getpixel(स्थान)==빛 for स्थान,빛 in 점들):return
                    assert time.monotonic()<अंति_म_समय_सीमा_मान,'Remmina framebuffer did not settle: '+नाम
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,अनुलंब_पद-7),(255,255,255)),((가로+7,अनुलंब_पद+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',खिड़की,str(가로-120),str(अनुलंब_पद-80),'mouseup','1')
            time.sleep(.4)
            ऑफ़सेट_मान=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ऑफ़सेट_मान)
            가상입력도구('mousemove','--window',खिड़की,'500','45')
            화상기다리기('remmina-resized.png',[
                ((शीर्षक_बार[0]+447,शीर्षक_बार[1]+279),(39,49,64)),((가로,अनुलंब_पद),(24,32,48))])
            if shutil.which('dpkg-query'):
                संस्करण_संख्या=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                संस्करण_संख्या=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            प्रमाणीकरण_रिपोर्ट.update(passed=True,display=환경['DISPLAY'],remmina_version=संस्करण_संख्या,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not प्रमाणीकरण_रिपोर्ट['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(परिणाम_डेटा/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for डेटा_पद in reversed(실행과정들):
                if डेटा_पद.poll() is None:
                    if डेटा_पद.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(डेटा_पद.pid,signal.SIGTERM)
                    else:डेटा_पद.terminate()
                    try:डेटा_पद.wait(timeout=5)
                    except subprocess.TimeoutExpired:डेटा_पद.kill();डेटा_पद.wait()
            सिलेक्टर.close()
            for फ़ाइल_एन्ट्री in 기록들:फ़ाइल_एन्ट्री.close()
            (परिणाम_डेटा/'serial.log').write_bytes(직렬입출력)
            (परिणाम_डेटा/'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':चलाएँ()
