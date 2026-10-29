// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 커널의 표준 ନିର୍ଗମ. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class ନିର୍ଗମ {
    private ନିର୍ଗମ() {}
    public static void ଲେଖନ୍ତୁ(String ପାଠ୍ଯ) { System.out.print(ପାଠ୍ଯ); }
    public static void ଲିଖନ_ରେଖା(String ପାଠ୍ଯ) { System.out.println(ପାଠ୍ଯ); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
