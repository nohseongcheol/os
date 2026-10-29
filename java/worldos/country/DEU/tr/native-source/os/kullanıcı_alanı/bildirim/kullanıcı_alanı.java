// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros kullanıcı_alanı ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class kullanıcı_alanı {
    public static native int açık_Dosya_tanımlayıcı(int[] Dosya_girdi_ad, int açık_Ayarlar);
    public static native int 파일한바이트읽기(int Dosya_tanımlayıcı);
    public static native int 파일한바이트쓰기(int Dosya_tanımlayıcı, int bayt_değer);
    public static native int Kapat_Dosya_tanımlayıcı(int Dosya_tanımlayıcı);
    public static native int commit_Dosyalar(int Dosya_tanımlayıcı);
    public static native int 파일읽기(int[] İsim, int[] veri);
    public static native int yazma_karakter_değer(int 문자);
    public static native int yazma_Dosya(int[] İsim, int[] veri, int süre_değer);
    public static native int Yazma(String içerik_değer);
    public static native int 인수개수();
    public static native String bağımsız_değişkenler(int Dizin);
    public static native int yürütme_izin();
    public static native int açık_ağ(int yerel_taşımak);
    public static native int göndermek_veri(int sap_değer, int ADRES, int hedef_taşımak, int[] veri, int süre_değer);
    public static native int almak_veri(int sap_değer, int[] veri, int 제한밀리초);
    public static native int Kapat_ağ(int sap_değer);
    public static native int 내주소();
    public static native int 보낸주소(int sap_değer);
    public static native int 보낸창구(int sap_değer);
}
