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
from 실행 import задача_корень


def запустить():
    KR_данные=задача_корень/'build/verification/remmina';KR_данные.mkdir(parents=True,exist_ok=True)
    проверка_Отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];селектор=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            виртуальный_дисплей=shutil.which('Xvfb')
            if виртуальный_дисплей: сервер_ЗНАЧЕН=[виртуальный_дисплей]
            else:
                뿌리파일계층=задача_корень.parent/'rpi4/build/rootfs'
                сервер_ЗНАЧЕН=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def запустить(аргумент_МАССИВ,среда=None,**именованные_аргументы):
                LOG_ЗАПИСЬ=(KR_данные/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_ЗАПИСЬ)
                данные_позиция=subprocess.Popen(аргумент_МАССИВ,env=среда,stdout=LOG_ЗАПИСЬ,stderr=subprocess.STDOUT,**именованные_аргументы)
                실행과정들.append(данные_позиция);return данные_позиция
            среда=dict(os.environ)
            for Название in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):среда.pop(Название,None)
            среда.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(товар_СЧЁТ for товар_СЧЁТ in range(80,200) if not Path('/tmp/.X11-unix/X'+str(товар_СЧЁТ)).exists() and not Path('/tmp/.X%d-lock'%товар_СЧЁТ).exists())
            среда['DISPLAY']=':'+str(수치)
            дисплей=запустить(сервер_ЗНАЧЕН+[среда['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],среда=среда)
            крайний_срок_ВРЕМЯ=time.monotonic()+30
            while True:
                assert дисплей.poll() is None and time.monotonic()<крайний_срок_ВРЕМЯ,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=среда,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            гость=subprocess.Popen(['python3',str(задача_корень/'инструменты/실행.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(гость);селектор.register(гость.stdout,selectors.EVENT_READ)
            def 기다리기(метка,СМЕЩ_ЗНАЧЕН=0):
                крайний_срок_ВРЕМЯ=time.monotonic()+45
                while метка not in 직렬입출력[СМЕЩ_ЗНАЧЕН:]:
                    assert гость.poll() is None and time.monotonic()<крайний_срок_ВРЕМЯ,직렬입출력[СМЕЩ_ЗНАЧЕН:].decode('utf-8','replace')
                    for 누름값,_ in селектор.select(.1):
                        данные=누름값.fileobj.read(65536)
                        if данные:직렬입출력.extend(данные)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            номер_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profile=작업경로/'test.remmina'
            Profile.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%номер_порта)
            запустить(['dbus-run-session','--','remmina','-c',str(Profile)],среда=среда,start_new_session=True)
            def виртуальный_входные_данные_средство(*аргумент_МАССИВ):return subprocess.check_output(['xdotool']+list(аргумент_МАССИВ),env=среда,stderr=subprocess.STDOUT)
            крайний_срок_ВРЕМЯ=time.monotonic()+60;Окно=None
            while time.monotonic()<крайний_срок_ВРЕМЯ:
                ПОИСК_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=среда,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ПОИСК_KR.returncode==0:
                    соискатель=ПОИСК_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Важное=subprocess.run(['xdotool','windowfocus','--sync',соискатель],env=среда,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Важное.returncode==0:Окно=соискатель;break
                time.sleep(.1)
            assert Окно,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            виртуальный_входные_данные_средство('mousemove','--window',Окно,'280','240','click','1')
            time.sleep(1)
            def 글자입력(текст):виртуальный_входные_данные_средство('type','--clearmodifiers','--delay','50',текст)
            def 누름값(*누름열):виртуальный_входные_данные_средство('key','--clearmodifiers',*누름열)
            СМЕЩ_ЗНАЧЕН=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/нуль_операнд Ключ_ЗНАЧЕН, Shift+Space 또는 F9'.encode(),СМЕЩ_ЗНАЧЕН);기다리기(b'jkoros-native> ',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),СМЕЩ_ЗНАЧЕН)
            subprocess.check_call(['import','-display',среда['DISPLAY'],'-window',Окно,str(KR_данные/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',СМЕЩ_ЗНАЧЕН)
            # фактический_данные Remmina의 экран 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            рисунок_ЗНАЧЕН=Image.open(str(KR_данные/'remmina-korean.png')).convert('RGB')
            заголовок=None
            for Вертикаль_позиция in range(рисунок_ЗНАЧЕН.height):
                가로들=[가로 for 가로 in range(рисунок_ЗНАЧЕН.width) if рисунок_ЗНАЧЕН.getpixel((가로,Вертикаль_позиция))==(32,80,144)]
                if len(가로들)>=500:заголовок=(min(가로들),Вертикаль_позиция);break
            assert заголовок,'native terminal title bar not found'
            가로,Вертикаль_позиция=заголовок[0]+564,заголовок[1]+356
            виртуальный_входные_данные_средство('mousemove','--window',Окно,str(가로),str(Вертикаль_позиция))
            def 화상기다리기(Название,점들):
                крайний_срок_ЗНАЧЕН=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',среда['DISPLAY'],'-window',Окно,str(KR_данные/Название)])
                    точечный_рисунок_фото=Image.open(str(KR_данные/Название)).convert('RGB')
                    if all(точечный_рисунок_фото.getpixel(позиция)==빛 for позиция,빛 in 점들):return
                    assert time.monotonic()<крайний_срок_ЗНАЧЕН,'Remmina framebuffer did not settle: '+Название
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Вертикаль_позиция-7),(255,255,255)),((가로+7,Вертикаль_позиция+7),(255,255,255))])
            виртуальный_входные_данные_средство('mousedown','1','mousemove','--window',Окно,str(가로-120),str(Вертикаль_позиция-80),'mouseup','1')
            time.sleep(.4)
            СМЕЩ_ЗНАЧЕН=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',СМЕЩ_ЗНАЧЕН)
            виртуальный_входные_данные_средство('mousemove','--window',Окно,'500','45')
            화상기다리기('remmina-resized.png',[
                ((заголовок[0]+447,заголовок[1]+279),(39,49,64)),((가로,Вертикаль_позиция),(24,32,48))])
            if shutil.which('dpkg-query'):
                номер_версии=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                номер_версии=subprocess.check_output(['remmina','--version'],env=среда,stderr=subprocess.STDOUT).decode('utf-8','replace')
            проверка_Отчет.update(passed=True,display=среда['DISPLAY'],remmina_version=номер_версии,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not проверка_Отчет['passed'] and 'среда' in locals() and среда.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',среда['DISPLAY'],'-window','root',str(KR_данные/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for данные_позиция in reversed(실행과정들):
                if данные_позиция.poll() is None:
                    if данные_позиция.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(данные_позиция.pid,signal.SIGTERM)
                    else:данные_позиция.terminate()
                    try:данные_позиция.wait(timeout=5)
                    except subprocess.TimeoutExpired:данные_позиция.kill();данные_позиция.wait()
            селектор.close()
            for файл_ввод in 기록들:файл_ввод.close()
            (KR_данные/'serial.log').write_bytes(직렬입출력)
            (KR_данные/'report.json').write_text(json.dumps(проверка_Отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':запустить()
