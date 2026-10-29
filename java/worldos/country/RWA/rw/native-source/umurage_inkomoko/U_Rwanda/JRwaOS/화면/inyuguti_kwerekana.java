// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package U_Rwanda.JRwaOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class inyuguti_kwerekana {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int 세로;

    public inyuguti_kwerekana() {
        지우기();
    }

    public void 출력(String Ibirimo_agaciro) {
        for (int umugerekashakiro = 0; umugerekashakiro < Ibirimo_agaciro.length(); umugerekashakiro++) {
            char 문자 = Ibirimo_agaciro.charAt(umugerekashakiro);
            if (문자 == '\n') {
                가로 = 0;
                세로++;
            } else {
                문자출력(가로++, 세로, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                세로++;
            }
            if (세로 >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int 세로) {
        위치확인(가로, 세로);
        return 문자들[세로 * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        세로 = 0;
    }

    private void 문자출력(int 가로, int 세로, char 문자) {
        위치확인(가로, 세로);
        문자들[세로 * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        세로 = 높이 - 1;
    }

    private void 위치확인(int 가로, int 세로) {
        if (가로 < 0 || 가로 >= 너비 || 세로 < 0 || 세로 >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

