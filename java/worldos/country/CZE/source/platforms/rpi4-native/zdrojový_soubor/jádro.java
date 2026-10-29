// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** vlastní Java 커널의 Pi4 počáteční_stav 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class jádro {
    static int[] 작업횟수 = new int[3];
    static int[] úkol_SUMA = new int[3];
    static int úkol_pořadí;
    static int úkol_chyba;
    static int 난수씨 = 17;

    static void ověřit(boolean podmínka, int INDEX) {
        if (!podmínka) { 단말.Zápis("FAIL "); 단말.číslo(INDEX); Panel.Zastavit(INDEX); }
    }
    static int větev(int HODNOTA) {
        switch (HODNOTA) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int HODNOTA) {
        switch (HODNOTA) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] Vratka_pole(int[] pole_HODNOTA) { return pole_HODNOTA; }
    static void 계산시험() {
        int HODNOTA = 난수씨;
        ověřit(HODNOTA * 7 - HODNOTA == 102 && HODNOTA / 3 == 5 && HODNOTA % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        ověřit(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        ověřit(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        ověřit((-HODNOTA >> 2) == -5 && (-HODNOTA >>> 2) == 1073741819 && (HODNOTA << 33) == 34, 4);
        ověřit((byte)(HODNOTA * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] pole_HODNOTA = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < pole_HODNOTA.length; Loop_INDEX++) pole_HODNOTA[Loop_INDEX] = Loop_INDEX * HODNOTA;
        pole_HODNOTA[2]++;
        ověřit(Vratka_pole(pole_HODNOTA) == pole_HODNOTA && pole_HODNOTA[2] == 35 && pole_HODNOTA[4] == 68, 6);
        ověřit(větev(HODNOTA - 117) == 7 && větev(HODNOTA - 15) == 9 && větev(HODNOTA) == 3 && 촘촘분기(HODNOTA - 15) == 17, 7);
        String text = "한글 😀";
        ověřit(text.length() == 5 && text.charAt(0) == '한' && text.charAt(3) == 0xd83d, 8);
        ověřit(Panel.CPU_oprávnění_úroveň() == 1, 9);
        단말.Zápis("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 místní_obor 변수가 보존되는지 검사: 각 작업은 독립된 počítač 스택을 쓴다.
        int místní_HODNOTA = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (úkol_pořadí % 2 + 1 != INDEX) úkol_chyba++;
            úkol_pořadí++;
            místní_HODNOTA += Loop_INDEX + INDEX;
            úkol_SUMA[INDEX] = místní_HODNOTA;
            작업횟수[INDEX]++;
            Panel.YIELD_CPU();
            if (místní_HODNOTA != úkol_SUMA[INDEX]) úkol_chyba++;
        }
    }
    static void test_Tasks() {
        úkol_pořadí = 0; úkol_chyba = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        ověřit(Panel.Create_úkol(1) == 0 && Panel.Create_úkol(2) == 0, 20);
        int rotace_POČET = 0;
        while (Panel.úkol_Stav(1) != 0 || Panel.úkol_Stav(2) != 0) {
            Panel.YIELD_CPU();
            ověřit(++rotace_POČET < 100, 21);
        }
        ověřit(작업횟수[1] == 10 && 작업횟수[2] == 10 && úkol_pořadí == 20 && úkol_chyba == 0, 22);
        ověřit(úkol_SUMA[1] == 155 && úkol_SUMA[2] == 265, 23);
        단말.Zápis("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void obdélník(int 가로, int Svislá_pozice, int 너비, int výška_HODNOTA, int 색) {
        for (int Y_souřadnice = Svislá_pozice; Y_souřadnice < Svislá_pozice + výška_HODNOTA; Y_souřadnice++)
            for (int souřadnice_x = 가로; souřadnice_x < 가로 + 너비; souřadnice_x++) Panel.화면점(souřadnice_x, Y_souřadnice, 색);
    }
    static void 화면() {
        if (Panel.화면준비() == 0) { 단말.Zápis("FRAMEBUFFER unavailable\n"); return; }
        obdélník(0, 0, Panel.화면너비(), Panel.화면높이(), 0x302018);
        obdélník(40, 40, 560, 400, 0xefe8e2);
        obdélník(40, 40, 560, 40, 0x905020);
        obdélník(60, 110, 240, 140, 0x90b050);
        obdélník(320, 110, 260, 140, 0xd0a040);
        obdélník(60, 290, 520, 120, 0xd8d0c8);
        단말.Zápis("FRAMEBUFFER PASS "); 단말.číslo(Panel.화면너비()); 단말.문자('x');
        단말.číslo(Panel.화면높이()); 단말.Zápis(" RGB32 (drawing only)\n");
    }
    static void test_C() {
        int VÝSLEDEK = Panel.씨플러스시험();
        ověřit(VÝSLEDEK == 0, 100 + VÝSLEDEK);
        단말.Zápis("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        ověřit(Panel.šek_uživatel_program() == 0, 200);
        단말.Zápis("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Panel.spustit_uživatel_program(0);
        if (처음결과 != 0) { 단말.Zápis("USER DEMO RESULT "); 단말.číslo(처음결과); 단말.문자(10); }
        ověřit(처음결과 == 0, 201);
        단말.Zápis("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Zápis("USER CHECK "); 단말.číslo(INDEX); 단말.문자(10);
            int VÝSLEDEK = Panel.spustit_uživatel_program(INDEX + 1);
            if (VÝSLEDEK != 예상[INDEX]) { 단말.Zápis("USER RESULT "); 단말.číslo(VÝSLEDEK); 단말.문자(10); }
            ověřit(VÝSLEDEK == 예상[INDEX], 210 + INDEX);
        }
        ověřit(Panel.spustit_uživatel_program(0) == 0, 220);
        단말.Zápis("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void test_Sítě() {
        int VÝSLEDEK = Panel.spustit_uživatel_program(9);
        if (VÝSLEDEK != 0) { 단말.Zápis("UDP RESULT "); 단말.číslo(VÝSLEDEK); 단말.문자(10); }
        ověřit(VÝSLEDEK == 0, 230);
    }
    static void Informace_o_systému() {
        단말.Zápis("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Zápis("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Zápis("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Zápis("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Zápis("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Spustit_2() {
        단말.Zápis("WorldOS cs · čeština · 😀\n");
        계산시험();
        test_C();
        test_Tasks();
        화면();
        사용자시험();
        test_Sítě();
        단말.Zápis("NATIVE READY\n");
        příkaz_interpret.Provést_příkaz();
    }
}
