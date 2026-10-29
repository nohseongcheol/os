// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Kirjoitus 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] syöte_ARVO = new int[128];
    static int kesto_ARVO = 0;
    static boolean 앞줄복귀 = false;
    static boolean rivi_ylivuoto = false;

    static boolean komento(String Nimi) {
        if (kesto_ARVO < Nimi.length()) return false;
        for (int INDEKSI = 0; INDEKSI < Nimi.length(); INDEKSI++)
            if (syöte_ARVO[INDEKSI] != Nimi.charAt(INDEKSI)) return false;
        return kesto_ARVO == Nimi.length() || syöte_ARVO[Nimi.length()] == ' ';
    }

    static void näytä_ohje() {
        SMS_Pääte.Kirjoitus("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Pääte.Kirjoitus("apps | run NAME [ARGS] | net\n");
        SMS_Pääte.Kirjoitus("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Pääte.Kirjoitus("sync (연결된 JKSTORE1 Store_ARVO 장치에 tiedoston_nimi 보존)\n");
    }

    static void prosessi_ARVO_merkintä() {
        if (kesto_ARVO == 0) return;
        if (komento("help")) näytä_ohje();
        else if (komento("sync")) {
            int TULOS = 파일보존.synkronoi();
            SMS_Pääte.Kirjoitus("Sync: "); SMS_Pääte.kirjoitus_numero(TULOS); SMS_Pääte.문자(10);
        }
        else if (komento("ls")) Muisti_tiedostojärjestelmä.merkintä_luettelo();
        else if (komento("edit")) Muisti_tiedostojärjestelmä.komento(syöte_ARVO, 4, kesto_ARVO, 0);
        else if (komento("cat")) Muisti_tiedostojärjestelmä.komento(syöte_ARVO, 3, kesto_ARVO, 1);
        else if (komento("rm")) Muisti_tiedostojärjestelmä.komento(syöte_ARVO, 2, kesto_ARVO, 2);
        else if (komento("java") || komento("javac")) {
            int TULOS = suoritus_Valvoja.Suorita_komento(syöte_ARVO, 0, kesto_ARVO);
            SMS_Pääte.Kirjoitus("Exit: "); SMS_Pääte.kirjoitus_numero(TULOS); SMS_Pääte.문자(10);
        }
        else if (komento("apps")) suoritus_Valvoja.merkintä_luettelo();
        else if (komento("net")) verkko_Pino.Tila_ARVO();
        else if (komento("run")) {
            int TULOS = suoritus_Valvoja.Suorita_komento(syöte_ARVO, 3, kesto_ARVO);
            SMS_Pääte.Kirjoitus("Exit: "); SMS_Pääte.kirjoitus_numero(TULOS); SMS_Pääte.Kirjoitus("\n");
        } else if (komento("info")) {
            SMS_Pääte.Kirjoitus("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (komento("mem")) {
            SMS_Pääte.Kirjoitus("위쪽 Muisti_ARVO OSOITE_alue(KiB): "); SMS_Pääte.kirjoitus_numero(Muisti_alue.ISOT_Muisti_muuttaa_kokoa());
            SMS_Pääte.Kirjoitus("\n배열 동적 Muisti_ARVO OSOITE_alue(tavu_ARVO): "); SMS_Pääte.kirjoitus_numero(laite_ARVO.MATRIISI_kulutus());
            SMS_Pääte.Kirjoitus(" / 262144\n작업 OSOITE_alue osa_ARVO: "); SMS_Pääte.kirjoitus_numero(Muisti_alue.사용개수());
            SMS_Pääte.Kirjoitus(" / 8 (각 4096바이트)\n");
        } else if (komento("alloc")) {
            int INDEKSI = Muisti_alue.jakaa_Tallennus();
            SMS_Pääte.Kirjoitus("osa_ARVO INDEKSI: "); SMS_Pääte.kirjoitus_numero(INDEKSI); SMS_Pääte.Kirjoitus("\n");
        } else if (komento("free")) {
            if (kesto_ARVO == 6 && syöte_ARVO[4] == ' ' && syöte_ARVO[5] >= '0' && syöte_ARVO[5] <= '7') {
                SMS_Pääte.Kirjoitus(Muisti_alue.palauttaa_KR(syöte_ARVO[5] - '0') ? "반환됨\n" : "할당되지 않은 osa_ARVO\n");
            } else SMS_Pääte.Kirjoitus("사용법: free 0..7\n");
        } else if (komento("echo")) {
            for (int INDEKSI = 5; INDEKSI < kesto_ARVO; INDEKSI++) SMS_Pääte.문자(syöte_ARVO[INDEKSI]);
            SMS_Pääte.문자(10);
        } else if (komento("clear")) SMS_Pääte.poistaa_merkintä_c8dbc399();
        else if (komento("test")) ydin.testit();
        else if (komento("halt")) {
            SMS_Pääte.Kirjoitus("HALTED\n");
            laite_ARVO.정지();
        } else SMS_Pääte.Kirjoitus("알 numero 없는 명령입니다. help를 입력하세요.\n");
    }

    static void hyväksyä_JA_kirjoitus(int ARVO) {
        if (ARVO == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = ARVO == 13;
        if (ARVO == 10 || ARVO == 13) {
            SMS_Pääte.문자(10);
            if (Muisti_tiedostojärjestelmä.편집중) Muisti_tiedostojärjestelmä.Muokattu_rivi(syöte_ARVO, kesto_ARVO, rivi_ylivuoto);
            else prosessi_ARVO_merkintä();
            kesto_ARVO = 0;
            rivi_ylivuoto = false;
            SMS_Pääte.Kirjoitus(Muisti_tiedostojärjestelmä.편집중 ? "...> " : "jkoros> ");
        } else if (ARVO == 8 || ARVO == 127) {
            if (kesto_ARVO > 0) {
                kesto_ARVO--;
                SMS_Pääte.직렬바이트(8); SMS_Pääte.직렬바이트(32); SMS_Pääte.직렬바이트(8);
                SMS_Pääte.화면문자(8);
            }
        } else if (ARVO >= 32 && ARVO < 127 && kesto_ARVO < syöte_ARVO.length) {
            syöte_ARVO[kesto_ARVO++] = ARVO;
            SMS_Pääte.문자(ARVO);
        } else if (ARVO >= 32 && ARVO < 127) rivi_ylivuoto = true;
    }

    static void Suorita_2() {
        näytä_ohje();
        SMS_Pääte.Kirjoitus("READY\njkoros> ");
        while (true) {
            int ARVO = SMS_Pääte.직렬읽기();
            if (ARVO < 0) ARVO = näppäimistö.Luku();
            if (ARVO >= 0) hyväksyä_JA_kirjoitus(ARVO);
            else { verkko_Pino.tarkistaa(); laite_ARVO.잠시양보(); }
        }
    }
}
