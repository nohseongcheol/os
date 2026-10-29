// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class eitean {
    static int[] 작업횟수 = new int[3];
    static int[] saothair_SUM = new int[3];
    static int saothair_òrdugh;
    static int saothair_mearachd;
    static int 난수씨 = 17;

    static void dearbh(boolean cumha, int INDEX) {
        if (!cumha) { 단말.sgrìobh("FAIL "); 단말.수(INDEX); bòrd.Stad(INDEX); }
    }
    static int meur(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] return_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        dearbh(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        dearbh(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        dearbh(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        dearbh((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        dearbh((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int lùb_INDEX = 0; lùb_INDEX < ARRAY_VALUE.length; lùb_INDEX++) ARRAY_VALUE[lùb_INDEX] = lùb_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        dearbh(return_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        dearbh(meur(VALUE - 117) == 7 && meur(VALUE - 15) == 9 && meur(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String SMS = "한글 😀";
        dearbh(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        dearbh(bòrd.시피유권한() == 1, 9);
        단말.sgrìobh("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 ionadail_sgòp 변수가 보존되는지 검사: 각 작업은 독립된 inneal 스택을 쓴다.
        int ionadail_VALUE = INDEX * 100;
        for (int lùb_INDEX = 0; lùb_INDEX < 10; lùb_INDEX++) {
            if (saothair_òrdugh % 2 + 1 != INDEX) saothair_mearachd++;
            saothair_òrdugh++;
            ionadail_VALUE += lùb_INDEX + INDEX;
            saothair_SUM[INDEX] = ionadail_VALUE;
            작업횟수[INDEX]++;
            bòrd.YIELD_CPU();
            if (ionadail_VALUE != saothair_SUM[INDEX]) saothair_mearachd++;
        }
    }
    static void 작업시험() {
        saothair_òrdugh = 0; saothair_mearachd = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        dearbh(bòrd.Create_saothair(1) == 0 && bòrd.Create_saothair(2) == 0, 20);
        int cuairteachadh_COUNT = 0;
        while (bòrd.saothair_cor(1) != 0 || bòrd.saothair_cor(2) != 0) {
            bòrd.YIELD_CPU();
            dearbh(++cuairteachadh_COUNT < 100, 21);
        }
        dearbh(작업횟수[1] == 10 && 작업횟수[2] == 10 && saothair_òrdugh == 20 && saothair_mearachd == 0, 22);
        dearbh(saothair_SUM[1] == 155 && saothair_SUM[2] == 265, 23);
        단말.sgrìobh("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int inghearach_suidhich, int 너비, int 높이, int 색) {
        for (int 세로좌표 = inghearach_suidhich; 세로좌표 < inghearach_suidhich + 높이; 세로좌표++)
            for (int co_chomharra_x = 가로; co_chomharra_x < 가로 + 너비; co_chomharra_x++) bòrd.화면점(co_chomharra_x, 세로좌표, 색);
    }
    static void 화면() {
        if (bòrd.화면준비() == 0) { 단말.sgrìobh("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, bòrd.화면너비(), bòrd.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.sgrìobh("FRAMEBUFFER PASS "); 단말.수(bòrd.화면너비()); 단말.문자('x');
        단말.수(bòrd.화면높이()); 단말.sgrìobh(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int tomhas = bòrd.씨플러스시험();
        dearbh(tomhas == 0, 100 + tomhas);
        단말.sgrìobh("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        dearbh(bòrd.seic_cleachdaiche_ap() == 0, 200);
        단말.sgrìobh("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = bòrd.ruith_cleachdaiche_ap(0);
        if (처음결과 != 0) { 단말.sgrìobh("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        dearbh(처음결과 == 0, 201);
        단말.sgrìobh("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.sgrìobh("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int tomhas = bòrd.ruith_cleachdaiche_ap(INDEX + 1);
            if (tomhas != 예상[INDEX]) { 단말.sgrìobh("USER RESULT "); 단말.수(tomhas); 단말.문자(10); }
            dearbh(tomhas == 예상[INDEX], 210 + INDEX);
        }
        dearbh(bòrd.ruith_cleachdaiche_ap(0) == 0, 220);
        단말.sgrìobh("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int tomhas = bòrd.ruith_cleachdaiche_ap(9);
        if (tomhas != 0) { 단말.sgrìobh("UDP RESULT "); 단말.수(tomhas); 단말.문자(10); }
        dearbh(tomhas == 0, 230);
    }
    static void msinfo32_exe() {
        단말.sgrìobh("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.sgrìobh("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.sgrìobh("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.sgrìobh("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.sgrìobh("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void ruith() {
        단말.sgrìobh("WorldOS gd · gd · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.sgrìobh("NATIVE READY\n");
        명령해석기.gnìomhaich_àithne();
    }
}
