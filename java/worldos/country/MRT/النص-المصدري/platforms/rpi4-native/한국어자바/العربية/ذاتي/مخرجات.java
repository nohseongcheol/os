// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;
/** ذاتي 커널의 표준 مخرجات. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class مخرجات {
    private مخرجات() {}
    public static void كتابة(String نص) { System.out.print(نص); }
    public static void كتابة_خط(String نص) { System.out.println(نص); }
    public static void كتابة_رقم(int رقم) { System.out.println(رقم); }
}
