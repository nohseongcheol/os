#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ejecutarComando import raízProyecto,comando

def ponerEnMarcha():
    posiciónValorDestino=raízProyecto/'build/verification/windows';posiciónValorDestino.mkdir(parents=True,exist_ok=True)
    informeValidación={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest()};registroEntradaDiario=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as rutaTrabajoEnCurso:
        conexiónControlDoblePrueba=Path(rutaTrabajoEnCurso)/'qmp.sock'
        posiciónDatos=subprocess.Popen(comando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(conexiónControlDoblePrueba)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        Selector=selectors.DefaultSelector();Selector.register(posiciónDatos.stdout,selectors.EVENT_READ)
        def eventoManejador(unidadSegundos=.1):
            for valorPulsado,_ in Selector.select(unidadSegundos):
                valorSegundo=valorPulsado.fileobj.read(65536)
                if valorSegundo:registroEntradaDiario.extend(valorSegundo)
            assert b'PANIC:' not in registroEntradaDiario and b'HALTED' not in registroEntradaDiario,registroEntradaDiario[-2048:]
        def esperarFin(marcador,posiciónActual,unidadSegundos=50):
            desfaseFin=time.monotonic()+unidadSegundos
            while marcador not in registroEntradaDiario[posiciónActual:]:
                if time.monotonic()>desfaseFin or posiciónDatos.poll() is not None:raise AssertionError(registroEntradaDiario[posiciónActual:].decode('utf-8','replace'))
                eventoManejador()
            return bytes(registroEntradaDiario[posiciónActual:])
        def enviar(valorSegundo,marcador=b'jkoros-native> '):
            posiciónActual=len(registroEntradaDiario);posiciónDatos.stdin.write(valorSegundo);posiciónDatos.stdin.flush();return esperarFin(marcador,posiciónActual)
        def intérpreteComandos(datosCadena):return enviar((datosCadena+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def valorAtajo(índiceTercero):return bytes([30,2,índiceTercero,0,0,0,0])
        def botónPulsarRatón(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical):return bytes([30,1,1,coordenadaCoordenadaHorizontal&255,coordenadaCoordenadaHorizontal>>8,coordenadaCoordenadaVertical&255,coordenadaCoordenadaVertical>>8,30,1,0,coordenadaCoordenadaHorizontal&255,coordenadaCoordenadaHorizontal>>8,coordenadaCoordenadaVertical&255,coordenadaCoordenadaVertical>>8])
        def modoComando():
            posiciónDatos.stdin.write(b'\x1b');posiciónDatos.stdin.flush();desfaseFin=time.monotonic()+.2
            while time.monotonic()<desfaseFin:eventoManejador(.03)
        try:
            esperarFin(b'jkoros-native> ',0)
            intérpreteComandos('terminal');eventoManejador(.3)
            intérpreteComandos('mkdir first; cd first; export NAME=one')
            enviar('vi ordinalPrimero.py\n'.encode(),b'NORMAL')
            enviar('i값 = 21\nprint(valor * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            desfaseFin=time.monotonic()+3
            while time.monotonic()<desfaseFin:eventoManejador(.1)
            enviar(valorAtajo(1),b'TERMINAL FOCUS 2');eventoManejador(.2)
            assert b'/\r\n' in intérpreteComandos('pwd')
            intérpreteComandos('export NAME=two')
            enviar('vi ordinalSegundo.txt\n'.encode(),b'NORMAL')
            enviar('i두 번째 ventana\n'.encode(),b'INSERT')
            enviar(botónPulsarRatón(180,12),b'TERMINAL FOCUS 1');eventoManejador(.2)
            modoComando();enviar(b':wq\r')
            assert b'one:/first' in intérpreteComandos('echo "$NAME:$PWD"')
            assert 'valor = 21\r\nprint(valor * 2)'.encode() in intérpreteComandos('cat ordinalPrimero.py')
            resultado=intérpreteComandos('python ordinalPrimero.py');assert b'42\r\n' in resultado,resultado
            # Close the first shell with its actual title-bar X; second editor resumes.
            enviar(botónPulsarRatón(560,63),b'TERMINAL FOCUS 2');eventoManejador(.2)
            modoComando();enviar(b':wq\r')
            assert b'two:/' in intérpreteComandos('echo "$NAME:$PWD"')
            assert '두 번째 ventana'.encode() in intérpreteComandos('cat ordinalSegundo.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            enviar('vi ordinalSegundo.txt\n'.encode(),b'NORMAL');enviar(b'xu',b'NORMAL')
            enviar(b'iX',b'INSERT');modoComando();enviar(b':q\r',b'Unsaved')
            enviar(b':q!\r');assert '두 번째 ventana'.encode() in intérpreteComandos('cat ordinalSegundo.txt')
            enviar(valorAtajo(1),b'TERMINAL FOCUS 1');eventoManejador(.2)
            enviar(valorAtajo(1),b'TERMINAL FOCUS 3');eventoManejador(.2)
            enviar(valorAtajo(1),b'TERMINAL FOCUS 4');eventoManejador(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            posiciónDatos.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));posiciónDatos.stdin.flush()
            intérpreteComandos('echo DRAGGED_OK')
            enviar('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            enviar('i저장하지 않은 Datos'.encode(),b'INSERT')
            enviar(botónPulsarRatón(578,97),b'TERMINAL FOCUS 3');eventoManejador(.2)
            assert '버릴문서.txt'.encode() not in intérpreteComandos('ls')
            enviar(valorAtajo(1),b'TERMINAL FOCUS 4');eventoManejador(.2)
            intérpreteComandos('echo REUSED_WINDOW_OK')
            importeCompletado=registroEntradaDiario.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            esperarFin(b'jkoros-native> ',importeCompletado)
            # UART completion precedes the next QEMU display refresh.
            desfaseFin=time.monotonic()+.3
            while time.monotonic()<desfaseFin:eventoManejador(.05)
            with socket.socket(socket.AF_UNIX) as códigoCarácter:
                códigoCarácter.settimeout(10);códigoCarácter.connect(str(conexiónControlDoblePrueba))
                with códigoCarácter.makefile('rwb') as entradaElementoArchivo:
                    json.loads(entradaElementoArchivo.readline())
                    for valorPetición in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(posiciónValorDestino/'four-terminals.png'),'format':'png'}}):
                        entradaElementoArchivo.write((json.dumps(valorPetición)+'\n').encode());entradaElementoArchivo.flush()
                        while True:
                            valorDevuelto=json.loads(entradaElementoArchivo.readline())
                            if 'error' in valorDevuelto:raise AssertionError(valorDevuelto)
                            if 'return' in valorDevuelto:break
            from PIL import Image
            listaPíxeles=Image.open(str(posiciónValorDestino/'four-terminals.png')).convert('RGB')
            for parCoordenada,colorPíxel in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert listaPíxeles.getpixel(parCoordenada)==colorPíxel,(parCoordenada,listaPíxeles.getpixel(parCoordenada))
            intérpreteComandos('echo FOUR_WINDOWS_OK')
            informeValidación.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if posiciónDatos.poll() is None:posiciónDatos.terminate()
            try:posiciónDatos.wait(timeout=5)
            except subprocess.TimeoutExpired:posiciónDatos.kill();posiciónDatos.wait()
            Selector.close();posiciónDatos.stdin.close();posiciónDatos.stdout.close();(posiciónValorDestino/'serial.log').write_bytes(registroEntradaDiario);(posiciónValorDestino/'report.json').write_text(json.dumps(informeValidación,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ponerEnMarcha()
