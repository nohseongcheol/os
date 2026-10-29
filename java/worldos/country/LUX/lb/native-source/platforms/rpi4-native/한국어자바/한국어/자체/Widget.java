// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class Widget {
    private Widget() {}
    public static void 나중에실행(실행할일 To_do_Aktioun) { Evenement_Schlaang.나중에실행(To_do_Aktioun); }
    public static Numm_5ce2bd6f Tag_VALUE(String SMS, int 가로, int Vertikal_positionéieren, int 폭, int 높이) {
        return new Numm_5ce2bd6f(SMS, 가로, Vertikal_positionéieren, 폭, 높이);
    }
    public static Tast Tast(String SMS, int 가로, int Vertikal_positionéieren, int 폭, int 높이, 동작받이 받이) {
        return new Tast(SMS, 가로, Vertikal_positionéieren, 폭, 높이, 받이);
    }
    public static Textfeld Textfeld(String SMS, int 가로, int Vertikal_positionéieren, int 폭, int 높이) {
        return new Textfeld(SMS, 가로, Vertikal_positionéieren, 폭, 높이);
    }
}
