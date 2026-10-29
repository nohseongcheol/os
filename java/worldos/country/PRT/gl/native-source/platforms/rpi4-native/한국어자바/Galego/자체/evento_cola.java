// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
/** 자체 화면 Evento 큐에 실행할 일을 맡긴다. */
public final class evento_cola {
    private evento_cola() {}
    public static native void 나중에실행(실행할일 tarefa_acción);
    public static native boolean 사건처리중인가();
}
