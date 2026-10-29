// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALORE) {
        if (VALORE < 0x80) scheda.scrivere_seriale(VALORE);
        else if (VALORE < 0x800) {
            scheda.scrivere_seriale(0xc0 | (VALORE >> 6)); scheda.scrivere_seriale(0x80 | (VALORE & 63));
        } else if (VALORE < 0x10000) {
            scheda.scrivere_seriale(0xe0 | (VALORE >> 12)); scheda.scrivere_seriale(0x80 | ((VALORE >> 6) & 63)); scheda.scrivere_seriale(0x80 | (VALORE & 63));
        } else {
            scheda.scrivere_seriale(0xf0 | (VALORE >> 18)); scheda.scrivere_seriale(0x80 | ((VALORE >> 12) & 63));
            scheda.scrivere_seriale(0x80 | ((VALORE >> 6) & 63)); scheda.scrivere_seriale(0x80 | (VALORE & 63));
        }
    }
    static void Scrittura(String testo) {
        for (int INDICE = 0; INDICE < testo.length(); INDICE++) {
            int VALORE = testo.charAt(INDICE);
            if (VALORE >= 0xd800 && VALORE <= 0xdbff && INDICE + 1 < testo.length()) {
                int 아래 = testo.charAt(INDICE + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VALORE = 0x10000 + ((VALORE - 0xd800) << 10) + 아래 - 0xdc00; INDICE++;
                }
            }
            if (VALORE >= 0xd800 && VALORE <= 0xdfff) VALORE = 0xfffd;
            문자(VALORE);
        }
    }
    static void numero(int VALORE) {
        if (VALORE < 0) 문자('-'); else VALORE = -VALORE;
        int funzione_INDICE = 1000000000;
        boolean avvia = false;
        while (funzione_INDICE > 0) {
            int cifra_VALORE = -(VALORE / funzione_INDICE);
            if (cifra_VALORE != 0 || avvia || funzione_INDICE == 1) { 문자('0' + cifra_VALORE); avvia = true; }
            VALORE %= funzione_INDICE; funzione_INDICE /= 10;
        }
    }
}
