// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Сербія.JSrbOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class символ_дисплей {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Вертикаль_посада;

    public символ_дисплей() {
        видаляти_запис();
    }

    public void Вивід(String Вміст_значення) {
        for (int індекс = 0; індекс < Вміст_значення.length(); індекс++) {
            char 문자 = Вміст_значення.charAt(індекс);
            if (문자 == '\n') {
                가로 = 0;
                Вертикаль_посада++;
            } else {
                문자출력(가로++, Вертикаль_посада, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Вертикаль_посада++;
            }
            if (Вертикаль_посада >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Вертикаль_посада) {
        перевіряти_посада(가로, Вертикаль_посада);
        return 문자들[Вертикаль_посада * 너비 + 가로];
    }

    public void видаляти_запис() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Вертикаль_посада = 0;
    }

    private void 문자출력(int 가로, int Вертикаль_посада, char 문자) {
        перевіряти_посада(가로, Вертикаль_посада);
        문자들[Вертикаль_посада * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Вертикаль_посада = 높이 - 1;
    }

    private void перевіряти_посада(int 가로, int Вертикаль_посада) {
        if (가로 < 0 || 가로 >= 너비 || Вертикаль_посада < 0 || Вертикаль_посада >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

