// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 makine sınır_değer. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Pano {
    public static native int 표시화소읽기(int 가로, int Dikey_konum);
    public static native void yazma_monitör_piksel(int 가로, int Dikey_konum, int 색);
    public static native int gölge_kullanım(int Tip_değer, int Eylem);
    public static native void Bitiş_uzak_komut(int Durum_değer);
    public static native void uzak_bekle(int Durum_değer);
    public static native void 직렬쓰기(int değer);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_izin_düzey();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Dikey_konum, int 색);
    public static native void ÖDEME_CPU();
    public static native int açmak_Görev(int Dizin);
    public static native int Görev_Durum(int Dizin);
    public static native void Durdur(int Durum_değer);
    public static native int 씨플러스시험();
    public static native int çalıştırma_kullanıcı_program(int Dizin);
    public static native int çek_kullanıcı_program();
    public static native int 인수준비(int öğe_BAĞ_DEĞ_SAY);
    public static native int yürütmek_kullanıcı_Dosya();
    public static native int 리눅스파일실행();
    public static native int bağımsız_değişken_bayt(int Dizin, int konum, int değer);
    public static native int uçbirim(int Eylem);
    public static native int denetim_kullanıcı_program(int Eylem);
    public static native void 입출력전환(int Eylem);
    public static native int dosya_aktarımı_hizmet(int Eylem);
    public static native int ağ_Durum(int girdi_değer, int Dizin);
    public static native int ağ_Ayarlar(int Eylem, int ADRES, int maske_değer, int ağ_geçidi_değer);
    public static native int göndermek_cevap(int ADRES, int düzen_değer);
    public static native int 응답읽기(int girdi_değer);
    public static native int sorgu_Sistem(int girdi_değer, int Dizin);
    public static native void 전원끄기();
}
