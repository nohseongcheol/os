// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Separa los descriptores de un único proceso de usuario de las descripciones de archivos abiertos. Los números de llamada se documentan en la ABI POSIX. */
public final class GestiónDescriptoresArchivo {
    static final int límiteDescriptor = 32;
    static final int leerBanderaEscribir = 2, crearEntradaElemento = 64, crearExclusivamente = 128, borrarContenidoContenido = 512;
    static final int añadirFinalContinuación = 1024, esperarNoOperadorHacer = 2048, cerrarOperaciónEjecuciónActivado = 524288;
    static int[] abrirManejador = new int[límiteDescriptor], establecerDescriptor = new int[límiteDescriptor];
    static int[] valorClaseTipo = new int[límiteDescriptor], valorObjetivo = new int[límiteDescriptor];
    static int[] posiciónArchivo = new int[límiteDescriptor], abrirAjustes = new int[límiteDescriptor], númeroElementosReferencia = new int[límiteDescriptor];
    static int[] manejadorRed = new int[límiteDescriptor], recibirMilisegundosTiempoEspera = new int[límiteDescriptor];
    static int[] nombreRuta = new int[64], datosTransferencia = new int[1024];

    static int encontrarDescriptor(int descriptorArchivo) {
        if (descriptorArchivo < 0 || descriptorArchivo >= límiteDescriptor) return -9;
        return abrirManejador[descriptorArchivo] - 1;
    }
    static int descriptorVacíoEstado(int ponerEnMarcha) {
        for (int número = ponerEnMarcha; número < límiteDescriptor; número++) if (abrirManejador[número] == 0) return número;
        return -24;
    }
    static int manejadorVacíoEstado() {
        for (int número = 0; número < límiteDescriptor; número++) if (númeroElementosReferencia[número] == 0) return número;
        return -24;
    }
    static int conectar(int entradaElementoDescriptor, int valorDescriptor, int claseTipoArchivo, int valorObjetivoArchivo, int ajustes) {
        abrirManejador[entradaElementoDescriptor] = valorDescriptor + 1; establecerDescriptor[entradaElementoDescriptor] = (ajustes & cerrarOperaciónEjecuciónActivado) != 0 ? 1 : 0;
        valorClaseTipo[valorDescriptor] = claseTipoArchivo; valorObjetivo[valorDescriptor] = valorObjetivoArchivo; númeroElementosReferencia[valorDescriptor] = 1;
        abrirAjustes[valorDescriptor] = ajustes & (3 | añadirFinalContinuación | esperarNoOperadorHacer); posiciónArchivo[valorDescriptor] = 0;
        manejadorRed[valorDescriptor] = 0; recibirMilisegundosTiempoEspera[valorDescriptor] = 0;
        return entradaElementoDescriptor;
    }
    static void iniciarProceso() {
        procesoLimpiar();
        for (int número = 0; número < 3; número++) conectar(número, número, 1, número, número == 0 ? 0 : 1);
    }
    static void procesoLimpiar() {
        for (int número = 0; número < límiteDescriptor; número++) if (abrirManejador[número] != 0) cerrarArchivo(número);
    }
    static int cerrarArchivo(int entradaElementoDescriptor) {
        int valorDescriptor = encontrarDescriptor(entradaElementoDescriptor);
        if (valorDescriptor < 0) return -9;
        abrirManejador[entradaElementoDescriptor] = 0; establecerDescriptor[entradaElementoDescriptor] = 0;
        númeroElementosReferencia[valorDescriptor]--;
        if (númeroElementosReferencia[valorDescriptor] == 0) {
            if (valorClaseTipo[valorDescriptor] == 2) SistemaArchivosMemoria.abrirNúmeroElementos[valorObjetivo[valorDescriptor]]--;
            if (valorClaseTipo[valorDescriptor] == 3 && manejadorRed[valorDescriptor] != 0) PilaRed.cerrar(manejadorRed[valorDescriptor]);
            valorClaseTipo[valorDescriptor] = 0;
        }
        return 0;
    }
    // Las rutas C son cadenas de bytes terminadas en NUL. Solo se admite un nombre directamente bajo la raíz.
    static int leerRuta(int dirección) {
        if (!GestiónEjecución.recortar(dirección, 1)) return -14;
        int posición = Dispositivo.leerMemoria(dirección) == '/' ? 1 : 0;
        for (int longitud = 0; longitud < 64; longitud++) {
            if (!GestiónEjecución.recortar(dirección + posición + longitud, 1)) return -14;
            int valor = Dispositivo.leerMemoria(dirección + posición + longitud);
            nombreRuta[longitud] = valor;
            if (valor == 0) return longitud == 0 ? -2 : (SistemaArchivosMemoria.comprobarNombre(nombreRuta, longitud) ? longitud : -22);
            if (valor == '/') return -20;
        }
        return -36;
    }
    static int abrirArchivo(int direcciónNombre, int ajustes, int concederPermiso) {
        int longitud = leerRuta(direcciónNombre);
        if (longitud < 0) return longitud;
        if ((ajustes & ~(3 | crearEntradaElemento | crearExclusivamente | borrarContenidoContenido | añadirFinalContinuación | esperarNoOperadorHacer | cerrarOperaciónEjecuciónActivado)) != 0) return -95;
        if ((ajustes & 3) == 3 || ((ajustes & borrarContenidoContenido) != 0 && (ajustes & 3) == 0)) return -22;
        int Archivo = SistemaArchivosMemoria.encontrarEntradaElemento(nombreRuta, longitud);
        if (Archivo >= 0 && (ajustes & (crearEntradaElemento | crearExclusivamente)) == (crearEntradaElemento | crearExclusivamente)) return -17;
        if (Archivo == -2 && (ajustes & crearEntradaElemento) == 0) return -2;
        int entradaElementoDescriptor = descriptorVacíoEstado(0), valorDescriptor = manejadorVacíoEstado();
        if (entradaElementoDescriptor < 0 || valorDescriptor < 0) return -24;
        if (Archivo == -2) {
            int resultado = SistemaArchivosMemoria.valorAlmacenar(nombreRuta, longitud, nombreRuta, 0);
            if (resultado < 0) return resultado;
            Archivo = SistemaArchivosMemoria.encontrarEntradaElemento(nombreRuta, longitud);
            SistemaArchivosMemoria.concesionesPermiso[Archivo] = concederPermiso & 511;
        }
        if (Archivo < 0) return Archivo;
        if ((ajustes & borrarContenidoContenido) != 0) SistemaArchivosMemoria.listaTamaño[Archivo] = 0;
        SistemaArchivosMemoria.abrirNúmeroElementos[Archivo]++;
        return conectar(entradaElementoDescriptor, valorDescriptor, 2, Archivo, ajustes);
    }
    static int leerArchivo(int entradaElementoDescriptor, int direcciónDatos, int longitud) {
        int valorDescriptor = encontrarDescriptor(entradaElementoDescriptor);
        if (valorDescriptor < 0 || (abrirAjustes[valorDescriptor] & 3) == 1) return -9;
        if (longitud < 0) return -22;
        if (longitud == 0) return 0;
        if (!GestiónEjecución.recortar(direcciónDatos, longitud)) return -14;
        if (valorClaseTipo[valorDescriptor] == 3) return recibirDatosDatagrama(entradaElementoDescriptor, direcciónDatos, longitud, 0, 0);
        if (valorClaseTipo[valorDescriptor] == 1) {
            int númeroElementosRecibido = 0;
            while (númeroElementosRecibido < longitud) {
                int valor = TerminalTexto.leerSerie();
                if (valor < 0) valor = Teclado.leer();
                if (valor < 0) {
                    if (númeroElementosRecibido > 0) return númeroElementosRecibido;
                    if ((abrirAjustes[valorDescriptor] & esperarNoOperadorHacer) != 0) return -11;
                    if (Dispositivo.milisegundosRestanteUsuario() <= 10) return -11;
                    PilaRed.verificar(); Dispositivo.cederBrevemente();
                } else {
                    Dispositivo.escribirMemoria(direcciónDatos + númeroElementosRecibido, valor); númeroElementosRecibido++;
                }
            }
            return númeroElementosRecibido;
        }
        int Archivo = valorObjetivo[valorDescriptor], posición = posiciónArchivo[valorDescriptor];
        if (posición >= SistemaArchivosMemoria.listaTamaño[Archivo]) return 0;
        if (longitud > SistemaArchivosMemoria.listaTamaño[Archivo] - posición) longitud = SistemaArchivosMemoria.listaTamaño[Archivo] - posición;
        int direcciónOriginal = Dispositivo.memoriaArchivo() + Archivo * SistemaArchivosMemoria.tamañoMáximo + posición;
        for (int número = 0; número < longitud; número++) Dispositivo.escribirMemoria(direcciónDatos + número, Dispositivo.leerMemoria(direcciónOriginal + número));
        posiciónArchivo[valorDescriptor] += longitud;
        return longitud;
    }
    static int escribirArchivo(int entradaElementoDescriptor, int direcciónDatos, int longitud) {
        int valorDescriptor = encontrarDescriptor(entradaElementoDescriptor);
        if (valorDescriptor < 0 || (abrirAjustes[valorDescriptor] & 3) == 0) return -9;
        if (longitud < 0) return -22;
        if (longitud == 0) return 0;
        if (!GestiónEjecución.recortar(direcciónDatos, longitud)) return -14;
        if (valorClaseTipo[valorDescriptor] == 3) return -89; // Un extremo de datagramas sin conexión necesita una dirección de destino.
        if (valorClaseTipo[valorDescriptor] == 1) {
            if (longitud > 16384) longitud = 16384;
            for (int número = 0; número < longitud; número++) {
                int valor = Dispositivo.leerMemoria(direcciónDatos + número);
                TerminalTexto.byteSerie(valor); TerminalTexto.carácterPantalla(valor);
            }
            return longitud;
        }
        int Archivo = valorObjetivo[valorDescriptor], tamaño = SistemaArchivosMemoria.listaTamaño[Archivo];
        int posición = (abrirAjustes[valorDescriptor] & añadirFinalContinuación) != 0 ? tamaño : posiciónArchivo[valorDescriptor];
        if (posición >= SistemaArchivosMemoria.tamañoMáximo) return -27;
        if (longitud > SistemaArchivosMemoria.tamañoMáximo - posición) longitud = SistemaArchivosMemoria.tamañoMáximo - posición;
        int direcciónDestino = Dispositivo.memoriaArchivo() + Archivo * SistemaArchivosMemoria.tamañoMáximo;
        for (int número = tamaño; número < posición; número++) Dispositivo.escribirMemoria(direcciónDestino + número, 0);
        for (int número = 0; número < longitud; número++) Dispositivo.escribirMemoria(direcciónDestino + posición + número, Dispositivo.leerMemoria(direcciónDatos + número));
        posiciónArchivo[valorDescriptor] = posición + longitud;
        if (posición + longitud > tamaño) SistemaArchivosMemoria.listaTamaño[Archivo] = posición + longitud;
        return longitud;
    }
    static int posicionarArchivo(int entradaElementoDescriptor, int valorDesfase, int raízProyecto) {
        int valorDescriptor = encontrarDescriptor(entradaElementoDescriptor);
        if (valorDescriptor < 0) return -9;
        if (valorClaseTipo[valorDescriptor] != 2) return -29;
        if (raízProyecto < 0 || raízProyecto > 2) return -22;
        int valorFondo = raízProyecto == 0 ? 0 : (raízProyecto == 1 ? posiciónArchivo[valorDescriptor] : SistemaArchivosMemoria.listaTamaño[valorObjetivo[valorDescriptor]]);
        if (valorDesfase > 0 && valorFondo > 2147483647 - valorDesfase) return -75;
        if (valorDesfase < 0 && valorDesfase < -valorFondo) return -22;
        posiciónArchivo[valorDescriptor] = valorFondo + valorDesfase;
        return posiciónArchivo[valorDescriptor];
    }
    static int descriptorDuplicado(int entradaElementoDescriptor, int descriptorNuevo, boolean valorAsignar, int ajustes) {
        int valorDescriptor = encontrarDescriptor(entradaElementoDescriptor);
        if (valorDescriptor < 0) return -9;
        if (descriptorNuevo < 0 || descriptorNuevo >= límiteDescriptor) return valorAsignar ? -9 : -22;
        if (valorAsignar && entradaElementoDescriptor == descriptorNuevo) return descriptorNuevo;
        if (valorAsignar) { if (abrirManejador[descriptorNuevo] != 0) cerrarArchivo(descriptorNuevo); }
        else { descriptorNuevo = descriptorVacíoEstado(descriptorNuevo); if (descriptorNuevo < 0) return descriptorNuevo; }
        abrirManejador[descriptorNuevo] = valorDescriptor + 1; establecerDescriptor[descriptorNuevo] = ajustes; númeroElementosReferencia[valorDescriptor]++;
        return descriptorNuevo;
    }
    static int eliminarNombreEntradaElementoArchivo(int direcciónNombre) {
        int longitud = leerRuta(direcciónNombre);
        if (longitud < 0) return longitud;
        int Archivo = SistemaArchivosMemoria.encontrarEntradaElemento(nombreRuta, longitud);
        if (Archivo < 0) return Archivo;
        SistemaArchivosMemoria.listaNombres[Archivo * 64] = 0;
        return 0;
    }
    static int establecerLongitudArchivo(int entradaElementoDescriptor, int longitud) {
        int valorDescriptor = encontrarDescriptor(entradaElementoDescriptor);
        if (valorDescriptor < 0) return -9;
        if (valorClaseTipo[valorDescriptor] != 2 || (abrirAjustes[valorDescriptor] & 3) == 0 || longitud < 0) return -22;
        if (longitud > SistemaArchivosMemoria.tamañoMáximo) return -27;
        int Archivo = valorObjetivo[valorDescriptor], dirección = Dispositivo.memoriaArchivo() + Archivo * SistemaArchivosMemoria.tamañoMáximo;
        for (int número = SistemaArchivosMemoria.listaTamaño[Archivo]; número < longitud; número++) Dispositivo.escribirMemoria(dirección + número, 0);
        SistemaArchivosMemoria.listaTamaño[Archivo] = longitud;
        return 0;
    }
    static int leerEstadoArchivo(int entradaElementoDescriptor, int dirección) {
        int valorDescriptor = encontrarDescriptor(entradaElementoDescriptor);
        if (valorDescriptor < 0) return -9;
        if (!GestiónEjecución.recortar(dirección, 48)) return -14;
        for (int número = 0; número < 12; número++) GestiónEjecución.escribirNúmero(dirección + número * 4, 0);
        int Archivo = valorObjetivo[valorDescriptor], tamaño = valorClaseTipo[valorDescriptor] == 2 ? SistemaArchivosMemoria.listaTamaño[Archivo] : 0;
        int concederPermiso = valorClaseTipo[valorDescriptor] == 2 ? SistemaArchivosMemoria.concesionesPermiso[Archivo] : 438;
        GestiónEjecución.escribirNúmero(dirección, 1);
        GestiónEjecución.escribirNúmero(dirección + 4, valorClaseTipo[valorDescriptor] == 2 ? Archivo + 1 : 100 + valorDescriptor);
        GestiónEjecución.escribirNúmero(dirección + 8, (valorClaseTipo[valorDescriptor] == 2 ? 32768 : (valorClaseTipo[valorDescriptor] == 1 ? 8192 : 49152)) | concederPermiso);
        GestiónEjecución.escribirNúmero(dirección + 12, valorClaseTipo[valorDescriptor] == 2 && SistemaArchivosMemoria.listaNombres[Archivo * 64] == 0 ? 0 : 1);
        GestiónEjecución.escribirNúmero(dirección + 28, tamaño); GestiónEjecución.escribirNúmero(dirección + 32, 512);
        GestiónEjecución.escribirNúmero(dirección + 36, (tamaño + 511) / 512);
        return 0;
    }
    static int descriptorControl(int entradaElementoDescriptor, int comando, int valor) {
        int valorDescriptor = encontrarDescriptor(entradaElementoDescriptor);
        if (valorDescriptor < 0) return -9;
        if (comando == 0 || comando == 1030) return descriptorDuplicado(entradaElementoDescriptor, valor, false, comando == 1030 ? 1 : 0);
        if (comando == 1) return establecerDescriptor[entradaElementoDescriptor];
        if (comando == 2) { if ((valor & ~1) != 0) return -22; establecerDescriptor[entradaElementoDescriptor] = valor; return 0; }
        if (comando == 3) return abrirAjustes[valorDescriptor];
        if (comando == 4) {
            if ((valor & ~(3 | añadirFinalContinuación | esperarNoOperadorHacer)) != 0) return -95;
            abrirAjustes[valorDescriptor] = (abrirAjustes[valorDescriptor] & 3) | (valor & (añadirFinalContinuación | esperarNoOperadorHacer)); return 0;
        }
        return -95;
    }
    static int crearExtremo(int esquemaDirección, int claseTipoRed, int númeroContrato) {
        if (esquemaDirección != 2) return -97;
        if (claseTipoRed != 2) return -93;
        if (númeroContrato != 0 && númeroContrato != 17) return -93;
        int entradaElementoDescriptor = descriptorVacíoEstado(0), valorDescriptor = manejadorVacíoEstado();
        if (entradaElementoDescriptor < 0 || valorDescriptor < 0) return -24;
        return conectar(entradaElementoDescriptor, valorDescriptor, 3, 0, leerBanderaEscribir);
    }
    static int descriptorExtremo(int entradaElementoDescriptor) {
        int valorDescriptor = encontrarDescriptor(entradaElementoDescriptor);
        if (valorDescriptor < 0) return -9;
        return valorClaseTipo[valorDescriptor] == 3 ? valorDescriptor : -88;
    }
    static int dirección32(int dirección) {
        return Dispositivo.leerMemoria(dirección) << 24 | Dispositivo.leerMemoria(dirección + 1) << 16
            | Dispositivo.leerMemoria(dirección + 2) << 8 | Dispositivo.leerMemoria(dirección + 3);
    }
    static int comprobarDirección(int dirección, int longitud) {
        if (longitud < 16) return -22;
        if (!GestiónEjecución.recortar(dirección, 16)) return -14;
        return GestiónEjecución.valorCorto(dirección) == 2 ? 0 : -97;
    }
    static int asociarDirección(int entradaElementoDescriptor, int dirección, int longitud) {
        int valorDescriptor = descriptorExtremo(entradaElementoDescriptor);
        if (valorDescriptor < 0) return valorDescriptor;
        int resultado = comprobarDirección(dirección, longitud);
        if (resultado < 0) return resultado;
        if (manejadorRed[valorDescriptor] != 0) return -22;
        int direcciónRed = dirección32(dirección + 4);
        if (direcciónRed != 0 && direcciónRed != PilaRed.direcciónPropio) return -99;
        int númeroPuerto = Dispositivo.leerMemoria(dirección + 2) << 8 | Dispositivo.leerMemoria(dirección + 3);
        resultado = PilaRed.abrir(númeroPuerto);
        if (resultado < 0) return resultado;
        manejadorRed[valorDescriptor] = resultado; valorObjetivo[valorDescriptor] = direcciónRed;
        return 0;
    }
    static int asociarModoAuto(int valorDescriptor) {
        if (manejadorRed[valorDescriptor] != 0) return 0;
        int resultado = PilaRed.abrir(0);
        if (resultado < 0) return resultado;
        manejadorRed[valorDescriptor] = resultado;
        return 0;
    }
    // Los dos últimos argumentos de sendto/recvfrom se pasan en una estructura de solicitud de 8 bytes.
    static int enviarDatosDatagrama(int entradaElementoDescriptor, int direcciónDatos, int longitud, int ajustes, int direcciónSolicitado) {
        int valorDescriptor = descriptorExtremo(entradaElementoDescriptor);
        if (valorDescriptor < 0) return valorDescriptor;
        if (ajustes != 0) return -95;
        if (longitud < 0 || longitud > 1024) return -90;
        if (longitud != 0 && !GestiónEjecución.recortar(direcciónDatos, longitud)) return -14;
        if (!GestiónEjecución.recortar(direcciónSolicitado, 8)) return -14;
        int dirección = GestiónEjecución.númeroValor(direcciónSolicitado);
        int resultado = comprobarDirección(dirección, GestiónEjecución.númeroValor(direcciónSolicitado + 4));
        if (resultado < 0) return resultado;
        int númeroPuerto = Dispositivo.leerMemoria(dirección + 2) << 8 | Dispositivo.leerMemoria(dirección + 3);
        if (númeroPuerto == 0) return -22;
        resultado = asociarModoAuto(valorDescriptor);
        if (resultado < 0) return resultado;
        for (int número = 0; número < longitud; número++) datosTransferencia[número] = Dispositivo.leerMemoria(direcciónDatos + número);
        return PilaRed.enviar(manejadorRed[valorDescriptor], dirección32(dirección + 4), númeroPuerto, datosTransferencia, longitud);
    }
    static void escribirDirección(int dirección, int longitud, int direcciónRed, int númeroPuerto) {
        for (int número = 0; número < longitud && número < 16; número++) {
            int valor = 0;
            if (número == 0) valor = 2;
            if (número == 2) valor = númeroPuerto >>> 8;
            if (número == 3) valor = númeroPuerto;
            if (número >= 4 && número < 8) valor = direcciónRed >>> (56 - número * 8);
            Dispositivo.escribirMemoria(dirección + número, valor & 255);
        }
    }
    static int recibirDatosDatagrama(int entradaElementoDescriptor, int direcciónDatos, int longitud, int ajustes, int direcciónSolicitado) {
        int valorDescriptor = descriptorExtremo(entradaElementoDescriptor);
        if (valorDescriptor < 0) return valorDescriptor;
        if ((ajustes & ~64) != 0) return -95;
        if (longitud < 0) return -22;
        if (longitud != 0 && !GestiónEjecución.recortar(direcciónDatos, longitud)) return -14;
        int dirección = 0, direcciónLongitudDirección = 0, longitudDirección = 0;
        if (direcciónSolicitado != 0) {
            if (!GestiónEjecución.recortar(direcciónSolicitado, 8)) return -14;
            dirección = GestiónEjecución.númeroValor(direcciónSolicitado); direcciónLongitudDirección = GestiónEjecución.númeroValor(direcciónSolicitado + 4);
            if (dirección != 0) {
                if (!GestiónEjecución.recortar(direcciónLongitudDirección, 4)) return -14;
                longitudDirección = GestiónEjecución.númeroValor(direcciónLongitudDirección);
                if (longitudDirección < 0) return -22;
                if (!GestiónEjecución.recortar(dirección, longitudDirección < 16 ? longitudDirección : 16)) return -14;
            }
        }
        int resultado = asociarModoAuto(valorDescriptor);
        if (resultado < 0) return resultado;
        int ponerEnMarcha = Dispositivo.milisegundos();
        while (true) {
            resultado = PilaRed.recibir(manejadorRed[valorDescriptor], datosTransferencia, 1024, 0);
            if (resultado != -11) break;
            if ((ajustes & 64) != 0 || (abrirAjustes[valorDescriptor] & esperarNoOperadorHacer) != 0) return -11;
            if (recibirMilisegundosTiempoEspera[valorDescriptor] > 0 && Dispositivo.milisegundos() - ponerEnMarcha >= recibirMilisegundosTiempoEspera[valorDescriptor]) return -11;
            if (Dispositivo.milisegundosRestanteUsuario() <= 10) return -11;
            Dispositivo.cederBrevemente();
        }
        if (resultado < 0) return resultado;
        if (resultado > longitud) resultado = longitud;
        for (int número = 0; número < resultado; número++) Dispositivo.escribirMemoria(direcciónDatos + número, datosTransferencia[número]);
        if (dirección != 0) {
            escribirDirección(dirección, longitudDirección, PilaRed.direcciónParRed(manejadorRed[valorDescriptor]), PilaRed.númeroPuertoParRed(manejadorRed[valorDescriptor]));
            GestiónEjecución.escribirNúmero(direcciónLongitudDirección, 16);
        }
        return resultado;
    }
    static int leerDirecciónConectorRed(int entradaElementoDescriptor, int dirección, int direcciónLongitud) {
        int valorDescriptor = descriptorExtremo(entradaElementoDescriptor);
        if (valorDescriptor < 0) return valorDescriptor;
        if (!GestiónEjecución.recortar(direcciónLongitud, 4)) return -14;
        int longitud = GestiónEjecución.númeroValor(direcciónLongitud);
        if (longitud < 0) return -22;
        if (!GestiónEjecución.recortar(dirección, longitud < 16 ? longitud : 16)) return -14;
        int entradaElementoRanura = PilaRed.número(manejadorRed[valorDescriptor]);
        escribirDirección(dirección, longitud, valorObjetivo[valorDescriptor], entradaElementoRanura < 0 ? 0 : PilaRed.puertos[entradaElementoRanura]);
        GestiónEjecución.escribirNúmero(direcciónLongitud, 16);
        return 0;
    }
    static int establecerTiempoEsperaRecibir(int entradaElementoDescriptor, int milisegundos) {
        int valorDescriptor = descriptorExtremo(entradaElementoDescriptor);
        if (valorDescriptor < 0) return valorDescriptor;
        if (milisegundos < 0 || milisegundos > 2000) return -22;
        recibirMilisegundosTiempoEspera[valorDescriptor] = milisegundos;
        return 0;
    }
}
