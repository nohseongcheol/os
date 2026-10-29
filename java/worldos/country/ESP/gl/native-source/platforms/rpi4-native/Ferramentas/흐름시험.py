#!/usr/bin/env python3
import hashlib,json,subprocess
from executar_comando import Project_raíz

def Executar_2():
    medida_datos=Project_raíz/'build/verification/stream';medida_datos.mkdir(parents=True,exist_ok=True)
    validación_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(medida_datos),str(Project_raíz/'시험/자바/흐름시험.java')])
        datos_cargo=subprocess.run(['python3',str(Project_raíz/'Ferramentas/executar_Ficheiro.py'),str(medida_datos/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (medida_datos/'serial.log').write_bytes(datos_cargo.stdout);assert datos_cargo.returncode==0,datos_cargo.stdout.decode('utf-8','replace')
        Texto=datos_cargo.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Texto,Texto
        validación_informe.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(medida_datos/'report.json').write_text(json.dumps(validación_informe,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Executar_2()
