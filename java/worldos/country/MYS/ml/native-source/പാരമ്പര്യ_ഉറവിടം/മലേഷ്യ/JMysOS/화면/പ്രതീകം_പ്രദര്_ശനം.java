// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package മലേഷ്യ.JMysOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class പ്രതീകം_പ്രദര്_ശനം {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int ലംബം_പദവി;

    public പ്രതീകം_പ്രദര്_ശനം() {
        മായ്ക്കുക_എന്_ട്രി();
    }

    public void ഫലം(String ഉള്ളടക്കം_മൂല്യം) {
        for (int സൂചിക = 0; സൂചിക < ഉള്ളടക്കം_മൂല്യം.length(); സൂചിക++) {
            char 문자 = ഉള്ളടക്കം_മൂല്യം.charAt(സൂചിക);
            if (문자 == '\n') {
                가로 = 0;
                ലംബം_പദവി++;
            } else {
                문자출력(가로++, ലംബം_പദവി, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                ലംബം_പദവി++;
            }
            if (ലംബം_പദവി >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int ലംബം_പദവി) {
        പരിശോധിക്കുക_പദവി(가로, ലംബം_പദവി);
        return 문자들[ലംബം_പദവി * 너비 + 가로];
    }

    public void മായ്ക്കുക_എന്_ട്രി() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        ലംബം_പദവി = 0;
    }

    private void 문자출력(int 가로, int ലംബം_പദവി, char 문자) {
        പരിശോധിക്കുക_പദവി(가로, ലംബം_പദവി);
        문자들[ലംബം_പദവി * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        ലംബം_പദവി = 높이 - 1;
    }

    private void പരിശോധിക്കുക_പദവി(int 가로, int ലംബം_പദവി) {
        if (가로 < 0 || 가로 >= 너비 || ലംബം_പദവി < 0 || ലംബം_പദവി >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

