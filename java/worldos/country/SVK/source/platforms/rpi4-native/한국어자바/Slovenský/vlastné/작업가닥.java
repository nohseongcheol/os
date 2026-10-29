// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
/** vlastné JVM 스케줄러가 관리하는 Vykonať_príkaz Stream_VALUE. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 úloha_Akcia) {
        throw new Stav_výnimka("vlastné JVM의 Slovenský 작업 vlákno_VALUE generovať 기능이 필요합니다.");
    }
    public native void START_úloha() throws vlákno_Stav_výnimka;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_úloha();
}
