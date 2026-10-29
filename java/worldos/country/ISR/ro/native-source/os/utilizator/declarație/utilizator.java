// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros utilizator ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class utilizator {
    public static native int 파일서술자열기(int[] Fișier_intrare_nume, int crea_Setări);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int comitere_Fișiere(int 파일서술자);
    public static native int 파일읽기(int[] Nume, int[] date);
    public static native int scriere_caracter_VALUE(int 문자);
    public static native int scriere_Fișier(int[] Nume, int[] date, int lungime_VALUE);
    public static native int Scriere(String Conținut_VALUE);
    public static native int 인수개수();
    public static native String Argumente(int INDEX);
    public static native int executare_permisiune();
    public static native int crea_rețea(int local_muta);
    public static native int trimite_date(int handle_VALUE, int adresa, int destinație_muta, int[] date, int lungime_VALUE);
    public static native int primi_date(int handle_VALUE, int[] date, int 제한밀리초);
    public static native int închide_rețea(int handle_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int handle_VALUE);
    public static native int 보낸창구(int handle_VALUE);
}
