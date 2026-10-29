// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
/** নিজ 커널의 표준 নির্গম. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class নির্গম {
    private নির্গম() {}
    public static void লেখা(String পাঠ) { System.out.print(পাঠ); }
    public static void লেখা_লাইন(String পাঠ) { System.out.println(পাঠ); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
