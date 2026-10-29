// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** nativo Java 커널의 Pi4 estado_inicial 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class Núcleo {
    static int[] 작업횟수 = new int[3];
    static int[] Tarefa_SUM = new int[3];
    static int Tarefa_ordem;
    static int Tarefa_erro;
    static int aleatório_semente = 17;

    static void verificar(boolean doença, int ÍNDICE) {
        if (!doença) { 단말.Escrita("FAIL "); 단말.número(ÍNDICE); Quadro.Parar(ÍNDICE); }
    }
    static int branch(int VALOR) {
        switch (VALOR) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALOR) {
        switch (VALOR) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] devolver_MATRIZ(int[] MATRIZ_VALOR) { return MATRIZ_VALOR; }
    static void 계산시험() {
        int VALOR = aleatório_semente;
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
        verificar(branch(VALOR - 117) == 7 && branch(VALOR - 15) == 9 && branch(VALOR) == 3 && 촘촘분기(VALOR - 15) == 17, 7);
        String texto = "한글 😀";
        verificar(texto.length() == 5 && texto.charAt(0) == '한' && texto.charAt(3) == 0xd83d, 8);
        verificar(Quadro.CPU_permissão_nível() == 1, 9);
        단말.Escrita("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int ÍNDICE) {
        // LUCRO_CPU 전후 local_Scope 변수가 보존되는지 검사: 각 작업은 독립된 computador 스택을 쓴다.
        int local_VALOR = ÍNDICE * 100;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 10; Loop_ÍNDICE++) {
            if (Tarefa_ordem % 2 + 1 != ÍNDICE) Tarefa_erro++;
            Tarefa_ordem++;
            local_VALOR += Loop_ÍNDICE + ÍNDICE;
            Tarefa_SUM[ÍNDICE] = local_VALOR;
            작업횟수[ÍNDICE]++;
            Quadro.LUCRO_CPU();
            if (local_VALOR != Tarefa_SUM[ÍNDICE]) Tarefa_erro++;
        }
    }
    static void teste_Tasks() {
        Tarefa_ordem = 0; Tarefa_erro = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verificar(Quadro.Criar_Tarefa(1) == 0 && Quadro.Criar_Tarefa(2) == 0, 20);
        int rotação_CONT_NÚM = 0;
        while (Quadro.Tarefa_Estado(1) != 0 || Quadro.Tarefa_Estado(2) != 0) {
            Quadro.LUCRO_CPU();
            verificar(++rotação_CONT_NÚM < 100, 21);
        }
        verificar(작업횟수[1] == 10 && 작업횟수[2] == 10 && Tarefa_ordem == 20 && Tarefa_erro == 0, 22);
        verificar(Tarefa_SUM[1] == 155 && Tarefa_SUM[2] == 265, 23);
        단말.Escrita("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void retângulo(int 가로, int Vertical_cargo, int 너비, int altura_VALOR, int 색) {
        for (int Y_coordenada = Vertical_cargo; Y_coordenada < Vertical_cargo + altura_VALOR; Y_coordenada++)
            for (int coordenada_X = 가로; coordenada_X < 가로 + 너비; coordenada_X++) Quadro.화면점(coordenada_X, Y_coordenada, 색);
    }
    static void tela() {
        if (Quadro.Preparar_tela() == 0) { 단말.Escrita("FRAMEBUFFER unavailable\n"); return; }
        retângulo(0, 0, Quadro.화면너비(), Quadro.tela_altura(), 0x302018);
        retângulo(40, 40, 560, 400, 0xefe8e2);
        retângulo(40, 40, 560, 40, 0x905020);
        retângulo(60, 110, 240, 140, 0x90b050);
        retângulo(320, 110, 260, 140, 0xd0a040);
        retângulo(60, 290, 520, 120, 0xd8d0c8);
        단말.Escrita("FRAMEBUFFER PASS "); 단말.número(Quadro.화면너비()); 단말.문자('x');
        단말.número(Quadro.tela_altura()); 단말.Escrita(" RGB32 (drawing only)\n");
    }
    static void teste_C() {
        int resultado = Quadro.씨플러스시험();
        verificar(resultado == 0, 100 + resultado);
        단말.Escrita("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verificar(Quadro.cheque_usuário_app() == 0, 200);
        단말.Escrita("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Quadro.executar_usuário_app(0);
        if (처음결과 != 0) { 단말.Escrita("USER DEMO RESULT "); 단말.número(처음결과); 단말.문자(10); }
        verificar(처음결과 == 0, 201);
        단말.Escrita("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int ÍNDICE = 0; ÍNDICE < 예상.length; ÍNDICE++) {
            단말.Escrita("USER CHECK "); 단말.número(ÍNDICE); 단말.문자(10);
            int resultado = Quadro.executar_usuário_app(ÍNDICE + 1);
            if (resultado != 예상[ÍNDICE]) { 단말.Escrita("USER RESULT "); 단말.número(resultado); 단말.문자(10); }
            verificar(resultado == 예상[ÍNDICE], 210 + ÍNDICE);
        }
        verificar(Quadro.executar_usuário_app(0) == 0, 220);
        단말.Escrita("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void teste_Rede() {
        int resultado = Quadro.executar_usuário_app(9);
        if (resultado != 0) { 단말.Escrita("UDP RESULT "); 단말.número(resultado); 단말.문자(10); }
        verificar(resultado == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Escrita("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Escrita("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Escrita("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Escrita("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Escrita("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void iniciar() {
        단말.Escrita("WorldOS pt · Olá · 😀\n");
        계산시험();
        teste_C();
        teste_Tasks();
        tela();
        사용자시험();
        teste_Rede();
        단말.Escrita("NATIVE READY\n");
        InterpretadorComandos.Executar_comando();
    }
}
