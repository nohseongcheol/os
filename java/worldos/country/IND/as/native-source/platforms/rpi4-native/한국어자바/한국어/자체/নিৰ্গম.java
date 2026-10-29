// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 커널의 표준 নিৰ্গম. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class নিৰ্গম {
    private নিৰ্গম() {}
    public static void লিখা(String টেক্সট) { System.out.print(টেক্সট); }
    public static void লিখক_লাইন(String টেক্সট) { System.out.println(টেক্সট); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
