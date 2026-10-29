// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class nukleo {
    static int[] 작업횟수 = new int[3];
    static int[] ataza_BATU = new int[3];
    static int ataza_ordena;
    static int ataza_errore;
    static int 난수씨 = 17;

    static void egiaztatu(boolean baldintza, int INDIZE) {
        if (!baldintza) { 단말.Idatzi("FAIL "); 단말.수(INDIZE); arbel.Gelditu(INDIZE); }
    }
    static int adar(int balio) {
        switch (balio) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int balio) {
        switch (balio) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] itzuli_matrize(int[] matrize_balio) { return matrize_balio; }
    static void 계산시험() {
        int balio = 난수씨;
        egiaztatu(balio * 7 - balio == 102 && balio / 3 == 5 && balio % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        egiaztatu(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        egiaztatu(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        egiaztatu((-balio >> 2) == -5 && (-balio >>> 2) == 1073741819 && (balio << 33) == 34, 4);
        egiaztatu((byte)(balio * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] matrize_balio = new int[5];
        for (int Loop_INDIZE = 0; Loop_INDIZE < matrize_balio.length; Loop_INDIZE++) matrize_balio[Loop_INDIZE] = Loop_INDIZE * balio;
        matrize_balio[2]++;
        egiaztatu(itzuli_matrize(matrize_balio) == matrize_balio && matrize_balio[2] == 35 && matrize_balio[4] == 68, 6);
        egiaztatu(adar(balio - 117) == 7 && adar(balio - 15) == 9 && adar(balio) == 3 && 촘촘분기(balio - 15) == 17, 7);
        String Testua = "한글 😀";
        egiaztatu(Testua.length() == 5 && Testua.charAt(0) == '한' && Testua.charAt(3) == 0xd83d, 8);
        egiaztatu(arbel.PUZ_baimen_maila() == 1, 9);
        단말.Idatzi("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDIZE) {
        // YIELD_PUZ 전후 lokal_esparru 변수가 보존되는지 검사: 각 작업은 독립된 gailu 스택을 쓴다.
        int lokal_balio = INDIZE * 100;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 10; Loop_INDIZE++) {
            if (ataza_ordena % 2 + 1 != INDIZE) ataza_errore++;
            ataza_ordena++;
            lokal_balio += Loop_INDIZE + INDIZE;
            ataza_BATU[INDIZE] = lokal_balio;
            작업횟수[INDIZE]++;
            arbel.YIELD_PUZ();
            if (lokal_balio != ataza_BATU[INDIZE]) ataza_errore++;
        }
    }
    static void 작업시험() {
        ataza_ordena = 0; ataza_errore = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        egiaztatu(arbel.sortu_ataza(1) == 0 && arbel.sortu_ataza(2) == 0, 20);
        int biraketa_ZENBATU = 0;
        while (arbel.ataza_Egoera(1) != 0 || arbel.ataza_Egoera(2) != 0) {
            arbel.YIELD_PUZ();
            egiaztatu(++biraketa_ZENBATU < 100, 21);
        }
        egiaztatu(작업횟수[1] == 10 && 작업횟수[2] == 10 && ataza_ordena == 20 && ataza_errore == 0, 22);
        egiaztatu(ataza_BATU[1] == 155 && ataza_BATU[2] == 265, 23);
        단말.Idatzi("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Bertikala_kargu, int 너비, int 높이, int 색) {
        for (int Y_koordenatu = Bertikala_kargu; Y_koordenatu < Bertikala_kargu + 높이; Y_koordenatu++)
            for (int X_koordenatu = 가로; X_koordenatu < 가로 + 너비; X_koordenatu++) arbel.화면점(X_koordenatu, Y_koordenatu, 색);
    }
    static void 화면() {
        if (arbel.화면준비() == 0) { 단말.Idatzi("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, arbel.화면너비(), arbel.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Idatzi("FRAMEBUFFER PASS "); 단말.수(arbel.화면너비()); 단말.문자('x');
        단말.수(arbel.화면높이()); 단말.Idatzi(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int EMAITZA = arbel.씨플러스시험();
        egiaztatu(EMAITZA == 0, 100 + EMAITZA);
        단말.Idatzi("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        egiaztatu(arbel.txeke_erabiltzaile_aplik() == 0, 200);
        단말.Idatzi("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = arbel.exekutatu_erabiltzaile_aplik(0);
        if (처음결과 != 0) { 단말.Idatzi("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        egiaztatu(처음결과 == 0, 201);
        단말.Idatzi("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDIZE = 0; INDIZE < 예상.length; INDIZE++) {
            단말.Idatzi("USER CHECK "); 단말.수(INDIZE); 단말.문자(10);
            int EMAITZA = arbel.exekutatu_erabiltzaile_aplik(INDIZE + 1);
            if (EMAITZA != 예상[INDIZE]) { 단말.Idatzi("USER RESULT "); 단말.수(EMAITZA); 단말.문자(10); }
            egiaztatu(EMAITZA == 예상[INDIZE], 210 + INDIZE);
        }
        egiaztatu(arbel.exekutatu_erabiltzaile_aplik(0) == 0, 220);
        단말.Idatzi("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int EMAITZA = arbel.exekutatu_erabiltzaile_aplik(9);
        if (EMAITZA != 0) { 단말.Idatzi("UDP RESULT "); 단말.수(EMAITZA); 단말.문자(10); }
        egiaztatu(EMAITZA == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Idatzi("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Idatzi("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Idatzi("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Idatzi("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Idatzi("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Exekutatu_2() {
        단말.Idatzi("WorldOS eu · eu · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Idatzi("NATIVE READY\n");
        명령해석기.exekutatu_komando();
    }
}
