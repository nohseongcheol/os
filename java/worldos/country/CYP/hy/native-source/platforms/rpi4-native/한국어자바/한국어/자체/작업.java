// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 շղթա_արժեք: 하나의 կատարել_հրաման հոսք_արժեք. 자체 JVM 안에서 Հրահանգ 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Գործարկել(실행할일 խնդիր_գործողություն) { 작업가닥 շղթա_արժեք = new 작업가닥(խնդիր_գործողություն); շղթա_արժեք.Մեկնարկ_խնդիր(); return շղթա_արժեք; }
    public static void 기다리기(작업가닥 շղթա_արժեք) throws 대기중단예외 { շղթա_արժեք.기다리기(); }
    public static boolean 살아있는가(작업가닥 շղթա_արժեք) { return շղթա_արժեք.살아있는가(); }
    public static void կասեցնել_խնդիր() { 작업가닥.կասեցնել_խնդիր(); }
}
