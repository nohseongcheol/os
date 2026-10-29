// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 커널의 표준 అవుట్పుట్. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class అవుట్పుట్ {
    private అవుట్పుట్() {}
    public static void వ్రాయుము(String పాఠ్యము) { System.out.print(పాఠ్యము); }
    public static void వ్రాయి_పంక్తి(String పాఠ్యము) { System.out.println(పాఠ్యము); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
