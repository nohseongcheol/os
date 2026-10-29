// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
/** 작업 tråd_VERDI: 하나의 Utfør_kommando strøm_VERDI. eget JVM 안에서 Kommando 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static arbeider Kjør_2(실행할일 oppgave_Gjøremål) { arbeider tråd_VERDI = new arbeider(oppgave_Gjøremål); tråd_VERDI.START_oppgave(); return tråd_VERDI; }
    public static void 기다리기(arbeider tråd_VERDI) throws 대기중단예외 { tråd_VERDI.기다리기(); }
    public static boolean 살아있는가(arbeider tråd_VERDI) { return tråd_VERDI.살아있는가(); }
    public static void AVKAST_oppgave() { arbeider.AVKAST_oppgave(); }
}
