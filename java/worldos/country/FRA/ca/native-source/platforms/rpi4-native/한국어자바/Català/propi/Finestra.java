// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
/** propi JVM과 커널의 Finestra 관리 기능에 직접 연결되는 Finestra. */
public final class Finestra extends 화면구성요소 {
    public Finestra(String finestra_Títol, int 폭, int 높이) {
        throw new Estat_excepció("propi JVM의 Català Finestra generar 기능이 필요합니다.");
    }
    public native void afegir_element(화면구성요소 element_VALOR);
    public native void mostrar_finestra();
    public native void Tanca();
    public native boolean 보이는가();
}
