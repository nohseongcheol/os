// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
/** savas 화면 Įvykis 큐에 실행할 일을 맡긴다. */
public final class įvykis_eilė {
    private įvykis_eilė() {}
    public static native void 나중에실행(실행할일 užduotis_gavinys);
    public static native boolean 사건처리중인가();
}
