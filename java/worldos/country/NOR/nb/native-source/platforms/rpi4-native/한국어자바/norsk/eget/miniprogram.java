// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
/** norsk skjermbilde 구성요소를 만드는 편의 FUNKSJON_VERDI. */
public final class miniprogram {
    private miniprogram() {}
    public static void 나중에실행(실행할일 oppgave_Gjøremål) { hendelse_kø.나중에실행(oppgave_Gjøremål); }
    public static Etikett kode_VERDI(String Tekst, int 가로, int vertikal_plassere, int 폭, int 높이) {
        return new Etikett(Tekst, 가로, vertikal_plassere, 폭, 높이);
    }
    public static Knapp Knapp(String Tekst, int 가로, int vertikal_plassere, int 폭, int 높이, 동작받이 받이) {
        return new Knapp(Tekst, 가로, vertikal_plassere, 폭, 높이, 받이);
    }
    public static tekstfelt tekstfelt(String Tekst, int 가로, int vertikal_plassere, int 폭, int 높이) {
        return new tekstfelt(Tekst, 가로, vertikal_plassere, 폭, 높이);
    }
}
