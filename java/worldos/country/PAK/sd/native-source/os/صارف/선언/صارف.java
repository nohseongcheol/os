// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros صارف ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class صارف {
    public static native int 파일서술자열기(int[] فائل_داخلا_نالو, int ٺاھيو_سيٽنگون);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int بائٽ_قدر);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] نالو, int[] ڪوائف);
    public static native int لکو_ڪريڪٽر_قدر(int 문자);
    public static native int لکو_فائل(int[] نالو, int[] ڪوائف, int لمبائي_قدر);
    public static native int لکو(String مواد_قدر);
    public static native int 인수개수();
    public static native String 인수(int ابتدائي);
    public static native int 실행권한();
    public static native int ٺاھيو_نيٽ_ورڪ(int مقامي_پورٽ);
    public static native int اي_ميل_ڪوائف(int منهن_ڏيڻ_قدر, int پتو, int منزل_مقصود_پورٽ, int[] ڪوائف, int لمبائي_قدر);
    public static native int 자료받기(int منهن_ڏيڻ_قدر, int[] ڪوائف, int 제한밀리초);
    public static native int بند_ڪرڻ_نيٽ_ورڪ(int منهن_ڏيڻ_قدر);
    public static native int 내주소();
    public static native int 보낸주소(int منهن_ڏيڻ_قدر);
    public static native int 보낸창구(int منهن_ڏيڻ_قدر);
}
