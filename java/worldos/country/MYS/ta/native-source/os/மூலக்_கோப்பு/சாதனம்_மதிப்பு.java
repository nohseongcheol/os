// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** x86 명령과 물리 முகவரி 접근만 담당하는 컴파일러의 제한된 native 경계. */
public final class சாதனம்_மதிப்பு {
    public static native int கோப்பு_நினைவகம்();
    public static native int 자바파일묶음();
    public static native int 자바파일묶음크기();
    public static native int 입출력바이트읽기(int அடைவு);
    public static native void 입출력바이트쓰기(int அடைவு, int மதிப்பு);
    public static native int 기억읽기(int முகவரி);
    public static native void எழுது_நினைவகம்(int முகவரி, int மதிப்பு);
    public static native int 부팅표식();
    public static native int 부팅정보();
    public static native int 배열사용량();
    public static native void 잠시양보();
    public static native void 정지();
    public static native void 시험종료(int மதிப்பு);
    public static native int 입출력정수읽기(int அடைவு);
    public static native void 입출력정수쓰기(int அடைவு, int மதிப்பு);
    public static native void 입출력짧은수쓰기(int அடைவு, int மதிப்பு);
    public static native int 입출력짧은수읽기(int அடைவு);
    public static native void தயார்படுத்த_பயனர்_நிரல்();
    public static native void பயனர்_அழி_உள்ளடக்கங்கள்();
    public static native int இயக்கு_பயனர்_நிரல்(int உள்ளீடு_முகவரி, int 스택주소);
    public static native int 밀리초();
    public static native int 사용자남은밀리초();
    public static native int செயல்படுத்தக்கூடிய_கோப்பு_மூட்டை();
    public static native int செயல்படுத்தக்கூடிய_கோப்பு_மூட்டை_அளவு();
    public static native int பிணையம்_நினைவகம்();
}
