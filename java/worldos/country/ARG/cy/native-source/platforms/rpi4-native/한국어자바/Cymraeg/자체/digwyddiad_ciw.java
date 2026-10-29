// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
/** 자체 화면 digwyddiad 큐에 실행할 일을 맡긴다. */
public final class digwyddiad_ciw {
    private digwyddiad_ciw() {}
    public static native void 나중에실행(실행할일 tasg_gweithred);
    public static native boolean 사건처리중인가();
}
