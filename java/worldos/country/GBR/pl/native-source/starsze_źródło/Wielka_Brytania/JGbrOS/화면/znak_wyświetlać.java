// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Wielka_Brytania.JGbrOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class znak_wyświetlać {
    public static final int 너비 = 80;
    public static final int wysokość_WARTOŚĆ = 25;
    private final char[] 문자들 = new char[너비 * wysokość_WARTOŚĆ];
    private int 가로;
    private int gałąź_stanowisko;

    public znak_wyświetlać() {
        usunąć_wpis();
    }

    public void pozycja_wyjścia(String treść_WARTOŚĆ_cb0f2404) {
        for (int INDEKS = 0; INDEKS < treść_WARTOŚĆ_cb0f2404.length(); INDEKS++) {
            char 문자 = treść_WARTOŚĆ_cb0f2404.charAt(INDEKS);
            if (문자 == '\n') {
                가로 = 0;
                gałąź_stanowisko++;
            } else {
                문자출력(가로++, gałąź_stanowisko, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                gałąź_stanowisko++;
            }
            if (gałąź_stanowisko >= wysokość_WARTOŚĆ) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int gałąź_stanowisko) {
        위치확인(가로, gałąź_stanowisko);
        return 문자들[gałąź_stanowisko * 너비 + 가로];
    }

    public void usunąć_wpis() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        gałąź_stanowisko = 0;
    }

    private void 문자출력(int 가로, int gałąź_stanowisko, char 문자) {
        위치확인(가로, gałąź_stanowisko);
        문자들[gałąź_stanowisko * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (wysokość_WARTOŚĆ - 1));
        Arrays.fill(문자들, 너비 * (wysokość_WARTOŚĆ - 1), 문자들.length, ' ');
        gałąź_stanowisko = wysokość_WARTOŚĆ - 1;
    }

    private void 위치확인(int 가로, int gałąź_stanowisko) {
        if (가로 < 0 || 가로 >= 너비 || gałąź_stanowisko < 0 || gałąź_stanowisko >= wysokość_WARTOŚĆ) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

