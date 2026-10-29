// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class znak_displej {
    public static final int 너비 = 80;
    public static final int výška_VALUE = 25;
    private final char[] 문자들 = new char[너비 * výška_VALUE];
    private int 가로;
    private int vertikála_pozícia;

    public znak_displej() {
        vymazať_položka();
    }

    public void Výstup(String obsah_VALUE) {
        for (int INDEX = 0; INDEX < obsah_VALUE.length(); INDEX++) {
            char 문자 = obsah_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                vertikála_pozícia++;
            } else {
                문자출력(가로++, vertikála_pozícia, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                vertikála_pozícia++;
            }
            if (vertikála_pozícia >= výška_VALUE) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int vertikála_pozícia) {
        overiť_pozícia(가로, vertikála_pozícia);
        return 문자들[vertikála_pozícia * 너비 + 가로];
    }

    public void vymazať_položka() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        vertikála_pozícia = 0;
    }

    private void 문자출력(int 가로, int vertikála_pozícia, char 문자) {
        overiť_pozícia(가로, vertikála_pozícia);
        문자들[vertikála_pozícia * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (výška_VALUE - 1));
        Arrays.fill(문자들, 너비 * (výška_VALUE - 1), 문자들.length, ' ');
        vertikála_pozícia = výška_VALUE - 1;
    }

    private void overiť_pozícia(int 가로, int vertikála_pozícia) {
        if (가로 < 0 || 가로 >= 너비 || vertikála_pozícia < 0 || vertikála_pozícia >= výška_VALUE) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

