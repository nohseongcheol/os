// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 ришта_қимат: 하나의 иҷро_кардан_фармон ҷараён_қимат. 자체 JVM 안에서 фармон 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 порча(실행할일 вазифа_амал) { 작업가닥 ришта_қимат = new 작업가닥(вазифа_амал); ришта_қимат.Оғоз_вазифа(); return ришта_қимат; }
    public static void 기다리기(작업가닥 ришта_қимат) throws 대기중단예외 { ришта_қимат.기다리기(); }
    public static boolean 살아있는가(작업가닥 ришта_қимат) { return ришта_қимат.살아있는가(); }
    public static void боздоштан_вазифа() { 작업가닥.боздоштан_вазифа(); }
}
