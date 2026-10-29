// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** saját Java 커널의 Pi4 kiinduló_állapot 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kernel {
    static int[] 작업횟수 = new int[3];
    static int[] teendő_SUM = new int[3];
    static int teendő_rendel;
    static int teendő_hiba;
    static int véletlenszerű_beültet = 17;

    static void igazol(boolean állapot, int INDEX) {
        if (!állapot) { 단말.Írás("FAIL "); 단말.szám(INDEX); fal.Leállítás(INDEX); }
    }
    static int ág(int ÉRTÉK) {
        switch (ÉRTÉK) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int ÉRTÉK) {
        switch (ÉRTÉK) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] visszaküld_TÖMB(int[] TÖMB_ÉRTÉK) { return TÖMB_ÉRTÉK; }
    static void 계산시험() {
        int ÉRTÉK = véletlenszerű_beültet;
        igazol(ÉRTÉK * 7 - ÉRTÉK == 102 && ÉRTÉK / 3 == 5 && ÉRTÉK % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        igazol(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        igazol(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        igazol((-ÉRTÉK >> 2) == -5 && (-ÉRTÉK >>> 2) == 1073741819 && (ÉRTÉK << 33) == 34, 4);
        igazol((byte)(ÉRTÉK * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] TÖMB_ÉRTÉK = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < TÖMB_ÉRTÉK.length; Loop_INDEX++) TÖMB_ÉRTÉK[Loop_INDEX] = Loop_INDEX * ÉRTÉK;
        TÖMB_ÉRTÉK[2]++;
        igazol(visszaküld_TÖMB(TÖMB_ÉRTÉK) == TÖMB_ÉRTÉK && TÖMB_ÉRTÉK[2] == 35 && TÖMB_ÉRTÉK[4] == 68, 6);
        igazol(ág(ÉRTÉK - 117) == 7 && ág(ÉRTÉK - 15) == 9 && ág(ÉRTÉK) == 3 && 촘촘분기(ÉRTÉK - 15) == 17, 7);
        String Szöveg = "한글 😀";
        igazol(Szöveg.length() == 5 && Szöveg.charAt(0) == '한' && Szöveg.charAt(3) == 0xd83d, 8);
        igazol(fal.CPU_jog_szint() == 1, 9);
        단말.Írás("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // HOZAM_CPU 전후 helyi_hatókör 변수가 보존되는지 검사: 각 작업은 독립된 gép 스택을 쓴다.
        int helyi_ÉRTÉK = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (teendő_rendel % 2 + 1 != INDEX) teendő_hiba++;
            teendő_rendel++;
            helyi_ÉRTÉK += Loop_INDEX + INDEX;
            teendő_SUM[INDEX] = helyi_ÉRTÉK;
            작업횟수[INDEX]++;
            fal.HOZAM_CPU();
            if (helyi_ÉRTÉK != teendő_SUM[INDEX]) teendő_hiba++;
        }
    }
    static void teszt_Tasks() {
        teendő_rendel = 0; teendő_hiba = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        igazol(fal.készít_teendő(1) == 0 && fal.készít_teendő(2) == 0, 20);
        int elforgatás_DARAB = 0;
        while (fal.teendő_Állapot(1) != 0 || fal.teendő_Állapot(2) != 0) {
            fal.HOZAM_CPU();
            igazol(++elforgatás_DARAB < 100, 21);
        }
        igazol(작업횟수[1] == 10 && 작업횟수[2] == 10 && teendő_rendel == 20 && teendő_hiba == 0, 22);
        igazol(teendő_SUM[1] == 155 && teendő_SUM[2] == 265, 23);
        단말.Írás("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void téglalap(int 가로, int szektor_pozíció, int 너비, int 높이, int 색) {
        for (int Y_koordináta = szektor_pozíció; Y_koordináta < szektor_pozíció + 높이; Y_koordináta++)
            for (int x_koordináta = 가로; x_koordináta < 가로 + 너비; x_koordináta++) fal.화면점(x_koordináta, Y_koordináta, 색);
    }
    static void 화면() {
        if (fal.화면준비() == 0) { 단말.Írás("FRAMEBUFFER unavailable\n"); return; }
        téglalap(0, 0, fal.화면너비(), fal.화면높이(), 0x302018);
        téglalap(40, 40, 560, 400, 0xefe8e2);
        téglalap(40, 40, 560, 40, 0x905020);
        téglalap(60, 110, 240, 140, 0x90b050);
        téglalap(320, 110, 260, 140, 0xd0a040);
        téglalap(60, 290, 520, 120, 0xd8d0c8);
        단말.Írás("FRAMEBUFFER PASS "); 단말.szám(fal.화면너비()); 단말.문자('x');
        단말.szám(fal.화면높이()); 단말.Írás(" RGB32 (drawing only)\n");
    }
    static void teszt_C() {
        int KR = fal.씨플러스시험();
        igazol(KR == 0, 100 + KR);
        단말.Írás("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        igazol(fal.csekk_felhasználó_app() == 0, 200);
        단말.Írás("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = fal.futtat_felhasználó_app(0);
        if (처음결과 != 0) { 단말.Írás("USER DEMO RESULT "); 단말.szám(처음결과); 단말.문자(10); }
        igazol(처음결과 == 0, 201);
        단말.Írás("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Írás("USER CHECK "); 단말.szám(INDEX); 단말.문자(10);
            int KR = fal.futtat_felhasználó_app(INDEX + 1);
            if (KR != 예상[INDEX]) { 단말.Írás("USER RESULT "); 단말.szám(KR); 단말.문자(10); }
            igazol(KR == 예상[INDEX], 210 + INDEX);
        }
        igazol(fal.futtat_felhasználó_app(0) == 0, 220);
        단말.Írás("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void teszt_hálózat() {
        int KR = fal.futtat_felhasználó_app(9);
        if (KR != 0) { 단말.Írás("UDP RESULT "); 단말.szám(KR); 단말.문자(10); }
        igazol(KR == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Írás("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Írás("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Írás("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Írás("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Írás("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Futtatás() {
        단말.Írás("WorldOS hu · magyar · 😀\n");
        계산시험();
        teszt_C();
        teszt_Tasks();
        화면();
        사용자시험();
        teszt_hálózat();
        단말.Írás("NATIVE READY\n");
        명령해석기.végrehajt_parancs();
    }
}
