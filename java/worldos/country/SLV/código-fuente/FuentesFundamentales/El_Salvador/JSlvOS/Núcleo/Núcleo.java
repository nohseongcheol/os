// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package El_Salvador.JSlvOS.Núcleo;

import El_Salvador.JSlvOS.EspacioMemoria.GestorMemoria;
import El_Salvador.JSlvOS.EspacioMemoria.GestorPágina;
import El_Salvador.JSlvOS.valorEntrada.GestorEntrada;
import El_Salvador.JSlvOS.Tarea.valorProceso;
import El_Salvador.JSlvOS.Tarea.Planificador;
import El_Salvador.JSlvOS.LlamadaSistema.LlamadaSistema;
import El_Salvador.JSlvOS.SistemaArchivo.tablaDescriptorArchivo;
import El_Salvador.JSlvOS.SistemaArchivo.SistemaArchivo;

/** Ensambla e inicia el núcleo gestionado en Java. */
public final class Núcleo {
    private final valorEquipoFísico Dispositivo;
    private final GestorMemoria EspacioMemoria = new GestorMemoria(32 * 1024 * 1024);
    private final GestorPágina gestiónPágina = new GestorPágina();
    private final SistemaArchivo SistemaArchivo = new SistemaArchivo();
    private final Planificador Planificador = new Planificador(gestiónPágina);
    private final GestorEntrada GestiónEntrada = new GestorEntrada(256);
    private final valorProceso procesoPrimero;
    private final LlamadaSistema LlamadaSistema;

    public Núcleo(valorEquipoFísico Dispositivo) {
        this.Dispositivo = Dispositivo;
        procesoPrimero = Planificador.procesoPrimero(new tablaDescriptorArchivo(SistemaArchivo));
        LlamadaSistema = new LlamadaSistema(SistemaArchivo, gestiónPágina, Planificador, Dispositivo, GestiónEntrada);
    }

    public void ponerEnMarcha() {
        Dispositivo.salidaSerie("=== JSlvOS 관리 valorNúcleo ===\n");
    }

    public void ejecutarPasoUnidad() {
        Dispositivo.cPUDetenerMáquina();
    }

    public GestorMemoria EspacioMemoria() {
        return EspacioMemoria;
    }

    public GestorPágina gestiónPágina() {
        return gestiónPágina;
    }

    public SistemaArchivo SistemaArchivo() {
        return SistemaArchivo;
    }

    public Planificador Planificador() {
        return Planificador;
    }

    public GestorEntrada GestiónEntrada() {
        return GestiónEntrada;
    }

    public valorProceso procesoPrimero() {
        return procesoPrimero;
    }

    public LlamadaSistema LlamadaSistema() {
        return LlamadaSistema;
    }
}
