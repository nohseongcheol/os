// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 рачунар 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Табла {
    public static native int 표시화소읽기(int 가로, int вертикала_позиција);
    public static native void писати_екран_пиксел(int 가로, int вертикала_позиција, int 색);
    public static native int даљинска_контрола(int 종류, int радња);
    public static native void завршити_удаљен_команда(int стање_вриједност);
    public static native void удаљен_чекај(int стање_вриједност);
    public static native void 직렬쓰기(int вриједност);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int процесор_дозвола_ниво();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int вертикала_позиција, int 색);
    public static native void обуставити_процесор();
    public static native int Направи_задатак(int индекс);
    public static native int задатак_стање(int индекс);
    public static native void Заустави(int стање_вриједност);
    public static native int 씨플러스시험();
    public static native int низ_корисник_програм(int индекс);
    public static native int чек_корисник_програм();
    public static native int 인수준비(int 개수);
    public static native int Изврши_корисник_фајл();
    public static native int 리눅스파일실행();
    public static native int аргумент_бајт(int индекс, int Положај, int вриједност);
    public static native int Терминал(int радња);
    public static native int контрола_корисник_програм(int радња);
    public static native void 입출력전환(int радња);
    public static native int фајл_пренос_услуга(int радња);
    public static native int Мрежа_стање(int унос_вриједност, int индекс);
    public static native int Мрежа_Поставке(int радња, int адреса, int маска_вриједност, int мрежни_пролаз_вриједност);
    public static native int послати_одговор(int адреса, int поредати_вриједност);
    public static native int 응답읽기(int унос_вриједност);
    public static native int упит_систем(int унос_вриједност, int индекс);
    public static native void 전원끄기();
}
