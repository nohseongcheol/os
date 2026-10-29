// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
/** eget JVM과 커널의 Vindu 관리 기능에 직접 연결되는 Vindu. */
public final class Vindu extends skjermbilde_element {
    public Vindu(String vindu_Tittel, int 폭, int 높이) {
        throw new status_unntak("eget JVM의 norsk Vindu generere 기능이 필요합니다.");
    }
    public native void Legg_til_element(skjermbilde_element element_VERDI);
    public native void vise_vindu();
    public native void Lukk();
    public native boolean 보이는가();
}
