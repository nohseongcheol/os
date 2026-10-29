// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class znak_displej {
    public static final int 너비 = 80;
    public static final int výška_HODNOTA = 25;
    private final char[] 문자들 = new char[너비 * výška_HODNOTA];
    private int 가로;
    private int Svislá_pozice;

    public znak_displej() {
        vymazat_položka();
    }

    public void výstupní_pozice(String Obsah_HODNOTA) {
        for (int INDEX = 0; INDEX < Obsah_HODNOTA.length(); INDEX++) {
            char 문자 = Obsah_HODNOTA.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Svislá_pozice++;
            } else {
                문자출력(가로++, Svislá_pozice, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Svislá_pozice++;
            }
            if (Svislá_pozice >= výška_HODNOTA) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Svislá_pozice) {
        ověřit_pozice(가로, Svislá_pozice);
        return 문자들[Svislá_pozice * 너비 + 가로];
    }

    public void vymazat_položka() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Svislá_pozice = 0;
    }

    private void 문자출력(int 가로, int Svislá_pozice, char 문자) {
        ověřit_pozice(가로, Svislá_pozice);
        문자들[Svislá_pozice * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (výška_HODNOTA - 1));
        Arrays.fill(문자들, 너비 * (výška_HODNOTA - 1), 문자들.length, ' ');
        Svislá_pozice = výška_HODNOTA - 1;
    }

    private void ověřit_pozice(int 가로, int Svislá_pozice) {
        if (가로 < 0 || 가로 >= 너비 || Svislá_pozice < 0 || Svislá_pozice >= výška_HODNOTA) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

