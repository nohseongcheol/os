// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
/** Slovenský 화면 구성요소를 만드는 편의 funkcia_VALUE. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 úloha_Akcia) { udalosť_front.나중에실행(úloha_Akcia); }
    public static Nápis značka_VALUE(String Spracovanie_textu, int 가로, int vertikála_pozícia, int 폭, int výška_VALUE) {
        return new Nápis(Spracovanie_textu, 가로, vertikála_pozícia, 폭, výška_VALUE);
    }
    public static Tlačidlo Tlačidlo(String Spracovanie_textu, int 가로, int vertikála_pozícia, int 폭, int výška_VALUE, 동작받이 받이) {
        return new Tlačidlo(Spracovanie_textu, 가로, vertikála_pozícia, 폭, výška_VALUE, 받이);
    }
    public static textové_pole textové_pole(String Spracovanie_textu, int 가로, int vertikála_pozícia, int 폭, int výška_VALUE) {
        return new textové_pole(Spracovanie_textu, 가로, vertikála_pozícia, 폭, výška_VALUE);
    }
}
