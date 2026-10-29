// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 motšhine 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void kwala_bontsha_phele(int 가로, int 세로, int 색);
    public static native int ritifatsa(int 종류, int tiro);
    public static native void kgaola_kgakala_Taelo(int kemo_Boleng);
    public static native void 원격대기(int kemo_Boleng);
    public static native void 직렬쓰기(int Boleng);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_tetla_Maemo();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void emisa_ka_nakwana_CPU();
    public static native int tlhama_Tiro(int tshupane);
    public static native int Tiro_kemo(int tshupane);
    public static native void emisa(int kemo_Boleng);
    public static native int 씨플러스시험();
    public static native int dirisa_modirisi_Tiriso(int tshupane);
    public static native int tlhola_modirisi_Tiriso();
    public static native int 인수준비(int 개수);
    public static native int diragatsa_modirisi_faele();
    public static native int 리눅스파일실행();
    public static native int Thulaganyo_baete(int tshupane, int 위치, int Boleng);
    public static native int 터미널(int tiro);
    public static native int taolo_modirisi_Tiriso(int tiro);
    public static native void 입출력전환(int tiro);
    public static native int faele_fudusa_Tirelo(int tiro);
    public static native int Neteweke_kemo(int tsenyo_Boleng, int tshupane);
    public static native int Neteweke_Diseting(int tiro, int aterese, int mmaseke_Boleng, int kgorotsamaiso_Boleng);
    public static native int 응답보내기(int aterese, int thulaganyo_Boleng);
    public static native int 응답읽기(int tsenyo_Boleng);
    public static native int fenenkolola_tsamaiso(int tsenyo_Boleng, int tshupane);
    public static native void 전원끄기();
}
