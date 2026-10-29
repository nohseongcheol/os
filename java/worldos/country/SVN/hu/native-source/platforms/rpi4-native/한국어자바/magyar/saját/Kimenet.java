// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** saját 커널의 표준 Kimenet. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Kimenet {
    private Kimenet() {}
    public static void Írás(String Szöveg) { System.out.print(Szöveg); }
    public static void ír_sor(String Szöveg) { System.out.println(Szöveg); }
    public static void ír_szám(int szám) { System.out.println(szám); }
}
