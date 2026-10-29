// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** saját JVM이 직접 생성하고 그리는 magyar 화면 elem_ÉRTÉK. */
public final class Címke extends 화면구성요소 {
    public Címke(String Szöveg, int 가로, int szektor_pozíció, int 폭, int 높이) {
        throw new Állapot_kivétel("saját JVM의 magyar 화면 elem_ÉRTÉK generálás 기능이 필요합니다.");
    }
}
