// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
/** 작업 থ্রেড_মান: 하나의 কার্যকর_করুন_আদেশ প্রবাহ_মান. নিজ JVM 안에서 আদেশ 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 চালনা(실행할일 কার্য_কর্ম) { 작업가닥 থ্রেড_মান = new 작업가닥(কার্য_কর্ম); থ্রেড_মান.শুরু_কার্য(); return থ্রেড_মান; }
    public static void 기다리기(작업가닥 থ্রেড_মান) throws 대기중단예외 { থ্রেড_মান.기다리기(); }
    public static boolean 살아있는가(작업가닥 থ্রেড_মান) { return থ্রেড_মান.살아있는가(); }
    public static void স্থগিত_করুন_কার্য() { 작업가닥.স্থগিত_করুন_কার্য(); }
}
