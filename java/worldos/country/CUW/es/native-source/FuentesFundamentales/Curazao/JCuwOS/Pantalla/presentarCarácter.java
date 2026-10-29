// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Curazao.JCuwOS.Pantalla;

import java.util.Arrays;

/** Modelo de pantalla de 80x25 caracteres, como el modo de texto VGA. */
public final class presentarCarácter {
    public static final int valorAnchura = 80;
    public static final int valorAltura = 25;
    private final char[] valoresCarácter = new char[valorAnchura * valorAltura];
    private int posiciónHorizontal;
    private int posiciónVertical;

    public presentarCarácter() {
        borrarEntradaElemento();
    }

    public void Salida(String valorContenidoValor) {
        for (int número = 0; número < valorContenidoValor.length(); número++) {
            char Caracteres = valorContenidoValor.charAt(número);
            if (Caracteres == '\n') {
                posiciónHorizontal = 0;
                posiciónVertical++;
            } else {
                imprimirCarácter(posiciónHorizontal++, posiciónVertical, Caracteres);
            }
            if (posiciónHorizontal >= valorAnchura) {
                posiciónHorizontal = 0;
                posiciónVertical++;
            }
            if (posiciónVertical >= valorAltura) {
                arribaDesplazarVista();
            }
        }
    }

    public char Caracteres(int posiciónHorizontal, int posiciónVertical) {
        verificarPosición(posiciónHorizontal, posiciónVertical);
        return valoresCarácter[posiciónVertical * valorAnchura + posiciónHorizontal];
    }

    public void borrarEntradaElemento() {
        Arrays.fill(valoresCarácter, ' ');
        posiciónHorizontal = 0;
        posiciónVertical = 0;
    }

    private void imprimirCarácter(int posiciónHorizontal, int posiciónVertical, char Caracteres) {
        verificarPosición(posiciónHorizontal, posiciónVertical);
        valoresCarácter[posiciónVertical * valorAnchura + posiciónHorizontal] = Caracteres;
    }

    private void arribaDesplazarVista() {
        System.arraycopy(valoresCarácter, valorAnchura, valoresCarácter, 0, valorAnchura * (valorAltura - 1));
        Arrays.fill(valoresCarácter, valorAnchura * (valorAltura - 1), valoresCarácter.length, ' ');
        posiciónVertical = valorAltura - 1;
    }

    private void verificarPosición(int posiciónHorizontal, int posiciónVertical) {
        if (posiciónHorizontal < 0 || posiciónHorizontal >= valorAnchura || posiciónVertical < 0 || posiciónVertical >= valorAltura) {
            throw new IllegalArgumentException("Pantalla 위치가 올바르지 않습니다.");
        }
    }
}

