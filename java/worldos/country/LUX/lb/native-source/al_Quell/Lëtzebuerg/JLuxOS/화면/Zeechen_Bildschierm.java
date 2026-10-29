// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class Zeechen_Bildschierm {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Vertikal_positionéieren;

    public Zeechen_Bildschierm() {
        지우기();
    }

    public void 출력(String Inhalt_VALUE) {
        for (int INDEX = 0; INDEX < Inhalt_VALUE.length(); INDEX++) {
            char 문자 = Inhalt_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Vertikal_positionéieren++;
            } else {
                문자출력(가로++, Vertikal_positionéieren, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Vertikal_positionéieren++;
            }
            if (Vertikal_positionéieren >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Vertikal_positionéieren) {
        verifizéieren_positionéieren(가로, Vertikal_positionéieren);
        return 문자들[Vertikal_positionéieren * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Vertikal_positionéieren = 0;
    }

    private void 문자출력(int 가로, int Vertikal_positionéieren, char 문자) {
        verifizéieren_positionéieren(가로, Vertikal_positionéieren);
        문자들[Vertikal_positionéieren * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Vertikal_positionéieren = 높이 - 1;
    }

    private void verifizéieren_positionéieren(int 가로, int Vertikal_positionéieren) {
        if (가로 < 0 || 가로 >= 너비 || Vertikal_positionéieren < 0 || Vertikal_positionéieren >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

