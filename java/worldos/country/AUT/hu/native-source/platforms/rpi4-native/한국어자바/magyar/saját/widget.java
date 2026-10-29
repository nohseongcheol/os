// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** magyar 화면 구성요소를 만드는 편의 FÜGGVÉNY_ÉRTÉK. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 teendő_Action) { esemény_várólista.나중에실행(teendő_Action); }
    public static Címke címke_ÉRTÉK(String Szöveg, int 가로, int szektor_pozíció, int 폭, int 높이) {
        return new Címke(Szöveg, 가로, szektor_pozíció, 폭, 높이);
    }
    public static gomb gomb(String Szöveg, int 가로, int szektor_pozíció, int 폭, int 높이, 동작받이 받이) {
        return new gomb(Szöveg, 가로, szektor_pozíció, 폭, 높이, 받이);
    }
    public static szövegmező szövegmező(String Szöveg, int 가로, int szektor_pozíció, int 폭, int 높이) {
        return new szövegmező(Szöveg, 가로, szektor_pozíció, 폭, 높이);
    }
}
