// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Εργαλεία 전용 SVC Σύνδεση. 기존 x86 Εργαλεία 원문을 함께 빌드한다. */
public final class χρήστης {
    public static native int 파일서술자열기(int[] Όνομα, int Ρυθμίσεις);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int τιμή);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Όνομα, int[] δεδομένα);
    public static native int εγγράφω_Αρχείο(int[] Όνομα, int[] δεδομένα, int διάρκεια_τιμή);
    public static native int Εγγραφή(String Κείμενο);
    public static native int εγγράφω_χαρακτήρας_τιμή(int τιμή);
    public static native int 인수개수();
    public static native String Παράμετροι(int Ευρετήριο);
    public static native int 도구번호();
    public static native int 화면연결(int Ενέργεια, int Ευρετήριο, int 가, int 나, int 다, int 라);
    public static native int 화면글(int Ευρετήριο, int[] Κείμενο, int διάρκεια_τιμή);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ροή_έλεγχος(int Ενέργεια, int 서술자, int τιμή);
    public static native int συνδέω_ροή(int 서술자, int διεύθυνση, int θύρα_τιμή);
    public static native int ανοίγω_δίκτυο(int θύρα_τιμή);
    public static native int στέλνω_δίκτυο(int 서술자, int διεύθυνση, int θύρα_τιμή, int[] δεδομένα, int διάρκεια_τιμή);
    public static native int λαμβάνω_δίκτυο(int 서술자, int[] δεδομένα, int διάρκεια_τιμή);
    public static native int δίκτυο_θύρα(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int ορθογώνιο(int 가로, int τομέας_θέση, int 폭, int ύψος_τιμή, int 색);
}
