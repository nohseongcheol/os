// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.JIdnOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class aksara_papar {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Menegak_jawatan;

    public aksara_papar() {
        padam_pemasukan();
    }

    public void 출력(String Kandungan_VALUE) {
        for (int INDEX = 0; INDEX < Kandungan_VALUE.length(); INDEX++) {
            char 문자 = Kandungan_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Menegak_jawatan++;
            } else {
                문자출력(가로++, Menegak_jawatan, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Menegak_jawatan++;
            }
            if (Menegak_jawatan >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Menegak_jawatan) {
        tentu_sahkan_jawatan(가로, Menegak_jawatan);
        return 문자들[Menegak_jawatan * 너비 + 가로];
    }

    public void padam_pemasukan() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Menegak_jawatan = 0;
    }

    private void 문자출력(int 가로, int Menegak_jawatan, char 문자) {
        tentu_sahkan_jawatan(가로, Menegak_jawatan);
        문자들[Menegak_jawatan * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Menegak_jawatan = 높이 - 1;
    }

    private void tentu_sahkan_jawatan(int 가로, int Menegak_jawatan) {
        if (가로 < 0 || 가로 >= 너비 || Menegak_jawatan < 0 || Menegak_jawatan >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

