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
from Esegui_comando import azione_radice


def avvia():
    KR_dati=azione_radice/'build/verification/remmina';KR_dati.mkdir(parents=True,exist_ok=True)
    convalida_Report={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];selettore=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuale_display=shutil.which('Xvfb')
            if virtuale_display: server_VALORE=[virtuale_display]
            else:
                뿌리파일계층=azione_radice.parent/'rpi4/build/rootfs'
                server_VALORE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def avvia(argomento_array,ambiente=None,**argomento_predefinito):
                LOG_riga=(KR_dati/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_riga)
                dati_funzione=subprocess.Popen(argomento_array,env=ambiente,stdout=LOG_riga,stderr=subprocess.STDOUT,**argomento_predefinito)
                실행과정들.append(dati_funzione);return dati_funzione
            ambiente=dict(os.environ)
            for Nome in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):ambiente.pop(Nome,None)
            ambiente.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(articolo_CONTA_NUMERI for articolo_CONTA_NUMERI in range(80,200) if not Path('/tmp/.X11-unix/X'+str(articolo_CONTA_NUMERI)).exists() and not Path('/tmp/.X%d-lock'%articolo_CONTA_NUMERI).exists())
            ambiente['DISPLAY']=':'+str(수치)
            display=avvia(server_VALORE+[ambiente['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],ambiente=ambiente)
            scadenza_time=time.monotonic()+30
            while True:
                assert display.poll() is None and time.monotonic()<scadenza_time,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=ambiente,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            guest=subprocess.Popen(['python3',str(azione_radice/'strumenti/Esegui_comando.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(guest);selettore.register(guest.stdout,selectors.EVENT_READ)
            def 기다리기(marcatore,SCARTO_VALORE=0):
                scadenza_time=time.monotonic()+45
                while marcatore not in 직렬입출력[SCARTO_VALORE:]:
                    assert guest.poll() is None and time.monotonic()<scadenza_time,직렬입출력[SCARTO_VALORE:].decode('utf-8','replace')
                    for 누름값,_ in selettore.select(.1):
                        dati=누름값.fileobj.read(65536)
                        if dati:직렬입출력.extend(dati)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            numero_di_porta=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profilo=작업경로/'test.remmina'
            Profilo.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%numero_di_porta)
            avvia(['dbus-run-session','--','remmina','-c',str(Profilo)],ambiente=ambiente,start_new_session=True)
            def virtuale_input_strumento(*argomento_array):return subprocess.check_output(['xdotool']+list(argomento_array),env=ambiente,stderr=subprocess.STDOUT)
            scadenza_time=time.monotonic()+60;Finestra=None
            while time.monotonic()<scadenza_time:
                Cerca_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=ambiente,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Cerca_KR.returncode==0:
                    candidato=Cerca_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Evidenziata=subprocess.run(['xdotool','windowfocus','--sync',candidato],env=ambiente,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Evidenziata.returncode==0:Finestra=candidato;break
                time.sleep(.1)
            assert Finestra,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtuale_input_strumento('mousemove','--window',Finestra,'280','240','click','1')
            time.sleep(1)
            def 글자입력(testo):virtuale_input_strumento('type','--clearmodifiers','--delay','50',testo)
            def 누름값(*누름열):virtuale_input_strumento('key','--clearmodifiers',*누름열)
            SCARTO_VALORE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),SCARTO_VALORE)
            SCARTO_VALORE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),SCARTO_VALORE)
            SCARTO_VALORE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/zero_operando tasto_VALORE, Shift+Space 또는 F9'.encode(),SCARTO_VALORE);기다리기(b'jkoros-native> ',SCARTO_VALORE)
            SCARTO_VALORE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),SCARTO_VALORE)
            subprocess.check_call(['import','-display',ambiente['DISPLAY'],'-window',Finestra,str(KR_dati/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',SCARTO_VALORE)
            # effettivo_dati Remmina의 schermata 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            disegno_VALORE=Image.open(str(KR_dati/'remmina-korean.png')).convert('RGB')
            barra_del_titolo=None
            for Verticale_funzione in range(disegno_VALORE.height):
                가로들=[가로 for 가로 in range(disegno_VALORE.width) if disegno_VALORE.getpixel((가로,Verticale_funzione))==(32,80,144)]
                if len(가로들)>=500:barra_del_titolo=(min(가로들),Verticale_funzione);break
            assert barra_del_titolo,'native terminal title bar not found'
            가로,Verticale_funzione=barra_del_titolo[0]+564,barra_del_titolo[1]+356
            virtuale_input_strumento('mousemove','--window',Finestra,str(가로),str(Verticale_funzione))
            def 화상기다리기(Nome,점들):
                scadenza_VALORE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',ambiente['DISPLAY'],'-window',Finestra,str(KR_dati/Nome)])
                    bitmap_foto=Image.open(str(KR_dati/Nome)).convert('RGB')
                    if all(bitmap_foto.getpixel(posizione)==빛 for posizione,빛 in 점들):return
                    assert time.monotonic()<scadenza_VALORE,'Remmina framebuffer did not settle: '+Nome
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Verticale_funzione-7),(255,255,255)),((가로+7,Verticale_funzione+7),(255,255,255))])
            virtuale_input_strumento('mousedown','1','mousemove','--window',Finestra,str(가로-120),str(Verticale_funzione-80),'mouseup','1')
            time.sleep(.4)
            SCARTO_VALORE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',SCARTO_VALORE)
            virtuale_input_strumento('mousemove','--window',Finestra,'500','45')
            화상기다리기('remmina-resized.png',[
                ((barra_del_titolo[0]+447,barra_del_titolo[1]+279),(39,49,64)),((가로,Verticale_funzione),(24,32,48))])
            if shutil.which('dpkg-query'):
                numero_di_versione=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                numero_di_versione=subprocess.check_output(['remmina','--version'],env=ambiente,stderr=subprocess.STDOUT).decode('utf-8','replace')
            convalida_Report.update(passed=True,display=ambiente['DISPLAY'],remmina_version=numero_di_versione,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not convalida_Report['passed'] and 'ambiente' in locals() and ambiente.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',ambiente['DISPLAY'],'-window','root',str(KR_dati/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for dati_funzione in reversed(실행과정들):
                if dati_funzione.poll() is None:
                    if dati_funzione.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(dati_funzione.pid,signal.SIGTERM)
                    else:dati_funzione.terminate()
                    try:dati_funzione.wait(timeout=5)
                    except subprocess.TimeoutExpired:dati_funzione.kill();dati_funzione.wait()
            selettore.close()
            for File_voce in 기록들:File_voce.close()
            (KR_dati/'serial.log').write_bytes(직렬입출력)
            (KR_dati/'report.json').write_text(json.dumps(convalida_Report,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':avvia()
