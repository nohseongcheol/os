// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class vidžet {
    private vidžet() {}
    public static void 나중에실행(실행할일 obaveza_radnja) { događaj_red.나중에실행(obaveza_radnja); }
    public static oznaka oznaka_VALUE(String SMS, int 가로, int vertikala_pozicija, int 폭, int 높이) {
        return new oznaka(SMS, 가로, vertikala_pozicija, 폭, 높이);
    }
    public static taster taster(String SMS, int 가로, int vertikala_pozicija, int 폭, int 높이, 동작받이 받이) {
        return new taster(SMS, 가로, vertikala_pozicija, 폭, 높이, 받이);
    }
    public static tekstualno_polje tekstualno_polje(String SMS, int 가로, int vertikala_pozicija, int 폭, int 높이) {
        return new tekstualno_polje(SMS, 가로, vertikala_pozicija, 폭, 높이);
    }
}
