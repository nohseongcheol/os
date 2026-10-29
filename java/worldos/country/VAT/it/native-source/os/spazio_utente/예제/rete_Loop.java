// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Dimensione/홀수 durata_VALORE 데이터그램으로 effettivo_dati RTL8139 ricevere_VALORE Loop_VALORE 순환을 시험한다. */
public final class rete_Loop {
    public static int avvia() {
        if (spazio_utente.인수개수() != 1) { spazio_utente.Scrittura("Usage: run stress PORT\n"); return 2; }
        String testo = spazio_utente.argomenti(0);
        int porta_VALORE = 0;
        for (int INDICE = 0; INDICE < testo.length(); INDICE++) {
            if (testo.charAt(INDICE) < '0' || testo.charAt(INDICE) > '9' || porta_VALORE > 6553) return 2;
            porta_VALORE = porta_VALORE * 10 + testo.charAt(INDICE) - '0';
        }
        if (porta_VALORE < 1 || porta_VALORE > 65535) return 2;
        int handle_VALORE = spazio_utente.aperto_rete(0);
        if (handle_VALORE < 0) return 3;
        int[] dati = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int durata_VALORE = 1024 - (회차 & 1);
            for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) dati[INDICE] = (INDICE + 회차) & 255;
            if (spazio_utente.inviare_dati(handle_VALORE, 0x0a000202, porta_VALORE, dati, durata_VALORE) != durata_VALORE) return 4;
            if (spazio_utente.ricevere_dati(handle_VALORE, dati, 300) != durata_VALORE) return 5;
            for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) if (dati[INDICE] != ((INDICE + 회차) & 255)) return 6;
        }
        spazio_utente.Chiudi_rete(handle_VALORE);
        spazio_utente.Scrittura("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
