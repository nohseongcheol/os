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
from ejecutarComando import raízProyecto


def ponerEnMarcha():
    datosResultado=raízProyecto/'build/verification/remmina';datosResultado.mkdir(parents=True,exist_ok=True)
    informeValidación={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as rutaTrabajoEnCurso:
        rutaTrabajoEnCurso=Path(rutaTrabajoEnCurso);procesosEnEjecución=[];selector=selectors.DefaultSelector();entradaSalidaSerie=bytearray()
        registrosDiario=[]
        try:
            presentarVirtual=shutil.which('Xvfb')
            if presentarVirtual: valorServidor=[presentarVirtual]
            else:
                sistemaArchivosRaíz=raízProyecto.parent/'rpi4/build/rootfs'
                valorServidor=['qemu-aarch64','-L',str(sistemaArchivosRaíz),str(sistemaArchivosRaíz/'usr/bin/Xvfb')]
            def ponerEnMarcha(arregloArgumento,entorno=None,**argumentoNombrado):
                registroEntradaDiario=(datosResultado/('process-%d.log'%len(registrosDiario))).open('wb');registrosDiario.append(registroEntradaDiario)
                posiciónDatos=subprocess.Popen(arregloArgumento,env=entorno,stdout=registroEntradaDiario,stderr=subprocess.STDOUT,**argumentoNombrado)
                procesosEnEjecución.append(posiciónDatos);return posiciónDatos
            entorno=dict(os.environ)
            for nombre in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):entorno.pop(nombre,None)
            entorno.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(rutaTrabajoEnCurso/'config'),XDG_DATA_HOME=str(rutaTrabajoEnCurso/'data'),XDG_CACHE_HOME=str(rutaTrabajoEnCurso/'cache'))
            valorNumérico=next(númeroElementosElementoLista for númeroElementosElementoLista in range(80,200) if not Path('/tmp/.X11-unix/X'+str(númeroElementosElementoLista)).exists() and not Path('/tmp/.X%d-lock'%númeroElementosElementoLista).exists())
            entorno['DISPLAY']=':'+str(valorNumérico)
            dispositivoPresentar=ponerEnMarcha(valorServidor+[entorno['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],entorno=entorno)
            tiempoPlazo=time.monotonic()+30
            while True:
                assert dispositivoPresentar.poll() is None and time.monotonic()<tiempoPlazo,'Xvfb failed; see process-0.log'
                terminadoPreparación=subprocess.run(['xdotool','getdisplaygeometry'],env=entorno,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if terminadoPreparación.returncode==0:break
                time.sleep(.1)
            invitado=subprocess.Popen(['python3',str(raízProyecto/'Herramientas/ejecutarComando.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            procesosEnEjecución.append(invitado);selector.register(invitado.stdout,selectors.EVENT_READ)
            def esperarFin(marcador,valorDesfase=0):
                tiempoPlazo=time.monotonic()+45
                while marcador not in entradaSalidaSerie[valorDesfase:]:
                    assert invitado.poll() is None and time.monotonic()<tiempoPlazo,entradaSalidaSerie[valorDesfase:].decode('utf-8','replace')
                    for valorPulsado,_ in selector.select(.1):
                        Datos=valorPulsado.fileobj.read(65536)
                        if Datos:entradaSalidaSerie.extend(Datos)
            esperarFin(b'TERMINAL READY');esperarFin(b'jkoros-native> ',entradaSalidaSerie.rfind(b'TERMINAL READY'))
            númeroPuerto=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',entradaSalidaSerie).group(1))
            perfil=rutaTrabajoEnCurso/'test.remmina'
            perfil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%númeroPuerto)
            ponerEnMarcha(['dbus-run-session','--','remmina','-c',str(perfil)],entorno=entorno,start_new_session=True)
            def herramientaEntradaVirtual(*arregloArgumento):return subprocess.check_output(['xdotool']+list(arregloArgumento),env=entorno,stderr=subprocess.STDOUT)
            tiempoPlazo=time.monotonic()+60;ventana=None
            while time.monotonic()<tiempoPlazo:
                buscarCoincidenciaResultado=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=entorno,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if buscarCoincidenciaResultado.returncode==0:
                    candidato=buscarCoincidenciaResultado.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    enfocado=subprocess.run(['xdotool','windowfocus','--sync',candidato],env=entorno,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if enfocado.returncode==0:ventana=candidato;break
                time.sleep(.1)
            assert ventana,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            herramientaEntradaVirtual('mousemove','--window',ventana,'280','240','click','1')
            time.sleep(1)
            def carácterIngresado(texto):herramientaEntradaVirtual('type','--clearmodifiers','--delay','50',texto)
            def valorPulsado(*teclasPulsado):herramientaEntradaVirtual('key','--clearmodifiers',*teclasPulsado)
            valorDesfase=len(entradaSalidaSerie);carácterIngresado('echo ');valorPulsado('F9');carácterIngresado('dkssudgktpdy gksrmf');valorPulsado('F9','Return')
            esperarFin('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),valorDesfase)
            valorDesfase=len(entradaSalidaSerie);carácterIngresado('echo ');valorPulsado('shift+space');carácterIngresado('rhk rkqtk');valorPulsado('shift+space','Return')
            esperarFin('\r\n과 갑사\r\njkoros-native> '.encode(),valorDesfase)
            valorDesfase=len(entradaSalidaSerie);carácterIngresado('help ko');valorPulsado('Return')
            esperarFin('한/operandoCero valorTecla, Shift+Space 또는 F9'.encode(),valorDesfase);esperarFin(b'jkoros-native> ',valorDesfase)
            valorDesfase=len(entradaSalidaSerie);carácterIngresado('echo ');valorPulsado('F9');carácterIngresado('gksrmf dlfr')
            esperarFin('읽'.encode(),valorDesfase)
            subprocess.check_call(['import','-display',entorno['DISPLAY'],'-window',ventana,str(datosResultado/'remmina-korean.png')])
            valorPulsado('F9','Return')
            esperarFin(b'jkoros-native> ',valorDesfase)
            # datosEfectivo Remmina의 Pantalla 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            Dibujo=Image.open(str(datosResultado/'remmina-korean.png')).convert('RGB')
            barraTítulo=None
            for posiciónVertical in range(Dibujo.height):
                posicionesHorizontal=[posiciónHorizontal for posiciónHorizontal in range(Dibujo.width) if Dibujo.getpixel((posiciónHorizontal,posiciónVertical))==(32,80,144)]
                if len(posicionesHorizontal)>=500:barraTítulo=(min(posicionesHorizontal),posiciónVertical);break
            assert barraTítulo,'native terminal title bar not found'
            posiciónHorizontal,posiciónVertical=barraTítulo[0]+564,barraTítulo[1]+356
            herramientaEntradaVirtual('mousemove','--window',ventana,str(posiciónHorizontal),str(posiciónVertical))
            def esperarMapaBitsPara(nombre,listaPuntos):
                valorPlazo=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',entorno['DISPLAY'],'-window',ventana,str(datosResultado/nombre)])
                    imagenMapaBits=Image.open(str(datosResultado/nombre)).convert('RGB')
                    if all(imagenMapaBits.getpixel(posición)==Color for posición,Color in listaPuntos):return
                    assert time.monotonic()<valorPlazo,'Remmina framebuffer did not settle: '+nombre
                    time.sleep(.1)
            esperarMapaBitsPara('remmina-resize-cursor.png',[
                ((posiciónHorizontal-7,posiciónVertical-7),(255,255,255)),((posiciónHorizontal+7,posiciónVertical+7),(255,255,255))])
            herramientaEntradaVirtual('mousedown','1','mousemove','--window',ventana,str(posiciónHorizontal-120),str(posiciónVertical-80),'mouseup','1')
            time.sleep(.4)
            valorDesfase=len(entradaSalidaSerie);carácterIngresado('terminal size');valorPulsado('Return')
            esperarFin(b'TERMINAL SIZE 53x14\r\n',valorDesfase)
            herramientaEntradaVirtual('mousemove','--window',ventana,'500','45')
            esperarMapaBitsPara('remmina-resized.png',[
                ((barraTítulo[0]+447,barraTítulo[1]+279),(39,49,64)),((posiciónHorizontal,posiciónVertical),(24,32,48))])
            if shutil.which('dpkg-query'):
                númeroVersión=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                númeroVersión=subprocess.check_output(['remmina','--version'],env=entorno,stderr=subprocess.STDOUT).decode('utf-8','replace')
            informeValidación.update(passed=True,display=entorno['DISPLAY'],remmina_version=númeroVersión,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not informeValidación['passed'] and 'entorno' in locals() and entorno.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',entorno['DISPLAY'],'-window','root',str(datosResultado/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for posiciónDatos in reversed(procesosEnEjecución):
                if posiciónDatos.poll() is None:
                    if posiciónDatos.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(posiciónDatos.pid,signal.SIGTERM)
                    else:posiciónDatos.terminate()
                    try:posiciónDatos.wait(timeout=5)
                    except subprocess.TimeoutExpired:posiciónDatos.kill();posiciónDatos.wait()
            selector.close()
            for entradaElementoArchivo in registrosDiario:entradaElementoArchivo.close()
            (datosResultado/'serial.log').write_bytes(entradaSalidaSerie)
            (datosResultado/'report.json').write_text(json.dumps(informeValidación,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ponerEnMarcha()
