// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
/** eigin 커널의 표준 úttak. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class úttak {
    private úttak() {}
    public static void Skrift(String Texti) { System.out.print(Texti); }
    public static void skrifa_lína(String Texti) { System.out.println(Texti); }
    public static void skrifa_númer(int númer) { System.out.println(númer); }
}
