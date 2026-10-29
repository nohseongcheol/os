// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 thread_VALUE: 하나의 zbatoj_komandë Stream_VALUE. 자체 JVM 안에서 Komanda 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Ekzekuto(실행할일 detyrë_veprim) { 작업가닥 thread_VALUE = new 작업가닥(detyrë_veprim); thread_VALUE.nis_detyrë(); return thread_VALUE; }
    public static void 기다리기(작업가닥 thread_VALUE) throws 대기중단예외 { thread_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 thread_VALUE) { return thread_VALUE.살아있는가(); }
    public static void YIELD_detyrë() { 작업가닥.YIELD_detyrë(); }
}
