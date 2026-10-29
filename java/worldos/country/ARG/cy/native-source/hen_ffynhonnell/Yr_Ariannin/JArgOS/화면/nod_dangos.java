// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yr_Ariannin.JArgOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class nod_dangos {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Ar_i_fyny_safle;

    public nod_dangos() {
        지우기();
    }

    public void Allbwn(String Cynnwys_VALUE) {
        for (int INDEX = 0; INDEX < Cynnwys_VALUE.length(); INDEX++) {
            char 문자 = Cynnwys_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Ar_i_fyny_safle++;
            } else {
                문자출력(가로++, Ar_i_fyny_safle, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Ar_i_fyny_safle++;
            }
            if (Ar_i_fyny_safle >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Ar_i_fyny_safle) {
        dilysu_safle(가로, Ar_i_fyny_safle);
        return 문자들[Ar_i_fyny_safle * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Ar_i_fyny_safle = 0;
    }

    private void 문자출력(int 가로, int Ar_i_fyny_safle, char 문자) {
        dilysu_safle(가로, Ar_i_fyny_safle);
        문자들[Ar_i_fyny_safle * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Ar_i_fyny_safle = 높이 - 1;
    }

    private void dilysu_safle(int 가로, int Ar_i_fyny_safle) {
        if (가로 < 0 || 가로 >= 너비 || Ar_i_fyny_safle < 0 || Ar_i_fyny_safle >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

