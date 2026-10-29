// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
/** 작업 thread_VALORE: 하나의 Esegui_comando Stream_VALORE. nativo JVM 안에서 comando 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static esecutoreAsincrono avvia(실행할일 task_Action) { esecutoreAsincrono thread_VALORE = new esecutoreAsincrono(task_Action); thread_VALORE.START_task(); return thread_VALORE; }
    public static void 기다리기(esecutoreAsincrono thread_VALORE) throws 대기중단예외 { thread_VALORE.기다리기(); }
    public static boolean 살아있는가(esecutoreAsincrono thread_VALORE) { return thread_VALORE.살아있는가(); }
    public static void REND_task() { esecutoreAsincrono.REND_task(); }
}
