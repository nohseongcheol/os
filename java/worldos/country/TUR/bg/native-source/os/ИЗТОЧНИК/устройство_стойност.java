// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** x86 명령과 물리 адрес 접근만 담당하는 컴파일러의 제한된 native 경계. */
public final class устройство_стойност {
    public static native int Файл_Памет();
    public static native int 자바파일묶음();
    public static native int 자바파일묶음크기();
    public static native int 입출력바이트읽기(int индекс);
    public static native void 입출력바이트쓰기(int индекс, int стойност);
    public static native int 기억읽기(int адрес);
    public static native void записване_Памет(int адрес, int стойност);
    public static native int 부팅표식();
    public static native int 부팅정보();
    public static native int масив_употреба();
    public static native void 잠시양보();
    public static native void 정지();
    public static native void 시험종료(int стойност);
    public static native int 입출력정수읽기(int индекс);
    public static native void 입출력정수쓰기(int индекс, int стойност);
    public static native void 입출력짧은수쓰기(int индекс, int стойност);
    public static native int 입출력짧은수읽기(int индекс);
    public static native void Подготвяне_потребител_програма();
    public static native void потребител_изчиствам_Съдържание();
    public static native int изпълнение_потребител_програма(int запис_адрес, int операнд_стек_адрес);
    public static native int 밀리초();
    public static native int 사용자남은밀리초();
    public static native int 실행묶음();
    public static native int 실행묶음크기();
    public static native int мрежа_Памет();
}
