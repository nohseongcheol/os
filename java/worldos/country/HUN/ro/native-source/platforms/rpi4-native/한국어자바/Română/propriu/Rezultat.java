// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
/** propriu 커널의 표준 Rezultat. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Rezultat {
    private Rezultat() {}
    public static void Scriere(String SMS) { System.out.print(SMS); }
    public static void scriere_linie(String SMS) { System.out.println(SMS); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
