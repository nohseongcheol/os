// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
/** 자체 JVM과 커널의 Xanela 관리 기능에 직접 연결되는 Xanela. */
public final class Xanela extends 화면구성요소 {
    public Xanela(String ventá_Título, int 폭, int 높이) {
        throw new Estado_excepción("자체 JVM의 Galego Xanela xerar 기능이 필요합니다.");
    }
    public native void engadir_elemento(화면구성요소 elemento_VALOR);
    public native void mostrar_ventá();
    public native void Pechar();
    public native boolean 보이는가();
}
