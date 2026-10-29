// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class वर्ण_प्रदर्शन {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int उबें_स्थिती;

    public वर्ण_प्रदर्शन() {
        지우기();
    }

    public void 출력(String अनुक्रमणिका_मोल) {
        for (int INDEX = 0; INDEX < अनुक्रमणिका_मोल.length(); INDEX++) {
            char 문자 = अनुक्रमणिका_मोल.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                उबें_स्थिती++;
            } else {
                문자출력(가로++, उबें_स्थिती, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                उबें_स्थिती++;
            }
            if (उबें_स्थिती >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int उबें_स्थिती) {
        पुनर्तपासणी_करची_स्थिती(가로, उबें_स्थिती);
        return 문자들[उबें_स्थिती * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        उबें_स्थिती = 0;
    }

    private void 문자출력(int 가로, int उबें_स्थिती, char 문자) {
        पुनर्तपासणी_करची_स्थिती(가로, उबें_स्थिती);
        문자들[उबें_स्थिती * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        उबें_स्थिती = 높이 - 1;
    }

    private void पुनर्तपासणी_करची_स्थिती(int 가로, int उबें_स्थिती) {
        if (가로 < 0 || 가로 >= 너비 || उबें_स्थिती < 0 || उबें_स्थिती >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

