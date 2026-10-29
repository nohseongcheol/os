// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kernel {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int ᏯᏛᏁᏗ_ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ;
    static int ᏯᏛᏁᏗ_ᎦᎵᏓᏍᏔᏅ;
    static int 난수씨 = 17;

    static void ᎰᎯᏳᏓ(boolean ᎤᏍᏗᏓᏅ, int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        if (!ᎤᏍᏗᏓᏅ) { 단말.ᎪᏪᎶᏗ("FAIL "); 단말.수(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ); 보드.ᎭᎴᏫᏍᏓ(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ); }
    }
    static int 분기(int ᏧᎬᏩᎶᏗᏯ) {
        switch (ᏧᎬᏩᎶᏗᏯ) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int ᏧᎬᏩᎶᏗᏯ) {
        switch (ᏧᎬᏩᎶᏗᏯ) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] array_ᏧᎬᏩᎶᏗᏯ) { return array_ᏧᎬᏩᎶᏗᏯ; }
    static void 계산시험() {
        int ᏧᎬᏩᎶᏗᏯ = 난수씨;
        ᎰᎯᏳᏓ(ᏧᎬᏩᎶᏗᏯ * 7 - ᏧᎬᏩᎶᏗᏯ == 102 && ᏧᎬᏩᎶᏗᏯ / 3 == 5 && ᏧᎬᏩᎶᏗᏯ % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        ᎰᎯᏳᏓ(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        ᎰᎯᏳᏓ(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        ᎰᎯᏳᏓ((-ᏧᎬᏩᎶᏗᏯ >> 2) == -5 && (-ᏧᎬᏩᎶᏗᏯ >>> 2) == 1073741819 && (ᏧᎬᏩᎶᏗᏯ << 33) == 34, 4);
        ᎰᎯᏳᏓ((byte)(ᏧᎬᏩᎶᏗᏯ * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] array_ᏧᎬᏩᎶᏗᏯ = new int[5];
        for (int ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < array_ᏧᎬᏩᎶᏗᏯ.length; ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) array_ᏧᎬᏩᎶᏗᏯ[ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] = ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ * ᏧᎬᏩᎶᏗᏯ;
        array_ᏧᎬᏩᎶᏗᏯ[2]++;
        ᎰᎯᏳᏓ(배열돌려주기(array_ᏧᎬᏩᎶᏗᏯ) == array_ᏧᎬᏩᎶᏗᏯ && array_ᏧᎬᏩᎶᏗᏯ[2] == 35 && array_ᏧᎬᏩᎶᏗᏯ[4] == 68, 6);
        ᎰᎯᏳᏓ(분기(ᏧᎬᏩᎶᏗᏯ - 117) == 7 && 분기(ᏧᎬᏩᎶᏗᏯ - 15) == 9 && 분기(ᏧᎬᏩᎶᏗᏯ) == 3 && 촘촘분기(ᏧᎬᏩᎶᏗᏯ - 15) == 17, 7);
        String ᎠᎪᎵᏰᏗ = "한글 😀";
        ᎰᎯᏳᏓ(ᎠᎪᎵᏰᏗ.length() == 5 && ᎠᎪᎵᏰᏗ.charAt(0) == '한' && ᎠᎪᎵᏰᏗ.charAt(3) == 0xd83d, 8);
        ᎰᎯᏳᏓ(보드.시피유권한() == 1, 9);
        단말.ᎪᏪᎶᏗ("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        // ᏗᏲᎯᏍᏗᎢ_CPU 전후 ᎡᏍᎦᏂ_ᎢᎦᎢ 변수가 보존되는지 검사: 각 작업은 독립된 기계 스택을 쓴다.
        int ᎡᏍᎦᏂ_ᏧᎬᏩᎶᏗᏯ = ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ * 100;
        for (int ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 10; ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
            if (ᏯᏛᏁᏗ_ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ % 2 + 1 != ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) ᏯᏛᏁᏗ_ᎦᎵᏓᏍᏔᏅ++;
            ᏯᏛᏁᏗ_ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ++;
            ᎡᏍᎦᏂ_ᏧᎬᏩᎶᏗᏯ += ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ + ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ;
            작업합[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] = ᎡᏍᎦᏂ_ᏧᎬᏩᎶᏗᏯ;
            작업횟수[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ]++;
            보드.ᏗᏲᎯᏍᏗᎢ_CPU();
            if (ᎡᏍᎦᏂ_ᏧᎬᏩᎶᏗᏯ != 작업합[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ]) ᏯᏛᏁᏗ_ᎦᎵᏓᏍᏔᏅ++;
        }
    }
    static void 작업시험() {
        ᏯᏛᏁᏗ_ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ = 0; ᏯᏛᏁᏗ_ᎦᎵᏓᏍᏔᏅ = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        ᎰᎯᏳᏓ(보드.작업만들기(1) == 0 && 보드.작업만들기(2) == 0, 20);
        int 회전 = 0;
        while (보드.ᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅ(1) != 0 || 보드.ᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅ(2) != 0) {
            보드.ᏗᏲᎯᏍᏗᎢ_CPU();
            ᎰᎯᏳᏓ(++회전 < 100, 21);
        }
        ᎰᎯᏳᏓ(작업횟수[1] == 10 && 작업횟수[2] == 10 && ᏯᏛᏁᏗ_ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ == 20 && ᏯᏛᏁᏗ_ᎦᎵᏓᏍᏔᏅ == 0, 22);
        ᎰᎯᏳᏓ(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.ᎪᏪᎶᏗ("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int 가로좌표 = 가로; 가로좌표 < 가로 + 너비; 가로좌표++) 보드.화면점(가로좌표, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.ᎪᏪᎶᏗ("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.ᎪᏪᎶᏗ("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.ᎪᏪᎶᏗ(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        ᎰᎯᏳᏓ(결과 == 0, 100 + 결과);
        단말.ᎪᏪᎶᏗ("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        ᎰᎯᏳᏓ(보드.ᎪᎯᏳᏔᏅ_ᎬᏗᏍᎩ_ᎬᏙᏗ() == 0, 200);
        단말.ᎪᏪᎶᏗ("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.ᎠᎢᏎᏍᏗ_ᎬᏗᏍᎩ_ᎬᏙᏗ(0);
        if (처음결과 != 0) { 단말.ᎪᏪᎶᏗ("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        ᎰᎯᏳᏓ(처음결과 == 0, 201);
        단말.ᎪᏪᎶᏗ("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 예상.length; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
            단말.ᎪᏪᎶᏗ("USER CHECK "); 단말.수(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ); 단말.문자(10);
            int 결과 = 보드.ᎠᎢᏎᏍᏗ_ᎬᏗᏍᎩ_ᎬᏙᏗ(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ + 1);
            if (결과 != 예상[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ]) { 단말.ᎪᏪᎶᏗ("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            ᎰᎯᏳᏓ(결과 == 예상[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ], 210 + ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
        }
        ᎰᎯᏳᏓ(보드.ᎠᎢᏎᏍᏗ_ᎬᏗᏍᎩ_ᎬᏙᏗ(0) == 0, 220);
        단말.ᎪᏪᎶᏗ("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.ᎠᎢᏎᏍᏗ_ᎬᏗᏍᎩ_ᎬᏙᏗ(9);
        if (결과 != 0) { 단말.ᎪᏪᎶᏗ("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        ᎰᎯᏳᏓ(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.ᎪᏪᎶᏗ("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.ᎪᏪᎶᏗ("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.ᎪᏪᎶᏗ("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.ᎪᏪᎶᏗ("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.ᎪᏪᎶᏗ("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void ᎠᎢᏎᏍᏗ() {
        단말.ᎪᏪᎶᏗ("WorldOS chr · chr · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.ᎪᏪᎶᏗ("NATIVE READY\n");
        명령해석기.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ();
    }
}
