// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
/** 자체 화면 hui 큐에 실행할 일을 맡긴다. */
public final class hui_tūtira {
    private hui_tūtira() {}
    public static native void 나중에실행(실행할일 tūmahi_hohenga);
    public static native boolean 사건처리중인가();
}
