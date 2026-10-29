// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ruang_pengguna ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ruang_pengguna {
    public static native int 파일서술자열기(int[] file_entri_nama, int buat_Pengaturan);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int penerapan_Files(int 파일서술자);
    public static native int 파일읽기(int[] Nama_2, int[] data);
    public static native int tulis_karakter_VALUE(int 문자);
    public static native int tulis_file(int[] Nama_2, int[] data, int panjang_VALUE);
    public static native int Tulis(String Isi_VALUE);
    public static native int 인수개수();
    public static native String argumen(int INDEX);
    public static native int 실행권한();
    public static native int buat_jaringan(int lokal_port);
    public static native int kirim_data(int handel_VALUE, int surel, int tujuan_port, int[] data, int panjang_VALUE);
    public static native int Data_Penerimaan(int handel_VALUE, int[] data, int 제한밀리초);
    public static native int Tutup_jaringan(int handel_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int handel_VALUE);
    public static native int 보낸창구(int handel_VALUE);
}
