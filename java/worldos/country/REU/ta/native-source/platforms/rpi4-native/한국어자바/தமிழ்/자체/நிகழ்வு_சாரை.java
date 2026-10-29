// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
/** 자체 화면 நிகழ்வு 큐에 실행할 일을 맡긴다. */
public final class நிகழ்வு_சாரை {
    private நிகழ்வு_சாரை() {}
    public static native void 나중에실행(실행할일 பணி_செயல்);
    public static native boolean 사건처리중인가();
}
