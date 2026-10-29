// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
/** Asli 화면 Peristiwa 큐에 실행할 일을 맡긴다. */
public final class acara_baris {
    private acara_baris() {}
    public static native void 나중에실행(실행할일 tugas_cadangan);
    public static native boolean 사건처리중인가();
}
