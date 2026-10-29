// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
/** nativo JVM 스케줄러가 관리하는 Esegui_comando Stream_VALORE. 표준 Thread를 감싸지 않는다. */
public final class esecutoreAsincrono {
    public esecutoreAsincrono(실행할일 task_Action) {
        throw new Stato_eccezione("nativo JVM의 Italiano 작업 thread_VALORE generare 기능이 필요합니다.");
    }
    public native void START_task() throws thread_Stato_eccezione;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void REND_task();
}
