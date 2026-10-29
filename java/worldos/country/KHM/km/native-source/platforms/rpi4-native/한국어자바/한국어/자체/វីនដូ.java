// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 វីនដូ 관리 기능에 직접 연결되는 វីនដូ. */
public final class វីនដូ extends 화면구성요소 {
    public វីនដូ(String វីនដូ_ចំណងជើង, int 폭, int 높이) {
        throw new ភាព_ការលើកលែង("자체 JVM의 한국어 វីនដូ បង្កើត 기능이 필요합니다.");
    }
    public native void បន្ថែម_ធាតុ(화면구성요소 ធាតុ_តំលៃ);
    public native void បង្ហាញ_វីនដូ();
    public native void បិទ();
    public native boolean 보이는가();
}
