// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
/** 작업 tråd_värde: 하나의 köra_kommando flöde_värde. eget JVM 안에서 kommando 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static arbete Kör(실행할일 uppgift_Action) { arbete tråd_värde = new arbete(uppgift_Action); tråd_värde.START_uppgift(); return tråd_värde; }
    public static void 기다리기(arbete tråd_värde) throws 대기중단예외 { tråd_värde.기다리기(); }
    public static boolean 살아있는가(arbete tråd_värde) { return tråd_värde.살아있는가(); }
    public static void NOMAVK_uppgift() { arbete.NOMAVK_uppgift(); }
}
