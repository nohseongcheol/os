// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
/** 작업 snáithe_VALUE: 하나의 Rith_ordú sruth_VALUE. 자체 JVM 안에서 Ordú 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Rith_2(실행할일 tasc_gníomh) { 작업가닥 snáithe_VALUE = new 작업가닥(tasc_gníomh); snáithe_VALUE.Start_tasc(); return snáithe_VALUE; }
    public static void 기다리기(작업가닥 snáithe_VALUE) throws 대기중단예외 { snáithe_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 snáithe_VALUE) { return snáithe_VALUE.살아있는가(); }
    public static void YIELD_tasc() { 작업가닥.YIELD_tasc(); }
}
