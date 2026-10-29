// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** vlastiti Java 커널의 Pi4 početno_stanje 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class jezgra_sustava {
    static int[] 작업횟수 = new int[3];
    static int[] obaveza_SUM = new int[3];
    static int obaveza_narudžba;
    static int obaveza_pogreška;
    static int slučajan_početno_unijeti = 17;

    static void provjeriti(boolean uvjet, int INDEX) {
        if (!uvjet) { 단말.Zapisuj("FAIL "); 단말.수(INDEX); pano.Zaustavi(INDEX); }
    }
    static int grana(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] vratiti_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = slučajan_početno_unijeti;
        provjeriti(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        provjeriti(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        provjeriti(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        provjeriti((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        provjeriti((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        provjeriti(vratiti_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        provjeriti(grana(VALUE - 117) == 7 && grana(VALUE - 15) == 9 && grana(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Tekst = "한글 😀";
        provjeriti(Tekst.length() == 5 && Tekst.charAt(0) == '한' && Tekst.charAt(3) == 0xd83d, 8);
        provjeriti(pano.CPU_dozvola_razina() == 1, 9);
        단말.Zapisuj("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 lokalno_doseg 변수가 보존되는지 검사: 각 작업은 독립된 stroj 스택을 쓴다.
        int lokalno_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (obaveza_narudžba % 2 + 1 != INDEX) obaveza_pogreška++;
            obaveza_narudžba++;
            lokalno_VALUE += Loop_INDEX + INDEX;
            obaveza_SUM[INDEX] = lokalno_VALUE;
            작업횟수[INDEX]++;
            pano.YIELD_CPU();
            if (lokalno_VALUE != obaveza_SUM[INDEX]) obaveza_pogreška++;
        }
    }
    static void 작업시험() {
        obaveza_narudžba = 0; obaveza_pogreška = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        provjeriti(pano.Create_obaveza(1) == 0 && pano.Create_obaveza(2) == 0, 20);
        int rotacija_COUNT = 0;
        while (pano.obaveza_Stanje(1) != 0 || pano.obaveza_Stanje(2) != 0) {
            pano.YIELD_CPU();
            provjeriti(++rotacija_COUNT < 100, 21);
        }
        provjeriti(작업횟수[1] == 10 && 작업횟수[2] == 10 && obaveza_narudžba == 20 && obaveza_pogreška == 0, 22);
        provjeriti(obaveza_SUM[1] == 155 && obaveza_SUM[2] == 265, 23);
        단말.Zapisuj("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void pravokutnik(int 가로, int Okomito_položaj, int 너비, int 높이, int 색) {
        for (int 세로좌표 = Okomito_položaj; 세로좌표 < Okomito_položaj + 높이; 세로좌표++)
            for (int koordinata_x = 가로; koordinata_x < 가로 + 너비; koordinata_x++) pano.화면점(koordinata_x, 세로좌표, 색);
    }
    static void 화면() {
        if (pano.화면준비() == 0) { 단말.Zapisuj("FRAMEBUFFER unavailable\n"); return; }
        pravokutnik(0, 0, pano.화면너비(), pano.화면높이(), 0x302018);
        pravokutnik(40, 40, 560, 400, 0xefe8e2);
        pravokutnik(40, 40, 560, 40, 0x905020);
        pravokutnik(60, 110, 240, 140, 0x90b050);
        pravokutnik(320, 110, 260, 140, 0xd0a040);
        pravokutnik(60, 290, 520, 120, 0xd8d0c8);
        단말.Zapisuj("FRAMEBUFFER PASS "); 단말.수(pano.화면너비()); 단말.문자('x');
        단말.수(pano.화면높이()); 단말.Zapisuj(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int REZULTAT = pano.씨플러스시험();
        provjeriti(REZULTAT == 0, 100 + REZULTAT);
        단말.Zapisuj("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        provjeriti(pano.사용자검사() == 0, 200);
        단말.Zapisuj("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = pano.izvršiti_korisnik_program(0);
        if (처음결과 != 0) { 단말.Zapisuj("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        provjeriti(처음결과 == 0, 201);
        단말.Zapisuj("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Zapisuj("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int REZULTAT = pano.izvršiti_korisnik_program(INDEX + 1);
            if (REZULTAT != 예상[INDEX]) { 단말.Zapisuj("USER RESULT "); 단말.수(REZULTAT); 단말.문자(10); }
            provjeriti(REZULTAT == 예상[INDEX], 210 + INDEX);
        }
        provjeriti(pano.izvršiti_korisnik_program(0) == 0, 220);
        단말.Zapisuj("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int REZULTAT = pano.izvršiti_korisnik_program(9);
        if (REZULTAT != 0) { 단말.Zapisuj("UDP RESULT "); 단말.수(REZULTAT); 단말.문자(10); }
        provjeriti(REZULTAT == 0, 230);
    }
    static void Podaci_o_sustavu() {
        단말.Zapisuj("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Zapisuj("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Zapisuj("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Zapisuj("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Zapisuj("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Pokreni() {
        단말.Zapisuj("WorldOS hr · hr · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Zapisuj("NATIVE READY\n");
        명령해석기.Izvrši_naredba();
    }
}
