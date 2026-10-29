// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java time_VERDI 파일에서 독립 ARM64 커널용 C 원문을 만든다. vert JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Oversettelse_feil extends RuntimeException {
        Oversettelse_feil(String 설명) { super(설명); }
    }
    static final class data_Leser {
        final byte[] data;
        int Posisjon;
        data_Leser(byte[] inndata_data) { data = inndata_data; }
        byte[] Les(int lengde_VERDI) {
            if (lengde_VERDI < 0 || lengde_VERDI > data.length - Posisjon) throw new Oversettelse_feil("잘린 time_VERDI 또는 Kommando data");
            byte[] KR = Arrays.copyOfRange(data, Posisjon, Posisjon + lengde_VERDI); Posisjon += lengde_VERDI; return KR;
        }
        int 한바이트() { if (Posisjon >= data.length) throw new Oversettelse_feil("잘린 Kommando data"); return data[Posisjon++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class medlem_data {
        final int tilgang_oppføring;
        final String Navn, 서술;
        final Map<String, byte[]> attributtverdi;
        medlem_data(int tilgang_VERDI, String navn_VERDI, String 서술값, Map<String, byte[]> attributt_data) {
            tilgang_oppføring = tilgang_VERDI; Navn = navn_VERDI; 서술 = 서술값; attributtverdi = attributt_data;
        }
    }
    static final class metode_referere implements Comparable<metode_referere> {
        final String eier_VERDI, Navn, 서술;
        metode_referere(String 소유값, String navn_VERDI, String 서술값) { eier_VERDI = 소유값; Navn = navn_VERDI; 서술 = 서술값; }
        String[] 부분들() { return new String[]{eier_VERDI, Navn, 서술}; }
        public int compareTo(metode_referere node_VERDI_6a3b6fa7) {
            int Sammenligning_VERDI = eier_VERDI.compareTo(node_VERDI_6a3b6fa7.eier_VERDI);
            if (Sammenligning_VERDI == 0) Sammenligning_VERDI = Navn.compareTo(node_VERDI_6a3b6fa7.Navn);
            return Sammenligning_VERDI == 0 ? 서술.compareTo(node_VERDI_6a3b6fa7.서술) : Sammenligning_VERDI;
        }
        public boolean equals(Object node_VERDI_6a3b6fa7) { return node_VERDI_6a3b6fa7 instanceof metode_referere && compareTo((metode_referere) node_VERDI_6a3b6fa7) == 0; }
        public int hashCode() { return Objects.hash(eier_VERDI, Navn, 서술); }
    }
    static final class time_data {
        final int[] 상수종류;
        final Object[] konstant_data;
        final String Navn;
        final List<medlem_data> feltverdi, FUNKSJON_VERDI;
        time_data(Path Sti) throws IOException {
            data_Leser Leser_VERDI = new data_Leser(Files.readAllBytes(Sti));
            if (Leser_VERDI.네바이트() != 0xcafebabe) throw new Oversettelse_feil("Java time_VERDI 표식이 아님");
            Leser_VERDI.Les(4);
            int vare_ANTALL = Leser_VERDI.두바이트(); 상수종류 = new int[vare_ANTALL]; konstant_data = new Object[vare_ANTALL];
            for (int 순번 = 1; 순번 < vare_ANTALL; 순번++) {
                int 종류 = Leser_VERDI.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int lengde_VERDI = Leser_VERDI.두바이트();
                        byte[] tegn_bufre = Leser_VERDI.Les(lengde_VERDI), 길이붙인자료 = new byte[lengde_VERDI + 2];
                        길이붙인자료[0] = (byte)(lengde_VERDI >> 8); 길이붙인자료[1] = (byte)lengde_VERDI;
                        System.arraycopy(tegn_bufre, 0, 길이붙인자료, 2, lengde_VERDI);
                        konstant_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstant_data[순번] = Leser_VERDI.네바이트(); break;
                    case 4: Leser_VERDI.Les(4); break;
                    case 5: case 6: Leser_VERDI.Les(8); 순번++; break;
                    case 7: case 8: case 16: konstant_data[순번] = Leser_VERDI.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstant_data[순번] = new int[]{Leser_VERDI.두바이트(), Leser_VERDI.두바이트()}; break;
                    case 15: konstant_data[순번] = new int[]{Leser_VERDI.한바이트(), Leser_VERDI.두바이트()}; break;
                    default: throw new Oversettelse_feil("지원하지 않는 konstant_VERDI 종류: " + 종류);
                }
            }
            Leser_VERDI.두바이트(); Navn = klassenavn(Leser_VERDI.두바이트());
            if (!klassenavn(Leser_VERDI.두바이트()).equals("java/lang/Object") || Leser_VERDI.두바이트() != 0)
                throw new Oversettelse_feil(Navn + ": 상속 및 인터페이스 미지원");
            feltverdi = 멤버읽기(Leser_VERDI); FUNKSJON_VERDI = 멤버읽기(Leser_VERDI); 속성읽기(Leser_VERDI);
            if (Leser_VERDI.Posisjon != Leser_VERDI.data.length) throw new Oversettelse_feil("time_VERDI 뒤에 남은 data");
        }
        String 문자(int INDEKS) {
            if (INDEKS < 1 || INDEKS >= 상수종류.length || 상수종류[INDEKS] != 1) throw new Oversettelse_feil("문자 konstant_VERDI INDEKS feil");
            return (String) konstant_data[INDEKS];
        }
        String klassenavn(int INDEKS) {
            if (INDEKS < 1 || INDEKS >= 상수종류.length || 상수종류[INDEKS] != 7) throw new Oversettelse_feil("time_VERDI referere feil");
            return 문자((Integer)konstant_data[INDEKS]);
        }
        metode_referere referere(int INDEKS) {
            if (INDEKS < 1 || INDEKS >= 상수종류.length || 상수종류[INDEKS] < 9 || 상수종류[INDEKS] > 11) throw new Oversettelse_feil("멤버 referere feil");
            int[] pare_VERDI = (int[])konstant_data[INDEKS], navn_pare = (int[])konstant_data[pare_VERDI[1]];
            return new metode_referere(klassenavn(pare_VERDI[0]), 문자(navn_pare[0]), 문자(navn_pare[1]));
        }
        Map<String, byte[]> 속성읽기(data_Leser Leser_VERDI) {
            Map<String, byte[]> KR = new LinkedHashMap<>();
            int vare_ANTALL = Leser_VERDI.두바이트();
            for (int 순번 = 0; 순번 < vare_ANTALL; 순번++) {
                String attributt_navn = 문자(Leser_VERDI.두바이트()); byte[] VERDI = Leser_VERDI.Les(Leser_VERDI.네바이트());
                if (KR.put(attributt_navn, VERDI) != null) throw new Oversettelse_feil("겹친 attributtverdi: " + attributt_navn);
            }
            return KR;
        }
        List<medlem_data> 멤버읽기(data_Leser Leser_VERDI) {
            List<medlem_data> KR = new ArrayList<>(); int vare_ANTALL = Leser_VERDI.두바이트();
            for (int 순번 = 0; 순번 < vare_ANTALL; 순번++) {
                int tilgang_oppføring = Leser_VERDI.두바이트(); String metode_oppføring_navn = 문자(Leser_VERDI.두바이트()), 서술 = 문자(Leser_VERDI.두바이트());
                KR.add(new medlem_data(tilgang_oppføring, metode_oppføring_navn, 서술, 속성읽기(Leser_VERDI)));
            }
            return KR;
        }
    }
    static final class 함수형식 {
        final List<String> Argumenter = new ArrayList<>();
        final String return_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Oversettelse_feil("FUNKSJON_VERDI 서술 feil: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Oversettelse_feil("FUNKSJON_VERDI 서술 feil: " + 서술);
            Argumenter.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumenter.contains("V") || 반환들.size() != 1) throw new Oversettelse_feil("FUNKSJON_VERDI 서술 feil: " + 서술);
            return_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> KR = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Posisjon = 0; Posisjon < 서술.length();) {
            String merket_område_VERDI = null;
            for (String format_VERDI : 허용형식) if (서술.startsWith(format_VERDI, Posisjon)) { merket_område_VERDI = format_VERDI; break; }
            if (merket_område_VERDI == null) throw new Oversettelse_feil("지원하지 않는 datatype: " + 서술);
            KR.add(merket_område_VERDI); Posisjon += merket_område_VERDI.length();
        }
        return KR;
    }
    static String symbol(String 종류, String... 부분들) {
        try {
            byte[] hash_Fil = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Tekst = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Tekst.append(String.format(Locale.ROOT, "%02x", hash_Fil[순번] & 255));
            return Tekst.toString();
        } catch (Exception feil) { throw new Oversettelse_feil(feil.toString()); }
    }
    final Map<String, time_data> 클래스들 = new TreeMap<>();
    final Map<metode_referere, medlem_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), maskin_Functions_c3a8e64a = new LinkedHashMap<>();
    final String kjøring_mål, maskin_time;
    final int heap_ord_ANTALL;
    final Path ressurs_bane;
    기계어미리번역(List<Path> bane_Liste, String mål, int 낱말수, Path ressurs_VERDI) throws IOException {
        if ((!mål.equals("kernel") && !mål.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Oversettelse_feil("Utfør_kommando mål 또는 Minne_VERDI e_post_område Størrelse feil");
        kjøring_mål = mål; heap_ord_ANTALL = 낱말수; ressurs_bane = ressurs_VERDI;
        // 이 이름도 국가별 kilde_tre generere 시 해당 언어로 옮긴다.
        maskin_time = mål.equals("kernel") ? "Tavle" : "bruker";
        for (String Linje : Files.readAllLines(ressurs_VERDI.resolve("maskin_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Linje.split("\t", -1);
            if (부분들.length != 4) throw new Oversettelse_feil("maskin FUNKSJON_VERDI data feil");
            if (부분들[0].equals(mål)) maskin_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Sti : bane_Liste) {
            time_data data = new time_data(Sti);
            if (클래스들.put(data.Navn, data) != null) throw new Oversettelse_feil("중복 time_VERDI: " + data.Navn);
            for (medlem_data feltverdi : data.feltverdi) {
                if ((feltverdi.tilgang_oppføring & 8) == 0 || 형식읽기(feltverdi.서술).equals(Collections.singletonList("V"))) throw new Oversettelse_feil("statisk_VERDI 필드만 støtte_VERDI");
                if (필드들.put(new metode_referere(data.Navn, feltverdi.Navn, feltverdi.서술), feltverdi) != null) throw new Oversettelse_feil("중복 feltverdi");
            }
            for (medlem_data FUNKSJON_VERDI : data.FUNKSJON_VERDI) {
                if (FUNKSJON_VERDI.Navn.equals("<init>")) continue;
                if ((FUNKSJON_VERDI.tilgang_oppføring & 8) == 0 || (FUNKSJON_VERDI.tilgang_oppføring & (0x20 | 0x400)) != 0) throw new Oversettelse_feil("statisk_VERDI 비동기화 함수만 støtte_VERDI");
                new 함수형식(FUNKSJON_VERDI.서술);
                if (함수들.put(new metode_referere(data.Navn, FUNKSJON_VERDI.Navn, FUNKSJON_VERDI.서술), FUNKSJON_VERDI) != null) throw new Oversettelse_feil("중복 FUNKSJON_VERDI");
            }
        }
    }
    String streng_symbol(String Tekst) { return 문자열들.computeIfAbsent(Tekst, VERDI -> "j_text_" + 문자열들.size()); }
    String konstantuttrykk(time_data data, int INDEKS) {
        if (INDEKS < 1 || INDEKS >= data.상수종류.length) throw new Oversettelse_feil("konstant_VERDI INDEKS klippe feil");
        if (data.상수종류[INDEKS] == 3) return "(word)(uint32_t)(" + data.konstant_data[INDEKS] + ")";
        if (data.상수종류[INDEKS] == 8) return "(word)" + streng_symbol(data.문자((Integer)data.konstant_data[INDEKS]));
        throw new Oversettelse_feil("정수와 streng_VERDI 상수만 støtte_VERDI");
    }
    String 함수원형(metode_referere referere) {
        List<String> 인수들 = new ArrayList<>(); int vare_ANTALL = new 함수형식(referere.서술).Argumenter.size();
        for (int 순번 = 0; 순번 < vare_ANTALL; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symbol("method", referere.부분들()) + "(" + (vare_ANTALL == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void sjekk_lokal(int INDEKS, int lokal_variabel_ANTALL) { if (INDEKS < 0 || INDEKS >= lokal_variabel_ANTALL) throw new Oversettelse_feil("lokal_Omfang variabel_VERDI INDEKS klippe feil"); }
    void 분기넣기(List<String> Utgang, Set<Integer> gren_Liste, int Posisjon, int 이동량, String vilkår) {
        int mål_VERDI = Posisjon + 이동량; gren_Liste.add(mål_VERDI);
        Utgang.add((vilkår == null ? "" : "if (" + vilkår + ") ") + "goto b" + mål_VERDI + ";");
    }
    String metode_brødtekst(metode_referere FUNKSJON_VERDI, medlem_data data) {
        byte[] brødtekst_data = data.attributtverdi.get("Code"); if (brødtekst_data == null) throw new Oversettelse_feil("FUNKSJON_VERDI 몸체가 없음: " + FUNKSJON_VERDI.Navn);
        data_Leser Leser_VERDI = new data_Leser(brødtekst_data); int 쌓임깊이 = Leser_VERDI.두바이트(), lokal_variabel_ANTALL = Leser_VERDI.두바이트();
        data_Leser kommando_data = new data_Leser(Leser_VERDI.Les(Leser_VERDI.네바이트()));
        if (Leser_VERDI.두바이트() != 0) throw new Oversettelse_feil("try/catch/finally 미지원");
        함수형식 format_VERDI = new 함수형식(FUNKSJON_VERDI.서술); if (lokal_variabel_ANTALL < format_VERDI.Argumenter.size()) throw new Oversettelse_feil("매개변수보다 적은 lokal_Omfang variabel_VERDI");
        time_data time_VERDI = 클래스들.get(FUNKSJON_VERDI.eier_VERDI);
        List<String> Utgang = new ArrayList<>(); Utgang.add(함수원형(FUNKSJON_VERDI) + " {");
        Utgang.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(lokal_variabel_ANTALL, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VERDI.Argumenter.size(); 순번++) Utgang.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), gren_Liste = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (kommando_data.Posisjon < kommando_data.data.length) {
            int Posisjon = kommando_data.Posisjon, Kommando = kommando_data.한바이트(); 경계들.add(Posisjon); Utgang.add("b" + Posisjon + ":;");
            if (Kommando == 0) continue;
            if (Kommando == 1) Utgang.add("PUSH(0);");
            else if (Kommando >= 2 && Kommando <= 8) Utgang.add("PUSH((uint32_t)(" + (Kommando - 3) + "));");
            else if (Kommando == 16 || Kommando == 17) Utgang.add("PUSH((uint32_t)(" + (Kommando == 16 ? kommando_data.부호한바이트() : kommando_data.부호두바이트()) + "));");
            else if (Kommando == 18 || Kommando == 19) Utgang.add("PUSH(" + konstantuttrykk(time_VERDI, Kommando == 18 ? kommando_data.한바이트() : kommando_data.두바이트()) + ");");
            else if (Kommando == 21 || Kommando == 25 || (Kommando >= 26 && Kommando <= 29) || (Kommando >= 42 && Kommando <= 45)) {
                int INDEKS = Kommando == 21 || Kommando == 25 ? kommando_data.한바이트() : Kommando - (Kommando <= 29 ? 26 : 42);
                sjekk_lokal(INDEKS, lokal_variabel_ANTALL); Utgang.add("PUSH(l[" + INDEKS + "]);");
            } else if (Kommando == 54 || Kommando == 58 || (Kommando >= 59 && Kommando <= 62) || (Kommando >= 75 && Kommando <= 78)) {
                int INDEKS = Kommando == 54 || Kommando == 58 ? kommando_data.한바이트() : Kommando - (Kommando <= 62 ? 59 : 75);
                sjekk_lokal(INDEKS, lokal_variabel_ANTALL); Utgang.add("l[" + INDEKS + "] = POP();");
            } else if (Kommando == 46) Utgang.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Kommando == 79) Utgang.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Kommando == 87 || Kommando == 88) Utgang.add(Kommando == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Kommando >= 89 && Kommando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ordre_Liste = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Kommando - 89]; 순번++) Utgang.add("abcd".charAt(순번) + " = POP();");
                for (char VERDI : ordre_Liste[Kommando - 89].toCharArray()) Utgang.add("PUSH(" + VERDI + ");");
            } else if (Kommando == 96 || Kommando == 100 || Kommando == 104 || Kommando == 126 || Kommando == 128 || Kommando == 130) {
                String operasjon_VERDI = Kommando == 96 ? "+" : Kommando == 100 ? "-" : Kommando == 104 ? "*" : Kommando == 126 ? "&" : Kommando == 128 ? "|" : "^";
                Utgang.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operasjon_VERDI + " (uint32_t)b);");
            } else if (Kommando == 108 || Kommando == 112) Utgang.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Kommando == 112 ? 1 : 0) + "));");
            else if (Kommando == 116) Utgang.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Kommando == 120 || Kommando == 122 || Kommando == 124) {
                Utgang.add("b = POP(); a = POP();"); Utgang.add("PUSH(" + (Kommando == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Kommando == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Kommando == 132) {
                int INDEKS = kommando_data.한바이트(), øke_trinnvis_beløp = kommando_data.부호한바이트(); sjekk_lokal(INDEKS, lokal_variabel_ANTALL);
                Utgang.add("l[" + INDEKS + "] = (uint32_t)l[" + INDEKS + "] + (uint32_t)(" + øke_trinnvis_beløp + ");");
            } else if (Kommando >= 145 && Kommando <= 147) Utgang.add("a = POP(); PUSH((uint32_t)(" + (Kommando == 145 ? "int8_t" : Kommando == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Kommando >= 153 && Kommando <= 158) {
                Utgang.add("a = POP();"); 분기넣기(Utgang, gren_Liste, Posisjon, kommando_data.부호두바이트(), "(int32_t)a " + 비교들[Kommando - 153] + " 0");
            } else if (Kommando >= 159 && Kommando <= 166) {
                Utgang.add("b = POP(); a = POP();"); 분기넣기(Utgang, gren_Liste, Posisjon, kommando_data.부호두바이트(), Kommando >= 165 ? "a " + 비교들[Kommando - 159] + " b" : "(int32_t)a " + 비교들[Kommando - 159] + " (int32_t)b");
            } else if (Kommando == 167 || Kommando == 200) 분기넣기(Utgang, gren_Liste, Posisjon, Kommando == 167 ? kommando_data.부호두바이트() : kommando_data.네바이트(), null);
            else if (Kommando == 170 || Kommando == 171) {
                while (kommando_data.Posisjon % 4 != 0) kommando_data.한바이트();
                int standardverdi = kommando_data.네바이트(); Utgang.add("a = POP();");
                if (Kommando == 170) {
                    int 아래 = kommando_data.네바이트(), 위 = kommando_data.네바이트(); long vare_ANTALL = (long)위 - 아래 + 1;
                    if (vare_ANTALL < 1 || vare_ANTALL > (kommando_data.data.length - kommando_data.Posisjon) / 4) throw new Oversettelse_feil("switch klippe feil");
                    for (long VERDI = 아래; VERDI <= 위; VERDI++) 분기넣기(Utgang, gren_Liste, Posisjon, kommando_data.네바이트(), "(int32_t)a == (" + VERDI + ")");
                } else {
                    int vare_ANTALL = kommando_data.네바이트(), frontkamera_data = 0;
                    if (vare_ANTALL < 0 || vare_ANTALL > (kommando_data.data.length - kommando_data.Posisjon) / 8) throw new Oversettelse_feil("switch Størrelse feil");
                    for (int 순번 = 0; 순번 < vare_ANTALL; 순번++) {
                        int VERDI = kommando_data.네바이트(); if (순번 > 0 && VERDI <= frontkamera_data) throw new Oversettelse_feil("switch ordre_VERDI feil"); frontkamera_data = VERDI;
                        분기넣기(Utgang, gren_Liste, Posisjon, kommando_data.네바이트(), "(int32_t)a == (" + VERDI + ")");
                    }
                }
                분기넣기(Utgang, gren_Liste, Posisjon, standardverdi, null);
            } else if (Kommando == 172 || Kommando == 176 || Kommando == 177) Utgang.add("return " + (Kommando == 177 ? "0" : "POP()") + ";");
            else if (Kommando == 178 || Kommando == 179) {
                metode_referere referere = time_VERDI.referere(kommando_data.두바이트()); if (!필드들.containsKey(referere)) throw new Oversettelse_feil("알 nummer 없는 feltverdi");
                Utgang.add(symbol("init", referere.eier_VERDI) + "();"); String feltverdi = symbol("field", referere.부분들());
                Utgang.add(Kommando == 178 ? "PUSH(" + feltverdi + ");" : feltverdi + " = POP();");
            } else if (Kommando == 184) {
                metode_referere referere = time_VERDI.referere(kommando_data.두바이트()); if (!함수들.containsKey(referere)) throw new Oversettelse_feil("알 nummer 없는 FUNKSJON_VERDI");
                함수형식 호출형식 = new 함수형식(referere.서술); int vare_ANTALL = 호출형식.Argumenter.size();
                Utgang.add(symbol("init", referere.eier_VERDI) + "();"); Utgang.add("if(sp < " + vare_ANTALL + ") kernel_panic(\"call stack underflow\"); sp -= " + vare_ANTALL + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < vare_ANTALL; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Utgang.add("a = " + symbol("method", referere.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.return_KR.equals("V")) Utgang.add("PUSH(a);");
            } else if (Kommando == 182) {
                metode_referere referere = time_VERDI.referere(kommando_data.두바이트());
                if (referere.equals(new metode_referere("java/lang/String", "length", "()I"))) Utgang.add("a = POP(); PUSH(length(a));");
                else if (referere.equals(new metode_referere("java/lang/String", "charAt", "(I)C"))) Utgang.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Oversettelse_feil("가상 FUNKSJON_VERDI 호출 미지원");
            } else if (Kommando == 188) {
                if (kommando_data.한바이트() != 10) throw new Oversettelse_feil("new int[]만 støtte_VERDI"); Utgang.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Kommando == 190) Utgang.add("a = POP(); PUSH(length(a));");
            else if (Kommando == 196) {
                int filtype_VERDI = kommando_data.한바이트(), INDEKS = kommando_data.두바이트(); sjekk_lokal(INDEKS, lokal_variabel_ANTALL);
                if (filtype_VERDI == 21 || filtype_VERDI == 25) Utgang.add("PUSH(l[" + INDEKS + "]);");
                else if (filtype_VERDI == 54 || filtype_VERDI == 58) Utgang.add("l[" + INDEKS + "] = POP();");
                else if (filtype_VERDI == 132) Utgang.add("l[" + INDEKS + "] = (uint32_t)l[" + INDEKS + "] + (uint32_t)(" + kommando_data.부호두바이트() + ");");
                else throw new Oversettelse_feil("미지원 wide Kommando");
            } else if (Kommando == 198 || Kommando == 199) {
                Utgang.add("a = POP();"); 분기넣기(Utgang, gren_Liste, Posisjon, kommando_data.부호두바이트(), "a " + (Kommando == 198 ? "==" : "!=") + " 0");
            } else throw new Oversettelse_feil(FUNKSJON_VERDI.eier_VERDI + "." + FUNKSJON_VERDI.Navn + ", byte_VERDI " + Posisjon + ": 미지원 Kommando " + Kommando);
        }
        if (!경계들.containsAll(gren_Liste)) throw new Oversettelse_feil("Kommando 경계가 아닌 곳으로 gren");
        Utgang.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Utgang);
    }
    String eksportere_metode(String koble_symbol, String mål, boolean 진입점여부) {
        int posisjonsindeks = mål.lastIndexOf('.'); if (posisjonsindeks < 0 || !koble_symbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Oversettelse_feil("내보내기 overdra_VERDI feil");
        String eier_VERDI = mål.substring(0, posisjonsindeks).replace('.', '/'), Navn = mål.substring(posisjonsindeks + 1); metode_referere merket_område_VERDI = null;
        for (metode_referere referere : 함수들.keySet()) if (referere.eier_VERDI.equals(eier_VERDI) && referere.Navn.equals(Navn)) {
            if (merket_område_VERDI != null) throw new Oversettelse_feil("겹친 내보내기 mål"); merket_område_VERDI = referere;
        }
        if (merket_område_VERDI == null || (함수들.get(merket_område_VERDI).tilgang_oppføring & 0x100) != 0) throw new Oversettelse_feil("내보낼 함수가 없음 또는 native FUNKSJON_VERDI");
        함수형식 format_VERDI = new 함수형식(merket_område_VERDI.서술);
        if ((진입점여부 && !format_VERDI.Argumenter.isEmpty()) || !Arrays.asList("V", "I").contains(format_VERDI.return_KR)) throw new Oversettelse_feil("inngangspunkt_VERDI 또는 C grense_VERDI format_VERDI feil");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VERDI.Argumenter.size(); 순번++) {
            if (!format_VERDI.Argumenter.get(순번).equals("I")) throw new Oversettelse_feil("C 경계는 int 인수만 støtte_VERDI");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VERDI.return_KR.equals("V") ? "void " : "int32_t ") + koble_symbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symbol("init", merket_område_VERDI.eier_VERDI) + "(); " + (format_VERDI.return_KR.equals("V") ? "" : "return (int32_t)") + symbol("method", merket_område_VERDI.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generere(String inngangspunkt, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metode_referere, medlem_data> oppføring_VERDI : 함수들.entrySet()) {
            metode_referere referere = oppføring_VERDI.getKey(); medlem_data data = oppføring_VERDI.getValue(); 선언들.add(함수원형(referere) + ";");
            if ((data.tilgang_oppføring & 0x100) != 0) {
                String Koble_til = maskin_Functions_c3a8e64a.get(referere.Navn + referere.서술);
                if (!referere.eier_VERDI.equals(maskin_time) || Koble_til == null) throw new Oversettelse_feil("허용되지 않은 native FUNKSJON_VERDI: " + referere.Navn);
                int vare_ANTALL = new 함수형식(referere.서술).Argumenter.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < vare_ANTALL; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Koble_til + "(" + (vare_ANTALL == 0 ? "void" : String.join(",", Collections.nCopies(vare_ANTALL, "word"))) + ");");
                몸체들.add(함수원형(referere) + " { return " + Koble_til + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metode_brødtekst(referere, data));
        }
        for (Map.Entry<metode_referere, medlem_data> oppføring_VERDI : 필드들.entrySet()) {
            metode_referere referere = oppføring_VERDI.getKey(); byte[] konstant_VERDI = oppføring_VERDI.getValue().attributtverdi.get("ConstantValue");
            String VERDI = konstant_VERDI == null ? "0" : konstantuttrykk(클래스들.get(referere.eier_VERDI), new data_Leser(konstant_VERDI).두바이트());
            필드선언들.add("static word " + symbol("field", referere.부분들()) + " = " + VERDI + ";");
        }
        for (String Navn : 클래스들.keySet()) {
            String starte = symbol("init", Navn), status_VERDI = symbol("state", Navn);
            선언들.add("static void " + starte + "(void);"); 필드선언들.add("static unsigned " + status_VERDI + ";");
            metode_referere referere = new metode_referere(Navn, "<clinit>", "()V");
            몸체들.add("static void " + starte + "(void) { if(" + status_VERDI + ") return; " + status_VERDI + " = 1; " + (함수들.containsKey(referere) ? symbol("method", referere.부분들()) + "(); " : "") + status_VERDI + " = 2; }");
        }
        몸체들.add(eksportere_metode("java_entry", inngangspunkt, true)); Set<String> 공개이름 = new HashSet<>();
        for (String overdra_VERDI : 내보내기목록) {
            int posisjonsindeks = overdra_VERDI.indexOf('='); if (posisjonsindeks < 1) throw new Oversettelse_feil("내보내기 overdra_VERDI feil");
            String Navn = overdra_VERDI.substring(0, posisjonsindeks); 공개이름.add(Navn); 몸체들.add(eksportere_metode(Navn, overdra_VERDI.substring(posisjonsindeks + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> oppføring_VERDI : 문자열들.entrySet()) {
            String Tekst = oppføring_VERDI.getKey(); StringBuilder MATRISE_VERDI = new StringBuilder("static const word " + oppføring_VERDI.getValue() + "[] = {" + Tekst.length());
            for (int 순번 = 0; 순번 < Tekst.length(); 순번++) MATRISE_VERDI.append(", ").append((int)Tekst.charAt(순번));
            문자열선언들.add(MATRISE_VERDI.append("};").toString());
        }
        String støtte_VERDI = Files.readString(ressurs_bane.resolve("CLR_støtte.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(heap_ord_ANTALL));
        return 기계원문한국어화(støtte_VERDI + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String KILDE, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> navn_tabell = new HashMap<>();
        for (String Linje : Files.readAllLines(ressurs_bane.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] pare_VERDI = Linje.split("\t"); navn_tabell.put(pare_VERDI[0], pare_VERDI[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(KILDE); StringBuffer KR = new StringBuffer();
        while (찾개.find()) {
            String Navn = 찾개.group(), 새이름 = Navn;
            if (!Navn.startsWith("//") && !Navn.startsWith("/*") && !Navn.startsWith("\"") && !Navn.startsWith("'") && !공개이름.contains(Navn)) {
                새이름 = navn_tabell.getOrDefault(Navn, Navn);
                if (Navn.matches("a[0-9]+")) 새이름 = "Argumenter" + Navn.substring(1);
                if (Navn.matches("b[0-9]+")) 새이름 = "gren" + Navn.substring(1);
                if (범용표기) {
                    StringBuilder notasjon_VERDI = new StringBuilder();
                    for (char tegn_VERDI : 새이름.toCharArray()) notasjon_VERDI.append(tegn_VERDI < 128 ? Character.toString(tegn_VERDI) : String.format(Locale.ROOT, "\\u%04x", (int)tegn_VERDI));
                    새이름 = notasjon_VERDI.toString();
                }
            }
            찾개.appendReplacement(KR, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(KR); return KR.toString();
    }
    String X_86_metode_brødtekst(metode_referere FUNKSJON_VERDI, medlem_data data, Map<String,String> maskin_tabell, String mål) {
        String tusj_VERDI = symbol("method", FUNKSJON_VERDI.부분들());
        List<String> Linje = new ArrayList<>();
        if ((data.tilgang_oppføring & 0x100) != 0) {
            String Koble_til = maskin_tabell.get(FUNKSJON_VERDI.Navn + FUNKSJON_VERDI.서술);
            if (!FUNKSJON_VERDI.eier_VERDI.equals(mål.equals("kernel") ? "enhet_VERDI" : "bruker") || Koble_til == null) throw new Oversettelse_feil("허용되지 않은 native FUNKSJON_VERDI");
            return ".text\n" + tusj_VERDI + ":\njmp " + Koble_til;
        }
        byte[] brødtekst = data.attributtverdi.get("Code"); if (brødtekst == null) throw new Oversettelse_feil("FUNKSJON_VERDI 몸체가 없음");
        data_Leser Leser_VERDI = new data_Leser(brødtekst); Leser_VERDI.두바이트(); int lokal_ANTALL = Leser_VERDI.두바이트();
        data_Leser kommando_data = new data_Leser(Leser_VERDI.Les(Leser_VERDI.네바이트()));
        if (Leser_VERDI.두바이트() != 0) throw new Oversettelse_feil("try/catch/finally 미지원");
        함수형식 format_VERDI = new 함수형식(FUNKSJON_VERDI.서술); if (lokal_ANTALL < format_VERDI.Argumenter.size()) throw new Oversettelse_feil("매개변수보다 적은 lokal_Omfang variabel_VERDI");
        Collections.addAll(Linje,".text",".globl " + tusj_VERDI,".type " + tusj_VERDI + ", @function",tusj_VERDI + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_ANTALL * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VERDI.Argumenter.size(); 순번++) Collections.addAll(Linje,"movl " + (8 + 4 * (format_VERDI.Argumenter.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        time_data time_VERDI = 클래스들.get(FUNKSJON_VERDI.eier_VERDI); Set<Integer> 경계들 = new HashSet<>(), gren_Liste = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (kommando_data.Posisjon < kommando_data.data.length) {
            int Posisjon = kommando_data.Posisjon, Kommando = kommando_data.한바이트(); String posisjonsindeks = tusj_VERDI + "_b" + Posisjon;
            Linje.add(posisjonsindeks + ":"); 경계들.add(Posisjon);
            if (Kommando == 0) Linje.add("nop");
            else if (Kommando == 1) Linje.add("pushl $0");
            else if (Kommando >= 2 && Kommando <= 8) Linje.add("pushl $" + (Kommando - 3));
            else if (Kommando == 16 || Kommando == 17) Linje.add("pushl $" + (Kommando == 16 ? kommando_data.부호한바이트() : kommando_data.부호두바이트()));
            else if (Kommando == 18 || Kommando == 19) {
                int INDEKS = Kommando == 18 ? kommando_data.한바이트() : kommando_data.두바이트();
                Linje.add("pushl $" + X_86_konstant(time_VERDI,INDEKS));
            } else if (Kommando == 21 || Kommando == 25 || (Kommando >= 26 && Kommando <= 29) || (Kommando >= 42 && Kommando <= 45) || Kommando == 54 || Kommando == 58 || (Kommando >= 59 && Kommando <= 62) || (Kommando >= 75 && Kommando <= 78)) {
                boolean 읽음 = Kommando < 54; int INDEKS = Kommando == 21 || Kommando == 25 || Kommando == 54 || Kommando == 58 ? kommando_data.한바이트() : Kommando - (Kommando <= 29 ? 26 : Kommando <= 45 ? 42 : Kommando <= 62 ? 59 : 75);
                sjekk_lokal(INDEKS,lokal_ANTALL); Linje.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEKS + 1)) + "(%ebp)");
            } else if (Kommando == 46) Collections.addAll(Linje,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Kommando == 79) Collections.addAll(Linje,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Kommando == 87 || Kommando == 88) Linje.add("addl $" + (Kommando == 87 ? 4 : 8) + ", %esp");
            else if (Kommando >= 89 && Kommando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ordre_Liste = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Kommando - 89]; 순번++) Linje.add("popl " + 저장기들[순번]);
                for (int 순번 : ordre_Liste[Kommando - 89]) Linje.add("pushl " + 저장기들[순번]);
            } else if (Kommando == 96 || Kommando == 100 || Kommando == 104 || Kommando == 126 || Kommando == 128 || Kommando == 130) {
                String operasjon_VERDI = Kommando == 96 ? "addl" : Kommando == 100 ? "subl" : Kommando == 104 ? "imull" : Kommando == 126 ? "andl" : Kommando == 128 ? "orl" : "xorl";
                Collections.addAll(Linje,"popl %ecx","popl %eax",operasjon_VERDI + " %ecx, %eax","pushl %eax");
            } else if (Kommando == 108 || Kommando == 112) Collections.addAll(Linje,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + posisjonsindeks + "_divide","cmpl $0x80000000, %eax","jne " + posisjonsindeks + "_divide","xorl %edx, %edx","jmp " + posisjonsindeks + "_done",posisjonsindeks + "_divide:","cltd","idivl %ecx",posisjonsindeks + "_done:","pushl " + (Kommando == 108 ? "%eax" : "%edx"));
            else if (Kommando == 116) Linje.add("negl (%esp)");
            else if (Kommando == 120 || Kommando == 122 || Kommando == 124) Collections.addAll(Linje,"popl %ecx","popl %eax",(Kommando == 120 ? "sall" : Kommando == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Kommando == 132) {
                int INDEKS = kommando_data.한바이트(), øke_trinnvis_VERDI = kommando_data.부호한바이트(); sjekk_lokal(INDEKS,lokal_ANTALL); Linje.add("addl $" + øke_trinnvis_VERDI + ", -" + (4 * (INDEKS + 1)) + "(%ebp)");
            } else if (Kommando >= 145 && Kommando <= 147) Collections.addAll(Linje,"popl %eax",Kommando == 145 ? "movsbl %al, %eax" : Kommando == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Kommando >= 153 && Kommando <= 166) {
                if (Kommando <= 158) Collections.addAll(Linje,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Linje,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int mål_VERDI = Posisjon + kommando_data.부호두바이트(); gren_Liste.add(mål_VERDI); Linje.add(비교들[Kommando - (Kommando <= 158 ? 153 : 159)] + " " + tusj_VERDI + "_b" + mål_VERDI);
            } else if (Kommando == 167 || Kommando == 200) {
                int mål_VERDI = Posisjon + (Kommando == 167 ? kommando_data.부호두바이트() : kommando_data.네바이트()); gren_Liste.add(mål_VERDI); Linje.add("jmp " + tusj_VERDI + "_b" + mål_VERDI);
            } else if (Kommando == 170 || Kommando == 171) {
                while (kommando_data.Posisjon % 4 != 0) kommando_data.한바이트();
                int standardverdi = Posisjon + kommando_data.네바이트(); gren_Liste.add(standardverdi); Linje.add("popl %eax");
                int vare_ANTALL, 아래 = 0;
                if (Kommando == 170) { 아래 = kommando_data.네바이트(); int 위 = kommando_data.네바이트(); long lengde_VERDI = (long)위 - 아래 + 1; if (lengde_VERDI < 1 || lengde_VERDI > (kommando_data.data.length - kommando_data.Posisjon) / 4) throw new Oversettelse_feil("switch klippe feil"); vare_ANTALL = (int)lengde_VERDI; }
                else { vare_ANTALL = kommando_data.네바이트(); if (vare_ANTALL < 0 || vare_ANTALL > (kommando_data.data.length - kommando_data.Posisjon) / 8) throw new Oversettelse_feil("switch Størrelse feil"); }
                for (int 순번 = 0; 순번 < vare_ANTALL; 순번++) {
                    int VERDI = Kommando == 170 ? 아래 + 순번 : kommando_data.네바이트(), mål_VERDI = Posisjon + kommando_data.네바이트(); gren_Liste.add(mål_VERDI);
                    Collections.addAll(Linje,"cmpl $" + VERDI + ", %eax","je " + tusj_VERDI + "_b" + mål_VERDI);
                }
                Linje.add("jmp " + tusj_VERDI + "_b" + standardverdi);
            } else if (Kommando == 172 || Kommando == 176 || Kommando == 177) {
                if (Kommando != 177) Linje.add("popl %eax"); Collections.addAll(Linje,"leave","ret");
            } else if (Kommando == 178 || Kommando == 179) {
                metode_referere referere = time_VERDI.referere(kommando_data.두바이트()); if (!필드들.containsKey(referere)) throw new Oversettelse_feil("알 nummer 없는 feltverdi");
                Collections.addAll(Linje,"call " + symbol("init",referere.eier_VERDI),(Kommando == 178 ? "pushl " : "popl ") + symbol("field",referere.부분들()));
            } else if (Kommando == 184) {
                metode_referere referere = time_VERDI.referere(kommando_data.두바이트()); if (!함수들.containsKey(referere)) throw new Oversettelse_feil("알 nummer 없는 FUNKSJON_VERDI");
                함수형식 호출형식 = new 함수형식(referere.서술); Collections.addAll(Linje,"call " + symbol("init",referere.eier_VERDI),"call " + symbol("method",referere.부분들()));
                if (!호출형식.Argumenter.isEmpty()) Linje.add("addl $" + 호출형식.Argumenter.size() * 4 + ", %esp");
                if (!호출형식.return_KR.equals("V")) Linje.add("pushl %eax");
            } else if (Kommando == 182) {
                metode_referere referere = time_VERDI.referere(kommando_data.두바이트());
                if (referere.equals(new metode_referere("java/lang/String","length","()I"))) Collections.addAll(Linje,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (referere.equals(new metode_referere("java/lang/String","charAt","(I)C"))) Collections.addAll(Linje,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Oversettelse_feil("가상 FUNKSJON_VERDI 호출 미지원");
            } else if (Kommando == 188) {
                if (kommando_data.한바이트() != 10) throw new Oversettelse_feil("new int[]만 støtte_VERDI"); Collections.addAll(Linje,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Kommando == 190) Collections.addAll(Linje,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Kommando == 196) {
                int filtype_VERDI = kommando_data.한바이트(), INDEKS = kommando_data.두바이트(); sjekk_lokal(INDEKS,lokal_ANTALL);
                if (filtype_VERDI == 21 || filtype_VERDI == 25 || filtype_VERDI == 54 || filtype_VERDI == 58) Linje.add((filtype_VERDI <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEKS + 1) + "(%ebp)");
                else if (filtype_VERDI == 132) Linje.add("addl $" + kommando_data.부호두바이트() + ", -" + 4 * (INDEKS + 1) + "(%ebp)");
                else throw new Oversettelse_feil("wide Kommando 미지원");
            } else if (Kommando == 198 || Kommando == 199) {
                int mål_VERDI = Posisjon + kommando_data.부호두바이트(); gren_Liste.add(mål_VERDI); Collections.addAll(Linje,"popl %eax","testl %eax, %eax",(Kommando == 198 ? "je " : "jne ") + tusj_VERDI + "_b" + mål_VERDI);
            } else throw new Oversettelse_feil("미지원 Kommando: " + Kommando);
        }
        if (!경계들.containsAll(gren_Liste)) throw new Oversettelse_feil("Kommando 경계가 아닌 곳으로 gren");
        Linje.add(".size " + tusj_VERDI + ", .-" + tusj_VERDI); return String.join("\n",Linje);
    }
    String X_86_konstant(time_data data, int INDEKS) {
        if (data.상수종류[INDEKS] == 3) return data.konstant_data[INDEKS].toString();
        if (data.상수종류[INDEKS] == 8) return streng_symbol(data.문자((Integer)data.konstant_data[INDEKS]));
        throw new Oversettelse_feil("정수와 streng_VERDI 상수만 støtte_VERDI");
    }
    String X_86_samling(String inngangspunkt, List<String> 내보냄, String mål) throws IOException {
        Map<String,String> maskin_tabell = new HashMap<>();
        for (String Linje : Files.readAllLines(ressurs_bane.resolve("_86_maskin_Functions.tsv"))) { String[] pare_VERDI = Linje.split("\t"); if (pare_VERDI[0].equals(mål)) maskin_tabell.put(pare_VERDI[1] + pare_VERDI[2],pare_VERDI[3]); }
        int posisjonsindeks = inngangspunkt.lastIndexOf('.'); if (posisjonsindeks < 0) throw new Oversettelse_feil("inngangspunkt overdra_VERDI feil");
        String eier_VERDI = inngangspunkt.substring(0,posisjonsindeks).replace('.','/'), metode_oppføring_navn = inngangspunkt.substring(posisjonsindeks + 1); metode_referere inngangspunkt_VERDI = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metode_referere referere = new metode_referere(eier_VERDI,metode_oppføring_navn,서술); if (함수들.containsKey(referere)) { if (inngangspunkt_VERDI != null) throw new Oversettelse_feil("겹친 inngangspunkt"); inngangspunkt_VERDI = referere; } }
        if (inngangspunkt_VERDI == null || (함수들.get(inngangspunkt_VERDI).tilgang_oppføring & 0x100) != 0) throw new Oversettelse_feil("inngangspunkt_VERDI FUNKSJON_VERDI format_VERDI feil");
        List<String> Linje = new ArrayList<>(); Linje.add(".code32");
        for (time_data data : 클래스들.values()) {
            String status_VERDI = symbol("state",data.Navn), starte = symbol("init",data.Navn);
            Collections.addAll(Linje,".bss",".balign 4",status_VERDI + ": .long 0",".text",starte + ":","cmpl $0, " + status_VERDI,"jne " + starte + "_done","movl $1, " + status_VERDI);
            metode_referere 초기화참조 = new metode_referere(data.Navn,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Linje.add("call " + symbol("method",초기화참조.부분들()));
            Collections.addAll(Linje,"movl $2, " + status_VERDI,starte + "_done:","ret");
            for (medlem_data feltverdi : data.feltverdi) {
                byte[] konstant_VERDI = feltverdi.attributtverdi.get("ConstantValue"); String VERDI = konstant_VERDI == null ? "0" : X_86_konstant(data,new data_Leser(konstant_VERDI).두바이트());
                Collections.addAll(Linje,".data",".balign 4",symbol("field",data.Navn,feltverdi.Navn,feltverdi.서술) + ": .long " + VERDI);
            }
            for (medlem_data FUNKSJON_VERDI : data.FUNKSJON_VERDI) if (!FUNKSJON_VERDI.Navn.equals("<init>")) Linje.add(X_86_metode_brødtekst(new metode_referere(data.Navn,FUNKSJON_VERDI.Navn,FUNKSJON_VERDI.서술),FUNKSJON_VERDI,maskin_tabell,mål));
        }
        Collections.addAll(Linje,".text",".globl java_entry","java_entry:","call " + symbol("init",inngangspunkt_VERDI.eier_VERDI),"call " + symbol("method",inngangspunkt_VERDI.부분들()));
        if (inngangspunkt_VERDI.서술.equals("()V")) Linje.add("xorl %eax, %eax"); Linje.add("ret");
        for (String overdra_VERDI : 내보냄) {
            int skilletegn_VERDI = overdra_VERDI.indexOf('='); if (skilletegn_VERDI < 1) throw new Oversettelse_feil("내보내기 overdra_VERDI feil");
            String ekstern_VERDI = overdra_VERDI.substring(0,skilletegn_VERDI), FUNKSJON_VERDI = overdra_VERDI.substring(skilletegn_VERDI + 1); int Divisjon_KR = FUNKSJON_VERDI.lastIndexOf('.');
            if (Divisjon_KR < 0 || !ekstern_VERDI.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Oversettelse_feil("내보내기 symbol feil");
            String time_VERDI = FUNKSJON_VERDI.substring(0,Divisjon_KR).replace('.','/'), Navn = FUNKSJON_VERDI.substring(Divisjon_KR + 1); metode_referere merket_område_VERDI = null;
            for (metode_referere referere : 함수들.keySet()) if (referere.eier_VERDI.equals(time_VERDI) && referere.Navn.equals(Navn)) { if (merket_område_VERDI != null) throw new Oversettelse_feil("겹친 내보내기 mål"); merket_område_VERDI = referere; }
            if (merket_område_VERDI == null) throw new Oversettelse_feil("내보낼 함수가 없음");
            Collections.addAll(Linje,".text",".globl " + ekstern_VERDI,ekstern_VERDI + ":","call " + symbol("init",merket_område_VERDI.eier_VERDI),"jmp " + symbol("method",merket_område_VERDI.부분들()));
        }
        Linje.add(".section .rodata");
        for (Map.Entry<String,String> oppføring_VERDI : 문자열들.entrySet()) {
            Collections.addAll(Linje,".balign 4",oppføring_VERDI.getValue() + ":",".long " + oppføring_VERDI.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char enhet_VERDI_7c611f50 : oppføring_VERDI.getKey().toCharArray()) 단위들.add(Integer.toString(enhet_VERDI_7c611f50)); if (!단위들.isEmpty()) Linje.add(".long " + String.join(",",단위들));
        }
        Linje.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Linje) + "\n";
    }
    static void Utfør_verktøy(List<String> Kommando) throws Exception {
        if (new ProcessBuilder(Kommando).inheritIO().start().waitFor() != 0) throw new Oversettelse_feil("kompilere_kilde feil: " + Kommando.get(0));
    }
    static String data_streng(String Tekst) { return "\"" + Tekst.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Oversettelse(List<Path> inndata_Liste, String mål, String inngangspunkt, List<String> 내보냄, Path Utgang, Path ressurs_VERDI) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), time_bane = 임시.resolve("classes"); Files.createDirectory(time_bane);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",time_bane.toString(),"-sourcepath",time_bane.toString(),"-d",time_bane.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int kilde_ANTALL = 0;
            for (Path inndata_VERDI : inndata_Liste) {
                if (Utgang.toAbsolutePath().normalize().equals(inndata_VERDI.toAbsolutePath().normalize())) throw new Oversettelse_feil("Utgang 파일과 입력이 같음");
                if (inndata_VERDI.toString().endsWith(".java")) { 자바명령.add(inndata_VERDI.toString()); kilde_ANTALL++; }
                else if (inndata_VERDI.toString().endsWith(".class")) 바이트코드.add(inndata_VERDI);
                else throw new Oversettelse_feil(".java 또는 .class만 støtte_VERDI");
            }
            if (kilde_ANTALL > 0) Utfør_verktøy(자바명령);
            try (java.util.stream.Stream<Path> bane_Liste = Files.walk(time_bane)) { bane_Liste.filter(Sti -> Sti.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 KONVERTER_VERDI = new 기계어미리번역(바이트코드,mål.equals("user") ? "user" : "kernel",262144,ressurs_VERDI);
            String 조립 = KONVERTER_VERDI.X_86_samling(inngangspunkt,내보냄,mål); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path verktøy_plassere = ressurs_VERDI.getParent();
            Utfør_verktøy(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Utfør_verktøy(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),verktøy_plassere.resolve("CLR_støtte.s").toString()));
            List<String> Koble_til = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (mål.equals("kernel")) Koble_til.add("-r");
            else {
                Utfør_verktøy(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),verktøy_plassere.resolve(mål.equals("user") ? "START_bruker_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Koble_til,"-e","_start",임시.resolve("start.o").toString());
                if (mål.equals("user")) Collections.addAll(Koble_til,"-T",verktøy_plassere.resolve("bruker_koble_Oppsett.ld").toString());
            }
            Collections.addAll(Koble_til,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Utfør_verktøy(Koble_til);
            Utgang = Utgang.toAbsolutePath(); Files.createDirectories(Utgang.getParent()); Path publisere_VERDI = Files.createTempFile(Utgang.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publisere_VERDI,StandardCopyOption.REPLACE_EXISTING); Files.move(publisere_VERDI,Utgang,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publisere_VERDI); }
            Files.setPosixFilePermissions(Utgang,java.nio.file.attribute.PosixFilePermissions.fromString(mål.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Utgang + ".s"),조립,StandardCharsets.UTF_8);
            List<String> symbol_data = new ArrayList<>(), kilde_data = new ArrayList<>();
            for (metode_referere referere : KONVERTER_VERDI.함수들.keySet()) symbol_data.add(data_streng(symbol("method",referere.부분들())) + ":" + data_streng(referere.eier_VERDI + "." + referere.Navn + referere.서술));
            for (Path inndata_VERDI : inndata_Liste) {
                byte[] hash_Fil = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(inndata_VERDI)); StringBuilder Tekst = new StringBuilder(); for (byte VERDI : hash_Fil) Tekst.append(String.format(Locale.ROOT,"%02x",VERDI & 255));
                kilde_data.add(data_streng(inndata_VERDI.toAbsolutePath().toString()) + ":" + data_streng(Tekst.toString()));
            }
            Files.writeString(Paths.get(Utgang + ".json"),"{\"target\":" + data_streng(mål) + ",\"entry\":" + data_streng(inngangspunkt) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbol_data) + "},\"sources\":{" + String.join(",",kilde_data) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> bane_Liste = Files.walk(임시)) { for (Path Sti : (Iterable<Path>)bane_Liste.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Sti); }
        }
    }
    public static void main(String[] Argumenter) {
        try {
            String inngangspunkt = null, mål = "kernel", X_86_mål = null; Path produksjon_bane = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> bane_Liste = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumenter.length; 순번++) {
                String VERDI = Argumenter[순번];
                switch (VERDI) {
                    case "--target": X_86_mål = Argumenter[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry time_VERDI.FUNKSJON_VERDI -o Utgang [--target linux|kernel|user] [--profile kernel|user] [--export symbol=time_VERDI.FUNKSJON_VERDI] 클래스파일 또는 Java원문"); return;
                    case "--entry": inngangspunkt = Argumenter[++순번]; break;
                    case "--profile": mål = Argumenter[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumenter[++순번]); break;
                    case "--export": 내보냄.add(Argumenter[++순번]); break;
                    case "-o": produksjon_bane = Paths.get(Argumenter[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VERDI.startsWith("-")) throw new Oversettelse_feil("알 nummer 없는 옵션: " + VERDI); bane_Liste.add(Paths.get(VERDI));
                }
            }
            if (inngangspunkt == null || produksjon_bane == null || bane_Liste.isEmpty()) throw new Oversettelse_feil("--entry, -o, time_VERDI 파일이 필요합니다");
            Path ressurs_VERDI = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_mål != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_mål)) throw new Oversettelse_feil("알 nummer 없는 Utfør_kommando mål");
                X_86_Oversettelse(bane_Liste,X_86_mål,inngangspunkt,내보냄,produksjon_bane,ressurs_VERDI); return;
            }
            String KILDE = new 기계어미리번역(bane_Liste, mål, 낱말수, ressurs_VERDI).generere(inngangspunkt, 내보냄, 범용표기);
            produksjon_bane = produksjon_bane.toAbsolutePath(); Files.createDirectories(produksjon_bane.getParent());
            Path 임시 = Files.createTempFile(produksjon_bane.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, KILDE, StandardCharsets.UTF_8); Files.move(임시, produksjon_bane, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception feil) { System.err.println("kompilere_kilde feil: " + feil.getMessage()); System.exit(1); }
    }
}
