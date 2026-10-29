// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** x86 명령과 물리 Adress 접근만 담당하는 컴파일러의 제한된 native gräns_värde. */
public final class enhet_värde {
    public static native int fil_Minne();
    public static native int 자바파일묶음();
    public static native int 자바파일묶음크기();
    public static native int 입출력바이트읽기(int INDEX);
    public static native void 입출력바이트쓰기(int INDEX, int värde);
    public static native int läsa_Minne(int Adress);
    public static native void skriva_Minne(int Adress, int värde);
    public static native int 부팅표식();
    public static native int 부팅정보();
    public static native int MATRIS_användning();
    public static native void 잠시양보();
    public static native void 정지();
    public static native void slut_test(int värde);
    public static native int 입출력정수읽기(int INDEX);
    public static native void 입출력정수쓰기(int INDEX, int värde);
    public static native void 입출력짧은수쓰기(int INDEX, int värde);
    public static native int 입출력짧은수읽기(int INDEX);
    public static native void Förbereda_användare_app();
    public static native void användare_rensa_Innehåll();
    public static native int köra_användare_app(int post_ADRESS, int operand_Stack_ADRESS);
    public static native int 밀리초();
    public static native int 사용자남은밀리초();
    public static native int körbar_fil_bunt();
    public static native int körbar_fil_bunt_storlek();
    public static native int nätverk_Minne();
}
