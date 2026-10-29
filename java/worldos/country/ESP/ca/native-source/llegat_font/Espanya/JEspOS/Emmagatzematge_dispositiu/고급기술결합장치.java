// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.Emmagatzematge_dispositiu;

import java.util.Arrays;

/** ATA 28비트 Ordre 계층과 같은 512바이트 논리 secció_VALOR 장치다. */
public final class 고급기술결합장치 {
    public static final int secció_canviar_la_mida = 512;
    private final byte[] dades;
    private final boolean només_de_lectura_VALOR;

    public 고급기술결합장치(int secció_COMPT, boolean només_de_lectura_VALOR) {
        if (secció_COMPT <= 0) {
            throw new IllegalArgumentException("secció_VALOR 수가 올바르지 않습니다.");
        }
        dades = new byte[Math.multiplyExact(secció_COMPT, secció_canviar_la_mida)];
        this.només_de_lectura_VALOR = només_de_lectura_VALOR;
    }

    public int secció_COMPT() {
        return dades.length / secció_canviar_la_mida;
    }

    public void Lectura(int secció_INDEX, byte[] rebre_destinació) {
        xec_interval(secció_INDEX, rebre_destinació);
        System.arraycopy(dades, secció_INDEX * secció_canviar_la_mida, rebre_destinació, 0, secció_canviar_la_mida);
    }

    public void Escriptura(int secció_INDEX, byte[] 쓸자료) {
        if (només_de_lectura_VALOR) {
            throw new IllegalStateException("Lectura 전용 장치입니다.");
        }
        xec_interval(secció_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, dades, secció_INDEX * secció_canviar_la_mida, secció_canviar_la_mida);
    }

    public void esborrar_introducció() {
        if (només_de_lectura_VALOR) {
            throw new IllegalStateException("Lectura 전용 장치입니다.");
        }
        Arrays.fill(dades, (byte) 0);
    }

    private void xec_interval(int secció_INDEX, byte[] 임시공간) {
        if (secció_INDEX < 0 || secció_INDEX >= secció_COMPT() || 임시공간.length < secció_canviar_la_mida) {
            throw new IllegalArgumentException("ATA secció_VALOR 범위가 올바르지 않습니다.");
        }
    }
}

