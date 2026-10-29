// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 imashini 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void kwandika_kwerekana_pel(int 가로, int 세로, int 색);
    public static native int icengera(int 종류, int Igikorwa);
    public static native void kurangiza_kure_ibwiriza(int imimerere_agaciro);
    public static native void 원격대기(int imimerere_agaciro);
    public static native void 직렬쓰기(int agaciro);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void gusubika_CPU();
    public static native int kurema_umukoro(int umugerekashakiro);
    public static native int umukoro_imimerere(int umugerekashakiro);
    public static native void Guhagarara(int imimerere_agaciro);
    public static native int 씨플러스시험();
    public static native int ihuriro_ukoresha_porogaramu(int umugerekashakiro);
    public static native int sheki_ukoresha_porogaramu();
    public static native int 인수준비(int 개수);
    public static native int gukora_ukoresha_dosiye();
    public static native int 리눅스파일실행();
    public static native int ingingo_bayiti(int umugerekashakiro, int 위치, int agaciro);
    public static native int 터미널(int Igikorwa);
    public static native int icunga_ukoresha_porogaramu(int Igikorwa);
    public static native void 입출력전환(int Igikorwa);
    public static native int dosiye_iyimura_serivisi(int Igikorwa);
    public static native int Urusobemiyoboro_imimerere(int icyinjizwa_agaciro, int umugerekashakiro);
    public static native int Urusobemiyoboro_Amagenamiterere(int Igikorwa, int aderesi, int masiki_agaciro, int muhuzaporotokore_agaciro);
    public static native int 응답보내기(int aderesi, int umujyo_agaciro);
    public static native int 응답읽기(int icyinjizwa_agaciro);
    public static native int isaba_sisitemu(int icyinjizwa_agaciro, int umugerekashakiro);
    public static native void 전원끄기();
}
