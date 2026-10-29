// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** propi Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class nucli {
    static int[] 작업횟수 = new int[3];
    static int[] tasca_SUMA = new int[3];
    static int tasca_comanda;
    static int tasca_error;
    static int 난수씨 = 17;

    static void verificar(boolean condició, int INDEX) {
        if (!condició) { 단말.Escriptura("FAIL "); 단말.수(INDEX); Tauler.Atura(INDEX); }
    }
    static int branca(int VALOR) {
        switch (VALOR) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALOR) {
        switch (VALOR) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] tornar_les_tasques_MATRIU(int[] MATRIU_VALOR) { return MATRIU_VALOR; }
    static void 계산시험() {
        int VALOR = 난수씨;
        verificar(VALOR * 7 - VALOR == 102 && VALOR / 3 == 5 && VALOR % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        verificar(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        verificar(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        verificar((-VALOR >> 2) == -5 && (-VALOR >>> 2) == 1073741819 && (VALOR << 33) == 34, 4);
        verificar((byte)(VALOR * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] MATRIU_VALOR = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < MATRIU_VALOR.length; Loop_INDEX++) MATRIU_VALOR[Loop_INDEX] = Loop_INDEX * VALOR;
        MATRIU_VALOR[2]++;
        verificar(tornar_les_tasques_MATRIU(MATRIU_VALOR) == MATRIU_VALOR && MATRIU_VALOR[2] == 35 && MATRIU_VALOR[4] == 68, 6);
        verificar(branca(VALOR - 117) == 7 && branca(VALOR - 15) == 9 && branca(VALOR) == 3 && 촘촘분기(VALOR - 15) == 17, 7);
        String SMS = "한글 😀";
        verificar(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        verificar(Tauler.CPU_permís_nivell() == 1, 9);
        단말.Escriptura("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // RENDTO_CPU 전후 local_Àmbit 변수가 보존되는지 검사: 각 작업은 독립된 màquina 스택을 쓴다.
        int local_VALOR = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (tasca_comanda % 2 + 1 != INDEX) tasca_error++;
            tasca_comanda++;
            local_VALOR += Loop_INDEX + INDEX;
            tasca_SUMA[INDEX] = local_VALOR;
            작업횟수[INDEX]++;
            Tauler.RENDTO_CPU();
            if (local_VALOR != tasca_SUMA[INDEX]) tasca_error++;
        }
    }
    static void 작업시험() {
        tasca_comanda = 0; tasca_error = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verificar(Tauler.Crear_tasca(1) == 0 && Tauler.Crear_tasca(2) == 0, 20);
        int rotació_COMPT = 0;
        while (Tauler.tasca_Estat(1) != 0 || Tauler.tasca_Estat(2) != 0) {
            Tauler.RENDTO_CPU();
            verificar(++rotació_COMPT < 100, 21);
        }
        verificar(작업횟수[1] == 10 && 작업횟수[2] == 10 && tasca_comanda == 20 && tasca_error == 0, 22);
        verificar(tasca_SUMA[1] == 155 && tasca_SUMA[2] == 265, 23);
        단말.Escriptura("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Vertical_càrrec, int 너비, int 높이, int 색) {
        for (int Y_coordenada = Vertical_càrrec; Y_coordenada < Vertical_càrrec + 높이; Y_coordenada++)
            for (int X_coordenada = 가로; X_coordenada < 가로 + 너비; X_coordenada++) Tauler.화면점(X_coordenada, Y_coordenada, 색);
    }
    static void 화면() {
        if (Tauler.화면준비() == 0) { 단말.Escriptura("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, Tauler.화면너비(), Tauler.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Escriptura("FRAMEBUFFER PASS "); 단말.수(Tauler.화면너비()); 단말.문자('x');
        단말.수(Tauler.화면높이()); 단말.Escriptura(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int RESULTAT = Tauler.씨플러스시험();
        verificar(RESULTAT == 0, 100 + RESULTAT);
        단말.Escriptura("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verificar(Tauler.xec_usuari_programa() == 0, 200);
        단말.Escriptura("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Tauler.execució_usuari_programa(0);
        if (처음결과 != 0) { 단말.Escriptura("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        verificar(처음결과 == 0, 201);
        단말.Escriptura("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Escriptura("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int RESULTAT = Tauler.execució_usuari_programa(INDEX + 1);
            if (RESULTAT != 예상[INDEX]) { 단말.Escriptura("USER RESULT "); 단말.수(RESULTAT); 단말.문자(10); }
            verificar(RESULTAT == 예상[INDEX], 210 + INDEX);
        }
        verificar(Tauler.execució_usuari_programa(0) == 0, 220);
        단말.Escriptura("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int RESULTAT = Tauler.execució_usuari_programa(9);
        if (RESULTAT != 0) { 단말.Escriptura("UDP RESULT "); 단말.수(RESULTAT); 단말.문자(10); }
        verificar(RESULTAT == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Escriptura("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Escriptura("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Escriptura("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Escriptura("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Escriptura("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Executa_2() {
        단말.Escriptura("WorldOS ca · Català · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Escriptura("NATIVE READY\n");
        명령해석기.Executa_ordre();
    }
}
