#!/usr/bin/env python3
"""real_datos OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from executar_comando import Project_raíz, Orde
from Rede_ponte import Rede_ponte


def Executar_2():
    analizador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizador_48ee4b1b.add_argument('--kernel', type=Path, default=Project_raíz / 'build/kernel8.img')
    analizador_48ee4b1b.add_argument('--access', type=Path, default=Project_raíz / 'build/remote/access.json')
    analizador_48ee4b1b.add_argument('--output', type=Path, default=Project_raíz / 'build/verification/native-remote')
    Argumentos = analizador_48ee4b1b.parse_args()
    Saída = Argumentos.output
    Saída.mkdir(parents=True, exist_ok=True)
    Configuración = json.loads(Argumentos.access.read_text())
    informe_VALOR = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumentos.kernel.read_bytes()).hexdigest(), 'checks': []}
    def baleiro_porto():
        with socket.socket() as Conectar:
            Conectar.bind(('127.0.0.5', 0))
            return Conectar.getsockname()[1]
    shell_porto, 화면포트, Ficheiro_porto = baleiro_porto(), baleiro_porto(), baleiro_porto()
    LOG_fila = bytearray()
    Proceso_VALOR = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Rede_ponte(Ficheiro_porto,
                ['tcp:{}:22'.format(shell_porto), 'tcp:{}:5900'.format(화면포트)], hospedar_ENDEREZO='127.0.0.5') as ponte_VALOR:
            실행인수 = Orde()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumentos.kernel.resolve())
            Proceso_VALOR = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ponte_VALOR.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    datos = Proceso_VALOR.stdout.read(4096)
                    if not datos: break
                    LOG_fila.extend(datos)
            tema_VALOR = threading.Thread(target=수집, daemon=True)
            tema_VALOR.start()
            def agarda_Estado(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_fila[처음:]:
                    if time.monotonic()>끝 or Proceso_VALOR.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_fila[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            agarda_Estado(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def seguro_shell(contrasinal_VALOR, instrución_VALOR_4c26ea1b, Anexar_introdución=()):
                환경['JKOROS_TEST_PASSWORD']=contrasinal_VALOR
                Argumentos=['ssh','-v']+list(Anexar_introdución)+['-p',str(shell_porto),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instrución_VALOR_4c26ea1b]
                RESULTANTE=subprocess.run(Argumentos,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return RESULTANTE
            RESULTANTE=seguro_shell('!' + Configuración['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Saída/'ssh-rejected.log').write_bytes(RESULTANTE.stderr)
            assert RESULTANTE.returncode!=0 and b'Permission denied' in RESULTANTE.stderr and b'SHOULD_NOT_RUN' not in LOG_fila, RESULTANTE.stderr
            informe_VALOR['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            RESULTANTE=seguro_shell(Configuración['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Saída/'ssh.log').write_bytes(RESULTANTE.stderr)
            (Saída/'ssh-output.txt').write_bytes(RESULTANTE.stdout)
            assert RESULTANTE.returncode==0 and b'SSH_NATIVE_PASS' in RESULTANTE.stdout, (RESULTANTE.returncode,RESULTANTE.stdout,RESULTANTE.stderr)
            informe_VALOR['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in RESULTANTE.stderr, RESULTANTE.stderr
            informe_VALOR['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            RESULTANTE=seguro_shell(Configuración['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert RESULTANTE.returncode==0 and 'JAVA Saída: 안녕하세요 😀'.encode() in RESULTANTE.stdout,RESULTANTE.stdout
            informe_VALOR['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            RESULTANTE=seguro_shell(Configuración['ssh_password'], 'missing_remote_command')
            assert RESULTANTE.returncode==127,RESULTANTE.returncode
            informe_VALOR['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            RESULTANTE=seguro_shell(Configuración['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Saída/'ssh-rekey.log').write_bytes(RESULTANTE.stderr)
            assert RESULTANTE.returncode==0 and 'class 창예제'.encode() in RESULTANTE.stdout, (RESULTANTE.returncode,RESULTANTE.stdout,RESULTANTE.stderr)
            assert RESULTANTE.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, RESULTANTE.stderr
            informe_VALOR['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(shell_porto),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interactivo_sesión=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();selección_VALOR=selectors.DefaultSelector();selección_VALOR.register(interactivo_sesión.stdout,selectors.EVENT_READ)
            def 대화읽기(mostrar_VALOR):
                마감=time.monotonic()+30
                while mostrar_VALOR not in 대화기록:
                    if time.monotonic()>마감 or interactivo_sesión.poll() is not None:raise AssertionError('SSH interactive missing '+repr(mostrar_VALOR)+' '+repr(bytes(대화기록)))
                    for introdución_VALOR,_ in selección_VALOR.select(.1):
                        조각=introdución_VALOR.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                interactivo_sesión.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interactivo_sesión.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interactivo_sesión.stdin.write(b'\x04');interactivo_sesión.stdin.flush();나머지,ERRO=interactivo_sesión.communicate(timeout=15)
                assert interactivo_sesión.returncode==0 and b'PTY allocation request failed' not in ERRO,(interactivo_sesión.returncode,ERRO)
                (Saída/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                selección_VALOR.close()
                if interactivo_sesión.poll() is None:interactivo_sesión.kill();interactivo_sesión.wait()
            informe_VALOR['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Conectar, 수):
                datos=bytearray()
                while len(datos)<수:
                    덩이=Conectar.recv(수-len(datos))
                    if not 덩이: raise AssertionError('RFB EOF')
                    datos.extend(덩이)
                return bytes(datos)
            def 화면인증(contrasinal_VALOR):
                Conectar=socket.create_connection(('127.0.0.5',화면포트),10);Conectar.settimeout(30)
                assert 정확히(Conectar,12)==b'RFB 003.008\n'
                Conectar.sendall(b'RFB 003.008\n');assert 정확히(Conectar,2)==b'\x01\x02'
                Conectar.sendall(b'\x02');desafío_VALOR=정확히(Conectar,16)
                입력암호=contrasinal_VALOR.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Conectar.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(desafío_VALOR))
                Estado_VALOR=struct.unpack('!I',정확히(Conectar,4))[0]
                return Conectar,Estado_VALOR
            non_válido_contrasinal='!' if not Configuración['vnc_password'].startswith('!') else '?'
            Conectar,Estado_VALOR=화면인증(non_válido_contrasinal);assert Estado_VALOR==1;Conectar.close();time.sleep(.6)
            informe_VALOR['checks'].append('VNC incorrect password rejected')
            Conectar,Estado_VALOR=화면인증(Configuración['vnc_password']);assert Estado_VALOR==0
            with Conectar:
                Conectar.sendall(b'\x01');초기=정확히(Conectar,24);너비,높이=struct.unpack('!HH',초기[:4]);Nome=정확히(Conectar,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Nome
                def 화면(증분=0):
                    Conectar.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Conectar,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    그림=bytearray(너비*높이*4)
                    for _ in range(수):
                        X_coordenada,Y_coordenada,영역너비,영역높이,방식=struct.unpack('!HHHHi',정확히(Conectar,12));assert 방식==0 and X_coordenada+영역너비<=너비 and Y_coordenada+영역높이<=높이
                        píxel=정확히(Conectar,영역너비*영역높이*4);합계+=len(píxel)
                        for Liña in range(영역높이):그림[((Y_coordenada+Liña)*너비+X_coordenada)*4:((Y_coordenada+Liña)*너비+X_coordenada+영역너비)*4]=píxel[Liña*영역너비*4:(Liña+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(그림),'raw','BGRX').save(str(Saída/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                informe_VALOR['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                informe_VALOR['checks'].append('RFB incremental update')
                처음=len(LOG_fila)
                for carácter_VALOR in 'echo VNC_NATIVE_PASS\r':
                    símbolo=0xff0d if carácter_VALOR=='\r' else ord(carácter_VALOR)
                    Conectar.sendall(struct.pack('!BBHI',4,1,0,símbolo));Conectar.sendall(struct.pack('!BBHI',4,0,0,símbolo))
                agarda_Estado(b'VNC_NATIVE_PASS',처음)
                informe_VALOR['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(símbolo,pulsar_VALOR=1):Conectar.sendall(struct.pack('!BBHI',4,pulsar_VALOR,0,símbolo))
                처음=len(LOG_fila)
                for carácter_VALOR in 'echo ':글쇠(ord(carácter_VALOR))
                글쇠(0xffc6)
                for carácter_VALOR in 'gksrmf':글쇠(ord(carácter_VALOR))
                글쇠(0xffc6);글쇠(0xff0d)
                agarda_Estado('\r\n한글\r\n'.encode(),처음)
                informe_VALOR['checks'].append('Native VNC F9 two-set Hangul composition')
                Conectar.sendall(struct.pack('!BBHH',5,0,120,100))
                informe_VALOR['checks'].append('VNC pointer input accepted')
            Proceso_VALOR.stdin.write(b'poweroff\n');Proceso_VALOR.stdin.flush();Proceso_VALOR.wait(timeout=15);assert Proceso_VALOR.returncode==0
            informe_VALOR['passed']=True
    finally:
        if Proceso_VALOR and Proceso_VALOR.poll() is None:
            Proceso_VALOR.terminate()
            try: Proceso_VALOR.wait(timeout=5)
            except subprocess.TimeoutExpired: Proceso_VALOR.kill();Proceso_VALOR.wait()
        (Saída/'serial.log').write_bytes(LOG_fila)
        (Saída/'report.json').write_text(json.dumps(informe_VALOR,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(informe_VALOR,ensure_ascii=False,indent=2))


if __name__=='__main__': Executar_2()
