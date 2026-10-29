// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkiya.JTurOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class belgi_ekran {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Vertikal_holat;

    public belgi_ekran() {
        tozalash_kiritish();
    }

    public void 출력(String tarkib_VALUE) {
        for (int INDEX = 0; INDEX < tarkib_VALUE.length(); INDEX++) {
            char 문자 = tarkib_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Vertikal_holat++;
            } else {
                문자출력(가로++, Vertikal_holat, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Vertikal_holat++;
            }
            if (Vertikal_holat >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Vertikal_holat) {
        tasdiqlamoq_holat(가로, Vertikal_holat);
        return 문자들[Vertikal_holat * 너비 + 가로];
    }

    public void tozalash_kiritish() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Vertikal_holat = 0;
    }

    private void 문자출력(int 가로, int Vertikal_holat, char 문자) {
        tasdiqlamoq_holat(가로, Vertikal_holat);
        문자들[Vertikal_holat * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Vertikal_holat = 높이 - 1;
    }

    private void tasdiqlamoq_holat(int 가로, int Vertikal_holat) {
        if (가로 < 0 || 가로 >= 너비 || Vertikal_holat < 0 || Vertikal_holat >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

