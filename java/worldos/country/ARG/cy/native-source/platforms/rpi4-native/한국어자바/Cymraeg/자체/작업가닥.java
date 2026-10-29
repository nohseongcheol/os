// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
/** 자체 JVM 스케줄러가 관리하는 Gweithredu_gorchymyn ffrwd_VALUE. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 tasg_gweithred) {
        throw new cyflwr_eithriad("자체 JVM의 Cymraeg 작업 edefyn_VALUE cynhyrchu 기능이 필요합니다.");
    }
    public native void START_tasg() throws edefyn_cyflwr_eithriad;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void atal_tasg();
}
