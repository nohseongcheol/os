// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
/** eget JVM 스케줄러가 관리하는 köra_kommando flöde_värde. 표준 Thread를 감싸지 않는다. */
public final class arbete {
    public arbete(실행할일 uppgift_Action) {
        throw new status_fel("eget JVM의 Svenska 작업 tråd_värde generera 기능이 필요합니다.");
    }
    public native void START_uppgift() throws tråd_status_fel;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void NOMAVK_uppgift();
}
