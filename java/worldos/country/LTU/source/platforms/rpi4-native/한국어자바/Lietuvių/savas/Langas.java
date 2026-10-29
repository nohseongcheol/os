// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
/** savas JVM과 커널의 Langas 관리 기능에 직접 연결되는 Langas. */
public final class Langas extends 화면구성요소 {
    public Langas(String langas_Pavadinimas, int 폭, int 높이) {
        throw new Būsena_išimtis("savas JVM의 Lietuvių Langas generuoti 기능이 필요합니다.");
    }
    public native void Įtraukti_elementas(화면구성요소 elementas_VALUE);
    public native void laida_langas();
    public native void Užverti();
    public native boolean 보이는가();
}
