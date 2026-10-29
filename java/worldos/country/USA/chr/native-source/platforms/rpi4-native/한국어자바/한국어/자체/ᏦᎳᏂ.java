// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 ᏦᎳᏂ 관리 기능에 직접 연결되는 ᏦᎳᏂ. */
public final class ᏦᎳᏂ extends 화면구성요소 {
    public ᏦᎳᏂ(String 제목, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 ᏦᎳᏂ 생성 기능이 필요합니다.");
    }
    public native void ᎧᏁᏉᏍᏗ_ᏑᏓᎴᎩ(화면구성요소 ᏑᏓᎴᎩ_ᏧᎬᏩᎶᏗᏯ);
    public native void ᏍᎩᎪᏩᏛᏓ_ᏦᎳᏂ();
    public native void ᎯᏍᏚᎲᎦ();
    public native boolean 보이는가();
}
