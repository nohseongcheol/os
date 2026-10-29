// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros простір_користувача ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class простір_користувача {
    public static native int 파일서술자열기(int[] Файл_запис_ім_я, int відкрито_Настройки);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int байт_значення);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int затвердження_файлове_сховище(int 파일서술자);
    public static native int 파일읽기(int[] Назва, int[] дані);
    public static native int записування_символ_значення(int 문자);
    public static native int записування_Файл(int[] Назва, int[] дані, int 길이);
    public static native int Запис(String Вміст_значення);
    public static native int 인수개수();
    public static native String аргументи(int індекс);
    public static native int 실행권한();
    public static native int відкрито_мережа(int місцевий_порт);
    public static native int надсилати_дані(int маркер_значення, int Адреса, int місце_порт, int[] дані, int 길이);
    public static native int отримувати_дані(int маркер_значення, int[] дані, int 제한밀리초);
    public static native int Закрити_мережа(int маркер_значення);
    public static native int 내주소();
    public static native int 보낸주소(int маркер_значення);
    public static native int 보낸창구(int маркер_значення);
}
