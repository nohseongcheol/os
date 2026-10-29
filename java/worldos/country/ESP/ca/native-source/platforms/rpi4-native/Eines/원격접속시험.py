#!/usr/bin/env python3
"""real_dades OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Executa_ordre import Project_rel, Ordre
from xarxa_pont import xarxa_pont


def Executa_2():
    analitzador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analitzador_48ee4b1b.add_argument('--kernel', type=Path, default=Project_rel / 'build/kernel8.img')
    analitzador_48ee4b1b.add_argument('--access', type=Path, default=Project_rel / 'build/remote/access.json')
    analitzador_48ee4b1b.add_argument('--output', type=Path, default=Project_rel / 'build/verification/native-remote')
    인수 = analitzador_48ee4b1b.parse_args()
    Sortida = 인수.output
    Sortida.mkdir(parents=True, exist_ok=True)
    Ajusts = json.loads(인수.access.read_text())
    informe_VALOR = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Connecta:
            Connecta.bind(('127.0.0.5', 0))
            return Connecta.getsockname()[1]
    shell_port, 화면포트, arxiu_port = 빈포트(), 빈포트(), 빈포트()
    LOG_fila = bytearray()
    Procés_VALOR = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, xarxa_pont(arxiu_port,
                ['tcp:{}:22'.format(shell_port), 'tcp:{}:5900'.format(화면포트)], allotjar_ADREÇA='127.0.0.5') as pont_VALOR:
            실행인수 = Ordre()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Procés_VALOR = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + pont_VALOR.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    dades = Procés_VALOR.stdout.read(4096)
                    if not dades: break
                    LOG_fila.extend(dades)
            fil_VALOR = threading.Thread(target=수집, daemon=True)
            fil_VALOR.start()
            def Espera_Estat(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_fila[처음:]:
                    if time.monotonic()>끝 or Procés_VALOR.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_fila[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            Espera_Estat(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            entorn = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def segur_shell(contrasenya_VALOR, instrucció_VALOR_4c26ea1b, Annexa_introducció=()):
                entorn['JKOROS_TEST_PASSWORD']=contrasenya_VALOR
                인수=['ssh','-v']+list(Annexa_introducció)+['-p',str(shell_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instrucció_VALOR_4c26ea1b]
                RESULTAT=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=entorn,start_new_session=True,timeout=50)
                return RESULTAT
            RESULTAT=segur_shell('!' + Ajusts['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Sortida/'ssh-rejected.log').write_bytes(RESULTAT.stderr)
            assert RESULTAT.returncode!=0 and b'Permission denied' in RESULTAT.stderr and b'SHOULD_NOT_RUN' not in LOG_fila, RESULTAT.stderr
            informe_VALOR['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            RESULTAT=segur_shell(Ajusts['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Sortida/'ssh.log').write_bytes(RESULTAT.stderr)
            (Sortida/'ssh-output.txt').write_bytes(RESULTAT.stdout)
            assert RESULTAT.returncode==0 and b'SSH_NATIVE_PASS' in RESULTAT.stdout, (RESULTAT.returncode,RESULTAT.stdout,RESULTAT.stderr)
            informe_VALOR['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in RESULTAT.stderr, RESULTAT.stderr
            informe_VALOR['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            RESULTAT=segur_shell(Ajusts['ssh_password'], 'cd /example/java; java ExempleSortida; cd /')
            assert RESULTAT.returncode==0 and 'JAVA Sortida: 안녕하세요 😀'.encode() in RESULTAT.stdout,RESULTAT.stdout
            informe_VALOR['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            RESULTAT=segur_shell(Ajusts['ssh_password'], 'missing_remote_command')
            assert RESULTAT.returncode==127,RESULTAT.returncode
            informe_VALOR['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            RESULTAT=segur_shell(Ajusts['ssh_password'], 'cat /example/java/ExempleFinestra.java', ('-o', 'RekeyLimit=1K'))
            (Sortida/'ssh-rekey.log').write_bytes(RESULTAT.stderr)
            assert RESULTAT.returncode==0 and 'class ExempleFinestra'.encode() in RESULTAT.stdout, (RESULTAT.returncode,RESULTAT.stdout,RESULTAT.stderr)
            assert RESULTAT.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, RESULTAT.stderr
            informe_VALOR['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(shell_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interactiu_sessió=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=entorn,start_new_session=True,bufsize=0)
            대화기록=bytearray();selecció_VALOR=selectors.DefaultSelector();selecció_VALOR.register(interactiu_sessió.stdout,selectors.EVENT_READ)
            def tancar_interactiu(mostrar_VALOR):
                마감=time.monotonic()+30
                while mostrar_VALOR not in 대화기록:
                    if time.monotonic()>마감 or interactiu_sessió.poll() is not None:raise AssertionError('SSH interactive missing '+repr(mostrar_VALOR)+' '+repr(bytes(대화기록)))
                    for introducció_VALOR,_ in selecció_VALOR.select(.1):
                        조각=introducció_VALOR.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                tancar_interactiu(b'shared native console')
                interactiu_sessió.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interactiu_sessió.stdin.flush();tancar_interactiu(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interactiu_sessió.stdin.write(b'\x04');interactiu_sessió.stdin.flush();나머지,s_ha_produït_un_error=interactiu_sessió.communicate(timeout=15)
                assert interactiu_sessió.returncode==0 and b'PTY allocation request failed' not in s_ha_produït_un_error,(interactiu_sessió.returncode,s_ha_produït_un_error)
                (Sortida/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                selecció_VALOR.close()
                if interactiu_sessió.poll() is None:interactiu_sessió.kill();interactiu_sessió.wait()
            informe_VALOR['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Connecta, 수):
                dades=bytearray()
                while len(dades)<수:
                    덩이=Connecta.recv(수-len(dades))
                    if not 덩이: raise AssertionError('RFB EOF')
                    dades.extend(덩이)
                return bytes(dades)
            def 화면인증(contrasenya_VALOR):
                Connecta=socket.create_connection(('127.0.0.5',화면포트),10);Connecta.settimeout(30)
                assert 정확히(Connecta,12)==b'RFB 003.008\n'
                Connecta.sendall(b'RFB 003.008\n');assert 정확히(Connecta,2)==b'\x01\x02'
                Connecta.sendall(b'\x02');repte_VALOR=정확히(Connecta,16)
                입력암호=contrasenya_VALOR.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Connecta.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(repte_VALOR))
                Estat_VALOR=struct.unpack('!I',정확히(Connecta,4))[0]
                return Connecta,Estat_VALOR
            invàlid_contrasenya='!' if not Ajusts['vnc_password'].startswith('!') else '?'
            Connecta,Estat_VALOR=화면인증(invàlid_contrasenya);assert Estat_VALOR==1;Connecta.close();time.sleep(.6)
            informe_VALOR['checks'].append('VNC incorrect password rejected')
            Connecta,Estat_VALOR=화면인증(Ajusts['vnc_password']);assert Estat_VALOR==0
            with Connecta:
                Connecta.sendall(b'\x01');초기=정확히(Connecta,24);너비,높이=struct.unpack('!HH',초기[:4]);Nom=정확히(Connecta,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Nom
                def 화면(증분=0):
                    Connecta.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Connecta,4);수=struct.unpack('!H',머리[2:])[0];total_VALOR=0
                    dibuix_VALOR=bytearray(너비*높이*4)
                    for _ in range(수):
                        X_coordenada,Y_coordenada,영역너비,영역높이,방식=struct.unpack('!HHHHi',정확히(Connecta,12));assert 방식==0 and X_coordenada+영역너비<=너비 and Y_coordenada+영역높이<=높이
                        píxel=정확히(Connecta,영역너비*영역높이*4);total_VALOR+=len(píxel)
                        for línia in range(영역높이):dibuix_VALOR[((Y_coordenada+línia)*너비+X_coordenada)*4:((Y_coordenada+línia)*너비+X_coordenada+영역너비)*4]=píxel[línia*영역너비*4:(línia+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(dibuix_VALOR),'raw','BGRX').save(str(Sortida/'native-vnc.png'))
                    return 수,total_VALOR
                수,total_VALOR=화면();assert 수>0 and total_VALOR==너비*높이*4
                informe_VALOR['checks'].append('Native framebuffer RFB full update {} bytes'.format(total_VALOR))
                수,total_VALOR=화면(1);assert total_VALOR<너비*높이*4
                informe_VALOR['checks'].append('RFB incremental update')
                처음=len(LOG_fila)
                for caràcter_VALOR in 'echo VNC_NATIVE_PASS\r':
                    símbol=0xff0d if caràcter_VALOR=='\r' else ord(caràcter_VALOR)
                    Connecta.sendall(struct.pack('!BBHI',4,1,0,símbol));Connecta.sendall(struct.pack('!BBHI',4,0,0,símbol))
                Espera_Estat(b'VNC_NATIVE_PASS',처음)
                informe_VALOR['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(símbol,prémer_VALOR=1):Connecta.sendall(struct.pack('!BBHI',4,prémer_VALOR,0,símbol))
                처음=len(LOG_fila)
                for caràcter_VALOR in 'echo ':글쇠(ord(caràcter_VALOR))
                글쇠(0xffc6)
                for caràcter_VALOR in 'gksrmf':글쇠(ord(caràcter_VALOR))
                글쇠(0xffc6);글쇠(0xff0d)
                Espera_Estat('\r\n한글\r\n'.encode(),처음)
                informe_VALOR['checks'].append('Native VNC F9 two-set Hangul composition')
                Connecta.sendall(struct.pack('!BBHH',5,0,120,100))
                informe_VALOR['checks'].append('VNC pointer input accepted')
            Procés_VALOR.stdin.write(b'poweroff\n');Procés_VALOR.stdin.flush();Procés_VALOR.wait(timeout=15);assert Procés_VALOR.returncode==0
            informe_VALOR['passed']=True
    finally:
        if Procés_VALOR and Procés_VALOR.poll() is None:
            Procés_VALOR.terminate()
            try: Procés_VALOR.wait(timeout=5)
            except subprocess.TimeoutExpired: Procés_VALOR.kill();Procés_VALOR.wait()
        (Sortida/'serial.log').write_bytes(LOG_fila)
        (Sortida/'report.json').write_text(json.dumps(informe_VALOR,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(informe_VALOR,ensure_ascii=False,indent=2))


if __name__=='__main__': Executa_2()
