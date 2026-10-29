// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
/** 자체 화면 ઇવેંટ 큐에 실행할 일을 맡긴다. */
public final class ઇવેંટ_કતાર {
    private ઇવેંટ_કતાર() {}
    public static native void 나중에실행(실행할일 કાર્ય_સંદેશ);
    public static native boolean 사건처리중인가();
}
