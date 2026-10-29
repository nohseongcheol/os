// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** Comprueba las condiciones esperadas en los ejemplos ejecutables y las pruebas. */
public final class Comprobaciones {
    private Comprobaciones() {}
    public static void exigir(boolean condición, String valorCausa) {
        if (!condición) throw new ExcepciónArgumentoInválido(valorCausa);
    }
}
