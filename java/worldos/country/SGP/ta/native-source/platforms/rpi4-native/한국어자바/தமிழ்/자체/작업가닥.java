// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
/** 자체 JVM 스케줄러가 관리하는 இயக்கு_கட்டளை தொடரோடி_மதிப்பு. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 பணி_செயல்) {
        throw new நிலை_விதிவிலக்கு("자체 JVM의 தமிழ் 작업 தொடரிழை_மதிப்பு உருவாக்குக 기능이 필요합니다.");
    }
    public native void தொடங்கு_பணி() throws தொடரிழை_நிலை_விதிவிலக்கு;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void இடைநீக்கம்_செய்யப்பட்டது_பணி();
}
