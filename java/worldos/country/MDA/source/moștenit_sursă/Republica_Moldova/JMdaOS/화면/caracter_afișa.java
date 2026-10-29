// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republica_Moldova.JMdaOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class caracter_afișa {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Verticală_poziție;

    public caracter_afișa() {
        șterge_intrare();
    }

    public void Rezultat(String Conținut_VALUE) {
        for (int INDEX = 0; INDEX < Conținut_VALUE.length(); INDEX++) {
            char 문자 = Conținut_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Verticală_poziție++;
            } else {
                문자출력(가로++, Verticală_poziție, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Verticală_poziție++;
            }
            if (Verticală_poziție >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Verticală_poziție) {
        verifica_poziție(가로, Verticală_poziție);
        return 문자들[Verticală_poziție * 너비 + 가로];
    }

    public void șterge_intrare() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Verticală_poziție = 0;
    }

    private void 문자출력(int 가로, int Verticală_poziție, char 문자) {
        verifica_poziție(가로, Verticală_poziție);
        문자들[Verticală_poziție * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Verticală_poziție = 높이 - 1;
    }

    private void verifica_poziție(int 가로, int Verticală_poziție) {
        if (가로 < 0 || 가로 >= 너비 || Verticală_poziție < 0 || Verticală_poziție >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

