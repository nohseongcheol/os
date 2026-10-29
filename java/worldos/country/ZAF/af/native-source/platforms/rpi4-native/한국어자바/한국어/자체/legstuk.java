// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 funksie_VALUE. */
public final class legstuk {
    private legstuk() {}
    public static void 나중에실행(실행할일 taak_aksie) { gebeurtenis_tou.나중에실행(taak_aksie); }
    public static etiket merk_VALUE(String Teks, int 가로, int Vertikaal_plaas, int 폭, int 높이) {
        return new etiket(Teks, 가로, Vertikaal_plaas, 폭, 높이);
    }
    public static knoppie knoppie(String Teks, int 가로, int Vertikaal_plaas, int 폭, int 높이, 동작받이 받이) {
        return new knoppie(Teks, 가로, Vertikaal_plaas, 폭, 높이, 받이);
    }
    public static SMS_veld SMS_veld(String Teks, int 가로, int Vertikaal_plaas, int 폭, int 높이) {
        return new SMS_veld(Teks, 가로, Vertikaal_plaas, 폭, 높이);
    }
}
