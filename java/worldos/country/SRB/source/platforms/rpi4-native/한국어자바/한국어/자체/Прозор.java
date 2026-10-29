// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 Прозор 관리 기능에 직접 연결되는 Прозор. */
public final class Прозор extends 화면구성요소 {
    public Прозор(String прозор_Наслов, int 폭, int 높이) {
        throw new стање_изузетак("자체 JVM의 한국어 Прозор генерисати 기능이 필요합니다.");
    }
    public native void додати_елемент(화면구성요소 елемент_вриједност);
    public native void емисија_прозор();
    public native void Затворен();
    public native boolean 보이는가();
}
