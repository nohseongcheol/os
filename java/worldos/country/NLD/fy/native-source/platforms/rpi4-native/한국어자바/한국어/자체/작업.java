// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 가닥: 하나의 실행 흐름. 자체 JVM 안에서 Kommando 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Start(실행할일 할일) { 작업가닥 가닥 = new 작업가닥(할일); 가닥.시작하기(); return 가닥; }
    public static void 기다리기(작업가닥 가닥) throws 대기중단예외 { 가닥.기다리기(); }
    public static boolean 살아있는가(작업가닥 가닥) { return 가닥.살아있는가(); }
    public static void 양보하기() { 작업가닥.양보하기(); }
}
