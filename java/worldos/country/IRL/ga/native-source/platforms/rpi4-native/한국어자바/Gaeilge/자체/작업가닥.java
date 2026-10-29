// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
/** 자체 JVM 스케줄러가 관리하는 Rith_ordú sruth_VALUE. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 tasc_gníomh) {
        throw new staid_eisceacht("자체 JVM의 Gaeilge 작업 snáithe_VALUE giniúint 기능이 필요합니다.");
    }
    public native void Start_tasc() throws snáithe_staid_eisceacht;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_tasc();
}
