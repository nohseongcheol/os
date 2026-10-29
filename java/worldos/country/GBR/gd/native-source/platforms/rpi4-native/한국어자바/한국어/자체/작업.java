// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 snàithlean_VALUE: 하나의 gnìomhaich_àithne sruth_VALUE. 자체 JVM 안에서 àithne 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ruith(실행할일 saothair_gnìomh) { 작업가닥 snàithlean_VALUE = new 작업가닥(saothair_gnìomh); snàithlean_VALUE.Start_saothair(); return snàithlean_VALUE; }
    public static void 기다리기(작업가닥 snàithlean_VALUE) throws 대기중단예외 { snàithlean_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 snàithlean_VALUE) { return snàithlean_VALUE.살아있는가(); }
    public static void YIELD_saothair() { 작업가닥.YIELD_saothair(); }
}
