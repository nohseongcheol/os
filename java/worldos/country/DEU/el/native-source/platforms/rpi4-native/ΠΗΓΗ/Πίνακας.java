// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 υπολογιστής_5eb260fa όριο_τιμή. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Πίνακας {
    public static native int 표시화소읽기(int 가로, int τομέας_θέση);
    public static native void 표시화소쓰기(int 가로, int τομέας_θέση, int 색);
    public static native int απομακρυσμένος_έλεγχος(int 종류, int Ενέργεια);
    public static native void Τελική_οντότητα_απομακρυσμένος_εντολή(int Κατάσταση_τιμή);
    public static native void απομακρυσμένος_περίμενε(int Κατάσταση_τιμή);
    public static native void 직렬쓰기(int τιμή);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int κεντρική_μονάδα_επεξεργασίας_δικαίωμα_επίπεδο();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int τομέας_θέση, int 색);
    public static native void Απόδοση_εκτελών_την_επεξεργασία();
    public static native int ανοίγω_εργασία(int Ευρετήριο);
    public static native int εργασία_Κατάσταση(int Ευρετήριο);
    public static native void Στοπ(int Κατάσταση_τιμή);
    public static native int 씨플러스시험();
    public static native int εκτελώ_χρήστης_εφαρμογή(int Ευρετήριο);
    public static native int ελέγχω_χρήστης_εφαρμογή();
    public static native int 인수준비(int 개수);
    public static native int εκτελώ_χρήστης_Αρχείο();
    public static native int 리눅스파일실행();
    public static native int 인수바이트(int Ευρετήριο, int Θέση, int τιμή);
    public static native int Τερματικό(int Ενέργεια);
    public static native int έλεγχος_χρήστης_εφαρμογή(int Ενέργεια);
    public static native void 입출력전환(int Ενέργεια);
    public static native int μεταφορά_αρχείων_υπηρεσία(int Ενέργεια);
    public static native int δίκτυο_κατάσταση(int καταχώρηση_τιμή, int Ευρετήριο);
    public static native int δίκτυο_Ρυθμίσεις(int Ενέργεια, int διεύθυνση, int μάσκα_τιμή, int πύλη_τιμή);
    public static native int στέλνω_απάντηση(int διεύθυνση, int σειρά_τιμή);
    public static native int 응답읽기(int καταχώρηση_τιμή);
    public static native int ερώτημα_Σύστημα(int καταχώρηση_τιμή, int Ευρετήριο);
    public static native void 전원끄기();
}
