// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class karakter_tampilan {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Vertikal_posisi;

    public karakter_tampilan() {
        hapus_entri_c8dbc399();
    }

    public void keluaranTeks(String Isi_VALUE) {
        for (int INDEX = 0; INDEX < Isi_VALUE.length(); INDEX++) {
            char 문자 = Isi_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Vertikal_posisi++;
            } else {
                cetak_karakter(가로++, Vertikal_posisi, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Vertikal_posisi++;
            }
            if (Vertikal_posisi >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Vertikal_posisi) {
        periksa_posisi(가로, Vertikal_posisi);
        return 문자들[Vertikal_posisi * 너비 + 가로];
    }

    public void hapus_entri_c8dbc399() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Vertikal_posisi = 0;
    }

    private void cetak_karakter(int 가로, int Vertikal_posisi, char 문자) {
        periksa_posisi(가로, Vertikal_posisi);
        문자들[Vertikal_posisi * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Vertikal_posisi = 높이 - 1;
    }

    private void periksa_posisi(int 가로, int Vertikal_posisi) {
        if (가로 < 0 || 가로 >= 너비 || Vertikal_posisi < 0 || Vertikal_posisi >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

