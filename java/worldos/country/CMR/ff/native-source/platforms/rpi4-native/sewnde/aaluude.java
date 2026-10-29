// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class aaluude {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int golle_deggondiral;
    static int golle_juumre;
    static int 난수씨 = 17;

    static void ƴeewtaade(boolean ngonka, int joopirdu) {
        if (!ngonka) { 단말.winndude("FAIL "); 단말.수(joopirdu); 보드.dartinde(joopirdu); }
    }
    static int 분기(int njaru) {
        switch (njaru) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int njaru) {
        switch (njaru) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] 배열) { return 배열; }
    static void 계산시험() {
        int njaru = 난수씨;
        ƴeewtaade(njaru * 7 - njaru == 102 && njaru / 3 == 5 && njaru % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        ƴeewtaade(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        ƴeewtaade(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        ƴeewtaade((-njaru >> 2) == -5 && (-njaru >>> 2) == 1073741819 && (njaru << 33) == 34, 4);
        ƴeewtaade((byte)(njaru * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] 배열 = new int[5];
        for (int kowal_joopirdu = 0; kowal_joopirdu < 배열.length; kowal_joopirdu++) 배열[kowal_joopirdu] = kowal_joopirdu * njaru;
        배열[2]++;
        ƴeewtaade(배열돌려주기(배열) == 배열 && 배열[2] == 35 && 배열[4] == 68, 6);
        ƴeewtaade(분기(njaru - 117) == 7 && 분기(njaru - 15) == 9 && 분기(njaru) == 3 && 촘촘분기(njaru - 15) == 17, 7);
        String binndi = "한글 😀";
        ƴeewtaade(binndi.length() == 5 && binndi.charAt(0) == '한' && binndi.charAt(3) == 0xd83d, 8);
        ƴeewtaade(보드.시피유권한() == 1, 9);
        단말.winndude("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int joopirdu) {
        // 양보 전후 nokkuwal_njaajeendi 변수가 보존되는지 검사: 각 작업은 독립된 기계 스택을 쓴다.
        int nokkuwal_njaru = joopirdu * 100;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 10; kowal_joopirdu++) {
            if (golle_deggondiral % 2 + 1 != joopirdu) golle_juumre++;
            golle_deggondiral++;
            nokkuwal_njaru += kowal_joopirdu + joopirdu;
            작업합[joopirdu] = nokkuwal_njaru;
            작업횟수[joopirdu]++;
            보드.양보();
            if (nokkuwal_njaru != 작업합[joopirdu]) golle_juumre++;
        }
    }
    static void 작업시험() {
        golle_deggondiral = 0; golle_juumre = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        ƴeewtaade(보드.작업만들기(1) == 0 && 보드.작업만들기(2) == 0, 20);
        int 회전 = 0;
        while (보드.golle_ngonka(1) != 0 || 보드.golle_ngonka(2) != 0) {
            보드.양보();
            ƴeewtaade(++회전 < 100, 21);
        }
        ƴeewtaade(작업횟수[1] == 10 && 작업횟수[2] == 10 && golle_deggondiral == 20 && golle_juumre == 0, 22);
        ƴeewtaade(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.winndude("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int 가로좌표 = 가로; 가로좌표 < 가로 + 너비; 가로좌표++) 보드.화면점(가로좌표, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.winndude("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.winndude("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.winndude(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        ƴeewtaade(결과 == 0, 100 + 결과);
        단말.winndude("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        ƴeewtaade(보드.sek_kuutoro_tafirde() == 0, 200);
        단말.winndude("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.huutoraade_kuutoro_tafirde(0);
        if (처음결과 != 0) { 단말.winndude("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        ƴeewtaade(처음결과 == 0, 201);
        단말.winndude("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int joopirdu = 0; joopirdu < 예상.length; joopirdu++) {
            단말.winndude("USER CHECK "); 단말.수(joopirdu); 단말.문자(10);
            int 결과 = 보드.huutoraade_kuutoro_tafirde(joopirdu + 1);
            if (결과 != 예상[joopirdu]) { 단말.winndude("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            ƴeewtaade(결과 == 예상[joopirdu], 210 + joopirdu);
        }
        ƴeewtaade(보드.huutoraade_kuutoro_tafirde(0) == 0, 220);
        단말.winndude("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.huutoraade_kuutoro_tafirde(9);
        if (결과 != 0) { 단말.winndude("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        ƴeewtaade(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.winndude("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.winndude("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.winndude("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.winndude("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.winndude("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void huutoraade() {
        단말.winndude("WorldOS ff · ff · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.winndude("NATIVE READY\n");
        명령해석기.실행();
    }
}
