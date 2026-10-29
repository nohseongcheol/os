// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class वर्ण_प्रदर्शन {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int ठाडो_राख्नुहोस्;

    public वर्ण_प्रदर्शन() {
        지우기();
    }

    public void 출력(String सामग्री_मान) {
        for (int अनुक्रमणिका = 0; अनुक्रमणिका < सामग्री_मान.length(); अनुक्रमणिका++) {
            char 문자 = सामग्री_मान.charAt(अनुक्रमणिका);
            if (문자 == '\n') {
                가로 = 0;
                ठाडो_राख्नुहोस्++;
            } else {
                문자출력(가로++, ठाडो_राख्नुहोस्, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                ठाडो_राख्नुहोस्++;
            }
            if (ठाडो_राख्नुहोस् >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int ठाडो_राख्नुहोस्) {
        रुजू_गर्नुहोस्_राख्नुहोस्(가로, ठाडो_राख्नुहोस्);
        return 문자들[ठाडो_राख्नुहोस् * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        ठाडो_राख्नुहोस् = 0;
    }

    private void 문자출력(int 가로, int ठाडो_राख्नुहोस्, char 문자) {
        रुजू_गर्नुहोस्_राख्नुहोस्(가로, ठाडो_राख्नुहोस्);
        문자들[ठाडो_राख्नुहोस् * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        ठाडो_राख्नुहोस् = 높이 - 1;
    }

    private void रुजू_गर्नुहोस्_राख्नुहोस्(int 가로, int ठाडो_राख्नुहोस्) {
        if (가로 < 0 || 가로 >= 너비 || ठाडो_राख्नुहोस् < 0 || ठाडो_राख्नुहोस् >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

