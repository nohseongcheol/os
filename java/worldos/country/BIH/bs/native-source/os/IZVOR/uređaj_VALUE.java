// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** x86 명령과 물리 adresa 접근만 담당하는 컴파일러의 제한된 native 경계. */
public final class uređaj_VALUE {
    public static native int fajl_Memorija();
    public static native int 자바파일묶음();
    public static native int 자바파일묶음크기();
    public static native int 입출력바이트읽기(int INDEX);
    public static native void 입출력바이트쓰기(int INDEX, int VALUE);
    public static native int 기억읽기(int adresa);
    public static native void pisati_Memorija(int adresa, int VALUE);
    public static native int 부팅표식();
    public static native int 부팅정보();
    public static native int niz_potrošnja();
    public static native void 잠시양보();
    public static native void 정지();
    public static native void 시험종료(int VALUE);
    public static native int 입출력정수읽기(int INDEX);
    public static native void 입출력정수쓰기(int INDEX, int VALUE);
    public static native void 입출력짧은수쓰기(int INDEX, int VALUE);
    public static native int 입출력짧은수읽기(int INDEX);
    public static native void Pripremiti_korisnik_program();
    public static native void korisnik_obrisati_TOC();
    public static native int niz_korisnik_program(int unos_adresa, int operand_snop_adresa);
    public static native int 밀리초();
    public static native int 사용자남은밀리초();
    public static native int 실행묶음();
    public static native int 실행묶음크기();
    public static native int Mreža_Memorija();
}
