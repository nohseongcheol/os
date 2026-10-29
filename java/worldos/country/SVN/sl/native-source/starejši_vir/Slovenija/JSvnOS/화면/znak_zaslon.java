// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class znak_zaslon {
    public static final int 너비 = 80;
    public static final int višina_VALUE = 25;
    private final char[] 문자들 = new char[너비 * višina_VALUE];
    private int 가로;
    private int Navpično_položaj;

    public znak_zaslon() {
        izbrisati_vnos();
    }

    public void Izpis(String vsebina_VALUE) {
        for (int INDEX = 0; INDEX < vsebina_VALUE.length(); INDEX++) {
            char 문자 = vsebina_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Navpično_položaj++;
            } else {
                문자출력(가로++, Navpično_položaj, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Navpično_položaj++;
            }
            if (Navpično_položaj >= višina_VALUE) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Navpično_položaj) {
        위치확인(가로, Navpično_položaj);
        return 문자들[Navpično_položaj * 너비 + 가로];
    }

    public void izbrisati_vnos() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Navpično_položaj = 0;
    }

    private void 문자출력(int 가로, int Navpično_položaj, char 문자) {
        위치확인(가로, Navpično_položaj);
        문자들[Navpično_položaj * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (višina_VALUE - 1));
        Arrays.fill(문자들, 너비 * (višina_VALUE - 1), 문자들.length, ' ');
        Navpično_položaj = višina_VALUE - 1;
    }

    private void 위치확인(int 가로, int Navpično_položaj) {
        if (가로 < 0 || 가로 >= 너비 || Navpično_položaj < 0 || Navpično_položaj >= višina_VALUE) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

