// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Rakstīt 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int 길이 = 0;
    static boolean 앞줄복귀 = false;
    static boolean līnija_pārpilde = false;

    static boolean Komanda(String Nosaukums) {
        if (길이 < Nosaukums.length()) return false;
        for (int INDEX = 0; INDEX < Nosaukums.length(); INDEX++)
            if (입력[INDEX] != Nosaukums.charAt(INDEX)) return false;
        return 길이 == Nosaukums.length() || 입력[Nosaukums.length()] == ' ';
    }

    static void rādīt_palīdzība() {
        SMS_Terminālis.Rakstīt("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminālis.Rakstīt("apps | run NAME [ARGS] | net\n");
        SMS_Terminālis.Rakstīt("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminālis.Rakstīt("sync (연결된 JKSTORE1 Store_VALUE 장치에 Fails 보존)\n");
    }

    static void Process_VALUE_ievade() {
        if (길이 == 0) return;
        if (Komanda("help")) rādīt_palīdzība();
        else if (Komanda("sync")) {
            int mērs = 파일보존.sinhronizēt();
            SMS_Terminālis.Rakstīt("Sync: "); SMS_Terminālis.rakstīšana_numurs(mērs); SMS_Terminālis.문자(10);
        }
        else if (Komanda("ls")) atmiņa_failu_sistēma.ievade_Saraksts();
        else if (Komanda("edit")) atmiņa_failu_sistēma.Komanda(입력, 4, 길이, 0);
        else if (Komanda("cat")) atmiņa_failu_sistēma.Komanda(입력, 3, 길이, 1);
        else if (Komanda("rm")) atmiņa_failu_sistēma.Komanda(입력, 2, 길이, 2);
        else if (Komanda("java") || Komanda("javac")) {
            int mērs = 실행관리.Izpildīt_komanda(입력, 0, 길이);
            SMS_Terminālis.Rakstīt("Exit: "); SMS_Terminālis.rakstīšana_numurs(mērs); SMS_Terminālis.문자(10);
        }
        else if (Komanda("apps")) 실행관리.ievade_Saraksts();
        else if (Komanda("net")) tīkls_kopa.Statuss_VALUE();
        else if (Komanda("run")) {
            int mērs = 실행관리.Izpildīt_komanda(입력, 3, 길이);
            SMS_Terminālis.Rakstīt("Exit: "); SMS_Terminālis.rakstīšana_numurs(mērs); SMS_Terminālis.Rakstīt("\n");
        } else if (Komanda("info")) {
            SMS_Terminālis.Rakstīt("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Komanda("mem")) {
            SMS_Terminālis.Rakstīt("위쪽 atmiņa_VALUE adrese_reģions(KiB): "); SMS_Terminālis.rakstīšana_numurs(atmiņa_reģions.UPPER_atmiņa_mainīt_izmērus());
            SMS_Terminālis.Rakstīt("\n배열 동적 atmiņa_VALUE adrese_reģions(byte_VALUE): "); SMS_Terminālis.rakstīšana_numurs(ierīce_VALUE.ARRAY_patēriņš());
            SMS_Terminālis.Rakstīt(" / 262144\n작업 adrese_reģions sadaļa_VALUE: "); SMS_Terminālis.rakstīšana_numurs(atmiņa_reģions.사용개수());
            SMS_Terminālis.Rakstīt(" / 8 (각 4096바이트)\n");
        } else if (Komanda("alloc")) {
            int INDEX = atmiņa_reģions.piešķirt_Krātuve();
            SMS_Terminālis.Rakstīt("sadaļa_VALUE INDEX: "); SMS_Terminālis.rakstīšana_numurs(INDEX); SMS_Terminālis.Rakstīt("\n");
        } else if (Komanda("free")) {
            if (길이 == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminālis.Rakstīt(atmiņa_reģions.atdot_mērs(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 sadaļa_VALUE\n");
            } else SMS_Terminālis.Rakstīt("사용법: free 0..7\n");
        } else if (Komanda("echo")) {
            for (int INDEX = 5; INDEX < 길이; INDEX++) SMS_Terminālis.문자(입력[INDEX]);
            SMS_Terminālis.문자(10);
        } else if (Komanda("clear")) SMS_Terminālis.dzēst_ievade();
        else if (Komanda("test")) kodols.시험();
        else if (Komanda("halt")) {
            SMS_Terminālis.Rakstīt("HALTED\n");
            ierīce_VALUE.정지();
        } else SMS_Terminālis.Rakstīt("알 numurs 없는 명령입니다. help를 입력하세요.\n");
    }

    static void akceptēt_AND_rakstīšana(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminālis.문자(10);
            if (atmiņa_failu_sistēma.편집중) atmiņa_failu_sistēma.Rediģētie_līnija(입력, 길이, līnija_pārpilde);
            else Process_VALUE_ievade();
            길이 = 0;
            līnija_pārpilde = false;
            SMS_Terminālis.Rakstīt(atmiņa_failu_sistēma.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (길이 > 0) {
                길이--;
                SMS_Terminālis.직렬바이트(8); SMS_Terminālis.직렬바이트(32); SMS_Terminālis.직렬바이트(8);
                SMS_Terminālis.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && 길이 < 입력.length) {
            입력[길이++] = VALUE;
            SMS_Terminālis.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) līnija_pārpilde = true;
    }

    static void Palaist() {
        rādīt_palīdzība();
        SMS_Terminālis.Rakstīt("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminālis.직렬읽기();
            if (VALUE < 0) VALUE = tastatūra.Lasīt();
            if (VALUE >= 0) akceptēt_AND_rakstīšana(VALUE);
            else { tīkls_kopa.verificēt(); ierīce_VALUE.잠시양보(); }
        }
    }
}
