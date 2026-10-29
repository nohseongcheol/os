// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 مشين 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void لکو_ڊسپلي_پيل(int 가로, int 세로, int 색);
    public static native int پاڇيداري(int 종류, int عمل);
    public static native void ختم_ڪريو_بعيد_حڪم(int حالت_قدر);
    public static native void 원격대기(int حالت_قدر);
    public static native void 직렬쓰기(int قدر);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void معطل_ڪريو_عمل_ڪار();
    public static native int ٺاھيو_ٽاسڪ(int ابتدائي);
    public static native int ٽاسڪ_حالت(int ابتدائي);
    public static native void روڪيو(int حالت_قدر);
    public static native int 씨플러스시험();
    public static native int هلائڻ_صارف_ائپ(int ابتدائي);
    public static native int پڙتال_ڪريو_صارف_ائپ();
    public static native int 인수준비(int 개수);
    public static native int تعميل_ڪرڻ_صارف_فائل();
    public static native int 리눅스파일실행();
    public static native int دليل_بائٽ(int ابتدائي, int 위치, int قدر);
    public static native int 터미널(int عمل);
    public static native int ڪنٽرول_صارف_ائپ(int عمل);
    public static native void 입출력전환(int عمل);
    public static native int فائل_منتقلي_خدمت(int عمل);
    public static native int نيٽ_ورڪ_حالت(int داخلا_قدر, int ابتدائي);
    public static native int نيٽ_ورڪ_سيٽنگون(int عمل, int پتو, int 가림, int 관문);
    public static native int 응답보내기(int پتو, int ترتيب_قدر);
    public static native int 응답읽기(int داخلا_قدر);
    public static native int سوال_سسٽم(int داخلا_قدر, int ابتدائي);
    public static native void 전원끄기();
}
