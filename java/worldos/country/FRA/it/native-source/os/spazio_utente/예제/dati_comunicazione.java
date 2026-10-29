// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class dati_comunicazione {
    static int cifra_VALORE(String testo) {
        if (testo == null || testo.length() == 0) return -1;
        int risultato = 0;
        for (int INDICE = 0; INDICE < testo.length(); INDICE++) {
            int VALORE = testo.charAt(INDICE) - '0';
            if (VALORE < 0 || VALORE > 9 || risultato > 6553) return -1;
            risultato = risultato * 10 + VALORE;
            if (risultato > 65535) return -1;
        }
        return risultato;
    }
    static int e_mail(String testo) {
        if (testo == null) return 0;
        int VALORE = 0, risultato = 0, 부분 = 0, 자릿수 = 0;
        for (int INDICE = 0; INDICE <= testo.length(); INDICE++) {
            int 문자 = INDICE == testo.length() ? '.' : testo.charAt(INDICE);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                risultato = (risultato << 8) | VALORE; 부분++; VALORE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALORE = VALORE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALORE > 255) return 0;
            }
        }
        return 부분 == 4 ? risultato : 0;
    }
    public static int avvia() {
        if (spazio_utente.인수개수() != 3) { spazio_utente.Scrittura("Usage: run udp IP PORT TEXT\n"); return 2; }
        int e_mail = e_mail(spazio_utente.argomenti(0)), porta_VALORE = cifra_VALORE(spazio_utente.argomenti(1));
        String Contenuto_VALORE = spazio_utente.argomenti(2);
        if (e_mail == 0 || porta_VALORE < 1 || Contenuto_VALORE.length() > 1024) { spazio_utente.Scrittura("Bad destination\n"); return 2; }
        int handle_VALORE = spazio_utente.aperto_rete(0);
        if (handle_VALORE < 0) { spazio_utente.Scrittura("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] dati = new int[1024];
        for (int INDICE = 0; INDICE < Contenuto_VALORE.length(); INDICE++) dati[INDICE] = Contenuto_VALORE.charAt(INDICE);
        if (spazio_utente.inviare_dati(handle_VALORE, e_mail, porta_VALORE, dati, Contenuto_VALORE.length()) < 0) {
            spazio_utente.Scrittura("UDP SEND FAILED\n"); spazio_utente.Chiudi_rete(handle_VALORE); return 4;
        }
        spazio_utente.Scrittura("UDP SENT\n");
        int RICEV_SCAD_durata = spazio_utente.ricevere_dati(handle_VALORE, dati, 1500);
        boolean 같음 = RICEV_SCAD_durata == Contenuto_VALORE.length() && spazio_utente.보낸주소(handle_VALORE) == e_mail && spazio_utente.보낸창구(handle_VALORE) == porta_VALORE;
        if (같음) for (int INDICE = 0; INDICE < RICEV_SCAD_durata; INDICE++) if (dati[INDICE] != Contenuto_VALORE.charAt(INDICE)) 같음 = false;
        spazio_utente.Chiudi_rete(handle_VALORE);
        if (RICEV_SCAD_durata < 0) { spazio_utente.Scrittura("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        spazio_utente.Scrittura(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
