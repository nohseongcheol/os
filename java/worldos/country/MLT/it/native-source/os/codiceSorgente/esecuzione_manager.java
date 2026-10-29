// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lettura 전용 Esegui_comando 묶음의 ELF32 convalidare, argomenti Avanti_VALORE, 한 번에 한 spazio_utente Processi_VALORE Esegui_comando. */
public final class esecuzione_manager {
    static final int START_USER_app = 0x04000000;
    static final int USER_chiudere = 0x04400000;
    static final int foto_indirizzo_finale = 0x04200000;
    static final int argomento_START = 0x04300000;
    static int argomento_CONTA_NUMERI = 0;
    static int[] argomento_e_mail = new int[16];

    static boolean ritagliare(int e_mail, int durata_VALORE) {
        return e_mail >= START_USER_app && e_mail < USER_chiudere && durata_VALORE >= 0 && durata_VALORE <= USER_chiudere - e_mail;
    }

    static int numero(int e_mail) { return Memoria_area.analizzare_intero(e_mail); }
    static int 짧은수(int e_mail) { return cellulare_VALORE.기억읽기(e_mail) | cellulare_VALORE.기억읽기(e_mail + 1) << 8; }
    static void scrivere_numero(int e_mail, int VALORE) {
        for (int INDICE = 0; INDICE < 4; INDICE++) cellulare_VALORE.scrivere_Memoria(e_mail + INDICE, VALORE >>> (INDICE * 8));
    }

    static int gruppo_CONTA_NUMERI() {
        int e_mail = cellulare_VALORE.eseguibile_aggregare();
        int Dimensione = cellulare_VALORE.eseguibile_aggregare_ridimensionare();
        if (Dimensione < 8 || numero(e_mail) != 0x50414b4a) return 0;
        int articolo_CONTA_NUMERI = numero(e_mail + 4);
        return articolo_CONTA_NUMERI >= 0 && articolo_CONTA_NUMERI <= 32 && articolo_CONTA_NUMERI <= (Dimensione - 8) / 24 ? articolo_CONTA_NUMERI : 0;
    }

    static void voce_elenco() {
        for (int INDICE = 0; INDICE < gruppo_CONTA_NUMERI(); INDICE++) {
            int voce_VALORE = cellulare_VALORE.eseguibile_aggregare() + 8 + INDICE * 24;
            for (int carattere_VALORE = 0; carattere_VALORE < 16 && cellulare_VALORE.기억읽기(voce_VALORE + carattere_VALORE) != 0; carattere_VALORE++)
                SMS_Terminale.문자(cellulare_VALORE.기억읽기(voce_VALORE + carattere_VALORE));
            SMS_Terminale.Scrittura("\n");
        }
    }

    static int TROVA_voce(int[] input_VALORE, int avvia, int durata_VALORE) {
        if (durata_VALORE <= 0 || durata_VALORE >= 16) return 0;
        for (int INDICE = 0; INDICE < gruppo_CONTA_NUMERI(); INDICE++) {
            int voce_VALORE = cellulare_VALORE.eseguibile_aggregare() + 8 + INDICE * 24;
            boolean 같음 = cellulare_VALORE.기억읽기(voce_VALORE + durata_VALORE) == 0;
            for (int carattere_VALORE = 0; carattere_VALORE < durata_VALORE; carattere_VALORE++)
                if (input_VALORE[avvia + carattere_VALORE] != cellulare_VALORE.기억읽기(voce_VALORE + carattere_VALORE)) 같음 = false;
            if (같음) return voce_VALORE;
        }
        return 0;
    }

