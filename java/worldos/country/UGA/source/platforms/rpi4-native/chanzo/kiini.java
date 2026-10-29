// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kiini {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int kazi_mpangilio;
    static int kazi_kosa;
    static int 난수씨 = 17;

    static void thibitisha(boolean sharti, int kielezo) {
        if (!sharti) { 단말.andika("FAIL "); 단말.수(kielezo); 보드.Simama(kielezo); }
    }
    static int tawi(int thamani) {
        switch (thamani) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int thamani) {
        switch (thamani) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ARRAY_thamani) { return ARRAY_thamani; }
    static void 계산시험() {
        int thamani = 난수씨;
        thibitisha(thamani * 7 - thamani == 102 && thamani / 3 == 5 && thamani % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        thibitisha(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        thibitisha(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        thibitisha((-thamani >> 2) == -5 && (-thamani >>> 2) == 1073741819 && (thamani << 33) == 34, 4);
        thibitisha((byte)(thamani * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_thamani = new int[5];
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < ARRAY_thamani.length; kitanzi_kielezo++) ARRAY_thamani[kitanzi_kielezo] = kitanzi_kielezo * thamani;
        ARRAY_thamani[2]++;
        thibitisha(배열돌려주기(ARRAY_thamani) == ARRAY_thamani && ARRAY_thamani[2] == 35 && ARRAY_thamani[4] == 68, 6);
        thibitisha(tawi(thamani - 117) == 7 && tawi(thamani - 15) == 9 && tawi(thamani) == 3 && 촘촘분기(thamani - 15) == 17, 7);
        String SMS = "한글 😀";
        thibitisha(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        thibitisha(보드.CPU_kibali_kiwango() == 1, 9);
        단말.andika("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int kielezo) {
        // ahirisha_CPU 전후 jirani_upeo 변수가 보존되는지 검사: 각 작업은 독립된 mashine 스택을 쓴다.
        int jirani_thamani = kielezo * 100;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 10; kitanzi_kielezo++) {
            if (kazi_mpangilio % 2 + 1 != kielezo) kazi_kosa++;
            kazi_mpangilio++;
            jirani_thamani += kitanzi_kielezo + kielezo;
            작업합[kielezo] = jirani_thamani;
            작업횟수[kielezo]++;
            보드.ahirisha_CPU();
            if (jirani_thamani != 작업합[kielezo]) kazi_kosa++;
        }
    }
    static void 작업시험() {
        kazi_mpangilio = 0; kazi_kosa = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        thibitisha(보드.unda_kazi(1) == 0 && 보드.unda_kazi(2) == 0, 20);
        int 회전 = 0;
        while (보드.kazi_hali(1) != 0 || 보드.kazi_hali(2) != 0) {
            보드.ahirisha_CPU();
            thibitisha(++회전 < 100, 21);
        }
        thibitisha(작업횟수[1] == 10 && 작업횟수[2] == 10 && kazi_mpangilio == 20 && kazi_kosa == 0, 22);
        thibitisha(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.andika("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int Kitufe_cha_Y_kiratibu = 세로; Kitufe_cha_Y_kiratibu < 세로 + 높이; Kitufe_cha_Y_kiratibu++)
            for (int jira_x = 가로; jira_x < 가로 + 너비; jira_x++) 보드.화면점(jira_x, Kitufe_cha_Y_kiratibu, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.andika("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.andika("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.andika(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        thibitisha(결과 == 0, 100 + 결과);
        단말.andika("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        thibitisha(보드.hundi_mtumiaji_programu() == 0, 200);
        단말.andika("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.endesha_mtumiaji_programu(0);
        if (처음결과 != 0) { 단말.andika("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        thibitisha(처음결과 == 0, 201);
        단말.andika("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int kielezo = 0; kielezo < 예상.length; kielezo++) {
            단말.andika("USER CHECK "); 단말.수(kielezo); 단말.문자(10);
            int 결과 = 보드.endesha_mtumiaji_programu(kielezo + 1);
            if (결과 != 예상[kielezo]) { 단말.andika("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            thibitisha(결과 == 예상[kielezo], 210 + kielezo);
        }
        thibitisha(보드.endesha_mtumiaji_programu(0) == 0, 220);
        단말.andika("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.endesha_mtumiaji_programu(9);
        if (결과 != 0) { 단말.andika("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        thibitisha(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.andika("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.andika("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.andika("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.andika("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.andika("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void endesha() {
        단말.andika("WorldOS sw · Swahili (macrolanguage) · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.andika("NATIVE READY\n");
        명령해석기.tekeleza_amri();
    }
}
