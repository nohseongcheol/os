// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** x86 명령과 물리 ADRES 접근만 담당하는 컴파일러의 제한된 native sınır_değer. */
public final class cihaz_değer {
    public static native int Dosya_Bellek();
    public static native int 자바파일묶음();
    public static native int 자바파일묶음크기();
    public static native int 입출력바이트읽기(int Dizin);
    public static native void 입출력바이트쓰기(int Dizin, int değer);
    public static native int 기억읽기(int ADRES);
    public static native void yazma_Bellek(int ADRES, int değer);
    public static native int 부팅표식();
    public static native int 부팅정보();
    public static native int DİZİ_kullanım();
    public static native void 잠시양보();
    public static native void 정지();
    public static native void Son_test(int değer);
    public static native int 입출력정수읽기(int Dizin);
    public static native void 입출력정수쓰기(int Dizin, int değer);
    public static native void 입출력짧은수쓰기(int Dizin, int değer);
    public static native int 입출력짧은수읽기(int Dizin);
    public static native void Hazırlan_kullanıcı_program();
    public static native void kullanıcı_takas_içindekiler();
    public static native int çalıştırma_kullanıcı_program(int girdi_ADRES, int işlenen_Yığın_ADRES);
    public static native int 밀리초();
    public static native int 사용자남은밀리초();
    public static native int yürütülebilir_paket_iş();
    public static native int yürütülebilir_paket_iş_boyutlandırmak();
    public static native int ağ_Bellek();
}
