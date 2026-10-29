// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
/** 자체 JVM과 커널의 matapihi 관리 기능에 직접 연결되는 matapihi. */
public final class matapihi extends 화면구성요소 {
    public matapihi(String matapihi_Taitara, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 Reo_Māori matapihi waihanga 기능이 필요합니다.");
    }
    public native void tāpiri_huānga(화면구성요소 huānga_uara);
    public native void whakaatu_matapihi();
    public native void Kati();
    public native boolean 보이는가();
}
