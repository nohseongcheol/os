// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
/** اپنا JVM과 커널의 ونڈو 관리 기능에 직접 연결되는 ونڈو. */
public final class ونڈو extends 화면구성요소 {
    public ونڈو(String دریچہ_عنوان, int 폭, int 높이) {
        throw new حالت_استثنا("اپنا JVM의 اردو ونڈو تخلیق_کرنا 기능이 필요합니다.");
    }
    public native void شامل_کریں_عنصر(화면구성요소 عنصر_قدر);
    public native void دکھانا_دریچہ();
    public native void بند_کریں();
    public native boolean 보이는가();
}
