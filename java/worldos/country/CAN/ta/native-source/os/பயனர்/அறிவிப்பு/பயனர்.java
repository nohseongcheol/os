// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros பயனர் ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class பயனர் {
    public static native int 파일서술자열기(int[] கோப்பு_உள்ளீடு_பெயர், int திற_அமைப்புகள்);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int பைட்_மதிப்பு);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] பெயர், int[] தரவு);
    public static native int எழுது_எழுத்துக்குறி_மதிப்பு(int 문자);
    public static native int எழுது_கோப்பு(int[] பெயர், int[] தரவு, int நீளம்_மதிப்பு);
    public static native int எழுது(String உள்ளடக்கம்_மதிப்பு);
    public static native int 인수개수();
    public static native String செயலுருபுகள்(int அடைவு);
    public static native int 실행권한();
    public static native int திற_பிணையம்(int தனி_முணையம்);
    public static native int அனுப்பு_தரவு(int நடத்தி_மதிப்பு, int முகவரி, int இலக்கு_முணையம், int[] தரவு, int நீளம்_மதிப்பு);
    public static native int 자료받기(int நடத்தி_மதிப்பு, int[] தரவு, int 제한밀리초);
    public static native int மூடு_பிணையம்(int நடத்தி_மதிப்பு);
    public static native int 내주소();
    public static native int 보낸주소(int நடத்தி_மதிப்பு);
    public static native int 보낸창구(int நடத்தி_மதிப்பு);
}
