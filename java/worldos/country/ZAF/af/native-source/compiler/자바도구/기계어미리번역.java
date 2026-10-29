// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Klas_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. hou JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Vertaling_fout extends RuntimeException {
        Vertaling_fout(String 설명) { super(설명); }
    }
    static final class data_Leser {
        final byte[] data;
        int Posisie;
        data_Leser(byte[] 입력자료) { data = 입력자료; }
        byte[] Lees(int lengte_VALUE) {
            if (lengte_VALUE < 0 || lengte_VALUE > data.length - Posisie) throw new Vertaling_fout("잘린 Klas_VALUE 또는 Opdrag data");
            byte[] maatreël = Arrays.copyOfRange(data, Posisie, Posisie + lengte_VALUE); Posisie += lengte_VALUE; return maatreël;
        }
        int 한바이트() { if (Posisie >= data.length) throw new Vertaling_fout("잘린 Opdrag data"); return data[Posisie++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class lid_data {
        final int toegang_inskrywing;
        final String Naam, 서술;
        final Map<String, byte[]> kenmerk_VALUE;
        lid_data(int toegang_VALUE, String naam_VALUE, String 서술값, Map<String, byte[]> kenmerk_data) {
            toegang_inskrywing = toegang_VALUE; Naam = naam_VALUE; 서술 = 서술값; kenmerk_VALUE = kenmerk_data;
        }
    }
    static final class metode_Naslaan implements Comparable<metode_Naslaan> {
        final String eienaar_VALUE, Naam, 서술;
        metode_Naslaan(String 소유값, String naam_VALUE, String 서술값) { eienaar_VALUE = 소유값; Naam = naam_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{eienaar_VALUE, Naam, 서술}; }
        public int compareTo(metode_Naslaan portuur_VALUE) {
            int Vergelyking_VALUE = eienaar_VALUE.compareTo(portuur_VALUE.eienaar_VALUE);
            if (Vergelyking_VALUE == 0) Vergelyking_VALUE = Naam.compareTo(portuur_VALUE.Naam);
            return Vergelyking_VALUE == 0 ? 서술.compareTo(portuur_VALUE.서술) : Vergelyking_VALUE;
        }
        public boolean equals(Object portuur_VALUE) { return portuur_VALUE instanceof metode_Naslaan && compareTo((metode_Naslaan) portuur_VALUE) == 0; }
        public int hashCode() { return Objects.hash(eienaar_VALUE, Naam, 서술); }
    }
    static final class Klas_data {
        final int[] 상수종류;
        final Object[] konstante_data;
        final String Naam;
        final List<lid_data> veld_VALUE, funksie_VALUE;
        Klas_data(Path Pad) throws IOException {
            data_Leser Leser_VALUE = new data_Leser(Files.readAllBytes(Pad));
            if (Leser_VALUE.네바이트() != 0xcafebabe) throw new Vertaling_fout("Java Klas_VALUE 표식이 아님");
            Leser_VALUE.Lees(4);
            int item_COUNT = Leser_VALUE.두바이트(); 상수종류 = new int[item_COUNT]; konstante_data = new Object[item_COUNT];
            for (int 순번 = 1; 순번 < item_COUNT; 순번++) {
                int 종류 = Leser_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int lengte_VALUE = Leser_VALUE.두바이트();
                        byte[] karakter_buffer = Leser_VALUE.Lees(lengte_VALUE), 길이붙인자료 = new byte[lengte_VALUE + 2];
                        길이붙인자료[0] = (byte)(lengte_VALUE >> 8); 길이붙인자료[1] = (byte)lengte_VALUE;
                        System.arraycopy(karakter_buffer, 0, 길이붙인자료, 2, lengte_VALUE);
                        konstante_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstante_data[순번] = Leser_VALUE.네바이트(); break;
                    case 4: Leser_VALUE.Lees(4); break;
                    case 5: case 6: Leser_VALUE.Lees(8); 순번++; break;
                    case 7: case 8: case 16: konstante_data[순번] = Leser_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstante_data[순번] = new int[]{Leser_VALUE.두바이트(), Leser_VALUE.두바이트()}; break;
                    case 15: konstante_data[순번] = new int[]{Leser_VALUE.한바이트(), Leser_VALUE.두바이트()}; break;
                    default: throw new Vertaling_fout("지원하지 않는 konstante_VALUE 종류: " + 종류);
                }
            }
            Leser_VALUE.두바이트(); Naam = Klas_naam(Leser_VALUE.두바이트());
            if (!Klas_naam(Leser_VALUE.두바이트()).equals("java/lang/Object") || Leser_VALUE.두바이트() != 0)
                throw new Vertaling_fout(Naam + ": 상속 및 인터페이스 미지원");
            veld_VALUE = 멤버읽기(Leser_VALUE); funksie_VALUE = 멤버읽기(Leser_VALUE); 속성읽기(Leser_VALUE);
            if (Leser_VALUE.Posisie != Leser_VALUE.data.length) throw new Vertaling_fout("Klas_VALUE 뒤에 남은 data");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Vertaling_fout("문자 konstante_VALUE INDEX Fout");
            return (String) konstante_data[INDEX];
        }
        String Klas_naam(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Vertaling_fout("Klas_VALUE Naslaan Fout");
            return 문자((Integer)konstante_data[INDEX]);
        }
        metode_Naslaan Naslaan(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Vertaling_fout("멤버 Naslaan Fout");
            int[] paar_VALUE = (int[])konstante_data[INDEX], naam_paar = (int[])konstante_data[paar_VALUE[1]];
            return new metode_Naslaan(Klas_naam(paar_VALUE[0]), 문자(naam_paar[0]), 문자(naam_paar[1]));
        }
        Map<String, byte[]> 속성읽기(data_Leser Leser_VALUE) {
            Map<String, byte[]> maatreël = new LinkedHashMap<>();
            int item_COUNT = Leser_VALUE.두바이트();
            for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                String kenmerk_naam = 문자(Leser_VALUE.두바이트()); byte[] VALUE = Leser_VALUE.Lees(Leser_VALUE.네바이트());
                if (maatreël.put(kenmerk_naam, VALUE) != null) throw new Vertaling_fout("겹친 kenmerk_VALUE: " + kenmerk_naam);
            }
            return maatreël;
        }
        List<lid_data> 멤버읽기(data_Leser Leser_VALUE) {
            List<lid_data> maatreël = new ArrayList<>(); int item_COUNT = Leser_VALUE.두바이트();
            for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                int toegang_inskrywing = Leser_VALUE.두바이트(); String metode_inskrywing_naam = 문자(Leser_VALUE.두바이트()), 서술 = 문자(Leser_VALUE.두바이트());
                maatreël.add(new lid_data(toegang_inskrywing, metode_inskrywing_naam, 서술, 속성읽기(Leser_VALUE)));
            }
            return maatreël;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String teruggee_maatreël;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Vertaling_fout("funksie_VALUE 서술 Fout: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Vertaling_fout("funksie_VALUE 서술 Fout: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Vertaling_fout("funksie_VALUE 서술 Fout: " + 서술);
            teruggee_maatreël = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> maatreël = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Posisie = 0; Posisie < 서술.length();) {
            String seleksie_VALUE = null;
            for (String formaat_VALUE : 허용형식) if (서술.startsWith(formaat_VALUE, Posisie)) { seleksie_VALUE = formaat_VALUE; break; }
            if (seleksie_VALUE == null) throw new Vertaling_fout("지원하지 않는 datatipe: " + 서술);
            maatreël.add(seleksie_VALUE); Posisie += seleksie_VALUE.length();
        }
        return maatreël;
    }
    static String simbool(String 종류, String... 부분들) {
        try {
            byte[] huts_lêer = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Teks = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Teks.append(String.format(Locale.ROOT, "%02x", huts_lêer[순번] & 255));
            return Teks.toString();
        } catch (Exception Fout) { throw new Vertaling_fout(Fout.toString()); }
    }
    final Map<String, Klas_data> 클래스들 = new TreeMap<>();
    final Map<metode_Naslaan, lid_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, masjien_Klas;
    final int 동적기억낱말수;
    final Path hulpbron_pad;
    기계어미리번역(List<Path> pad_Lys, String teiken, int 낱말수, Path hulpbron_VALUE) throws IOException {
        if ((!teiken.equals("kernel") && !teiken.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Vertaling_fout("uitvoer_bevel teiken 또는 Geheue_VALUE 공간 Grootte Fout");
        실행대상 = teiken; 동적기억낱말수 = 낱말수; hulpbron_pad = hulpbron_VALUE;
        // 이 이름도 국가별 bron_boom genereer 시 해당 언어로 옮긴다.
        masjien_Klas = teiken.equals("kernel") ? "bord" : "gebruiker";
        for (String lyn : Files.readAllLines(hulpbron_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = lyn.split("\t", -1);
            if (부분들.length != 4) throw new Vertaling_fout("masjien funksie_VALUE data Fout");
            if (부분들[0].equals(teiken)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Pad : pad_Lys) {
            Klas_data data = new Klas_data(Pad);
            if (클래스들.put(data.Naam, data) != null) throw new Vertaling_fout("중복 Klas_VALUE: " + data.Naam);
            for (lid_data veld_VALUE : data.veld_VALUE) {
                if ((veld_VALUE.toegang_inskrywing & 8) == 0 || 형식읽기(veld_VALUE.서술).equals(Collections.singletonList("V"))) throw new Vertaling_fout("staties_VALUE 필드만 Bystand_VALUE");
                if (필드들.put(new metode_Naslaan(data.Naam, veld_VALUE.Naam, veld_VALUE.서술), veld_VALUE) != null) throw new Vertaling_fout("중복 veld_VALUE");
            }
            for (lid_data funksie_VALUE : data.funksie_VALUE) {
                if (funksie_VALUE.Naam.equals("<init>")) continue;
                if ((funksie_VALUE.toegang_inskrywing & 8) == 0 || (funksie_VALUE.toegang_inskrywing & (0x20 | 0x400)) != 0) throw new Vertaling_fout("staties_VALUE 비동기화 함수만 Bystand_VALUE");
                new 함수형식(funksie_VALUE.서술);
                if (함수들.put(new metode_Naslaan(data.Naam, funksie_VALUE.Naam, funksie_VALUE.서술), funksie_VALUE) != null) throw new Vertaling_fout("중복 funksie_VALUE");
            }
        }
    }
    String string_simbool(String Teks) { return 문자열들.computeIfAbsent(Teks, VALUE -> "j_text_" + 문자열들.size()); }
    String konstante_uitdrukking(Klas_data data, int INDEX) {
        if (INDEX < 1 || INDEX >= data.상수종류.length) throw new Vertaling_fout("konstante_VALUE INDEX snit Fout");
        if (data.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + data.konstante_data[INDEX] + ")";
        if (data.상수종류[INDEX] == 8) return "(word)" + string_simbool(data.문자((Integer)data.konstante_data[INDEX]));
        throw new Vertaling_fout("정수와 string_VALUE 상수만 Bystand_VALUE");
    }
    String 함수원형(metode_Naslaan Naslaan) {
        List<String> 인수들 = new ArrayList<>(); int item_COUNT = new 함수형식(Naslaan.서술).인수.size();
        for (int 순번 = 0; 순번 < item_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbool("method", Naslaan.부분들()) + "(" + (item_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void tjek_lokaal(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Vertaling_fout("lokaal_bestek 변수 INDEX snit Fout"); }
    void 분기넣기(List<String> Afvoer, Set<Integer> tak_Lys, int Posisie, int 이동량, String toestand) {
        int bestemming_VALUE = Posisie + 이동량; tak_Lys.add(bestemming_VALUE);
        Afvoer.add((toestand == null ? "" : "if (" + toestand + ") ") + "goto b" + bestemming_VALUE + ";");
    }
    String 함수본문(metode_Naslaan funksie_VALUE, lid_data data) {
        byte[] 본문자료 = data.kenmerk_VALUE.get("Code"); if (본문자료 == null) throw new Vertaling_fout("funksie_VALUE 몸체가 없음: " + funksie_VALUE.Naam);
        data_Leser Leser_VALUE = new data_Leser(본문자료); int 쌓임깊이 = Leser_VALUE.두바이트(), 지역변수수 = Leser_VALUE.두바이트();
        data_Leser bevel_data = new data_Leser(Leser_VALUE.Lees(Leser_VALUE.네바이트()));
        if (Leser_VALUE.두바이트() != 0) throw new Vertaling_fout("try/catch/finally 미지원");
        함수형식 formaat_VALUE = new 함수형식(funksie_VALUE.서술); if (지역변수수 < formaat_VALUE.인수.size()) throw new Vertaling_fout("매개변수보다 적은 lokaal_bestek 변수");
        Klas_data Klas_VALUE = 클래스들.get(funksie_VALUE.eienaar_VALUE);
        List<String> Afvoer = new ArrayList<>(); Afvoer.add(함수원형(funksie_VALUE) + " {");
        Afvoer.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formaat_VALUE.인수.size(); 순번++) Afvoer.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), tak_Lys = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (bevel_data.Posisie < bevel_data.data.length) {
            int Posisie = bevel_data.Posisie, Opdrag = bevel_data.한바이트(); 경계들.add(Posisie); Afvoer.add("b" + Posisie + ":;");
            if (Opdrag == 0) continue;
            if (Opdrag == 1) Afvoer.add("PUSH(0);");
            else if (Opdrag >= 2 && Opdrag <= 8) Afvoer.add("PUSH((uint32_t)(" + (Opdrag - 3) + "));");
            else if (Opdrag == 16 || Opdrag == 17) Afvoer.add("PUSH((uint32_t)(" + (Opdrag == 16 ? bevel_data.부호한바이트() : bevel_data.부호두바이트()) + "));");
            else if (Opdrag == 18 || Opdrag == 19) Afvoer.add("PUSH(" + konstante_uitdrukking(Klas_VALUE, Opdrag == 18 ? bevel_data.한바이트() : bevel_data.두바이트()) + ");");
            else if (Opdrag == 21 || Opdrag == 25 || (Opdrag >= 26 && Opdrag <= 29) || (Opdrag >= 42 && Opdrag <= 45)) {
                int INDEX = Opdrag == 21 || Opdrag == 25 ? bevel_data.한바이트() : Opdrag - (Opdrag <= 29 ? 26 : 42);
                tjek_lokaal(INDEX, 지역변수수); Afvoer.add("PUSH(l[" + INDEX + "]);");
            } else if (Opdrag == 54 || Opdrag == 58 || (Opdrag >= 59 && Opdrag <= 62) || (Opdrag >= 75 && Opdrag <= 78)) {
                int INDEX = Opdrag == 54 || Opdrag == 58 ? bevel_data.한바이트() : Opdrag - (Opdrag <= 62 ? 59 : 75);
                tjek_lokaal(INDEX, 지역변수수); Afvoer.add("l[" + INDEX + "] = POP();");
            } else if (Opdrag == 46) Afvoer.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Opdrag == 79) Afvoer.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Opdrag == 87 || Opdrag == 88) Afvoer.add(Opdrag == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Opdrag >= 89 && Opdrag <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] volgorde_Lys = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Opdrag - 89]; 순번++) Afvoer.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : volgorde_Lys[Opdrag - 89].toCharArray()) Afvoer.add("PUSH(" + VALUE + ");");
            } else if (Opdrag == 96 || Opdrag == 100 || Opdrag == 104 || Opdrag == 126 || Opdrag == 128 || Opdrag == 130) {
                String werking_VALUE = Opdrag == 96 ? "+" : Opdrag == 100 ? "-" : Opdrag == 104 ? "*" : Opdrag == 126 ? "&" : Opdrag == 128 ? "|" : "^";
                Afvoer.add("b = POP(); a = POP(); PUSH((uint32_t)a " + werking_VALUE + " (uint32_t)b);");
            } else if (Opdrag == 108 || Opdrag == 112) Afvoer.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Opdrag == 112 ? 1 : 0) + "));");
            else if (Opdrag == 116) Afvoer.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Opdrag == 120 || Opdrag == 122 || Opdrag == 124) {
                Afvoer.add("b = POP(); a = POP();"); Afvoer.add("PUSH(" + (Opdrag == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Opdrag == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Opdrag == 132) {
                int INDEX = bevel_data.한바이트(), 증가량 = bevel_data.부호한바이트(); tjek_lokaal(INDEX, 지역변수수);
                Afvoer.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Opdrag >= 145 && Opdrag <= 147) Afvoer.add("a = POP(); PUSH((uint32_t)(" + (Opdrag == 145 ? "int8_t" : Opdrag == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Opdrag >= 153 && Opdrag <= 158) {
                Afvoer.add("a = POP();"); 분기넣기(Afvoer, tak_Lys, Posisie, bevel_data.부호두바이트(), "(int32_t)a " + 비교들[Opdrag - 153] + " 0");
            } else if (Opdrag >= 159 && Opdrag <= 166) {
                Afvoer.add("b = POP(); a = POP();"); 분기넣기(Afvoer, tak_Lys, Posisie, bevel_data.부호두바이트(), Opdrag >= 165 ? "a " + 비교들[Opdrag - 159] + " b" : "(int32_t)a " + 비교들[Opdrag - 159] + " (int32_t)b");
            } else if (Opdrag == 167 || Opdrag == 200) 분기넣기(Afvoer, tak_Lys, Posisie, Opdrag == 167 ? bevel_data.부호두바이트() : bevel_data.네바이트(), null);
            else if (Opdrag == 170 || Opdrag == 171) {
                while (bevel_data.Posisie % 4 != 0) bevel_data.한바이트();
                int verstekwaarde = bevel_data.네바이트(); Afvoer.add("a = POP();");
                if (Opdrag == 170) {
                    int 아래 = bevel_data.네바이트(), 위 = bevel_data.네바이트(); long item_COUNT = (long)위 - 아래 + 1;
                    if (item_COUNT < 1 || item_COUNT > (bevel_data.data.length - bevel_data.Posisie) / 4) throw new Vertaling_fout("switch snit Fout");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Afvoer, tak_Lys, Posisie, bevel_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int item_COUNT = bevel_data.네바이트(), voor_data = 0;
                    if (item_COUNT < 0 || item_COUNT > (bevel_data.data.length - bevel_data.Posisie) / 8) throw new Vertaling_fout("switch Grootte Fout");
                    for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                        int VALUE = bevel_data.네바이트(); if (순번 > 0 && VALUE <= voor_data) throw new Vertaling_fout("switch volgorde_VALUE Fout"); voor_data = VALUE;
                        분기넣기(Afvoer, tak_Lys, Posisie, bevel_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Afvoer, tak_Lys, Posisie, verstekwaarde, null);
            } else if (Opdrag == 172 || Opdrag == 176 || Opdrag == 177) Afvoer.add("return " + (Opdrag == 177 ? "0" : "POP()") + ";");
            else if (Opdrag == 178 || Opdrag == 179) {
                metode_Naslaan Naslaan = Klas_VALUE.Naslaan(bevel_data.두바이트()); if (!필드들.containsKey(Naslaan)) throw new Vertaling_fout("알 수 없는 veld_VALUE");
                Afvoer.add(simbool("init", Naslaan.eienaar_VALUE) + "();"); String veld_VALUE = simbool("field", Naslaan.부분들());
                Afvoer.add(Opdrag == 178 ? "PUSH(" + veld_VALUE + ");" : veld_VALUE + " = POP();");
            } else if (Opdrag == 184) {
                metode_Naslaan Naslaan = Klas_VALUE.Naslaan(bevel_data.두바이트()); if (!함수들.containsKey(Naslaan)) throw new Vertaling_fout("알 수 없는 funksie_VALUE");
                함수형식 호출형식 = new 함수형식(Naslaan.서술); int item_COUNT = 호출형식.인수.size();
                Afvoer.add(simbool("init", Naslaan.eienaar_VALUE) + "();"); Afvoer.add("if(sp < " + item_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + item_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < item_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Afvoer.add("a = " + simbool("method", Naslaan.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.teruggee_maatreël.equals("V")) Afvoer.add("PUSH(a);");
            } else if (Opdrag == 182) {
                metode_Naslaan Naslaan = Klas_VALUE.Naslaan(bevel_data.두바이트());
                if (Naslaan.equals(new metode_Naslaan("java/lang/String", "length", "()I"))) Afvoer.add("a = POP(); PUSH(length(a));");
                else if (Naslaan.equals(new metode_Naslaan("java/lang/String", "charAt", "(I)C"))) Afvoer.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Vertaling_fout("가상 funksie_VALUE 호출 미지원");
            } else if (Opdrag == 188) {
                if (bevel_data.한바이트() != 10) throw new Vertaling_fout("new int[]만 Bystand_VALUE"); Afvoer.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Opdrag == 190) Afvoer.add("a = POP(); PUSH(length(a));");
            else if (Opdrag == 196) {
                int uitbreiding_VALUE = bevel_data.한바이트(), INDEX = bevel_data.두바이트(); tjek_lokaal(INDEX, 지역변수수);
                if (uitbreiding_VALUE == 21 || uitbreiding_VALUE == 25) Afvoer.add("PUSH(l[" + INDEX + "]);");
                else if (uitbreiding_VALUE == 54 || uitbreiding_VALUE == 58) Afvoer.add("l[" + INDEX + "] = POP();");
                else if (uitbreiding_VALUE == 132) Afvoer.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + bevel_data.부호두바이트() + ");");
                else throw new Vertaling_fout("미지원 wide Opdrag");
            } else if (Opdrag == 198 || Opdrag == 199) {
                Afvoer.add("a = POP();"); 분기넣기(Afvoer, tak_Lys, Posisie, bevel_data.부호두바이트(), "a " + (Opdrag == 198 ? "==" : "!=") + " 0");
            } else throw new Vertaling_fout(funksie_VALUE.eienaar_VALUE + "." + funksie_VALUE.Naam + ", greep_VALUE " + Posisie + ": 미지원 Opdrag " + Opdrag);
        }
        if (!경계들.containsAll(tak_Lys)) throw new Vertaling_fout("Opdrag 경계가 아닌 곳으로 tak");
        Afvoer.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Afvoer);
    }
    String uitvoer_metode(String Skakel_simbool, String teiken, boolean 진입점여부) {
        int plaas_INDEX = teiken.lastIndexOf('.'); if (plaas_INDEX < 0 || !Skakel_simbool.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Vertaling_fout("내보내기 toeken_VALUE Fout");
        String eienaar_VALUE = teiken.substring(0, plaas_INDEX).replace('.', '/'), Naam = teiken.substring(plaas_INDEX + 1); metode_Naslaan seleksie_VALUE = null;
        for (metode_Naslaan Naslaan : 함수들.keySet()) if (Naslaan.eienaar_VALUE.equals(eienaar_VALUE) && Naslaan.Naam.equals(Naam)) {
            if (seleksie_VALUE != null) throw new Vertaling_fout("겹친 내보내기 teiken"); seleksie_VALUE = Naslaan;
        }
        if (seleksie_VALUE == null || (함수들.get(seleksie_VALUE).toegang_inskrywing & 0x100) != 0) throw new Vertaling_fout("내보낼 함수가 없음 또는 native funksie_VALUE");
        함수형식 formaat_VALUE = new 함수형식(seleksie_VALUE.서술);
        if ((진입점여부 && !formaat_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(formaat_VALUE.teruggee_maatreël)) throw new Vertaling_fout("inskrywing_p_VALUE 또는 C 경계 formaat_VALUE Fout");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formaat_VALUE.인수.size(); 순번++) {
            if (!formaat_VALUE.인수.get(순번).equals("I")) throw new Vertaling_fout("C 경계는 int 인수만 Bystand_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formaat_VALUE.teruggee_maatreël.equals("V") ? "void " : "int32_t ") + Skakel_simbool + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbool("init", seleksie_VALUE.eienaar_VALUE) + "(); " + (formaat_VALUE.teruggee_maatreël.equals("V") ? "" : "return (int32_t)") + simbool("method", seleksie_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String genereer(String inskrywing_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metode_Naslaan, lid_data> inskrywing_VALUE : 함수들.entrySet()) {
            metode_Naslaan Naslaan = inskrywing_VALUE.getKey(); lid_data data = inskrywing_VALUE.getValue(); 선언들.add(함수원형(Naslaan) + ";");
            if ((data.toegang_inskrywing & 0x100) != 0) {
                String Koppel = 기계함수들.get(Naslaan.Naam + Naslaan.서술);
                if (!Naslaan.eienaar_VALUE.equals(masjien_Klas) || Koppel == null) throw new Vertaling_fout("허용되지 않은 native funksie_VALUE: " + Naslaan.Naam);
                int item_COUNT = new 함수형식(Naslaan.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < item_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Koppel + "(" + (item_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(item_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Naslaan) + " { return " + Koppel + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Naslaan, data));
        }
        for (Map.Entry<metode_Naslaan, lid_data> inskrywing_VALUE : 필드들.entrySet()) {
            metode_Naslaan Naslaan = inskrywing_VALUE.getKey(); byte[] konstante_VALUE = inskrywing_VALUE.getValue().kenmerk_VALUE.get("ConstantValue");
            String VALUE = konstante_VALUE == null ? "0" : konstante_uitdrukking(클래스들.get(Naslaan.eienaar_VALUE), new data_Leser(konstante_VALUE).두바이트());
            필드선언들.add("static word " + simbool("field", Naslaan.부분들()) + " = " + VALUE + ";");
        }
        for (String Naam : 클래스들.keySet()) {
            String inisialiseer = simbool("init", Naam), stand_VALUE = simbool("state", Naam);
            선언들.add("static void " + inisialiseer + "(void);"); 필드선언들.add("static unsigned " + stand_VALUE + ";");
            metode_Naslaan Naslaan = new metode_Naslaan(Naam, "<clinit>", "()V");
            몸체들.add("static void " + inisialiseer + "(void) { if(" + stand_VALUE + ") return; " + stand_VALUE + " = 1; " + (함수들.containsKey(Naslaan) ? simbool("method", Naslaan.부분들()) + "(); " : "") + stand_VALUE + " = 2; }");
        }
        몸체들.add(uitvoer_metode("java_entry", inskrywing_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String toeken_VALUE : 내보내기목록) {
            int plaas_INDEX = toeken_VALUE.indexOf('='); if (plaas_INDEX < 1) throw new Vertaling_fout("내보내기 toeken_VALUE Fout");
            String Naam = toeken_VALUE.substring(0, plaas_INDEX); 공개이름.add(Naam); 몸체들.add(uitvoer_metode(Naam, toeken_VALUE.substring(plaas_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> inskrywing_VALUE : 문자열들.entrySet()) {
            String Teks = inskrywing_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + inskrywing_VALUE.getValue() + "[] = {" + Teks.length());
            for (int 순번 = 0; 순번 < Teks.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Teks.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Bystand_VALUE = Files.readString(hulpbron_pad.resolve("algemene_taallooptyd_Bystand.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Bystand_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String Bron, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> naam_tabel = new HashMap<>();
        for (String lyn : Files.readAllLines(hulpbron_pad.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] paar_VALUE = lyn.split("\t"); naam_tabel.put(paar_VALUE[0], paar_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(Bron); StringBuffer maatreël = new StringBuffer();
        while (찾개.find()) {
            String Naam = 찾개.group(), 새이름 = Naam;
            if (!Naam.startsWith("//") && !Naam.startsWith("/*") && !Naam.startsWith("\"") && !Naam.startsWith("'") && !공개이름.contains(Naam)) {
                새이름 = naam_tabel.getOrDefault(Naam, Naam);
                if (Naam.matches("a[0-9]+")) 새이름 = "인수" + Naam.substring(1);
                if (Naam.matches("b[0-9]+")) 새이름 = "tak" + Naam.substring(1);
                if (범용표기) {
                    StringBuilder notasie_VALUE = new StringBuilder();
                    for (char karakter_VALUE : 새이름.toCharArray()) notasie_VALUE.append(karakter_VALUE < 128 ? Character.toString(karakter_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)karakter_VALUE));
                    새이름 = notasie_VALUE.toString();
                }
            }
            찾개.appendReplacement(maatreël, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(maatreël); return maatreël.toString();
    }
    String 엑스함수본문(metode_Naslaan funksie_VALUE, lid_data data, Map<String,String> masjien_tabel, String teiken) {
        String 표식 = simbool("method", funksie_VALUE.부분들());
        List<String> lyn = new ArrayList<>();
        if ((data.toegang_inskrywing & 0x100) != 0) {
            String Koppel = masjien_tabel.get(funksie_VALUE.Naam + funksie_VALUE.서술);
            if (!funksie_VALUE.eienaar_VALUE.equals(teiken.equals("kernel") ? "mobiel_VALUE" : "gebruiker") || Koppel == null) throw new Vertaling_fout("허용되지 않은 native funksie_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Koppel;
        }
        byte[] inhoudteks = data.kenmerk_VALUE.get("Code"); if (inhoudteks == null) throw new Vertaling_fout("funksie_VALUE 몸체가 없음");
        data_Leser Leser_VALUE = new data_Leser(inhoudteks); Leser_VALUE.두바이트(); int lokaal_COUNT = Leser_VALUE.두바이트();
        data_Leser bevel_data = new data_Leser(Leser_VALUE.Lees(Leser_VALUE.네바이트()));
        if (Leser_VALUE.두바이트() != 0) throw new Vertaling_fout("try/catch/finally 미지원");
        함수형식 formaat_VALUE = new 함수형식(funksie_VALUE.서술); if (lokaal_COUNT < formaat_VALUE.인수.size()) throw new Vertaling_fout("매개변수보다 적은 lokaal_bestek 변수");
        Collections.addAll(lyn,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokaal_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formaat_VALUE.인수.size(); 순번++) Collections.addAll(lyn,"movl " + (8 + 4 * (formaat_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Klas_data Klas_VALUE = 클래스들.get(funksie_VALUE.eienaar_VALUE); Set<Integer> 경계들 = new HashSet<>(), tak_Lys = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (bevel_data.Posisie < bevel_data.data.length) {
            int Posisie = bevel_data.Posisie, Opdrag = bevel_data.한바이트(); String plaas_INDEX = 표식 + "_b" + Posisie;
            lyn.add(plaas_INDEX + ":"); 경계들.add(Posisie);
            if (Opdrag == 0) lyn.add("nop");
            else if (Opdrag == 1) lyn.add("pushl $0");
            else if (Opdrag >= 2 && Opdrag <= 8) lyn.add("pushl $" + (Opdrag - 3));
            else if (Opdrag == 16 || Opdrag == 17) lyn.add("pushl $" + (Opdrag == 16 ? bevel_data.부호한바이트() : bevel_data.부호두바이트()));
            else if (Opdrag == 18 || Opdrag == 19) {
                int INDEX = Opdrag == 18 ? bevel_data.한바이트() : bevel_data.두바이트();
                lyn.add("pushl $" + X_86_konstante(Klas_VALUE,INDEX));
            } else if (Opdrag == 21 || Opdrag == 25 || (Opdrag >= 26 && Opdrag <= 29) || (Opdrag >= 42 && Opdrag <= 45) || Opdrag == 54 || Opdrag == 58 || (Opdrag >= 59 && Opdrag <= 62) || (Opdrag >= 75 && Opdrag <= 78)) {
                boolean 읽음 = Opdrag < 54; int INDEX = Opdrag == 21 || Opdrag == 25 || Opdrag == 54 || Opdrag == 58 ? bevel_data.한바이트() : Opdrag - (Opdrag <= 29 ? 26 : Opdrag <= 45 ? 42 : Opdrag <= 62 ? 59 : 75);
                tjek_lokaal(INDEX,lokaal_COUNT); lyn.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Opdrag == 46) Collections.addAll(lyn,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Opdrag == 79) Collections.addAll(lyn,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Opdrag == 87 || Opdrag == 88) lyn.add("addl $" + (Opdrag == 87 ? 4 : 8) + ", %esp");
            else if (Opdrag >= 89 && Opdrag <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] volgorde_Lys = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Opdrag - 89]; 순번++) lyn.add("popl " + 저장기들[순번]);
                for (int 순번 : volgorde_Lys[Opdrag - 89]) lyn.add("pushl " + 저장기들[순번]);
            } else if (Opdrag == 96 || Opdrag == 100 || Opdrag == 104 || Opdrag == 126 || Opdrag == 128 || Opdrag == 130) {
                String werking_VALUE = Opdrag == 96 ? "addl" : Opdrag == 100 ? "subl" : Opdrag == 104 ? "imull" : Opdrag == 126 ? "andl" : Opdrag == 128 ? "orl" : "xorl";
                Collections.addAll(lyn,"popl %ecx","popl %eax",werking_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Opdrag == 108 || Opdrag == 112) Collections.addAll(lyn,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + plaas_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + plaas_INDEX + "_divide","xorl %edx, %edx","jmp " + plaas_INDEX + "_done",plaas_INDEX + "_divide:","cltd","idivl %ecx",plaas_INDEX + "_done:","pushl " + (Opdrag == 108 ? "%eax" : "%edx"));
            else if (Opdrag == 116) lyn.add("negl (%esp)");
            else if (Opdrag == 120 || Opdrag == 122 || Opdrag == 124) Collections.addAll(lyn,"popl %ecx","popl %eax",(Opdrag == 120 ? "sall" : Opdrag == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Opdrag == 132) {
                int INDEX = bevel_data.한바이트(), 증가 = bevel_data.부호한바이트(); tjek_lokaal(INDEX,lokaal_COUNT); lyn.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Opdrag >= 145 && Opdrag <= 147) Collections.addAll(lyn,"popl %eax",Opdrag == 145 ? "movsbl %al, %eax" : Opdrag == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Opdrag >= 153 && Opdrag <= 166) {
                if (Opdrag <= 158) Collections.addAll(lyn,"popl %eax","testl %eax, %eax");
                else Collections.addAll(lyn,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int bestemming_VALUE = Posisie + bevel_data.부호두바이트(); tak_Lys.add(bestemming_VALUE); lyn.add(비교들[Opdrag - (Opdrag <= 158 ? 153 : 159)] + " " + 표식 + "_b" + bestemming_VALUE);
            } else if (Opdrag == 167 || Opdrag == 200) {
                int bestemming_VALUE = Posisie + (Opdrag == 167 ? bevel_data.부호두바이트() : bevel_data.네바이트()); tak_Lys.add(bestemming_VALUE); lyn.add("jmp " + 표식 + "_b" + bestemming_VALUE);
            } else if (Opdrag == 170 || Opdrag == 171) {
                while (bevel_data.Posisie % 4 != 0) bevel_data.한바이트();
                int verstekwaarde = Posisie + bevel_data.네바이트(); tak_Lys.add(verstekwaarde); lyn.add("popl %eax");
                int item_COUNT, 아래 = 0;
                if (Opdrag == 170) { 아래 = bevel_data.네바이트(); int 위 = bevel_data.네바이트(); long lengte_VALUE = (long)위 - 아래 + 1; if (lengte_VALUE < 1 || lengte_VALUE > (bevel_data.data.length - bevel_data.Posisie) / 4) throw new Vertaling_fout("switch snit Fout"); item_COUNT = (int)lengte_VALUE; }
                else { item_COUNT = bevel_data.네바이트(); if (item_COUNT < 0 || item_COUNT > (bevel_data.data.length - bevel_data.Posisie) / 8) throw new Vertaling_fout("switch Grootte Fout"); }
                for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                    int VALUE = Opdrag == 170 ? 아래 + 순번 : bevel_data.네바이트(), bestemming_VALUE = Posisie + bevel_data.네바이트(); tak_Lys.add(bestemming_VALUE);
                    Collections.addAll(lyn,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + bestemming_VALUE);
                }
                lyn.add("jmp " + 표식 + "_b" + verstekwaarde);
            } else if (Opdrag == 172 || Opdrag == 176 || Opdrag == 177) {
                if (Opdrag != 177) lyn.add("popl %eax"); Collections.addAll(lyn,"leave","ret");
            } else if (Opdrag == 178 || Opdrag == 179) {
                metode_Naslaan Naslaan = Klas_VALUE.Naslaan(bevel_data.두바이트()); if (!필드들.containsKey(Naslaan)) throw new Vertaling_fout("알 수 없는 veld_VALUE");
                Collections.addAll(lyn,"call " + simbool("init",Naslaan.eienaar_VALUE),(Opdrag == 178 ? "pushl " : "popl ") + simbool("field",Naslaan.부분들()));
            } else if (Opdrag == 184) {
                metode_Naslaan Naslaan = Klas_VALUE.Naslaan(bevel_data.두바이트()); if (!함수들.containsKey(Naslaan)) throw new Vertaling_fout("알 수 없는 funksie_VALUE");
                함수형식 호출형식 = new 함수형식(Naslaan.서술); Collections.addAll(lyn,"call " + simbool("init",Naslaan.eienaar_VALUE),"call " + simbool("method",Naslaan.부분들()));
                if (!호출형식.인수.isEmpty()) lyn.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.teruggee_maatreël.equals("V")) lyn.add("pushl %eax");
            } else if (Opdrag == 182) {
                metode_Naslaan Naslaan = Klas_VALUE.Naslaan(bevel_data.두바이트());
                if (Naslaan.equals(new metode_Naslaan("java/lang/String","length","()I"))) Collections.addAll(lyn,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Naslaan.equals(new metode_Naslaan("java/lang/String","charAt","(I)C"))) Collections.addAll(lyn,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Vertaling_fout("가상 funksie_VALUE 호출 미지원");
            } else if (Opdrag == 188) {
                if (bevel_data.한바이트() != 10) throw new Vertaling_fout("new int[]만 Bystand_VALUE"); Collections.addAll(lyn,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Opdrag == 190) Collections.addAll(lyn,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Opdrag == 196) {
                int uitbreiding_VALUE = bevel_data.한바이트(), INDEX = bevel_data.두바이트(); tjek_lokaal(INDEX,lokaal_COUNT);
                if (uitbreiding_VALUE == 21 || uitbreiding_VALUE == 25 || uitbreiding_VALUE == 54 || uitbreiding_VALUE == 58) lyn.add((uitbreiding_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (uitbreiding_VALUE == 132) lyn.add("addl $" + bevel_data.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Vertaling_fout("wide Opdrag 미지원");
            } else if (Opdrag == 198 || Opdrag == 199) {
                int bestemming_VALUE = Posisie + bevel_data.부호두바이트(); tak_Lys.add(bestemming_VALUE); Collections.addAll(lyn,"popl %eax","testl %eax, %eax",(Opdrag == 198 ? "je " : "jne ") + 표식 + "_b" + bestemming_VALUE);
            } else throw new Vertaling_fout("미지원 Opdrag: " + Opdrag);
        }
        if (!경계들.containsAll(tak_Lys)) throw new Vertaling_fout("Opdrag 경계가 아닌 곳으로 tak");
        lyn.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",lyn);
    }
    String X_86_konstante(Klas_data data, int INDEX) {
        if (data.상수종류[INDEX] == 3) return data.konstante_data[INDEX].toString();
        if (data.상수종류[INDEX] == 8) return string_simbool(data.문자((Integer)data.konstante_data[INDEX]));
        throw new Vertaling_fout("정수와 string_VALUE 상수만 Bystand_VALUE");
    }
    String 엑스조립본(String inskrywing_p, List<String> 내보냄, String teiken) throws IOException {
        Map<String,String> masjien_tabel = new HashMap<>();
        for (String lyn : Files.readAllLines(hulpbron_pad.resolve("엑스기계함수.tsv"))) { String[] paar_VALUE = lyn.split("\t"); if (paar_VALUE[0].equals(teiken)) masjien_tabel.put(paar_VALUE[1] + paar_VALUE[2],paar_VALUE[3]); }
        int plaas_INDEX = inskrywing_p.lastIndexOf('.'); if (plaas_INDEX < 0) throw new Vertaling_fout("inskrywing_p toeken_VALUE Fout");
        String eienaar_VALUE = inskrywing_p.substring(0,plaas_INDEX).replace('.','/'), metode_inskrywing_naam = inskrywing_p.substring(plaas_INDEX + 1); metode_Naslaan inskrywing_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metode_Naslaan Naslaan = new metode_Naslaan(eienaar_VALUE,metode_inskrywing_naam,서술); if (함수들.containsKey(Naslaan)) { if (inskrywing_p_VALUE != null) throw new Vertaling_fout("겹친 inskrywing_p"); inskrywing_p_VALUE = Naslaan; } }
        if (inskrywing_p_VALUE == null || (함수들.get(inskrywing_p_VALUE).toegang_inskrywing & 0x100) != 0) throw new Vertaling_fout("inskrywing_p_VALUE funksie_VALUE formaat_VALUE Fout");
        List<String> lyn = new ArrayList<>(); lyn.add(".code32");
        for (Klas_data data : 클래스들.values()) {
            String stand_VALUE = simbool("state",data.Naam), inisialiseer = simbool("init",data.Naam);
            Collections.addAll(lyn,".bss",".balign 4",stand_VALUE + ": .long 0",".text",inisialiseer + ":","cmpl $0, " + stand_VALUE,"jne " + inisialiseer + "_done","movl $1, " + stand_VALUE);
            metode_Naslaan 초기화참조 = new metode_Naslaan(data.Naam,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) lyn.add("call " + simbool("method",초기화참조.부분들()));
            Collections.addAll(lyn,"movl $2, " + stand_VALUE,inisialiseer + "_done:","ret");
            for (lid_data veld_VALUE : data.veld_VALUE) {
                byte[] konstante_VALUE = veld_VALUE.kenmerk_VALUE.get("ConstantValue"); String VALUE = konstante_VALUE == null ? "0" : X_86_konstante(data,new data_Leser(konstante_VALUE).두바이트());
                Collections.addAll(lyn,".data",".balign 4",simbool("field",data.Naam,veld_VALUE.Naam,veld_VALUE.서술) + ": .long " + VALUE);
            }
            for (lid_data funksie_VALUE : data.funksie_VALUE) if (!funksie_VALUE.Naam.equals("<init>")) lyn.add(엑스함수본문(new metode_Naslaan(data.Naam,funksie_VALUE.Naam,funksie_VALUE.서술),funksie_VALUE,masjien_tabel,teiken));
        }
        Collections.addAll(lyn,".text",".globl java_entry","java_entry:","call " + simbool("init",inskrywing_p_VALUE.eienaar_VALUE),"call " + simbool("method",inskrywing_p_VALUE.부분들()));
        if (inskrywing_p_VALUE.서술.equals("()V")) lyn.add("xorl %eax, %eax"); lyn.add("ret");
        for (String toeken_VALUE : 내보냄) {
            int skeier_VALUE = toeken_VALUE.indexOf('='); if (skeier_VALUE < 1) throw new Vertaling_fout("내보내기 toeken_VALUE Fout");
            String 외부 = toeken_VALUE.substring(0,skeier_VALUE), funksie_VALUE = toeken_VALUE.substring(skeier_VALUE + 1); int deling_maatreël = funksie_VALUE.lastIndexOf('.');
            if (deling_maatreël < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Vertaling_fout("내보내기 simbool Fout");
            String Klas_VALUE = funksie_VALUE.substring(0,deling_maatreël).replace('.','/'), Naam = funksie_VALUE.substring(deling_maatreël + 1); metode_Naslaan seleksie_VALUE = null;
            for (metode_Naslaan Naslaan : 함수들.keySet()) if (Naslaan.eienaar_VALUE.equals(Klas_VALUE) && Naslaan.Naam.equals(Naam)) { if (seleksie_VALUE != null) throw new Vertaling_fout("겹친 내보내기 teiken"); seleksie_VALUE = Naslaan; }
            if (seleksie_VALUE == null) throw new Vertaling_fout("내보낼 함수가 없음");
            Collections.addAll(lyn,".text",".globl " + 외부,외부 + ":","call " + simbool("init",seleksie_VALUE.eienaar_VALUE),"jmp " + simbool("method",seleksie_VALUE.부분들()));
        }
        lyn.add(".section .rodata");
        for (Map.Entry<String,String> inskrywing_VALUE : 문자열들.entrySet()) {
            Collections.addAll(lyn,".balign 4",inskrywing_VALUE.getValue() + ":",".long " + inskrywing_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char les_VALUE : inskrywing_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(les_VALUE)); if (!단위들.isEmpty()) lyn.add(".long " + String.join(",",단위들));
        }
        lyn.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",lyn) + "\n";
    }
    static void uitvoer_nutsmiddel(List<String> Opdrag) throws Exception {
        if (new ProcessBuilder(Opdrag).inheritIO().start().waitFor() != 0) throw new Vertaling_fout("bou_bron Fout: " + Opdrag.get(0));
    }
    static String data_string(String Teks) { return "\"" + Teks.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Vertaling(List<Path> 입력들, String teiken, String inskrywing_p, List<String> 내보냄, Path Afvoer, Path hulpbron_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Klas_pad = 임시.resolve("classes"); Files.createDirectory(Klas_pad);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Klas_pad.toString(),"-sourcepath",Klas_pad.toString(),"-d",Klas_pad.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int bron_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Afvoer.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Vertaling_fout("Afvoer 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); bron_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Vertaling_fout(".java 또는 .class만 Bystand_VALUE");
            }
            if (bron_COUNT > 0) uitvoer_nutsmiddel(자바명령);
            try (java.util.stream.Stream<Path> pad_Lys = Files.walk(Klas_pad)) { pad_Lys.filter(Pad -> Pad.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,teiken.equals("user") ? "user" : "kernel",262144,hulpbron_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(inskrywing_p,내보냄,teiken); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path nutsmiddel_plaas = hulpbron_VALUE.getParent();
            uitvoer_nutsmiddel(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            uitvoer_nutsmiddel(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),nutsmiddel_plaas.resolve("algemene_taallooptyd_Bystand.s").toString()));
            List<String> Koppel = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (teiken.equals("kernel")) Koppel.add("-r");
            else {
                uitvoer_nutsmiddel(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),nutsmiddel_plaas.resolve(teiken.equals("user") ? "BEGIN_gebruiker_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(Koppel,"-e","_start",임시.resolve("start.o").toString());
                if (teiken.equals("user")) Collections.addAll(Koppel,"-T",nutsmiddel_plaas.resolve("gebruiker_Skakel_Uitleg.ld").toString());
            }
            Collections.addAll(Koppel,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); uitvoer_nutsmiddel(Koppel);
            Afvoer = Afvoer.toAbsolutePath(); Files.createDirectories(Afvoer.getParent()); Path publiseer_VALUE = Files.createTempFile(Afvoer.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publiseer_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(publiseer_VALUE,Afvoer,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publiseer_VALUE); }
            Files.setPosixFilePermissions(Afvoer,java.nio.file.attribute.PosixFilePermissions.fromString(teiken.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Afvoer + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbool_data = new ArrayList<>(), brondata = new ArrayList<>();
            for (metode_Naslaan Naslaan : CONVERT_VALUE.함수들.keySet()) simbool_data.add(data_string(simbool("method",Naslaan.부분들())) + ":" + data_string(Naslaan.eienaar_VALUE + "." + Naslaan.Naam + Naslaan.서술));
            for (Path 입력 : 입력들) {
                byte[] huts_lêer = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Teks = new StringBuilder(); for (byte VALUE : huts_lêer) Teks.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                brondata.add(data_string(입력.toAbsolutePath().toString()) + ":" + data_string(Teks.toString()));
            }
            Files.writeString(Paths.get(Afvoer + ".json"),"{\"target\":" + data_string(teiken) + ",\"entry\":" + data_string(inskrywing_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbool_data) + "},\"sources\":{" + String.join(",",brondata) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> pad_Lys = Files.walk(임시)) { for (Path Pad : (Iterable<Path>)pad_Lys.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Pad); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String inskrywing_p = null, teiken = "kernel", X_86_teiken = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> pad_Lys = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": X_86_teiken = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Klas_VALUE.funksie_VALUE -o Afvoer [--target linux|kernel|user] [--profile kernel|user] [--export simbool=Klas_VALUE.funksie_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": inskrywing_p = 인수[++순번]; break;
                    case "--profile": teiken = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Vertaling_fout("알 수 없는 옵션: " + VALUE); pad_Lys.add(Paths.get(VALUE));
                }
            }
            if (inskrywing_p == null || 출력경로 == null || pad_Lys.isEmpty()) throw new Vertaling_fout("--entry, -o, Klas_VALUE 파일이 필요합니다");
            Path hulpbron_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_teiken != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_teiken)) throw new Vertaling_fout("알 수 없는 uitvoer_bevel teiken");
                X_86_Vertaling(pad_Lys,X_86_teiken,inskrywing_p,내보냄,출력경로,hulpbron_VALUE); return;
            }
            String Bron = new 기계어미리번역(pad_Lys, teiken, 낱말수, hulpbron_VALUE).genereer(inskrywing_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, Bron, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Fout) { System.err.println("bou_bron Fout: " + Fout.getMessage()); System.exit(1); }
    }
}
