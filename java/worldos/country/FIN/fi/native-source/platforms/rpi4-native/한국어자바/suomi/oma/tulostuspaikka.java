// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** oma 커널의 표준 tulostuspaikka. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class tulostuspaikka {
    private tulostuspaikka() {}
    public static void Kirjoitus(String teksti) { System.out.print(teksti); }
    public static void kirjoitus_rivi(String teksti) { System.out.println(teksti); }
    public static void kirjoitus_numero(int numero) { System.out.println(numero); }
}
