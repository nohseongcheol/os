// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kjerne {
    static int[] 작업횟수 = new int[3];
    static int[] oppgåve_SUM = new int[3];
    static int oppgåve_rekkjefølgje;
    static int oppgåve_feil;
    static int 난수씨 = 17;

    static void stadfeste(boolean tilstand, int INDEX) {
        if (!tilstand) { 단말.Skriv("FAIL "); 단말.수(INDEX); Tavle.Stopp(INDEX); }
    }
    static int grein(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] levere_tilbake_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        stadfeste(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        stadfeste(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        stadfeste(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        stadfeste((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        stadfeste((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        stadfeste(levere_tilbake_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        stadfeste(grein(VALUE - 117) == 7 && grein(VALUE - 15) == 9 && grein(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Tekst = "한글 😀";
        stadfeste(Tekst.length() == 5 && Tekst.charAt(0) == '한' && Tekst.charAt(3) == 0xd83d, 8);
        stadfeste(Tavle.CPU_løyve_nivå() == 1, 9);
        단말.Skriv("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 lokal_område 변수가 보존되는지 검사: 각 작업은 독립된 maskin 스택을 쓴다.
        int lokal_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (oppgåve_rekkjefølgje % 2 + 1 != INDEX) oppgåve_feil++;
            oppgåve_rekkjefølgje++;
            lokal_VALUE += Loop_INDEX + INDEX;
            oppgåve_SUM[INDEX] = lokal_VALUE;
            작업횟수[INDEX]++;
            Tavle.YIELD_CPU();
            if (lokal_VALUE != oppgåve_SUM[INDEX]) oppgåve_feil++;
        }
    }
    static void 작업시험() {
        oppgåve_rekkjefølgje = 0; oppgåve_feil = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        stadfeste(Tavle.Opprett_oppgåve(1) == 0 && Tavle.Opprett_oppgåve(2) == 0, 20);
        int rotasjon_COUNT = 0;
        while (Tavle.oppgåve_status(1) != 0 || Tavle.oppgåve_status(2) != 0) {
            Tavle.YIELD_CPU();
            stadfeste(++rotasjon_COUNT < 100, 21);
        }
        stadfeste(작업횟수[1] == 10 && 작업횟수[2] == 10 && oppgåve_rekkjefølgje == 20 && oppgåve_feil == 0, 22);
        stadfeste(oppgåve_SUM[1] == 155 && oppgåve_SUM[2] == 265, 23);
        단말.Skriv("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int vertikalvising_plassere, int 너비, int 높이, int 색) {
        for (int Y_koordinat = vertikalvising_plassere; Y_koordinat < vertikalvising_plassere + 높이; Y_koordinat++)
            for (int x_koordinat = 가로; x_koordinat < 가로 + 너비; x_koordinat++) Tavle.화면점(x_koordinat, Y_koordinat, 색);
    }
    static void 화면() {
        if (Tavle.화면준비() == 0) { 단말.Skriv("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, Tavle.화면너비(), Tavle.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Skriv("FRAMEBUFFER PASS "); 단말.수(Tavle.화면너비()); 단말.문자('x');
        단말.수(Tavle.화면높이()); 단말.Skriv(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int forretningsmål = Tavle.씨플러스시험();
        stadfeste(forretningsmål == 0, 100 + forretningsmål);
        단말.Skriv("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        stadfeste(Tavle.sjekk_brukar_app() == 0, 200);
        단말.Skriv("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Tavle.køyre_brukar_app(0);
        if (처음결과 != 0) { 단말.Skriv("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        stadfeste(처음결과 == 0, 201);
        단말.Skriv("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Skriv("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int forretningsmål = Tavle.køyre_brukar_app(INDEX + 1);
            if (forretningsmål != 예상[INDEX]) { 단말.Skriv("USER RESULT "); 단말.수(forretningsmål); 단말.문자(10); }
            stadfeste(forretningsmål == 예상[INDEX], 210 + INDEX);
        }
        stadfeste(Tavle.køyre_brukar_app(0) == 0, 220);
        단말.Skriv("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int forretningsmål = Tavle.køyre_brukar_app(9);
        if (forretningsmål != 0) { 단말.Skriv("UDP RESULT "); 단말.수(forretningsmål); 단말.문자(10); }
        stadfeste(forretningsmål == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Skriv("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Skriv("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Skriv("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Skriv("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Skriv("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Køyr_2() {
        단말.Skriv("WorldOS nn · nn · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Skriv("NATIVE READY\n");
        명령해석기.Utfør_kommando();
    }
}
