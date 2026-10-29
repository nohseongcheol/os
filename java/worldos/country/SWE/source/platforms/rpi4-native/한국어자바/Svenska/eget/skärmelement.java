// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
/** Svenska skärmbild 구성요소를 만드는 편의 FUNKTION_värde. */
public final class skärmelement {
    private skärmelement() {}
    public static void 나중에실행(실행할일 uppgift_Action) { händelse_kö.나중에실행(uppgift_Action); }
    public static Etikett tagg_värde(String text, int 가로, int bransch_placera, int 폭, int 높이) {
        return new Etikett(text, 가로, bransch_placera, 폭, 높이);
    }
    public static knapp knapp(String text, int 가로, int bransch_placera, int 폭, int 높이, 동작받이 받이) {
        return new knapp(text, 가로, bransch_placera, 폭, 높이, 받이);
    }
    public static textfält textfält(String text, int 가로, int bransch_placera, int 폭, int 높이) {
        return new textfält(text, 가로, bransch_placera, 폭, 높이);
    }
}
