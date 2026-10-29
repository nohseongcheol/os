#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

posición = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as valorTemporal:
    valorDirectorio = Path(valorTemporal)
    valorFrontera = valorDirectorio / '시험장치.java'
    valorFrontera.write_text('''
class Dispositivo { static int valorMarcaTiempo; static int milisegundos() { return valorMarcaTiempo++; } static void cederBrevemente() {} }
class TerminalTexto { static void escribir(String valor) {} static void escribirNúmero(int valor) {} }
class ControladorRed {
    static int direcciónBaseEntradaSalida = 1, númeroElementosTransmitir, recibirNúmeroElementos;
    static int[] direcciónDispositivo = {0x52,0x54,0,0x12,0x34,0x56}, valorReciente;
    static int recibir(int[] Datos) { return 0; }
    static int enviar(int[] Datos, int longitud) { valorReciente = Datos.clone(); return longitud; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(valorDirectorio), str(valorFrontera),
                    str(posición / 'fuente/PilaRed.java'), str(posición / 'Pruebas/PruebaPaqueteDatos.java')], check=True)
    subprocess.run(['java', '-cp', str(valorDirectorio), 'PruebaPaqueteDatos'], check=True, timeout=10)
