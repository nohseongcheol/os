// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** x86 명령과 물리 አድራሻ 접근만 담당하는 컴파일러의 제한된 native 경계. */
public final class መሳሪያ_እሴት {
    public static native int ፋይል_ማስቀመጫ();
    public static native int 자바파일묶음();
    public static native int 자바파일묶음크기();
    public static native int 입출력바이트읽기(int መረጃ_ጠቆመ);
    public static native void 입출력바이트쓰기(int መረጃ_ጠቆመ, int እሴት);
    public static native int 기억읽기(int አድራሻ);
    public static native void ጻፍ_ማስቀመጫ(int አድራሻ, int እሴት);
    public static native int 부팅표식();
    public static native int 부팅정보();
    public static native int ድርድር_ጥቅም_ላይ_የዋለ();
    public static native void 잠시양보();
    public static native void 정지();
    public static native void 시험종료(int እሴት);
    public static native int 입출력정수읽기(int መረጃ_ጠቆመ);
    public static native void 입출력정수쓰기(int መረጃ_ጠቆመ, int እሴት);
    public static native void 입출력짧은수쓰기(int መረጃ_ጠቆመ, int እሴት);
    public static native int 입출력짧은수읽기(int መረጃ_ጠቆመ);
    public static native void አዘጋጅ_ተጠቃሚ_ፕሮግራም();
    public static native void ተጠቃሚ_አጽዳ_ይዞታዎች();
    public static native int አሂድ_ተጠቃሚ_ፕሮግራም(int ምዝግብ_አድራሻ, int 스택주소);
    public static native int 밀리초();
    public static native int 사용자남은밀리초();
    public static native int 실행묶음();
    public static native int 실행묶음크기();
    public static native int መረብ_ማስቀመጫ();
}
