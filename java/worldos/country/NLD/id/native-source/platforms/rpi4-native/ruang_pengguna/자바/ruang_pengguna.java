// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 alat 전용 SVC Sambung. 기존 x86 alat 원문을 함께 빌드한다. */
public final class ruang_pengguna {
    public static native int 파일서술자열기(int[] Nama_2, int Konfigurasi);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Nama_2, int[] data);
    public static native int tulis_file(int[] Nama_2, int[] data, int panjang_VALUE);
    public static native int Tulis(String teks);
    public static native int tulis_karakter_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String argumen(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Aksi, int INDEX, int 가, int SECOND_operand, int 다, int 라);
    public static native int 화면글(int INDEX, int[] teks, int panjang_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_kontrol(int Aksi, int 서술자, int VALUE);
    public static native int CONNECT_Stream(int 서술자, int surel, int port_VALUE);
    public static native int buat_jaringan(int port_VALUE);
    public static native int kirim_jaringan(int 서술자, int surel, int port_VALUE, int[] data, int panjang_VALUE);
    public static native int terima_jaringan(int 서술자, int[] data, int panjang_VALUE);
    public static native int jaringan_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int persegi(int 가로, int Vertikal_posisi, int 폭, int 높이, int 색);
}
