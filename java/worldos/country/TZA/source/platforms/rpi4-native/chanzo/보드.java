// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 mashine 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void andika_onyesha_elepi(int 가로, int 세로, int 색);
    public static native int mtagusano(int 종류, int Kitendo);
    public static native void tamatia_kwa_mbali_amri(int hali_thamani);
    public static native void kwa_mbali_subiri(int hali_thamani);
    public static native void 직렬쓰기(int thamani);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_kibali_kiwango();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void ahirisha_CPU();
    public static native int unda_kazi(int kielezo);
    public static native int kazi_hali(int kielezo);
    public static native void Simama(int hali_thamani);
    public static native int 씨플러스시험();
    public static native int endesha_mtumiaji_programu(int kielezo);
    public static native int hundi_mtumiaji_programu();
    public static native int 인수준비(int 개수);
    public static native int tekeleza_mtumiaji_faili();
    public static native int 리눅스파일실행();
    public static native int hoja_baiti(int kielezo, int 위치, int thamani);
    public static native int 터미널(int Kitendo);
    public static native int udhibiti_mtumiaji_programu(int Kitendo);
    public static native void 입출력전환(int Kitendo);
    public static native int faili_hamisha_huduma(int Kitendo);
    public static native int Mtandao_hali(int ingizo_thamani, int kielezo);
    public static native int Mtandao_Mipangilio(int Kitendo, int anwani, int barakoa_thamani, int kichanganishi_mtandao_thamani);
    public static native int 응답보내기(int anwani, int mpangilio_thamani);
    public static native int 응답읽기(int ingizo_thamani);
    public static native int uliza_mfumo(int ingizo_thamani, int kielezo);
    public static native void 전원끄기();
}