    static int convalidare(int file, int durata_VALORE) {
        if (durata_VALORE < 52 || numero(file) != 0x464c457f || cellulare_VALORE.기억읽기(file + 4) != 1
            || cellulare_VALORE.기억읽기(file + 5) != 1 || cellulare_VALORE.기억읽기(file + 6) != 1
            || 짧은수(file + 16) != 2 || 짧은수(file + 18) != 3 || numero(file + 20) != 1
            || 짧은수(file + 40) != 52 || 짧은수(file + 42) != 32) return -8;
        int punto_di_ingresso_VALORE = numero(file + 24);
        int tabella_funzione = numero(file + 28);
        int articolo_CONTA_NUMERI = 짧은수(file + 44);
        if (articolo_CONTA_NUMERI == 0 || articolo_CONTA_NUMERI > 16 || tabella_funzione < 52 || tabella_funzione > durata_VALORE - articolo_CONTA_NUMERI * 32) return -8;
        boolean reparto_IT_eseguibile = false;
        for (int INDICE = 0; INDICE < articolo_CONTA_NUMERI; INDICE++) {
            int tabella_di_ricerca = file + tabella_funzione + INDICE * 32;
            int Kind_VALORE = numero(tabella_di_ricerca);
            if (Kind_VALORE == 2 || Kind_VALORE == 3) return -8; // 동적 Connetti/parser_48ee4b1b 미지원
            if (Kind_VALORE != 1) continue;
            int posizione = numero(tabella_di_ricerca + 4), e_mail = numero(tabella_di_ricerca + 8), dimensioni_del_file = numero(tabella_di_ricerca + 16), Memoria_ridimensionare = numero(tabella_di_ricerca + 20);
            int allineare_VALORE = numero(tabella_di_ricerca + 28);
            if (e_mail < START_USER_app || e_mail >= foto_indirizzo_finale || Memoria_ridimensionare < 0 || Memoria_ridimensionare > foto_indirizzo_finale - e_mail
                || dimensioni_del_file < 0 || dimensioni_del_file > Memoria_ridimensionare || posizione < 0 || (dimensioni_del_file > 0 && posizione > durata_VALORE - dimensioni_del_file)
                || (allineare_VALORE != 0 && (allineare_VALORE < 0 || (allineare_VALORE & (allineare_VALORE - 1)) != 0
                    || ((e_mail - posizione) & (allineare_VALORE - 1)) != 0))) return -8;
            for (int frontale_VALORE = 0; frontale_VALORE < INDICE; frontale_VALORE++) {
                int Indietro_articolo = file + tabella_funzione + frontale_VALORE * 32;
                if (numero(Indietro_articolo) == 1 && Memoria_ridimensionare > 0 && numero(Indietro_articolo + 20) > 0
                    && e_mail < numero(Indietro_articolo + 8) + numero(Indietro_articolo + 20) && numero(Indietro_articolo + 8) < e_mail + Memoria_ridimensionare) return -8;
            }
            if ((numero(tabella_di_ricerca + 24) & 1) != 0 && punto_di_ingresso_VALORE >= e_mail && punto_di_ingresso_VALORE - e_mail < dimensioni_del_file) reparto_IT_eseguibile = true;
        }
        return reparto_IT_eseguibile ? punto_di_ingresso_VALORE : -8;
    }

    static int Esegui_comando(int[] input_VALORE, int avvia, int durata_VALORE) {
        while (avvia < durata_VALORE && input_VALORE[avvia] == ' ') avvia++;
        int 끝 = avvia;
        while (끝 < durata_VALORE && input_VALORE[끝] != ' ') 끝++;
        int voce_VALORE = TROVA_voce(input_VALORE, avvia, 끝 - avvia);
        if (voce_VALORE == 0) return -2;
        int posizione = numero(voce_VALORE + 16), Dimensione = numero(voce_VALORE + 20);
        if (posizione < 8 + gruppo_CONTA_NUMERI() * 24 || Dimensione < 52 || posizione > cellulare_VALORE.eseguibile_aggregare_ridimensionare() - Dimensione) return -8;
        int file = cellulare_VALORE.eseguibile_aggregare() + posizione;
        int punto_di_ingresso_VALORE = convalidare(file, Dimensione);
        if (punto_di_ingresso_VALORE < 0) return punto_di_ingresso_VALORE;
        cellulare_VALORE.USER_liquidare_Sommario();
        int tabella_funzione = numero(file + 28), articolo_CONTA_NUMERI = 짧은수(file + 44);
        for (int INDICE = 0; INDICE < articolo_CONTA_NUMERI; INDICE++) {
            int tabella_di_ricerca = file + tabella_funzione + INDICE * 32;
            if (numero(tabella_di_ricerca) != 1) continue;
            int 원본 = file + numero(tabella_di_ricerca + 4), meta_VALORE = numero(tabella_di_ricerca + 8), dimensioni_del_file = numero(tabella_di_ricerca + 16);
            for (int byte_VALORE = 0; byte_VALORE < dimensioni_del_file; byte_VALORE++) cellulare_VALORE.scrivere_Memoria(meta_VALORE + byte_VALORE, cellulare_VALORE.기억읽기(원본 + byte_VALORE));
        }
        argomento_CONTA_NUMERI = 0;
        int Store_VALORE = argomento_START;
        while (끝 < durata_VALORE) {
            while (끝 < durata_VALORE && input_VALORE[끝] == ' ') 끝++;
            if (끝 == durata_VALORE) break;
            if (argomento_CONTA_NUMERI == argomento_e_mail.length) return -22;
            avvia = 끝;
            while (끝 < durata_VALORE && input_VALORE[끝] != ' ') 끝++;
            argomento_e_mail[argomento_CONTA_NUMERI++] = Store_VALORE;
            scrivere_numero(Store_VALORE, 끝 - avvia);
            for (int carattere_VALORE = avvia; carattere_VALORE < 끝; carattere_VALORE++) scrivere_numero(Store_VALORE + 4 + (carattere_VALORE - avvia) * 4, input_VALORE[carattere_VALORE]);
            Store_VALORE += 4 + (끝 - avvia) * 4;
        }
        rete_Pila.LIBERA_Processi();
        File_descrittore_manager.START_Processi();
        int risultato = cellulare_VALORE.eseguire_USER_app(punto_di_ingresso_VALORE, USER_chiudere - 16);
        File_descrittore_manager.LIBERA_Processi();
        rete_Pila.LIBERA_Processi();
        return risultato;
    }
}
