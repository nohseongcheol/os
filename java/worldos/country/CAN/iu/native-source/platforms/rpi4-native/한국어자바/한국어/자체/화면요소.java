// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 sugiakkannirut_atuutilik. */
public final class 화면요소 {
    private 화면요소() {}
    public static void 나중에실행(실행할일 sujassaq_sugiarut) { piniku_utaqqivik.나중에실행(sujassaq_sugiarut); }
    public static nalunairli nalunaikkutaq_atuutilik(String titiqqaq, int 가로, int 세로, int 폭, int 높이) {
        return new nalunairli(titiqqaq, 가로, 세로, 폭, 높이);
    }
    public static tikkuagaq tikkuagaq(String titiqqaq, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new tikkuagaq(titiqqaq, 가로, 세로, 폭, 높이, 받이);
    }
    public static titiqqaq_kisumuungavik titiqqaq_kisumuungavik(String titiqqaq, int 가로, int 세로, int 폭, int 높이) {
        return new titiqqaq_kisumuungavik(titiqqaq, 가로, 세로, 폭, 높이);
    }
}
