// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 alat 전용 SVC Sambung. 기존 x86 alat 원문을 함께 빌드한다. */
public final class ruang_pengguna {
    public static native int 파일서술자열기(int[] Nama, int Tetapan);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Nama, int[] data);
    public static native int tulis_fail(int[] Nama, int[] data, int kepanjangan_VALUE);
    public static native int Tulis(String Teks);
    public static native int tulis_aksara_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Aksi, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Teks, int kepanjangan_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int strim_kawalan(int Aksi, int 서술자, int VALUE);
    public static native int CONNECT_strim(int 서술자, int e_mel, int port_VALUE);
    public static native int buka_rangkaian(int port_VALUE);
    public static native int e_mel_rangkaian(int 서술자, int e_mel, int port_VALUE, int[] data, int kepanjangan_VALUE);
    public static native int 통신받기(int 서술자, int[] data, int kepanjangan_VALUE);
    public static native int rangkaian_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int segi_empat_tepat(int 가로, int Menegak_jawatan, int 폭, int 높이, int 색);
}
