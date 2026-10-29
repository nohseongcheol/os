// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
/** 자체 JVM과 커널의 መስኮት 관리 기능에 직접 연결되는 መስኮት. */
public final class መስኮት extends 화면구성요소 {
    public መስኮት(String መስኮት_ኣርእስቲ, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 ትግርኛ መስኮት 생성 기능이 필요합니다.");
    }
    public native void ወስኽ_ንጥረ_ነገር(화면구성요소 ንጥረ_ነገር_ዋጋ);
    public native void ኣርእይ_መስኮት();
    public native void ዕጸው();
    public native boolean 보이는가();
}
