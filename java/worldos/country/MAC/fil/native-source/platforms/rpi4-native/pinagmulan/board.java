// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 machine 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class board {
    public static native int 표시화소읽기(int 가로, int archive_posisyon);
    public static native void sumulat_display_pel(int 가로, int archive_posisyon, int 색);
    public static native int pag_shadow(int 종류, int aksyon);
    public static native void tapusin_malayuan_utos(int katayuan_VALUE);
    public static native void malayuan_maghintay(int katayuan_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_pahintulot_antas();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int archive_posisyon, int 색);
    public static native void YIELD_CPU();
    public static native int Create_gawain(int INDEX);
    public static native int gawain_katayuan(int INDEX);
    public static native void Hinto(int katayuan_VALUE);
    public static native int 씨플러스시험();
    public static native int run_gumagamit_app(int INDEX);
    public static native int tseke_gumagamit_app();
    public static native int 인수준비(int item_COUNT);
    public static native int Mag_execute_gumagamit_file();
    public static native int 리눅스파일실행();
    public static native int argumento_byte(int INDEX, int posisyon, int VALUE);
    public static native int Terminal(int aksyon);
    public static native int control_gumagamit_app(int aksyon);
    public static native void 입출력전환(int aksyon);
    public static native int file_lipat_serbisyo(int aksyon);
    public static native int Network_katayuan(int pagpasok_VALUE, int INDEX);
    public static native int Network_Mga_Setting(int aksyon, int email, int mask_VALUE, int entrada_VALUE);
    public static native int 응답보내기(int email, int pagkakasunud_sunod_VALUE);
    public static native int 응답읽기(int pagpasok_VALUE);
    public static native int query_system(int pagpasok_VALUE, int INDEX);
    public static native void 전원끄기();
}
