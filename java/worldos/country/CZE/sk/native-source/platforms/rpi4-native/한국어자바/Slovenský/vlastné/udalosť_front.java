// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
/** vlastné 화면 Udalosť 큐에 실행할 일을 맡긴다. */
public final class udalosť_front {
    private udalosť_front() {}
    public static native void 나중에실행(실행할일 úloha_Akcia);
    public static native boolean 사건처리중인가();
}
