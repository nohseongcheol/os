// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros пайдаланушы ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class пайдаланушы {
    public static native int 파일서술자열기(int[] файл_енгізу_аты, int ашу_Параметрлер);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int байт_мән);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int бекіту_файл_сақтау_орны(int 파일서술자);
    public static native int 파일읽기(int[] Аты, int[] деректер);
    public static native int жазу_таңба_мән(int 문자);
    public static native int жазу_файл(int[] Аты, int[] деректер, int ұзындық_мән);
    public static native int Жазу(String мазмұн_мән);
    public static native int 인수개수();
    public static native String Аргументтер(int индекс);
    public static native int 실행권한();
    public static native int ашу_желі(int жергілікті_порт);
    public static native int жіберу_деректер(int дескриптор_мән, int мекенжай, int тағайындау_порт, int[] деректер, int ұзындық_мән);
    public static native int 자료받기(int дескриптор_мән, int[] деректер, int 제한밀리초);
    public static native int Жабу_желі(int дескриптор_мән);
    public static native int 내주소();
    public static native int 보낸주소(int дескриптор_мән);
    public static native int 보낸창구(int дескриптор_мән);
}
