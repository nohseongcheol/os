// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Eigen Java 커널의 Pi4 begintoestand 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class Kern {
    static int[] 작업횟수 = new int[3];
    static int[] taak_SOM = new int[3];
    static int taak_order;
    static int taak_fout;
    static int willekeurig_seed = 17;

    static void bevestigen(boolean toestand, int INDEX) {
        if (!toestand) { 단말.Schrijven("FAIL "); 단말.nummer(INDEX); Bord.Stoppen(INDEX); }
    }
    static int branch(int WAARDE) {
        switch (WAARDE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int WAARDE) {
        switch (WAARDE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] Retour_MATRIX(int[] MATRIX_WAARDE) { return MATRIX_WAARDE; }
    static void 계산시험() {
        int WAARDE = willekeurig_seed;
        bevestigen(WAARDE * 7 - WAARDE == 102 && WAARDE / 3 == 5 && WAARDE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        bevestigen(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        bevestigen(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        bevestigen((-WAARDE >> 2) == -5 && (-WAARDE >>> 2) == 1073741819 && (WAARDE << 33) == 34, 4);
        bevestigen((byte)(WAARDE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] MATRIX_WAARDE = new int[5];
        for (int lus_INDEX = 0; lus_INDEX < MATRIX_WAARDE.length; lus_INDEX++) MATRIX_WAARDE[lus_INDEX] = lus_INDEX * WAARDE;
        MATRIX_WAARDE[2]++;
        bevestigen(Retour_MATRIX(MATRIX_WAARDE) == MATRIX_WAARDE && MATRIX_WAARDE[2] == 35 && MATRIX_WAARDE[4] == 68, 6);
        bevestigen(branch(WAARDE - 117) == 7 && branch(WAARDE - 15) == 9 && branch(WAARDE) == 3 && 촘촘분기(WAARDE - 15) == 17, 7);
        String tekst = "한글 😀";
        bevestigen(tekst.length() == 5 && tekst.charAt(0) == '한' && tekst.charAt(3) == 0xd83d, 8);
        bevestigen(Bord.CPU_machtiging_niveau() == 1, 9);
        단말.Schrijven("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // RENDEMENT_CPU 전후 lokaal_scope 변수가 보존되는지 검사: 각 작업은 독립된 machine 스택을 쓴다.
        int lokaal_WAARDE = INDEX * 100;
        for (int lus_INDEX = 0; lus_INDEX < 10; lus_INDEX++) {
            if (taak_order % 2 + 1 != INDEX) taak_fout++;
            taak_order++;
            lokaal_WAARDE += lus_INDEX + INDEX;
            taak_SOM[INDEX] = lokaal_WAARDE;
            작업횟수[INDEX]++;
            Bord.RENDEMENT_CPU();
            if (lokaal_WAARDE != taak_SOM[INDEX]) taak_fout++;
        }
    }
    static void test_Tasks() {
        taak_order = 0; taak_fout = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        bevestigen(Bord.maken_taak(1) == 0 && Bord.maken_taak(2) == 0, 20);
        int draaien_AANTAL = 0;
        while (Bord.taak_Status(1) != 0 || Bord.taak_Status(2) != 0) {
            Bord.RENDEMENT_CPU();
            bevestigen(++draaien_AANTAL < 100, 21);
        }
        bevestigen(작업횟수[1] == 10 && 작업횟수[2] == 10 && taak_order == 20 && taak_fout == 0, 22);
        bevestigen(taak_SOM[1] == 155 && taak_SOM[2] == 265, 23);
        단말.Schrijven("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void rechthoek(int 가로, int Verticaal_functie, int 너비, int hoogte_WAARDE, int 색) {
        for (int Y_coördinaat = Verticaal_functie; Y_coördinaat < Verticaal_functie + hoogte_WAARDE; Y_coördinaat++)
            for (int x_coördinaat = 가로; x_coördinaat < 가로 + 너비; x_coördinaat++) Bord.화면점(x_coördinaat, Y_coördinaat, 색);
    }
    static void scherm() {
        if (Bord.Bereid_voor_scherm() == 0) { 단말.Schrijven("FRAMEBUFFER unavailable\n"); return; }
        rechthoek(0, 0, Bord.화면너비(), Bord.scherm_hoogte(), 0x302018);
        rechthoek(40, 40, 560, 400, 0xefe8e2);
        rechthoek(40, 40, 560, 40, 0x905020);
        rechthoek(60, 110, 240, 140, 0x90b050);
        rechthoek(320, 110, 260, 140, 0xd0a040);
        rechthoek(60, 290, 520, 120, 0xd8d0c8);
        단말.Schrijven("FRAMEBUFFER PASS "); 단말.nummer(Bord.화면너비()); 단말.문자('x');
        단말.nummer(Bord.scherm_hoogte()); 단말.Schrijven(" RGB32 (drawing only)\n");
    }
    static void test_C() {
        int resultaat = Bord.씨플러스시험();
        bevestigen(resultaat == 0, 100 + resultaat);
        단말.Schrijven("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        bevestigen(Bord.cheque_gebruiker_app() == 0, 200);
        단말.Schrijven("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Bord.uitvoeren_gebruiker_app(0);
        if (처음결과 != 0) { 단말.Schrijven("USER DEMO RESULT "); 단말.nummer(처음결과); 단말.문자(10); }
        bevestigen(처음결과 == 0, 201);
        단말.Schrijven("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Schrijven("USER CHECK "); 단말.nummer(INDEX); 단말.문자(10);
            int resultaat = Bord.uitvoeren_gebruiker_app(INDEX + 1);
            if (resultaat != 예상[INDEX]) { 단말.Schrijven("USER RESULT "); 단말.nummer(resultaat); 단말.문자(10); }
            bevestigen(resultaat == 예상[INDEX], 210 + INDEX);
        }
        bevestigen(Bord.uitvoeren_gebruiker_app(0) == 0, 220);
        단말.Schrijven("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void test_Netwerken() {
        int resultaat = Bord.uitvoeren_gebruiker_app(9);
        if (resultaat != 0) { 단말.Schrijven("UDP RESULT "); 단말.nummer(resultaat); 단말.문자(10); }
        bevestigen(resultaat == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Schrijven("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Schrijven("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Schrijven("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Schrijven("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Schrijven("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void starten() {
        단말.Schrijven("WorldOS nl · Hallo · 😀\n");
        계산시험();
        test_C();
        test_Tasks();
        scherm();
        사용자시험();
        test_Netwerken();
        단말.Schrijven("NATIVE READY\n");
        Opdrachtvertolker.Uitvoeren_opdracht();
    }
}
