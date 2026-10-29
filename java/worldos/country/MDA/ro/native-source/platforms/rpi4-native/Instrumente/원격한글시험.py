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
from executa_comandă import Project_rădăcină


def Pornește():
    KR_date=Project_rădăcină/'build/verification/remmina';KR_date.mkdir(parents=True,exist_ok=True)
    validare_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];selector=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: server_VALUE=[가상표시장치]
            else:
                뿌리파일계층=Project_rădăcină.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Pornește(argument_ARRAY,환경=None,**argument_denumit):
                LOG_RECORD=(KR_date/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_RECORD)
                date_poziție=subprocess.Popen(argument_ARRAY,env=환경,stdout=LOG_RECORD,stderr=subprocess.STDOUT,**argument_denumit)
                실행과정들.append(date_poziție);return date_poziție
            환경=dict(os.environ)
            for Nume in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Nume,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(element_COUNT for element_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(element_COUNT)).exists() and not Path('/tmp/.X%d-lock'%element_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            afișaj=Pornește(server_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            dată_limită_oră=time.monotonic()+30
            while True:
                assert afișaj.poll() is None and time.monotonic()<dată_limită_oră,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            invitat=subprocess.Popen(['python3',str(Project_rădăcină/'Instrumente/executa_comandă.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(invitat);selector.register(invitat.stdout,selectors.EVENT_READ)
            def 기다리기(marcaj,OFFSET_VALUE=0):
                dată_limită_oră=time.monotonic()+45
                while marcaj not in 직렬입출력[OFFSET_VALUE:]:
                    assert invitat.poll() is None and time.monotonic()<dată_limită_oră,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in selector.select(.1):
                        date=누름값.fileobj.read(65536)
                        if date:직렬입출력.extend(date)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            număr_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%număr_port)
            Pornește(['dbus-run-session','--','remmina','-c',str(Profil)],환경=환경,start_new_session=True)
            def 가상입력도구(*argument_ARRAY):return subprocess.check_output(['xdotool']+list(argument_ARRAY),env=환경,stderr=subprocess.STDOUT)
            dată_limită_oră=time.monotonic()+60;Fereastră=None
            while time.monotonic()<dată_limită_oră:
                căuta_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if căuta_KR.returncode==0:
                    후보=căuta_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Prioritare=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Prioritare.returncode==0:Fereastră=후보;break
                time.sleep(.1)
            assert Fereastră,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Fereastră,'280','240','click','1')
            time.sleep(1)
            def 글자입력(SMS):가상입력도구('type','--clearmodifiers','--delay','50',SMS)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/zero_operand Cheie_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Fereastră,str(KR_date/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # real_date Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            desen_VALUE=Image.open(str(KR_date/'remmina-korean.png')).convert('RGB')
            bară_de_titlu=None
            for Verticală_poziție in range(desen_VALUE.height):
                가로들=[가로 for 가로 in range(desen_VALUE.width) if desen_VALUE.getpixel((가로,Verticală_poziție))==(32,80,144)]
                if len(가로들)>=500:bară_de_titlu=(min(가로들),Verticală_poziție);break
            assert bară_de_titlu,'native terminal title bar not found'
            가로,Verticală_poziție=bară_de_titlu[0]+564,bară_de_titlu[1]+356
            가상입력도구('mousemove','--window',Fereastră,str(가로),str(Verticală_poziție))
            def 화상기다리기(Nume,점들):
                dată_limită_VALUE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Fereastră,str(KR_date/Nume)])
                    bitmap_IMAGE=Image.open(str(KR_date/Nume)).convert('RGB')
                    if all(bitmap_IMAGE.getpixel(Poziție)==빛 for Poziție,빛 in 점들):return
                    assert time.monotonic()<dată_limită_VALUE,'Remmina framebuffer did not settle: '+Nume
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Verticală_poziție-7),(255,255,255)),((가로+7,Verticală_poziție+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Fereastră,str(가로-120),str(Verticală_poziție-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',Fereastră,'500','45')
            화상기다리기('remmina-resized.png',[
                ((bară_de_titlu[0]+447,bară_de_titlu[1]+279),(39,49,64)),((가로,Verticală_poziție),(24,32,48))])
            if shutil.which('dpkg-query'):
                număr_de_versiune=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                număr_de_versiune=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validare_raport.update(passed=True,display=환경['DISPLAY'],remmina_version=număr_de_versiune,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validare_raport['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(KR_date/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for date_poziție in reversed(실행과정들):
                if date_poziție.poll() is None:
                    if date_poziție.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(date_poziție.pid,signal.SIGTERM)
                    else:date_poziție.terminate()
                    try:date_poziție.wait(timeout=5)
                    except subprocess.TimeoutExpired:date_poziție.kill();date_poziție.wait()
            selector.close()
            for Fișier_intrare in 기록들:Fișier_intrare.close()
            (KR_date/'serial.log').write_bytes(직렬입출력)
            (KR_date/'report.json').write_text(json.dumps(validare_raport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Pornește()
