// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 আঁহ_মান: 하나의 নিষ্পাদন_আদেশ ষ্ট্ৰিম_মান. 자체 JVM 안에서 কমান্ড 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 সঞ্চালন(실행할일 কার্য্য_কাৰ্য) { 작업가닥 আঁহ_মান = new 작업가닥(কার্য্য_কাৰ্য); আঁহ_মান.আৰম্ভ_কার্য্য(); return আঁহ_মান; }
    public static void 기다리기(작업가닥 আঁহ_মান) throws 대기중단예외 { আঁহ_মান.기다리기(); }
    public static boolean 살아있는가(작업가닥 আঁহ_মান) { return আঁহ_মান.살아있는가(); }
    public static void নিলম্বিত_কার্য্য() { 작업가닥.নিলম্বিত_কার্য্য(); }
}
