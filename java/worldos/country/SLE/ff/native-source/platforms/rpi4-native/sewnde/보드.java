// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 기계 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void winndude_jaytino_piksel(int 가로, int 세로, int 색);
    public static native int 원격제어(int 종류, int gollal);
    public static native void 원격명령끝(int ngonka_njaru);
    public static native void 원격대기(int ngonka_njaru);
    public static native void 직렬쓰기(int njaru);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void 양보();
    public static native int 작업만들기(int joopirdu);
    public static native int golle_ngonka(int joopirdu);
    public static native void dartinde(int ngonka_njaru);
    public static native int 씨플러스시험();
    public static native int huutoraade_kuutoro_tafirde(int joopirdu);
    public static native int sek_kuutoro_tafirde();
    public static native int 인수준비(int 개수);
    public static native int 사용자파일실행();
    public static native int 리눅스파일실행();
    public static native int hujja_oktee(int joopirdu, int 위치, int njaru);
    public static native int 터미널(int gollal);
    public static native int yuurnitorde_kuutoro_tafirde(int gollal);
    public static native void 입출력전환(int gollal);
    public static native int fiilde_egginde_carwol(int gollal);
    public static native int laylaytol_ngonka(int naatnugol_njaru, int joopirdu);
    public static native int 망설정(int gollal, int ñiiɓirde, int 가림, int 관문);
    public static native int 응답보내기(int ñiiɓirde, int deggondiral_njaru);
    public static native int 응답읽기(int naatnugol_njaru);
    public static native int ɗaɓɓal_yuɓɓo(int naatnugol_njaru, int joopirdu);
    public static native void 전원끄기();
}
