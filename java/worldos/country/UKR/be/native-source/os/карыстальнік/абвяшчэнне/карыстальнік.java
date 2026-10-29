// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros карыстальнік ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class карыстальнік {
    public static native int 파일서술자열기(int[] файл_увядзенне_імя, int адкрыць_Налады);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int байт_значэнне);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Назва, int[] дадзеныя);
    public static native int напісаць_сімвал_значэнне(int 문자);
    public static native int напісаць_файл(int[] Назва, int[] дадзеныя, int даўжыня_значэнне);
    public static native int Запіс(String кантэнт_значэнне);
    public static native int 인수개수();
    public static native String 인수(int індэкс);
    public static native int 실행권한();
    public static native int адкрыць_Сетка(int мясцовы_порт);
    public static native int адправіць_дадзеныя(int маркер_значэнне, int адрас, int прызначэнне_порт, int[] дадзеныя, int даўжыня_значэнне);
    public static native int 자료받기(int маркер_значэнне, int[] дадзеныя, int 제한밀리초);
    public static native int закрыць_Сетка(int маркер_значэнне);
    public static native int 내주소();
    public static native int 보낸주소(int маркер_значэнне);
    public static native int 보낸창구(int маркер_значэнне);
}
