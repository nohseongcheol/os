// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
/** اردو 화면 구성요소를 만드는 편의 فعل_قدر. */
public final class ویجٹ {
    private ویجٹ() {}
    public static void 나중에실행(실행할일 ٹاسک_عمل) { ایونٹ_قطار.나중에실행(ٹاسک_عمل); }
    public static سرنامہ ٹیگ_قدر(String متن, int 가로, int عمودی_پوزیشن_ٹھیک_کریں, int 폭, int 높이) {
        return new سرنامہ(متن, 가로, عمودی_پوزیشن_ٹھیک_کریں, 폭, 높이);
    }
    public static بٹن بٹن(String متن, int 가로, int عمودی_پوزیشن_ٹھیک_کریں, int 폭, int 높이, 동작받이 받이) {
        return new بٹن(متن, 가로, عمودی_پوزیشن_ٹھیک_کریں, 폭, 높이, 받이);
    }
    public static متن_فیلڈ متن_فیلڈ(String متن, int 가로, int عمودی_پوزیشن_ٹھیک_کریں, int 폭, int 높이) {
        return new متن_فیلڈ(متن, 가로, عمودی_پوزیشن_ٹھیک_کریں, 폭, 높이);
    }
}
