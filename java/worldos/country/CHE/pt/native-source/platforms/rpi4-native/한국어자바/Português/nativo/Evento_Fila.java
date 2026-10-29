// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
/** nativo tela Evento 큐에 실행할 일을 맡긴다. */
public final class Evento_Fila {
    private Evento_Fila() {}
    public static native void 나중에실행(실행할일 Tarefa_Ação);
    public static native boolean 사건처리중인가();
}
