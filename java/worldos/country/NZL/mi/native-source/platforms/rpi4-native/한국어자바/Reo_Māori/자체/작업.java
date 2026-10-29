// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
/** 작업 miro_uara: 하나의 kawe_tono roma_uara. 자체 JVM 안에서 tono 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 whakahaere(실행할일 tūmahi_hohenga) { 작업가닥 miro_uara = new 작업가닥(tūmahi_hohenga); miro_uara.Start_tūmahi(); return miro_uara; }
    public static void 기다리기(작업가닥 miro_uara) throws 대기중단예외 { miro_uara.기다리기(); }
    public static boolean 살아있는가(작업가닥 miro_uara) { return miro_uara.살아있는가(); }
    public static void YIELD_tūmahi() { 작업가닥.YIELD_tūmahi(); }
}
