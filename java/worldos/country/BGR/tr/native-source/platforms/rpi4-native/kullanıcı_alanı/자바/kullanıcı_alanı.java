// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 araçlar 전용 SVC Bağlan. 기존 x86 araçlar 원문을 함께 빌드한다. */
public final class kullanıcı_alanı {
    public static native int açık_Dosya_tanımlayıcı(int[] İsim, int Ayarlar);
    public static native int 파일한바이트읽기(int tanımlayıcı_girdi);
    public static native int 파일한바이트쓰기(int tanımlayıcı_girdi, int değer);
    public static native int Kapat_Dosya_tanımlayıcı(int tanımlayıcı_girdi);
    public static native int 파일읽기(int[] İsim, int[] veri);
    public static native int yazma_Dosya(int[] İsim, int[] veri, int süre_değer);
    public static native int Yazma(String metin);
    public static native int yazma_karakter_değer(int değer);
    public static native int 인수개수();
    public static native String bağımsız_değişkenler(int Dizin);
    public static native int 도구번호();
    public static native int 화면연결(int Eylem, int Dizin, int 가, int SANİYE_işlenen, int 다, int 라);
    public static native int 화면글(int Dizin, int[] metin, int süre_değer);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int akış_denetim(int Eylem, int tanımlayıcı_girdi, int değer);
    public static native int bağla_akış(int tanımlayıcı_girdi, int ADRES, int taşımak_değer);
    public static native int açık_ağ(int taşımak_değer);
    public static native int göndermek_ağ(int tanımlayıcı_girdi, int ADRES, int taşımak_değer, int[] veri, int süre_değer);
    public static native int almak_ağ(int tanımlayıcı_girdi, int[] veri, int süre_değer);
    public static native int ağ_taşımak(int tanımlayıcı_girdi);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int dikdörtgen(int 가로, int Dikey_konum, int 폭, int 높이, int 색);
}
