// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
/** nativo JVM 스케줄러가 관리하는 Executar_comando fluxo_VALOR. 표준 Thread를 감싸지 않는다. */
public final class tarefaSegundoPlano {
    public tarefaSegundoPlano(실행할일 Tarefa_Ação) {
        throw new Estado_exceção("nativo JVM의 Português 작업 thread_VALOR gerar 기능이 필요합니다.");
    }
    public native void START_Tarefa() throws thread_Estado_exceção;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void LUCRO_Tarefa();
}
