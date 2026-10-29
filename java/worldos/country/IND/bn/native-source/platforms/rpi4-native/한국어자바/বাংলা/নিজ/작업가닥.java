// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
/** নিজ JVM 스케줄러가 관리하는 কার্যকর_করুন_আদেশ প্রবাহ_মান. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 কার্য_কর্ম) {
        throw new অবস্হা_ব্যতিক্রম("নিজ JVM의 বাংলা 작업 থ্রেড_মান সৃষ্টি_করুন 기능이 필요합니다.");
    }
    public native void শুরু_কার্য() throws থ্রেড_অবস্হা_ব্যতিক্রম;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void স্থগিত_করুন_কার্য();
}
