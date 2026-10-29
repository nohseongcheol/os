// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
/** 작업 нишка_VALUE: 하나의 Изврши_наредба Stream_VALUE. 자체 JVM 안에서 Команда 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Изврши_2(실행할일 задача_Дејство) { 작업가닥 нишка_VALUE = new 작업가닥(задача_Дејство); нишка_VALUE.Start_задача(); return нишка_VALUE; }
    public static void 기다리기(작업가닥 нишка_VALUE) throws 대기중단예외 { нишка_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 нишка_VALUE) { return нишка_VALUE.살아있는가(); }
    public static void YIELD_задача() { 작업가닥.YIELD_задача(); }
}
