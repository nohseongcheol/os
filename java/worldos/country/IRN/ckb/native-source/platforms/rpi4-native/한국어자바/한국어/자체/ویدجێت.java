// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 کردار_نرخ. */
public final class ویدجێت {
    private ویدجێت() {}
    public static void 나중에실행(실행할일 ئەرک_ئاکشن) { پێشهات_ڕیز.나중에실행(ئەرک_ئاکشن); }
    public static نیشانە نیشان_نرخ(String دەق, int 가로, int 세로, int 폭, int 높이) {
        return new نیشانە(دەق, 가로, 세로, 폭, 높이);
    }
    public static دوگمه دوگمه(String دەق, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new دوگمه(دەق, 가로, 세로, 폭, 높이, 받이);
    }
    public static دەق_خانە دەق_خانە(String دەق, int 가로, int 세로, int 폭, int 높이) {
        return new دەق_خانە(دەق, 가로, 세로, 폭, 높이);
    }
}
