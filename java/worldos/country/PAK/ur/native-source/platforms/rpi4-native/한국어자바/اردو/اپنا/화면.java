// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
/** 화면(畫面): 부팅 때 선택한 크기의 اپنا کرنیل_قدر RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int قدر = کرنیل_قدر.화면너비(); if (قدر < 0) throw new حالت_استثنا("프레임버퍼 없음"); return قدر; }
    public static int 높이() { int قدر = کرنیل_قدر.화면높이(); if (قدر < 0) throw new حالت_استثنا("프레임버퍼 없음"); return قدر; }
    public static void 사각형(int 가로, int عمودی_پوزیشن_ٹھیک_کریں, int 폭, int 높이, int 색) {
        if (가로 < 0 || عمودی_پوزیشن_ٹھیک_کریں < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || عمودی_پوزیشن_ٹھیک_کریں > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - عمودی_پوزیشن_ٹھیک_کریں) throw new بے_جواز_دلائل_استثنا("화면 تراشہ");
        if (کرنیل_قدر.사각형(가로, عمودی_پوزیشن_ٹھیک_کریں, 폭, 높이, 색) < 0) throw new حالت_استثنا("프레임버퍼 없음");
    }
    public static void 지우기(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (کرنیل_قدر.그림대기() < 0) throw new حالت_استثنا("متعامل 입력 필요"); }
}
