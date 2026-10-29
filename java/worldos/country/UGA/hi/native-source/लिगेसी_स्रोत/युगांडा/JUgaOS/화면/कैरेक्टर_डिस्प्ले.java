// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package युगांडा.JUgaOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class कैरेक्टर_डिस्प्ले {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int अनुलंब_पद;

    public कैरेक्टर_डिस्प्ले() {
        मिटाएँ_एन्ट्री();
    }

    public void निर्गम(String सामग्री_मान) {
        for (int इंडेक्स = 0; इंडेक्स < सामग्री_मान.length(); इंडेक्स++) {
            char 문자 = सामग्री_मान.charAt(इंडेक्स);
            if (문자 == '\n') {
                가로 = 0;
                अनुलंब_पद++;
            } else {
                मुद्रित_करें_कैरेक्टर(가로++, अनुलंब_पद, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                अनुलंब_पद++;
            }
            if (अनुलंब_पद >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int अनुलंब_पद) {
        सत्यापित_करें_पद(가로, अनुलंब_पद);
        return 문자들[अनुलंब_पद * 너비 + 가로];
    }

    public void मिटाएँ_एन्ट्री() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        अनुलंब_पद = 0;
    }

    private void मुद्रित_करें_कैरेक्टर(int 가로, int अनुलंब_पद, char 문자) {
        सत्यापित_करें_पद(가로, अनुलंब_पद);
        문자들[अनुलंब_पद * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        अनुलंब_पद = 높이 - 1;
    }

    private void सत्यापित_करें_पद(int 가로, int अनुलंब_पद) {
        if (가로 < 0 || 가로 >= 너비 || अनुलंब_पद < 0 || अनुलंब_पद >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

