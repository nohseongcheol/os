// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جۇڭگو.JChnOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class ھەرپ_بەلگە_كۆرسەتكۈچ {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int تىك_ئورۇنلاشتۇرۇش;

    public ھەرپ_بەلگە_كۆرسەتكۈچ() {
        지우기();
    }

    public void چىقار(String مەزمۇن_قىممىتى) {
        for (int ئىندېكس = 0; ئىندېكس < مەزمۇن_قىممىتى.length(); ئىندېكس++) {
            char 문자 = مەزمۇن_قىممىتى.charAt(ئىندېكس);
            if (문자 == '\n') {
                가로 = 0;
                تىك_ئورۇنلاشتۇرۇش++;
            } else {
                문자출력(가로++, تىك_ئورۇنلاشتۇرۇش, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                تىك_ئورۇنلاشتۇرۇش++;
            }
            if (تىك_ئورۇنلاشتۇرۇش >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int تىك_ئورۇنلاشتۇرۇش) {
        دەلىللىمەك_ئورۇنلاشتۇرۇش(가로, تىك_ئورۇنلاشتۇرۇش);
        return 문자들[تىك_ئورۇنلاشتۇرۇش * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        تىك_ئورۇنلاشتۇرۇش = 0;
    }

    private void 문자출력(int 가로, int تىك_ئورۇنلاشتۇرۇش, char 문자) {
        دەلىللىمەك_ئورۇنلاشتۇرۇش(가로, تىك_ئورۇنلاشتۇرۇش);
        문자들[تىك_ئورۇنلاشتۇرۇش * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        تىك_ئورۇنلاشتۇرۇش = 높이 - 1;
    }

    private void دەلىللىمەك_ئورۇنلاشتۇرۇش(int 가로, int تىك_ئورۇنلاشتۇرۇش) {
        if (가로 < 0 || 가로 >= 너비 || تىك_ئورۇنلاشتۇرۇش < 0 || تىك_ئورۇنلاشتۇرۇش >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

