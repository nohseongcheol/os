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
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ


def ચલાવો_2():
    પરિમાણ_ડેટા=પ્રોજેક્ટ_રૂટ/'build/verification/remmina';પરિમાણ_ડેટા.mkdir(parents=True,exist_ok=True)
    માન્યતા_અહેવાલ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];પસંદકર્તા=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            વર્ચુઅલ_પ્રદર્શન=shutil.which('Xvfb')
            if વર્ચુઅલ_પ્રદર્શન: સર્વર_મૂલ્ય=[વર્ચુઅલ_પ્રદર્શન]
            else:
                뿌리파일계층=પ્રોજેક્ટ_રૂટ.parent/'rpi4/build/rootfs'
                સર્વર_મૂલ્ય=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def ચલાવો_2(દલીલ_અરે,환경=None,**이름붙인인수):
                લૉગ_પંક્તિ=(પરિમાણ_ડેટા/('process-%d.log'%len(기록들))).open('wb');기록들.append(લૉગ_પંક્તિ)
                ડેટા_સ્થિતિ=subprocess.Popen(દલીલ_અરે,env=환경,stdout=લૉગ_પંક્તિ,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ડેટા_સ્થિતિ);return ડેટા_સ્થિતિ
            환경=dict(os.environ)
            for નામ in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(નામ,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            પ્રદર્શન=ચલાવો_2(સર્વર_મૂલ્ય+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert પ્રદર્શન.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            અતિથિ=subprocess.Popen(['python3',str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_આદેશ.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(અતિથિ);પસંદકર્તા.register(અતિથિ.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ઑફસેટ_મૂલ્ય=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ઑફસેટ_મૂલ્ય:]:
                    assert અતિથિ.poll() is None and time.monotonic()<마감시각,직렬입출력[ઑફસેટ_મૂલ્ય:].decode('utf-8','replace')
                    for 누름값,_ in પસંદકર્તા.select(.1):
                        ડેટા=누름값.fileobj.read(65536)
                        if ડેટા:직렬입출력.extend(ડેટા)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            પોર્ટ_નંબર=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            પ્રોફાઇલ=작업경로/'test.remmina'
            પ્રોફાઇલ.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%પોર્ટ_નંબર)
            ચલાવો_2(['dbus-run-session','--','remmina','-c',str(પ્રોફાઇલ)],환경=환경,start_new_session=True)
            def 가상입력도구(*દલીલ_અરે):return subprocess.check_output(['xdotool']+list(દલીલ_અરે),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;વિંડો=None
            while time.monotonic()<마감시각:
                શોધ_પરિમાણ=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if શોધ_પરિમાણ.returncode==0:
                    후보=શોધ_પરિમાણ.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ફોકસ_કરાયેલ=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ફોકસ_કરાયેલ.returncode==0:વિંડો=후보;break
                time.sleep(.1)
            assert વિંડો,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',વિંડો,'280','240','click','1')
            time.sleep(1)
            def 글자입력(લખાણ):가상입력도구('type','--clearmodifiers','--delay','50',લખાણ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ઑફસેટ_મૂલ્ય=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 કી_મૂલ્ય, Shift+Space 또는 F9'.encode(),ઑફસેટ_મૂલ્ય);기다리기(b'jkoros-native> ',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ઑફસેટ_મૂલ્ય)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',વિંડો,str(પરિમાણ_ડેટા/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ઑફસેટ_મૂલ્ય)
            # વાસ્તવિક_ડેટા Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            રેખાંકન_મૂલ્ય=Image.open(str(પરિમાણ_ડેટા/'remmina-korean.png')).convert('RGB')
            શીર્ષક_પટ્ટી=None
            for ઊભી_સ્થિતિ in range(રેખાંકન_મૂલ્ય.height):
                가로들=[가로 for 가로 in range(રેખાંકન_મૂલ્ય.width) if રેખાંકન_મૂલ્ય.getpixel((가로,ઊભી_સ્થિતિ))==(32,80,144)]
                if len(가로들)>=500:શીર્ષક_પટ્ટી=(min(가로들),ઊભી_સ્થિતિ);break
            assert શીર્ષક_પટ્ટી,'native terminal title bar not found'
            가로,ઊભી_સ્થિતિ=શીર્ષક_પટ્ટી[0]+564,શીર્ષક_પટ્ટી[1]+356
            가상입력도구('mousemove','--window',વિંડો,str(가로),str(ઊભી_સ્થિતિ))
            def 화상기다리기(નામ,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',વિંડો,str(પરિમાણ_ડેટા/નામ)])
                    બિટમૅપ_છબી=Image.open(str(પરિમાણ_ડેટા/નામ)).convert('RGB')
                    if all(બિટમૅપ_છબી.getpixel(સ્થાન)==빛 for સ્થાન,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+નામ
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,ઊભી_સ્થિતિ-7),(255,255,255)),((가로+7,ઊભી_સ્થિતિ+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',વિંડો,str(가로-120),str(ઊભી_સ્થિતિ-80),'mouseup','1')
            time.sleep(.4)
            ઑફસેટ_મૂલ્ય=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ઑફસેટ_મૂલ્ય)
            가상입력도구('mousemove','--window',વિંડો,'500','45')
            화상기다리기('remmina-resized.png',[
                ((શીર્ષક_પટ્ટી[0]+447,શીર્ષક_પટ્ટી[1]+279),(39,49,64)),((가로,ઊભી_સ્થિતિ),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            માન્યતા_અહેવાલ.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not માન્યતા_અહેવાલ['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(પરિમાણ_ડેટા/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ડેટા_સ્થિતિ in reversed(실행과정들):
                if ડેટા_સ્થિતિ.poll() is None:
                    if ડેટા_સ્થિતિ.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ડેટા_સ્થિતિ.pid,signal.SIGTERM)
                    else:ડેટા_સ્થિતિ.terminate()
                    try:ડેટા_સ્થિતિ.wait(timeout=5)
                    except subprocess.TimeoutExpired:ડેટા_સ્થિતિ.kill();ડેટા_સ્થિતિ.wait()
            પસંદકર્તા.close()
            for ફાઇલ_પ્રવેશ in 기록들:ફાઇલ_પ્રવેશ.close()
            (પરિમાણ_ડેટા/'serial.log').write_bytes(직렬입출력)
            (પરિમાણ_ડેટા/'report.json').write_text(json.dumps(માન્યતા_અહેવાલ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ચલાવો_2()
