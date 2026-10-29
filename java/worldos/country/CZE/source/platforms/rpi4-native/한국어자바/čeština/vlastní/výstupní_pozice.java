// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
/** vlastní 커널의 표준 výstupní_pozice. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class výstupní_pozice {
    private výstupní_pozice() {}
    public static void Zápis(String text) { System.out.print(text); }
    public static void zápis_čára(String text) { System.out.println(text); }
    public static void zápis_číslo(int číslo) { System.out.println(číslo); }
}
