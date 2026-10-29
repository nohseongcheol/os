// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gibraltar.JGibOS.Pruebas;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Gibraltar.JGibOS.EspacioMemoria.GestorMemoria;
import Gibraltar.JGibOS.EspacioMemoria.GestorPágina;
import Gibraltar.JGibOS.valorEntrada.eventoEntrada;
import Gibraltar.JGibOS.Tarea.valorProceso;
import Gibraltar.JGibOS.LlamadaSistema.LlamadaSistema;
import Gibraltar.JGibOS.SistemaArchivo.CargadorCódigoEjecutable;
import Gibraltar.JGibOS.Núcleo.Núcleo;
import Gibraltar.JGibOS.Anfitrión.EquipoFísicoAnfitrión;
import Gibraltar.JGibOS.interrumpir.GestorInterrumpir;
import Gibraltar.JGibOS.entradaElementoDescriptor.TablaDescriptorGlobal;
import Gibraltar.JGibOS.dispositivoAlmacenamiento.AdjuntoTecnologíaAvanzado;
import Gibraltar.JGibOS.Dispositivo.GestorBusPeriférico;
import Gibraltar.JGibOS.PilaRed.HerramientasRed;
import Gibraltar.JGibOS.PilaRed.CapaRed;
import Gibraltar.JGibOS.Dispositivo.Reloj;
import Gibraltar.JGibOS.entradaElementoDescriptor.SegmentoEstadoValorTarea;
import Gibraltar.JGibOS.Pantalla.presentarCarácter;
import Gibraltar.JGibOS.SistemaArchivo.tablaParticiónPrimario;

public final class pruebaTodos {
    private static int númeroElementosPaso;

    private pruebaTodos() {
    }

    public static void main(String[] argumentoParámetro) {
        EquipoFísicoAnfitrión Dispositivo = new EquipoFísicoAnfitrión();
        Núcleo valorNúcleo = new Núcleo(Dispositivo);
        valorNúcleo.ponerEnMarcha();

        pruebaMemoria(valorNúcleo);
        pruebaGestiónPágina(valorNúcleo);
        pruebaProcesosYArchivos(valorNúcleo);
        pruebaELF(valorNúcleo);
        pruebaEntrada(valorNúcleo);
        pruebaEquipoFísico(Dispositivo);
        pruebaDescriptoresYInterrupciones();
        pruebaConexiónRedYAlmacenamiento();
        pruebaRelojYPantalla();

        System.out.println("JGibOS Pruebas valorPaso: " + númeroElementosPaso);
    }

    private static void pruebaMemoria(Núcleo valorNúcleo) {
        GestorMemoria valorGestor = valorNúcleo.EspacioMemoria();
        int direcciónPrimero = valorGestor.asignarMemoriaAlineado(100, 64);
        verificar((direcciónPrimero & 63) == 0, "valorAlinear asignarMemoriaAlmacenamiento");
        valorGestor.escribirValorByte(direcciónPrimero, (byte) 0x5a);
        verificar(valorGestor.leerValorByte(direcciónPrimero) == (byte) 0x5a, "물리 EspacioMemoria 읽고 escribir");
        int usarAntes = valorGestor.tamañoUsado();
        valorGestor.liberarAlmacenamiento(direcciónPrimero);
        verificar(valorGestor.tamañoUsado() < usarAntes, "EspacioMemoria liberarAlmacenamiento");
    }

    private static void pruebaGestiónPágina(Núcleo valorNúcleo) {
        GestorPágina valorGestor = valorNúcleo.gestiónPágina();
        GestorPágina.EspacioDirección espacioPadre = valorGestor.espacioDirecciónNuevo();
        valorGestor.páginaTablaCorrespondencia(espacioPadre, 0x1000, true);
        valorGestor.escribirValorByte(espacioPadre, 0x1010, (byte) 7);
        GestorPágina.EspacioDirección espacioHijo = valorGestor.escribirActivadoCopiarClonar(espacioPadre);
        valorGestor.escribirValorByte(espacioHijo, 0x1010, (byte) 9);
        verificar(valorGestor.leerValorByte(espacioPadre, 0x1010) == 7, "escribir 시 copiarValor valorPadre 격리");
        verificar(valorGestor.leerValorByte(espacioHijo, 0x1010) == 9, "escribir 시 copiarValor valorHijo escribir");
    }

