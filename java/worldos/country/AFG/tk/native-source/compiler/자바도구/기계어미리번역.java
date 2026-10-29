// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java klas_baha 파일에서 독립 ARM64 커널용 C 원문을 만든다. esasy JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Terjime_säwlik extends RuntimeException {
        Terjime_säwlik(String 설명) { super(설명); }
    }
    static final class maglumat_okyjy {
        final byte[] maglumat;
        int 위치;
        maglumat_okyjy(byte[] 입력자료) { maglumat = 입력자료; }
        byte[] Oka(int dowamlylyk_baha) {
            if (dowamlylyk_baha < 0 || dowamlylyk_baha > maglumat.length - 위치) throw new Terjime_säwlik("잘린 klas_baha 또는 buýruk maglumat");
            byte[] 결과 = Arrays.copyOfRange(maglumat, 위치, 위치 + dowamlylyk_baha); 위치 += dowamlylyk_baha; return 결과;
        }
        int 한바이트() { if (위치 >= maglumat.length) throw new Terjime_säwlik("잘린 buýruk maglumat"); return maglumat[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class agza_maglumat {
        final int ygtyýarlylyk_girizmeklik;
        final String Ad, 서술;
        final Map<String, byte[]> alamat_baha;
        agza_maglumat(int ygtyýarlylyk_baha, String at_baha, String 서술값, Map<String, byte[]> alamat_maglumat) {
            ygtyýarlylyk_girizmeklik = ygtyýarlylyk_baha; Ad = at_baha; 서술 = 서술값; alamat_baha = alamat_maglumat;
        }
    }
    static final class usul_Salgylanma implements Comparable<usul_Salgylanma> {
        final String eýe_baha, Ad, 서술;
        usul_Salgylanma(String 소유값, String at_baha, String 서술값) { eýe_baha = 소유값; Ad = at_baha; 서술 = 서술값; }
        String[] 부분들() { return new String[]{eýe_baha, Ad, 서술}; }
        public int compareTo(usul_Salgylanma deň_derejeli_düwün_baha) {
            int 비교값 = eýe_baha.compareTo(deň_derejeli_düwün_baha.eýe_baha);
            if (비교값 == 0) 비교값 = Ad.compareTo(deň_derejeli_düwün_baha.Ad);
            return 비교값 == 0 ? 서술.compareTo(deň_derejeli_düwün_baha.서술) : 비교값;
        }
        public boolean equals(Object deň_derejeli_düwün_baha) { return deň_derejeli_düwün_baha instanceof usul_Salgylanma && compareTo((usul_Salgylanma) deň_derejeli_düwün_baha) == 0; }
        public int hashCode() { return Objects.hash(eýe_baha, Ad, 서술); }
    }
    static final class klas_maglumat {
        final int[] 상수종류;
        final Object[] hemişelik_maglumat;
        final String Ad;
        final List<agza_maglumat> meýdan_baha, FUNCTION_baha;
        klas_maglumat(Path Ýol) throws IOException {
            maglumat_okyjy okyjy_baha = new maglumat_okyjy(Files.readAllBytes(Ýol));
            if (okyjy_baha.네바이트() != 0xcafebabe) throw new Terjime_säwlik("Java klas_baha 표식이 아님");
            okyjy_baha.Oka(4);
            int 개수 = okyjy_baha.두바이트(); 상수종류 = new int[개수]; hemişelik_maglumat = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = okyjy_baha.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int dowamlylyk_baha = okyjy_baha.두바이트();
                        byte[] nyşan_bufer = okyjy_baha.Oka(dowamlylyk_baha), 길이붙인자료 = new byte[dowamlylyk_baha + 2];
                        길이붙인자료[0] = (byte)(dowamlylyk_baha >> 8); 길이붙인자료[1] = (byte)dowamlylyk_baha;
                        System.arraycopy(nyşan_bufer, 0, 길이붙인자료, 2, dowamlylyk_baha);
                        hemişelik_maglumat[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: hemişelik_maglumat[순번] = okyjy_baha.네바이트(); break;
                    case 4: okyjy_baha.Oka(4); break;
                    case 5: case 6: okyjy_baha.Oka(8); 순번++; break;
                    case 7: case 8: case 16: hemişelik_maglumat[순번] = okyjy_baha.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        hemişelik_maglumat[순번] = new int[]{okyjy_baha.두바이트(), okyjy_baha.두바이트()}; break;
                    case 15: hemişelik_maglumat[순번] = new int[]{okyjy_baha.한바이트(), okyjy_baha.두바이트()}; break;
                    default: throw new Terjime_säwlik("지원하지 않는 hemişelik_baha 종류: " + 종류);
                }
            }
            okyjy_baha.두바이트(); Ad = klas_at(okyjy_baha.두바이트());
            if (!klas_at(okyjy_baha.두바이트()).equals("java/lang/Object") || okyjy_baha.두바이트() != 0)
                throw new Terjime_säwlik(Ad + ": 상속 및 인터페이스 미지원");
            meýdan_baha = 멤버읽기(okyjy_baha); FUNCTION_baha = 멤버읽기(okyjy_baha); 속성읽기(okyjy_baha);
            if (okyjy_baha.위치 != okyjy_baha.maglumat.length) throw new Terjime_säwlik("klas_baha 뒤에 남은 maglumat");
        }
        String 문자(int indeks) {
            if (indeks < 1 || indeks >= 상수종류.length || 상수종류[indeks] != 1) throw new Terjime_säwlik("문자 hemişelik_baha indeks Hata");
            return (String) hemişelik_maglumat[indeks];
        }
        String klas_at(int indeks) {
            if (indeks < 1 || indeks >= 상수종류.length || 상수종류[indeks] != 7) throw new Terjime_säwlik("klas_baha Salgylanma Hata");
            return 문자((Integer)hemişelik_maglumat[indeks]);
        }
        usul_Salgylanma Salgylanma(int indeks) {
            if (indeks < 1 || indeks >= 상수종류.length || 상수종류[indeks] < 9 || 상수종류[indeks] > 11) throw new Terjime_säwlik("멤버 Salgylanma Hata");
            int[] goşa_bol_baha = (int[])hemişelik_maglumat[indeks], at_goşa_bol = (int[])hemişelik_maglumat[goşa_bol_baha[1]];
            return new usul_Salgylanma(klas_at(goşa_bol_baha[0]), 문자(at_goşa_bol[0]), 문자(at_goşa_bol[1]));
        }
        Map<String, byte[]> 속성읽기(maglumat_okyjy okyjy_baha) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = okyjy_baha.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String alamat_at = 문자(okyjy_baha.두바이트()); byte[] baha = okyjy_baha.Oka(okyjy_baha.네바이트());
                if (결과.put(alamat_at, baha) != null) throw new Terjime_säwlik("겹친 alamat_baha: " + alamat_at);
            }
            return 결과;
        }
        List<agza_maglumat> 멤버읽기(maglumat_okyjy okyjy_baha) {
            List<agza_maglumat> 결과 = new ArrayList<>(); int 개수 = okyjy_baha.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int ygtyýarlylyk_girizmeklik = okyjy_baha.두바이트(); String usul_girizmeklik_at = 문자(okyjy_baha.두바이트()), 서술 = 문자(okyjy_baha.두바이트());
                결과.add(new agza_maglumat(ygtyýarlylyk_girizmeklik, usul_girizmeklik_at, 서술, 속성읽기(okyjy_baha)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Terjime_säwlik("FUNCTION_baha 서술 Hata: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Terjime_säwlik("FUNCTION_baha 서술 Hata: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Terjime_säwlik("FUNCTION_baha 서술 Hata: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String saýlama_baha = null;
            for (String format_baha : 허용형식) if (서술.startsWith(format_baha, 위치)) { saýlama_baha = format_baha; break; }
            if (saýlama_baha == null) throw new Terjime_säwlik("지원하지 않는 maglumatlaryň_görnüşi: " + 서술);
            결과.add(saýlama_baha); 위치 += saýlama_baha.length();
        }
        return 결과;
    }
    static String nyşan(String 종류, String... 부분들) {
        try {
            byte[] heş_kody_faýl = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Metin = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Metin.append(String.format(Locale.ROOT, "%02x", heş_kody_faýl[순번] & 255));
            return Metin.toString();
        } catch (Exception Hata) { throw new Terjime_säwlik(Hata.toString()); }
    }
    final Map<String, klas_maglumat> 클래스들 = new TreeMap<>();
    final Map<usul_Salgylanma, agza_maglumat> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, kompýuter_klas;
    final int 동적기억낱말수;
    final Path gor_ýol;
    기계어미리번역(List<Path> ýol_Sanaw, String niýet, int 낱말수, Path gor_baha) throws IOException {
        if ((!niýet.equals("kernel") && !niýet.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Terjime_säwlik("ýerine_ýetir_buýruk niýet 또는 ýat_baha 공간 Ululyk Hata");
        실행대상 = niýet; 동적기억낱말수 = 낱말수; gor_ýol = gor_baha;
        // 이 이름도 국가별 gor_agaç 생성 시 해당 언어로 옮긴다.
        kompýuter_klas = niýet.equals("kernel") ? "보드" : "ulanyjy";
        for (String setir : Files.readAllLines(gor_baha.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = setir.split("\t", -1);
            if (부분들.length != 4) throw new Terjime_säwlik("kompýuter FUNCTION_baha maglumat Hata");
            if (부분들[0].equals(niýet)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Ýol : ýol_Sanaw) {
            klas_maglumat maglumat = new klas_maglumat(Ýol);
            if (클래스들.put(maglumat.Ad, maglumat) != null) throw new Terjime_säwlik("중복 klas_baha: " + maglumat.Ad);
            for (agza_maglumat meýdan_baha : maglumat.meýdan_baha) {
                if ((meýdan_baha.ygtyýarlylyk_girizmeklik & 8) == 0 || 형식읽기(meýdan_baha.서술).equals(Collections.singletonList("V"))) throw new Terjime_säwlik("statiki_baha 필드만 Goldaw_baha");
                if (필드들.put(new usul_Salgylanma(maglumat.Ad, meýdan_baha.Ad, meýdan_baha.서술), meýdan_baha) != null) throw new Terjime_säwlik("중복 meýdan_baha");
            }
            for (agza_maglumat FUNCTION_baha : maglumat.FUNCTION_baha) {
                if (FUNCTION_baha.Ad.equals("<init>")) continue;
                if ((FUNCTION_baha.ygtyýarlylyk_girizmeklik & 8) == 0 || (FUNCTION_baha.ygtyýarlylyk_girizmeklik & (0x20 | 0x400)) != 0) throw new Terjime_säwlik("statiki_baha 비동기화 함수만 Goldaw_baha");
                new 함수형식(FUNCTION_baha.서술);
                if (함수들.put(new usul_Salgylanma(maglumat.Ad, FUNCTION_baha.Ad, FUNCTION_baha.서술), FUNCTION_baha) != null) throw new Terjime_säwlik("중복 FUNCTION_baha");
            }
        }
    }
    String setir_nyşan(String Metin) { return 문자열들.computeIfAbsent(Metin, baha -> "j_text_" + 문자열들.size()); }
    String hemişelik_aňlatma(klas_maglumat maglumat, int indeks) {
        if (indeks < 1 || indeks >= maglumat.상수종류.length) throw new Terjime_säwlik("hemişelik_baha indeks klip Hata");
        if (maglumat.상수종류[indeks] == 3) return "(word)(uint32_t)(" + maglumat.hemişelik_maglumat[indeks] + ")";
        if (maglumat.상수종류[indeks] == 8) return "(word)" + setir_nyşan(maglumat.문자((Integer)maglumat.hemişelik_maglumat[indeks]));
        throw new Terjime_säwlik("정수와 setir_baha_6ca8363c 상수만 Goldaw_baha");
    }
    String 함수원형(usul_Salgylanma Salgylanma) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Salgylanma.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + nyşan("method", Salgylanma.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void derňe_ýerli(int indeks, int 지역변수수) { if (indeks < 0 || indeks >= 지역변수수) throw new Terjime_säwlik("ýerli_elýeterli_gor 변수 indeks klip Hata"); }
    void 분기넣기(List<String> 출력, Set<Integer> şahalanma_Sanaw, int 위치, int 이동량, String şert) {
        int barylmaly_ýer_baha = 위치 + 이동량; şahalanma_Sanaw.add(barylmaly_ýer_baha);
        출력.add((şert == null ? "" : "if (" + şert + ") ") + "goto b" + barylmaly_ýer_baha + ";");
    }
    String 함수본문(usul_Salgylanma FUNCTION_baha, agza_maglumat maglumat) {
        byte[] 본문자료 = maglumat.alamat_baha.get("Code"); if (본문자료 == null) throw new Terjime_säwlik("FUNCTION_baha 몸체가 없음: " + FUNCTION_baha.Ad);
        maglumat_okyjy okyjy_baha = new maglumat_okyjy(본문자료); int 쌓임깊이 = okyjy_baha.두바이트(), 지역변수수 = okyjy_baha.두바이트();
        maglumat_okyjy buýruk_maglumat = new maglumat_okyjy(okyjy_baha.Oka(okyjy_baha.네바이트()));
        if (okyjy_baha.두바이트() != 0) throw new Terjime_säwlik("try/catch/finally 미지원");
        함수형식 format_baha = new 함수형식(FUNCTION_baha.서술); if (지역변수수 < format_baha.인수.size()) throw new Terjime_säwlik("매개변수보다 적은 ýerli_elýeterli_gor 변수");
        klas_maglumat klas_baha = 클래스들.get(FUNCTION_baha.eýe_baha);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(FUNCTION_baha) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_baha.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), şahalanma_Sanaw = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (buýruk_maglumat.위치 < buýruk_maglumat.maglumat.length) {
            int 위치 = buýruk_maglumat.위치, buýruk = buýruk_maglumat.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (buýruk == 0) continue;
            if (buýruk == 1) 출력.add("PUSH(0);");
            else if (buýruk >= 2 && buýruk <= 8) 출력.add("PUSH((uint32_t)(" + (buýruk - 3) + "));");
            else if (buýruk == 16 || buýruk == 17) 출력.add("PUSH((uint32_t)(" + (buýruk == 16 ? buýruk_maglumat.부호한바이트() : buýruk_maglumat.부호두바이트()) + "));");
            else if (buýruk == 18 || buýruk == 19) 출력.add("PUSH(" + hemişelik_aňlatma(klas_baha, buýruk == 18 ? buýruk_maglumat.한바이트() : buýruk_maglumat.두바이트()) + ");");
            else if (buýruk == 21 || buýruk == 25 || (buýruk >= 26 && buýruk <= 29) || (buýruk >= 42 && buýruk <= 45)) {
                int indeks = buýruk == 21 || buýruk == 25 ? buýruk_maglumat.한바이트() : buýruk - (buýruk <= 29 ? 26 : 42);
                derňe_ýerli(indeks, 지역변수수); 출력.add("PUSH(l[" + indeks + "]);");
            } else if (buýruk == 54 || buýruk == 58 || (buýruk >= 59 && buýruk <= 62) || (buýruk >= 75 && buýruk <= 78)) {
                int indeks = buýruk == 54 || buýruk == 58 ? buýruk_maglumat.한바이트() : buýruk - (buýruk <= 62 ? 59 : 75);
                derňe_ýerli(indeks, 지역변수수); 출력.add("l[" + indeks + "] = POP();");
            } else if (buýruk == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (buýruk == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (buýruk == 87 || buýruk == 88) 출력.add(buýruk == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (buýruk >= 89 && buýruk <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] tertip_Sanaw = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[buýruk - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char baha : tertip_Sanaw[buýruk - 89].toCharArray()) 출력.add("PUSH(" + baha + ");");
            } else if (buýruk == 96 || buýruk == 100 || buýruk == 104 || buýruk == 126 || buýruk == 128 || buýruk == 130) {
                String amal_baha = buýruk == 96 ? "+" : buýruk == 100 ? "-" : buýruk == 104 ? "*" : buýruk == 126 ? "&" : buýruk == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + amal_baha + " (uint32_t)b);");
            } else if (buýruk == 108 || buýruk == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (buýruk == 112 ? 1 : 0) + "));");
            else if (buýruk == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (buýruk == 120 || buýruk == 122 || buýruk == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (buýruk == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (buýruk == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (buýruk == 132) {
                int indeks = buýruk_maglumat.한바이트(), 증가량 = buýruk_maglumat.부호한바이트(); derňe_ýerli(indeks, 지역변수수);
                출력.add("l[" + indeks + "] = (uint32_t)l[" + indeks + "] + (uint32_t)(" + 증가량 + ");");
            } else if (buýruk >= 145 && buýruk <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (buýruk == 145 ? "int8_t" : buýruk == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (buýruk >= 153 && buýruk <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, şahalanma_Sanaw, 위치, buýruk_maglumat.부호두바이트(), "(int32_t)a " + 비교들[buýruk - 153] + " 0");
            } else if (buýruk >= 159 && buýruk <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, şahalanma_Sanaw, 위치, buýruk_maglumat.부호두바이트(), buýruk >= 165 ? "a " + 비교들[buýruk - 159] + " b" : "(int32_t)a " + 비교들[buýruk - 159] + " (int32_t)b");
            } else if (buýruk == 167 || buýruk == 200) 분기넣기(출력, şahalanma_Sanaw, 위치, buýruk == 167 ? buýruk_maglumat.부호두바이트() : buýruk_maglumat.네바이트(), null);
            else if (buýruk == 170 || buýruk == 171) {
                while (buýruk_maglumat.위치 % 4 != 0) buýruk_maglumat.한바이트();
                int öňünden_kabul_edilen_baha = buýruk_maglumat.네바이트(); 출력.add("a = POP();");
                if (buýruk == 170) {
                    int 아래 = buýruk_maglumat.네바이트(), 위 = buýruk_maglumat.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (buýruk_maglumat.maglumat.length - buýruk_maglumat.위치) / 4) throw new Terjime_säwlik("switch klip Hata");
                    for (long baha = 아래; baha <= 위; baha++) 분기넣기(출력, şahalanma_Sanaw, 위치, buýruk_maglumat.네바이트(), "(int32_t)a == (" + baha + ")");
                } else {
                    int 개수 = buýruk_maglumat.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (buýruk_maglumat.maglumat.length - buýruk_maglumat.위치) / 8) throw new Terjime_säwlik("switch Ululyk Hata");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int baha = buýruk_maglumat.네바이트(); if (순번 > 0 && baha <= 앞값) throw new Terjime_säwlik("switch tertip_baha Hata"); 앞값 = baha;
                        분기넣기(출력, şahalanma_Sanaw, 위치, buýruk_maglumat.네바이트(), "(int32_t)a == (" + baha + ")");
                    }
                }
                분기넣기(출력, şahalanma_Sanaw, 위치, öňünden_kabul_edilen_baha, null);
            } else if (buýruk == 172 || buýruk == 176 || buýruk == 177) 출력.add("return " + (buýruk == 177 ? "0" : "POP()") + ";");
            else if (buýruk == 178 || buýruk == 179) {
                usul_Salgylanma Salgylanma = klas_baha.Salgylanma(buýruk_maglumat.두바이트()); if (!필드들.containsKey(Salgylanma)) throw new Terjime_säwlik("알 수 없는 meýdan_baha");
                출력.add(nyşan("init", Salgylanma.eýe_baha) + "();"); String meýdan_baha = nyşan("field", Salgylanma.부분들());
                출력.add(buýruk == 178 ? "PUSH(" + meýdan_baha + ");" : meýdan_baha + " = POP();");
            } else if (buýruk == 184) {
                usul_Salgylanma Salgylanma = klas_baha.Salgylanma(buýruk_maglumat.두바이트()); if (!함수들.containsKey(Salgylanma)) throw new Terjime_säwlik("알 수 없는 FUNCTION_baha");
                함수형식 호출형식 = new 함수형식(Salgylanma.서술); int 개수 = 호출형식.인수.size();
                출력.add(nyşan("init", Salgylanma.eýe_baha) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + nyşan("method", Salgylanma.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (buýruk == 182) {
                usul_Salgylanma Salgylanma = klas_baha.Salgylanma(buýruk_maglumat.두바이트());
                if (Salgylanma.equals(new usul_Salgylanma("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Salgylanma.equals(new usul_Salgylanma("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Terjime_säwlik("가상 FUNCTION_baha 호출 미지원");
            } else if (buýruk == 188) {
                if (buýruk_maglumat.한바이트() != 10) throw new Terjime_säwlik("new int[]만 Goldaw_baha"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (buýruk == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (buýruk == 196) {
                int giňelme_baha = buýruk_maglumat.한바이트(), indeks = buýruk_maglumat.두바이트(); derňe_ýerli(indeks, 지역변수수);
                if (giňelme_baha == 21 || giňelme_baha == 25) 출력.add("PUSH(l[" + indeks + "]);");
                else if (giňelme_baha == 54 || giňelme_baha == 58) 출력.add("l[" + indeks + "] = POP();");
                else if (giňelme_baha == 132) 출력.add("l[" + indeks + "] = (uint32_t)l[" + indeks + "] + (uint32_t)(" + buýruk_maglumat.부호두바이트() + ");");
                else throw new Terjime_säwlik("미지원 wide buýruk");
            } else if (buýruk == 198 || buýruk == 199) {
                출력.add("a = POP();"); 분기넣기(출력, şahalanma_Sanaw, 위치, buýruk_maglumat.부호두바이트(), "a " + (buýruk == 198 ? "==" : "!=") + " 0");
            } else throw new Terjime_säwlik(FUNCTION_baha.eýe_baha + "." + FUNCTION_baha.Ad + ", baýt_baha " + 위치 + ": 미지원 buýruk " + buýruk);
        }
        if (!경계들.containsAll(şahalanma_Sanaw)) throw new Terjime_säwlik("buýruk 경계가 아닌 곳으로 şahalanma");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String eksport_et_usul(String Bag_nyşan, String niýet, boolean 진입점여부) {
        int 자리 = niýet.lastIndexOf('.'); if (자리 < 0 || !Bag_nyşan.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Terjime_säwlik("내보내기 지정 Hata");
        String eýe_baha = niýet.substring(0, 자리).replace('.', '/'), Ad = niýet.substring(자리 + 1); usul_Salgylanma saýlama_baha = null;
        for (usul_Salgylanma Salgylanma : 함수들.keySet()) if (Salgylanma.eýe_baha.equals(eýe_baha) && Salgylanma.Ad.equals(Ad)) {
            if (saýlama_baha != null) throw new Terjime_säwlik("겹친 내보내기 niýet"); saýlama_baha = Salgylanma;
        }
        if (saýlama_baha == null || (함수들.get(saýlama_baha).ygtyýarlylyk_girizmeklik & 0x100) != 0) throw new Terjime_säwlik("내보낼 함수가 없음 또는 native FUNCTION_baha");
        함수형식 format_baha = new 함수형식(saýlama_baha.서술);
        if ((진입점여부 && !format_baha.인수.isEmpty()) || !Arrays.asList("V", "I").contains(format_baha.반환)) throw new Terjime_säwlik("girizmeklik_utuk_baha 또는 C 경계 format_baha Hata");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_baha.인수.size(); 순번++) {
            if (!format_baha.인수.get(순번).equals("I")) throw new Terjime_säwlik("C 경계는 int 인수만 Goldaw_baha");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_baha.반환.equals("V") ? "void " : "int32_t ") + Bag_nyşan + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + nyşan("init", saýlama_baha.eýe_baha) + "(); " + (format_baha.반환.equals("V") ? "" : "return (int32_t)") + nyşan("method", saýlama_baha.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String girizmeklik_utuk, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<usul_Salgylanma, agza_maglumat> girizmeklik_baha : 함수들.entrySet()) {
            usul_Salgylanma Salgylanma = girizmeklik_baha.getKey(); agza_maglumat maglumat = girizmeklik_baha.getValue(); 선언들.add(함수원형(Salgylanma) + ";");
            if ((maglumat.ygtyýarlylyk_girizmeklik & 0x100) != 0) {
                String Birikme = 기계함수들.get(Salgylanma.Ad + Salgylanma.서술);
                if (!Salgylanma.eýe_baha.equals(kompýuter_klas) || Birikme == null) throw new Terjime_säwlik("허용되지 않은 native FUNCTION_baha: " + Salgylanma.Ad);
                int 개수 = new 함수형식(Salgylanma.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Birikme + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Salgylanma) + " { return " + Birikme + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Salgylanma, maglumat));
        }
        for (Map.Entry<usul_Salgylanma, agza_maglumat> girizmeklik_baha : 필드들.entrySet()) {
            usul_Salgylanma Salgylanma = girizmeklik_baha.getKey(); byte[] hemişelik_baha = girizmeklik_baha.getValue().alamat_baha.get("ConstantValue");
            String baha = hemişelik_baha == null ? "0" : hemişelik_aňlatma(클래스들.get(Salgylanma.eýe_baha), new maglumat_okyjy(hemişelik_baha).두바이트());
            필드선언들.add("static word " + nyşan("field", Salgylanma.부분들()) + " = " + baha + ";");
        }
        for (String Ad : 클래스들.keySet()) {
            String ulanyşa_taýýarla = nyşan("init", Ad), ýagdaý_baha = nyşan("state", Ad);
            선언들.add("static void " + ulanyşa_taýýarla + "(void);"); 필드선언들.add("static unsigned " + ýagdaý_baha + ";");
            usul_Salgylanma Salgylanma = new usul_Salgylanma(Ad, "<clinit>", "()V");
            몸체들.add("static void " + ulanyşa_taýýarla + "(void) { if(" + ýagdaý_baha + ") return; " + ýagdaý_baha + " = 1; " + (함수들.containsKey(Salgylanma) ? nyşan("method", Salgylanma.부분들()) + "(); " : "") + ýagdaý_baha + " = 2; }");
        }
        몸체들.add(eksport_et_usul("java_entry", girizmeklik_utuk, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new Terjime_säwlik("내보내기 지정 Hata");
            String Ad = 지정.substring(0, 자리); 공개이름.add(Ad); 몸체들.add(eksport_et_usul(Ad, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> girizmeklik_baha : 문자열들.entrySet()) {
            String Metin = girizmeklik_baha.getKey(); StringBuilder ARRAY_baha = new StringBuilder("static const word " + girizmeklik_baha.getValue() + "[] = {" + Metin.length());
            for (int 순번 = 0; 순번 < Metin.length(); 순번++) ARRAY_baha.append(", ").append((int)Metin.charAt(순번));
            문자열선언들.add(ARRAY_baha.append("};").toString());
        }
        String Goldaw_baha = Files.readString(gor_ýol.resolve("umumy_dil_işlediş_gurşawy_Goldaw.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Goldaw_baha + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String Çeşme, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> at_tablisa = new HashMap<>();
        for (String setir : Files.readAllLines(gor_ýol.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] goşa_bol_baha = setir.split("\t"); at_tablisa.put(goşa_bol_baha[0], goşa_bol_baha[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(Çeşme); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Ad = 찾개.group(), 새이름 = Ad;
            if (!Ad.startsWith("//") && !Ad.startsWith("/*") && !Ad.startsWith("\"") && !Ad.startsWith("'") && !공개이름.contains(Ad)) {
                새이름 = at_tablisa.getOrDefault(Ad, Ad);
                if (Ad.matches("a[0-9]+")) 새이름 = "인수" + Ad.substring(1);
                if (Ad.matches("b[0-9]+")) 새이름 = "şahalanma" + Ad.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char nyşan_baha_068c2631 : 새이름.toCharArray()) 표기.append(nyşan_baha_068c2631 < 128 ? Character.toString(nyşan_baha_068c2631) : String.format(Locale.ROOT, "\\u%04x", (int)nyşan_baha_068c2631));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(usul_Salgylanma FUNCTION_baha, agza_maglumat maglumat, Map<String,String> kompýuter_tablisa, String niýet) {
        String 표식 = nyşan("method", FUNCTION_baha.부분들());
        List<String> setir = new ArrayList<>();
        if ((maglumat.ygtyýarlylyk_girizmeklik & 0x100) != 0) {
            String Birikme = kompýuter_tablisa.get(FUNCTION_baha.Ad + FUNCTION_baha.서술);
            if (!FUNCTION_baha.eýe_baha.equals(niýet.equals("kernel") ? "enjam_baha" : "ulanyjy") || Birikme == null) throw new Terjime_säwlik("허용되지 않은 native FUNCTION_baha");
            return ".text\n" + 표식 + ":\njmp " + Birikme;
        }
        byte[] göwre_teksti = maglumat.alamat_baha.get("Code"); if (göwre_teksti == null) throw new Terjime_säwlik("FUNCTION_baha 몸체가 없음");
        maglumat_okyjy okyjy_baha = new maglumat_okyjy(göwre_teksti); okyjy_baha.두바이트(); int 지역수 = okyjy_baha.두바이트();
        maglumat_okyjy buýruk_maglumat = new maglumat_okyjy(okyjy_baha.Oka(okyjy_baha.네바이트()));
        if (okyjy_baha.두바이트() != 0) throw new Terjime_säwlik("try/catch/finally 미지원");
        함수형식 format_baha = new 함수형식(FUNCTION_baha.서술); if (지역수 < format_baha.인수.size()) throw new Terjime_säwlik("매개변수보다 적은 ýerli_elýeterli_gor 변수");
        Collections.addAll(setir,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_baha.인수.size(); 순번++) Collections.addAll(setir,"movl " + (8 + 4 * (format_baha.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        klas_maglumat klas_baha = 클래스들.get(FUNCTION_baha.eýe_baha); Set<Integer> 경계들 = new HashSet<>(), şahalanma_Sanaw = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (buýruk_maglumat.위치 < buýruk_maglumat.maglumat.length) {
            int 위치 = buýruk_maglumat.위치, buýruk = buýruk_maglumat.한바이트(); String 자리 = 표식 + "_b" + 위치;
            setir.add(자리 + ":"); 경계들.add(위치);
            if (buýruk == 0) setir.add("nop");
            else if (buýruk == 1) setir.add("pushl $0");
            else if (buýruk >= 2 && buýruk <= 8) setir.add("pushl $" + (buýruk - 3));
            else if (buýruk == 16 || buýruk == 17) setir.add("pushl $" + (buýruk == 16 ? buýruk_maglumat.부호한바이트() : buýruk_maglumat.부호두바이트()));
            else if (buýruk == 18 || buýruk == 19) {
                int indeks = buýruk == 18 ? buýruk_maglumat.한바이트() : buýruk_maglumat.두바이트();
                setir.add("pushl $" + 엑스상수(klas_baha,indeks));
            } else if (buýruk == 21 || buýruk == 25 || (buýruk >= 26 && buýruk <= 29) || (buýruk >= 42 && buýruk <= 45) || buýruk == 54 || buýruk == 58 || (buýruk >= 59 && buýruk <= 62) || (buýruk >= 75 && buýruk <= 78)) {
                boolean 읽음 = buýruk < 54; int indeks = buýruk == 21 || buýruk == 25 || buýruk == 54 || buýruk == 58 ? buýruk_maglumat.한바이트() : buýruk - (buýruk <= 29 ? 26 : buýruk <= 45 ? 42 : buýruk <= 62 ? 59 : 75);
                derňe_ýerli(indeks,지역수); setir.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (indeks + 1)) + "(%ebp)");
            } else if (buýruk == 46) Collections.addAll(setir,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (buýruk == 79) Collections.addAll(setir,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (buýruk == 87 || buýruk == 88) setir.add("addl $" + (buýruk == 87 ? 4 : 8) + ", %esp");
            else if (buýruk >= 89 && buýruk <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] tertip_Sanaw = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[buýruk - 89]; 순번++) setir.add("popl " + 저장기들[순번]);
                for (int 순번 : tertip_Sanaw[buýruk - 89]) setir.add("pushl " + 저장기들[순번]);
            } else if (buýruk == 96 || buýruk == 100 || buýruk == 104 || buýruk == 126 || buýruk == 128 || buýruk == 130) {
                String amal_baha = buýruk == 96 ? "addl" : buýruk == 100 ? "subl" : buýruk == 104 ? "imull" : buýruk == 126 ? "andl" : buýruk == 128 ? "orl" : "xorl";
                Collections.addAll(setir,"popl %ecx","popl %eax",amal_baha + " %ecx, %eax","pushl %eax");
            } else if (buýruk == 108 || buýruk == 112) Collections.addAll(setir,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (buýruk == 108 ? "%eax" : "%edx"));
            else if (buýruk == 116) setir.add("negl (%esp)");
            else if (buýruk == 120 || buýruk == 122 || buýruk == 124) Collections.addAll(setir,"popl %ecx","popl %eax",(buýruk == 120 ? "sall" : buýruk == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (buýruk == 132) {
                int indeks = buýruk_maglumat.한바이트(), 증가 = buýruk_maglumat.부호한바이트(); derňe_ýerli(indeks,지역수); setir.add("addl $" + 증가 + ", -" + (4 * (indeks + 1)) + "(%ebp)");
            } else if (buýruk >= 145 && buýruk <= 147) Collections.addAll(setir,"popl %eax",buýruk == 145 ? "movsbl %al, %eax" : buýruk == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (buýruk >= 153 && buýruk <= 166) {
                if (buýruk <= 158) Collections.addAll(setir,"popl %eax","testl %eax, %eax");
                else Collections.addAll(setir,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int barylmaly_ýer_baha = 위치 + buýruk_maglumat.부호두바이트(); şahalanma_Sanaw.add(barylmaly_ýer_baha); setir.add(비교들[buýruk - (buýruk <= 158 ? 153 : 159)] + " " + 표식 + "_b" + barylmaly_ýer_baha);
            } else if (buýruk == 167 || buýruk == 200) {
                int barylmaly_ýer_baha = 위치 + (buýruk == 167 ? buýruk_maglumat.부호두바이트() : buýruk_maglumat.네바이트()); şahalanma_Sanaw.add(barylmaly_ýer_baha); setir.add("jmp " + 표식 + "_b" + barylmaly_ýer_baha);
            } else if (buýruk == 170 || buýruk == 171) {
                while (buýruk_maglumat.위치 % 4 != 0) buýruk_maglumat.한바이트();
                int öňünden_kabul_edilen_baha = 위치 + buýruk_maglumat.네바이트(); şahalanma_Sanaw.add(öňünden_kabul_edilen_baha); setir.add("popl %eax");
                int 개수, 아래 = 0;
                if (buýruk == 170) { 아래 = buýruk_maglumat.네바이트(); int 위 = buýruk_maglumat.네바이트(); long dowamlylyk_baha = (long)위 - 아래 + 1; if (dowamlylyk_baha < 1 || dowamlylyk_baha > (buýruk_maglumat.maglumat.length - buýruk_maglumat.위치) / 4) throw new Terjime_säwlik("switch klip Hata"); 개수 = (int)dowamlylyk_baha; }
                else { 개수 = buýruk_maglumat.네바이트(); if (개수 < 0 || 개수 > (buýruk_maglumat.maglumat.length - buýruk_maglumat.위치) / 8) throw new Terjime_säwlik("switch Ululyk Hata"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int baha = buýruk == 170 ? 아래 + 순번 : buýruk_maglumat.네바이트(), barylmaly_ýer_baha = 위치 + buýruk_maglumat.네바이트(); şahalanma_Sanaw.add(barylmaly_ýer_baha);
                    Collections.addAll(setir,"cmpl $" + baha + ", %eax","je " + 표식 + "_b" + barylmaly_ýer_baha);
                }
                setir.add("jmp " + 표식 + "_b" + öňünden_kabul_edilen_baha);
            } else if (buýruk == 172 || buýruk == 176 || buýruk == 177) {
                if (buýruk != 177) setir.add("popl %eax"); Collections.addAll(setir,"leave","ret");
            } else if (buýruk == 178 || buýruk == 179) {
                usul_Salgylanma Salgylanma = klas_baha.Salgylanma(buýruk_maglumat.두바이트()); if (!필드들.containsKey(Salgylanma)) throw new Terjime_säwlik("알 수 없는 meýdan_baha");
                Collections.addAll(setir,"call " + nyşan("init",Salgylanma.eýe_baha),(buýruk == 178 ? "pushl " : "popl ") + nyşan("field",Salgylanma.부분들()));
            } else if (buýruk == 184) {
                usul_Salgylanma Salgylanma = klas_baha.Salgylanma(buýruk_maglumat.두바이트()); if (!함수들.containsKey(Salgylanma)) throw new Terjime_säwlik("알 수 없는 FUNCTION_baha");
                함수형식 호출형식 = new 함수형식(Salgylanma.서술); Collections.addAll(setir,"call " + nyşan("init",Salgylanma.eýe_baha),"call " + nyşan("method",Salgylanma.부분들()));
                if (!호출형식.인수.isEmpty()) setir.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) setir.add("pushl %eax");
            } else if (buýruk == 182) {
                usul_Salgylanma Salgylanma = klas_baha.Salgylanma(buýruk_maglumat.두바이트());
                if (Salgylanma.equals(new usul_Salgylanma("java/lang/String","length","()I"))) Collections.addAll(setir,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Salgylanma.equals(new usul_Salgylanma("java/lang/String","charAt","(I)C"))) Collections.addAll(setir,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Terjime_säwlik("가상 FUNCTION_baha 호출 미지원");
            } else if (buýruk == 188) {
                if (buýruk_maglumat.한바이트() != 10) throw new Terjime_säwlik("new int[]만 Goldaw_baha"); Collections.addAll(setir,"popl %eax","call rt_new_array","pushl %eax");
            } else if (buýruk == 190) Collections.addAll(setir,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (buýruk == 196) {
                int giňelme_baha = buýruk_maglumat.한바이트(), indeks = buýruk_maglumat.두바이트(); derňe_ýerli(indeks,지역수);
                if (giňelme_baha == 21 || giňelme_baha == 25 || giňelme_baha == 54 || giňelme_baha == 58) setir.add((giňelme_baha <= 25 ? "pushl " : "popl ") + "-" + 4 * (indeks + 1) + "(%ebp)");
                else if (giňelme_baha == 132) setir.add("addl $" + buýruk_maglumat.부호두바이트() + ", -" + 4 * (indeks + 1) + "(%ebp)");
                else throw new Terjime_säwlik("wide buýruk 미지원");
            } else if (buýruk == 198 || buýruk == 199) {
                int barylmaly_ýer_baha = 위치 + buýruk_maglumat.부호두바이트(); şahalanma_Sanaw.add(barylmaly_ýer_baha); Collections.addAll(setir,"popl %eax","testl %eax, %eax",(buýruk == 198 ? "je " : "jne ") + 표식 + "_b" + barylmaly_ýer_baha);
            } else throw new Terjime_säwlik("미지원 buýruk: " + buýruk);
        }
        if (!경계들.containsAll(şahalanma_Sanaw)) throw new Terjime_säwlik("buýruk 경계가 아닌 곳으로 şahalanma");
        setir.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",setir);
    }
    String 엑스상수(klas_maglumat maglumat, int indeks) {
        if (maglumat.상수종류[indeks] == 3) return maglumat.hemişelik_maglumat[indeks].toString();
        if (maglumat.상수종류[indeks] == 8) return setir_nyşan(maglumat.문자((Integer)maglumat.hemişelik_maglumat[indeks]));
        throw new Terjime_säwlik("정수와 setir_baha_6ca8363c 상수만 Goldaw_baha");
    }
    String 엑스조립본(String girizmeklik_utuk, List<String> 내보냄, String niýet) throws IOException {
        Map<String,String> kompýuter_tablisa = new HashMap<>();
        for (String setir : Files.readAllLines(gor_ýol.resolve("엑스기계함수.tsv"))) { String[] goşa_bol_baha = setir.split("\t"); if (goşa_bol_baha[0].equals(niýet)) kompýuter_tablisa.put(goşa_bol_baha[1] + goşa_bol_baha[2],goşa_bol_baha[3]); }
        int 자리 = girizmeklik_utuk.lastIndexOf('.'); if (자리 < 0) throw new Terjime_säwlik("girizmeklik_utuk 지정 Hata");
        String eýe_baha = girizmeklik_utuk.substring(0,자리).replace('.','/'), usul_girizmeklik_at = girizmeklik_utuk.substring(자리 + 1); usul_Salgylanma girizmeklik_utuk_baha = null;
        for (String 서술 : Arrays.asList("()I","()V")) { usul_Salgylanma Salgylanma = new usul_Salgylanma(eýe_baha,usul_girizmeklik_at,서술); if (함수들.containsKey(Salgylanma)) { if (girizmeklik_utuk_baha != null) throw new Terjime_säwlik("겹친 girizmeklik_utuk"); girizmeklik_utuk_baha = Salgylanma; } }
        if (girizmeklik_utuk_baha == null || (함수들.get(girizmeklik_utuk_baha).ygtyýarlylyk_girizmeklik & 0x100) != 0) throw new Terjime_säwlik("girizmeklik_utuk_baha FUNCTION_baha format_baha Hata");
        List<String> setir = new ArrayList<>(); setir.add(".code32");
        for (klas_maglumat maglumat : 클래스들.values()) {
            String ýagdaý_baha = nyşan("state",maglumat.Ad), ulanyşa_taýýarla = nyşan("init",maglumat.Ad);
            Collections.addAll(setir,".bss",".balign 4",ýagdaý_baha + ": .long 0",".text",ulanyşa_taýýarla + ":","cmpl $0, " + ýagdaý_baha,"jne " + ulanyşa_taýýarla + "_done","movl $1, " + ýagdaý_baha);
            usul_Salgylanma 초기화참조 = new usul_Salgylanma(maglumat.Ad,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) setir.add("call " + nyşan("method",초기화참조.부분들()));
            Collections.addAll(setir,"movl $2, " + ýagdaý_baha,ulanyşa_taýýarla + "_done:","ret");
            for (agza_maglumat meýdan_baha : maglumat.meýdan_baha) {
                byte[] hemişelik_baha = meýdan_baha.alamat_baha.get("ConstantValue"); String baha = hemişelik_baha == null ? "0" : 엑스상수(maglumat,new maglumat_okyjy(hemişelik_baha).두바이트());
                Collections.addAll(setir,".data",".balign 4",nyşan("field",maglumat.Ad,meýdan_baha.Ad,meýdan_baha.서술) + ": .long " + baha);
            }
            for (agza_maglumat FUNCTION_baha : maglumat.FUNCTION_baha) if (!FUNCTION_baha.Ad.equals("<init>")) setir.add(엑스함수본문(new usul_Salgylanma(maglumat.Ad,FUNCTION_baha.Ad,FUNCTION_baha.서술),FUNCTION_baha,kompýuter_tablisa,niýet));
        }
        Collections.addAll(setir,".text",".globl java_entry","java_entry:","call " + nyşan("init",girizmeklik_utuk_baha.eýe_baha),"call " + nyşan("method",girizmeklik_utuk_baha.부분들()));
        if (girizmeklik_utuk_baha.서술.equals("()V")) setir.add("xorl %eax, %eax"); setir.add("ret");
        for (String 지정 : 내보냄) {
            int bölüji_baha_d8ba4873 = 지정.indexOf('='); if (bölüji_baha_d8ba4873 < 1) throw new Terjime_säwlik("내보내기 지정 Hata");
            String 외부 = 지정.substring(0,bölüji_baha_d8ba4873), FUNCTION_baha = 지정.substring(bölüji_baha_d8ba4873 + 1); int 나눔 = FUNCTION_baha.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Terjime_säwlik("내보내기 nyşan Hata");
            String klas_baha = FUNCTION_baha.substring(0,나눔).replace('.','/'), Ad = FUNCTION_baha.substring(나눔 + 1); usul_Salgylanma saýlama_baha = null;
            for (usul_Salgylanma Salgylanma : 함수들.keySet()) if (Salgylanma.eýe_baha.equals(klas_baha) && Salgylanma.Ad.equals(Ad)) { if (saýlama_baha != null) throw new Terjime_säwlik("겹친 내보내기 niýet"); saýlama_baha = Salgylanma; }
            if (saýlama_baha == null) throw new Terjime_säwlik("내보낼 함수가 없음");
            Collections.addAll(setir,".text",".globl " + 외부,외부 + ":","call " + nyşan("init",saýlama_baha.eýe_baha),"jmp " + nyşan("method",saýlama_baha.부분들()));
        }
        setir.add(".section .rodata");
        for (Map.Entry<String,String> girizmeklik_baha : 문자열들.entrySet()) {
            Collections.addAll(setir,".balign 4",girizmeklik_baha.getValue() + ":",".long " + girizmeklik_baha.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char sapak_baha : girizmeklik_baha.getKey().toCharArray()) 단위들.add(Integer.toString(sapak_baha)); if (!단위들.isEmpty()) setir.add(".long " + String.join(",",단위들));
        }
        setir.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",setir) + "\n";
    }
    static void ýerine_ýetir_gural(List<String> buýruk) throws Exception {
        if (new ProcessBuilder(buýruk).inheritIO().start().waitFor() != 0) throw new Terjime_säwlik("düz_gor Hata: " + buýruk.get(0));
    }
    static String maglumat_setir(String Metin) { return "\"" + Metin.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String niýet, String girizmeklik_utuk, List<String> 내보냄, Path 출력, Path gor_baha) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), klas_ýol = 임시.resolve("classes"); Files.createDirectory(klas_ýol);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",klas_ýol.toString(),"-sourcepath",klas_ýol.toString(),"-d",klas_ýol.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Terjime_säwlik("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Terjime_säwlik(".java 또는 .class만 Goldaw_baha");
            }
            if (원문수 > 0) ýerine_ýetir_gural(자바명령);
            try (java.util.stream.Stream<Path> ýol_Sanaw = Files.walk(klas_ýol)) { ýol_Sanaw.filter(Ýol -> Ýol.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,niýet.equals("user") ? "user" : "kernel",262144,gor_baha);
            String 조립 = 변환.엑스조립본(girizmeklik_utuk,내보냄,niýet); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = gor_baha.getParent();
            ýerine_ýetir_gural(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            ýerine_ýetir_gural(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("umumy_dil_işlediş_gurşawy_Goldaw.s").toString()));
            List<String> Birikme = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (niýet.equals("kernel")) Birikme.add("-r");
            else {
                ýerine_ýetir_gural(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(niýet.equals("user") ? "başlat_ulanyjy_programma.s" : "리눅스시작.s").toString()));
                Collections.addAll(Birikme,"-e","_start",임시.resolve("start.o").toString());
                if (niýet.equals("user")) Collections.addAll(Birikme,"-T",도구위치.resolve("ulanyjy_Bag_Ýerleşiş.ld").toString());
            }
            Collections.addAll(Birikme,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); ýerine_ýetir_gural(Birikme);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path neşir_et_baha = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),neşir_et_baha,StandardCopyOption.REPLACE_EXISTING); Files.move(neşir_et_baha,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(neşir_et_baha); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(niýet.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> nyşan_maglumat = new ArrayList<>(), maglumatlar_gory = new ArrayList<>();
            for (usul_Salgylanma Salgylanma : 변환.함수들.keySet()) nyşan_maglumat.add(maglumat_setir(nyşan("method",Salgylanma.부분들())) + ":" + maglumat_setir(Salgylanma.eýe_baha + "." + Salgylanma.Ad + Salgylanma.서술));
            for (Path 입력 : 입력들) {
                byte[] heş_kody_faýl = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Metin = new StringBuilder(); for (byte baha : heş_kody_faýl) Metin.append(String.format(Locale.ROOT,"%02x",baha & 255));
                maglumatlar_gory.add(maglumat_setir(입력.toAbsolutePath().toString()) + ":" + maglumat_setir(Metin.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + maglumat_setir(niýet) + ",\"entry\":" + maglumat_setir(girizmeklik_utuk) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",nyşan_maglumat) + "},\"sources\":{" + String.join(",",maglumatlar_gory) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> ýol_Sanaw = Files.walk(임시)) { for (Path Ýol : (Iterable<Path>)ýol_Sanaw.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Ýol); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String girizmeklik_utuk = null, niýet = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> ýol_Sanaw = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String baha = 인수[순번];
                switch (baha) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry klas_baha.FUNCTION_baha -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export nyşan=klas_baha.FUNCTION_baha] 클래스파일 또는 Java원문"); return;
                    case "--entry": girizmeklik_utuk = 인수[++순번]; break;
                    case "--profile": niýet = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (baha.startsWith("-")) throw new Terjime_säwlik("알 수 없는 옵션: " + baha); ýol_Sanaw.add(Paths.get(baha));
                }
            }
            if (girizmeklik_utuk == null || 출력경로 == null || ýol_Sanaw.isEmpty()) throw new Terjime_säwlik("--entry, -o, klas_baha 파일이 필요합니다");
            Path gor_baha = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Terjime_säwlik("알 수 없는 ýerine_ýetir_buýruk niýet");
                엑스번역(ýol_Sanaw,엑스대상,girizmeklik_utuk,내보냄,출력경로,gor_baha); return;
            }
            String Çeşme = new 기계어미리번역(ýol_Sanaw, niýet, 낱말수, gor_baha).생성(girizmeklik_utuk, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, Çeşme, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Hata) { System.err.println("düz_gor Hata: " + Hata.getMessage()); System.exit(1); }
    }
}
