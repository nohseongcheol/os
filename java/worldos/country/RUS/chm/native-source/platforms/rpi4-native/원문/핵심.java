// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class 핵심 {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int 작업순서;
    static int 작업오류;
    static int 난수씨 = 17;

    static void 확인(boolean 조건, int 번호) {
        if (!조건) { 단말.쓰기("FAIL "); 단말.수(번호); 보드.중지(번호); }
    }
    static int 분기(int 값) {
        switch (값) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int 값) {
        switch (값) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] 배열) { return 배열; }
    static void 계산시험() {
        int 값 = 난수씨;
        확인(값 * 7 - 값 == 102 && 값 / 3 == 5 && 값 % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        확인(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        확인(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        확인((-값 >> 2) == -5 && (-값 >>> 2) == 1073741819 && (값 << 33) == 34, 4);
        확인((byte)(값 * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] 배열 = new int[5];
        for (int 반복자리 = 0; 반복자리 < 배열.length; 반복자리++) 배열[반복자리] = 반복자리 * 값;
        배열[2]++;
        확인(배열돌려주기(배열) == 배열 && 배열[2] == 35 && 배열[4] == 68, 6);
        확인(분기(값 - 117) == 7 && 분기(값 - 15) == 9 && 분기(값) == 3 && 촘촘분기(값 - 15) == 17, 7);
        String 글 = "한글 😀";
        확인(글.length() == 5 && 글.charAt(0) == '한' && 글.charAt(3) == 0xd83d, 8);
        확인(보드.시피유권한() == 1, 9);
        단말.쓰기("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int 번호) {
        // 양보 전후 지역 변수가 보존되는지 검사: 각 작업은 독립된 기계 스택을 쓴다.
        int 지역값 = 번호 * 100;
        for (int 반복자리 = 0; 반복자리 < 10; 반복자리++) {
            if (작업순서 % 2 + 1 != 번호) 작업오류++;
            작업순서++;
            지역값 += 반복자리 + 번호;
            작업합[번호] = 지역값;
            작업횟수[번호]++;
            보드.양보();
            if (지역값 != 작업합[번호]) 작업오류++;
        }
    }
    static void 작업시험() {
        작업순서 = 0; 작업오류 = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        확인(보드.작업만들기(1) == 0 && 보드.작업만들기(2) == 0, 20);
        int 회전 = 0;
        while (보드.작업상태(1) != 0 || 보드.작업상태(2) != 0) {
            보드.양보();
            확인(++회전 < 100, 21);
        }
        확인(작업횟수[1] == 10 && 작업횟수[2] == 10 && 작업순서 == 20 && 작업오류 == 0, 22);
        확인(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.쓰기("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int 가로좌표 = 가로; 가로좌표 < 가로 + 너비; 가로좌표++) 보드.화면점(가로좌표, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.쓰기("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.쓰기("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.쓰기(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        확인(결과 == 0, 100 + 결과);
        단말.쓰기("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        확인(보드.사용자검사() == 0, 200);
        단말.쓰기("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.사용자실행(0);
        if (처음결과 != 0) { 단말.쓰기("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        확인(처음결과 == 0, 201);
        단말.쓰기("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int 번호 = 0; 번호 < 예상.length; 번호++) {
            단말.쓰기("USER CHECK "); 단말.수(번호); 단말.문자(10);
            int 결과 = 보드.사용자실행(번호 + 1);
            if (결과 != 예상[번호]) { 단말.쓰기("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            확인(결과 == 예상[번호], 210 + 번호);
        }
        확인(보드.사용자실행(0) == 0, 220);
        단말.쓰기("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.사용자실행(9);
        if (결과 != 0) { 단말.쓰기("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        확인(결과 == 0, 230);
    }
    static void 정보() {
        단말.쓰기("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.쓰기("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.쓰기("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.쓰기("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.쓰기("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void 시작() {
        단말.쓰기("WorldOS chm · chm · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.쓰기("NATIVE READY\n");
        명령해석기.실행();
    }
}
