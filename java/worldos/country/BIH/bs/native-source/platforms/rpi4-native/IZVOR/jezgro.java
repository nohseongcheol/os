// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class jezgro {
    static int[] 작업횟수 = new int[3];
    static int[] zadatak_SUM = new int[3];
    static int zadatak_redoslijed;
    static int zadatak_greška;
    static int 난수씨 = 17;

    static void potvrditi(boolean uvjet, int INDEX) {
        if (!uvjet) { 단말.Piši("FAIL "); 단말.수(INDEX); ploča.Zaustavi(INDEX); }
    }
    static int ogranak(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] vratiti_niz(int[] niz_VALUE) { return niz_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        potvrditi(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        potvrditi(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        potvrditi(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        potvrditi((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        potvrditi((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] niz_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < niz_VALUE.length; Loop_INDEX++) niz_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        niz_VALUE[2]++;
        potvrditi(vratiti_niz(niz_VALUE) == niz_VALUE && niz_VALUE[2] == 35 && niz_VALUE[4] == 68, 6);
        potvrditi(ogranak(VALUE - 117) == 7 && ogranak(VALUE - 15) == 9 && ogranak(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Tekst = "한글 😀";
        potvrditi(Tekst.length() == 5 && Tekst.charAt(0) == '한' && Tekst.charAt(3) == 0xd83d, 8);
        potvrditi(ploča.CPU_dozvola_nivo() == 1, 9);
        단말.Piši("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 lokalni_opseg 변수가 보존되는지 검사: 각 작업은 독립된 mašina 스택을 쓴다.
        int lokalni_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (zadatak_redoslijed % 2 + 1 != INDEX) zadatak_greška++;
            zadatak_redoslijed++;
            lokalni_VALUE += Loop_INDEX + INDEX;
            zadatak_SUM[INDEX] = lokalni_VALUE;
            작업횟수[INDEX]++;
            ploča.YIELD_CPU();
            if (lokalni_VALUE != zadatak_SUM[INDEX]) zadatak_greška++;
        }
    }
    static void 작업시험() {
        zadatak_redoslijed = 0; zadatak_greška = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        potvrditi(ploča.Create_zadatak(1) == 0 && ploča.Create_zadatak(2) == 0, 20);
        int rotacija_slike_prstima_COUNT = 0;
        while (ploča.zadatak_stanje(1) != 0 || ploča.zadatak_stanje(2) != 0) {
            ploča.YIELD_CPU();
            potvrditi(++rotacija_slike_prstima_COUNT < 100, 21);
        }
        potvrditi(작업횟수[1] == 10 && 작업횟수[2] == 10 && zadatak_redoslijed == 20 && zadatak_greška == 0, 22);
        potvrditi(zadatak_SUM[1] == 155 && zadatak_SUM[2] == 265, 23);
        단말.Piši("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Vertikalno_položaj, int 너비, int 높이, int 색) {
        for (int Y_koordinata = Vertikalno_položaj; Y_koordinata < Vertikalno_položaj + 높이; Y_koordinata++)
            for (int koordinata_x = 가로; koordinata_x < 가로 + 너비; koordinata_x++) ploča.화면점(koordinata_x, Y_koordinata, 색);
    }
    static void 화면() {
        if (ploča.화면준비() == 0) { 단말.Piši("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, ploča.화면너비(), ploča.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Piši("FRAMEBUFFER PASS "); 단말.수(ploča.화면너비()); 단말.문자('x');
        단말.수(ploča.화면높이()); 단말.Piši(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int mjera = ploča.씨플러스시험();
        potvrditi(mjera == 0, 100 + mjera);
        단말.Piši("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        potvrditi(ploča.ček_korisnik_program() == 0, 200);
        단말.Piši("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = ploča.niz_korisnik_program(0);
        if (처음결과 != 0) { 단말.Piši("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        potvrditi(처음결과 == 0, 201);
        단말.Piši("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Piši("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int mjera = ploča.niz_korisnik_program(INDEX + 1);
            if (mjera != 예상[INDEX]) { 단말.Piši("USER RESULT "); 단말.수(mjera); 단말.문자(10); }
            potvrditi(mjera == 예상[INDEX], 210 + INDEX);
        }
        potvrditi(ploča.niz_korisnik_program(0) == 0, 220);
        단말.Piši("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int mjera = ploča.niz_korisnik_program(9);
        if (mjera != 0) { 단말.Piši("UDP RESULT "); 단말.수(mjera); 단말.문자(10); }
        potvrditi(mjera == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Piši("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Piši("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Piši("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Piši("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Piši("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Pokreni() {
        단말.Piši("WorldOS bs · bs · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Piši("NATIVE READY\n");
        명령해석기.Izvrši_komanda();
    }
}
