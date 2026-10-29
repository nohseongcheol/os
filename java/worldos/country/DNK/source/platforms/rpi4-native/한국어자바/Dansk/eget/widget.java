// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
/** Dansk skærmbillede 구성요소를 만드는 편의 FUNKTION_VÆRDI. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 job_To_do) { hændelse_kø.나중에실행(job_To_do); }
    public static Etiket tag_VÆRDI(String Tekst, int 가로, int Lodret_placere, int 폭, int 높이) {
        return new Etiket(Tekst, 가로, Lodret_placere, 폭, 높이);
    }
    public static knap knap(String Tekst, int 가로, int Lodret_placere, int 폭, int 높이, 동작받이 받이) {
        return new knap(Tekst, 가로, Lodret_placere, 폭, 높이, 받이);
    }
    public static tekstfelt tekstfelt(String Tekst, int 가로, int Lodret_placere, int 폭, int 높이) {
        return new tekstfelt(Tekst, 가로, Lodret_placere, 폭, 높이);
    }
}
