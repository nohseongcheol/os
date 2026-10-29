// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
/** เอง 커널의 표준 ข้อความออก. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class ข้อความออก {
    private ข้อความออก() {}
    public static void เขียน(String ข้อความ) { System.out.print(ข้อความ); }
    public static void 줄쓰기(String ข้อความ) { System.out.println(ข้อความ); }
    public static void 수쓰기(int หมายเลข) { System.out.println(หมายเลข); }
}
