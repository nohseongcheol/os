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
from executar_comando import Project_raíz


def Executar_2():
    medida_datos=Project_raíz/'build/verification/remmina';medida_datos.mkdir(parents=True,exist_ok=True)
    validación_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];준비선택기=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtual_mostrar=shutil.which('Xvfb')
            if virtual_mostrar: servidor_VALOR=[virtual_mostrar]
            else:
                뿌리파일계층=Project_raíz.parent/'rpi4/build/rootfs'
                servidor_VALOR=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Executar_2(argumento_MATRIZ,환경=None,**이름붙인인수):
                LOG_fila=(medida_datos/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_fila)
                datos_cargo=subprocess.Popen(argumento_MATRIZ,env=환경,stdout=LOG_fila,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(datos_cargo);return datos_cargo
            환경=dict(os.environ)
            for Nome in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Nome,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(elemento_CONTAR for elemento_CONTAR in range(80,200) if not Path('/tmp/.X11-unix/X'+str(elemento_CONTAR)).exists() and not Path('/tmp/.X%d-lock'%elemento_CONTAR).exists())
            환경['DISPLAY']=':'+str(수치)
            pantalla=Executar_2(servidor_VALOR+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert pantalla.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            convidado=subprocess.Popen(['python3',str(Project_raíz/'Ferramentas/executar_comando.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(convidado);준비선택기.register(convidado.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,DESPRAZAMENTO_VALOR=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[DESPRAZAMENTO_VALOR:]:
                    assert convidado.poll() is None and time.monotonic()<마감시각,직렬입출력[DESPRAZAMENTO_VALOR:].decode('utf-8','replace')
                    for 누름값,_ in 준비선택기.select(.1):
                        datos=누름값.fileobj.read(65536)
                        if datos:직렬입출력.extend(datos)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            número_do_porto=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Perfil=작업경로/'test.remmina'
            Perfil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%número_do_porto)
            Executar_2(['dbus-run-session','--','remmina','-c',str(Perfil)],환경=환경,start_new_session=True)
            def 가상입력도구(*argumento_MATRIZ):return subprocess.check_output(['xdotool']+list(argumento_MATRIZ),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;Xanela=None
            while time.monotonic()<마감시각:
                ACHAR_medida=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ACHAR_medida.returncode==0:
                    후보=ACHAR_medida.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Importantes=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Importantes.returncode==0:Xanela=후보;break
                time.sleep(.1)
            assert Xanela,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Xanela,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Texto):가상입력도구('type','--clearmodifiers','--delay','50',Texto)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            DESPRAZAMENTO_VALOR=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Chave_VALOR, Shift+Space 또는 F9'.encode(),DESPRAZAMENTO_VALOR);기다리기(b'jkoros-native> ',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),DESPRAZAMENTO_VALOR)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Xanela,str(medida_datos/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',DESPRAZAMENTO_VALOR)
            # real_datos Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            그림=Image.open(str(medida_datos/'remmina-korean.png')).convert('RGB')
            barra_de_título=None
            for Vertical_cargo in range(그림.height):
                가로들=[가로 for 가로 in range(그림.width) if 그림.getpixel((가로,Vertical_cargo))==(32,80,144)]
                if len(가로들)>=500:barra_de_título=(min(가로들),Vertical_cargo);break
            assert barra_de_título,'native terminal title bar not found'
            가로,Vertical_cargo=barra_de_título[0]+564,barra_de_título[1]+356
            가상입력도구('mousemove','--window',Xanela,str(가로),str(Vertical_cargo))
            def 화상기다리기(Nome,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Xanela,str(medida_datos/Nome)])
                    mapa_de_bits_IMAXE=Image.open(str(medida_datos/Nome)).convert('RGB')
                    if all(mapa_de_bits_IMAXE.getpixel(Posición)==빛 for Posición,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Nome
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Vertical_cargo-7),(255,255,255)),((가로+7,Vertical_cargo+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Xanela,str(가로-120),str(Vertical_cargo-80),'mouseup','1')
            time.sleep(.4)
            DESPRAZAMENTO_VALOR=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',DESPRAZAMENTO_VALOR)
            가상입력도구('mousemove','--window',Xanela,'500','45')
            화상기다리기('remmina-resized.png',[
                ((barra_de_título[0]+447,barra_de_título[1]+279),(39,49,64)),((가로,Vertical_cargo),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validación_informe.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validación_informe['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(medida_datos/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for datos_cargo in reversed(실행과정들):
                if datos_cargo.poll() is None:
                    if datos_cargo.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(datos_cargo.pid,signal.SIGTERM)
                    else:datos_cargo.terminate()
                    try:datos_cargo.wait(timeout=5)
                    except subprocess.TimeoutExpired:datos_cargo.kill();datos_cargo.wait()
            준비선택기.close()
            for Ficheiro_introdución in 기록들:Ficheiro_introdución.close()
            (medida_datos/'serial.log').write_bytes(직렬입출력)
            (medida_datos/'report.json').write_text(json.dumps(validación_informe,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Executar_2()
