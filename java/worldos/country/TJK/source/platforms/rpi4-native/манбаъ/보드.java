// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 компютер 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void навиштан_дисплей_пиксел(int 가로, int 세로, int 색);
    public static native int сояандоз(int 종류, int Амал);
    public static native void анҷом_додан_дурдаст_фармон(int вазъият_қимат);
    public static native void 원격대기(int вазъият_қимат);
    public static native void 직렬쓰기(int қимат);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void боздоштан_просессор();
    public static native int эҷод_кардан_вазифа(int индекс);
    public static native int вазифа_вазъият(int индекс);
    public static native void қатъ_кардан(int вазъият_қимат);
    public static native int 씨플러스시험();
    public static native int порча_корбар_барнома(int индекс);
    public static native int санҷиш_корбар_барнома();
    public static native int 인수준비(int 개수);
    public static native int иҷро_кардан_корбар_файл();
    public static native int 리눅스파일실행();
    public static native int аргумент_байт(int индекс, int 위치, int қимат);
    public static native int 터미널(int Амал);
    public static native int идоракунӣ_корбар_барнома(int Амал);
    public static native void 입출력전환(int Амал);
    public static native int файл_интиқол_хидмат(int Амал);
    public static native int Шабака_вазъият(int ворида_қимат, int индекс);
    public static native int Шабака_Танзимот(int Амал, int суроға, int 가림, int 관문);
    public static native int 응답보내기(int суроға, int тартиб_қимат);
    public static native int 응답읽기(int ворида_қимат);
    public static native int ковиш_система(int ворида_қимат, int индекс);
    public static native void 전원끄기();
}
