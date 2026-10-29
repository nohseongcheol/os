// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class karaktere_pantaila {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Bertikala_kargu;

    public karaktere_pantaila() {
        ezabatu_sarrera();
    }

    public void Irteera(String eduki_balio) {
        for (int INDIZE = 0; INDIZE < eduki_balio.length(); INDIZE++) {
            char 문자 = eduki_balio.charAt(INDIZE);
            if (문자 == '\n') {
                가로 = 0;
                Bertikala_kargu++;
            } else {
                inprimatu_karaktere(가로++, Bertikala_kargu, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Bertikala_kargu++;
            }
            if (Bertikala_kargu >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Bertikala_kargu) {
        egiaztatu_kargu(가로, Bertikala_kargu);
        return 문자들[Bertikala_kargu * 너비 + 가로];
    }

    public void ezabatu_sarrera() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Bertikala_kargu = 0;
    }

    private void inprimatu_karaktere(int 가로, int Bertikala_kargu, char 문자) {
        egiaztatu_kargu(가로, Bertikala_kargu);
        문자들[Bertikala_kargu * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Bertikala_kargu = 높이 - 1;
    }

    private void egiaztatu_kargu(int 가로, int Bertikala_kargu) {
        if (가로 < 0 || 가로 >= 너비 || Bertikala_kargu < 0 || Bertikala_kargu >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

