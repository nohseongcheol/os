#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ejecutarComando import raízProyecto

def ponerEnMarcha():
    datosResultado=raízProyecto/'build/verification/coding';datosResultado.mkdir(parents=True,exist_ok=True)
    informeValidación={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(raízProyecto/'Herramientas/sDKExportar.py')])
        with tarfile.open(str(raízProyecto/'dist/jkoros-native-aarch64-sdk.tar.gz')) as paqueteComprimido:paqueteComprimido.extractall(str(datosResultado))
        juegoHerramientasDesarrollo=datosResultado/'jkoros-native-sdk'
        listaSímbolos=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(juegoHerramientasDesarrollo/'lib/libposix-kor-user.a')]).decode()
        for nombre in ('crearExtremo','asociarDirección','enviarDatosDatagrama','recibirDatosDatagrama','abrirArchivo','leerDatosArchivo','escribirDatosArchivo'):
            assert ' T '+nombre+'\n' in listaSímbolos, nombre
        (datosResultado/'korean-function-symbols.txt').write_text(listaSímbolos)
        informeValidación['checks'].append('real-korean-c-function-symbols')
        def ejecutarComando(nombre,ruta,arregloArgumento,esperado):
            posiciónDatos=subprocess.run(['python3',str(raízProyecto/'Herramientas/ejecutarArchivo.py'),str(ruta)]+arregloArgumento,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (datosResultado/(nombre+'.log')).write_bytes(posiciónDatos.stdout);assert posiciónDatos.returncode==0,posiciónDatos.stdout.decode('utf-8','replace')
            assert esperado.encode() in posiciónDatos.stdout,posiciónDatos.stdout;informeValidación['checks'].append(nombre)
        for valorSufijo in ('c','cpp'):
            archivoCódigoEjecutable=datosResultado/('Saludo-'+valorSufijo+'.elf')
            subprocess.check_call(['python3',str(juegoHerramientasDesarrollo/'compile.py'),str(juegoHerramientasDesarrollo/'examples'/('Saludo.'+valorSufijo)),'-o',str(archivoCódigoEjecutable)])
            ejecutarComando('korean-'+valorSufijo,archivoCódigoEjecutable,[],'posix-kor invocar')
        archivoCódigoEjecutable=datosResultado/'valorFlujo.elf'
        subprocess.check_call(['python3',str(juegoHerramientasDesarrollo/'compile.py'),str(juegoHerramientasDesarrollo/'examples/valorFlujo.c'),'-o',str(archivoCódigoEjecutable)])
        ejecutarComando('c-stream-queues',archivoCódigoEjecutable,[],'C posix-kor 연결형 Comunicación PASS')
        ejecutarComando('korean-python',raízProyecto/'Ejemplos/CodificaciónHangul/Saludo.py',['--include',str(raízProyecto/'Ejemplos/CodificaciónHangul/español.py')],'안녕하세요 누리')
        ejecutarComando('guest-korean-javac',raízProyecto/'Ejemplos/CodificaciónHangul/Saludo.java',[],'안녕하세요 · valorTotal=42')
        informeValidación['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(datosResultado/'report.json').write_text(json.dumps(informeValidación,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ponerEnMarcha()
