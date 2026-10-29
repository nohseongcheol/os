// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
/** savs 커널의 표준 Izvade. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Izvade {
    private Izvade() {}
    public static void Rakstīt(String Teksts) { System.out.print(Teksts); }
    public static void rakstīšana_līnija(String Teksts) { System.out.println(Teksts); }
    public static void rakstīšana_numurs(int numurs) { System.out.println(numurs); }
}
