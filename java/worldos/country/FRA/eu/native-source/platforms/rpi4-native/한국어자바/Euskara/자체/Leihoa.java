// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
/** 자체 JVM과 커널의 Leihoa 관리 기능에 직접 연결되는 Leihoa. */
public final class Leihoa extends 화면구성요소 {
    public Leihoa(String leiho_Izenburua, int 폭, int 높이) {
        throw new Egoera_salbuespen("자체 JVM의 Euskara Leihoa sortu 기능이 필요합니다.");
    }
    public native void gehitu_elementu(화면구성요소 elementu_balio);
    public native void erakutsi_leiho();
    public native void Itxi();
    public native boolean 보이는가();
}
