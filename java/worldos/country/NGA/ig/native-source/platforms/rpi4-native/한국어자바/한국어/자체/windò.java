// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 windò 관리 기능에 직접 연결되는 windò. */
public final class windò extends 화면구성요소 {
    public windò(String windò_Isi_okwu, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 windò 생성 기능이 필요합니다.");
    }
    public native void gbakwụnye_njìmebe(화면구성요소 njìmebe_valuu);
    public native void gòsi_windò();
    public native void Mechie();
    public native boolean 보이는가();
}
