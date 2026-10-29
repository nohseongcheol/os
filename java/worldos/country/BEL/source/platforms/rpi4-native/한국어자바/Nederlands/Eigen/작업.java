// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** 작업 thread_WAARDE: 하나의 Uitvoeren_opdracht Stream_WAARDE. Eigen JVM 안에서 opdracht 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static achtergrondwerker starten(실행할일 taak_Actie) { achtergrondwerker thread_WAARDE = new achtergrondwerker(taak_Actie); thread_WAARDE.START_taak(); return thread_WAARDE; }
    public static void 기다리기(achtergrondwerker thread_WAARDE) throws 대기중단예외 { thread_WAARDE.기다리기(); }
    public static boolean 살아있는가(achtergrondwerker thread_WAARDE) { return thread_WAARDE.살아있는가(); }
    public static void RENDEMENT_taak() { achtergrondwerker.RENDEMENT_taak(); }
}
