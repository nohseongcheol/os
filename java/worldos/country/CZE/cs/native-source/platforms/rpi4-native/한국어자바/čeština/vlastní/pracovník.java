// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
/** vlastní JVM 스케줄러가 관리하는 Provést_příkaz tok_HODNOTA. 표준 Thread를 감싸지 않는다. */
public final class pracovník {
    public pracovník(실행할일 úkol_Akce) {
        throw new Stav_výjimka("vlastní JVM의 čeština 작업 vlákno_HODNOTA generovat 기능이 필요합니다.");
    }
    public native void START_úkol() throws vlákno_Stav_výjimka;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_úkol();
}
