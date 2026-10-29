// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 mesin 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Papan {
    public static native int 표시화소읽기(int 가로, int Vertikal_posisi);
    public static native void tulis_tampilan_elgam(int 가로, int Vertikal_posisi, int 색);
    public static native int bayangan(int 종류, int Aksi);
    public static native void mengakhiri_jarak_jauh_perintah(int Status_VALUE);
    public static native void jarak_jauh_tunggu(int Status_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_izin_tingkat();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Vertikal_posisi, int 색);
    public static native void YIELD_CPU();
    public static native int Buat_tugas(int INDEX);
    public static native int tugas_Status(int INDEX);
    public static native void Hentikan(int Status_VALUE);
    public static native int 씨플러스시험();
    public static native int eksekusi_pengguna_apl(int INDEX);
    public static native int cek_pengguna_apl();
    public static native int 인수준비(int item_COUNT);
    public static native int Jalankan_pengguna_file();
    public static native int 리눅스파일실행();
    public static native int argumen_byte(int INDEX, int posisi, int VALUE);
    public static native int terminal(int Aksi);
    public static native int kontrol_pengguna_apl(int Aksi);
    public static native void 입출력전환(int Aksi);
    public static native int transfer_file_layanan(int Aksi);
    public static native int jaringan_status(int entri_VALUE, int INDEX);
    public static native int jaringan_Pengaturan(int Aksi, int surel, int masker_VALUE, int gateway_VALUE);
    public static native int kirim_respons(int surel, int urutan_VALUE);
    public static native int 응답읽기(int entri_VALUE);
    public static native int kueri_sistem(int entri_VALUE, int INDEX);
    public static native void 전원끄기();
}
