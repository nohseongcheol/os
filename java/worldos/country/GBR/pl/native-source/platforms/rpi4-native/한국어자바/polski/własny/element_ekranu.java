// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
/** polski 화면 구성요소를 만드는 편의 FUNKCJA_WARTOŚĆ. */
public final class element_ekranu {
    private element_ekranu() {}
    public static void 나중에실행(실행할일 zadanie_akcja) { konkurs_kolejka.나중에실행(zadanie_akcja); }
    public static Etykieta tag_WARTOŚĆ(String tekst, int 가로, int gałąź_stanowisko, int 폭, int wysokość_WARTOŚĆ) {
        return new Etykieta(tekst, 가로, gałąź_stanowisko, 폭, wysokość_WARTOŚĆ);
    }
    public static przycisk przycisk(String tekst, int 가로, int gałąź_stanowisko, int 폭, int wysokość_WARTOŚĆ, 동작받이 받이) {
        return new przycisk(tekst, 가로, gałąź_stanowisko, 폭, wysokość_WARTOŚĆ, 받이);
    }
    public static pole_tekstowe pole_tekstowe(String tekst, int 가로, int gałąź_stanowisko, int 폭, int wysokość_WARTOŚĆ) {
        return new pole_tekstowe(tekst, 가로, gałąź_stanowisko, 폭, wysokość_WARTOŚĆ);
    }
}
