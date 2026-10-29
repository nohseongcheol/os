// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 thread_VALUE: 하나의 Mag_execute_utos Stream_VALUE. 자체 JVM 안에서 utos 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 run(실행할일 gawain_aksyon) { 작업가닥 thread_VALUE = new 작업가닥(gawain_aksyon); thread_VALUE.Start_gawain(); return thread_VALUE; }
    public static void 기다리기(작업가닥 thread_VALUE) throws 대기중단예외 { thread_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 thread_VALUE) { return thread_VALUE.살아있는가(); }
    public static void YIELD_gawain() { 작업가닥.YIELD_gawain(); }
}
