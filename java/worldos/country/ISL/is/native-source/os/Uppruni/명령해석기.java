// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Skrift 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int lengd_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean lína_yfirflæði = false;

    static boolean Skipun(String Heiti) {
        if (lengd_VALUE < Heiti.length()) return false;
        for (int INDEX = 0; INDEX < Heiti.length(); INDEX++)
            if (입력[INDEX] != Heiti.charAt(INDEX)) return false;
        return lengd_VALUE == Heiti.length() || 입력[Heiti.length()] == ' ';
    }

    static void sýna_hjálp() {
        SMS_Endastöð.Skrift("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Endastöð.Skrift("apps | run NAME [ARGS] | net\n");
        SMS_Endastöð.Skrift("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Endastöð.Skrift("sync (연결된 JKSTORE1 Store_VALUE 장치에 Skrá 보존)\n");
    }

    static void Ferli_VALUE_færsla() {
        if (lengd_VALUE == 0) return;
        if (Skipun("help")) sýna_hjálp();
        else if (Skipun("sync")) {
            int NIÐURSTAÐA = 파일보존.samstilla();
            SMS_Endastöð.Skrift("Sync: "); SMS_Endastöð.skrifa_númer(NIÐURSTAÐA); SMS_Endastöð.문자(10);
        }
        else if (Skipun("ls")) Minni_skrárkerfi.færsla_Listi();
        else if (Skipun("edit")) Minni_skrárkerfi.Skipun(입력, 4, lengd_VALUE, 0);
        else if (Skipun("cat")) Minni_skrárkerfi.Skipun(입력, 3, lengd_VALUE, 1);
        else if (Skipun("rm")) Minni_skrárkerfi.Skipun(입력, 2, lengd_VALUE, 2);
        else if (Skipun("java") || Skipun("javac")) {
            int NIÐURSTAÐA = 실행관리.keyra_skipun(입력, 0, lengd_VALUE);
            SMS_Endastöð.Skrift("Exit: "); SMS_Endastöð.skrifa_númer(NIÐURSTAÐA); SMS_Endastöð.문자(10);
        }
        else if (Skipun("apps")) 실행관리.færsla_Listi();
        else if (Skipun("net")) Net_bunki.staða_VALUE_e10195a1();
        else if (Skipun("run")) {
            int NIÐURSTAÐA = 실행관리.keyra_skipun(입력, 3, lengd_VALUE);
            SMS_Endastöð.Skrift("Exit: "); SMS_Endastöð.skrifa_númer(NIÐURSTAÐA); SMS_Endastöð.Skrift("\n");
        } else if (Skipun("info")) {
            SMS_Endastöð.Skrift("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Skipun("mem")) {
            SMS_Endastöð.Skrift("위쪽 Minni_VALUE 공간(KiB): "); SMS_Endastöð.skrifa_númer(기억공간.UPPER_Minni_breyta_stærð());
            SMS_Endastöð.Skrift("\n배열 동적 Minni_VALUE 공간(bæti_VALUE): "); SMS_Endastöð.skrifa_númer(tæki_VALUE.ARRAY_notkun());
            SMS_Endastöð.Skrift(" / 262144\n작업 공간 hluti_VALUE: "); SMS_Endastöð.skrifa_númer(기억공간.사용개수());
            SMS_Endastöð.Skrift(" / 8 (각 4096바이트)\n");
        } else if (Skipun("alloc")) {
            int INDEX = 기억공간.úthluta_geymsla();
            SMS_Endastöð.Skrift("hluti_VALUE INDEX: "); SMS_Endastöð.skrifa_númer(INDEX); SMS_Endastöð.Skrift("\n");
        } else if (Skipun("free")) {
            if (lengd_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Endastöð.Skrift(기억공간.skila_mæld_stærð(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 hluti_VALUE\n");
            } else SMS_Endastöð.Skrift("사용법: free 0..7\n");
        } else if (Skipun("echo")) {
            for (int INDEX = 5; INDEX < lengd_VALUE; INDEX++) SMS_Endastöð.문자(입력[INDEX]);
            SMS_Endastöð.문자(10);
        } else if (Skipun("clear")) SMS_Endastöð.eyða_færsla();
        else if (Skipun("test")) kjarni.시험();
        else if (Skipun("halt")) {
            SMS_Endastöð.Skrift("HALTED\n");
            tæki_VALUE.정지();
        } else SMS_Endastöð.Skrift("알 númer 없는 명령입니다. help를 입력하세요.\n");
    }

    static void samþykkja_AND_skrifa(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Endastöð.문자(10);
            if (Minni_skrárkerfi.편집중) Minni_skrárkerfi.편집줄(입력, lengd_VALUE, lína_yfirflæði);
            else Ferli_VALUE_færsla();
            lengd_VALUE = 0;
            lína_yfirflæði = false;
            SMS_Endastöð.Skrift(Minni_skrárkerfi.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (lengd_VALUE > 0) {
                lengd_VALUE--;
                SMS_Endastöð.직렬바이트(8); SMS_Endastöð.직렬바이트(32); SMS_Endastöð.직렬바이트(8);
                SMS_Endastöð.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && lengd_VALUE < 입력.length) {
            입력[lengd_VALUE++] = VALUE;
            SMS_Endastöð.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) lína_yfirflæði = true;
    }

    static void Keyra_2() {
        sýna_hjálp();
        SMS_Endastöð.Skrift("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Endastöð.직렬읽기();
            if (VALUE < 0) VALUE = lyklaborð.Lestur();
            if (VALUE >= 0) samþykkja_AND_skrifa(VALUE);
            else { Net_bunki.sannprófa(); tæki_VALUE.잠시양보(); }
        }
    }
}
