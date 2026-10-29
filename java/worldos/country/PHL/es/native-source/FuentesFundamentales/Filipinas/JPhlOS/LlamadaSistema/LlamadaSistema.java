// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Filipinas.JPhlOS.LlamadaSistema;

import Filipinas.JPhlOS.EspacioMemoria.GestorPágina;
import Filipinas.JPhlOS.Tarea.valorProceso;
import Filipinas.JPhlOS.Tarea.Planificador;
import Filipinas.JPhlOS.SistemaArchivo.CargadorCódigoEjecutable;
import Filipinas.JPhlOS.SistemaArchivo.SistemaArchivo;
import Filipinas.JPhlOS.SistemaArchivo.informaciónArchivo;
import Filipinas.JPhlOS.Núcleo.valorEquipoFísico;
import Filipinas.JPhlOS.valorEntrada.GestorEntrada;
import Filipinas.JPhlOS.valorEntrada.eventoEntrada;

/** Capa de gestión Java para la primera fase de llamadas POSIX de engos. */
public final class LlamadaSistema {
    public static final int leerBanderaSolamente = 0;
    public static final int buscarCoincidenciaIniciar = 0;
    public static final int buscarCoincidenciaActual = 1;
    public static final int encontrarFinEntradaElemento = 2;

    private final SistemaArchivo SistemaArchivo;
    private final GestorPágina gestiónPágina;
    private final Planificador Planificador;
    private final CargadorCódigoEjecutable cargador = new CargadorCódigoEjecutable();
    private final valorEquipoFísico Dispositivo;
    private final GestorEntrada GestiónEntrada;

    public LlamadaSistema(SistemaArchivo SistemaArchivo, GestorPágina gestiónPágina, Planificador Planificador, valorEquipoFísico Dispositivo, GestorEntrada GestiónEntrada) {
        this.SistemaArchivo = SistemaArchivo;
        this.gestiónPágina = gestiónPágina;
        this.Planificador = Planificador;
        this.Dispositivo = Dispositivo;
        this.GestiónEntrada = GestiónEntrada;
    }

    public int identificadorProceso(valorProceso procesoActual) {
        return procesoActual.valorIdentificador();
    }

    public int identificadorProcesoPadre(valorProceso procesoActual) {
        return procesoActual.identificadorPadre();
    }

    public int abrir(valorProceso procesoActual, String nombre, int valorBandera) {
        if (valorBandera != leerBanderaSolamente) {
            return -30;
        }
        return procesoActual.descriptorArchivo().abrir(nombre);
    }

    public int leer(valorProceso procesoActual, int entradaElementoDescriptor, byte[] recibirDestino, int tamaño) {
        if (entradaElementoDescriptor == 0) {
            if (tamaño <= 0 || recibirDestino.length == 0) {
                return 0;
            }
            eventoEntrada evento = GestiónEntrada.eventoSiguiente();
            if (evento == null || evento.claseTipoEvento() != eventoEntrada.valorClaseTipo.abajoTecla) {
                return -11;
            }
            recibirDestino[0] = (byte) evento.valorPrimero();
            return 1;
        }
        return procesoActual.descriptorArchivo().leer(entradaElementoDescriptor, recibirDestino, tamaño);
    }

    public int escribir(valorProceso procesoActual, int entradaElementoDescriptor, byte[] Datos, int tamaño) {
        if (entradaElementoDescriptor != 1 && entradaElementoDescriptor != 2) {
            return procesoActual.descriptorArchivo().esAbrir(entradaElementoDescriptor) ? -30 : -9;
        }
        if (tamaño < 0 || tamaño > Datos.length) {
            return -22;
        }
        Dispositivo.salidaSerie(new String(Datos, 0, tamaño, java.nio.charset.StandardCharsets.UTF_8));
        return tamaño;
    }

    public int cerrar(valorProceso procesoActual, int entradaElementoDescriptor) {
        return procesoActual.descriptorArchivo().cerrar(entradaElementoDescriptor);
    }

