// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class xoox {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int ligeey_toftale;
    static int ligeey_njumte;
    static int 난수씨 = 17;

    static void luñutu(boolean anam, int àlluwa_tur) {
        if (!anam) { 단말.biir("FAIL "); 단말.수(àlluwa_tur); 보드.tees(àlluwa_tur); }
    }
    static int car(int xëyma) {
        switch (xëyma) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int xëyma) {
        switch (xëyma) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] TABLO_xëyma) { return TABLO_xëyma; }
    static void 계산시험() {
        int xëyma = 난수씨;
        luñutu(xëyma * 7 - xëyma == 102 && xëyma / 3 == 5 && xëyma % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        luñutu(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        luñutu(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        luñutu((-xëyma >> 2) == -5 && (-xëyma >>> 2) == 1073741819 && (xëyma << 33) == 34, 4);
        luñutu((byte)(xëyma * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] TABLO_xëyma = new int[5];
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < TABLO_xëyma.length; wërngël_àlluwa_tur++) TABLO_xëyma[wërngël_àlluwa_tur] = wërngël_àlluwa_tur * xëyma;
        TABLO_xëyma[2]++;
        luñutu(배열돌려주기(TABLO_xëyma) == TABLO_xëyma && TABLO_xëyma[2] == 35 && TABLO_xëyma[4] == 68, 6);
        luñutu(car(xëyma - 117) == 7 && car(xëyma - 15) == 9 && car(xëyma) == 3 && 촘촘분기(xëyma - 15) == 17, 7);
        String Tekst = "한글 😀";
        luñutu(Tekst.length() == 5 && Tekst.charAt(0) == '한' && Tekst.charAt(3) == 0xd83d, 8);
        luñutu(보드.시피유권한() == 1, 9);
        단말.biir("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int àlluwa_tur) {
        // dakkal_UC 전후 dënnd_nameef 변수가 보존되는지 검사: 각 작업은 독립된 masin 스택을 쓴다.
        int dënnd_xëyma = àlluwa_tur * 100;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 10; wërngël_àlluwa_tur++) {
            if (ligeey_toftale % 2 + 1 != àlluwa_tur) ligeey_njumte++;
            ligeey_toftale++;
            dënnd_xëyma += wërngël_àlluwa_tur + àlluwa_tur;
            작업합[àlluwa_tur] = dënnd_xëyma;
            작업횟수[àlluwa_tur]++;
            보드.dakkal_UC();
            if (dënnd_xëyma != 작업합[àlluwa_tur]) ligeey_njumte++;
        }
    }
    static void 작업시험() {
        ligeey_toftale = 0; ligeey_njumte = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        luñutu(보드.sos_ligeey(1) == 0 && 보드.sos_ligeey(2) == 0, 20);
        int 회전 = 0;
        while (보드.ligeey_nekkin(1) != 0 || 보드.ligeey_nekkin(2) != 0) {
            보드.dakkal_UC();
            luñutu(++회전 < 100, 21);
        }
        luñutu(작업횟수[1] == 10 && 작업횟수[2] == 10 && ligeey_toftale == 20 && ligeey_njumte == 0, 22);
        luñutu(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.biir("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int rëddu_iks_yi = 가로; rëddu_iks_yi < 가로 + 너비; rëddu_iks_yi++) 보드.화면점(rëddu_iks_yi, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.biir("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.biir("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.biir(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        luñutu(결과 == 0, 100 + 결과);
        단말.biir("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        luñutu(보드.sek_kiy_jariñoo_internet_jëfekaay() == 0, 200);
        단말.biir("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.daw_kiy_jariñoo_internet_jëfekaay(0);
        if (처음결과 != 0) { 단말.biir("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        luñutu(처음결과 == 0, 201);
        단말.biir("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int àlluwa_tur = 0; àlluwa_tur < 예상.length; àlluwa_tur++) {
            단말.biir("USER CHECK "); 단말.수(àlluwa_tur); 단말.문자(10);
            int 결과 = 보드.daw_kiy_jariñoo_internet_jëfekaay(àlluwa_tur + 1);
            if (결과 != 예상[àlluwa_tur]) { 단말.biir("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            luñutu(결과 == 예상[àlluwa_tur], 210 + àlluwa_tur);
        }
        luñutu(보드.daw_kiy_jariñoo_internet_jëfekaay(0) == 0, 220);
        단말.biir("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.daw_kiy_jariñoo_internet_jëfekaay(9);
        if (결과 != 0) { 단말.biir("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        luñutu(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.biir("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.biir("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.biir("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.biir("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.biir("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void daw() {
        단말.biir("WorldOS wo · Wolof · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.biir("NATIVE READY\n");
        명령해석기.def_ndigel();
    }
}
