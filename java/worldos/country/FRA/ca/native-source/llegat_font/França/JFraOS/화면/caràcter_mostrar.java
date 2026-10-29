// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package França.JFraOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class caràcter_mostrar {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Vertical_càrrec;

    public caràcter_mostrar() {
        esborrar_introducció();
    }

    public void Sortida(String contingut_VALOR) {
        for (int INDEX = 0; INDEX < contingut_VALOR.length(); INDEX++) {
            char 문자 = contingut_VALOR.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Vertical_càrrec++;
            } else {
                imprimir_caràcter(가로++, Vertical_càrrec, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Vertical_càrrec++;
            }
            if (Vertical_càrrec >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Vertical_càrrec) {
        verificar_càrrec(가로, Vertical_càrrec);
        return 문자들[Vertical_càrrec * 너비 + 가로];
    }

    public void esborrar_introducció() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Vertical_càrrec = 0;
    }

    private void imprimir_caràcter(int 가로, int Vertical_càrrec, char 문자) {
        verificar_càrrec(가로, Vertical_càrrec);
        문자들[Vertical_càrrec * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Vertical_càrrec = 높이 - 1;
    }

    private void verificar_càrrec(int 가로, int Vertical_càrrec) {
        if (가로 < 0 || 가로 >= 너비 || Vertical_càrrec < 0 || Vertical_càrrec >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

