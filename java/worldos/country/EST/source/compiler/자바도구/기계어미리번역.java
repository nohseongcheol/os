// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java tund_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Tõlkimine_tõrge extends RuntimeException {
        Tõlkimine_tõrge(String 설명) { super(설명); }
    }
    static final class andmed_Reader {
        final byte[] andmed;
        int Asukoht;
        andmed_Reader(byte[] 입력자료) { andmed = 입력자료; }
        byte[] Lugemine(int 길이) {
            if (길이 < 0 || 길이 > andmed.length - Asukoht) throw new Tõlkimine_tõrge("잘린 tund_VALUE 또는 Käsk andmed");
            byte[] TULEMUS = Arrays.copyOfRange(andmed, Asukoht, Asukoht + 길이); Asukoht += 길이; return TULEMUS;
        }
        int 한바이트() { if (Asukoht >= andmed.length) throw new Tõlkimine_tõrge("잘린 Käsk andmed"); return andmed[Asukoht++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class liige_andmed {
        final int pöördus_kirje;
        final String Nimi_2, 서술;
        final Map<String, byte[]> atribuut_VALUE;
        liige_andmed(int pöördus_VALUE, String nimetus_VALUE, String 서술값, Map<String, byte[]> atribuut_andmed) {
            pöördus_kirje = pöördus_VALUE; Nimi_2 = nimetus_VALUE; 서술 = 서술값; atribuut_VALUE = atribuut_andmed;
        }
    }
    static final class meetod_viide implements Comparable<meetod_viide> {
        final String omanik_VALUE, Nimi_2, 서술;
        meetod_viide(String 소유값, String nimetus_VALUE, String 서술값) { omanik_VALUE = 소유값; Nimi_2 = nimetus_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{omanik_VALUE, Nimi_2, 서술}; }
        public int compareTo(meetod_viide partner_VALUE) {
            int Võrdlus_VALUE = omanik_VALUE.compareTo(partner_VALUE.omanik_VALUE);
            if (Võrdlus_VALUE == 0) Võrdlus_VALUE = Nimi_2.compareTo(partner_VALUE.Nimi_2);
            return Võrdlus_VALUE == 0 ? 서술.compareTo(partner_VALUE.서술) : Võrdlus_VALUE;
        }
        public boolean equals(Object partner_VALUE) { return partner_VALUE instanceof meetod_viide && compareTo((meetod_viide) partner_VALUE) == 0; }
        public int hashCode() { return Objects.hash(omanik_VALUE, Nimi_2, 서술); }
    }
    static final class tund_andmed {
        final int[] 상수종류;
        final Object[] konstant_andmed;
        final String Nimi_2;
        final List<liige_andmed> väljaväärtus, FUNCTION_VALUE;
        tund_andmed(Path RADA) throws IOException {
            andmed_Reader Reader_VALUE = new andmed_Reader(Files.readAllBytes(RADA));
            if (Reader_VALUE.네바이트() != 0xcafebabe) throw new Tõlkimine_tõrge("Java tund_VALUE 표식이 아님");
            Reader_VALUE.Lugemine(4);
            int kaup_COUNT = Reader_VALUE.두바이트(); 상수종류 = new int[kaup_COUNT]; konstant_andmed = new Object[kaup_COUNT];
            for (int 순번 = 1; 순번 < kaup_COUNT; 순번++) {
                int 종류 = Reader_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int 길이 = Reader_VALUE.두바이트();
                        byte[] märk_puhver = Reader_VALUE.Lugemine(길이), 길이붙인자료 = new byte[길이 + 2];
                        길이붙인자료[0] = (byte)(길이 >> 8); 길이붙인자료[1] = (byte)길이;
                        System.arraycopy(märk_puhver, 0, 길이붙인자료, 2, 길이);
                        konstant_andmed[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstant_andmed[순번] = Reader_VALUE.네바이트(); break;
                    case 4: Reader_VALUE.Lugemine(4); break;
                    case 5: case 6: Reader_VALUE.Lugemine(8); 순번++; break;
                    case 7: case 8: case 16: konstant_andmed[순번] = Reader_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstant_andmed[순번] = new int[]{Reader_VALUE.두바이트(), Reader_VALUE.두바이트()}; break;
                    case 15: konstant_andmed[순번] = new int[]{Reader_VALUE.한바이트(), Reader_VALUE.두바이트()}; break;
                    default: throw new Tõlkimine_tõrge("지원하지 않는 konstant_VALUE 종류: " + 종류);
                }
            }
            Reader_VALUE.두바이트(); Nimi_2 = klassinimi(Reader_VALUE.두바이트());
            if (!klassinimi(Reader_VALUE.두바이트()).equals("java/lang/Object") || Reader_VALUE.두바이트() != 0)
                throw new Tõlkimine_tõrge(Nimi_2 + ": 상속 및 인터페이스 미지원");
            väljaväärtus = 멤버읽기(Reader_VALUE); FUNCTION_VALUE = 멤버읽기(Reader_VALUE); 속성읽기(Reader_VALUE);
            if (Reader_VALUE.Asukoht != Reader_VALUE.andmed.length) throw new Tõlkimine_tõrge("tund_VALUE 뒤에 남은 andmed");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Tõlkimine_tõrge("문자 konstant_VALUE INDEX VIGA");
            return (String) konstant_andmed[INDEX];
        }
        String klassinimi(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Tõlkimine_tõrge("tund_VALUE viide VIGA");
            return 문자((Integer)konstant_andmed[INDEX]);
        }
        meetod_viide viide(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Tõlkimine_tõrge("멤버 viide VIGA");
            int[] siduma_VALUE = (int[])konstant_andmed[INDEX], nimetus_siduma = (int[])konstant_andmed[siduma_VALUE[1]];
            return new meetod_viide(klassinimi(siduma_VALUE[0]), 문자(nimetus_siduma[0]), 문자(nimetus_siduma[1]));
        }
        Map<String, byte[]> 속성읽기(andmed_Reader Reader_VALUE) {
            Map<String, byte[]> TULEMUS = new LinkedHashMap<>();
            int kaup_COUNT = Reader_VALUE.두바이트();
            for (int 순번 = 0; 순번 < kaup_COUNT; 순번++) {
                String atribuut_nimetus = 문자(Reader_VALUE.두바이트()); byte[] VALUE = Reader_VALUE.Lugemine(Reader_VALUE.네바이트());
                if (TULEMUS.put(atribuut_nimetus, VALUE) != null) throw new Tõlkimine_tõrge("겹친 atribuut_VALUE: " + atribuut_nimetus);
            }
            return TULEMUS;
        }
        List<liige_andmed> 멤버읽기(andmed_Reader Reader_VALUE) {
            List<liige_andmed> TULEMUS = new ArrayList<>(); int kaup_COUNT = Reader_VALUE.두바이트();
            for (int 순번 = 0; 순번 < kaup_COUNT; 순번++) {
                int pöördus_kirje = Reader_VALUE.두바이트(); String meetod_kirje_nimetus = 문자(Reader_VALUE.두바이트()), 서술 = 문자(Reader_VALUE.두바이트());
                TULEMUS.add(new liige_andmed(pöördus_kirje, meetod_kirje_nimetus, 서술, 속성읽기(Reader_VALUE)));
            }
            return TULEMUS;
        }
    }
    static final class 함수형식 {
        final List<String> Argumendid = new ArrayList<>();
        final String tagasi_saatma_näitaja;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Tõlkimine_tõrge("FUNCTION_VALUE 서술 VIGA: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Tõlkimine_tõrge("FUNCTION_VALUE 서술 VIGA: " + 서술);
            Argumendid.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumendid.contains("V") || 반환들.size() != 1) throw new Tõlkimine_tõrge("FUNCTION_VALUE 서술 VIGA: " + 서술);
            tagasi_saatma_näitaja = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> TULEMUS = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Asukoht = 0; Asukoht < 서술.length();) {
            String valim_VALUE = null;
            for (String vorming_VALUE : 허용형식) if (서술.startsWith(vorming_VALUE, Asukoht)) { valim_VALUE = vorming_VALUE; break; }
            if (valim_VALUE == null) throw new Tõlkimine_tõrge("지원하지 않는 andmetüüp: " + 서술);
            TULEMUS.add(valim_VALUE); Asukoht += valim_VALUE.length();
        }
        return TULEMUS;
    }
    static String sümbol(String 종류, String... 부분들) {
        try {
            byte[] räsikood_Fail = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Tekst = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Tekst.append(String.format(Locale.ROOT, "%02x", räsikood_Fail[순번] & 255));
            return Tekst.toString();
        } catch (Exception VIGA) { throw new Tõlkimine_tõrge(VIGA.toString()); }
    }
    final Map<String, tund_andmed> 클래스들 = new TreeMap<>();
    final Map<meetod_viide, liige_andmed> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), arvuti_Azure_i_funktsioonid_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, arvuti_tund;
    final int 동적기억낱말수;
    final Path ressurss_tee;
    기계어미리번역(List<Path> tee_Loend, String siht, int 낱말수, Path ressurss_VALUE) throws IOException {
        if ((!siht.equals("kernel") && !siht.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Tõlkimine_tõrge("Täida_käsk siht 또는 Mälu_VALUE ADDRESS_regioon Suurus VIGA");
        실행대상 = siht; 동적기억낱말수 = 낱말수; ressurss_tee = ressurss_VALUE;
        // 이 이름도 국가별 lähe_puu genereerima 시 해당 언어로 옮긴다.
        arvuti_tund = siht.equals("kernel") ? "Tahvel" : "kasutaja";
        for (String Joon : Files.readAllLines(ressurss_VALUE.resolve("arvuti_Azure_i_funktsioonid.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Joon.split("\t", -1);
            if (부분들.length != 4) throw new Tõlkimine_tõrge("arvuti FUNCTION_VALUE andmed VIGA");
            if (부분들[0].equals(siht)) arvuti_Azure_i_funktsioonid_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path RADA : tee_Loend) {
            tund_andmed andmed = new tund_andmed(RADA);
            if (클래스들.put(andmed.Nimi_2, andmed) != null) throw new Tõlkimine_tõrge("중복 tund_VALUE: " + andmed.Nimi_2);
            for (liige_andmed väljaväärtus : andmed.väljaväärtus) {
                if ((väljaväärtus.pöördus_kirje & 8) == 0 || 형식읽기(väljaväärtus.서술).equals(Collections.singletonList("V"))) throw new Tõlkimine_tõrge("정적 필드만 tugi_VALUE");
                if (필드들.put(new meetod_viide(andmed.Nimi_2, väljaväärtus.Nimi_2, väljaväärtus.서술), väljaväärtus) != null) throw new Tõlkimine_tõrge("중복 väljaväärtus");
            }
            for (liige_andmed FUNCTION_VALUE : andmed.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Nimi_2.equals("<init>")) continue;
                if ((FUNCTION_VALUE.pöördus_kirje & 8) == 0 || (FUNCTION_VALUE.pöördus_kirje & (0x20 | 0x400)) != 0) throw new Tõlkimine_tõrge("정적 비동기화 함수만 tugi_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new meetod_viide(andmed.Nimi_2, FUNCTION_VALUE.Nimi_2, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Tõlkimine_tõrge("중복 FUNCTION_VALUE");
            }
        }
    }
    String string_sümbol(String Tekst) { return 문자열들.computeIfAbsent(Tekst, VALUE -> "j_text_" + 문자열들.size()); }
    String konstant_avaldis(tund_andmed andmed, int INDEX) {
        if (INDEX < 1 || INDEX >= andmed.상수종류.length) throw new Tõlkimine_tõrge("konstant_VALUE INDEX klipp VIGA");
        if (andmed.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + andmed.konstant_andmed[INDEX] + ")";
        if (andmed.상수종류[INDEX] == 8) return "(word)" + string_sümbol(andmed.문자((Integer)andmed.konstant_andmed[INDEX]));
        throw new Tõlkimine_tõrge("정수와 string_VALUE 상수만 tugi_VALUE");
    }
    String 함수원형(meetod_viide viide) {
        List<String> 인수들 = new ArrayList<>(); int kaup_COUNT = new 함수형식(viide.서술).Argumendid.size();
        for (int 순번 = 0; 순번 < kaup_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + sümbol("method", viide.부분들()) + "(" + (kaup_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void tšekk_kohalik(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Tõlkimine_tõrge("kohalik_skoop 변수 INDEX klipp VIGA"); }
    void 분기넣기(List<String> Väljund, Set<Integer> haru_Loend, int Asukoht, int 이동량, String tingimus) {
        int sihtkoht_VALUE = Asukoht + 이동량; haru_Loend.add(sihtkoht_VALUE);
        Väljund.add((tingimus == null ? "" : "if (" + tingimus + ") ") + "goto b" + sihtkoht_VALUE + ";");
    }
    String meetod_sisu(meetod_viide FUNCTION_VALUE, liige_andmed andmed) {
        byte[] sisu_andmed = andmed.atribuut_VALUE.get("Code"); if (sisu_andmed == null) throw new Tõlkimine_tõrge("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Nimi_2);
        andmed_Reader Reader_VALUE = new andmed_Reader(sisu_andmed); int 쌓임깊이 = Reader_VALUE.두바이트(), 지역변수수 = Reader_VALUE.두바이트();
        andmed_Reader käsk_andmed = new andmed_Reader(Reader_VALUE.Lugemine(Reader_VALUE.네바이트()));
        if (Reader_VALUE.두바이트() != 0) throw new Tõlkimine_tõrge("try/catch/finally 미지원");
        함수형식 vorming_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (지역변수수 < vorming_VALUE.Argumendid.size()) throw new Tõlkimine_tõrge("매개변수보다 적은 kohalik_skoop 변수");
        tund_andmed tund_VALUE = 클래스들.get(FUNCTION_VALUE.omanik_VALUE);
        List<String> Väljund = new ArrayList<>(); Väljund.add(함수원형(FUNCTION_VALUE) + " {");
        Väljund.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < vorming_VALUE.Argumendid.size(); 순번++) Väljund.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), haru_Loend = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (käsk_andmed.Asukoht < käsk_andmed.andmed.length) {
            int Asukoht = käsk_andmed.Asukoht, Käsk = käsk_andmed.한바이트(); 경계들.add(Asukoht); Väljund.add("b" + Asukoht + ":;");
            if (Käsk == 0) continue;
            if (Käsk == 1) Väljund.add("PUSH(0);");
            else if (Käsk >= 2 && Käsk <= 8) Väljund.add("PUSH((uint32_t)(" + (Käsk - 3) + "));");
            else if (Käsk == 16 || Käsk == 17) Väljund.add("PUSH((uint32_t)(" + (Käsk == 16 ? käsk_andmed.부호한바이트() : käsk_andmed.부호두바이트()) + "));");
            else if (Käsk == 18 || Käsk == 19) Väljund.add("PUSH(" + konstant_avaldis(tund_VALUE, Käsk == 18 ? käsk_andmed.한바이트() : käsk_andmed.두바이트()) + ");");
            else if (Käsk == 21 || Käsk == 25 || (Käsk >= 26 && Käsk <= 29) || (Käsk >= 42 && Käsk <= 45)) {
                int INDEX = Käsk == 21 || Käsk == 25 ? käsk_andmed.한바이트() : Käsk - (Käsk <= 29 ? 26 : 42);
                tšekk_kohalik(INDEX, 지역변수수); Väljund.add("PUSH(l[" + INDEX + "]);");
            } else if (Käsk == 54 || Käsk == 58 || (Käsk >= 59 && Käsk <= 62) || (Käsk >= 75 && Käsk <= 78)) {
                int INDEX = Käsk == 54 || Käsk == 58 ? käsk_andmed.한바이트() : Käsk - (Käsk <= 62 ? 59 : 75);
                tšekk_kohalik(INDEX, 지역변수수); Väljund.add("l[" + INDEX + "] = POP();");
            } else if (Käsk == 46) Väljund.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Käsk == 79) Väljund.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Käsk == 87 || Käsk == 88) Väljund.add(Käsk == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Käsk >= 89 && Käsk <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] tellimus_Loend = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Käsk - 89]; 순번++) Väljund.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : tellimus_Loend[Käsk - 89].toCharArray()) Väljund.add("PUSH(" + VALUE + ");");
            } else if (Käsk == 96 || Käsk == 100 || Käsk == 104 || Käsk == 126 || Käsk == 128 || Käsk == 130) {
                String lõikus_VALUE = Käsk == 96 ? "+" : Käsk == 100 ? "-" : Käsk == 104 ? "*" : Käsk == 126 ? "&" : Käsk == 128 ? "|" : "^";
                Väljund.add("b = POP(); a = POP(); PUSH((uint32_t)a " + lõikus_VALUE + " (uint32_t)b);");
            } else if (Käsk == 108 || Käsk == 112) Väljund.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Käsk == 112 ? 1 : 0) + "));");
            else if (Käsk == 116) Väljund.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Käsk == 120 || Käsk == 122 || Käsk == 124) {
                Väljund.add("b = POP(); a = POP();"); Väljund.add("PUSH(" + (Käsk == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Käsk == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Käsk == 132) {
                int INDEX = käsk_andmed.한바이트(), samm_kogus = käsk_andmed.부호한바이트(); tšekk_kohalik(INDEX, 지역변수수);
                Väljund.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + samm_kogus + ");");
            } else if (Käsk >= 145 && Käsk <= 147) Väljund.add("a = POP(); PUSH((uint32_t)(" + (Käsk == 145 ? "int8_t" : Käsk == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Käsk >= 153 && Käsk <= 158) {
                Väljund.add("a = POP();"); 분기넣기(Väljund, haru_Loend, Asukoht, käsk_andmed.부호두바이트(), "(int32_t)a " + 비교들[Käsk - 153] + " 0");
            } else if (Käsk >= 159 && Käsk <= 166) {
                Väljund.add("b = POP(); a = POP();"); 분기넣기(Väljund, haru_Loend, Asukoht, käsk_andmed.부호두바이트(), Käsk >= 165 ? "a " + 비교들[Käsk - 159] + " b" : "(int32_t)a " + 비교들[Käsk - 159] + " (int32_t)b");
            } else if (Käsk == 167 || Käsk == 200) 분기넣기(Väljund, haru_Loend, Asukoht, Käsk == 167 ? käsk_andmed.부호두바이트() : käsk_andmed.네바이트(), null);
            else if (Käsk == 170 || Käsk == 171) {
                while (käsk_andmed.Asukoht % 4 != 0) käsk_andmed.한바이트();
                int vaikeväärtus = käsk_andmed.네바이트(); Väljund.add("a = POP();");
                if (Käsk == 170) {
                    int 아래 = käsk_andmed.네바이트(), 위 = käsk_andmed.네바이트(); long kaup_COUNT = (long)위 - 아래 + 1;
                    if (kaup_COUNT < 1 || kaup_COUNT > (käsk_andmed.andmed.length - käsk_andmed.Asukoht) / 4) throw new Tõlkimine_tõrge("switch klipp VIGA");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Väljund, haru_Loend, Asukoht, käsk_andmed.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int kaup_COUNT = käsk_andmed.네바이트(), esikaamera_andmed = 0;
                    if (kaup_COUNT < 0 || kaup_COUNT > (käsk_andmed.andmed.length - käsk_andmed.Asukoht) / 8) throw new Tõlkimine_tõrge("switch Suurus VIGA");
                    for (int 순번 = 0; 순번 < kaup_COUNT; 순번++) {
                        int VALUE = käsk_andmed.네바이트(); if (순번 > 0 && VALUE <= esikaamera_andmed) throw new Tõlkimine_tõrge("switch tellimus_VALUE VIGA"); esikaamera_andmed = VALUE;
                        분기넣기(Väljund, haru_Loend, Asukoht, käsk_andmed.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Väljund, haru_Loend, Asukoht, vaikeväärtus, null);
            } else if (Käsk == 172 || Käsk == 176 || Käsk == 177) Väljund.add("return " + (Käsk == 177 ? "0" : "POP()") + ";");
            else if (Käsk == 178 || Käsk == 179) {
                meetod_viide viide = tund_VALUE.viide(käsk_andmed.두바이트()); if (!필드들.containsKey(viide)) throw new Tõlkimine_tõrge("알 number 없는 väljaväärtus");
                Väljund.add(sümbol("init", viide.omanik_VALUE) + "();"); String väljaväärtus = sümbol("field", viide.부분들());
                Väljund.add(Käsk == 178 ? "PUSH(" + väljaväärtus + ");" : väljaväärtus + " = POP();");
            } else if (Käsk == 184) {
                meetod_viide viide = tund_VALUE.viide(käsk_andmed.두바이트()); if (!함수들.containsKey(viide)) throw new Tõlkimine_tõrge("알 number 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(viide.서술); int kaup_COUNT = 호출형식.Argumendid.size();
                Väljund.add(sümbol("init", viide.omanik_VALUE) + "();"); Väljund.add("if(sp < " + kaup_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + kaup_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < kaup_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Väljund.add("a = " + sümbol("method", viide.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.tagasi_saatma_näitaja.equals("V")) Väljund.add("PUSH(a);");
            } else if (Käsk == 182) {
                meetod_viide viide = tund_VALUE.viide(käsk_andmed.두바이트());
                if (viide.equals(new meetod_viide("java/lang/String", "length", "()I"))) Väljund.add("a = POP(); PUSH(length(a));");
                else if (viide.equals(new meetod_viide("java/lang/String", "charAt", "(I)C"))) Väljund.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Tõlkimine_tõrge("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Käsk == 188) {
                if (käsk_andmed.한바이트() != 10) throw new Tõlkimine_tõrge("new int[]만 tugi_VALUE"); Väljund.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Käsk == 190) Väljund.add("a = POP(); PUSH(length(a));");
            else if (Käsk == 196) {
                int laiendus_VALUE = käsk_andmed.한바이트(), INDEX = käsk_andmed.두바이트(); tšekk_kohalik(INDEX, 지역변수수);
                if (laiendus_VALUE == 21 || laiendus_VALUE == 25) Väljund.add("PUSH(l[" + INDEX + "]);");
                else if (laiendus_VALUE == 54 || laiendus_VALUE == 58) Väljund.add("l[" + INDEX + "] = POP();");
                else if (laiendus_VALUE == 132) Väljund.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + käsk_andmed.부호두바이트() + ");");
                else throw new Tõlkimine_tõrge("미지원 wide Käsk");
            } else if (Käsk == 198 || Käsk == 199) {
                Väljund.add("a = POP();"); 분기넣기(Väljund, haru_Loend, Asukoht, käsk_andmed.부호두바이트(), "a " + (Käsk == 198 ? "==" : "!=") + " 0");
            } else throw new Tõlkimine_tõrge(FUNCTION_VALUE.omanik_VALUE + "." + FUNCTION_VALUE.Nimi_2 + ", bait_VALUE " + Asukoht + ": 미지원 Käsk " + Käsk);
        }
        if (!경계들.containsAll(haru_Loend)) throw new Tõlkimine_tõrge("Käsk 경계가 아닌 곳으로 haru");
        Väljund.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Väljund);
    }
    String eksportima_meetod(String Link_sümbol, String siht, boolean 진입점여부) {
        int asukohaindeks = siht.lastIndexOf('.'); if (asukohaindeks < 0 || !Link_sümbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tõlkimine_tõrge("내보내기 Määra_VALUE VIGA");
        String omanik_VALUE = siht.substring(0, asukohaindeks).replace('.', '/'), Nimi_2 = siht.substring(asukohaindeks + 1); meetod_viide valim_VALUE = null;
        for (meetod_viide viide : 함수들.keySet()) if (viide.omanik_VALUE.equals(omanik_VALUE) && viide.Nimi_2.equals(Nimi_2)) {
            if (valim_VALUE != null) throw new Tõlkimine_tõrge("겹친 내보내기 siht"); valim_VALUE = viide;
        }
        if (valim_VALUE == null || (함수들.get(valim_VALUE).pöördus_kirje & 0x100) != 0) throw new Tõlkimine_tõrge("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 vorming_VALUE = new 함수형식(valim_VALUE.서술);
        if ((진입점여부 && !vorming_VALUE.Argumendid.isEmpty()) || !Arrays.asList("V", "I").contains(vorming_VALUE.tagasi_saatma_näitaja)) throw new Tõlkimine_tõrge("kirje_p_VALUE 또는 C 경계 vorming_VALUE VIGA");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < vorming_VALUE.Argumendid.size(); 순번++) {
            if (!vorming_VALUE.Argumendid.get(순번).equals("I")) throw new Tõlkimine_tõrge("C 경계는 int 인수만 tugi_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (vorming_VALUE.tagasi_saatma_näitaja.equals("V") ? "void " : "int32_t ") + Link_sümbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + sümbol("init", valim_VALUE.omanik_VALUE) + "(); " + (vorming_VALUE.tagasi_saatma_näitaja.equals("V") ? "" : "return (int32_t)") + sümbol("method", valim_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String genereerima(String kirje_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<meetod_viide, liige_andmed> kirje_VALUE : 함수들.entrySet()) {
            meetod_viide viide = kirje_VALUE.getKey(); liige_andmed andmed = kirje_VALUE.getValue(); 선언들.add(함수원형(viide) + ";");
            if ((andmed.pöördus_kirje & 0x100) != 0) {
                String Ühendu = arvuti_Azure_i_funktsioonid_c3a8e64a.get(viide.Nimi_2 + viide.서술);
                if (!viide.omanik_VALUE.equals(arvuti_tund) || Ühendu == null) throw new Tõlkimine_tõrge("허용되지 않은 native FUNCTION_VALUE: " + viide.Nimi_2);
                int kaup_COUNT = new 함수형식(viide.서술).Argumendid.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < kaup_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Ühendu + "(" + (kaup_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(kaup_COUNT, "word"))) + ");");
                몸체들.add(함수원형(viide) + " { return " + Ühendu + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(meetod_sisu(viide, andmed));
        }
        for (Map.Entry<meetod_viide, liige_andmed> kirje_VALUE : 필드들.entrySet()) {
            meetod_viide viide = kirje_VALUE.getKey(); byte[] konstant_VALUE = kirje_VALUE.getValue().atribuut_VALUE.get("ConstantValue");
            String VALUE = konstant_VALUE == null ? "0" : konstant_avaldis(클래스들.get(viide.omanik_VALUE), new andmed_Reader(konstant_VALUE).두바이트());
            필드선언들.add("static word " + sümbol("field", viide.부분들()) + " = " + VALUE + ";");
        }
        for (String Nimi_2 : 클래스들.keySet()) {
            String 초기화 = sümbol("init", Nimi_2), Olek_VALUE = sümbol("state", Nimi_2);
            선언들.add("static void " + 초기화 + "(void);"); 필드선언들.add("static unsigned " + Olek_VALUE + ";");
            meetod_viide viide = new meetod_viide(Nimi_2, "<clinit>", "()V");
            몸체들.add("static void " + 초기화 + "(void) { if(" + Olek_VALUE + ") return; " + Olek_VALUE + " = 1; " + (함수들.containsKey(viide) ? sümbol("method", viide.부분들()) + "(); " : "") + Olek_VALUE + " = 2; }");
        }
        몸체들.add(eksportima_meetod("java_entry", kirje_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Määra_VALUE : 내보내기목록) {
            int asukohaindeks = Määra_VALUE.indexOf('='); if (asukohaindeks < 1) throw new Tõlkimine_tõrge("내보내기 Määra_VALUE VIGA");
            String Nimi_2 = Määra_VALUE.substring(0, asukohaindeks); 공개이름.add(Nimi_2); 몸체들.add(eksportima_meetod(Nimi_2, Määra_VALUE.substring(asukohaindeks + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> kirje_VALUE : 문자열들.entrySet()) {
            String Tekst = kirje_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + kirje_VALUE.getValue() + "[] = {" + Tekst.length());
            for (int 순번 = 0; 순번 < Tekst.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Tekst.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String tugi_VALUE = Files.readString(ressurss_tee.resolve("CLR_tugi.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(tugi_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ALLIKAS, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nimetus_tabel = new HashMap<>();
        for (String Joon : Files.readAllLines(ressurss_tee.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] siduma_VALUE = Joon.split("\t"); nimetus_tabel.put(siduma_VALUE[0], siduma_VALUE[1]);
        }
        Pattern kogum_avaldis = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = kogum_avaldis.matcher(ALLIKAS); StringBuffer TULEMUS = new StringBuffer();
        while (찾개.find()) {
            String Nimi_2 = 찾개.group(), 새이름 = Nimi_2;
            if (!Nimi_2.startsWith("//") && !Nimi_2.startsWith("/*") && !Nimi_2.startsWith("\"") && !Nimi_2.startsWith("'") && !공개이름.contains(Nimi_2)) {
                새이름 = nimetus_tabel.getOrDefault(Nimi_2, Nimi_2);
                if (Nimi_2.matches("a[0-9]+")) 새이름 = "Argumendid" + Nimi_2.substring(1);
                if (Nimi_2.matches("b[0-9]+")) 새이름 = "haru" + Nimi_2.substring(1);
                if (범용표기) {
                    StringBuilder esitus_VALUE = new StringBuilder();
                    for (char märk_VALUE : 새이름.toCharArray()) esitus_VALUE.append(märk_VALUE < 128 ? Character.toString(märk_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)märk_VALUE));
                    새이름 = esitus_VALUE.toString();
                }
            }
            찾개.appendReplacement(TULEMUS, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(TULEMUS); return TULEMUS.toString();
    }
    String X_86_meetod_sisu(meetod_viide FUNCTION_VALUE, liige_andmed andmed, Map<String,String> arvuti_tabel, String siht) {
        String marker_VALUE = sümbol("method", FUNCTION_VALUE.부분들());
        List<String> Joon = new ArrayList<>();
        if ((andmed.pöördus_kirje & 0x100) != 0) {
            String Ühendu = arvuti_tabel.get(FUNCTION_VALUE.Nimi_2 + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.omanik_VALUE.equals(siht.equals("kernel") ? "seade_VALUE" : "kasutaja") || Ühendu == null) throw new Tõlkimine_tõrge("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + marker_VALUE + ":\njmp " + Ühendu;
        }
        byte[] sisu_SMS = andmed.atribuut_VALUE.get("Code"); if (sisu_SMS == null) throw new Tõlkimine_tõrge("FUNCTION_VALUE 몸체가 없음");
        andmed_Reader Reader_VALUE = new andmed_Reader(sisu_SMS); Reader_VALUE.두바이트(); int kohalik_COUNT = Reader_VALUE.두바이트();
        andmed_Reader käsk_andmed = new andmed_Reader(Reader_VALUE.Lugemine(Reader_VALUE.네바이트()));
        if (Reader_VALUE.두바이트() != 0) throw new Tõlkimine_tõrge("try/catch/finally 미지원");
        함수형식 vorming_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (kohalik_COUNT < vorming_VALUE.Argumendid.size()) throw new Tõlkimine_tõrge("매개변수보다 적은 kohalik_skoop 변수");
        Collections.addAll(Joon,".text",".globl " + marker_VALUE,".type " + marker_VALUE + ", @function",marker_VALUE + ":","pushl %ebp","movl %esp, %ebp","subl $" + kohalik_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < vorming_VALUE.Argumendid.size(); 순번++) Collections.addAll(Joon,"movl " + (8 + 4 * (vorming_VALUE.Argumendid.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        tund_andmed tund_VALUE = 클래스들.get(FUNCTION_VALUE.omanik_VALUE); Set<Integer> 경계들 = new HashSet<>(), haru_Loend = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (käsk_andmed.Asukoht < käsk_andmed.andmed.length) {
            int Asukoht = käsk_andmed.Asukoht, Käsk = käsk_andmed.한바이트(); String asukohaindeks = marker_VALUE + "_b" + Asukoht;
            Joon.add(asukohaindeks + ":"); 경계들.add(Asukoht);
            if (Käsk == 0) Joon.add("nop");
            else if (Käsk == 1) Joon.add("pushl $0");
            else if (Käsk >= 2 && Käsk <= 8) Joon.add("pushl $" + (Käsk - 3));
            else if (Käsk == 16 || Käsk == 17) Joon.add("pushl $" + (Käsk == 16 ? käsk_andmed.부호한바이트() : käsk_andmed.부호두바이트()));
            else if (Käsk == 18 || Käsk == 19) {
                int INDEX = Käsk == 18 ? käsk_andmed.한바이트() : käsk_andmed.두바이트();
                Joon.add("pushl $" + X_86_konstant(tund_VALUE,INDEX));
            } else if (Käsk == 21 || Käsk == 25 || (Käsk >= 26 && Käsk <= 29) || (Käsk >= 42 && Käsk <= 45) || Käsk == 54 || Käsk == 58 || (Käsk >= 59 && Käsk <= 62) || (Käsk >= 75 && Käsk <= 78)) {
                boolean 읽음 = Käsk < 54; int INDEX = Käsk == 21 || Käsk == 25 || Käsk == 54 || Käsk == 58 ? käsk_andmed.한바이트() : Käsk - (Käsk <= 29 ? 26 : Käsk <= 45 ? 42 : Käsk <= 62 ? 59 : 75);
                tšekk_kohalik(INDEX,kohalik_COUNT); Joon.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Käsk == 46) Collections.addAll(Joon,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Käsk == 79) Collections.addAll(Joon,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Käsk == 87 || Käsk == 88) Joon.add("addl $" + (Käsk == 87 ? 4 : 8) + ", %esp");
            else if (Käsk >= 89 && Käsk <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] tellimus_Loend = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Käsk - 89]; 순번++) Joon.add("popl " + 저장기들[순번]);
                for (int 순번 : tellimus_Loend[Käsk - 89]) Joon.add("pushl " + 저장기들[순번]);
            } else if (Käsk == 96 || Käsk == 100 || Käsk == 104 || Käsk == 126 || Käsk == 128 || Käsk == 130) {
                String lõikus_VALUE = Käsk == 96 ? "addl" : Käsk == 100 ? "subl" : Käsk == 104 ? "imull" : Käsk == 126 ? "andl" : Käsk == 128 ? "orl" : "xorl";
                Collections.addAll(Joon,"popl %ecx","popl %eax",lõikus_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Käsk == 108 || Käsk == 112) Collections.addAll(Joon,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + asukohaindeks + "_divide","cmpl $0x80000000, %eax","jne " + asukohaindeks + "_divide","xorl %edx, %edx","jmp " + asukohaindeks + "_done",asukohaindeks + "_divide:","cltd","idivl %ecx",asukohaindeks + "_done:","pushl " + (Käsk == 108 ? "%eax" : "%edx"));
            else if (Käsk == 116) Joon.add("negl (%esp)");
            else if (Käsk == 120 || Käsk == 122 || Käsk == 124) Collections.addAll(Joon,"popl %ecx","popl %eax",(Käsk == 120 ? "sall" : Käsk == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Käsk == 132) {
                int INDEX = käsk_andmed.한바이트(), samm_VALUE = käsk_andmed.부호한바이트(); tšekk_kohalik(INDEX,kohalik_COUNT); Joon.add("addl $" + samm_VALUE + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Käsk >= 145 && Käsk <= 147) Collections.addAll(Joon,"popl %eax",Käsk == 145 ? "movsbl %al, %eax" : Käsk == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Käsk >= 153 && Käsk <= 166) {
                if (Käsk <= 158) Collections.addAll(Joon,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Joon,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int sihtkoht_VALUE = Asukoht + käsk_andmed.부호두바이트(); haru_Loend.add(sihtkoht_VALUE); Joon.add(비교들[Käsk - (Käsk <= 158 ? 153 : 159)] + " " + marker_VALUE + "_b" + sihtkoht_VALUE);
            } else if (Käsk == 167 || Käsk == 200) {
                int sihtkoht_VALUE = Asukoht + (Käsk == 167 ? käsk_andmed.부호두바이트() : käsk_andmed.네바이트()); haru_Loend.add(sihtkoht_VALUE); Joon.add("jmp " + marker_VALUE + "_b" + sihtkoht_VALUE);
            } else if (Käsk == 170 || Käsk == 171) {
                while (käsk_andmed.Asukoht % 4 != 0) käsk_andmed.한바이트();
                int vaikeväärtus = Asukoht + käsk_andmed.네바이트(); haru_Loend.add(vaikeväärtus); Joon.add("popl %eax");
                int kaup_COUNT, 아래 = 0;
                if (Käsk == 170) { 아래 = käsk_andmed.네바이트(); int 위 = käsk_andmed.네바이트(); long 길이 = (long)위 - 아래 + 1; if (길이 < 1 || 길이 > (käsk_andmed.andmed.length - käsk_andmed.Asukoht) / 4) throw new Tõlkimine_tõrge("switch klipp VIGA"); kaup_COUNT = (int)길이; }
                else { kaup_COUNT = käsk_andmed.네바이트(); if (kaup_COUNT < 0 || kaup_COUNT > (käsk_andmed.andmed.length - käsk_andmed.Asukoht) / 8) throw new Tõlkimine_tõrge("switch Suurus VIGA"); }
                for (int 순번 = 0; 순번 < kaup_COUNT; 순번++) {
                    int VALUE = Käsk == 170 ? 아래 + 순번 : käsk_andmed.네바이트(), sihtkoht_VALUE = Asukoht + käsk_andmed.네바이트(); haru_Loend.add(sihtkoht_VALUE);
                    Collections.addAll(Joon,"cmpl $" + VALUE + ", %eax","je " + marker_VALUE + "_b" + sihtkoht_VALUE);
                }
                Joon.add("jmp " + marker_VALUE + "_b" + vaikeväärtus);
            } else if (Käsk == 172 || Käsk == 176 || Käsk == 177) {
                if (Käsk != 177) Joon.add("popl %eax"); Collections.addAll(Joon,"leave","ret");
            } else if (Käsk == 178 || Käsk == 179) {
                meetod_viide viide = tund_VALUE.viide(käsk_andmed.두바이트()); if (!필드들.containsKey(viide)) throw new Tõlkimine_tõrge("알 number 없는 väljaväärtus");
                Collections.addAll(Joon,"call " + sümbol("init",viide.omanik_VALUE),(Käsk == 178 ? "pushl " : "popl ") + sümbol("field",viide.부분들()));
            } else if (Käsk == 184) {
                meetod_viide viide = tund_VALUE.viide(käsk_andmed.두바이트()); if (!함수들.containsKey(viide)) throw new Tõlkimine_tõrge("알 number 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(viide.서술); Collections.addAll(Joon,"call " + sümbol("init",viide.omanik_VALUE),"call " + sümbol("method",viide.부분들()));
                if (!호출형식.Argumendid.isEmpty()) Joon.add("addl $" + 호출형식.Argumendid.size() * 4 + ", %esp");
                if (!호출형식.tagasi_saatma_näitaja.equals("V")) Joon.add("pushl %eax");
            } else if (Käsk == 182) {
                meetod_viide viide = tund_VALUE.viide(käsk_andmed.두바이트());
                if (viide.equals(new meetod_viide("java/lang/String","length","()I"))) Collections.addAll(Joon,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (viide.equals(new meetod_viide("java/lang/String","charAt","(I)C"))) Collections.addAll(Joon,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Tõlkimine_tõrge("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Käsk == 188) {
                if (käsk_andmed.한바이트() != 10) throw new Tõlkimine_tõrge("new int[]만 tugi_VALUE"); Collections.addAll(Joon,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Käsk == 190) Collections.addAll(Joon,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Käsk == 196) {
                int laiendus_VALUE = käsk_andmed.한바이트(), INDEX = käsk_andmed.두바이트(); tšekk_kohalik(INDEX,kohalik_COUNT);
                if (laiendus_VALUE == 21 || laiendus_VALUE == 25 || laiendus_VALUE == 54 || laiendus_VALUE == 58) Joon.add((laiendus_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (laiendus_VALUE == 132) Joon.add("addl $" + käsk_andmed.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Tõlkimine_tõrge("wide Käsk 미지원");
            } else if (Käsk == 198 || Käsk == 199) {
                int sihtkoht_VALUE = Asukoht + käsk_andmed.부호두바이트(); haru_Loend.add(sihtkoht_VALUE); Collections.addAll(Joon,"popl %eax","testl %eax, %eax",(Käsk == 198 ? "je " : "jne ") + marker_VALUE + "_b" + sihtkoht_VALUE);
            } else throw new Tõlkimine_tõrge("미지원 Käsk: " + Käsk);
        }
        if (!경계들.containsAll(haru_Loend)) throw new Tõlkimine_tõrge("Käsk 경계가 아닌 곳으로 haru");
        Joon.add(".size " + marker_VALUE + ", .-" + marker_VALUE); return String.join("\n",Joon);
    }
    String X_86_konstant(tund_andmed andmed, int INDEX) {
        if (andmed.상수종류[INDEX] == 3) return andmed.konstant_andmed[INDEX].toString();
        if (andmed.상수종류[INDEX] == 8) return string_sümbol(andmed.문자((Integer)andmed.konstant_andmed[INDEX]));
        throw new Tõlkimine_tõrge("정수와 string_VALUE 상수만 tugi_VALUE");
    }
    String X_86_komplekt(String kirje_p, List<String> 내보냄, String siht) throws IOException {
        Map<String,String> arvuti_tabel = new HashMap<>();
        for (String Joon : Files.readAllLines(ressurss_tee.resolve("_86_arvuti_Azure_i_funktsioonid.tsv"))) { String[] siduma_VALUE = Joon.split("\t"); if (siduma_VALUE[0].equals(siht)) arvuti_tabel.put(siduma_VALUE[1] + siduma_VALUE[2],siduma_VALUE[3]); }
        int asukohaindeks = kirje_p.lastIndexOf('.'); if (asukohaindeks < 0) throw new Tõlkimine_tõrge("kirje_p Määra_VALUE VIGA");
        String omanik_VALUE = kirje_p.substring(0,asukohaindeks).replace('.','/'), meetod_kirje_nimetus = kirje_p.substring(asukohaindeks + 1); meetod_viide kirje_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { meetod_viide viide = new meetod_viide(omanik_VALUE,meetod_kirje_nimetus,서술); if (함수들.containsKey(viide)) { if (kirje_p_VALUE != null) throw new Tõlkimine_tõrge("겹친 kirje_p"); kirje_p_VALUE = viide; } }
        if (kirje_p_VALUE == null || (함수들.get(kirje_p_VALUE).pöördus_kirje & 0x100) != 0) throw new Tõlkimine_tõrge("kirje_p_VALUE FUNCTION_VALUE vorming_VALUE VIGA");
        List<String> Joon = new ArrayList<>(); Joon.add(".code32");
        for (tund_andmed andmed : 클래스들.values()) {
            String Olek_VALUE = sümbol("state",andmed.Nimi_2), 초기화 = sümbol("init",andmed.Nimi_2);
            Collections.addAll(Joon,".bss",".balign 4",Olek_VALUE + ": .long 0",".text",초기화 + ":","cmpl $0, " + Olek_VALUE,"jne " + 초기화 + "_done","movl $1, " + Olek_VALUE);
            meetod_viide 초기화참조 = new meetod_viide(andmed.Nimi_2,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Joon.add("call " + sümbol("method",초기화참조.부분들()));
            Collections.addAll(Joon,"movl $2, " + Olek_VALUE,초기화 + "_done:","ret");
            for (liige_andmed väljaväärtus : andmed.väljaväärtus) {
                byte[] konstant_VALUE = väljaväärtus.atribuut_VALUE.get("ConstantValue"); String VALUE = konstant_VALUE == null ? "0" : X_86_konstant(andmed,new andmed_Reader(konstant_VALUE).두바이트());
                Collections.addAll(Joon,".data",".balign 4",sümbol("field",andmed.Nimi_2,väljaväärtus.Nimi_2,väljaväärtus.서술) + ": .long " + VALUE);
            }
            for (liige_andmed FUNCTION_VALUE : andmed.FUNCTION_VALUE) if (!FUNCTION_VALUE.Nimi_2.equals("<init>")) Joon.add(X_86_meetod_sisu(new meetod_viide(andmed.Nimi_2,FUNCTION_VALUE.Nimi_2,FUNCTION_VALUE.서술),FUNCTION_VALUE,arvuti_tabel,siht));
        }
        Collections.addAll(Joon,".text",".globl java_entry","java_entry:","call " + sümbol("init",kirje_p_VALUE.omanik_VALUE),"call " + sümbol("method",kirje_p_VALUE.부분들()));
        if (kirje_p_VALUE.서술.equals("()V")) Joon.add("xorl %eax, %eax"); Joon.add("ret");
        for (String Määra_VALUE : 내보냄) {
            int eraldaja_VALUE_d8ba4873 = Määra_VALUE.indexOf('='); if (eraldaja_VALUE_d8ba4873 < 1) throw new Tõlkimine_tõrge("내보내기 Määra_VALUE VIGA");
            String väline_VALUE = Määra_VALUE.substring(0,eraldaja_VALUE_d8ba4873), FUNCTION_VALUE = Määra_VALUE.substring(eraldaja_VALUE_d8ba4873 + 1); int allüksus_näitaja = FUNCTION_VALUE.lastIndexOf('.');
            if (allüksus_näitaja < 0 || !väline_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tõlkimine_tõrge("내보내기 sümbol VIGA");
            String tund_VALUE = FUNCTION_VALUE.substring(0,allüksus_näitaja).replace('.','/'), Nimi_2 = FUNCTION_VALUE.substring(allüksus_näitaja + 1); meetod_viide valim_VALUE = null;
            for (meetod_viide viide : 함수들.keySet()) if (viide.omanik_VALUE.equals(tund_VALUE) && viide.Nimi_2.equals(Nimi_2)) { if (valim_VALUE != null) throw new Tõlkimine_tõrge("겹친 내보내기 siht"); valim_VALUE = viide; }
            if (valim_VALUE == null) throw new Tõlkimine_tõrge("내보낼 함수가 없음");
            Collections.addAll(Joon,".text",".globl " + väline_VALUE,väline_VALUE + ":","call " + sümbol("init",valim_VALUE.omanik_VALUE),"jmp " + sümbol("method",valim_VALUE.부분들()));
        }
        Joon.add(".section .rodata");
        for (Map.Entry<String,String> kirje_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Joon,".balign 4",kirje_VALUE.getValue() + ":",".long " + kirje_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char ühik_VALUE : kirje_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(ühik_VALUE)); if (!단위들.isEmpty()) Joon.add(".long " + String.join(",",단위들));
        }
        Joon.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Joon) + "\n";
    }
    static void Täida_tööriist(List<String> Käsk) throws Exception {
        if (new ProcessBuilder(Käsk).inheritIO().start().waitFor() != 0) throw new Tõlkimine_tõrge("kompileerima_lähe VIGA: " + Käsk.get(0));
    }
    static String andmed_string(String Tekst) { return "\"" + Tekst.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Tõlkimine(List<Path> 입력들, String siht, String kirje_p, List<String> 내보냄, Path Väljund, Path ressurss_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), tund_tee = 임시.resolve("classes"); Files.createDirectory(tund_tee);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",tund_tee.toString(),"-sourcepath",tund_tee.toString(),"-d",tund_tee.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int lähe_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Väljund.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Tõlkimine_tõrge("Väljund 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); lähe_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Tõlkimine_tõrge(".java 또는 .class만 tugi_VALUE");
            }
            if (lähe_COUNT > 0) Täida_tööriist(자바명령);
            try (java.util.stream.Stream<Path> tee_Loend = Files.walk(tund_tee)) { tee_Loend.filter(RADA -> RADA.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,siht.equals("user") ? "user" : "kernel",262144,ressurss_VALUE);
            String 조립 = CONVERT_VALUE.X_86_komplekt(kirje_p,내보냄,siht); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path tööriist_ametikoht = ressurss_VALUE.getParent();
            Täida_tööriist(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Täida_tööriist(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),tööriist_ametikoht.resolve("CLR_tugi.s").toString()));
            List<String> Ühendu = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (siht.equals("kernel")) Ühendu.add("-r");
            else {
                Täida_tööriist(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),tööriist_ametikoht.resolve(siht.equals("user") ? "START_kasutaja_programm.s" : "리눅스시작.s").toString()));
                Collections.addAll(Ühendu,"-e","_start",임시.resolve("start.o").toString());
                if (siht.equals("user")) Collections.addAll(Ühendu,"-T",tööriist_ametikoht.resolve("kasutaja_Link_küljend.ld").toString());
            }
            Collections.addAll(Ühendu,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Täida_tööriist(Ühendu);
            Väljund = Väljund.toAbsolutePath(); Files.createDirectories(Väljund.getParent()); Path avaldama_VALUE = Files.createTempFile(Väljund.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),avaldama_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(avaldama_VALUE,Väljund,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(avaldama_VALUE); }
            Files.setPosixFilePermissions(Väljund,java.nio.file.attribute.PosixFilePermissions.fromString(siht.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Väljund + ".s"),조립,StandardCharsets.UTF_8);
            List<String> sümbol_andmed = new ArrayList<>(), lähe_andmed = new ArrayList<>();
            for (meetod_viide viide : CONVERT_VALUE.함수들.keySet()) sümbol_andmed.add(andmed_string(sümbol("method",viide.부분들())) + ":" + andmed_string(viide.omanik_VALUE + "." + viide.Nimi_2 + viide.서술));
            for (Path 입력 : 입력들) {
                byte[] räsikood_Fail = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Tekst = new StringBuilder(); for (byte VALUE : räsikood_Fail) Tekst.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                lähe_andmed.add(andmed_string(입력.toAbsolutePath().toString()) + ":" + andmed_string(Tekst.toString()));
            }
            Files.writeString(Paths.get(Väljund + ".json"),"{\"target\":" + andmed_string(siht) + ",\"entry\":" + andmed_string(kirje_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",sümbol_andmed) + "},\"sources\":{" + String.join(",",lähe_andmed) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> tee_Loend = Files.walk(임시)) { for (Path RADA : (Iterable<Path>)tee_Loend.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(RADA); }
        }
    }
    public static void main(String[] Argumendid) {
        try {
            String kirje_p = null, siht = "kernel", X_86_siht = null; Path toodang_tee = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> tee_Loend = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumendid.length; 순번++) {
                String VALUE = Argumendid[순번];
                switch (VALUE) {
                    case "--target": X_86_siht = Argumendid[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry tund_VALUE.FUNCTION_VALUE -o Väljund [--target linux|kernel|user] [--profile kernel|user] [--export sümbol=tund_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": kirje_p = Argumendid[++순번]; break;
                    case "--profile": siht = Argumendid[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumendid[++순번]); break;
                    case "--export": 내보냄.add(Argumendid[++순번]); break;
                    case "-o": toodang_tee = Paths.get(Argumendid[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Tõlkimine_tõrge("알 number 없는 옵션: " + VALUE); tee_Loend.add(Paths.get(VALUE));
                }
            }
            if (kirje_p == null || toodang_tee == null || tee_Loend.isEmpty()) throw new Tõlkimine_tõrge("--entry, -o, tund_VALUE 파일이 필요합니다");
            Path ressurss_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_siht != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_siht)) throw new Tõlkimine_tõrge("알 number 없는 Täida_käsk siht");
                X_86_Tõlkimine(tee_Loend,X_86_siht,kirje_p,내보냄,toodang_tee,ressurss_VALUE); return;
            }
            String ALLIKAS = new 기계어미리번역(tee_Loend, siht, 낱말수, ressurss_VALUE).genereerima(kirje_p, 내보냄, 범용표기);
            toodang_tee = toodang_tee.toAbsolutePath(); Files.createDirectories(toodang_tee.getParent());
            Path 임시 = Files.createTempFile(toodang_tee.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ALLIKAS, StandardCharsets.UTF_8); Files.move(임시, toodang_tee, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception VIGA) { System.err.println("kompileerima_lähe VIGA: " + VIGA.getMessage()); System.exit(1); }
    }
}
