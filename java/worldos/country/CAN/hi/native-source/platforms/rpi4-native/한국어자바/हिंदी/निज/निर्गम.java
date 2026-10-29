// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
/** निज 커널의 표준 निर्गम. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class निर्गम {
    private निर्गम() {}
    public static void लिखें(String पाठ) { System.out.print(पाठ); }
    public static void लिखना_लाइन(String पाठ) { System.out.println(पाठ); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
