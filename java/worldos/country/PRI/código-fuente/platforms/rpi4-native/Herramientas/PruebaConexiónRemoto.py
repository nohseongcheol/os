#!/usr/bin/env python3
"""datosEfectivo OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import selectors
from Crypto.Cipher import DES
from ejecutarComando import raízProyecto, comando
from puenteRed import puenteRed


def ponerEnMarcha():
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('--kernel', type=Path, default=raízProyecto / 'build/kernel8.img')
    Analizador.add_argument('--access', type=Path, default=raízProyecto / 'build/remote/access.json')
    Analizador.add_argument('--output', type=Path, default=raízProyecto / 'build/verification/native-remote')
    argumentos = Analizador.parse_args()
    Salida = argumentos.output
    Salida.mkdir(parents=True, exist_ok=True)
    ajustes = json.loads(argumentos.access.read_text())
    valorInforme = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argumentos.kernel.read_bytes()).hexdigest(), 'checks': []}
    def puertoVacíoEstado():
        with socket.socket() as conectar:
            conectar.bind(('127.0.0.5', 0))
            return conectar.getsockname()[1]
    puertoIntérpreteComandos, puertoPantalla, puertoArchivo = puertoVacíoEstado(), puertoVacíoEstado(), puertoVacíoEstado()
    registroEntradaDiario = bytearray()
    valorProceso = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as valorTemporal, puenteRed(puertoArchivo,
                ['tcp:{}:22'.format(puertoIntérpreteComandos), 'tcp:{}:5900'.format(puertoPantalla)], direcciónAnfitrión='127.0.0.5') as valorPuente:
            Argumentos = comando()
            Argumentos[Argumentos.index('-kernel') + 1] = str(argumentos.kernel.resolve())
            valorProceso = subprocess.Popen(Argumentos + ['-display','none','-monitor','none','-serial','stdio'] + valorPuente.argumentoReenviado(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def reunirValores():
                while True:
                    Datos = valorProceso.stdout.read(4096)
                    if not Datos: break
                    registroEntradaDiario.extend(Datos)
            valorHiloEjecución = threading.Thread(target=reunirValores, daemon=True)
            valorHiloEjecución.start()
            def esperarEstadoValor(textoPalabra, elementoListaInicialValor=0, valorLímite=60):
                terminación = time.monotonic() + valorLímite
                while textoPalabra not in registroEntradaDiario[elementoListaInicialValor:]:
                    if time.monotonic()>terminación or valorProceso.poll() is not None:
                        raise AssertionError('Missing '+repr(textoPalabra)+'\n'+registroEntradaDiario[elementoListaInicialValor:].decode('utf-8','replace'))
                    time.sleep(.02)
            esperarEstadoValor(b'jkoros-native> ')
            valorAyudante = Path(valorTemporal)/'askpass'
            valorAyudante.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            valorAyudante.chmod(0o700)
            entorno = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(valorAyudante), SSH_ASKPASS_REQUIRE='force')
            def intérpreteComandosAsegurar(valorContraseña, valorInstrucciónMáquina, añadirFinalEntradaElemento=()):
                entorno['JKOROS_TEST_PASSWORD']=valorContraseña
                argumentos=['ssh','-v']+list(añadirFinalEntradaElemento)+['-p',str(puertoIntérpreteComandos),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(valorTemporal)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',valorInstrucciónMáquina]
                resultado=subprocess.run(argumentos,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=entorno,start_new_session=True,timeout=50)
                return resultado
            resultado=intérpreteComandosAsegurar('!' + ajustes['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Salida/'ssh-rejected.log').write_bytes(resultado.stderr)
            assert resultado.returncode!=0 and b'Permission denied' in resultado.stderr and b'SHOULD_NOT_RUN' not in registroEntradaDiario, resultado.stderr
            valorInforme['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            resultado=intérpreteComandosAsegurar(ajustes['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Salida/'ssh.log').write_bytes(resultado.stderr)
            (Salida/'ssh-output.txt').write_bytes(resultado.stdout)
            assert resultado.returncode==0 and b'SSH_NATIVE_PASS' in resultado.stdout, (resultado.returncode,resultado.stdout,resultado.stderr)
            valorInforme['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in resultado.stderr, resultado.stderr
            valorInforme['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            resultado=intérpreteComandosAsegurar(ajustes['ssh_password'], 'cd /example/java; java EjemploSalida; cd /')
            assert resultado.returncode==0 and 'JAVA Salida: 안녕하세요 😀'.encode() in resultado.stdout,resultado.stdout
            valorInforme['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            resultado=intérpreteComandosAsegurar(ajustes['ssh_password'], 'missing_remote_command')
            assert resultado.returncode==127,resultado.returncode
            valorInforme['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            resultado=intérpreteComandosAsegurar(ajustes['ssh_password'], 'cat /example/java/EjemploVentana.java', ('-o', 'RekeyLimit=1K'))
            (Salida/'ssh-rekey.log').write_bytes(resultado.stderr)
            assert resultado.returncode==0 and 'class EjemploVentana'.encode() in resultado.stdout, (resultado.returncode,resultado.stdout,resultado.stderr)
            assert resultado.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, resultado.stderr
            valorInforme['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            argumentosInteractivo=['ssh','-tt','-p',str(puertoIntérpreteComandos),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(valorTemporal)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            sesiónInteractivo=subprocess.Popen(argumentosInteractivo,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=entorno,start_new_session=True,bufsize=0)
            transcripción=bytearray();valorSelección=selectors.DefaultSelector();valorSelección.register(sesiónInteractivo.stdout,selectors.EVENT_READ)
            def leerInteractivo(mostrarValor):
                valorPlazo=time.monotonic()+30
                while mostrarValor not in transcripción:
                    if time.monotonic()>valorPlazo or sesiónInteractivo.poll() is not None:raise AssertionError('SSH interactive missing '+repr(mostrarValor)+' '+repr(bytes(transcripción)))
                    for valorEntradaElemento,_ in valorSelección.select(.1):
                        valorFragmento=valorEntradaElemento.fileobj.read(4096)
                        if valorFragmento:transcripción.extend(valorFragmento)
            try:
                leerInteractivo(b'shared native console')
                sesiónInteractivo.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');sesiónInteractivo.stdin.flush();leerInteractivo(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                sesiónInteractivo.stdin.write(b'\x04');sesiónInteractivo.stdin.flush();valorRestoDivisión,error=sesiónInteractivo.communicate(timeout=15)
                assert sesiónInteractivo.returncode==0 and b'PTY allocation request failed' not in error,(sesiónInteractivo.returncode,error)
                (Salida/'ssh-interactive.txt').write_bytes(transcripción+valorRestoDivisión)
            finally:
                valorSelección.close()
                if sesiónInteractivo.poll() is None:sesiónInteractivo.kill();sesiónInteractivo.wait()
            valorInforme['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def valorExactamente(conectar, númeroValor):
                Datos=bytearray()
                while len(Datos)<númeroValor:
                    valorFragmentoBloque=conectar.recv(númeroValor-len(Datos))
                    if not valorFragmentoBloque: raise AssertionError('RFB EOF')
                    Datos.extend(valorFragmentoBloque)
                return bytes(Datos)
            def autenticaciónPantalla(valorContraseña):
                conectar=socket.create_connection(('127.0.0.5',puertoPantalla),10);conectar.settimeout(30)
                assert valorExactamente(conectar,12)==b'RFB 003.008\n'
                conectar.sendall(b'RFB 003.008\n');assert valorExactamente(conectar,2)==b'\x01\x02'
                conectar.sendall(b'\x02');valorDesafío=valorExactamente(conectar,16)
                contraseñaEntrada=valorContraseña.encode('ascii')[:8].ljust(8, b'\0')
                materialTecla=bytes(int('{:08b}'.format(númeroValor)[::-1],2) for númeroValor in contraseñaEntrada)
                conectar.sendall(DES.new(materialTecla,DES.MODE_ECB).encrypt(valorDesafío))
                valorEstadoValor=struct.unpack('!I',valorExactamente(conectar,4))[0]
                return conectar,valorEstadoValor
            contraseñaInválido='!' if not ajustes['vnc_password'].startswith('!') else '?'
            conectar,valorEstadoValor=autenticaciónPantalla(contraseñaInválido);assert valorEstadoValor==1;conectar.close();time.sleep(.6)
            valorInforme['checks'].append('VNC incorrect password rejected')
            conectar,valorEstadoValor=autenticaciónPantalla(ajustes['vnc_password']);assert valorEstadoValor==0
            with conectar:
                conectar.sendall(b'\x01');estadoValorInicialValor=valorExactamente(conectar,24);valorAnchura,valorAltura=struct.unpack('!HH',estadoValorInicialValor[:4]);nombre=valorExactamente(conectar,struct.unpack('!I',estadoValorInicialValor[20:24])[0])
                assert (valorAnchura,valorAltura)==(640,480) and b'jkoros native'==nombre
                def Pantalla(pasoUnidadIncremento=0):
                    conectar.sendall(struct.pack('!BBHHHH',3,pasoUnidadIncremento,0,0,valorAnchura,valorAltura));valorCabecera=valorExactamente(conectar,4);númeroValor=struct.unpack('!H',valorCabecera[2:])[0];valorTotal=0
                    Dibujo=bytearray(valorAnchura*valorAltura*4)
                    for _ in range(númeroValor):
                        coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,anchuraRegión,alturaRegión,modoMétodo=struct.unpack('!HHHHi',valorExactamente(conectar,12));assert modoMétodo==0 and coordenadaCoordenadaHorizontal+anchuraRegión<=valorAnchura and coordenadaCoordenadaVertical+alturaRegión<=valorAltura
                        píxel=valorExactamente(conectar,anchuraRegión*alturaRegión*4);valorTotal+=len(píxel)
                        for línea in range(alturaRegión):Dibujo[((coordenadaCoordenadaVertical+línea)*valorAnchura+coordenadaCoordenadaHorizontal)*4:((coordenadaCoordenadaVertical+línea)*valorAnchura+coordenadaCoordenadaHorizontal+anchuraRegión)*4]=píxel[línea*anchuraRegión*4:(línea+1)*anchuraRegión*4]
                    if not pasoUnidadIncremento:
                        from PIL import Image
                        Image.frombytes('RGB',(valorAnchura,valorAltura),bytes(Dibujo),'raw','BGRX').save(str(Salida/'native-vnc.png'))
                    return númeroValor,valorTotal
                númeroValor,valorTotal=Pantalla();assert númeroValor>0 and valorTotal==valorAnchura*valorAltura*4
                valorInforme['checks'].append('Native framebuffer RFB full update {} bytes'.format(valorTotal))
                númeroValor,valorTotal=Pantalla(1);assert valorTotal<valorAnchura*valorAltura*4
                valorInforme['checks'].append('RFB incremental update')
                elementoListaInicialValor=len(registroEntradaDiario)
                for valorCarácter in 'echo VNC_NATIVE_PASS\r':
                    símbolo=0xff0d if valorCarácter=='\r' else ord(valorCarácter)
                    conectar.sendall(struct.pack('!BBHI',4,1,0,símbolo));conectar.sendall(struct.pack('!BBHI',4,0,0,símbolo))
                esperarEstadoValor(b'VNC_NATIVE_PASS',elementoListaInicialValor)
                valorInforme['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def trazoTecla(símbolo,valorPulsar=1):conectar.sendall(struct.pack('!BBHI',4,valorPulsar,0,símbolo))
                elementoListaInicialValor=len(registroEntradaDiario)
                for valorCarácter in 'echo ':trazoTecla(ord(valorCarácter))
                trazoTecla(0xffc6)
                for valorCarácter in 'gksrmf':trazoTecla(ord(valorCarácter))
                trazoTecla(0xffc6);trazoTecla(0xff0d)
                esperarEstadoValor('\r\n한글\r\n'.encode(),elementoListaInicialValor)
                valorInforme['checks'].append('Native VNC F9 two-set Hangul composition')
                conectar.sendall(struct.pack('!BBHH',5,0,120,100))
                valorInforme['checks'].append('VNC pointer input accepted')
            valorProceso.stdin.write(b'poweroff\n');valorProceso.stdin.flush();valorProceso.wait(timeout=15);assert valorProceso.returncode==0
            valorInforme['passed']=True
    finally:
        if valorProceso and valorProceso.poll() is None:
            valorProceso.terminate()
            try: valorProceso.wait(timeout=5)
            except subprocess.TimeoutExpired: valorProceso.kill();valorProceso.wait()
        (Salida/'serial.log').write_bytes(registroEntradaDiario)
        (Salida/'report.json').write_text(json.dumps(valorInforme,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(valorInforme,ensure_ascii=False,indent=2))


if __name__=='__main__': ponerEnMarcha()