    private static void pruebaProcesosYArchivos(Núcleo valorNúcleo) {
        byte[] valorContenidoValor = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        valorNúcleo.SistemaArchivo().añadirFinalArchivo("Pruebas", valorContenidoValor);
        valorProceso valorPadre = valorNúcleo.procesoPrimero();
        LlamadaSistema invocar = valorNúcleo.LlamadaSistema();
        int entradaElementoDescriptor = invocar.abrir(valorPadre, "/Pruebas", LlamadaSistema.leerBanderaSolamente);
        verificar(entradaElementoDescriptor >= 3, "Archivo abrir");

        byte[] recibirDestino = new byte[valorContenidoValor.length];
        verificar(invocar.leer(valorPadre, entradaElementoDescriptor, recibirDestino, recibirDestino.length) == valorContenidoValor.length, "Archivo leer");
        verificar(Arrays.equals(valorContenidoValor, recibirDestino), "Archivo valorContenidoValor");
        verificar(invocar.posiciónMover(valorPadre, entradaElementoDescriptor, 0, LlamadaSistema.buscarCoincidenciaIniciar) == 0, "Archivo posición valorMover");

        int descriptorClonado = invocar.descriptorDuplicado(valorPadre, entradaElementoDescriptor);
        verificar(descriptorClonado >= 0, "entradaElementoDescriptor valorClonar");
        valorProceso valorHijo = invocar.procesoClonar(valorPadre);
        verificar(valorHijo.valorIdentificador() != valorPadre.valorIdentificador(), "valorProceso valorIdentificador 분리");
        verificar(valorHijo.identificadorPadre() == valorPadre.valorIdentificador(), "valorPadre valorProceso valorIdentificador");
        verificar(invocar.cerrar(valorHijo, entradaElementoDescriptor) == 0 && valorPadre.descriptorArchivo().esAbrir(entradaElementoDescriptor), "valorHijo cerrar 격리");

        int finElementoPrevio = invocar.aumentarInterrumpirBuclePrograma(valorPadre, 8192);
        verificar(finElementoPrevio == 0x06000000, "Programa terminación 늘리기");
        verificar(valorPadre.interrumpirBuclePrograma() == 0x06002000, "Programa terminación 반영");
        verificar(valorHijo.interrumpirBuclePrograma() == 0x06000000, "과정별 Programa terminación 격리");

        valorHijo.programaSalir(7);
        verificar(invocar.esperarHijoPara(valorPadre, valorHijo.valorIdentificador(), false) == (7 << 8), "valorHijo programaSalir esperarFin");
        verificar(invocar.esAccesible("Pruebas", 1) == -13, "ejecutarComando valorPermiso rechazarValor");
        verificar(invocar.identificadorUsuario() == 0 && invocar.identificadorGrupo() == 0, "사용자와 무리 valorIdentificador");
        verificar("/".equals(invocar.listaTareaActual(2)) && invocar.listaTareaConmutar("/") == 0, "elementoListaActual Tarea listaEntradaElemento");
        verificar(invocar.esTerminal(valorPadre, 1), "표준 Salida EntradaSalidaTerminal");
        verificar("JGibOS".equals(invocar.detallesSistema().nombreSistema()), "valorSistemaOperación informaciónSistema");
    }

