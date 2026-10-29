// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
/** hrvatski 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 obaveza_akcija) { događaj_red_čekanja.나중에실행(obaveza_akcija); }
    public static Natpis oznaka_VALUE(String Tekst, int 가로, int Okomito_položaj, int 폭, int 높이) {
        return new Natpis(Tekst, 가로, Okomito_položaj, 폭, 높이);
    }
    public static gumb gumb(String Tekst, int 가로, int Okomito_položaj, int 폭, int 높이, 동작받이 받이) {
        return new gumb(Tekst, 가로, Okomito_položaj, 폭, 높이, 받이);
    }
    public static tekstno_polje tekstno_polje(String Tekst, int 가로, int Okomito_položaj, int 폭, int 높이) {
        return new tekstno_polje(Tekst, 가로, Okomito_položaj, 폭, 높이);
    }
}
