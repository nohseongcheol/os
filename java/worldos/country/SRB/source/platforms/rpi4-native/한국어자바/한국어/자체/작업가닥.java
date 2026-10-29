// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM 스케줄러가 관리하는 Изврши_команда ток_вриједност. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 задатак_радња) {
        throw new стање_изузетак("자체 JVM의 한국어 작업 нит_вриједност генерисати 기능이 필요합니다.");
    }
    public native void Старт_задатак() throws нит_стање_изузетак;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void обуставити_задатак();
}
