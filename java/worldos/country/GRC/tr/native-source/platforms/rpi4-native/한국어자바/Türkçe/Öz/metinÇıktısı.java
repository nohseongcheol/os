// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
/** Öz 커널의 표준 metinÇıktısı. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class metinÇıktısı {
    private metinÇıktısı() {}
    public static void Yazma(String metin) { System.out.print(metin); }
    public static void yazma_hat(String metin) { System.out.println(metin); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
