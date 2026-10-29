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
from Executa_ordre import Project_rel


def Executa_2():
    mesura_dades=Project_rel/'build/verification/remmina';mesura_dades.mkdir(parents=True,exist_ok=True)
    validació_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];준비선택기=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtual_mostrar=shutil.which('Xvfb')
            if virtual_mostrar: servidor_VALOR=[virtual_mostrar]
            else:
                뿌리파일계층=Project_rel.parent/'rpi4/build/rootfs'
                servidor_VALOR=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Executa_2(arg_MATRIU,entorn=None,**이름붙인인수):
                LOG_fila=(mesura_dades/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_fila)
                dades_càrrec=subprocess.Popen(arg_MATRIU,env=entorn,stdout=LOG_fila,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(dades_càrrec);return dades_càrrec
            entorn=dict(os.environ)
            for Nom in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):entorn.pop(Nom,None)
            entorn.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(element_COMPT for element_COMPT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(element_COMPT)).exists() and not Path('/tmp/.X%d-lock'%element_COMPT).exists())
            entorn['DISPLAY']=':'+str(수치)
            pantalla=Executa_2(servidor_VALOR+[entorn['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],entorn=entorn)
            마감시각=time.monotonic()+30
            while True:
                assert pantalla.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=entorn,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            convidat=subprocess.Popen(['python3',str(Project_rel/'Eines/Executa_ordre.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(convidat);준비선택기.register(convidat.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,DESPLAÇAMENT_VALOR=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[DESPLAÇAMENT_VALOR:]:
                    assert convidat.poll() is None and time.monotonic()<마감시각,직렬입출력[DESPLAÇAMENT_VALOR:].decode('utf-8','replace')
                    for 누름값,_ in 준비선택기.select(.1):
                        dades=누름값.fileobj.read(65536)
                        if dades:직렬입출력.extend(dades)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            número_de_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Perfil=작업경로/'test.remmina'
            Perfil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%número_de_port)
            Executa_2(['dbus-run-session','--','remmina','-c',str(Perfil)],entorn=entorn,start_new_session=True)
            def 가상입력도구(*arg_MATRIU):return subprocess.check_output(['xdotool']+list(arg_MATRIU),env=entorn,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;Finestra=None
            while time.monotonic()<마감시각:
                Cerca_mesura=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=entorn,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Cerca_mesura.returncode==0:
                    후보=Cerca_mesura.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Prioritaris=subprocess.run(['xdotool','windowfocus','--sync',후보],env=entorn,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Prioritaris.returncode==0:Finestra=후보;break
                time.sleep(.1)
            assert Finestra,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Finestra,'280','240','click','1')
            time.sleep(1)
            def 글자입력(SMS):가상입력도구('type','--clearmodifiers','--delay','50',SMS)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            DESPLAÇAMENT_VALOR=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Clau_VALOR, Shift+Space 또는 F9'.encode(),DESPLAÇAMENT_VALOR);기다리기(b'jkoros-native> ',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),DESPLAÇAMENT_VALOR)
            subprocess.check_call(['import','-display',entorn['DISPLAY'],'-window',Finestra,str(mesura_dades/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',DESPLAÇAMENT_VALOR)
            # real_dades Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            dibuix_VALOR=Image.open(str(mesura_dades/'remmina-korean.png')).convert('RGB')
            barra_de_títol=None
            for Vertical_càrrec in range(dibuix_VALOR.height):
                가로들=[가로 for 가로 in range(dibuix_VALOR.width) if dibuix_VALOR.getpixel((가로,Vertical_càrrec))==(32,80,144)]
                if len(가로들)>=500:barra_de_títol=(min(가로들),Vertical_càrrec);break
            assert barra_de_títol,'native terminal title bar not found'
            가로,Vertical_càrrec=barra_de_títol[0]+564,barra_de_títol[1]+356
            가상입력도구('mousemove','--window',Finestra,str(가로),str(Vertical_càrrec))
            def 화상기다리기(Nom,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',entorn['DISPLAY'],'-window',Finestra,str(mesura_dades/Nom)])
                    mapa_de_bits_IMATGE=Image.open(str(mesura_dades/Nom)).convert('RGB')
                    if all(mapa_de_bits_IMATGE.getpixel(Posició)==빛 for Posició,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Nom
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Vertical_càrrec-7),(255,255,255)),((가로+7,Vertical_càrrec+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Finestra,str(가로-120),str(Vertical_càrrec-80),'mouseup','1')
            time.sleep(.4)
            DESPLAÇAMENT_VALOR=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',DESPLAÇAMENT_VALOR)
            가상입력도구('mousemove','--window',Finestra,'500','45')
            화상기다리기('remmina-resized.png',[
                ((barra_de_títol[0]+447,barra_de_títol[1]+279),(39,49,64)),((가로,Vertical_càrrec),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=entorn,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validació_informe.update(passed=True,display=entorn['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validació_informe['passed'] and 'entorn' in locals() and entorn.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',entorn['DISPLAY'],'-window','root',str(mesura_dades/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for dades_càrrec in reversed(실행과정들):
                if dades_càrrec.poll() is None:
                    if dades_càrrec.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(dades_càrrec.pid,signal.SIGTERM)
                    else:dades_càrrec.terminate()
                    try:dades_càrrec.wait(timeout=5)
                    except subprocess.TimeoutExpired:dades_càrrec.kill();dades_càrrec.wait()
            준비선택기.close()
            for arxiu_introducció in 기록들:arxiu_introducció.close()
            (mesura_dades/'serial.log').write_bytes(직렬입출력)
            (mesura_dades/'report.json').write_text(json.dumps(validació_informe,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Executa_2()
