// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
/** 작업 fir_VALUE: 하나의 executa_comandă flux_VALUE. propriu JVM 안에서 Comandă 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Pornește(실행할일 sarcină_Acțiune) { 작업가닥 fir_VALUE = new 작업가닥(sarcină_Acțiune); fir_VALUE.buta_sarcină(); return fir_VALUE; }
    public static void 기다리기(작업가닥 fir_VALUE) throws 대기중단예외 { fir_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 fir_VALUE) { return fir_VALUE.살아있는가(); }
    public static void YIELD_sarcină() { 작업가닥.YIELD_sarcină(); }
}
