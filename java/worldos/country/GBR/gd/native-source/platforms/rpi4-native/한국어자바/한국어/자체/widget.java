// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 saothair_gnìomh) { tachartas_ciutha.나중에실행(saothair_gnìomh); }
    public static bileag taga_VALUE(String SMS, int 가로, int inghearach_suidhich, int 폭, int 높이) {
        return new bileag(SMS, 가로, inghearach_suidhich, 폭, 높이);
    }
    public static putan putan(String SMS, int 가로, int inghearach_suidhich, int 폭, int 높이, 동작받이 받이) {
        return new putan(SMS, 가로, inghearach_suidhich, 폭, 높이, 받이);
    }
    public static raon_teacsa raon_teacsa(String SMS, int 가로, int inghearach_suidhich, int 폭, int 높이) {
        return new raon_teacsa(SMS, 가로, inghearach_suidhich, 폭, 높이);
    }
}
