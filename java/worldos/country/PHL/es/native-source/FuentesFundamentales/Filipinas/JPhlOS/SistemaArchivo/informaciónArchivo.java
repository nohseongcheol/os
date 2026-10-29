// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Filipinas.JPhlOS.SistemaArchivo;

public final class informaciónArchivo {
    private final int tamaño;
    private final int claseTipoForma;

    public informaciónArchivo(int tamaño, int claseTipoForma) {
        this.tamaño = tamaño;
        this.claseTipoForma = claseTipoForma;
    }

    public int tamaño() {
        return tamaño;
    }

    public int claseTipoForma() {
        return claseTipoForma;
    }
}