    private static void pruebaELF(Núcleo valorNúcleo) {
        byte[] Datos = new byte[92];
        Datos[0] = 0x7f;
        Datos[1] = 'E';
        Datos[2] = 'L';
        Datos[3] = 'F';
        Datos[4] = 1;
        Datos[5] = 1;
        escribirValorEnteroValor(Datos, 24, 0x04001000);
        escribirValorEnteroValor(Datos, 32, 52);
        escribirEnteroValorCorto(Datos, 46, 40);
        escribirEnteroValorCorto(Datos, 48, 1);
        escribirValorEnteroValor(Datos, 56, 8);
        escribirValorEnteroValor(Datos, 60, 2);
        escribirValorEnteroValor(Datos, 64, 0x04002000);
        escribirValorEnteroValor(Datos, 72, 64);

        CargadorCódigoEjecutable.imagen valorImagen = new CargadorCódigoEjecutable().Comprobaciones(Datos);
        verificar(valorImagen.iniciarDirección() == 0x04001000, "ELF ponerEnMarcha dirección");
        verificar(valorImagen.listaSecciones().size() == 1 && valorImagen.listaSecciones().get(0).valorClaseTipo() == 8, "ELF 빈 Datos valorSección");
        int entradaElementoDescriptor = valorNúcleo.LlamadaSistema().abrir(valorNúcleo.procesoPrimero(), "Pruebas", LlamadaSistema.leerBanderaSolamente);
        verificar(valorNúcleo.LlamadaSistema().controlArchivo(valorNúcleo.procesoPrimero(), entradaElementoDescriptor, 2, 1) == 0, "ejecutarComando 시 cerrar ajustes");
        verificar(valorNúcleo.LlamadaSistema().ejecutarComando(valorNúcleo.procesoPrimero(), Datos, new String[] {"Pruebas", "값"}, new String[] {"Lengua=español"}) == 0, "ELF ejecutarComando valorImagen 적재");
        verificar(valorNúcleo.procesoPrimero().direcciónIniciarEjecución() == 0x04001000, "ejecutarComando ponerEnMarcha dirección 반영");
        verificar(valorNúcleo.procesoPrimero().argumentoEjecución().length == 2 && valorNúcleo.procesoPrimero().valorEntorno().length == 1, "ejecutarComando 인자와 entorno");
        verificar(!valorNúcleo.procesoPrimero().descriptorArchivo().esAbrir(entradaElementoDescriptor), "ejecutarComando 시 entradaElementoDescriptor cerrar");
        verificar(valorNúcleo.gestiónPágina().leerValorByte(valorNúcleo.procesoPrimero().EspacioDirección(), 0x04002000) == 0, "빈 Datos valorSección operandoCero inicializar");
    }

    private static void pruebaEntrada(Núcleo valorNúcleo) {
        valorNúcleo.GestiónEntrada().abajoTecla('가');
        valorNúcleo.GestiónEntrada().movimientoRatón(3, -2);
        eventoEntrada eventoPrimero = valorNúcleo.GestiónEntrada().eventoSiguiente();
        eventoEntrada eventoSegundo = valorNúcleo.GestiónEntrada().eventoSiguiente();
        verificar(eventoPrimero.claseTipoEvento() == eventoEntrada.valorClaseTipo.abajoTecla, "자판 evento");
        verificar(eventoSegundo.valorPrimero() == 3 && eventoSegundo.valorSegundo() == -2, "쥐 valorMover evento");
    }

    private static void pruebaEquipoFísico(EquipoFísicoAnfitrión Dispositivo) {
        Dispositivo.escribirBytePuerto(0x3f8, 0xab);
        verificar(Dispositivo.leerBytePuerto(0x3f8) == 0xab, "puertoEquipoFísico salidaEntrada valorFrontera");
        verificar(Dispositivo.diarioSerie().contains("JGibOS"), "valorSerie registroEntradaDiario");
    }

    private static void pruebaDescriptoresYInterrupciones() {
        GestorInterrumpir valorGestor = new GestorInterrumpir();
        valorGestor.registroEntradaElemento(0x21, direcciónAlmacenamiento -> direcciónAlmacenamiento + 4);
        valorGestor.activar();
        verificar(valorGestor.distribuirValor(0x21, 100) == 104, "interrumpir distribuirValor");
        valorGestor.desactivar();
        verificar(valorGestor.distribuirValor(0x21, 100) == 100, "interrumpir desactivar");

        TablaDescriptorGlobal tablaDescriptor = new TablaDescriptorGlobal();
        tablaDescriptor.establecerValorPredeterminado();
        verificar(tablaDescriptor.listaFragmentos().size() == 5, "전역 tablaDescriptor");
        SegmentoEstadoValorTarea estadoValorTarea = new SegmentoEstadoValorTarea();
        estadoValorTarea.establecerPilaPrivilegiado(0x10, 0x800000);
        verificar(estadoValorTarea.bloqueCeroPila() == 0x10 && estadoValorTarea.direcciónCeroPila() == 0x800000, "Tarea valorEstadoValor valorSección");
    }

