// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
/** nativo 커널의 표준 saídaTexto. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class saídaTexto {
    private saídaTexto() {}
    public static void Escrita(String texto) { System.out.print(texto); }
    public static void gravar_linha(String texto) { System.out.println(texto); }
    public static void gravar_número(int número) { System.out.println(número); }
}
