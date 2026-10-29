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
from орындау_пәрмен import жоба_түбір


def Орындау_2():
    өлшем_деректер=жоба_түбір/'build/verification/remmina';өлшем_деректер.mkdir(parents=True,exist_ok=True)
    тексерім_есеп={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];селектор=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            виртуалды_дисплей=shutil.which('Xvfb')
            if виртуалды_дисплей: сервер_мән=[виртуалды_дисплей]
            else:
                뿌리파일계층=жоба_түбір.parent/'rpi4/build/rootfs'
                сервер_мән=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Орындау_2(аргумент_массив,환경=None,**деректі_аргумент):
                журнал_жол=(өлшем_деректер/('process-%d.log'%len(기록들))).open('wb');기록들.append(журнал_жол)
                деректер_лауазым=subprocess.Popen(аргумент_массив,env=환경,stdout=журнал_жол,stderr=subprocess.STDOUT,**деректі_аргумент)
                실행과정들.append(деректер_лауазым);return деректер_лауазым
            환경=dict(os.environ)
            for Аты in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Аты,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            дисплей=Орындау_2(сервер_мән+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            ең_соңғы_мерзім_уақыт=time.monotonic()+30
            while True:
                assert дисплей.poll() is None and time.monotonic()<ең_соңғы_мерзім_уақыт,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            қонақ=subprocess.Popen(['python3',str(жоба_түбір/'Құралдар/орындау_пәрмен.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(қонақ);селектор.register(қонақ.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,жылжыту_мән_450fc799=0):
                ең_соңғы_мерзім_уақыт=time.monotonic()+45
                while 확인표시 not in 직렬입출력[жылжыту_мән_450fc799:]:
                    assert қонақ.poll() is None and time.monotonic()<ең_соңғы_мерзім_уақыт,직렬입출력[жылжыту_мән_450fc799:].decode('utf-8','replace')
                    for 누름값,_ in селектор.select(.1):
                        деректер=누름값.fileobj.read(65536)
                        if деректер:직렬입출력.extend(деректер)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            порт_нөмірі=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Профиль=작업경로/'test.remmina'
            Профиль.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%порт_нөмірі)
            Орындау_2(['dbus-run-session','--','remmina','-c',str(Профиль)],환경=환경,start_new_session=True)
            def 가상입력도구(*аргумент_массив):return subprocess.check_output(['xdotool']+list(аргумент_массив),env=환경,stderr=subprocess.STDOUT)
            ең_соңғы_мерзім_уақыт=time.monotonic()+60;Терезе=None
            while time.monotonic()<ең_соңғы_мерзім_уақыт:
                Іздеу_өлшем=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Іздеу_өлшем.returncode==0:
                    후보=Іздеу_өлшем.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Cұрыпталған=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Cұрыпталған.returncode==0:Терезе=후보;break
                time.sleep(.1)
            assert Терезе,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Терезе,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Мәтін):가상입력도구('type','--clearmodifiers','--delay','50',Мәтін)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            жылжыту_мән_450fc799=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Кілт_мән, Shift+Space 또는 F9'.encode(),жылжыту_мән_450fc799);기다리기(b'jkoros-native> ',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),жылжыту_мән_450fc799)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Терезе,str(өлшем_деректер/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',жылжыту_мән_450fc799)
            # нақты_деректер Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            сызба_мән=Image.open(str(өлшем_деректер/'remmina-korean.png')).convert('RGB')
            терезе_тақырыбы=None
            for Тік_лауазым in range(сызба_мән.height):
                가로들=[가로 for 가로 in range(сызба_мән.width) if сызба_мән.getpixel((가로,Тік_лауазым))==(32,80,144)]
                if len(가로들)>=500:терезе_тақырыбы=(min(가로들),Тік_лауазым);break
            assert терезе_тақырыбы,'native terminal title bar not found'
            가로,Тік_лауазым=терезе_тақырыбы[0]+564,терезе_тақырыбы[1]+356
            가상입력도구('mousemove','--window',Терезе,str(가로),str(Тік_лауазым))
            def 화상기다리기(Аты,점들):
                ең_соңғы_мерзім_мән=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Терезе,str(өлшем_деректер/Аты)])
                    нүктелік_кескін_сурет=Image.open(str(өлшем_деректер/Аты)).convert('RGB')
                    if all(нүктелік_кескін_сурет.getpixel(Орны)==빛 for Орны,빛 in 점들):return
                    assert time.monotonic()<ең_соңғы_мерзім_мән,'Remmina framebuffer did not settle: '+Аты
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Тік_лауазым-7),(255,255,255)),((가로+7,Тік_лауазым+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Терезе,str(가로-120),str(Тік_лауазым-80),'mouseup','1')
            time.sleep(.4)
            жылжыту_мән_450fc799=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',жылжыту_мән_450fc799)
            가상입력도구('mousemove','--window',Терезе,'500','45')
            화상기다리기('remmina-resized.png',[
                ((терезе_тақырыбы[0]+447,терезе_тақырыбы[1]+279),(39,49,64)),((가로,Тік_лауазым),(24,32,48))])
            if shutil.which('dpkg-query'):
                Нұсқа_нөмірі=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                Нұсқа_нөмірі=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            тексерім_есеп.update(passed=True,display=환경['DISPLAY'],remmina_version=Нұсқа_нөмірі,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not тексерім_есеп['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(өлшем_деректер/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for деректер_лауазым in reversed(실행과정들):
                if деректер_лауазым.poll() is None:
                    if деректер_лауазым.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(деректер_лауазым.pid,signal.SIGTERM)
                    else:деректер_лауазым.terminate()
                    try:деректер_лауазым.wait(timeout=5)
                    except subprocess.TimeoutExpired:деректер_лауазым.kill();деректер_лауазым.wait()
            селектор.close()
            for файл_енгізу in 기록들:файл_енгізу.close()
            (өлшем_деректер/'serial.log').write_bytes(직렬입출력)
            (өлшем_деректер/'report.json').write_text(json.dumps(тексерім_есеп,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Орындау_2()
