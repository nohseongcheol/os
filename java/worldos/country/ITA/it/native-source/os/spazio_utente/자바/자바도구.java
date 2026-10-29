// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 strumenti 공통 uscitaTesto 및 ASCII file Nome Processi_VALORE_voce. */
public final class 자바도구 {
    /** UTF-8 byte_VALORE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 rifiutare_VALORE. */
    static int 원문해독(int[] dati, int durata_VALORE) {
        int Lettura = 0, Scrittura = 0;
        if (durata_VALORE >= 3 && dati[0] == 239 && dati[1] == 187 && dati[2] == 191) Lettura = 3;
        while (Lettura < durata_VALORE) {
            int VALORE = dati[Lettura++], numero = 0, 최소 = 0;
            if (VALORE >= 194 && VALORE <= 223) { numero = 1; 최소 = 128; VALORE &= 31; }
            else if (VALORE >= 224 && VALORE <= 239) { numero = 2; 최소 = 2048; VALORE &= 15; }
            else if (VALORE >= 240 && VALORE <= 244) { numero = 3; 최소 = 65536; VALORE &= 7; }
            else if (VALORE >= 128 || VALORE < 0) return -1;
            if (numero > durata_VALORE - Lettura) return -1;
            for (int i = 0; i < numero; i++) {
                int Avanti_articolo = dati[Lettura++]; if ((Avanti_articolo & 192) != 128) return -1;
                VALORE = (VALORE << 6) | (Avanti_articolo & 63);
            }
            if (VALORE < 최소 || VALORE > 0x10ffff || (VALORE >= 0xd800 && VALORE <= 0xdfff)) return -1;
            if (VALORE >= 65536) { VALORE -= 65536; dati[Scrittura++] = 0xd800 | (VALORE >> 10); dati[Scrittura++] = 0xdc00 | (VALORE & 1023); }
            else dati[Scrittura++] = VALORE;
        }
        return Scrittura;
    }
    static void scrivere_numero(int VALORE) {
        if (VALORE < 0) spazio_utente.scrivere_carattere_VALORE('-'); else VALORE = -VALORE;
        int funzione_INDICE = 1000000000;
        boolean avvia = false;
        while (funzione_INDICE != 0) {
            int numero = -(VALORE / funzione_INDICE);
            if (numero != 0 || avvia || funzione_INDICE == 1) { spazio_utente.scrivere_carattere_VALORE('0' + numero); avvia = true; }
            VALORE %= funzione_INDICE; funzione_INDICE /= 10;
        }
    }
    static int Nome(int[] meta_VALORE, String 원본) {
        if (원본.length() >= meta_VALORE.length) return -1;
        for (int numero = 0; numero < meta_VALORE.length; numero++) meta_VALORE[numero] = numero < 원본.length() ? 원본.charAt(numero) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECONDO_operando) {
        if (가.length() != SECONDO_operando.length()) return false;
        for (int numero = 0; numero < 가.length(); numero++) if (가.charAt(numero) != SECONDO_operando.charAt(numero)) return false;
        return true;
    }
}
