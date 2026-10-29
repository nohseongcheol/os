// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 detyrë_veprim) { ngjarje_radhë.나중에실행(detyrë_veprim); }
    public static Etiketë shenjë_VALUE(String Teksti, int 가로, int Vertikal_pozicioni, int 폭, int 높이) {
        return new Etiketë(Teksti, 가로, Vertikal_pozicioni, 폭, 높이);
    }
    public static Buton Buton(String Teksti, int 가로, int Vertikal_pozicioni, int 폭, int 높이, 동작받이 받이) {
        return new Buton(Teksti, 가로, Vertikal_pozicioni, 폭, 높이, 받이);
    }
    public static SMS_fushë SMS_fushë(String Teksti, int 가로, int Vertikal_pozicioni, int 폭, int 높이) {
        return new SMS_fushë(Teksti, 가로, Vertikal_pozicioni, 폭, 높이);
    }
}
