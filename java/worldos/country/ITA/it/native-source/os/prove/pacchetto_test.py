#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

posizione = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    elenco_VALORE = Path(임시)
    limite_VALORE = elenco_VALORE / '시험장치.java'
    limite_VALORE.write_text('''
class cellulare_VALORE { static int timestamp_VALORE; static int 밀리초() { return timestamp_VALORE++; } static void 잠시양보() {} }
class SMS_Terminale { static void Scrittura(String VALORE) {} static void scrivere_numero(int VALORE) {} }
class rete_driver {
    static int 입출력기준주소 = 1, trasmettere_CONTA_NUMERI, ricevere_CONTA_NUMERI;
    static int[] cellulare_e_mail = {0x52,0x54,0,0x12,0x34,0x56}, recenti_VALORE;
    static int ricevere(int[] dati) { return 0; }
    static int inviare(int[] dati, int durata_VALORE) { recenti_VALORE = dati.clone(); return durata_VALORE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(elenco_VALORE), str(limite_VALORE),
                    str(posizione / 'codiceSorgente/rete_Pila.java'), str(posizione / 'prove/pacchetto_test.java')], check=True)
    subprocess.run(['java', '-cp', str(elenco_VALORE), 'pacchetto_test'], check=True, timeout=10)
