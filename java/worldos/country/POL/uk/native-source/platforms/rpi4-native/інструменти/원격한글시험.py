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
from Виконати_команда import Дії_корінь


def запустити():
    КР_дані=Дії_корінь/'build/verification/remmina';КР_дані.mkdir(parents=True,exist_ok=True)
    перевірка_звіт={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];селектор=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: сервер_значення=[가상표시장치]
            else:
                뿌리파일계층=Дії_корінь.parent/'rpi4/build/rootfs'
                сервер_значення=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def запустити(аргумент_масив,середовище=None,**іменований_аргумент):
                журнал_запис=(КР_дані/('process-%d.log'%len(기록들))).open('wb');기록들.append(журнал_запис)
                дані_посада=subprocess.Popen(аргумент_масив,env=середовище,stdout=журнал_запис,stderr=subprocess.STDOUT,**іменований_аргумент)
                실행과정들.append(дані_посада);return дані_посада
            середовище=dict(os.environ)
            for Назва in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):середовище.pop(Назва,None)
            середовище.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            середовище['DISPLAY']=':'+str(수치)
            дисплей=запустити(сервер_значення+[середовище['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],середовище=середовище)
            крайнiй_термін_час=time.monotonic()+30
            while True:
                assert дисплей.poll() is None and time.monotonic()<крайнiй_термін_час,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=середовище,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            гість=subprocess.Popen(['python3',str(Дії_корінь/'інструменти/Виконати_команда.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(гість);селектор.register(гість.stdout,selectors.EVENT_READ)
            def 기다리기(маркер,Зміщена_копія_значення=0):
                крайнiй_термін_час=time.monotonic()+45
                while маркер not in 직렬입출력[Зміщена_копія_значення:]:
                    assert гість.poll() is None and time.monotonic()<крайнiй_термін_час,직렬입출력[Зміщена_копія_значення:].decode('utf-8','replace')
                    for 누름값,_ in селектор.select(.1):
                        дані=누름값.fileobj.read(65536)
                        if дані:직렬입출력.extend(дані)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            номер_порту=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Профіль=작업경로/'test.remmina'
            Профіль.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%номер_порту)
            запустити(['dbus-run-session','--','remmina','-c',str(Профіль)],середовище=середовище,start_new_session=True)
            def 가상입력도구(*аргумент_масив):return subprocess.check_output(['xdotool']+list(аргумент_масив),env=середовище,stderr=subprocess.STDOUT)
            крайнiй_термін_час=time.monotonic()+60;Вікно=None
            while time.monotonic()<крайнiй_термін_час:
                Пошук_КР=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=середовище,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Пошук_КР.returncode==0:
                    кандидат=Пошук_КР.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Важливі=subprocess.run(['xdotool','windowfocus','--sync',кандидат],env=середовище,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Важливі.returncode==0:Вікно=кандидат;break
                time.sleep(.1)
            assert Вікно,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Вікно,'280','240','click','1')
            time.sleep(1)
            def 글자입력(текст):가상입력도구('type','--clearmodifiers','--delay','50',текст)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Зміщена_копія_значення=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Зміщена_копія_значення)
            Зміщена_копія_значення=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Зміщена_копія_значення)
            Зміщена_копія_значення=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/нуль_операнд Ключ_значення, Shift+Space 또는 F9'.encode(),Зміщена_копія_значення);기다리기(b'jkoros-native> ',Зміщена_копія_значення)
            Зміщена_копія_значення=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Зміщена_копія_значення)
            subprocess.check_call(['import','-display',середовище['DISPLAY'],'-window',Вікно,str(КР_дані/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Зміщена_копія_значення)
            # фактично_дані Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            малювання_значення=Image.open(str(КР_дані/'remmina-korean.png')).convert('RGB')
            рядок_заголовка=None
            for Вертикаль_посада in range(малювання_значення.height):
                가로들=[가로 for 가로 in range(малювання_значення.width) if малювання_значення.getpixel((가로,Вертикаль_посада))==(32,80,144)]
                if len(가로들)>=500:рядок_заголовка=(min(가로들),Вертикаль_посада);break
            assert рядок_заголовка,'native terminal title bar not found'
            가로,Вертикаль_посада=рядок_заголовка[0]+564,рядок_заголовка[1]+356
            가상입력도구('mousemove','--window',Вікно,str(가로),str(Вертикаль_посада))
            def 화상기다리기(Назва,점들):
                крайнiй_термін_значення=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',середовище['DISPLAY'],'-window',Вікно,str(КР_дані/Назва)])
                    бітова_карта_фото=Image.open(str(КР_дані/Назва)).convert('RGB')
                    if all(бітова_карта_фото.getpixel(позиція)==빛 for позиція,빛 in 점들):return
                    assert time.monotonic()<крайнiй_термін_значення,'Remmina framebuffer did not settle: '+Назва
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Вертикаль_посада-7),(255,255,255)),((가로+7,Вертикаль_посада+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Вікно,str(가로-120),str(Вертикаль_посада-80),'mouseup','1')
            time.sleep(.4)
            Зміщена_копія_значення=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Зміщена_копія_значення)
            가상입력도구('mousemove','--window',Вікно,'500','45')
            화상기다리기('remmina-resized.png',[
                ((рядок_заголовка[0]+447,рядок_заголовка[1]+279),(39,49,64)),((가로,Вертикаль_посада),(24,32,48))])
            if shutil.which('dpkg-query'):
                номер_версії=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                номер_версії=subprocess.check_output(['remmina','--version'],env=середовище,stderr=subprocess.STDOUT).decode('utf-8','replace')
            перевірка_звіт.update(passed=True,display=середовище['DISPLAY'],remmina_version=номер_версії,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not перевірка_звіт['passed'] and 'середовище' in locals() and середовище.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',середовище['DISPLAY'],'-window','root',str(КР_дані/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for дані_посада in reversed(실행과정들):
                if дані_посада.poll() is None:
                    if дані_посада.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(дані_посада.pid,signal.SIGTERM)
                    else:дані_посада.terminate()
                    try:дані_посада.wait(timeout=5)
                    except subprocess.TimeoutExpired:дані_посада.kill();дані_посада.wait()
            селектор.close()
            for Файл_запис in 기록들:Файл_запис.close()
            (КР_дані/'serial.log').write_bytes(직렬입출력)
            (КР_дані/'report.json').write_text(json.dumps(перевірка_звіт,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':запустити()
