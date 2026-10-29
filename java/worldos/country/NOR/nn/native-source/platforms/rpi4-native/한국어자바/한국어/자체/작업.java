// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 tråd_VALUE: 하나의 Utfør_kommando Stream_VALUE. 자체 JVM 안에서 Kommando 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Køyr_2(실행할일 oppgåve_handling) { 작업가닥 tråd_VALUE = new 작업가닥(oppgåve_handling); tråd_VALUE.START_oppgåve(); return tråd_VALUE; }
    public static void 기다리기(작업가닥 tråd_VALUE) throws 대기중단예외 { tråd_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 tråd_VALUE) { return tråd_VALUE.살아있는가(); }
    public static void YIELD_oppgåve() { 작업가닥.YIELD_oppgåve(); }
}
