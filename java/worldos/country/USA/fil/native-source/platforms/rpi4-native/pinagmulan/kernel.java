// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kernel {
    static int[] 작업횟수 = new int[3];
    static int[] gawain_SUM = new int[3];
    static int gawain_pagkakasunud_sunod;
    static int gawain_error;
    static int 난수씨 = 17;

    static void tiyakin_kumpirmahin(boolean kondisyon, int INDEX) {
        if (!kondisyon) { 단말.sumulat("FAIL "); 단말.수(INDEX); board.Hinto(INDEX); }
    }
    static int sanga(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        tiyakin_kumpirmahin(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        tiyakin_kumpirmahin(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        tiyakin_kumpirmahin(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        tiyakin_kumpirmahin((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        tiyakin_kumpirmahin((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        tiyakin_kumpirmahin(배열돌려주기(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        tiyakin_kumpirmahin(sanga(VALUE - 117) == 7 && sanga(VALUE - 15) == 9 && sanga(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String SMS = "한글 😀";
        tiyakin_kumpirmahin(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        tiyakin_kumpirmahin(board.CPU_pahintulot_antas() == 1, 9);
        단말.sumulat("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 lokal_lawak 변수가 보존되는지 검사: 각 작업은 독립된 machine 스택을 쓴다.
        int lokal_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (gawain_pagkakasunud_sunod % 2 + 1 != INDEX) gawain_error++;
            gawain_pagkakasunud_sunod++;
            lokal_VALUE += Loop_INDEX + INDEX;
            gawain_SUM[INDEX] = lokal_VALUE;
            작업횟수[INDEX]++;
            board.YIELD_CPU();
            if (lokal_VALUE != gawain_SUM[INDEX]) gawain_error++;
        }
    }
    static void 작업시험() {
        gawain_pagkakasunud_sunod = 0; gawain_error = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        tiyakin_kumpirmahin(board.Create_gawain(1) == 0 && board.Create_gawain(2) == 0, 20);
        int pagpapaikot_COUNT = 0;
        while (board.gawain_katayuan(1) != 0 || board.gawain_katayuan(2) != 0) {
            board.YIELD_CPU();
            tiyakin_kumpirmahin(++pagpapaikot_COUNT < 100, 21);
        }
        tiyakin_kumpirmahin(작업횟수[1] == 10 && 작업횟수[2] == 10 && gawain_pagkakasunud_sunod == 20 && gawain_error == 0, 22);
        tiyakin_kumpirmahin(gawain_SUM[1] == 155 && gawain_SUM[2] == 265, 23);
        단말.sumulat("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int archive_posisyon, int 너비, int 높이, int 색) {
        for (int Y_button_coordinate = archive_posisyon; Y_button_coordinate < archive_posisyon + 높이; Y_button_coordinate++)
            for (int x_coordinate = 가로; x_coordinate < 가로 + 너비; x_coordinate++) board.화면점(x_coordinate, Y_button_coordinate, 색);
    }
    static void 화면() {
        if (board.화면준비() == 0) { 단말.sumulat("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, board.화면너비(), board.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.sumulat("FRAMEBUFFER PASS "); 단말.수(board.화면너비()); 단말.문자('x');
        단말.수(board.화면높이()); 단말.sumulat(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int sukat = board.씨플러스시험();
        tiyakin_kumpirmahin(sukat == 0, 100 + sukat);
        단말.sumulat("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        tiyakin_kumpirmahin(board.tseke_gumagamit_app() == 0, 200);
        단말.sumulat("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = board.run_gumagamit_app(0);
        if (처음결과 != 0) { 단말.sumulat("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        tiyakin_kumpirmahin(처음결과 == 0, 201);
        단말.sumulat("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.sumulat("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int sukat = board.run_gumagamit_app(INDEX + 1);
            if (sukat != 예상[INDEX]) { 단말.sumulat("USER RESULT "); 단말.수(sukat); 단말.문자(10); }
            tiyakin_kumpirmahin(sukat == 예상[INDEX], 210 + INDEX);
        }
        tiyakin_kumpirmahin(board.run_gumagamit_app(0) == 0, 220);
        단말.sumulat("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int sukat = board.run_gumagamit_app(9);
        if (sukat != 0) { 단말.sumulat("UDP RESULT "); 단말.수(sukat); 단말.문자(10); }
        tiyakin_kumpirmahin(sukat == 0, 230);
    }
    static void msinfo32_exe() {
        단말.sumulat("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.sumulat("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.sumulat("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.sumulat("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.sumulat("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void run() {
        단말.sumulat("WorldOS fil · fil · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.sumulat("NATIVE READY\n");
        명령해석기.Mag_execute_utos();
    }
}
