// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 थ्रॅड_मोल: 하나의 पाळो_दिवचो_आदेश Stream_मोल. 자체 JVM 안에서 आदेश 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 चलोवप(실행할일 कार्य_कृती) { 작업가닥 थ्रॅड_मोल = new 작업가닥(कार्य_कृती); थ्रॅड_मोल.Start_कार्य(); return थ्रॅड_मोल; }
    public static void 기다리기(작업가닥 थ्रॅड_मोल) throws 대기중단예외 { थ्रॅड_मोल.기다리기(); }
    public static boolean 살아있는가(작업가닥 थ्रॅड_मोल) { return थ्रॅड_मोल.살아있는가(); }
    public static void YIELD_कार्य() { 작업가닥.YIELD_कार्य(); }
}
