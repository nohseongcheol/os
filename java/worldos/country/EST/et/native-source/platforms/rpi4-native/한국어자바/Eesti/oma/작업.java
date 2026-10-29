// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
/** 작업 lõim_VALUE: 하나의 Täida_käsk voog_VALUE. oma JVM 안에서 Käsk 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static töötaja Käivita_2(실행할일 tööüksus_Toiming) { töötaja lõim_VALUE = new töötaja(tööüksus_Toiming); lõim_VALUE.START_tööüksus(); return lõim_VALUE; }
    public static void 기다리기(töötaja lõim_VALUE) throws 대기중단예외 { lõim_VALUE.기다리기(); }
    public static boolean 살아있는가(töötaja lõim_VALUE) { return lõim_VALUE.살아있는가(); }
    public static void YIELD_tööüksus() { töötaja.YIELD_tööüksus(); }
}
