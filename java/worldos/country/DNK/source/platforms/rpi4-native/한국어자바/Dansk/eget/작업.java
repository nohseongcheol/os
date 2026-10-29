// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
/** 작업 tråd_VÆRDI: 하나의 Udfør_kommando strøm_VÆRDI. eget JVM 안에서 Kommando 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static arbejder Kør_2(실행할일 job_To_do) { arbejder tråd_VÆRDI = new arbejder(job_To_do); tråd_VÆRDI.START_job(); return tråd_VÆRDI; }
    public static void 기다리기(arbejder tråd_VÆRDI) throws 대기중단예외 { tråd_VÆRDI.기다리기(); }
    public static boolean 살아있는가(arbejder tråd_VÆRDI) { return tråd_VÆRDI.살아있는가(); }
    public static void AFKAST_job() { arbejder.AFKAST_job(); }
}
