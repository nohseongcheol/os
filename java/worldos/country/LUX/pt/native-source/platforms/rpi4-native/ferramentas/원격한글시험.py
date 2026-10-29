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
from Executar_comando import ação_raiz


def iniciar():
    RC_dados=ação_raiz/'build/verification/remmina';RC_dados.mkdir(parents=True,exist_ok=True)
    validação_relatar={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];seletor=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtual_visor=shutil.which('Xvfb')
            if virtual_visor: servidor_VALOR=[virtual_visor]
            else:
                뿌리파일계층=ação_raiz.parent/'rpi4/build/rootfs'
                servidor_VALOR=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def iniciar(argumento_MATRIZ,ambiente=None,**argumento_nomeado):
                LOG_linha=(RC_dados/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_linha)
                dados_cargo=subprocess.Popen(argumento_MATRIZ,env=ambiente,stdout=LOG_linha,stderr=subprocess.STDOUT,**argumento_nomeado)
                실행과정들.append(dados_cargo);return dados_cargo
            ambiente=dict(os.environ)
            for Nome in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):ambiente.pop(Nome,None)
            ambiente.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(item_CONT_NÚM for item_CONT_NÚM in range(80,200) if not Path('/tmp/.X11-unix/X'+str(item_CONT_NÚM)).exists() and not Path('/tmp/.X%d-lock'%item_CONT_NÚM).exists())
            ambiente['DISPLAY']=':'+str(수치)
            visor=iniciar(servidor_VALOR+[ambiente['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],ambiente=ambiente)
            data_limite_time=time.monotonic()+30
            while True:
                assert visor.poll() is None and time.monotonic()<data_limite_time,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=ambiente,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            convidado=subprocess.Popen(['python3',str(ação_raiz/'ferramentas/Executar_comando.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(convidado);seletor.register(convidado.stdout,selectors.EVENT_READ)
            def 기다리기(favorito,DESLOC_VALOR=0):
                data_limite_time=time.monotonic()+45
                while favorito not in 직렬입출력[DESLOC_VALOR:]:
                    assert convidado.poll() is None and time.monotonic()<data_limite_time,직렬입출력[DESLOC_VALOR:].decode('utf-8','replace')
                    for 누름값,_ in seletor.select(.1):
                        dados=누름값.fileobj.read(65536)
                        if dados:직렬입출력.extend(dados)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            número_da_porta=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Perfil=작업경로/'test.remmina'
            Perfil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%número_da_porta)
            iniciar(['dbus-run-session','--','remmina','-c',str(Perfil)],ambiente=ambiente,start_new_session=True)
            def virtual_entrada_ferramenta(*argumento_MATRIZ):return subprocess.check_output(['xdotool']+list(argumento_MATRIZ),env=ambiente,stderr=subprocess.STDOUT)
            data_limite_time=time.monotonic()+60;Janela=None
            while time.monotonic()<data_limite_time:
                busca_RC=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=ambiente,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if busca_RC.returncode==0:
                    candidato=busca_RC.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Destaques=subprocess.run(['xdotool','windowfocus','--sync',candidato],env=ambiente,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Destaques.returncode==0:Janela=candidato;break
                time.sleep(.1)
            assert Janela,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtual_entrada_ferramenta('mousemove','--window',Janela,'280','240','click','1')
            time.sleep(1)
            def 글자입력(texto):virtual_entrada_ferramenta('type','--clearmodifiers','--delay','50',texto)
            def 누름값(*누름열):virtual_entrada_ferramenta('key','--clearmodifiers',*누름열)
            DESLOC_VALOR=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),DESLOC_VALOR)
            DESLOC_VALOR=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),DESLOC_VALOR)
            DESLOC_VALOR=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/zero_operando Chave_VALOR, Shift+Space 또는 F9'.encode(),DESLOC_VALOR);기다리기(b'jkoros-native> ',DESLOC_VALOR)
            DESLOC_VALOR=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),DESLOC_VALOR)
            subprocess.check_call(['import','-display',ambiente['DISPLAY'],'-window',Janela,str(RC_dados/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',DESLOC_VALOR)
            # real_dados Remmina의 tela 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            desenho_VALOR=Image.open(str(RC_dados/'remmina-korean.png')).convert('RGB')
            barra_de_título=None
            for Vertical_cargo in range(desenho_VALOR.height):
                가로들=[가로 for 가로 in range(desenho_VALOR.width) if desenho_VALOR.getpixel((가로,Vertical_cargo))==(32,80,144)]
                if len(가로들)>=500:barra_de_título=(min(가로들),Vertical_cargo);break
            assert barra_de_título,'native terminal title bar not found'
            가로,Vertical_cargo=barra_de_título[0]+564,barra_de_título[1]+356
            virtual_entrada_ferramenta('mousemove','--window',Janela,str(가로),str(Vertical_cargo))
            def 화상기다리기(Nome,점들):
                data_limite_VALOR=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',ambiente['DISPLAY'],'-window',Janela,str(RC_dados/Nome)])
                    bitmap_foto=Image.open(str(RC_dados/Nome)).convert('RGB')
                    if all(bitmap_foto.getpixel(posição)==빛 for posição,빛 in 점들):return
                    assert time.monotonic()<data_limite_VALOR,'Remmina framebuffer did not settle: '+Nome
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Vertical_cargo-7),(255,255,255)),((가로+7,Vertical_cargo+7),(255,255,255))])
            virtual_entrada_ferramenta('mousedown','1','mousemove','--window',Janela,str(가로-120),str(Vertical_cargo-80),'mouseup','1')
            time.sleep(.4)
            DESLOC_VALOR=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',DESLOC_VALOR)
            virtual_entrada_ferramenta('mousemove','--window',Janela,'500','45')
            화상기다리기('remmina-resized.png',[
                ((barra_de_título[0]+447,barra_de_título[1]+279),(39,49,64)),((가로,Vertical_cargo),(24,32,48))])
            if shutil.which('dpkg-query'):
                número_de_versão=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                número_de_versão=subprocess.check_output(['remmina','--version'],env=ambiente,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validação_relatar.update(passed=True,display=ambiente['DISPLAY'],remmina_version=número_de_versão,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validação_relatar['passed'] and 'ambiente' in locals() and ambiente.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',ambiente['DISPLAY'],'-window','root',str(RC_dados/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for dados_cargo in reversed(실행과정들):
                if dados_cargo.poll() is None:
                    if dados_cargo.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(dados_cargo.pid,signal.SIGTERM)
                    else:dados_cargo.terminate()
                    try:dados_cargo.wait(timeout=5)
                    except subprocess.TimeoutExpired:dados_cargo.kill();dados_cargo.wait()
            seletor.close()
            for Arquivo_entrada in 기록들:Arquivo_entrada.close()
            (RC_dados/'serial.log').write_bytes(직렬입출력)
            (RC_dados/'report.json').write_text(json.dumps(validação_relatar,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':iniciar()
