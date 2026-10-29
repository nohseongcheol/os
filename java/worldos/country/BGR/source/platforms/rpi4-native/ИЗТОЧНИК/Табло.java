// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 машина 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Табло {
    public static native int 표시화소읽기(int 가로, int вертикал_позиция);
    public static native void записване_дисплей_пиксел(int 가로, int вертикал_позиция, int 색);
    public static native int отдалечено_управление(int 종류, int Операция);
    public static native void прекратяване_на_повикването_отдалечен_команда(int Състояние_стойност);
    public static native void отдалечен_почакай(int Състояние_стойност);
    public static native void 직렬쓰기(int стойност);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ЦП_привилегия_ниво();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int вертикал_позиция, int 색);
    public static native void преустановявам_временно_ЦП();
    public static native int Създаване_задача(int индекс);
    public static native int задача_Състояние(int индекс);
    public static native void Спиране(int Състояние_стойност);
    public static native int 씨플러스시험();
    public static native int изпълнение_потребител_програма(int индекс);
    public static native int проверявам_потребител_програма();
    public static native int 인수준비(int 개수);
    public static native int изпълнявам_потребител_Файл();
    public static native int 리눅스파일실행();
    public static native int аргумент_байт(int индекс, int Позиция, int стойност);
    public static native int Терминал(int Операция);
    public static native int контрол_потребител_програма(int Операция);
    public static native void 입출력전환(int Операция);
    public static native int прехвърляне_на_файл_услуга(int Операция);
    public static native int мрежа_статус(int запис_стойност, int индекс);
    public static native int мрежа_Настройки(int Операция, int адрес, int маска_стойност, int шлюз_стойност);
    public static native int изпращам_отговор(int адрес, int ред_стойност);
    public static native int 응답읽기(int запис_стойност);
    public static native int заявка_система(int запис_стойност, int индекс);
    public static native void 전원끄기();
}
