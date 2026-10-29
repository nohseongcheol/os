// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sezione_VALORE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class dispositivo_di_archiviazione_connessione {
    static boolean reparto_IT_Disponibile = false;
    static int[] sezione_dati = new int[512];
    static void 잠깐기다리기() {
        for (int INDICE = 0; INDICE < 4; INDICE++) cellulare_VALORE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int avvia = cellulare_VALORE.밀리초();
        while (cellulare_VALORE.밀리초() - avvia < 500) {
            int Stato_VALORE = cellulare_VALORE.입출력바이트읽기(0x1f7);
            if (Stato_VALORE == 0 || Stato_VALORE == 255) return -19;
            if ((Stato_VALORE & 128) == 0) {
                if ((Stato_VALORE & 33) != 0) return -5;
                if (!자료필요 || (Stato_VALORE & 8) != 0) return 0;
            }
            cellulare_VALORE.잠시양보();
        }
        return -110;
    }
    static int richiesta(int sezione_VALORE, int comando) {
        if (sezione_VALORE < 0 || sezione_VALORE >= 2048) return -22;
        cellulare_VALORE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ usare_VALORE 안 함
        cellulare_VALORE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int risultato = 준비기다리기(false);
        if (risultato < 0) return risultato;
        cellulare_VALORE.입출력바이트쓰기(0x1f2, 1);
        cellulare_VALORE.입출력바이트쓰기(0x1f3, sezione_VALORE & 255);
        cellulare_VALORE.입출력바이트쓰기(0x1f4, (sezione_VALORE >>> 8) & 255);
        cellulare_VALORE.입출력바이트쓰기(0x1f5, 0);
        cellulare_VALORE.입출력바이트쓰기(0x1f7, comando); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Lettura(int sezione_VALORE) {
        int risultato = richiesta(sezione_VALORE, 0x20);
        if (risultato < 0) return risultato;
        for (int INDICE = 0; INDICE < 256; INDICE++) {
            int VALORE = cellulare_VALORE.입출력짧은수읽기(0x1f0);
            sezione_dati[INDICE * 2] = VALORE & 255; sezione_dati[INDICE * 2 + 1] = VALORE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Scrittura(int sezione_VALORE) {
        if (!reparto_IT_Disponibile || sezione_VALORE < 1 || sezione_VALORE > 518) return -19;
        int risultato = richiesta(sezione_VALORE, 0x30);
        if (risultato < 0) return risultato;
        for (int INDICE = 0; INDICE < 256; INDICE++)
            cellulare_VALORE.입출력짧은수쓰기(0x1f0, sezione_dati[INDICE * 2] | sezione_dati[INDICE * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int allineato_output() {
        if (!reparto_IT_Disponibile) return -19;
        cellulare_VALORE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analizzare_intero(int posizione) {
        return sezione_dati[posizione] | sezione_dati[posizione + 1] << 8 | sezione_dati[posizione + 2] << 16 | sezione_dati[posizione + 3] << 24;
    }
    static void scrivere_intero_VALORE(int posizione, int VALORE) {
        for (int INDICE = 0; INDICE < 4; INDICE++) sezione_dati[posizione + INDICE] = (VALORE >>> (INDICE * 8)) & 255;
    }
}
