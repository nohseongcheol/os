// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 اوزار 전용 SVC ڪنيڪٽ. 기존 x86 اوزار 원문을 함께 빌드한다. */
public final class صارف {
    public static native int 파일서술자열기(int[] نالو, int سيٽنگون);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int قدر);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] نالو, int[] ڪوائف);
    public static native int لکو_فائل(int[] نالو, int[] ڪوائف, int لمبائي_قدر);
    public static native int لکو(String متن);
    public static native int لکو_ڪريڪٽر_قدر(int قدر);
    public static native int 인수개수();
    public static native String 인수(int ابتدائي);
    public static native int 도구번호();
    public static native int 화면연결(int عمل, int ابتدائي, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ابتدائي, int[] متن, int لمبائي_قدر);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int اسٽريم_ڪنٽرول(int عمل, int 서술자, int قدر);
    public static native int ڪنيڪٽ_اسٽريم(int 서술자, int پتو, int پورٽ_قدر);
    public static native int ٺاھيو_نيٽ_ورڪ(int پورٽ_قدر);
    public static native int اي_ميل_نيٽ_ورڪ(int 서술자, int پتو, int پورٽ_قدر, int[] ڪوائف, int لمبائي_قدر);
    public static native int 통신받기(int 서술자, int[] ڪوائف, int لمبائي_قدر);
    public static native int نيٽ_ورڪ_پورٽ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
