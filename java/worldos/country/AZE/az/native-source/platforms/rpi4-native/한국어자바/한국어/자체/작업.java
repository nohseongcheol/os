// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 axın_VALUE_5b72a632: 하나의 icra_etmək_əmr axın_VALUE. 자체 JVM 안에서 Əmr 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 İcra_Et(실행할일 tapşırıq_aktiv) { 작업가닥 axın_VALUE_5b72a632 = new 작업가닥(tapşırıq_aktiv); axın_VALUE_5b72a632.Başla_tapşırıq(); return axın_VALUE_5b72a632; }
    public static void 기다리기(작업가닥 axın_VALUE_5b72a632) throws 대기중단예외 { axın_VALUE_5b72a632.기다리기(); }
    public static boolean 살아있는가(작업가닥 axın_VALUE_5b72a632) { return axın_VALUE_5b72a632.살아있는가(); }
    public static void YIELD_tapşırıq() { 작업가닥.YIELD_tapşırıq(); }
}
