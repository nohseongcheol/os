// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
/** ίδιο JVM 스케줄러가 관리하는 εκτελώ_εντολή ροή_τιμή. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 εργασία_έργο) {
        throw new Κατάσταση_εξαίρεση("ίδιο JVM의 ελληνικά 작업 νήμα_τιμή δημιουργώ 기능이 필요합니다.");
    }
    public native void αρχή_εργασία() throws νήμα_Κατάσταση_εξαίρεση;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void Απόδοση_εργασία();
}
