// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 فعل_قدر. */
public final class وجيٽ {
    private وجيٽ() {}
    public static void 나중에실행(실행할일 ٽاسڪ_عمل) { واقعو_قطار.나중에실행(ٽاسڪ_عمل); }
    public static پرچي ٽئگ_قدر(String متن, int 가로, int 세로, int 폭, int 높이) {
        return new پرچي(متن, 가로, 세로, 폭, 높이);
    }
    public static بٽن بٽن(String متن, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new بٽن(متن, 가로, 세로, 폭, 높이, 받이);
    }
    public static متن_فيلڊ متن_فيلڊ(String متن, int 가로, int 세로, int 폭, int 높이) {
        return new متن_فيلڊ(متن, 가로, 세로, 폭, 높이);
    }
}
