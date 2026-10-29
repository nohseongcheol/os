// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class תו_צג {
    public static final int 너비 = 80;
    public static final int גובה_ערך = 25;
    private final char[] 문자들 = new char[너비 * גובה_ערך];
    private int 가로;
    private int אנכי_עמדה;

    public תו_צג() {
        מחק_ערך();
    }

    public void פלטטקסט(String תוכן_ערך) {
        for (int מדד = 0; מדד < תוכן_ערך.length(); מדד++) {
            char 문자 = תוכן_ערך.charAt(מדד);
            if (문자 == '\n') {
                가로 = 0;
                אנכי_עמדה++;
            } else {
                הדפס_תו(가로++, אנכי_עמדה, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                אנכי_עמדה++;
            }
            if (אנכי_עמדה >= גובה_ערך) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int אנכי_עמדה) {
        ודא_אמת_עמדה(가로, אנכי_עמדה);
        return 문자들[אנכי_עמדה * 너비 + 가로];
    }

    public void מחק_ערך() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        אנכי_עמדה = 0;
    }

    private void הדפס_תו(int 가로, int אנכי_עמדה, char 문자) {
        ודא_אמת_עמדה(가로, אנכי_עמדה);
        문자들[אנכי_עמדה * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (גובה_ערך - 1));
        Arrays.fill(문자들, 너비 * (גובה_ערך - 1), 문자들.length, ' ');
        אנכי_עמדה = גובה_ערך - 1;
    }

    private void ודא_אמת_עמדה(int 가로, int אנכי_עמדה) {
        if (가로 < 0 || 가로 >= 너비 || אנכי_עמדה < 0 || אנכי_עמדה >= גובה_ערך) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

