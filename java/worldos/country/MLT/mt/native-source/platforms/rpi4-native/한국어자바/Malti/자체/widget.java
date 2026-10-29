// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
/** Malti 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 attività_azzjoni) { avveniment_kju.나중에실행(attività_azzjoni); }
    public static tikketta tag_VALUE(String SMS, int 가로, int Vertikali_pożizzjoni, int 폭, int 높이) {
        return new tikketta(SMS, 가로, Vertikali_pożizzjoni, 폭, 높이);
    }
    public static buttuna buttuna(String SMS, int 가로, int Vertikali_pożizzjoni, int 폭, int 높이, 동작받이 받이) {
        return new buttuna(SMS, 가로, Vertikali_pożizzjoni, 폭, 높이, 받이);
    }
    public static qasam_ta_test qasam_ta_test(String SMS, int 가로, int Vertikali_pożizzjoni, int 폭, int 높이) {
        return new qasam_ta_test(SMS, 가로, Vertikali_pożizzjoni, 폭, 높이);
    }
}
