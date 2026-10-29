// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украина.JUkrOS.экран;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 экран 모형이다. */
public final class знак_дисплей {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Вертикаль_позиция;

    public знак_дисплей() {
        удалить_ввод_c8dbc399();
    }

    public void текстовыйВывод(String контент_ЗНАЧЕН) {
        for (int ИНДЕКС = 0; ИНДЕКС < контент_ЗНАЧЕН.length(); ИНДЕКС++) {
            char 문자 = контент_ЗНАЧЕН.charAt(ИНДЕКС);
            if (문자 == '\n') {
                가로 = 0;
                Вертикаль_позиция++;
            } else {
                печатать_знак(가로++, Вертикаль_позиция, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Вертикаль_позиция++;
            }
            if (Вертикаль_позиция >= 높이) {
                Scroll_up();
            }
        }
    }

    public char 문자(int 가로, int Вертикаль_позиция) {
        проверять_позиция(가로, Вертикаль_позиция);
        return 문자들[Вертикаль_позиция * 너비 + 가로];
    }

    public void удалить_ввод_c8dbc399() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Вертикаль_позиция = 0;
    }

    private void печатать_знак(int 가로, int Вертикаль_позиция, char 문자) {
        проверять_позиция(가로, Вертикаль_позиция);
        문자들[Вертикаль_позиция * 너비 + 가로] = 문자;
    }

    private void Scroll_up() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Вертикаль_позиция = 높이 - 1;
    }

    private void проверять_позиция(int 가로, int Вертикаль_позиция) {
        if (가로 < 0 || 가로 >= 너비 || Вертикаль_позиция < 0 || Вертикаль_позиция >= 높이) {
            throw new IllegalArgumentException("экран 위치가 올바르지 않습니다.");
        }
    }
}

