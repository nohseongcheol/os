// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 기계 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void ليکل_ښوون_پکسل(int 가로, int 세로, int 색);
    public static native int 원격제어(int 종류, int چار);
    public static native void 원격명령끝(int انکړ_ارزښت);
    public static native void 원격대기(int انکړ_ارزښت);
    public static native void 직렬쓰기(int ارزښت);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void 양보();
    public static native int 작업만들기(int لړیال);
    public static native int دنده_انکړ(int لړیال);
    public static native void تمول(int انکړ_ارزښت);
    public static native int 씨플러스시험();
    public static native int 사용자실행(int لړیال);
    public static native int کتل_کارن_کاريال();
    public static native int 인수준비(int 개수);
    public static native int 사용자파일실행();
    public static native int 리눅스파일실행();
    public static native int ارزښتوړى_بايټ(int لړیال, int ځای, int ارزښت);
    public static native int پايالی(int چار);
    public static native int مهار_کارن_کاريال(int چار);
    public static native void 입출력전환(int چار);
    public static native int دوتنه_لېږدول_پالنه(int چار);
    public static native int جال_انکړ(int ننوت_ارزښت, int لړیال);
    public static native int 망설정(int چار, int پته, int وربوزۍ_ارزښت, int ورلار_ارزښت);
    public static native int 응답보내기(int پته, int اڼن_اوډون_ارزښت);
    public static native int 응답읽기(int ننوت_ارزښت);
    public static native int پوښتنه_غونډال(int ننوت_ارزښت, int لړیال);
    public static native void 전원끄기();
}
