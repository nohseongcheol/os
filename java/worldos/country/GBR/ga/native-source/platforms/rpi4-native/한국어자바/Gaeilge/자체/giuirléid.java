// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
/** Gaeilge 화면 구성요소를 만드는 편의 feidhm_VALUE. */
public final class giuirléid {
    private giuirléid() {}
    public static void 나중에실행(실행할일 tasc_gníomh) { ócáid_scuaine.나중에실행(tasc_gníomh); }
    public static Lipéad clib_VALUE(String Téacs, int 가로, int Ingearach_suíomh, int 폭, int 높이) {
        return new Lipéad(Téacs, 가로, Ingearach_suíomh, 폭, 높이);
    }
    public static cnaipe cnaipe(String Téacs, int 가로, int Ingearach_suíomh, int 폭, int 높이, 동작받이 받이) {
        return new cnaipe(Téacs, 가로, Ingearach_suíomh, 폭, 높이, 받이);
    }
    public static réimse_téacs réimse_téacs(String Téacs, int 가로, int Ingearach_suíomh, int 폭, int 높이) {
        return new réimse_téacs(Téacs, 가로, Ingearach_suíomh, 폭, 높이);
    }
}
