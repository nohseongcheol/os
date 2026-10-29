// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 motšhene 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void ngwala_bontšha_phele(int 가로, int 세로, int 색);
    public static native int kekišo(int 종류, int Mogato);
    public static native void fetša_ya_kgole_taelo(int boemo_boleng);
    public static native void 원격대기(int boemo_boleng);
    public static native void 직렬쓰기(int boleng);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_tumelelo_kgato();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void e_thibetšwe_CPU();
    public static native int 작업만들기(int lokela);
    public static native int mošomo_boemo(int lokela);
    public static native void Emiša(int boemo_boleng);
    public static native int 씨플러스시험();
    public static native int sepetša_mošomiši_tirišo(int lokela);
    public static native int lekola_mošomiši_tirišo();
    public static native int 인수준비(int 개수);
    public static native int phethagatša_mošomiši_faele();
    public static native int 리눅스파일실행();
    public static native int akumente_paete(int lokela, int 위치, int boleng);
    public static native int 터미널(int Mogato);
    public static native int taolo_mošomiši_tirišo(int Mogato);
    public static native void 입출력전환(int Mogato);
    public static native int faele_fetišetša_tirelo(int Mogato);
    public static native int Netweke_boemo(int go_tsenya_tshedimošo_boleng, int lokela);
    public static native int Netweke_Dipeakanyo(int Mogato, int atrese, int maseke_boleng, int tsela_ya_netweke_boleng);
    public static native int 응답보내기(int atrese, int thulaganyo_boleng);
    public static native int 응답읽기(int go_tsenya_tshedimošo_boleng);
    public static native int kwiri_lenaneo(int go_tsenya_tshedimošo_boleng, int lokela);
    public static native void 전원끄기();
}
