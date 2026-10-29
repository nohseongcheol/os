// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Dosbarth_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. lletya JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Cyfieithu_gwall extends RuntimeException {
        Cyfieithu_gwall(String 설명) { super(설명); }
    }
    static final class data_darllenwr {
        final byte[] data;
        int safle;
        data_darllenwr(byte[] 입력자료) { data = 입력자료; }
        byte[] Darllen(int hyd_VALUE) {
            if (hyd_VALUE < 0 || hyd_VALUE > data.length - safle) throw new Cyfieithu_gwall("잘린 Dosbarth_VALUE 또는 Gorchymyn data");
            byte[] mesur = Arrays.copyOfRange(data, safle, safle + hyd_VALUE); safle += hyd_VALUE; return mesur;
        }
        int 한바이트() { if (safle >= data.length) throw new Cyfieithu_gwall("잘린 Gorchymyn data"); return data[safle++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class aelod_data {
        final int mynediad_cofnod;
        final String Enw, 서술;
        final Map<String, byte[]> priodoledd_VALUE;
        aelod_data(int mynediad_VALUE, String enw_VALUE, String 서술값, Map<String, byte[]> priodoledd_data) {
            mynediad_cofnod = mynediad_VALUE; Enw = enw_VALUE; 서술 = 서술값; priodoledd_VALUE = priodoledd_data;
        }
    }
    static final class dull_cyfeiriad implements Comparable<dull_cyfeiriad> {
        final String perchennog_VALUE, Enw, 서술;
        dull_cyfeiriad(String 소유값, String enw_VALUE, String 서술값) { perchennog_VALUE = 소유값; Enw = enw_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{perchennog_VALUE, Enw, 서술}; }
        public int compareTo(dull_cyfeiriad cymar_VALUE) {
            int 비교값 = perchennog_VALUE.compareTo(cymar_VALUE.perchennog_VALUE);
            if (비교값 == 0) 비교값 = Enw.compareTo(cymar_VALUE.Enw);
            return 비교값 == 0 ? 서술.compareTo(cymar_VALUE.서술) : 비교값;
        }
        public boolean equals(Object cymar_VALUE) { return cymar_VALUE instanceof dull_cyfeiriad && compareTo((dull_cyfeiriad) cymar_VALUE) == 0; }
        public int hashCode() { return Objects.hash(perchennog_VALUE, Enw, 서술); }
    }
    static final class Dosbarth_data {
        final int[] 상수종류;
        final Object[] cysonyn_data;
        final String Enw;
        final List<aelod_data> maes_VALUE, SWYDDOGAETH_VALUE;
        Dosbarth_data(Path LLWYBR) throws IOException {
            data_darllenwr darllenwr_VALUE = new data_darllenwr(Files.readAllBytes(LLWYBR));
            if (darllenwr_VALUE.네바이트() != 0xcafebabe) throw new Cyfieithu_gwall("Java Dosbarth_VALUE 표식이 아님");
            darllenwr_VALUE.Darllen(4);
            int eitem_COUNT = darllenwr_VALUE.두바이트(); 상수종류 = new int[eitem_COUNT]; cysonyn_data = new Object[eitem_COUNT];
            for (int 순번 = 1; 순번 < eitem_COUNT; 순번++) {
                int 종류 = darllenwr_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int hyd_VALUE = darllenwr_VALUE.두바이트();
                        byte[] nod_byffer = darllenwr_VALUE.Darllen(hyd_VALUE), 길이붙인자료 = new byte[hyd_VALUE + 2];
                        길이붙인자료[0] = (byte)(hyd_VALUE >> 8); 길이붙인자료[1] = (byte)hyd_VALUE;
                        System.arraycopy(nod_byffer, 0, 길이붙인자료, 2, hyd_VALUE);
                        cysonyn_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: cysonyn_data[순번] = darllenwr_VALUE.네바이트(); break;
                    case 4: darllenwr_VALUE.Darllen(4); break;
                    case 5: case 6: darllenwr_VALUE.Darllen(8); 순번++; break;
                    case 7: case 8: case 16: cysonyn_data[순번] = darllenwr_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        cysonyn_data[순번] = new int[]{darllenwr_VALUE.두바이트(), darllenwr_VALUE.두바이트()}; break;
                    case 15: cysonyn_data[순번] = new int[]{darllenwr_VALUE.한바이트(), darllenwr_VALUE.두바이트()}; break;
                    default: throw new Cyfieithu_gwall("지원하지 않는 cysonyn_VALUE 종류: " + 종류);
                }
            }
            darllenwr_VALUE.두바이트(); Enw = Dosbarth_enw(darllenwr_VALUE.두바이트());
            if (!Dosbarth_enw(darllenwr_VALUE.두바이트()).equals("java/lang/Object") || darllenwr_VALUE.두바이트() != 0)
                throw new Cyfieithu_gwall(Enw + ": 상속 및 인터페이스 미지원");
            maes_VALUE = 멤버읽기(darllenwr_VALUE); SWYDDOGAETH_VALUE = 멤버읽기(darllenwr_VALUE); 속성읽기(darllenwr_VALUE);
            if (darllenwr_VALUE.safle != darllenwr_VALUE.data.length) throw new Cyfieithu_gwall("Dosbarth_VALUE 뒤에 남은 data");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Cyfieithu_gwall("문자 cysonyn_VALUE INDEX Gwall");
            return (String) cysonyn_data[INDEX];
        }
        String Dosbarth_enw(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Cyfieithu_gwall("Dosbarth_VALUE cyfeiriad Gwall");
            return 문자((Integer)cysonyn_data[INDEX]);
        }
        dull_cyfeiriad cyfeiriad(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Cyfieithu_gwall("멤버 cyfeiriad Gwall");
            int[] pâr_VALUE = (int[])cysonyn_data[INDEX], enw_pâr = (int[])cysonyn_data[pâr_VALUE[1]];
            return new dull_cyfeiriad(Dosbarth_enw(pâr_VALUE[0]), 문자(enw_pâr[0]), 문자(enw_pâr[1]));
        }
        Map<String, byte[]> 속성읽기(data_darllenwr darllenwr_VALUE) {
            Map<String, byte[]> mesur = new LinkedHashMap<>();
            int eitem_COUNT = darllenwr_VALUE.두바이트();
            for (int 순번 = 0; 순번 < eitem_COUNT; 순번++) {
                String priodoledd_enw = 문자(darllenwr_VALUE.두바이트()); byte[] VALUE = darllenwr_VALUE.Darllen(darllenwr_VALUE.네바이트());
                if (mesur.put(priodoledd_enw, VALUE) != null) throw new Cyfieithu_gwall("겹친 priodoledd_VALUE: " + priodoledd_enw);
            }
            return mesur;
        }
        List<aelod_data> 멤버읽기(data_darllenwr darllenwr_VALUE) {
            List<aelod_data> mesur = new ArrayList<>(); int eitem_COUNT = darllenwr_VALUE.두바이트();
            for (int 순번 = 0; 순번 < eitem_COUNT; 순번++) {
                int mynediad_cofnod = darllenwr_VALUE.두바이트(); String dull_cofnod_enw = 문자(darllenwr_VALUE.두바이트()), 서술 = 문자(darllenwr_VALUE.두바이트());
                mesur.add(new aelod_data(mynediad_cofnod, dull_cofnod_enw, 서술, 속성읽기(darllenwr_VALUE)));
            }
            return mesur;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String return_mesur;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Cyfieithu_gwall("SWYDDOGAETH_VALUE 서술 Gwall: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Cyfieithu_gwall("SWYDDOGAETH_VALUE 서술 Gwall: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Cyfieithu_gwall("SWYDDOGAETH_VALUE 서술 Gwall: " + 서술);
            return_mesur = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> mesur = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int safle = 0; safle < 서술.length();) {
            String dewisiad_VALUE = null;
            for (String fformat_VALUE : 허용형식) if (서술.startsWith(fformat_VALUE, safle)) { dewisiad_VALUE = fformat_VALUE; break; }
            if (dewisiad_VALUE == null) throw new Cyfieithu_gwall("지원하지 않는 math_data: " + 서술);
            mesur.add(dewisiad_VALUE); safle += dewisiad_VALUE.length();
        }
        return mesur;
    }
    static String symbol(String 종류, String... 부분들) {
        try {
            byte[] hash_ffeil = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Testun = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Testun.append(String.format(Locale.ROOT, "%02x", hash_ffeil[순번] & 255));
            return Testun.toString();
        } catch (Exception Gwall) { throw new Cyfieithu_gwall(Gwall.toString()); }
    }
    final Map<String, Dosbarth_data> 클래스들 = new TreeMap<>();
    final Map<dull_cyfeiriad, aelod_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, peiriant_Dosbarth;
    final int 동적기억낱말수;
    final Path adnodd_llwybr;
    기계어미리번역(List<Path> llwybr_Rhestr, String targed, int 낱말수, Path adnodd_VALUE) throws IOException {
        if ((!targed.equals("kernel") && !targed.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Cyfieithu_gwall("Gweithredu_gorchymyn targed 또는 Cof_VALUE 공간 Maint Gwall");
        실행대상 = targed; 동적기억낱말수 = 낱말수; adnodd_llwybr = adnodd_VALUE;
        // 이 이름도 국가별 ffynhonnell_coeden cynhyrchu 시 해당 언어로 옮긴다.
        peiriant_Dosbarth = targed.equals("kernel") ? "bwrdd" : "defnyddiwr";
        for (String llinell : Files.readAllLines(adnodd_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = llinell.split("\t", -1);
            if (부분들.length != 4) throw new Cyfieithu_gwall("peiriant SWYDDOGAETH_VALUE data Gwall");
            if (부분들[0].equals(targed)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path LLWYBR : llwybr_Rhestr) {
            Dosbarth_data data = new Dosbarth_data(LLWYBR);
            if (클래스들.put(data.Enw, data) != null) throw new Cyfieithu_gwall("중복 Dosbarth_VALUE: " + data.Enw);
            for (aelod_data maes_VALUE : data.maes_VALUE) {
                if ((maes_VALUE.mynediad_cofnod & 8) == 0 || 형식읽기(maes_VALUE.서술).equals(Collections.singletonList("V"))) throw new Cyfieithu_gwall("statig_VALUE 필드만 Cymorth_VALUE");
                if (필드들.put(new dull_cyfeiriad(data.Enw, maes_VALUE.Enw, maes_VALUE.서술), maes_VALUE) != null) throw new Cyfieithu_gwall("중복 maes_VALUE");
            }
            for (aelod_data SWYDDOGAETH_VALUE : data.SWYDDOGAETH_VALUE) {
                if (SWYDDOGAETH_VALUE.Enw.equals("<init>")) continue;
                if ((SWYDDOGAETH_VALUE.mynediad_cofnod & 8) == 0 || (SWYDDOGAETH_VALUE.mynediad_cofnod & (0x20 | 0x400)) != 0) throw new Cyfieithu_gwall("statig_VALUE 비동기화 함수만 Cymorth_VALUE");
                new 함수형식(SWYDDOGAETH_VALUE.서술);
                if (함수들.put(new dull_cyfeiriad(data.Enw, SWYDDOGAETH_VALUE.Enw, SWYDDOGAETH_VALUE.서술), SWYDDOGAETH_VALUE) != null) throw new Cyfieithu_gwall("중복 SWYDDOGAETH_VALUE");
            }
        }
    }
    String testun_symbol(String Testun) { return 문자열들.computeIfAbsent(Testun, VALUE -> "j_text_" + 문자열들.size()); }
    String cysonyn_mynegiad(Dosbarth_data data, int INDEX) {
        if (INDEX < 1 || INDEX >= data.상수종류.length) throw new Cyfieithu_gwall("cysonyn_VALUE INDEX clip Gwall");
        if (data.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + data.cysonyn_data[INDEX] + ")";
        if (data.상수종류[INDEX] == 8) return "(word)" + testun_symbol(data.문자((Integer)data.cysonyn_data[INDEX]));
        throw new Cyfieithu_gwall("정수와 testun_VALUE 상수만 Cymorth_VALUE");
    }
    String 함수원형(dull_cyfeiriad cyfeiriad) {
        List<String> 인수들 = new ArrayList<>(); int eitem_COUNT = new 함수형식(cyfeiriad.서술).인수.size();
        for (int 순번 = 0; 순번 < eitem_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symbol("method", cyfeiriad.부분들()) + "(" + (eitem_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void gwirio_lleol(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Cyfieithu_gwall("lleol_cwmpas 변수 INDEX clip Gwall"); }
    void 분기넣기(List<String> Allbwn, Set<Integer> cangen_Rhestr, int safle, int 이동량, String cyflwr) {
        int cyrchfan_VALUE = safle + 이동량; cangen_Rhestr.add(cyrchfan_VALUE);
        Allbwn.add((cyflwr == null ? "" : "if (" + cyflwr + ") ") + "goto b" + cyrchfan_VALUE + ";");
    }
    String dull_corff(dull_cyfeiriad SWYDDOGAETH_VALUE, aelod_data data) {
        byte[] corff_data = data.priodoledd_VALUE.get("Code"); if (corff_data == null) throw new Cyfieithu_gwall("SWYDDOGAETH_VALUE 몸체가 없음: " + SWYDDOGAETH_VALUE.Enw);
        data_darllenwr darllenwr_VALUE = new data_darllenwr(corff_data); int 쌓임깊이 = darllenwr_VALUE.두바이트(), 지역변수수 = darllenwr_VALUE.두바이트();
        data_darllenwr gorchymyn_data = new data_darllenwr(darllenwr_VALUE.Darllen(darllenwr_VALUE.네바이트()));
        if (darllenwr_VALUE.두바이트() != 0) throw new Cyfieithu_gwall("try/catch/finally 미지원");
        함수형식 fformat_VALUE = new 함수형식(SWYDDOGAETH_VALUE.서술); if (지역변수수 < fformat_VALUE.인수.size()) throw new Cyfieithu_gwall("매개변수보다 적은 lleol_cwmpas 변수");
        Dosbarth_data Dosbarth_VALUE = 클래스들.get(SWYDDOGAETH_VALUE.perchennog_VALUE);
        List<String> Allbwn = new ArrayList<>(); Allbwn.add(함수원형(SWYDDOGAETH_VALUE) + " {");
        Allbwn.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < fformat_VALUE.인수.size(); 순번++) Allbwn.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), cangen_Rhestr = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (gorchymyn_data.safle < gorchymyn_data.data.length) {
            int safle = gorchymyn_data.safle, Gorchymyn = gorchymyn_data.한바이트(); 경계들.add(safle); Allbwn.add("b" + safle + ":;");
            if (Gorchymyn == 0) continue;
            if (Gorchymyn == 1) Allbwn.add("PUSH(0);");
            else if (Gorchymyn >= 2 && Gorchymyn <= 8) Allbwn.add("PUSH((uint32_t)(" + (Gorchymyn - 3) + "));");
            else if (Gorchymyn == 16 || Gorchymyn == 17) Allbwn.add("PUSH((uint32_t)(" + (Gorchymyn == 16 ? gorchymyn_data.부호한바이트() : gorchymyn_data.부호두바이트()) + "));");
            else if (Gorchymyn == 18 || Gorchymyn == 19) Allbwn.add("PUSH(" + cysonyn_mynegiad(Dosbarth_VALUE, Gorchymyn == 18 ? gorchymyn_data.한바이트() : gorchymyn_data.두바이트()) + ");");
            else if (Gorchymyn == 21 || Gorchymyn == 25 || (Gorchymyn >= 26 && Gorchymyn <= 29) || (Gorchymyn >= 42 && Gorchymyn <= 45)) {
                int INDEX = Gorchymyn == 21 || Gorchymyn == 25 ? gorchymyn_data.한바이트() : Gorchymyn - (Gorchymyn <= 29 ? 26 : 42);
                gwirio_lleol(INDEX, 지역변수수); Allbwn.add("PUSH(l[" + INDEX + "]);");
            } else if (Gorchymyn == 54 || Gorchymyn == 58 || (Gorchymyn >= 59 && Gorchymyn <= 62) || (Gorchymyn >= 75 && Gorchymyn <= 78)) {
                int INDEX = Gorchymyn == 54 || Gorchymyn == 58 ? gorchymyn_data.한바이트() : Gorchymyn - (Gorchymyn <= 62 ? 59 : 75);
                gwirio_lleol(INDEX, 지역변수수); Allbwn.add("l[" + INDEX + "] = POP();");
            } else if (Gorchymyn == 46) Allbwn.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Gorchymyn == 79) Allbwn.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Gorchymyn == 87 || Gorchymyn == 88) Allbwn.add(Gorchymyn == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Gorchymyn >= 89 && Gorchymyn <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] trefn_Rhestr = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Gorchymyn - 89]; 순번++) Allbwn.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : trefn_Rhestr[Gorchymyn - 89].toCharArray()) Allbwn.add("PUSH(" + VALUE + ");");
            } else if (Gorchymyn == 96 || Gorchymyn == 100 || Gorchymyn == 104 || Gorchymyn == 126 || Gorchymyn == 128 || Gorchymyn == 130) {
                String gweithrediad_VALUE = Gorchymyn == 96 ? "+" : Gorchymyn == 100 ? "-" : Gorchymyn == 104 ? "*" : Gorchymyn == 126 ? "&" : Gorchymyn == 128 ? "|" : "^";
                Allbwn.add("b = POP(); a = POP(); PUSH((uint32_t)a " + gweithrediad_VALUE + " (uint32_t)b);");
            } else if (Gorchymyn == 108 || Gorchymyn == 112) Allbwn.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Gorchymyn == 112 ? 1 : 0) + "));");
            else if (Gorchymyn == 116) Allbwn.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Gorchymyn == 120 || Gorchymyn == 122 || Gorchymyn == 124) {
                Allbwn.add("b = POP(); a = POP();"); Allbwn.add("PUSH(" + (Gorchymyn == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Gorchymyn == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Gorchymyn == 132) {
                int INDEX = gorchymyn_data.한바이트(), 증가량 = gorchymyn_data.부호한바이트(); gwirio_lleol(INDEX, 지역변수수);
                Allbwn.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Gorchymyn >= 145 && Gorchymyn <= 147) Allbwn.add("a = POP(); PUSH((uint32_t)(" + (Gorchymyn == 145 ? "int8_t" : Gorchymyn == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Gorchymyn >= 153 && Gorchymyn <= 158) {
                Allbwn.add("a = POP();"); 분기넣기(Allbwn, cangen_Rhestr, safle, gorchymyn_data.부호두바이트(), "(int32_t)a " + 비교들[Gorchymyn - 153] + " 0");
            } else if (Gorchymyn >= 159 && Gorchymyn <= 166) {
                Allbwn.add("b = POP(); a = POP();"); 분기넣기(Allbwn, cangen_Rhestr, safle, gorchymyn_data.부호두바이트(), Gorchymyn >= 165 ? "a " + 비교들[Gorchymyn - 159] + " b" : "(int32_t)a " + 비교들[Gorchymyn - 159] + " (int32_t)b");
            } else if (Gorchymyn == 167 || Gorchymyn == 200) 분기넣기(Allbwn, cangen_Rhestr, safle, Gorchymyn == 167 ? gorchymyn_data.부호두바이트() : gorchymyn_data.네바이트(), null);
            else if (Gorchymyn == 170 || Gorchymyn == 171) {
                while (gorchymyn_data.safle % 4 != 0) gorchymyn_data.한바이트();
                int gwerth_diofyn = gorchymyn_data.네바이트(); Allbwn.add("a = POP();");
                if (Gorchymyn == 170) {
                    int 아래 = gorchymyn_data.네바이트(), 위 = gorchymyn_data.네바이트(); long eitem_COUNT = (long)위 - 아래 + 1;
                    if (eitem_COUNT < 1 || eitem_COUNT > (gorchymyn_data.data.length - gorchymyn_data.safle) / 4) throw new Cyfieithu_gwall("switch clip Gwall");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Allbwn, cangen_Rhestr, safle, gorchymyn_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int eitem_COUNT = gorchymyn_data.네바이트(), 앞값 = 0;
                    if (eitem_COUNT < 0 || eitem_COUNT > (gorchymyn_data.data.length - gorchymyn_data.safle) / 8) throw new Cyfieithu_gwall("switch Maint Gwall");
                    for (int 순번 = 0; 순번 < eitem_COUNT; 순번++) {
                        int VALUE = gorchymyn_data.네바이트(); if (순번 > 0 && VALUE <= 앞값) throw new Cyfieithu_gwall("switch trefn_VALUE Gwall"); 앞값 = VALUE;
                        분기넣기(Allbwn, cangen_Rhestr, safle, gorchymyn_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Allbwn, cangen_Rhestr, safle, gwerth_diofyn, null);
            } else if (Gorchymyn == 172 || Gorchymyn == 176 || Gorchymyn == 177) Allbwn.add("return " + (Gorchymyn == 177 ? "0" : "POP()") + ";");
            else if (Gorchymyn == 178 || Gorchymyn == 179) {
                dull_cyfeiriad cyfeiriad = Dosbarth_VALUE.cyfeiriad(gorchymyn_data.두바이트()); if (!필드들.containsKey(cyfeiriad)) throw new Cyfieithu_gwall("알 수 없는 maes_VALUE");
                Allbwn.add(symbol("init", cyfeiriad.perchennog_VALUE) + "();"); String maes_VALUE = symbol("field", cyfeiriad.부분들());
                Allbwn.add(Gorchymyn == 178 ? "PUSH(" + maes_VALUE + ");" : maes_VALUE + " = POP();");
            } else if (Gorchymyn == 184) {
                dull_cyfeiriad cyfeiriad = Dosbarth_VALUE.cyfeiriad(gorchymyn_data.두바이트()); if (!함수들.containsKey(cyfeiriad)) throw new Cyfieithu_gwall("알 수 없는 SWYDDOGAETH_VALUE");
                함수형식 호출형식 = new 함수형식(cyfeiriad.서술); int eitem_COUNT = 호출형식.인수.size();
                Allbwn.add(symbol("init", cyfeiriad.perchennog_VALUE) + "();"); Allbwn.add("if(sp < " + eitem_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + eitem_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < eitem_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Allbwn.add("a = " + symbol("method", cyfeiriad.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.return_mesur.equals("V")) Allbwn.add("PUSH(a);");
            } else if (Gorchymyn == 182) {
                dull_cyfeiriad cyfeiriad = Dosbarth_VALUE.cyfeiriad(gorchymyn_data.두바이트());
                if (cyfeiriad.equals(new dull_cyfeiriad("java/lang/String", "length", "()I"))) Allbwn.add("a = POP(); PUSH(length(a));");
                else if (cyfeiriad.equals(new dull_cyfeiriad("java/lang/String", "charAt", "(I)C"))) Allbwn.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Cyfieithu_gwall("가상 SWYDDOGAETH_VALUE 호출 미지원");
            } else if (Gorchymyn == 188) {
                if (gorchymyn_data.한바이트() != 10) throw new Cyfieithu_gwall("new int[]만 Cymorth_VALUE"); Allbwn.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Gorchymyn == 190) Allbwn.add("a = POP(); PUSH(length(a));");
            else if (Gorchymyn == 196) {
                int estyniad_VALUE = gorchymyn_data.한바이트(), INDEX = gorchymyn_data.두바이트(); gwirio_lleol(INDEX, 지역변수수);
                if (estyniad_VALUE == 21 || estyniad_VALUE == 25) Allbwn.add("PUSH(l[" + INDEX + "]);");
                else if (estyniad_VALUE == 54 || estyniad_VALUE == 58) Allbwn.add("l[" + INDEX + "] = POP();");
                else if (estyniad_VALUE == 132) Allbwn.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + gorchymyn_data.부호두바이트() + ");");
                else throw new Cyfieithu_gwall("미지원 wide Gorchymyn");
            } else if (Gorchymyn == 198 || Gorchymyn == 199) {
                Allbwn.add("a = POP();"); 분기넣기(Allbwn, cangen_Rhestr, safle, gorchymyn_data.부호두바이트(), "a " + (Gorchymyn == 198 ? "==" : "!=") + " 0");
            } else throw new Cyfieithu_gwall(SWYDDOGAETH_VALUE.perchennog_VALUE + "." + SWYDDOGAETH_VALUE.Enw + ", beit_VALUE " + safle + ": 미지원 Gorchymyn " + Gorchymyn);
        }
        if (!경계들.containsAll(cangen_Rhestr)) throw new Cyfieithu_gwall("Gorchymyn 경계가 아닌 곳으로 cangen");
        Allbwn.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Allbwn);
    }
    String allgludo_dull(String Dolen_symbol, String targed, boolean 진입점여부) {
        int safle_INDEX = targed.lastIndexOf('.'); if (safle_INDEX < 0 || !Dolen_symbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Cyfieithu_gwall("내보내기 지정 Gwall");
        String perchennog_VALUE = targed.substring(0, safle_INDEX).replace('.', '/'), Enw = targed.substring(safle_INDEX + 1); dull_cyfeiriad dewisiad_VALUE = null;
        for (dull_cyfeiriad cyfeiriad : 함수들.keySet()) if (cyfeiriad.perchennog_VALUE.equals(perchennog_VALUE) && cyfeiriad.Enw.equals(Enw)) {
            if (dewisiad_VALUE != null) throw new Cyfieithu_gwall("겹친 내보내기 targed"); dewisiad_VALUE = cyfeiriad;
        }
        if (dewisiad_VALUE == null || (함수들.get(dewisiad_VALUE).mynediad_cofnod & 0x100) != 0) throw new Cyfieithu_gwall("내보낼 함수가 없음 또는 native SWYDDOGAETH_VALUE");
        함수형식 fformat_VALUE = new 함수형식(dewisiad_VALUE.서술);
        if ((진입점여부 && !fformat_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(fformat_VALUE.return_mesur)) throw new Cyfieithu_gwall("cofnod_p_VALUE 또는 C 경계 fformat_VALUE Gwall");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < fformat_VALUE.인수.size(); 순번++) {
            if (!fformat_VALUE.인수.get(순번).equals("I")) throw new Cyfieithu_gwall("C 경계는 int 인수만 Cymorth_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (fformat_VALUE.return_mesur.equals("V") ? "void " : "int32_t ") + Dolen_symbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symbol("init", dewisiad_VALUE.perchennog_VALUE) + "(); " + (fformat_VALUE.return_mesur.equals("V") ? "" : "return (int32_t)") + symbol("method", dewisiad_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String cynhyrchu(String cofnod_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<dull_cyfeiriad, aelod_data> cofnod_VALUE : 함수들.entrySet()) {
            dull_cyfeiriad cyfeiriad = cofnod_VALUE.getKey(); aelod_data data = cofnod_VALUE.getValue(); 선언들.add(함수원형(cyfeiriad) + ";");
            if ((data.mynediad_cofnod & 0x100) != 0) {
                String Cysylltu = 기계함수들.get(cyfeiriad.Enw + cyfeiriad.서술);
                if (!cyfeiriad.perchennog_VALUE.equals(peiriant_Dosbarth) || Cysylltu == null) throw new Cyfieithu_gwall("허용되지 않은 native SWYDDOGAETH_VALUE: " + cyfeiriad.Enw);
                int eitem_COUNT = new 함수형식(cyfeiriad.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < eitem_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Cysylltu + "(" + (eitem_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(eitem_COUNT, "word"))) + ");");
                몸체들.add(함수원형(cyfeiriad) + " { return " + Cysylltu + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(dull_corff(cyfeiriad, data));
        }
        for (Map.Entry<dull_cyfeiriad, aelod_data> cofnod_VALUE : 필드들.entrySet()) {
            dull_cyfeiriad cyfeiriad = cofnod_VALUE.getKey(); byte[] cysonyn_VALUE = cofnod_VALUE.getValue().priodoledd_VALUE.get("ConstantValue");
            String VALUE = cysonyn_VALUE == null ? "0" : cysonyn_mynegiad(클래스들.get(cyfeiriad.perchennog_VALUE), new data_darllenwr(cysonyn_VALUE).두바이트());
            필드선언들.add("static word " + symbol("field", cyfeiriad.부분들()) + " = " + VALUE + ";");
        }
        for (String Enw : 클래스들.keySet()) {
            String ymgychwyn = symbol("init", Enw), cyflwr_VALUE = symbol("state", Enw);
            선언들.add("static void " + ymgychwyn + "(void);"); 필드선언들.add("static unsigned " + cyflwr_VALUE + ";");
            dull_cyfeiriad cyfeiriad = new dull_cyfeiriad(Enw, "<clinit>", "()V");
            몸체들.add("static void " + ymgychwyn + "(void) { if(" + cyflwr_VALUE + ") return; " + cyflwr_VALUE + " = 1; " + (함수들.containsKey(cyfeiriad) ? symbol("method", cyfeiriad.부분들()) + "(); " : "") + cyflwr_VALUE + " = 2; }");
        }
        몸체들.add(allgludo_dull("java_entry", cofnod_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int safle_INDEX = 지정.indexOf('='); if (safle_INDEX < 1) throw new Cyfieithu_gwall("내보내기 지정 Gwall");
            String Enw = 지정.substring(0, safle_INDEX); 공개이름.add(Enw); 몸체들.add(allgludo_dull(Enw, 지정.substring(safle_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> cofnod_VALUE : 문자열들.entrySet()) {
            String Testun = cofnod_VALUE.getKey(); StringBuilder ARAE_VALUE = new StringBuilder("static const word " + cofnod_VALUE.getValue() + "[] = {" + Testun.length());
            for (int 순번 = 0; 순번 < Testun.length(); 순번++) ARAE_VALUE.append(", ").append((int)Testun.charAt(순번));
            문자열선언들.add(ARAE_VALUE.append("};").toString());
        }
        String Cymorth_VALUE = Files.readString(adnodd_llwybr.resolve("amser_rhedeg_iaith_gyffredin_Cymorth.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Cymorth_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String FFYNHONNELL, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> enw_tabl = new HashMap<>();
        for (String llinell : Files.readAllLines(adnodd_llwybr.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] pâr_VALUE = llinell.split("\t"); enw_tabl.put(pâr_VALUE[0], pâr_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(FFYNHONNELL); StringBuffer mesur = new StringBuffer();
        while (찾개.find()) {
            String Enw = 찾개.group(), 새이름 = Enw;
            if (!Enw.startsWith("//") && !Enw.startsWith("/*") && !Enw.startsWith("\"") && !Enw.startsWith("'") && !공개이름.contains(Enw)) {
                새이름 = enw_tabl.getOrDefault(Enw, Enw);
                if (Enw.matches("a[0-9]+")) 새이름 = "인수" + Enw.substring(1);
                if (Enw.matches("b[0-9]+")) 새이름 = "cangen" + Enw.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char nod_VALUE : 새이름.toCharArray()) 표기.append(nod_VALUE < 128 ? Character.toString(nod_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)nod_VALUE));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(mesur, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(mesur); return mesur.toString();
    }
    String X_86_dull_corff(dull_cyfeiriad SWYDDOGAETH_VALUE, aelod_data data, Map<String,String> peiriant_tabl, String targed) {
        String 표식 = symbol("method", SWYDDOGAETH_VALUE.부분들());
        List<String> llinell = new ArrayList<>();
        if ((data.mynediad_cofnod & 0x100) != 0) {
            String Cysylltu = peiriant_tabl.get(SWYDDOGAETH_VALUE.Enw + SWYDDOGAETH_VALUE.서술);
            if (!SWYDDOGAETH_VALUE.perchennog_VALUE.equals(targed.equals("kernel") ? "dyfais_VALUE" : "defnyddiwr") || Cysylltu == null) throw new Cyfieithu_gwall("허용되지 않은 native SWYDDOGAETH_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Cysylltu;
        }
        byte[] corff_y_testun = data.priodoledd_VALUE.get("Code"); if (corff_y_testun == null) throw new Cyfieithu_gwall("SWYDDOGAETH_VALUE 몸체가 없음");
        data_darllenwr darllenwr_VALUE = new data_darllenwr(corff_y_testun); darllenwr_VALUE.두바이트(); int lleol_COUNT = darllenwr_VALUE.두바이트();
        data_darllenwr gorchymyn_data = new data_darllenwr(darllenwr_VALUE.Darllen(darllenwr_VALUE.네바이트()));
        if (darllenwr_VALUE.두바이트() != 0) throw new Cyfieithu_gwall("try/catch/finally 미지원");
        함수형식 fformat_VALUE = new 함수형식(SWYDDOGAETH_VALUE.서술); if (lleol_COUNT < fformat_VALUE.인수.size()) throw new Cyfieithu_gwall("매개변수보다 적은 lleol_cwmpas 변수");
        Collections.addAll(llinell,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lleol_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < fformat_VALUE.인수.size(); 순번++) Collections.addAll(llinell,"movl " + (8 + 4 * (fformat_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Dosbarth_data Dosbarth_VALUE = 클래스들.get(SWYDDOGAETH_VALUE.perchennog_VALUE); Set<Integer> 경계들 = new HashSet<>(), cangen_Rhestr = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (gorchymyn_data.safle < gorchymyn_data.data.length) {
            int safle = gorchymyn_data.safle, Gorchymyn = gorchymyn_data.한바이트(); String safle_INDEX = 표식 + "_b" + safle;
            llinell.add(safle_INDEX + ":"); 경계들.add(safle);
            if (Gorchymyn == 0) llinell.add("nop");
            else if (Gorchymyn == 1) llinell.add("pushl $0");
            else if (Gorchymyn >= 2 && Gorchymyn <= 8) llinell.add("pushl $" + (Gorchymyn - 3));
            else if (Gorchymyn == 16 || Gorchymyn == 17) llinell.add("pushl $" + (Gorchymyn == 16 ? gorchymyn_data.부호한바이트() : gorchymyn_data.부호두바이트()));
            else if (Gorchymyn == 18 || Gorchymyn == 19) {
                int INDEX = Gorchymyn == 18 ? gorchymyn_data.한바이트() : gorchymyn_data.두바이트();
                llinell.add("pushl $" + X_86_cysonyn(Dosbarth_VALUE,INDEX));
            } else if (Gorchymyn == 21 || Gorchymyn == 25 || (Gorchymyn >= 26 && Gorchymyn <= 29) || (Gorchymyn >= 42 && Gorchymyn <= 45) || Gorchymyn == 54 || Gorchymyn == 58 || (Gorchymyn >= 59 && Gorchymyn <= 62) || (Gorchymyn >= 75 && Gorchymyn <= 78)) {
                boolean 읽음 = Gorchymyn < 54; int INDEX = Gorchymyn == 21 || Gorchymyn == 25 || Gorchymyn == 54 || Gorchymyn == 58 ? gorchymyn_data.한바이트() : Gorchymyn - (Gorchymyn <= 29 ? 26 : Gorchymyn <= 45 ? 42 : Gorchymyn <= 62 ? 59 : 75);
                gwirio_lleol(INDEX,lleol_COUNT); llinell.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Gorchymyn == 46) Collections.addAll(llinell,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Gorchymyn == 79) Collections.addAll(llinell,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Gorchymyn == 87 || Gorchymyn == 88) llinell.add("addl $" + (Gorchymyn == 87 ? 4 : 8) + ", %esp");
            else if (Gorchymyn >= 89 && Gorchymyn <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] trefn_Rhestr = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Gorchymyn - 89]; 순번++) llinell.add("popl " + 저장기들[순번]);
                for (int 순번 : trefn_Rhestr[Gorchymyn - 89]) llinell.add("pushl " + 저장기들[순번]);
            } else if (Gorchymyn == 96 || Gorchymyn == 100 || Gorchymyn == 104 || Gorchymyn == 126 || Gorchymyn == 128 || Gorchymyn == 130) {
                String gweithrediad_VALUE = Gorchymyn == 96 ? "addl" : Gorchymyn == 100 ? "subl" : Gorchymyn == 104 ? "imull" : Gorchymyn == 126 ? "andl" : Gorchymyn == 128 ? "orl" : "xorl";
                Collections.addAll(llinell,"popl %ecx","popl %eax",gweithrediad_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Gorchymyn == 108 || Gorchymyn == 112) Collections.addAll(llinell,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + safle_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + safle_INDEX + "_divide","xorl %edx, %edx","jmp " + safle_INDEX + "_done",safle_INDEX + "_divide:","cltd","idivl %ecx",safle_INDEX + "_done:","pushl " + (Gorchymyn == 108 ? "%eax" : "%edx"));
            else if (Gorchymyn == 116) llinell.add("negl (%esp)");
            else if (Gorchymyn == 120 || Gorchymyn == 122 || Gorchymyn == 124) Collections.addAll(llinell,"popl %ecx","popl %eax",(Gorchymyn == 120 ? "sall" : Gorchymyn == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Gorchymyn == 132) {
                int INDEX = gorchymyn_data.한바이트(), 증가 = gorchymyn_data.부호한바이트(); gwirio_lleol(INDEX,lleol_COUNT); llinell.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Gorchymyn >= 145 && Gorchymyn <= 147) Collections.addAll(llinell,"popl %eax",Gorchymyn == 145 ? "movsbl %al, %eax" : Gorchymyn == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Gorchymyn >= 153 && Gorchymyn <= 166) {
                if (Gorchymyn <= 158) Collections.addAll(llinell,"popl %eax","testl %eax, %eax");
                else Collections.addAll(llinell,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int cyrchfan_VALUE = safle + gorchymyn_data.부호두바이트(); cangen_Rhestr.add(cyrchfan_VALUE); llinell.add(비교들[Gorchymyn - (Gorchymyn <= 158 ? 153 : 159)] + " " + 표식 + "_b" + cyrchfan_VALUE);
            } else if (Gorchymyn == 167 || Gorchymyn == 200) {
                int cyrchfan_VALUE = safle + (Gorchymyn == 167 ? gorchymyn_data.부호두바이트() : gorchymyn_data.네바이트()); cangen_Rhestr.add(cyrchfan_VALUE); llinell.add("jmp " + 표식 + "_b" + cyrchfan_VALUE);
            } else if (Gorchymyn == 170 || Gorchymyn == 171) {
                while (gorchymyn_data.safle % 4 != 0) gorchymyn_data.한바이트();
                int gwerth_diofyn = safle + gorchymyn_data.네바이트(); cangen_Rhestr.add(gwerth_diofyn); llinell.add("popl %eax");
                int eitem_COUNT, 아래 = 0;
                if (Gorchymyn == 170) { 아래 = gorchymyn_data.네바이트(); int 위 = gorchymyn_data.네바이트(); long hyd_VALUE = (long)위 - 아래 + 1; if (hyd_VALUE < 1 || hyd_VALUE > (gorchymyn_data.data.length - gorchymyn_data.safle) / 4) throw new Cyfieithu_gwall("switch clip Gwall"); eitem_COUNT = (int)hyd_VALUE; }
                else { eitem_COUNT = gorchymyn_data.네바이트(); if (eitem_COUNT < 0 || eitem_COUNT > (gorchymyn_data.data.length - gorchymyn_data.safle) / 8) throw new Cyfieithu_gwall("switch Maint Gwall"); }
                for (int 순번 = 0; 순번 < eitem_COUNT; 순번++) {
                    int VALUE = Gorchymyn == 170 ? 아래 + 순번 : gorchymyn_data.네바이트(), cyrchfan_VALUE = safle + gorchymyn_data.네바이트(); cangen_Rhestr.add(cyrchfan_VALUE);
                    Collections.addAll(llinell,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + cyrchfan_VALUE);
                }
                llinell.add("jmp " + 표식 + "_b" + gwerth_diofyn);
            } else if (Gorchymyn == 172 || Gorchymyn == 176 || Gorchymyn == 177) {
                if (Gorchymyn != 177) llinell.add("popl %eax"); Collections.addAll(llinell,"leave","ret");
            } else if (Gorchymyn == 178 || Gorchymyn == 179) {
                dull_cyfeiriad cyfeiriad = Dosbarth_VALUE.cyfeiriad(gorchymyn_data.두바이트()); if (!필드들.containsKey(cyfeiriad)) throw new Cyfieithu_gwall("알 수 없는 maes_VALUE");
                Collections.addAll(llinell,"call " + symbol("init",cyfeiriad.perchennog_VALUE),(Gorchymyn == 178 ? "pushl " : "popl ") + symbol("field",cyfeiriad.부분들()));
            } else if (Gorchymyn == 184) {
                dull_cyfeiriad cyfeiriad = Dosbarth_VALUE.cyfeiriad(gorchymyn_data.두바이트()); if (!함수들.containsKey(cyfeiriad)) throw new Cyfieithu_gwall("알 수 없는 SWYDDOGAETH_VALUE");
                함수형식 호출형식 = new 함수형식(cyfeiriad.서술); Collections.addAll(llinell,"call " + symbol("init",cyfeiriad.perchennog_VALUE),"call " + symbol("method",cyfeiriad.부분들()));
                if (!호출형식.인수.isEmpty()) llinell.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.return_mesur.equals("V")) llinell.add("pushl %eax");
            } else if (Gorchymyn == 182) {
                dull_cyfeiriad cyfeiriad = Dosbarth_VALUE.cyfeiriad(gorchymyn_data.두바이트());
                if (cyfeiriad.equals(new dull_cyfeiriad("java/lang/String","length","()I"))) Collections.addAll(llinell,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (cyfeiriad.equals(new dull_cyfeiriad("java/lang/String","charAt","(I)C"))) Collections.addAll(llinell,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Cyfieithu_gwall("가상 SWYDDOGAETH_VALUE 호출 미지원");
            } else if (Gorchymyn == 188) {
                if (gorchymyn_data.한바이트() != 10) throw new Cyfieithu_gwall("new int[]만 Cymorth_VALUE"); Collections.addAll(llinell,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Gorchymyn == 190) Collections.addAll(llinell,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Gorchymyn == 196) {
                int estyniad_VALUE = gorchymyn_data.한바이트(), INDEX = gorchymyn_data.두바이트(); gwirio_lleol(INDEX,lleol_COUNT);
                if (estyniad_VALUE == 21 || estyniad_VALUE == 25 || estyniad_VALUE == 54 || estyniad_VALUE == 58) llinell.add((estyniad_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (estyniad_VALUE == 132) llinell.add("addl $" + gorchymyn_data.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Cyfieithu_gwall("wide Gorchymyn 미지원");
            } else if (Gorchymyn == 198 || Gorchymyn == 199) {
                int cyrchfan_VALUE = safle + gorchymyn_data.부호두바이트(); cangen_Rhestr.add(cyrchfan_VALUE); Collections.addAll(llinell,"popl %eax","testl %eax, %eax",(Gorchymyn == 198 ? "je " : "jne ") + 표식 + "_b" + cyrchfan_VALUE);
            } else throw new Cyfieithu_gwall("미지원 Gorchymyn: " + Gorchymyn);
        }
        if (!경계들.containsAll(cangen_Rhestr)) throw new Cyfieithu_gwall("Gorchymyn 경계가 아닌 곳으로 cangen");
        llinell.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",llinell);
    }
    String X_86_cysonyn(Dosbarth_data data, int INDEX) {
        if (data.상수종류[INDEX] == 3) return data.cysonyn_data[INDEX].toString();
        if (data.상수종류[INDEX] == 8) return testun_symbol(data.문자((Integer)data.cysonyn_data[INDEX]));
        throw new Cyfieithu_gwall("정수와 testun_VALUE 상수만 Cymorth_VALUE");
    }
    String 엑스조립본(String cofnod_p, List<String> 내보냄, String targed) throws IOException {
        Map<String,String> peiriant_tabl = new HashMap<>();
        for (String llinell : Files.readAllLines(adnodd_llwybr.resolve("엑스기계함수.tsv"))) { String[] pâr_VALUE = llinell.split("\t"); if (pâr_VALUE[0].equals(targed)) peiriant_tabl.put(pâr_VALUE[1] + pâr_VALUE[2],pâr_VALUE[3]); }
        int safle_INDEX = cofnod_p.lastIndexOf('.'); if (safle_INDEX < 0) throw new Cyfieithu_gwall("cofnod_p 지정 Gwall");
        String perchennog_VALUE = cofnod_p.substring(0,safle_INDEX).replace('.','/'), dull_cofnod_enw = cofnod_p.substring(safle_INDEX + 1); dull_cyfeiriad cofnod_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { dull_cyfeiriad cyfeiriad = new dull_cyfeiriad(perchennog_VALUE,dull_cofnod_enw,서술); if (함수들.containsKey(cyfeiriad)) { if (cofnod_p_VALUE != null) throw new Cyfieithu_gwall("겹친 cofnod_p"); cofnod_p_VALUE = cyfeiriad; } }
        if (cofnod_p_VALUE == null || (함수들.get(cofnod_p_VALUE).mynediad_cofnod & 0x100) != 0) throw new Cyfieithu_gwall("cofnod_p_VALUE SWYDDOGAETH_VALUE fformat_VALUE Gwall");
        List<String> llinell = new ArrayList<>(); llinell.add(".code32");
        for (Dosbarth_data data : 클래스들.values()) {
            String cyflwr_VALUE = symbol("state",data.Enw), ymgychwyn = symbol("init",data.Enw);
            Collections.addAll(llinell,".bss",".balign 4",cyflwr_VALUE + ": .long 0",".text",ymgychwyn + ":","cmpl $0, " + cyflwr_VALUE,"jne " + ymgychwyn + "_done","movl $1, " + cyflwr_VALUE);
            dull_cyfeiriad 초기화참조 = new dull_cyfeiriad(data.Enw,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) llinell.add("call " + symbol("method",초기화참조.부분들()));
            Collections.addAll(llinell,"movl $2, " + cyflwr_VALUE,ymgychwyn + "_done:","ret");
            for (aelod_data maes_VALUE : data.maes_VALUE) {
                byte[] cysonyn_VALUE = maes_VALUE.priodoledd_VALUE.get("ConstantValue"); String VALUE = cysonyn_VALUE == null ? "0" : X_86_cysonyn(data,new data_darllenwr(cysonyn_VALUE).두바이트());
                Collections.addAll(llinell,".data",".balign 4",symbol("field",data.Enw,maes_VALUE.Enw,maes_VALUE.서술) + ": .long " + VALUE);
            }
            for (aelod_data SWYDDOGAETH_VALUE : data.SWYDDOGAETH_VALUE) if (!SWYDDOGAETH_VALUE.Enw.equals("<init>")) llinell.add(X_86_dull_corff(new dull_cyfeiriad(data.Enw,SWYDDOGAETH_VALUE.Enw,SWYDDOGAETH_VALUE.서술),SWYDDOGAETH_VALUE,peiriant_tabl,targed));
        }
        Collections.addAll(llinell,".text",".globl java_entry","java_entry:","call " + symbol("init",cofnod_p_VALUE.perchennog_VALUE),"call " + symbol("method",cofnod_p_VALUE.부분들()));
        if (cofnod_p_VALUE.서술.equals("()V")) llinell.add("xorl %eax, %eax"); llinell.add("ret");
        for (String 지정 : 내보냄) {
            int amffinydd_VALUE = 지정.indexOf('='); if (amffinydd_VALUE < 1) throw new Cyfieithu_gwall("내보내기 지정 Gwall");
            String 외부 = 지정.substring(0,amffinydd_VALUE), SWYDDOGAETH_VALUE = 지정.substring(amffinydd_VALUE + 1); int rhannu_mesur = SWYDDOGAETH_VALUE.lastIndexOf('.');
            if (rhannu_mesur < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Cyfieithu_gwall("내보내기 symbol Gwall");
            String Dosbarth_VALUE = SWYDDOGAETH_VALUE.substring(0,rhannu_mesur).replace('.','/'), Enw = SWYDDOGAETH_VALUE.substring(rhannu_mesur + 1); dull_cyfeiriad dewisiad_VALUE = null;
            for (dull_cyfeiriad cyfeiriad : 함수들.keySet()) if (cyfeiriad.perchennog_VALUE.equals(Dosbarth_VALUE) && cyfeiriad.Enw.equals(Enw)) { if (dewisiad_VALUE != null) throw new Cyfieithu_gwall("겹친 내보내기 targed"); dewisiad_VALUE = cyfeiriad; }
            if (dewisiad_VALUE == null) throw new Cyfieithu_gwall("내보낼 함수가 없음");
            Collections.addAll(llinell,".text",".globl " + 외부,외부 + ":","call " + symbol("init",dewisiad_VALUE.perchennog_VALUE),"jmp " + symbol("method",dewisiad_VALUE.부분들()));
        }
        llinell.add(".section .rodata");
        for (Map.Entry<String,String> cofnod_VALUE : 문자열들.entrySet()) {
            Collections.addAll(llinell,".balign 4",cofnod_VALUE.getValue() + ":",".long " + cofnod_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char gwers_VALUE : cofnod_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(gwers_VALUE)); if (!단위들.isEmpty()) llinell.add(".long " + String.join(",",단위들));
        }
        llinell.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",llinell) + "\n";
    }
    static void Gweithredu_offeryn(List<String> Gorchymyn) throws Exception {
        if (new ProcessBuilder(Gorchymyn).inheritIO().start().waitFor() != 0) throw new Cyfieithu_gwall("llunio_ffynhonnell Gwall: " + Gorchymyn.get(0));
    }
    static String data_testun(String Testun) { return "\"" + Testun.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Cyfieithu(List<Path> 입력들, String targed, String cofnod_p, List<String> 내보냄, Path Allbwn, Path adnodd_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Dosbarth_llwybr = 임시.resolve("classes"); Files.createDirectory(Dosbarth_llwybr);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Dosbarth_llwybr.toString(),"-sourcepath",Dosbarth_llwybr.toString(),"-d",Dosbarth_llwybr.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int ffynhonnell_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Allbwn.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Cyfieithu_gwall("Allbwn 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); ffynhonnell_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Cyfieithu_gwall(".java 또는 .class만 Cymorth_VALUE");
            }
            if (ffynhonnell_COUNT > 0) Gweithredu_offeryn(자바명령);
            try (java.util.stream.Stream<Path> llwybr_Rhestr = Files.walk(Dosbarth_llwybr)) { llwybr_Rhestr.filter(LLWYBR -> LLWYBR.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,targed.equals("user") ? "user" : "kernel",262144,adnodd_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(cofnod_p,내보냄,targed); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path offeryn_safle = adnodd_VALUE.getParent();
            Gweithredu_offeryn(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Gweithredu_offeryn(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),offeryn_safle.resolve("amser_rhedeg_iaith_gyffredin_Cymorth.s").toString()));
            List<String> Cysylltu = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (targed.equals("kernel")) Cysylltu.add("-r");
            else {
                Gweithredu_offeryn(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),offeryn_safle.resolve(targed.equals("user") ? "START_defnyddiwr_Rhaglen.s" : "리눅스시작.s").toString()));
                Collections.addAll(Cysylltu,"-e","_start",임시.resolve("start.o").toString());
                if (targed.equals("user")) Collections.addAll(Cysylltu,"-T",offeryn_safle.resolve("defnyddiwr_Dolen_Llywio.ld").toString());
            }
            Collections.addAll(Cysylltu,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Gweithredu_offeryn(Cysylltu);
            Allbwn = Allbwn.toAbsolutePath(); Files.createDirectories(Allbwn.getParent()); Path cyhoeddi_VALUE = Files.createTempFile(Allbwn.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),cyhoeddi_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(cyhoeddi_VALUE,Allbwn,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(cyhoeddi_VALUE); }
            Files.setPosixFilePermissions(Allbwn,java.nio.file.attribute.PosixFilePermissions.fromString(targed.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Allbwn + ".s"),조립,StandardCharsets.UTF_8);
            List<String> symbol_data = new ArrayList<>(), data_ffynhonnell = new ArrayList<>();
            for (dull_cyfeiriad cyfeiriad : CONVERT_VALUE.함수들.keySet()) symbol_data.add(data_testun(symbol("method",cyfeiriad.부분들())) + ":" + data_testun(cyfeiriad.perchennog_VALUE + "." + cyfeiriad.Enw + cyfeiriad.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_ffeil = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Testun = new StringBuilder(); for (byte VALUE : hash_ffeil) Testun.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                data_ffynhonnell.add(data_testun(입력.toAbsolutePath().toString()) + ":" + data_testun(Testun.toString()));
            }
            Files.writeString(Paths.get(Allbwn + ".json"),"{\"target\":" + data_testun(targed) + ",\"entry\":" + data_testun(cofnod_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbol_data) + "},\"sources\":{" + String.join(",",data_ffynhonnell) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> llwybr_Rhestr = Files.walk(임시)) { for (Path LLWYBR : (Iterable<Path>)llwybr_Rhestr.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(LLWYBR); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String cofnod_p = null, targed = "kernel", X_86_targed = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> llwybr_Rhestr = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": X_86_targed = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Dosbarth_VALUE.SWYDDOGAETH_VALUE -o Allbwn [--target linux|kernel|user] [--profile kernel|user] [--export symbol=Dosbarth_VALUE.SWYDDOGAETH_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": cofnod_p = 인수[++순번]; break;
                    case "--profile": targed = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Cyfieithu_gwall("알 수 없는 옵션: " + VALUE); llwybr_Rhestr.add(Paths.get(VALUE));
                }
            }
            if (cofnod_p == null || 출력경로 == null || llwybr_Rhestr.isEmpty()) throw new Cyfieithu_gwall("--entry, -o, Dosbarth_VALUE 파일이 필요합니다");
            Path adnodd_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_targed != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_targed)) throw new Cyfieithu_gwall("알 수 없는 Gweithredu_gorchymyn targed");
                X_86_Cyfieithu(llwybr_Rhestr,X_86_targed,cofnod_p,내보냄,출력경로,adnodd_VALUE); return;
            }
            String FFYNHONNELL = new 기계어미리번역(llwybr_Rhestr, targed, 낱말수, adnodd_VALUE).cynhyrchu(cofnod_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, FFYNHONNELL, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Gwall) { System.err.println("llunio_ffynhonnell Gwall: " + Gwall.getMessage()); System.exit(1); }
    }
}
