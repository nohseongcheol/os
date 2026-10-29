// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
/** اپنا JVM 스케줄러가 관리하는 نفاذ_کریں_حکم بہاؤ_قدر. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 ٹاسک_عمل) {
        throw new حالت_استثنا("اپنا JVM의 اردو 작업 تھریڈ_قدر تخلیق_کرنا 기능이 필요합니다.");
    }
    public native void ابتدا_ٹاسک() throws تھریڈ_حالت_استثنا;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void معطل_کریں_ٹاسک();
}
