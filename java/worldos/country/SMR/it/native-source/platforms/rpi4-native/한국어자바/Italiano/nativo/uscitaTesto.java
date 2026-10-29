// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
/** nativo 커널의 표준 uscitaTesto. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class uscitaTesto {
    private uscitaTesto() {}
    public static void Scrittura(String testo) { System.out.print(testo); }
    public static void scrivere_riga(String testo) { System.out.println(testo); }
    public static void scrivere_numero(int numero) { System.out.println(numero); }
}
