// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 ngwa_komputa 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void dee_gosịpụta_pel(int 가로, int 세로, int 색);
    public static native int njizi_dị̀anyā(int 종류, int mmèm);
    public static native void mèdebe_ebe_dị̀anyā_nnyemiwu(int ọnọdụ_valuu);
    public static native void 원격대기(int ọnọdụ_valuu);
    public static native void 직렬쓰기(int valuu);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_ikikere_làrìì();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void kwụsịtụ_CPU();
    public static native int mepụta_ọrụ(int indèks);
    public static native int ọrụ_ọnọdụ(int indèks);
    public static native void Kwụsị(int ọnọdụ_valuu);
    public static native int 씨플러스시험();
    public static native int mee_òjìàrụ_app(int indèks);
    public static native int cheèk_òjìàrụ_app();
    public static native int 인수준비(int 개수);
    public static native int mee_òjìàrụ_ọbọakwụkwọ();
    public static native int 리눅스파일실행();
    public static native int agụment_baịtị(int indèks, int 위치, int valuu);
    public static native int 터미널(int mmèm);
    public static native int njizi_òjìàrụ_app(int mmèm);
    public static native void 입출력전환(int mmèm);
    public static native int ọbọakwụkwọ_dògharịa_ọrụ(int mmèm);
    public static native int Netwọọkụ_ọnọdụ(int ndebà_valuu, int indèks);
    public static native int Netwọọkụ_Mwube(int mmèm, int àdreèsì, int mkpù_valuu, int ụzọmbànye_valuu);
    public static native int 응답보내기(int àdreèsì, int ùsòrò_valuu);
    public static native int 응답읽기(int ndebà_valuu);
    public static native int mgbaajụjụ_sistèm(int ndebà_valuu, int indèks);
    public static native void 전원끄기();
}
