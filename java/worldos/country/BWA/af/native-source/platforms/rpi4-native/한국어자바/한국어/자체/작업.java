// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 draad_VALUE: 하나의 uitvoer_bevel Stream_VALUE. 자체 JVM 안에서 Opdrag 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Loop(실행할일 taak_aksie) { 작업가닥 draad_VALUE = new 작업가닥(taak_aksie); draad_VALUE.BEGIN_taak(); return draad_VALUE; }
    public static void 기다리기(작업가닥 draad_VALUE) throws 대기중단예외 { draad_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 draad_VALUE) { return draad_VALUE.살아있는가(); }
    public static void YIELD_taak() { 작업가닥.YIELD_taak(); }
}
