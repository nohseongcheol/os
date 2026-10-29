// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Alemania.JDeuOS.Tarea;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Alemania.JDeuOS.EspacioMemoria.GestorPágina;
import Alemania.JDeuOS.SistemaArchivo.tablaDescriptorArchivo;

/** Gestiona identificadores de proceso y una cola de preparados por turnos. */
public final class Planificador {
    private final GestorPágina gestiónPágina;
    private final Map<Integer, valorProceso> listaProceso = new HashMap<Integer, valorProceso>();
    private final Queue<valorProceso> colaListo = new ArrayDeque<valorProceso>();
    private int identificadorSiguiente = 1;

    public Planificador(GestorPágina gestiónPágina) {
        this.gestiónPágina = gestiónPágina;
    }

    public valorProceso procesoPrimero(tablaDescriptorArchivo descriptorArchivo) {
        valorProceso procesoNuevo = new valorProceso(asignarMemoriaIdentificador(), 0, gestiónPágina.espacioDirecciónNuevo(), descriptorArchivo);
        listaProceso.put(Integer.valueOf(procesoNuevo.valorIdentificador()), procesoNuevo);
        colaListo.offer(procesoNuevo);
        return procesoNuevo;
    }

    public valorProceso valorClonar(valorProceso valorPadre) {
        valorProceso valorHijo = new valorProceso(
                asignarMemoriaIdentificador(),
                valorPadre.valorIdentificador(),
                gestiónPágina.escribirActivadoCopiarClonar(valorPadre.EspacioDirección()),
                valorPadre.descriptorArchivo().valorClonar());
        valorHijo.establecerInterrumpirBuclePrograma(valorPadre.interrumpirBuclePrograma());
        listaProceso.put(Integer.valueOf(valorHijo.valorIdentificador()), valorHijo);
        colaListo.offer(valorHijo);
        return valorHijo;
    }

    public valorProceso procesoSiguiente() {
        int comprobarNúmeroElementos = colaListo.size();
        for (int número = 0; número < comprobarNúmeroElementos; número++) {
            valorProceso elementoListaSiguiente = colaListo.poll();
            if (elementoListaSiguiente != null && (elementoListaSiguiente.valorEstadoValor() == estadoValorProceso.preparar || elementoListaSiguiente.valorEstadoValor() == estadoValorProceso.ejecutarComando)) {
                elementoListaSiguiente.establecerEstadoValor(estadoValorProceso.ejecutarComando);
                colaListo.offer(elementoListaSiguiente);
                return elementoListaSiguiente;
            }
        }
        return null;
    }

    public int esperarHijoPara(valorProceso valorPadre, int identificadorHijo, boolean bloqueanteNoCondición) {
        for (valorProceso candidato : listaProceso.values()) {
            if (candidato.identificadorPadre() != valorPadre.valorIdentificador()) {
                continue;
            }
            if (identificadorHijo > 0 && candidato.valorIdentificador() != identificadorHijo) {
                continue;
            }
            if (candidato.valorEstadoValor() == estadoValorProceso.programaSalir) {
                int resultado = (candidato.códigoSalir() & 0xff) << 8;
                listaProceso.remove(Integer.valueOf(candidato.valorIdentificador()));
                return resultado;
            }
            return bloqueanteNoCondición ? 0 : -11;
        }
        return -10;
    }

    public valorProceso encontrarProceso(int valorIdentificador) {
        return listaProceso.get(Integer.valueOf(valorIdentificador));
    }

    private int asignarMemoriaIdentificador() {
        return identificadorSiguiente++;
    }
}
