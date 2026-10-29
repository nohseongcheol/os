// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class ቁምፊ_ማሳያ {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int ቋሚ_በቦታ_አስቀመጠ;

    public ቁምፊ_ማሳያ() {
        አስወግድ_ምዝግብ_c8dbc399();
    }

    public void ውጤት(String ይዘት_እሴት) {
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < ይዘት_እሴት.length(); መረጃ_ጠቆመ++) {
            char 문자 = ይዘት_እሴት.charAt(መረጃ_ጠቆመ);
            if (문자 == '\n') {
                가로 = 0;
                ቋሚ_በቦታ_አስቀመጠ++;
            } else {
                문자출력(가로++, ቋሚ_በቦታ_አስቀመጠ, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                ቋሚ_በቦታ_አስቀመጠ++;
            }
            if (ቋሚ_በቦታ_አስቀመጠ >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int ቋሚ_በቦታ_አስቀመጠ) {
        አረጋግጥ_በቦታ_አስቀመጠ(가로, ቋሚ_በቦታ_አስቀመጠ);
        return 문자들[ቋሚ_በቦታ_አስቀመጠ * 너비 + 가로];
    }

    public void አስወግድ_ምዝግብ_c8dbc399() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        ቋሚ_በቦታ_አስቀመጠ = 0;
    }

    private void 문자출력(int 가로, int ቋሚ_በቦታ_አስቀመጠ, char 문자) {
        አረጋግጥ_በቦታ_አስቀመጠ(가로, ቋሚ_በቦታ_አስቀመጠ);
        문자들[ቋሚ_በቦታ_አስቀመጠ * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        ቋሚ_በቦታ_አስቀመጠ = 높이 - 1;
    }

    private void አረጋግጥ_በቦታ_አስቀመጠ(int 가로, int ቋሚ_በቦታ_አስቀመጠ) {
        if (가로 < 0 || 가로 >= 너비 || ቋሚ_በቦታ_አስቀመጠ < 0 || ቋሚ_በቦታ_አስቀመጠ >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

