// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 Терезе 관리 기능에 직접 연결되는 Терезе. */
public final class Терезе extends 화면구성요소 {
    public Терезе(String терезе_Тақырып, int 폭, int 높이) {
        throw new күй_ерекшелік("자체 JVM의 한국어 Терезе жасау 기능이 필요합니다.");
    }
    public native void Қосу_элемент(화면구성요소 элемент_мән);
    public native void көрсету_терезе();
    public native void Жабу();
    public native boolean 보이는가();
}
