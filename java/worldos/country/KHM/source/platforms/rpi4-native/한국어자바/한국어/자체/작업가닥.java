// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM 스케줄러가 관리하는 អនុវត្ត_ពាក្យបញ្ជា ស្ទ្រីម_តំលៃ. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 ធូឌូ_ការណែនាំ) {
        throw new ភាព_ការលើកលែង("자체 JVM의 한국어 작업 ស្រេត_តំលៃ បង្កើត 기능이 필요합니다.");
    }
    public native void ផ្តើម_ធូឌូ() throws ស្រេត_ភាព_ការលើកលែង;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void ផ្អាក_ធូឌូ();
}
