// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 기계 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void писати_екран_Пел(int 가로, int 세로, int 색);
    public static native int удаљено_контрола(int 종류, int радња);
    public static native void завршити_удаљено_команда(int стање_вриједност);
    public static native void 원격대기(int стање_вриједност);
    public static native void 직렬쓰기(int вриједност);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_дозвола_ниво();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void 양보();
    public static native int 작업만들기(int индекс);
    public static native int задатак_стање(int индекс);
    public static native void стати(int стање_вриједност);
    public static native int 씨플러스시험();
    public static native int 사용자실행(int индекс);
    public static native int чек_корисник_програм();
    public static native int 인수준비(int 개수);
    public static native int 사용자파일실행();
    public static native int 리눅스파일실행();
    public static native int аргумент_бајт(int индекс, int 위치, int вриједност);
    public static native int 터미널(int радња);
    public static native int контрола_корисник_програм(int радња);
    public static native void 입출력전환(int радња);
    public static native int фајл_пријенос_услуга(int радња);
    public static native int Мрежа_стање(int унос_вриједност, int индекс);
    public static native int Мрежа_Подешавања(int радња, int адреса, int маска_вриједност, int приступни_уређај_вриједност);
    public static native int 응답보내기(int адреса, int редослијед_сортирања_вриједност);
    public static native int 응답읽기(int унос_вриједност);
    public static native int упит_систем(int унос_вриједност, int индекс);
    public static native void 전원끄기();
}
