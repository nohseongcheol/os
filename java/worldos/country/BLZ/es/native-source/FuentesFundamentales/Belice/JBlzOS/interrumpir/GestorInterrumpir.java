// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belice.JBlzOS.interrumpir;

import java.util.Arrays;

/** Registra y distribuye los manejadores IDT del lado gestionado por Java. */
public final class GestorInterrumpir {
    private final ManejadorEventoInterrumpir[] listaManejadorEvento = new ManejadorEventoInterrumpir[256];
    private boolean activo;

    public void registroEntradaElemento(int número, ManejadorEventoInterrumpir ManejadorEvento) {
        verificarNúmero(número);
        listaManejadorEvento[número] = ManejadorEvento;
    }

    public void liberarAlmacenamiento(int número) {
        verificarNúmero(número);
        listaManejadorEvento[número] = null;
    }

    public int distribuirValor(int número, int direcciónPilaGuardado) {
        verificarNúmero(número);
        if (!activo) {
            return direcciónPilaGuardado;
        }
        ManejadorEventoInterrumpir ManejadorEvento = listaManejadorEvento[número];
        return ManejadorEvento == null ? direcciónPilaGuardado : ManejadorEvento.entradaElementoValorProceso(direcciónPilaGuardado);
    }

    public void activar() {
        activo = true;
    }

    public void desactivar() {
        activo = false;
    }

    public boolean esActivo() {
        return activo;
    }

    public void liberarTodos() {
        Arrays.fill(listaManejadorEvento, null);
    }

    private void verificarNúmero(int número) {
        if (número < 0 || número >= listaManejadorEvento.length) {
            throw new IllegalArgumentException("interrumpir 번호가 올바르지 않습니다.");
        }
    }
}

