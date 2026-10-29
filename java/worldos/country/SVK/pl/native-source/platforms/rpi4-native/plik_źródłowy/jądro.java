// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** własny Java 커널의 Pi4 stan_początkowy 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class jądro {
    static int[] 작업횟수 = new int[3];
    static int[] zadanie_SUMA = new int[3];
    static int zadanie_zamówić;
    static int zadanie_błąd;
    static int losowy_umieścić = 17;

    static void 확인(boolean choroba, int INDEKS) {
        if (!choroba) { 단말.Zapis("FAIL "); 단말.identyfikator(INDEKS); Tablica.Zatrzymaj(INDEKS); }
    }
    static int gałąź_22e01337(int WARTOŚĆ) {
        switch (WARTOŚĆ) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int WARTOŚĆ) {
        switch (WARTOŚĆ) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] Zwrot_TABLICA(int[] TABLICA_WARTOŚĆ) { return TABLICA_WARTOŚĆ; }
    static void 계산시험() {
        int WARTOŚĆ = losowy_umieścić;
        확인(WARTOŚĆ * 7 - WARTOŚĆ == 102 && WARTOŚĆ / 3 == 5 && WARTOŚĆ % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        확인(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        확인(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        확인((-WARTOŚĆ >> 2) == -5 && (-WARTOŚĆ >>> 2) == 1073741819 && (WARTOŚĆ << 33) == 34, 4);
        확인((byte)(WARTOŚĆ * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] TABLICA_WARTOŚĆ = new int[5];
        for (int Loop_INDEKS = 0; Loop_INDEKS < TABLICA_WARTOŚĆ.length; Loop_INDEKS++) TABLICA_WARTOŚĆ[Loop_INDEKS] = Loop_INDEKS * WARTOŚĆ;
        TABLICA_WARTOŚĆ[2]++;
        확인(Zwrot_TABLICA(TABLICA_WARTOŚĆ) == TABLICA_WARTOŚĆ && TABLICA_WARTOŚĆ[2] == 35 && TABLICA_WARTOŚĆ[4] == 68, 6);
        확인(gałąź_22e01337(WARTOŚĆ - 117) == 7 && gałąź_22e01337(WARTOŚĆ - 15) == 9 && gałąź_22e01337(WARTOŚĆ) == 3 && 촘촘분기(WARTOŚĆ - 15) == 17, 7);
        String tekst = "한글 😀";
        확인(tekst.length() == 5 && tekst.charAt(0) == '한' && tekst.charAt(3) == 0xd83d, 8);
        확인(Tablica.CPU_uprawnienie_poziom() == 1, 9);
        단말.Zapis("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEKS) {
        // Dochód_CPU 전후 lokalny_Scope 변수가 보존되는지 검사: 각 작업은 독립된 maszyna 스택을 쓴다.
        int lokalny_WARTOŚĆ = INDEKS * 100;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 10; Loop_INDEKS++) {
            if (zadanie_zamówić % 2 + 1 != INDEKS) zadanie_błąd++;
            zadanie_zamówić++;
            lokalny_WARTOŚĆ += Loop_INDEKS + INDEKS;
            zadanie_SUMA[INDEKS] = lokalny_WARTOŚĆ;
            작업횟수[INDEKS]++;
            Tablica.Dochód_CPU();
            if (lokalny_WARTOŚĆ != zadanie_SUMA[INDEKS]) zadanie_błąd++;
        }
    }
    static void test_Tasks() {
        zadanie_zamówić = 0; zadanie_błąd = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        확인(Tablica.Twórca_zadanie(1) == 0 && Tablica.Twórca_zadanie(2) == 0, 20);
        int obrót_ILE_LICZB = 0;
        while (Tablica.zadanie_Stan(1) != 0 || Tablica.zadanie_Stan(2) != 0) {
            Tablica.Dochód_CPU();
            확인(++obrót_ILE_LICZB < 100, 21);
        }
        확인(작업횟수[1] == 10 && 작업횟수[2] == 10 && zadanie_zamówić == 20 && zadanie_błąd == 0, 22);
        확인(zadanie_SUMA[1] == 155 && zadanie_SUMA[2] == 265, 23);
        단말.Zapis("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void prostokąt(int 가로, int gałąź_stanowisko, int 너비, int wysokość_WARTOŚĆ, int 색) {
        for (int Y_współrzędna = gałąź_stanowisko; Y_współrzędna < gałąź_stanowisko + wysokość_WARTOŚĆ; Y_współrzędna++)
            for (int współrzędna_X = 가로; współrzędna_X < 가로 + 너비; współrzędna_X++) Tablica.화면점(współrzędna_X, Y_współrzędna, 색);
    }
    static void 화면() {
        if (Tablica.화면준비() == 0) { 단말.Zapis("FRAMEBUFFER unavailable\n"); return; }
        prostokąt(0, 0, Tablica.화면너비(), Tablica.화면높이(), 0x302018);
        prostokąt(40, 40, 560, 400, 0xefe8e2);
        prostokąt(40, 40, 560, 40, 0x905020);
        prostokąt(60, 110, 240, 140, 0x90b050);
        prostokąt(320, 110, 260, 140, 0xd0a040);
        prostokąt(60, 290, 520, 120, 0xd8d0c8);
        단말.Zapis("FRAMEBUFFER PASS "); 단말.identyfikator(Tablica.화면너비()); 단말.문자('x');
        단말.identyfikator(Tablica.화면높이()); 단말.Zapis(" RGB32 (drawing only)\n");
    }
    static void test_C() {
        int WYNIK = Tablica.씨플러스시험();
        확인(WYNIK == 0, 100 + WYNIK);
        단말.Zapis("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        확인(Tablica.czek_użytkownik_program() == 0, 200);
        단말.Zapis("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Tablica.przebieg_użytkownik_program(0);
        if (처음결과 != 0) { 단말.Zapis("USER DEMO RESULT "); 단말.identyfikator(처음결과); 단말.문자(10); }
        확인(처음결과 == 0, 201);
        단말.Zapis("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEKS = 0; INDEKS < 예상.length; INDEKS++) {
            단말.Zapis("USER CHECK "); 단말.identyfikator(INDEKS); 단말.문자(10);
            int WYNIK = Tablica.przebieg_użytkownik_program(INDEKS + 1);
            if (WYNIK != 예상[INDEKS]) { 단말.Zapis("USER RESULT "); 단말.identyfikator(WYNIK); 단말.문자(10); }
            확인(WYNIK == 예상[INDEKS], 210 + INDEKS);
        }
        확인(Tablica.przebieg_użytkownik_program(0) == 0, 220);
        단말.Zapis("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void test_Sieć() {
        int WYNIK = Tablica.przebieg_użytkownik_program(9);
        if (WYNIK != 0) { 단말.Zapis("UDP RESULT "); 단말.identyfikator(WYNIK); 단말.문자(10); }
        확인(WYNIK == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Zapis("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Zapis("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Zapis("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Zapis("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Zapis("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Uruchom_2() {
        단말.Zapis("WorldOS pl · Witaj · 😀\n");
        계산시험();
        test_C();
        test_Tasks();
        화면();
        사용자시험();
        test_Sieć();
        단말.Zapis("NATIVE READY\n");
        polecenie_interpreter.Wykonaj_polecenie();
    }
}
