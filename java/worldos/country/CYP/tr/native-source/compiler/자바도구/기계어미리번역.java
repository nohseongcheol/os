// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Sınıf_değer 파일에서 독립 ARM64 커널용 C 원문을 만든다. konak JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Çeviri_hata extends RuntimeException {
        Çeviri_hata(String 설명) { super(설명); }
    }
    static final class veri_Okuyucu {
        final byte[] veri;
        int konum;
        veri_Okuyucu(byte[] artış_veri) { veri = artış_veri; }
        byte[] Okuma(int süre_değer) {
            if (süre_değer < 0 || süre_değer > veri.length - konum) throw new Çeviri_hata("잘린 Sınıf_değer 또는 komut veri");
            byte[] sonuç = Arrays.copyOfRange(veri, konum, konum + süre_değer); konum += süre_değer; return sonuç;
        }
        int 한바이트() { if (konum >= veri.length) throw new Çeviri_hata("잘린 komut veri"); return veri[konum++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class üye_veri {
        final int erişim_girdi;
        final String İsim, 서술;
        final Map<String, byte[]> öznitelik_değer;
        üye_veri(int erişim_değer, String ad_değer, String tanımlayıcı_veri, Map<String, byte[]> öznitelik_veri) {
            erişim_girdi = erişim_değer; İsim = ad_değer; 서술 = tanımlayıcı_veri; öznitelik_değer = öznitelik_veri;
        }
    }
    static final class metot_Başvuru implements Comparable<metot_Başvuru> {
        final String sahip_değer, İsim, 서술;
        metot_Başvuru(String 소유값, String ad_değer, String tanımlayıcı_veri) { sahip_değer = 소유값; İsim = ad_değer; 서술 = tanımlayıcı_veri; }
        String[] 부분들() { return new String[]{sahip_değer, İsim, 서술}; }
        public int compareTo(metot_Başvuru eş_değer) {
            int Karşılaştırma_değer = sahip_değer.compareTo(eş_değer.sahip_değer);
            if (Karşılaştırma_değer == 0) Karşılaştırma_değer = İsim.compareTo(eş_değer.İsim);
            return Karşılaştırma_değer == 0 ? 서술.compareTo(eş_değer.서술) : Karşılaştırma_değer;
        }
        public boolean equals(Object eş_değer) { return eş_değer instanceof metot_Başvuru && compareTo((metot_Başvuru) eş_değer) == 0; }
        public int hashCode() { return Objects.hash(sahip_değer, İsim, 서술); }
    }
    static final class Sınıf_veri {
        final int[] sabit_Tip;
        final Object[] sabit_veri;
        final String İsim;
        final List<üye_veri> alan_değeri, işlev_değer;
        Sınıf_veri(Path yol) throws IOException {
            veri_Okuyucu Okuyucu_değer = new veri_Okuyucu(Files.readAllBytes(yol));
            if (Okuyucu_değer.네바이트() != 0xcafebabe) throw new Çeviri_hata("Java Sınıf_değer 표식이 아님");
            Okuyucu_değer.Okuma(4);
            int öğe_BAĞ_DEĞ_SAY = Okuyucu_değer.두바이트(); sabit_Tip = new int[öğe_BAĞ_DEĞ_SAY]; sabit_veri = new Object[öğe_BAĞ_DEĞ_SAY];
            for (int 순번 = 1; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) {
                int Tip_değer = Okuyucu_değer.한바이트(); sabit_Tip[순번] = Tip_değer;
                switch (Tip_değer) {
                    case 1:
                        int süre_değer = Okuyucu_değer.두바이트();
                        byte[] karakter_tampon = Okuyucu_değer.Okuma(süre_değer), 길이붙인자료 = new byte[süre_değer + 2];
                        길이붙인자료[0] = (byte)(süre_değer >> 8); 길이붙인자료[1] = (byte)süre_değer;
                        System.arraycopy(karakter_tampon, 0, 길이붙인자료, 2, süre_değer);
                        sabit_veri[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: sabit_veri[순번] = Okuyucu_değer.네바이트(); break;
                    case 4: Okuyucu_değer.Okuma(4); break;
                    case 5: case 6: Okuyucu_değer.Okuma(8); 순번++; break;
                    case 7: case 8: case 16: sabit_veri[순번] = Okuyucu_değer.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        sabit_veri[순번] = new int[]{Okuyucu_değer.두바이트(), Okuyucu_değer.두바이트()}; break;
                    case 15: sabit_veri[순번] = new int[]{Okuyucu_değer.한바이트(), Okuyucu_değer.두바이트()}; break;
                    default: throw new Çeviri_hata("지원하지 않는 sabit_değer Tip_değer: " + Tip_değer);
                }
            }
            Okuyucu_değer.두바이트(); İsim = sınıf_adı(Okuyucu_değer.두바이트());
            if (!sınıf_adı(Okuyucu_değer.두바이트()).equals("java/lang/Object") || Okuyucu_değer.두바이트() != 0)
                throw new Çeviri_hata(İsim + ": 상속 및 인터페이스 미지원");
            alan_değeri = 멤버읽기(Okuyucu_değer); işlev_değer = 멤버읽기(Okuyucu_değer); 속성읽기(Okuyucu_değer);
            if (Okuyucu_değer.konum != Okuyucu_değer.veri.length) throw new Çeviri_hata("Sınıf_değer 뒤에 남은 veri");
        }
        String 문자(int Dizin) {
            if (Dizin < 1 || Dizin >= sabit_Tip.length || sabit_Tip[Dizin] != 1) throw new Çeviri_hata("문자 sabit_değer Dizin hata");
            return (String) sabit_veri[Dizin];
        }
        String sınıf_adı(int Dizin) {
            if (Dizin < 1 || Dizin >= sabit_Tip.length || sabit_Tip[Dizin] != 7) throw new Çeviri_hata("Sınıf_değer Başvuru hata");
            return 문자((Integer)sabit_veri[Dizin]);
        }
        metot_Başvuru Başvuru(int Dizin) {
            if (Dizin < 1 || Dizin >= sabit_Tip.length || sabit_Tip[Dizin] < 9 || sabit_Tip[Dizin] > 11) throw new Çeviri_hata("멤버 Başvuru hata");
            int[] eşleştirmek_değer = (int[])sabit_veri[Dizin], ad_eşleştirmek = (int[])sabit_veri[eşleştirmek_değer[1]];
            return new metot_Başvuru(sınıf_adı(eşleştirmek_değer[0]), 문자(ad_eşleştirmek[0]), 문자(ad_eşleştirmek[1]));
        }
        Map<String, byte[]> 속성읽기(veri_Okuyucu Okuyucu_değer) {
            Map<String, byte[]> sonuç = new LinkedHashMap<>();
            int öğe_BAĞ_DEĞ_SAY = Okuyucu_değer.두바이트();
            for (int 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) {
                String öznitelik_ad = 문자(Okuyucu_değer.두바이트()); byte[] değer = Okuyucu_değer.Okuma(Okuyucu_değer.네바이트());
                if (sonuç.put(öznitelik_ad, değer) != null) throw new Çeviri_hata("겹친 öznitelik_değer: " + öznitelik_ad);
            }
            return sonuç;
        }
        List<üye_veri> 멤버읽기(veri_Okuyucu Okuyucu_değer) {
            List<üye_veri> sonuç = new ArrayList<>(); int öğe_BAĞ_DEĞ_SAY = Okuyucu_değer.두바이트();
            for (int 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) {
                int erişim_girdi = Okuyucu_değer.두바이트(); String metot_girdi_ad = 문자(Okuyucu_değer.두바이트()), 서술 = 문자(Okuyucu_değer.두바이트());
                sonuç.add(new üye_veri(erişim_girdi, metot_girdi_ad, 서술, 속성읽기(Okuyucu_değer)));
            }
            return sonuç;
        }
    }
    static final class metot_tanımlayıcı {
        final List<String> bağımsız_değişkenler = new ArrayList<>();
        final String İade_KR;
        metot_tanımlayıcı(String 서술) {
            if (!서술.startsWith("(")) throw new Çeviri_hata("işlev_değer 서술 hata: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Çeviri_hata("işlev_değer 서술 hata: " + 서술);
            bağımsız_değişkenler.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (bağımsız_değişkenler.contains("V") || 반환들.size() != 1) throw new Çeviri_hata("işlev_değer 서술 hata: " + 서술);
            İade_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> sonuç = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int konum = 0; konum < 서술.length();) {
            String seçim_değer = null;
            for (String biçim_değer : 허용형식) if (서술.startsWith(biçim_değer, konum)) { seçim_değer = biçim_değer; break; }
            if (seçim_değer == null) throw new Çeviri_hata("지원하지 않는 veri_türü: " + 서술);
            sonuç.add(seçim_değer); konum += seçim_değer.length();
        }
        return sonuç;
    }
    static String simge(String Tip_değer, String... 부분들) {
        try {
            byte[] özet_Dosya = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder metin = new StringBuilder("j_" + Tip_değer + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) metin.append(String.format(Locale.ROOT, "%02x", özet_Dosya[순번] & 255));
            return metin.toString();
        } catch (Exception hata) { throw new Çeviri_hata(hata.toString()); }
    }
    final Map<String, Sınıf_veri> 클래스들 = new TreeMap<>();
    final Map<metot_Başvuru, üye_veri> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), makine_İşlevler_c3a8e64a = new LinkedHashMap<>();
    final String yürütme_hedef, makine_Sınıf;
    final int yığın_Word_BAĞ_DEĞ_SAY;
    final Path kaynak_yol;
    기계어미리번역(List<Path> yol_Liste, String hedef, int 낱말수, Path kaynak_değer) throws IOException {
        if ((!hedef.equals("kernel") && !hedef.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Çeviri_hata("yürütmek_komut hedef 또는 Bellek_değer ADRES_bölge Boyut hata");
        yürütme_hedef = hedef; yığın_Word_BAĞ_DEĞ_SAY = 낱말수; kaynak_yol = kaynak_değer;
        // 이 이름도 국가별 kaynak_ağaç oluşturmak 시 해당 언어로 옮긴다.
        makine_Sınıf = hedef.equals("kernel") ? "Pano" : "kullanıcı_alanı";
        for (String girdi_satırı : Files.readAllLines(kaynak_değer.resolve("makine_İşlevler.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = girdi_satırı.split("\t", -1);
            if (부분들.length != 4) throw new Çeviri_hata("makine işlev_değer veri hata");
            if (부분들[0].equals(hedef)) makine_İşlevler_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path yol : yol_Liste) {
            Sınıf_veri veri = new Sınıf_veri(yol);
            if (클래스들.put(veri.İsim, veri) != null) throw new Çeviri_hata("중복 Sınıf_değer: " + veri.İsim);
            for (üye_veri alan_değeri : veri.alan_değeri) {
                if ((alan_değeri.erişim_girdi & 8) == 0 || 형식읽기(alan_değeri.서술).equals(Collections.singletonList("V"))) throw new Çeviri_hata("statik_değer 필드만 Destek_değer");
                if (필드들.put(new metot_Başvuru(veri.İsim, alan_değeri.İsim, alan_değeri.서술), alan_değeri) != null) throw new Çeviri_hata("중복 alan_değeri");
            }
            for (üye_veri işlev_değer : veri.işlev_değer) {
                if (işlev_değer.İsim.equals("<init>")) continue;
                if ((işlev_değer.erişim_girdi & 8) == 0 || (işlev_değer.erişim_girdi & (0x20 | 0x400)) != 0) throw new Çeviri_hata("statik_değer 비동기화 함수만 Destek_değer");
                new metot_tanımlayıcı(işlev_değer.서술);
                if (함수들.put(new metot_Başvuru(veri.İsim, işlev_değer.İsim, işlev_değer.서술), işlev_değer) != null) throw new Çeviri_hata("중복 işlev_değer");
            }
        }
    }
    String dize_simge(String metin) { return 문자열들.computeIfAbsent(metin, değer -> "j_text_" + 문자열들.size()); }
    String sabit_ifade(Sınıf_veri veri, int Dizin) {
        if (Dizin < 1 || Dizin >= veri.sabit_Tip.length) throw new Çeviri_hata("sabit_değer Dizin klip hata");
        if (veri.sabit_Tip[Dizin] == 3) return "(word)(uint32_t)(" + veri.sabit_veri[Dizin] + ")";
        if (veri.sabit_Tip[Dizin] == 8) return "(word)" + dize_simge(veri.문자((Integer)veri.sabit_veri[Dizin]));
        throw new Çeviri_hata("정수와 dize_değer 상수만 Destek_değer");
    }
    String metot_prototip(metot_Başvuru Başvuru) {
        List<String> 인수들 = new ArrayList<>(); int öğe_BAĞ_DEĞ_SAY = new metot_tanımlayıcı(Başvuru.서술).bağımsız_değişkenler.size();
        for (int 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simge("method", Başvuru.부분들()) + "(" + (öğe_BAĞ_DEĞ_SAY == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void çek_yerel(int Dizin, int yerel_değişken_BAĞ_DEĞ_SAY) { if (Dizin < 0 || Dizin >= yerel_değişken_BAĞ_DEĞ_SAY) throw new Çeviri_hata("yerel_Scope değişken_değer Dizin klip hata"); }
    void 분기넣기(List<String> metinÇıktısı, Set<Integer> dal_Liste, int konum, int 이동량, String koşul) {
        int hedef_değer = konum + 이동량; dal_Liste.add(hedef_değer);
        metinÇıktısı.add((koşul == null ? "" : "if (" + koşul + ") ") + "goto b" + hedef_değer + ";");
    }
    String metot_gövdesi(metot_Başvuru işlev_değer, üye_veri veri) {
        byte[] gövde_veri = veri.öznitelik_değer.get("Code"); if (gövde_veri == null) throw new Çeviri_hata("işlev_değer 몸체가 없음: " + işlev_değer.İsim);
        veri_Okuyucu Okuyucu_değer = new veri_Okuyucu(gövde_veri); int 쌓임깊이 = Okuyucu_değer.두바이트(), yerel_değişken_BAĞ_DEĞ_SAY = Okuyucu_değer.두바이트();
        veri_Okuyucu komut_veri = new veri_Okuyucu(Okuyucu_değer.Okuma(Okuyucu_değer.네바이트()));
        if (Okuyucu_değer.두바이트() != 0) throw new Çeviri_hata("try/catch/finally 미지원");
        metot_tanımlayıcı biçim_değer = new metot_tanımlayıcı(işlev_değer.서술); if (yerel_değişken_BAĞ_DEĞ_SAY < biçim_değer.bağımsız_değişkenler.size()) throw new Çeviri_hata("매개변수보다 적은 yerel_Scope değişken_değer");
        Sınıf_veri Sınıf_değer = 클래스들.get(işlev_değer.sahip_değer);
        List<String> metinÇıktısı = new ArrayList<>(); metinÇıktısı.add(metot_prototip(işlev_değer) + " {");
        metinÇıktısı.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(yerel_değişken_BAĞ_DEĞ_SAY, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < biçim_değer.bağımsız_değişkenler.size(); 순번++) metinÇıktısı.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), dal_Liste = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (komut_veri.konum < komut_veri.veri.length) {
            int konum = komut_veri.konum, komut = komut_veri.한바이트(); 경계들.add(konum); metinÇıktısı.add("b" + konum + ":;");
            if (komut == 0) continue;
            if (komut == 1) metinÇıktısı.add("PUSH(0);");
            else if (komut >= 2 && komut <= 8) metinÇıktısı.add("PUSH((uint32_t)(" + (komut - 3) + "));");
            else if (komut == 16 || komut == 17) metinÇıktısı.add("PUSH((uint32_t)(" + (komut == 16 ? komut_veri.부호한바이트() : komut_veri.부호두바이트()) + "));");
            else if (komut == 18 || komut == 19) metinÇıktısı.add("PUSH(" + sabit_ifade(Sınıf_değer, komut == 18 ? komut_veri.한바이트() : komut_veri.두바이트()) + ");");
            else if (komut == 21 || komut == 25 || (komut >= 26 && komut <= 29) || (komut >= 42 && komut <= 45)) {
                int Dizin = komut == 21 || komut == 25 ? komut_veri.한바이트() : komut - (komut <= 29 ? 26 : 42);
                çek_yerel(Dizin, yerel_değişken_BAĞ_DEĞ_SAY); metinÇıktısı.add("PUSH(l[" + Dizin + "]);");
            } else if (komut == 54 || komut == 58 || (komut >= 59 && komut <= 62) || (komut >= 75 && komut <= 78)) {
                int Dizin = komut == 54 || komut == 58 ? komut_veri.한바이트() : komut - (komut <= 62 ? 59 : 75);
                çek_yerel(Dizin, yerel_değişken_BAĞ_DEĞ_SAY); metinÇıktısı.add("l[" + Dizin + "] = POP();");
            } else if (komut == 46) metinÇıktısı.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (komut == 79) metinÇıktısı.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (komut == 87 || komut == 88) metinÇıktısı.add(komut == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (komut >= 89 && komut <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] düzen_Liste = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[komut - 89]; 순번++) metinÇıktısı.add("abcd".charAt(순번) + " = POP();");
                for (char değer : düzen_Liste[komut - 89].toCharArray()) metinÇıktısı.add("PUSH(" + değer + ");");
            } else if (komut == 96 || komut == 100 || komut == 104 || komut == 126 || komut == 128 || komut == 130) {
                String işlem_değer_c96707fb = komut == 96 ? "+" : komut == 100 ? "-" : komut == 104 ? "*" : komut == 126 ? "&" : komut == 128 ? "|" : "^";
                metinÇıktısı.add("b = POP(); a = POP(); PUSH((uint32_t)a " + işlem_değer_c96707fb + " (uint32_t)b);");
            } else if (komut == 108 || komut == 112) metinÇıktısı.add("b = POP(); a = POP(); PUSH(divide(a,b," + (komut == 112 ? 1 : 0) + "));");
            else if (komut == 116) metinÇıktısı.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (komut == 120 || komut == 122 || komut == 124) {
                metinÇıktısı.add("b = POP(); a = POP();"); metinÇıktısı.add("PUSH(" + (komut == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (komut == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (komut == 132) {
                int Dizin = komut_veri.한바이트(), artış_tutar = komut_veri.부호한바이트(); çek_yerel(Dizin, yerel_değişken_BAĞ_DEĞ_SAY);
                metinÇıktısı.add("l[" + Dizin + "] = (uint32_t)l[" + Dizin + "] + (uint32_t)(" + artış_tutar + ");");
            } else if (komut >= 145 && komut <= 147) metinÇıktısı.add("a = POP(); PUSH((uint32_t)(" + (komut == 145 ? "int8_t" : komut == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (komut >= 153 && komut <= 158) {
                metinÇıktısı.add("a = POP();"); 분기넣기(metinÇıktısı, dal_Liste, konum, komut_veri.부호두바이트(), "(int32_t)a " + 비교들[komut - 153] + " 0");
            } else if (komut >= 159 && komut <= 166) {
                metinÇıktısı.add("b = POP(); a = POP();"); 분기넣기(metinÇıktısı, dal_Liste, konum, komut_veri.부호두바이트(), komut >= 165 ? "a " + 비교들[komut - 159] + " b" : "(int32_t)a " + 비교들[komut - 159] + " (int32_t)b");
            } else if (komut == 167 || komut == 200) 분기넣기(metinÇıktısı, dal_Liste, konum, komut == 167 ? komut_veri.부호두바이트() : komut_veri.네바이트(), null);
            else if (komut == 170 || komut == 171) {
                while (komut_veri.konum % 4 != 0) komut_veri.한바이트();
                int varsayılan_değer = komut_veri.네바이트(); metinÇıktısı.add("a = POP();");
                if (komut == 170) {
                    int 아래 = komut_veri.네바이트(), 위 = komut_veri.네바이트(); long öğe_BAĞ_DEĞ_SAY = (long)위 - 아래 + 1;
                    if (öğe_BAĞ_DEĞ_SAY < 1 || öğe_BAĞ_DEĞ_SAY > (komut_veri.veri.length - komut_veri.konum) / 4) throw new Çeviri_hata("switch klip hata");
                    for (long değer = 아래; değer <= 위; değer++) 분기넣기(metinÇıktısı, dal_Liste, konum, komut_veri.네바이트(), "(int32_t)a == (" + değer + ")");
                } else {
                    int öğe_BAĞ_DEĞ_SAY = komut_veri.네바이트(), ön_kamera_veri = 0;
                    if (öğe_BAĞ_DEĞ_SAY < 0 || öğe_BAĞ_DEĞ_SAY > (komut_veri.veri.length - komut_veri.konum) / 8) throw new Çeviri_hata("switch Boyut hata");
                    for (int 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) {
                        int değer = komut_veri.네바이트(); if (순번 > 0 && değer <= ön_kamera_veri) throw new Çeviri_hata("switch düzen_değer hata"); ön_kamera_veri = değer;
                        분기넣기(metinÇıktısı, dal_Liste, konum, komut_veri.네바이트(), "(int32_t)a == (" + değer + ")");
                    }
                }
                분기넣기(metinÇıktısı, dal_Liste, konum, varsayılan_değer, null);
            } else if (komut == 172 || komut == 176 || komut == 177) metinÇıktısı.add("return " + (komut == 177 ? "0" : "POP()") + ";");
            else if (komut == 178 || komut == 179) {
                metot_Başvuru Başvuru = Sınıf_değer.Başvuru(komut_veri.두바이트()); if (!필드들.containsKey(Başvuru)) throw new Çeviri_hata("알 수 없는 alan_değeri");
                metinÇıktısı.add(simge("init", Başvuru.sahip_değer) + "();"); String alan_değeri = simge("field", Başvuru.부분들());
                metinÇıktısı.add(komut == 178 ? "PUSH(" + alan_değeri + ");" : alan_değeri + " = POP();");
            } else if (komut == 184) {
                metot_Başvuru Başvuru = Sınıf_değer.Başvuru(komut_veri.두바이트()); if (!함수들.containsKey(Başvuru)) throw new Çeviri_hata("알 수 없는 işlev_değer");
                metot_tanımlayıcı çağrı_TÜR = new metot_tanımlayıcı(Başvuru.서술); int öğe_BAĞ_DEĞ_SAY = çağrı_TÜR.bağımsız_değişkenler.size();
                metinÇıktısı.add(simge("init", Başvuru.sahip_değer) + "();"); metinÇıktısı.add("if(sp < " + öğe_BAĞ_DEĞ_SAY + ") kernel_panic(\"call stack underflow\"); sp -= " + öğe_BAĞ_DEĞ_SAY + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                metinÇıktısı.add("a = " + simge("method", Başvuru.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!çağrı_TÜR.İade_KR.equals("V")) metinÇıktısı.add("PUSH(a);");
            } else if (komut == 182) {
                metot_Başvuru Başvuru = Sınıf_değer.Başvuru(komut_veri.두바이트());
                if (Başvuru.equals(new metot_Başvuru("java/lang/String", "length", "()I"))) metinÇıktısı.add("a = POP(); PUSH(length(a));");
                else if (Başvuru.equals(new metot_Başvuru("java/lang/String", "charAt", "(I)C"))) metinÇıktısı.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Çeviri_hata("가상 işlev_değer 호출 미지원");
            } else if (komut == 188) {
                if (komut_veri.한바이트() != 10) throw new Çeviri_hata("new int[]만 Destek_değer"); metinÇıktısı.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (komut == 190) metinÇıktısı.add("a = POP(); PUSH(length(a));");
            else if (komut == 196) {
                int uzantı_değer = komut_veri.한바이트(), Dizin = komut_veri.두바이트(); çek_yerel(Dizin, yerel_değişken_BAĞ_DEĞ_SAY);
                if (uzantı_değer == 21 || uzantı_değer == 25) metinÇıktısı.add("PUSH(l[" + Dizin + "]);");
                else if (uzantı_değer == 54 || uzantı_değer == 58) metinÇıktısı.add("l[" + Dizin + "] = POP();");
                else if (uzantı_değer == 132) metinÇıktısı.add("l[" + Dizin + "] = (uint32_t)l[" + Dizin + "] + (uint32_t)(" + komut_veri.부호두바이트() + ");");
                else throw new Çeviri_hata("미지원 wide komut");
            } else if (komut == 198 || komut == 199) {
                metinÇıktısı.add("a = POP();"); 분기넣기(metinÇıktısı, dal_Liste, konum, komut_veri.부호두바이트(), "a " + (komut == 198 ? "==" : "!=") + " 0");
            } else throw new Çeviri_hata(işlev_değer.sahip_değer + "." + işlev_değer.İsim + ", bayt_değer " + konum + ": 미지원 komut " + komut);
        }
        if (!경계들.containsAll(dal_Liste)) throw new Çeviri_hata("komut 경계가 아닌 곳으로 dal");
        metinÇıktısı.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", metinÇıktısı);
    }
    String dışarı_aktarmak_metot(String köprü_simge, String hedef, boolean 진입점여부) {
        int konum_dizini = hedef.lastIndexOf('.'); if (konum_dizini < 0 || !köprü_simge.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Çeviri_hata("내보내기 Ata_değer hata");
        String sahip_değer = hedef.substring(0, konum_dizini).replace('.', '/'), İsim = hedef.substring(konum_dizini + 1); metot_Başvuru seçim_değer = null;
        for (metot_Başvuru Başvuru : 함수들.keySet()) if (Başvuru.sahip_değer.equals(sahip_değer) && Başvuru.İsim.equals(İsim)) {
            if (seçim_değer != null) throw new Çeviri_hata("겹친 내보내기 hedef"); seçim_değer = Başvuru;
        }
        if (seçim_değer == null || (함수들.get(seçim_değer).erişim_girdi & 0x100) != 0) throw new Çeviri_hata("내보낼 함수가 없음 또는 native işlev_değer");
        metot_tanımlayıcı biçim_değer = new metot_tanımlayıcı(seçim_değer.서술);
        if ((진입점여부 && !biçim_değer.bağımsız_değişkenler.isEmpty()) || !Arrays.asList("V", "I").contains(biçim_değer.İade_KR)) throw new Çeviri_hata("giriş_noktası_değer 또는 C sınır_değer biçim_değer hata");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < biçim_değer.bağımsız_değişkenler.size(); 순번++) {
            if (!biçim_değer.bağımsız_değişkenler.get(순번).equals("I")) throw new Çeviri_hata("C 경계는 int 인수만 Destek_değer");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (biçim_değer.İade_KR.equals("V") ? "void " : "int32_t ") + köprü_simge + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simge("init", seçim_değer.sahip_değer) + "(); " + (biçim_değer.İade_KR.equals("V") ? "" : "return (int32_t)") + simge("method", seçim_değer.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String oluşturmak(String giriş_noktası, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metot_Başvuru, üye_veri> girdi_değer : 함수들.entrySet()) {
            metot_Başvuru Başvuru = girdi_değer.getKey(); üye_veri veri = girdi_değer.getValue(); 선언들.add(metot_prototip(Başvuru) + ";");
            if ((veri.erişim_girdi & 0x100) != 0) {
                String Bağlan = makine_İşlevler_c3a8e64a.get(Başvuru.İsim + Başvuru.서술);
                if (!Başvuru.sahip_değer.equals(makine_Sınıf) || Bağlan == null) throw new Çeviri_hata("허용되지 않은 native işlev_değer: " + Başvuru.İsim);
                int öğe_BAĞ_DEĞ_SAY = new metot_tanımlayıcı(Başvuru.서술).bağımsız_değişkenler.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Bağlan + "(" + (öğe_BAĞ_DEĞ_SAY == 0 ? "void" : String.join(",", Collections.nCopies(öğe_BAĞ_DEĞ_SAY, "word"))) + ");");
                몸체들.add(metot_prototip(Başvuru) + " { return " + Bağlan + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metot_gövdesi(Başvuru, veri));
        }
        for (Map.Entry<metot_Başvuru, üye_veri> girdi_değer : 필드들.entrySet()) {
            metot_Başvuru Başvuru = girdi_değer.getKey(); byte[] sabit_değer = girdi_değer.getValue().öznitelik_değer.get("ConstantValue");
            String değer = sabit_değer == null ? "0" : sabit_ifade(클래스들.get(Başvuru.sahip_değer), new veri_Okuyucu(sabit_değer).두바이트());
            필드선언들.add("static word " + simge("field", Başvuru.부분들()) + " = " + değer + ";");
        }
        for (String İsim : 클래스들.keySet()) {
            String başlat = simge("init", İsim), Durum_değer = simge("state", İsim);
            선언들.add("static void " + başlat + "(void);"); 필드선언들.add("static unsigned " + Durum_değer + ";");
            metot_Başvuru Başvuru = new metot_Başvuru(İsim, "<clinit>", "()V");
            몸체들.add("static void " + başlat + "(void) { if(" + Durum_değer + ") return; " + Durum_değer + " = 1; " + (함수들.containsKey(Başvuru) ? simge("method", Başvuru.부분들()) + "(); " : "") + Durum_değer + " = 2; }");
        }
        몸체들.add(dışarı_aktarmak_metot("java_entry", giriş_noktası, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Ata_değer : 내보내기목록) {
            int konum_dizini = Ata_değer.indexOf('='); if (konum_dizini < 1) throw new Çeviri_hata("내보내기 Ata_değer hata");
            String İsim = Ata_değer.substring(0, konum_dizini); 공개이름.add(İsim); 몸체들.add(dışarı_aktarmak_metot(İsim, Ata_değer.substring(konum_dizini + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> girdi_değer : 문자열들.entrySet()) {
            String metin = girdi_değer.getKey(); StringBuilder DİZİ_değer = new StringBuilder("static const word " + girdi_değer.getValue() + "[] = {" + metin.length());
            for (int 순번 = 0; 순번 < metin.length(); 순번++) DİZİ_değer.append(", ").append((int)metin.charAt(순번));
            문자열선언들.add(DİZİ_değer.append("};").toString());
        }
        String Destek_değer = Files.readString(kaynak_yol.resolve("CLR_Destek.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(yığın_Word_BAĞ_DEĞ_SAY));
        return 기계원문한국어화(Destek_değer + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String kaynakKod, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ad_tablo = new HashMap<>();
        for (String girdi_satırı : Files.readAllLines(kaynak_yol.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] eşleştirmek_değer = girdi_satırı.split("\t"); ad_tablo.put(eşleştirmek_değer[0], eşleştirmek_değer[1]);
        }
        Pattern öbek_ifade = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = öbek_ifade.matcher(kaynakKod); StringBuffer sonuç = new StringBuffer();
        while (찾개.find()) {
            String İsim = 찾개.group(), 새이름 = İsim;
            if (!İsim.startsWith("//") && !İsim.startsWith("/*") && !İsim.startsWith("\"") && !İsim.startsWith("'") && !공개이름.contains(İsim)) {
                새이름 = ad_tablo.getOrDefault(İsim, İsim);
                if (İsim.matches("a[0-9]+")) 새이름 = "bağımsız_değişkenler" + İsim.substring(1);
                if (İsim.matches("b[0-9]+")) 새이름 = "dal" + İsim.substring(1);
                if (범용표기) {
                    StringBuilder gösterim_değer = new StringBuilder();
                    for (char karakter_değer : 새이름.toCharArray()) gösterim_değer.append(karakter_değer < 128 ? Character.toString(karakter_değer) : String.format(Locale.ROOT, "\\u%04x", (int)karakter_değer));
                    새이름 = gösterim_değer.toString();
                }
            }
            찾개.appendReplacement(sonuç, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(sonuç); return sonuç.toString();
    }
    String X_86_metot_gövdesi(metot_Başvuru işlev_değer, üye_veri veri, Map<String,String> makine_tablo, String hedef) {
        String işaret_değer = simge("method", işlev_değer.부분들());
        List<String> girdi_satırı = new ArrayList<>();
        if ((veri.erişim_girdi & 0x100) != 0) {
            String Bağlan = makine_tablo.get(işlev_değer.İsim + işlev_değer.서술);
            if (!işlev_değer.sahip_değer.equals(hedef.equals("kernel") ? "cihaz_değer" : "kullanıcı_alanı") || Bağlan == null) throw new Çeviri_hata("허용되지 않은 native işlev_değer");
            return ".text\n" + işaret_değer + ":\njmp " + Bağlan;
        }
        byte[] gövde_metni = veri.öznitelik_değer.get("Code"); if (gövde_metni == null) throw new Çeviri_hata("işlev_değer 몸체가 없음");
        veri_Okuyucu Okuyucu_değer = new veri_Okuyucu(gövde_metni); Okuyucu_değer.두바이트(); int yerel_BAĞ_DEĞ_SAY = Okuyucu_değer.두바이트();
        veri_Okuyucu komut_veri = new veri_Okuyucu(Okuyucu_değer.Okuma(Okuyucu_değer.네바이트()));
        if (Okuyucu_değer.두바이트() != 0) throw new Çeviri_hata("try/catch/finally 미지원");
        metot_tanımlayıcı biçim_değer = new metot_tanımlayıcı(işlev_değer.서술); if (yerel_BAĞ_DEĞ_SAY < biçim_değer.bağımsız_değişkenler.size()) throw new Çeviri_hata("매개변수보다 적은 yerel_Scope değişken_değer");
        Collections.addAll(girdi_satırı,".text",".globl " + işaret_değer,".type " + işaret_değer + ", @function",işaret_değer + ":","pushl %ebp","movl %esp, %ebp","subl $" + yerel_BAĞ_DEĞ_SAY * 4 + ", %esp");
        for (int 순번 = 0; 순번 < biçim_değer.bağımsız_değişkenler.size(); 순번++) Collections.addAll(girdi_satırı,"movl " + (8 + 4 * (biçim_değer.bağımsız_değişkenler.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Sınıf_veri Sınıf_değer = 클래스들.get(işlev_değer.sahip_değer); Set<Integer> 경계들 = new HashSet<>(), dal_Liste = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (komut_veri.konum < komut_veri.veri.length) {
            int konum = komut_veri.konum, komut = komut_veri.한바이트(); String konum_dizini = işaret_değer + "_b" + konum;
            girdi_satırı.add(konum_dizini + ":"); 경계들.add(konum);
            if (komut == 0) girdi_satırı.add("nop");
            else if (komut == 1) girdi_satırı.add("pushl $0");
            else if (komut >= 2 && komut <= 8) girdi_satırı.add("pushl $" + (komut - 3));
            else if (komut == 16 || komut == 17) girdi_satırı.add("pushl $" + (komut == 16 ? komut_veri.부호한바이트() : komut_veri.부호두바이트()));
            else if (komut == 18 || komut == 19) {
                int Dizin = komut == 18 ? komut_veri.한바이트() : komut_veri.두바이트();
                girdi_satırı.add("pushl $" + X_86_sabit(Sınıf_değer,Dizin));
            } else if (komut == 21 || komut == 25 || (komut >= 26 && komut <= 29) || (komut >= 42 && komut <= 45) || komut == 54 || komut == 58 || (komut >= 59 && komut <= 62) || (komut >= 75 && komut <= 78)) {
                boolean 읽음 = komut < 54; int Dizin = komut == 21 || komut == 25 || komut == 54 || komut == 58 ? komut_veri.한바이트() : komut - (komut <= 29 ? 26 : komut <= 45 ? 42 : komut <= 62 ? 59 : 75);
                çek_yerel(Dizin,yerel_BAĞ_DEĞ_SAY); girdi_satırı.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (Dizin + 1)) + "(%ebp)");
            } else if (komut == 46) Collections.addAll(girdi_satırı,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (komut == 79) Collections.addAll(girdi_satırı,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (komut == 87 || komut == 88) girdi_satırı.add("addl $" + (komut == 87 ? 4 : 8) + ", %esp");
            else if (komut >= 89 && komut <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] düzen_Liste = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[komut - 89]; 순번++) girdi_satırı.add("popl " + 저장기들[순번]);
                for (int 순번 : düzen_Liste[komut - 89]) girdi_satırı.add("pushl " + 저장기들[순번]);
            } else if (komut == 96 || komut == 100 || komut == 104 || komut == 126 || komut == 128 || komut == 130) {
                String işlem_değer_c96707fb = komut == 96 ? "addl" : komut == 100 ? "subl" : komut == 104 ? "imull" : komut == 126 ? "andl" : komut == 128 ? "orl" : "xorl";
                Collections.addAll(girdi_satırı,"popl %ecx","popl %eax",işlem_değer_c96707fb + " %ecx, %eax","pushl %eax");
            } else if (komut == 108 || komut == 112) Collections.addAll(girdi_satırı,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + konum_dizini + "_divide","cmpl $0x80000000, %eax","jne " + konum_dizini + "_divide","xorl %edx, %edx","jmp " + konum_dizini + "_done",konum_dizini + "_divide:","cltd","idivl %ecx",konum_dizini + "_done:","pushl " + (komut == 108 ? "%eax" : "%edx"));
            else if (komut == 116) girdi_satırı.add("negl (%esp)");
            else if (komut == 120 || komut == 122 || komut == 124) Collections.addAll(girdi_satırı,"popl %ecx","popl %eax",(komut == 120 ? "sall" : komut == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (komut == 132) {
                int Dizin = komut_veri.한바이트(), artış_değer_d3e2c4bb = komut_veri.부호한바이트(); çek_yerel(Dizin,yerel_BAĞ_DEĞ_SAY); girdi_satırı.add("addl $" + artış_değer_d3e2c4bb + ", -" + (4 * (Dizin + 1)) + "(%ebp)");
            } else if (komut >= 145 && komut <= 147) Collections.addAll(girdi_satırı,"popl %eax",komut == 145 ? "movsbl %al, %eax" : komut == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (komut >= 153 && komut <= 166) {
                if (komut <= 158) Collections.addAll(girdi_satırı,"popl %eax","testl %eax, %eax");
                else Collections.addAll(girdi_satırı,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int hedef_değer = konum + komut_veri.부호두바이트(); dal_Liste.add(hedef_değer); girdi_satırı.add(비교들[komut - (komut <= 158 ? 153 : 159)] + " " + işaret_değer + "_b" + hedef_değer);
            } else if (komut == 167 || komut == 200) {
                int hedef_değer = konum + (komut == 167 ? komut_veri.부호두바이트() : komut_veri.네바이트()); dal_Liste.add(hedef_değer); girdi_satırı.add("jmp " + işaret_değer + "_b" + hedef_değer);
            } else if (komut == 170 || komut == 171) {
                while (komut_veri.konum % 4 != 0) komut_veri.한바이트();
                int varsayılan_değer = konum + komut_veri.네바이트(); dal_Liste.add(varsayılan_değer); girdi_satırı.add("popl %eax");
                int öğe_BAĞ_DEĞ_SAY, 아래 = 0;
                if (komut == 170) { 아래 = komut_veri.네바이트(); int 위 = komut_veri.네바이트(); long süre_değer = (long)위 - 아래 + 1; if (süre_değer < 1 || süre_değer > (komut_veri.veri.length - komut_veri.konum) / 4) throw new Çeviri_hata("switch klip hata"); öğe_BAĞ_DEĞ_SAY = (int)süre_değer; }
                else { öğe_BAĞ_DEĞ_SAY = komut_veri.네바이트(); if (öğe_BAĞ_DEĞ_SAY < 0 || öğe_BAĞ_DEĞ_SAY > (komut_veri.veri.length - komut_veri.konum) / 8) throw new Çeviri_hata("switch Boyut hata"); }
                for (int 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) {
                    int değer = komut == 170 ? 아래 + 순번 : komut_veri.네바이트(), hedef_değer = konum + komut_veri.네바이트(); dal_Liste.add(hedef_değer);
                    Collections.addAll(girdi_satırı,"cmpl $" + değer + ", %eax","je " + işaret_değer + "_b" + hedef_değer);
                }
                girdi_satırı.add("jmp " + işaret_değer + "_b" + varsayılan_değer);
            } else if (komut == 172 || komut == 176 || komut == 177) {
                if (komut != 177) girdi_satırı.add("popl %eax"); Collections.addAll(girdi_satırı,"leave","ret");
            } else if (komut == 178 || komut == 179) {
                metot_Başvuru Başvuru = Sınıf_değer.Başvuru(komut_veri.두바이트()); if (!필드들.containsKey(Başvuru)) throw new Çeviri_hata("알 수 없는 alan_değeri");
                Collections.addAll(girdi_satırı,"call " + simge("init",Başvuru.sahip_değer),(komut == 178 ? "pushl " : "popl ") + simge("field",Başvuru.부분들()));
            } else if (komut == 184) {
                metot_Başvuru Başvuru = Sınıf_değer.Başvuru(komut_veri.두바이트()); if (!함수들.containsKey(Başvuru)) throw new Çeviri_hata("알 수 없는 işlev_değer");
                metot_tanımlayıcı çağrı_TÜR = new metot_tanımlayıcı(Başvuru.서술); Collections.addAll(girdi_satırı,"call " + simge("init",Başvuru.sahip_değer),"call " + simge("method",Başvuru.부분들()));
                if (!çağrı_TÜR.bağımsız_değişkenler.isEmpty()) girdi_satırı.add("addl $" + çağrı_TÜR.bağımsız_değişkenler.size() * 4 + ", %esp");
                if (!çağrı_TÜR.İade_KR.equals("V")) girdi_satırı.add("pushl %eax");
            } else if (komut == 182) {
                metot_Başvuru Başvuru = Sınıf_değer.Başvuru(komut_veri.두바이트());
                if (Başvuru.equals(new metot_Başvuru("java/lang/String","length","()I"))) Collections.addAll(girdi_satırı,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Başvuru.equals(new metot_Başvuru("java/lang/String","charAt","(I)C"))) Collections.addAll(girdi_satırı,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Çeviri_hata("가상 işlev_değer 호출 미지원");
            } else if (komut == 188) {
                if (komut_veri.한바이트() != 10) throw new Çeviri_hata("new int[]만 Destek_değer"); Collections.addAll(girdi_satırı,"popl %eax","call rt_new_array","pushl %eax");
            } else if (komut == 190) Collections.addAll(girdi_satırı,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (komut == 196) {
                int uzantı_değer = komut_veri.한바이트(), Dizin = komut_veri.두바이트(); çek_yerel(Dizin,yerel_BAĞ_DEĞ_SAY);
                if (uzantı_değer == 21 || uzantı_değer == 25 || uzantı_değer == 54 || uzantı_değer == 58) girdi_satırı.add((uzantı_değer <= 25 ? "pushl " : "popl ") + "-" + 4 * (Dizin + 1) + "(%ebp)");
                else if (uzantı_değer == 132) girdi_satırı.add("addl $" + komut_veri.부호두바이트() + ", -" + 4 * (Dizin + 1) + "(%ebp)");
                else throw new Çeviri_hata("wide komut 미지원");
            } else if (komut == 198 || komut == 199) {
                int hedef_değer = konum + komut_veri.부호두바이트(); dal_Liste.add(hedef_değer); Collections.addAll(girdi_satırı,"popl %eax","testl %eax, %eax",(komut == 198 ? "je " : "jne ") + işaret_değer + "_b" + hedef_değer);
            } else throw new Çeviri_hata("미지원 komut: " + komut);
        }
        if (!경계들.containsAll(dal_Liste)) throw new Çeviri_hata("komut 경계가 아닌 곳으로 dal");
        girdi_satırı.add(".size " + işaret_değer + ", .-" + işaret_değer); return String.join("\n",girdi_satırı);
    }
    String X_86_sabit(Sınıf_veri veri, int Dizin) {
        if (veri.sabit_Tip[Dizin] == 3) return veri.sabit_veri[Dizin].toString();
        if (veri.sabit_Tip[Dizin] == 8) return dize_simge(veri.문자((Integer)veri.sabit_veri[Dizin]));
        throw new Çeviri_hata("정수와 dize_değer 상수만 Destek_değer");
    }
    String X_86_derleme(String giriş_noktası, List<String> 내보냄, String hedef) throws IOException {
        Map<String,String> makine_tablo = new HashMap<>();
        for (String girdi_satırı : Files.readAllLines(kaynak_yol.resolve("_86_makine_İşlevler.tsv"))) { String[] eşleştirmek_değer = girdi_satırı.split("\t"); if (eşleştirmek_değer[0].equals(hedef)) makine_tablo.put(eşleştirmek_değer[1] + eşleştirmek_değer[2],eşleştirmek_değer[3]); }
        int konum_dizini = giriş_noktası.lastIndexOf('.'); if (konum_dizini < 0) throw new Çeviri_hata("giriş_noktası Ata_değer hata");
        String sahip_değer = giriş_noktası.substring(0,konum_dizini).replace('.','/'), metot_girdi_ad = giriş_noktası.substring(konum_dizini + 1); metot_Başvuru giriş_noktası_değer = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metot_Başvuru Başvuru = new metot_Başvuru(sahip_değer,metot_girdi_ad,서술); if (함수들.containsKey(Başvuru)) { if (giriş_noktası_değer != null) throw new Çeviri_hata("겹친 giriş_noktası"); giriş_noktası_değer = Başvuru; } }
        if (giriş_noktası_değer == null || (함수들.get(giriş_noktası_değer).erişim_girdi & 0x100) != 0) throw new Çeviri_hata("giriş_noktası_değer işlev_değer biçim_değer hata");
        List<String> girdi_satırı = new ArrayList<>(); girdi_satırı.add(".code32");
        for (Sınıf_veri veri : 클래스들.values()) {
            String Durum_değer = simge("state",veri.İsim), başlat = simge("init",veri.İsim);
            Collections.addAll(girdi_satırı,".bss",".balign 4",Durum_değer + ": .long 0",".text",başlat + ":","cmpl $0, " + Durum_değer,"jne " + başlat + "_done","movl $1, " + Durum_değer);
            metot_Başvuru başlatıcı_Başvuru = new metot_Başvuru(veri.İsim,"<clinit>","()V"); if (함수들.containsKey(başlatıcı_Başvuru)) girdi_satırı.add("call " + simge("method",başlatıcı_Başvuru.부분들()));
            Collections.addAll(girdi_satırı,"movl $2, " + Durum_değer,başlat + "_done:","ret");
            for (üye_veri alan_değeri : veri.alan_değeri) {
                byte[] sabit_değer = alan_değeri.öznitelik_değer.get("ConstantValue"); String değer = sabit_değer == null ? "0" : X_86_sabit(veri,new veri_Okuyucu(sabit_değer).두바이트());
                Collections.addAll(girdi_satırı,".data",".balign 4",simge("field",veri.İsim,alan_değeri.İsim,alan_değeri.서술) + ": .long " + değer);
            }
            for (üye_veri işlev_değer : veri.işlev_değer) if (!işlev_değer.İsim.equals("<init>")) girdi_satırı.add(X_86_metot_gövdesi(new metot_Başvuru(veri.İsim,işlev_değer.İsim,işlev_değer.서술),işlev_değer,makine_tablo,hedef));
        }
        Collections.addAll(girdi_satırı,".text",".globl java_entry","java_entry:","call " + simge("init",giriş_noktası_değer.sahip_değer),"call " + simge("method",giriş_noktası_değer.부분들()));
        if (giriş_noktası_değer.서술.equals("()V")) girdi_satırı.add("xorl %eax, %eax"); girdi_satırı.add("ret");
        for (String Ata_değer : 내보냄) {
            int sınırlayıcı_değer = Ata_değer.indexOf('='); if (sınırlayıcı_değer < 1) throw new Çeviri_hata("내보내기 Ata_değer hata");
            String dış_değer = Ata_değer.substring(0,sınırlayıcı_değer), işlev_değer = Ata_değer.substring(sınırlayıcı_değer + 1); int Bölge_KR = işlev_değer.lastIndexOf('.');
            if (Bölge_KR < 0 || !dış_değer.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Çeviri_hata("내보내기 simge hata");
            String Sınıf_değer = işlev_değer.substring(0,Bölge_KR).replace('.','/'), İsim = işlev_değer.substring(Bölge_KR + 1); metot_Başvuru seçim_değer = null;
            for (metot_Başvuru Başvuru : 함수들.keySet()) if (Başvuru.sahip_değer.equals(Sınıf_değer) && Başvuru.İsim.equals(İsim)) { if (seçim_değer != null) throw new Çeviri_hata("겹친 내보내기 hedef"); seçim_değer = Başvuru; }
            if (seçim_değer == null) throw new Çeviri_hata("내보낼 함수가 없음");
            Collections.addAll(girdi_satırı,".text",".globl " + dış_değer,dış_değer + ":","call " + simge("init",seçim_değer.sahip_değer),"jmp " + simge("method",seçim_değer.부분들()));
        }
        girdi_satırı.add(".section .rodata");
        for (Map.Entry<String,String> girdi_değer : 문자열들.entrySet()) {
            Collections.addAll(girdi_satırı,".balign 4",girdi_değer.getValue() + ":",".long " + girdi_değer.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char ders_değer : girdi_değer.getKey().toCharArray()) 단위들.add(Integer.toString(ders_değer)); if (!단위들.isEmpty()) girdi_satırı.add(".long " + String.join(",",단위들));
        }
        girdi_satırı.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",girdi_satırı) + "\n";
    }
    static void yürütmek_araç(List<String> komut) throws Exception {
        if (new ProcessBuilder(komut).inheritIO().start().waitFor() != 0) throw new Çeviri_hata("derlemek_kaynak hata: " + komut.get(0));
    }
    static String veri_dize(String metin) { return "\"" + metin.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Çeviri(List<Path> artış_Liste, String hedef, String giriş_noktası, List<String> 내보냄, Path metinÇıktısı, Path kaynak_değer) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Sınıf_yol = 임시.resolve("classes"); Files.createDirectory(Sınıf_yol);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Sınıf_yol.toString(),"-sourcepath",Sınıf_yol.toString(),"-d",Sınıf_yol.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int kaynak_BAĞ_DEĞ_SAY = 0;
            for (Path artış_değer : artış_Liste) {
                if (metinÇıktısı.toAbsolutePath().normalize().equals(artış_değer.toAbsolutePath().normalize())) throw new Çeviri_hata("metinÇıktısı 파일과 입력이 같음");
                if (artış_değer.toString().endsWith(".java")) { 자바명령.add(artış_değer.toString()); kaynak_BAĞ_DEĞ_SAY++; }
                else if (artış_değer.toString().endsWith(".class")) 바이트코드.add(artış_değer);
                else throw new Çeviri_hata(".java 또는 .class만 Destek_değer");
            }
            if (kaynak_BAĞ_DEĞ_SAY > 0) yürütmek_araç(자바명령);
            try (java.util.stream.Stream<Path> yol_Liste = Files.walk(Sınıf_yol)) { yol_Liste.filter(yol -> yol.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 ÇEVİR_değer = new 기계어미리번역(바이트코드,hedef.equals("user") ? "user" : "kernel",262144,kaynak_değer);
            String çevirmek_değer = ÇEVİR_değer.X_86_derleme(giriş_noktası,내보냄,hedef); Files.writeString(임시.resolve("program.s"),çevirmek_değer,StandardCharsets.UTF_8);
            Path araç_konum = kaynak_değer.getParent();
            yürütmek_araç(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            yürütmek_araç(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),araç_konum.resolve("CLR_Destek.s").toString()));
            List<String> Bağlan = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (hedef.equals("kernel")) Bağlan.add("-r");
            else {
                yürütmek_araç(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),araç_konum.resolve(hedef.equals("user") ? "Start_kullanıcı_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(Bağlan,"-e","_start",임시.resolve("start.o").toString());
                if (hedef.equals("user")) Collections.addAll(Bağlan,"-T",araç_konum.resolve("kullanıcı_köprü_Düzen.ld").toString());
            }
            Collections.addAll(Bağlan,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); yürütmek_araç(Bağlan);
            metinÇıktısı = metinÇıktısı.toAbsolutePath(); Files.createDirectories(metinÇıktısı.getParent()); Path yayımlamak_değer = Files.createTempFile(metinÇıktısı.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),yayımlamak_değer,StandardCopyOption.REPLACE_EXISTING); Files.move(yayımlamak_değer,metinÇıktısı,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(yayımlamak_değer); }
            Files.setPosixFilePermissions(metinÇıktısı,java.nio.file.attribute.PosixFilePermissions.fromString(hedef.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(metinÇıktısı + ".s"),çevirmek_değer,StandardCharsets.UTF_8);
            List<String> simge_veri = new ArrayList<>(), kaynak_veri = new ArrayList<>();
            for (metot_Başvuru Başvuru : ÇEVİR_değer.함수들.keySet()) simge_veri.add(veri_dize(simge("method",Başvuru.부분들())) + ":" + veri_dize(Başvuru.sahip_değer + "." + Başvuru.İsim + Başvuru.서술));
            for (Path artış_değer : artış_Liste) {
                byte[] özet_Dosya = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(artış_değer)); StringBuilder metin = new StringBuilder(); for (byte değer : özet_Dosya) metin.append(String.format(Locale.ROOT,"%02x",değer & 255));
                kaynak_veri.add(veri_dize(artış_değer.toAbsolutePath().toString()) + ":" + veri_dize(metin.toString()));
            }
            Files.writeString(Paths.get(metinÇıktısı + ".json"),"{\"target\":" + veri_dize(hedef) + ",\"entry\":" + veri_dize(giriş_noktası) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simge_veri) + "},\"sources\":{" + String.join(",",kaynak_veri) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> yol_Liste = Files.walk(임시)) { for (Path yol : (Iterable<Path>)yol_Liste.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(yol); }
        }
    }
    public static void main(String[] bağımsız_değişkenler) {
        try {
            String giriş_noktası = null, hedef = "kernel", X_86_hedef = null; Path çıktı_yol = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> yol_Liste = new ArrayList<>();
            for (int 순번 = 0; 순번 < bağımsız_değişkenler.length; 순번++) {
                String değer = bağımsız_değişkenler[순번];
                switch (değer) {
                    case "--target": X_86_hedef = bağımsız_değişkenler[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Sınıf_değer.işlev_değer -o metinÇıktısı [--target linux|kernel|user] [--profile kernel|user] [--export simge=Sınıf_değer.işlev_değer] 클래스파일 또는 Java원문"); return;
                    case "--entry": giriş_noktası = bağımsız_değişkenler[++순번]; break;
                    case "--profile": hedef = bağımsız_değişkenler[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(bağımsız_değişkenler[++순번]); break;
                    case "--export": 내보냄.add(bağımsız_değişkenler[++순번]); break;
                    case "-o": çıktı_yol = Paths.get(bağımsız_değişkenler[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (değer.startsWith("-")) throw new Çeviri_hata("알 수 없는 옵션: " + değer); yol_Liste.add(Paths.get(değer));
                }
            }
            if (giriş_noktası == null || çıktı_yol == null || yol_Liste.isEmpty()) throw new Çeviri_hata("--entry, -o, Sınıf_değer 파일이 필요합니다");
            Path kaynak_değer = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_hedef != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_hedef)) throw new Çeviri_hata("알 수 없는 yürütmek_komut hedef");
                X_86_Çeviri(yol_Liste,X_86_hedef,giriş_noktası,내보냄,çıktı_yol,kaynak_değer); return;
            }
            String kaynakKod = new 기계어미리번역(yol_Liste, hedef, 낱말수, kaynak_değer).oluşturmak(giriş_noktası, 내보냄, 범용표기);
            çıktı_yol = çıktı_yol.toAbsolutePath(); Files.createDirectories(çıktı_yol.getParent());
            Path 임시 = Files.createTempFile(çıktı_yol.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, kaynakKod, StandardCharsets.UTF_8); Files.move(임시, çıktı_yol, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception hata) { System.err.println("derlemek_kaynak hata: " + hata.getMessage()); System.exit(1); }
    }
}
