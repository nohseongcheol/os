// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** eget Java 커널의 Pi4 starttilstand 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kerne {
    static int[] 작업횟수 = new int[3];
    static int[] job_SUM = new int[3];
    static int job_ordre;
    static int job_fejl;
    static int vilkårlig_så = 17;

    static void bekræfte(boolean lidelse, int INDEKS) {
        if (!lidelse) { 단말.Skrive("FAIL "); 단말.tal(INDEKS); Tavle.Stop(INDEKS); }
    }
    static int gren(int VÆRDI) {
        switch (VÆRDI) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VÆRDI) {
        switch (VÆRDI) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] returnere_MATRIX(int[] MATRIX_VÆRDI) { return MATRIX_VÆRDI; }
    static void 계산시험() {
        int VÆRDI = vilkårlig_så;
        bekræfte(VÆRDI * 7 - VÆRDI == 102 && VÆRDI / 3 == 5 && VÆRDI % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        bekræfte(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        bekræfte(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        bekræfte((-VÆRDI >> 2) == -5 && (-VÆRDI >>> 2) == 1073741819 && (VÆRDI << 33) == 34, 4);
        bekræfte((byte)(VÆRDI * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] MATRIX_VÆRDI = new int[5];
        for (int Loop_INDEKS = 0; Loop_INDEKS < MATRIX_VÆRDI.length; Loop_INDEKS++) MATRIX_VÆRDI[Loop_INDEKS] = Loop_INDEKS * VÆRDI;
        MATRIX_VÆRDI[2]++;
        bekræfte(returnere_MATRIX(MATRIX_VÆRDI) == MATRIX_VÆRDI && MATRIX_VÆRDI[2] == 35 && MATRIX_VÆRDI[4] == 68, 6);
        bekræfte(gren(VÆRDI - 117) == 7 && gren(VÆRDI - 15) == 9 && gren(VÆRDI) == 3 && 촘촘분기(VÆRDI - 15) == 17, 7);
        String Tekst = "한글 😀";
        bekræfte(Tekst.length() == 5 && Tekst.charAt(0) == '한' && Tekst.charAt(3) == 0xd83d, 8);
        bekræfte(Tavle.CPU_rettighed_vater() == 1, 9);
        단말.Skrive("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEKS) {
        // AFKAST_CPU 전후 lokal_Omfang 변수가 보존되는지 검사: 각 작업은 독립된 maskine 스택을 쓴다.
        int lokal_VÆRDI = INDEKS * 100;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 10; Loop_INDEKS++) {
            if (job_ordre % 2 + 1 != INDEKS) job_fejl++;
            job_ordre++;
            lokal_VÆRDI += Loop_INDEKS + INDEKS;
            job_SUM[INDEKS] = lokal_VÆRDI;
            작업횟수[INDEKS]++;
            Tavle.AFKAST_CPU();
            if (lokal_VÆRDI != job_SUM[INDEKS]) job_fejl++;
        }
    }
    static void test_Tasks() {
        job_ordre = 0; job_fejl = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        bekræfte(Tavle.åbne_job(1) == 0 && Tavle.åbne_job(2) == 0, 20);
        int rotation_TÆL = 0;
        while (Tavle.job_status(1) != 0 || Tavle.job_status(2) != 0) {
            Tavle.AFKAST_CPU();
            bekræfte(++rotation_TÆL < 100, 21);
        }
        bekræfte(작업횟수[1] == 10 && 작업횟수[2] == 10 && job_ordre == 20 && job_fejl == 0, 22);
        bekræfte(job_SUM[1] == 155 && job_SUM[2] == 265, 23);
        단말.Skrive("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void rektangel(int 가로, int Lodret_placere, int 너비, int 높이, int 색) {
        for (int Y_koordinat = Lodret_placere; Y_koordinat < Lodret_placere + 높이; Y_koordinat++)
            for (int X_koordinat = 가로; X_koordinat < 가로 + 너비; X_koordinat++) Tavle.화면점(X_koordinat, Y_koordinat, 색);
    }
    static void skærmbillede() {
        if (Tavle.Tilrettelæg_skærmbillede() == 0) { 단말.Skrive("FRAMEBUFFER unavailable\n"); return; }
        rektangel(0, 0, Tavle.화면너비(), Tavle.화면높이(), 0x302018);
        rektangel(40, 40, 560, 400, 0xefe8e2);
        rektangel(40, 40, 560, 40, 0x905020);
        rektangel(60, 110, 240, 140, 0x90b050);
        rektangel(320, 110, 260, 140, 0xd0a040);
        rektangel(60, 290, 520, 120, 0xd8d0c8);
        단말.Skrive("FRAMEBUFFER PASS "); 단말.tal(Tavle.화면너비()); 단말.문자('x');
        단말.tal(Tavle.화면높이()); 단말.Skrive(" RGB32 (drawing only)\n");
    }
    static void test_C() {
        int KR = Tavle.씨플러스시험();
        bekræfte(KR == 0, 100 + KR);
        단말.Skrive("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        bekræfte(Tavle.check_bruger_app() == 0, 200);
        단말.Skrive("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Tavle.køre_bruger_app(0);
        if (처음결과 != 0) { 단말.Skrive("USER DEMO RESULT "); 단말.tal(처음결과); 단말.문자(10); }
        bekræfte(처음결과 == 0, 201);
        단말.Skrive("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEKS = 0; INDEKS < 예상.length; INDEKS++) {
            단말.Skrive("USER CHECK "); 단말.tal(INDEKS); 단말.문자(10);
            int KR = Tavle.køre_bruger_app(INDEKS + 1);
            if (KR != 예상[INDEKS]) { 단말.Skrive("USER RESULT "); 단말.tal(KR); 단말.문자(10); }
            bekræfte(KR == 예상[INDEKS], 210 + INDEKS);
        }
        bekræfte(Tavle.køre_bruger_app(0) == 0, 220);
        단말.Skrive("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void test_Netværk() {
        int KR = Tavle.køre_bruger_app(9);
        if (KR != 0) { 단말.Skrive("UDP RESULT "); 단말.tal(KR); 단말.문자(10); }
        bekræfte(KR == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Skrive("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Skrive("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Skrive("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Skrive("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Skrive("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Kør_2() {
        단말.Skrive("WorldOS da · Hej · 😀\n");
        계산시험();
        test_C();
        test_Tasks();
        skærmbillede();
        사용자시험();
        test_Netværk();
        단말.Skrive("NATIVE READY\n");
        명령해석기.Udfør_kommando();
    }
}
