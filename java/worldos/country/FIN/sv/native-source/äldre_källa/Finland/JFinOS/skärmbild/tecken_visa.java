// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Finland.JFinOS.skärmbild;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 skärmbild 모형이다. */
public final class tecken_visa {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int bransch_placera;

    public tecken_visa() {
        radera_post();
    }

    public void utmatningsposition(String Innehåll_värde) {
        for (int INDEX = 0; INDEX < Innehåll_värde.length(); INDEX++) {
            char 문자 = Innehåll_värde.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                bransch_placera++;
            } else {
                skriva_ut_tecken(가로++, bransch_placera, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                bransch_placera++;
            }
            if (bransch_placera >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int bransch_placera) {
        verifiera_placera(가로, bransch_placera);
        return 문자들[bransch_placera * 너비 + 가로];
    }

    public void radera_post() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        bransch_placera = 0;
    }

    private void skriva_ut_tecken(int 가로, int bransch_placera, char 문자) {
        verifiera_placera(가로, bransch_placera);
        문자들[bransch_placera * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        bransch_placera = 높이 - 1;
    }

    private void verifiera_placera(int 가로, int bransch_placera) {
        if (가로 < 0 || 가로 >= 너비 || bransch_placera < 0 || bransch_placera >= 높이) {
            throw new IllegalArgumentException("skärmbild 위치가 올바르지 않습니다.");
        }
    }
}

