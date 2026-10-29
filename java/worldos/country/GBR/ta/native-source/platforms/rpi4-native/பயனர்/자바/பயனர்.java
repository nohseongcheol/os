// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 கருவிகள் 전용 SVC இணைக்க. 기존 x86 கருவிகள் 원문을 함께 빌드한다. */
public final class பயனர் {
    public static native int 파일서술자열기(int[] பெயர், int அமைப்புகள்);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int மதிப்பு);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] பெயர், int[] தரவு);
    public static native int எழுது_கோப்பு(int[] பெயர், int[] தரவு, int நீளம்_மதிப்பு);
    public static native int எழுது(String உரை);
    public static native int எழுது_எழுத்துக்குறி_மதிப்பு(int மதிப்பு);
    public static native int 인수개수();
    public static native String செயலுருபுகள்(int அடைவு);
    public static native int 도구번호();
    public static native int 화면연결(int செயல், int அடைவு, int 가, int 나, int 다, int 라);
    public static native int 화면글(int அடைவு, int[] உரை, int நீளம்_மதிப்பு);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int தொடரோடி_கட்டுப்பாடு(int செயல், int 서술자, int மதிப்பு);
    public static native int இணை_தொடரோடி(int 서술자, int முகவரி, int முணையம்_மதிப்பு);
    public static native int திற_பிணையம்(int முணையம்_மதிப்பு);
    public static native int அனுப்பு_பிணையம்(int 서술자, int முகவரி, int முணையம்_மதிப்பு, int[] தரவு, int நீளம்_மதிப்பு);
    public static native int 통신받기(int 서술자, int[] தரவு, int நீளம்_மதிப்பு);
    public static native int பிணையம்_முணையம்(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int வெர்டிகல்_நிலை, int 폭, int 높이, int 색);
}
