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
from uitvoer_bevel import Project_wortel


def Loop():
    maatreël_data=Project_wortel/'build/verification/remmina';maatreël_data.mkdir(parents=True,exist_ok=True)
    validering_verslag={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];selekteerder=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtueel_wys=shutil.which('Xvfb')
            if virtueel_wys: bediener_VALUE=[virtueel_wys]
            else:
                뿌리파일계층=Project_wortel.parent/'rpi4/build/rootfs'
                bediener_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Loop(argument_ARRAY,환경=None,**이름붙인인수):
                LOG_ry=(maatreël_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_ry)
                data_plaas=subprocess.Popen(argument_ARRAY,env=환경,stdout=LOG_ry,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(data_plaas);return data_plaas
            환경=dict(os.environ)
            for Naam in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Naam,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(item_COUNT for item_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(item_COUNT)).exists() and not Path('/tmp/.X%d-lock'%item_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            skerm=Loop(bediener_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert skerm.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gas=subprocess.Popen(['python3',str(Project_wortel/'Nutsmiddels/uitvoer_bevel.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gas);selekteerder.register(gas.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert gas.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in selekteerder.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profiel=작업경로/'test.remmina'
            Profiel.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            Loop(['dbus-run-session','--','remmina','-c',str(Profiel)],환경=환경,start_new_session=True)
            def 가상입력도구(*argument_ARRAY):return subprocess.check_output(['xdotool']+list(argument_ARRAY),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;venster=None
            while time.monotonic()<마감시각:
                Soek_maatreël=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Soek_maatreël.returncode==0:
                    후보=Soek_maatreël.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Gefokus=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Gefokus.returncode==0:venster=후보;break
                time.sleep(.1)
            assert venster,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',venster,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Teks):가상입력도구('type','--clearmodifiers','--delay','50',Teks)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Sleutel_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',venster,str(maatreël_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # werklik_data Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            tekening_VALUE=Image.open(str(maatreël_data/'remmina-korean.png')).convert('RGB')
            titelbalk=None
            for Vertikaal_plaas in range(tekening_VALUE.height):
                가로들=[가로 for 가로 in range(tekening_VALUE.width) if tekening_VALUE.getpixel((가로,Vertikaal_plaas))==(32,80,144)]
                if len(가로들)>=500:titelbalk=(min(가로들),Vertikaal_plaas);break
            assert titelbalk,'native terminal title bar not found'
            가로,Vertikaal_plaas=titelbalk[0]+564,titelbalk[1]+356
            가상입력도구('mousemove','--window',venster,str(가로),str(Vertikaal_plaas))
            def 화상기다리기(Naam,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',venster,str(maatreël_data/Naam)])
                    bispatroon_foto=Image.open(str(maatreël_data/Naam)).convert('RGB')
                    if all(bispatroon_foto.getpixel(Posisie)==빛 for Posisie,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Naam
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Vertikaal_plaas-7),(255,255,255)),((가로+7,Vertikaal_plaas+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',venster,str(가로-120),str(Vertikaal_plaas-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',venster,'500','45')
            화상기다리기('remmina-resized.png',[
                ((titelbalk[0]+447,titelbalk[1]+279),(39,49,64)),((가로,Vertikaal_plaas),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validering_verslag.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validering_verslag['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(maatreël_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_plaas in reversed(실행과정들):
                if data_plaas.poll() is None:
                    if data_plaas.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_plaas.pid,signal.SIGTERM)
                    else:data_plaas.terminate()
                    try:data_plaas.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_plaas.kill();data_plaas.wait()
            selekteerder.close()
            for lêer_inskrywing in 기록들:lêer_inskrywing.close()
            (maatreël_data/'serial.log').write_bytes(직렬입출력)
            (maatreël_data/'report.json').write_text(json.dumps(validering_verslag,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Loop()
