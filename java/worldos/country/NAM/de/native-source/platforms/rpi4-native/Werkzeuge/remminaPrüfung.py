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
from befehlAusführen import projektWurzel


def ausführenVorgang():
    ergebnisDaten=projektWurzel/'build/verification/remmina';ergebnisDaten.mkdir(parents=True,exist_ok=True)
    validierungBericht={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as arbeitendPfad:
        arbeitendPfad=Path(arbeitendPfad);laufendProzesse=[];auswähler=selectors.DefaultSelector();seriellEinAusgabe=bytearray()
        protokolldateiAufzeichnungen=[]
        try:
            virtuellDarstellen=shutil.which('Xvfb')
            if virtuellDarstellen: dienstanbieterWert=[virtuellDarstellen]
            else:
                wurzeldateisystem=projektWurzel.parent/'rpi4/build/rootfs'
                dienstanbieterWert=['qemu-aarch64','-L',str(wurzeldateisystem),str(wurzeldateisystem/'usr/bin/Xvfb')]
            def ausführenVorgang(argumentDatenfeld,umgebung=None,**benanntArgument):
                protokolldateiAufzeichnung=(ergebnisDaten/('process-%d.log'%len(protokolldateiAufzeichnungen))).open('wb');protokolldateiAufzeichnungen.append(protokolldateiAufzeichnung)
                datenPosition=subprocess.Popen(argumentDatenfeld,env=umgebung,stdout=protokolldateiAufzeichnung,stderr=subprocess.STDOUT,**benanntArgument)
                laufendProzesse.append(datenPosition);return datenPosition
            umgebung=dict(os.environ)
            for Name in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):umgebung.pop(Name,None)
            umgebung.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(arbeitendPfad/'config'),XDG_DATA_HOME=str(arbeitendPfad/'data'),XDG_CACHE_HOME=str(arbeitendPfad/'cache'))
            numerischWert=next(elementeintragAnzahl for elementeintragAnzahl in range(80,200) if not Path('/tmp/.X11-unix/X'+str(elementeintragAnzahl)).exists() and not Path('/tmp/.X%d-lock'%elementeintragAnzahl).exists())
            umgebung['DISPLAY']=':'+str(numerischWert)
            darstellenGerät=ausführenVorgang(dienstanbieterWert+[umgebung['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],umgebung=umgebung)
            fristZeit=time.monotonic()+30
            while True:
                assert darstellenGerät.poll() is None and time.monotonic()<fristZeit,'Xvfb failed; see process-0.log'
                vorbereitungFertig=subprocess.run(['xdotool','getdisplaygeometry'],env=umgebung,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if vorbereitungFertig.returncode==0:break
                time.sleep(.1)
            gast=subprocess.Popen(['python3',str(projektWurzel/'Werkzeuge/befehlAusführen.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            laufendProzesse.append(gast);auswähler.register(gast.stdout,selectors.EVENT_READ)
            def abwarten(markierung,versatzwertWert=0):
                fristZeit=time.monotonic()+45
                while markierung not in seriellEinAusgabe[versatzwertWert:]:
                    assert gast.poll() is None and time.monotonic()<fristZeit,seriellEinAusgabe[versatzwertWert:].decode('utf-8','replace')
                    for gedrücktWert,_ in auswähler.select(.1):
                        Daten=gedrücktWert.fileobj.read(65536)
                        if Daten:seriellEinAusgabe.extend(Daten)
            abwarten(b'TERMINAL READY');abwarten(b'jkoros-native> ',seriellEinAusgabe.rfind(b'TERMINAL READY'))
            portNummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',seriellEinAusgabe).group(1))
            profil=arbeitendPfad/'test.remmina'
            profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%portNummer)
            ausführenVorgang(['dbus-run-session','--','remmina','-c',str(profil)],umgebung=umgebung,start_new_session=True)
            def virtuellEingabeWerkzeug(*argumentDatenfeld):return subprocess.check_output(['xdotool']+list(argumentDatenfeld),env=umgebung,stderr=subprocess.STDOUT)
            fristZeit=time.monotonic()+60;fenster=None
            while time.monotonic()<fristZeit:
                ergebnisSuchen=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=umgebung,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ergebnisSuchen.returncode==0:
                    kandidat=ergebnisSuchen.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    fokussiert=subprocess.run(['xdotool','windowfocus','--sync',kandidat],env=umgebung,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if fokussiert.returncode==0:fenster=kandidat;break
                time.sleep(.1)
            assert fenster,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtuellEingabeWerkzeug('mousemove','--window',fenster,'280','240','click','1')
            time.sleep(1)
            def eingegebenZeichen(Text):virtuellEingabeWerkzeug('type','--clearmodifiers','--delay','50',Text)
            def gedrücktWert(*gedrücktTasten):virtuellEingabeWerkzeug('key','--clearmodifiers',*gedrücktTasten)
            versatzwertWert=len(seriellEinAusgabe);eingegebenZeichen('echo ');gedrücktWert('F9');eingegebenZeichen('dkssudgktpdy gksrmf');gedrücktWert('F9','Return')
            abwarten('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),versatzwertWert)
            versatzwertWert=len(seriellEinAusgabe);eingegebenZeichen('echo ');gedrücktWert('shift+space');eingegebenZeichen('rhk rkqtk');gedrücktWert('shift+space','Return')
            abwarten('\r\n과 갑사\r\njkoros-native> '.encode(),versatzwertWert)
            versatzwertWert=len(seriellEinAusgabe);eingegebenZeichen('help ko');gedrücktWert('Return')
            abwarten('한/nullwertOperand tasteWert, Shift+Space 또는 F9'.encode(),versatzwertWert);abwarten(b'jkoros-native> ',versatzwertWert)
            versatzwertWert=len(seriellEinAusgabe);eingegebenZeichen('echo ');gedrücktWert('F9');eingegebenZeichen('gksrmf dlfr')
            abwarten('읽'.encode(),versatzwertWert)
            subprocess.check_call(['import','-display',umgebung['DISPLAY'],'-window',fenster,str(ergebnisDaten/'remmina-korean.png')])
            gedrücktWert('F9','Return')
            abwarten(b'jkoros-native> ',versatzwertWert)
            # tatsächlichDaten Remmina의 Bildschirm 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            Zeichnung=Image.open(str(ergebnisDaten/'remmina-korean.png')).convert('RGB')
            titelLeiste=None
            for senkrechtPosition in range(Zeichnung.height):
                waagerechtStellungen=[waagerechtPosition for waagerechtPosition in range(Zeichnung.width) if Zeichnung.getpixel((waagerechtPosition,senkrechtPosition))==(32,80,144)]
                if len(waagerechtStellungen)>=500:titelLeiste=(min(waagerechtStellungen),senkrechtPosition);break
            assert titelLeiste,'native terminal title bar not found'
            waagerechtPosition,senkrechtPosition=titelLeiste[0]+564,titelLeiste[1]+356
            virtuellEingabeWerkzeug('mousemove','--window',fenster,str(waagerechtPosition),str(senkrechtPosition))
            def fürBitkarteWarten(Name,punkteListe):
                fristWert=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',umgebung['DISPLAY'],'-window',fenster,str(ergebnisDaten/Name)])
                    bitkarteAbbild=Image.open(str(ergebnisDaten/Name)).convert('RGB')
                    if all(bitkarteAbbild.getpixel(position)==Farbe for position,Farbe in punkteListe):return
                    assert time.monotonic()<fristWert,'Remmina framebuffer did not settle: '+Name
                    time.sleep(.1)
            fürBitkarteWarten('remmina-resize-cursor.png',[
                ((waagerechtPosition-7,senkrechtPosition-7),(255,255,255)),((waagerechtPosition+7,senkrechtPosition+7),(255,255,255))])
            virtuellEingabeWerkzeug('mousedown','1','mousemove','--window',fenster,str(waagerechtPosition-120),str(senkrechtPosition-80),'mouseup','1')
            time.sleep(.4)
            versatzwertWert=len(seriellEinAusgabe);eingegebenZeichen('terminal size');gedrücktWert('Return')
            abwarten(b'TERMINAL SIZE 53x14\r\n',versatzwertWert)
            virtuellEingabeWerkzeug('mousemove','--window',fenster,'500','45')
            fürBitkarteWarten('remmina-resized.png',[
                ((titelLeiste[0]+447,titelLeiste[1]+279),(39,49,64)),((waagerechtPosition,senkrechtPosition),(24,32,48))])
            if shutil.which('dpkg-query'):
                versionNummer=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versionNummer=subprocess.check_output(['remmina','--version'],env=umgebung,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validierungBericht.update(passed=True,display=umgebung['DISPLAY'],remmina_version=versionNummer,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validierungBericht['passed'] and 'umgebung' in locals() and umgebung.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',umgebung['DISPLAY'],'-window','root',str(ergebnisDaten/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for datenPosition in reversed(laufendProzesse):
                if datenPosition.poll() is None:
                    if datenPosition.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(datenPosition.pid,signal.SIGTERM)
                    else:datenPosition.terminate()
                    try:datenPosition.wait(timeout=5)
                    except subprocess.TimeoutExpired:datenPosition.kill();datenPosition.wait()
            auswähler.close()
            for dateiEintrag in protokolldateiAufzeichnungen:dateiEintrag.close()
            (ergebnisDaten/'serial.log').write_bytes(seriellEinAusgabe)
            (ergebnisDaten/'report.json').write_text(json.dumps(validierungBericht,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ausführenVorgang()
