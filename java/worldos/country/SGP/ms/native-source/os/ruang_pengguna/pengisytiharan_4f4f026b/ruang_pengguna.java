// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ruang_pengguna ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ruang_pengguna {
    public static native int 파일서술자열기(int[] fail_pemasukan_nama, int buka_Seting);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bait_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int lakukan_storan_fail(int 파일서술자);
    public static native int 파일읽기(int[] Nama, int[] data);
    public static native int tulis_aksara_VALUE(int 문자);
    public static native int tulis_fail(int[] Nama, int[] data, int kepanjangan_VALUE);
    public static native int Tulis(String Kandungan_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int buka_rangkaian(int setempat_port);
    public static native int e_mel_data_5b5410b2(int pemegang_VALUE, int e_mel, int destinasi_port, int[] data, int kepanjangan_VALUE);
    public static native int 자료받기(int pemegang_VALUE, int[] data, int 제한밀리초);
    public static native int Tutup_rangkaian(int pemegang_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int pemegang_VALUE);
    public static native int 보낸창구(int pemegang_VALUE);
}
