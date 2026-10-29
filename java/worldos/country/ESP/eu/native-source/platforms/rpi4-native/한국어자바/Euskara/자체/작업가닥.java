// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
/** 자체 JVM 스케줄러가 관리하는 exekutatu_komando Stream_balio. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 ataza_ekintza) {
        throw new Egoera_salbuespen("자체 JVM의 Euskara 작업 hari_balio sortu 기능이 필요합니다.");
    }
    public native void HASI_ataza() throws hari_Egoera_salbuespen;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_ataza();
}
