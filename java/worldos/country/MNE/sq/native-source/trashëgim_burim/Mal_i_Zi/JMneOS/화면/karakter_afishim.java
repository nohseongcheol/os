// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mal_i_Zi.JMneOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class karakter_afishim {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Vertikal_pozicioni;

    public karakter_afishim() {
        spastroj_futje();
    }

    public void 출력(String Përmbajtje_VALUE) {
        for (int INDEX = 0; INDEX < Përmbajtje_VALUE.length(); INDEX++) {
            char 문자 = Përmbajtje_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Vertikal_pozicioni++;
            } else {
                문자출력(가로++, Vertikal_pozicioni, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Vertikal_pozicioni++;
            }
            if (Vertikal_pozicioni >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Vertikal_pozicioni) {
        verifikoj_pozicioni(가로, Vertikal_pozicioni);
        return 문자들[Vertikal_pozicioni * 너비 + 가로];
    }

    public void spastroj_futje() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Vertikal_pozicioni = 0;
    }

    private void 문자출력(int 가로, int Vertikal_pozicioni, char 문자) {
        verifikoj_pozicioni(가로, Vertikal_pozicioni);
        문자들[Vertikal_pozicioni * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Vertikal_pozicioni = 높이 - 1;
    }

    private void verifikoj_pozicioni(int 가로, int Vertikal_pozicioni) {
        if (가로 < 0 || 가로 >= 너비 || Vertikal_pozicioni < 0 || Vertikal_pozicioni >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

