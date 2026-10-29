// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class stafur_birta {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Lóðrétt_staða;

    public stafur_birta() {
        eyða_færsla();
    }

    public void úttak(String Efni_VALUE) {
        for (int INDEX = 0; INDEX < Efni_VALUE.length(); INDEX++) {
            char 문자 = Efni_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Lóðrétt_staða++;
            } else {
                문자출력(가로++, Lóðrétt_staða, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Lóðrétt_staða++;
            }
            if (Lóðrétt_staða >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Lóðrétt_staða) {
        sannprófa_staða(가로, Lóðrétt_staða);
        return 문자들[Lóðrétt_staða * 너비 + 가로];
    }

    public void eyða_færsla() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Lóðrétt_staða = 0;
    }

    private void 문자출력(int 가로, int Lóðrétt_staða, char 문자) {
        sannprófa_staða(가로, Lóðrétt_staða);
        문자들[Lóðrétt_staða * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Lóðrétt_staða = 높이 - 1;
    }

    private void sannprófa_staða(int 가로, int Lóðrétt_staða) {
        if (가로 < 0 || 가로 >= 너비 || Lóðrétt_staða < 0 || Lóðrétt_staða >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

