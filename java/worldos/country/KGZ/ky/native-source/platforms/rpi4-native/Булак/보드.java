// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 машина 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void жазуу_дисплей_пиксел(int 가로, int 세로, int 색);
    public static native int көлөкө(int 종류, int Аракети);
    public static native void аяктоо_алыскы_буйрук(int абал_маани);
    public static native void 원격대기(int абал_маани);
    public static native void 직렬쓰기(int маани);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int процессор_уруксат_деңгээл();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void токтотуу_процессор();
    public static native int түзүү_маселе(int индекс);
    public static native int маселе_абал(int индекс);
    public static native void Токтотуу(int абал_маани);
    public static native int 씨플러스시험();
    public static native int топтом_колдонуучу_програм(int индекс);
    public static native int чек_колдонуучу_програм();
    public static native int 인수준비(int 개수);
    public static native int аткаруу_колдонуучу_файл();
    public static native int 리눅스파일실행();
    public static native int аргумент_байт(int индекс, int Турган_жери, int маани);
    public static native int Терминал(int Аракети);
    public static native int башкаруу_колдонуучу_програм(int Аракети);
    public static native void 입출력전환(int Аракети);
    public static native int файл_ташүү_кызмат(int Аракети);
    public static native int Желе_абал(int киргизме_жазуу_маани, int индекс);
    public static native int Желе_Орнотуулар(int Аракети, int дарек, int маска_маани, int шлюз_маани);
    public static native int 응답보내기(int дарек, int ылгоо_ирети_маани);
    public static native int 응답읽기(int киргизме_жазуу_маани);
    public static native int сурам_тутум(int киргизме_жазуу_маани, int индекс);
    public static native void 전원끄기();
}
