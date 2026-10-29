// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 sumulat 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int haba_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean linya_sobrang_teksto = false;

    static boolean utos(String pangalan) {
        if (haba_VALUE < pangalan.length()) return false;
        for (int INDEX = 0; INDEX < pangalan.length(); INDEX++)
            if (입력[INDEX] != pangalan.charAt(INDEX)) return false;
        return haba_VALUE == pangalan.length() || 입력[pangalan.length()] == ' ';
    }

    static void ipakita_tulong() {
        SMS_Terminal.sumulat("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.sumulat("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.sumulat("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.sumulat("sync (연결된 JKSTORE1 Store_VALUE 장치에 file 보존)\n");
    }

    static void Proseso_VALUE_pagpasok() {
        if (haba_VALUE == 0) return;
        if (utos("help")) ipakita_tulong();
        else if (utos("sync")) {
            int sukat = 파일보존.iakma();
            SMS_Terminal.sumulat("Sync: "); SMS_Terminal.수쓰기(sukat); SMS_Terminal.문자(10);
        }
        else if (utos("ls")) Memory_sistema_ng_file.pagpasok_list();
        else if (utos("edit")) Memory_sistema_ng_file.utos(입력, 4, haba_VALUE, 0);
        else if (utos("cat")) Memory_sistema_ng_file.utos(입력, 3, haba_VALUE, 1);
        else if (utos("rm")) Memory_sistema_ng_file.utos(입력, 2, haba_VALUE, 2);
        else if (utos("java") || utos("javac")) {
            int sukat = 실행관리.Mag_execute_utos(입력, 0, haba_VALUE);
            SMS_Terminal.sumulat("Exit: "); SMS_Terminal.수쓰기(sukat); SMS_Terminal.문자(10);
        }
        else if (utos("apps")) 실행관리.pagpasok_list();
        else if (utos("net")) Network_Stack.katayuan_VALUE();
        else if (utos("run")) {
            int sukat = 실행관리.Mag_execute_utos(입력, 3, haba_VALUE);
            SMS_Terminal.sumulat("Exit: "); SMS_Terminal.수쓰기(sukat); SMS_Terminal.sumulat("\n");
        } else if (utos("info")) {
            SMS_Terminal.sumulat("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (utos("mem")) {
            SMS_Terminal.sumulat("위쪽 Memory_VALUE 공간(KiB): "); SMS_Terminal.수쓰기(기억공간.UPPER_Memory_sukat());
            SMS_Terminal.sumulat("\n배열 동적 Memory_VALUE 공간(byte_VALUE): "); SMS_Terminal.수쓰기(device_VALUE.ARRAY_paggamit());
            SMS_Terminal.sumulat(" / 262144\n작업 공간 seksiyon_VALUE: "); SMS_Terminal.수쓰기(기억공간.사용개수());
            SMS_Terminal.sumulat(" / 8 (각 4096바이트)\n");
        } else if (utos("alloc")) {
            int INDEX = 기억공간.maglaan_Storage();
            SMS_Terminal.sumulat("seksiyon_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.sumulat("\n");
        } else if (utos("free")) {
            if (haba_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.sumulat(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 seksiyon_VALUE\n");
            } else SMS_Terminal.sumulat("사용법: free 0..7\n");
        } else if (utos("echo")) {
            for (int INDEX = 5; INDEX < haba_VALUE; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (utos("clear")) SMS_Terminal.burahin_pagpasok();
        else if (utos("test")) kernel.시험();
        else if (utos("halt")) {
            SMS_Terminal.sumulat("HALTED\n");
            device_VALUE.정지();
        } else SMS_Terminal.sumulat("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void tanggapin_AND_sumulat(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Memory_sistema_ng_file.편집중) Memory_sistema_ng_file.편집줄(입력, haba_VALUE, linya_sobrang_teksto);
            else Proseso_VALUE_pagpasok();
            haba_VALUE = 0;
            linya_sobrang_teksto = false;
            SMS_Terminal.sumulat(Memory_sistema_ng_file.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (haba_VALUE > 0) {
                haba_VALUE--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && haba_VALUE < 입력.length) {
            입력[haba_VALUE++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) linya_sobrang_teksto = true;
    }

    static void run() {
        ipakita_tulong();
        SMS_Terminal.sumulat("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = keyboard.읽기();
            if (VALUE >= 0) tanggapin_AND_sumulat(VALUE);
            else { Network_Stack.tiyakin_kumpirmahin(); device_VALUE.잠시양보(); }
        }
    }
}
