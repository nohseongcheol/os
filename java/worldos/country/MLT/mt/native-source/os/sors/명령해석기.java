// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 kiteb 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int tul_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean linja_overflow = false;

    static boolean kmand(String isem) {
        if (tul_VALUE < isem.length()) return false;
        for (int INDEX = 0; INDEX < isem.length(); INDEX++)
            if (입력[INDEX] != isem.charAt(INDEX)) return false;
        return tul_VALUE == isem.length() || 입력[isem.length()] == ' ';
    }

    static void wera_għajnuna() {
        SMS_Terminal.kiteb("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.kiteb("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.kiteb("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.kiteb("sync (연결된 JKSTORE1 Store_VALUE 장치에 fajl 보존)\n");
    }

    static void Proċess_VALUE_entrata() {
        if (tul_VALUE == 0) return;
        if (kmand("help")) wera_għajnuna();
        else if (kmand("sync")) {
            int miżura = 파일보존.ssinkronizza();
            SMS_Terminal.kiteb("Sync: "); SMS_Terminal.수쓰기(miżura); SMS_Terminal.문자(10);
        }
        else if (kmand("ls")) Memorja_sistema_tal_fajls.entrata_Lista();
        else if (kmand("edit")) Memorja_sistema_tal_fajls.kmand(입력, 4, tul_VALUE, 0);
        else if (kmand("cat")) Memorja_sistema_tal_fajls.kmand(입력, 3, tul_VALUE, 1);
        else if (kmand("rm")) Memorja_sistema_tal_fajls.kmand(입력, 2, tul_VALUE, 2);
        else if (kmand("java") || kmand("javac")) {
            int miżura = 실행관리.eżegwixxa_kmand(입력, 0, tul_VALUE);
            SMS_Terminal.kiteb("Exit: "); SMS_Terminal.수쓰기(miżura); SMS_Terminal.문자(10);
        }
        else if (kmand("apps")) 실행관리.entrata_Lista();
        else if (kmand("net")) netwerk_Munzell.stat_VALUE();
        else if (kmand("run")) {
            int miżura = 실행관리.eżegwixxa_kmand(입력, 3, tul_VALUE);
            SMS_Terminal.kiteb("Exit: "); SMS_Terminal.수쓰기(miżura); SMS_Terminal.kiteb("\n");
        } else if (kmand("info")) {
            SMS_Terminal.kiteb("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (kmand("mem")) {
            SMS_Terminal.kiteb("위쪽 Memorja_VALUE 공간(KiB): "); SMS_Terminal.수쓰기(기억공간.UPPER_Memorja_daqqas());
            SMS_Terminal.kiteb("\n배열 동적 Memorja_VALUE 공간(byte_VALUE): "); SMS_Terminal.수쓰기(mowbajl_VALUE.ARRAY_użu());
            SMS_Terminal.kiteb(" / 262144\n작업 공간 taqsima_VALUE_366e0bfa: "); SMS_Terminal.수쓰기(기억공간.사용개수());
            SMS_Terminal.kiteb(" / 8 (각 4096바이트)\n");
        } else if (kmand("alloc")) {
            int INDEX = 기억공간.alloka_Ħażna();
            SMS_Terminal.kiteb("taqsima_VALUE_366e0bfa INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.kiteb("\n");
        } else if (kmand("free")) {
            if (tul_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.kiteb(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 taqsima_VALUE_366e0bfa\n");
            } else SMS_Terminal.kiteb("사용법: free 0..7\n");
        } else if (kmand("echo")) {
            for (int INDEX = 5; INDEX < tul_VALUE; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (kmand("clear")) SMS_Terminal.지우기();
        else if (kmand("test")) kernel.시험();
        else if (kmand("halt")) {
            SMS_Terminal.kiteb("HALTED\n");
            mowbajl_VALUE.정지();
        } else SMS_Terminal.kiteb("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void aċċetta_AND_kiteb(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Memorja_sistema_tal_fajls.편집중) Memorja_sistema_tal_fajls.편집줄(입력, tul_VALUE, linja_overflow);
            else Proċess_VALUE_entrata();
            tul_VALUE = 0;
            linja_overflow = false;
            SMS_Terminal.kiteb(Memorja_sistema_tal_fajls.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (tul_VALUE > 0) {
                tul_VALUE--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && tul_VALUE < 입력.length) {
            입력[tul_VALUE++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) linja_overflow = true;
    }

    static void serje() {
        wera_għajnuna();
        SMS_Terminal.kiteb("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = tastiera.읽기();
            if (VALUE >= 0) aċċetta_AND_kiteb(VALUE);
            else { netwerk_Munzell.vverifika(); mowbajl_VALUE.잠시양보(); }
        }
    }
}
