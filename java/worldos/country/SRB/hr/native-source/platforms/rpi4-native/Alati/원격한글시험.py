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
from Izvrši_naredba import akcija_korijen


def Pokreni():
    KR_podaci=akcija_korijen/'build/verification/remmina';KR_podaci.mkdir(parents=True,exist_ok=True)
    provjera_izvješće={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];odabirač=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: server_VALUE=[가상표시장치]
            else:
                뿌리파일계층=akcija_korijen.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Pokreni(argument_ARRAY,okruženje=None,**imenovani_argument):
                LOG_zapis=(KR_podaci/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_zapis)
                podaci_položaj=subprocess.Popen(argument_ARRAY,env=okruženje,stdout=LOG_zapis,stderr=subprocess.STDOUT,**imenovani_argument)
                실행과정들.append(podaci_položaj);return podaci_položaj
            okruženje=dict(os.environ)
            for Ime in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):okruženje.pop(Ime,None)
            okruženje.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(artikl_COUNT for artikl_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(artikl_COUNT)).exists() and not Path('/tmp/.X%d-lock'%artikl_COUNT).exists())
            okruženje['DISPLAY']=':'+str(수치)
            zaslon=Pokreni(server_VALUE+[okruženje['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],okruženje=okruženje)
            rok_za_dovršetak_TIME=time.monotonic()+30
            while True:
                assert zaslon.poll() is None and time.monotonic()<rok_za_dovršetak_TIME,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=okruženje,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gost=subprocess.Popen(['python3',str(akcija_korijen/'Alati/Izvrši_naredba.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gost);odabirač.register(gost.stdout,selectors.EVENT_READ)
            def 기다리기(marker,pomak_VALUE=0):
                rok_za_dovršetak_TIME=time.monotonic()+45
                while marker not in 직렬입출력[pomak_VALUE:]:
                    assert gost.poll() is None and time.monotonic()<rok_za_dovršetak_TIME,직렬입출력[pomak_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in odabirač.select(.1):
                        podaci=누름값.fileobj.read(65536)
                        if podaci:직렬입출력.extend(podaci)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            broj_priključka=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%broj_priključka)
            Pokreni(['dbus-run-session','--','remmina','-c',str(Profil)],okruženje=okruženje,start_new_session=True)
            def 가상입력도구(*argument_ARRAY):return subprocess.check_output(['xdotool']+list(argument_ARRAY),env=okruženje,stderr=subprocess.STDOUT)
            rok_za_dovršetak_TIME=time.monotonic()+60;Prozor=None
            while time.monotonic()<rok_za_dovršetak_TIME:
                Traži_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=okruženje,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Traži_KR.returncode==0:
                    후보=Traži_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    U_fokusu=subprocess.run(['xdotool','windowfocus','--sync',후보],env=okruženje,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if U_fokusu.returncode==0:Prozor=후보;break
                time.sleep(.1)
            assert Prozor,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Prozor,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Tekst):가상입력도구('type','--clearmodifiers','--delay','50',Tekst)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            pomak_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),pomak_VALUE)
            pomak_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),pomak_VALUE)
            pomak_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nula_operand Ključ_VALUE, Shift+Space 또는 F9'.encode(),pomak_VALUE);기다리기(b'jkoros-native> ',pomak_VALUE)
            pomak_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),pomak_VALUE)
            subprocess.check_call(['import','-display',okruženje['DISPLAY'],'-window',Prozor,str(KR_podaci/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',pomak_VALUE)
            # stvaran_podaci Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            crtež_VALUE=Image.open(str(KR_podaci/'remmina-korean.png')).convert('RGB')
            naslovna_traka=None
            for Okomito_položaj in range(crtež_VALUE.height):
                가로들=[가로 for 가로 in range(crtež_VALUE.width) if crtež_VALUE.getpixel((가로,Okomito_položaj))==(32,80,144)]
                if len(가로들)>=500:naslovna_traka=(min(가로들),Okomito_položaj);break
            assert naslovna_traka,'native terminal title bar not found'
            가로,Okomito_položaj=naslovna_traka[0]+564,naslovna_traka[1]+356
            가상입력도구('mousemove','--window',Prozor,str(가로),str(Okomito_položaj))
            def 화상기다리기(Ime,점들):
                rok_za_dovršetak_VALUE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',okruženje['DISPLAY'],'-window',Prozor,str(KR_podaci/Ime)])
                    bitmap_IMAGE=Image.open(str(KR_podaci/Ime)).convert('RGB')
                    if all(bitmap_IMAGE.getpixel(Položaj)==빛 for Položaj,빛 in 점들):return
                    assert time.monotonic()<rok_za_dovršetak_VALUE,'Remmina framebuffer did not settle: '+Ime
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Okomito_položaj-7),(255,255,255)),((가로+7,Okomito_položaj+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Prozor,str(가로-120),str(Okomito_položaj-80),'mouseup','1')
            time.sleep(.4)
            pomak_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',pomak_VALUE)
            가상입력도구('mousemove','--window',Prozor,'500','45')
            화상기다리기('remmina-resized.png',[
                ((naslovna_traka[0]+447,naslovna_traka[1]+279),(39,49,64)),((가로,Okomito_položaj),(24,32,48))])
            if shutil.which('dpkg-query'):
                broj_verzije=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                broj_verzije=subprocess.check_output(['remmina','--version'],env=okruženje,stderr=subprocess.STDOUT).decode('utf-8','replace')
            provjera_izvješće.update(passed=True,display=okruženje['DISPLAY'],remmina_version=broj_verzije,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not provjera_izvješće['passed'] and 'okruženje' in locals() and okruženje.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',okruženje['DISPLAY'],'-window','root',str(KR_podaci/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for podaci_položaj in reversed(실행과정들):
                if podaci_položaj.poll() is None:
                    if podaci_položaj.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(podaci_položaj.pid,signal.SIGTERM)
                    else:podaci_položaj.terminate()
                    try:podaci_položaj.wait(timeout=5)
                    except subprocess.TimeoutExpired:podaci_položaj.kill();podaci_položaj.wait()
            odabirač.close()
            for Datoteka_unos in 기록들:Datoteka_unos.close()
            (KR_podaci/'serial.log').write_bytes(직렬입출력)
            (KR_podaci/'report.json').write_text(json.dumps(provjera_izvješće,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Pokreni()
