// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
/** vlastné 커널의 표준 Výstup. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Výstup {
    private Výstup() {}
    public static void Zápis(String Spracovanie_textu) { System.out.print(Spracovanie_textu); }
    public static void zapísať_linka(String Spracovanie_textu) { System.out.println(Spracovanie_textu); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
