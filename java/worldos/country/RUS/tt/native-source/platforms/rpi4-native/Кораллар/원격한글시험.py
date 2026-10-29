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
from үтәргә_команда import экранга_җибәрү_тамыр


def эшләтү():
    үлчәм_мәгълүмат=экранга_җибәрү_тамыр/'build/verification/remmina';үлчәм_мәгълүмат.mkdir(parents=True,exist_ok=True)
    раслау_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];сайлагыч=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            виртуаль_дисплей=shutil.which('Xvfb')
            if виртуаль_дисплей: сервер_VALUE=[виртуаль_дисплей]
            else:
                뿌리파일계층=экранга_җибәрү_тамыр.parent/'rpi4/build/rootfs'
                сервер_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def эшләтү(аргумент_МАССИВ,환경=None,**이름붙인인수):
                LOG_юл=(үлчәм_мәгълүмат/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_юл)
                мәгълүмат_урнаштыру=subprocess.Popen(аргумент_МАССИВ,env=환경,stdout=LOG_юл,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(мәгълүмат_урнаштыру);return мәгълүмат_урнаштыру
            환경=dict(os.environ)
            for исем in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(исем,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(элемент_COUNT for элемент_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(элемент_COUNT)).exists() and not Path('/tmp/.X%d-lock'%элемент_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            дисплей=эшләтү(сервер_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert дисплей.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            кунак=subprocess.Popen(['python3',str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_команда.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(кунак);сайлагыч.register(кунак.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert кунак.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in сайлагыч.select(.1):
                        мәгълүмат=누름값.fileobj.read(65536)
                        if мәгълүмат:직렬입출력.extend(мәгълүмат)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Профиль=작업경로/'test.remmina'
            Профиль.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            эшләтү(['dbus-run-session','--','remmina','-c',str(Профиль)],환경=환경,start_new_session=True)
            def 가상입력도구(*аргумент_МАССИВ):return subprocess.check_output(['xdotool']+list(аргумент_МАССИВ),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;тәрәз=None
            while time.monotonic()<마감시각:
                Эзләү_үлчәм=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Эзләү_үлчәм.returncode==0:
                    후보=Эзләү_үлчәм.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Тупланылган=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Тупланылган.returncode==0:тәрәз=후보;break
                time.sleep(.1)
            assert тәрәз,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',тәрәз,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Mäten):가상입력도구('type','--clearmodifiers','--delay','50',Mäten)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ачкыч_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',тәрәз,str(үлчәм_мәгълүмат/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # фактик_мәгълүмат Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            сызым_VALUE=Image.open(str(үлчәм_мәгълүмат/'remmina-korean.png')).convert('RGB')
            тәрәз_башламы=None
            for Вертикаль_урнаштыру in range(сызым_VALUE.height):
                가로들=[가로 for 가로 in range(сызым_VALUE.width) if сызым_VALUE.getpixel((가로,Вертикаль_урнаштыру))==(32,80,144)]
                if len(가로들)>=500:тәрәз_башламы=(min(가로들),Вертикаль_урнаштыру);break
            assert тәрәз_башламы,'native terminal title bar not found'
            가로,Вертикаль_урнаштыру=тәрәз_башламы[0]+564,тәрәз_башламы[1]+356
            가상입력도구('mousemove','--window',тәрәз,str(가로),str(Вертикаль_урнаштыру))
            def 화상기다리기(исем,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',тәрәз,str(үлчәм_мәгълүмат/исем)])
                    нокталы_рәсем_IMAGE=Image.open(str(үлчәм_мәгълүмат/исем)).convert('RGB')
                    if all(нокталы_рәсем_IMAGE.getpixel(урнаштыру)==빛 for урнаштыру,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+исем
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Вертикаль_урнаштыру-7),(255,255,255)),((가로+7,Вертикаль_урнаштыру+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',тәрәз,str(가로-120),str(Вертикаль_урнаштыру-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',тәрәз,'500','45')
            화상기다리기('remmina-resized.png',[
                ((тәрәз_башламы[0]+447,тәрәз_башламы[1]+279),(39,49,64)),((가로,Вертикаль_урнаштыру),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            раслау_отчет.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not раслау_отчет['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(үлчәм_мәгълүмат/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for мәгълүмат_урнаштыру in reversed(실행과정들):
                if мәгълүмат_урнаштыру.poll() is None:
                    if мәгълүмат_урнаштыру.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(мәгълүмат_урнаштыру.pid,signal.SIGTERM)
                    else:мәгълүмат_урнаштыру.terminate()
                    try:мәгълүмат_урнаштыру.wait(timeout=5)
                    except subprocess.TimeoutExpired:мәгълүмат_урнаштыру.kill();мәгълүмат_урнаштыру.wait()
            сайлагыч.close()
            for файл_кертү in 기록들:файл_кертү.close()
            (үлчәм_мәгълүмат/'serial.log').write_bytes(직렬입출력)
            (үлчәм_мәгълүмат/'report.json').write_text(json.dumps(раслау_отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':эшләтү()
