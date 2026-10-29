// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
/** 자체 JVM과 커널의 Прозорец 관리 기능에 직접 연결되는 Прозорец. */
public final class Прозорец extends 화면구성요소 {
    public Прозорец(String прозорец_Заглавие, int 폭, int 높이) {
        throw new Състояние_изключение("자체 JVM의 Български Прозорец генерирам 기능이 필요합니다.");
    }
    public native void добавям_елемент(화면구성요소 елемент_стойност);
    public native void показвам_прозорец();
    public native void Затворен();
    public native boolean 보이는가();
}
