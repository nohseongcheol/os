// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros کارن ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class کارن {
    public static native int 파일서술자열기(int[] 파일이름, int 열기설정);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int بايټ_ارزښت);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] نوم, int[] اومتوک);
    public static native int ليکل_لوښه_ارزښت(int 문자);
    public static native int ليکل_دوتنه(int[] نوم, int[] اومتوک, int اوږدوالى_ارزښت);
    public static native int لوستل_2(String منځپانګه_ارزښت);
    public static native int 인수개수();
    public static native String 인수(int لړیال);
    public static native int 실행권한();
    public static native int 통신열기(int 지역창구);
    public static native int استول_اومتوک(int لاستى_ارزښت, int پته, int موخه_درشل, int[] اومتوک, int اوږدوالى_ارزښت);
    public static native int 자료받기(int لاستى_ارزښت, int[] اومتوک, int 제한밀리초);
    public static native int بندول_جال(int لاستى_ارزښت);
    public static native int 내주소();
    public static native int 보낸주소(int لاستى_ارزښت);
    public static native int 보낸창구(int لاستى_ارزښت);
}
