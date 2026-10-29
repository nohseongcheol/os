// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
/** eget JVM 스케줄러가 관리하는 Udfør_kommando strøm_VÆRDI. 표준 Thread를 감싸지 않는다. */
public final class arbejder {
    public arbejder(실행할일 job_To_do) {
        throw new status_undtagelse("eget JVM의 Dansk 작업 tråd_VÆRDI generere 기능이 필요합니다.");
    }
    public native void START_job() throws tråd_status_undtagelse;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void AFKAST_job();
}
