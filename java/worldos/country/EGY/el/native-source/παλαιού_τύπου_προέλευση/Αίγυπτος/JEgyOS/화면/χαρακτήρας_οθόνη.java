// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Αίγυπτος.JEgyOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class χαρακτήρας_οθόνη {
    public static final int 너비 = 80;
    public static final int ύψος_τιμή = 25;
    private final char[] 문자들 = new char[너비 * ύψος_τιμή];
    private int 가로;
    private int τομέας_θέση;

    public χαρακτήρας_οθόνη() {
        διαγράφω_καταχώρηση();
    }

    public void Έξοδος(String Περιεχόμενο_τιμή) {
        for (int Ευρετήριο = 0; Ευρετήριο < Περιεχόμενο_τιμή.length(); Ευρετήριο++) {
            char 문자 = Περιεχόμενο_τιμή.charAt(Ευρετήριο);
            if (문자 == '\n') {
                가로 = 0;
                τομέας_θέση++;
            } else {
                εκτυπώνω_χαρακτήρας(가로++, τομέας_θέση, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                τομέας_θέση++;
            }
            if (τομέας_θέση >= ύψος_τιμή) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int τομέας_θέση) {
        επαληθεύω_θέση(가로, τομέας_θέση);
        return 문자들[τομέας_θέση * 너비 + 가로];
    }

    public void διαγράφω_καταχώρηση() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        τομέας_θέση = 0;
    }

    private void εκτυπώνω_χαρακτήρας(int 가로, int τομέας_θέση, char 문자) {
        επαληθεύω_θέση(가로, τομέας_θέση);
        문자들[τομέας_θέση * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (ύψος_τιμή - 1));
        Arrays.fill(문자들, 너비 * (ύψος_τιμή - 1), 문자들.length, ' ');
        τομέας_θέση = ύψος_τιμή - 1;
    }

    private void επαληθεύω_θέση(int 가로, int τομέας_θέση) {
        if (가로 < 0 || 가로 >= 너비 || τομέας_θέση < 0 || τομέας_θέση >= ύψος_τιμή) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

