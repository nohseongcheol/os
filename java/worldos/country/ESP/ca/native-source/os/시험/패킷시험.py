#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Posició = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    directori_VALOR = Path(임시)
    경계 = directori_VALOR / '시험장치.java'
    경계.write_text('''
class dispositiu_VALOR { static int data_i_hora_VALOR; static int 밀리초() { return data_i_hora_VALOR++; } static void 잠시양보() {} }
class SMS_Terminal { static void Escriptura(String VALOR) {} static void 수쓰기(int VALOR) {} }
class xarxa_controlador {
    static int 입출력기준주소 = 1, 송신수, rebre_COMPT;
    static int[] dispositiu_ADREÇA = {0x52,0x54,0,0x12,0x34,0x56}, recent_VALOR;
    static int rebre(int[] dades) { return 0; }
    static int enviar(int[] dades, int durada_VALOR) { recent_VALOR = dades.clone(); return durada_VALOR; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(directori_VALOR), str(경계),
                    str(Posició / 'FONT/xarxa_Pila.java'), str(Posició / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(directori_VALOR), '패킷시험'], check=True, timeout=10)
