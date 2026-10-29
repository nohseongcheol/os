// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
/** 작업 vlákno_HODNOTA: 하나의 Provést_příkaz tok_HODNOTA. vlastní JVM 안에서 příkaz 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static pracovník Spustit_2(실행할일 úkol_Akce) { pracovník vlákno_HODNOTA = new pracovník(úkol_Akce); vlákno_HODNOTA.START_úkol(); return vlákno_HODNOTA; }
    public static void 기다리기(pracovník vlákno_HODNOTA) throws 대기중단예외 { vlákno_HODNOTA.기다리기(); }
    public static boolean 살아있는가(pracovník vlákno_HODNOTA) { return vlákno_HODNOTA.살아있는가(); }
    public static void YIELD_úkol() { pracovník.YIELD_úkol(); }
}
