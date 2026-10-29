// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 Thread_VALUE: 하나의 ausféieren_Befeel Stream_VALUE. 자체 JVM 안에서 Befeel 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Laf(실행할일 To_do_Aktioun) { 작업가닥 Thread_VALUE = new 작업가닥(To_do_Aktioun); Thread_VALUE.Start_To_do(); return Thread_VALUE; }
    public static void 기다리기(작업가닥 Thread_VALUE) throws 대기중단예외 { Thread_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 Thread_VALUE) { return Thread_VALUE.살아있는가(); }
    public static void YIELD_To_do() { 작업가닥.YIELD_To_do(); }
}
