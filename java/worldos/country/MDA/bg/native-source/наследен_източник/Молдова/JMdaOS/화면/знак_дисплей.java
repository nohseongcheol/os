// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Молдова.JMdaOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class знак_дисплей {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int вертикал_позиция;

    public знак_дисплей() {
        изтривам_запис();
    }

    public void Изход(String Съдържание_стойност) {
        for (int индекс = 0; индекс < Съдържание_стойност.length(); индекс++) {
            char 문자 = Съдържание_стойност.charAt(индекс);
            if (문자 == '\n') {
                가로 = 0;
                вертикал_позиция++;
            } else {
                문자출력(가로++, вертикал_позиция, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                вертикал_позиция++;
            }
            if (вертикал_позиция >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int вертикал_позиция) {
        проверявам_позиция(가로, вертикал_позиция);
        return 문자들[вертикал_позиция * 너비 + 가로];
    }

    public void изтривам_запис() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        вертикал_позиция = 0;
    }

    private void 문자출력(int 가로, int вертикал_позиция, char 문자) {
        проверявам_позиция(가로, вертикал_позиция);
        문자들[вертикал_позиция * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        вертикал_позиция = 높이 - 1;
    }

    private void проверявам_позиция(int 가로, int вертикал_позиция) {
        if (가로 < 0 || 가로 >= 너비 || вертикал_позиция < 0 || вертикал_позиция >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

