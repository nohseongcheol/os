// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 juɓɓol_njaru. */
public final class 화면요소 {
    private 화면요소() {}
    public static void 나중에실행(실행할일 golle_gollal) { saɗteende_lappol.나중에실행(golle_gollal); }
    public static tinndinoore hebtinirde_njaru(String binndi, int 가로, int 세로, int 폭, int 높이) {
        return new tinndinoore(binndi, 가로, 세로, 폭, 높이);
    }
    public static feɗoode feɗoode(String binndi, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new feɗoode(binndi, 가로, 세로, 폭, 높이, 받이);
    }
    public static binndi_suudu binndi_suudu(String binndi, int 가로, int 세로, int 폭, int 높이) {
        return new binndi_suudu(binndi, 가로, 세로, 폭, 높이);
    }
}
