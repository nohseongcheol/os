// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 threte_boleng: 하나의 phethagatša_taelo Stream_boleng. 자체 JVM 안에서 Taelo 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Diriša(실행할일 mošomo_tiro) { 작업가닥 threte_boleng = new 작업가닥(mošomo_tiro); threte_boleng.Thomišo_mošomo(); return threte_boleng; }
    public static void 기다리기(작업가닥 threte_boleng) throws 대기중단예외 { threte_boleng.기다리기(); }
    public static boolean 살아있는가(작업가닥 threte_boleng) { return threte_boleng.살아있는가(); }
    public static void e_thibetšwe_mošomo() { 작업가닥.e_thibetšwe_mošomo(); }
}
