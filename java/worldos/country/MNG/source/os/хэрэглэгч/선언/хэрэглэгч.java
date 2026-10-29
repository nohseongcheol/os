// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros хэрэглэгч ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class хэрэглэгч {
    public static native int 파일서술자열기(int[] файл_оролт_нэр, int нээх_Тохиргоо);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int байт_утга);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Нэр, int[] өгөгдөл);
    public static native int бичих_тэмдэгт_утга(int 문자);
    public static native int бичих_файл(int[] Нэр, int[] өгөгдөл, int урт_утга);
    public static native int Бичих(String Агуулга_утга);
    public static native int 인수개수();
    public static native String 인수(int индекс);
    public static native int 실행권한();
    public static native int нээх_Сүлжээ(int локал_порт);
    public static native int илгээх_өгөгдөл(int барих_утга, int хаяг, int товлосон_газар_порт, int[] өгөгдөл, int урт_утга);
    public static native int 자료받기(int барих_утга, int[] өгөгдөл, int 제한밀리초);
    public static native int хаах_Сүлжээ(int барих_утга);
    public static native int 내주소();
    public static native int 보낸주소(int барих_утга);
    public static native int 보낸창구(int барих_утга);
}
