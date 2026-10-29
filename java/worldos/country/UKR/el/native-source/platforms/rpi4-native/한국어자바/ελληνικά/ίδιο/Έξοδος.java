// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
/** ίδιο 커널의 표준 Έξοδος. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Έξοδος {
    private Έξοδος() {}
    public static void Εγγραφή(String Κείμενο) { System.out.print(Κείμενο); }
    public static void εγγράφω_γραμμή(String Κείμενο) { System.out.println(Κείμενο); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
