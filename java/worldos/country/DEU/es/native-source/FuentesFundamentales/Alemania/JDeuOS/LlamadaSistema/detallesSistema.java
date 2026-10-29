// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Alemania.JDeuOS.LlamadaSistema;

public final class detallesSistema {
    private final String nombreSistema;
    private final String nombreNodo;
    private final String valorEdición;
    private final String valorVersión;
    private final String máquina;

    public detallesSistema(String nombreSistema, String nombreNodo, String valorEdición, String valorVersión, String máquina) {
        this.nombreSistema = nombreSistema;
        this.nombreNodo = nombreNodo;
        this.valorEdición = valorEdición;
        this.valorVersión = valorVersión;
        this.máquina = máquina;
    }

    public String nombreSistema() { return nombreSistema; }
    public String nombreNodo() { return nombreNodo; }
    public String valorEdición() { return valorEdición; }
    public String valorVersión() { return valorVersión; }
    public String máquina() { return máquina; }
}
