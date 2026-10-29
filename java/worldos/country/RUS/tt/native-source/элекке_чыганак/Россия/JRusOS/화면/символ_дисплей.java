// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class символ_дисплей {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Вертикаль_урнаштыру;

    public символ_дисплей() {
        지우기();
    }

    public void 출력(String Эчтәлек_VALUE) {
        for (int INDEX = 0; INDEX < Эчтәлек_VALUE.length(); INDEX++) {
            char 문자 = Эчтәлек_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Вертикаль_урнаштыру++;
            } else {
                문자출력(가로++, Вертикаль_урнаштыру, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Вертикаль_урнаштыру++;
            }
            if (Вертикаль_урнаштыру >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Вертикаль_урнаштыру) {
        раслау_урнаштыру(가로, Вертикаль_урнаштыру);
        return 문자들[Вертикаль_урнаштыру * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Вертикаль_урнаштыру = 0;
    }

    private void 문자출력(int 가로, int Вертикаль_урнаштыру, char 문자) {
        раслау_урнаштыру(가로, Вертикаль_урнаштыру);
        문자들[Вертикаль_урнаштыру * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Вертикаль_урнаштыру = 높이 - 1;
    }

    private void раслау_урнаштыру(int 가로, int Вертикаль_урнаштыру) {
        if (가로 < 0 || 가로 >= 너비 || Вертикаль_урнаштыру < 0 || Вертикаль_урнаштыру >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

