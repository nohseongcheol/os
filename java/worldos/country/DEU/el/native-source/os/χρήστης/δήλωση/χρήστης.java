// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros χρήστης ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class χρήστης {
    public static native int 파일서술자열기(int[] Αρχείο_καταχώρηση_όνομα, int ανοίγω_Ρυθμίσεις);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int 바이트);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int δέσμευση_Αρχεία(int 파일서술자);
    public static native int 파일읽기(int[] Όνομα, int[] δεδομένα);
    public static native int εγγράφω_χαρακτήρας_τιμή(int 문자);
    public static native int εγγράφω_Αρχείο(int[] Όνομα, int[] δεδομένα, int διάρκεια_τιμή);
    public static native int Εγγραφή(String Περιεχόμενο_τιμή);
    public static native int 인수개수();
    public static native String Παράμετροι(int Ευρετήριο);
    public static native int εκτέλεση_άδεια();
    public static native int ανοίγω_δίκτυο(int τοπικός_θύρα);
    public static native int στέλνω_δεδομένα(int δείκτης_χειρισμού_τιμή, int διεύθυνση, int προορισμός_θύρα, int[] δεδομένα, int διάρκεια_τιμή);
    public static native int λαμβάνω_δεδομένα(int δείκτης_χειρισμού_τιμή, int[] δεδομένα, int 제한밀리초);
    public static native int κλείνω_δίκτυο(int δείκτης_χειρισμού_τιμή);
    public static native int 내주소();
    public static native int 보낸주소(int δείκτης_χειρισμού_τιμή);
    public static native int 보낸창구(int δείκτης_χειρισμού_τιμή);
}
