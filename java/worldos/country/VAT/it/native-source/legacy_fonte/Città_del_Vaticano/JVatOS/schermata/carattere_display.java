// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Città_del_Vaticano.JVatOS.schermata;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 schermata 모형이다. */
public final class carattere_display {
    public static final int 너비 = 80;
    public static final int altezza_VALORE = 25;
    private final char[] 문자들 = new char[너비 * altezza_VALORE];
    private int 가로;
    private int Verticale_funzione;

    public carattere_display() {
        cancellare_voce();
    }

    public void uscitaTesto(String Contenuto_VALORE) {
        for (int INDICE = 0; INDICE < Contenuto_VALORE.length(); INDICE++) {
            char 문자 = Contenuto_VALORE.charAt(INDICE);
            if (문자 == '\n') {
                가로 = 0;
                Verticale_funzione++;
            } else {
                stampare_carattere(가로++, Verticale_funzione, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Verticale_funzione++;
            }
            if (Verticale_funzione >= altezza_VALORE) {
                Scorri_verso_l_alto();
            }
        }
    }

    public char 문자(int 가로, int Verticale_funzione) {
        verificare_funzione(가로, Verticale_funzione);
        return 문자들[Verticale_funzione * 너비 + 가로];
    }

    public void cancellare_voce() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Verticale_funzione = 0;
    }

    private void stampare_carattere(int 가로, int Verticale_funzione, char 문자) {
        verificare_funzione(가로, Verticale_funzione);
        문자들[Verticale_funzione * 너비 + 가로] = 문자;
    }

    private void Scorri_verso_l_alto() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (altezza_VALORE - 1));
        Arrays.fill(문자들, 너비 * (altezza_VALORE - 1), 문자들.length, ' ');
        Verticale_funzione = altezza_VALORE - 1;
    }

    private void verificare_funzione(int 가로, int Verticale_funzione) {
        if (가로 < 0 || 가로 >= 너비 || Verticale_funzione < 0 || Verticale_funzione >= altezza_VALORE) {
            throw new IllegalArgumentException("schermata 위치가 올바르지 않습니다.");
        }
    }
}

