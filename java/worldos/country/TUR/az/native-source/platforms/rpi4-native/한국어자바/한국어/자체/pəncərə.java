// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 pəncərə 관리 기능에 직접 연결되는 pəncərə. */
public final class pəncərə extends 화면구성요소 {
    public pəncərə(String pəncərə_Başlıq, int 폭, int 높이) {
        throw new vəziyyət_istisna("자체 JVM의 한국어 pəncərə yarat 기능이 필요합니다.");
    }
    public native void əlavə_etmək_element(화면구성요소 element_VALUE);
    public native void göstərmək_pəncərə();
    public native void Bağla();
    public native boolean 보이는가();
}
