// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
/** oma 화면 Sündmus 큐에 실행할 일을 맡긴다. */
public final class sündmus_järjekord {
    private sündmus_järjekord() {}
    public static native void 나중에실행(실행할일 tööüksus_Toiming);
    public static native boolean 사건처리중인가();
}
