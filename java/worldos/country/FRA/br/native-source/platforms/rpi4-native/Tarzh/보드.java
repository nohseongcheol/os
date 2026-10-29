// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 기계 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void 표시화소쓰기(int 가로, int 세로, int 색);
    public static native int 원격제어(int 종류, int Gwezhiad);
    public static native void 원격명령끝(int 상태);
    public static native void 원격대기(int 상태);
    public static native void 직렬쓰기(int 값);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void 양보();
    public static native int 작업만들기(int 번호);
    public static native int 작업상태(int 번호);
    public static native void Harz(int 상태);
    public static native int 씨플러스시험();
    public static native int 사용자실행(int 번호);
    public static native int 사용자검사();
    public static native int 인수준비(int 개수);
    public static native int 사용자파일실행();
    public static native int 리눅스파일실행();
    public static native int 인수바이트(int 번호, int Lec_hiadur, int 값);
    public static native int Termenell(int Gwezhiad);
    public static native int 사용자제어(int Gwezhiad);
    public static native void 입출력전환(int Gwezhiad);
    public static native int 파일전송서비스(int Gwezhiad);
    public static native int 망상태(int 항목, int 번호);
    public static native int 망설정(int Gwezhiad, int 주소, int 가림, int 관문);
    public static native int 응답보내기(int 주소, int 순서);
    public static native int 응답읽기(int 항목);
    public static native int 체계조회(int 항목, int 번호);
    public static native void 전원끄기();
}
