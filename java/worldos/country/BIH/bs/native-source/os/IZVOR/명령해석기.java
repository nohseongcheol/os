// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Piši 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int dužina_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean redak_prelijevanje = false;

    static boolean Naredba(String Naziv) {
        if (dužina_VALUE < Naziv.length()) return false;
        for (int INDEX = 0; INDEX < Naziv.length(); INDEX++)
            if (입력[INDEX] != Naziv.charAt(INDEX)) return false;
        return dužina_VALUE == Naziv.length() || 입력[Naziv.length()] == ' ';
    }

    static void program_pomoć() {
        SMS_Terminal.Piši("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Piši("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Piši("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Piši("sync (연결된 JKSTORE1 Store_VALUE 장치에 Fajl 보존)\n");
    }

    static void proces_VALUE_unos() {
        if (dužina_VALUE == 0) return;
        if (Naredba("help")) program_pomoć();
        else if (Naredba("sync")) {
            int mjera = 파일보존.sinhronizirati();
            SMS_Terminal.Piši("Sync: "); SMS_Terminal.수쓰기(mjera); SMS_Terminal.문자(10);
        }
        else if (Naredba("ls")) Memorija_fajl_sistem.unos_spisak();
        else if (Naredba("edit")) Memorija_fajl_sistem.Naredba(입력, 4, dužina_VALUE, 0);
        else if (Naredba("cat")) Memorija_fajl_sistem.Naredba(입력, 3, dužina_VALUE, 1);
        else if (Naredba("rm")) Memorija_fajl_sistem.Naredba(입력, 2, dužina_VALUE, 2);
        else if (Naredba("java") || Naredba("javac")) {
            int mjera = 실행관리.Izvrši_komanda(입력, 0, dužina_VALUE);
            SMS_Terminal.Piši("Exit: "); SMS_Terminal.수쓰기(mjera); SMS_Terminal.문자(10);
        }
        else if (Naredba("apps")) 실행관리.unos_spisak();
        else if (Naredba("net")) Mreža_snop.stanje_VALUE();
        else if (Naredba("run")) {
            int mjera = 실행관리.Izvrši_komanda(입력, 3, dužina_VALUE);
            SMS_Terminal.Piši("Exit: "); SMS_Terminal.수쓰기(mjera); SMS_Terminal.Piši("\n");
        } else if (Naredba("info")) {
            SMS_Terminal.Piši("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Naredba("mem")) {
            SMS_Terminal.Piši("위쪽 Memorija_VALUE 공간(KiB): "); SMS_Terminal.수쓰기(기억공간.UPPER_Memorija_podesiti_veličinu());
            SMS_Terminal.Piši("\n배열 동적 Memorija_VALUE 공간(bajt_VALUE): "); SMS_Terminal.수쓰기(uređaj_VALUE.niz_potrošnja());
            SMS_Terminal.Piši(" / 262144\n작업 공간 sekcija_VALUE: "); SMS_Terminal.수쓰기(기억공간.사용개수());
            SMS_Terminal.Piši(" / 8 (각 4096바이트)\n");
        } else if (Naredba("alloc")) {
            int INDEX = 기억공간.dodijeliti_Pohrana();
            SMS_Terminal.Piši("sekcija_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.Piši("\n");
        } else if (Naredba("free")) {
            if (dužina_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Piši(기억공간.vratiti_mjera(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 sekcija_VALUE\n");
            } else SMS_Terminal.Piši("사용법: free 0..7\n");
        } else if (Naredba("echo")) {
            for (int INDEX = 5; INDEX < dužina_VALUE; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (Naredba("clear")) SMS_Terminal.지우기();
        else if (Naredba("test")) jezgro.시험();
        else if (Naredba("halt")) {
            SMS_Terminal.Piši("HALTED\n");
            uređaj_VALUE.정지();
        } else SMS_Terminal.Piši("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void prihvatiti_AND_pisati(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Memorija_fajl_sistem.편집중) Memorija_fajl_sistem.Uređivano_redak(입력, dužina_VALUE, redak_prelijevanje);
            else proces_VALUE_unos();
            dužina_VALUE = 0;
            redak_prelijevanje = false;
            SMS_Terminal.Piši(Memorija_fajl_sistem.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (dužina_VALUE > 0) {
                dužina_VALUE--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && dužina_VALUE < 입력.length) {
            입력[dužina_VALUE++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) redak_prelijevanje = true;
    }

    static void Pokreni() {
        program_pomoć();
        SMS_Terminal.Piši("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = tastatura.Čitaj();
            if (VALUE >= 0) prihvatiti_AND_pisati(VALUE);
            else { Mreža_snop.potvrditi(); uređaj_VALUE.잠시양보(); }
        }
    }
}
