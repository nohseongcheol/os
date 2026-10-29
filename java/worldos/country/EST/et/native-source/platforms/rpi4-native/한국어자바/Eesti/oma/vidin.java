// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
/** Eesti 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class vidin {
    private vidin() {}
    public static void 나중에실행(실행할일 tööüksus_Toiming) { sündmus_järjekord.나중에실행(tööüksus_Toiming); }
    public static Silt silt_VALUE(String Tekst, int 가로, int vertikaal_ametikoht, int 폭, int 높이) {
        return new Silt(Tekst, 가로, vertikaal_ametikoht, 폭, 높이);
    }
    public static nupp nupp(String Tekst, int 가로, int vertikaal_ametikoht, int 폭, int 높이, 동작받이 받이) {
        return new nupp(Tekst, 가로, vertikaal_ametikoht, 폭, 높이, 받이);
    }
    public static tekstiväli tekstiväli(String Tekst, int 가로, int vertikaal_ametikoht, int 폭, int 높이) {
        return new tekstiväli(Tekst, 가로, vertikaal_ametikoht, 폭, 높이);
    }
}
