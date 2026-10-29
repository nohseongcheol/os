// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
/** 작업 hari_balio: 하나의 exekutatu_komando Stream_balio. 자체 JVM 안에서 Komandoa 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Exekutatu_2(실행할일 ataza_ekintza) { 작업가닥 hari_balio = new 작업가닥(ataza_ekintza); hari_balio.HASI_ataza(); return hari_balio; }
    public static void 기다리기(작업가닥 hari_balio) throws 대기중단예외 { hari_balio.기다리기(); }
    public static boolean 살아있는가(작업가닥 hari_balio) { return hari_balio.살아있는가(); }
    public static void YIELD_ataza() { 작업가닥.YIELD_ataza(); }
}
