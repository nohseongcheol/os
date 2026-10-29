// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Zapisuj 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int 길이 = 0;
    static boolean 앞줄복귀 = false;
    static boolean red_preljev = false;

    static boolean Naredba(String Ime) {
        if (길이 < Ime.length()) return false;
        for (int INDEX = 0; INDEX < Ime.length(); INDEX++)
            if (입력[INDEX] != Ime.charAt(INDEX)) return false;
        return 길이 == Ime.length() || 입력[Ime.length()] == ' ';
    }

    static void emisija_pomoć() {
        SMS_Terminal.Zapisuj("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Zapisuj("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Zapisuj("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Zapisuj("sync (연결된 JKSTORE1 Store_VALUE 장치에 Datoteka 보존)\n");
    }

    static void Proces_VALUE_unos() {
        if (길이 == 0) return;
        if (Naredba("help")) emisija_pomoć();
        else if (Naredba("sync")) {
            int REZULTAT = 파일보존.sinkronizacija();
            SMS_Terminal.Zapisuj("Sync: "); SMS_Terminal.수쓰기(REZULTAT); SMS_Terminal.문자(10);
        }
        else if (Naredba("ls")) Memorija_datotečni_sustav.unos_Popis();
        else if (Naredba("edit")) Memorija_datotečni_sustav.Naredba(입력, 4, 길이, 0);
        else if (Naredba("cat")) Memorija_datotečni_sustav.Naredba(입력, 3, 길이, 1);
        else if (Naredba("rm")) Memorija_datotečni_sustav.Naredba(입력, 2, 길이, 2);
        else if (Naredba("java") || Naredba("javac")) {
            int REZULTAT = 실행관리.Izvrši_naredba(입력, 0, 길이);
            SMS_Terminal.Zapisuj("Exit: "); SMS_Terminal.수쓰기(REZULTAT); SMS_Terminal.문자(10);
        }
        else if (Naredba("apps")) 실행관리.unos_Popis();
        else if (Naredba("net")) mreža_hrpa.Stanje_VALUE();
        else if (Naredba("run")) {
            int REZULTAT = 실행관리.Izvrši_naredba(입력, 3, 길이);
            SMS_Terminal.Zapisuj("Exit: "); SMS_Terminal.수쓰기(REZULTAT); SMS_Terminal.Zapisuj("\n");
        } else if (Naredba("info")) {
            SMS_Terminal.Zapisuj("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Naredba("mem")) {
            SMS_Terminal.Zapisuj("위쪽 Memorija_VALUE adresa_regije(KiB): "); SMS_Terminal.수쓰기(Memorija_regije.UPPER_Memorija_promijeniti_veličinu());
            SMS_Terminal.Zapisuj("\n배열 동적 Memorija_VALUE adresa_regije(bajt_VALUE): "); SMS_Terminal.수쓰기(uređaj_VALUE.ARRAY_iskorištenost());
            SMS_Terminal.Zapisuj(" / 262144\n작업 adresa_regije sekcija_VALUE: "); SMS_Terminal.수쓰기(Memorija_regije.사용개수());
            SMS_Terminal.Zapisuj(" / 8 (각 4096바이트)\n");
        } else if (Naredba("alloc")) {
            int INDEX = Memorija_regije.dodijeli_Pohrana();
            SMS_Terminal.Zapisuj("sekcija_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.Zapisuj("\n");
        } else if (Naredba("free")) {
            if (길이 == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Zapisuj(Memorija_regije.vratiti_KR(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 sekcija_VALUE\n");
            } else SMS_Terminal.Zapisuj("사용법: free 0..7\n");
        } else if (Naredba("echo")) {
            for (int INDEX = 5; INDEX < 길이; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (Naredba("clear")) SMS_Terminal.izbrisati_unos();
        else if (Naredba("test")) jezgra_sustava.시험();
        else if (Naredba("halt")) {
            SMS_Terminal.Zapisuj("HALTED\n");
            uređaj_VALUE.정지();
        } else SMS_Terminal.Zapisuj("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void prihvatiti_AND_zapisivanje(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Memorija_datotečni_sustav.편집중) Memorija_datotečni_sustav.Uređivano_red(입력, 길이, red_preljev);
            else Proces_VALUE_unos();
            길이 = 0;
            red_preljev = false;
            SMS_Terminal.Zapisuj(Memorija_datotečni_sustav.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (길이 > 0) {
                길이--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && 길이 < 입력.length) {
            입력[길이++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) red_preljev = true;
    }

    static void Pokreni() {
        emisija_pomoć();
        SMS_Terminal.Zapisuj("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = tipkovnica.Čitaj();
            if (VALUE >= 0) prihvatiti_AND_zapisivanje(VALUE);
            else { mreža_hrpa.provjeriti(); uređaj_VALUE.잠시양보(); }
        }
    }
}
