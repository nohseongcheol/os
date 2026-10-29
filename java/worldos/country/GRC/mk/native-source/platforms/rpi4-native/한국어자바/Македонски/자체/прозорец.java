// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
/** 자체 JVM과 커널의 прозорец 관리 기능에 직접 연결되는 прозорец. */
public final class прозорец extends 화면구성요소 {
    public прозорец(String прозорец_Наслов, int 폭, int 높이) {
        throw new статус_исклучок("자체 JVM의 Македонски прозорец генерира 기능이 필요합니다.");
    }
    public native void додавање_елемент(화면구성요소 елемент_VALUE);
    public native void прикажи_прозорец();
    public native void Затвори();
    public native boolean 보이는가();
}
