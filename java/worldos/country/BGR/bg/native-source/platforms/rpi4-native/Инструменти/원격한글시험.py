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
from изпълнявам_команда import проект_корен


def Стартиране():
    мярка_данни=проект_корен/'build/verification/remmina';мярка_данни.mkdir(parents=True,exist_ok=True)
    проверка_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];свързан_елемент_за_избор=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: сървър_стойност=[가상표시장치]
            else:
                뿌리파일계층=проект_корен.parent/'rpi4/build/rootfs'
                сървър_стойност=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Стартиране(аргумент_масив,환경=None,**аргумент_с_предварително_зададено_име):
                регистрирам_запис=(мярка_данни/('process-%d.log'%len(기록들))).open('wb');기록들.append(регистрирам_запис)
                данни_позиция=subprocess.Popen(аргумент_масив,env=환경,stdout=регистрирам_запис,stderr=subprocess.STDOUT,**аргумент_с_предварително_зададено_име)
                실행과정들.append(данни_позиция);return данни_позиция
            환경=dict(os.environ)
            for Име in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Име,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            дисплей=Стартиране(сървър_стойност+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            краен_срок_час=time.monotonic()+30
            while True:
                assert дисплей.poll() is None and time.monotonic()<краен_срок_час,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            гост=subprocess.Popen(['python3',str(проект_корен/'Инструменти/изпълнявам_команда.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(гост);свързан_елемент_за_избор.register(гост.stdout,selectors.EVENT_READ)
            def 기다리기(маркер,Изместване_стойност=0):
                краен_срок_час=time.monotonic()+45
                while маркер not in 직렬입출력[Изместване_стойност:]:
                    assert гост.poll() is None and time.monotonic()<краен_срок_час,직렬입출력[Изместване_стойност:].decode('utf-8','replace')
                    for 누름값,_ in свързан_елемент_за_избор.select(.1):
                        данни=누름값.fileobj.read(65536)
                        if данни:직렬입출력.extend(данни)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            номер_на_порт=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Профил=작업경로/'test.remmina'
            Профил.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%номер_на_порт)
            Стартиране(['dbus-run-session','--','remmina','-c',str(Профил)],환경=환경,start_new_session=True)
            def 가상입력도구(*аргумент_масив):return subprocess.check_output(['xdotool']+list(аргумент_масив),env=환경,stderr=subprocess.STDOUT)
            краен_срок_час=time.monotonic()+60;Прозорец=None
            while time.monotonic()<краен_срок_час:
                търся_мярка=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if търся_мярка.returncode==0:
                    후보=търся_мярка.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Фокусирани=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Фокусирани.returncode==0:Прозорец=후보;break
                time.sleep(.1)
            assert Прозорец,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Прозорец,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Текст):가상입력도구('type','--clearmodifiers','--delay','50',Текст)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Изместване_стойност=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Изместване_стойност)
            Изместване_стойност=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Изместване_стойност)
            Изместване_стойност=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/нула_операнд Ключ_стойност, Shift+Space 또는 F9'.encode(),Изместване_стойност);기다리기(b'jkoros-native> ',Изместване_стойност)
            Изместване_стойност=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Изместване_стойност)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Прозорец,str(мярка_данни/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Изместване_стойност)
            # действителен_данни Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            чертеж_стойност=Image.open(str(мярка_данни/'remmina-korean.png')).convert('RGB')
            заглавна_лента=None
            for вертикал_позиция in range(чертеж_стойност.height):
                가로들=[가로 for 가로 in range(чертеж_стойност.width) if чертеж_стойност.getpixel((가로,вертикал_позиция))==(32,80,144)]
                if len(가로들)>=500:заглавна_лента=(min(가로들),вертикал_позиция);break
            assert заглавна_лента,'native terminal title bar not found'
            가로,вертикал_позиция=заглавна_лента[0]+564,заглавна_лента[1]+356
            가상입력도구('mousemove','--window',Прозорец,str(가로),str(вертикал_позиция))
            def 화상기다리기(Име,점들):
                краен_срок_стойност=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Прозорец,str(мярка_данни/Име)])
                    побитово_представяне_снимка=Image.open(str(мярка_данни/Име)).convert('RGB')
                    if all(побитово_представяне_снимка.getpixel(Позиция)==빛 for Позиция,빛 in 점들):return
                    assert time.monotonic()<краен_срок_стойност,'Remmina framebuffer did not settle: '+Име
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,вертикал_позиция-7),(255,255,255)),((가로+7,вертикал_позиция+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Прозорец,str(가로-120),str(вертикал_позиция-80),'mouseup','1')
            time.sleep(.4)
            Изместване_стойност=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Изместване_стойност)
            가상입력도구('mousemove','--window',Прозорец,'500','45')
            화상기다리기('remmina-resized.png',[
                ((заглавна_лента[0]+447,заглавна_лента[1]+279),(39,49,64)),((가로,вертикал_позиция),(24,32,48))])
            if shutil.which('dpkg-query'):
                номер_на_версия=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                номер_на_версия=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            проверка_отчет.update(passed=True,display=환경['DISPLAY'],remmina_version=номер_на_версия,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not проверка_отчет['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(мярка_данни/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for данни_позиция in reversed(실행과정들):
                if данни_позиция.poll() is None:
                    if данни_позиция.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(данни_позиция.pid,signal.SIGTERM)
                    else:данни_позиция.terminate()
                    try:данни_позиция.wait(timeout=5)
                    except subprocess.TimeoutExpired:данни_позиция.kill();данни_позиция.wait()
            свързан_елемент_за_избор.close()
            for Файл_запис in 기록들:Файл_запис.close()
            (мярка_данни/'serial.log').write_bytes(직렬입출력)
            (мярка_данни/'report.json').write_text(json.dumps(проверка_отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Стартиране()
