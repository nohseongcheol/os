// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
/** vlastiti 화면 Događaj 큐에 실행할 일을 맡긴다. */
public final class događaj_red_čekanja {
    private događaj_red_čekanja() {}
    public static native void 나중에실행(실행할일 obaveza_akcija);
    public static native boolean 사건처리중인가();
}
