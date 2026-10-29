// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALORE formato_VALORE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, generazione_numero = 0;
    static int[] File_tabella = new int[1024];
    static int 바이트해시(int VALORE, int dati) { return (VALORE ^ dati) * 16777619; }
    static void liquidare_dati() {
        for (int INDICE = 0; INDICE < 512; INDICE++) dispositivo_di_archiviazione_connessione.sezione_dati[INDICE] = 0;
    }
    static int tabella_intero(int posizione) {
        return File_tabella[posizione] | File_tabella[posizione + 1] << 8 | File_tabella[posizione + 2] << 16 | File_tabella[posizione + 3] << 24;
    }
    static void scrivere_tabella_intero(int posizione, int VALORE) {
        for (int INDICE = 0; INDICE < 4; INDICE++) File_tabella[posizione + INDICE] = (VALORE >>> (INDICE * 8)) & 255;
    }
    static boolean assegno_tabella() {
        for (int file = 0; file < 8; file++) {
            int durata_VALORE = 0;
            for (int slot_voce = 0; slot_voce < 64; slot_voce++) Memoria_file_system.Nome[slot_voce] = File_tabella[file * 72 + slot_voce];
            while (durata_VALORE < 64 && Memoria_file_system.Nome[durata_VALORE] != 0) durata_VALORE++;
            if (durata_VALORE == 0) continue;
            if (!Memoria_file_system.assegno_nome(Memoria_file_system.Nome, durata_VALORE)
                || tabella_intero(file * 72 + 64) < 0 || tabella_intero(file * 72 + 64) > 16384) return false;
            for (int frontale_VALORE = 0; frontale_VALORE < file; frontale_VALORE++) {
                boolean 같음 = File_tabella[frontale_VALORE * 72 + durata_VALORE] == 0;
                for (int slot_voce = 0; slot_voce < durata_VALORE; slot_voce++) if (File_tabella[frontale_VALORE * 72 + slot_voce] != Memoria_file_system.Nome[slot_voce]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_sezione = 1 + 보존본 * 259;
        if (dispositivo_di_archiviazione_connessione.Lettura(START_sezione) < 0 || dispositivo_di_archiviazione_connessione.analizzare_intero(0) != 0x4a4b534e) return -1;
        int generazione_VALORE = dispositivo_di_archiviazione_connessione.analizzare_intero(4), checksum = dispositivo_di_archiviazione_connessione.analizzare_intero(8);
        if (generazione_VALORE < 1 || dispositivo_di_archiviazione_connessione.analizzare_intero(12) != (generazione_VALORE ^ checksum ^ 0x4a4b534e)) return -1;
        int hash_File = 0x811c9dc5;
        for (int sezione_VALORE = 0; sezione_VALORE < 258; sezione_VALORE++) {
            if (dispositivo_di_archiviazione_connessione.Lettura(START_sezione + 1 + sezione_VALORE) < 0) return -1;
            for (int slot_voce = 0; slot_voce < 512; slot_voce++) {
                int VALORE = dispositivo_di_archiviazione_connessione.sezione_dati[slot_voce];
                hash_File = 바이트해시(hash_File, VALORE);
                if (sezione_VALORE < 2) File_tabella[sezione_VALORE * 512 + slot_voce] = VALORE;
            }
        }
        return hash_File == checksum && assegno_tabella() ? generazione_VALORE : -1;
    }
    static int caricaSorgente(int 보존본) {
        int START_sezione = 1 + 보존본 * 259;
        for (int sezione_VALORE = 0; sezione_VALORE < 2; sezione_VALORE++) {
            if (dispositivo_di_archiviazione_connessione.Lettura(START_sezione + 1 + sezione_VALORE) < 0) return -5;
            for (int slot_voce = 0; slot_voce < 512; slot_voce++) File_tabella[sezione_VALORE * 512 + slot_voce] = dispositivo_di_archiviazione_connessione.sezione_dati[slot_voce];
        }
        for (int file = 0; file < 8; file++) {
            for (int slot_voce = 0; slot_voce < 64; slot_voce++) Memoria_file_system.이름들[file * 64 + slot_voce] = File_tabella[file * 72 + slot_voce];
            Memoria_file_system.ridimensionare_elenco[file] = File_tabella[file * 72] == 0 ? 0 : tabella_intero(file * 72 + 64);
            Memoria_file_system.허가들[file] = tabella_intero(file * 72 + 68) & 511;
            for (int sezione_VALORE = 0; sezione_VALORE < 32; sezione_VALORE++) {
                if (dispositivo_di_archiviazione_connessione.Lettura(START_sezione + 3 + file * 32 + sezione_VALORE) < 0) return -5;
                int e_mail = cellulare_VALORE.File_Memoria() + file * 16384 + sezione_VALORE * 512;
                for (int slot_voce = 0; slot_voce < 512; slot_voce++) cellulare_VALORE.scrivere_Memoria(e_mail + slot_voce, dispositivo_di_archiviazione_connessione.sezione_dati[slot_voce]);
            }
        }
        return 0;
    }
    static void Prepara() {
        if (dispositivo_di_archiviazione_connessione.Lettura(0) < 0 || dispositivo_di_archiviazione_connessione.analizzare_intero(0) != 0x54534b4a
            || dispositivo_di_archiviazione_connessione.analizzare_intero(4) != 0x3145524f || dispositivo_di_archiviazione_connessione.analizzare_intero(8) != 2048
            || dispositivo_di_archiviazione_connessione.analizzare_intero(12) != 0x3153464a) {
            SMS_Terminale.Scrittura("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        dispositivo_di_archiviazione_connessione.reparto_IT_Disponibile = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminale.Scrittura("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; generazione_numero = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (caricaSorgente(현재보존본) < 0) {
            SMS_Terminale.Scrittura("STORE read failed; halted to preserve files\n"); cellulare_VALORE.정지();
        }
        SMS_Terminale.Scrittura("STORE restored generation "); SMS_Terminale.scrivere_numero(generazione_numero); SMS_Terminale.문자(10);
    }
    static int sincronizzare() {
        if (!dispositivo_di_archiviazione_connessione.reparto_IT_Disponibile) return -19;
        if (generazione_numero == 2147483647) return -75;
        int Avanti_articolo = 현재보존본 == 0 ? 1 : 0, START_sezione = 1 + Avanti_articolo * 259;
        // 새 본문보다 먼저 Indietro_articolo commit을 무효화하고 cellulare_VALORE 캐시를 비운다.
        liquidare_dati();
        if (dispositivo_di_archiviazione_connessione.Scrittura(START_sezione) < 0 || dispositivo_di_archiviazione_connessione.allineato_output() < 0) return -5;
        for (int slot_voce = 0; slot_voce < 1024; slot_voce++) File_tabella[slot_voce] = 0;
        for (int file = 0; file < 8; file++) if (Memoria_file_system.이름들[file * 64] != 0) {
            for (int slot_voce = 0; slot_voce < 64; slot_voce++) File_tabella[file * 72 + slot_voce] = Memoria_file_system.이름들[file * 64 + slot_voce];
            scrivere_tabella_intero(file * 72 + 64, Memoria_file_system.ridimensionare_elenco[file]);
            scrivere_tabella_intero(file * 72 + 68, Memoria_file_system.허가들[file]);
        }
        int hash_File = 0x811c9dc5;
        for (int sezione_VALORE = 0; sezione_VALORE < 258; sezione_VALORE++) {
            for (int slot_voce = 0; slot_voce < 512; slot_voce++) {
                int VALORE = 0;
                if (sezione_VALORE < 2) VALORE = File_tabella[sezione_VALORE * 512 + slot_voce];
                else {
                    int file = (sezione_VALORE - 2) / 32, posizione = (sezione_VALORE - 2) % 32 * 512 + slot_voce;
                    if (File_tabella[file * 72] != 0 && posizione < Memoria_file_system.ridimensionare_elenco[file])
                        VALORE = cellulare_VALORE.기억읽기(cellulare_VALORE.File_Memoria() + file * 16384 + posizione);
                }
                dispositivo_di_archiviazione_connessione.sezione_dati[slot_voce] = VALORE; hash_File = 바이트해시(hash_File, VALORE);
            }
            if (dispositivo_di_archiviazione_connessione.Scrittura(START_sezione + 1 + sezione_VALORE) < 0) return -5;
        }
        if (dispositivo_di_archiviazione_connessione.allineato_output() < 0) return -5;
        liquidare_dati(); dispositivo_di_archiviazione_connessione.scrivere_intero_VALORE(0, 0x4a4b534e);
        dispositivo_di_archiviazione_connessione.scrivere_intero_VALORE(4, generazione_numero + 1); dispositivo_di_archiviazione_connessione.scrivere_intero_VALORE(8, hash_File);
        dispositivo_di_archiviazione_connessione.scrivere_intero_VALORE(12, (generazione_numero + 1) ^ hash_File ^ 0x4a4b534e);
        if (dispositivo_di_archiviazione_connessione.Scrittura(START_sezione) < 0 || dispositivo_di_archiviazione_connessione.allineato_output() < 0) return -5;
        현재보존본 = Avanti_articolo; generazione_numero++;
        return 0;
    }
}
