#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ejecutarComando import raízProyecto,comando

def ponerEnMarcha():
    posiciónValorDestino=raízProyecto/'build/verification/swing';posiciónValorDestino.mkdir(parents=True,exist_ok=True)
    rutaClase=raízProyecto/'build/verification/new-java';rutaClase.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(raízProyecto/'dist/jkoros-native-korean.jar'),'-d',str(rutaClase),str(raízProyecto/'Pruebas/Java/PruebaSwing.java'),str(raízProyecto/'Pruebas/Java/pruebaVentanaHangul.java')])
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
            Datos=(raízProyecto/'build/verification/new-java/PruebaSwing.class').read_bytes()
            enviar('load PruebaSwing.class\n'.encode(),b'hex> ')
            for índiceOrdinal in range(0,len(Datos),64):enviar(Datos[índiceOrdinal:índiceOrdinal+64].hex().encode()+b'\n',b'hex> ')
            enviar(b'.\n')
            enviar('java PruebaSwing\n'.encode(),b'SWING READY')
            desfaseFin=time.monotonic()+3
            while time.monotonic()<desfaseFin:eventoManejador(.1)
            # JFrame centered at (120,100), content at y=130.
            enviar(botónPulsarRatón(200,210),b'',)  # focus JTextField
            posiciónDatos.stdin.write('누리'.encode());posiciónDatos.stdin.flush()
            desfaseFin=time.monotonic()+.3
            while time.monotonic()<desfaseFin:eventoManejador(.05)
            resultado=enviar(botónPulsarRatón(200,255),'SWING CLICK 이름누리'.encode())
            esperarFin(b'true',len(registroEntradaDiario)-len(resultado))
            enviar(valorAtajo(1),b'TERMINAL FOCUS 2')
            resultado=intérpreteComandos('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in resultado
            enviar(botónPulsarRatón(180,12),b'TERMINAL FOCUS 1')
            desfaseFin=time.monotonic()+.3
            while time.monotonic()<desfaseFin:eventoManejador(.05)
            with socket.socket(socket.AF_UNIX) as códigoCarácter:
                códigoCarácter.settimeout(10);códigoCarácter.connect(str(conexiónControlDoblePrueba))
                with códigoCarácter.makefile('rwb') as entradaElementoArchivo:
                    json.loads(entradaElementoArchivo.readline())
                    for valorPetición in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(posiciónValorDestino/'native-swing.png'),'format':'png'}}):
                        entradaElementoArchivo.write((json.dumps(valorPetición)+'\n').encode());entradaElementoArchivo.flush()
                        while True:
                            valorDevuelto=json.loads(entradaElementoArchivo.readline())
                            if 'error' in valorDevuelto:raise AssertionError(valorDevuelto)
                            if 'return' in valorDevuelto:break
            enviar(botónPulsarRatón(505,115))
            intérpreteComandos('echo SWING_CLOSED_OK')
            Datos=(rutaClase/'pruebaVentanaHangul.class').read_bytes()
            enviar('load pruebaVentanaHangul.class\n'.encode(),b'hex> ')
            for índiceOrdinal in range(0,len(Datos),64):enviar(Datos[índiceOrdinal:índiceOrdinal+64].hex().encode()+b'\n',b'hex> ')
            enviar(b'.\n')
            enviar('java pruebaVentanaHangul\n'.encode(),b'KOREAN SWING READY')
            enviar(botónPulsarRatón(200,255),'KOREAN SWING CLICK nombre'.encode())
            enviar(botónPulsarRatón(505,115))
            intérpreteComandos('echo KOREAN_SWING_CLOSED_OK')
            informeValidación.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','español ventana/botón/NotificaciónAcción/ColaEvento directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if posiciónDatos.poll() is None:posiciónDatos.terminate()
            try:posiciónDatos.wait(timeout=5)
            except subprocess.TimeoutExpired:posiciónDatos.kill();posiciónDatos.wait()
            Selector.close();posiciónDatos.stdin.close();posiciónDatos.stdout.close();(posiciónValorDestino/'serial.log').write_bytes(registroEntradaDiario);(posiciónValorDestino/'report.json').write_text(json.dumps(informeValidación,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ponerEnMarcha()
