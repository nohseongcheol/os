// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
/** eget JVM 스케줄러가 관리하는 Utfør_kommando strøm_VERDI. 표준 Thread를 감싸지 않는다. */
public final class arbeider {
    public arbeider(실행할일 oppgave_Gjøremål) {
        throw new status_unntak("eget JVM의 norsk 작업 tråd_VERDI generere 기능이 필요합니다.");
    }
    public native void START_oppgave() throws tråd_status_unntak;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void AVKAST_oppgave();
}
