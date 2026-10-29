// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
/** oma JVM 스케줄러가 관리하는 Täida_käsk voog_VALUE. 표준 Thread를 감싸지 않는다. */
public final class töötaja {
    public töötaja(실행할일 tööüksus_Toiming) {
        throw new Olek_erand("oma JVM의 Eesti 작업 lõim_VALUE genereerima 기능이 필요합니다.");
    }
    public native void START_tööüksus() throws lõim_Olek_erand;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_tööüksus();
}
