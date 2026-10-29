// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 화면 միջոցառում 큐에 실행할 일을 맡긴다. */
public final class միջոցառում_հերթ {
    private միջոցառում_հերթ() {}
    public static native void 나중에실행(실행할일 խնդիր_գործողություն);
    public static native boolean 사건처리중인가();
}
