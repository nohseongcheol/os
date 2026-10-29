// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM file 64개, 파일당 16384바이트, descrittore_voce 16개. 모든 dati/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. negativo_VALORE 반환은 errore 번호다.
 */
public final class FileMemoria {
    static final int File_CONTA_NUMERI = 64;
    static int[] Nome = new int[File_CONTA_NUMERI * 64];
    static int[] 이름길이 = new int[File_CONTA_NUMERI];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Contenuto_VALORE = new int[File_CONTA_NUMERI * 4096];
    static int[] durata_VALORE = new int[File_CONTA_NUMERI];
    static int[] fonti_CONTA_NUMERI = new int[File_CONTA_NUMERI];
    static int[] usare_VALORE = new int[16];
    static int[] target = new int[16];
    static int[] posizione = new int[16];
    static int[] metodo_MODA = new int[16];
    static int[] percorso = new int[64];
    static int percorso_durata;

    public static int 파일한도() { return File_CONTA_NUMERI; }
    static int 자료읽기(int file, int funzione_INDICE) { return (Contenuto_VALORE[file * 4096 + funzione_INDICE / 4] >>> ((funzione_INDICE & 3) * 8)) & 255; }
    static void scrivere_dati(int file, int funzione_INDICE, int VALORE) {
        int slot_voce = file * 4096 + funzione_INDICE / 4, spostare_VALORE = (funzione_INDICE & 3) * 8;
        Contenuto_VALORE[slot_voce] = (Contenuto_VALORE[slot_voce] & ~(255 << spostare_VALORE)) | ((VALORE & 255) << spostare_VALORE);
    }

