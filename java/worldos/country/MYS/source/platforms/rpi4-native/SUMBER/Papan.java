// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 mesin 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Papan {
    public static native int 표시화소읽기(int 가로, int Menegak_jawatan);
    public static native void tulis_papar_pel(int 가로, int Menegak_jawatan, int 색);
    public static native int pembayangan(int 종류, int Aksi);
    public static native void tamat_jauh_perintah(int status_VALUE);
    public static native void jauh_tunggu(int status_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_keizinan_aras();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Menegak_jawatan, int 색);
    public static native void YIELD_CPU();
    public static native int cipta_tugas(int INDEX);
    public static native int tugas_status(int INDEX);
    public static native void Henti(int status_VALUE);
    public static native int 씨플러스시험();
    public static native int jalankan_pengguna_aplikasi(int INDEX);
    public static native int cek_pengguna_aplikasi();
    public static native int 인수준비(int item_COUNT);
    public static native int laksanakan_pengguna_fail();
    public static native int 리눅스파일실행();
    public static native int argumen_bait(int INDEX, int Kedudukan, int VALUE);
    public static native int Terminal(int Aksi);
    public static native int kawalan_pengguna_aplikasi(int Aksi);
    public static native void 입출력전환(int Aksi);
    public static native int pemindahan_fail_khidmat(int Aksi);
    public static native int rangkaian_status(int pemasukan_VALUE, int INDEX);
    public static native int rangkaian_Seting(int Aksi, int e_mel, int topeng_VALUE, int get_laluan_VALUE);
    public static native int e_mel_respons(int e_mel, int tertib_VALUE);
    public static native int 응답읽기(int pemasukan_VALUE);
    public static native int pertanyaan_sistem(int pemasukan_VALUE, int INDEX);
    public static native void 전원끄기();
}
