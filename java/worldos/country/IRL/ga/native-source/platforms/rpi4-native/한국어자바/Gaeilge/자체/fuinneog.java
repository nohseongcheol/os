// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
/** 자체 JVM과 커널의 fuinneog 관리 기능에 직접 연결되는 fuinneog. */
public final class fuinneog extends 화면구성요소 {
    public fuinneog(String fuinneog_Teideal, int 폭, int 높이) {
        throw new staid_eisceacht("자체 JVM의 Gaeilge fuinneog giniúint 기능이 필요합니다.");
    }
    public native void cuir_le_eilimint(화면구성요소 eilimint_VALUE);
    public native void seó_fuinneog();
    public native void Dún();
    public native boolean 보이는가();
}
