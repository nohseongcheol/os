// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
/** eget JVM과 커널의 Vindue 관리 기능에 직접 연결되는 Vindue. */
public final class Vindue extends skærmbillede_element {
    public Vindue(String vindue_Titel, int 폭, int 높이) {
        throw new status_undtagelse("eget JVM의 Dansk Vindue generere 기능이 필요합니다.");
    }
    public native void Tilføj_element(skærmbillede_element element_VÆRDI);
    public native void vise_vindue();
    public native void Luk();
    public native boolean 보이는가();
}