    private static void pruebaConexiónRedYAlmacenamiento() {
        AdjuntoTecnologíaAvanzado dispositivoAlmacenamiento = new AdjuntoTecnologíaAvanzado(4, false);
        byte[] escribirHaciaDatos = new byte[AdjuntoTecnologíaAvanzado.tamañoSección];
        byte[] leerValorDatos = new byte[AdjuntoTecnologíaAvanzado.tamañoSección];
        escribirHaciaDatos[17] = 42;
        dispositivoAlmacenamiento.escribir(2, escribirHaciaDatos);
        dispositivoAlmacenamiento.leer(2, leerValorDatos);
        verificar(leerValorDatos[17] == 42, "ATA valorSección 읽고 escribir");

        GestorBusPeriférico periférico = new GestorBusPeriférico();
        periférico.valorDescubierto(new GestorBusPeriférico.Dispositivo(0x1022, 0x2000, 0xc000, 11));
        verificar(periférico.encontrarEntradaElemento(0x1022, 0x2000) != null, "주변 Dispositivo encontrarEntradaElemento");

        byte[] marcoEthernet = new byte[34];
        marcoEthernet[12] = 0x08;
        marcoEthernet[13] = 0x00;
        marcoEthernet[14] = 0x45;
        verificar(HerramientasRed.protocoloSuperiorEthernet(marcoEthernet) == 0x0800, "이더넷 상위 valorContrato");
        verificar(HerramientasRed.esProtocolo4VersiónIP(marcoEthernet, 14), "상호통신망규약 4판");
        verificar(HerramientasRed.sumaComprobaciónInternet(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 sumaComprobación");

        byte[] secciónPrimero = new byte[512];
        secciónPrimero[510] = 0x55;
        secciónPrimero[511] = (byte) 0xaa;
        secciónPrimero[450] = 0x0b;
        escribirValorEnteroValor(secciónPrimero, 454, 63);
        escribirValorEnteroValor(secciónPrimero, 458, 1024);
        verificar(new tablaParticiónPrimario().leer(secciónPrimero).size() == 1, "valorPredeterminado 분할 영역표");

        CapaRed valorCapa = new CapaRed();
        int[] númeroElementosRecibido = new int[1];
        valorCapa.registroUnidadDatosUsuario(7, (Datos, ponerEnMarcha, longitud) -> númeroElementosRecibido[0]++);
        byte[] índiceMarco = new byte[14 + 20 + 8];
        índiceMarco[12] = 0x08;
        índiceMarco[13] = 0x00;
        índiceMarco[14] = 0x45;
        índiceMarco[16] = 0;
        índiceMarco[17] = 28;
        índiceMarco[23] = 17;
        índiceMarco[36] = 0;
        índiceMarco[37] = 7;
        verificar(valorCapa.recibirEthernet(índiceMarco) && númeroElementosRecibido[0] == 1, "Usuario Datos valorUnidad distribuirValor");
    }

    private static void pruebaRelojYPantalla() {
        presentarCarácter Pantalla = new presentarCarácter();
        Pantalla.Salida("가나\n다");
        verificar(Pantalla.Caracteres(0, 0) == '가' && Pantalla.Caracteres(0, 1) == '다', "Caracteres Pantalla Salida");
        Reloj Reloj = new Reloj(100);
        for (int número = 0; número < 10; número++) {
            Reloj.valorPulso();
        }
        verificar(Reloj.milisegundosTranscurrido() == 100, "Reloj valorPulso convertirValor");
    }

    private static void escribirValorEnteroValor(byte[] Datos, int posición, int valor) {
        Datos[posición] = (byte) valor;
        Datos[posición + 1] = (byte) (valor >>> 8);
        Datos[posición + 2] = (byte) (valor >>> 16);
        Datos[posición + 3] = (byte) (valor >>> 24);
    }

    private static void escribirEnteroValorCorto(byte[] Datos, int posición, int valor) {
        Datos[posición] = (byte) valor;
        Datos[posición + 1] = (byte) (valor >>> 8);
    }

    private static void verificar(boolean condición, String nombre) {
        if (!condición) {
            throw new AssertionError("valorFallo: " + nombre);
        }
        númeroElementosPaso++;
        System.out.println("valorPaso: " + nombre);
    }
}
