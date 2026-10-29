// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
/** čeština 화면 구성요소를 만드는 편의 funkce_HODNOTA. */
public final class prvek_obrazovky {
    private prvek_obrazovky() {}
    public static void 나중에실행(실행할일 úkol_Akce) { událost_fronta.나중에실행(úkol_Akce); }
    public static Popisek značka_HODNOTA(String text, int 가로, int Svislá_pozice, int 폭, int výška_HODNOTA) {
        return new Popisek(text, 가로, Svislá_pozice, 폭, výška_HODNOTA);
    }
    public static tlačítko tlačítko(String text, int 가로, int Svislá_pozice, int 폭, int výška_HODNOTA, 동작받이 받이) {
        return new tlačítko(text, 가로, Svislá_pozice, 폭, výška_HODNOTA, 받이);
    }
    public static textové_pole textové_pole(String text, int 가로, int Svislá_pozice, int 폭, int výška_HODNOTA) {
        return new textové_pole(text, 가로, Svislá_pozice, 폭, výška_HODNOTA);
    }
}
