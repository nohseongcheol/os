// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM 스케줄러가 관리하는 Utfør_kommando Stream_VALUE. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 oppgåve_handling) {
        throw new status_unntak("자체 JVM의 한국어 작업 tråd_VALUE generere 기능이 필요합니다.");
    }
    public native void START_oppgåve() throws tråd_status_unntak;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_oppgåve();
}
