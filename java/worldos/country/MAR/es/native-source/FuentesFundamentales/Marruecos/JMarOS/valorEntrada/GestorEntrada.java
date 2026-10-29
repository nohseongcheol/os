// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Marruecos.JMarOS.valorEntrada;

import java.util.ArrayDeque;
import java.util.Queue;

/** Transfiere de forma segura los eventos de entrada entre interrupciones y código gestionado. */
public final class GestorEntrada {
    private final Queue<eventoEntrada> listaEventos = new ArrayDeque<eventoEntrada>();
    private final int númeroElementosEventoMáximo;
    private int númeroElementosEventoDescartadosNúmero;

    public GestorEntrada(int númeroElementosEventoMáximo) {
        if (númeroElementosEventoMáximo <= 0) {
            throw new IllegalArgumentException("evento 수가 올바르지 않습니다.");
        }
        this.númeroElementosEventoMáximo = númeroElementosEventoMáximo;
    }

    public synchronized void abajoTecla(int datosTecla) {
        ponerValor(new eventoEntrada(eventoEntrada.valorClaseTipo.abajoTecla, datosTecla & 0xff, 0));
    }

    public synchronized void arribaTecla(int datosTecla) {
        ponerValor(new eventoEntrada(eventoEntrada.valorClaseTipo.arribaTecla, datosTecla & 0xff, 0));
    }

    public synchronized void movimientoRatón(int posiciónHorizontal, int posiciónVertical) {
        ponerValor(new eventoEntrada(eventoEntrada.valorClaseTipo.movimientoRatón, posiciónHorizontal, posiciónVertical));
    }

    public synchronized eventoEntrada eventoSiguiente() {
        return listaEventos.poll();
    }

    public synchronized int númeroElementosEventoDescartadosNúmero() {
        return númeroElementosEventoDescartadosNúmero;
    }

    private void ponerValor(eventoEntrada evento) {
        if (listaEventos.size() == númeroElementosEventoMáximo) {
            listaEventos.poll();
            númeroElementosEventoDescartadosNúmero++;
        }
        listaEventos.offer(evento);
    }
}

