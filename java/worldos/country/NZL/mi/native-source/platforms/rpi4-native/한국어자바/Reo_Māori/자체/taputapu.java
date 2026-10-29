// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
/** Reo_Māori 화면 구성요소를 만드는 편의 TAUMAHI_uara. */
public final class taputapu {
    private taputapu() {}
    public static void 나중에실행(실행할일 tūmahi_hohenga) { hui_tūtira.나중에실행(tūmahi_hohenga); }
    public static tapanga tūtohu_uara(String Ngā_kupu, int 가로, int Poutū_tūranga, int 폭, int 높이) {
        return new tapanga(Ngā_kupu, 가로, Poutū_tūranga, 폭, 높이);
    }
    public static pātene pātene(String Ngā_kupu, int 가로, int Poutū_tūranga, int 폭, int 높이, 동작받이 받이) {
        return new pātene(Ngā_kupu, 가로, Poutū_tūranga, 폭, 높이, 받이);
    }
    public static āpure_kuputuhi āpure_kuputuhi(String Ngā_kupu, int 가로, int Poutū_tūranga, int 폭, int 높이) {
        return new āpure_kuputuhi(Ngā_kupu, 가로, Poutū_tūranga, 폭, 높이);
    }
}
