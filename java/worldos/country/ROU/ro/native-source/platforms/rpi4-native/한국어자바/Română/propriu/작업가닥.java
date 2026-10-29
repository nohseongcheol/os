// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
/** propriu JVM 스케줄러가 관리하는 executa_comandă flux_VALUE. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 sarcină_Acțiune) {
        throw new Stare_excepție("propriu JVM의 Română 작업 fir_VALUE genera 기능이 필요합니다.");
    }
    public native void buta_sarcină() throws fir_Stare_excepție;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_sarcină();
}
