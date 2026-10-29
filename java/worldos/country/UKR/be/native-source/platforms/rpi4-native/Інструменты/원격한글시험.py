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
from выканаць_каманда import 기준


def Выканаць():
    결과자료=기준/'build/verification/remmina';결과자료.mkdir(parents=True,exist_ok=True)
    праверка_справаздача={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];селектар=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            віртуальны_дысплэй=shutil.which('Xvfb')
            if віртуальны_дысплэй: сервер_значэнне=[віртуальны_дысплэй]
            else:
                뿌리파일계층=기준.parent/'rpi4/build/rootfs'
                сервер_значэнне=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Выканаць(аргумент_масіў,환경=None,**이름붙인인수):
                журнал_запіс=(결과자료/('process-%d.log'%len(기록들))).open('wb');기록들.append(журнал_запіс)
                자료위치=subprocess.Popen(аргумент_масіў,env=환경,stdout=журнал_запіс,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(자료위치);return 자료위치
            환경=dict(os.environ)
            for Назва in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Назва,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            дысплэй=Выканаць(сервер_значэнне+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert дысплэй.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            госць=subprocess.Popen(['python3',str(기준/'Інструменты/выканаць_каманда.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(госць);селектар.register(госць.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,Зрух_значэнне=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[Зрух_значэнне:]:
                    assert госць.poll() is None and time.monotonic()<마감시각,직렬입출력[Зрух_значэнне:].decode('utf-8','replace')
                    for 누름값,_ in селектар.select(.1):
                        дадзеныя=누름값.fileobj.read(65536)
                        if дадзеныя:직렬입출력.extend(дадзеныя)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            нумар_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Профіль=작업경로/'test.remmina'
            Профіль.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%нумар_порта)
            Выканаць(['dbus-run-session','--','remmina','-c',str(Профіль)],환경=환경,start_new_session=True)
            def 가상입력도구(*аргумент_масіў):return subprocess.check_output(['xdotool']+list(аргумент_масіў),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;акно=None
            while time.monotonic()<마감시각:
                찾은결과=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if 찾은결과.returncode==0:
                    후보=찾은결과.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Важнае=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Важнае.returncode==0:акно=후보;break
                time.sleep(.1)
            assert акно,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',акно,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Тэкст):가상입력도구('type','--clearmodifiers','--delay','50',Тэкст)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Зрух_значэнне=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Зрух_значэнне)
            Зрух_значэнне=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Зрух_значэнне)
            Зрух_значэнне=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 клавіша_значэнне, Shift+Space 또는 F9'.encode(),Зрух_значэнне);기다리기(b'jkoros-native> ',Зрух_значэнне)
            Зрух_значэнне=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Зрух_значэнне)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',акно,str(결과자료/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Зрух_значэнне)
            # фактычны_дадзеныя Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            рукапісная_графіка_значэнне=Image.open(str(결과자료/'remmina-korean.png')).convert('RGB')
            загаловак_акна=None
            for 세로 in range(рукапісная_графіка_значэнне.height):
                가로들=[가로 for 가로 in range(рукапісная_графіка_значэнне.width) if рукапісная_графіка_значэнне.getpixel((가로,세로))==(32,80,144)]
                if len(가로들)>=500:загаловак_акна=(min(가로들),세로);break
            assert загаловак_акна,'native terminal title bar not found'
            가로,세로=загаловак_акна[0]+564,загаловак_акна[1]+356
            가상입력도구('mousemove','--window',акно,str(가로),str(세로))
            def 화상기다리기(Назва,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',акно,str(결과자료/Назва)])
                    растравая_выява_выява=Image.open(str(결과자료/Назва)).convert('RGB')
                    if all(растравая_выява_выява.getpixel(Пазіцыя)==빛 for Пазіцыя,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Назва
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,세로-7),(255,255,255)),((가로+7,세로+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',акно,str(가로-120),str(세로-80),'mouseup','1')
            time.sleep(.4)
            Зрух_значэнне=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Зрух_значэнне)
            가상입력도구('mousemove','--window',акно,'500','45')
            화상기다리기('remmina-resized.png',[
                ((загаловак_акна[0]+447,загаловак_акна[1]+279),(39,49,64)),((가로,세로),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            праверка_справаздача.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not праверка_справаздача['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(결과자료/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for 자료위치 in reversed(실행과정들):
                if 자료위치.poll() is None:
                    if 자료위치.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(자료위치.pid,signal.SIGTERM)
                    else:자료위치.terminate()
                    try:자료위치.wait(timeout=5)
                    except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            селектар.close()
            for файл_увядзенне in 기록들:файл_увядзенне.close()
            (결과자료/'serial.log').write_bytes(직렬입출력)
            (결과자료/'report.json').write_text(json.dumps(праверка_справаздача,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Выканаць()
