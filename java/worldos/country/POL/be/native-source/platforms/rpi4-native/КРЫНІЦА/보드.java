// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 камп_ютар 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void напісаць_дысплэй_пэл(int 가로, int 세로, int 색);
    public static native int ценявое_капіяванне(int 종류, int Дзеянне);
    public static native void скончыць_аддалены_каманда(int стан_значэнне);
    public static native void аддалены_чакае(int стан_значэнне);
    public static native void 직렬쓰기(int значэнне);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int працэсар_дазвол_узровень();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void прыпыніць_працэсар();
    public static native int стварыць_задача(int індэкс);
    public static native int задача_стан(int індэкс);
    public static native void Спыніць(int стан_значэнне);
    public static native int 씨플러스시험();
    public static native int паток_карыстальнік_праграма(int індэкс);
    public static native int чэк_карыстальнік_праграма();
    public static native int 인수준비(int 개수);
    public static native int выканаць_карыстальнік_файл();
    public static native int 리눅스파일실행();
    public static native int аргумент_байт(int індэкс, int Пазіцыя, int значэнне);
    public static native int Тэрмінал(int Дзеянне);
    public static native int кіраванне_карыстальнік_праграма(int Дзеянне);
    public static native void 입출력전환(int Дзеянне);
    public static native int файл_перанос_служба(int Дзеянне);
    public static native int Сетка_стан(int увядзенне_значэнне, int індэкс);
    public static native int Сетка_Налады(int Дзеянне, int адрас, int 가림, int 관문);
    public static native int 응답보내기(int адрас, int парадак_значэнне);
    public static native int 응답읽기(int увядзенне_значэнне);
    public static native int запыт_сістэма(int увядзенне_значэнне, int індэкс);
    public static native void 전원끄기();
}
