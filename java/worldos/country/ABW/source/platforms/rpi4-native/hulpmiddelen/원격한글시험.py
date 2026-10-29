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
from Uitvoeren_opdracht import Taken_wortel


def starten():
    HR_gegevens=Taken_wortel/'build/verification/remmina';HR_gegevens.mkdir(parents=True,exist_ok=True)
    validatie_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];selector=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtueel_weergeven=shutil.which('Xvfb')
            if virtueel_weergeven: server_WAARDE=[virtueel_weergeven]
            else:
                뿌리파일계층=Taken_wortel.parent/'rpi4/build/rootfs'
                server_WAARDE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def starten(argument_MATRIX,omgeving=None,**benoemd_argument):
                LOG_RECORD=(HR_gegevens/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_RECORD)
                gegevens_functie=subprocess.Popen(argument_MATRIX,env=omgeving,stdout=LOG_RECORD,stderr=subprocess.STDOUT,**benoemd_argument)
                실행과정들.append(gegevens_functie);return gegevens_functie
            omgeving=dict(os.environ)
            for Naam in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):omgeving.pop(Naam,None)
            omgeving.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(item_AANTAL for item_AANTAL in range(80,200) if not Path('/tmp/.X11-unix/X'+str(item_AANTAL)).exists() and not Path('/tmp/.X%d-lock'%item_AANTAL).exists())
            omgeving['DISPLAY']=':'+str(수치)
            beeldscherm=starten(server_WAARDE+[omgeving['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],omgeving=omgeving)
            deadline_TIJD=time.monotonic()+30
            while True:
                assert beeldscherm.poll() is None and time.monotonic()<deadline_TIJD,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=omgeving,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gast=subprocess.Popen(['python3',str(Taken_wortel/'hulpmiddelen/Uitvoeren_opdracht.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gast);selector.register(gast.stdout,selectors.EVENT_READ)
            def 기다리기(markering,VERSCHUIVING_WAARDE=0):
                deadline_TIJD=time.monotonic()+45
                while markering not in 직렬입출력[VERSCHUIVING_WAARDE:]:
                    assert gast.poll() is None and time.monotonic()<deadline_TIJD,직렬입출력[VERSCHUIVING_WAARDE:].decode('utf-8','replace')
                    for 누름값,_ in selector.select(.1):
                        gegevens=누름값.fileobj.read(65536)
                        if gegevens:직렬입출력.extend(gegevens)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            poortnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profiel=작업경로/'test.remmina'
            Profiel.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%poortnummer)
            starten(['dbus-run-session','--','remmina','-c',str(Profiel)],omgeving=omgeving,start_new_session=True)
            def virtueel_invoer_hulpmiddel(*argument_MATRIX):return subprocess.check_output(['xdotool']+list(argument_MATRIX),env=omgeving,stderr=subprocess.STDOUT)
            deadline_TIJD=time.monotonic()+60;Venster=None
            while time.monotonic()<deadline_TIJD:
                Search_HR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=omgeving,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Search_HR.returncode==0:
                    sollicitant=Search_HR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Prioriteit=subprocess.run(['xdotool','windowfocus','--sync',sollicitant],env=omgeving,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Prioriteit.returncode==0:Venster=sollicitant;break
                time.sleep(.1)
            assert Venster,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtueel_invoer_hulpmiddel('mousemove','--window',Venster,'280','240','click','1')
            time.sleep(1)
            def 글자입력(tekst):virtueel_invoer_hulpmiddel('type','--clearmodifiers','--delay','50',tekst)
            def 누름값(*누름열):virtueel_invoer_hulpmiddel('key','--clearmodifiers',*누름열)
            VERSCHUIVING_WAARDE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nul_operand toets_WAARDE, Shift+Space 또는 F9'.encode(),VERSCHUIVING_WAARDE);기다리기(b'jkoros-native> ',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),VERSCHUIVING_WAARDE)
            subprocess.check_call(['import','-display',omgeving['DISPLAY'],'-window',Venster,str(HR_gegevens/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',VERSCHUIVING_WAARDE)
            # werkelijk_gegevens Remmina의 scherm 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            tekening_WAARDE=Image.open(str(HR_gegevens/'remmina-korean.png')).convert('RGB')
            titelbalk=None
            for Verticaal_functie in range(tekening_WAARDE.height):
                가로들=[가로 for 가로 in range(tekening_WAARDE.width) if tekening_WAARDE.getpixel((가로,Verticaal_functie))==(32,80,144)]
                if len(가로들)>=500:titelbalk=(min(가로들),Verticaal_functie);break
            assert titelbalk,'native terminal title bar not found'
            가로,Verticaal_functie=titelbalk[0]+564,titelbalk[1]+356
            virtueel_invoer_hulpmiddel('mousemove','--window',Venster,str(가로),str(Verticaal_functie))
            def 화상기다리기(Naam,점들):
                deadline_WAARDE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',omgeving['DISPLAY'],'-window',Venster,str(HR_gegevens/Naam)])
                    bitmap_kopie=Image.open(str(HR_gegevens/Naam)).convert('RGB')
                    if all(bitmap_kopie.getpixel(positie)==빛 for positie,빛 in 점들):return
                    assert time.monotonic()<deadline_WAARDE,'Remmina framebuffer did not settle: '+Naam
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Verticaal_functie-7),(255,255,255)),((가로+7,Verticaal_functie+7),(255,255,255))])
            virtueel_invoer_hulpmiddel('mousedown','1','mousemove','--window',Venster,str(가로-120),str(Verticaal_functie-80),'mouseup','1')
            time.sleep(.4)
            VERSCHUIVING_WAARDE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',VERSCHUIVING_WAARDE)
            virtueel_invoer_hulpmiddel('mousemove','--window',Venster,'500','45')
            화상기다리기('remmina-resized.png',[
                ((titelbalk[0]+447,titelbalk[1]+279),(39,49,64)),((가로,Verticaal_functie),(24,32,48))])
            if shutil.which('dpkg-query'):
                versienummer=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versienummer=subprocess.check_output(['remmina','--version'],env=omgeving,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validatie_Rapport.update(passed=True,display=omgeving['DISPLAY'],remmina_version=versienummer,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validatie_Rapport['passed'] and 'omgeving' in locals() and omgeving.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',omgeving['DISPLAY'],'-window','root',str(HR_gegevens/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for gegevens_functie in reversed(실행과정들):
                if gegevens_functie.poll() is None:
                    if gegevens_functie.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(gegevens_functie.pid,signal.SIGTERM)
                    else:gegevens_functie.terminate()
                    try:gegevens_functie.wait(timeout=5)
                    except subprocess.TimeoutExpired:gegevens_functie.kill();gegevens_functie.wait()
            selector.close()
            for Bestand_invoer in 기록들:Bestand_invoer.close()
            (HR_gegevens/'serial.log').write_bytes(직렬입출력)
            (HR_gegevens/'report.json').write_text(json.dumps(validatie_Rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':starten()
