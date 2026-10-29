// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.Almacenamento_dispositivo;

import java.util.Arrays;

/** ATA 28비트 Orde 계층과 같은 512바이트 논리 sección_VALOR 장치다. */
public final class 고급기술결합장치 {
    public static final int 구역크기 = 512;
    private final byte[] datos;
    private final boolean só_de_lectura_VALOR;

    public 고급기술결합장치(int sección_CONTAR, boolean só_de_lectura_VALOR) {
        if (sección_CONTAR <= 0) {
            throw new IllegalArgumentException("sección_VALOR 수가 올바르지 않습니다.");
        }
        datos = new byte[Math.multiplyExact(sección_CONTAR, 구역크기)];
        this.só_de_lectura_VALOR = só_de_lectura_VALOR;
    }

    public int sección_CONTAR() {
        return datos.length / 구역크기;
    }

    public void Lectura(int sección_ÍNDICE, byte[] 받을곳) {
        cheque_intervalo(sección_ÍNDICE, 받을곳);
        System.arraycopy(datos, sección_ÍNDICE * 구역크기, 받을곳, 0, 구역크기);
    }

    public void Escritura(int sección_ÍNDICE, byte[] 쓸자료) {
        if (só_de_lectura_VALOR) {
            throw new IllegalStateException("Lectura 전용 장치입니다.");
        }
        cheque_intervalo(sección_ÍNDICE, 쓸자료);
        System.arraycopy(쓸자료, 0, datos, sección_ÍNDICE * 구역크기, 구역크기);
    }

    public void borrar_introdución() {
        if (só_de_lectura_VALOR) {
            throw new IllegalStateException("Lectura 전용 장치입니다.");
        }
        Arrays.fill(datos, (byte) 0);
    }

    private void cheque_intervalo(int sección_ÍNDICE, byte[] 임시공간) {
        if (sección_ÍNDICE < 0 || sección_ÍNDICE >= sección_CONTAR() || 임시공간.length < 구역크기) {
            throw new IllegalArgumentException("ATA sección_VALOR 범위가 올바르지 않습니다.");
        }
    }
}

