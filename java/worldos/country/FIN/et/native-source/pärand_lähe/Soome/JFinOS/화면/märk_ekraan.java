// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class märk_ekraan {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int vertikaal_ametikoht;

    public märk_ekraan() {
        kustutama_kirje();
    }

    public void Väljund(String Sisu_VALUE) {
        for (int INDEX = 0; INDEX < Sisu_VALUE.length(); INDEX++) {
            char 문자 = Sisu_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                vertikaal_ametikoht++;
            } else {
                printima_märk(가로++, vertikaal_ametikoht, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                vertikaal_ametikoht++;
            }
            if (vertikaal_ametikoht >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int vertikaal_ametikoht) {
        kinnitama_ametikoht(가로, vertikaal_ametikoht);
        return 문자들[vertikaal_ametikoht * 너비 + 가로];
    }

    public void kustutama_kirje() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        vertikaal_ametikoht = 0;
    }

    private void printima_märk(int 가로, int vertikaal_ametikoht, char 문자) {
        kinnitama_ametikoht(가로, vertikaal_ametikoht);
        문자들[vertikaal_ametikoht * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        vertikaal_ametikoht = 높이 - 1;
    }

    private void kinnitama_ametikoht(int 가로, int vertikaal_ametikoht) {
        if (가로 < 0 || 가로 >= 너비 || vertikaal_ametikoht < 0 || vertikaal_ametikoht >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

