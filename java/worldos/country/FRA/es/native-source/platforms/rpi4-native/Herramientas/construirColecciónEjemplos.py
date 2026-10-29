"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from construirBibliotecaJava import crearBibliotecaJava


def crearColecciónEjemplos(rutaRaíz, rutaRepositorio, ejecutarComando):
    datosOriginal=rutaRepositorio/'example';datosResultado=rutaRaíz/'build/examples';datosResultado.mkdir(parents=True,exist_ok=True)
    rutaClase=datosResultado/'classes';rutaClase.mkdir(exist_ok=True)
    crearBibliotecaJava(rutaRaíz,ejecutarComando)
    ip_settings = read_config(rutaRaíz)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = datosResultado/'java-source'; java_sources.mkdir(exist_ok=True)
    ejecutarJava=[]
    for path in sorted((datosOriginal/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); ejecutarJava.append(target)
    ejecutarComando(['javac','--release','8','-encoding','UTF-8','-cp',rutaRaíz/'build/java-library/classes','-d',rutaClase]+ejecutarJava)
    secuenciaInstrucciónMáquina=['public final class PaqueteEjemplo { public static int instalarValor(int Lengua) { int valorProcesado;',
          'valorProcesado=IntérpreteComandos.directorioEjemplo("/example"); if(valorProcesado<0)return valorProcesado;']
    manifiestoPaquete={}
    léame=guest_bytes(datosOriginal/'README.md')
    if len(léame)>16384: raise ValueError('example README exceeds native VFS limit')
    secuenciaInstrucciónMáquina.append('valorProcesado=IntérpreteComandos.archivoEjemplo("/example/README.md","%s"); if(valorProcesado<0)return valorProcesado;'%léame.hex())
    manifiestoPaquete['/example/README.md']={'bytes':len(léame),'sha256':hashlib.sha256(léame).hexdigest()}
    secuenciaInstrucciónMáquina.append('if(Lengua==0){valorProcesado=IntérpreteComandos.directorioEjemplo("/lib"); if(valorProcesado<0)return valorProcesado;')
    for ruta in [datosOriginal/'python/español.py'] + sorted((rutaRaíz/'puentePython/biblioteca').glob('*.py')):
        valorContenidoValor=guest_bytes(ruta);valorObjetivo='/lib/'+ruta.name
        if len(valorContenidoValor)>16384 or len(valorObjetivo.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+valorObjetivo)
        secuenciaInstrucciónMáquina.append('valorProcesado=IntérpreteComandos.archivoEjemplo(%s,"%s"); if(valorProcesado<0)return valorProcesado;'%(json.dumps(valorObjetivo,ensure_ascii=True),valorContenidoValor.hex()))
        manifiestoPaquete[valorObjetivo]={'bytes':len(valorContenidoValor),'sha256':hashlib.sha256(valorContenidoValor).hexdigest()}
    secuenciaInstrucciónMáquina.append('}')
    for índiceBuscar,Lengua in enumerate(('java','c','python')):
        listaArchivo=[(posiciónDatos.name,posiciónDatos) for posiciónDatos in sorted((datosOriginal/Lengua).iterdir()) if posiciónDatos.is_file()]
        if Lengua=='java':listaArchivo += [(posiciónDatos.stem+'.class',rutaClase/(posiciónDatos.stem+'.class')) for posiciónDatos in ejecutarJava]
        secuenciaInstrucciónMáquina += ['if(Lengua==%d){'%índiceBuscar,'valorProcesado=IntérpreteComandos.directorioEjemplo("/example/%s"); if(valorProcesado<0)return valorProcesado;'%Lengua]
        for nombre,ruta in listaArchivo:
            valorContenidoValor=guest_bytes(ruta);valorObjetivo='/example/'+Lengua+'/'+nombre
            if len(valorContenidoValor)>16384 or len(valorObjetivo.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+valorObjetivo)
            secuenciaInstrucciónMáquina.append('valorProcesado=IntérpreteComandos.archivoEjemplo(%s,"%s"); if(valorProcesado<0)return valorProcesado;'%(json.dumps(valorObjetivo,ensure_ascii=True),valorContenidoValor.hex()))
            manifiestoPaquete[valorObjetivo]={'bytes':len(valorContenidoValor),'sha256':hashlib.sha256(valorContenidoValor).hexdigest()}
        secuenciaInstrucciónMáquina += ['return 0;}']
    secuenciaInstrucciónMáquina += ['return -22;}}']
    (rutaRaíz/'build/PaqueteEjemplo.java').write_text('\n'.join(secuenciaInstrucciónMáquina)+'\n')
    (datosResultado/'manifest.json').write_text(json.dumps(manifiestoPaquete,ensure_ascii=False,indent=2)+'\n')
