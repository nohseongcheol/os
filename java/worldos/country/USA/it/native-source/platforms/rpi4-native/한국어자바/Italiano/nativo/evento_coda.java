// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
/** nativo schermata Evento 큐에 실행할 일을 맡긴다. */
public final class evento_coda {
    private evento_coda() {}
    public static native void 나중에실행(실행할일 task_Action);
    public static native boolean 사건처리중인가();
}
