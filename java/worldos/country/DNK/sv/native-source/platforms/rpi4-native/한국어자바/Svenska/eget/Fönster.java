// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
/** eget JVM과 커널의 Fönster 관리 기능에 직접 연결되는 Fönster. */
public final class Fönster extends skärmbild_element {
    public Fönster(String fönster_titel, int 폭, int 높이) {
        throw new status_fel("eget JVM의 Svenska Fönster generera 기능이 필요합니다.");
    }
    public native void Lägg_till_element(skärmbild_element element_värde);
    public native void visa_fönster();
    public native void Stäng();
    public native boolean 보이는가();
}
