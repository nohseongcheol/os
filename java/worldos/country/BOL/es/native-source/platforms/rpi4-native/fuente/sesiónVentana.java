// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Estado del intérprete para cuatro terminales. El almacenamiento de archivos es compartido; rutas, variables, historial y entrada son independientes. */
public final class sesiónVentana {
    static int[] preservarValor = new int[4 * 30000], preparar = new int[4];
    static int elementoListaActual, posición;
    static boolean leerContinuación;
    static void valorArreglo(int[] Datos, boolean valorAlmacenar) {
        for (int índiceBucle = 0; índiceBucle < Datos.length; índiceBucle++) { if (valorAlmacenar) preservarValor[posición++] = Datos[índiceBucle]; else Datos[índiceBucle] = preservarValor[posición++]; }
    }
    static int valor(int valorDatos, boolean almacenadoEra) { if (almacenadoEra) { preservarValor[posición++] = valorDatos; return valorDatos; } return preservarValor[posición++]; }
    static void posicionarPosición(int ranuraPreservado, boolean almacenadoEra) {
        posición = ranuraPreservado * 30000;
        valorArreglo(ArchivosMemoria.elementoListaActual, almacenadoEra); ArchivosMemoria.longitudActual = valor(ArchivosMemoria.longitudActual, almacenadoEra);
        valorArreglo(SintaxisIntérpreteComandos.nombreVariable, almacenadoEra); valorArreglo(SintaxisIntérpreteComandos.datosVariable, almacenadoEra); valorArreglo(SintaxisIntérpreteComandos.longitudNombre, almacenadoEra); valorArreglo(SintaxisIntérpreteComandos.longitudValor, almacenadoEra);
        SintaxisIntérpreteComandos.valorEstadoValor = valor(SintaxisIntérpreteComandos.valorEstadoValor, almacenadoEra);
        valorArreglo(EditorLínea.registroEntradaDiario, almacenadoEra); valorArreglo(EditorLínea.longitudDiario, almacenadoEra); valorArreglo(EditorLínea.valorAlmacenar, almacenadoEra); valorArreglo(IntérpreteComandos.línea, almacenadoEra);
        EditorLínea.númeroElementosDiario = valor(EditorLínea.númeroElementosDiario, almacenadoEra); EditorLínea.finRegistroEntradaDiario = valor(EditorLínea.finRegistroEntradaDiario, almacenadoEra);
        EditorLínea.buscarCoincidenciaValor = valor(EditorLínea.buscarCoincidenciaValor, almacenadoEra); EditorLínea.longitudAlmacenado = valor(EditorLínea.longitudAlmacenado, almacenadoEra);
        EditorLínea.tamaño = valor(EditorLínea.tamaño, almacenadoEra); EditorLínea.valorCursor = valor(EditorLínea.valorCursor, almacenadoEra); EditorLínea.iniciarVentana = valor(EditorLínea.iniciarVentana, almacenadoEra);
        preparar[ranuraPreservado] = 1;
    }
    static void entradaElementoValorProceso() {
        int númeroEvento = Placa.terminal(12); if (númeroEvento == 0) return;
        posicionarPosición(elementoListaActual, true);
        for (int índiceBucle = 0; índiceBucle < 4; índiceBucle++) {
            if ((númeroEvento & (1 << (8 + índiceBucle))) != 0) { Placa.programaUsuarioControl(32 + índiceBucle); preparar[índiceBucle] = 0; }
            if ((númeroEvento & (1 << (4 + índiceBucle))) != 0 && índiceBucle != elementoListaActual) preparar[índiceBucle] = 0;
        }
        int posiciónSiguiente = (númeroEvento & 15) - 1; if (posiciónSiguiente < 0) posiciónSiguiente = 0;
        if (preparar[posiciónSiguiente] == 0) for (int índiceBucle = 0; índiceBucle < 30000; índiceBucle++) preservarValor[posiciónSiguiente * 30000 + índiceBucle] = 0;
        elementoListaActual = posiciónSiguiente; posicionarPosición(elementoListaActual, false); Placa.terminal(100 + elementoListaActual); leerContinuación = true;
        EntradaSalidaTerminal.escribir("\nTERMINAL FOCUS "); EntradaSalidaTerminal.númeroValor(elementoListaActual + 1); EntradaSalidaTerminal.Caracteres(10);
    }
    static boolean ejecuciónReanudar() {
        if (Placa.programaUsuarioControl(16 + elementoListaActual) == 0) return false;
        EntradaSalidaIntérpreteComandos.permitirInteractivo = true; EntradaSalidaIntérpreteComandos.ponerEnMarcha(false, false); Placa.entradaSalidaConmutar(1);
        int valorProcesado = Placa.programaUsuarioControl(elementoListaActual); EntradaSalidaIntérpreteComandos.terminación();
        if (valorProcesado != -1005) { leerContinuación = false; SintaxisIntérpreteComandos.valorEstadoValor = valorProcesado < 0 ? 126 : valorProcesado; EntradaSalidaTerminal.escribir("exit "); EntradaSalidaTerminal.númeroValor(valorProcesado); EntradaSalidaTerminal.Caracteres(10); Placa.terminal(3); }
        return true;
    }
}
