// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 терезе 관리 기능에 직접 연결되는 терезе. */
public final class терезе extends 화면구성요소 {
    public терезе(String терезе_Наам, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 терезе 생성 기능이 필요합니다.");
    }
    public native void кошуу_элемент(화면구성요소 элемент_маани);
    public native void көрсөтүү_терезе();
    public native void Жабуу();
    public native boolean 보이는가();
}
