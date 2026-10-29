// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class vidžet {
    private vidžet() {}
    public static void 나중에실행(실행할일 zadatak_radnja) { događaj_redoslijed.나중에실행(zadatak_radnja); }
    public static Oznaka oznaka_VALUE(String Tekst, int 가로, int Vertikalno_položaj, int 폭, int 높이) {
        return new Oznaka(Tekst, 가로, Vertikalno_položaj, 폭, 높이);
    }
    public static dugme dugme(String Tekst, int 가로, int Vertikalno_položaj, int 폭, int 높이, 동작받이 받이) {
        return new dugme(Tekst, 가로, Vertikalno_položaj, 폭, 높이, 받이);
    }
    public static SMS_polje SMS_polje(String Tekst, int 가로, int Vertikalno_položaj, int 폭, int 높이) {
        return new SMS_polje(Tekst, 가로, Vertikalno_položaj, 폭, 높이);
    }
}
