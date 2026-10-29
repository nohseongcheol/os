// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** Nederlands scherm 구성요소를 만드는 편의 FUNCTIE_WAARDE. */
public final class schermelement {
    private schermelement() {}
    public static void 나중에실행(실행할일 taak_Actie) { gebeurtenis_wachtrij.나중에실행(taak_Actie); }
    public static Etiket tag_WAARDE(String tekst, int 가로, int Verticaal_functie, int 폭, int hoogte_WAARDE) {
        return new Etiket(tekst, 가로, Verticaal_functie, 폭, hoogte_WAARDE);
    }
    public static knop knop(String tekst, int 가로, int Verticaal_functie, int 폭, int hoogte_WAARDE, 동작받이 받이) {
        return new knop(tekst, 가로, Verticaal_functie, 폭, hoogte_WAARDE, 받이);
    }
    public static tekstveld tekstveld(String tekst, int 가로, int Verticaal_functie, int 폭, int hoogte_WAARDE) {
        return new tekstveld(tekst, 가로, Verticaal_functie, 폭, hoogte_WAARDE);
    }
}
