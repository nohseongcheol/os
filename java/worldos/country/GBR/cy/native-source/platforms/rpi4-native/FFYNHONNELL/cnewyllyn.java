// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class cnewyllyn {
    static int[] 작업횟수 = new int[3];
    static int[] tasg_SUM = new int[3];
    static int tasg_trefn;
    static int tasg_gwall;
    static int 난수씨 = 17;

    static void dilysu(boolean cyflwr, int INDEX) {
        if (!cyflwr) { 단말.Ysgrifennu("FAIL "); 단말.수(INDEX); bwrdd.Atal(INDEX); }
    }
    static int cangen(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] return_ARAE(int[] ARAE_VALUE) { return ARAE_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        dilysu(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        dilysu(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        dilysu(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        dilysu((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        dilysu((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARAE_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARAE_VALUE.length; Loop_INDEX++) ARAE_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARAE_VALUE[2]++;
        dilysu(return_ARAE(ARAE_VALUE) == ARAE_VALUE && ARAE_VALUE[2] == 35 && ARAE_VALUE[4] == 68, 6);
        dilysu(cangen(VALUE - 117) == 7 && cangen(VALUE - 15) == 9 && cangen(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Testun = "한글 😀";
        dilysu(Testun.length() == 5 && Testun.charAt(0) == '한' && Testun.charAt(3) == 0xd83d, 8);
        dilysu(bwrdd.CPU_hawl_lefel() == 1, 9);
        단말.Ysgrifennu("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // atal_CPU 전후 lleol_cwmpas 변수가 보존되는지 검사: 각 작업은 독립된 peiriant 스택을 쓴다.
        int lleol_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (tasg_trefn % 2 + 1 != INDEX) tasg_gwall++;
            tasg_trefn++;
            lleol_VALUE += Loop_INDEX + INDEX;
            tasg_SUM[INDEX] = lleol_VALUE;
            작업횟수[INDEX]++;
            bwrdd.atal_CPU();
            if (lleol_VALUE != tasg_SUM[INDEX]) tasg_gwall++;
        }
    }
    static void 작업시험() {
        tasg_trefn = 0; tasg_gwall = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        dilysu(bwrdd.Creu_tasg(1) == 0 && bwrdd.Creu_tasg(2) == 0, 20);
        int cylchdroi_COUNT = 0;
        while (bwrdd.tasg_cyflwr(1) != 0 || bwrdd.tasg_cyflwr(2) != 0) {
            bwrdd.atal_CPU();
            dilysu(++cylchdroi_COUNT < 100, 21);
        }
        dilysu(작업횟수[1] == 10 && 작업횟수[2] == 10 && tasg_trefn == 20 && tasg_gwall == 0, 22);
        dilysu(tasg_SUM[1] == 155 && tasg_SUM[2] == 265, 23);
        단말.Ysgrifennu("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Ar_i_fyny_safle, int 너비, int 높이, int 색) {
        for (int Y_cyfesuryn = Ar_i_fyny_safle; Y_cyfesuryn < Ar_i_fyny_safle + 높이; Y_cyfesuryn++)
            for (int cyfesuryn_x = 가로; cyfesuryn_x < 가로 + 너비; cyfesuryn_x++) bwrdd.화면점(cyfesuryn_x, Y_cyfesuryn, 색);
    }
    static void 화면() {
        if (bwrdd.화면준비() == 0) { 단말.Ysgrifennu("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, bwrdd.화면너비(), bwrdd.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Ysgrifennu("FRAMEBUFFER PASS "); 단말.수(bwrdd.화면너비()); 단말.문자('x');
        단말.수(bwrdd.화면높이()); 단말.Ysgrifennu(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int mesur = bwrdd.씨플러스시험();
        dilysu(mesur == 0, 100 + mesur);
        단말.Ysgrifennu("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        dilysu(bwrdd.gwirio_defnyddiwr_Rhaglen() == 0, 200);
        단말.Ysgrifennu("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = bwrdd.rhedeg_defnyddiwr_Rhaglen(0);
        if (처음결과 != 0) { 단말.Ysgrifennu("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        dilysu(처음결과 == 0, 201);
        단말.Ysgrifennu("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Ysgrifennu("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int mesur = bwrdd.rhedeg_defnyddiwr_Rhaglen(INDEX + 1);
            if (mesur != 예상[INDEX]) { 단말.Ysgrifennu("USER RESULT "); 단말.수(mesur); 단말.문자(10); }
            dilysu(mesur == 예상[INDEX], 210 + INDEX);
        }
        dilysu(bwrdd.rhedeg_defnyddiwr_Rhaglen(0) == 0, 220);
        단말.Ysgrifennu("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int mesur = bwrdd.rhedeg_defnyddiwr_Rhaglen(9);
        if (mesur != 0) { 단말.Ysgrifennu("UDP RESULT "); 단말.수(mesur); 단말.문자(10); }
        dilysu(mesur == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Ysgrifennu("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Ysgrifennu("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Ysgrifennu("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Ysgrifennu("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Ysgrifennu("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Gweithredu_2() {
        단말.Ysgrifennu("WorldOS cy · cy · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Ysgrifennu("NATIVE READY\n");
        명령해석기.Gweithredu_gorchymyn();
    }
}
