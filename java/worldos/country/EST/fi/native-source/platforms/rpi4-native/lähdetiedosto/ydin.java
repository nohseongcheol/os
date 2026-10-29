// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** oma Java 커널의 Pi4 alkutila 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class ydin {
    static int[] 작업횟수 = new int[3];
    static int[] tehtävä_SUM = new int[3];
    static int tehtävä_tilata;
    static int tehtävä_virhe;
    static int 난수씨 = 17;

    static void tarkistaa(boolean ehto, int INDEKSI) {
        if (!ehto) { 단말.Kirjoitus("FAIL "); 단말.numero(INDEKSI); Taulu.Pysäytä(INDEKSI); }
    }
    static int haara(int ARVO) {
        switch (ARVO) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int ARVO) {
        switch (ARVO) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] palauttaa_MATRIISI(int[] MATRIISI_ARVO) { return MATRIISI_ARVO; }
    static void 계산시험() {
        int ARVO = 난수씨;
        tarkistaa(ARVO * 7 - ARVO == 102 && ARVO / 3 == 5 && ARVO % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        tarkistaa(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        tarkistaa(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        tarkistaa((-ARVO >> 2) == -5 && (-ARVO >>> 2) == 1073741819 && (ARVO << 33) == 34, 4);
        tarkistaa((byte)(ARVO * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] MATRIISI_ARVO = new int[5];
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < MATRIISI_ARVO.length; Loop_INDEKSI++) MATRIISI_ARVO[Loop_INDEKSI] = Loop_INDEKSI * ARVO;
        MATRIISI_ARVO[2]++;
        tarkistaa(palauttaa_MATRIISI(MATRIISI_ARVO) == MATRIISI_ARVO && MATRIISI_ARVO[2] == 35 && MATRIISI_ARVO[4] == 68, 6);
        tarkistaa(haara(ARVO - 117) == 7 && haara(ARVO - 15) == 9 && haara(ARVO) == 3 && 촘촘분기(ARVO - 15) == 17, 7);
        String teksti = "한글 😀";
        tarkistaa(teksti.length() == 5 && teksti.charAt(0) == '한' && teksti.charAt(3) == 0xd83d, 8);
        tarkistaa(Taulu.suoritin_oikeus_taso() == 1, 9);
        단말.Kirjoitus("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEKSI) {
        // TUOTTO_suoritin 전후 paikallinen_laajuus 변수가 보존되는지 검사: 각 작업은 독립된 kone 스택을 쓴다.
        int paikallinen_ARVO = INDEKSI * 100;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 10; Loop_INDEKSI++) {
            if (tehtävä_tilata % 2 + 1 != INDEKSI) tehtävä_virhe++;
            tehtävä_tilata++;
            paikallinen_ARVO += Loop_INDEKSI + INDEKSI;
            tehtävä_SUM[INDEKSI] = paikallinen_ARVO;
            작업횟수[INDEKSI]++;
            Taulu.TUOTTO_suoritin();
            if (paikallinen_ARVO != tehtävä_SUM[INDEKSI]) tehtävä_virhe++;
        }
    }
    static void testi_Tasks() {
        tehtävä_tilata = 0; tehtävä_virhe = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        tarkistaa(Taulu.Luo_tehtävä(1) == 0 && Taulu.Luo_tehtävä(2) == 0, 20);
        int kierto_LASKE = 0;
        while (Taulu.tehtävä_Tila(1) != 0 || Taulu.tehtävä_Tila(2) != 0) {
            Taulu.TUOTTO_suoritin();
            tarkistaa(++kierto_LASKE < 100, 21);
        }
        tarkistaa(작업횟수[1] == 10 && 작업횟수[2] == 10 && tehtävä_tilata == 20 && tehtävä_virhe == 0, 22);
        tarkistaa(tehtävä_SUM[1] == 155 && tehtävä_SUM[2] == 265, 23);
        단말.Kirjoitus("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void suorakulmio(int 가로, int toimiala_toimi, int 너비, int 높이, int 색) {
        for (int Y_koordinaatti = toimiala_toimi; Y_koordinaatti < toimiala_toimi + 높이; Y_koordinaatti++)
            for (int x_koordinaatti = 가로; x_koordinaatti < 가로 + 너비; x_koordinaatti++) Taulu.화면점(x_koordinaatti, Y_koordinaatti, 색);
    }
    static void 화면() {
        if (Taulu.화면준비() == 0) { 단말.Kirjoitus("FRAMEBUFFER unavailable\n"); return; }
        suorakulmio(0, 0, Taulu.화면너비(), Taulu.화면높이(), 0x302018);
        suorakulmio(40, 40, 560, 400, 0xefe8e2);
        suorakulmio(40, 40, 560, 40, 0x905020);
        suorakulmio(60, 110, 240, 140, 0x90b050);
        suorakulmio(320, 110, 260, 140, 0xd0a040);
        suorakulmio(60, 290, 520, 120, 0xd8d0c8);
        단말.Kirjoitus("FRAMEBUFFER PASS "); 단말.numero(Taulu.화면너비()); 단말.문자('x');
        단말.numero(Taulu.화면높이()); 단말.Kirjoitus(" RGB32 (drawing only)\n");
    }
    static void testi_C() {
        int TULOS = Taulu.씨플러스시험();
        tarkistaa(TULOS == 0, 100 + TULOS);
        단말.Kirjoitus("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        tarkistaa(Taulu.sekki_käyttäjä_ohjelma() == 0, 200);
        단말.Kirjoitus("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Taulu.suorittaa_käyttäjä_ohjelma(0);
        if (처음결과 != 0) { 단말.Kirjoitus("USER DEMO RESULT "); 단말.numero(처음결과); 단말.문자(10); }
        tarkistaa(처음결과 == 0, 201);
        단말.Kirjoitus("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEKSI = 0; INDEKSI < 예상.length; INDEKSI++) {
            단말.Kirjoitus("USER CHECK "); 단말.numero(INDEKSI); 단말.문자(10);
            int TULOS = Taulu.suorittaa_käyttäjä_ohjelma(INDEKSI + 1);
            if (TULOS != 예상[INDEKSI]) { 단말.Kirjoitus("USER RESULT "); 단말.numero(TULOS); 단말.문자(10); }
            tarkistaa(TULOS == 예상[INDEKSI], 210 + INDEKSI);
        }
        tarkistaa(Taulu.suorittaa_käyttäjä_ohjelma(0) == 0, 220);
        단말.Kirjoitus("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void testi_Verkot() {
        int TULOS = Taulu.suorittaa_käyttäjä_ohjelma(9);
        if (TULOS != 0) { 단말.Kirjoitus("UDP RESULT "); 단말.numero(TULOS); 단말.문자(10); }
        tarkistaa(TULOS == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Kirjoitus("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Kirjoitus("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Kirjoitus("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Kirjoitus("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Kirjoitus("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Suorita_2() {
        단말.Kirjoitus("WorldOS fi · Hei · 😀\n");
        계산시험();
        testi_C();
        testi_Tasks();
        화면();
        사용자시험();
        testi_Verkot();
        단말.Kirjoitus("NATIVE READY\n");
        명령해석기.Suorita_komento();
    }
}
