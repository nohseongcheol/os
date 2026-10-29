// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
/** עצמי 화면 אירוע 큐에 실행할 일을 맡긴다. */
public final class אירוע_תור {
    private אירוע_תור() {}
    public static native void 나중에실행(실행할일 משימה_המלצה);
    public static native boolean 사건처리중인가();
}
