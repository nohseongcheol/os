// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Северна_Македонија.JMkdOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class знак_екран {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int вертикала_позиционирање;

    public знак_екран() {
        избриши_внес();
    }

    public void 출력(String Содржина_VALUE) {
        for (int INDEX = 0; INDEX < Содржина_VALUE.length(); INDEX++) {
            char 문자 = Содржина_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                вертикала_позиционирање++;
            } else {
                문자출력(가로++, вертикала_позиционирање, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                вертикала_позиционирање++;
            }
            if (вертикала_позиционирање >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int вертикала_позиционирање) {
        провери_позиционирање(가로, вертикала_позиционирање);
        return 문자들[вертикала_позиционирање * 너비 + 가로];
    }

    public void избриши_внес() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        вертикала_позиционирање = 0;
    }

    private void 문자출력(int 가로, int вертикала_позиционирање, char 문자) {
        провери_позиционирање(가로, вертикала_позиционирање);
        문자들[вертикала_позиционирање * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        вертикала_позиционирање = 높이 - 1;
    }

    private void провери_позиционирање(int 가로, int вертикала_позиционирање) {
        if (가로 < 0 || 가로 >= 너비 || вертикала_позиционирање < 0 || вертикала_позиционирање >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

