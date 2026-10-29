// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Aji_Daraja 파일에서 독립 ARM64 커널용 C 원문을 만든다. sauka JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class 번역오류 extends RuntimeException {
        번역오류(String 설명) { super(설명); }
    }
    static final class Tarin_bayani_Manazarci {
        final byte[] Tarin_bayani;
        int 위치;
        Tarin_bayani_Manazarci(byte[] 입력자료) { Tarin_bayani = 입력자료; }
        byte[] Yi_Karatu(int Tsawo_Daraja) {
            if (Tsawo_Daraja < 0 || Tsawo_Daraja > Tarin_bayani.length - 위치) throw new 번역오류("잘린 Aji_Daraja 또는 Umarni Tarin_bayani");
            byte[] 결과 = Arrays.copyOfRange(Tarin_bayani, 위치, 위치 + Tsawo_Daraja); 위치 += Tsawo_Daraja; return 결과;
        }
        int 한바이트() { if (위치 >= Tarin_bayani.length) throw new 번역오류("잘린 Umarni Tarin_bayani"); return Tarin_bayani[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class Memba_Tarin_bayani {
        final int isa_Mashigar_bayanai;
        final String Suna, 서술;
        final Map<String, byte[]> siffofi_Daraja;
        Memba_Tarin_bayani(int isa_Daraja, String Suna_Daraja, String 서술값, Map<String, byte[]> siffofi_Tarin_bayani) {
            isa_Mashigar_bayanai = isa_Daraja; Suna = Suna_Daraja; 서술 = 서술값; siffofi_Daraja = siffofi_Tarin_bayani;
        }
    }
    static final class tsari_Manazarta implements Comparable<tsari_Manazarta> {
        final String mamallaki_Daraja, Suna, 서술;
        tsari_Manazarta(String 소유값, String Suna_Daraja, String 서술값) { mamallaki_Daraja = 소유값; Suna = Suna_Daraja; 서술 = 서술값; }
        String[] 부분들() { return new String[]{mamallaki_Daraja, Suna, 서술}; }
        public int compareTo(tsari_Manazarta Fiya_Daraja) {
            int Kwatantawa_Daraja = mamallaki_Daraja.compareTo(Fiya_Daraja.mamallaki_Daraja);
            if (Kwatantawa_Daraja == 0) Kwatantawa_Daraja = Suna.compareTo(Fiya_Daraja.Suna);
            return Kwatantawa_Daraja == 0 ? 서술.compareTo(Fiya_Daraja.서술) : Kwatantawa_Daraja;
        }
        public boolean equals(Object Fiya_Daraja) { return Fiya_Daraja instanceof tsari_Manazarta && compareTo((tsari_Manazarta) Fiya_Daraja) == 0; }
        public int hashCode() { return Objects.hash(mamallaki_Daraja, Suna, 서술); }
    }
    static final class Aji_Tarin_bayani {
        final int[] 상수종류;
        final Object[] Jurarre_Tarin_bayani;
        final String Suna;
        final List<Memba_Tarin_bayani> Fili_Daraja, AIKI_Daraja;
        Aji_Tarin_bayani(Path Hanyar_shiga) throws IOException {
            Tarin_bayani_Manazarci Manazarci_Daraja = new Tarin_bayani_Manazarci(Files.readAllBytes(Hanyar_shiga));
            if (Manazarci_Daraja.네바이트() != 0xcafebabe) throw new 번역오류("Java Aji_Daraja 표식이 아님");
            Manazarci_Daraja.Yi_Karatu(4);
            int 개수 = Manazarci_Daraja.두바이트(); 상수종류 = new int[개수]; Jurarre_Tarin_bayani = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = Manazarci_Daraja.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int Tsawo_Daraja = Manazarci_Daraja.두바이트();
                        byte[] Harafi_Tunani_na_wucin_gadi = Manazarci_Daraja.Yi_Karatu(Tsawo_Daraja), 길이붙인자료 = new byte[Tsawo_Daraja + 2];
                        길이붙인자료[0] = (byte)(Tsawo_Daraja >> 8); 길이붙인자료[1] = (byte)Tsawo_Daraja;
                        System.arraycopy(Harafi_Tunani_na_wucin_gadi, 0, 길이붙인자료, 2, Tsawo_Daraja);
                        Jurarre_Tarin_bayani[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: Jurarre_Tarin_bayani[순번] = Manazarci_Daraja.네바이트(); break;
                    case 4: Manazarci_Daraja.Yi_Karatu(4); break;
                    case 5: case 6: Manazarci_Daraja.Yi_Karatu(8); 순번++; break;
                    case 7: case 8: case 16: Jurarre_Tarin_bayani[순번] = Manazarci_Daraja.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        Jurarre_Tarin_bayani[순번] = new int[]{Manazarci_Daraja.두바이트(), Manazarci_Daraja.두바이트()}; break;
                    case 15: Jurarre_Tarin_bayani[순번] = new int[]{Manazarci_Daraja.한바이트(), Manazarci_Daraja.두바이트()}; break;
                    default: throw new 번역오류("지원하지 않는 Jurarre_Daraja 종류: " + 종류);
                }
            }
            Manazarci_Daraja.두바이트(); Suna = Aji_Suna(Manazarci_Daraja.두바이트());
            if (!Aji_Suna(Manazarci_Daraja.두바이트()).equals("java/lang/Object") || Manazarci_Daraja.두바이트() != 0)
                throw new 번역오류(Suna + ": 상속 및 인터페이스 미지원");
            Fili_Daraja = 멤버읽기(Manazarci_Daraja); AIKI_Daraja = 멤버읽기(Manazarci_Daraja); 속성읽기(Manazarci_Daraja);
            if (Manazarci_Daraja.위치 != Manazarci_Daraja.Tarin_bayani.length) throw new 번역오류("Aji_Daraja 뒤에 남은 Tarin_bayani");
        }
        String 문자(int Indes) {
            if (Indes < 1 || Indes >= 상수종류.length || 상수종류[Indes] != 1) throw new 번역오류("문자 Jurarre_Daraja Indes Kuskure");
            return (String) Jurarre_Tarin_bayani[Indes];
        }
        String Aji_Suna(int Indes) {
            if (Indes < 1 || Indes >= 상수종류.length || 상수종류[Indes] != 7) throw new 번역오류("Aji_Daraja Manazarta Kuskure");
            return 문자((Integer)Jurarre_Tarin_bayani[Indes]);
        }
        tsari_Manazarta Manazarta(int Indes) {
            if (Indes < 1 || Indes >= 상수종류.length || 상수종류[Indes] < 9 || 상수종류[Indes] > 11) throw new 번역오류("멤버 Manazarta Kuskure");
            int[] jona_Daraja = (int[])Jurarre_Tarin_bayani[Indes], Suna_jona = (int[])Jurarre_Tarin_bayani[jona_Daraja[1]];
            return new tsari_Manazarta(Aji_Suna(jona_Daraja[0]), 문자(Suna_jona[0]), 문자(Suna_jona[1]));
        }
        Map<String, byte[]> 속성읽기(Tarin_bayani_Manazarci Manazarci_Daraja) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = Manazarci_Daraja.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String siffofi_Suna = 문자(Manazarci_Daraja.두바이트()); byte[] Daraja = Manazarci_Daraja.Yi_Karatu(Manazarci_Daraja.네바이트());
                if (결과.put(siffofi_Suna, Daraja) != null) throw new 번역오류("겹친 siffofi_Daraja: " + siffofi_Suna);
            }
            return 결과;
        }
        List<Memba_Tarin_bayani> 멤버읽기(Tarin_bayani_Manazarci Manazarci_Daraja) {
            List<Memba_Tarin_bayani> 결과 = new ArrayList<>(); int 개수 = Manazarci_Daraja.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int isa_Mashigar_bayanai = Manazarci_Daraja.두바이트(); String tsari_Mashigar_bayanai_Suna = 문자(Manazarci_Daraja.두바이트()), 서술 = 문자(Manazarci_Daraja.두바이트());
                결과.add(new Memba_Tarin_bayani(isa_Mashigar_bayanai, tsari_Mashigar_bayanai_Suna, 서술, 속성읽기(Manazarci_Daraja)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new 번역오류("AIKI_Daraja 서술 Kuskure: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new 번역오류("AIKI_Daraja 서술 Kuskure: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new 번역오류("AIKI_Daraja 서술 Kuskure: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String bangaren_zaɓi_Daraja = null;
            for (String zubi_Daraja : 허용형식) if (서술.startsWith(zubi_Daraja, 위치)) { bangaren_zaɓi_Daraja = zubi_Daraja; break; }
            if (bangaren_zaɓi_Daraja == null) throw new 번역오류("지원하지 않는 Nau_in_tarin_bayani: " + 서술);
            결과.add(bangaren_zaɓi_Daraja); 위치 += bangaren_zaɓi_Daraja.length();
        }
        return 결과;
    }
    static String alama_ad6f1a96(String 종류, String... 부분들) {
        try {
            byte[] hash_Fayil = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", hash_Fayil[순번] & 255));
            return SMS.toString();
        } catch (Exception Kuskure) { throw new 번역오류(Kuskure.toString()); }
    }
    final Map<String, Aji_Tarin_bayani> 클래스들 = new TreeMap<>();
    final Map<tsari_Manazarta, Memba_Tarin_bayani> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, na_ura_mai_kwakwalwa_Aji;
    final int 동적기억낱말수;
    final Path albarkatu_Hanyar_shiga;
    기계어미리번역(List<Path> Hanyar_shiga_Jeri, String tageti, int 낱말수, Path albarkatu_Daraja) throws IOException {
        if ((!tageti.equals("kernel") && !tageti.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new 번역오류("gudanar_Umarni tageti 또는 Mahardatar_kwamfuta_Daraja 공간 Girma Kuskure");
        실행대상 = tageti; 동적기억낱말수 = 낱말수; albarkatu_Hanyar_shiga = albarkatu_Daraja;
        // 이 이름도 국가별 tushe_Li_irabin_tarin_bayanai 생성 시 해당 언어로 옮긴다.
        na_ura_mai_kwakwalwa_Aji = tageti.equals("kernel") ? "보드" : "Mai_anfani_da_kwamfuta";
        for (String Layi : Files.readAllLines(albarkatu_Daraja.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Layi.split("\t", -1);
            if (부분들.length != 4) throw new 번역오류("na_ura_mai_kwakwalwa AIKI_Daraja Tarin_bayani Kuskure");
            if (부분들[0].equals(tageti)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Hanyar_shiga : Hanyar_shiga_Jeri) {
            Aji_Tarin_bayani Tarin_bayani = new Aji_Tarin_bayani(Hanyar_shiga);
            if (클래스들.put(Tarin_bayani.Suna, Tarin_bayani) != null) throw new 번역오류("중복 Aji_Daraja: " + Tarin_bayani.Suna);
            for (Memba_Tarin_bayani Fili_Daraja : Tarin_bayani.Fili_Daraja) {
                if ((Fili_Daraja.isa_Mashigar_bayanai & 8) == 0 || 형식읽기(Fili_Daraja.서술).equals(Collections.singletonList("V"))) throw new 번역오류("Tsaye_cik_Daraja 필드만 taimako_Daraja");
                if (필드들.put(new tsari_Manazarta(Tarin_bayani.Suna, Fili_Daraja.Suna, Fili_Daraja.서술), Fili_Daraja) != null) throw new 번역오류("중복 Fili_Daraja");
            }
            for (Memba_Tarin_bayani AIKI_Daraja : Tarin_bayani.AIKI_Daraja) {
                if (AIKI_Daraja.Suna.equals("<init>")) continue;
                if ((AIKI_Daraja.isa_Mashigar_bayanai & 8) == 0 || (AIKI_Daraja.isa_Mashigar_bayanai & (0x20 | 0x400)) != 0) throw new 번역오류("Tsaye_cik_Daraja 비동기화 함수만 taimako_Daraja");
                new 함수형식(AIKI_Daraja.서술);
                if (함수들.put(new tsari_Manazarta(Tarin_bayani.Suna, AIKI_Daraja.Suna, AIKI_Daraja.서술), AIKI_Daraja) != null) throw new 번역오류("중복 AIKI_Daraja");
            }
        }
    }
    String Zare_alama(String SMS) { return 문자열들.computeIfAbsent(SMS, Daraja -> "j_text_" + 문자열들.size()); }
    String Jurarre_Aiyana_alƙaluma(Aji_Tarin_bayani Tarin_bayani, int Indes) {
        if (Indes < 1 || Indes >= Tarin_bayani.상수종류.length) throw new 번역오류("Jurarre_Daraja Indes darfi Kuskure");
        if (Tarin_bayani.상수종류[Indes] == 3) return "(word)(uint32_t)(" + Tarin_bayani.Jurarre_Tarin_bayani[Indes] + ")";
        if (Tarin_bayani.상수종류[Indes] == 8) return "(word)" + Zare_alama(Tarin_bayani.문자((Integer)Tarin_bayani.Jurarre_Tarin_bayani[Indes]));
        throw new 번역오류("정수와 Zare_Daraja 상수만 taimako_Daraja");
    }
    String 함수원형(tsari_Manazarta Manazarta) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Manazarta.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + alama_ad6f1a96("method", Manazarta.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void Bincika_na_gida(int Indes, int 지역변수수) { if (Indes < 0 || Indes >= 지역변수수) throw new 번역오류("na_gida_Kima 변수 Indes darfi Kuskure"); }
    void 분기넣기(List<String> 출력, Set<Integer> Reshe_Jeri, int 위치, int 이동량, String Yanayi) {
        int Zangon_ƙarshe_Daraja = 위치 + 이동량; Reshe_Jeri.add(Zangon_ƙarshe_Daraja);
        출력.add((Yanayi == null ? "" : "if (" + Yanayi + ") ") + "goto b" + Zangon_ƙarshe_Daraja + ";");
    }
    String tsari_jiki(tsari_Manazarta AIKI_Daraja, Memba_Tarin_bayani Tarin_bayani) {
        byte[] jiki_Tarin_bayani = Tarin_bayani.siffofi_Daraja.get("Code"); if (jiki_Tarin_bayani == null) throw new 번역오류("AIKI_Daraja 몸체가 없음: " + AIKI_Daraja.Suna);
        Tarin_bayani_Manazarci Manazarci_Daraja = new Tarin_bayani_Manazarci(jiki_Tarin_bayani); int 쌓임깊이 = Manazarci_Daraja.두바이트(), 지역변수수 = Manazarci_Daraja.두바이트();
        Tarin_bayani_Manazarci Umarni_Tarin_bayani = new Tarin_bayani_Manazarci(Manazarci_Daraja.Yi_Karatu(Manazarci_Daraja.네바이트()));
        if (Manazarci_Daraja.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 zubi_Daraja = new 함수형식(AIKI_Daraja.서술); if (지역변수수 < zubi_Daraja.인수.size()) throw new 번역오류("매개변수보다 적은 na_gida_Kima 변수");
        Aji_Tarin_bayani Aji_Daraja = 클래스들.get(AIKI_Daraja.mamallaki_Daraja);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(AIKI_Daraja) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < zubi_Daraja.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), Reshe_Jeri = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (Umarni_Tarin_bayani.위치 < Umarni_Tarin_bayani.Tarin_bayani.length) {
            int 위치 = Umarni_Tarin_bayani.위치, Umarni = Umarni_Tarin_bayani.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (Umarni == 0) continue;
            if (Umarni == 1) 출력.add("PUSH(0);");
            else if (Umarni >= 2 && Umarni <= 8) 출력.add("PUSH((uint32_t)(" + (Umarni - 3) + "));");
            else if (Umarni == 16 || Umarni == 17) 출력.add("PUSH((uint32_t)(" + (Umarni == 16 ? Umarni_Tarin_bayani.부호한바이트() : Umarni_Tarin_bayani.부호두바이트()) + "));");
            else if (Umarni == 18 || Umarni == 19) 출력.add("PUSH(" + Jurarre_Aiyana_alƙaluma(Aji_Daraja, Umarni == 18 ? Umarni_Tarin_bayani.한바이트() : Umarni_Tarin_bayani.두바이트()) + ");");
            else if (Umarni == 21 || Umarni == 25 || (Umarni >= 26 && Umarni <= 29) || (Umarni >= 42 && Umarni <= 45)) {
                int Indes = Umarni == 21 || Umarni == 25 ? Umarni_Tarin_bayani.한바이트() : Umarni - (Umarni <= 29 ? 26 : 42);
                Bincika_na_gida(Indes, 지역변수수); 출력.add("PUSH(l[" + Indes + "]);");
            } else if (Umarni == 54 || Umarni == 58 || (Umarni >= 59 && Umarni <= 62) || (Umarni >= 75 && Umarni <= 78)) {
                int Indes = Umarni == 54 || Umarni == 58 ? Umarni_Tarin_bayani.한바이트() : Umarni - (Umarni <= 62 ? 59 : 75);
                Bincika_na_gida(Indes, 지역변수수); 출력.add("l[" + Indes + "] = POP();");
            } else if (Umarni == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Umarni == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Umarni == 87 || Umarni == 88) 출력.add(Umarni == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Umarni >= 89 && Umarni <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] Hanyar_jejjerawa_Jeri = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Umarni - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char Daraja : Hanyar_jejjerawa_Jeri[Umarni - 89].toCharArray()) 출력.add("PUSH(" + Daraja + ");");
            } else if (Umarni == 96 || Umarni == 100 || Umarni == 104 || Umarni == 126 || Umarni == 128 || Umarni == 130) {
                String aiki_Daraja = Umarni == 96 ? "+" : Umarni == 100 ? "-" : Umarni == 104 ? "*" : Umarni == 126 ? "&" : Umarni == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + aiki_Daraja + " (uint32_t)b);");
            } else if (Umarni == 108 || Umarni == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Umarni == 112 ? 1 : 0) + "));");
            else if (Umarni == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Umarni == 120 || Umarni == 122 || Umarni == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Umarni == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Umarni == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Umarni == 132) {
                int Indes = Umarni_Tarin_bayani.한바이트(), 증가량 = Umarni_Tarin_bayani.부호한바이트(); Bincika_na_gida(Indes, 지역변수수);
                출력.add("l[" + Indes + "] = (uint32_t)l[" + Indes + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Umarni >= 145 && Umarni <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Umarni == 145 ? "int8_t" : Umarni == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Umarni >= 153 && Umarni <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, Reshe_Jeri, 위치, Umarni_Tarin_bayani.부호두바이트(), "(int32_t)a " + 비교들[Umarni - 153] + " 0");
            } else if (Umarni >= 159 && Umarni <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, Reshe_Jeri, 위치, Umarni_Tarin_bayani.부호두바이트(), Umarni >= 165 ? "a " + 비교들[Umarni - 159] + " b" : "(int32_t)a " + 비교들[Umarni - 159] + " (int32_t)b");
            } else if (Umarni == 167 || Umarni == 200) 분기넣기(출력, Reshe_Jeri, 위치, Umarni == 167 ? Umarni_Tarin_bayani.부호두바이트() : Umarni_Tarin_bayani.네바이트(), null);
            else if (Umarni == 170 || Umarni == 171) {
                while (Umarni_Tarin_bayani.위치 % 4 != 0) Umarni_Tarin_bayani.한바이트();
                int Tanadaddiyar_daraja = Umarni_Tarin_bayani.네바이트(); 출력.add("a = POP();");
                if (Umarni == 170) {
                    int 아래 = Umarni_Tarin_bayani.네바이트(), 위 = Umarni_Tarin_bayani.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (Umarni_Tarin_bayani.Tarin_bayani.length - Umarni_Tarin_bayani.위치) / 4) throw new 번역오류("switch darfi Kuskure");
                    for (long Daraja = 아래; Daraja <= 위; Daraja++) 분기넣기(출력, Reshe_Jeri, 위치, Umarni_Tarin_bayani.네바이트(), "(int32_t)a == (" + Daraja + ")");
                } else {
                    int 개수 = Umarni_Tarin_bayani.네바이트(), kyamarar_gaba_Tarin_bayani = 0;
                    if (개수 < 0 || 개수 > (Umarni_Tarin_bayani.Tarin_bayani.length - Umarni_Tarin_bayani.위치) / 8) throw new 번역오류("switch Girma Kuskure");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int Daraja = Umarni_Tarin_bayani.네바이트(); if (순번 > 0 && Daraja <= kyamarar_gaba_Tarin_bayani) throw new 번역오류("switch Hanyar_jejjerawa_Daraja Kuskure"); kyamarar_gaba_Tarin_bayani = Daraja;
                        분기넣기(출력, Reshe_Jeri, 위치, Umarni_Tarin_bayani.네바이트(), "(int32_t)a == (" + Daraja + ")");
                    }
                }
                분기넣기(출력, Reshe_Jeri, 위치, Tanadaddiyar_daraja, null);
            } else if (Umarni == 172 || Umarni == 176 || Umarni == 177) 출력.add("return " + (Umarni == 177 ? "0" : "POP()") + ";");
            else if (Umarni == 178 || Umarni == 179) {
                tsari_Manazarta Manazarta = Aji_Daraja.Manazarta(Umarni_Tarin_bayani.두바이트()); if (!필드들.containsKey(Manazarta)) throw new 번역오류("알 수 없는 Fili_Daraja");
                출력.add(alama_ad6f1a96("init", Manazarta.mamallaki_Daraja) + "();"); String Fili_Daraja = alama_ad6f1a96("field", Manazarta.부분들());
                출력.add(Umarni == 178 ? "PUSH(" + Fili_Daraja + ");" : Fili_Daraja + " = POP();");
            } else if (Umarni == 184) {
                tsari_Manazarta Manazarta = Aji_Daraja.Manazarta(Umarni_Tarin_bayani.두바이트()); if (!함수들.containsKey(Manazarta)) throw new 번역오류("알 수 없는 AIKI_Daraja");
                함수형식 호출형식 = new 함수형식(Manazarta.서술); int 개수 = 호출형식.인수.size();
                출력.add(alama_ad6f1a96("init", Manazarta.mamallaki_Daraja) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + alama_ad6f1a96("method", Manazarta.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Umarni == 182) {
                tsari_Manazarta Manazarta = Aji_Daraja.Manazarta(Umarni_Tarin_bayani.두바이트());
                if (Manazarta.equals(new tsari_Manazarta("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Manazarta.equals(new tsari_Manazarta("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 번역오류("가상 AIKI_Daraja 호출 미지원");
            } else if (Umarni == 188) {
                if (Umarni_Tarin_bayani.한바이트() != 10) throw new 번역오류("new int[]만 taimako_Daraja"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Umarni == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Umarni == 196) {
                int faɗi_Daraja = Umarni_Tarin_bayani.한바이트(), Indes = Umarni_Tarin_bayani.두바이트(); Bincika_na_gida(Indes, 지역변수수);
                if (faɗi_Daraja == 21 || faɗi_Daraja == 25) 출력.add("PUSH(l[" + Indes + "]);");
                else if (faɗi_Daraja == 54 || faɗi_Daraja == 58) 출력.add("l[" + Indes + "] = POP();");
                else if (faɗi_Daraja == 132) 출력.add("l[" + Indes + "] = (uint32_t)l[" + Indes + "] + (uint32_t)(" + Umarni_Tarin_bayani.부호두바이트() + ");");
                else throw new 번역오류("미지원 wide Umarni");
            } else if (Umarni == 198 || Umarni == 199) {
                출력.add("a = POP();"); 분기넣기(출력, Reshe_Jeri, 위치, Umarni_Tarin_bayani.부호두바이트(), "a " + (Umarni == 198 ? "==" : "!=") + " 0");
            } else throw new 번역오류(AIKI_Daraja.mamallaki_Daraja + "." + AIKI_Daraja.Suna + ", bayit_Daraja " + 위치 + ": 미지원 Umarni " + Umarni);
        }
        if (!경계들.containsAll(Reshe_Jeri)) throw new 번역오류("Umarni 경계가 아닌 곳으로 Reshe");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String Fitar_da_tsari(String Kafa_alama, String tageti, boolean 진입점여부) {
        int 자리 = tageti.lastIndexOf('.'); if (자리 < 0 || !Kafa_alama.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 sanya_Daraja Kuskure");
        String mamallaki_Daraja = tageti.substring(0, 자리).replace('.', '/'), Suna = tageti.substring(자리 + 1); tsari_Manazarta bangaren_zaɓi_Daraja = null;
        for (tsari_Manazarta Manazarta : 함수들.keySet()) if (Manazarta.mamallaki_Daraja.equals(mamallaki_Daraja) && Manazarta.Suna.equals(Suna)) {
            if (bangaren_zaɓi_Daraja != null) throw new 번역오류("겹친 내보내기 tageti"); bangaren_zaɓi_Daraja = Manazarta;
        }
        if (bangaren_zaɓi_Daraja == null || (함수들.get(bangaren_zaɓi_Daraja).isa_Mashigar_bayanai & 0x100) != 0) throw new 번역오류("내보낼 함수가 없음 또는 native AIKI_Daraja");
        함수형식 zubi_Daraja = new 함수형식(bangaren_zaɓi_Daraja.서술);
        if ((진입점여부 && !zubi_Daraja.인수.isEmpty()) || !Arrays.asList("V", "I").contains(zubi_Daraja.반환)) throw new 번역오류("Mashigar_bayanai_maki_Daraja 또는 C 경계 zubi_Daraja Kuskure");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < zubi_Daraja.인수.size(); 순번++) {
            if (!zubi_Daraja.인수.get(순번).equals("I")) throw new 번역오류("C 경계는 int 인수만 taimako_Daraja");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (zubi_Daraja.반환.equals("V") ? "void " : "int32_t ") + Kafa_alama + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + alama_ad6f1a96("init", bangaren_zaɓi_Daraja.mamallaki_Daraja) + "(); " + (zubi_Daraja.반환.equals("V") ? "" : "return (int32_t)") + alama_ad6f1a96("method", bangaren_zaɓi_Daraja.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String Mashigar_bayanai_maki, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<tsari_Manazarta, Memba_Tarin_bayani> Mashigar_bayanai_Daraja : 함수들.entrySet()) {
            tsari_Manazarta Manazarta = Mashigar_bayanai_Daraja.getKey(); Memba_Tarin_bayani Tarin_bayani = Mashigar_bayanai_Daraja.getValue(); 선언들.add(함수원형(Manazarta) + ";");
            if ((Tarin_bayani.isa_Mashigar_bayanai & 0x100) != 0) {
                String Haɗi = 기계함수들.get(Manazarta.Suna + Manazarta.서술);
                if (!Manazarta.mamallaki_Daraja.equals(na_ura_mai_kwakwalwa_Aji) || Haɗi == null) throw new 번역오류("허용되지 않은 native AIKI_Daraja: " + Manazarta.Suna);
                int 개수 = new 함수형식(Manazarta.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Haɗi + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Manazarta) + " { return " + Haɗi + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(tsari_jiki(Manazarta, Tarin_bayani));
        }
        for (Map.Entry<tsari_Manazarta, Memba_Tarin_bayani> Mashigar_bayanai_Daraja : 필드들.entrySet()) {
            tsari_Manazarta Manazarta = Mashigar_bayanai_Daraja.getKey(); byte[] Jurarre_Daraja = Mashigar_bayanai_Daraja.getValue().siffofi_Daraja.get("ConstantValue");
            String Daraja = Jurarre_Daraja == null ? "0" : Jurarre_Aiyana_alƙaluma(클래스들.get(Manazarta.mamallaki_Daraja), new Tarin_bayani_Manazarci(Jurarre_Daraja).두바이트());
            필드선언들.add("static word " + alama_ad6f1a96("field", Manazarta.부분들()) + " = " + Daraja + ";");
        }
        for (String Suna : 클래스들.keySet()) {
            String Farko = alama_ad6f1a96("init", Suna), Matsayi_Daraja = alama_ad6f1a96("state", Suna);
            선언들.add("static void " + Farko + "(void);"); 필드선언들.add("static unsigned " + Matsayi_Daraja + ";");
            tsari_Manazarta Manazarta = new tsari_Manazarta(Suna, "<clinit>", "()V");
            몸체들.add("static void " + Farko + "(void) { if(" + Matsayi_Daraja + ") return; " + Matsayi_Daraja + " = 1; " + (함수들.containsKey(Manazarta) ? alama_ad6f1a96("method", Manazarta.부분들()) + "(); " : "") + Matsayi_Daraja + " = 2; }");
        }
        몸체들.add(Fitar_da_tsari("java_entry", Mashigar_bayanai_maki, true)); Set<String> 공개이름 = new HashSet<>();
        for (String sanya_Daraja : 내보내기목록) {
            int 자리 = sanya_Daraja.indexOf('='); if (자리 < 1) throw new 번역오류("내보내기 sanya_Daraja Kuskure");
            String Suna = sanya_Daraja.substring(0, 자리); 공개이름.add(Suna); 몸체들.add(Fitar_da_tsari(Suna, sanya_Daraja.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> Mashigar_bayanai_Daraja : 문자열들.entrySet()) {
            String SMS = Mashigar_bayanai_Daraja.getKey(); StringBuilder TSARI_Daraja = new StringBuilder("static const word " + Mashigar_bayanai_Daraja.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) TSARI_Daraja.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(TSARI_Daraja.append("};").toString());
        }
        String taimako_Daraja = Files.readString(albarkatu_Hanyar_shiga.resolve("lokacin_bude_yaren_gama_gari_taimako.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(taimako_Daraja + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String tushe, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> Suna_tebur = new HashMap<>();
        for (String Layi : Files.readAllLines(albarkatu_Hanyar_shiga.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] jona_Daraja = Layi.split("\t"); Suna_tebur.put(jona_Daraja[0], jona_Daraja[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(tushe); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Suna = 찾개.group(), 새이름 = Suna;
            if (!Suna.startsWith("//") && !Suna.startsWith("/*") && !Suna.startsWith("\"") && !Suna.startsWith("'") && !공개이름.contains(Suna)) {
                새이름 = Suna_tebur.getOrDefault(Suna, Suna);
                if (Suna.matches("a[0-9]+")) 새이름 = "인수" + Suna.substring(1);
                if (Suna.matches("b[0-9]+")) 새이름 = "Reshe" + Suna.substring(1);
                if (범용표기) {
                    StringBuilder alama_Daraja_5d6b9af8 = new StringBuilder();
                    for (char Harafi_Daraja : 새이름.toCharArray()) alama_Daraja_5d6b9af8.append(Harafi_Daraja < 128 ? Character.toString(Harafi_Daraja) : String.format(Locale.ROOT, "\\u%04x", (int)Harafi_Daraja));
                    새이름 = alama_Daraja_5d6b9af8.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String Maɓallin_X_86_tsari_jiki(tsari_Manazarta AIKI_Daraja, Memba_Tarin_bayani Tarin_bayani, Map<String,String> na_ura_mai_kwakwalwa_tebur, String tageti) {
        String 표식 = alama_ad6f1a96("method", AIKI_Daraja.부분들());
        List<String> Layi = new ArrayList<>();
        if ((Tarin_bayani.isa_Mashigar_bayanai & 0x100) != 0) {
            String Haɗi = na_ura_mai_kwakwalwa_tebur.get(AIKI_Daraja.Suna + AIKI_Daraja.서술);
            if (!AIKI_Daraja.mamallaki_Daraja.equals(tageti.equals("kernel") ? "na_ura_Daraja" : "Mai_anfani_da_kwamfuta") || Haɗi == null) throw new 번역오류("허용되지 않은 native AIKI_Daraja");
            return ".text\n" + 표식 + ":\njmp " + Haɗi;
        }
        byte[] Gundarin_zube = Tarin_bayani.siffofi_Daraja.get("Code"); if (Gundarin_zube == null) throw new 번역오류("AIKI_Daraja 몸체가 없음");
        Tarin_bayani_Manazarci Manazarci_Daraja = new Tarin_bayani_Manazarci(Gundarin_zube); Manazarci_Daraja.두바이트(); int 지역수 = Manazarci_Daraja.두바이트();
        Tarin_bayani_Manazarci Umarni_Tarin_bayani = new Tarin_bayani_Manazarci(Manazarci_Daraja.Yi_Karatu(Manazarci_Daraja.네바이트()));
        if (Manazarci_Daraja.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 zubi_Daraja = new 함수형식(AIKI_Daraja.서술); if (지역수 < zubi_Daraja.인수.size()) throw new 번역오류("매개변수보다 적은 na_gida_Kima 변수");
        Collections.addAll(Layi,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < zubi_Daraja.인수.size(); 순번++) Collections.addAll(Layi,"movl " + (8 + 4 * (zubi_Daraja.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Aji_Tarin_bayani Aji_Daraja = 클래스들.get(AIKI_Daraja.mamallaki_Daraja); Set<Integer> 경계들 = new HashSet<>(), Reshe_Jeri = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (Umarni_Tarin_bayani.위치 < Umarni_Tarin_bayani.Tarin_bayani.length) {
            int 위치 = Umarni_Tarin_bayani.위치, Umarni = Umarni_Tarin_bayani.한바이트(); String 자리 = 표식 + "_b" + 위치;
            Layi.add(자리 + ":"); 경계들.add(위치);
            if (Umarni == 0) Layi.add("nop");
            else if (Umarni == 1) Layi.add("pushl $0");
            else if (Umarni >= 2 && Umarni <= 8) Layi.add("pushl $" + (Umarni - 3));
            else if (Umarni == 16 || Umarni == 17) Layi.add("pushl $" + (Umarni == 16 ? Umarni_Tarin_bayani.부호한바이트() : Umarni_Tarin_bayani.부호두바이트()));
            else if (Umarni == 18 || Umarni == 19) {
                int Indes = Umarni == 18 ? Umarni_Tarin_bayani.한바이트() : Umarni_Tarin_bayani.두바이트();
                Layi.add("pushl $" + Maɓallin_X_86_Jurarre(Aji_Daraja,Indes));
            } else if (Umarni == 21 || Umarni == 25 || (Umarni >= 26 && Umarni <= 29) || (Umarni >= 42 && Umarni <= 45) || Umarni == 54 || Umarni == 58 || (Umarni >= 59 && Umarni <= 62) || (Umarni >= 75 && Umarni <= 78)) {
                boolean 읽음 = Umarni < 54; int Indes = Umarni == 21 || Umarni == 25 || Umarni == 54 || Umarni == 58 ? Umarni_Tarin_bayani.한바이트() : Umarni - (Umarni <= 29 ? 26 : Umarni <= 45 ? 42 : Umarni <= 62 ? 59 : 75);
                Bincika_na_gida(Indes,지역수); Layi.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (Indes + 1)) + "(%ebp)");
            } else if (Umarni == 46) Collections.addAll(Layi,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Umarni == 79) Collections.addAll(Layi,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Umarni == 87 || Umarni == 88) Layi.add("addl $" + (Umarni == 87 ? 4 : 8) + ", %esp");
            else if (Umarni >= 89 && Umarni <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] Hanyar_jejjerawa_Jeri = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Umarni - 89]; 순번++) Layi.add("popl " + 저장기들[순번]);
                for (int 순번 : Hanyar_jejjerawa_Jeri[Umarni - 89]) Layi.add("pushl " + 저장기들[순번]);
            } else if (Umarni == 96 || Umarni == 100 || Umarni == 104 || Umarni == 126 || Umarni == 128 || Umarni == 130) {
                String aiki_Daraja = Umarni == 96 ? "addl" : Umarni == 100 ? "subl" : Umarni == 104 ? "imull" : Umarni == 126 ? "andl" : Umarni == 128 ? "orl" : "xorl";
                Collections.addAll(Layi,"popl %ecx","popl %eax",aiki_Daraja + " %ecx, %eax","pushl %eax");
            } else if (Umarni == 108 || Umarni == 112) Collections.addAll(Layi,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Umarni == 108 ? "%eax" : "%edx"));
            else if (Umarni == 116) Layi.add("negl (%esp)");
            else if (Umarni == 120 || Umarni == 122 || Umarni == 124) Collections.addAll(Layi,"popl %ecx","popl %eax",(Umarni == 120 ? "sall" : Umarni == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Umarni == 132) {
                int Indes = Umarni_Tarin_bayani.한바이트(), 증가 = Umarni_Tarin_bayani.부호한바이트(); Bincika_na_gida(Indes,지역수); Layi.add("addl $" + 증가 + ", -" + (4 * (Indes + 1)) + "(%ebp)");
            } else if (Umarni >= 145 && Umarni <= 147) Collections.addAll(Layi,"popl %eax",Umarni == 145 ? "movsbl %al, %eax" : Umarni == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Umarni >= 153 && Umarni <= 166) {
                if (Umarni <= 158) Collections.addAll(Layi,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Layi,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int Zangon_ƙarshe_Daraja = 위치 + Umarni_Tarin_bayani.부호두바이트(); Reshe_Jeri.add(Zangon_ƙarshe_Daraja); Layi.add(비교들[Umarni - (Umarni <= 158 ? 153 : 159)] + " " + 표식 + "_b" + Zangon_ƙarshe_Daraja);
            } else if (Umarni == 167 || Umarni == 200) {
                int Zangon_ƙarshe_Daraja = 위치 + (Umarni == 167 ? Umarni_Tarin_bayani.부호두바이트() : Umarni_Tarin_bayani.네바이트()); Reshe_Jeri.add(Zangon_ƙarshe_Daraja); Layi.add("jmp " + 표식 + "_b" + Zangon_ƙarshe_Daraja);
            } else if (Umarni == 170 || Umarni == 171) {
                while (Umarni_Tarin_bayani.위치 % 4 != 0) Umarni_Tarin_bayani.한바이트();
                int Tanadaddiyar_daraja = 위치 + Umarni_Tarin_bayani.네바이트(); Reshe_Jeri.add(Tanadaddiyar_daraja); Layi.add("popl %eax");
                int 개수, 아래 = 0;
                if (Umarni == 170) { 아래 = Umarni_Tarin_bayani.네바이트(); int 위 = Umarni_Tarin_bayani.네바이트(); long Tsawo_Daraja = (long)위 - 아래 + 1; if (Tsawo_Daraja < 1 || Tsawo_Daraja > (Umarni_Tarin_bayani.Tarin_bayani.length - Umarni_Tarin_bayani.위치) / 4) throw new 번역오류("switch darfi Kuskure"); 개수 = (int)Tsawo_Daraja; }
                else { 개수 = Umarni_Tarin_bayani.네바이트(); if (개수 < 0 || 개수 > (Umarni_Tarin_bayani.Tarin_bayani.length - Umarni_Tarin_bayani.위치) / 8) throw new 번역오류("switch Girma Kuskure"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int Daraja = Umarni == 170 ? 아래 + 순번 : Umarni_Tarin_bayani.네바이트(), Zangon_ƙarshe_Daraja = 위치 + Umarni_Tarin_bayani.네바이트(); Reshe_Jeri.add(Zangon_ƙarshe_Daraja);
                    Collections.addAll(Layi,"cmpl $" + Daraja + ", %eax","je " + 표식 + "_b" + Zangon_ƙarshe_Daraja);
                }
                Layi.add("jmp " + 표식 + "_b" + Tanadaddiyar_daraja);
            } else if (Umarni == 172 || Umarni == 176 || Umarni == 177) {
                if (Umarni != 177) Layi.add("popl %eax"); Collections.addAll(Layi,"leave","ret");
            } else if (Umarni == 178 || Umarni == 179) {
                tsari_Manazarta Manazarta = Aji_Daraja.Manazarta(Umarni_Tarin_bayani.두바이트()); if (!필드들.containsKey(Manazarta)) throw new 번역오류("알 수 없는 Fili_Daraja");
                Collections.addAll(Layi,"call " + alama_ad6f1a96("init",Manazarta.mamallaki_Daraja),(Umarni == 178 ? "pushl " : "popl ") + alama_ad6f1a96("field",Manazarta.부분들()));
            } else if (Umarni == 184) {
                tsari_Manazarta Manazarta = Aji_Daraja.Manazarta(Umarni_Tarin_bayani.두바이트()); if (!함수들.containsKey(Manazarta)) throw new 번역오류("알 수 없는 AIKI_Daraja");
                함수형식 호출형식 = new 함수형식(Manazarta.서술); Collections.addAll(Layi,"call " + alama_ad6f1a96("init",Manazarta.mamallaki_Daraja),"call " + alama_ad6f1a96("method",Manazarta.부분들()));
                if (!호출형식.인수.isEmpty()) Layi.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) Layi.add("pushl %eax");
            } else if (Umarni == 182) {
                tsari_Manazarta Manazarta = Aji_Daraja.Manazarta(Umarni_Tarin_bayani.두바이트());
                if (Manazarta.equals(new tsari_Manazarta("java/lang/String","length","()I"))) Collections.addAll(Layi,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Manazarta.equals(new tsari_Manazarta("java/lang/String","charAt","(I)C"))) Collections.addAll(Layi,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 번역오류("가상 AIKI_Daraja 호출 미지원");
            } else if (Umarni == 188) {
                if (Umarni_Tarin_bayani.한바이트() != 10) throw new 번역오류("new int[]만 taimako_Daraja"); Collections.addAll(Layi,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Umarni == 190) Collections.addAll(Layi,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Umarni == 196) {
                int faɗi_Daraja = Umarni_Tarin_bayani.한바이트(), Indes = Umarni_Tarin_bayani.두바이트(); Bincika_na_gida(Indes,지역수);
                if (faɗi_Daraja == 21 || faɗi_Daraja == 25 || faɗi_Daraja == 54 || faɗi_Daraja == 58) Layi.add((faɗi_Daraja <= 25 ? "pushl " : "popl ") + "-" + 4 * (Indes + 1) + "(%ebp)");
                else if (faɗi_Daraja == 132) Layi.add("addl $" + Umarni_Tarin_bayani.부호두바이트() + ", -" + 4 * (Indes + 1) + "(%ebp)");
                else throw new 번역오류("wide Umarni 미지원");
            } else if (Umarni == 198 || Umarni == 199) {
                int Zangon_ƙarshe_Daraja = 위치 + Umarni_Tarin_bayani.부호두바이트(); Reshe_Jeri.add(Zangon_ƙarshe_Daraja); Collections.addAll(Layi,"popl %eax","testl %eax, %eax",(Umarni == 198 ? "je " : "jne ") + 표식 + "_b" + Zangon_ƙarshe_Daraja);
            } else throw new 번역오류("미지원 Umarni: " + Umarni);
        }
        if (!경계들.containsAll(Reshe_Jeri)) throw new 번역오류("Umarni 경계가 아닌 곳으로 Reshe");
        Layi.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",Layi);
    }
    String Maɓallin_X_86_Jurarre(Aji_Tarin_bayani Tarin_bayani, int Indes) {
        if (Tarin_bayani.상수종류[Indes] == 3) return Tarin_bayani.Jurarre_Tarin_bayani[Indes].toString();
        if (Tarin_bayani.상수종류[Indes] == 8) return Zare_alama(Tarin_bayani.문자((Integer)Tarin_bayani.Jurarre_Tarin_bayani[Indes]));
        throw new 번역오류("정수와 Zare_Daraja 상수만 taimako_Daraja");
    }
    String 엑스조립본(String Mashigar_bayanai_maki, List<String> 내보냄, String tageti) throws IOException {
        Map<String,String> na_ura_mai_kwakwalwa_tebur = new HashMap<>();
        for (String Layi : Files.readAllLines(albarkatu_Hanyar_shiga.resolve("엑스기계함수.tsv"))) { String[] jona_Daraja = Layi.split("\t"); if (jona_Daraja[0].equals(tageti)) na_ura_mai_kwakwalwa_tebur.put(jona_Daraja[1] + jona_Daraja[2],jona_Daraja[3]); }
        int 자리 = Mashigar_bayanai_maki.lastIndexOf('.'); if (자리 < 0) throw new 번역오류("Mashigar_bayanai_maki sanya_Daraja Kuskure");
        String mamallaki_Daraja = Mashigar_bayanai_maki.substring(0,자리).replace('.','/'), tsari_Mashigar_bayanai_Suna = Mashigar_bayanai_maki.substring(자리 + 1); tsari_Manazarta Mashigar_bayanai_maki_Daraja = null;
        for (String 서술 : Arrays.asList("()I","()V")) { tsari_Manazarta Manazarta = new tsari_Manazarta(mamallaki_Daraja,tsari_Mashigar_bayanai_Suna,서술); if (함수들.containsKey(Manazarta)) { if (Mashigar_bayanai_maki_Daraja != null) throw new 번역오류("겹친 Mashigar_bayanai_maki"); Mashigar_bayanai_maki_Daraja = Manazarta; } }
        if (Mashigar_bayanai_maki_Daraja == null || (함수들.get(Mashigar_bayanai_maki_Daraja).isa_Mashigar_bayanai & 0x100) != 0) throw new 번역오류("Mashigar_bayanai_maki_Daraja AIKI_Daraja zubi_Daraja Kuskure");
        List<String> Layi = new ArrayList<>(); Layi.add(".code32");
        for (Aji_Tarin_bayani Tarin_bayani : 클래스들.values()) {
            String Matsayi_Daraja = alama_ad6f1a96("state",Tarin_bayani.Suna), Farko = alama_ad6f1a96("init",Tarin_bayani.Suna);
            Collections.addAll(Layi,".bss",".balign 4",Matsayi_Daraja + ": .long 0",".text",Farko + ":","cmpl $0, " + Matsayi_Daraja,"jne " + Farko + "_done","movl $1, " + Matsayi_Daraja);
            tsari_Manazarta 초기화참조 = new tsari_Manazarta(Tarin_bayani.Suna,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Layi.add("call " + alama_ad6f1a96("method",초기화참조.부분들()));
            Collections.addAll(Layi,"movl $2, " + Matsayi_Daraja,Farko + "_done:","ret");
            for (Memba_Tarin_bayani Fili_Daraja : Tarin_bayani.Fili_Daraja) {
                byte[] Jurarre_Daraja = Fili_Daraja.siffofi_Daraja.get("ConstantValue"); String Daraja = Jurarre_Daraja == null ? "0" : Maɓallin_X_86_Jurarre(Tarin_bayani,new Tarin_bayani_Manazarci(Jurarre_Daraja).두바이트());
                Collections.addAll(Layi,".data",".balign 4",alama_ad6f1a96("field",Tarin_bayani.Suna,Fili_Daraja.Suna,Fili_Daraja.서술) + ": .long " + Daraja);
            }
            for (Memba_Tarin_bayani AIKI_Daraja : Tarin_bayani.AIKI_Daraja) if (!AIKI_Daraja.Suna.equals("<init>")) Layi.add(Maɓallin_X_86_tsari_jiki(new tsari_Manazarta(Tarin_bayani.Suna,AIKI_Daraja.Suna,AIKI_Daraja.서술),AIKI_Daraja,na_ura_mai_kwakwalwa_tebur,tageti));
        }
        Collections.addAll(Layi,".text",".globl java_entry","java_entry:","call " + alama_ad6f1a96("init",Mashigar_bayanai_maki_Daraja.mamallaki_Daraja),"call " + alama_ad6f1a96("method",Mashigar_bayanai_maki_Daraja.부분들()));
        if (Mashigar_bayanai_maki_Daraja.서술.equals("()V")) Layi.add("xorl %eax, %eax"); Layi.add("ret");
        for (String sanya_Daraja : 내보냄) {
            int Haruffan_rabawa_Daraja = sanya_Daraja.indexOf('='); if (Haruffan_rabawa_Daraja < 1) throw new 번역오류("내보내기 sanya_Daraja Kuskure");
            String 외부 = sanya_Daraja.substring(0,Haruffan_rabawa_Daraja), AIKI_Daraja = sanya_Daraja.substring(Haruffan_rabawa_Daraja + 1); int 나눔 = AIKI_Daraja.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 alama_ad6f1a96 Kuskure");
            String Aji_Daraja = AIKI_Daraja.substring(0,나눔).replace('.','/'), Suna = AIKI_Daraja.substring(나눔 + 1); tsari_Manazarta bangaren_zaɓi_Daraja = null;
            for (tsari_Manazarta Manazarta : 함수들.keySet()) if (Manazarta.mamallaki_Daraja.equals(Aji_Daraja) && Manazarta.Suna.equals(Suna)) { if (bangaren_zaɓi_Daraja != null) throw new 번역오류("겹친 내보내기 tageti"); bangaren_zaɓi_Daraja = Manazarta; }
            if (bangaren_zaɓi_Daraja == null) throw new 번역오류("내보낼 함수가 없음");
            Collections.addAll(Layi,".text",".globl " + 외부,외부 + ":","call " + alama_ad6f1a96("init",bangaren_zaɓi_Daraja.mamallaki_Daraja),"jmp " + alama_ad6f1a96("method",bangaren_zaɓi_Daraja.부분들()));
        }
        Layi.add(".section .rodata");
        for (Map.Entry<String,String> Mashigar_bayanai_Daraja : 문자열들.entrySet()) {
            Collections.addAll(Layi,".balign 4",Mashigar_bayanai_Daraja.getValue() + ":",".long " + Mashigar_bayanai_Daraja.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char darasi_Daraja : Mashigar_bayanai_Daraja.getKey().toCharArray()) 단위들.add(Integer.toString(darasi_Daraja)); if (!단위들.isEmpty()) Layi.add(".long " + String.join(",",단위들));
        }
        Layi.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Layi) + "\n";
    }
    static void gudanar_kayan_aiki(List<String> Umarni) throws Exception {
        if (new ProcessBuilder(Umarni).inheritIO().start().waitFor() != 0) throw new 번역오류("Gina_tushe Kuskure: " + Umarni.get(0));
    }
    static String Tarin_bayani_Zare(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String tageti, String Mashigar_bayanai_maki, List<String> 내보냄, Path 출력, Path albarkatu_Daraja) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Aji_Hanyar_shiga = 임시.resolve("classes"); Files.createDirectory(Aji_Hanyar_shiga);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Aji_Hanyar_shiga.toString(),"-sourcepath",Aji_Hanyar_shiga.toString(),"-d",Aji_Hanyar_shiga.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new 번역오류("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new 번역오류(".java 또는 .class만 taimako_Daraja");
            }
            if (원문수 > 0) gudanar_kayan_aiki(자바명령);
            try (java.util.stream.Stream<Path> Hanyar_shiga_Jeri = Files.walk(Aji_Hanyar_shiga)) { Hanyar_shiga_Jeri.filter(Hanyar_shiga -> Hanyar_shiga.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,tageti.equals("user") ? "user" : "kernel",262144,albarkatu_Daraja);
            String 조립 = 변환.엑스조립본(Mashigar_bayanai_maki,내보냄,tageti); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = albarkatu_Daraja.getParent();
            gudanar_kayan_aiki(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            gudanar_kayan_aiki(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("lokacin_bude_yaren_gama_gari_taimako.s").toString()));
            List<String> Haɗi = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (tageti.equals("kernel")) Haɗi.add("-r");
            else {
                gudanar_kayan_aiki(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(tageti.equals("user") ? "Fara_Mai_anfani_da_kwamfuta_Shiri.s" : "리눅스시작.s").toString()));
                Collections.addAll(Haɗi,"-e","_start",임시.resolve("start.o").toString());
                if (tageti.equals("user")) Collections.addAll(Haɗi,"-T",도구위치.resolve("Mai_anfani_da_kwamfuta_Kafa_Zagaye.ld").toString());
            }
            Collections.addAll(Haɗi,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); gudanar_kayan_aiki(Haɗi);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path wallafa_Daraja = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),wallafa_Daraja,StandardCopyOption.REPLACE_EXISTING); Files.move(wallafa_Daraja,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(wallafa_Daraja); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(tageti.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> alama_Tarin_bayani = new ArrayList<>(), Tarin_bayanan_soma_aiki = new ArrayList<>();
            for (tsari_Manazarta Manazarta : 변환.함수들.keySet()) alama_Tarin_bayani.add(Tarin_bayani_Zare(alama_ad6f1a96("method",Manazarta.부분들())) + ":" + Tarin_bayani_Zare(Manazarta.mamallaki_Daraja + "." + Manazarta.Suna + Manazarta.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_Fayil = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte Daraja : hash_Fayil) SMS.append(String.format(Locale.ROOT,"%02x",Daraja & 255));
                Tarin_bayanan_soma_aiki.add(Tarin_bayani_Zare(입력.toAbsolutePath().toString()) + ":" + Tarin_bayani_Zare(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + Tarin_bayani_Zare(tageti) + ",\"entry\":" + Tarin_bayani_Zare(Mashigar_bayanai_maki) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",alama_Tarin_bayani) + "},\"sources\":{" + String.join(",",Tarin_bayanan_soma_aiki) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> Hanyar_shiga_Jeri = Files.walk(임시)) { for (Path Hanyar_shiga : (Iterable<Path>)Hanyar_shiga_Jeri.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Hanyar_shiga); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String Mashigar_bayanai_maki = null, tageti = "kernel", Maɓallin_X_86_tageti = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> Hanyar_shiga_Jeri = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String Daraja = 인수[순번];
                switch (Daraja) {
                    case "--target": Maɓallin_X_86_tageti = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Aji_Daraja.AIKI_Daraja -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export alama_ad6f1a96=Aji_Daraja.AIKI_Daraja] 클래스파일 또는 Java원문"); return;
                    case "--entry": Mashigar_bayanai_maki = 인수[++순번]; break;
                    case "--profile": tageti = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (Daraja.startsWith("-")) throw new 번역오류("알 수 없는 옵션: " + Daraja); Hanyar_shiga_Jeri.add(Paths.get(Daraja));
                }
            }
            if (Mashigar_bayanai_maki == null || 출력경로 == null || Hanyar_shiga_Jeri.isEmpty()) throw new 번역오류("--entry, -o, Aji_Daraja 파일이 필요합니다");
            Path albarkatu_Daraja = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (Maɓallin_X_86_tageti != null) {
                if (!Arrays.asList("linux","kernel","user").contains(Maɓallin_X_86_tageti)) throw new 번역오류("알 수 없는 gudanar_Umarni tageti");
                엑스번역(Hanyar_shiga_Jeri,Maɓallin_X_86_tageti,Mashigar_bayanai_maki,내보냄,출력경로,albarkatu_Daraja); return;
            }
            String tushe = new 기계어미리번역(Hanyar_shiga_Jeri, tageti, 낱말수, albarkatu_Daraja).생성(Mashigar_bayanai_maki, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, tushe, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Kuskure) { System.err.println("Gina_tushe Kuskure: " + Kuskure.getMessage()); System.exit(1); }
    }
}
