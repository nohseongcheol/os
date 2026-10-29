// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 інструменти 전용 SVC З_єднання. 기존 x86 інструменти 원문을 함께 빌드한다. */
public final class простір_користувача {
    public static native int 파일서술자열기(int[] Назва, int Налаштування);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int значення);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Назва, int[] дані);
    public static native int записування_Файл(int[] Назва, int[] дані, int 길이);
    public static native int Запис(String текст);
    public static native int записування_символ_значення(int значення);
    public static native int 인수개수();
    public static native String аргументи(int індекс);
    public static native int 도구번호();
    public static native int 화면연결(int Дія, int індекс, int 가, int 나, int 다, int 라);
    public static native int 화면글(int індекс, int[] текст, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int потік_керування(int Дія, int 서술자, int значення);
    public static native int зв_язок_потік(int 서술자, int Адреса, int порт_значення);
    public static native int відкрито_мережа(int порт_значення);
    public static native int надсилати_мережа(int 서술자, int Адреса, int порт_значення, int[] дані, int 길이);
    public static native int отримувати_мережа(int 서술자, int[] дані, int 길이);
    public static native int мережа_порт(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int прямокутник(int 가로, int Вертикаль_посада, int 폭, int 높이, int 색);
}
