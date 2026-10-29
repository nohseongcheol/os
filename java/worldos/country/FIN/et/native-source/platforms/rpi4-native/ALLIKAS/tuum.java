// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** oma Java 커널의 Pi4 lähteolek 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class tuum {
    static int[] 작업횟수 = new int[3];
    static int[] tööüksus_SUM = new int[3];
    static int tööüksus_tellimus;
    static int tööüksus_tõrge;
    static int juhuslik_seemendama = 17;

    static void kinnitama(boolean tingimus, int INDEX) {
        if (!tingimus) { 단말.Kirjutamine("FAIL "); 단말.number(INDEX); Tahvel.Peata(INDEX); }
    }
    static int haru(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] tagasi_saatma_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = juhuslik_seemendama;
        kinnitama(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        kinnitama(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        kinnitama(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        kinnitama((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        kinnitama((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        kinnitama(tagasi_saatma_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        kinnitama(haru(VALUE - 117) == 7 && haru(VALUE - 15) == 9 && haru(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Tekst = "한글 😀";
        kinnitama(Tekst.length() == 5 && Tekst.charAt(0) == '한' && Tekst.charAt(3) == 0xd83d, 8);
        kinnitama(Tahvel.CPU_luba_tase() == 1, 9);
        단말.Kirjutamine("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 kohalik_skoop 변수가 보존되는지 검사: 각 작업은 독립된 arvuti 스택을 쓴다.
        int kohalik_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (tööüksus_tellimus % 2 + 1 != INDEX) tööüksus_tõrge++;
            tööüksus_tellimus++;
            kohalik_VALUE += Loop_INDEX + INDEX;
            tööüksus_SUM[INDEX] = kohalik_VALUE;
            작업횟수[INDEX]++;
            Tahvel.YIELD_CPU();
            if (kohalik_VALUE != tööüksus_SUM[INDEX]) tööüksus_tõrge++;
        }
    }
    static void 작업시험() {
        tööüksus_tellimus = 0; tööüksus_tõrge = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        kinnitama(Tahvel.avama_tööüksus(1) == 0 && Tahvel.avama_tööüksus(2) == 0, 20);
        int keeramisliigutus_COUNT = 0;
        while (Tahvel.tööüksus_Olek(1) != 0 || Tahvel.tööüksus_Olek(2) != 0) {
            Tahvel.YIELD_CPU();
            kinnitama(++keeramisliigutus_COUNT < 100, 21);
        }
        kinnitama(작업횟수[1] == 10 && 작업횟수[2] == 10 && tööüksus_tellimus == 20 && tööüksus_tõrge == 0, 22);
        kinnitama(tööüksus_SUM[1] == 155 && tööüksus_SUM[2] == 265, 23);
        단말.Kirjutamine("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void ristkülik(int 가로, int vertikaal_ametikoht, int 너비, int 높이, int 색) {
        for (int 세로좌표 = vertikaal_ametikoht; 세로좌표 < vertikaal_ametikoht + 높이; 세로좌표++)
            for (int 가로좌표 = 가로; 가로좌표 < 가로 + 너비; 가로좌표++) Tahvel.화면점(가로좌표, 세로좌표, 색);
    }
    static void 화면() {
        if (Tahvel.화면준비() == 0) { 단말.Kirjutamine("FRAMEBUFFER unavailable\n"); return; }
        ristkülik(0, 0, Tahvel.화면너비(), Tahvel.화면높이(), 0x302018);
        ristkülik(40, 40, 560, 400, 0xefe8e2);
        ristkülik(40, 40, 560, 40, 0x905020);
        ristkülik(60, 110, 240, 140, 0x90b050);
        ristkülik(320, 110, 260, 140, 0xd0a040);
        ristkülik(60, 290, 520, 120, 0xd8d0c8);
        단말.Kirjutamine("FRAMEBUFFER PASS "); 단말.number(Tahvel.화면너비()); 단말.문자('x');
        단말.number(Tahvel.화면높이()); 단말.Kirjutamine(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int TULEMUS = Tahvel.씨플러스시험();
        kinnitama(TULEMUS == 0, 100 + TULEMUS);
        단말.Kirjutamine("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        kinnitama(Tahvel.tšekk_kasutaja_programm() == 0, 200);
        단말.Kirjutamine("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Tahvel.sari_kasutaja_programm(0);
        if (처음결과 != 0) { 단말.Kirjutamine("USER DEMO RESULT "); 단말.number(처음결과); 단말.문자(10); }
        kinnitama(처음결과 == 0, 201);
        단말.Kirjutamine("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Kirjutamine("USER CHECK "); 단말.number(INDEX); 단말.문자(10);
            int TULEMUS = Tahvel.sari_kasutaja_programm(INDEX + 1);
            if (TULEMUS != 예상[INDEX]) { 단말.Kirjutamine("USER RESULT "); 단말.number(TULEMUS); 단말.문자(10); }
            kinnitama(TULEMUS == 예상[INDEX], 210 + INDEX);
        }
        kinnitama(Tahvel.sari_kasutaja_programm(0) == 0, 220);
        단말.Kirjutamine("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int TULEMUS = Tahvel.sari_kasutaja_programm(9);
        if (TULEMUS != 0) { 단말.Kirjutamine("UDP RESULT "); 단말.number(TULEMUS); 단말.문자(10); }
        kinnitama(TULEMUS == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Kirjutamine("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Kirjutamine("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Kirjutamine("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Kirjutamine("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Kirjutamine("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Käivita_2() {
        단말.Kirjutamine("WorldOS et · et · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Kirjutamine("NATIVE READY\n");
        명령해석기.Täida_käsk();
    }
}