    public int posiciónMover(valorProceso procesoActual, int entradaElementoDescriptor, int valorDistancia, int raízProyecto) {
        return procesoActual.descriptorArchivo().posiciónMover(entradaElementoDescriptor, valorDistancia, raízProyecto);
    }

    public int descriptorDuplicado(valorProceso procesoActual, int entradaElementoDescriptor) {
        return procesoActual.descriptorArchivo().descriptorClonado(entradaElementoDescriptor, 0);
    }

    public int enPosiciónDescriptorDuplicado(valorProceso procesoActual, int entradaElementoDescriptor, int descriptorNuevo) {
        return procesoActual.descriptorArchivo().enPosiciónDuplicado(entradaElementoDescriptor, descriptorNuevo);
    }

    public int esAccesible(String nombre, int modoMétodo) {
        informaciónArchivo informaciónSistema = SistemaArchivo.informaciónSistema(nombre);
        if (informaciónSistema == null) {
            return -2;
        }
        if ((modoMétodo & 1) != 0 && (informaciónSistema.claseTipoForma() & 0111) == 0) {
            return -13;
        }
        if ((modoMétodo & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int listaTareaConmutar(String nombre) {
        return "/".equals(nombre) ? 0 : -20;
    }

    public String listaTareaActual(int recibirTamaño) {
        return recibirTamaño >= 2 ? "/" : null;
    }

    public int identificadorUsuario() { return 0; }
    public int identificadorUsuarioEficaz() { return 0; }
    public int identificadorGrupo() { return 0; }
    public int identificadorGrupoEficaz() { return 0; }

    public int sincronizarArchivo(valorProceso procesoActual, int entradaElementoDescriptor) {
        return procesoActual.descriptorArchivo().informaciónSistema(entradaElementoDescriptor) == null ? -9 : 0;
    }

    public void sincronizarTodos() {
        // El sistema de archivos actual es de solo lectura, por lo que no hay datos pendientes de volcado.
    }

    public boolean esTerminal(valorProceso procesoActual, int entradaElementoDescriptor) {
        informaciónArchivo informaciónSistema = procesoActual.descriptorArchivo().informaciónSistema(entradaElementoDescriptor);
        return informaciónSistema != null && (informaciónSistema.claseTipoForma() & 0170000) == 0020000;
    }

    public int controlArchivo(valorProceso procesoActual, int entradaElementoDescriptor, int comando, int argumentoParámetro) {
        if (comando == 0) {
            return procesoActual.descriptorArchivo().descriptorClonado(entradaElementoDescriptor, argumentoParámetro);
        }
        if (comando == 1) {
            return procesoActual.descriptorArchivo().cerrarValorOperaciónEjecuciónActivado(entradaElementoDescriptor);
        }
        if (comando == 2) {
            return procesoActual.descriptorArchivo().establecerOperaciónEjecuciónActivadoCerrar(entradaElementoDescriptor, (argumentoParámetro & 1) != 0);
        }
        if (comando == 3) {
            return procesoActual.descriptorArchivo().informaciónSistema(entradaElementoDescriptor) == null ? -9 : leerBanderaSolamente;
        }
        if (comando == 4) {
            return argumentoParámetro == leerBanderaSolamente ? 0 : -30;
        }
        return -22;
    }

    public int crearEntradaElemento(String nombre, int valorPermiso) {
        return -30;
    }

    public informaciónArchivo informaciónDescriptor(valorProceso procesoActual, int entradaElementoDescriptor) {
        return procesoActual.descriptorArchivo().informaciónSistema(entradaElementoDescriptor);
    }

    public detallesSistema detallesSistema() {
        return new detallesSistema("JPhlOS", "JPhlOS", "0.1", "Java managed kernel", "i386");
    }

    public informaciónArchivo informaciónArchivo(String nombre) {
        return SistemaArchivo.informaciónSistema(nombre);
    }

    public valorProceso procesoClonar(valorProceso valorPadre) {
        return Planificador.valorClonar(valorPadre);
    }

    public int esperarHijoPara(valorProceso valorPadre, int identificadorHijo, boolean bloqueanteNoCondición) {
        return Planificador.esperarHijoPara(valorPadre, identificadorHijo, bloqueanteNoCondición);
    }

    public int interrumpirBuclePrograma(valorProceso procesoActual, int finNuevo) {
        int finElementoPrevio = procesoActual.interrumpirBuclePrograma();
        if (finNuevo == 0) {
            return finElementoPrevio;
        }
        if (finNuevo < 0x06000000 || finNuevo > 0x07000000) {
            return -12;
        }
        int páginaPrimero = finElementoPrevio / GestorPágina.tamañoPágina;
        int páginaÚltimo = (finNuevo + GestorPágina.tamañoPágina - 1) / GestorPágina.tamañoPágina;
        if (finNuevo > finElementoPrevio) {
            for (int número = páginaPrimero; número < páginaÚltimo; número++) {
                int dirección = número * GestorPágina.tamañoPágina;
                try {
                    gestiónPágina.leerValorByte(procesoActual.EspacioDirección(), dirección);
                } catch (IllegalStateException error) {
                    gestiónPágina.páginaTablaCorrespondencia(procesoActual.EspacioDirección(), dirección, true);
                }
            }
        }
        procesoActual.establecerInterrumpirBuclePrograma(finNuevo);
        return finNuevo;
    }

    public int aumentarInterrumpirBuclePrograma(valorProceso procesoActual, int importeIncremento) {
        int finElementoPrevio = procesoActual.interrumpirBuclePrograma();
        int resultado = interrumpirBuclePrograma(procesoActual, finElementoPrevio + importeIncremento);
        return resultado < 0 ? resultado : finElementoPrevio;
    }

    public int ejecutarComando(valorProceso procesoActual, byte[] archivoCódigoEjecutable) {
        return ejecutarComando(procesoActual, archivoCódigoEjecutable, new String[0], new String[0]);
    }

    public int ejecutarComando(valorProceso procesoActual, byte[] archivoCódigoEjecutable, String[] argumentoParámetro, String[] entorno) {
        CargadorCódigoEjecutable.imagen valorImagen;
        try {
            valorImagen = cargador.Comprobaciones(archivoCódigoEjecutable);
        } catch (IllegalArgumentException error) {
            return -8;
        }
        if (argumentoParámetro == null || entorno == null || argumentoParámetro.length > 16 || entorno.length > 16) {
            return -7;
        }
        for (CargadorCódigoEjecutable.valorSección valorSección : valorImagen.listaSecciones()) {
            if ((valorSección.valorBandera() & 2) == 0 || valorSección.tamaño() == 0) {
                continue;
            }
            int páginaPrimero = valorSección.dirección() / GestorPágina.tamañoPágina;
            int páginaÚltimo = (valorSección.dirección() + valorSección.tamaño() + GestorPágina.tamañoPágina - 1) / GestorPágina.tamañoPágina;
            for (int número = páginaPrimero; número < páginaÚltimo; número++) {
                int dirección = número * GestorPágina.tamañoPágina;
                try {
                    gestiónPágina.leerValorByte(procesoActual.EspacioDirección(), dirección);
                    gestiónPágina.escribirRangoPrivado(procesoActual.EspacioDirección(), dirección, GestorPágina.tamañoPágina);
                } catch (IllegalStateException error) {
                    gestiónPágina.páginaTablaCorrespondencia(procesoActual.EspacioDirección(), dirección, true);
                }
            }
            for (int número = 0; número < valorSección.tamaño(); número++) {
                byte valor = valorSección.valorClaseTipo() == 8 ? 0 : archivoCódigoEjecutable[valorSección.posiciónArchivo() + número];
                gestiónPágina.escribirValorByte(procesoActual.EspacioDirección(), valorSección.dirección() + número, valor);
            }
        }
        procesoActual.establecerContextoEjecución(valorImagen.iniciarDirección(), argumentoParámetro, entorno);
        procesoActual.descriptorArchivo().cerrarOperaciónEjecuciónActivado();
        return 0;
    }

    public void programaTerminarSesión(valorProceso procesoActual, int valorEstadoValor) {
        procesoActual.programaSalir(valorEstadoValor);
    }
}
