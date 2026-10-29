// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java time_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. vert JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Omsetjing_feil extends RuntimeException {
        Omsetjing_feil(String 설명) { super(설명); }
    }
    static final class data_Lesar {
        final byte[] data;
        int Posisjon;
        data_Lesar(byte[] 입력자료) { data = 입력자료; }
        byte[] Les(int lengd_VALUE) {
            if (lengd_VALUE < 0 || lengd_VALUE > data.length - Posisjon) throw new Omsetjing_feil("잘린 time_VALUE 또는 Kommando data");
            byte[] forretningsmål = Arrays.copyOfRange(data, Posisjon, Posisjon + lengd_VALUE); Posisjon += lengd_VALUE; return forretningsmål;
        }
        int 한바이트() { if (Posisjon >= data.length) throw new Omsetjing_feil("잘린 Kommando data"); return data[Posisjon++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class medlem_data {
        final int tilgang_oppføring;
        final String Namn, 서술;
        final Map<String, byte[]> attributt_VALUE;
        medlem_data(int tilgang_VALUE, String namn_VALUE, String 서술값, Map<String, byte[]> attributt_data) {
            tilgang_oppføring = tilgang_VALUE; Namn = namn_VALUE; 서술 = 서술값; attributt_VALUE = attributt_data;
        }
    }
    static final class metode_Oppslagsverk implements Comparable<metode_Oppslagsverk> {
        final String eigar_VALUE, Namn, 서술;
        metode_Oppslagsverk(String 소유값, String namn_VALUE, String 서술값) { eigar_VALUE = 소유값; Namn = namn_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{eigar_VALUE, Namn, 서술}; }
        public int compareTo(metode_Oppslagsverk node_VALUE_6a3b6fa7) {
            int Samanlikning_VALUE = eigar_VALUE.compareTo(node_VALUE_6a3b6fa7.eigar_VALUE);
            if (Samanlikning_VALUE == 0) Samanlikning_VALUE = Namn.compareTo(node_VALUE_6a3b6fa7.Namn);
            return Samanlikning_VALUE == 0 ? 서술.compareTo(node_VALUE_6a3b6fa7.서술) : Samanlikning_VALUE;
        }
        public boolean equals(Object node_VALUE_6a3b6fa7) { return node_VALUE_6a3b6fa7 instanceof metode_Oppslagsverk && compareTo((metode_Oppslagsverk) node_VALUE_6a3b6fa7) == 0; }
        public int hashCode() { return Objects.hash(eigar_VALUE, Namn, 서술); }
    }
    static final class time_data {
        final int[] 상수종류;
        final Object[] konstant_data;
        final String Namn;
        final List<medlem_data> felt_VALUE_0f39cf1c, FUNCTION_VALUE;
        time_data(Path STIGE) throws IOException {
            data_Lesar Lesar_VALUE = new data_Lesar(Files.readAllBytes(STIGE));
            if (Lesar_VALUE.네바이트() != 0xcafebabe) throw new Omsetjing_feil("Java time_VALUE 표식이 아님");
            Lesar_VALUE.Les(4);
            int vare_COUNT = Lesar_VALUE.두바이트(); 상수종류 = new int[vare_COUNT]; konstant_data = new Object[vare_COUNT];
            for (int 순번 = 1; 순번 < vare_COUNT; 순번++) {
                int 종류 = Lesar_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int lengd_VALUE = Lesar_VALUE.두바이트();
                        byte[] teikn_buffer = Lesar_VALUE.Les(lengd_VALUE), 길이붙인자료 = new byte[lengd_VALUE + 2];
                        길이붙인자료[0] = (byte)(lengd_VALUE >> 8); 길이붙인자료[1] = (byte)lengd_VALUE;
                        System.arraycopy(teikn_buffer, 0, 길이붙인자료, 2, lengd_VALUE);
                        konstant_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstant_data[순번] = Lesar_VALUE.네바이트(); break;
                    case 4: Lesar_VALUE.Les(4); break;
                    case 5: case 6: Lesar_VALUE.Les(8); 순번++; break;
                    case 7: case 8: case 16: konstant_data[순번] = Lesar_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstant_data[순번] = new int[]{Lesar_VALUE.두바이트(), Lesar_VALUE.두바이트()}; break;
                    case 15: konstant_data[순번] = new int[]{Lesar_VALUE.한바이트(), Lesar_VALUE.두바이트()}; break;
                    default: throw new Omsetjing_feil("지원하지 않는 konstant_VALUE 종류: " + 종류);
                }
            }
            Lesar_VALUE.두바이트(); Namn = time_namn(Lesar_VALUE.두바이트());
            if (!time_namn(Lesar_VALUE.두바이트()).equals("java/lang/Object") || Lesar_VALUE.두바이트() != 0)
                throw new Omsetjing_feil(Namn + ": 상속 및 인터페이스 미지원");
            felt_VALUE_0f39cf1c = 멤버읽기(Lesar_VALUE); FUNCTION_VALUE = 멤버읽기(Lesar_VALUE); 속성읽기(Lesar_VALUE);
            if (Lesar_VALUE.Posisjon != Lesar_VALUE.data.length) throw new Omsetjing_feil("time_VALUE 뒤에 남은 data");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Omsetjing_feil("문자 konstant_VALUE INDEX FEIL");
            return (String) konstant_data[INDEX];
        }
        String time_namn(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Omsetjing_feil("time_VALUE Oppslagsverk FEIL");
            return 문자((Integer)konstant_data[INDEX]);
        }
        metode_Oppslagsverk Oppslagsverk(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Omsetjing_feil("멤버 Oppslagsverk FEIL");
            int[] pare_VALUE = (int[])konstant_data[INDEX], namn_pare = (int[])konstant_data[pare_VALUE[1]];
            return new metode_Oppslagsverk(time_namn(pare_VALUE[0]), 문자(namn_pare[0]), 문자(namn_pare[1]));
        }
        Map<String, byte[]> 속성읽기(data_Lesar Lesar_VALUE) {
            Map<String, byte[]> forretningsmål = new LinkedHashMap<>();
            int vare_COUNT = Lesar_VALUE.두바이트();
            for (int 순번 = 0; 순번 < vare_COUNT; 순번++) {
                String attributt_namn = 문자(Lesar_VALUE.두바이트()); byte[] VALUE = Lesar_VALUE.Les(Lesar_VALUE.네바이트());
                if (forretningsmål.put(attributt_namn, VALUE) != null) throw new Omsetjing_feil("겹친 attributt_VALUE: " + attributt_namn);
            }
            return forretningsmål;
        }
        List<medlem_data> 멤버읽기(data_Lesar Lesar_VALUE) {
            List<medlem_data> forretningsmål = new ArrayList<>(); int vare_COUNT = Lesar_VALUE.두바이트();
            for (int 순번 = 0; 순번 < vare_COUNT; 순번++) {
                int tilgang_oppføring = Lesar_VALUE.두바이트(); String metode_oppføring_namn = 문자(Lesar_VALUE.두바이트()), 서술 = 문자(Lesar_VALUE.두바이트());
                forretningsmål.add(new medlem_data(tilgang_oppføring, metode_oppføring_namn, 서술, 속성읽기(Lesar_VALUE)));
            }
            return forretningsmål;
        }
    }
    static final class 함수형식 {
        final List<String> Argument = new ArrayList<>();
        final String levere_tilbake_forretningsmål;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Omsetjing_feil("FUNCTION_VALUE 서술 FEIL: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Omsetjing_feil("FUNCTION_VALUE 서술 FEIL: " + 서술);
            Argument.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argument.contains("V") || 반환들.size() != 1) throw new Omsetjing_feil("FUNCTION_VALUE 서술 FEIL: " + 서술);
            levere_tilbake_forretningsmål = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> forretningsmål = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Posisjon = 0; Posisjon < 서술.length();) {
            String merkt_område_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, Posisjon)) { merkt_område_VALUE = format_VALUE; break; }
            if (merkt_område_VALUE == null) throw new Omsetjing_feil("지원하지 않는 datatype: " + 서술);
            forretningsmål.add(merkt_område_VALUE); Posisjon += merkt_område_VALUE.length();
        }
        return forretningsmål;
    }
    static String symbol(String 종류, String... 부분들) {
        try {
            byte[] hash_fil = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Tekst = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Tekst.append(String.format(Locale.ROOT, "%02x", hash_fil[순번] & 255));
            return Tekst.toString();
        } catch (Exception FEIL) { throw new Omsetjing_feil(FEIL.toString()); }
    }
    final Map<String, time_data> 클래스들 = new TreeMap<>();
    final Map<metode_Oppslagsverk, medlem_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, maskin_time;
    final int 동적기억낱말수;
    final Path ressurs_bane;
    기계어미리번역(List<Path> bane_Liste, String mål, int 낱말수, Path ressurs_VALUE) throws IOException {
        if ((!mål.equals("kernel") && !mål.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Omsetjing_feil("Utfør_kommando mål 또는 Minne_VALUE 공간 Storleik FEIL");
        실행대상 = mål; 동적기억낱말수 = 낱말수; ressurs_bane = ressurs_VALUE;
        // 이 이름도 국가별 kjelde_tre generere 시 해당 언어로 옮긴다.
        maskin_time = mål.equals("kernel") ? "Tavle" : "brukar";
        for (String linje : Files.readAllLines(ressurs_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = linje.split("\t", -1);
            if (부분들.length != 4) throw new Omsetjing_feil("maskin FUNCTION_VALUE data FEIL");
            if (부분들[0].equals(mål)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path STIGE : bane_Liste) {
            time_data data = new time_data(STIGE);
            if (클래스들.put(data.Namn, data) != null) throw new Omsetjing_feil("중복 time_VALUE: " + data.Namn);
            for (medlem_data felt_VALUE_0f39cf1c : data.felt_VALUE_0f39cf1c) {
                if ((felt_VALUE_0f39cf1c.tilgang_oppføring & 8) == 0 || 형식읽기(felt_VALUE_0f39cf1c.서술).equals(Collections.singletonList("V"))) throw new Omsetjing_feil("statisk_VALUE 필드만 støtte_VALUE");
                if (필드들.put(new metode_Oppslagsverk(data.Namn, felt_VALUE_0f39cf1c.Namn, felt_VALUE_0f39cf1c.서술), felt_VALUE_0f39cf1c) != null) throw new Omsetjing_feil("중복 felt_VALUE_0f39cf1c");
            }
            for (medlem_data FUNCTION_VALUE : data.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Namn.equals("<init>")) continue;
                if ((FUNCTION_VALUE.tilgang_oppføring & 8) == 0 || (FUNCTION_VALUE.tilgang_oppføring & (0x20 | 0x400)) != 0) throw new Omsetjing_feil("statisk_VALUE 비동기화 함수만 støtte_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new metode_Oppslagsverk(data.Namn, FUNCTION_VALUE.Namn, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Omsetjing_feil("중복 FUNCTION_VALUE");
            }
        }
    }
    String streng_symbol(String Tekst) { return 문자열들.computeIfAbsent(Tekst, VALUE -> "j_text_" + 문자열들.size()); }
    String konstant_uttrykk(time_data data, int INDEX) {
        if (INDEX < 1 || INDEX >= data.상수종류.length) throw new Omsetjing_feil("konstant_VALUE INDEX klipp FEIL");
        if (data.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + data.konstant_data[INDEX] + ")";
        if (data.상수종류[INDEX] == 8) return "(word)" + streng_symbol(data.문자((Integer)data.konstant_data[INDEX]));
        throw new Omsetjing_feil("정수와 streng_VALUE 상수만 støtte_VALUE");
    }
    String 함수원형(metode_Oppslagsverk Oppslagsverk) {
        List<String> 인수들 = new ArrayList<>(); int vare_COUNT = new 함수형식(Oppslagsverk.서술).Argument.size();
        for (int 순번 = 0; 순번 < vare_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symbol("method", Oppslagsverk.부분들()) + "(" + (vare_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void sjekk_lokal(int INDEX, int lokal_variabel_COUNT) { if (INDEX < 0 || INDEX >= lokal_variabel_COUNT) throw new Omsetjing_feil("lokal_område variabel_VALUE INDEX klipp FEIL"); }
    void 분기넣기(List<String> Utdata, Set<Integer> grein_Liste, int Posisjon, int 이동량, String tilstand) {
        int mål_VALUE = Posisjon + 이동량; grein_Liste.add(mål_VALUE);
        Utdata.add((tilstand == null ? "" : "if (" + tilstand + ") ") + "goto b" + mål_VALUE + ";");
    }
    String metode_brødtekst(metode_Oppslagsverk FUNCTION_VALUE, medlem_data data) {
        byte[] brødtekst_data = data.attributt_VALUE.get("Code"); if (brødtekst_data == null) throw new Omsetjing_feil("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Namn);
        data_Lesar Lesar_VALUE = new data_Lesar(brødtekst_data); int 쌓임깊이 = Lesar_VALUE.두바이트(), lokal_variabel_COUNT = Lesar_VALUE.두바이트();
        data_Lesar kommando_data = new data_Lesar(Lesar_VALUE.Les(Lesar_VALUE.네바이트()));
        if (Lesar_VALUE.두바이트() != 0) throw new Omsetjing_feil("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokal_variabel_COUNT < format_VALUE.Argument.size()) throw new Omsetjing_feil("매개변수보다 적은 lokal_område variabel_VALUE");
        time_data time_VALUE = 클래스들.get(FUNCTION_VALUE.eigar_VALUE);
        List<String> Utdata = new ArrayList<>(); Utdata.add(함수원형(FUNCTION_VALUE) + " {");
        Utdata.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(lokal_variabel_COUNT, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.Argument.size(); 순번++) Utdata.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), grein_Liste = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (kommando_data.Posisjon < kommando_data.data.length) {
            int Posisjon = kommando_data.Posisjon, Kommando = kommando_data.한바이트(); 경계들.add(Posisjon); Utdata.add("b" + Posisjon + ":;");
            if (Kommando == 0) continue;
            if (Kommando == 1) Utdata.add("PUSH(0);");
            else if (Kommando >= 2 && Kommando <= 8) Utdata.add("PUSH((uint32_t)(" + (Kommando - 3) + "));");
            else if (Kommando == 16 || Kommando == 17) Utdata.add("PUSH((uint32_t)(" + (Kommando == 16 ? kommando_data.부호한바이트() : kommando_data.부호두바이트()) + "));");
            else if (Kommando == 18 || Kommando == 19) Utdata.add("PUSH(" + konstant_uttrykk(time_VALUE, Kommando == 18 ? kommando_data.한바이트() : kommando_data.두바이트()) + ");");
            else if (Kommando == 21 || Kommando == 25 || (Kommando >= 26 && Kommando <= 29) || (Kommando >= 42 && Kommando <= 45)) {
                int INDEX = Kommando == 21 || Kommando == 25 ? kommando_data.한바이트() : Kommando - (Kommando <= 29 ? 26 : 42);
                sjekk_lokal(INDEX, lokal_variabel_COUNT); Utdata.add("PUSH(l[" + INDEX + "]);");
            } else if (Kommando == 54 || Kommando == 58 || (Kommando >= 59 && Kommando <= 62) || (Kommando >= 75 && Kommando <= 78)) {
                int INDEX = Kommando == 54 || Kommando == 58 ? kommando_data.한바이트() : Kommando - (Kommando <= 62 ? 59 : 75);
                sjekk_lokal(INDEX, lokal_variabel_COUNT); Utdata.add("l[" + INDEX + "] = POP();");
            } else if (Kommando == 46) Utdata.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Kommando == 79) Utdata.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Kommando == 87 || Kommando == 88) Utdata.add(Kommando == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Kommando >= 89 && Kommando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] rekkjefølgje_Liste = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Kommando - 89]; 순번++) Utdata.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : rekkjefølgje_Liste[Kommando - 89].toCharArray()) Utdata.add("PUSH(" + VALUE + ");");
            } else if (Kommando == 96 || Kommando == 100 || Kommando == 104 || Kommando == 126 || Kommando == 128 || Kommando == 130) {
                String operasjon_VALUE = Kommando == 96 ? "+" : Kommando == 100 ? "-" : Kommando == 104 ? "*" : Kommando == 126 ? "&" : Kommando == 128 ? "|" : "^";
                Utdata.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operasjon_VALUE + " (uint32_t)b);");
            } else if (Kommando == 108 || Kommando == 112) Utdata.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Kommando == 112 ? 1 : 0) + "));");
            else if (Kommando == 116) Utdata.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Kommando == 120 || Kommando == 122 || Kommando == 124) {
                Utdata.add("b = POP(); a = POP();"); Utdata.add("PUSH(" + (Kommando == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Kommando == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Kommando == 132) {
                int INDEX = kommando_data.한바이트(), 증가량 = kommando_data.부호한바이트(); sjekk_lokal(INDEX, lokal_variabel_COUNT);
                Utdata.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Kommando >= 145 && Kommando <= 147) Utdata.add("a = POP(); PUSH((uint32_t)(" + (Kommando == 145 ? "int8_t" : Kommando == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Kommando >= 153 && Kommando <= 158) {
                Utdata.add("a = POP();"); 분기넣기(Utdata, grein_Liste, Posisjon, kommando_data.부호두바이트(), "(int32_t)a " + 비교들[Kommando - 153] + " 0");
            } else if (Kommando >= 159 && Kommando <= 166) {
                Utdata.add("b = POP(); a = POP();"); 분기넣기(Utdata, grein_Liste, Posisjon, kommando_data.부호두바이트(), Kommando >= 165 ? "a " + 비교들[Kommando - 159] + " b" : "(int32_t)a " + 비교들[Kommando - 159] + " (int32_t)b");
            } else if (Kommando == 167 || Kommando == 200) 분기넣기(Utdata, grein_Liste, Posisjon, Kommando == 167 ? kommando_data.부호두바이트() : kommando_data.네바이트(), null);
            else if (Kommando == 170 || Kommando == 171) {
                while (kommando_data.Posisjon % 4 != 0) kommando_data.한바이트();
                int standardverdi = kommando_data.네바이트(); Utdata.add("a = POP();");
                if (Kommando == 170) {
                    int 아래 = kommando_data.네바이트(), 위 = kommando_data.네바이트(); long vare_COUNT = (long)위 - 아래 + 1;
                    if (vare_COUNT < 1 || vare_COUNT > (kommando_data.data.length - kommando_data.Posisjon) / 4) throw new Omsetjing_feil("switch klipp FEIL");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Utdata, grein_Liste, Posisjon, kommando_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int vare_COUNT = kommando_data.네바이트(), 앞값 = 0;
                    if (vare_COUNT < 0 || vare_COUNT > (kommando_data.data.length - kommando_data.Posisjon) / 8) throw new Omsetjing_feil("switch Storleik FEIL");
                    for (int 순번 = 0; 순번 < vare_COUNT; 순번++) {
                        int VALUE = kommando_data.네바이트(); if (순번 > 0 && VALUE <= 앞값) throw new Omsetjing_feil("switch rekkjefølgje_VALUE FEIL"); 앞값 = VALUE;
                        분기넣기(Utdata, grein_Liste, Posisjon, kommando_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Utdata, grein_Liste, Posisjon, standardverdi, null);
            } else if (Kommando == 172 || Kommando == 176 || Kommando == 177) Utdata.add("return " + (Kommando == 177 ? "0" : "POP()") + ";");
            else if (Kommando == 178 || Kommando == 179) {
                metode_Oppslagsverk Oppslagsverk = time_VALUE.Oppslagsverk(kommando_data.두바이트()); if (!필드들.containsKey(Oppslagsverk)) throw new Omsetjing_feil("알 수 없는 felt_VALUE_0f39cf1c");
                Utdata.add(symbol("init", Oppslagsverk.eigar_VALUE) + "();"); String felt_VALUE_0f39cf1c = symbol("field", Oppslagsverk.부분들());
                Utdata.add(Kommando == 178 ? "PUSH(" + felt_VALUE_0f39cf1c + ");" : felt_VALUE_0f39cf1c + " = POP();");
            } else if (Kommando == 184) {
                metode_Oppslagsverk Oppslagsverk = time_VALUE.Oppslagsverk(kommando_data.두바이트()); if (!함수들.containsKey(Oppslagsverk)) throw new Omsetjing_feil("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Oppslagsverk.서술); int vare_COUNT = 호출형식.Argument.size();
                Utdata.add(symbol("init", Oppslagsverk.eigar_VALUE) + "();"); Utdata.add("if(sp < " + vare_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + vare_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < vare_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Utdata.add("a = " + symbol("method", Oppslagsverk.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.levere_tilbake_forretningsmål.equals("V")) Utdata.add("PUSH(a);");
            } else if (Kommando == 182) {
                metode_Oppslagsverk Oppslagsverk = time_VALUE.Oppslagsverk(kommando_data.두바이트());
                if (Oppslagsverk.equals(new metode_Oppslagsverk("java/lang/String", "length", "()I"))) Utdata.add("a = POP(); PUSH(length(a));");
                else if (Oppslagsverk.equals(new metode_Oppslagsverk("java/lang/String", "charAt", "(I)C"))) Utdata.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Omsetjing_feil("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Kommando == 188) {
                if (kommando_data.한바이트() != 10) throw new Omsetjing_feil("new int[]만 støtte_VALUE"); Utdata.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Kommando == 190) Utdata.add("a = POP(); PUSH(length(a));");
            else if (Kommando == 196) {
                int filtype_VALUE = kommando_data.한바이트(), INDEX = kommando_data.두바이트(); sjekk_lokal(INDEX, lokal_variabel_COUNT);
                if (filtype_VALUE == 21 || filtype_VALUE == 25) Utdata.add("PUSH(l[" + INDEX + "]);");
                else if (filtype_VALUE == 54 || filtype_VALUE == 58) Utdata.add("l[" + INDEX + "] = POP();");
                else if (filtype_VALUE == 132) Utdata.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + kommando_data.부호두바이트() + ");");
                else throw new Omsetjing_feil("미지원 wide Kommando");
            } else if (Kommando == 198 || Kommando == 199) {
                Utdata.add("a = POP();"); 분기넣기(Utdata, grein_Liste, Posisjon, kommando_data.부호두바이트(), "a " + (Kommando == 198 ? "==" : "!=") + " 0");
            } else throw new Omsetjing_feil(FUNCTION_VALUE.eigar_VALUE + "." + FUNCTION_VALUE.Namn + ", byte_VALUE " + Posisjon + ": 미지원 Kommando " + Kommando);
        }
        if (!경계들.containsAll(grein_Liste)) throw new Omsetjing_feil("Kommando 경계가 아닌 곳으로 grein");
        Utdata.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Utdata);
    }
    String eksportere_metode(String kople_symbol, String mål, boolean 진입점여부) {
        int plassere_INDEX = mål.lastIndexOf('.'); if (plassere_INDEX < 0 || !kople_symbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Omsetjing_feil("내보내기 Tilordne_VALUE FEIL");
        String eigar_VALUE = mål.substring(0, plassere_INDEX).replace('.', '/'), Namn = mål.substring(plassere_INDEX + 1); metode_Oppslagsverk merkt_område_VALUE = null;
        for (metode_Oppslagsverk Oppslagsverk : 함수들.keySet()) if (Oppslagsverk.eigar_VALUE.equals(eigar_VALUE) && Oppslagsverk.Namn.equals(Namn)) {
            if (merkt_område_VALUE != null) throw new Omsetjing_feil("겹친 내보내기 mål"); merkt_område_VALUE = Oppslagsverk;
        }
        if (merkt_område_VALUE == null || (함수들.get(merkt_område_VALUE).tilgang_oppføring & 0x100) != 0) throw new Omsetjing_feil("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 format_VALUE = new 함수형식(merkt_område_VALUE.서술);
        if ((진입점여부 && !format_VALUE.Argument.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.levere_tilbake_forretningsmål)) throw new Omsetjing_feil("oppføring_p_VALUE 또는 C 경계 format_VALUE FEIL");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.Argument.size(); 순번++) {
            if (!format_VALUE.Argument.get(순번).equals("I")) throw new Omsetjing_feil("C 경계는 int 인수만 støtte_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.levere_tilbake_forretningsmål.equals("V") ? "void " : "int32_t ") + kople_symbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symbol("init", merkt_område_VALUE.eigar_VALUE) + "(); " + (format_VALUE.levere_tilbake_forretningsmål.equals("V") ? "" : "return (int32_t)") + symbol("method", merkt_område_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generere(String oppføring_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metode_Oppslagsverk, medlem_data> oppføring_VALUE : 함수들.entrySet()) {
            metode_Oppslagsverk Oppslagsverk = oppføring_VALUE.getKey(); medlem_data data = oppføring_VALUE.getValue(); 선언들.add(함수원형(Oppslagsverk) + ";");
            if ((data.tilgang_oppføring & 0x100) != 0) {
                String Kopla_til = 기계함수들.get(Oppslagsverk.Namn + Oppslagsverk.서술);
                if (!Oppslagsverk.eigar_VALUE.equals(maskin_time) || Kopla_til == null) throw new Omsetjing_feil("허용되지 않은 native FUNCTION_VALUE: " + Oppslagsverk.Namn);
                int vare_COUNT = new 함수형식(Oppslagsverk.서술).Argument.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < vare_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Kopla_til + "(" + (vare_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(vare_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Oppslagsverk) + " { return " + Kopla_til + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metode_brødtekst(Oppslagsverk, data));
        }
        for (Map.Entry<metode_Oppslagsverk, medlem_data> oppføring_VALUE : 필드들.entrySet()) {
            metode_Oppslagsverk Oppslagsverk = oppføring_VALUE.getKey(); byte[] konstant_VALUE = oppføring_VALUE.getValue().attributt_VALUE.get("ConstantValue");
            String VALUE = konstant_VALUE == null ? "0" : konstant_uttrykk(클래스들.get(Oppslagsverk.eigar_VALUE), new data_Lesar(konstant_VALUE).두바이트());
            필드선언들.add("static word " + symbol("field", Oppslagsverk.부분들()) + " = " + VALUE + ";");
        }
        for (String Namn : 클래스들.keySet()) {
            String starte = symbol("init", Namn), status_VALUE = symbol("state", Namn);
            선언들.add("static void " + starte + "(void);"); 필드선언들.add("static unsigned " + status_VALUE + ";");
            metode_Oppslagsverk Oppslagsverk = new metode_Oppslagsverk(Namn, "<clinit>", "()V");
            몸체들.add("static void " + starte + "(void) { if(" + status_VALUE + ") return; " + status_VALUE + " = 1; " + (함수들.containsKey(Oppslagsverk) ? symbol("method", Oppslagsverk.부분들()) + "(); " : "") + status_VALUE + " = 2; }");
        }
        몸체들.add(eksportere_metode("java_entry", oppføring_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Tilordne_VALUE : 내보내기목록) {
            int plassere_INDEX = Tilordne_VALUE.indexOf('='); if (plassere_INDEX < 1) throw new Omsetjing_feil("내보내기 Tilordne_VALUE FEIL");
            String Namn = Tilordne_VALUE.substring(0, plassere_INDEX); 공개이름.add(Namn); 몸체들.add(eksportere_metode(Namn, Tilordne_VALUE.substring(plassere_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> oppføring_VALUE : 문자열들.entrySet()) {
            String Tekst = oppføring_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + oppføring_VALUE.getValue() + "[] = {" + Tekst.length());
            for (int 순번 = 0; 순번 < Tekst.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Tekst.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String støtte_VALUE = Files.readString(ressurs_bane.resolve("Common_Language_Runtime_støtte.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(støtte_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String KJELDE, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> namn_tabell = new HashMap<>();
        for (String linje : Files.readAllLines(ressurs_bane.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] pare_VALUE = linje.split("\t"); namn_tabell.put(pare_VALUE[0], pare_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(KJELDE); StringBuffer forretningsmål = new StringBuffer();
        while (찾개.find()) {
            String Namn = 찾개.group(), 새이름 = Namn;
            if (!Namn.startsWith("//") && !Namn.startsWith("/*") && !Namn.startsWith("\"") && !Namn.startsWith("'") && !공개이름.contains(Namn)) {
                새이름 = namn_tabell.getOrDefault(Namn, Namn);
                if (Namn.matches("a[0-9]+")) 새이름 = "Argument" + Namn.substring(1);
                if (Namn.matches("b[0-9]+")) 새이름 = "grein" + Namn.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char teikn_VALUE : 새이름.toCharArray()) 표기.append(teikn_VALUE < 128 ? Character.toString(teikn_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)teikn_VALUE));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(forretningsmål, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(forretningsmål); return forretningsmål.toString();
    }
    String X_86_metode_brødtekst(metode_Oppslagsverk FUNCTION_VALUE, medlem_data data, Map<String,String> maskin_tabell, String mål) {
        String 표식 = symbol("method", FUNCTION_VALUE.부분들());
        List<String> linje = new ArrayList<>();
        if ((data.tilgang_oppføring & 0x100) != 0) {
            String Kopla_til = maskin_tabell.get(FUNCTION_VALUE.Namn + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.eigar_VALUE.equals(mål.equals("kernel") ? "mobil_VALUE" : "brukar") || Kopla_til == null) throw new Omsetjing_feil("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Kopla_til;
        }
        byte[] brødtekst = data.attributt_VALUE.get("Code"); if (brødtekst == null) throw new Omsetjing_feil("FUNCTION_VALUE 몸체가 없음");
        data_Lesar Lesar_VALUE = new data_Lesar(brødtekst); Lesar_VALUE.두바이트(); int lokal_COUNT = Lesar_VALUE.두바이트();
        data_Lesar kommando_data = new data_Lesar(Lesar_VALUE.Les(Lesar_VALUE.네바이트()));
        if (Lesar_VALUE.두바이트() != 0) throw new Omsetjing_feil("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokal_COUNT < format_VALUE.Argument.size()) throw new Omsetjing_feil("매개변수보다 적은 lokal_område variabel_VALUE");
        Collections.addAll(linje,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.Argument.size(); 순번++) Collections.addAll(linje,"movl " + (8 + 4 * (format_VALUE.Argument.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        time_data time_VALUE = 클래스들.get(FUNCTION_VALUE.eigar_VALUE); Set<Integer> 경계들 = new HashSet<>(), grein_Liste = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (kommando_data.Posisjon < kommando_data.data.length) {
            int Posisjon = kommando_data.Posisjon, Kommando = kommando_data.한바이트(); String plassere_INDEX = 표식 + "_b" + Posisjon;
            linje.add(plassere_INDEX + ":"); 경계들.add(Posisjon);
            if (Kommando == 0) linje.add("nop");
            else if (Kommando == 1) linje.add("pushl $0");
            else if (Kommando >= 2 && Kommando <= 8) linje.add("pushl $" + (Kommando - 3));
            else if (Kommando == 16 || Kommando == 17) linje.add("pushl $" + (Kommando == 16 ? kommando_data.부호한바이트() : kommando_data.부호두바이트()));
            else if (Kommando == 18 || Kommando == 19) {
                int INDEX = Kommando == 18 ? kommando_data.한바이트() : kommando_data.두바이트();
                linje.add("pushl $" + X_86_konstant(time_VALUE,INDEX));
            } else if (Kommando == 21 || Kommando == 25 || (Kommando >= 26 && Kommando <= 29) || (Kommando >= 42 && Kommando <= 45) || Kommando == 54 || Kommando == 58 || (Kommando >= 59 && Kommando <= 62) || (Kommando >= 75 && Kommando <= 78)) {
                boolean 읽음 = Kommando < 54; int INDEX = Kommando == 21 || Kommando == 25 || Kommando == 54 || Kommando == 58 ? kommando_data.한바이트() : Kommando - (Kommando <= 29 ? 26 : Kommando <= 45 ? 42 : Kommando <= 62 ? 59 : 75);
                sjekk_lokal(INDEX,lokal_COUNT); linje.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Kommando == 46) Collections.addAll(linje,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Kommando == 79) Collections.addAll(linje,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Kommando == 87 || Kommando == 88) linje.add("addl $" + (Kommando == 87 ? 4 : 8) + ", %esp");
            else if (Kommando >= 89 && Kommando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] rekkjefølgje_Liste = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Kommando - 89]; 순번++) linje.add("popl " + 저장기들[순번]);
                for (int 순번 : rekkjefølgje_Liste[Kommando - 89]) linje.add("pushl " + 저장기들[순번]);
            } else if (Kommando == 96 || Kommando == 100 || Kommando == 104 || Kommando == 126 || Kommando == 128 || Kommando == 130) {
                String operasjon_VALUE = Kommando == 96 ? "addl" : Kommando == 100 ? "subl" : Kommando == 104 ? "imull" : Kommando == 126 ? "andl" : Kommando == 128 ? "orl" : "xorl";
                Collections.addAll(linje,"popl %ecx","popl %eax",operasjon_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Kommando == 108 || Kommando == 112) Collections.addAll(linje,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + plassere_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + plassere_INDEX + "_divide","xorl %edx, %edx","jmp " + plassere_INDEX + "_done",plassere_INDEX + "_divide:","cltd","idivl %ecx",plassere_INDEX + "_done:","pushl " + (Kommando == 108 ? "%eax" : "%edx"));
            else if (Kommando == 116) linje.add("negl (%esp)");
            else if (Kommando == 120 || Kommando == 122 || Kommando == 124) Collections.addAll(linje,"popl %ecx","popl %eax",(Kommando == 120 ? "sall" : Kommando == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Kommando == 132) {
                int INDEX = kommando_data.한바이트(), 증가 = kommando_data.부호한바이트(); sjekk_lokal(INDEX,lokal_COUNT); linje.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Kommando >= 145 && Kommando <= 147) Collections.addAll(linje,"popl %eax",Kommando == 145 ? "movsbl %al, %eax" : Kommando == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Kommando >= 153 && Kommando <= 166) {
                if (Kommando <= 158) Collections.addAll(linje,"popl %eax","testl %eax, %eax");
                else Collections.addAll(linje,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int mål_VALUE = Posisjon + kommando_data.부호두바이트(); grein_Liste.add(mål_VALUE); linje.add(비교들[Kommando - (Kommando <= 158 ? 153 : 159)] + " " + 표식 + "_b" + mål_VALUE);
            } else if (Kommando == 167 || Kommando == 200) {
                int mål_VALUE = Posisjon + (Kommando == 167 ? kommando_data.부호두바이트() : kommando_data.네바이트()); grein_Liste.add(mål_VALUE); linje.add("jmp " + 표식 + "_b" + mål_VALUE);
            } else if (Kommando == 170 || Kommando == 171) {
                while (kommando_data.Posisjon % 4 != 0) kommando_data.한바이트();
                int standardverdi = Posisjon + kommando_data.네바이트(); grein_Liste.add(standardverdi); linje.add("popl %eax");
                int vare_COUNT, 아래 = 0;
                if (Kommando == 170) { 아래 = kommando_data.네바이트(); int 위 = kommando_data.네바이트(); long lengd_VALUE = (long)위 - 아래 + 1; if (lengd_VALUE < 1 || lengd_VALUE > (kommando_data.data.length - kommando_data.Posisjon) / 4) throw new Omsetjing_feil("switch klipp FEIL"); vare_COUNT = (int)lengd_VALUE; }
                else { vare_COUNT = kommando_data.네바이트(); if (vare_COUNT < 0 || vare_COUNT > (kommando_data.data.length - kommando_data.Posisjon) / 8) throw new Omsetjing_feil("switch Storleik FEIL"); }
                for (int 순번 = 0; 순번 < vare_COUNT; 순번++) {
                    int VALUE = Kommando == 170 ? 아래 + 순번 : kommando_data.네바이트(), mål_VALUE = Posisjon + kommando_data.네바이트(); grein_Liste.add(mål_VALUE);
                    Collections.addAll(linje,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + mål_VALUE);
                }
                linje.add("jmp " + 표식 + "_b" + standardverdi);
            } else if (Kommando == 172 || Kommando == 176 || Kommando == 177) {
                if (Kommando != 177) linje.add("popl %eax"); Collections.addAll(linje,"leave","ret");
            } else if (Kommando == 178 || Kommando == 179) {
                metode_Oppslagsverk Oppslagsverk = time_VALUE.Oppslagsverk(kommando_data.두바이트()); if (!필드들.containsKey(Oppslagsverk)) throw new Omsetjing_feil("알 수 없는 felt_VALUE_0f39cf1c");
                Collections.addAll(linje,"call " + symbol("init",Oppslagsverk.eigar_VALUE),(Kommando == 178 ? "pushl " : "popl ") + symbol("field",Oppslagsverk.부분들()));
            } else if (Kommando == 184) {
                metode_Oppslagsverk Oppslagsverk = time_VALUE.Oppslagsverk(kommando_data.두바이트()); if (!함수들.containsKey(Oppslagsverk)) throw new Omsetjing_feil("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Oppslagsverk.서술); Collections.addAll(linje,"call " + symbol("init",Oppslagsverk.eigar_VALUE),"call " + symbol("method",Oppslagsverk.부분들()));
                if (!호출형식.Argument.isEmpty()) linje.add("addl $" + 호출형식.Argument.size() * 4 + ", %esp");
                if (!호출형식.levere_tilbake_forretningsmål.equals("V")) linje.add("pushl %eax");
            } else if (Kommando == 182) {
                metode_Oppslagsverk Oppslagsverk = time_VALUE.Oppslagsverk(kommando_data.두바이트());
                if (Oppslagsverk.equals(new metode_Oppslagsverk("java/lang/String","length","()I"))) Collections.addAll(linje,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Oppslagsverk.equals(new metode_Oppslagsverk("java/lang/String","charAt","(I)C"))) Collections.addAll(linje,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Omsetjing_feil("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Kommando == 188) {
                if (kommando_data.한바이트() != 10) throw new Omsetjing_feil("new int[]만 støtte_VALUE"); Collections.addAll(linje,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Kommando == 190) Collections.addAll(linje,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Kommando == 196) {
                int filtype_VALUE = kommando_data.한바이트(), INDEX = kommando_data.두바이트(); sjekk_lokal(INDEX,lokal_COUNT);
                if (filtype_VALUE == 21 || filtype_VALUE == 25 || filtype_VALUE == 54 || filtype_VALUE == 58) linje.add((filtype_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (filtype_VALUE == 132) linje.add("addl $" + kommando_data.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Omsetjing_feil("wide Kommando 미지원");
            } else if (Kommando == 198 || Kommando == 199) {
                int mål_VALUE = Posisjon + kommando_data.부호두바이트(); grein_Liste.add(mål_VALUE); Collections.addAll(linje,"popl %eax","testl %eax, %eax",(Kommando == 198 ? "je " : "jne ") + 표식 + "_b" + mål_VALUE);
            } else throw new Omsetjing_feil("미지원 Kommando: " + Kommando);
        }
        if (!경계들.containsAll(grein_Liste)) throw new Omsetjing_feil("Kommando 경계가 아닌 곳으로 grein");
        linje.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",linje);
    }
    String X_86_konstant(time_data data, int INDEX) {
        if (data.상수종류[INDEX] == 3) return data.konstant_data[INDEX].toString();
        if (data.상수종류[INDEX] == 8) return streng_symbol(data.문자((Integer)data.konstant_data[INDEX]));
        throw new Omsetjing_feil("정수와 streng_VALUE 상수만 støtte_VALUE");
    }
    String 엑스조립본(String oppføring_p, List<String> 내보냄, String mål) throws IOException {
        Map<String,String> maskin_tabell = new HashMap<>();
        for (String linje : Files.readAllLines(ressurs_bane.resolve("엑스기계함수.tsv"))) { String[] pare_VALUE = linje.split("\t"); if (pare_VALUE[0].equals(mål)) maskin_tabell.put(pare_VALUE[1] + pare_VALUE[2],pare_VALUE[3]); }
        int plassere_INDEX = oppføring_p.lastIndexOf('.'); if (plassere_INDEX < 0) throw new Omsetjing_feil("oppføring_p Tilordne_VALUE FEIL");
        String eigar_VALUE = oppføring_p.substring(0,plassere_INDEX).replace('.','/'), metode_oppføring_namn = oppføring_p.substring(plassere_INDEX + 1); metode_Oppslagsverk oppføring_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metode_Oppslagsverk Oppslagsverk = new metode_Oppslagsverk(eigar_VALUE,metode_oppføring_namn,서술); if (함수들.containsKey(Oppslagsverk)) { if (oppføring_p_VALUE != null) throw new Omsetjing_feil("겹친 oppføring_p"); oppføring_p_VALUE = Oppslagsverk; } }
        if (oppføring_p_VALUE == null || (함수들.get(oppføring_p_VALUE).tilgang_oppføring & 0x100) != 0) throw new Omsetjing_feil("oppføring_p_VALUE FUNCTION_VALUE format_VALUE FEIL");
        List<String> linje = new ArrayList<>(); linje.add(".code32");
        for (time_data data : 클래스들.values()) {
            String status_VALUE = symbol("state",data.Namn), starte = symbol("init",data.Namn);
            Collections.addAll(linje,".bss",".balign 4",status_VALUE + ": .long 0",".text",starte + ":","cmpl $0, " + status_VALUE,"jne " + starte + "_done","movl $1, " + status_VALUE);
            metode_Oppslagsverk 초기화참조 = new metode_Oppslagsverk(data.Namn,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) linje.add("call " + symbol("method",초기화참조.부분들()));
            Collections.addAll(linje,"movl $2, " + status_VALUE,starte + "_done:","ret");
            for (medlem_data felt_VALUE_0f39cf1c : data.felt_VALUE_0f39cf1c) {
                byte[] konstant_VALUE = felt_VALUE_0f39cf1c.attributt_VALUE.get("ConstantValue"); String VALUE = konstant_VALUE == null ? "0" : X_86_konstant(data,new data_Lesar(konstant_VALUE).두바이트());
                Collections.addAll(linje,".data",".balign 4",symbol("field",data.Namn,felt_VALUE_0f39cf1c.Namn,felt_VALUE_0f39cf1c.서술) + ": .long " + VALUE);
            }
            for (medlem_data FUNCTION_VALUE : data.FUNCTION_VALUE) if (!FUNCTION_VALUE.Namn.equals("<init>")) linje.add(X_86_metode_brødtekst(new metode_Oppslagsverk(data.Namn,FUNCTION_VALUE.Namn,FUNCTION_VALUE.서술),FUNCTION_VALUE,maskin_tabell,mål));
        }
        Collections.addAll(linje,".text",".globl java_entry","java_entry:","call " + symbol("init",oppføring_p_VALUE.eigar_VALUE),"call " + symbol("method",oppføring_p_VALUE.부분들()));
        if (oppføring_p_VALUE.서술.equals("()V")) linje.add("xorl %eax, %eax"); linje.add("ret");
        for (String Tilordne_VALUE : 내보냄) {
            int skiljeteikn_VALUE = Tilordne_VALUE.indexOf('='); if (skiljeteikn_VALUE < 1) throw new Omsetjing_feil("내보내기 Tilordne_VALUE FEIL");
            String ekstern_VALUE = Tilordne_VALUE.substring(0,skiljeteikn_VALUE), FUNCTION_VALUE = Tilordne_VALUE.substring(skiljeteikn_VALUE + 1); int divisjon_forretningsmål = FUNCTION_VALUE.lastIndexOf('.');
            if (divisjon_forretningsmål < 0 || !ekstern_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Omsetjing_feil("내보내기 symbol FEIL");
            String time_VALUE = FUNCTION_VALUE.substring(0,divisjon_forretningsmål).replace('.','/'), Namn = FUNCTION_VALUE.substring(divisjon_forretningsmål + 1); metode_Oppslagsverk merkt_område_VALUE = null;
            for (metode_Oppslagsverk Oppslagsverk : 함수들.keySet()) if (Oppslagsverk.eigar_VALUE.equals(time_VALUE) && Oppslagsverk.Namn.equals(Namn)) { if (merkt_område_VALUE != null) throw new Omsetjing_feil("겹친 내보내기 mål"); merkt_område_VALUE = Oppslagsverk; }
            if (merkt_område_VALUE == null) throw new Omsetjing_feil("내보낼 함수가 없음");
            Collections.addAll(linje,".text",".globl " + ekstern_VALUE,ekstern_VALUE + ":","call " + symbol("init",merkt_område_VALUE.eigar_VALUE),"jmp " + symbol("method",merkt_område_VALUE.부분들()));
        }
        linje.add(".section .rodata");
        for (Map.Entry<String,String> oppføring_VALUE : 문자열들.entrySet()) {
            Collections.addAll(linje,".balign 4",oppføring_VALUE.getValue() + ":",".long " + oppføring_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char leksjon_VALUE : oppføring_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(leksjon_VALUE)); if (!단위들.isEmpty()) linje.add(".long " + String.join(",",단위들));
        }
        linje.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",linje) + "\n";
    }
    static void Utfør_verktøy(List<String> Kommando) throws Exception {
        if (new ProcessBuilder(Kommando).inheritIO().start().waitFor() != 0) throw new Omsetjing_feil("byggje_kjelde FEIL: " + Kommando.get(0));
    }
    static String data_streng(String Tekst) { return "\"" + Tekst.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Omsetjing(List<Path> 입력들, String mål, String oppføring_p, List<String> 내보냄, Path Utdata, Path ressurs_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), time_bane = 임시.resolve("classes"); Files.createDirectory(time_bane);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",time_bane.toString(),"-sourcepath",time_bane.toString(),"-d",time_bane.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int kjelde_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Utdata.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Omsetjing_feil("Utdata 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); kjelde_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Omsetjing_feil(".java 또는 .class만 støtte_VALUE");
            }
            if (kjelde_COUNT > 0) Utfør_verktøy(자바명령);
            try (java.util.stream.Stream<Path> bane_Liste = Files.walk(time_bane)) { bane_Liste.filter(STIGE -> STIGE.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,mål.equals("user") ? "user" : "kernel",262144,ressurs_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(oppføring_p,내보냄,mål); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path verktøy_plassere = ressurs_VALUE.getParent();
            Utfør_verktøy(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Utfør_verktøy(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),verktøy_plassere.resolve("Common_Language_Runtime_støtte.s").toString()));
            List<String> Kopla_til = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (mål.equals("kernel")) Kopla_til.add("-r");
            else {
                Utfør_verktøy(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),verktøy_plassere.resolve(mål.equals("user") ? "START_brukar_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Kopla_til,"-e","_start",임시.resolve("start.o").toString());
                if (mål.equals("user")) Collections.addAll(Kopla_til,"-T",verktøy_plassere.resolve("brukar_kople_Oppsett.ld").toString());
            }
            Collections.addAll(Kopla_til,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Utfør_verktøy(Kopla_til);
            Utdata = Utdata.toAbsolutePath(); Files.createDirectories(Utdata.getParent()); Path publiser_VALUE = Files.createTempFile(Utdata.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publiser_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(publiser_VALUE,Utdata,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publiser_VALUE); }
            Files.setPosixFilePermissions(Utdata,java.nio.file.attribute.PosixFilePermissions.fromString(mål.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Utdata + ".s"),조립,StandardCharsets.UTF_8);
            List<String> symbol_data = new ArrayList<>(), kjeldedata = new ArrayList<>();
            for (metode_Oppslagsverk Oppslagsverk : CONVERT_VALUE.함수들.keySet()) symbol_data.add(data_streng(symbol("method",Oppslagsverk.부분들())) + ":" + data_streng(Oppslagsverk.eigar_VALUE + "." + Oppslagsverk.Namn + Oppslagsverk.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_fil = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Tekst = new StringBuilder(); for (byte VALUE : hash_fil) Tekst.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                kjeldedata.add(data_streng(입력.toAbsolutePath().toString()) + ":" + data_streng(Tekst.toString()));
            }
            Files.writeString(Paths.get(Utdata + ".json"),"{\"target\":" + data_streng(mål) + ",\"entry\":" + data_streng(oppføring_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbol_data) + "},\"sources\":{" + String.join(",",kjeldedata) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> bane_Liste = Files.walk(임시)) { for (Path STIGE : (Iterable<Path>)bane_Liste.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(STIGE); }
        }
    }
    public static void main(String[] Argument) {
        try {
            String oppføring_p = null, mål = "kernel", X_86_mål = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> bane_Liste = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argument.length; 순번++) {
                String VALUE = Argument[순번];
                switch (VALUE) {
                    case "--target": X_86_mål = Argument[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry time_VALUE.FUNCTION_VALUE -o Utdata [--target linux|kernel|user] [--profile kernel|user] [--export symbol=time_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": oppføring_p = Argument[++순번]; break;
                    case "--profile": mål = Argument[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argument[++순번]); break;
                    case "--export": 내보냄.add(Argument[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argument[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Omsetjing_feil("알 수 없는 옵션: " + VALUE); bane_Liste.add(Paths.get(VALUE));
                }
            }
            if (oppføring_p == null || 출력경로 == null || bane_Liste.isEmpty()) throw new Omsetjing_feil("--entry, -o, time_VALUE 파일이 필요합니다");
            Path ressurs_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_mål != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_mål)) throw new Omsetjing_feil("알 수 없는 Utfør_kommando mål");
                X_86_Omsetjing(bane_Liste,X_86_mål,oppføring_p,내보냄,출력경로,ressurs_VALUE); return;
            }
            String KJELDE = new 기계어미리번역(bane_Liste, mål, 낱말수, ressurs_VALUE).generere(oppføring_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, KJELDE, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception FEIL) { System.err.println("byggje_kjelde FEIL: " + FEIL.getMessage()); System.exit(1); }
    }
}
