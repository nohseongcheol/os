// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 машина 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class табла {
    public static native int 표시화소읽기(int 가로, int вертикала_позиционирање);
    public static native void запиши_екран_пиксел(int 가로, int вертикала_позиционирање, int 색);
    public static native int набљудување(int 종류, int Дејство);
    public static native void крај_далечинскo_наредба(int статус_VALUE);
    public static native void далечинскo_почекај(int статус_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ЦПУ_дозвола_ниво();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int вертикала_позиционирање, int 색);
    public static native void YIELD_ЦПУ();
    public static native int Create_задача(int INDEX);
    public static native int задача_статус(int INDEX);
    public static native void Стоп(int статус_VALUE);
    public static native int 씨플러스시험();
    public static native int изврши_корисник_програма(int INDEX);
    public static native int провери_корисник_програма();
    public static native int 인수준비(int ставка_COUNT);
    public static native int Изврши_корисник_датотека();
    public static native int 리눅스파일실행();
    public static native int аргумент_бајт(int INDEX, int Позиција, int VALUE);
    public static native int Терминал(int Дејство);
    public static native int контрола_корисник_програма(int Дејство);
    public static native void 입출력전환(int Дејство);
    public static native int датотека_пренос_услуга(int Дејство);
    public static native int Мрежа_статус(int внес_VALUE, int INDEX);
    public static native int Мрежа_Параметри(int Дејство, int адреса, int маска_VALUE, int капија_VALUE);
    public static native int 응답보내기(int адреса, int редослед_VALUE);
    public static native int 응답읽기(int внес_VALUE);
    public static native int прашалник_систем(int внес_VALUE, int INDEX);
    public static native void 전원끄기();
}
