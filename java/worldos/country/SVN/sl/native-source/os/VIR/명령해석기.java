// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Pisanje 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int 길이 = 0;
    static boolean 앞줄복귀 = false;
    static boolean linija_presežek = false;

    static boolean Ukaz(String Ime) {
        if (길이 < Ime.length()) return false;
        for (int INDEX = 0; INDEX < Ime.length(); INDEX++)
            if (입력[INDEX] != Ime.charAt(INDEX)) return false;
        return 길이 == Ime.length() || 입력[Ime.length()] == ' ';
    }

    static void oddaja_spletna_pomoč() {
        SMS_Terminal.Pisanje("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Pisanje("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Pisanje("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Pisanje("sync (연결된 JKSTORE1 Store_VALUE 장치에 Datoteka 보존)\n");
    }

    static void Proces_VALUE_vnos() {
        if (길이 == 0) return;
        if (Ukaz("help")) oddaja_spletna_pomoč();
        else if (Ukaz("sync")) {
            int REZULTAT = 파일보존.sinhronizirati();
            SMS_Terminal.Pisanje("Sync: "); SMS_Terminal.수쓰기(REZULTAT); SMS_Terminal.문자(10);
        }
        else if (Ukaz("ls")) pomnilnik_datotečni_sistem.vnos_Seznam();
        else if (Ukaz("edit")) pomnilnik_datotečni_sistem.Ukaz(입력, 4, 길이, 0);
        else if (Ukaz("cat")) pomnilnik_datotečni_sistem.Ukaz(입력, 3, 길이, 1);
        else if (Ukaz("rm")) pomnilnik_datotečni_sistem.Ukaz(입력, 2, 길이, 2);
        else if (Ukaz("java") || Ukaz("javac")) {
            int REZULTAT = 실행관리.Izvedi_ukaz(입력, 0, 길이);
            SMS_Terminal.Pisanje("Exit: "); SMS_Terminal.수쓰기(REZULTAT); SMS_Terminal.문자(10);
        }
        else if (Ukaz("apps")) 실행관리.vnos_Seznam();
        else if (Ukaz("net")) mreža_Sklad.stanje_VALUE();
        else if (Ukaz("run")) {
            int REZULTAT = 실행관리.Izvedi_ukaz(입력, 3, 길이);
            SMS_Terminal.Pisanje("Exit: "); SMS_Terminal.수쓰기(REZULTAT); SMS_Terminal.Pisanje("\n");
        } else if (Ukaz("info")) {
            SMS_Terminal.Pisanje("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Ukaz("mem")) {
            SMS_Terminal.Pisanje("위쪽 pomnilnik_VALUE naslov_območje(KiB): "); SMS_Terminal.수쓰기(pomnilnik_območje.UPPER_pomnilnik_spremeniti_velikost());
            SMS_Terminal.Pisanje("\n배열 동적 pomnilnik_VALUE naslov_območje(bajt_VALUE): "); SMS_Terminal.수쓰기(naprava_VALUE.ARRAY_uporaba());
            SMS_Terminal.Pisanje(" / 262144\n작업 naslov_območje odsek_VALUE: "); SMS_Terminal.수쓰기(pomnilnik_območje.사용개수());
            SMS_Terminal.Pisanje(" / 8 (각 4096바이트)\n");
        } else if (Ukaz("alloc")) {
            int INDEX = pomnilnik_območje.dodeliti_Senzor_prostora();
            SMS_Terminal.Pisanje("odsek_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.Pisanje("\n");
        } else if (Ukaz("free")) {
            if (길이 == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Pisanje(pomnilnik_območje.vrni_KR(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 odsek_VALUE\n");
            } else SMS_Terminal.Pisanje("사용법: free 0..7\n");
        } else if (Ukaz("echo")) {
            for (int INDEX = 5; INDEX < 길이; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (Ukaz("clear")) SMS_Terminal.izbrisati_vnos();
        else if (Ukaz("test")) jedro.시험();
        else if (Ukaz("halt")) {
            SMS_Terminal.Pisanje("HALTED\n");
            naprava_VALUE.정지();
        } else SMS_Terminal.Pisanje("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void sprejeti_AND_pisati(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (pomnilnik_datotečni_sistem.편집중) pomnilnik_datotečni_sistem.Urejeno_linija(입력, 길이, linija_presežek);
            else Proces_VALUE_vnos();
            길이 = 0;
            linija_presežek = false;
            SMS_Terminal.Pisanje(pomnilnik_datotečni_sistem.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (길이 > 0) {
                길이--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && 길이 < 입력.length) {
            입력[길이++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) linija_presežek = true;
    }

    static void Zaženi() {
        oddaja_spletna_pomoč();
        SMS_Terminal.Pisanje("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = tipkovnica.Branje();
            if (VALUE >= 0) sprejeti_AND_pisati(VALUE);
            else { mreža_Sklad.확인(); naprava_VALUE.잠시양보(); }
        }
    }
}
