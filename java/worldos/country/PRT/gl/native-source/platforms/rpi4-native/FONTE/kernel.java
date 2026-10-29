// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kernel {
    static int[] 작업횟수 = new int[3];
    static int[] tarefa_SUMA = new int[3];
    static int tarefa_orde;
    static int tarefa_erro;
    static int 난수씨 = 17;

    static void verificar(boolean condición, int ÍNDICE) {
        if (!condición) { 단말.Escritura("FAIL "); 단말.수(ÍNDICE); Panel.Deter(ÍNDICE); }
    }
    static int ramificación(int VALOR) {
        switch (VALOR) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALOR) {
        switch (VALOR) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] devolver_MATRIZ(int[] MATRIZ_VALOR) { return MATRIZ_VALOR; }
    static void 계산시험() {
        int VALOR = 난수씨;
        verificar(VALOR * 7 - VALOR == 102 && VALOR / 3 == 5 && VALOR % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        verificar(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        verificar(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        verificar((-VALOR >> 2) == -5 && (-VALOR >>> 2) == 1073741819 && (VALOR << 33) == 34, 4);
        verificar((byte)(VALOR * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] MATRIZ_VALOR = new int[5];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < MATRIZ_VALOR.length; Loop_ÍNDICE++) MATRIZ_VALOR[Loop_ÍNDICE] = Loop_ÍNDICE * VALOR;
        MATRIZ_VALOR[2]++;
        verificar(devolver_MATRIZ(MATRIZ_VALOR) == MATRIZ_VALOR && MATRIZ_VALOR[2] == 35 && MATRIZ_VALOR[4] == 68, 6);
        verificar(ramificación(VALOR - 117) == 7 && ramificación(VALOR - 15) == 9 && ramificación(VALOR) == 3 && 촘촘분기(VALOR - 15) == 17, 7);
        String Texto = "한글 😀";
        verificar(Texto.length() == 5 && Texto.charAt(0) == '한' && Texto.charAt(3) == 0xd83d, 8);
        verificar(Panel.CPU_permiso_nivel() == 1, 9);
        단말.Escritura("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int ÍNDICE) {
        // suspender_CPU 전후 local_Ámbito 변수가 보존되는지 검사: 각 작업은 독립된 máquina 스택을 쓴다.
        int local_VALOR = ÍNDICE * 100;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 10; Loop_ÍNDICE++) {
            if (tarefa_orde % 2 + 1 != ÍNDICE) tarefa_erro++;
            tarefa_orde++;
            local_VALOR += Loop_ÍNDICE + ÍNDICE;
            tarefa_SUMA[ÍNDICE] = local_VALOR;
            작업횟수[ÍNDICE]++;
            Panel.suspender_CPU();
            if (local_VALOR != tarefa_SUMA[ÍNDICE]) tarefa_erro++;
        }
    }
    static void 작업시험() {
        tarefa_orde = 0; tarefa_erro = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verificar(Panel.crear_tarefa(1) == 0 && Panel.crear_tarefa(2) == 0, 20);
        int rotación_CONTAR = 0;
        while (Panel.tarefa_Estado(1) != 0 || Panel.tarefa_Estado(2) != 0) {
            Panel.suspender_CPU();
            verificar(++rotación_CONTAR < 100, 21);
        }
        verificar(작업횟수[1] == 10 && 작업횟수[2] == 10 && tarefa_orde == 20 && tarefa_erro == 0, 22);
        verificar(tarefa_SUMA[1] == 155 && tarefa_SUMA[2] == 265, 23);
        단말.Escritura("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Vertical_cargo, int 너비, int 높이, int 색) {
        for (int Y_coordenada = Vertical_cargo; Y_coordenada < Vertical_cargo + 높이; Y_coordenada++)
            for (int X_coordenada = 가로; X_coordenada < 가로 + 너비; X_coordenada++) Panel.화면점(X_coordenada, Y_coordenada, 색);
    }
    static void 화면() {
        if (Panel.화면준비() == 0) { 단말.Escritura("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, Panel.화면너비(), Panel.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Escritura("FRAMEBUFFER PASS "); 단말.수(Panel.화면너비()); 단말.문자('x');
        단말.수(Panel.화면높이()); 단말.Escritura(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int RESULTANTE = Panel.씨플러스시험();
        verificar(RESULTANTE == 0, 100 + RESULTANTE);
        단말.Escritura("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verificar(Panel.cheque_usuario_apl() == 0, 200);
        단말.Escritura("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Panel.executar_usuario_apl(0);
        if (처음결과 != 0) { 단말.Escritura("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        verificar(처음결과 == 0, 201);
        단말.Escritura("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int ÍNDICE = 0; ÍNDICE < 예상.length; ÍNDICE++) {
            단말.Escritura("USER CHECK "); 단말.수(ÍNDICE); 단말.문자(10);
            int RESULTANTE = Panel.executar_usuario_apl(ÍNDICE + 1);
            if (RESULTANTE != 예상[ÍNDICE]) { 단말.Escritura("USER RESULT "); 단말.수(RESULTANTE); 단말.문자(10); }
            verificar(RESULTANTE == 예상[ÍNDICE], 210 + ÍNDICE);
        }
        verificar(Panel.executar_usuario_apl(0) == 0, 220);
        단말.Escritura("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int RESULTANTE = Panel.executar_usuario_apl(9);
        if (RESULTANTE != 0) { 단말.Escritura("UDP RESULT "); 단말.수(RESULTANTE); 단말.문자(10); }
        verificar(RESULTANTE == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Escritura("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Escritura("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Escritura("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Escritura("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Escritura("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Executar_2() {
        단말.Escritura("WorldOS gl · gl · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Escritura("NATIVE READY\n");
        명령해석기.executar_comando();
    }
}
