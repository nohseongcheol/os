#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

posição = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Diretório_VALOR = Path(임시)
    limite_VALOR = Diretório_VALOR / '시험장치.java'
    limite_VALOR.write_text('''
class celular_VALOR { static int carimbo_de_data_hora_VALOR; static int 밀리초() { return carimbo_de_data_hora_VALOR++; } static void 잠시양보() {} }
class SMS_Terminal { static void Escrita(String VALOR) {} static void gravar_número(int VALOR) {} }
class rede_driver {
    static int 입출력기준주소 = 1, 송신수, receber_CONT_NÚM;
    static int[] celular_email = {0x52,0x54,0,0x12,0x34,0x56}, recente_VALOR;
    static int receber(int[] dados) { return 0; }
    static int enviar(int[] dados, int duração_VALOR) { recente_VALOR = dados.clone(); return duração_VALOR; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Diretório_VALOR), str(limite_VALOR),
                    str(posição / 'códigoFonte/rede_pilha.java'), str(posição / 'testes/pacote_teste.java')], check=True)
    subprocess.run(['java', '-cp', str(Diretório_VALOR), 'pacote_teste'], check=True, timeout=10)
