// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
/** 작업 vlákno_VALUE: 하나의 Vykonať_príkaz Stream_VALUE. vlastné JVM 안에서 Príkaz 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Spustiť_2(실행할일 úloha_Akcia) { 작업가닥 vlákno_VALUE = new 작업가닥(úloha_Akcia); vlákno_VALUE.START_úloha(); return vlákno_VALUE; }
    public static void 기다리기(작업가닥 vlákno_VALUE) throws 대기중단예외 { vlákno_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 vlákno_VALUE) { return vlákno_VALUE.살아있는가(); }
    public static void YIELD_úloha() { 작업가닥.YIELD_úloha(); }
}
