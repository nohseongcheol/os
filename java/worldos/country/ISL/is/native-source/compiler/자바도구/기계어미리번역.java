// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java klasi_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. hýsa JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Þýðing_villa extends RuntimeException {
        Þýðing_villa(String 설명) { super(설명); }
    }
    static final class gögn_Lesari {
        final byte[] gögn;
        int Staðsetning;
        gögn_Lesari(byte[] 입력자료) { gögn = 입력자료; }
        byte[] Lestur(int lengd_VALUE) {
            if (lengd_VALUE < 0 || lengd_VALUE > gögn.length - Staðsetning) throw new Þýðing_villa("잘린 klasi_VALUE 또는 Skipun gögn");
            byte[] NIÐURSTAÐA = Arrays.copyOfRange(gögn, Staðsetning, Staðsetning + lengd_VALUE); Staðsetning += lengd_VALUE; return NIÐURSTAÐA;
        }
        int 한바이트() { if (Staðsetning >= gögn.length) throw new Þýðing_villa("잘린 Skipun gögn"); return gögn[Staðsetning++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class aðili_gögn {
        final int aðgangur_færsla;
        final String Heiti, 서술;
        final Map<String, byte[]> eigind_VALUE;
        aðili_gögn(int aðgangur_VALUE, String heiti_VALUE, String 서술값, Map<String, byte[]> eigind_gögn) {
            aðgangur_færsla = aðgangur_VALUE; Heiti = heiti_VALUE; 서술 = 서술값; eigind_VALUE = eigind_gögn;
        }
    }
    static final class aðferð_tilvísun implements Comparable<aðferð_tilvísun> {
        final String eigandi_VALUE, Heiti, 서술;
        aðferð_tilvísun(String 소유값, String heiti_VALUE, String 서술값) { eigandi_VALUE = 소유값; Heiti = heiti_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{eigandi_VALUE, Heiti, 서술}; }
        public int compareTo(aðferð_tilvísun jafningi_VALUE) {
            int Samanburður_VALUE = eigandi_VALUE.compareTo(jafningi_VALUE.eigandi_VALUE);
            if (Samanburður_VALUE == 0) Samanburður_VALUE = Heiti.compareTo(jafningi_VALUE.Heiti);
            return Samanburður_VALUE == 0 ? 서술.compareTo(jafningi_VALUE.서술) : Samanburður_VALUE;
        }
        public boolean equals(Object jafningi_VALUE) { return jafningi_VALUE instanceof aðferð_tilvísun && compareTo((aðferð_tilvísun) jafningi_VALUE) == 0; }
        public int hashCode() { return Objects.hash(eigandi_VALUE, Heiti, 서술); }
    }
    static final class klasi_gögn {
        final int[] 상수종류;
        final Object[] fasti_gögn;
        final String Heiti;
        final List<aðili_gögn> reitur_VALUE, fall_VALUE;
        klasi_gögn(Path SLÓÐ) throws IOException {
            gögn_Lesari Lesari_VALUE = new gögn_Lesari(Files.readAllBytes(SLÓÐ));
            if (Lesari_VALUE.네바이트() != 0xcafebabe) throw new Þýðing_villa("Java klasi_VALUE 표식이 아님");
            Lesari_VALUE.Lestur(4);
            int vara_COUNT = Lesari_VALUE.두바이트(); 상수종류 = new int[vara_COUNT]; fasti_gögn = new Object[vara_COUNT];
            for (int 순번 = 1; 순번 < vara_COUNT; 순번++) {
                int 종류 = Lesari_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int lengd_VALUE = Lesari_VALUE.두바이트();
                        byte[] stafur_biðminni = Lesari_VALUE.Lestur(lengd_VALUE), 길이붙인자료 = new byte[lengd_VALUE + 2];
                        길이붙인자료[0] = (byte)(lengd_VALUE >> 8); 길이붙인자료[1] = (byte)lengd_VALUE;
                        System.arraycopy(stafur_biðminni, 0, 길이붙인자료, 2, lengd_VALUE);
                        fasti_gögn[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: fasti_gögn[순번] = Lesari_VALUE.네바이트(); break;
                    case 4: Lesari_VALUE.Lestur(4); break;
                    case 5: case 6: Lesari_VALUE.Lestur(8); 순번++; break;
                    case 7: case 8: case 16: fasti_gögn[순번] = Lesari_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        fasti_gögn[순번] = new int[]{Lesari_VALUE.두바이트(), Lesari_VALUE.두바이트()}; break;
                    case 15: fasti_gögn[순번] = new int[]{Lesari_VALUE.한바이트(), Lesari_VALUE.두바이트()}; break;
                    default: throw new Þýðing_villa("지원하지 않는 fasti_VALUE 종류: " + 종류);
                }
            }
            Lesari_VALUE.두바이트(); Heiti = klasi_heiti(Lesari_VALUE.두바이트());
            if (!klasi_heiti(Lesari_VALUE.두바이트()).equals("java/lang/Object") || Lesari_VALUE.두바이트() != 0)
                throw new Þýðing_villa(Heiti + ": 상속 및 인터페이스 미지원");
            reitur_VALUE = 멤버읽기(Lesari_VALUE); fall_VALUE = 멤버읽기(Lesari_VALUE); 속성읽기(Lesari_VALUE);
            if (Lesari_VALUE.Staðsetning != Lesari_VALUE.gögn.length) throw new Þýðing_villa("klasi_VALUE 뒤에 남은 gögn");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Þýðing_villa("문자 fasti_VALUE INDEX Villa");
            return (String) fasti_gögn[INDEX];
        }
        String klasi_heiti(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Þýðing_villa("klasi_VALUE tilvísun Villa");
            return 문자((Integer)fasti_gögn[INDEX]);
        }
        aðferð_tilvísun tilvísun(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Þýðing_villa("멤버 tilvísun Villa");
            int[] para_VALUE = (int[])fasti_gögn[INDEX], heiti_para = (int[])fasti_gögn[para_VALUE[1]];
            return new aðferð_tilvísun(klasi_heiti(para_VALUE[0]), 문자(heiti_para[0]), 문자(heiti_para[1]));
        }
        Map<String, byte[]> 속성읽기(gögn_Lesari Lesari_VALUE) {
            Map<String, byte[]> NIÐURSTAÐA = new LinkedHashMap<>();
            int vara_COUNT = Lesari_VALUE.두바이트();
            for (int 순번 = 0; 순번 < vara_COUNT; 순번++) {
                String eigind_heiti = 문자(Lesari_VALUE.두바이트()); byte[] VALUE = Lesari_VALUE.Lestur(Lesari_VALUE.네바이트());
                if (NIÐURSTAÐA.put(eigind_heiti, VALUE) != null) throw new Þýðing_villa("겹친 eigind_VALUE: " + eigind_heiti);
            }
            return NIÐURSTAÐA;
        }
        List<aðili_gögn> 멤버읽기(gögn_Lesari Lesari_VALUE) {
            List<aðili_gögn> NIÐURSTAÐA = new ArrayList<>(); int vara_COUNT = Lesari_VALUE.두바이트();
            for (int 순번 = 0; 순번 < vara_COUNT; 순번++) {
                int aðgangur_færsla = Lesari_VALUE.두바이트(); String aðferð_færsla_heiti = 문자(Lesari_VALUE.두바이트()), 서술 = 문자(Lesari_VALUE.두바이트());
                NIÐURSTAÐA.add(new aðili_gögn(aðgangur_færsla, aðferð_færsla_heiti, 서술, 속성읽기(Lesari_VALUE)));
            }
            return NIÐURSTAÐA;
        }
    }
    static final class 함수형식 {
        final List<String> Viðföng = new ArrayList<>();
        final String skila_mæld_stærð;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Þýðing_villa("fall_VALUE 서술 Villa: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Þýðing_villa("fall_VALUE 서술 Villa: " + 서술);
            Viðföng.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Viðföng.contains("V") || 반환들.size() != 1) throw new Þýðing_villa("fall_VALUE 서술 Villa: " + 서술);
            skila_mæld_stærð = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> NIÐURSTAÐA = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Staðsetning = 0; Staðsetning < 서술.length();) {
            String val_VALUE = null;
            for (String snið_VALUE : 허용형식) if (서술.startsWith(snið_VALUE, Staðsetning)) { val_VALUE = snið_VALUE; break; }
            if (val_VALUE == null) throw new Þýðing_villa("지원하지 않는 gagnagerð: " + 서술);
            NIÐURSTAÐA.add(val_VALUE); Staðsetning += val_VALUE.length();
        }
        return NIÐURSTAÐA;
    }
    static String tákn(String 종류, String... 부분들) {
        try {
            byte[] tæting_skrá = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Texti = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Texti.append(String.format(Locale.ROOT, "%02x", tæting_skrá[순번] & 255));
            return Texti.toString();
        } catch (Exception Villa) { throw new Þýðing_villa(Villa.toString()); }
    }
    final Map<String, klasi_gögn> 클래스들 = new TreeMap<>();
    final Map<aðferð_tilvísun, aðili_gögn> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, vél_klasi;
    final int 동적기억낱말수;
    final Path tilfang_slóð;
    기계어미리번역(List<Path> slóð_Listi, String markmið, int 낱말수, Path tilfang_VALUE) throws IOException {
        if ((!markmið.equals("kernel") && !markmið.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Þýðing_villa("keyra_skipun markmið 또는 Minni_VALUE 공간 Stærð Villa");
        실행대상 = markmið; 동적기억낱말수 = 낱말수; tilfang_slóð = tilfang_VALUE;
        // 이 이름도 국가별 uppruni_tré skapa 시 해당 언어로 옮긴다.
        vél_klasi = markmið.equals("kernel") ? "bretti" : "notandi";
        for (String Lína : Files.readAllLines(tilfang_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Lína.split("\t", -1);
            if (부분들.length != 4) throw new Þýðing_villa("vél fall_VALUE gögn Villa");
            if (부분들[0].equals(markmið)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path SLÓÐ : slóð_Listi) {
            klasi_gögn gögn = new klasi_gögn(SLÓÐ);
            if (클래스들.put(gögn.Heiti, gögn) != null) throw new Þýðing_villa("중복 klasi_VALUE: " + gögn.Heiti);
            for (aðili_gögn reitur_VALUE : gögn.reitur_VALUE) {
                if ((reitur_VALUE.aðgangur_færsla & 8) == 0 || 형식읽기(reitur_VALUE.서술).equals(Collections.singletonList("V"))) throw new Þýðing_villa("fast_VALUE 필드만 Aðstoð_VALUE");
                if (필드들.put(new aðferð_tilvísun(gögn.Heiti, reitur_VALUE.Heiti, reitur_VALUE.서술), reitur_VALUE) != null) throw new Þýðing_villa("중복 reitur_VALUE");
            }
            for (aðili_gögn fall_VALUE : gögn.fall_VALUE) {
                if (fall_VALUE.Heiti.equals("<init>")) continue;
                if ((fall_VALUE.aðgangur_færsla & 8) == 0 || (fall_VALUE.aðgangur_færsla & (0x20 | 0x400)) != 0) throw new Þýðing_villa("fast_VALUE 비동기화 함수만 Aðstoð_VALUE");
                new 함수형식(fall_VALUE.서술);
                if (함수들.put(new aðferð_tilvísun(gögn.Heiti, fall_VALUE.Heiti, fall_VALUE.서술), fall_VALUE) != null) throw new Þýðing_villa("중복 fall_VALUE");
            }
        }
    }
    String strengur_tákn(String Texti) { return 문자열들.computeIfAbsent(Texti, VALUE -> "j_text_" + 문자열들.size()); }
    String fasti_segð(klasi_gögn gögn, int INDEX) {
        if (INDEX < 1 || INDEX >= gögn.상수종류.length) throw new Þýðing_villa("fasti_VALUE INDEX miðlaskrá Villa");
        if (gögn.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + gögn.fasti_gögn[INDEX] + ")";
        if (gögn.상수종류[INDEX] == 8) return "(word)" + strengur_tákn(gögn.문자((Integer)gögn.fasti_gögn[INDEX]));
        throw new Þýðing_villa("정수와 strengur_VALUE 상수만 Aðstoð_VALUE");
    }
    String 함수원형(aðferð_tilvísun tilvísun) {
        List<String> 인수들 = new ArrayList<>(); int vara_COUNT = new 함수형식(tilvísun.서술).Viðföng.size();
        for (int 순번 = 0; 순번 < vara_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + tákn("method", tilvísun.부분들()) + "(" + (vara_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void athuga_staðbundið(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Þýðing_villa("staðbundið_umfang 변수 INDEX miðlaskrá Villa"); }
    void 분기넣기(List<String> úttak, Set<Integer> grein_Listi, int Staðsetning, int 이동량, String skilyrði) {
        int endastaður_VALUE = Staðsetning + 이동량; grein_Listi.add(endastaður_VALUE);
        úttak.add((skilyrði == null ? "" : "if (" + skilyrði + ") ") + "goto b" + endastaður_VALUE + ";");
    }
    String aðferð_meginmál(aðferð_tilvísun fall_VALUE, aðili_gögn gögn) {
        byte[] meginmál_gögn = gögn.eigind_VALUE.get("Code"); if (meginmál_gögn == null) throw new Þýðing_villa("fall_VALUE 몸체가 없음: " + fall_VALUE.Heiti);
        gögn_Lesari Lesari_VALUE = new gögn_Lesari(meginmál_gögn); int 쌓임깊이 = Lesari_VALUE.두바이트(), 지역변수수 = Lesari_VALUE.두바이트();
        gögn_Lesari skipun_gögn = new gögn_Lesari(Lesari_VALUE.Lestur(Lesari_VALUE.네바이트()));
        if (Lesari_VALUE.두바이트() != 0) throw new Þýðing_villa("try/catch/finally 미지원");
        함수형식 snið_VALUE = new 함수형식(fall_VALUE.서술); if (지역변수수 < snið_VALUE.Viðföng.size()) throw new Þýðing_villa("매개변수보다 적은 staðbundið_umfang 변수");
        klasi_gögn klasi_VALUE = 클래스들.get(fall_VALUE.eigandi_VALUE);
        List<String> úttak = new ArrayList<>(); úttak.add(함수원형(fall_VALUE) + " {");
        úttak.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < snið_VALUE.Viðföng.size(); 순번++) úttak.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), grein_Listi = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (skipun_gögn.Staðsetning < skipun_gögn.gögn.length) {
            int Staðsetning = skipun_gögn.Staðsetning, Skipun = skipun_gögn.한바이트(); 경계들.add(Staðsetning); úttak.add("b" + Staðsetning + ":;");
            if (Skipun == 0) continue;
            if (Skipun == 1) úttak.add("PUSH(0);");
            else if (Skipun >= 2 && Skipun <= 8) úttak.add("PUSH((uint32_t)(" + (Skipun - 3) + "));");
            else if (Skipun == 16 || Skipun == 17) úttak.add("PUSH((uint32_t)(" + (Skipun == 16 ? skipun_gögn.부호한바이트() : skipun_gögn.부호두바이트()) + "));");
            else if (Skipun == 18 || Skipun == 19) úttak.add("PUSH(" + fasti_segð(klasi_VALUE, Skipun == 18 ? skipun_gögn.한바이트() : skipun_gögn.두바이트()) + ");");
            else if (Skipun == 21 || Skipun == 25 || (Skipun >= 26 && Skipun <= 29) || (Skipun >= 42 && Skipun <= 45)) {
                int INDEX = Skipun == 21 || Skipun == 25 ? skipun_gögn.한바이트() : Skipun - (Skipun <= 29 ? 26 : 42);
                athuga_staðbundið(INDEX, 지역변수수); úttak.add("PUSH(l[" + INDEX + "]);");
            } else if (Skipun == 54 || Skipun == 58 || (Skipun >= 59 && Skipun <= 62) || (Skipun >= 75 && Skipun <= 78)) {
                int INDEX = Skipun == 54 || Skipun == 58 ? skipun_gögn.한바이트() : Skipun - (Skipun <= 62 ? 59 : 75);
                athuga_staðbundið(INDEX, 지역변수수); úttak.add("l[" + INDEX + "] = POP();");
            } else if (Skipun == 46) úttak.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Skipun == 79) úttak.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Skipun == 87 || Skipun == 88) úttak.add(Skipun == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Skipun >= 89 && Skipun <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] röð_Listi = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Skipun - 89]; 순번++) úttak.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : röð_Listi[Skipun - 89].toCharArray()) úttak.add("PUSH(" + VALUE + ");");
            } else if (Skipun == 96 || Skipun == 100 || Skipun == 104 || Skipun == 126 || Skipun == 128 || Skipun == 130) {
                String aðgerð_VALUE = Skipun == 96 ? "+" : Skipun == 100 ? "-" : Skipun == 104 ? "*" : Skipun == 126 ? "&" : Skipun == 128 ? "|" : "^";
                úttak.add("b = POP(); a = POP(); PUSH((uint32_t)a " + aðgerð_VALUE + " (uint32_t)b);");
            } else if (Skipun == 108 || Skipun == 112) úttak.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Skipun == 112 ? 1 : 0) + "));");
            else if (Skipun == 116) úttak.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Skipun == 120 || Skipun == 122 || Skipun == 124) {
                úttak.add("b = POP(); a = POP();"); úttak.add("PUSH(" + (Skipun == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Skipun == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Skipun == 132) {
                int INDEX = skipun_gögn.한바이트(), 증가량 = skipun_gögn.부호한바이트(); athuga_staðbundið(INDEX, 지역변수수);
                úttak.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Skipun >= 145 && Skipun <= 147) úttak.add("a = POP(); PUSH((uint32_t)(" + (Skipun == 145 ? "int8_t" : Skipun == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Skipun >= 153 && Skipun <= 158) {
                úttak.add("a = POP();"); 분기넣기(úttak, grein_Listi, Staðsetning, skipun_gögn.부호두바이트(), "(int32_t)a " + 비교들[Skipun - 153] + " 0");
            } else if (Skipun >= 159 && Skipun <= 166) {
                úttak.add("b = POP(); a = POP();"); 분기넣기(úttak, grein_Listi, Staðsetning, skipun_gögn.부호두바이트(), Skipun >= 165 ? "a " + 비교들[Skipun - 159] + " b" : "(int32_t)a " + 비교들[Skipun - 159] + " (int32_t)b");
            } else if (Skipun == 167 || Skipun == 200) 분기넣기(úttak, grein_Listi, Staðsetning, Skipun == 167 ? skipun_gögn.부호두바이트() : skipun_gögn.네바이트(), null);
            else if (Skipun == 170 || Skipun == 171) {
                while (skipun_gögn.Staðsetning % 4 != 0) skipun_gögn.한바이트();
                int sjálfgildi = skipun_gögn.네바이트(); úttak.add("a = POP();");
                if (Skipun == 170) {
                    int 아래 = skipun_gögn.네바이트(), 위 = skipun_gögn.네바이트(); long vara_COUNT = (long)위 - 아래 + 1;
                    if (vara_COUNT < 1 || vara_COUNT > (skipun_gögn.gögn.length - skipun_gögn.Staðsetning) / 4) throw new Þýðing_villa("switch miðlaskrá Villa");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(úttak, grein_Listi, Staðsetning, skipun_gögn.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int vara_COUNT = skipun_gögn.네바이트(), myndavél_að_framan_gögn = 0;
                    if (vara_COUNT < 0 || vara_COUNT > (skipun_gögn.gögn.length - skipun_gögn.Staðsetning) / 8) throw new Þýðing_villa("switch Stærð Villa");
                    for (int 순번 = 0; 순번 < vara_COUNT; 순번++) {
                        int VALUE = skipun_gögn.네바이트(); if (순번 > 0 && VALUE <= myndavél_að_framan_gögn) throw new Þýðing_villa("switch röð_VALUE Villa"); myndavél_að_framan_gögn = VALUE;
                        분기넣기(úttak, grein_Listi, Staðsetning, skipun_gögn.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(úttak, grein_Listi, Staðsetning, sjálfgildi, null);
            } else if (Skipun == 172 || Skipun == 176 || Skipun == 177) úttak.add("return " + (Skipun == 177 ? "0" : "POP()") + ";");
            else if (Skipun == 178 || Skipun == 179) {
                aðferð_tilvísun tilvísun = klasi_VALUE.tilvísun(skipun_gögn.두바이트()); if (!필드들.containsKey(tilvísun)) throw new Þýðing_villa("알 númer 없는 reitur_VALUE");
                úttak.add(tákn("init", tilvísun.eigandi_VALUE) + "();"); String reitur_VALUE = tákn("field", tilvísun.부분들());
                úttak.add(Skipun == 178 ? "PUSH(" + reitur_VALUE + ");" : reitur_VALUE + " = POP();");
            } else if (Skipun == 184) {
                aðferð_tilvísun tilvísun = klasi_VALUE.tilvísun(skipun_gögn.두바이트()); if (!함수들.containsKey(tilvísun)) throw new Þýðing_villa("알 númer 없는 fall_VALUE");
                함수형식 호출형식 = new 함수형식(tilvísun.서술); int vara_COUNT = 호출형식.Viðföng.size();
                úttak.add(tákn("init", tilvísun.eigandi_VALUE) + "();"); úttak.add("if(sp < " + vara_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + vara_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < vara_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                úttak.add("a = " + tákn("method", tilvísun.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.skila_mæld_stærð.equals("V")) úttak.add("PUSH(a);");
            } else if (Skipun == 182) {
                aðferð_tilvísun tilvísun = klasi_VALUE.tilvísun(skipun_gögn.두바이트());
                if (tilvísun.equals(new aðferð_tilvísun("java/lang/String", "length", "()I"))) úttak.add("a = POP(); PUSH(length(a));");
                else if (tilvísun.equals(new aðferð_tilvísun("java/lang/String", "charAt", "(I)C"))) úttak.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Þýðing_villa("가상 fall_VALUE 호출 미지원");
            } else if (Skipun == 188) {
                if (skipun_gögn.한바이트() != 10) throw new Þýðing_villa("new int[]만 Aðstoð_VALUE"); úttak.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Skipun == 190) úttak.add("a = POP(); PUSH(length(a));");
            else if (Skipun == 196) {
                int viðbót_VALUE = skipun_gögn.한바이트(), INDEX = skipun_gögn.두바이트(); athuga_staðbundið(INDEX, 지역변수수);
                if (viðbót_VALUE == 21 || viðbót_VALUE == 25) úttak.add("PUSH(l[" + INDEX + "]);");
                else if (viðbót_VALUE == 54 || viðbót_VALUE == 58) úttak.add("l[" + INDEX + "] = POP();");
                else if (viðbót_VALUE == 132) úttak.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + skipun_gögn.부호두바이트() + ");");
                else throw new Þýðing_villa("미지원 wide Skipun");
            } else if (Skipun == 198 || Skipun == 199) {
                úttak.add("a = POP();"); 분기넣기(úttak, grein_Listi, Staðsetning, skipun_gögn.부호두바이트(), "a " + (Skipun == 198 ? "==" : "!=") + " 0");
            } else throw new Þýðing_villa(fall_VALUE.eigandi_VALUE + "." + fall_VALUE.Heiti + ", bæti_VALUE " + Staðsetning + ": 미지원 Skipun " + Skipun);
        }
        if (!경계들.containsAll(grein_Listi)) throw new Þýðing_villa("Skipun 경계가 아닌 곳으로 grein");
        úttak.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", úttak);
    }
    String flytja_út_aðferð(String tengja_tákn, String markmið, boolean 진입점여부) {
        int staða_INDEX = markmið.lastIndexOf('.'); if (staða_INDEX < 0 || !tengja_tákn.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Þýðing_villa("내보내기 úthluta_VALUE Villa");
        String eigandi_VALUE = markmið.substring(0, staða_INDEX).replace('.', '/'), Heiti = markmið.substring(staða_INDEX + 1); aðferð_tilvísun val_VALUE = null;
        for (aðferð_tilvísun tilvísun : 함수들.keySet()) if (tilvísun.eigandi_VALUE.equals(eigandi_VALUE) && tilvísun.Heiti.equals(Heiti)) {
            if (val_VALUE != null) throw new Þýðing_villa("겹친 내보내기 markmið"); val_VALUE = tilvísun;
        }
        if (val_VALUE == null || (함수들.get(val_VALUE).aðgangur_færsla & 0x100) != 0) throw new Þýðing_villa("내보낼 함수가 없음 또는 native fall_VALUE");
        함수형식 snið_VALUE = new 함수형식(val_VALUE.서술);
        if ((진입점여부 && !snið_VALUE.Viðföng.isEmpty()) || !Arrays.asList("V", "I").contains(snið_VALUE.skila_mæld_stærð)) throw new Þýðing_villa("færsla_P_VALUE 또는 C 경계 snið_VALUE Villa");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < snið_VALUE.Viðföng.size(); 순번++) {
            if (!snið_VALUE.Viðföng.get(순번).equals("I")) throw new Þýðing_villa("C 경계는 int 인수만 Aðstoð_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (snið_VALUE.skila_mæld_stærð.equals("V") ? "void " : "int32_t ") + tengja_tákn + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + tákn("init", val_VALUE.eigandi_VALUE) + "(); " + (snið_VALUE.skila_mæld_stærð.equals("V") ? "" : "return (int32_t)") + tákn("method", val_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String skapa(String færsla_P, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<aðferð_tilvísun, aðili_gögn> færsla_VALUE : 함수들.entrySet()) {
            aðferð_tilvísun tilvísun = færsla_VALUE.getKey(); aðili_gögn gögn = færsla_VALUE.getValue(); 선언들.add(함수원형(tilvísun) + ";");
            if ((gögn.aðgangur_færsla & 0x100) != 0) {
                String Tengjast = 기계함수들.get(tilvísun.Heiti + tilvísun.서술);
                if (!tilvísun.eigandi_VALUE.equals(vél_klasi) || Tengjast == null) throw new Þýðing_villa("허용되지 않은 native fall_VALUE: " + tilvísun.Heiti);
                int vara_COUNT = new 함수형식(tilvísun.서술).Viðföng.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < vara_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Tengjast + "(" + (vara_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(vara_COUNT, "word"))) + ");");
                몸체들.add(함수원형(tilvísun) + " { return " + Tengjast + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(aðferð_meginmál(tilvísun, gögn));
        }
        for (Map.Entry<aðferð_tilvísun, aðili_gögn> færsla_VALUE : 필드들.entrySet()) {
            aðferð_tilvísun tilvísun = færsla_VALUE.getKey(); byte[] fasti_VALUE = færsla_VALUE.getValue().eigind_VALUE.get("ConstantValue");
            String VALUE = fasti_VALUE == null ? "0" : fasti_segð(클래스들.get(tilvísun.eigandi_VALUE), new gögn_Lesari(fasti_VALUE).두바이트());
            필드선언들.add("static word " + tákn("field", tilvísun.부분들()) + " = " + VALUE + ";");
        }
        for (String Heiti : 클래스들.keySet()) {
            String frumstilla = tákn("init", Heiti), staða_VALUE_e10195a1 = tákn("state", Heiti);
            선언들.add("static void " + frumstilla + "(void);"); 필드선언들.add("static unsigned " + staða_VALUE_e10195a1 + ";");
            aðferð_tilvísun tilvísun = new aðferð_tilvísun(Heiti, "<clinit>", "()V");
            몸체들.add("static void " + frumstilla + "(void) { if(" + staða_VALUE_e10195a1 + ") return; " + staða_VALUE_e10195a1 + " = 1; " + (함수들.containsKey(tilvísun) ? tákn("method", tilvísun.부분들()) + "(); " : "") + staða_VALUE_e10195a1 + " = 2; }");
        }
        몸체들.add(flytja_út_aðferð("java_entry", færsla_P, true)); Set<String> 공개이름 = new HashSet<>();
        for (String úthluta_VALUE : 내보내기목록) {
            int staða_INDEX = úthluta_VALUE.indexOf('='); if (staða_INDEX < 1) throw new Þýðing_villa("내보내기 úthluta_VALUE Villa");
            String Heiti = úthluta_VALUE.substring(0, staða_INDEX); 공개이름.add(Heiti); 몸체들.add(flytja_út_aðferð(Heiti, úthluta_VALUE.substring(staða_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> færsla_VALUE : 문자열들.entrySet()) {
            String Texti = færsla_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + færsla_VALUE.getValue() + "[] = {" + Texti.length());
            for (int 순번 = 0; 순번 < Texti.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Texti.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Aðstoð_VALUE = Files.readString(tilfang_slóð.resolve("CLR_Aðstoð.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Aðstoð_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String Uppruni, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> heiti_tafla = new HashMap<>();
        for (String Lína : Files.readAllLines(tilfang_slóð.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] para_VALUE = Lína.split("\t"); heiti_tafla.put(para_VALUE[0], para_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(Uppruni); StringBuffer NIÐURSTAÐA = new StringBuffer();
        while (찾개.find()) {
            String Heiti = 찾개.group(), 새이름 = Heiti;
            if (!Heiti.startsWith("//") && !Heiti.startsWith("/*") && !Heiti.startsWith("\"") && !Heiti.startsWith("'") && !공개이름.contains(Heiti)) {
                새이름 = heiti_tafla.getOrDefault(Heiti, Heiti);
                if (Heiti.matches("a[0-9]+")) 새이름 = "Viðföng" + Heiti.substring(1);
                if (Heiti.matches("b[0-9]+")) 새이름 = "grein" + Heiti.substring(1);
                if (범용표기) {
                    StringBuilder táknun_VALUE = new StringBuilder();
                    for (char stafur_VALUE : 새이름.toCharArray()) táknun_VALUE.append(stafur_VALUE < 128 ? Character.toString(stafur_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)stafur_VALUE));
                    새이름 = táknun_VALUE.toString();
                }
            }
            찾개.appendReplacement(NIÐURSTAÐA, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(NIÐURSTAÐA); return NIÐURSTAÐA.toString();
    }
    String X_86_aðferð_meginmál(aðferð_tilvísun fall_VALUE, aðili_gögn gögn, Map<String,String> vél_tafla, String markmið) {
        String 표식 = tákn("method", fall_VALUE.부분들());
        List<String> Lína = new ArrayList<>();
        if ((gögn.aðgangur_færsla & 0x100) != 0) {
            String Tengjast = vél_tafla.get(fall_VALUE.Heiti + fall_VALUE.서술);
            if (!fall_VALUE.eigandi_VALUE.equals(markmið.equals("kernel") ? "tæki_VALUE" : "notandi") || Tengjast == null) throw new Þýðing_villa("허용되지 않은 native fall_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Tengjast;
        }
        byte[] meginmál = gögn.eigind_VALUE.get("Code"); if (meginmál == null) throw new Þýðing_villa("fall_VALUE 몸체가 없음");
        gögn_Lesari Lesari_VALUE = new gögn_Lesari(meginmál); Lesari_VALUE.두바이트(); int staðbundið_COUNT = Lesari_VALUE.두바이트();
        gögn_Lesari skipun_gögn = new gögn_Lesari(Lesari_VALUE.Lestur(Lesari_VALUE.네바이트()));
        if (Lesari_VALUE.두바이트() != 0) throw new Þýðing_villa("try/catch/finally 미지원");
        함수형식 snið_VALUE = new 함수형식(fall_VALUE.서술); if (staðbundið_COUNT < snið_VALUE.Viðföng.size()) throw new Þýðing_villa("매개변수보다 적은 staðbundið_umfang 변수");
        Collections.addAll(Lína,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + staðbundið_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < snið_VALUE.Viðföng.size(); 순번++) Collections.addAll(Lína,"movl " + (8 + 4 * (snið_VALUE.Viðföng.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        klasi_gögn klasi_VALUE = 클래스들.get(fall_VALUE.eigandi_VALUE); Set<Integer> 경계들 = new HashSet<>(), grein_Listi = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (skipun_gögn.Staðsetning < skipun_gögn.gögn.length) {
            int Staðsetning = skipun_gögn.Staðsetning, Skipun = skipun_gögn.한바이트(); String staða_INDEX = 표식 + "_b" + Staðsetning;
            Lína.add(staða_INDEX + ":"); 경계들.add(Staðsetning);
            if (Skipun == 0) Lína.add("nop");
            else if (Skipun == 1) Lína.add("pushl $0");
            else if (Skipun >= 2 && Skipun <= 8) Lína.add("pushl $" + (Skipun - 3));
            else if (Skipun == 16 || Skipun == 17) Lína.add("pushl $" + (Skipun == 16 ? skipun_gögn.부호한바이트() : skipun_gögn.부호두바이트()));
            else if (Skipun == 18 || Skipun == 19) {
                int INDEX = Skipun == 18 ? skipun_gögn.한바이트() : skipun_gögn.두바이트();
                Lína.add("pushl $" + X_86_fasti(klasi_VALUE,INDEX));
            } else if (Skipun == 21 || Skipun == 25 || (Skipun >= 26 && Skipun <= 29) || (Skipun >= 42 && Skipun <= 45) || Skipun == 54 || Skipun == 58 || (Skipun >= 59 && Skipun <= 62) || (Skipun >= 75 && Skipun <= 78)) {
                boolean 읽음 = Skipun < 54; int INDEX = Skipun == 21 || Skipun == 25 || Skipun == 54 || Skipun == 58 ? skipun_gögn.한바이트() : Skipun - (Skipun <= 29 ? 26 : Skipun <= 45 ? 42 : Skipun <= 62 ? 59 : 75);
                athuga_staðbundið(INDEX,staðbundið_COUNT); Lína.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Skipun == 46) Collections.addAll(Lína,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Skipun == 79) Collections.addAll(Lína,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Skipun == 87 || Skipun == 88) Lína.add("addl $" + (Skipun == 87 ? 4 : 8) + ", %esp");
            else if (Skipun >= 89 && Skipun <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] röð_Listi = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Skipun - 89]; 순번++) Lína.add("popl " + 저장기들[순번]);
                for (int 순번 : röð_Listi[Skipun - 89]) Lína.add("pushl " + 저장기들[순번]);
            } else if (Skipun == 96 || Skipun == 100 || Skipun == 104 || Skipun == 126 || Skipun == 128 || Skipun == 130) {
                String aðgerð_VALUE = Skipun == 96 ? "addl" : Skipun == 100 ? "subl" : Skipun == 104 ? "imull" : Skipun == 126 ? "andl" : Skipun == 128 ? "orl" : "xorl";
                Collections.addAll(Lína,"popl %ecx","popl %eax",aðgerð_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Skipun == 108 || Skipun == 112) Collections.addAll(Lína,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + staða_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + staða_INDEX + "_divide","xorl %edx, %edx","jmp " + staða_INDEX + "_done",staða_INDEX + "_divide:","cltd","idivl %ecx",staða_INDEX + "_done:","pushl " + (Skipun == 108 ? "%eax" : "%edx"));
            else if (Skipun == 116) Lína.add("negl (%esp)");
            else if (Skipun == 120 || Skipun == 122 || Skipun == 124) Collections.addAll(Lína,"popl %ecx","popl %eax",(Skipun == 120 ? "sall" : Skipun == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Skipun == 132) {
                int INDEX = skipun_gögn.한바이트(), 증가 = skipun_gögn.부호한바이트(); athuga_staðbundið(INDEX,staðbundið_COUNT); Lína.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Skipun >= 145 && Skipun <= 147) Collections.addAll(Lína,"popl %eax",Skipun == 145 ? "movsbl %al, %eax" : Skipun == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Skipun >= 153 && Skipun <= 166) {
                if (Skipun <= 158) Collections.addAll(Lína,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Lína,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int endastaður_VALUE = Staðsetning + skipun_gögn.부호두바이트(); grein_Listi.add(endastaður_VALUE); Lína.add(비교들[Skipun - (Skipun <= 158 ? 153 : 159)] + " " + 표식 + "_b" + endastaður_VALUE);
            } else if (Skipun == 167 || Skipun == 200) {
                int endastaður_VALUE = Staðsetning + (Skipun == 167 ? skipun_gögn.부호두바이트() : skipun_gögn.네바이트()); grein_Listi.add(endastaður_VALUE); Lína.add("jmp " + 표식 + "_b" + endastaður_VALUE);
            } else if (Skipun == 170 || Skipun == 171) {
                while (skipun_gögn.Staðsetning % 4 != 0) skipun_gögn.한바이트();
                int sjálfgildi = Staðsetning + skipun_gögn.네바이트(); grein_Listi.add(sjálfgildi); Lína.add("popl %eax");
                int vara_COUNT, 아래 = 0;
                if (Skipun == 170) { 아래 = skipun_gögn.네바이트(); int 위 = skipun_gögn.네바이트(); long lengd_VALUE = (long)위 - 아래 + 1; if (lengd_VALUE < 1 || lengd_VALUE > (skipun_gögn.gögn.length - skipun_gögn.Staðsetning) / 4) throw new Þýðing_villa("switch miðlaskrá Villa"); vara_COUNT = (int)lengd_VALUE; }
                else { vara_COUNT = skipun_gögn.네바이트(); if (vara_COUNT < 0 || vara_COUNT > (skipun_gögn.gögn.length - skipun_gögn.Staðsetning) / 8) throw new Þýðing_villa("switch Stærð Villa"); }
                for (int 순번 = 0; 순번 < vara_COUNT; 순번++) {
                    int VALUE = Skipun == 170 ? 아래 + 순번 : skipun_gögn.네바이트(), endastaður_VALUE = Staðsetning + skipun_gögn.네바이트(); grein_Listi.add(endastaður_VALUE);
                    Collections.addAll(Lína,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + endastaður_VALUE);
                }
                Lína.add("jmp " + 표식 + "_b" + sjálfgildi);
            } else if (Skipun == 172 || Skipun == 176 || Skipun == 177) {
                if (Skipun != 177) Lína.add("popl %eax"); Collections.addAll(Lína,"leave","ret");
            } else if (Skipun == 178 || Skipun == 179) {
                aðferð_tilvísun tilvísun = klasi_VALUE.tilvísun(skipun_gögn.두바이트()); if (!필드들.containsKey(tilvísun)) throw new Þýðing_villa("알 númer 없는 reitur_VALUE");
                Collections.addAll(Lína,"call " + tákn("init",tilvísun.eigandi_VALUE),(Skipun == 178 ? "pushl " : "popl ") + tákn("field",tilvísun.부분들()));
            } else if (Skipun == 184) {
                aðferð_tilvísun tilvísun = klasi_VALUE.tilvísun(skipun_gögn.두바이트()); if (!함수들.containsKey(tilvísun)) throw new Þýðing_villa("알 númer 없는 fall_VALUE");
                함수형식 호출형식 = new 함수형식(tilvísun.서술); Collections.addAll(Lína,"call " + tákn("init",tilvísun.eigandi_VALUE),"call " + tákn("method",tilvísun.부분들()));
                if (!호출형식.Viðföng.isEmpty()) Lína.add("addl $" + 호출형식.Viðföng.size() * 4 + ", %esp");
                if (!호출형식.skila_mæld_stærð.equals("V")) Lína.add("pushl %eax");
            } else if (Skipun == 182) {
                aðferð_tilvísun tilvísun = klasi_VALUE.tilvísun(skipun_gögn.두바이트());
                if (tilvísun.equals(new aðferð_tilvísun("java/lang/String","length","()I"))) Collections.addAll(Lína,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (tilvísun.equals(new aðferð_tilvísun("java/lang/String","charAt","(I)C"))) Collections.addAll(Lína,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Þýðing_villa("가상 fall_VALUE 호출 미지원");
            } else if (Skipun == 188) {
                if (skipun_gögn.한바이트() != 10) throw new Þýðing_villa("new int[]만 Aðstoð_VALUE"); Collections.addAll(Lína,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Skipun == 190) Collections.addAll(Lína,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Skipun == 196) {
                int viðbót_VALUE = skipun_gögn.한바이트(), INDEX = skipun_gögn.두바이트(); athuga_staðbundið(INDEX,staðbundið_COUNT);
                if (viðbót_VALUE == 21 || viðbót_VALUE == 25 || viðbót_VALUE == 54 || viðbót_VALUE == 58) Lína.add((viðbót_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (viðbót_VALUE == 132) Lína.add("addl $" + skipun_gögn.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Þýðing_villa("wide Skipun 미지원");
            } else if (Skipun == 198 || Skipun == 199) {
                int endastaður_VALUE = Staðsetning + skipun_gögn.부호두바이트(); grein_Listi.add(endastaður_VALUE); Collections.addAll(Lína,"popl %eax","testl %eax, %eax",(Skipun == 198 ? "je " : "jne ") + 표식 + "_b" + endastaður_VALUE);
            } else throw new Þýðing_villa("미지원 Skipun: " + Skipun);
        }
        if (!경계들.containsAll(grein_Listi)) throw new Þýðing_villa("Skipun 경계가 아닌 곳으로 grein");
        Lína.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",Lína);
    }
    String X_86_fasti(klasi_gögn gögn, int INDEX) {
        if (gögn.상수종류[INDEX] == 3) return gögn.fasti_gögn[INDEX].toString();
        if (gögn.상수종류[INDEX] == 8) return strengur_tákn(gögn.문자((Integer)gögn.fasti_gögn[INDEX]));
        throw new Þýðing_villa("정수와 strengur_VALUE 상수만 Aðstoð_VALUE");
    }
    String X_86_samsetning(String færsla_P, List<String> 내보냄, String markmið) throws IOException {
        Map<String,String> vél_tafla = new HashMap<>();
        for (String Lína : Files.readAllLines(tilfang_slóð.resolve("엑스기계함수.tsv"))) { String[] para_VALUE = Lína.split("\t"); if (para_VALUE[0].equals(markmið)) vél_tafla.put(para_VALUE[1] + para_VALUE[2],para_VALUE[3]); }
        int staða_INDEX = færsla_P.lastIndexOf('.'); if (staða_INDEX < 0) throw new Þýðing_villa("færsla_P úthluta_VALUE Villa");
        String eigandi_VALUE = færsla_P.substring(0,staða_INDEX).replace('.','/'), aðferð_færsla_heiti = færsla_P.substring(staða_INDEX + 1); aðferð_tilvísun færsla_P_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { aðferð_tilvísun tilvísun = new aðferð_tilvísun(eigandi_VALUE,aðferð_færsla_heiti,서술); if (함수들.containsKey(tilvísun)) { if (færsla_P_VALUE != null) throw new Þýðing_villa("겹친 færsla_P"); færsla_P_VALUE = tilvísun; } }
        if (færsla_P_VALUE == null || (함수들.get(færsla_P_VALUE).aðgangur_færsla & 0x100) != 0) throw new Þýðing_villa("færsla_P_VALUE fall_VALUE snið_VALUE Villa");
        List<String> Lína = new ArrayList<>(); Lína.add(".code32");
        for (klasi_gögn gögn : 클래스들.values()) {
            String staða_VALUE_e10195a1 = tákn("state",gögn.Heiti), frumstilla = tákn("init",gögn.Heiti);
            Collections.addAll(Lína,".bss",".balign 4",staða_VALUE_e10195a1 + ": .long 0",".text",frumstilla + ":","cmpl $0, " + staða_VALUE_e10195a1,"jne " + frumstilla + "_done","movl $1, " + staða_VALUE_e10195a1);
            aðferð_tilvísun 초기화참조 = new aðferð_tilvísun(gögn.Heiti,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Lína.add("call " + tákn("method",초기화참조.부분들()));
            Collections.addAll(Lína,"movl $2, " + staða_VALUE_e10195a1,frumstilla + "_done:","ret");
            for (aðili_gögn reitur_VALUE : gögn.reitur_VALUE) {
                byte[] fasti_VALUE = reitur_VALUE.eigind_VALUE.get("ConstantValue"); String VALUE = fasti_VALUE == null ? "0" : X_86_fasti(gögn,new gögn_Lesari(fasti_VALUE).두바이트());
                Collections.addAll(Lína,".data",".balign 4",tákn("field",gögn.Heiti,reitur_VALUE.Heiti,reitur_VALUE.서술) + ": .long " + VALUE);
            }
            for (aðili_gögn fall_VALUE : gögn.fall_VALUE) if (!fall_VALUE.Heiti.equals("<init>")) Lína.add(X_86_aðferð_meginmál(new aðferð_tilvísun(gögn.Heiti,fall_VALUE.Heiti,fall_VALUE.서술),fall_VALUE,vél_tafla,markmið));
        }
        Collections.addAll(Lína,".text",".globl java_entry","java_entry:","call " + tákn("init",færsla_P_VALUE.eigandi_VALUE),"call " + tákn("method",færsla_P_VALUE.부분들()));
        if (færsla_P_VALUE.서술.equals("()V")) Lína.add("xorl %eax, %eax"); Lína.add("ret");
        for (String úthluta_VALUE : 내보냄) {
            int skiltákn_VALUE_d8ba4873 = úthluta_VALUE.indexOf('='); if (skiltákn_VALUE_d8ba4873 < 1) throw new Þýðing_villa("내보내기 úthluta_VALUE Villa");
            String 외부 = úthluta_VALUE.substring(0,skiltákn_VALUE_d8ba4873), fall_VALUE = úthluta_VALUE.substring(skiltákn_VALUE_d8ba4873 + 1); int deiling_mæld_stærð = fall_VALUE.lastIndexOf('.');
            if (deiling_mæld_stærð < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Þýðing_villa("내보내기 tákn Villa");
            String klasi_VALUE = fall_VALUE.substring(0,deiling_mæld_stærð).replace('.','/'), Heiti = fall_VALUE.substring(deiling_mæld_stærð + 1); aðferð_tilvísun val_VALUE = null;
            for (aðferð_tilvísun tilvísun : 함수들.keySet()) if (tilvísun.eigandi_VALUE.equals(klasi_VALUE) && tilvísun.Heiti.equals(Heiti)) { if (val_VALUE != null) throw new Þýðing_villa("겹친 내보내기 markmið"); val_VALUE = tilvísun; }
            if (val_VALUE == null) throw new Þýðing_villa("내보낼 함수가 없음");
            Collections.addAll(Lína,".text",".globl " + 외부,외부 + ":","call " + tákn("init",val_VALUE.eigandi_VALUE),"jmp " + tákn("method",val_VALUE.부분들()));
        }
        Lína.add(".section .rodata");
        for (Map.Entry<String,String> færsla_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Lína,".balign 4",færsla_VALUE.getValue() + ":",".long " + færsla_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char eining_VALUE_7c611f50 : færsla_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(eining_VALUE_7c611f50)); if (!단위들.isEmpty()) Lína.add(".long " + String.join(",",단위들));
        }
        Lína.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Lína) + "\n";
    }
    static void keyra_verkfæri(List<String> Skipun) throws Exception {
        if (new ProcessBuilder(Skipun).inheritIO().start().waitFor() != 0) throw new Þýðing_villa("þýða_uppruni Villa: " + Skipun.get(0));
    }
    static String gögn_strengur(String Texti) { return "\"" + Texti.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Þýðing(List<Path> 입력들, String markmið, String færsla_P, List<String> 내보냄, Path úttak, Path tilfang_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), klasi_slóð = 임시.resolve("classes"); Files.createDirectory(klasi_slóð);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",klasi_slóð.toString(),"-sourcepath",klasi_slóð.toString(),"-d",klasi_slóð.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int uppruni_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (úttak.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Þýðing_villa("úttak 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); uppruni_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Þýðing_villa(".java 또는 .class만 Aðstoð_VALUE");
            }
            if (uppruni_COUNT > 0) keyra_verkfæri(자바명령);
            try (java.util.stream.Stream<Path> slóð_Listi = Files.walk(klasi_slóð)) { slóð_Listi.filter(SLÓÐ -> SLÓÐ.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,markmið.equals("user") ? "user" : "kernel",262144,tilfang_VALUE);
            String 조립 = CONVERT_VALUE.X_86_samsetning(færsla_P,내보냄,markmið); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path verkfæri_staða = tilfang_VALUE.getParent();
            keyra_verkfæri(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            keyra_verkfæri(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),verkfæri_staða.resolve("CLR_Aðstoð.s").toString()));
            List<String> Tengjast = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (markmið.equals("kernel")) Tengjast.add("-r");
            else {
                keyra_verkfæri(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),verkfæri_staða.resolve(markmið.equals("user") ? "Opna_notandi_forrit.s" : "리눅스시작.s").toString()));
                Collections.addAll(Tengjast,"-e","_start",임시.resolve("start.o").toString());
                if (markmið.equals("user")) Collections.addAll(Tengjast,"-T",verkfæri_staða.resolve("notandi_tengja_útlit.ld").toString());
            }
            Collections.addAll(Tengjast,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); keyra_verkfæri(Tengjast);
            úttak = úttak.toAbsolutePath(); Files.createDirectories(úttak.getParent()); Path birta_VALUE = Files.createTempFile(úttak.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),birta_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(birta_VALUE,úttak,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(birta_VALUE); }
            Files.setPosixFilePermissions(úttak,java.nio.file.attribute.PosixFilePermissions.fromString(markmið.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(úttak + ".s"),조립,StandardCharsets.UTF_8);
            List<String> tákn_gögn = new ArrayList<>(), frumgögn = new ArrayList<>();
            for (aðferð_tilvísun tilvísun : CONVERT_VALUE.함수들.keySet()) tákn_gögn.add(gögn_strengur(tákn("method",tilvísun.부분들())) + ":" + gögn_strengur(tilvísun.eigandi_VALUE + "." + tilvísun.Heiti + tilvísun.서술));
            for (Path 입력 : 입력들) {
                byte[] tæting_skrá = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Texti = new StringBuilder(); for (byte VALUE : tæting_skrá) Texti.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                frumgögn.add(gögn_strengur(입력.toAbsolutePath().toString()) + ":" + gögn_strengur(Texti.toString()));
            }
            Files.writeString(Paths.get(úttak + ".json"),"{\"target\":" + gögn_strengur(markmið) + ",\"entry\":" + gögn_strengur(færsla_P) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",tákn_gögn) + "},\"sources\":{" + String.join(",",frumgögn) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> slóð_Listi = Files.walk(임시)) { for (Path SLÓÐ : (Iterable<Path>)slóð_Listi.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(SLÓÐ); }
        }
    }
    public static void main(String[] Viðföng) {
        try {
            String færsla_P = null, markmið = "kernel", X_86_markmið = null; Path úttak_slóð = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> slóð_Listi = new ArrayList<>();
            for (int 순번 = 0; 순번 < Viðföng.length; 순번++) {
                String VALUE = Viðföng[순번];
                switch (VALUE) {
                    case "--target": X_86_markmið = Viðföng[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry klasi_VALUE.fall_VALUE -o úttak [--target linux|kernel|user] [--profile kernel|user] [--export tákn=klasi_VALUE.fall_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": færsla_P = Viðföng[++순번]; break;
                    case "--profile": markmið = Viðföng[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Viðföng[++순번]); break;
                    case "--export": 내보냄.add(Viðföng[++순번]); break;
                    case "-o": úttak_slóð = Paths.get(Viðföng[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Þýðing_villa("알 númer 없는 옵션: " + VALUE); slóð_Listi.add(Paths.get(VALUE));
                }
            }
            if (færsla_P == null || úttak_slóð == null || slóð_Listi.isEmpty()) throw new Þýðing_villa("--entry, -o, klasi_VALUE 파일이 필요합니다");
            Path tilfang_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_markmið != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_markmið)) throw new Þýðing_villa("알 númer 없는 keyra_skipun markmið");
                X_86_Þýðing(slóð_Listi,X_86_markmið,færsla_P,내보냄,úttak_slóð,tilfang_VALUE); return;
            }
            String Uppruni = new 기계어미리번역(slóð_Listi, markmið, 낱말수, tilfang_VALUE).skapa(færsla_P, 내보냄, 범용표기);
            úttak_slóð = úttak_slóð.toAbsolutePath(); Files.createDirectories(úttak_slóð.getParent());
            Path 임시 = Files.createTempFile(úttak_slóð.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, Uppruni, StandardCharsets.UTF_8); Files.move(임시, úttak_slóð, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Villa) { System.err.println("þýða_uppruni Villa: " + Villa.getMessage()); System.exit(1); }
    }
}
