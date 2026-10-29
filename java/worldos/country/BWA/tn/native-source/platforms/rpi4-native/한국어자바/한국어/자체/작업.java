// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 tlhale_Boleng: 하나의 diragatsa_Taelo moela_Boleng. 자체 JVM 안에서 Taelo 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 dirisa(실행할일 Tiro_tiro) { 작업가닥 tlhale_Boleng = new 작업가닥(Tiro_tiro); tlhale_Boleng.simolola_Tiro(); return tlhale_Boleng; }
    public static void 기다리기(작업가닥 tlhale_Boleng) throws 대기중단예외 { tlhale_Boleng.기다리기(); }
    public static boolean 살아있는가(작업가닥 tlhale_Boleng) { return tlhale_Boleng.살아있는가(); }
    public static void emisa_ka_nakwana_Tiro() { 작업가닥.emisa_ka_nakwana_Tiro(); }
}
