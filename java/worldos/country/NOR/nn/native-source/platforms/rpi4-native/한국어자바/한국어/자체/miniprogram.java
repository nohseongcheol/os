// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class miniprogram {
    private miniprogram() {}
    public static void 나중에실행(실행할일 oppgåve_handling) { hending_kø.나중에실행(oppgåve_handling); }
    public static Etikett kode_VALUE(String Tekst, int 가로, int vertikalvising_plassere, int 폭, int 높이) {
        return new Etikett(Tekst, 가로, vertikalvising_plassere, 폭, 높이);
    }
    public static knapp knapp(String Tekst, int 가로, int vertikalvising_plassere, int 폭, int 높이, 동작받이 받이) {
        return new knapp(Tekst, 가로, vertikalvising_plassere, 폭, 높이, 받이);
    }
    public static SMS_felt SMS_felt(String Tekst, int 가로, int vertikalvising_plassere, int 폭, int 높이) {
        return new SMS_felt(Tekst, 가로, vertikalvising_plassere, 폭, 높이);
    }
}
