// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class نوغی {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int دنده_اڼن_اوډون;
    static int دنده_تېروتنه;
    static int 난수씨 = 17;

    static void 확인(boolean آړ, int لړیال) {
        if (!آړ) { 단말.لوستل_2("FAIL "); 단말.수(لړیال); 보드.تمول(لړیال); }
    }
    static int 분기(int ارزښت) {
        switch (ارزښت) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int ارزښت) {
        switch (ارزښت) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] لړوند_ارزښت) { return لړوند_ارزښت; }
    static void 계산시험() {
        int ارزښت = 난수씨;
        확인(ارزښت * 7 - ارزښت == 102 && ارزښت / 3 == 5 && ارزښت % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        확인(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        확인(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        확인((-ارزښت >> 2) == -5 && (-ارزښت >>> 2) == 1073741819 && (ارزښت << 33) == 34, 4);
        확인((byte)(ارزښت * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] لړوند_ارزښت = new int[5];
        for (int کړۍ_لړیال = 0; کړۍ_لړیال < لړوند_ارزښت.length; کړۍ_لړیال++) لړوند_ارزښت[کړۍ_لړیال] = کړۍ_لړیال * ارزښت;
        لړوند_ارزښت[2]++;
        확인(배열돌려주기(لړوند_ارزښت) == لړوند_ارزښت && لړوند_ارزښت[2] == 35 && لړوند_ارزښت[4] == 68, 6);
        확인(분기(ارزښت - 117) == 7 && 분기(ارزښت - 15) == 9 && 분기(ارزښت) == 3 && 촘촘분기(ارزښت - 15) == 17, 7);
        String ليکنه = "한글 😀";
        확인(ليکنه.length() == 5 && ليکنه.charAt(0) == '한' && ليکنه.charAt(3) == 0xd83d, 8);
        확인(보드.시피유권한() == 1, 9);
        단말.لوستل_2("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int لړیال) {
        // 양보 전후 지역 변수가 보존되는지 검사: 각 작업은 독립된 기계 스택을 쓴다.
        int 지역값 = لړیال * 100;
        for (int کړۍ_لړیال = 0; کړۍ_لړیال < 10; کړۍ_لړیال++) {
            if (دنده_اڼن_اوډون % 2 + 1 != لړیال) دنده_تېروتنه++;
            دنده_اڼن_اوډون++;
            지역값 += کړۍ_لړیال + لړیال;
            작업합[لړیال] = 지역값;
            작업횟수[لړیال]++;
            보드.양보();
            if (지역값 != 작업합[لړیال]) دنده_تېروتنه++;
        }
    }
    static void 작업시험() {
        دنده_اڼن_اوډون = 0; دنده_تېروتنه = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        확인(보드.작업만들기(1) == 0 && 보드.작업만들기(2) == 0, 20);
        int 회전 = 0;
        while (보드.دنده_انکړ(1) != 0 || 보드.دنده_انکړ(2) != 0) {
            보드.양보();
            확인(++회전 < 100, 21);
        }
        확인(작업횟수[1] == 10 && 작업횟수[2] == 10 && دنده_اڼن_اوډون == 20 && دنده_تېروتنه == 0, 22);
        확인(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.لوستل_2("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int 가로좌표 = 가로; 가로좌표 < 가로 + 너비; 가로좌표++) 보드.화면점(가로좌표, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.لوستل_2("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.لوستل_2("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.لوستل_2(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        확인(결과 == 0, 100 + 결과);
        단말.لوستل_2("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        확인(보드.کتل_کارن_کاريال() == 0, 200);
        단말.لوستل_2("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.사용자실행(0);
        if (처음결과 != 0) { 단말.لوستل_2("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        확인(처음결과 == 0, 201);
        단말.لوستل_2("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int لړیال = 0; لړیال < 예상.length; لړیال++) {
            단말.لوستل_2("USER CHECK "); 단말.수(لړیال); 단말.문자(10);
            int 결과 = 보드.사용자실행(لړیال + 1);
            if (결과 != 예상[لړیال]) { 단말.لوستل_2("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            확인(결과 == 예상[لړیال], 210 + لړیال);
        }
        확인(보드.사용자실행(0) == 0, 220);
        단말.لوستل_2("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.사용자실행(9);
        if (결과 != 0) { 단말.لوستل_2("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        확인(결과 == 0, 230);
    }
    static void 정보() {
        단말.لوستل_2("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.لوستل_2("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.لوستل_2("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.لوستل_2("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.لوستل_2("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void ځغلول() {
        단말.لوستل_2("WorldOS ps · ps · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.لوستل_2("NATIVE READY\n");
        명령해석기.실행();
    }
}
