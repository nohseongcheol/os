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
from Izvrši_komanda import radnja_koren


def koristiti():
    KR_podaci=radnja_koren/'build/verification/remmina';KR_podaci.mkdir(parents=True,exist_ok=True)
    provera_valjanosti_izveštaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];birač=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: server_VALUE=[가상표시장치]
            else:
                뿌리파일계층=radnja_koren.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def koristiti(argument_niz,환경=None,**imenovani_argument):
                LOG_snimi=(KR_podaci/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_snimi)
                podaci_pozicija=subprocess.Popen(argument_niz,env=환경,stdout=LOG_snimi,stderr=subprocess.STDOUT,**imenovani_argument)
                실행과정들.append(podaci_pozicija);return podaci_pozicija
            환경=dict(os.environ)
            for ime in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(ime,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(stavka_COUNT for stavka_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(stavka_COUNT)).exists() and not Path('/tmp/.X%d-lock'%stavka_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            ekran=koristiti(server_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            krajnji_rok_TIME=time.monotonic()+30
            while True:
                assert ekran.poll() is None and time.monotonic()<krajnji_rok_TIME,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gost=subprocess.Popen(['python3',str(radnja_koren/'Alatke/Izvrši_komanda.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gost);birač.register(gost.stdout,selectors.EVENT_READ)
            def 기다리기(označivač,Pomak_VALUE=0):
                krajnji_rok_TIME=time.monotonic()+45
                while označivač not in 직렬입출력[Pomak_VALUE:]:
                    assert gost.poll() is None and time.monotonic()<krajnji_rok_TIME,직렬입출력[Pomak_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in birač.select(.1):
                        podaci=누름값.fileobj.read(65536)
                        if podaci:직렬입출력.extend(podaci)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            broj_porta=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%broj_porta)
            koristiti(['dbus-run-session','--','remmina','-c',str(Profil)],환경=환경,start_new_session=True)
            def 가상입력도구(*argument_niz):return subprocess.check_output(['xdotool']+list(argument_niz),env=환경,stderr=subprocess.STDOUT)
            krajnji_rok_TIME=time.monotonic()+60;prozor=None
            while time.monotonic()<krajnji_rok_TIME:
                SEARCH_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if SEARCH_KR.returncode==0:
                    후보=SEARCH_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    U_fokusu=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if U_fokusu.returncode==0:prozor=후보;break
                time.sleep(.1)
            assert prozor,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',prozor,'280','240','click','1')
            time.sleep(1)
            def 글자입력(SMS):가상입력도구('type','--clearmodifiers','--delay','50',SMS)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Pomak_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Pomak_VALUE)
            Pomak_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Pomak_VALUE)
            Pomak_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nula_operand Ključ_VALUE, Shift+Space 또는 F9'.encode(),Pomak_VALUE);기다리기(b'jkoros-native> ',Pomak_VALUE)
            Pomak_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Pomak_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',prozor,str(KR_podaci/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Pomak_VALUE)
            # stvarni_podaci Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            crtež_VALUE=Image.open(str(KR_podaci/'remmina-korean.png')).convert('RGB')
            naslovna_traka=None
            for vertikala_pozicija in range(crtež_VALUE.height):
                가로들=[가로 for 가로 in range(crtež_VALUE.width) if crtež_VALUE.getpixel((가로,vertikala_pozicija))==(32,80,144)]
                if len(가로들)>=500:naslovna_traka=(min(가로들),vertikala_pozicija);break
            assert naslovna_traka,'native terminal title bar not found'
            가로,vertikala_pozicija=naslovna_traka[0]+564,naslovna_traka[1]+356
            가상입력도구('mousemove','--window',prozor,str(가로),str(vertikala_pozicija))
            def 화상기다리기(ime,점들):
                krajnji_rok_VALUE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',prozor,str(KR_podaci/ime)])
                    raster_IMAGE=Image.open(str(KR_podaci/ime)).convert('RGB')
                    if all(raster_IMAGE.getpixel(pozicija)==빛 for pozicija,빛 in 점들):return
                    assert time.monotonic()<krajnji_rok_VALUE,'Remmina framebuffer did not settle: '+ime
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,vertikala_pozicija-7),(255,255,255)),((가로+7,vertikala_pozicija+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',prozor,str(가로-120),str(vertikala_pozicija-80),'mouseup','1')
            time.sleep(.4)
            Pomak_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Pomak_VALUE)
            가상입력도구('mousemove','--window',prozor,'500','45')
            화상기다리기('remmina-resized.png',[
                ((naslovna_traka[0]+447,naslovna_traka[1]+279),(39,49,64)),((가로,vertikala_pozicija),(24,32,48))])
            if shutil.which('dpkg-query'):
                broj_verzije=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                broj_verzije=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            provera_valjanosti_izveštaj.update(passed=True,display=환경['DISPLAY'],remmina_version=broj_verzije,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not provera_valjanosti_izveštaj['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(KR_podaci/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for podaci_pozicija in reversed(실행과정들):
                if podaci_pozicija.poll() is None:
                    if podaci_pozicija.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(podaci_pozicija.pid,signal.SIGTERM)
                    else:podaci_pozicija.terminate()
                    try:podaci_pozicija.wait(timeout=5)
                    except subprocess.TimeoutExpired:podaci_pozicija.kill();podaci_pozicija.wait()
            birač.close()
            for Datoteka_stavka in 기록들:Datoteka_stavka.close()
            (KR_podaci/'serial.log').write_bytes(직렬입출력)
            (KR_podaci/'report.json').write_text(json.dumps(provera_valjanosti_izveštaj,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':koristiti()
