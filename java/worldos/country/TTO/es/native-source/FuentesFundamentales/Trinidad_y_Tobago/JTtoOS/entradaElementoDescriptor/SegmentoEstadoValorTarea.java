// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Trinidad_y_Tobago.JTtoOS.entradaElementoDescriptor;

/** Representación gestionada del TSS que proporciona una pila privilegiada al cambiar de tarea x86. */
public final class SegmentoEstadoValorTarea {
    private int bloqueCeroPila;
    private int direcciónCeroPila;
    private int posiciónTablaPermisoEntradaSalida = 104;

    public void establecerPilaPrivilegiado(int valorFragmento, int dirección) {
        bloqueCeroPila = valorFragmento;
        direcciónCeroPila = dirección;
    }

    public int bloqueCeroPila() { return bloqueCeroPila; }
    public int direcciónCeroPila() { return direcciónCeroPila; }
    public int posiciónTablaPermisoEntradaSalida() { return posiciónTablaPermisoEntradaSalida; }
}

