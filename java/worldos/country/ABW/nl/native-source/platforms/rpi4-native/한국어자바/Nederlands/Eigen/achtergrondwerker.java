// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** Eigen JVM 스케줄러가 관리하는 Uitvoeren_opdracht Stream_WAARDE. 표준 Thread를 감싸지 않는다. */
public final class achtergrondwerker {
    public achtergrondwerker(실행할일 taak_Actie) {
        throw new Status_uitzondering("Eigen JVM의 Nederlands 작업 thread_WAARDE genereren 기능이 필요합니다.");
    }
    public native void START_taak() throws thread_Status_uitzondering;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void RENDEMENT_taak();
}
