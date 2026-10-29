// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** vlastné Java 커널의 Pi4 počiatočný_stav 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class jadro {
    static int[] 작업횟수 = new int[3];
    static int[] úloha_SUM = new int[3];
    static int úloha_poradie;
    static int úloha_Chyba;
    static int náhodný_počiatočná_hodnota = 17;

    static void overiť(boolean podmienka, int INDEX) {
        if (!podmienka) { 단말.Zápis("FAIL "); 단말.수(INDEX); Panel.Zastaviť(INDEX); }
    }
    static int vetva(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] vrátiť_pole(int[] pole_VALUE) { return pole_VALUE; }
    static void 계산시험() {
        int VALUE = náhodný_počiatočná_hodnota;
        overiť(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        overiť(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        overiť(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        overiť((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        overiť((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] pole_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < pole_VALUE.length; Loop_INDEX++) pole_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        pole_VALUE[2]++;
        overiť(vrátiť_pole(pole_VALUE) == pole_VALUE && pole_VALUE[2] == 35 && pole_VALUE[4] == 68, 6);
        overiť(vetva(VALUE - 117) == 7 && vetva(VALUE - 15) == 9 && vetva(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Spracovanie_textu = "한글 😀";
        overiť(Spracovanie_textu.length() == 5 && Spracovanie_textu.charAt(0) == '한' && Spracovanie_textu.charAt(3) == 0xd83d, 8);
        overiť(Panel.procesor_povolenie_úroveň() == 1, 9);
        단말.Zápis("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_procesor 전후 miestny_Rozsah 변수가 보존되는지 검사: 각 작업은 독립된 počítač_5eb260fa 스택을 쓴다.
        int miestny_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (úloha_poradie % 2 + 1 != INDEX) úloha_Chyba++;
            úloha_poradie++;
            miestny_VALUE += Loop_INDEX + INDEX;
            úloha_SUM[INDEX] = miestny_VALUE;
            작업횟수[INDEX]++;
            Panel.YIELD_procesor();
            if (miestny_VALUE != úloha_SUM[INDEX]) úloha_Chyba++;
        }
    }
    static void test_Tasks() {
        úloha_poradie = 0; úloha_Chyba = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        overiť(Panel.Create_úloha(1) == 0 && Panel.Create_úloha(2) == 0, 20);
        int otáčanie_COUNT = 0;
        while (Panel.úloha_Stav(1) != 0 || Panel.úloha_Stav(2) != 0) {
            Panel.YIELD_procesor();
            overiť(++otáčanie_COUNT < 100, 21);
        }
        overiť(작업횟수[1] == 10 && 작업횟수[2] == 10 && úloha_poradie == 20 && úloha_Chyba == 0, 22);
        overiť(úloha_SUM[1] == 155 && úloha_SUM[2] == 265, 23);
        단말.Zápis("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void obdĺžnik(int 가로, int vertikála_pozícia, int 너비, int výška_VALUE, int 색) {
        for (int Y_súradnica = vertikála_pozícia; Y_súradnica < vertikála_pozícia + výška_VALUE; Y_súradnica++)
            for (int X_súradnica = 가로; X_súradnica < 가로 + 너비; X_súradnica++) Panel.화면점(X_súradnica, Y_súradnica, 색);
    }
    static void 화면() {
        if (Panel.화면준비() == 0) { 단말.Zápis("FRAMEBUFFER unavailable\n"); return; }
        obdĺžnik(0, 0, Panel.화면너비(), Panel.화면높이(), 0x302018);
        obdĺžnik(40, 40, 560, 400, 0xefe8e2);
        obdĺžnik(40, 40, 560, 40, 0x905020);
        obdĺžnik(60, 110, 240, 140, 0x90b050);
        obdĺžnik(320, 110, 260, 140, 0xd0a040);
        obdĺžnik(60, 290, 520, 120, 0xd8d0c8);
        단말.Zápis("FRAMEBUFFER PASS "); 단말.수(Panel.화면너비()); 단말.문자('x');
        단말.수(Panel.화면높이()); 단말.Zápis(" RGB32 (drawing only)\n");
    }
    static void test_C() {
        int KR = Panel.씨플러스시험();
        overiť(KR == 0, 100 + KR);
        단말.Zápis("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        overiť(Panel.skontrolovať_používateľ_program() == 0, 200);
        단말.Zápis("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Panel.spustiť_používateľ_program(0);
        if (처음결과 != 0) { 단말.Zápis("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        overiť(처음결과 == 0, 201);
        단말.Zápis("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Zápis("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int KR = Panel.spustiť_používateľ_program(INDEX + 1);
            if (KR != 예상[INDEX]) { 단말.Zápis("USER RESULT "); 단말.수(KR); 단말.문자(10); }
            overiť(KR == 예상[INDEX], 210 + INDEX);
        }
        overiť(Panel.spustiť_používateľ_program(0) == 0, 220);
        단말.Zápis("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void test_Siete() {
        int KR = Panel.spustiť_používateľ_program(9);
        if (KR != 0) { 단말.Zápis("UDP RESULT "); 단말.수(KR); 단말.문자(10); }
        overiť(KR == 0, 230);
    }
    static void Systémové_informácie() {
        단말.Zápis("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Zápis("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Zápis("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Zápis("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Zápis("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Spustiť_2() {
        단말.Zápis("WorldOS sk · Slovenský · 😀\n");
        계산시험();
        test_C();
        test_Tasks();
        화면();
        사용자시험();
        test_Siete();
        단말.Zápis("NATIVE READY\n");
        명령해석기.Vykonať_príkaz();
    }
}
