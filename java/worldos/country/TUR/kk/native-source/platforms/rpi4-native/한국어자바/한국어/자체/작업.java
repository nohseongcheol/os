// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 ағын_мән: 하나의 орындау_пәрмен ағым_мән. 자체 JVM 안에서 Команда 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Орындау_2(실행할일 тапсырма_ұсыныс) { 작업가닥 ағын_мән = new 작업가닥(тапсырма_ұсыныс); ағын_мән.басы_тапсырма(); return ағын_мән; }
    public static void 기다리기(작업가닥 ағын_мән) throws 대기중단예외 { ағын_мән.기다리기(); }
    public static boolean 살아있는가(작업가닥 ағын_мән) { return ағын_мән.살아있는가(); }
    public static void кідірту_тапсырма() { 작업가닥.кідірту_тапсырма(); }
}
