// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
/** 작업 νήμα_τιμή: 하나의 εκτελώ_εντολή ροή_τιμή. ίδιο JVM 안에서 Εντολή 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Εκτέλεση_2(실행할일 εργασία_έργο) { 작업가닥 νήμα_τιμή = new 작업가닥(εργασία_έργο); νήμα_τιμή.αρχή_εργασία(); return νήμα_τιμή; }
    public static void 기다리기(작업가닥 νήμα_τιμή) throws 대기중단예외 { νήμα_τιμή.기다리기(); }
    public static boolean 살아있는가(작업가닥 νήμα_τιμή) { return νήμα_τιμή.살아있는가(); }
    public static void Απόδοση_εργασία() { 작업가닥.Απόδοση_εργασία(); }
}
