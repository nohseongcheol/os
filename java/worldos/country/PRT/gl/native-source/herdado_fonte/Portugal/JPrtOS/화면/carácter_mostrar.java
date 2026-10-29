// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class carácter_mostrar {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Vertical_cargo;

    public carácter_mostrar() {
        borrar_introdución();
    }

    public void Saída(String Contido_VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < Contido_VALOR.length(); ÍNDICE++) {
            char 문자 = Contido_VALOR.charAt(ÍNDICE);
            if (문자 == '\n') {
                가로 = 0;
                Vertical_cargo++;
            } else {
                문자출력(가로++, Vertical_cargo, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Vertical_cargo++;
            }
            if (Vertical_cargo >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Vertical_cargo) {
        verificar_cargo(가로, Vertical_cargo);
        return 문자들[Vertical_cargo * 너비 + 가로];
    }

    public void borrar_introdución() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Vertical_cargo = 0;
    }

    private void 문자출력(int 가로, int Vertical_cargo, char 문자) {
        verificar_cargo(가로, Vertical_cargo);
        문자들[Vertical_cargo * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Vertical_cargo = 높이 - 1;
    }

    private void verificar_cargo(int 가로, int Vertical_cargo) {
        if (가로 < 0 || 가로 >= 너비 || Vertical_cargo < 0 || Vertical_cargo >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

