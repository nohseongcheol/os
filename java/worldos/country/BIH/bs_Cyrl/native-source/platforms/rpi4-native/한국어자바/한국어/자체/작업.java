// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 нит_вриједност: 하나의 실행 ток_вриједност. 자체 JVM 안에서 команда 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 시작(실행할일 задатак_радња) { 작업가닥 нит_вриједност = new 작업가닥(задатак_радња); нит_вриједност.почети_задатак(); return нит_вриједност; }
    public static void 기다리기(작업가닥 нит_вриједност) throws 대기중단예외 { нит_вриједност.기다리기(); }
    public static boolean 살아있는가(작업가닥 нит_вриједност) { return нит_вриједност.살아있는가(); }
    public static void 양보하기() { 작업가닥.양보하기(); }
}
