// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Інструменты 전용 SVC Злучыцца. 기존 x86 Інструменты 원문을 함께 빌드한다. */
public final class карыстальнік {
    public static native int 파일서술자열기(int[] Назва, int Усталёўкі);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int значэнне);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Назва, int[] дадзеныя);
    public static native int напісаць_файл(int[] Назва, int[] дадзеныя, int даўжыня_значэнне);
    public static native int Запіс(String Тэкст);
    public static native int напісаць_сімвал_значэнне(int значэнне);
    public static native int 인수개수();
    public static native String 인수(int індэкс);
    public static native int 도구번호();
    public static native int 화면연결(int Дзеянне, int індэкс, int 가, int 나, int 다, int 라);
    public static native int 화면글(int індэкс, int[] Тэкст, int даўжыня_значэнне);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int паток_кіраванне(int Дзеянне, int 서술자, int значэнне);
    public static native int злучаць_паток(int 서술자, int адрас, int порт_значэнне);
    public static native int адкрыць_Сетка(int порт_значэнне);
    public static native int адправіць_Сетка(int 서술자, int адрас, int порт_значэнне, int[] дадзеныя, int даўжыня_значэнне);
    public static native int 통신받기(int 서술자, int[] дадзеныя, int даўжыня_значэнне);
    public static native int Сетка_порт(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
