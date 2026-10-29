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
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट


def चलोवप():
    मेजप_डेटा=प्रॉजॅक्ट_रूट/'build/verification/remmina';मेजप_डेटा.mkdir(parents=True,exist_ok=True)
    वैधताय_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];वेंचक=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            भ्रामक_प्रदर्शन=shutil.which('Xvfb')
            if भ्रामक_प्रदर्शन: सर्वर_मोल=[भ्रामक_प्रदर्शन]
            else:
                뿌리파일계층=प्रॉजॅक्ट_रूट.parent/'rpi4/build/rootfs'
                सर्वर_मोल=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def चलोवप(युक्तीवाद_क्रम,환경=None,**이름붙인인수):
                LOG_नोंद=(मेजप_डेटा/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_नोंद)
                डेटा_स्थिती=subprocess.Popen(युक्तीवाद_क्रम,env=환경,stdout=LOG_नोंद,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(डेटा_स्थिती);return डेटा_स्थिती
            환경=dict(os.environ)
            for नांव in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(नांव,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(आयटम_COUNT for आयटम_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(आयटम_COUNT)).exists() and not Path('/tmp/.X%d-lock'%आयटम_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            प्रदर्शन=चलोवप(सर्वर_मोल+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert प्रदर्शन.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            सोयरो=subprocess.Popen(['python3',str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_आदेश.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(सोयरो);वेंचक.register(सोयरो.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ऑफसॅट_मोल=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ऑफसॅट_मोल:]:
                    assert सोयरो.poll() is None and time.monotonic()<마감시각,직렬입출력[ऑफसॅट_मोल:].decode('utf-8','replace')
                    for 누름값,_ in वेंचक.select(.1):
                        डेटा=누름값.fileobj.read(65536)
                        if डेटा:직렬입출력.extend(डेटा)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            प्रोफायल=작업경로/'test.remmina'
            प्रोफायल.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            चलोवप(['dbus-run-session','--','remmina','-c',str(प्रोफायल)],환경=환경,start_new_session=True)
            def 가상입력도구(*युक्तीवाद_क्रम):return subprocess.check_output(['xdotool']+list(युक्तीवाद_क्रम),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;विंडो=None
            while time.monotonic()<마감시각:
                सोद_मेजप=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if सोद_मेजप.returncode==0:
                    후보=सोद_मेजप.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    केंद्रीत=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if केंद्रीत.returncode==0:विंडो=후보;break
                time.sleep(.1)
            assert विंडो,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',विंडो,'280','240','click','1')
            time.sleep(1)
            def 글자입력(SMS):가상입력도구('type','--clearmodifiers','--delay','50',SMS)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ऑफसॅट_मोल=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ऑफसॅट_मोल)
            ऑफसॅट_मोल=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ऑफसॅट_मोल)
            ऑफसॅट_मोल=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 की_मोल, Shift+Space 또는 F9'.encode(),ऑफसॅट_मोल);기다리기(b'jkoros-native> ',ऑफसॅट_मोल)
            ऑफसॅट_मोल=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ऑफसॅट_मोल)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',विंडो,str(मेजप_डेटा/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ऑफसॅट_मोल)
            # प्रत्यक्ष_डेटा Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            रेखाटन_मोल=Image.open(str(मेजप_डेटा/'remmina-korean.png')).convert('RGB')
            शीर्षक_पट्टी=None
            for उबें_स्थिती in range(रेखाटन_मोल.height):
                가로들=[가로 for 가로 in range(रेखाटन_मोल.width) if रेखाटन_मोल.getpixel((가로,उबें_स्थिती))==(32,80,144)]
                if len(가로들)>=500:शीर्षक_पट्टी=(min(가로들),उबें_स्थिती);break
            assert शीर्षक_पट्टी,'native terminal title bar not found'
            가로,उबें_स्थिती=शीर्षक_पट्टी[0]+564,शीर्षक_पट्टी[1]+356
            가상입력도구('mousemove','--window',विंडो,str(가로),str(उबें_स्थिती))
            def 화상기다리기(नांव,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',विंडो,str(मेजप_डेटा/नांव)])
                    बिटमॅप_IMAGE=Image.open(str(मेजप_डेटा/नांव)).convert('RGB')
                    if all(बिटमॅप_IMAGE.getpixel(स्थिती)==빛 for स्थिती,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+नांव
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,उबें_स्थिती-7),(255,255,255)),((가로+7,उबें_स्थिती+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',विंडो,str(가로-120),str(उबें_स्थिती-80),'mouseup','1')
            time.sleep(.4)
            ऑफसॅट_मोल=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ऑफसॅट_मोल)
            가상입력도구('mousemove','--window',विंडो,'500','45')
            화상기다리기('remmina-resized.png',[
                ((शीर्षक_पट्टी[0]+447,शीर्षक_पट्टी[1]+279),(39,49,64)),((가로,उबें_स्थिती),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            वैधताय_अहवाल.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not वैधताय_अहवाल['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(मेजप_डेटा/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for डेटा_स्थिती in reversed(실행과정들):
                if डेटा_स्थिती.poll() is None:
                    if डेटा_स्थिती.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(डेटा_स्थिती.pid,signal.SIGTERM)
                    else:डेटा_स्थिती.terminate()
                    try:डेटा_स्थिती.wait(timeout=5)
                    except subprocess.TimeoutExpired:डेटा_स्थिती.kill();डेटा_स्थिती.wait()
            वेंचक.close()
            for फायल_प्रवेश in 기록들:फायल_प्रवेश.close()
            (मेजप_डेटा/'serial.log').write_bytes(직렬입출력)
            (मेजप_डेटा/'report.json').write_text(json.dumps(वैधताय_अहवाल,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':चलोवप()
