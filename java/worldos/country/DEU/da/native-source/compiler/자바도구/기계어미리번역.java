// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Hold_VÆRDI 파일에서 독립 ARM64 커널용 C 원문을 만든다. vært JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Oversættelse_fejl extends RuntimeException {
        Oversættelse_fejl(String 설명) { super(설명); }
    }
    static final class data_Læser {
        final byte[] data;
        int Placering;
        data_Læser(byte[] input_data) { data = input_data; }
        byte[] Læse(int varighed_VÆRDI) {
            if (varighed_VÆRDI < 0 || varighed_VÆRDI > data.length - Placering) throw new Oversættelse_fejl("잘린 Hold_VÆRDI 또는 Kommando data");
            byte[] KR = Arrays.copyOfRange(data, Placering, Placering + varighed_VÆRDI); Placering += varighed_VÆRDI; return KR;
        }
        int 한바이트() { if (Placering >= data.length) throw new Oversættelse_fejl("잘린 Kommando data"); return data[Placering++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class medlem_data {
        final int åbne_post;
        final String Navn, 서술;
        final Map<String, byte[]> attribut_VÆRDI;
        medlem_data(int åbne_VÆRDI, String navn_VÆRDI, String 서술값, Map<String, byte[]> attribut_data) {
            åbne_post = åbne_VÆRDI; Navn = navn_VÆRDI; 서술 = 서술값; attribut_VÆRDI = attribut_data;
        }
    }
    static final class metode_referere implements Comparable<metode_referere> {
        final String ejer_VÆRDI, Navn, 서술;
        metode_referere(String 소유값, String navn_VÆRDI, String 서술값) { ejer_VÆRDI = 소유값; Navn = navn_VÆRDI; 서술 = 서술값; }
        String[] 부분들() { return new String[]{ejer_VÆRDI, Navn, 서술}; }
        public int compareTo(metode_referere peer_VÆRDI) {
            int Sammenligning_VÆRDI = ejer_VÆRDI.compareTo(peer_VÆRDI.ejer_VÆRDI);
            if (Sammenligning_VÆRDI == 0) Sammenligning_VÆRDI = Navn.compareTo(peer_VÆRDI.Navn);
            return Sammenligning_VÆRDI == 0 ? 서술.compareTo(peer_VÆRDI.서술) : Sammenligning_VÆRDI;
        }
        public boolean equals(Object peer_VÆRDI) { return peer_VÆRDI instanceof metode_referere && compareTo((metode_referere) peer_VÆRDI) == 0; }
        public int hashCode() { return Objects.hash(ejer_VÆRDI, Navn, 서술); }
    }
    static final class Hold_data {
        final int[] 상수종류;
        final Object[] konstant_data;
        final String Navn;
        final List<medlem_data> feltværdi, FUNKTION_VÆRDI;
        Hold_data(Path Sti) throws IOException {
            data_Læser Læser_VÆRDI = new data_Læser(Files.readAllBytes(Sti));
            if (Læser_VÆRDI.네바이트() != 0xcafebabe) throw new Oversættelse_fejl("Java Hold_VÆRDI 표식이 아님");
            Læser_VÆRDI.Læse(4);
            int vare_TÆL = Læser_VÆRDI.두바이트(); 상수종류 = new int[vare_TÆL]; konstant_data = new Object[vare_TÆL];
            for (int 순번 = 1; 순번 < vare_TÆL; 순번++) {
                int 종류 = Læser_VÆRDI.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int varighed_VÆRDI = Læser_VÆRDI.두바이트();
                        byte[] tegn_buffer = Læser_VÆRDI.Læse(varighed_VÆRDI), 길이붙인자료 = new byte[varighed_VÆRDI + 2];
                        길이붙인자료[0] = (byte)(varighed_VÆRDI >> 8); 길이붙인자료[1] = (byte)varighed_VÆRDI;
                        System.arraycopy(tegn_buffer, 0, 길이붙인자료, 2, varighed_VÆRDI);
                        konstant_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstant_data[순번] = Læser_VÆRDI.네바이트(); break;
                    case 4: Læser_VÆRDI.Læse(4); break;
                    case 5: case 6: Læser_VÆRDI.Læse(8); 순번++; break;
                    case 7: case 8: case 16: konstant_data[순번] = Læser_VÆRDI.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstant_data[순번] = new int[]{Læser_VÆRDI.두바이트(), Læser_VÆRDI.두바이트()}; break;
                    case 15: konstant_data[순번] = new int[]{Læser_VÆRDI.한바이트(), Læser_VÆRDI.두바이트()}; break;
                    default: throw new Oversættelse_fejl("지원하지 않는 konstant_VÆRDI 종류: " + 종류);
                }
            }
            Læser_VÆRDI.두바이트(); Navn = klassenavn(Læser_VÆRDI.두바이트());
            if (!klassenavn(Læser_VÆRDI.두바이트()).equals("java/lang/Object") || Læser_VÆRDI.두바이트() != 0)
                throw new Oversættelse_fejl(Navn + ": 상속 및 인터페이스 미지원");
            feltværdi = 멤버읽기(Læser_VÆRDI); FUNKTION_VÆRDI = 멤버읽기(Læser_VÆRDI); 속성읽기(Læser_VÆRDI);
            if (Læser_VÆRDI.Placering != Læser_VÆRDI.data.length) throw new Oversættelse_fejl("Hold_VÆRDI 뒤에 남은 data");
        }
        String 문자(int INDEKS) {
            if (INDEKS < 1 || INDEKS >= 상수종류.length || 상수종류[INDEKS] != 1) throw new Oversættelse_fejl("문자 konstant_VÆRDI INDEKS fejl");
            return (String) konstant_data[INDEKS];
        }
        String klassenavn(int INDEKS) {
            if (INDEKS < 1 || INDEKS >= 상수종류.length || 상수종류[INDEKS] != 7) throw new Oversættelse_fejl("Hold_VÆRDI referere fejl");
            return 문자((Integer)konstant_data[INDEKS]);
        }
        metode_referere referere(int INDEKS) {
            if (INDEKS < 1 || INDEKS >= 상수종류.length || 상수종류[INDEKS] < 9 || 상수종류[INDEKS] > 11) throw new Oversættelse_fejl("멤버 referere fejl");
            int[] danne_par_VÆRDI = (int[])konstant_data[INDEKS], navn_danne_par = (int[])konstant_data[danne_par_VÆRDI[1]];
            return new metode_referere(klassenavn(danne_par_VÆRDI[0]), 문자(navn_danne_par[0]), 문자(navn_danne_par[1]));
        }
        Map<String, byte[]> 속성읽기(data_Læser Læser_VÆRDI) {
            Map<String, byte[]> KR = new LinkedHashMap<>();
            int vare_TÆL = Læser_VÆRDI.두바이트();
            for (int 순번 = 0; 순번 < vare_TÆL; 순번++) {
                String attribut_navn = 문자(Læser_VÆRDI.두바이트()); byte[] VÆRDI = Læser_VÆRDI.Læse(Læser_VÆRDI.네바이트());
                if (KR.put(attribut_navn, VÆRDI) != null) throw new Oversættelse_fejl("겹친 attribut_VÆRDI: " + attribut_navn);
            }
            return KR;
        }
        List<medlem_data> 멤버읽기(data_Læser Læser_VÆRDI) {
            List<medlem_data> KR = new ArrayList<>(); int vare_TÆL = Læser_VÆRDI.두바이트();
            for (int 순번 = 0; 순번 < vare_TÆL; 순번++) {
                int åbne_post = Læser_VÆRDI.두바이트(); String metode_post_navn = 문자(Læser_VÆRDI.두바이트()), 서술 = 문자(Læser_VÆRDI.두바이트());
                KR.add(new medlem_data(åbne_post, metode_post_navn, 서술, 속성읽기(Læser_VÆRDI)));
            }
            return KR;
        }
    }
    static final class 함수형식 {
        final List<String> Argumenter = new ArrayList<>();
        final String returnere_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Oversættelse_fejl("FUNKTION_VÆRDI 서술 fejl: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Oversættelse_fejl("FUNKTION_VÆRDI 서술 fejl: " + 서술);
            Argumenter.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumenter.contains("V") || 반환들.size() != 1) throw new Oversættelse_fejl("FUNKTION_VÆRDI 서술 fejl: " + 서술);
            returnere_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> KR = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Placering = 0; Placering < 서술.length();) {
            String markering_VÆRDI = null;
            for (String format_VÆRDI : 허용형식) if (서술.startsWith(format_VÆRDI, Placering)) { markering_VÆRDI = format_VÆRDI; break; }
            if (markering_VÆRDI == null) throw new Oversættelse_fejl("지원하지 않는 datatype: " + 서술);
            KR.add(markering_VÆRDI); Placering += markering_VÆRDI.length();
        }
        return KR;
    }
    static String symbol(String 종류, String... 부분들) {
        try {
            byte[] hash_fil = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Tekst = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Tekst.append(String.format(Locale.ROOT, "%02x", hash_fil[순번] & 255));
            return Tekst.toString();
        } catch (Exception fejl) { throw new Oversættelse_fejl(fejl.toString()); }
    }
    final Map<String, Hold_data> 클래스들 = new TreeMap<>();
    final Map<metode_referere, medlem_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), maskine_Functions_c3a8e64a = new LinkedHashMap<>();
    final String udførelse_mål, maskine_Hold;
    final int heap_Ord_TÆL;
    final Path ressource_sti;
    기계어미리번역(List<Path> sti_Liste, String mål, int 낱말수, Path ressource_VÆRDI) throws IOException {
        if ((!mål.equals("kernel") && !mål.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Oversættelse_fejl("Udfør_kommando mål 또는 Hukommelse_VÆRDI mail_område Størrelse fejl");
        udførelse_mål = mål; heap_Ord_TÆL = 낱말수; ressource_sti = ressource_VÆRDI;
        // 이 이름도 국가별 kilde_træ generere 시 해당 언어로 옮긴다.
        maskine_Hold = mål.equals("kernel") ? "Tavle" : "bruger";
        for (String Linje : Files.readAllLines(ressource_VÆRDI.resolve("maskine_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Linje.split("\t", -1);
            if (부분들.length != 4) throw new Oversættelse_fejl("maskine FUNKTION_VÆRDI data fejl");
            if (부분들[0].equals(mål)) maskine_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Sti : sti_Liste) {
            Hold_data data = new Hold_data(Sti);
            if (클래스들.put(data.Navn, data) != null) throw new Oversættelse_fejl("중복 Hold_VÆRDI: " + data.Navn);
            for (medlem_data feltværdi : data.feltværdi) {
                if ((feltværdi.åbne_post & 8) == 0 || 형식읽기(feltværdi.서술).equals(Collections.singletonList("V"))) throw new Oversættelse_fejl("statisk_VÆRDI 필드만 støtte_VÆRDI");
                if (필드들.put(new metode_referere(data.Navn, feltværdi.Navn, feltværdi.서술), feltværdi) != null) throw new Oversættelse_fejl("중복 feltværdi");
            }
            for (medlem_data FUNKTION_VÆRDI : data.FUNKTION_VÆRDI) {
                if (FUNKTION_VÆRDI.Navn.equals("<init>")) continue;
                if ((FUNKTION_VÆRDI.åbne_post & 8) == 0 || (FUNKTION_VÆRDI.åbne_post & (0x20 | 0x400)) != 0) throw new Oversættelse_fejl("statisk_VÆRDI 비동기화 함수만 støtte_VÆRDI");
                new 함수형식(FUNKTION_VÆRDI.서술);
                if (함수들.put(new metode_referere(data.Navn, FUNKTION_VÆRDI.Navn, FUNKTION_VÆRDI.서술), FUNKTION_VÆRDI) != null) throw new Oversættelse_fejl("중복 FUNKTION_VÆRDI");
            }
        }
    }
    String streng_symbol(String Tekst) { return 문자열들.computeIfAbsent(Tekst, VÆRDI -> "j_text_" + 문자열들.size()); }
    String konstant_udtryk(Hold_data data, int INDEKS) {
        if (INDEKS < 1 || INDEKS >= data.상수종류.length) throw new Oversættelse_fejl("konstant_VÆRDI INDEKS klippe fejl");
        if (data.상수종류[INDEKS] == 3) return "(word)(uint32_t)(" + data.konstant_data[INDEKS] + ")";
        if (data.상수종류[INDEKS] == 8) return "(word)" + streng_symbol(data.문자((Integer)data.konstant_data[INDEKS]));
        throw new Oversættelse_fejl("정수와 streng_VÆRDI 상수만 støtte_VÆRDI");
    }
    String 함수원형(metode_referere referere) {
        List<String> 인수들 = new ArrayList<>(); int vare_TÆL = new 함수형식(referere.서술).Argumenter.size();
        for (int 순번 = 0; 순번 < vare_TÆL; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symbol("method", referere.부분들()) + "(" + (vare_TÆL == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void check_lokal(int INDEKS, int lokal_variabel_TÆL) { if (INDEKS < 0 || INDEKS >= lokal_variabel_TÆL) throw new Oversættelse_fejl("lokal_Omfang variabel_VÆRDI INDEKS klippe fejl"); }
    void 분기넣기(List<String> Udgang, Set<Integer> gren_Liste, int Placering, int 이동량, String lidelse) {
        int destination_VÆRDI = Placering + 이동량; gren_Liste.add(destination_VÆRDI);
        Udgang.add((lidelse == null ? "" : "if (" + lidelse + ") ") + "goto b" + destination_VÆRDI + ";");
    }
    String metode_brødtekst(metode_referere FUNKTION_VÆRDI, medlem_data data) {
        byte[] brødtekst_data = data.attribut_VÆRDI.get("Code"); if (brødtekst_data == null) throw new Oversættelse_fejl("FUNKTION_VÆRDI 몸체가 없음: " + FUNKTION_VÆRDI.Navn);
        data_Læser Læser_VÆRDI = new data_Læser(brødtekst_data); int 쌓임깊이 = Læser_VÆRDI.두바이트(), lokal_variabel_TÆL = Læser_VÆRDI.두바이트();
        data_Læser kommando_data = new data_Læser(Læser_VÆRDI.Læse(Læser_VÆRDI.네바이트()));
        if (Læser_VÆRDI.두바이트() != 0) throw new Oversættelse_fejl("try/catch/finally 미지원");
        함수형식 format_VÆRDI = new 함수형식(FUNKTION_VÆRDI.서술); if (lokal_variabel_TÆL < format_VÆRDI.Argumenter.size()) throw new Oversættelse_fejl("매개변수보다 적은 lokal_Omfang variabel_VÆRDI");
        Hold_data Hold_VÆRDI = 클래스들.get(FUNKTION_VÆRDI.ejer_VÆRDI);
        List<String> Udgang = new ArrayList<>(); Udgang.add(함수원형(FUNKTION_VÆRDI) + " {");
        Udgang.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(lokal_variabel_TÆL, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VÆRDI.Argumenter.size(); 순번++) Udgang.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), gren_Liste = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (kommando_data.Placering < kommando_data.data.length) {
            int Placering = kommando_data.Placering, Kommando = kommando_data.한바이트(); 경계들.add(Placering); Udgang.add("b" + Placering + ":;");
            if (Kommando == 0) continue;
            if (Kommando == 1) Udgang.add("PUSH(0);");
            else if (Kommando >= 2 && Kommando <= 8) Udgang.add("PUSH((uint32_t)(" + (Kommando - 3) + "));");
            else if (Kommando == 16 || Kommando == 17) Udgang.add("PUSH((uint32_t)(" + (Kommando == 16 ? kommando_data.부호한바이트() : kommando_data.부호두바이트()) + "));");
            else if (Kommando == 18 || Kommando == 19) Udgang.add("PUSH(" + konstant_udtryk(Hold_VÆRDI, Kommando == 18 ? kommando_data.한바이트() : kommando_data.두바이트()) + ");");
            else if (Kommando == 21 || Kommando == 25 || (Kommando >= 26 && Kommando <= 29) || (Kommando >= 42 && Kommando <= 45)) {
                int INDEKS = Kommando == 21 || Kommando == 25 ? kommando_data.한바이트() : Kommando - (Kommando <= 29 ? 26 : 42);
                check_lokal(INDEKS, lokal_variabel_TÆL); Udgang.add("PUSH(l[" + INDEKS + "]);");
            } else if (Kommando == 54 || Kommando == 58 || (Kommando >= 59 && Kommando <= 62) || (Kommando >= 75 && Kommando <= 78)) {
                int INDEKS = Kommando == 54 || Kommando == 58 ? kommando_data.한바이트() : Kommando - (Kommando <= 62 ? 59 : 75);
                check_lokal(INDEKS, lokal_variabel_TÆL); Udgang.add("l[" + INDEKS + "] = POP();");
            } else if (Kommando == 46) Udgang.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Kommando == 79) Udgang.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Kommando == 87 || Kommando == 88) Udgang.add(Kommando == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Kommando >= 89 && Kommando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ordre_Liste = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Kommando - 89]; 순번++) Udgang.add("abcd".charAt(순번) + " = POP();");
                for (char VÆRDI : ordre_Liste[Kommando - 89].toCharArray()) Udgang.add("PUSH(" + VÆRDI + ");");
            } else if (Kommando == 96 || Kommando == 100 || Kommando == 104 || Kommando == 126 || Kommando == 128 || Kommando == 130) {
                String kirurgi_VÆRDI = Kommando == 96 ? "+" : Kommando == 100 ? "-" : Kommando == 104 ? "*" : Kommando == 126 ? "&" : Kommando == 128 ? "|" : "^";
                Udgang.add("b = POP(); a = POP(); PUSH((uint32_t)a " + kirurgi_VÆRDI + " (uint32_t)b);");
            } else if (Kommando == 108 || Kommando == 112) Udgang.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Kommando == 112 ? 1 : 0) + "));");
            else if (Kommando == 116) Udgang.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Kommando == 120 || Kommando == 122 || Kommando == 124) {
                Udgang.add("b = POP(); a = POP();"); Udgang.add("PUSH(" + (Kommando == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Kommando == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Kommando == 132) {
                int INDEKS = kommando_data.한바이트(), gradvis_forøgelse_sum = kommando_data.부호한바이트(); check_lokal(INDEKS, lokal_variabel_TÆL);
                Udgang.add("l[" + INDEKS + "] = (uint32_t)l[" + INDEKS + "] + (uint32_t)(" + gradvis_forøgelse_sum + ");");
            } else if (Kommando >= 145 && Kommando <= 147) Udgang.add("a = POP(); PUSH((uint32_t)(" + (Kommando == 145 ? "int8_t" : Kommando == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Kommando >= 153 && Kommando <= 158) {
                Udgang.add("a = POP();"); 분기넣기(Udgang, gren_Liste, Placering, kommando_data.부호두바이트(), "(int32_t)a " + 비교들[Kommando - 153] + " 0");
            } else if (Kommando >= 159 && Kommando <= 166) {
                Udgang.add("b = POP(); a = POP();"); 분기넣기(Udgang, gren_Liste, Placering, kommando_data.부호두바이트(), Kommando >= 165 ? "a " + 비교들[Kommando - 159] + " b" : "(int32_t)a " + 비교들[Kommando - 159] + " (int32_t)b");
            } else if (Kommando == 167 || Kommando == 200) 분기넣기(Udgang, gren_Liste, Placering, Kommando == 167 ? kommando_data.부호두바이트() : kommando_data.네바이트(), null);
            else if (Kommando == 170 || Kommando == 171) {
                while (kommando_data.Placering % 4 != 0) kommando_data.한바이트();
                int standardværdi = kommando_data.네바이트(); Udgang.add("a = POP();");
                if (Kommando == 170) {
                    int 아래 = kommando_data.네바이트(), 위 = kommando_data.네바이트(); long vare_TÆL = (long)위 - 아래 + 1;
                    if (vare_TÆL < 1 || vare_TÆL > (kommando_data.data.length - kommando_data.Placering) / 4) throw new Oversættelse_fejl("switch klippe fejl");
                    for (long VÆRDI = 아래; VÆRDI <= 위; VÆRDI++) 분기넣기(Udgang, gren_Liste, Placering, kommando_data.네바이트(), "(int32_t)a == (" + VÆRDI + ")");
                } else {
                    int vare_TÆL = kommando_data.네바이트(), frontvendt_data = 0;
                    if (vare_TÆL < 0 || vare_TÆL > (kommando_data.data.length - kommando_data.Placering) / 8) throw new Oversættelse_fejl("switch Størrelse fejl");
                    for (int 순번 = 0; 순번 < vare_TÆL; 순번++) {
                        int VÆRDI = kommando_data.네바이트(); if (순번 > 0 && VÆRDI <= frontvendt_data) throw new Oversættelse_fejl("switch ordre_VÆRDI fejl"); frontvendt_data = VÆRDI;
                        분기넣기(Udgang, gren_Liste, Placering, kommando_data.네바이트(), "(int32_t)a == (" + VÆRDI + ")");
                    }
                }
                분기넣기(Udgang, gren_Liste, Placering, standardværdi, null);
            } else if (Kommando == 172 || Kommando == 176 || Kommando == 177) Udgang.add("return " + (Kommando == 177 ? "0" : "POP()") + ";");
            else if (Kommando == 178 || Kommando == 179) {
                metode_referere referere = Hold_VÆRDI.referere(kommando_data.두바이트()); if (!필드들.containsKey(referere)) throw new Oversættelse_fejl("알 tal 없는 feltværdi");
                Udgang.add(symbol("init", referere.ejer_VÆRDI) + "();"); String feltværdi = symbol("field", referere.부분들());
                Udgang.add(Kommando == 178 ? "PUSH(" + feltværdi + ");" : feltværdi + " = POP();");
            } else if (Kommando == 184) {
                metode_referere referere = Hold_VÆRDI.referere(kommando_data.두바이트()); if (!함수들.containsKey(referere)) throw new Oversættelse_fejl("알 tal 없는 FUNKTION_VÆRDI");
                함수형식 호출형식 = new 함수형식(referere.서술); int vare_TÆL = 호출형식.Argumenter.size();
                Udgang.add(symbol("init", referere.ejer_VÆRDI) + "();"); Udgang.add("if(sp < " + vare_TÆL + ") kernel_panic(\"call stack underflow\"); sp -= " + vare_TÆL + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < vare_TÆL; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Udgang.add("a = " + symbol("method", referere.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.returnere_KR.equals("V")) Udgang.add("PUSH(a);");
            } else if (Kommando == 182) {
                metode_referere referere = Hold_VÆRDI.referere(kommando_data.두바이트());
                if (referere.equals(new metode_referere("java/lang/String", "length", "()I"))) Udgang.add("a = POP(); PUSH(length(a));");
                else if (referere.equals(new metode_referere("java/lang/String", "charAt", "(I)C"))) Udgang.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Oversættelse_fejl("가상 FUNKTION_VÆRDI 호출 미지원");
            } else if (Kommando == 188) {
                if (kommando_data.한바이트() != 10) throw new Oversættelse_fejl("new int[]만 støtte_VÆRDI"); Udgang.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Kommando == 190) Udgang.add("a = POP(); PUSH(length(a));");
            else if (Kommando == 196) {
                int udvidelse_VÆRDI = kommando_data.한바이트(), INDEKS = kommando_data.두바이트(); check_lokal(INDEKS, lokal_variabel_TÆL);
                if (udvidelse_VÆRDI == 21 || udvidelse_VÆRDI == 25) Udgang.add("PUSH(l[" + INDEKS + "]);");
                else if (udvidelse_VÆRDI == 54 || udvidelse_VÆRDI == 58) Udgang.add("l[" + INDEKS + "] = POP();");
                else if (udvidelse_VÆRDI == 132) Udgang.add("l[" + INDEKS + "] = (uint32_t)l[" + INDEKS + "] + (uint32_t)(" + kommando_data.부호두바이트() + ");");
                else throw new Oversættelse_fejl("미지원 wide Kommando");
            } else if (Kommando == 198 || Kommando == 199) {
                Udgang.add("a = POP();"); 분기넣기(Udgang, gren_Liste, Placering, kommando_data.부호두바이트(), "a " + (Kommando == 198 ? "==" : "!=") + " 0");
            } else throw new Oversættelse_fejl(FUNKTION_VÆRDI.ejer_VÆRDI + "." + FUNKTION_VÆRDI.Navn + ", byte_VÆRDI " + Placering + ": 미지원 Kommando " + Kommando);
        }
        if (!경계들.containsAll(gren_Liste)) throw new Oversættelse_fejl("Kommando 경계가 아닌 곳으로 gren");
        Udgang.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Udgang);
    }
    String eksportere_metode(String Link_symbol, String mål, boolean 진입점여부) {
        int positionsindeks = mål.lastIndexOf('.'); if (positionsindeks < 0 || !Link_symbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Oversættelse_fejl("내보내기 Tildel_VÆRDI fejl");
        String ejer_VÆRDI = mål.substring(0, positionsindeks).replace('.', '/'), Navn = mål.substring(positionsindeks + 1); metode_referere markering_VÆRDI = null;
        for (metode_referere referere : 함수들.keySet()) if (referere.ejer_VÆRDI.equals(ejer_VÆRDI) && referere.Navn.equals(Navn)) {
            if (markering_VÆRDI != null) throw new Oversættelse_fejl("겹친 내보내기 mål"); markering_VÆRDI = referere;
        }
        if (markering_VÆRDI == null || (함수들.get(markering_VÆRDI).åbne_post & 0x100) != 0) throw new Oversættelse_fejl("내보낼 함수가 없음 또는 native FUNKTION_VÆRDI");
        함수형식 format_VÆRDI = new 함수형식(markering_VÆRDI.서술);
        if ((진입점여부 && !format_VÆRDI.Argumenter.isEmpty()) || !Arrays.asList("V", "I").contains(format_VÆRDI.returnere_KR)) throw new Oversættelse_fejl("indgangspunkt_VÆRDI 또는 C grænse_VÆRDI format_VÆRDI fejl");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VÆRDI.Argumenter.size(); 순번++) {
            if (!format_VÆRDI.Argumenter.get(순번).equals("I")) throw new Oversættelse_fejl("C 경계는 int 인수만 støtte_VÆRDI");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VÆRDI.returnere_KR.equals("V") ? "void " : "int32_t ") + Link_symbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symbol("init", markering_VÆRDI.ejer_VÆRDI) + "(); " + (format_VÆRDI.returnere_KR.equals("V") ? "" : "return (int32_t)") + symbol("method", markering_VÆRDI.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generere(String indgangspunkt, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metode_referere, medlem_data> post_VÆRDI_962f286b : 함수들.entrySet()) {
            metode_referere referere = post_VÆRDI_962f286b.getKey(); medlem_data data = post_VÆRDI_962f286b.getValue(); 선언들.add(함수원형(referere) + ";");
            if ((data.åbne_post & 0x100) != 0) {
                String Tilslut = maskine_Functions_c3a8e64a.get(referere.Navn + referere.서술);
                if (!referere.ejer_VÆRDI.equals(maskine_Hold) || Tilslut == null) throw new Oversættelse_fejl("허용되지 않은 native FUNKTION_VÆRDI: " + referere.Navn);
                int vare_TÆL = new 함수형식(referere.서술).Argumenter.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < vare_TÆL; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Tilslut + "(" + (vare_TÆL == 0 ? "void" : String.join(",", Collections.nCopies(vare_TÆL, "word"))) + ");");
                몸체들.add(함수원형(referere) + " { return " + Tilslut + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metode_brødtekst(referere, data));
        }
        for (Map.Entry<metode_referere, medlem_data> post_VÆRDI_962f286b : 필드들.entrySet()) {
            metode_referere referere = post_VÆRDI_962f286b.getKey(); byte[] konstant_VÆRDI = post_VÆRDI_962f286b.getValue().attribut_VÆRDI.get("ConstantValue");
            String VÆRDI = konstant_VÆRDI == null ? "0" : konstant_udtryk(클래스들.get(referere.ejer_VÆRDI), new data_Læser(konstant_VÆRDI).두바이트());
            필드선언들.add("static word " + symbol("field", referere.부분들()) + " = " + VÆRDI + ";");
        }
        for (String Navn : 클래스들.keySet()) {
            String starte = symbol("init", Navn), status_VÆRDI = symbol("state", Navn);
            선언들.add("static void " + starte + "(void);"); 필드선언들.add("static unsigned " + status_VÆRDI + ";");
            metode_referere referere = new metode_referere(Navn, "<clinit>", "()V");
            몸체들.add("static void " + starte + "(void) { if(" + status_VÆRDI + ") return; " + status_VÆRDI + " = 1; " + (함수들.containsKey(referere) ? symbol("method", referere.부분들()) + "(); " : "") + status_VÆRDI + " = 2; }");
        }
        몸체들.add(eksportere_metode("java_entry", indgangspunkt, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Tildel_VÆRDI : 내보내기목록) {
            int positionsindeks = Tildel_VÆRDI.indexOf('='); if (positionsindeks < 1) throw new Oversættelse_fejl("내보내기 Tildel_VÆRDI fejl");
            String Navn = Tildel_VÆRDI.substring(0, positionsindeks); 공개이름.add(Navn); 몸체들.add(eksportere_metode(Navn, Tildel_VÆRDI.substring(positionsindeks + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> post_VÆRDI_962f286b : 문자열들.entrySet()) {
            String Tekst = post_VÆRDI_962f286b.getKey(); StringBuilder MATRIX_VÆRDI = new StringBuilder("static const word " + post_VÆRDI_962f286b.getValue() + "[] = {" + Tekst.length());
            for (int 순번 = 0; 순번 < Tekst.length(); 순번++) MATRIX_VÆRDI.append(", ").append((int)Tekst.charAt(순번));
            문자열선언들.add(MATRIX_VÆRDI.append("};").toString());
        }
        String støtte_VÆRDI = Files.readString(ressource_sti.resolve("CLR_støtte.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(heap_Ord_TÆL));
        return 기계원문한국어화(støtte_VÆRDI + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String KILDE, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> navn_tabel = new HashMap<>();
        for (String Linje : Files.readAllLines(ressource_sti.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] danne_par_VÆRDI = Linje.split("\t"); navn_tabel.put(danne_par_VÆRDI[0], danne_par_VÆRDI[1]);
        }
        Pattern del_udtryk = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = del_udtryk.matcher(KILDE); StringBuffer KR = new StringBuffer();
        while (찾개.find()) {
            String Navn = 찾개.group(), 새이름 = Navn;
            if (!Navn.startsWith("//") && !Navn.startsWith("/*") && !Navn.startsWith("\"") && !Navn.startsWith("'") && !공개이름.contains(Navn)) {
                새이름 = navn_tabel.getOrDefault(Navn, Navn);
                if (Navn.matches("a[0-9]+")) 새이름 = "Argumenter" + Navn.substring(1);
                if (Navn.matches("b[0-9]+")) 새이름 = "gren" + Navn.substring(1);
                if (범용표기) {
                    StringBuilder tegnsystem_VÆRDI = new StringBuilder();
                    for (char tegn_VÆRDI : 새이름.toCharArray()) tegnsystem_VÆRDI.append(tegn_VÆRDI < 128 ? Character.toString(tegn_VÆRDI) : String.format(Locale.ROOT, "\\u%04x", (int)tegn_VÆRDI));
                    새이름 = tegnsystem_VÆRDI.toString();
                }
            }
            찾개.appendReplacement(KR, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(KR); return KR.toString();
    }
    String X_86_metode_brødtekst(metode_referere FUNKTION_VÆRDI, medlem_data data, Map<String,String> maskine_tabel, String mål) {
        String mærke_VÆRDI = symbol("method", FUNKTION_VÆRDI.부분들());
        List<String> Linje = new ArrayList<>();
        if ((data.åbne_post & 0x100) != 0) {
            String Tilslut = maskine_tabel.get(FUNKTION_VÆRDI.Navn + FUNKTION_VÆRDI.서술);
            if (!FUNKTION_VÆRDI.ejer_VÆRDI.equals(mål.equals("kernel") ? "enhed_VÆRDI" : "bruger") || Tilslut == null) throw new Oversættelse_fejl("허용되지 않은 native FUNKTION_VÆRDI");
            return ".text\n" + mærke_VÆRDI + ":\njmp " + Tilslut;
        }
        byte[] brødtekst = data.attribut_VÆRDI.get("Code"); if (brødtekst == null) throw new Oversættelse_fejl("FUNKTION_VÆRDI 몸체가 없음");
        data_Læser Læser_VÆRDI = new data_Læser(brødtekst); Læser_VÆRDI.두바이트(); int lokal_TÆL = Læser_VÆRDI.두바이트();
        data_Læser kommando_data = new data_Læser(Læser_VÆRDI.Læse(Læser_VÆRDI.네바이트()));
        if (Læser_VÆRDI.두바이트() != 0) throw new Oversættelse_fejl("try/catch/finally 미지원");
        함수형식 format_VÆRDI = new 함수형식(FUNKTION_VÆRDI.서술); if (lokal_TÆL < format_VÆRDI.Argumenter.size()) throw new Oversættelse_fejl("매개변수보다 적은 lokal_Omfang variabel_VÆRDI");
        Collections.addAll(Linje,".text",".globl " + mærke_VÆRDI,".type " + mærke_VÆRDI + ", @function",mærke_VÆRDI + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_TÆL * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VÆRDI.Argumenter.size(); 순번++) Collections.addAll(Linje,"movl " + (8 + 4 * (format_VÆRDI.Argumenter.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Hold_data Hold_VÆRDI = 클래스들.get(FUNKTION_VÆRDI.ejer_VÆRDI); Set<Integer> 경계들 = new HashSet<>(), gren_Liste = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (kommando_data.Placering < kommando_data.data.length) {
            int Placering = kommando_data.Placering, Kommando = kommando_data.한바이트(); String positionsindeks = mærke_VÆRDI + "_b" + Placering;
            Linje.add(positionsindeks + ":"); 경계들.add(Placering);
            if (Kommando == 0) Linje.add("nop");
            else if (Kommando == 1) Linje.add("pushl $0");
            else if (Kommando >= 2 && Kommando <= 8) Linje.add("pushl $" + (Kommando - 3));
            else if (Kommando == 16 || Kommando == 17) Linje.add("pushl $" + (Kommando == 16 ? kommando_data.부호한바이트() : kommando_data.부호두바이트()));
            else if (Kommando == 18 || Kommando == 19) {
                int INDEKS = Kommando == 18 ? kommando_data.한바이트() : kommando_data.두바이트();
                Linje.add("pushl $" + X_86_konstant(Hold_VÆRDI,INDEKS));
            } else if (Kommando == 21 || Kommando == 25 || (Kommando >= 26 && Kommando <= 29) || (Kommando >= 42 && Kommando <= 45) || Kommando == 54 || Kommando == 58 || (Kommando >= 59 && Kommando <= 62) || (Kommando >= 75 && Kommando <= 78)) {
                boolean 읽음 = Kommando < 54; int INDEKS = Kommando == 21 || Kommando == 25 || Kommando == 54 || Kommando == 58 ? kommando_data.한바이트() : Kommando - (Kommando <= 29 ? 26 : Kommando <= 45 ? 42 : Kommando <= 62 ? 59 : 75);
                check_lokal(INDEKS,lokal_TÆL); Linje.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEKS + 1)) + "(%ebp)");
            } else if (Kommando == 46) Collections.addAll(Linje,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Kommando == 79) Collections.addAll(Linje,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Kommando == 87 || Kommando == 88) Linje.add("addl $" + (Kommando == 87 ? 4 : 8) + ", %esp");
            else if (Kommando >= 89 && Kommando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ordre_Liste = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Kommando - 89]; 순번++) Linje.add("popl " + 저장기들[순번]);
                for (int 순번 : ordre_Liste[Kommando - 89]) Linje.add("pushl " + 저장기들[순번]);
            } else if (Kommando == 96 || Kommando == 100 || Kommando == 104 || Kommando == 126 || Kommando == 128 || Kommando == 130) {
                String kirurgi_VÆRDI = Kommando == 96 ? "addl" : Kommando == 100 ? "subl" : Kommando == 104 ? "imull" : Kommando == 126 ? "andl" : Kommando == 128 ? "orl" : "xorl";
                Collections.addAll(Linje,"popl %ecx","popl %eax",kirurgi_VÆRDI + " %ecx, %eax","pushl %eax");
            } else if (Kommando == 108 || Kommando == 112) Collections.addAll(Linje,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + positionsindeks + "_divide","cmpl $0x80000000, %eax","jne " + positionsindeks + "_divide","xorl %edx, %edx","jmp " + positionsindeks + "_done",positionsindeks + "_divide:","cltd","idivl %ecx",positionsindeks + "_done:","pushl " + (Kommando == 108 ? "%eax" : "%edx"));
            else if (Kommando == 116) Linje.add("negl (%esp)");
            else if (Kommando == 120 || Kommando == 122 || Kommando == 124) Collections.addAll(Linje,"popl %ecx","popl %eax",(Kommando == 120 ? "sall" : Kommando == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Kommando == 132) {
                int INDEKS = kommando_data.한바이트(), gradvis_forøgelse_VÆRDI = kommando_data.부호한바이트(); check_lokal(INDEKS,lokal_TÆL); Linje.add("addl $" + gradvis_forøgelse_VÆRDI + ", -" + (4 * (INDEKS + 1)) + "(%ebp)");
            } else if (Kommando >= 145 && Kommando <= 147) Collections.addAll(Linje,"popl %eax",Kommando == 145 ? "movsbl %al, %eax" : Kommando == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Kommando >= 153 && Kommando <= 166) {
                if (Kommando <= 158) Collections.addAll(Linje,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Linje,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int destination_VÆRDI = Placering + kommando_data.부호두바이트(); gren_Liste.add(destination_VÆRDI); Linje.add(비교들[Kommando - (Kommando <= 158 ? 153 : 159)] + " " + mærke_VÆRDI + "_b" + destination_VÆRDI);
            } else if (Kommando == 167 || Kommando == 200) {
                int destination_VÆRDI = Placering + (Kommando == 167 ? kommando_data.부호두바이트() : kommando_data.네바이트()); gren_Liste.add(destination_VÆRDI); Linje.add("jmp " + mærke_VÆRDI + "_b" + destination_VÆRDI);
            } else if (Kommando == 170 || Kommando == 171) {
                while (kommando_data.Placering % 4 != 0) kommando_data.한바이트();
                int standardværdi = Placering + kommando_data.네바이트(); gren_Liste.add(standardværdi); Linje.add("popl %eax");
                int vare_TÆL, 아래 = 0;
                if (Kommando == 170) { 아래 = kommando_data.네바이트(); int 위 = kommando_data.네바이트(); long varighed_VÆRDI = (long)위 - 아래 + 1; if (varighed_VÆRDI < 1 || varighed_VÆRDI > (kommando_data.data.length - kommando_data.Placering) / 4) throw new Oversættelse_fejl("switch klippe fejl"); vare_TÆL = (int)varighed_VÆRDI; }
                else { vare_TÆL = kommando_data.네바이트(); if (vare_TÆL < 0 || vare_TÆL > (kommando_data.data.length - kommando_data.Placering) / 8) throw new Oversættelse_fejl("switch Størrelse fejl"); }
                for (int 순번 = 0; 순번 < vare_TÆL; 순번++) {
                    int VÆRDI = Kommando == 170 ? 아래 + 순번 : kommando_data.네바이트(), destination_VÆRDI = Placering + kommando_data.네바이트(); gren_Liste.add(destination_VÆRDI);
                    Collections.addAll(Linje,"cmpl $" + VÆRDI + ", %eax","je " + mærke_VÆRDI + "_b" + destination_VÆRDI);
                }
                Linje.add("jmp " + mærke_VÆRDI + "_b" + standardværdi);
            } else if (Kommando == 172 || Kommando == 176 || Kommando == 177) {
                if (Kommando != 177) Linje.add("popl %eax"); Collections.addAll(Linje,"leave","ret");
            } else if (Kommando == 178 || Kommando == 179) {
                metode_referere referere = Hold_VÆRDI.referere(kommando_data.두바이트()); if (!필드들.containsKey(referere)) throw new Oversættelse_fejl("알 tal 없는 feltværdi");
                Collections.addAll(Linje,"call " + symbol("init",referere.ejer_VÆRDI),(Kommando == 178 ? "pushl " : "popl ") + symbol("field",referere.부분들()));
            } else if (Kommando == 184) {
                metode_referere referere = Hold_VÆRDI.referere(kommando_data.두바이트()); if (!함수들.containsKey(referere)) throw new Oversættelse_fejl("알 tal 없는 FUNKTION_VÆRDI");
                함수형식 호출형식 = new 함수형식(referere.서술); Collections.addAll(Linje,"call " + symbol("init",referere.ejer_VÆRDI),"call " + symbol("method",referere.부분들()));
                if (!호출형식.Argumenter.isEmpty()) Linje.add("addl $" + 호출형식.Argumenter.size() * 4 + ", %esp");
                if (!호출형식.returnere_KR.equals("V")) Linje.add("pushl %eax");
            } else if (Kommando == 182) {
                metode_referere referere = Hold_VÆRDI.referere(kommando_data.두바이트());
                if (referere.equals(new metode_referere("java/lang/String","length","()I"))) Collections.addAll(Linje,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (referere.equals(new metode_referere("java/lang/String","charAt","(I)C"))) Collections.addAll(Linje,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Oversættelse_fejl("가상 FUNKTION_VÆRDI 호출 미지원");
            } else if (Kommando == 188) {
                if (kommando_data.한바이트() != 10) throw new Oversættelse_fejl("new int[]만 støtte_VÆRDI"); Collections.addAll(Linje,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Kommando == 190) Collections.addAll(Linje,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Kommando == 196) {
                int udvidelse_VÆRDI = kommando_data.한바이트(), INDEKS = kommando_data.두바이트(); check_lokal(INDEKS,lokal_TÆL);
                if (udvidelse_VÆRDI == 21 || udvidelse_VÆRDI == 25 || udvidelse_VÆRDI == 54 || udvidelse_VÆRDI == 58) Linje.add((udvidelse_VÆRDI <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEKS + 1) + "(%ebp)");
                else if (udvidelse_VÆRDI == 132) Linje.add("addl $" + kommando_data.부호두바이트() + ", -" + 4 * (INDEKS + 1) + "(%ebp)");
                else throw new Oversættelse_fejl("wide Kommando 미지원");
            } else if (Kommando == 198 || Kommando == 199) {
                int destination_VÆRDI = Placering + kommando_data.부호두바이트(); gren_Liste.add(destination_VÆRDI); Collections.addAll(Linje,"popl %eax","testl %eax, %eax",(Kommando == 198 ? "je " : "jne ") + mærke_VÆRDI + "_b" + destination_VÆRDI);
            } else throw new Oversættelse_fejl("미지원 Kommando: " + Kommando);
        }
        if (!경계들.containsAll(gren_Liste)) throw new Oversættelse_fejl("Kommando 경계가 아닌 곳으로 gren");
        Linje.add(".size " + mærke_VÆRDI + ", .-" + mærke_VÆRDI); return String.join("\n",Linje);
    }
    String X_86_konstant(Hold_data data, int INDEKS) {
        if (data.상수종류[INDEKS] == 3) return data.konstant_data[INDEKS].toString();
        if (data.상수종류[INDEKS] == 8) return streng_symbol(data.문자((Integer)data.konstant_data[INDEKS]));
        throw new Oversættelse_fejl("정수와 streng_VÆRDI 상수만 støtte_VÆRDI");
    }
    String X_86_montage(String indgangspunkt, List<String> 내보냄, String mål) throws IOException {
        Map<String,String> maskine_tabel = new HashMap<>();
        for (String Linje : Files.readAllLines(ressource_sti.resolve("_86_maskine_Functions.tsv"))) { String[] danne_par_VÆRDI = Linje.split("\t"); if (danne_par_VÆRDI[0].equals(mål)) maskine_tabel.put(danne_par_VÆRDI[1] + danne_par_VÆRDI[2],danne_par_VÆRDI[3]); }
        int positionsindeks = indgangspunkt.lastIndexOf('.'); if (positionsindeks < 0) throw new Oversættelse_fejl("indgangspunkt Tildel_VÆRDI fejl");
        String ejer_VÆRDI = indgangspunkt.substring(0,positionsindeks).replace('.','/'), metode_post_navn = indgangspunkt.substring(positionsindeks + 1); metode_referere indgangspunkt_VÆRDI = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metode_referere referere = new metode_referere(ejer_VÆRDI,metode_post_navn,서술); if (함수들.containsKey(referere)) { if (indgangspunkt_VÆRDI != null) throw new Oversættelse_fejl("겹친 indgangspunkt"); indgangspunkt_VÆRDI = referere; } }
        if (indgangspunkt_VÆRDI == null || (함수들.get(indgangspunkt_VÆRDI).åbne_post & 0x100) != 0) throw new Oversættelse_fejl("indgangspunkt_VÆRDI FUNKTION_VÆRDI format_VÆRDI fejl");
        List<String> Linje = new ArrayList<>(); Linje.add(".code32");
        for (Hold_data data : 클래스들.values()) {
            String status_VÆRDI = symbol("state",data.Navn), starte = symbol("init",data.Navn);
            Collections.addAll(Linje,".bss",".balign 4",status_VÆRDI + ": .long 0",".text",starte + ":","cmpl $0, " + status_VÆRDI,"jne " + starte + "_done","movl $1, " + status_VÆRDI);
            metode_referere 초기화참조 = new metode_referere(data.Navn,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Linje.add("call " + symbol("method",초기화참조.부분들()));
            Collections.addAll(Linje,"movl $2, " + status_VÆRDI,starte + "_done:","ret");
            for (medlem_data feltværdi : data.feltværdi) {
                byte[] konstant_VÆRDI = feltværdi.attribut_VÆRDI.get("ConstantValue"); String VÆRDI = konstant_VÆRDI == null ? "0" : X_86_konstant(data,new data_Læser(konstant_VÆRDI).두바이트());
                Collections.addAll(Linje,".data",".balign 4",symbol("field",data.Navn,feltværdi.Navn,feltværdi.서술) + ": .long " + VÆRDI);
            }
            for (medlem_data FUNKTION_VÆRDI : data.FUNKTION_VÆRDI) if (!FUNKTION_VÆRDI.Navn.equals("<init>")) Linje.add(X_86_metode_brødtekst(new metode_referere(data.Navn,FUNKTION_VÆRDI.Navn,FUNKTION_VÆRDI.서술),FUNKTION_VÆRDI,maskine_tabel,mål));
        }
        Collections.addAll(Linje,".text",".globl java_entry","java_entry:","call " + symbol("init",indgangspunkt_VÆRDI.ejer_VÆRDI),"call " + symbol("method",indgangspunkt_VÆRDI.부분들()));
        if (indgangspunkt_VÆRDI.서술.equals("()V")) Linje.add("xorl %eax, %eax"); Linje.add("ret");
        for (String Tildel_VÆRDI : 내보냄) {
            int afgrænser_VÆRDI = Tildel_VÆRDI.indexOf('='); if (afgrænser_VÆRDI < 1) throw new Oversættelse_fejl("내보내기 Tildel_VÆRDI fejl");
            String ekstern_VÆRDI = Tildel_VÆRDI.substring(0,afgrænser_VÆRDI), FUNKTION_VÆRDI = Tildel_VÆRDI.substring(afgrænser_VÆRDI + 1); int Division_KR = FUNKTION_VÆRDI.lastIndexOf('.');
            if (Division_KR < 0 || !ekstern_VÆRDI.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Oversættelse_fejl("내보내기 symbol fejl");
            String Hold_VÆRDI = FUNKTION_VÆRDI.substring(0,Division_KR).replace('.','/'), Navn = FUNKTION_VÆRDI.substring(Division_KR + 1); metode_referere markering_VÆRDI = null;
            for (metode_referere referere : 함수들.keySet()) if (referere.ejer_VÆRDI.equals(Hold_VÆRDI) && referere.Navn.equals(Navn)) { if (markering_VÆRDI != null) throw new Oversættelse_fejl("겹친 내보내기 mål"); markering_VÆRDI = referere; }
            if (markering_VÆRDI == null) throw new Oversættelse_fejl("내보낼 함수가 없음");
            Collections.addAll(Linje,".text",".globl " + ekstern_VÆRDI,ekstern_VÆRDI + ":","call " + symbol("init",markering_VÆRDI.ejer_VÆRDI),"jmp " + symbol("method",markering_VÆRDI.부분들()));
        }
        Linje.add(".section .rodata");
        for (Map.Entry<String,String> post_VÆRDI_962f286b : 문자열들.entrySet()) {
            Collections.addAll(Linje,".balign 4",post_VÆRDI_962f286b.getValue() + ":",".long " + post_VÆRDI_962f286b.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char enhed_VÆRDI_7c611f50 : post_VÆRDI_962f286b.getKey().toCharArray()) 단위들.add(Integer.toString(enhed_VÆRDI_7c611f50)); if (!단위들.isEmpty()) Linje.add(".long " + String.join(",",단위들));
        }
        Linje.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Linje) + "\n";
    }
    static void Udfør_værktøj(List<String> Kommando) throws Exception {
        if (new ProcessBuilder(Kommando).inheritIO().start().waitFor() != 0) throw new Oversættelse_fejl("kompilere_kilde fejl: " + Kommando.get(0));
    }
    static String data_streng(String Tekst) { return "\"" + Tekst.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Oversættelse(List<Path> input_Liste, String mål, String indgangspunkt, List<String> 내보냄, Path Udgang, Path ressource_VÆRDI) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Hold_sti = 임시.resolve("classes"); Files.createDirectory(Hold_sti);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Hold_sti.toString(),"-sourcepath",Hold_sti.toString(),"-d",Hold_sti.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int kilde_TÆL = 0;
            for (Path input_VÆRDI : input_Liste) {
                if (Udgang.toAbsolutePath().normalize().equals(input_VÆRDI.toAbsolutePath().normalize())) throw new Oversættelse_fejl("Udgang 파일과 입력이 같음");
                if (input_VÆRDI.toString().endsWith(".java")) { 자바명령.add(input_VÆRDI.toString()); kilde_TÆL++; }
                else if (input_VÆRDI.toString().endsWith(".class")) 바이트코드.add(input_VÆRDI);
                else throw new Oversættelse_fejl(".java 또는 .class만 støtte_VÆRDI");
            }
            if (kilde_TÆL > 0) Udfør_værktøj(자바명령);
            try (java.util.stream.Stream<Path> sti_Liste = Files.walk(Hold_sti)) { sti_Liste.filter(Sti -> Sti.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 KONVERTER_VÆRDI = new 기계어미리번역(바이트코드,mål.equals("user") ? "user" : "kernel",262144,ressource_VÆRDI);
            String oversætte_VÆRDI = KONVERTER_VÆRDI.X_86_montage(indgangspunkt,내보냄,mål); Files.writeString(임시.resolve("program.s"),oversætte_VÆRDI,StandardCharsets.UTF_8);
            Path værktøj_placere = ressource_VÆRDI.getParent();
            Udfør_værktøj(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Udfør_værktøj(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),værktøj_placere.resolve("CLR_støtte.s").toString()));
            List<String> Tilslut = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (mål.equals("kernel")) Tilslut.add("-r");
            else {
                Udfør_værktøj(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),værktøj_placere.resolve(mål.equals("user") ? "START_bruger_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Tilslut,"-e","_start",임시.resolve("start.o").toString());
                if (mål.equals("user")) Collections.addAll(Tilslut,"-T",værktøj_placere.resolve("bruger_Link_Layout.ld").toString());
            }
            Collections.addAll(Tilslut,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Udfør_værktøj(Tilslut);
            Udgang = Udgang.toAbsolutePath(); Files.createDirectories(Udgang.getParent()); Path udgive_VÆRDI = Files.createTempFile(Udgang.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),udgive_VÆRDI,StandardCopyOption.REPLACE_EXISTING); Files.move(udgive_VÆRDI,Udgang,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(udgive_VÆRDI); }
            Files.setPosixFilePermissions(Udgang,java.nio.file.attribute.PosixFilePermissions.fromString(mål.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Udgang + ".s"),oversætte_VÆRDI,StandardCharsets.UTF_8);
            List<String> symbol_data = new ArrayList<>(), kilde_data = new ArrayList<>();
            for (metode_referere referere : KONVERTER_VÆRDI.함수들.keySet()) symbol_data.add(data_streng(symbol("method",referere.부분들())) + ":" + data_streng(referere.ejer_VÆRDI + "." + referere.Navn + referere.서술));
            for (Path input_VÆRDI : input_Liste) {
                byte[] hash_fil = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(input_VÆRDI)); StringBuilder Tekst = new StringBuilder(); for (byte VÆRDI : hash_fil) Tekst.append(String.format(Locale.ROOT,"%02x",VÆRDI & 255));
                kilde_data.add(data_streng(input_VÆRDI.toAbsolutePath().toString()) + ":" + data_streng(Tekst.toString()));
            }
            Files.writeString(Paths.get(Udgang + ".json"),"{\"target\":" + data_streng(mål) + ",\"entry\":" + data_streng(indgangspunkt) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbol_data) + "},\"sources\":{" + String.join(",",kilde_data) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> sti_Liste = Files.walk(임시)) { for (Path Sti : (Iterable<Path>)sti_Liste.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Sti); }
        }
    }
    public static void main(String[] Argumenter) {
        try {
            String indgangspunkt = null, mål = "kernel", X_86_mål = null; Path produktoutput_sti = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> sti_Liste = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumenter.length; 순번++) {
                String VÆRDI = Argumenter[순번];
                switch (VÆRDI) {
                    case "--target": X_86_mål = Argumenter[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Hold_VÆRDI.FUNKTION_VÆRDI -o Udgang [--target linux|kernel|user] [--profile kernel|user] [--export symbol=Hold_VÆRDI.FUNKTION_VÆRDI] 클래스파일 또는 Java원문"); return;
                    case "--entry": indgangspunkt = Argumenter[++순번]; break;
                    case "--profile": mål = Argumenter[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumenter[++순번]); break;
                    case "--export": 내보냄.add(Argumenter[++순번]); break;
                    case "-o": produktoutput_sti = Paths.get(Argumenter[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VÆRDI.startsWith("-")) throw new Oversættelse_fejl("알 tal 없는 옵션: " + VÆRDI); sti_Liste.add(Paths.get(VÆRDI));
                }
            }
            if (indgangspunkt == null || produktoutput_sti == null || sti_Liste.isEmpty()) throw new Oversættelse_fejl("--entry, -o, Hold_VÆRDI 파일이 필요합니다");
            Path ressource_VÆRDI = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_mål != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_mål)) throw new Oversættelse_fejl("알 tal 없는 Udfør_kommando mål");
                X_86_Oversættelse(sti_Liste,X_86_mål,indgangspunkt,내보냄,produktoutput_sti,ressource_VÆRDI); return;
            }
            String KILDE = new 기계어미리번역(sti_Liste, mål, 낱말수, ressource_VÆRDI).generere(indgangspunkt, 내보냄, 범용표기);
            produktoutput_sti = produktoutput_sti.toAbsolutePath(); Files.createDirectories(produktoutput_sti.getParent());
            Path 임시 = Files.createTempFile(produktoutput_sti.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, KILDE, StandardCharsets.UTF_8); Files.move(임시, produktoutput_sti, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception fejl) { System.err.println("kompilere_kilde fejl: " + fejl.getMessage()); System.exit(1); }
    }
}
