// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** Eigen JVM과 커널의 Venster 관리 기능에 직접 연결되는 Venster. */
public final class Venster extends scherm_element {
    public Venster(String venster_Titel, int 폭, int hoogte_WAARDE) {
        throw new Status_uitzondering("Eigen JVM의 Nederlands Venster genereren 기능이 필요합니다.");
    }
    public native void Toevoegen_element(scherm_element element_WAARDE);
    public native void weergeven_venster();
    public native void Sluiten();
    public native boolean 보이는가();
}
