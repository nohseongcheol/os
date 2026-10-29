// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 компьютер 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void бичих_дэлгэц_нягтрал(int 가로, int 세로, int 색);
    public static native int сүүдэрлэлт(int 종류, int Үйлдэл);
    public static native void дуусгах_алсын_команд(int төлөв_утга);
    public static native void 원격대기(int төлөв_утга);
    public static native void 직렬쓰기(int утга);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int процессор_зөвшөөрөл_түвшин();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void түдгэлзүүлэх_процессор();
    public static native int үүсгэх_даалгавар(int индекс);
    public static native int даалгавар_төлөв(int индекс);
    public static native void Зогс(int төлөв_утга);
    public static native int 씨플러스시험();
    public static native int ажиллах_хэрэглэгч_програм(int индекс);
    public static native int чек_хэрэглэгч_програм();
    public static native int 인수준비(int 개수);
    public static native int Гүйцэтгэх_хэрэглэгч_файл();
    public static native int 리눅스파일실행();
    public static native int аргумент_байт(int индекс, int 위치, int утга);
    public static native int Терминал(int Үйлдэл);
    public static native int хяналт_хэрэглэгч_програм(int Үйлдэл);
    public static native void 입출력전환(int Үйлдэл);
    public static native int файл_дамжуулах_үйлчилгээ(int Үйлдэл);
    public static native int Сүлжээ_төлөв(int оролт_утга, int индекс);
    public static native int Сүлжээ_Тохиргоо(int Үйлдэл, int хаяг, int маск_утга, int гарц_утга);
    public static native int 응답보내기(int хаяг, int дараалал_утга);
    public static native int 응답읽기(int оролт_утга);
    public static native int асуулга_систем(int оролт_утга, int индекс);
    public static native void 전원끄기();
}
