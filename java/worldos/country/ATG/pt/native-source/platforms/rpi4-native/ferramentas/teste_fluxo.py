#!/usr/bin/env python3
import hashlib,json,subprocess
from Executar_comando import ação_raiz

def iniciar():
    RC_dados=ação_raiz/'build/verification/stream';RC_dados.mkdir(parents=True,exist_ok=True)
    validação_relatar={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(RC_dados),str(ação_raiz/'testes/자바/teste_fluxo.java')])
        dados_cargo=subprocess.run(['python3',str(ação_raiz/'ferramentas/Executar_Arquivo.py'),str(RC_dados/'teste_fluxo.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (RC_dados/'serial.log').write_bytes(dados_cargo.stdout);assert dados_cargo.returncode==0,dados_cargo.stdout.decode('utf-8','replace')
        texto=dados_cargo.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in texto,texto
        validação_relatar.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(RC_dados/'report.json').write_text(json.dumps(validação_relatar,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':iniciar()
