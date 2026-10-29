// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Antígua_e_Barbuda.JAtgOS.tela;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 tela 모형이다. */
public final class caractere_visor {
    public static final int 너비 = 80;
    public static final int altura_VALOR = 25;
    private final char[] 문자들 = new char[너비 * altura_VALOR];
    private int 가로;
    private int Vertical_cargo;

    public caractere_visor() {
        apagar_entrada();
    }

    public void saídaTexto(String Conteúdo_VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < Conteúdo_VALOR.length(); ÍNDICE++) {
            char 문자 = Conteúdo_VALOR.charAt(ÍNDICE);
            if (문자 == '\n') {
                가로 = 0;
                Vertical_cargo++;
            } else {
                imprimir_caractere(가로++, Vertical_cargo, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Vertical_cargo++;
            }
            if (Vertical_cargo >= altura_VALOR) {
                Scroll_up();
            }
        }
    }

    public char 문자(int 가로, int Vertical_cargo) {
        verificar_cargo(가로, Vertical_cargo);
        return 문자들[Vertical_cargo * 너비 + 가로];
    }

    public void apagar_entrada() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Vertical_cargo = 0;
    }

    private void imprimir_caractere(int 가로, int Vertical_cargo, char 문자) {
        verificar_cargo(가로, Vertical_cargo);
        문자들[Vertical_cargo * 너비 + 가로] = 문자;
    }

    private void Scroll_up() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (altura_VALOR - 1));
        Arrays.fill(문자들, 너비 * (altura_VALOR - 1), 문자들.length, ' ');
        Vertical_cargo = altura_VALOR - 1;
    }

    private void verificar_cargo(int 가로, int Vertical_cargo) {
        if (가로 < 0 || 가로 >= 너비 || Vertical_cargo < 0 || Vertical_cargo >= altura_VALOR) {
            throw new IllegalArgumentException("tela 위치가 올바르지 않습니다.");
        }
    }
}

