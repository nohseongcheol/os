// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 쓰기 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int 길이 = 0;
    static boolean 앞줄복귀 = false;
    static boolean red_višak = false;

    static boolean komanda(String ime) {
        if (길이 < ime.length()) return false;
        for (int INDEX = 0; INDEX < ime.length(); INDEX++)
            if (입력[INDEX] != ime.charAt(INDEX)) return false;
        return 길이 == ime.length() || 입력[ime.length()] == ' ';
    }

    static void emisija_pomoć_na_mreži() {
        SMS_Terminal.쓰기("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.쓰기("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.쓰기("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.쓰기("sync (연결된 JKSTORE1 Store_VALUE 장치에 Datoteka 보존)\n");
    }

    static void Proces_VALUE_stavka() {
        if (길이 == 0) return;
        if (komanda("help")) emisija_pomoć_na_mreži();
        else if (komanda("sync")) {
            int KR = 파일보존.sinhronizovati();
            SMS_Terminal.쓰기("Sync: "); SMS_Terminal.수쓰기(KR); SMS_Terminal.문자(10);
        }
        else if (komanda("ls")) Memorija_sistem_datoteka.stavka_Lista();
        else if (komanda("edit")) Memorija_sistem_datoteka.komanda(입력, 4, 길이, 0);
        else if (komanda("cat")) Memorija_sistem_datoteka.komanda(입력, 3, 길이, 1);
        else if (komanda("rm")) Memorija_sistem_datoteka.komanda(입력, 2, 길이, 2);
        else if (komanda("java") || komanda("javac")) {
            int KR = 실행관리.Izvrši_komanda(입력, 0, 길이);
            SMS_Terminal.쓰기("Exit: "); SMS_Terminal.수쓰기(KR); SMS_Terminal.문자(10);
        }
        else if (komanda("apps")) 실행관리.stavka_Lista();
        else if (komanda("net")) Mreža_stek.Status_VALUE();
        else if (komanda("run")) {
            int KR = 실행관리.Izvrši_komanda(입력, 3, 길이);
            SMS_Terminal.쓰기("Exit: "); SMS_Terminal.수쓰기(KR); SMS_Terminal.쓰기("\n");
        } else if (komanda("info")) {
            SMS_Terminal.쓰기("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (komanda("mem")) {
            SMS_Terminal.쓰기("위쪽 Memorija_VALUE adresa_oblast(KiB): "); SMS_Terminal.수쓰기(Memorija_oblast.UPPER_Memorija_promeniti_veličinu());
            SMS_Terminal.쓰기("\n배열 동적 Memorija_VALUE adresa_oblast(bajt_VALUE): "); SMS_Terminal.수쓰기(uređaj_VALUE.niz_upotreba());
            SMS_Terminal.쓰기(" / 262144\n작업 adresa_oblast odeljak_VALUE: "); SMS_Terminal.수쓰기(Memorija_oblast.사용개수());
            SMS_Terminal.쓰기(" / 8 (각 4096바이트)\n");
        } else if (komanda("alloc")) {
            int INDEX = Memorija_oblast.dodeliti_Skladište();
            SMS_Terminal.쓰기("odeljak_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.쓰기("\n");
        } else if (komanda("free")) {
            if (길이 == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.쓰기(Memorija_oblast.vratiti_KR(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 odeljak_VALUE\n");
            } else SMS_Terminal.쓰기("사용법: free 0..7\n");
        } else if (komanda("echo")) {
            for (int INDEX = 5; INDEX < 길이; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (komanda("clear")) SMS_Terminal.obrisati_stavka();
        else if (komanda("test")) jezgro.시험();
        else if (komanda("halt")) {
            SMS_Terminal.쓰기("HALTED\n");
            uređaj_VALUE.정지();
        } else SMS_Terminal.쓰기("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Memorija_sistem_datoteka.편집중) Memorija_sistem_datoteka.Uređivano_red(입력, 길이, red_višak);
            else Proces_VALUE_stavka();
            길이 = 0;
            red_višak = false;
            SMS_Terminal.쓰기(Memorija_sistem_datoteka.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (길이 > 0) {
                길이--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && 길이 < 입력.length) {
            입력[길이++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) red_višak = true;
    }

    static void koristiti() {
        emisija_pomoć_na_mreži();
        SMS_Terminal.쓰기("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = tastatura.읽기();
            if (VALUE >= 0) 받아쓰기(VALUE);
            else { Mreža_stek.verifikovati(); uređaj_VALUE.잠시양보(); }
        }
    }
}
