#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Posición = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    directorio_VALOR = Path(임시)
    경계 = directorio_VALOR / '시험장치.java'
    경계.write_text('''
class dispositivo_VALOR { static int marca_de_hora_VALOR; static int 밀리초() { return marca_de_hora_VALOR++; } static void 잠시양보() {} }
class SMS_Terminal { static void Escritura(String VALOR) {} static void 수쓰기(int VALOR) {} }
class Rede_controlador {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] dispositivo_ENDEREZO = {0x52,0x54,0,0x12,0x34,0x56}, recente_VALOR;
    static int 받기(int[] datos) { return 0; }
    static int enviar(int[] datos, int duración_VALOR) { recente_VALOR = datos.clone(); return duración_VALOR; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(directorio_VALOR), str(경계),
                    str(Posición / 'FONTE/Rede_Montón.java'), str(Posición / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(directorio_VALOR), '패킷시험'], check=True, timeout=10)
