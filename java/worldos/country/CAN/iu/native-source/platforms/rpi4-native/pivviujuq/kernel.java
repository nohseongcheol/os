// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kernel {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int sujassaq_agguijjut;
    static int sujassaq_tammarniq;
    static int 난수씨 = 17;

    static void nalunairli_1aacb54c(boolean qanuinniq, int nalunaiqsimavik) {
        if (!qanuinniq) { 단말.titiraq("FAIL "); 단말.수(nalunaiqsimavik); 보드.nuqqarli(nalunaiqsimavik); }
    }
    static int avalangajuq(int atuutilik) {
        switch (atuutilik) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int atuutilik) {
        switch (atuutilik) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] array_atuutilik) { return array_atuutilik; }
    static void 계산시험() {
        int atuutilik = 난수씨;
        nalunairli_1aacb54c(atuutilik * 7 - atuutilik == 102 && atuutilik / 3 == 5 && atuutilik % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        nalunairli_1aacb54c(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        nalunairli_1aacb54c(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        nalunairli_1aacb54c((-atuutilik >> 2) == -5 && (-atuutilik >>> 2) == 1073741819 && (atuutilik << 33) == 34, 4);
        nalunairli_1aacb54c((byte)(atuutilik * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] array_atuutilik = new int[5];
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < array_atuutilik.length; piliqqittaajuq_nalunaiqsimavik++) array_atuutilik[piliqqittaajuq_nalunaiqsimavik] = piliqqittaajuq_nalunaiqsimavik * atuutilik;
        array_atuutilik[2]++;
        nalunairli_1aacb54c(배열돌려주기(array_atuutilik) == array_atuutilik && array_atuutilik[2] == 35 && array_atuutilik[4] == 68, 6);
        nalunairli_1aacb54c(avalangajuq(atuutilik - 117) == 7 && avalangajuq(atuutilik - 15) == 9 && avalangajuq(atuutilik) == 3 && 촘촘분기(atuutilik - 15) == 17, 7);
        String titiqqaq = "한글 😀";
        nalunairli_1aacb54c(titiqqaq.length() == 5 && titiqqaq.charAt(0) == '한' && titiqqaq.charAt(3) == 0xd83d, 8);
        nalunairli_1aacb54c(보드.CPU_pijunnautitaarumaniq_sukuttia() == 1, 9);
        단말.titiraq("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int nalunaiqsimavik) {
        // 양보 전후 tamaani_qinirvik 변수가 보존되는지 검사: 각 작업은 독립된 기계 스택을 쓴다.
        int tamaani_atuutilik = nalunaiqsimavik * 100;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 10; piliqqittaajuq_nalunaiqsimavik++) {
            if (sujassaq_agguijjut % 2 + 1 != nalunaiqsimavik) sujassaq_tammarniq++;
            sujassaq_agguijjut++;
            tamaani_atuutilik += piliqqittaajuq_nalunaiqsimavik + nalunaiqsimavik;
            작업합[nalunaiqsimavik] = tamaani_atuutilik;
            작업횟수[nalunaiqsimavik]++;
            보드.양보();
            if (tamaani_atuutilik != 작업합[nalunaiqsimavik]) sujassaq_tammarniq++;
        }
    }
    static void 작업시험() {
        sujassaq_agguijjut = 0; sujassaq_tammarniq = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        nalunairli_1aacb54c(보드.작업만들기(1) == 0 && 보드.작업만들기(2) == 0, 20);
        int 회전 = 0;
        while (보드.sujassaq_qanuilinganiq(1) != 0 || 보드.sujassaq_qanuilinganiq(2) != 0) {
            보드.양보();
            nalunairli_1aacb54c(++회전 < 100, 21);
        }
        nalunairli_1aacb54c(작업횟수[1] == 10 && 작업횟수[2] == 10 && sujassaq_agguijjut == 20 && sujassaq_tammarniq == 0, 22);
        nalunairli_1aacb54c(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.titiraq("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int 가로좌표 = 가로; 가로좌표 < 가로 + 너비; 가로좌표++) 보드.화면점(가로좌표, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.titiraq("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.titiraq("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.titiraq(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        nalunairli_1aacb54c(결과 == 0, 100 + 결과);
        단말.titiraq("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        nalunairli_1aacb54c(보드.qaujigiarli_atuqtuq_pilirijjut() == 0, 200);
        단말.titiraq("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.사용자실행(0);
        if (처음결과 != 0) { 단말.titiraq("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        nalunairli_1aacb54c(처음결과 == 0, 201);
        단말.titiraq("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 예상.length; nalunaiqsimavik++) {
            단말.titiraq("USER CHECK "); 단말.수(nalunaiqsimavik); 단말.문자(10);
            int 결과 = 보드.사용자실행(nalunaiqsimavik + 1);
            if (결과 != 예상[nalunaiqsimavik]) { 단말.titiraq("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            nalunairli_1aacb54c(결과 == 예상[nalunaiqsimavik], 210 + nalunaiqsimavik);
        }
        nalunairli_1aacb54c(보드.사용자실행(0) == 0, 220);
        단말.titiraq("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.사용자실행(9);
        if (결과 != 0) { 단말.titiraq("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        nalunairli_1aacb54c(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.titiraq("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.titiraq("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.titiraq("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.titiraq("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.titiraq("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void 시작() {
        단말.titiraq("WorldOS iu · iu · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.titiraq("NATIVE READY\n");
        명령해석기.실행();
    }
}
