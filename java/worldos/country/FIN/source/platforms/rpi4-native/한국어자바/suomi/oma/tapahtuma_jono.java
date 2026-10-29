// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** oma 화면 Tapahtuma 큐에 실행할 일을 맡긴다. */
public final class tapahtuma_jono {
    private tapahtuma_jono() {}
    public static native void 나중에실행(실행할일 tehtävä_toimi);
    public static native boolean 사건처리중인가();
}
