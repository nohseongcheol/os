// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** x86 명령과 물리 адреса 접근만 담당하는 컴파일러의 제한된 native 경계. */
public final class уређај_вриједност {
    public static native int фајл_меморија();
    public static native int 자바파일묶음();
    public static native int 자바파일묶음크기();
    public static native int 입출력바이트읽기(int индекс);
    public static native void 입출력바이트쓰기(int индекс, int вриједност);
    public static native int 기억읽기(int адреса);
    public static native void писати_меморија(int адреса, int вриједност);
    public static native int 부팅표식();
    public static native int 부팅정보();
    public static native int низ_потрошња();
    public static native void 잠시양보();
    public static native void 정지();
    public static native void 시험종료(int вриједност);
    public static native int 입출력정수읽기(int индекс);
    public static native void 입출력정수쓰기(int индекс, int вриједност);
    public static native void 입출력짧은수쓰기(int индекс, int вриједност);
    public static native int 입출력짧은수읽기(int индекс);
    public static native void Припремити_корисник_програм();
    public static native void корисник_избрисати_TOC();
    public static native int 사용자실행(int унос_адреса, int 스택주소);
    public static native int 밀리초();
    public static native int 사용자남은밀리초();
    public static native int 실행묶음();
    public static native int 실행묶음크기();
    public static native int Мрежа_меморија();
}
