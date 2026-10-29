// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
/** slovenščina 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class pripomoček {
    private pripomoček() {}
    public static void 나중에실행(실행할일 opravek_akcija) { dogodek_čakalna_vrsta.나중에실행(opravek_akcija); }
    public static Oznaka oznaka_VALUE(String Besedilo, int 가로, int Navpično_položaj, int 폭, int višina_VALUE) {
        return new Oznaka(Besedilo, 가로, Navpično_položaj, 폭, višina_VALUE);
    }
    public static Gumb Gumb(String Besedilo, int 가로, int Navpično_položaj, int 폭, int višina_VALUE, 동작받이 받이) {
        return new Gumb(Besedilo, 가로, Navpično_položaj, 폭, višina_VALUE, 받이);
    }
    public static SMS_polje SMS_polje(String Besedilo, int 가로, int Navpično_položaj, int 폭, int višina_VALUE) {
        return new SMS_polje(Besedilo, 가로, Navpično_položaj, 폭, višina_VALUE);
    }
}
