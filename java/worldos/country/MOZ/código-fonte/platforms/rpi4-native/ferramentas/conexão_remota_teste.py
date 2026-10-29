#!/usr/bin/env python3
"""real_dados OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Executar_comando import ação_raiz, comando
from ponte_3de4fe3a import ponte_3de4fe3a


def iniciar():
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('--kernel', type=Path, default=ação_raiz / 'build/kernel8.img')
    analisador_48ee4b1b.add_argument('--access', type=Path, default=ação_raiz / 'build/remote/access.json')
    analisador_48ee4b1b.add_argument('--output', type=Path, default=ação_raiz / 'build/verification/native-remote')
    argumentos = analisador_48ee4b1b.parse_args()
    saídaTexto = argumentos.output
    saídaTexto.mkdir(parents=True, exist_ok=True)
    Definições = json.loads(argumentos.access.read_text())
    relatar_VALOR = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argumentos.kernel.read_bytes()).hexdigest(), 'checks': []}
    def vazio_porta():
        with socket.socket() as Ligar:
            Ligar.bind(('127.0.0.5', 0))
            return Ligar.getsockname()[1]
    shell_porta, tela_porta, porta_de_arquivo = vazio_porta(), vazio_porta(), vazio_porta()
    LOG_linha = bytearray()
    Processo_VALOR = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, ponte_3de4fe3a(porta_de_arquivo,
                ['tcp:{}:22'.format(shell_porta), 'tcp:{}:5900'.format(tela_porta)], ID_do_host='127.0.0.5') as ponte_VALOR:
            실행인수 = comando()
            실행인수[실행인수.index('-kernel') + 1] = str(argumentos.kernel.resolve())
            Processo_VALOR = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ponte_VALOR.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    dados = Processo_VALOR.stdout.read(4096)
                    if not dados: break
                    LOG_linha.extend(dados)
            thread_VALOR = threading.Thread(target=수집, daemon=True)
            thread_VALOR.start()
            def estado_de_espera(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_linha[처음:]:
                    if time.monotonic()>끝 or Processo_VALOR.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_linha[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            estado_de_espera(b'jkoros-native> ')
            auxiliar_VALOR = Path(임시)/'askpass'
            auxiliar_VALOR.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            auxiliar_VALOR.chmod(0o700)
            ambiente = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(auxiliar_VALOR), SSH_ASKPASS_REQUIRE='force')
            def SSH(senha_VALOR, instrução_VALOR_4c26ea1b, Acrescentar_entrada=()):
                ambiente['JKOROS_TEST_PASSWORD']=senha_VALOR
                argumentos=['ssh','-v']+list(Acrescentar_entrada)+['-p',str(shell_porta),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instrução_VALOR_4c26ea1b]
                resultado=subprocess.run(argumentos,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=ambiente,start_new_session=True,timeout=50)
                return resultado
            resultado=SSH('!' + Definições['ssh_password'], 'echo SHOULD_NOT_RUN')
            (saídaTexto/'ssh-rejected.log').write_bytes(resultado.stderr)
            assert resultado.returncode!=0 and b'Permission denied' in resultado.stderr and b'SHOULD_NOT_RUN' not in LOG_linha, resultado.stderr
            relatar_VALOR['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            resultado=SSH(Definições['ssh_password'], 'echo SSH_NATIVE_PASS')
            (saídaTexto/'ssh.log').write_bytes(resultado.stderr)
            (saídaTexto/'ssh-output.txt').write_bytes(resultado.stdout)
            assert resultado.returncode==0 and b'SSH_NATIVE_PASS' in resultado.stdout, (resultado.returncode,resultado.stdout,resultado.stderr)
            relatar_VALOR['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in resultado.stderr, resultado.stderr
            relatar_VALOR['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            resultado=SSH(Definições['ssh_password'], 'cd /example/java; java ExemploSaída; cd /')
            assert resultado.returncode==0 and 'JAVA saídaTexto: 안녕하세요 😀'.encode() in resultado.stdout,resultado.stdout
            relatar_VALOR['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            resultado=SSH(Definições['ssh_password'], 'missing_remote_command')
            assert resultado.returncode==127,resultado.returncode
            relatar_VALOR['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            resultado=SSH(Definições['ssh_password'], 'cat /example/java/ExemploJanela.java', ('-o', 'RekeyLimit=1K'))
            (saídaTexto/'ssh-rekey.log').write_bytes(resultado.stderr)
            assert resultado.returncode==0 and 'class ExemploJanela'.encode() in resultado.stdout, (resultado.returncode,resultado.stdout,resultado.stderr)
            assert resultado.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, resultado.stderr
            relatar_VALOR['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(shell_porta),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interativo_sessão=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=ambiente,start_new_session=True,bufsize=0)
            transcrição=bytearray();seleção_VALOR=selectors.DefaultSelector();seleção_VALOR.register(interativo_sessão.stdout,selectors.EVENT_READ)
            def leitura_interativo(mostrar_VALOR):
                data_limite_VALOR=time.monotonic()+30
                while mostrar_VALOR not in transcrição:
                    if time.monotonic()>data_limite_VALOR or interativo_sessão.poll() is not None:raise AssertionError('SSH interactive missing '+repr(mostrar_VALOR)+' '+repr(bytes(transcrição)))
                    for entrada_VALOR_962f286b,_ in seleção_VALOR.select(.1):
                        fragmento_VALOR=entrada_VALOR_962f286b.fileobj.read(4096)
                        if fragmento_VALOR:transcrição.extend(fragmento_VALOR)
            try:
                leitura_interativo(b'shared native console')
                interativo_sessão.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interativo_sessão.stdin.flush();leitura_interativo(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interativo_sessão.stdin.write(b'\x04');interativo_sessão.stdin.flush();나머지,erro=interativo_sessão.communicate(timeout=15)
                assert interativo_sessão.returncode==0 and b'PTY allocation request failed' not in erro,(interativo_sessão.returncode,erro)
                (saídaTexto/'ssh-interactive.txt').write_bytes(transcrição+나머지)
            finally:
                seleção_VALOR.close()
                if interativo_sessão.poll() is None:interativo_sessão.kill();interativo_sessão.wait()
            relatar_VALOR['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Ligar, número):
                dados=bytearray()
                while len(dados)<número:
                    parte_VALOR=Ligar.recv(número-len(dados))
                    if not parte_VALOR: raise AssertionError('RFB EOF')
                    dados.extend(parte_VALOR)
                return bytes(dados)
            def tela_autenticação(senha_VALOR):
                Ligar=socket.create_connection(('127.0.0.5',tela_porta),10);Ligar.settimeout(30)
                assert 정확히(Ligar,12)==b'RFB 003.008\n'
                Ligar.sendall(b'RFB 003.008\n');assert 정확히(Ligar,2)==b'\x01\x02'
                Ligar.sendall(b'\x02');desafio_VALOR=정확히(Ligar,16)
                entrada_senha=senha_VALOR.encode('ascii')[:8].ljust(8, b'\0')
                Chave_material=bytes(int('{:08b}'.format(número)[::-1],2) for número in entrada_senha)
                Ligar.sendall(DES.new(Chave_material,DES.MODE_ECB).encrypt(desafio_VALOR))
                Estado_VALOR=struct.unpack('!I',정확히(Ligar,4))[0]
                return Ligar,Estado_VALOR
            inválido_senha='!' if not Definições['vnc_password'].startswith('!') else '?'
            Ligar,Estado_VALOR=tela_autenticação(inválido_senha);assert Estado_VALOR==1;Ligar.close();time.sleep(.6)
            relatar_VALOR['checks'].append('VNC incorrect password rejected')
            Ligar,Estado_VALOR=tela_autenticação(Definições['vnc_password']);assert Estado_VALOR==0
            with Ligar:
                Ligar.sendall(b'\x01');estado_inicial=정확히(Ligar,24);너비,altura_VALOR=struct.unpack('!HH',estado_inicial[:4]);Nome=정확히(Ligar,struct.unpack('!I',estado_inicial[20:24])[0])
                assert (너비,altura_VALOR)==(640,480) and b'jkoros native'==Nome
                def tela(incremento_etapa=0):
                    Ligar.sendall(struct.pack('!BBHHHH',3,incremento_etapa,0,0,너비,altura_VALOR));HEAD_VALOR=정확히(Ligar,4);número=struct.unpack('!H',HEAD_VALOR[2:])[0];total_VALOR=0
                    desenho_VALOR=bytearray(너비*altura_VALOR*4)
                    for _ in range(número):
                        coordenada_X,Y_coordenada,영역너비,região_altura,método_MODO=struct.unpack('!HHHHi',정확히(Ligar,12));assert método_MODO==0 and coordenada_X+영역너비<=너비 and Y_coordenada+região_altura<=altura_VALOR
                        pixel=정확히(Ligar,영역너비*região_altura*4);total_VALOR+=len(pixel)
                        for linha_de_entrada in range(região_altura):desenho_VALOR[((Y_coordenada+linha_de_entrada)*너비+coordenada_X)*4:((Y_coordenada+linha_de_entrada)*너비+coordenada_X+영역너비)*4]=pixel[linha_de_entrada*영역너비*4:(linha_de_entrada+1)*영역너비*4]
                    if not incremento_etapa:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,altura_VALOR),bytes(desenho_VALOR),'raw','BGRX').save(str(saídaTexto/'native-vnc.png'))
                    return número,total_VALOR
                número,total_VALOR=tela();assert número>0 and total_VALOR==너비*altura_VALOR*4
                relatar_VALOR['checks'].append('Native framebuffer RFB full update {} bytes'.format(total_VALOR))
                número,total_VALOR=tela(1);assert total_VALOR<너비*altura_VALOR*4
                relatar_VALOR['checks'].append('RFB incremental update')
                처음=len(LOG_linha)
                for caractere_VALOR in 'echo VNC_NATIVE_PASS\r':
                    símbolo=0xff0d if caractere_VALOR=='\r' else ord(caractere_VALOR)
                    Ligar.sendall(struct.pack('!BBHI',4,1,0,símbolo));Ligar.sendall(struct.pack('!BBHI',4,0,0,símbolo))
                estado_de_espera(b'VNC_NATIVE_PASS',처음)
                relatar_VALOR['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Chave_traço(símbolo,누름=1):Ligar.sendall(struct.pack('!BBHI',4,누름,0,símbolo))
                처음=len(LOG_linha)
                for caractere_VALOR in 'echo ':Chave_traço(ord(caractere_VALOR))
                Chave_traço(0xffc6)
                for caractere_VALOR in 'gksrmf':Chave_traço(ord(caractere_VALOR))
                Chave_traço(0xffc6);Chave_traço(0xff0d)
                estado_de_espera('\r\n한글\r\n'.encode(),처음)
                relatar_VALOR['checks'].append('Native VNC F9 two-set Hangul composition')
                Ligar.sendall(struct.pack('!BBHH',5,0,120,100))
                relatar_VALOR['checks'].append('VNC pointer input accepted')
            Processo_VALOR.stdin.write(b'poweroff\n');Processo_VALOR.stdin.flush();Processo_VALOR.wait(timeout=15);assert Processo_VALOR.returncode==0
            relatar_VALOR['passed']=True
    finally:
        if Processo_VALOR and Processo_VALOR.poll() is None:
            Processo_VALOR.terminate()
            try: Processo_VALOR.wait(timeout=5)
            except subprocess.TimeoutExpired: Processo_VALOR.kill();Processo_VALOR.wait()
        (saídaTexto/'serial.log').write_bytes(LOG_linha)
        (saídaTexto/'report.json').write_text(json.dumps(relatar_VALOR,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(relatar_VALOR,ensure_ascii=False,indent=2))


if __name__=='__main__': iniciar()
