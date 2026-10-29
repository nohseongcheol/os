// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 dosya. 원본 Düzenle_değer/derlemek_kaynak hata_değer 시 기존 파일을 보존한다. */
public final class Bellek_dosya_sistemi {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] boyutlandırmak_Liste = new int[8];
    static int[] açık_BAĞ_DEĞ_SAY = new int[8], 허가들 = new int[8];
    static int[] İsim = new int[64];
    static int[] Düzenle_değer = new int[최대크기];
    static boolean 편집중 = false;
    static boolean Taşma_değer = false;
    static int Düzenle_boyutlandırmak = 0;

    static boolean çek_ad(int[] karakter_değer, int süre_değer) {
        if (süre_değer < 1 || süre_değer > 63) return false;
        for (int 수 = 0; 수 < süre_değer; 수++) {
            int değer = karakter_değer[수];
            if (!(değer >= 'a' && değer <= 'z') && !(değer >= 'A' && değer <= 'Z')
                && !(değer >= '0' && değer <= '9') && değer != '_' && değer != '-' && değer != '.') return false;
        }
        return karakter_değer[0] != '.';
    }

    static int BUL_girdi(int[] karakter_değer, int süre_değer) {
        if (!çek_ad(karakter_değer, süre_değer)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + süre_değer] == 0;
            for (int yuva_girdi = 0; yuva_girdi < süre_değer; yuva_girdi++) if (이름들[수 * 64 + yuva_girdi] != karakter_değer[yuva_girdi]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int depo_değer(int[] karakter_değer, int süre_değer, int[] veri, int Boyut) {
        if (!çek_ad(karakter_değer, süre_değer) || Boyut < 0 || Boyut > veri.length) return -22;
        if (Boyut > 최대크기) return -90;
        int Dizin = BUL_girdi(karakter_değer, süre_değer);
        if (Dizin == -2) {
            for (int 수 = 0; 수 < 8 && Dizin < 0; 수++) if (이름들[수 * 64] == 0 && açık_BAĞ_DEĞ_SAY[수] == 0) Dizin = 수;
            if (Dizin >= 0) 허가들[Dizin] = 438;
        }
        if (Dizin < 0) return -28;
        int ADRES = cihaz_değer.Dosya_Bellek() + Dizin * 최대크기;
        for (int 수 = 0; 수 < Boyut; 수++) cihaz_değer.yazma_Bellek(ADRES + 수, veri[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[Dizin * 64 + 수] = 수 < süre_değer ? karakter_değer[수] : 0;
        boyutlandırmak_Liste[Dizin] = Boyut;
        return Boyut;
    }

    static void girdi_Liste() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int yuva_girdi = 0; yuva_girdi < 64 && 이름들[수 * 64 + yuva_girdi] != 0; yuva_girdi++) SMS_Terminal.문자(이름들[수 * 64 + yuva_girdi]);
            SMS_Terminal.Yazma("  "); SMS_Terminal.수쓰기(boyutlandırmak_Liste[수]); SMS_Terminal.Yazma("bayt_değer\n");
        }
        SMS_Terminal.Yazma(depolama_aygıtı_cxn.bilgi_teknolojisi_Aktif_9e72441a ? "dosya 8칸, 파일당 16384바이트; sync로 depo_değer 장치에 보존\n"
            : "임시 dosya 8칸, 파일당 16384바이트; yeniden_denemek_değer 시작하면 사라짐\n");
    }

    static void komut(int[] artış_değer, int çalıştır, int süre_değer, int Eylem) {
        while (çalıştır < süre_değer && artış_değer[çalıştır] == ' ') çalıştır++;
        int 끝 = süre_değer;
        while (끝 > çalıştır && artış_değer[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - çalıştır;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Yazma("올바르지 않은 dosya İsim\n"); return; }
        for (int yuva_girdi = 0; yuva_girdi < 64; yuva_girdi++) İsim[yuva_girdi] = yuva_girdi < 수 ? artış_değer[çalıştır + yuva_girdi] : 0;
        int Dizin = BUL_girdi(İsim, 수);
        if (Dizin == -22) { SMS_Terminal.Yazma("올바르지 않은 dosya İsim\n"); return; }
        if (Eylem == 0) {
            편집중 = true; Düzenle_boyutlandırmak = 0; Taşma_değer = false;
            SMS_Terminal.Yazma("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (Dizin < 0) SMS_Terminal.Yazma("파일을 찾을 수 없습니다\n");
        else if (Eylem == 1) {
            int ADRES = cihaz_değer.Dosya_Bellek() + Dizin * 최대크기;
            for (int yuva_girdi = 0; yuva_girdi < boyutlandırmak_Liste[Dizin]; yuva_girdi++) SMS_Terminal.문자(cihaz_değer.기억읽기(ADRES + yuva_girdi));
            SMS_Terminal.문자(10);
        } else { 이름들[Dizin * 64] = 0; boyutlandırmak_Liste[Dizin] = 0; SMS_Terminal.Yazma("파일을 지웠습니다\n"); }
    }

    static boolean bilgi_teknolojisi_ÖZDEŞ(int[] artış_değer, int süre_değer, String 문구) {
        if (süre_değer != 문구.length()) return false;
        for (int yuva_girdi = 0; yuva_girdi < süre_değer; yuva_girdi++) if (artış_değer[yuva_girdi] != 문구.charAt(yuva_girdi)) return false;
        return true;
    }

    static void Düzenlenen_hat(int[] artış_değer, int süre_değer, boolean hat_Taşma) {
        if (bilgi_teknolojisi_ÖZDEŞ(artış_değer, süre_değer, ".cancel")) {
            편집중 = false; SMS_Terminal.Yazma("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (bilgi_teknolojisi_ÖZDEŞ(artış_değer, süre_değer, ".save")) {
            편집중 = false;
            if (Taşma_değer) { SMS_Terminal.Yazma("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && İsim[수] != 0) 수++;
            int sonuç = depo_değer(İsim, 수, Düzenle_değer, Düzenle_boyutlandırmak);
            SMS_Terminal.Yazma(sonuç >= 0 ? "보존한 bayt_değer 수: " : "보존 hata_değer: ");
            SMS_Terminal.수쓰기(sonuç); SMS_Terminal.문자(10);
        } else if (hat_Taşma || süre_değer + 1 > 최대크기 - Düzenle_boyutlandırmak) Taşma_değer = true;
        else {
            for (int 수 = 0; 수 < süre_değer; 수++) Düzenle_değer[Düzenle_boyutlandırmak++] = artış_değer[수];
            Düzenle_değer[Düzenle_boyutlandırmak++] = 10;
        }
    }

    static void 예제(String dosya, String içerik_değer) {
        for (int 수 = 0; 수 < 64; 수++) İsim[수] = 수 < dosya.length() ? dosya.charAt(수) : 0;
        for (int 수 = 0; 수 < içerik_değer.length(); 수++) Düzenle_değer[수] = içerik_değer.charAt(수);
        depo_değer(İsim, dosya.length(), Düzenle_değer, içerik_değer.length());
    }

    static void Hazırlan() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grup_değer = cihaz_değer.자바파일묶음(), Boyut = cihaz_değer.자바파일묶음크기();
        if (Boyut < 8 || yürütme_yönetici.수(Grup_değer) != 0x464a4b4a) { SMS_Terminal.Yazma("올바르지 않은 Java dosya Grup_değer\n"); return; }
        int öğe_BAĞ_DEĞ_SAY = yürütme_yönetici.수(Grup_değer + 4);
        if (öğe_BAĞ_DEĞ_SAY < 0 || öğe_BAĞ_DEĞ_SAY > 8 || öğe_BAĞ_DEĞ_SAY > (Boyut - 8) / 72) { SMS_Terminal.Yazma("올바르지 않은 Java dosya girdi_Liste\n"); return; }
        for (int 수 = 0; 수 < öğe_BAĞ_DEĞ_SAY; 수++) {
            int girdi_değer = Grup_değer + 8 + 수 * 72, süre_değer = 0;
            for (int yuva_girdi = 0; yuva_girdi < 64; yuva_girdi++) İsim[yuva_girdi] = cihaz_değer.기억읽기(girdi_değer + yuva_girdi);
            while (süre_değer < 64 && İsim[süre_değer] != 0) süre_değer++;
            int konum = yürütme_yönetici.수(girdi_değer + 64), dosya_boyutu = yürütme_yönetici.수(girdi_değer + 68);
            if (!çek_ad(İsim, süre_değer) || dosya_boyutu < 0 || dosya_boyutu > 최대크기 || konum < 8 + öğe_BAĞ_DEĞ_SAY * 72 || konum > Boyut - dosya_boyutu) {
                SMS_Terminal.Yazma("올바르지 않은 Java dosya girdi_değer\n"); return;
            }
            for (int yuva_girdi = 0; yuva_girdi < dosya_boyutu; yuva_girdi++) Düzenle_değer[yuva_girdi] = cihaz_değer.기억읽기(Grup_değer + konum + yuva_girdi);
            if (depo_değer(İsim, süre_değer, Düzenle_değer, dosya_boyutu) < 0) { SMS_Terminal.Yazma("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
