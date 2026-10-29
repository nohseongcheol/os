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
from Wykonaj_polecenie import Project_korzeń


def Uruchom_2():
    KR_dane=Project_korzeń/'build/verification/remmina';KR_dane.mkdir(parents=True,exist_ok=True)
    walidacja_Raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];selektor=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            wirtualny_wyświetlać=shutil.which('Xvfb')
            if wirtualny_wyświetlać: serwer_WARTOŚĆ=[wirtualny_wyświetlać]
            else:
                뿌리파일계층=Project_korzeń.parent/'rpi4/build/rootfs'
                serwer_WARTOŚĆ=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Uruchom_2(argument_TABLICA,środowisko=None,**argument_nazwany):
                LOG_zapis=(KR_dane/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_zapis)
                dane_stanowisko=subprocess.Popen(argument_TABLICA,env=środowisko,stdout=LOG_zapis,stderr=subprocess.STDOUT,**argument_nazwany)
                실행과정들.append(dane_stanowisko);return dane_stanowisko
            środowisko=dict(os.environ)
            for Nazwa in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):środowisko.pop(Nazwa,None)
            środowisko.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(towar_ILE_LICZB for towar_ILE_LICZB in range(80,200) if not Path('/tmp/.X11-unix/X'+str(towar_ILE_LICZB)).exists() and not Path('/tmp/.X%d-lock'%towar_ILE_LICZB).exists())
            środowisko['DISPLAY']=':'+str(수치)
            wyświetlacz=Uruchom_2(serwer_WARTOŚĆ+[środowisko['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],środowisko=środowisko)
            termin_ostateczny_CZAS=time.monotonic()+30
            while True:
                assert wyświetlacz.poll() is None and time.monotonic()<termin_ostateczny_CZAS,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=środowisko,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gość=subprocess.Popen(['python3',str(Project_korzeń/'narzędzia/Wykonaj_polecenie.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gość);selektor.register(gość.stdout,selectors.EVENT_READ)
            def 기다리기(pisak,przesunąć_WARTOŚĆ_450fc799=0):
                termin_ostateczny_CZAS=time.monotonic()+45
                while pisak not in 직렬입출력[przesunąć_WARTOŚĆ_450fc799:]:
                    assert gość.poll() is None and time.monotonic()<termin_ostateczny_CZAS,직렬입출력[przesunąć_WARTOŚĆ_450fc799:].decode('utf-8','replace')
                    for 누름값,_ in selektor.select(.1):
                        dane=누름값.fileobj.read(65536)
                        if dane:직렬입출력.extend(dane)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            numer_portu=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%numer_portu)
            Uruchom_2(['dbus-run-session','--','remmina','-c',str(Profil)],środowisko=środowisko,start_new_session=True)
            def wirtualny_wejście_narzędzie(*argument_TABLICA):return subprocess.check_output(['xdotool']+list(argument_TABLICA),env=środowisko,stderr=subprocess.STDOUT)
            termin_ostateczny_CZAS=time.monotonic()+60;Okno=None
            while time.monotonic()<termin_ostateczny_CZAS:
                Search_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=środowisko,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Search_KR.returncode==0:
                    kandydat=Search_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Priorytetowe=subprocess.run(['xdotool','windowfocus','--sync',kandydat],env=środowisko,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Priorytetowe.returncode==0:Okno=kandydat;break
                time.sleep(.1)
            assert Okno,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            wirtualny_wejście_narzędzie('mousemove','--window',Okno,'280','240','click','1')
            time.sleep(1)
            def 글자입력(tekst):wirtualny_wejście_narzędzie('type','--clearmodifiers','--delay','50',tekst)
            def 누름값(*누름열):wirtualny_wejście_narzędzie('key','--clearmodifiers',*누름열)
            przesunąć_WARTOŚĆ_450fc799=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),przesunąć_WARTOŚĆ_450fc799)
            przesunąć_WARTOŚĆ_450fc799=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),przesunąć_WARTOŚĆ_450fc799)
            przesunąć_WARTOŚĆ_450fc799=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/zero_operand Klucz_WARTOŚĆ, Shift+Space 또는 F9'.encode(),przesunąć_WARTOŚĆ_450fc799);기다리기(b'jkoros-native> ',przesunąć_WARTOŚĆ_450fc799)
            przesunąć_WARTOŚĆ_450fc799=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),przesunąć_WARTOŚĆ_450fc799)
            subprocess.check_call(['import','-display',środowisko['DISPLAY'],'-window',Okno,str(KR_dane/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',przesunąć_WARTOŚĆ_450fc799)
            # rzeczywisty_dane Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            rysunek_WARTOŚĆ=Image.open(str(KR_dane/'remmina-korean.png')).convert('RGB')
            pasek_tytułu=None
            for gałąź_stanowisko in range(rysunek_WARTOŚĆ.height):
                가로들=[가로 for 가로 in range(rysunek_WARTOŚĆ.width) if rysunek_WARTOŚĆ.getpixel((가로,gałąź_stanowisko))==(32,80,144)]
                if len(가로들)>=500:pasek_tytułu=(min(가로들),gałąź_stanowisko);break
            assert pasek_tytułu,'native terminal title bar not found'
            가로,gałąź_stanowisko=pasek_tytułu[0]+564,pasek_tytułu[1]+356
            wirtualny_wejście_narzędzie('mousemove','--window',Okno,str(가로),str(gałąź_stanowisko))
            def 화상기다리기(Nazwa,점들):
                termin_ostateczny_WARTOŚĆ=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',środowisko['DISPLAY'],'-window',Okno,str(KR_dane/Nazwa)])
                    mapa_bitowa_OBRAZ=Image.open(str(KR_dane/Nazwa)).convert('RGB')
                    if all(mapa_bitowa_OBRAZ.getpixel(pozycja)==빛 for pozycja,빛 in 점들):return
                    assert time.monotonic()<termin_ostateczny_WARTOŚĆ,'Remmina framebuffer did not settle: '+Nazwa
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,gałąź_stanowisko-7),(255,255,255)),((가로+7,gałąź_stanowisko+7),(255,255,255))])
            wirtualny_wejście_narzędzie('mousedown','1','mousemove','--window',Okno,str(가로-120),str(gałąź_stanowisko-80),'mouseup','1')
            time.sleep(.4)
            przesunąć_WARTOŚĆ_450fc799=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',przesunąć_WARTOŚĆ_450fc799)
            wirtualny_wejście_narzędzie('mousemove','--window',Okno,'500','45')
            화상기다리기('remmina-resized.png',[
                ((pasek_tytułu[0]+447,pasek_tytułu[1]+279),(39,49,64)),((가로,gałąź_stanowisko),(24,32,48))])
            if shutil.which('dpkg-query'):
                numer_wersji=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                numer_wersji=subprocess.check_output(['remmina','--version'],env=środowisko,stderr=subprocess.STDOUT).decode('utf-8','replace')
            walidacja_Raport.update(passed=True,display=środowisko['DISPLAY'],remmina_version=numer_wersji,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not walidacja_Raport['passed'] and 'środowisko' in locals() and środowisko.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',środowisko['DISPLAY'],'-window','root',str(KR_dane/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for dane_stanowisko in reversed(실행과정들):
                if dane_stanowisko.poll() is None:
                    if dane_stanowisko.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(dane_stanowisko.pid,signal.SIGTERM)
                    else:dane_stanowisko.terminate()
                    try:dane_stanowisko.wait(timeout=5)
                    except subprocess.TimeoutExpired:dane_stanowisko.kill();dane_stanowisko.wait()
            selektor.close()
            for Plik_wpis in 기록들:Plik_wpis.close()
            (KR_dane/'serial.log').write_bytes(직렬입출력)
            (KR_dane/'report.json').write_text(json.dumps(walidacja_Raport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Uruchom_2()
