// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;
/** 자체 JVM과 커널의 idirishya 관리 기능에 직접 연결되는 idirishya. */
public final class idirishya extends 화면구성요소 {
    public idirishya(String idirishya_Umutwe, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 Ikinyarwanda idirishya 생성 기능이 필요합니다.");
    }
    public native void kongeraho_ikintu(화면구성요소 ikintu_agaciro);
    public native void kugaragaza_idirishya();
    public native void Gufunga();
    public native boolean 보이는가();
}
