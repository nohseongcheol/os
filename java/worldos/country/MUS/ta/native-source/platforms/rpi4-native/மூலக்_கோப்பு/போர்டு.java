// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 இயந்திரம் 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class போர்டு {
    public static native int 표시화소읽기(int 가로, int வெர்டிகல்_நிலை);
    public static native void எழுது_காட்சி_படக்_கூறு(int 가로, int வெர்டிகல்_நிலை, int 색);
    public static native int நிழலிடல்(int 종류, int செயல்);
    public static native void முடி_தொலைநிலை_கட்டளை(int நிலை_மதிப்பு_e10195a1);
    public static native void தொலைநிலை_காத்திரு(int நிலை_மதிப்பு_e10195a1);
    public static native void 직렬쓰기(int மதிப்பு);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int செயலி_அனுமதி_நிலை();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int வெர்டிகல்_நிலை, int 색);
    public static native void இடைநீக்கம்_செய்யப்பட்டது_செயலி();
    public static native int உருவாக்கு_பணி(int அடைவு);
    public static native int பணி_நிலை(int அடைவு);
    public static native void நிறுத்து(int நிலை_மதிப்பு_e10195a1);
    public static native int 씨플러스시험();
    public static native int இயக்கு_பயனர்_நிரல்(int அடைவு);
    public static native int காசோலை_பயனர்_நிரல்();
    public static native int 인수준비(int 개수);
    public static native int இயக்கு_பயனர்_கோப்பு();
    public static native int 리눅스파일실행();
    public static native int மதிப்புரு_பைட்(int அடைவு, int இடம், int மதிப்பு);
    public static native int கட்டளை_விளக்கி(int செயல்);
    public static native int கட்டுப்பாடு_பயனர்_நிரல்(int செயல்);
    public static native void 입출력전환(int செயல்);
    public static native int கோப்பு_இடமாற்று_சேவை(int செயல்);
    public static native int பிணையம்_நிலை(int உள்ளீடு_மதிப்பு, int அடைவு);
    public static native int பிணையம்_அமைப்புகள்(int செயல், int முகவரி, int முகமூடி_மதிப்பு, int நுழைவாயில்_மதிப்பு);
    public static native int 응답보내기(int முகவரி, int வரிசை_மதிப்பு);
    public static native int 응답읽기(int உள்ளீடு_மதிப்பு);
    public static native int வினவல்_முறைமை(int உள்ளீடு_மதிப்பு, int அடைவு);
    public static native void 전원끄기();
}
