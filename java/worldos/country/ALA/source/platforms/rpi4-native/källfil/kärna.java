// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** eget Java 커널의 Pi4 starttillstånd 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kärna {
    static int[] 작업횟수 = new int[3];
    static int[] uppgift_SUM = new int[3];
    static int uppgift_order;
    static int uppgift_fel;
    static int slumpmässig_så = 17;

    static void verifiera(boolean villkor, int INDEX) {
        if (!villkor) { 단말.Skriv("FAIL "); 단말.nummer(INDEX); Tavla.Stopp(INDEX); }
    }
    static int gren(int värde) {
        switch (värde) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int värde) {
        switch (värde) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] Retur_MATRIS(int[] MATRIS_värde) { return MATRIS_värde; }
    static void 계산시험() {
        int värde = slumpmässig_så;
        verifiera(värde * 7 - värde == 102 && värde / 3 == 5 && värde % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        verifiera(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        verifiera(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        verifiera((-värde >> 2) == -5 && (-värde >>> 2) == 1073741819 && (värde << 33) == 34, 4);
        verifiera((byte)(värde * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] MATRIS_värde = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < MATRIS_värde.length; Loop_INDEX++) MATRIS_värde[Loop_INDEX] = Loop_INDEX * värde;
        MATRIS_värde[2]++;
        verifiera(Retur_MATRIS(MATRIS_värde) == MATRIS_värde && MATRIS_värde[2] == 35 && MATRIS_värde[4] == 68, 6);
        verifiera(gren(värde - 117) == 7 && gren(värde - 15) == 9 && gren(värde) == 3 && 촘촘분기(värde - 15) == 17, 7);
        String text = "한글 😀";
        verifiera(text.length() == 5 && text.charAt(0) == '한' && text.charAt(3) == 0xd83d, 8);
        verifiera(Tavla.CPU_behörighet_nivå() == 1, 9);
        단말.Skriv("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // NOMAVK_CPU 전후 lokal_scope 변수가 보존되는지 검사: 각 작업은 독립된 dator 스택을 쓴다.
        int lokal_värde = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (uppgift_order % 2 + 1 != INDEX) uppgift_fel++;
            uppgift_order++;
            lokal_värde += Loop_INDEX + INDEX;
            uppgift_SUM[INDEX] = lokal_värde;
            작업횟수[INDEX]++;
            Tavla.NOMAVK_CPU();
            if (lokal_värde != uppgift_SUM[INDEX]) uppgift_fel++;
        }
    }
    static void test_Tasks() {
        uppgift_order = 0; uppgift_fel = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verifiera(Tavla.Skapa_uppgift(1) == 0 && Tavla.Skapa_uppgift(2) == 0, 20);
        int rotering_ANTAL = 0;
        while (Tavla.uppgift_status(1) != 0 || Tavla.uppgift_status(2) != 0) {
            Tavla.NOMAVK_CPU();
            verifiera(++rotering_ANTAL < 100, 21);
        }
        verifiera(작업횟수[1] == 10 && 작업횟수[2] == 10 && uppgift_order == 20 && uppgift_fel == 0, 22);
        verifiera(uppgift_SUM[1] == 155 && uppgift_SUM[2] == 265, 23);
        단말.Skriv("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void rektangel(int 가로, int bransch_placera, int 너비, int 높이, int 색) {
        for (int Y_koordinat = bransch_placera; Y_koordinat < bransch_placera + 높이; Y_koordinat++)
            for (int x_koordinat = 가로; x_koordinat < 가로 + 너비; x_koordinat++) Tavla.화면점(x_koordinat, Y_koordinat, 색);
    }
    static void skärmbild() {
        if (Tavla.Förbereda_skärmbild() == 0) { 단말.Skriv("FRAMEBUFFER unavailable\n"); return; }
        rektangel(0, 0, Tavla.화면너비(), Tavla.화면높이(), 0x302018);
        rektangel(40, 40, 560, 400, 0xefe8e2);
        rektangel(40, 40, 560, 40, 0x905020);
        rektangel(60, 110, 240, 140, 0x90b050);
        rektangel(320, 110, 260, 140, 0xd0a040);
        rektangel(60, 290, 520, 120, 0xd8d0c8);
        단말.Skriv("FRAMEBUFFER PASS "); 단말.nummer(Tavla.화면너비()); 단말.문자('x');
        단말.nummer(Tavla.화면높이()); 단말.Skriv(" RGB32 (drawing only)\n");
    }
    static void test_C() {
        int RESULTAT = Tavla.씨플러스시험();
        verifiera(RESULTAT == 0, 100 + RESULTAT);
        단말.Skriv("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verifiera(Tavla.check_användare_app() == 0, 200);
        단말.Skriv("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Tavla.köra_användare_app(0);
        if (처음결과 != 0) { 단말.Skriv("USER DEMO RESULT "); 단말.nummer(처음결과); 단말.문자(10); }
        verifiera(처음결과 == 0, 201);
        단말.Skriv("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Skriv("USER CHECK "); 단말.nummer(INDEX); 단말.문자(10);
            int RESULTAT = Tavla.köra_användare_app(INDEX + 1);
            if (RESULTAT != 예상[INDEX]) { 단말.Skriv("USER RESULT "); 단말.nummer(RESULTAT); 단말.문자(10); }
            verifiera(RESULTAT == 예상[INDEX], 210 + INDEX);
        }
        verifiera(Tavla.köra_användare_app(0) == 0, 220);
        단말.Skriv("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void test_Nätverk() {
        int RESULTAT = Tavla.köra_användare_app(9);
        if (RESULTAT != 0) { 단말.Skriv("UDP RESULT "); 단말.nummer(RESULTAT); 단말.문자(10); }
        verifiera(RESULTAT == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Skriv("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Skriv("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Skriv("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Skriv("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Skriv("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Kör() {
        단말.Skriv("WorldOS sv · Hej · 😀\n");
        계산시험();
        test_C();
        test_Tasks();
        skärmbild();
        사용자시험();
        test_Nätverk();
        단말.Skriv("NATIVE READY\n");
        명령해석기.köra_kommando();
    }
}