    public static int percorso_START(int Dimensione) {
        percorso_durata = 0;
        if (Dimensione < 1 || Dimensione > 63) return -36;
        percorso_durata = Dimensione;
        for (int Loop_INDICE = 0; Loop_INDICE < Dimensione; Loop_INDICE++) percorso[Loop_INDICE] = 0;
        return 0;
    }
    public static int percorso_byte(int INDICE, int VALORE) {
        if (INDICE < 0 || INDICE >= percorso_durata || VALORE < 1 || VALORE > 255) return -22;
        percorso[INDICE] = VALORE; return 0;
    }
    static int TROVA_voce() {
        for (int File_INDICE = 0; File_INDICE < File_CONTA_NUMERI; File_INDICE++) if (이름길이[File_INDICE] > 0 && 이름길이[File_INDICE] == Canonical_durata && 접두(Nome, File_INDICE * 64, 이름길이[File_INDICE], Canonical_VALORE, Canonical_durata)) return File_INDICE;
        return -1;
    }
    public static int Apri(int 플래그) {
        if (percorso_durata == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDICE = 0; Loop_INDICE < percorso_durata; Loop_INDICE++) if (percorso[Loop_INDICE] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int risultato = normalizzare_VALORE(); if (risultato < 0) return risultato;
        if (TROVA_elenco(Canonical_durata) >= 0) return -21;
        risultato = assegno_padre(); if (risultato < 0) return risultato;
        int file = TROVA_voce();
        if (file >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (file < 0 && (플래그 & 0x40) == 0) return -2;
        int descrittore_voce = -1;
        for (int Loop_INDICE = 0; Loop_INDICE < 16; Loop_INDICE++) if (usare_VALORE[Loop_INDICE] == 0) { descrittore_voce = Loop_INDICE; break; }
        if (descrittore_voce < 0) return -24;
        if (file < 0) {
            for (int Loop_INDICE = 0; Loop_INDICE < File_CONTA_NUMERI; Loop_INDICE++) if (이름길이[Loop_INDICE] == 0 && fonti_CONTA_NUMERI[Loop_INDICE] == 0) { file = Loop_INDICE; break; }
            if (file < 0) return -28;
            이름길이[file] = Canonical_durata;
            for (int Loop_INDICE = 0; Loop_INDICE < Canonical_durata; Loop_INDICE++) Nome[file * 64 + Loop_INDICE] = Canonical_VALORE[Loop_INDICE];
            durata_VALORE[file] = 0;
        }
        if ((플래그 & 0x200) != 0) durata_VALORE[file] = 0;
        usare_VALORE[descrittore_voce] = 1; target[descrittore_voce] = file; posizione[descrittore_voce] = 0; metodo_MODA[descrittore_voce] = 플래그;
        fonti_CONTA_NUMERI[file]++;
        return descrittore_voce + 3;
    }
    static int verificare(int descrittore_voce) {
        return descrittore_voce >= 3 && descrittore_voce < 19 && usare_VALORE[descrittore_voce - 3] != 0 ? descrittore_voce - 3 : -1;
    }
    public static int Lettura(int descrittore_voce) {
        int slot_voce = verificare(descrittore_voce);
        if (slot_voce < 0 || (metodo_MODA[slot_voce] & 3) == 1) return -9;
        int file = target[slot_voce];
        if (posizione[slot_voce] >= durata_VALORE[file]) return 256; // EOF와 effettivo_dati 0x00..0xff 구별
        return 자료읽기(file, posizione[slot_voce]++);
    }
    public static int Scrittura(int descrittore_voce, int VALORE) {
        int slot_voce = verificare(descrittore_voce);
        if (slot_voce < 0 || (metodo_MODA[slot_voce] & 3) == 0) return -9;
        int file = target[slot_voce];
        if ((metodo_MODA[slot_voce] & 0x400) != 0) posizione[slot_voce] = durata_VALORE[file];
        if (posizione[slot_voce] >= 16384) return -28;
        while (durata_VALORE[file] < posizione[slot_voce]) scrivere_dati(file, durata_VALORE[file]++, 0);
        scrivere_dati(file, posizione[slot_voce]++, VALORE);
        if (durata_VALORE[file] < posizione[slot_voce]) durata_VALORE[file] = posizione[slot_voce];
        return 1;
    }
    public static int cercare_funzione(int descrittore_voce, int 거리, int azione_radice) {
        int slot_voce = verificare(descrittore_voce);
        if (slot_voce < 0) return -9;
        if (azione_radice < 0 || azione_radice > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (azione_radice == 0 ? 0 : azione_radice == 1 ? posizione[slot_voce] : durata_VALORE[target[slot_voce]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        posizione[slot_voce] = 새위치; return 새위치;
    }
    public static int Chiudi(int descrittore_voce) {
        int slot_voce = verificare(descrittore_voce);
        if (slot_voce < 0) return -9;
        fonti_CONTA_NUMERI[target[slot_voce]]--; usare_VALORE[slot_voce] = 0; return 0;
    }
    public static int Dimensione(int descrittore_voce) {
        int slot_voce = verificare(descrittore_voce); return slot_voce < 0 ? -9 : durata_VALORE[target[slot_voce]];
    }
    public static int set_durata(int descrittore_voce, int Dimensione) {
        int slot_voce = verificare(descrittore_voce);
        if (slot_voce < 0 || (metodo_MODA[slot_voce] & 3) == 0) return -9;
        if (Dimensione < 0 || Dimensione > 16384) return -22;
        int file = target[slot_voce];
        while (durata_VALORE[file] < Dimensione) scrivere_dati(file, durata_VALORE[file]++, 0);
        durata_VALORE[file] = Dimensione; return 0;
    }
    public static int cancellare_voce() {
        if (percorso_durata == 0) return -22;
        int risultato = normalizzare_VALORE(); if (risultato < 0) return risultato;
        if (TROVA_elenco(Canonical_durata) >= 0) return -21;
        risultato = assegno_padre(); if (risultato < 0) return risultato;
        int file = TROVA_voce();
        if (file < 0) return -2;
        이름길이[file] = 0; return 0; // 열려 있는 파일은 마지막 close까지 mantenere_VALORE
    }
    static void voce_elenco() {
        percorso_START(1); percorso_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDICE) {
        if (INDICE < 0 || INDICE >= File_CONTA_NUMERI || 이름길이[INDICE] == 0) return 0;
        for (int Loop_INDICE = 0; Loop_INDICE < 이름길이[INDICE]; Loop_INDICE++) if (Nome[INDICE * 64 + Loop_INDICE] == '/') return 0;
        return 이름길이[INDICE];
    }
    public static int 공개이름바이트(int INDICE, int funzione_INDICE) {
        return INDICE >= 0 && INDICE < File_CONTA_NUMERI && funzione_INDICE >= 0 && funzione_INDICE < 이름길이[INDICE] ? Nome[INDICE * 64 + funzione_INDICE] : -22;
    }
    public static int 공개파일크기(int INDICE) { return INDICE >= 0 && INDICE < File_CONTA_NUMERI ? durata_VALORE[INDICE] : -22; }
    static int[] Canonical_VALORE = new int[64], Regolari_articolo = new int[64], elenco_nome = new int[16 * 64], elenco_durata = new int[16];
    static int Canonical_durata, Regolari_durata;
    static boolean 접두(int[] 이름들, int avvia, int percorso_VALORE, int[] frontale_VALORE, int interlinea_percorso) {
        if (percorso_VALORE < interlinea_percorso) return false;
        for (int Loop_INDICE = 0; Loop_INDICE < interlinea_percorso; Loop_INDICE++) if (이름들[avvia + Loop_INDICE] != frontale_VALORE[Loop_INDICE]) return false;
        return true;
    }
    static int normalizzare_VALORE() {
        if (percorso_durata == 0) return -22;
        Canonical_durata = percorso[0] == '/' ? 0 : Regolari_durata;
        for (int Loop_INDICE = 0; Loop_INDICE < Canonical_durata; Loop_INDICE++) Canonical_VALORE[Loop_INDICE] = Regolari_articolo[Loop_INDICE];
        int 읽는자리 = 0;
        while (읽는자리 < percorso_durata) {
            while (읽는자리 < percorso_durata && percorso[읽는자리] == '/') 읽는자리++;
            int START_funzione = 읽는자리; while (읽는자리 < percorso_durata && percorso[읽는자리] != '/') { if (percorso[읽는자리] == 0) return -22; 읽는자리++; }
            int voce_CONTA_NUMERI = 읽는자리 - START_funzione; if (voce_CONTA_NUMERI == 0 || voce_CONTA_NUMERI == 1 && percorso[START_funzione] == '.') continue;
            if (voce_CONTA_NUMERI == 2 && percorso[START_funzione] == '.' && percorso[START_funzione + 1] == '.') {
                while (Canonical_durata > 0 && Canonical_VALORE[Canonical_durata - 1] != '/') Canonical_durata--;
                if (Canonical_durata > 0) Canonical_durata--;
                continue;
            }
            if (Canonical_durata + voce_CONTA_NUMERI + (Canonical_durata == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_durata > 0) Canonical_VALORE[Canonical_durata++] = '/';
            for (int Loop_INDICE = START_funzione; Loop_INDICE < 읽는자리; Loop_INDICE++) Canonical_VALORE[Canonical_durata++] = percorso[Loop_INDICE];
        }
        return 0;
    }
    static int TROVA_elenco(int voce_CONTA_NUMERI) {
        if (voce_CONTA_NUMERI == 0) return 0;
        for (int Loop_INDICE = 1; Loop_INDICE < 16; Loop_INDICE++) if (elenco_durata[Loop_INDICE] == voce_CONTA_NUMERI && 접두(elenco_nome, Loop_INDICE * 64, voce_CONTA_NUMERI, Canonical_VALORE, voce_CONTA_NUMERI)) return Loop_INDICE;
        return -1;
    }
    static int assegno_padre() {
        int voce_CONTA_NUMERI = Canonical_durata; while (voce_CONTA_NUMERI > 0 && Canonical_VALORE[voce_CONTA_NUMERI - 1] != '/') voce_CONTA_NUMERI--;
        return TROVA_elenco(voce_CONTA_NUMERI == 0 ? 0 : voce_CONTA_NUMERI - 1) < 0 ? -2 : 0;
    }
    public static int Crea_elenco() {
        int 처리값 = normalizzare_VALORE(); if (처리값 < 0) return 처리값;
        if (TROVA_elenco(Canonical_durata) >= 0 || TROVA_voce() >= 0) return -17;
        처리값 = assegno_padre(); if (처리값 < 0) return 처리값;
        for (int Loop_INDICE = 1; Loop_INDICE < 16; Loop_INDICE++) if (elenco_durata[Loop_INDICE] == 0) {
            elenco_durata[Loop_INDICE] = Canonical_durata; for (int inner_funzione = 0; inner_funzione < Canonical_durata; inner_funzione++) elenco_nome[Loop_INDICE * 64 + inner_funzione] = Canonical_VALORE[inner_funzione]; return 0;
        }
        return -28;
    }
    public static int voce_Kind() {
        int 처리값 = normalizzare_VALORE(); if (처리값 < 0) return 처리값;
        if (TROVA_elenco(Canonical_durata) >= 0) return 2;
        return TROVA_voce() >= 0 ? 1 : 0;
    }
    public static int cambiare_elenco() {
        int 처리값 = normalizzare_VALORE(); if (처리값 < 0) return 처리값;
        if (TROVA_elenco(Canonical_durata) < 0) return -2;
        Regolari_durata = Canonical_durata; for (int Loop_INDICE = 0; Loop_INDICE < Regolari_durata; Loop_INDICE++) Regolari_articolo[Loop_INDICE] = Canonical_VALORE[Loop_INDICE]; return 0;
    }
    public static int rimuovere_elenco() {
        int 처리값 = normalizzare_VALORE(); if (처리값 < 0) return 처리값;
        int elenco_numero = TROVA_elenco(Canonical_durata); if (elenco_numero < 0) return -2; if (elenco_numero == 0) return -16;
        if (Regolari_durata == Canonical_durata && 접두(Regolari_articolo, 0, Regolari_durata, Canonical_VALORE, Canonical_durata)) return -16;
        for (int Loop_INDICE = 0; Loop_INDICE < File_CONTA_NUMERI; Loop_INDICE++) {
            if (이름길이[Loop_INDICE] > Canonical_durata && 접두(Nome, Loop_INDICE * 64, 이름길이[Loop_INDICE], Canonical_VALORE, Canonical_durata) && Nome[Loop_INDICE * 64 + Canonical_durata] == '/') return -39;
        }
        for (int Loop_INDICE = 0; Loop_INDICE < 16; Loop_INDICE++) {
            if (elenco_durata[Loop_INDICE] > Canonical_durata && 접두(elenco_nome, Loop_INDICE * 64, elenco_durata[Loop_INDICE], Canonical_VALORE, Canonical_durata) && elenco_nome[Loop_INDICE * 64 + Canonical_durata] == '/') return -39;
        }
        elenco_durata[elenco_numero] = 0; return 0;
    }
    public static int Rinomina_voce(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= File_CONTA_NUMERI || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizzare_VALORE(); if (처리값 < 0) return 처리값;
        if (TROVA_elenco(Canonical_durata) >= 0) return -21;
        처리값 = assegno_padre(); if (처리값 < 0) return 처리값;
        int Indietro_VALORE = TROVA_voce(); if (Indietro_VALORE == 원본번호) return 0;
        if (Indietro_VALORE >= 0) 이름길이[Indietro_VALORE] = 0;
        이름길이[원본번호] = Canonical_durata; for (int Loop_INDICE = 0; Loop_INDICE < Canonical_durata; Loop_INDICE++) Nome[원본번호 * 64 + Loop_INDICE] = Canonical_VALORE[Loop_INDICE]; return 0;
    }
    static int voce_START(int[] dati_array, int 시작점, int voce_CONTA_NUMERI) {
        if (!접두(dati_array, 시작점, voce_CONTA_NUMERI, Canonical_VALORE, Canonical_durata)) return -1;
        int START_funzione = Canonical_durata;
        if (START_funzione > 0) { if (voce_CONTA_NUMERI <= START_funzione || dati_array[시작점 + START_funzione] != '/') return -1; START_funzione++; }
        if (voce_CONTA_NUMERI <= START_funzione) return -1;
        for (int Loop_INDICE = START_funzione; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) if (dati_array[시작점 + Loop_INDICE] == '/') return -1;
        return START_funzione;
    }
    static void Regolari_scrivere() { 단말.문자('/'); for (int Loop_INDICE = 0; Loop_INDICE < Regolari_durata; Loop_INDICE++) scheda.scrivere_seriale(Regolari_articolo[Loop_INDICE]); }
    static int 경로목록() {
        int 처리값 = normalizzare_VALORE(); if (처리값 < 0) return 처리값;
        int File_target = TROVA_voce();
        if (File_target >= 0) { for (int Loop_INDICE = 0; Loop_INDICE < Canonical_durata; Loop_INDICE++) scheda.scrivere_seriale(Canonical_VALORE[Loop_INDICE]); 단말.Scrittura("  "); 단말.numero(durata_VALORE[File_target]); 단말.Scrittura("byte_VALORE(주기억 file)\n"); return 0; }
        if (TROVA_elenco(Canonical_durata) < 0) return -2;
        for (int finale_VALORE = 1; finale_VALORE < 16; finale_VALORE++) if (elenco_durata[finale_VALORE] > 0) {
            int START_funzione = voce_START(elenco_nome, finale_VALORE * 64, elenco_durata[finale_VALORE]); if (START_funzione < 0) continue;
            for (int Loop_INDICE = START_funzione; Loop_INDICE < elenco_durata[finale_VALORE]; Loop_INDICE++) scheda.scrivere_seriale(elenco_nome[finale_VALORE * 64 + Loop_INDICE]); 단말.Scrittura("/\n");
        }
        for (int File_INDICE = 0; File_INDICE < File_CONTA_NUMERI; File_INDICE++) if (이름길이[File_INDICE] > 0) {
            int START_funzione = voce_START(Nome, File_INDICE * 64, 이름길이[File_INDICE]); if (START_funzione < 0) continue;
            for (int Loop_INDICE = START_funzione; Loop_INDICE < 이름길이[File_INDICE]; Loop_INDICE++) scheda.scrivere_seriale(Nome[File_INDICE * 64 + Loop_INDICE]);
            단말.Scrittura("  "); 단말.numero(durata_VALORE[File_INDICE]); 단말.Scrittura("byte_VALORE(주기억 file)\n");
        }
        return 0;
    }
}
