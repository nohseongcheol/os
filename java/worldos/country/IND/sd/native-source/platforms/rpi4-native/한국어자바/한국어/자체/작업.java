// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 لڙي_قدر: 하나의 تعميل_ڪرڻ_حڪم اسٽريم_قدر. 자체 JVM 안에서 حڪم 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 هلائڻ(실행할일 ٽاسڪ_عمل) { 작업가닥 لڙي_قدر = new 작업가닥(ٽاسڪ_عمل); لڙي_قدر.شروع_ٽاسڪ(); return لڙي_قدر; }
    public static void 기다리기(작업가닥 لڙي_قدر) throws 대기중단예외 { لڙي_قدر.기다리기(); }
    public static boolean 살아있는가(작업가닥 لڙي_قدر) { return لڙي_قدر.살아있는가(); }
    public static void معطل_ڪريو_ٽاسڪ() { 작업가닥.معطل_ڪريو_ٽاسڪ(); }
}
