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
from Vykonať_príkaz import akcia_koreň


def Spustiť_2():
    KR_údaje=akcia_koreň/'build/verification/remmina';KR_údaje.mkdir(parents=True,exist_ok=True)
    overenie_správa={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];selektor=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuálny_displej=shutil.which('Xvfb')
            if virtuálny_displej: server_VALUE=[virtuálny_displej]
            else:
                뿌리파일계층=akcia_koreň.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Spustiť_2(argument_pole,환경=None,**pomenované_argumenty):
                LOG_RECORD=(KR_údaje/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_RECORD)
                údaje_pozícia=subprocess.Popen(argument_pole,env=환경,stdout=LOG_RECORD,stderr=subprocess.STDOUT,**pomenované_argumenty)
                실행과정들.append(údaje_pozícia);return údaje_pozícia
            환경=dict(os.environ)
            for Názov in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Názov,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(položka_COUNT for položka_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(položka_COUNT)).exists() and not Path('/tmp/.X%d-lock'%položka_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            displej=Spustiť_2(server_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            termín_čas=time.monotonic()+30
            while True:
                assert displej.poll() is None and time.monotonic()<termín_čas,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            hosť=subprocess.Popen(['python3',str(akcia_koreň/'Nástroje/Vykonať_príkaz.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(hosť);selektor.register(hosť.stdout,selectors.EVENT_READ)
            def 기다리기(fixka,Posun_VALUE=0):
                termín_čas=time.monotonic()+45
                while fixka not in 직렬입출력[Posun_VALUE:]:
                    assert hosť.poll() is None and time.monotonic()<termín_čas,직렬입출력[Posun_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in selektor.select(.1):
                        údaje=누름값.fileobj.read(65536)
                        if údaje:직렬입출력.extend(údaje)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            číslo_portu=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%číslo_portu)
            Spustiť_2(['dbus-run-session','--','remmina','-c',str(Profil)],환경=환경,start_new_session=True)
            def virtuálny_vstup_nástroj(*argument_pole):return subprocess.check_output(['xdotool']+list(argument_pole),env=환경,stderr=subprocess.STDOUT)
            termín_čas=time.monotonic()+60;Okno=None
            while time.monotonic()<termín_čas:
                Hľadať_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Hľadať_KR.returncode==0:
                    후보=Hľadať_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Prioritné=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Prioritné.returncode==0:Okno=후보;break
                time.sleep(.1)
            assert Okno,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtuálny_vstup_nástroj('mousemove','--window',Okno,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Spracovanie_textu):virtuálny_vstup_nástroj('type','--clearmodifiers','--delay','50',Spracovanie_textu)
            def 누름값(*누름열):virtuálny_vstup_nástroj('key','--clearmodifiers',*누름열)
            Posun_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Posun_VALUE)
            Posun_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Posun_VALUE)
            Posun_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Kľúč_VALUE, Shift+Space 또는 F9'.encode(),Posun_VALUE);기다리기(b'jkoros-native> ',Posun_VALUE)
            Posun_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Posun_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Okno,str(KR_údaje/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Posun_VALUE)
            # skutočný_údaje Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            kresba_VALUE=Image.open(str(KR_údaje/'remmina-korean.png')).convert('RGB')
            záhlavie_okna=None
            for vertikála_pozícia in range(kresba_VALUE.height):
                가로들=[가로 for 가로 in range(kresba_VALUE.width) if kresba_VALUE.getpixel((가로,vertikála_pozícia))==(32,80,144)]
                if len(가로들)>=500:záhlavie_okna=(min(가로들),vertikála_pozícia);break
            assert záhlavie_okna,'native terminal title bar not found'
            가로,vertikála_pozícia=záhlavie_okna[0]+564,záhlavie_okna[1]+356
            virtuálny_vstup_nástroj('mousemove','--window',Okno,str(가로),str(vertikála_pozícia))
            def 화상기다리기(Názov,점들):
                termín_VALUE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Okno,str(KR_údaje/Názov)])
                    bitová_mapa_IMAGE=Image.open(str(KR_údaje/Názov)).convert('RGB')
                    if all(bitová_mapa_IMAGE.getpixel(Pozícia)==빛 for Pozícia,빛 in 점들):return
                    assert time.monotonic()<termín_VALUE,'Remmina framebuffer did not settle: '+Názov
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,vertikála_pozícia-7),(255,255,255)),((가로+7,vertikála_pozícia+7),(255,255,255))])
            virtuálny_vstup_nástroj('mousedown','1','mousemove','--window',Okno,str(가로-120),str(vertikála_pozícia-80),'mouseup','1')
            time.sleep(.4)
            Posun_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Posun_VALUE)
            virtuálny_vstup_nástroj('mousemove','--window',Okno,'500','45')
            화상기다리기('remmina-resized.png',[
                ((záhlavie_okna[0]+447,záhlavie_okna[1]+279),(39,49,64)),((가로,vertikála_pozícia),(24,32,48))])
            if shutil.which('dpkg-query'):
                číslo_verzie=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                číslo_verzie=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            overenie_správa.update(passed=True,display=환경['DISPLAY'],remmina_version=číslo_verzie,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not overenie_správa['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(KR_údaje/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for údaje_pozícia in reversed(실행과정들):
                if údaje_pozícia.poll() is None:
                    if údaje_pozícia.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(údaje_pozícia.pid,signal.SIGTERM)
                    else:údaje_pozícia.terminate()
                    try:údaje_pozícia.wait(timeout=5)
                    except subprocess.TimeoutExpired:údaje_pozícia.kill();údaje_pozícia.wait()
            selektor.close()
            for Súbor_položka in 기록들:Súbor_položka.close()
            (KR_údaje/'serial.log').write_bytes(직렬입출력)
            (KR_údaje/'report.json').write_text(json.dumps(overenie_správa,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Spustiť_2()
