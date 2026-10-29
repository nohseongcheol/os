// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class znak_ekran {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Vertikalno_položaj;

    public znak_ekran() {
        지우기();
    }

    public void Ispis(String Sadržaj_VALUE) {
        for (int INDEX = 0; INDEX < Sadržaj_VALUE.length(); INDEX++) {
            char 문자 = Sadržaj_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Vertikalno_položaj++;
            } else {
                문자출력(가로++, Vertikalno_položaj, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Vertikalno_položaj++;
            }
            if (Vertikalno_položaj >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Vertikalno_položaj) {
        potvrditi_položaj(가로, Vertikalno_položaj);
        return 문자들[Vertikalno_položaj * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Vertikalno_položaj = 0;
    }

    private void 문자출력(int 가로, int Vertikalno_položaj, char 문자) {
        potvrditi_položaj(가로, Vertikalno_položaj);
        문자들[Vertikalno_položaj * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Vertikalno_položaj = 높이 - 1;
    }

    private void potvrditi_položaj(int 가로, int Vertikalno_položaj) {
        if (가로 < 0 || 가로 >= 너비 || Vertikalno_položaj < 0 || Vertikalno_položaj >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

