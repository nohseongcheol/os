// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
/** اپنا 커널의 표준 اخراج_کا_مقام. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class اخراج_کا_مقام {
    private اخراج_کا_مقام() {}
    public static void لکھیں(String متن) { System.out.print(متن); }
    public static void لکھیں_لائن(String متن) { System.out.println(متن); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
