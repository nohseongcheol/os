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
from Изврши_наредба import Project_корен


def Изврши_2():
    мерка_податоци=Project_корен/'build/verification/remmina';мерка_податоци.mkdir(parents=True,exist_ok=True)
    проверка_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];избирач=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            виртуелен_екран=shutil.which('Xvfb')
            if виртуелен_екран: сервер_VALUE=[виртуелен_екран]
            else:
                뿌리파일계층=Project_корен.parent/'rpi4/build/rootfs'
                сервер_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Изврши_2(аргумент_низа,환경=None,**이름붙인인수):
                LOG_ред=(мерка_податоци/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_ред)
                податоци_позиционирање=subprocess.Popen(аргумент_низа,env=환경,stdout=LOG_ред,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(податоци_позиционирање);return податоци_позиционирање
            환경=dict(os.environ)
            for Име in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Име,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(ставка_COUNT for ставка_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(ставка_COUNT)).exists() and not Path('/tmp/.X%d-lock'%ставка_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            екран=Изврши_2(сервер_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert екран.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            гостин=subprocess.Popen(['python3',str(Project_корен/'Алатки/Изврши_наредба.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(гостин);избирач.register(гостин.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert гостин.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in избирач.select(.1):
                        податоци=누름값.fileobj.read(65536)
                        if податоци:직렬입출력.extend(податоци)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            број_на_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Профил=작업경로/'test.remmina'
            Профил.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%број_на_порта)
            Изврши_2(['dbus-run-session','--','remmina','-c',str(Профил)],환경=환경,start_new_session=True)
            def 가상입력도구(*аргумент_низа):return subprocess.check_output(['xdotool']+list(аргумент_низа),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;прозорец=None
            while time.monotonic()<마감시각:
                SEARCH_мерка=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if SEARCH_мерка.returncode==0:
                    후보=SEARCH_мерка.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Фокусирано=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Фокусирано.returncode==0:прозорец=후보;break
                time.sleep(.1)
            assert прозорец,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',прозорец,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Текст):가상입력도구('type','--clearmodifiers','--delay','50',Текст)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Клуч_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',прозорец,str(мерка_податоци/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # реален_податоци Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            цртеж_VALUE=Image.open(str(мерка_податоци/'remmina-korean.png')).convert('RGB')
            насловна_лента=None
            for вертикала_позиционирање in range(цртеж_VALUE.height):
                가로들=[가로 for 가로 in range(цртеж_VALUE.width) if цртеж_VALUE.getpixel((가로,вертикала_позиционирање))==(32,80,144)]
                if len(가로들)>=500:насловна_лента=(min(가로들),вертикала_позиционирање);break
            assert насловна_лента,'native terminal title bar not found'
            가로,вертикала_позиционирање=насловна_лента[0]+564,насловна_лента[1]+356
            가상입력도구('mousemove','--window',прозорец,str(가로),str(вертикала_позиционирање))
            def 화상기다리기(Име,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',прозорец,str(мерка_податоци/Име)])
                    бит_мапа_IMAGE=Image.open(str(мерка_податоци/Име)).convert('RGB')
                    if all(бит_мапа_IMAGE.getpixel(Позиција)==빛 for Позиција,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Име
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,вертикала_позиционирање-7),(255,255,255)),((가로+7,вертикала_позиционирање+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',прозорец,str(가로-120),str(вертикала_позиционирање-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',прозорец,'500','45')
            화상기다리기('remmina-resized.png',[
                ((насловна_лента[0]+447,насловна_лента[1]+279),(39,49,64)),((가로,вертикала_позиционирање),(24,32,48))])
            if shutil.which('dpkg-query'):
                број_на_верзија=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                број_на_верзија=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            проверка_извештај.update(passed=True,display=환경['DISPLAY'],remmina_version=број_на_верзија,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not проверка_извештај['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(мерка_податоци/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for податоци_позиционирање in reversed(실행과정들):
                if податоци_позиционирање.poll() is None:
                    if податоци_позиционирање.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(податоци_позиционирање.pid,signal.SIGTERM)
                    else:податоци_позиционирање.terminate()
                    try:податоци_позиционирање.wait(timeout=5)
                    except subprocess.TimeoutExpired:податоци_позиционирање.kill();податоци_позиционирање.wait()
            избирач.close()
            for датотека_внес in 기록들:датотека_внес.close()
            (мерка_податоци/'serial.log').write_bytes(직렬입출력)
            (мерка_податоци/'report.json').write_text(json.dumps(проверка_извештај,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Изврши_2()
