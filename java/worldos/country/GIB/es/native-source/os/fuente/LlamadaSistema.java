// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Invocada por la puerta int 0x80. Validar todos los punteros y longitudes de usuario antes del acceso. */
public final class LlamadaSistema {
    static int[] búferTemporal = new int[1024];

    static int longitudArreglo(int dirección) {
        if (!GestiónEjecución.recortar(dirección, 4)) return -14;
        int longitud = GestiónEjecución.númeroValor(dirección);
        if (longitud < 0 || longitud > (GestiónEjecución.finUsuario - dirección - 4) / 4) return -14;
        return longitud;
    }

    public static int entradaElementoValorProceso(int número, int operandoPrimero, int operandoSegundo, int operandoTercero, int operandoCuarto, int operandoQuinto) {
        if (número == 30) return GestiónDescriptoresArchivo.abrirArchivo(operandoPrimero, operandoSegundo, operandoTercero);
        if (número == 31) return GestiónDescriptoresArchivo.leerArchivo(operandoPrimero, operandoSegundo, operandoTercero);
        if (número == 32) return GestiónDescriptoresArchivo.escribirArchivo(operandoPrimero, operandoSegundo, operandoTercero);
        if (número == 33) return GestiónDescriptoresArchivo.cerrarArchivo(operandoPrimero);
        if (número == 34) return GestiónDescriptoresArchivo.posicionarArchivo(operandoPrimero, operandoSegundo, operandoTercero);
        if (número == 35) return GestiónDescriptoresArchivo.descriptorDuplicado(operandoPrimero, 0, false, 0);
        if (número == 36) return GestiónDescriptoresArchivo.descriptorDuplicado(operandoPrimero, operandoSegundo, true, 0);
        if (número == 37) return GestiónDescriptoresArchivo.leerEstadoArchivo(operandoPrimero, operandoSegundo);
        if (número == 38) return GestiónDescriptoresArchivo.eliminarNombreEntradaElementoArchivo(operandoPrimero);
        if (número == 39) return GestiónDescriptoresArchivo.establecerLongitudArchivo(operandoPrimero, operandoSegundo);
        if (número == 40) return GestiónDescriptoresArchivo.descriptorControl(operandoPrimero, operandoSegundo, operandoTercero);
        if (número == 41) return GestiónDescriptoresArchivo.crearExtremo(operandoPrimero, operandoSegundo, operandoTercero);
        if (número == 42) return GestiónDescriptoresArchivo.asociarDirección(operandoPrimero, operandoSegundo, operandoTercero);
        if (número == 43) return GestiónDescriptoresArchivo.enviarDatosDatagrama(operandoPrimero, operandoSegundo, operandoTercero, operandoCuarto, operandoQuinto);
        if (número == 44) return GestiónDescriptoresArchivo.recibirDatosDatagrama(operandoPrimero, operandoSegundo, operandoTercero, operandoCuarto, operandoQuinto);
        if (número == 45) return GestiónDescriptoresArchivo.leerDirecciónConectorRed(operandoPrimero, operandoSegundo, operandoTercero);
        if (número == 46) return GestiónDescriptoresArchivo.establecerTiempoEsperaRecibir(operandoPrimero, operandoSegundo);
        if (número == 47) {
            int valorDescriptor = GestiónDescriptoresArchivo.encontrarDescriptor(operandoPrimero);
            if (valorDescriptor < 0) return -9;
            if (GestiónDescriptoresArchivo.valorClaseTipo[valorDescriptor] != 2) return -22;
            return PersistenciaArchivos.sincronizar();
        }
        if (número == 1) {
            int longitud = longitudArreglo(operandoPrimero);
            if (longitud < 0) return longitud;
            if (longitud > 4096) return -90;
            for (int valorCarácter = 0; valorCarácter < longitud; valorCarácter++) TerminalTexto.Caracteres(GestiónEjecución.númeroValor(operandoPrimero + 4 + valorCarácter * 4) & 65535);
            return longitud;
        }
        if (número == 2) return GestiónEjecución.númeroElementosArgumento;
        if (número == 3) return operandoPrimero >= 0 && operandoPrimero < GestiónEjecución.númeroElementosArgumento ? GestiónEjecución.direcciónArgumento[operandoPrimero] : 0;
        if (número == 10) return PilaRed.abrir(operandoPrimero);
        if (número == 11) {
            int longitud = longitudArreglo(operandoCuarto);
            if (longitud < 0) return longitud;
            if (operandoQuinto < 0 || operandoQuinto > longitud || operandoQuinto > 1024) return -90;
            for (int posición = 0; posición < operandoQuinto; posición++) búferTemporal[posición] = GestiónEjecución.númeroValor(operandoCuarto + 4 + posición * 4) & 255;
            return PilaRed.enviar(operandoPrimero, operandoSegundo, operandoTercero, búferTemporal, operandoQuinto);
        }
        if (número == 12) {
            int longitud = longitudArreglo(operandoSegundo);
            if (longitud < 0) return longitud;
            if (operandoTercero < 0 || operandoTercero > 2000) return -22;
            int resultado = PilaRed.recibir(operandoPrimero, búferTemporal, longitud < 1024 ? longitud : 1024, operandoTercero);
            if (resultado >= 0) for (int posición = 0; posición < resultado; posición++) GestiónEjecución.escribirNúmero(operandoSegundo + 4 + posición * 4, búferTemporal[posición]);
            return resultado;
        }
        if (número == 13) return PilaRed.cerrar(operandoPrimero);
        if (número == 14) return PilaRed.direcciónPropio;
        if (número == 15) return PilaRed.direcciónParRed(operandoPrimero);
        if (número == 16) return PilaRed.númeroPuertoParRed(operandoPrimero);
        if (número == 22) {
            if (operandoPrimero < 0 || operandoPrimero > 65535) return -22;
            TerminalTexto.Caracteres(operandoPrimero); return 1;
        }
        if (número == 20 || número == 21) {
            int tamañoNombre = longitudArreglo(operandoPrimero), tamañoDatos = longitudArreglo(operandoSegundo);
            if (tamañoNombre < 0 || tamañoDatos < 0) return -14;
            if (tamañoNombre < 1 || tamañoNombre > 64) return -22;
            int longitud = 0;
            while (longitud < tamañoNombre && GestiónEjecución.númeroValor(operandoPrimero + 4 + longitud * 4) != 0) {
                SistemaArchivosMemoria.nombre[longitud] = GestiónEjecución.númeroValor(operandoPrimero + 4 + longitud * 4);
                longitud++;
            }
            if (!SistemaArchivosMemoria.comprobarNombre(SistemaArchivosMemoria.nombre, longitud)) return -22;
            if (número == 20) {
                int Archivo = SistemaArchivosMemoria.encontrarEntradaElemento(SistemaArchivosMemoria.nombre, longitud);
                if (Archivo < 0) return Archivo;
                int tamaño = SistemaArchivosMemoria.listaTamaño[Archivo];
                if (tamaño > tamañoDatos) return -90;
                int dirección = Dispositivo.memoriaArchivo() + Archivo * SistemaArchivosMemoria.tamañoMáximo;
                for (int númeroValor = 0; númeroValor < tamaño; númeroValor++) GestiónEjecución.escribirNúmero(operandoSegundo + 4 + númeroValor * 4, Dispositivo.leerMemoria(dirección + númeroValor));
                return tamaño;
            }
            if (operandoTercero < 0 || operandoTercero > tamañoDatos) return -22;
            if (operandoTercero > SistemaArchivosMemoria.tamañoMáximo) return -90;
            for (int númeroValor = 0; númeroValor < operandoTercero; númeroValor++) SistemaArchivosMemoria.valorEditar[númeroValor] = GestiónEjecución.númeroValor(operandoSegundo + 4 + númeroValor * 4) & 255;
            return SistemaArchivosMemoria.valorAlmacenar(SistemaArchivosMemoria.nombre, longitud, SistemaArchivosMemoria.valorEditar, operandoTercero);
        }
        return -38;
    }
}
