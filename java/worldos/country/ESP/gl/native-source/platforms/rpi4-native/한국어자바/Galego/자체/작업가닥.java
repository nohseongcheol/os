// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
/** 자체 JVM 스케줄러가 관리하는 executar_comando fluxo_VALOR. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 tarefa_acción) {
        throw new Estado_excepción("자체 JVM의 Galego 작업 tema_VALOR xerar 기능이 필요합니다.");
    }
    public native void START_tarefa() throws tema_Estado_excepción;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void suspender_tarefa();
}
