// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
/** 작업 агым_VALUE_5b72a632: 하나의 үтәргә_команда агым_VALUE. 자체 JVM 안에서 команда 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 эшләтү(실행할일 мәсьәлә_гамәл) { 작업가닥 агым_VALUE_5b72a632 = new 작업가닥(мәсьәлә_гамәл); агым_VALUE_5b72a632.Start_мәсьәлә(); return агым_VALUE_5b72a632; }
    public static void 기다리기(작업가닥 агым_VALUE_5b72a632) throws 대기중단예외 { агым_VALUE_5b72a632.기다리기(); }
    public static boolean 살아있는가(작업가닥 агым_VALUE_5b72a632) { return агым_VALUE_5b72a632.살아있는가(); }
    public static void YIELD_мәсьәлә() { 작업가닥.YIELD_мәсьәлә(); }
}
