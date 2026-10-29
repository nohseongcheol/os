// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Kurs_värde 파일에서 독립 ARM64 커널용 C 원문을 만든다. värd JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Översättning_fel extends RuntimeException {
        Översättning_fel(String 설명) { super(설명); }
    }
    static final class data_Läsare {
        final byte[] data;
        int position;
        data_Läsare(byte[] indata_data) { data = indata_data; }
        byte[] Läs(int längd_värde) {
            if (längd_värde < 0 || längd_värde > data.length - position) throw new Översättning_fel("잘린 Kurs_värde 또는 kommando data");
            byte[] RESULTAT = Arrays.copyOfRange(data, position, position + längd_värde); position += längd_värde; return RESULTAT;
        }
        int läsa_byte() { if (position >= data.length) throw new Översättning_fel("잘린 kommando data"); return data[position++] & 255; }
        int 두바이트() { return (läsa_byte() << 8) | läsa_byte(); }
        int läsa_HELTAL() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) läsa_byte(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class medlem_data {
        final int ansluta_post;
        final String Namn, 서술;
        final Map<String, byte[]> attribut_värde;
        medlem_data(int ansluta_värde, String namn_värde, String 서술값, Map<String, byte[]> attribut_data) {
            ansluta_post = ansluta_värde; Namn = namn_värde; 서술 = 서술값; attribut_värde = attribut_data;
        }
    }
    static final class metod_referens implements Comparable<metod_referens> {
        final String ägare_värde, Namn, 서술;
        metod_referens(String 소유값, String namn_värde, String 서술값) { ägare_värde = 소유값; Namn = namn_värde; 서술 = 서술값; }
        String[] 부분들() { return new String[]{ägare_värde, Namn, 서술}; }
        public int compareTo(metod_referens peer_värde) {
            int Jämförelse_värde = ägare_värde.compareTo(peer_värde.ägare_värde);
            if (Jämförelse_värde == 0) Jämförelse_värde = Namn.compareTo(peer_värde.Namn);
            return Jämförelse_värde == 0 ? 서술.compareTo(peer_värde.서술) : Jämförelse_värde;
        }
        public boolean equals(Object peer_värde) { return peer_värde instanceof metod_referens && compareTo((metod_referens) peer_värde) == 0; }
        public int hashCode() { return Objects.hash(ägare_värde, Namn, 서술); }
    }
    static final class Kurs_data {
        final int[] konstant_variant;
        final Object[] konstant_data;
        final String Namn;
        final List<medlem_data> fältvärde, FUNKTION_värde;
        Kurs_data(Path sökväg_2) throws IOException {
            data_Läsare Läsare_värde = new data_Läsare(Files.readAllBytes(sökväg_2));
            if (Läsare_värde.läsa_HELTAL() != 0xcafebabe) throw new Översättning_fel("Java Kurs_värde 표식이 아님");
            Läsare_värde.Läs(4);
            int objekt_ANTAL = Läsare_värde.두바이트(); konstant_variant = new int[objekt_ANTAL]; konstant_data = new Object[objekt_ANTAL];
            for (int 순번 = 1; 순번 < objekt_ANTAL; 순번++) {
                int variant_värde = Läsare_värde.läsa_byte(); konstant_variant[순번] = variant_värde;
                switch (variant_värde) {
                    case 1:
                        int längd_värde = Läsare_värde.두바이트();
                        byte[] tecken_buffra = Läsare_värde.Läs(längd_värde), 길이붙인자료 = new byte[längd_värde + 2];
                        길이붙인자료[0] = (byte)(längd_värde >> 8); 길이붙인자료[1] = (byte)längd_värde;
                        System.arraycopy(tecken_buffra, 0, 길이붙인자료, 2, längd_värde);
                        konstant_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstant_data[순번] = Läsare_värde.läsa_HELTAL(); break;
                    case 4: Läsare_värde.Läs(4); break;
                    case 5: case 6: Läsare_värde.Läs(8); 순번++; break;
                    case 7: case 8: case 16: konstant_data[순번] = Läsare_värde.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstant_data[순번] = new int[]{Läsare_värde.두바이트(), Läsare_värde.두바이트()}; break;
                    case 15: konstant_data[순번] = new int[]{Läsare_värde.läsa_byte(), Läsare_värde.두바이트()}; break;
                    default: throw new Översättning_fel("지원하지 않는 konstant_värde variant_värde: " + variant_värde);
                }
            }
            Läsare_värde.두바이트(); Namn = klassnamn(Läsare_värde.두바이트());
            if (!klassnamn(Läsare_värde.두바이트()).equals("java/lang/Object") || Läsare_värde.두바이트() != 0)
                throw new Översättning_fel(Namn + ": 상속 및 인터페이스 미지원");
            fältvärde = 멤버읽기(Läsare_värde); FUNKTION_värde = 멤버읽기(Läsare_värde); läsa_personlig_information(Läsare_värde);
            if (Läsare_värde.position != Läsare_värde.data.length) throw new Översättning_fel("Kurs_värde 뒤에 남은 data");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= konstant_variant.length || konstant_variant[INDEX] != 1) throw new Översättning_fel("문자 konstant_värde INDEX fel");
            return (String) konstant_data[INDEX];
        }
        String klassnamn(int INDEX) {
            if (INDEX < 1 || INDEX >= konstant_variant.length || konstant_variant[INDEX] != 7) throw new Översättning_fel("Kurs_värde referens fel");
            return 문자((Integer)konstant_data[INDEX]);
        }
        metod_referens referens(int INDEX) {
            if (INDEX < 1 || INDEX >= konstant_variant.length || konstant_variant[INDEX] < 9 || konstant_variant[INDEX] > 11) throw new Översättning_fel("멤버 referens fel");
            int[] länka_värde = (int[])konstant_data[INDEX], namn_länka = (int[])konstant_data[länka_värde[1]];
            return new metod_referens(klassnamn(länka_värde[0]), 문자(namn_länka[0]), 문자(namn_länka[1]));
        }
        Map<String, byte[]> läsa_personlig_information(data_Läsare Läsare_värde) {
            Map<String, byte[]> RESULTAT = new LinkedHashMap<>();
            int objekt_ANTAL = Läsare_värde.두바이트();
            for (int 순번 = 0; 순번 < objekt_ANTAL; 순번++) {
                String attribut_namn = 문자(Läsare_värde.두바이트()); byte[] värde = Läsare_värde.Läs(Läsare_värde.läsa_HELTAL());
                if (RESULTAT.put(attribut_namn, värde) != null) throw new Översättning_fel("겹친 attribut_värde: " + attribut_namn);
            }
            return RESULTAT;
        }
        List<medlem_data> 멤버읽기(data_Läsare Läsare_värde) {
            List<medlem_data> RESULTAT = new ArrayList<>(); int objekt_ANTAL = Läsare_värde.두바이트();
            for (int 순번 = 0; 순번 < objekt_ANTAL; 순번++) {
                int ansluta_post = Läsare_värde.두바이트(); String metod_post_namn = 문자(Läsare_värde.두바이트()), 서술 = 문자(Läsare_värde.두바이트());
                RESULTAT.add(new medlem_data(ansluta_post, metod_post_namn, 서술, läsa_personlig_information(Läsare_värde)));
            }
            return RESULTAT;
        }
    }
    static final class 함수형식 {
        final List<String> argument = new ArrayList<>();
        final String Retur_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Översättning_fel("FUNKTION_värde 서술 fel: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Översättning_fel("FUNKTION_värde 서술 fel: " + 서술);
            argument.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (argument.contains("V") || 반환들.size() != 1) throw new Översättning_fel("FUNKTION_värde 서술 fel: " + 서술);
            Retur_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> RESULTAT = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int position = 0; position < 서술.length();) {
            String markering_värde = null;
            for (String format_värde : 허용형식) if (서술.startsWith(format_värde, position)) { markering_värde = format_värde; break; }
            if (markering_värde == null) throw new Översättning_fel("지원하지 않는 datatyp: " + 서술);
            RESULTAT.add(markering_värde); position += markering_värde.length();
        }
        return RESULTAT;
    }
    static String symbol(String variant_värde, String... 부분들) {
        try {
            byte[] hash_fil = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder text = new StringBuilder("j_" + variant_värde + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) text.append(String.format(Locale.ROOT, "%02x", hash_fil[순번] & 255));
            return text.toString();
        } catch (Exception fel) { throw new Översättning_fel(fel.toString()); }
    }
    final Map<String, Kurs_data> 클래스들 = new TreeMap<>();
    final Map<metod_referens, medlem_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), dator_Functions_c3a8e64a = new LinkedHashMap<>();
    final String körning_mål, dator_Kurs;
    final int heap_Ord_ANTAL;
    final Path resurs_väg;
    기계어미리번역(List<Path> väg_ange, String mål, int 낱말수, Path resurs_värde) throws IOException {
        if ((!mål.equals("kernel") && !mål.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Översättning_fel("köra_kommando mål 또는 Minne_värde ADRESS_område Storlek fel");
        körning_mål = mål; heap_Ord_ANTAL = 낱말수; resurs_väg = resurs_värde;
        // 이 이름도 국가별 källa_träd generera 시 해당 언어로 옮긴다.
        dator_Kurs = mål.equals("kernel") ? "Tavla" : "användarutrymme";
        for (String inmatningsrad : Files.readAllLines(resurs_värde.resolve("dator_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = inmatningsrad.split("\t", -1);
            if (부분들.length != 4) throw new Översättning_fel("dator FUNKTION_värde data fel");
            if (부분들[0].equals(mål)) dator_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path sökväg_2 : väg_ange) {
            Kurs_data data = new Kurs_data(sökväg_2);
            if (클래스들.put(data.Namn, data) != null) throw new Översättning_fel("중복 Kurs_värde: " + data.Namn);
            for (medlem_data fältvärde : data.fältvärde) {
                if ((fältvärde.ansluta_post & 8) == 0 || 형식읽기(fältvärde.서술).equals(Collections.singletonList("V"))) throw new Översättning_fel("statisk_värde 필드만 stöd_värde");
                if (필드들.put(new metod_referens(data.Namn, fältvärde.Namn, fältvärde.서술), fältvärde) != null) throw new Översättning_fel("중복 fältvärde");
            }
            for (medlem_data FUNKTION_värde : data.FUNKTION_värde) {
                if (FUNKTION_värde.Namn.equals("<init>")) continue;
                if ((FUNKTION_värde.ansluta_post & 8) == 0 || (FUNKTION_värde.ansluta_post & (0x20 | 0x400)) != 0) throw new Översättning_fel("statisk_värde 비동기화 함수만 stöd_värde");
                new 함수형식(FUNKTION_värde.서술);
                if (함수들.put(new metod_referens(data.Namn, FUNKTION_värde.Namn, FUNKTION_värde.서술), FUNKTION_värde) != null) throw new Översättning_fel("중복 FUNKTION_värde");
            }
        }
    }
    String sträng_symbol(String text) { return 문자열들.computeIfAbsent(text, värde -> "j_text_" + 문자열들.size()); }
    String konstant_uttryck(Kurs_data data, int INDEX) {
        if (INDEX < 1 || INDEX >= data.konstant_variant.length) throw new Översättning_fel("konstant_värde INDEX klipp fel");
        if (data.konstant_variant[INDEX] == 3) return "(word)(uint32_t)(" + data.konstant_data[INDEX] + ")";
        if (data.konstant_variant[INDEX] == 8) return "(word)" + sträng_symbol(data.문자((Integer)data.konstant_data[INDEX]));
        throw new Översättning_fel("정수와 sträng_värde 상수만 stöd_värde");
    }
    String 함수원형(metod_referens referens) {
        List<String> 인수들 = new ArrayList<>(); int objekt_ANTAL = new 함수형식(referens.서술).argument.size();
        for (int 순번 = 0; 순번 < objekt_ANTAL; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symbol("method", referens.부분들()) + "(" + (objekt_ANTAL == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void check_lokal(int INDEX, int lokal_variabel_ANTAL) { if (INDEX < 0 || INDEX >= lokal_variabel_ANTAL) throw new Översättning_fel("lokal_scope variabel_värde INDEX klipp fel"); }
    void 분기넣기(List<String> utmatningsposition, Set<Integer> gren_ange, int position, int 이동량, String villkor) {
        int mål_värde = position + 이동량; gren_ange.add(mål_värde);
        utmatningsposition.add((villkor == null ? "" : "if (" + villkor + ") ") + "goto b" + mål_värde + ";");
    }
    String metod_brödtext(metod_referens FUNKTION_värde, medlem_data data) {
        byte[] brödtext_data = data.attribut_värde.get("Code"); if (brödtext_data == null) throw new Översättning_fel("FUNKTION_värde 몸체가 없음: " + FUNKTION_värde.Namn);
        data_Läsare Läsare_värde = new data_Läsare(brödtext_data); int 쌓임깊이 = Läsare_värde.두바이트(), lokal_variabel_ANTAL = Läsare_värde.두바이트();
        data_Läsare kommando_data = new data_Läsare(Läsare_värde.Läs(Läsare_värde.läsa_HELTAL()));
        if (Läsare_värde.두바이트() != 0) throw new Översättning_fel("try/catch/finally 미지원");
        함수형식 format_värde = new 함수형식(FUNKTION_värde.서술); if (lokal_variabel_ANTAL < format_värde.argument.size()) throw new Översättning_fel("매개변수보다 적은 lokal_scope variabel_värde");
        Kurs_data Kurs_värde = 클래스들.get(FUNKTION_värde.ägare_värde);
        List<String> utmatningsposition = new ArrayList<>(); utmatningsposition.add(함수원형(FUNKTION_värde) + " {");
        utmatningsposition.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(lokal_variabel_ANTAL, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_värde.argument.size(); 순번++) utmatningsposition.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), gren_ange = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (kommando_data.position < kommando_data.data.length) {
            int position = kommando_data.position, kommando = kommando_data.läsa_byte(); 경계들.add(position); utmatningsposition.add("b" + position + ":;");
            if (kommando == 0) continue;
            if (kommando == 1) utmatningsposition.add("PUSH(0);");
            else if (kommando >= 2 && kommando <= 8) utmatningsposition.add("PUSH((uint32_t)(" + (kommando - 3) + "));");
            else if (kommando == 16 || kommando == 17) utmatningsposition.add("PUSH((uint32_t)(" + (kommando == 16 ? kommando_data.부호한바이트() : kommando_data.부호두바이트()) + "));");
            else if (kommando == 18 || kommando == 19) utmatningsposition.add("PUSH(" + konstant_uttryck(Kurs_värde, kommando == 18 ? kommando_data.läsa_byte() : kommando_data.두바이트()) + ");");
            else if (kommando == 21 || kommando == 25 || (kommando >= 26 && kommando <= 29) || (kommando >= 42 && kommando <= 45)) {
                int INDEX = kommando == 21 || kommando == 25 ? kommando_data.läsa_byte() : kommando - (kommando <= 29 ? 26 : 42);
                check_lokal(INDEX, lokal_variabel_ANTAL); utmatningsposition.add("PUSH(l[" + INDEX + "]);");
            } else if (kommando == 54 || kommando == 58 || (kommando >= 59 && kommando <= 62) || (kommando >= 75 && kommando <= 78)) {
                int INDEX = kommando == 54 || kommando == 58 ? kommando_data.läsa_byte() : kommando - (kommando <= 62 ? 59 : 75);
                check_lokal(INDEX, lokal_variabel_ANTAL); utmatningsposition.add("l[" + INDEX + "] = POP();");
            } else if (kommando == 46) utmatningsposition.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (kommando == 79) utmatningsposition.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (kommando == 87 || kommando == 88) utmatningsposition.add(kommando == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (kommando >= 89 && kommando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] order_ange = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[kommando - 89]; 순번++) utmatningsposition.add("abcd".charAt(순번) + " = POP();");
                for (char värde : order_ange[kommando - 89].toCharArray()) utmatningsposition.add("PUSH(" + värde + ");");
            } else if (kommando == 96 || kommando == 100 || kommando == 104 || kommando == 126 || kommando == 128 || kommando == 130) {
                String åtgärd_värde = kommando == 96 ? "+" : kommando == 100 ? "-" : kommando == 104 ? "*" : kommando == 126 ? "&" : kommando == 128 ? "|" : "^";
                utmatningsposition.add("b = POP(); a = POP(); PUSH((uint32_t)a " + åtgärd_värde + " (uint32_t)b);");
            } else if (kommando == 108 || kommando == 112) utmatningsposition.add("b = POP(); a = POP(); PUSH(divide(a,b," + (kommando == 112 ? 1 : 0) + "));");
            else if (kommando == 116) utmatningsposition.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (kommando == 120 || kommando == 122 || kommando == 124) {
                utmatningsposition.add("b = POP(); a = POP();"); utmatningsposition.add("PUSH(" + (kommando == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (kommando == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (kommando == 132) {
                int INDEX = kommando_data.läsa_byte(), inkrement_belopp = kommando_data.부호한바이트(); check_lokal(INDEX, lokal_variabel_ANTAL);
                utmatningsposition.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + inkrement_belopp + ");");
            } else if (kommando >= 145 && kommando <= 147) utmatningsposition.add("a = POP(); PUSH((uint32_t)(" + (kommando == 145 ? "int8_t" : kommando == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (kommando >= 153 && kommando <= 158) {
                utmatningsposition.add("a = POP();"); 분기넣기(utmatningsposition, gren_ange, position, kommando_data.부호두바이트(), "(int32_t)a " + 비교들[kommando - 153] + " 0");
            } else if (kommando >= 159 && kommando <= 166) {
                utmatningsposition.add("b = POP(); a = POP();"); 분기넣기(utmatningsposition, gren_ange, position, kommando_data.부호두바이트(), kommando >= 165 ? "a " + 비교들[kommando - 159] + " b" : "(int32_t)a " + 비교들[kommando - 159] + " (int32_t)b");
            } else if (kommando == 167 || kommando == 200) 분기넣기(utmatningsposition, gren_ange, position, kommando == 167 ? kommando_data.부호두바이트() : kommando_data.läsa_HELTAL(), null);
            else if (kommando == 170 || kommando == 171) {
                while (kommando_data.position % 4 != 0) kommando_data.läsa_byte();
                int standardvärde = kommando_data.läsa_HELTAL(); utmatningsposition.add("a = POP();");
                if (kommando == 170) {
                    int 아래 = kommando_data.läsa_HELTAL(), 위 = kommando_data.läsa_HELTAL(); long objekt_ANTAL = (long)위 - 아래 + 1;
                    if (objekt_ANTAL < 1 || objekt_ANTAL > (kommando_data.data.length - kommando_data.position) / 4) throw new Översättning_fel("switch klipp fel");
                    for (long värde = 아래; värde <= 위; värde++) 분기넣기(utmatningsposition, gren_ange, position, kommando_data.läsa_HELTAL(), "(int32_t)a == (" + värde + ")");
                } else {
                    int objekt_ANTAL = kommando_data.läsa_HELTAL(), framåtvänd_data = 0;
                    if (objekt_ANTAL < 0 || objekt_ANTAL > (kommando_data.data.length - kommando_data.position) / 8) throw new Översättning_fel("switch Storlek fel");
                    for (int 순번 = 0; 순번 < objekt_ANTAL; 순번++) {
                        int värde = kommando_data.läsa_HELTAL(); if (순번 > 0 && värde <= framåtvänd_data) throw new Översättning_fel("switch order_värde fel"); framåtvänd_data = värde;
                        분기넣기(utmatningsposition, gren_ange, position, kommando_data.läsa_HELTAL(), "(int32_t)a == (" + värde + ")");
                    }
                }
                분기넣기(utmatningsposition, gren_ange, position, standardvärde, null);
            } else if (kommando == 172 || kommando == 176 || kommando == 177) utmatningsposition.add("return " + (kommando == 177 ? "0" : "POP()") + ";");
            else if (kommando == 178 || kommando == 179) {
                metod_referens referens = Kurs_värde.referens(kommando_data.두바이트()); if (!필드들.containsKey(referens)) throw new Översättning_fel("알 nummer 없는 fältvärde");
                utmatningsposition.add(symbol("init", referens.ägare_värde) + "();"); String fältvärde = symbol("field", referens.부분들());
                utmatningsposition.add(kommando == 178 ? "PUSH(" + fältvärde + ");" : fältvärde + " = POP();");
            } else if (kommando == 184) {
                metod_referens referens = Kurs_värde.referens(kommando_data.두바이트()); if (!함수들.containsKey(referens)) throw new Översättning_fel("알 nummer 없는 FUNKTION_värde");
                함수형식 호출형식 = new 함수형식(referens.서술); int objekt_ANTAL = 호출형식.argument.size();
                utmatningsposition.add(symbol("init", referens.ägare_värde) + "();"); utmatningsposition.add("if(sp < " + objekt_ANTAL + ") kernel_panic(\"call stack underflow\"); sp -= " + objekt_ANTAL + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < objekt_ANTAL; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                utmatningsposition.add("a = " + symbol("method", referens.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.Retur_KR.equals("V")) utmatningsposition.add("PUSH(a);");
            } else if (kommando == 182) {
                metod_referens referens = Kurs_värde.referens(kommando_data.두바이트());
                if (referens.equals(new metod_referens("java/lang/String", "length", "()I"))) utmatningsposition.add("a = POP(); PUSH(length(a));");
                else if (referens.equals(new metod_referens("java/lang/String", "charAt", "(I)C"))) utmatningsposition.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Översättning_fel("가상 FUNKTION_värde 호출 미지원");
            } else if (kommando == 188) {
                if (kommando_data.läsa_byte() != 10) throw new Översättning_fel("new int[]만 stöd_värde"); utmatningsposition.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (kommando == 190) utmatningsposition.add("a = POP(); PUSH(length(a));");
            else if (kommando == 196) {
                int tillägg_värde = kommando_data.läsa_byte(), INDEX = kommando_data.두바이트(); check_lokal(INDEX, lokal_variabel_ANTAL);
                if (tillägg_värde == 21 || tillägg_värde == 25) utmatningsposition.add("PUSH(l[" + INDEX + "]);");
                else if (tillägg_värde == 54 || tillägg_värde == 58) utmatningsposition.add("l[" + INDEX + "] = POP();");
                else if (tillägg_värde == 132) utmatningsposition.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + kommando_data.부호두바이트() + ");");
                else throw new Översättning_fel("미지원 wide kommando");
            } else if (kommando == 198 || kommando == 199) {
                utmatningsposition.add("a = POP();"); 분기넣기(utmatningsposition, gren_ange, position, kommando_data.부호두바이트(), "a " + (kommando == 198 ? "==" : "!=") + " 0");
            } else throw new Översättning_fel(FUNKTION_värde.ägare_värde + "." + FUNKTION_värde.Namn + ", byte_värde " + position + ": 미지원 kommando " + kommando);
        }
        if (!경계들.containsAll(gren_ange)) throw new Översättning_fel("kommando 경계가 아닌 곳으로 gren");
        utmatningsposition.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", utmatningsposition);
    }
    String exportera_metod(String Länk_symbol, String mål, boolean 진입점여부) {
        int positionsindex = mål.lastIndexOf('.'); if (positionsindex < 0 || !Länk_symbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Översättning_fel("내보내기 Tilldela_värde fel");
        String ägare_värde = mål.substring(0, positionsindex).replace('.', '/'), Namn = mål.substring(positionsindex + 1); metod_referens markering_värde = null;
        for (metod_referens referens : 함수들.keySet()) if (referens.ägare_värde.equals(ägare_värde) && referens.Namn.equals(Namn)) {
            if (markering_värde != null) throw new Översättning_fel("겹친 내보내기 mål"); markering_värde = referens;
        }
        if (markering_värde == null || (함수들.get(markering_värde).ansluta_post & 0x100) != 0) throw new Översättning_fel("내보낼 함수가 없음 또는 native FUNKTION_värde");
        함수형식 format_värde = new 함수형식(markering_värde.서술);
        if ((진입점여부 && !format_värde.argument.isEmpty()) || !Arrays.asList("V", "I").contains(format_värde.Retur_KR)) throw new Översättning_fel("startpunkt_värde 또는 C gräns_värde format_värde fel");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_värde.argument.size(); 순번++) {
            if (!format_värde.argument.get(순번).equals("I")) throw new Översättning_fel("C 경계는 int 인수만 stöd_värde");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_värde.Retur_KR.equals("V") ? "void " : "int32_t ") + Länk_symbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symbol("init", markering_värde.ägare_värde) + "(); " + (format_värde.Retur_KR.equals("V") ? "" : "return (int32_t)") + symbol("method", markering_värde.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generera(String startpunkt, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metod_referens, medlem_data> post_värde : 함수들.entrySet()) {
            metod_referens referens = post_värde.getKey(); medlem_data data = post_värde.getValue(); 선언들.add(함수원형(referens) + ";");
            if ((data.ansluta_post & 0x100) != 0) {
                String Anslut = dator_Functions_c3a8e64a.get(referens.Namn + referens.서술);
                if (!referens.ägare_värde.equals(dator_Kurs) || Anslut == null) throw new Översättning_fel("허용되지 않은 native FUNKTION_värde: " + referens.Namn);
                int objekt_ANTAL = new 함수형식(referens.서술).argument.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < objekt_ANTAL; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Anslut + "(" + (objekt_ANTAL == 0 ? "void" : String.join(",", Collections.nCopies(objekt_ANTAL, "word"))) + ");");
                몸체들.add(함수원형(referens) + " { return " + Anslut + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metod_brödtext(referens, data));
        }
        for (Map.Entry<metod_referens, medlem_data> post_värde : 필드들.entrySet()) {
            metod_referens referens = post_värde.getKey(); byte[] konstant_värde = post_värde.getValue().attribut_värde.get("ConstantValue");
            String värde = konstant_värde == null ? "0" : konstant_uttryck(클래스들.get(referens.ägare_värde), new data_Läsare(konstant_värde).두바이트());
            필드선언들.add("static word " + symbol("field", referens.부분들()) + " = " + värde + ";");
        }
        for (String Namn : 클래스들.keySet()) {
            String starta = symbol("init", Namn), status_värde = symbol("state", Namn);
            선언들.add("static void " + starta + "(void);"); 필드선언들.add("static unsigned " + status_värde + ";");
            metod_referens referens = new metod_referens(Namn, "<clinit>", "()V");
            몸체들.add("static void " + starta + "(void) { if(" + status_värde + ") return; " + status_värde + " = 1; " + (함수들.containsKey(referens) ? symbol("method", referens.부분들()) + "(); " : "") + status_värde + " = 2; }");
        }
        몸체들.add(exportera_metod("java_entry", startpunkt, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Tilldela_värde : 내보내기목록) {
            int positionsindex = Tilldela_värde.indexOf('='); if (positionsindex < 1) throw new Översättning_fel("내보내기 Tilldela_värde fel");
            String Namn = Tilldela_värde.substring(0, positionsindex); 공개이름.add(Namn); 몸체들.add(exportera_metod(Namn, Tilldela_värde.substring(positionsindex + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> post_värde : 문자열들.entrySet()) {
            String text = post_värde.getKey(); StringBuilder MATRIS_värde = new StringBuilder("static const word " + post_värde.getValue() + "[] = {" + text.length());
            for (int 순번 = 0; 순번 < text.length(); 순번++) MATRIS_värde.append(", ").append((int)text.charAt(순번));
            문자열선언들.add(MATRIS_värde.append("};").toString());
        }
        String stöd_värde = Files.readString(resurs_väg.resolve("CLR_stöd.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(heap_Ord_ANTAL));
        return 기계원문한국어화(stöd_värde + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String källfil, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> namn_tabell = new HashMap<>();
        for (String inmatningsrad : Files.readAllLines(resurs_väg.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] länka_värde = inmatningsrad.split("\t"); namn_tabell.put(länka_värde[0], länka_värde[1]);
        }
        Pattern segment_uttryck = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = segment_uttryck.matcher(källfil); StringBuffer RESULTAT = new StringBuffer();
        while (찾개.find()) {
            String Namn = 찾개.group(), 새이름 = Namn;
            if (!Namn.startsWith("//") && !Namn.startsWith("/*") && !Namn.startsWith("\"") && !Namn.startsWith("'") && !공개이름.contains(Namn)) {
                새이름 = namn_tabell.getOrDefault(Namn, Namn);
                if (Namn.matches("a[0-9]+")) 새이름 = "argument" + Namn.substring(1);
                if (Namn.matches("b[0-9]+")) 새이름 = "gren" + Namn.substring(1);
                if (범용표기) {
                    StringBuilder notation_värde = new StringBuilder();
                    for (char tecken_värde : 새이름.toCharArray()) notation_värde.append(tecken_värde < 128 ? Character.toString(tecken_värde) : String.format(Locale.ROOT, "\\u%04x", (int)tecken_värde));
                    새이름 = notation_värde.toString();
                }
            }
            찾개.appendReplacement(RESULTAT, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(RESULTAT); return RESULTAT.toString();
    }
    String X_86_metod_brödtext(metod_referens FUNKTION_värde, medlem_data data, Map<String,String> dator_tabell, String mål) {
        String markör_värde = symbol("method", FUNKTION_värde.부분들());
        List<String> inmatningsrad = new ArrayList<>();
        if ((data.ansluta_post & 0x100) != 0) {
            String Anslut = dator_tabell.get(FUNKTION_värde.Namn + FUNKTION_värde.서술);
            if (!FUNKTION_värde.ägare_värde.equals(mål.equals("kernel") ? "enhet_värde" : "användarutrymme") || Anslut == null) throw new Översättning_fel("허용되지 않은 native FUNKTION_värde");
            return ".text\n" + markör_värde + ":\njmp " + Anslut;
        }
        byte[] brödtext = data.attribut_värde.get("Code"); if (brödtext == null) throw new Översättning_fel("FUNKTION_värde 몸체가 없음");
        data_Läsare Läsare_värde = new data_Läsare(brödtext); Läsare_värde.두바이트(); int lokal_ANTAL = Läsare_värde.두바이트();
        data_Läsare kommando_data = new data_Läsare(Läsare_värde.Läs(Läsare_värde.läsa_HELTAL()));
        if (Läsare_värde.두바이트() != 0) throw new Översättning_fel("try/catch/finally 미지원");
        함수형식 format_värde = new 함수형식(FUNKTION_värde.서술); if (lokal_ANTAL < format_värde.argument.size()) throw new Översättning_fel("매개변수보다 적은 lokal_scope variabel_värde");
        Collections.addAll(inmatningsrad,".text",".globl " + markör_värde,".type " + markör_värde + ", @function",markör_värde + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_ANTAL * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_värde.argument.size(); 순번++) Collections.addAll(inmatningsrad,"movl " + (8 + 4 * (format_värde.argument.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Kurs_data Kurs_värde = 클래스들.get(FUNKTION_värde.ägare_värde); Set<Integer> 경계들 = new HashSet<>(), gren_ange = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (kommando_data.position < kommando_data.data.length) {
            int position = kommando_data.position, kommando = kommando_data.läsa_byte(); String positionsindex = markör_värde + "_b" + position;
            inmatningsrad.add(positionsindex + ":"); 경계들.add(position);
            if (kommando == 0) inmatningsrad.add("nop");
            else if (kommando == 1) inmatningsrad.add("pushl $0");
            else if (kommando >= 2 && kommando <= 8) inmatningsrad.add("pushl $" + (kommando - 3));
            else if (kommando == 16 || kommando == 17) inmatningsrad.add("pushl $" + (kommando == 16 ? kommando_data.부호한바이트() : kommando_data.부호두바이트()));
            else if (kommando == 18 || kommando == 19) {
                int INDEX = kommando == 18 ? kommando_data.läsa_byte() : kommando_data.두바이트();
                inmatningsrad.add("pushl $" + X_86_konstant(Kurs_värde,INDEX));
            } else if (kommando == 21 || kommando == 25 || (kommando >= 26 && kommando <= 29) || (kommando >= 42 && kommando <= 45) || kommando == 54 || kommando == 58 || (kommando >= 59 && kommando <= 62) || (kommando >= 75 && kommando <= 78)) {
                boolean läsa_KR = kommando < 54; int INDEX = kommando == 21 || kommando == 25 || kommando == 54 || kommando == 58 ? kommando_data.läsa_byte() : kommando - (kommando <= 29 ? 26 : kommando <= 45 ? 42 : kommando <= 62 ? 59 : 75);
                check_lokal(INDEX,lokal_ANTAL); inmatningsrad.add((läsa_KR ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (kommando == 46) Collections.addAll(inmatningsrad,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (kommando == 79) Collections.addAll(inmatningsrad,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (kommando == 87 || kommando == 88) inmatningsrad.add("addl $" + (kommando == 87 ? 4 : 8) + ", %esp");
            else if (kommando >= 89 && kommando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] order_ange = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[kommando - 89]; 순번++) inmatningsrad.add("popl " + 저장기들[순번]);
                for (int 순번 : order_ange[kommando - 89]) inmatningsrad.add("pushl " + 저장기들[순번]);
            } else if (kommando == 96 || kommando == 100 || kommando == 104 || kommando == 126 || kommando == 128 || kommando == 130) {
                String åtgärd_värde = kommando == 96 ? "addl" : kommando == 100 ? "subl" : kommando == 104 ? "imull" : kommando == 126 ? "andl" : kommando == 128 ? "orl" : "xorl";
                Collections.addAll(inmatningsrad,"popl %ecx","popl %eax",åtgärd_värde + " %ecx, %eax","pushl %eax");
            } else if (kommando == 108 || kommando == 112) Collections.addAll(inmatningsrad,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + positionsindex + "_divide","cmpl $0x80000000, %eax","jne " + positionsindex + "_divide","xorl %edx, %edx","jmp " + positionsindex + "_done",positionsindex + "_divide:","cltd","idivl %ecx",positionsindex + "_done:","pushl " + (kommando == 108 ? "%eax" : "%edx"));
            else if (kommando == 116) inmatningsrad.add("negl (%esp)");
            else if (kommando == 120 || kommando == 122 || kommando == 124) Collections.addAll(inmatningsrad,"popl %ecx","popl %eax",(kommando == 120 ? "sall" : kommando == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (kommando == 132) {
                int INDEX = kommando_data.läsa_byte(), inkrement_värde = kommando_data.부호한바이트(); check_lokal(INDEX,lokal_ANTAL); inmatningsrad.add("addl $" + inkrement_värde + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (kommando >= 145 && kommando <= 147) Collections.addAll(inmatningsrad,"popl %eax",kommando == 145 ? "movsbl %al, %eax" : kommando == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (kommando >= 153 && kommando <= 166) {
                if (kommando <= 158) Collections.addAll(inmatningsrad,"popl %eax","testl %eax, %eax");
                else Collections.addAll(inmatningsrad,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int mål_värde = position + kommando_data.부호두바이트(); gren_ange.add(mål_värde); inmatningsrad.add(비교들[kommando - (kommando <= 158 ? 153 : 159)] + " " + markör_värde + "_b" + mål_värde);
            } else if (kommando == 167 || kommando == 200) {
                int mål_värde = position + (kommando == 167 ? kommando_data.부호두바이트() : kommando_data.läsa_HELTAL()); gren_ange.add(mål_värde); inmatningsrad.add("jmp " + markör_värde + "_b" + mål_värde);
            } else if (kommando == 170 || kommando == 171) {
                while (kommando_data.position % 4 != 0) kommando_data.läsa_byte();
                int standardvärde = position + kommando_data.läsa_HELTAL(); gren_ange.add(standardvärde); inmatningsrad.add("popl %eax");
                int objekt_ANTAL, 아래 = 0;
                if (kommando == 170) { 아래 = kommando_data.läsa_HELTAL(); int 위 = kommando_data.läsa_HELTAL(); long längd_värde = (long)위 - 아래 + 1; if (längd_värde < 1 || längd_värde > (kommando_data.data.length - kommando_data.position) / 4) throw new Översättning_fel("switch klipp fel"); objekt_ANTAL = (int)längd_värde; }
                else { objekt_ANTAL = kommando_data.läsa_HELTAL(); if (objekt_ANTAL < 0 || objekt_ANTAL > (kommando_data.data.length - kommando_data.position) / 8) throw new Översättning_fel("switch Storlek fel"); }
                for (int 순번 = 0; 순번 < objekt_ANTAL; 순번++) {
                    int värde = kommando == 170 ? 아래 + 순번 : kommando_data.läsa_HELTAL(), mål_värde = position + kommando_data.läsa_HELTAL(); gren_ange.add(mål_värde);
                    Collections.addAll(inmatningsrad,"cmpl $" + värde + ", %eax","je " + markör_värde + "_b" + mål_värde);
                }
                inmatningsrad.add("jmp " + markör_värde + "_b" + standardvärde);
            } else if (kommando == 172 || kommando == 176 || kommando == 177) {
                if (kommando != 177) inmatningsrad.add("popl %eax"); Collections.addAll(inmatningsrad,"leave","ret");
            } else if (kommando == 178 || kommando == 179) {
                metod_referens referens = Kurs_värde.referens(kommando_data.두바이트()); if (!필드들.containsKey(referens)) throw new Översättning_fel("알 nummer 없는 fältvärde");
                Collections.addAll(inmatningsrad,"call " + symbol("init",referens.ägare_värde),(kommando == 178 ? "pushl " : "popl ") + symbol("field",referens.부분들()));
            } else if (kommando == 184) {
                metod_referens referens = Kurs_värde.referens(kommando_data.두바이트()); if (!함수들.containsKey(referens)) throw new Översättning_fel("알 nummer 없는 FUNKTION_värde");
                함수형식 호출형식 = new 함수형식(referens.서술); Collections.addAll(inmatningsrad,"call " + symbol("init",referens.ägare_värde),"call " + symbol("method",referens.부분들()));
                if (!호출형식.argument.isEmpty()) inmatningsrad.add("addl $" + 호출형식.argument.size() * 4 + ", %esp");
                if (!호출형식.Retur_KR.equals("V")) inmatningsrad.add("pushl %eax");
            } else if (kommando == 182) {
                metod_referens referens = Kurs_värde.referens(kommando_data.두바이트());
                if (referens.equals(new metod_referens("java/lang/String","length","()I"))) Collections.addAll(inmatningsrad,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (referens.equals(new metod_referens("java/lang/String","charAt","(I)C"))) Collections.addAll(inmatningsrad,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Översättning_fel("가상 FUNKTION_värde 호출 미지원");
            } else if (kommando == 188) {
                if (kommando_data.läsa_byte() != 10) throw new Översättning_fel("new int[]만 stöd_värde"); Collections.addAll(inmatningsrad,"popl %eax","call rt_new_array","pushl %eax");
            } else if (kommando == 190) Collections.addAll(inmatningsrad,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (kommando == 196) {
                int tillägg_värde = kommando_data.läsa_byte(), INDEX = kommando_data.두바이트(); check_lokal(INDEX,lokal_ANTAL);
                if (tillägg_värde == 21 || tillägg_värde == 25 || tillägg_värde == 54 || tillägg_värde == 58) inmatningsrad.add((tillägg_värde <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (tillägg_värde == 132) inmatningsrad.add("addl $" + kommando_data.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Översättning_fel("wide kommando 미지원");
            } else if (kommando == 198 || kommando == 199) {
                int mål_värde = position + kommando_data.부호두바이트(); gren_ange.add(mål_värde); Collections.addAll(inmatningsrad,"popl %eax","testl %eax, %eax",(kommando == 198 ? "je " : "jne ") + markör_värde + "_b" + mål_värde);
            } else throw new Översättning_fel("미지원 kommando: " + kommando);
        }
        if (!경계들.containsAll(gren_ange)) throw new Översättning_fel("kommando 경계가 아닌 곳으로 gren");
        inmatningsrad.add(".size " + markör_värde + ", .-" + markör_värde); return String.join("\n",inmatningsrad);
    }
    String X_86_konstant(Kurs_data data, int INDEX) {
        if (data.konstant_variant[INDEX] == 3) return data.konstant_data[INDEX].toString();
        if (data.konstant_variant[INDEX] == 8) return sträng_symbol(data.문자((Integer)data.konstant_data[INDEX]));
        throw new Översättning_fel("정수와 sträng_värde 상수만 stöd_värde");
    }
    String X_86_montering(String startpunkt, List<String> 내보냄, String mål) throws IOException {
        Map<String,String> dator_tabell = new HashMap<>();
        for (String inmatningsrad : Files.readAllLines(resurs_väg.resolve("_86_dator_Functions.tsv"))) { String[] länka_värde = inmatningsrad.split("\t"); if (länka_värde[0].equals(mål)) dator_tabell.put(länka_värde[1] + länka_värde[2],länka_värde[3]); }
        int positionsindex = startpunkt.lastIndexOf('.'); if (positionsindex < 0) throw new Översättning_fel("startpunkt Tilldela_värde fel");
        String ägare_värde = startpunkt.substring(0,positionsindex).replace('.','/'), metod_post_namn = startpunkt.substring(positionsindex + 1); metod_referens startpunkt_värde = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metod_referens referens = new metod_referens(ägare_värde,metod_post_namn,서술); if (함수들.containsKey(referens)) { if (startpunkt_värde != null) throw new Översättning_fel("겹친 startpunkt"); startpunkt_värde = referens; } }
        if (startpunkt_värde == null || (함수들.get(startpunkt_värde).ansluta_post & 0x100) != 0) throw new Översättning_fel("startpunkt_värde FUNKTION_värde format_värde fel");
        List<String> inmatningsrad = new ArrayList<>(); inmatningsrad.add(".code32");
        for (Kurs_data data : 클래스들.values()) {
            String status_värde = symbol("state",data.Namn), starta = symbol("init",data.Namn);
            Collections.addAll(inmatningsrad,".bss",".balign 4",status_värde + ": .long 0",".text",starta + ":","cmpl $0, " + status_värde,"jne " + starta + "_done","movl $1, " + status_värde);
            metod_referens 초기화참조 = new metod_referens(data.Namn,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) inmatningsrad.add("call " + symbol("method",초기화참조.부분들()));
            Collections.addAll(inmatningsrad,"movl $2, " + status_värde,starta + "_done:","ret");
            for (medlem_data fältvärde : data.fältvärde) {
                byte[] konstant_värde = fältvärde.attribut_värde.get("ConstantValue"); String värde = konstant_värde == null ? "0" : X_86_konstant(data,new data_Läsare(konstant_värde).두바이트());
                Collections.addAll(inmatningsrad,".data",".balign 4",symbol("field",data.Namn,fältvärde.Namn,fältvärde.서술) + ": .long " + värde);
            }
            for (medlem_data FUNKTION_värde : data.FUNKTION_värde) if (!FUNKTION_värde.Namn.equals("<init>")) inmatningsrad.add(X_86_metod_brödtext(new metod_referens(data.Namn,FUNKTION_värde.Namn,FUNKTION_värde.서술),FUNKTION_värde,dator_tabell,mål));
        }
        Collections.addAll(inmatningsrad,".text",".globl java_entry","java_entry:","call " + symbol("init",startpunkt_värde.ägare_värde),"call " + symbol("method",startpunkt_värde.부분들()));
        if (startpunkt_värde.서술.equals("()V")) inmatningsrad.add("xorl %eax, %eax"); inmatningsrad.add("ret");
        for (String Tilldela_värde : 내보냄) {
            int avgränsare_värde_d8ba4873 = Tilldela_värde.indexOf('='); if (avgränsare_värde_d8ba4873 < 1) throw new Översättning_fel("내보내기 Tilldela_värde fel");
            String extern_värde = Tilldela_värde.substring(0,avgränsare_värde_d8ba4873), FUNKTION_värde = Tilldela_värde.substring(avgränsare_värde_d8ba4873 + 1); int Division_KR = FUNKTION_värde.lastIndexOf('.');
            if (Division_KR < 0 || !extern_värde.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Översättning_fel("내보내기 symbol fel");
            String Kurs_värde = FUNKTION_värde.substring(0,Division_KR).replace('.','/'), Namn = FUNKTION_värde.substring(Division_KR + 1); metod_referens markering_värde = null;
            for (metod_referens referens : 함수들.keySet()) if (referens.ägare_värde.equals(Kurs_värde) && referens.Namn.equals(Namn)) { if (markering_värde != null) throw new Översättning_fel("겹친 내보내기 mål"); markering_värde = referens; }
            if (markering_värde == null) throw new Översättning_fel("내보낼 함수가 없음");
            Collections.addAll(inmatningsrad,".text",".globl " + extern_värde,extern_värde + ":","call " + symbol("init",markering_värde.ägare_värde),"jmp " + symbol("method",markering_värde.부분들()));
        }
        inmatningsrad.add(".section .rodata");
        for (Map.Entry<String,String> post_värde : 문자열들.entrySet()) {
            Collections.addAll(inmatningsrad,".balign 4",post_värde.getValue() + ":",".long " + post_värde.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char enhet_värde_7c611f50 : post_värde.getKey().toCharArray()) 단위들.add(Integer.toString(enhet_värde_7c611f50)); if (!단위들.isEmpty()) inmatningsrad.add(".long " + String.join(",",단위들));
        }
        inmatningsrad.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",inmatningsrad) + "\n";
    }
    static void köra_verktyg(List<String> kommando) throws Exception {
        if (new ProcessBuilder(kommando).inheritIO().start().waitFor() != 0) throw new Översättning_fel("kompilera_källa fel: " + kommando.get(0));
    }
    static String data_sträng(String text) { return "\"" + text.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Översättning(List<Path> indata_ange, String mål, String startpunkt, List<String> 내보냄, Path utmatningsposition, Path resurs_värde) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Kurs_väg = 임시.resolve("classes"); Files.createDirectory(Kurs_väg);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Kurs_väg.toString(),"-sourcepath",Kurs_väg.toString(),"-d",Kurs_väg.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int källa_ANTAL = 0;
            for (Path indata_värde : indata_ange) {
                if (utmatningsposition.toAbsolutePath().normalize().equals(indata_värde.toAbsolutePath().normalize())) throw new Översättning_fel("utmatningsposition 파일과 입력이 같음");
                if (indata_värde.toString().endsWith(".java")) { 자바명령.add(indata_värde.toString()); källa_ANTAL++; }
                else if (indata_värde.toString().endsWith(".class")) 바이트코드.add(indata_värde);
                else throw new Översättning_fel(".java 또는 .class만 stöd_värde");
            }
            if (källa_ANTAL > 0) köra_verktyg(자바명령);
            try (java.util.stream.Stream<Path> väg_ange = Files.walk(Kurs_väg)) { väg_ange.filter(sökväg_2 -> sökväg_2.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 KONVERTERA_värde = new 기계어미리번역(바이트코드,mål.equals("user") ? "user" : "kernel",262144,resurs_värde);
            String assemblera_värde = KONVERTERA_värde.X_86_montering(startpunkt,내보냄,mål); Files.writeString(임시.resolve("program.s"),assemblera_värde,StandardCharsets.UTF_8);
            Path verktyg_placera = resurs_värde.getParent();
            köra_verktyg(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            köra_verktyg(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),verktyg_placera.resolve("CLR_stöd.s").toString()));
            List<String> Anslut = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (mål.equals("kernel")) Anslut.add("-r");
            else {
                köra_verktyg(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),verktyg_placera.resolve(mål.equals("user") ? "START_användare_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Anslut,"-e","_start",임시.resolve("start.o").toString());
                if (mål.equals("user")) Collections.addAll(Anslut,"-T",verktyg_placera.resolve("användare_Länk_Layout.ld").toString());
            }
            Collections.addAll(Anslut,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); köra_verktyg(Anslut);
            utmatningsposition = utmatningsposition.toAbsolutePath(); Files.createDirectories(utmatningsposition.getParent()); Path publicera_värde = Files.createTempFile(utmatningsposition.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publicera_värde,StandardCopyOption.REPLACE_EXISTING); Files.move(publicera_värde,utmatningsposition,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publicera_värde); }
            Files.setPosixFilePermissions(utmatningsposition,java.nio.file.attribute.PosixFilePermissions.fromString(mål.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(utmatningsposition + ".s"),assemblera_värde,StandardCharsets.UTF_8);
            List<String> symbol_data = new ArrayList<>(), källa_data = new ArrayList<>();
            for (metod_referens referens : KONVERTERA_värde.함수들.keySet()) symbol_data.add(data_sträng(symbol("method",referens.부분들())) + ":" + data_sträng(referens.ägare_värde + "." + referens.Namn + referens.서술));
            for (Path indata_värde : indata_ange) {
                byte[] hash_fil = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(indata_värde)); StringBuilder text = new StringBuilder(); for (byte värde : hash_fil) text.append(String.format(Locale.ROOT,"%02x",värde & 255));
                källa_data.add(data_sträng(indata_värde.toAbsolutePath().toString()) + ":" + data_sträng(text.toString()));
            }
            Files.writeString(Paths.get(utmatningsposition + ".json"),"{\"target\":" + data_sträng(mål) + ",\"entry\":" + data_sträng(startpunkt) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbol_data) + "},\"sources\":{" + String.join(",",källa_data) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> väg_ange = Files.walk(임시)) { for (Path sökväg_2 : (Iterable<Path>)väg_ange.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(sökväg_2); }
        }
    }
    public static void main(String[] argument) {
        try {
            String startpunkt = null, mål = "kernel", X_86_mål = null; Path utleverans_väg = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> väg_ange = new ArrayList<>();
            for (int 순번 = 0; 순번 < argument.length; 순번++) {
                String värde = argument[순번];
                switch (värde) {
                    case "--target": X_86_mål = argument[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Kurs_värde.FUNKTION_värde -o utmatningsposition [--target linux|kernel|user] [--profile kernel|user] [--export symbol=Kurs_värde.FUNKTION_värde] 클래스파일 또는 Java원문"); return;
                    case "--entry": startpunkt = argument[++순번]; break;
                    case "--profile": mål = argument[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(argument[++순번]); break;
                    case "--export": 내보냄.add(argument[++순번]); break;
                    case "-o": utleverans_väg = Paths.get(argument[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (värde.startsWith("-")) throw new Översättning_fel("알 nummer 없는 옵션: " + värde); väg_ange.add(Paths.get(värde));
                }
            }
            if (startpunkt == null || utleverans_väg == null || väg_ange.isEmpty()) throw new Översättning_fel("--entry, -o, Kurs_värde 파일이 필요합니다");
            Path resurs_värde = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_mål != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_mål)) throw new Översättning_fel("알 nummer 없는 köra_kommando mål");
                X_86_Översättning(väg_ange,X_86_mål,startpunkt,내보냄,utleverans_väg,resurs_värde); return;
            }
            String källfil = new 기계어미리번역(väg_ange, mål, 낱말수, resurs_värde).generera(startpunkt, 내보냄, 범용표기);
            utleverans_väg = utleverans_väg.toAbsolutePath(); Files.createDirectories(utleverans_väg.getParent());
            Path 임시 = Files.createTempFile(utleverans_väg.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, källfil, StandardCharsets.UTF_8); Files.move(임시, utleverans_väg, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception fel) { System.err.println("kompilera_källa fel: " + fel.getMessage()); System.exit(1); }
    }
}
