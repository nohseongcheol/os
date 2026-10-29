// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package México.JMexOS.Núcleo;

import México.JMexOS.EspacioMemoria.GestorMemoria;
import México.JMexOS.EspacioMemoria.GestorPágina;
import México.JMexOS.valorEntrada.GestorEntrada;
import México.JMexOS.Tarea.valorProceso;
import México.JMexOS.Tarea.Planificador;
import México.JMexOS.LlamadaSistema.LlamadaSistema;
import México.JMexOS.SistemaArchivo.tablaDescriptorArchivo;
import México.JMexOS.SistemaArchivo.SistemaArchivo;

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
        Dispositivo.salidaSerie("=== JMexOS 관리 valorNúcleo ===\n");
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
