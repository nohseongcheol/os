// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aruba.JAbwOS.scherm;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 scherm 모형이다. */
public final class teken_weergeven {
    public static final int 너비 = 80;
    public static final int hoogte_WAARDE = 25;
    private final char[] 문자들 = new char[너비 * hoogte_WAARDE];
    private int 가로;
    private int Verticaal_functie;

    public teken_weergeven() {
        wissen_invoer();
    }

    public void tekstuitvoer(String Inhoud_WAARDE) {
        for (int INDEX = 0; INDEX < Inhoud_WAARDE.length(); INDEX++) {
            char 문자 = Inhoud_WAARDE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Verticaal_functie++;
            } else {
                afdrukken_teken(가로++, Verticaal_functie, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Verticaal_functie++;
            }
            if (Verticaal_functie >= hoogte_WAARDE) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Verticaal_functie) {
        bevestigen_functie(가로, Verticaal_functie);
        return 문자들[Verticaal_functie * 너비 + 가로];
    }

    public void wissen_invoer() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Verticaal_functie = 0;
    }

    private void afdrukken_teken(int 가로, int Verticaal_functie, char 문자) {
        bevestigen_functie(가로, Verticaal_functie);
        문자들[Verticaal_functie * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (hoogte_WAARDE - 1));
        Arrays.fill(문자들, 너비 * (hoogte_WAARDE - 1), 문자들.length, ' ');
        Verticaal_functie = hoogte_WAARDE - 1;
    }

    private void bevestigen_functie(int 가로, int Verticaal_functie) {
        if (가로 < 0 || 가로 >= 너비 || Verticaal_functie < 0 || Verticaal_functie >= hoogte_WAARDE) {
            throw new IllegalArgumentException("scherm 위치가 올바르지 않습니다.");
        }
    }
}

