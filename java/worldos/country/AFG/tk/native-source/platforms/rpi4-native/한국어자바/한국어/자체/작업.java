// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 akym_baha: 하나의 ýerine_ýetir_buýruk Stream_baha. 자체 JVM 안에서 buýruk 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Bitir(실행할일 tabşyryk_iş) { 작업가닥 akym_baha = new 작업가닥(tabşyryk_iş); akym_baha.başlat_tabşyryk(); return akym_baha; }
    public static void 기다리기(작업가닥 akym_baha) throws 대기중단예외 { akym_baha.기다리기(); }
    public static boolean 살아있는가(작업가닥 akym_baha) { return akym_baha.살아있는가(); }
    public static void togtatmak_tabşyryk() { 작업가닥.togtatmak_tabşyryk(); }
}
