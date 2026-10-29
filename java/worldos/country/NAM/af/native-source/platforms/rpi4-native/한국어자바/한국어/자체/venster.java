// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 venster 관리 기능에 직접 연결되는 venster. */
public final class venster extends 화면구성요소 {
    public venster(String venster_Titel, int 폭, int 높이) {
        throw new stand_uitsondering("자체 JVM의 한국어 venster genereer 기능이 필요합니다.");
    }
    public native void byvoeg_element(화면구성요소 element_VALUE);
    public native void wys_venster();
    public native void Sluit();
    public native boolean 보이는가();
}
