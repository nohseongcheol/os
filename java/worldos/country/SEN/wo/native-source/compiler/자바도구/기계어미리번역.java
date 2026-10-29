// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java maas_xëyma 파일에서 독립 ARM64 커널용 C 원문을 만든다. dalal JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Tekki_njumte extends RuntimeException {
        Tekki_njumte(String 설명) { super(설명); }
    }
    static final class mbir_jangkat {
        final byte[] mbir;
        int 위치;
        mbir_jangkat(byte[] 입력자료) { mbir = 입력자료; }
        byte[] 읽기(int diir_xëyma) {
            if (diir_xëyma < 0 || diir_xëyma > mbir.length - 위치) throw new Tekki_njumte("잘린 maas_xëyma 또는 ndigel mbir");
            byte[] 결과 = Arrays.copyOfRange(mbir, 위치, 위치 + diir_xëyma); 위치 += diir_xëyma; return 결과;
        }
        int 한바이트() { if (위치 >= mbir.length) throw new Tekki_njumte("잘린 ndigel mbir"); return mbir[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class Way_bokk_mbir {
        final int jot_dugal_xabaar;
        final String tur_253d1510, 서술;
        final Map<String, byte[]> jagle_xëyma;
        Way_bokk_mbir(int jot_xëyma, String tur_xëyma, String 서술값, Map<String, byte[]> jagle_mbir) {
            jot_dugal_xabaar = jot_xëyma; tur_253d1510 = tur_xëyma; 서술 = 서술값; jagle_xëyma = jagle_mbir;
        }
    }
    static final class doxalin_Royukaay implements Comparable<doxalin_Royukaay> {
        final String boroom_xëyma, tur_253d1510, 서술;
        doxalin_Royukaay(String 소유값, String tur_xëyma, String 서술값) { boroom_xëyma = 소유값; tur_253d1510 = tur_xëyma; 서술 = 서술값; }
        String[] 부분들() { return new String[]{boroom_xëyma, tur_253d1510, 서술}; }
        public int compareTo(doxalin_Royukaay Nàttangoo_xëyma) {
            int 비교값 = boroom_xëyma.compareTo(Nàttangoo_xëyma.boroom_xëyma);
            if (비교값 == 0) 비교값 = tur_253d1510.compareTo(Nàttangoo_xëyma.tur_253d1510);
            return 비교값 == 0 ? 서술.compareTo(Nàttangoo_xëyma.서술) : 비교값;
        }
        public boolean equals(Object Nàttangoo_xëyma) { return Nàttangoo_xëyma instanceof doxalin_Royukaay && compareTo((doxalin_Royukaay) Nàttangoo_xëyma) == 0; }
        public int hashCode() { return Objects.hash(boroom_xëyma, tur_253d1510, 서술); }
    }
    static final class maas_mbir {
        final int[] 상수종류;
        final Object[] Lees_dul_soppi_mbir;
        final String tur_253d1510;
        final List<Way_bokk_mbir> barabu_denc_ab_joxe_xëyma, liëey_xëyma;
        maas_mbir(Path Yoonu_jëmale) throws IOException {
            mbir_jangkat jangkat_xëyma = new mbir_jangkat(Files.readAllBytes(Yoonu_jëmale));
            if (jangkat_xëyma.네바이트() != 0xcafebabe) throw new Tekki_njumte("Java maas_xëyma 표식이 아님");
            jangkat_xëyma.읽기(4);
            int 개수 = jangkat_xëyma.두바이트(); 상수종류 = new int[개수]; Lees_dul_soppi_mbir = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = jangkat_xëyma.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int diir_xëyma = jangkat_xëyma.두바이트();
                        byte[] Araf_dencandikaay = jangkat_xëyma.읽기(diir_xëyma), 길이붙인자료 = new byte[diir_xëyma + 2];
                        길이붙인자료[0] = (byte)(diir_xëyma >> 8); 길이붙인자료[1] = (byte)diir_xëyma;
                        System.arraycopy(Araf_dencandikaay, 0, 길이붙인자료, 2, diir_xëyma);
                        Lees_dul_soppi_mbir[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: Lees_dul_soppi_mbir[순번] = jangkat_xëyma.네바이트(); break;
                    case 4: jangkat_xëyma.읽기(4); break;
                    case 5: case 6: jangkat_xëyma.읽기(8); 순번++; break;
                    case 7: case 8: case 16: Lees_dul_soppi_mbir[순번] = jangkat_xëyma.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        Lees_dul_soppi_mbir[순번] = new int[]{jangkat_xëyma.두바이트(), jangkat_xëyma.두바이트()}; break;
                    case 15: Lees_dul_soppi_mbir[순번] = new int[]{jangkat_xëyma.한바이트(), jangkat_xëyma.두바이트()}; break;
                    default: throw new Tekki_njumte("지원하지 않는 Lees_dul_soppi_xëyma 종류: " + 종류);
                }
            }
            jangkat_xëyma.두바이트(); tur_253d1510 = maas_tur(jangkat_xëyma.두바이트());
            if (!maas_tur(jangkat_xëyma.두바이트()).equals("java/lang/Object") || jangkat_xëyma.두바이트() != 0)
                throw new Tekki_njumte(tur_253d1510 + ": 상속 및 인터페이스 미지원");
            barabu_denc_ab_joxe_xëyma = 멤버읽기(jangkat_xëyma); liëey_xëyma = 멤버읽기(jangkat_xëyma); 속성읽기(jangkat_xëyma);
            if (jangkat_xëyma.위치 != jangkat_xëyma.mbir.length) throw new Tekki_njumte("maas_xëyma 뒤에 남은 mbir");
        }
        String 문자(int àlluwa_tur) {
            if (àlluwa_tur < 1 || àlluwa_tur >= 상수종류.length || 상수종류[àlluwa_tur] != 1) throw new Tekki_njumte("문자 Lees_dul_soppi_xëyma àlluwa_tur njumte");
            return (String) Lees_dul_soppi_mbir[àlluwa_tur];
        }
        String maas_tur(int àlluwa_tur) {
            if (àlluwa_tur < 1 || àlluwa_tur >= 상수종류.length || 상수종류[àlluwa_tur] != 7) throw new Tekki_njumte("maas_xëyma Royukaay njumte");
            return 문자((Integer)Lees_dul_soppi_mbir[àlluwa_tur]);
        }
        doxalin_Royukaay Royukaay(int àlluwa_tur) {
            if (àlluwa_tur < 1 || àlluwa_tur >= 상수종류.length || 상수종류[àlluwa_tur] < 9 || 상수종류[àlluwa_tur] > 11) throw new Tekki_njumte("멤버 Royukaay njumte");
            int[] ñaar_ñaar_xëyma = (int[])Lees_dul_soppi_mbir[àlluwa_tur], tur_ñaar_ñaar = (int[])Lees_dul_soppi_mbir[ñaar_ñaar_xëyma[1]];
            return new doxalin_Royukaay(maas_tur(ñaar_ñaar_xëyma[0]), 문자(tur_ñaar_ñaar[0]), 문자(tur_ñaar_ñaar[1]));
        }
        Map<String, byte[]> 속성읽기(mbir_jangkat jangkat_xëyma) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = jangkat_xëyma.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String jagle_tur = 문자(jangkat_xëyma.두바이트()); byte[] xëyma = jangkat_xëyma.읽기(jangkat_xëyma.네바이트());
                if (결과.put(jagle_tur, xëyma) != null) throw new Tekki_njumte("겹친 jagle_xëyma: " + jagle_tur);
            }
            return 결과;
        }
        List<Way_bokk_mbir> 멤버읽기(mbir_jangkat jangkat_xëyma) {
            List<Way_bokk_mbir> 결과 = new ArrayList<>(); int 개수 = jangkat_xëyma.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int jot_dugal_xabaar = jangkat_xëyma.두바이트(); String doxalin_dugal_xabaar_tur = 문자(jangkat_xëyma.두바이트()), 서술 = 문자(jangkat_xëyma.두바이트());
                결과.add(new Way_bokk_mbir(jot_dugal_xabaar, doxalin_dugal_xabaar_tur, 서술, 속성읽기(jangkat_xëyma)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Tekki_njumte("liëey_xëyma 서술 njumte: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Tekki_njumte("liëey_xëyma 서술 njumte: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Tekki_njumte("liëey_xëyma 서술 njumte: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String tanneef_xëyma = null;
            for (String dayo_xëyma : 허용형식) if (서술.startsWith(dayo_xëyma, 위치)) { tanneef_xëyma = dayo_xëyma; break; }
            if (tanneef_xëyma == null) throw new Tekki_njumte("지원하지 않는 xéeti_mbir: " + 서술);
            결과.add(tanneef_xëyma); 위치 += tanneef_xëyma.length();
        }
        return 결과;
    }
    static String sembóol(String 종류, String... 부분들) {
        try {
            byte[] caabiy_teqale_bi_bara_denc = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Tekst = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Tekst.append(String.format(Locale.ROOT, "%02x", caabiy_teqale_bi_bara_denc[순번] & 255));
            return Tekst.toString();
        } catch (Exception njumte) { throw new Tekki_njumte(njumte.toString()); }
    }
    final Map<String, maas_mbir> 클래스들 = new TreeMap<>();
    final Map<doxalin_Royukaay, Way_bokk_mbir> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, masin_maas;
    final int 동적기억낱말수;
    final Path Kàttan_Yoonu_jëmale;
    기계어미리번역(List<Path> Yoonu_jëmale_lim, String luñu_name, int 낱말수, Path Kàttan_xëyma) throws IOException {
        if ((!luñu_name.equals("kernel") && !luñu_name.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Tekki_njumte("def_ndigel luñu_name 또는 fatlekookaay_xëyma 공간 tolluwaay njumte");
        실행대상 = luñu_name; 동적기억낱말수 = 낱말수; Kàttan_Yoonu_jëmale = Kàttan_xëyma;
        // 이 이름도 국가별 Cosaan_tëralinuy_pàcc 생성 시 해당 언어로 옮긴다.
        masin_maas = luñu_name.equals("kernel") ? "보드" : "kiy_jariñoo_internet";
        for (String buum : Files.readAllLines(Kàttan_xëyma.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = buum.split("\t", -1);
            if (부분들.length != 4) throw new Tekki_njumte("masin liëey_xëyma mbir njumte");
            if (부분들[0].equals(luñu_name)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Yoonu_jëmale : Yoonu_jëmale_lim) {
            maas_mbir mbir = new maas_mbir(Yoonu_jëmale);
            if (클래스들.put(mbir.tur_253d1510, mbir) != null) throw new Tekki_njumte("중복 maas_xëyma: " + mbir.tur_253d1510);
            for (Way_bokk_mbir barabu_denc_ab_joxe_xëyma : mbir.barabu_denc_ab_joxe_xëyma) {
                if ((barabu_denc_ab_joxe_xëyma.jot_dugal_xabaar & 8) == 0 || 형식읽기(barabu_denc_ab_joxe_xëyma.서술).equals(Collections.singletonList("V"))) throw new Tekki_njumte("Soppeekoodi_xëyma 필드만 Ndimbal_xëyma");
                if (필드들.put(new doxalin_Royukaay(mbir.tur_253d1510, barabu_denc_ab_joxe_xëyma.tur_253d1510, barabu_denc_ab_joxe_xëyma.서술), barabu_denc_ab_joxe_xëyma) != null) throw new Tekki_njumte("중복 barabu_denc_ab_joxe_xëyma");
            }
            for (Way_bokk_mbir liëey_xëyma : mbir.liëey_xëyma) {
                if (liëey_xëyma.tur_253d1510.equals("<init>")) continue;
                if ((liëey_xëyma.jot_dugal_xabaar & 8) == 0 || (liëey_xëyma.jot_dugal_xabaar & (0x20 | 0x400)) != 0) throw new Tekki_njumte("Soppeekoodi_xëyma 비동기화 함수만 Ndimbal_xëyma");
                new 함수형식(liëey_xëyma.서술);
                if (함수들.put(new doxalin_Royukaay(mbir.tur_253d1510, liëey_xëyma.tur_253d1510, liëey_xëyma.서술), liëey_xëyma) != null) throw new Tekki_njumte("중복 liëey_xëyma");
            }
        }
    }
    String araf_yu_bennoo_sembóol(String Tekst) { return 문자열들.computeIfAbsent(Tekst, xëyma -> "j_text_" + 문자열들.size()); }
    String Lees_dul_soppi_guddalinu_méngale(maas_mbir mbir, int àlluwa_tur) {
        if (àlluwa_tur < 1 || àlluwa_tur >= mbir.상수종류.length) throw new Tekki_njumte("Lees_dul_soppi_xëyma àlluwa_tur kilip njumte");
        if (mbir.상수종류[àlluwa_tur] == 3) return "(word)(uint32_t)(" + mbir.Lees_dul_soppi_mbir[àlluwa_tur] + ")";
        if (mbir.상수종류[àlluwa_tur] == 8) return "(word)" + araf_yu_bennoo_sembóol(mbir.문자((Integer)mbir.Lees_dul_soppi_mbir[àlluwa_tur]));
        throw new Tekki_njumte("정수와 araf_yu_bennoo_xëyma 상수만 Ndimbal_xëyma");
    }
    String 함수원형(doxalin_Royukaay Royukaay) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Royukaay.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + sembóol("method", Royukaay.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void sek_dënnd(int àlluwa_tur, int 지역변수수) { if (àlluwa_tur < 0 || àlluwa_tur >= 지역변수수) throw new Tekki_njumte("dënnd_nameef 변수 àlluwa_tur kilip njumte"); }
    void 분기넣기(List<String> 출력, Set<Integer> car_lim, int 위치, int 이동량, String anam) {
        int jëmmukaay_xëyma = 위치 + 이동량; car_lim.add(jëmmukaay_xëyma);
        출력.add((anam == null ? "" : "if (" + anam + ") ") + "goto b" + jëmmukaay_xëyma + ";");
    }
    String 함수본문(doxalin_Royukaay liëey_xëyma, Way_bokk_mbir mbir) {
        byte[] 본문자료 = mbir.jagle_xëyma.get("Code"); if (본문자료 == null) throw new Tekki_njumte("liëey_xëyma 몸체가 없음: " + liëey_xëyma.tur_253d1510);
        mbir_jangkat jangkat_xëyma = new mbir_jangkat(본문자료); int 쌓임깊이 = jangkat_xëyma.두바이트(), 지역변수수 = jangkat_xëyma.두바이트();
        mbir_jangkat ndigel_mbir = new mbir_jangkat(jangkat_xëyma.읽기(jangkat_xëyma.네바이트()));
        if (jangkat_xëyma.두바이트() != 0) throw new Tekki_njumte("try/catch/finally 미지원");
        함수형식 dayo_xëyma = new 함수형식(liëey_xëyma.서술); if (지역변수수 < dayo_xëyma.인수.size()) throw new Tekki_njumte("매개변수보다 적은 dënnd_nameef 변수");
        maas_mbir maas_xëyma = 클래스들.get(liëey_xëyma.boroom_xëyma);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(liëey_xëyma) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < dayo_xëyma.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), car_lim = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (ndigel_mbir.위치 < ndigel_mbir.mbir.length) {
            int 위치 = ndigel_mbir.위치, ndigel = ndigel_mbir.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (ndigel == 0) continue;
            if (ndigel == 1) 출력.add("PUSH(0);");
            else if (ndigel >= 2 && ndigel <= 8) 출력.add("PUSH((uint32_t)(" + (ndigel - 3) + "));");
            else if (ndigel == 16 || ndigel == 17) 출력.add("PUSH((uint32_t)(" + (ndigel == 16 ? ndigel_mbir.부호한바이트() : ndigel_mbir.부호두바이트()) + "));");
            else if (ndigel == 18 || ndigel == 19) 출력.add("PUSH(" + Lees_dul_soppi_guddalinu_méngale(maas_xëyma, ndigel == 18 ? ndigel_mbir.한바이트() : ndigel_mbir.두바이트()) + ");");
            else if (ndigel == 21 || ndigel == 25 || (ndigel >= 26 && ndigel <= 29) || (ndigel >= 42 && ndigel <= 45)) {
                int àlluwa_tur = ndigel == 21 || ndigel == 25 ? ndigel_mbir.한바이트() : ndigel - (ndigel <= 29 ? 26 : 42);
                sek_dënnd(àlluwa_tur, 지역변수수); 출력.add("PUSH(l[" + àlluwa_tur + "]);");
            } else if (ndigel == 54 || ndigel == 58 || (ndigel >= 59 && ndigel <= 62) || (ndigel >= 75 && ndigel <= 78)) {
                int àlluwa_tur = ndigel == 54 || ndigel == 58 ? ndigel_mbir.한바이트() : ndigel - (ndigel <= 62 ? 59 : 75);
                sek_dënnd(àlluwa_tur, 지역변수수); 출력.add("l[" + àlluwa_tur + "] = POP();");
            } else if (ndigel == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (ndigel == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (ndigel == 87 || ndigel == 88) 출력.add(ndigel == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (ndigel >= 89 && ndigel <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] toftale_lim = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[ndigel - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char xëyma : toftale_lim[ndigel - 89].toCharArray()) 출력.add("PUSH(" + xëyma + ");");
            } else if (ndigel == 96 || ndigel == 100 || ndigel == 104 || ndigel == 126 || ndigel == 128 || ndigel == 130) {
                String sëfu_xayma_xëyma = ndigel == 96 ? "+" : ndigel == 100 ? "-" : ndigel == 104 ? "*" : ndigel == 126 ? "&" : ndigel == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + sëfu_xayma_xëyma + " (uint32_t)b);");
            } else if (ndigel == 108 || ndigel == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (ndigel == 112 ? 1 : 0) + "));");
            else if (ndigel == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (ndigel == 120 || ndigel == 122 || ndigel == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (ndigel == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (ndigel == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (ndigel == 132) {
                int àlluwa_tur = ndigel_mbir.한바이트(), 증가량 = ndigel_mbir.부호한바이트(); sek_dënnd(àlluwa_tur, 지역변수수);
                출력.add("l[" + àlluwa_tur + "] = (uint32_t)l[" + àlluwa_tur + "] + (uint32_t)(" + 증가량 + ");");
            } else if (ndigel >= 145 && ndigel <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (ndigel == 145 ? "int8_t" : ndigel == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (ndigel >= 153 && ndigel <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, car_lim, 위치, ndigel_mbir.부호두바이트(), "(int32_t)a " + 비교들[ndigel - 153] + " 0");
            } else if (ndigel >= 159 && ndigel <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, car_lim, 위치, ndigel_mbir.부호두바이트(), ndigel >= 165 ? "a " + 비교들[ndigel - 159] + " b" : "(int32_t)a " + 비교들[ndigel - 159] + " (int32_t)b");
            } else if (ndigel == 167 || ndigel == 200) 분기넣기(출력, car_lim, 위치, ndigel == 167 ? ndigel_mbir.부호두바이트() : ndigel_mbir.네바이트(), null);
            else if (ndigel == 170 || ndigel == 171) {
                while (ndigel_mbir.위치 % 4 != 0) ndigel_mbir.한바이트();
                int xayma_bi_teew = ndigel_mbir.네바이트(); 출력.add("a = POP();");
                if (ndigel == 170) {
                    int 아래 = ndigel_mbir.네바이트(), 위 = ndigel_mbir.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (ndigel_mbir.mbir.length - ndigel_mbir.위치) / 4) throw new Tekki_njumte("switch kilip njumte");
                    for (long xëyma = 아래; xëyma <= 위; xëyma++) 분기넣기(출력, car_lim, 위치, ndigel_mbir.네바이트(), "(int32_t)a == (" + xëyma + ")");
                } else {
                    int 개수 = ndigel_mbir.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (ndigel_mbir.mbir.length - ndigel_mbir.위치) / 8) throw new Tekki_njumte("switch tolluwaay njumte");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int xëyma = ndigel_mbir.네바이트(); if (순번 > 0 && xëyma <= 앞값) throw new Tekki_njumte("switch toftale_xëyma njumte"); 앞값 = xëyma;
                        분기넣기(출력, car_lim, 위치, ndigel_mbir.네바이트(), "(int32_t)a == (" + xëyma + ")");
                    }
                }
                분기넣기(출력, car_lim, 위치, xayma_bi_teew, null);
            } else if (ndigel == 172 || ndigel == 176 || ndigel == 177) 출력.add("return " + (ndigel == 177 ? "0" : "POP()") + ";");
            else if (ndigel == 178 || ndigel == 179) {
                doxalin_Royukaay Royukaay = maas_xëyma.Royukaay(ndigel_mbir.두바이트()); if (!필드들.containsKey(Royukaay)) throw new Tekki_njumte("알 수 없는 barabu_denc_ab_joxe_xëyma");
                출력.add(sembóol("init", Royukaay.boroom_xëyma) + "();"); String barabu_denc_ab_joxe_xëyma = sembóol("field", Royukaay.부분들());
                출력.add(ndigel == 178 ? "PUSH(" + barabu_denc_ab_joxe_xëyma + ");" : barabu_denc_ab_joxe_xëyma + " = POP();");
            } else if (ndigel == 184) {
                doxalin_Royukaay Royukaay = maas_xëyma.Royukaay(ndigel_mbir.두바이트()); if (!함수들.containsKey(Royukaay)) throw new Tekki_njumte("알 수 없는 liëey_xëyma");
                함수형식 호출형식 = new 함수형식(Royukaay.서술); int 개수 = 호출형식.인수.size();
                출력.add(sembóol("init", Royukaay.boroom_xëyma) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + sembóol("method", Royukaay.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (ndigel == 182) {
                doxalin_Royukaay Royukaay = maas_xëyma.Royukaay(ndigel_mbir.두바이트());
                if (Royukaay.equals(new doxalin_Royukaay("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Royukaay.equals(new doxalin_Royukaay("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Tekki_njumte("가상 liëey_xëyma 호출 미지원");
            } else if (ndigel == 188) {
                if (ndigel_mbir.한바이트() != 10) throw new Tekki_njumte("new int[]만 Ndimbal_xëyma"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (ndigel == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (ndigel == 196) {
                int ñàmbaas_xëyma = ndigel_mbir.한바이트(), àlluwa_tur = ndigel_mbir.두바이트(); sek_dënnd(àlluwa_tur, 지역변수수);
                if (ñàmbaas_xëyma == 21 || ñàmbaas_xëyma == 25) 출력.add("PUSH(l[" + àlluwa_tur + "]);");
                else if (ñàmbaas_xëyma == 54 || ñàmbaas_xëyma == 58) 출력.add("l[" + àlluwa_tur + "] = POP();");
                else if (ñàmbaas_xëyma == 132) 출력.add("l[" + àlluwa_tur + "] = (uint32_t)l[" + àlluwa_tur + "] + (uint32_t)(" + ndigel_mbir.부호두바이트() + ");");
                else throw new Tekki_njumte("미지원 wide ndigel");
            } else if (ndigel == 198 || ndigel == 199) {
                출력.add("a = POP();"); 분기넣기(출력, car_lim, 위치, ndigel_mbir.부호두바이트(), "a " + (ndigel == 198 ? "==" : "!=") + " 0");
            } else throw new Tekki_njumte(liëey_xëyma.boroom_xëyma + "." + liëey_xëyma.tur_253d1510 + ", okte_xëyma " + 위치 + ": 미지원 ndigel " + ndigel);
        }
        if (!경계들.containsAll(car_lim)) throw new Tekki_njumte("ndigel 경계가 아닌 곳으로 car");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String toxal_doxalin(String lëkkale_sembóol, String luñu_name, boolean 진입점여부) {
        int 자리 = luñu_name.lastIndexOf('.'); if (자리 < 0 || !lëkkale_sembóol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tekki_njumte("내보내기 지정 njumte");
        String boroom_xëyma = luñu_name.substring(0, 자리).replace('.', '/'), tur_253d1510 = luñu_name.substring(자리 + 1); doxalin_Royukaay tanneef_xëyma = null;
        for (doxalin_Royukaay Royukaay : 함수들.keySet()) if (Royukaay.boroom_xëyma.equals(boroom_xëyma) && Royukaay.tur_253d1510.equals(tur_253d1510)) {
            if (tanneef_xëyma != null) throw new Tekki_njumte("겹친 내보내기 luñu_name"); tanneef_xëyma = Royukaay;
        }
        if (tanneef_xëyma == null || (함수들.get(tanneef_xëyma).jot_dugal_xabaar & 0x100) != 0) throw new Tekki_njumte("내보낼 함수가 없음 또는 native liëey_xëyma");
        함수형식 dayo_xëyma = new 함수형식(tanneef_xëyma.서술);
        if ((진입점여부 && !dayo_xëyma.인수.isEmpty()) || !Arrays.asList("V", "I").contains(dayo_xëyma.반환)) throw new Tekki_njumte("dugal_xabaar_Tomb_xëyma 또는 C 경계 dayo_xëyma njumte");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < dayo_xëyma.인수.size(); 순번++) {
            if (!dayo_xëyma.인수.get(순번).equals("I")) throw new Tekki_njumte("C 경계는 int 인수만 Ndimbal_xëyma");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (dayo_xëyma.반환.equals("V") ? "void " : "int32_t ") + lëkkale_sembóol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + sembóol("init", tanneef_xëyma.boroom_xëyma) + "(); " + (dayo_xëyma.반환.equals("V") ? "" : "return (int32_t)") + sembóol("method", tanneef_xëyma.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String dugal_xabaar_Tomb, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<doxalin_Royukaay, Way_bokk_mbir> dugal_xabaar_xëyma : 함수들.entrySet()) {
            doxalin_Royukaay Royukaay = dugal_xabaar_xëyma.getKey(); Way_bokk_mbir mbir = dugal_xabaar_xëyma.getValue(); 선언들.add(함수원형(Royukaay) + ";");
            if ((mbir.jot_dugal_xabaar & 0x100) != 0) {
                String JOKKOO = 기계함수들.get(Royukaay.tur_253d1510 + Royukaay.서술);
                if (!Royukaay.boroom_xëyma.equals(masin_maas) || JOKKOO == null) throw new Tekki_njumte("허용되지 않은 native liëey_xëyma: " + Royukaay.tur_253d1510);
                int 개수 = new 함수형식(Royukaay.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + JOKKOO + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Royukaay) + " { return " + JOKKOO + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Royukaay, mbir));
        }
        for (Map.Entry<doxalin_Royukaay, Way_bokk_mbir> dugal_xabaar_xëyma : 필드들.entrySet()) {
            doxalin_Royukaay Royukaay = dugal_xabaar_xëyma.getKey(); byte[] Lees_dul_soppi_xëyma = dugal_xabaar_xëyma.getValue().jagle_xëyma.get("ConstantValue");
            String xëyma = Lees_dul_soppi_xëyma == null ? "0" : Lees_dul_soppi_guddalinu_méngale(클래스들.get(Royukaay.boroom_xëyma), new mbir_jangkat(Lees_dul_soppi_xëyma).두바이트());
            필드선언들.add("static word " + sembóol("field", Royukaay.부분들()) + " = " + xëyma + ";");
        }
        for (String tur_253d1510 : 클래스들.keySet()) {
            String doortal = sembóol("init", tur_253d1510), nekkin_xëyma = sembóol("state", tur_253d1510);
            선언들.add("static void " + doortal + "(void);"); 필드선언들.add("static unsigned " + nekkin_xëyma + ";");
            doxalin_Royukaay Royukaay = new doxalin_Royukaay(tur_253d1510, "<clinit>", "()V");
            몸체들.add("static void " + doortal + "(void) { if(" + nekkin_xëyma + ") return; " + nekkin_xëyma + " = 1; " + (함수들.containsKey(Royukaay) ? sembóol("method", Royukaay.부분들()) + "(); " : "") + nekkin_xëyma + " = 2; }");
        }
        몸체들.add(toxal_doxalin("java_entry", dugal_xabaar_Tomb, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new Tekki_njumte("내보내기 지정 njumte");
            String tur_253d1510 = 지정.substring(0, 자리); 공개이름.add(tur_253d1510); 몸체들.add(toxal_doxalin(tur_253d1510, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> dugal_xabaar_xëyma : 문자열들.entrySet()) {
            String Tekst = dugal_xabaar_xëyma.getKey(); StringBuilder TABLO_xëyma = new StringBuilder("static const word " + dugal_xabaar_xëyma.getValue() + "[] = {" + Tekst.length());
            for (int 순번 = 0; 순번 < Tekst.length(); 순번++) TABLO_xëyma.append(", ").append((int)Tekst.charAt(순번));
            문자열선언들.add(TABLO_xëyma.append("};").toString());
        }
        String Ndimbal_xëyma = Files.readString(Kàttan_Yoonu_jëmale.resolve("common_language_runtime_Ndimbal.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Ndimbal_xëyma + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String Cosaan, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> tur_àlluwa = new HashMap<>();
        for (String buum : Files.readAllLines(Kàttan_Yoonu_jëmale.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] ñaar_ñaar_xëyma = buum.split("\t"); tur_àlluwa.put(ñaar_ñaar_xëyma[0], ñaar_ñaar_xëyma[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(Cosaan); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String tur_253d1510 = 찾개.group(), 새이름 = tur_253d1510;
            if (!tur_253d1510.startsWith("//") && !tur_253d1510.startsWith("/*") && !tur_253d1510.startsWith("\"") && !tur_253d1510.startsWith("'") && !공개이름.contains(tur_253d1510)) {
                새이름 = tur_àlluwa.getOrDefault(tur_253d1510, tur_253d1510);
                if (tur_253d1510.matches("a[0-9]+")) 새이름 = "인수" + tur_253d1510.substring(1);
                if (tur_253d1510.matches("b[0-9]+")) 새이름 = "car" + tur_253d1510.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char Araf_xëyma : 새이름.toCharArray()) 표기.append(Araf_xëyma < 128 ? Character.toString(Araf_xëyma) : String.format(Locale.ROOT, "\\u%04x", (int)Araf_xëyma));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(doxalin_Royukaay liëey_xëyma, Way_bokk_mbir mbir, Map<String,String> masin_àlluwa, String luñu_name) {
        String 표식 = sembóol("method", liëey_xëyma.부분들());
        List<String> buum = new ArrayList<>();
        if ((mbir.jot_dugal_xabaar & 0x100) != 0) {
            String JOKKOO = masin_àlluwa.get(liëey_xëyma.tur_253d1510 + liëey_xëyma.서술);
            if (!liëey_xëyma.boroom_xëyma.equals(luñu_name.equals("kernel") ? "toftal_xëyma" : "kiy_jariñoo_internet") || JOKKOO == null) throw new Tekki_njumte("허용되지 않은 native liëey_xëyma");
            return ".text\n" + 표식 + ":\njmp " + JOKKOO;
        }
        byte[] yaxub_mool = mbir.jagle_xëyma.get("Code"); if (yaxub_mool == null) throw new Tekki_njumte("liëey_xëyma 몸체가 없음");
        mbir_jangkat jangkat_xëyma = new mbir_jangkat(yaxub_mool); jangkat_xëyma.두바이트(); int 지역수 = jangkat_xëyma.두바이트();
        mbir_jangkat ndigel_mbir = new mbir_jangkat(jangkat_xëyma.읽기(jangkat_xëyma.네바이트()));
        if (jangkat_xëyma.두바이트() != 0) throw new Tekki_njumte("try/catch/finally 미지원");
        함수형식 dayo_xëyma = new 함수형식(liëey_xëyma.서술); if (지역수 < dayo_xëyma.인수.size()) throw new Tekki_njumte("매개변수보다 적은 dënnd_nameef 변수");
        Collections.addAll(buum,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < dayo_xëyma.인수.size(); 순번++) Collections.addAll(buum,"movl " + (8 + 4 * (dayo_xëyma.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        maas_mbir maas_xëyma = 클래스들.get(liëey_xëyma.boroom_xëyma); Set<Integer> 경계들 = new HashSet<>(), car_lim = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (ndigel_mbir.위치 < ndigel_mbir.mbir.length) {
            int 위치 = ndigel_mbir.위치, ndigel = ndigel_mbir.한바이트(); String 자리 = 표식 + "_b" + 위치;
            buum.add(자리 + ":"); 경계들.add(위치);
            if (ndigel == 0) buum.add("nop");
            else if (ndigel == 1) buum.add("pushl $0");
            else if (ndigel >= 2 && ndigel <= 8) buum.add("pushl $" + (ndigel - 3));
            else if (ndigel == 16 || ndigel == 17) buum.add("pushl $" + (ndigel == 16 ? ndigel_mbir.부호한바이트() : ndigel_mbir.부호두바이트()));
            else if (ndigel == 18 || ndigel == 19) {
                int àlluwa_tur = ndigel == 18 ? ndigel_mbir.한바이트() : ndigel_mbir.두바이트();
                buum.add("pushl $" + 엑스상수(maas_xëyma,àlluwa_tur));
            } else if (ndigel == 21 || ndigel == 25 || (ndigel >= 26 && ndigel <= 29) || (ndigel >= 42 && ndigel <= 45) || ndigel == 54 || ndigel == 58 || (ndigel >= 59 && ndigel <= 62) || (ndigel >= 75 && ndigel <= 78)) {
                boolean 읽음 = ndigel < 54; int àlluwa_tur = ndigel == 21 || ndigel == 25 || ndigel == 54 || ndigel == 58 ? ndigel_mbir.한바이트() : ndigel - (ndigel <= 29 ? 26 : ndigel <= 45 ? 42 : ndigel <= 62 ? 59 : 75);
                sek_dënnd(àlluwa_tur,지역수); buum.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (àlluwa_tur + 1)) + "(%ebp)");
            } else if (ndigel == 46) Collections.addAll(buum,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (ndigel == 79) Collections.addAll(buum,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (ndigel == 87 || ndigel == 88) buum.add("addl $" + (ndigel == 87 ? 4 : 8) + ", %esp");
            else if (ndigel >= 89 && ndigel <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] toftale_lim = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[ndigel - 89]; 순번++) buum.add("popl " + 저장기들[순번]);
                for (int 순번 : toftale_lim[ndigel - 89]) buum.add("pushl " + 저장기들[순번]);
            } else if (ndigel == 96 || ndigel == 100 || ndigel == 104 || ndigel == 126 || ndigel == 128 || ndigel == 130) {
                String sëfu_xayma_xëyma = ndigel == 96 ? "addl" : ndigel == 100 ? "subl" : ndigel == 104 ? "imull" : ndigel == 126 ? "andl" : ndigel == 128 ? "orl" : "xorl";
                Collections.addAll(buum,"popl %ecx","popl %eax",sëfu_xayma_xëyma + " %ecx, %eax","pushl %eax");
            } else if (ndigel == 108 || ndigel == 112) Collections.addAll(buum,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (ndigel == 108 ? "%eax" : "%edx"));
            else if (ndigel == 116) buum.add("negl (%esp)");
            else if (ndigel == 120 || ndigel == 122 || ndigel == 124) Collections.addAll(buum,"popl %ecx","popl %eax",(ndigel == 120 ? "sall" : ndigel == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (ndigel == 132) {
                int àlluwa_tur = ndigel_mbir.한바이트(), 증가 = ndigel_mbir.부호한바이트(); sek_dënnd(àlluwa_tur,지역수); buum.add("addl $" + 증가 + ", -" + (4 * (àlluwa_tur + 1)) + "(%ebp)");
            } else if (ndigel >= 145 && ndigel <= 147) Collections.addAll(buum,"popl %eax",ndigel == 145 ? "movsbl %al, %eax" : ndigel == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (ndigel >= 153 && ndigel <= 166) {
                if (ndigel <= 158) Collections.addAll(buum,"popl %eax","testl %eax, %eax");
                else Collections.addAll(buum,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int jëmmukaay_xëyma = 위치 + ndigel_mbir.부호두바이트(); car_lim.add(jëmmukaay_xëyma); buum.add(비교들[ndigel - (ndigel <= 158 ? 153 : 159)] + " " + 표식 + "_b" + jëmmukaay_xëyma);
            } else if (ndigel == 167 || ndigel == 200) {
                int jëmmukaay_xëyma = 위치 + (ndigel == 167 ? ndigel_mbir.부호두바이트() : ndigel_mbir.네바이트()); car_lim.add(jëmmukaay_xëyma); buum.add("jmp " + 표식 + "_b" + jëmmukaay_xëyma);
            } else if (ndigel == 170 || ndigel == 171) {
                while (ndigel_mbir.위치 % 4 != 0) ndigel_mbir.한바이트();
                int xayma_bi_teew = 위치 + ndigel_mbir.네바이트(); car_lim.add(xayma_bi_teew); buum.add("popl %eax");
                int 개수, 아래 = 0;
                if (ndigel == 170) { 아래 = ndigel_mbir.네바이트(); int 위 = ndigel_mbir.네바이트(); long diir_xëyma = (long)위 - 아래 + 1; if (diir_xëyma < 1 || diir_xëyma > (ndigel_mbir.mbir.length - ndigel_mbir.위치) / 4) throw new Tekki_njumte("switch kilip njumte"); 개수 = (int)diir_xëyma; }
                else { 개수 = ndigel_mbir.네바이트(); if (개수 < 0 || 개수 > (ndigel_mbir.mbir.length - ndigel_mbir.위치) / 8) throw new Tekki_njumte("switch tolluwaay njumte"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int xëyma = ndigel == 170 ? 아래 + 순번 : ndigel_mbir.네바이트(), jëmmukaay_xëyma = 위치 + ndigel_mbir.네바이트(); car_lim.add(jëmmukaay_xëyma);
                    Collections.addAll(buum,"cmpl $" + xëyma + ", %eax","je " + 표식 + "_b" + jëmmukaay_xëyma);
                }
                buum.add("jmp " + 표식 + "_b" + xayma_bi_teew);
            } else if (ndigel == 172 || ndigel == 176 || ndigel == 177) {
                if (ndigel != 177) buum.add("popl %eax"); Collections.addAll(buum,"leave","ret");
            } else if (ndigel == 178 || ndigel == 179) {
                doxalin_Royukaay Royukaay = maas_xëyma.Royukaay(ndigel_mbir.두바이트()); if (!필드들.containsKey(Royukaay)) throw new Tekki_njumte("알 수 없는 barabu_denc_ab_joxe_xëyma");
                Collections.addAll(buum,"call " + sembóol("init",Royukaay.boroom_xëyma),(ndigel == 178 ? "pushl " : "popl ") + sembóol("field",Royukaay.부분들()));
            } else if (ndigel == 184) {
                doxalin_Royukaay Royukaay = maas_xëyma.Royukaay(ndigel_mbir.두바이트()); if (!함수들.containsKey(Royukaay)) throw new Tekki_njumte("알 수 없는 liëey_xëyma");
                함수형식 호출형식 = new 함수형식(Royukaay.서술); Collections.addAll(buum,"call " + sembóol("init",Royukaay.boroom_xëyma),"call " + sembóol("method",Royukaay.부분들()));
                if (!호출형식.인수.isEmpty()) buum.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) buum.add("pushl %eax");
            } else if (ndigel == 182) {
                doxalin_Royukaay Royukaay = maas_xëyma.Royukaay(ndigel_mbir.두바이트());
                if (Royukaay.equals(new doxalin_Royukaay("java/lang/String","length","()I"))) Collections.addAll(buum,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Royukaay.equals(new doxalin_Royukaay("java/lang/String","charAt","(I)C"))) Collections.addAll(buum,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Tekki_njumte("가상 liëey_xëyma 호출 미지원");
            } else if (ndigel == 188) {
                if (ndigel_mbir.한바이트() != 10) throw new Tekki_njumte("new int[]만 Ndimbal_xëyma"); Collections.addAll(buum,"popl %eax","call rt_new_array","pushl %eax");
            } else if (ndigel == 190) Collections.addAll(buum,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (ndigel == 196) {
                int ñàmbaas_xëyma = ndigel_mbir.한바이트(), àlluwa_tur = ndigel_mbir.두바이트(); sek_dënnd(àlluwa_tur,지역수);
                if (ñàmbaas_xëyma == 21 || ñàmbaas_xëyma == 25 || ñàmbaas_xëyma == 54 || ñàmbaas_xëyma == 58) buum.add((ñàmbaas_xëyma <= 25 ? "pushl " : "popl ") + "-" + 4 * (àlluwa_tur + 1) + "(%ebp)");
                else if (ñàmbaas_xëyma == 132) buum.add("addl $" + ndigel_mbir.부호두바이트() + ", -" + 4 * (àlluwa_tur + 1) + "(%ebp)");
                else throw new Tekki_njumte("wide ndigel 미지원");
            } else if (ndigel == 198 || ndigel == 199) {
                int jëmmukaay_xëyma = 위치 + ndigel_mbir.부호두바이트(); car_lim.add(jëmmukaay_xëyma); Collections.addAll(buum,"popl %eax","testl %eax, %eax",(ndigel == 198 ? "je " : "jne ") + 표식 + "_b" + jëmmukaay_xëyma);
            } else throw new Tekki_njumte("미지원 ndigel: " + ndigel);
        }
        if (!경계들.containsAll(car_lim)) throw new Tekki_njumte("ndigel 경계가 아닌 곳으로 car");
        buum.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",buum);
    }
    String 엑스상수(maas_mbir mbir, int àlluwa_tur) {
        if (mbir.상수종류[àlluwa_tur] == 3) return mbir.Lees_dul_soppi_mbir[àlluwa_tur].toString();
        if (mbir.상수종류[àlluwa_tur] == 8) return araf_yu_bennoo_sembóol(mbir.문자((Integer)mbir.Lees_dul_soppi_mbir[àlluwa_tur]));
        throw new Tekki_njumte("정수와 araf_yu_bennoo_xëyma 상수만 Ndimbal_xëyma");
    }
    String 엑스조립본(String dugal_xabaar_Tomb, List<String> 내보냄, String luñu_name) throws IOException {
        Map<String,String> masin_àlluwa = new HashMap<>();
        for (String buum : Files.readAllLines(Kàttan_Yoonu_jëmale.resolve("엑스기계함수.tsv"))) { String[] ñaar_ñaar_xëyma = buum.split("\t"); if (ñaar_ñaar_xëyma[0].equals(luñu_name)) masin_àlluwa.put(ñaar_ñaar_xëyma[1] + ñaar_ñaar_xëyma[2],ñaar_ñaar_xëyma[3]); }
        int 자리 = dugal_xabaar_Tomb.lastIndexOf('.'); if (자리 < 0) throw new Tekki_njumte("dugal_xabaar_Tomb 지정 njumte");
        String boroom_xëyma = dugal_xabaar_Tomb.substring(0,자리).replace('.','/'), doxalin_dugal_xabaar_tur = dugal_xabaar_Tomb.substring(자리 + 1); doxalin_Royukaay dugal_xabaar_Tomb_xëyma = null;
        for (String 서술 : Arrays.asList("()I","()V")) { doxalin_Royukaay Royukaay = new doxalin_Royukaay(boroom_xëyma,doxalin_dugal_xabaar_tur,서술); if (함수들.containsKey(Royukaay)) { if (dugal_xabaar_Tomb_xëyma != null) throw new Tekki_njumte("겹친 dugal_xabaar_Tomb"); dugal_xabaar_Tomb_xëyma = Royukaay; } }
        if (dugal_xabaar_Tomb_xëyma == null || (함수들.get(dugal_xabaar_Tomb_xëyma).jot_dugal_xabaar & 0x100) != 0) throw new Tekki_njumte("dugal_xabaar_Tomb_xëyma liëey_xëyma dayo_xëyma njumte");
        List<String> buum = new ArrayList<>(); buum.add(".code32");
        for (maas_mbir mbir : 클래스들.values()) {
            String nekkin_xëyma = sembóol("state",mbir.tur_253d1510), doortal = sembóol("init",mbir.tur_253d1510);
            Collections.addAll(buum,".bss",".balign 4",nekkin_xëyma + ": .long 0",".text",doortal + ":","cmpl $0, " + nekkin_xëyma,"jne " + doortal + "_done","movl $1, " + nekkin_xëyma);
            doxalin_Royukaay 초기화참조 = new doxalin_Royukaay(mbir.tur_253d1510,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) buum.add("call " + sembóol("method",초기화참조.부분들()));
            Collections.addAll(buum,"movl $2, " + nekkin_xëyma,doortal + "_done:","ret");
            for (Way_bokk_mbir barabu_denc_ab_joxe_xëyma : mbir.barabu_denc_ab_joxe_xëyma) {
                byte[] Lees_dul_soppi_xëyma = barabu_denc_ab_joxe_xëyma.jagle_xëyma.get("ConstantValue"); String xëyma = Lees_dul_soppi_xëyma == null ? "0" : 엑스상수(mbir,new mbir_jangkat(Lees_dul_soppi_xëyma).두바이트());
                Collections.addAll(buum,".data",".balign 4",sembóol("field",mbir.tur_253d1510,barabu_denc_ab_joxe_xëyma.tur_253d1510,barabu_denc_ab_joxe_xëyma.서술) + ": .long " + xëyma);
            }
            for (Way_bokk_mbir liëey_xëyma : mbir.liëey_xëyma) if (!liëey_xëyma.tur_253d1510.equals("<init>")) buum.add(엑스함수본문(new doxalin_Royukaay(mbir.tur_253d1510,liëey_xëyma.tur_253d1510,liëey_xëyma.서술),liëey_xëyma,masin_àlluwa,luñu_name));
        }
        Collections.addAll(buum,".text",".globl java_entry","java_entry:","call " + sembóol("init",dugal_xabaar_Tomb_xëyma.boroom_xëyma),"call " + sembóol("method",dugal_xabaar_Tomb_xëyma.부분들()));
        if (dugal_xabaar_Tomb_xëyma.서술.equals("()V")) buum.add("xorl %eax, %eax"); buum.add("ret");
        for (String 지정 : 내보냄) {
            int yemalekat_xëyma = 지정.indexOf('='); if (yemalekat_xëyma < 1) throw new Tekki_njumte("내보내기 지정 njumte");
            String 외부 = 지정.substring(0,yemalekat_xëyma), liëey_xëyma = 지정.substring(yemalekat_xëyma + 1); int 나눔 = liëey_xëyma.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tekki_njumte("내보내기 sembóol njumte");
            String maas_xëyma = liëey_xëyma.substring(0,나눔).replace('.','/'), tur_253d1510 = liëey_xëyma.substring(나눔 + 1); doxalin_Royukaay tanneef_xëyma = null;
            for (doxalin_Royukaay Royukaay : 함수들.keySet()) if (Royukaay.boroom_xëyma.equals(maas_xëyma) && Royukaay.tur_253d1510.equals(tur_253d1510)) { if (tanneef_xëyma != null) throw new Tekki_njumte("겹친 내보내기 luñu_name"); tanneef_xëyma = Royukaay; }
            if (tanneef_xëyma == null) throw new Tekki_njumte("내보낼 함수가 없음");
            Collections.addAll(buum,".text",".globl " + 외부,외부 + ":","call " + sembóol("init",tanneef_xëyma.boroom_xëyma),"jmp " + sembóol("method",tanneef_xëyma.부분들()));
        }
        buum.add(".section .rodata");
        for (Map.Entry<String,String> dugal_xabaar_xëyma : 문자열들.entrySet()) {
            Collections.addAll(buum,".balign 4",dugal_xabaar_xëyma.getValue() + ":",".long " + dugal_xabaar_xëyma.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char sa_xëyma : dugal_xabaar_xëyma.getKey().toCharArray()) 단위들.add(Integer.toString(sa_xëyma)); if (!단위들.isEmpty()) buum.add(".long " + String.join(",",단위들));
        }
        buum.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",buum) + "\n";
    }
    static void def_jumtukaay(List<String> ndigel) throws Exception {
        if (new ProcessBuilder(ndigel).inheritIO().start().waitFor() != 0) throw new Tekki_njumte("tabax_Cosaan njumte: " + ndigel.get(0));
    }
    static String mbir_araf_yu_bennoo(String Tekst) { return "\"" + Tekst.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String luñu_name, String dugal_xabaar_Tomb, List<String> 내보냄, Path 출력, Path Kàttan_xëyma) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), maas_Yoonu_jëmale = 임시.resolve("classes"); Files.createDirectory(maas_Yoonu_jëmale);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",maas_Yoonu_jëmale.toString(),"-sourcepath",maas_Yoonu_jëmale.toString(),"-d",maas_Yoonu_jëmale.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Tekki_njumte("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Tekki_njumte(".java 또는 .class만 Ndimbal_xëyma");
            }
            if (원문수 > 0) def_jumtukaay(자바명령);
            try (java.util.stream.Stream<Path> Yoonu_jëmale_lim = Files.walk(maas_Yoonu_jëmale)) { Yoonu_jëmale_lim.filter(Yoonu_jëmale -> Yoonu_jëmale.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,luñu_name.equals("user") ? "user" : "kernel",262144,Kàttan_xëyma);
            String 조립 = 변환.엑스조립본(dugal_xabaar_Tomb,내보냄,luñu_name); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = Kàttan_xëyma.getParent();
            def_jumtukaay(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            def_jumtukaay(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("common_language_runtime_Ndimbal.s").toString()));
            List<String> JOKKOO = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (luñu_name.equals("kernel")) JOKKOO.add("-r");
            else {
                def_jumtukaay(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(luñu_name.equals("user") ? "Door_kiy_jariñoo_internet_jëfekaay.s" : "리눅스시작.s").toString()));
                Collections.addAll(JOKKOO,"-e","_start",임시.resolve("start.o").toString());
                if (luñu_name.equals("user")) Collections.addAll(JOKKOO,"-T",도구위치.resolve("kiy_jariñoo_internet_lëkkale_Tëralin.ld").toString());
            }
            Collections.addAll(JOKKOO,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); def_jumtukaay(JOKKOO);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path Siiwal_xëyma = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),Siiwal_xëyma,StandardCopyOption.REPLACE_EXISTING); Files.move(Siiwal_xëyma,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(Siiwal_xëyma); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(luñu_name.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> sembóol_mbir = new ArrayList<>(), mbiri_cosaan = new ArrayList<>();
            for (doxalin_Royukaay Royukaay : 변환.함수들.keySet()) sembóol_mbir.add(mbir_araf_yu_bennoo(sembóol("method",Royukaay.부분들())) + ":" + mbir_araf_yu_bennoo(Royukaay.boroom_xëyma + "." + Royukaay.tur_253d1510 + Royukaay.서술));
            for (Path 입력 : 입력들) {
                byte[] caabiy_teqale_bi_bara_denc = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Tekst = new StringBuilder(); for (byte xëyma : caabiy_teqale_bi_bara_denc) Tekst.append(String.format(Locale.ROOT,"%02x",xëyma & 255));
                mbiri_cosaan.add(mbir_araf_yu_bennoo(입력.toAbsolutePath().toString()) + ":" + mbir_araf_yu_bennoo(Tekst.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + mbir_araf_yu_bennoo(luñu_name) + ",\"entry\":" + mbir_araf_yu_bennoo(dugal_xabaar_Tomb) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",sembóol_mbir) + "},\"sources\":{" + String.join(",",mbiri_cosaan) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> Yoonu_jëmale_lim = Files.walk(임시)) { for (Path Yoonu_jëmale : (Iterable<Path>)Yoonu_jëmale_lim.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Yoonu_jëmale); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String dugal_xabaar_Tomb = null, luñu_name = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> Yoonu_jëmale_lim = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String xëyma = 인수[순번];
                switch (xëyma) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry maas_xëyma.liëey_xëyma -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export sembóol=maas_xëyma.liëey_xëyma] 클래스파일 또는 Java원문"); return;
                    case "--entry": dugal_xabaar_Tomb = 인수[++순번]; break;
                    case "--profile": luñu_name = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (xëyma.startsWith("-")) throw new Tekki_njumte("알 수 없는 옵션: " + xëyma); Yoonu_jëmale_lim.add(Paths.get(xëyma));
                }
            }
            if (dugal_xabaar_Tomb == null || 출력경로 == null || Yoonu_jëmale_lim.isEmpty()) throw new Tekki_njumte("--entry, -o, maas_xëyma 파일이 필요합니다");
            Path Kàttan_xëyma = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Tekki_njumte("알 수 없는 def_ndigel luñu_name");
                엑스번역(Yoonu_jëmale_lim,엑스대상,dugal_xabaar_Tomb,내보냄,출력경로,Kàttan_xëyma); return;
            }
            String Cosaan = new 기계어미리번역(Yoonu_jëmale_lim, luñu_name, 낱말수, Kàttan_xëyma).생성(dugal_xabaar_Tomb, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, Cosaan, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception njumte) { System.err.println("tabax_Cosaan njumte: " + njumte.getMessage()); System.exit(1); }
    }
}
