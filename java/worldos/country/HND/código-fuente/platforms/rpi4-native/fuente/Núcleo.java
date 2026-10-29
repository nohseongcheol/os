// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Primera adaptación a Pi4 del núcleo Java autónomo; se ejecuta directamente, sin Linux ni JVM anfitriona. */
public final class Núcleo {
    static int[] númeroIteracionesTarea = new int[3];
    static int[] totalSumaTarea = new int[3];
    static int ordenTarea;
    static int errorTarea;
    static int semillaAleatorio = 17;

    static void verificar(boolean condición, int número) {
        if (!condición) { EntradaSalidaTerminal.escribir("FAIL "); EntradaSalidaTerminal.númeroValor(número); Placa.detener(número); }
    }
    static int rama(int valor) {
        switch (valor) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int conmutarDenso(int valor) {
        switch (valor) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] arregloRetornar(int[] valorArreglo) { return valorArreglo; }
    static void pruebaAritmética() {
        int valor = semillaAleatorio;
        verificar(valor * 7 - valor == 102 && valor / 3 == 5 && valor % 3 == 2, 1);
        int enteroValorMínimo = 0x80000000, unoNegativo = -1;
        verificar(enteroValorMínimo / unoNegativo == enteroValorMínimo && enteroValorMínimo % unoNegativo == 0, 2);
        verificar(enteroValorMínimo + enteroValorMínimo == 0 && -enteroValorMínimo == enteroValorMínimo, 3);
        verificar((-valor >> 2) == -5 && (-valor >>> 2) == 1073741819 && (valor << 33) == 34, 4);
        verificar((byte)(valor * 16) == 16 && (short)65535 == -1 && (char)unoNegativo == 65535, 5);
        int[] valorArreglo = new int[5];
        for (int índiceBucle = 0; índiceBucle < valorArreglo.length; índiceBucle++) valorArreglo[índiceBucle] = índiceBucle * valor;
        valorArreglo[2]++;
        verificar(arregloRetornar(valorArreglo) == valorArreglo && valorArreglo[2] == 35 && valorArreglo[4] == 68, 6);
        verificar(rama(valor - 117) == 7 && rama(valor - 15) == 9 && rama(valor) == 3 && conmutarDenso(valor - 15) == 17, 7);
        String texto = "한글 😀";
        verificar(texto.length() == 5 && texto.charAt(0) == '한' && texto.charAt(3) == 0xd83d, 8);
        verificar(Placa.nivelPrivilegioCPU() == 1, 9);
        EntradaSalidaTerminal.escribir("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void Tarea(int número) {
        // Comprobar que las variables locales se conservan al ceder la ejecución; cada tarea usa su propia pila de máquina.
        int valorLocal = número * 100;
        for (int índiceBucle = 0; índiceBucle < 10; índiceBucle++) {
            if (ordenTarea % 2 + 1 != número) errorTarea++;
            ordenTarea++;
            valorLocal += índiceBucle + número;
            totalSumaTarea[número] = valorLocal;
            númeroIteracionesTarea[número]++;
            Placa.cederProcesador();
            if (valorLocal != totalSumaTarea[número]) errorTarea++;
        }
    }
    static void pruebaTareas() {
        ordenTarea = 0; errorTarea = 0;
        númeroIteracionesTarea[1] = 0; númeroIteracionesTarea[2] = 0;
        verificar(Placa.crearTarea(1) == 0 && Placa.crearTarea(2) == 0, 20);
        int númeroElementosRotación = 0;
        while (Placa.estadoValorTarea(1) != 0 || Placa.estadoValorTarea(2) != 0) {
            Placa.cederProcesador();
            verificar(++númeroElementosRotación < 100, 21);
        }
        verificar(númeroIteracionesTarea[1] == 10 && númeroIteracionesTarea[2] == 10 && ordenTarea == 20 && errorTarea == 0, 22);
        verificar(totalSumaTarea[1] == 155 && totalSumaTarea[2] == 265, 23);
        EntradaSalidaTerminal.escribir("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void rectángulo(int posiciónHorizontal, int posiciónVertical, int valorAnchura, int valorAltura, int valorColor) {
        for (int coordenadaCoordenadaVertical = posiciónVertical; coordenadaCoordenadaVertical < posiciónVertical + valorAltura; coordenadaCoordenadaVertical++)
            for (int coordenadaCoordenadaHorizontal = posiciónHorizontal; coordenadaCoordenadaHorizontal < posiciónHorizontal + valorAnchura; coordenadaCoordenadaHorizontal++) Placa.ponerPíxelPantalla(coordenadaCoordenadaHorizontal, coordenadaCoordenadaVertical, valorColor);
    }
    static void Pantalla() {
        if (Placa.prepararPantalla() == 0) { EntradaSalidaTerminal.escribir("FRAMEBUFFER unavailable\n"); return; }
        rectángulo(0, 0, Placa.anchuraPantalla(), Placa.alturaPantalla(), 0x302018);
        rectángulo(40, 40, 560, 400, 0xefe8e2);
        rectángulo(40, 40, 560, 40, 0x905020);
        rectángulo(60, 110, 240, 140, 0x90b050);
        rectángulo(320, 110, 260, 140, 0xd0a040);
        rectángulo(60, 290, 520, 120, 0xd8d0c8);
        EntradaSalidaTerminal.escribir("FRAMEBUFFER PASS "); EntradaSalidaTerminal.númeroValor(Placa.anchuraPantalla()); EntradaSalidaTerminal.Caracteres('x');
        EntradaSalidaTerminal.númeroValor(Placa.alturaPantalla()); EntradaSalidaTerminal.escribir(" RGB32 (drawing only)\n");
    }
    static void pruebaC() {
        int resultado = Placa.pruebaCpp();
        verificar(resultado == 0, 100 + resultado);
        EntradaSalidaTerminal.escribir("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void pruebaProgramasUsuario() {
        verificar(Placa.comprobarProgramaUsuario() == 0, 200);
        EntradaSalidaTerminal.escribir("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int resultadoInicialValor = Placa.ponerEnMarchaProgramaUsuario(0);
        if (resultadoInicialValor != 0) { EntradaSalidaTerminal.escribir("USER DEMO RESULT "); EntradaSalidaTerminal.númeroValor(resultadoInicialValor); EntradaSalidaTerminal.Caracteres(10); }
        verificar(resultadoInicialValor == 0, 201);
        EntradaSalidaTerminal.escribir("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] valoresEsperado = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int número = 0; número < valoresEsperado.length; número++) {
            EntradaSalidaTerminal.escribir("USER CHECK "); EntradaSalidaTerminal.númeroValor(número); EntradaSalidaTerminal.Caracteres(10);
            int resultado = Placa.ponerEnMarchaProgramaUsuario(número + 1);
            if (resultado != valoresEsperado[número]) { EntradaSalidaTerminal.escribir("USER RESULT "); EntradaSalidaTerminal.númeroValor(resultado); EntradaSalidaTerminal.Caracteres(10); }
            verificar(resultado == valoresEsperado[número], 210 + número);
        }
        verificar(Placa.ponerEnMarchaProgramaUsuario(0) == 0, 220);
        EntradaSalidaTerminal.escribir("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void pruebaConexiónRed() {
        int resultado = Placa.ponerEnMarchaProgramaUsuario(9);
        if (resultado != 0) { EntradaSalidaTerminal.escribir("UDP RESULT "); EntradaSalidaTerminal.númeroValor(resultado); EntradaSalidaTerminal.Caracteres(10); }
        verificar(resultado == 0, 230);
    }
    static void informaciónSistema() {
        EntradaSalidaTerminal.escribir("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        EntradaSalidaTerminal.escribir("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        EntradaSalidaTerminal.escribir("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        EntradaSalidaTerminal.escribir("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        EntradaSalidaTerminal.escribir("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void ponerEnMarcha() {
        EntradaSalidaTerminal.escribir("WorldOS es · Hola · 😀\n");
        pruebaAritmética();
        pruebaC();
        pruebaTareas();
        Pantalla();
        pruebaProgramasUsuario();
        pruebaConexiónRed();
        EntradaSalidaTerminal.escribir("NATIVE READY\n");
        IntérpreteComandos.ejecutarComando();
    }
}
