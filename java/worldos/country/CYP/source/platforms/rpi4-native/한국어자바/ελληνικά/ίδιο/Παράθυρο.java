// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
/** ίδιο JVM과 커널의 Παράθυρο 관리 기능에 직접 연결되는 Παράθυρο. */
public final class Παράθυρο extends 화면구성요소 {
    public Παράθυρο(String Παράθυρο_Τίτλος, int 폭, int ύψος_τιμή) {
        throw new Κατάσταση_εξαίρεση("ίδιο JVM의 ελληνικά Παράθυρο δημιουργώ 기능이 필요합니다.");
    }
    public native void Προσθήκη_στοιχείο(화면구성요소 στοιχείο_τιμή);
    public native void εμφανίζω_Παράθυρο();
    public native void Κλείσιμο();
    public native boolean 보이는가();
}
