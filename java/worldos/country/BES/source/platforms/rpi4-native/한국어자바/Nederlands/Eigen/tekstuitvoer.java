// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** Eigen 커널의 표준 tekstuitvoer. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class tekstuitvoer {
    private tekstuitvoer() {}
    public static void Schrijven(String tekst) { System.out.print(tekst); }
    public static void schrijven_lijn(String tekst) { System.out.println(tekst); }
    public static void schrijven_nummer(int nummer) { System.out.println(nummer); }
}
