// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** eget Java 커널의 Pi4 opprinnelig_tilstand 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kjerne {
    static int[] 작업횟수 = new int[3];
    static int[] oppgave_SUMMER = new int[3];
    static int oppgave_ordre;
    static int oppgave_feil;
    static int 난수씨 = 17;

    static void bekrefte(boolean vilkår, int INDEKS) {
        if (!vilkår) { 단말.Skriv("FAIL "); 단말.nummer(INDEKS); Tavle.Stopp(INDEKS); }
    }
    static int gren(int VERDI) {
        switch (VERDI) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VERDI) {
        switch (VERDI) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] return_MATRISE(int[] MATRISE_VERDI) { return MATRISE_VERDI; }
    static void 계산시험() {
        int VERDI = 난수씨;
        bekrefte(VERDI * 7 - VERDI == 102 && VERDI / 3 == 5 && VERDI % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        bekrefte(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        bekrefte(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        bekrefte((-VERDI >> 2) == -5 && (-VERDI >>> 2) == 1073741819 && (VERDI << 33) == 34, 4);
        bekrefte((byte)(VERDI * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] MATRISE_VERDI = new int[5];
        for (int Loop_INDEKS = 0; Loop_INDEKS < MATRISE_VERDI.length; Loop_INDEKS++) MATRISE_VERDI[Loop_INDEKS] = Loop_INDEKS * VERDI;
        MATRISE_VERDI[2]++;
        bekrefte(return_MATRISE(MATRISE_VERDI) == MATRISE_VERDI && MATRISE_VERDI[2] == 35 && MATRISE_VERDI[4] == 68, 6);
        bekrefte(gren(VERDI - 117) == 7 && gren(VERDI - 15) == 9 && gren(VERDI) == 3 && 촘촘분기(VERDI - 15) == 17, 7);
        String Tekst = "한글 😀";
        bekrefte(Tekst.length() == 5 && Tekst.charAt(0) == '한' && Tekst.charAt(3) == 0xd83d, 8);
        bekrefte(Tavle.CPU_rettighet_nivå() == 1, 9);
        단말.Skriv("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEKS) {
        // AVKAST_CPU 전후 lokal_Omfang 변수가 보존되는지 검사: 각 작업은 독립된 maskin 스택을 쓴다.
        int lokal_VERDI = INDEKS * 100;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 10; Loop_INDEKS++) {
            if (oppgave_ordre % 2 + 1 != INDEKS) oppgave_feil++;
            oppgave_ordre++;
            lokal_VERDI += Loop_INDEKS + INDEKS;
            oppgave_SUMMER[INDEKS] = lokal_VERDI;
            작업횟수[INDEKS]++;
            Tavle.AVKAST_CPU();
            if (lokal_VERDI != oppgave_SUMMER[INDEKS]) oppgave_feil++;
        }
    }
    static void test_Tasks() {
        oppgave_ordre = 0; oppgave_feil = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        bekrefte(Tavle.åpne_oppgave(1) == 0 && Tavle.åpne_oppgave(2) == 0, 20);
        int rotasjon_ANTALL = 0;
        while (Tavle.oppgave_status(1) != 0 || Tavle.oppgave_status(2) != 0) {
            Tavle.AVKAST_CPU();
            bekrefte(++rotasjon_ANTALL < 100, 21);
        }
        bekrefte(작업횟수[1] == 10 && 작업횟수[2] == 10 && oppgave_ordre == 20 && oppgave_feil == 0, 22);
        bekrefte(oppgave_SUMMER[1] == 155 && oppgave_SUMMER[2] == 265, 23);
        단말.Skriv("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void rektangel(int 가로, int vertikal_plassere, int 너비, int 높이, int 색) {
        for (int Y_koordinat = vertikal_plassere; Y_koordinat < vertikal_plassere + 높이; Y_koordinat++)
            for (int x_koordinat = 가로; x_koordinat < 가로 + 너비; x_koordinat++) Tavle.화면점(x_koordinat, Y_koordinat, 색);
    }
    static void skjermbilde() {
        if (Tavle.Forbered_skjermbilde() == 0) { 단말.Skriv("FRAMEBUFFER unavailable\n"); return; }
        rektangel(0, 0, Tavle.화면너비(), Tavle.화면높이(), 0x302018);
        rektangel(40, 40, 560, 400, 0xefe8e2);
        rektangel(40, 40, 560, 40, 0x905020);
        rektangel(60, 110, 240, 140, 0x90b050);
        rektangel(320, 110, 260, 140, 0xd0a040);
        rektangel(60, 290, 520, 120, 0xd8d0c8);
        단말.Skriv("FRAMEBUFFER PASS "); 단말.nummer(Tavle.화면너비()); 단말.문자('x');
        단말.nummer(Tavle.화면높이()); 단말.Skriv(" RGB32 (drawing only)\n");
    }
    static void test_C() {
        int KR = Tavle.씨플러스시험();
        bekrefte(KR == 0, 100 + KR);
        단말.Skriv("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        bekrefte(Tavle.sjekk_bruker_app() == 0, 200);
        단말.Skriv("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Tavle.kjøre_bruker_app(0);
        if (처음결과 != 0) { 단말.Skriv("USER DEMO RESULT "); 단말.nummer(처음결과); 단말.문자(10); }
        bekrefte(처음결과 == 0, 201);
        단말.Skriv("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEKS = 0; INDEKS < 예상.length; INDEKS++) {
            단말.Skriv("USER CHECK "); 단말.nummer(INDEKS); 단말.문자(10);
            int KR = Tavle.kjøre_bruker_app(INDEKS + 1);
            if (KR != 예상[INDEKS]) { 단말.Skriv("USER RESULT "); 단말.nummer(KR); 단말.문자(10); }
            bekrefte(KR == 예상[INDEKS], 210 + INDEKS);
        }
        bekrefte(Tavle.kjøre_bruker_app(0) == 0, 220);
        단말.Skriv("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void test_Nettverk() {
        int KR = Tavle.kjøre_bruker_app(9);
        if (KR != 0) { 단말.Skriv("UDP RESULT "); 단말.nummer(KR); 단말.문자(10); }
        bekrefte(KR == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Skriv("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Skriv("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Skriv("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Skriv("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Skriv("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Kjør_2() {
        단말.Skriv("WorldOS nb · Hei · 😀\n");
        계산시험();
        test_C();
        test_Tasks();
        skjermbilde();
        사용자시험();
        test_Nettverk();
        단말.Skriv("NATIVE READY\n");
        명령해석기.Utfør_kommando();
    }
}
