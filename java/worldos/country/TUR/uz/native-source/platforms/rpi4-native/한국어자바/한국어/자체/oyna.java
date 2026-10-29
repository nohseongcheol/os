// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 oyna 관리 기능에 직접 연결되는 oyna. */
public final class oyna extends 화면구성요소 {
    public oyna(String oyna_Nom, int 폭, int 높이) {
        throw new holat_istisno("자체 JVM의 한국어 oyna generatsiiyalash 기능이 필요합니다.");
    }
    public native void qo_shmoq_element(화면구성요소 element_VALUE);
    public native void ko_rsatmoq_oyna();
    public native void Yopish();
    public native boolean 보이는가();
}
