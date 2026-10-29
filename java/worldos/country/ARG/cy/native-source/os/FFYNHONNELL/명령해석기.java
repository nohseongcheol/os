// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Ysgrifennu 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int hyd_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean llinell_gorlif = false;

    static boolean Gorchymyn(String Enw) {
        if (hyd_VALUE < Enw.length()) return false;
        for (int INDEX = 0; INDEX < Enw.length(); INDEX++)
            if (입력[INDEX] != Enw.charAt(INDEX)) return false;
        return hyd_VALUE == Enw.length() || 입력[Enw.length()] == ' ';
    }

    static void sioe_help() {
        SMS_Terfynell.Ysgrifennu("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terfynell.Ysgrifennu("apps | run NAME [ARGS] | net\n");
        SMS_Terfynell.Ysgrifennu("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terfynell.Ysgrifennu("sync (연결된 JKSTORE1 Store_VALUE 장치에 Ffeil 보존)\n");
    }

    static void Proses_VALUE_cofnod() {
        if (hyd_VALUE == 0) return;
        if (Gorchymyn("help")) sioe_help();
        else if (Gorchymyn("sync")) {
            int mesur = 파일보존.cysoni();
            SMS_Terfynell.Ysgrifennu("Sync: "); SMS_Terfynell.수쓰기(mesur); SMS_Terfynell.문자(10);
        }
        else if (Gorchymyn("ls")) Cof_system_ffeiliau.cofnod_Rhestr();
        else if (Gorchymyn("edit")) Cof_system_ffeiliau.Gorchymyn(입력, 4, hyd_VALUE, 0);
        else if (Gorchymyn("cat")) Cof_system_ffeiliau.Gorchymyn(입력, 3, hyd_VALUE, 1);
        else if (Gorchymyn("rm")) Cof_system_ffeiliau.Gorchymyn(입력, 2, hyd_VALUE, 2);
        else if (Gorchymyn("java") || Gorchymyn("javac")) {
            int mesur = 실행관리.Gweithredu_gorchymyn(입력, 0, hyd_VALUE);
            SMS_Terfynell.Ysgrifennu("Exit: "); SMS_Terfynell.수쓰기(mesur); SMS_Terfynell.문자(10);
        }
        else if (Gorchymyn("apps")) 실행관리.cofnod_Rhestr();
        else if (Gorchymyn("net")) Rhwydwaith_pentwr.cyflwr_VALUE();
        else if (Gorchymyn("run")) {
            int mesur = 실행관리.Gweithredu_gorchymyn(입력, 3, hyd_VALUE);
            SMS_Terfynell.Ysgrifennu("Exit: "); SMS_Terfynell.수쓰기(mesur); SMS_Terfynell.Ysgrifennu("\n");
        } else if (Gorchymyn("info")) {
            SMS_Terfynell.Ysgrifennu("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Gorchymyn("mem")) {
            SMS_Terfynell.Ysgrifennu("위쪽 Cof_VALUE 공간(KiB): "); SMS_Terfynell.수쓰기(기억공간.UPPER_Cof_newid_maint());
            SMS_Terfynell.Ysgrifennu("\n배열 동적 Cof_VALUE 공간(beit_VALUE): "); SMS_Terfynell.수쓰기(dyfais_VALUE.ARAE_data_defnyddio());
            SMS_Terfynell.Ysgrifennu(" / 262144\n작업 공간 adran_VALUE: "); SMS_Terfynell.수쓰기(기억공간.사용개수());
            SMS_Terfynell.Ysgrifennu(" / 8 (각 4096바이트)\n");
        } else if (Gorchymyn("alloc")) {
            int INDEX = 기억공간.dyrannu_Storio();
            SMS_Terfynell.Ysgrifennu("adran_VALUE INDEX: "); SMS_Terfynell.수쓰기(INDEX); SMS_Terfynell.Ysgrifennu("\n");
        } else if (Gorchymyn("free")) {
            if (hyd_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terfynell.Ysgrifennu(기억공간.return_mesur(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 adran_VALUE\n");
            } else SMS_Terfynell.Ysgrifennu("사용법: free 0..7\n");
        } else if (Gorchymyn("echo")) {
            for (int INDEX = 5; INDEX < hyd_VALUE; INDEX++) SMS_Terfynell.문자(입력[INDEX]);
            SMS_Terfynell.문자(10);
        } else if (Gorchymyn("clear")) SMS_Terfynell.지우기();
        else if (Gorchymyn("test")) cnewyllyn.시험();
        else if (Gorchymyn("halt")) {
            SMS_Terfynell.Ysgrifennu("HALTED\n");
            dyfais_VALUE.정지();
        } else SMS_Terfynell.Ysgrifennu("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void derbyn_AND_ysgrifennu(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terfynell.문자(10);
            if (Cof_system_ffeiliau.편집중) Cof_system_ffeiliau.편집줄(입력, hyd_VALUE, llinell_gorlif);
            else Proses_VALUE_cofnod();
            hyd_VALUE = 0;
            llinell_gorlif = false;
            SMS_Terfynell.Ysgrifennu(Cof_system_ffeiliau.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (hyd_VALUE > 0) {
                hyd_VALUE--;
                SMS_Terfynell.직렬바이트(8); SMS_Terfynell.직렬바이트(32); SMS_Terfynell.직렬바이트(8);
                SMS_Terfynell.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && hyd_VALUE < 입력.length) {
            입력[hyd_VALUE++] = VALUE;
            SMS_Terfynell.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) llinell_gorlif = true;
    }

    static void Gweithredu_2() {
        sioe_help();
        SMS_Terfynell.Ysgrifennu("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terfynell.직렬읽기();
            if (VALUE < 0) VALUE = allweddell.Darllen();
            if (VALUE >= 0) derbyn_AND_ysgrifennu(VALUE);
            else { Rhwydwaith_pentwr.dilysu(); dyfais_VALUE.잠시양보(); }
        }
    }
}
