// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 igalaangujaq 관리 기능에 직접 연결되는 igalaangujaq. */
public final class igalaangujaq extends 화면구성요소 {
    public igalaangujaq(String 제목, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 igalaangujaq 생성 기능이 필요합니다.");
    }
    public native void ilali_ilanga(화면구성요소 ilanga_atuutilik);
    public native void saqqilli_igalaangujaq();
    public native void matuli();
    public native boolean 보이는가();
}
