// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Luokka_ARVO 파일에서 독립 ARM64 커널용 C 원문을 만든다. isäntä JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Käännös_virhe extends RuntimeException {
        Käännös_virhe(String 설명) { super(설명); }
    }
    static final class data_Lukija {
        final byte[] data;
        int paikka;
        data_Lukija(byte[] syöte_data) { data = syöte_data; }
        byte[] Luku(int kesto_ARVO) {
            if (kesto_ARVO < 0 || kesto_ARVO > data.length - paikka) throw new Käännös_virhe("잘린 Luokka_ARVO 또는 komento data");
            byte[] TULOS = Arrays.copyOfRange(data, paikka, paikka + kesto_ARVO); paikka += kesto_ARVO; return TULOS;
        }
        int lukea_tavu() { if (paikka >= data.length) throw new Käännös_virhe("잘린 komento data"); return data[paikka++] & 255; }
        int 두바이트() { return (lukea_tavu() << 8) | lukea_tavu(); }
        int lukea_KOKONAISLUKU() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) lukea_tavu(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class jäsen_data {
        final int pääsy_merkintä_68aed533;
        final String Nimi, 서술;
        final Map<String, byte[]> määritteen_arvo;
        jäsen_data(int pääsy_ARVO, String nimi_ARVO, String 서술값, Map<String, byte[]> määrite_data) {
            pääsy_merkintä_68aed533 = pääsy_ARVO; Nimi = nimi_ARVO; 서술 = 서술값; määritteen_arvo = määrite_data;
        }
    }
    static final class menetelmä_viite implements Comparable<menetelmä_viite> {
        final String omistaja_ARVO, Nimi, 서술;
        menetelmä_viite(String 소유값, String nimi_ARVO, String 서술값) { omistaja_ARVO = 소유값; Nimi = nimi_ARVO; 서술 = 서술값; }
        String[] 부분들() { return new String[]{omistaja_ARVO, Nimi, 서술}; }
        public int compareTo(menetelmä_viite vertaissolmu_ARVO) {
            int Vertailu_ARVO = omistaja_ARVO.compareTo(vertaissolmu_ARVO.omistaja_ARVO);
            if (Vertailu_ARVO == 0) Vertailu_ARVO = Nimi.compareTo(vertaissolmu_ARVO.Nimi);
            return Vertailu_ARVO == 0 ? 서술.compareTo(vertaissolmu_ARVO.서술) : Vertailu_ARVO;
        }
        public boolean equals(Object vertaissolmu_ARVO) { return vertaissolmu_ARVO instanceof menetelmä_viite && compareTo((menetelmä_viite) vertaissolmu_ARVO) == 0; }
        public int hashCode() { return Objects.hash(omistaja_ARVO, Nimi, 서술); }
    }
    static final class Luokka_data {
        final int[] 상수종류;
        final Object[] vakio_data;
        final String Nimi;
        final List<jäsen_data> kentän_arvo, funktio_ARVO;
        Luokka_data(Path polku_2) throws IOException {
            data_Lukija Lukija_ARVO = new data_Lukija(Files.readAllBytes(polku_2));
            if (Lukija_ARVO.lukea_KOKONAISLUKU() != 0xcafebabe) throw new Käännös_virhe("Java Luokka_ARVO 표식이 아님");
            Lukija_ARVO.Luku(4);
            int kohde_LASKE = Lukija_ARVO.두바이트(); 상수종류 = new int[kohde_LASKE]; vakio_data = new Object[kohde_LASKE];
            for (int 순번 = 1; 순번 < kohde_LASKE; 순번++) {
                int 종류 = Lukija_ARVO.lukea_tavu(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int kesto_ARVO = Lukija_ARVO.두바이트();
                        byte[] merkki_puskuri = Lukija_ARVO.Luku(kesto_ARVO), 길이붙인자료 = new byte[kesto_ARVO + 2];
                        길이붙인자료[0] = (byte)(kesto_ARVO >> 8); 길이붙인자료[1] = (byte)kesto_ARVO;
                        System.arraycopy(merkki_puskuri, 0, 길이붙인자료, 2, kesto_ARVO);
                        vakio_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: vakio_data[순번] = Lukija_ARVO.lukea_KOKONAISLUKU(); break;
                    case 4: Lukija_ARVO.Luku(4); break;
                    case 5: case 6: Lukija_ARVO.Luku(8); 순번++; break;
                    case 7: case 8: case 16: vakio_data[순번] = Lukija_ARVO.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        vakio_data[순번] = new int[]{Lukija_ARVO.두바이트(), Lukija_ARVO.두바이트()}; break;
                    case 15: vakio_data[순번] = new int[]{Lukija_ARVO.lukea_tavu(), Lukija_ARVO.두바이트()}; break;
                    default: throw new Käännös_virhe("지원하지 않는 vakio_ARVO 종류: " + 종류);
                }
            }
            Lukija_ARVO.두바이트(); Nimi = luokan_nimi(Lukija_ARVO.두바이트());
            if (!luokan_nimi(Lukija_ARVO.두바이트()).equals("java/lang/Object") || Lukija_ARVO.두바이트() != 0)
                throw new Käännös_virhe(Nimi + ": 상속 및 인터페이스 미지원");
            kentän_arvo = 멤버읽기(Lukija_ARVO); funktio_ARVO = 멤버읽기(Lukija_ARVO); lukea_määritteet(Lukija_ARVO);
            if (Lukija_ARVO.paikka != Lukija_ARVO.data.length) throw new Käännös_virhe("Luokka_ARVO 뒤에 남은 data");
        }
        String 문자(int INDEKSI) {
            if (INDEKSI < 1 || INDEKSI >= 상수종류.length || 상수종류[INDEKSI] != 1) throw new Käännös_virhe("문자 vakio_ARVO INDEKSI VIRHE");
            return (String) vakio_data[INDEKSI];
        }
        String luokan_nimi(int INDEKSI) {
            if (INDEKSI < 1 || INDEKSI >= 상수종류.length || 상수종류[INDEKSI] != 7) throw new Käännös_virhe("Luokka_ARVO viite VIRHE");
            return 문자((Integer)vakio_data[INDEKSI]);
        }
        menetelmä_viite viite(int INDEKSI) {
            if (INDEKSI < 1 || INDEKSI >= 상수종류.length || 상수종류[INDEKSI] < 9 || 상수종류[INDEKSI] > 11) throw new Käännös_virhe("멤버 viite VIRHE");
            int[] muodostaa_pari_ARVO = (int[])vakio_data[INDEKSI], nimi_muodostaa_pari = (int[])vakio_data[muodostaa_pari_ARVO[1]];
            return new menetelmä_viite(luokan_nimi(muodostaa_pari_ARVO[0]), 문자(nimi_muodostaa_pari[0]), 문자(nimi_muodostaa_pari[1]));
        }
        Map<String, byte[]> lukea_määritteet(data_Lukija Lukija_ARVO) {
            Map<String, byte[]> TULOS = new LinkedHashMap<>();
            int kohde_LASKE = Lukija_ARVO.두바이트();
            for (int 순번 = 0; 순번 < kohde_LASKE; 순번++) {
                String määrite_nimi = 문자(Lukija_ARVO.두바이트()); byte[] ARVO = Lukija_ARVO.Luku(Lukija_ARVO.lukea_KOKONAISLUKU());
                if (TULOS.put(määrite_nimi, ARVO) != null) throw new Käännös_virhe("겹친 määritteen_arvo: " + määrite_nimi);
            }
            return TULOS;
        }
        List<jäsen_data> 멤버읽기(data_Lukija Lukija_ARVO) {
            List<jäsen_data> TULOS = new ArrayList<>(); int kohde_LASKE = Lukija_ARVO.두바이트();
            for (int 순번 = 0; 순번 < kohde_LASKE; 순번++) {
                int pääsy_merkintä_68aed533 = Lukija_ARVO.두바이트(); String menetelmä_merkintä_nimi = 문자(Lukija_ARVO.두바이트()), 서술 = 문자(Lukija_ARVO.두바이트());
                TULOS.add(new jäsen_data(pääsy_merkintä_68aed533, menetelmä_merkintä_nimi, 서술, lukea_määritteet(Lukija_ARVO)));
            }
            return TULOS;
        }
    }
    static final class 함수형식 {
        final List<String> argumentit = new ArrayList<>();
        final String palauttaa_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Käännös_virhe("funktio_ARVO 서술 VIRHE: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Käännös_virhe("funktio_ARVO 서술 VIRHE: " + 서술);
            argumentit.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (argumentit.contains("V") || 반환들.size() != 1) throw new Käännös_virhe("funktio_ARVO 서술 VIRHE: " + 서술);
            palauttaa_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> TULOS = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int paikka = 0; paikka < 서술.length();) {
            String valinta_ARVO = null;
            for (String muoto_ARVO : 허용형식) if (서술.startsWith(muoto_ARVO, paikka)) { valinta_ARVO = muoto_ARVO; break; }
            if (valinta_ARVO == null) throw new Käännös_virhe("지원하지 않는 tietotyyppi: " + 서술);
            TULOS.add(valinta_ARVO); paikka += valinta_ARVO.length();
        }
        return TULOS;
    }
    static String symboli(String 종류, String... 부분들) {
        try {
            byte[] hajautusarvo_Tiedosto = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder teksti = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) teksti.append(String.format(Locale.ROOT, "%02x", hajautusarvo_Tiedosto[순번] & 255));
            return teksti.toString();
        } catch (Exception VIRHE) { throw new Käännös_virhe(VIRHE.toString()); }
    }
    final Map<String, Luokka_data> 클래스들 = new TreeMap<>();
    final Map<menetelmä_viite, jäsen_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), kone_Funktiot_c3a8e64a = new LinkedHashMap<>();
    final String suoritus_kohde, kone_Luokka;
    final int keko_Word_LASKE;
    final Path resurssi_polku;
    기계어미리번역(List<Path> polku_luettelo, String tavoite, int 낱말수, Path resurssi_ARVO) throws IOException {
        if ((!tavoite.equals("kernel") && !tavoite.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Käännös_virhe("Suorita_komento tavoite 또는 Muisti_ARVO OSOITE_alue Koko VIRHE");
        suoritus_kohde = tavoite; keko_Word_LASKE = 낱말수; resurssi_polku = resurssi_ARVO;
        // 이 이름도 국가별 lähde_puu generoida 시 해당 언어로 옮긴다.
        kone_Luokka = tavoite.equals("kernel") ? "Taulu" : "käyttäjätila";
        for (String syöterivi : Files.readAllLines(resurssi_ARVO.resolve("kone_Funktiot.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = syöterivi.split("\t", -1);
            if (부분들.length != 4) throw new Käännös_virhe("kone funktio_ARVO data VIRHE");
            if (부분들[0].equals(tavoite)) kone_Funktiot_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path polku_2 : polku_luettelo) {
            Luokka_data data = new Luokka_data(polku_2);
            if (클래스들.put(data.Nimi, data) != null) throw new Käännös_virhe("중복 Luokka_ARVO: " + data.Nimi);
            for (jäsen_data kentän_arvo : data.kentän_arvo) {
                if ((kentän_arvo.pääsy_merkintä_68aed533 & 8) == 0 || 형식읽기(kentän_arvo.서술).equals(Collections.singletonList("V"))) throw new Käännös_virhe("staattinen_ARVO 필드만 Tuki_ARVO");
                if (필드들.put(new menetelmä_viite(data.Nimi, kentän_arvo.Nimi, kentän_arvo.서술), kentän_arvo) != null) throw new Käännös_virhe("중복 kentän_arvo");
            }
            for (jäsen_data funktio_ARVO : data.funktio_ARVO) {
                if (funktio_ARVO.Nimi.equals("<init>")) continue;
                if ((funktio_ARVO.pääsy_merkintä_68aed533 & 8) == 0 || (funktio_ARVO.pääsy_merkintä_68aed533 & (0x20 | 0x400)) != 0) throw new Käännös_virhe("staattinen_ARVO 비동기화 함수만 Tuki_ARVO");
                new 함수형식(funktio_ARVO.서술);
                if (함수들.put(new menetelmä_viite(data.Nimi, funktio_ARVO.Nimi, funktio_ARVO.서술), funktio_ARVO) != null) throw new Käännös_virhe("중복 funktio_ARVO");
            }
        }
    }
    String merkkijono_symboli(String teksti) { return 문자열들.computeIfAbsent(teksti, ARVO -> "j_text_" + 문자열들.size()); }
    String vakio_lauseke(Luokka_data data, int INDEKSI) {
        if (INDEKSI < 1 || INDEKSI >= data.상수종류.length) throw new Käännös_virhe("vakio_ARVO INDEKSI leikata VIRHE");
        if (data.상수종류[INDEKSI] == 3) return "(word)(uint32_t)(" + data.vakio_data[INDEKSI] + ")";
        if (data.상수종류[INDEKSI] == 8) return "(word)" + merkkijono_symboli(data.문자((Integer)data.vakio_data[INDEKSI]));
        throw new Käännös_virhe("정수와 merkkijono_ARVO 상수만 Tuki_ARVO");
    }
    String 함수원형(menetelmä_viite viite) {
        List<String> 인수들 = new ArrayList<>(); int kohde_LASKE = new 함수형식(viite.서술).argumentit.size();
        for (int 순번 = 0; 순번 < kohde_LASKE; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symboli("method", viite.부분들()) + "(" + (kohde_LASKE == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void sekki_paikallinen(int INDEKSI, int paikallinen_muuttuja_LASKE) { if (INDEKSI < 0 || INDEKSI >= paikallinen_muuttuja_LASKE) throw new Käännös_virhe("paikallinen_laajuus muuttuja_ARVO INDEKSI leikata VIRHE"); }
    void 분기넣기(List<String> tulostuspaikka, Set<Integer> haara_luettelo, int paikka, int 이동량, String ehto) {
        int kohde_ARVO = paikka + 이동량; haara_luettelo.add(kohde_ARVO);
        tulostuspaikka.add((ehto == null ? "" : "if (" + ehto + ") ") + "goto b" + kohde_ARVO + ";");
    }
    String menetelmä_teksti(menetelmä_viite funktio_ARVO, jäsen_data data) {
        byte[] teksti_data = data.määritteen_arvo.get("Code"); if (teksti_data == null) throw new Käännös_virhe("funktio_ARVO 몸체가 없음: " + funktio_ARVO.Nimi);
        data_Lukija Lukija_ARVO = new data_Lukija(teksti_data); int 쌓임깊이 = Lukija_ARVO.두바이트(), paikallinen_muuttuja_LASKE = Lukija_ARVO.두바이트();
        data_Lukija komento_data = new data_Lukija(Lukija_ARVO.Luku(Lukija_ARVO.lukea_KOKONAISLUKU()));
        if (Lukija_ARVO.두바이트() != 0) throw new Käännös_virhe("try/catch/finally 미지원");
        함수형식 muoto_ARVO = new 함수형식(funktio_ARVO.서술); if (paikallinen_muuttuja_LASKE < muoto_ARVO.argumentit.size()) throw new Käännös_virhe("매개변수보다 적은 paikallinen_laajuus muuttuja_ARVO");
        Luokka_data Luokka_ARVO = 클래스들.get(funktio_ARVO.omistaja_ARVO);
        List<String> tulostuspaikka = new ArrayList<>(); tulostuspaikka.add(함수원형(funktio_ARVO) + " {");
        tulostuspaikka.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(paikallinen_muuttuja_LASKE, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < muoto_ARVO.argumentit.size(); 순번++) tulostuspaikka.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), haara_luettelo = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (komento_data.paikka < komento_data.data.length) {
            int paikka = komento_data.paikka, komento = komento_data.lukea_tavu(); 경계들.add(paikka); tulostuspaikka.add("b" + paikka + ":;");
            if (komento == 0) continue;
            if (komento == 1) tulostuspaikka.add("PUSH(0);");
            else if (komento >= 2 && komento <= 8) tulostuspaikka.add("PUSH((uint32_t)(" + (komento - 3) + "));");
            else if (komento == 16 || komento == 17) tulostuspaikka.add("PUSH((uint32_t)(" + (komento == 16 ? komento_data.부호한바이트() : komento_data.부호두바이트()) + "));");
            else if (komento == 18 || komento == 19) tulostuspaikka.add("PUSH(" + vakio_lauseke(Luokka_ARVO, komento == 18 ? komento_data.lukea_tavu() : komento_data.두바이트()) + ");");
            else if (komento == 21 || komento == 25 || (komento >= 26 && komento <= 29) || (komento >= 42 && komento <= 45)) {
                int INDEKSI = komento == 21 || komento == 25 ? komento_data.lukea_tavu() : komento - (komento <= 29 ? 26 : 42);
                sekki_paikallinen(INDEKSI, paikallinen_muuttuja_LASKE); tulostuspaikka.add("PUSH(l[" + INDEKSI + "]);");
            } else if (komento == 54 || komento == 58 || (komento >= 59 && komento <= 62) || (komento >= 75 && komento <= 78)) {
                int INDEKSI = komento == 54 || komento == 58 ? komento_data.lukea_tavu() : komento - (komento <= 62 ? 59 : 75);
                sekki_paikallinen(INDEKSI, paikallinen_muuttuja_LASKE); tulostuspaikka.add("l[" + INDEKSI + "] = POP();");
            } else if (komento == 46) tulostuspaikka.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (komento == 79) tulostuspaikka.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (komento == 87 || komento == 88) tulostuspaikka.add(komento == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (komento >= 89 && komento <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] tilata_luettelo = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[komento - 89]; 순번++) tulostuspaikka.add("abcd".charAt(순번) + " = POP();");
                for (char ARVO : tilata_luettelo[komento - 89].toCharArray()) tulostuspaikka.add("PUSH(" + ARVO + ");");
            } else if (komento == 96 || komento == 100 || komento == 104 || komento == 126 || komento == 128 || komento == 130) {
                String leikkaus_ARVO = komento == 96 ? "+" : komento == 100 ? "-" : komento == 104 ? "*" : komento == 126 ? "&" : komento == 128 ? "|" : "^";
                tulostuspaikka.add("b = POP(); a = POP(); PUSH((uint32_t)a " + leikkaus_ARVO + " (uint32_t)b);");
            } else if (komento == 108 || komento == 112) tulostuspaikka.add("b = POP(); a = POP(); PUSH(divide(a,b," + (komento == 112 ? 1 : 0) + "));");
            else if (komento == 116) tulostuspaikka.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (komento == 120 || komento == 122 || komento == 124) {
                tulostuspaikka.add("b = POP(); a = POP();"); tulostuspaikka.add("PUSH(" + (komento == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (komento == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (komento == 132) {
                int INDEKSI = komento_data.lukea_tavu(), 증가량 = komento_data.부호한바이트(); sekki_paikallinen(INDEKSI, paikallinen_muuttuja_LASKE);
                tulostuspaikka.add("l[" + INDEKSI + "] = (uint32_t)l[" + INDEKSI + "] + (uint32_t)(" + 증가량 + ");");
            } else if (komento >= 145 && komento <= 147) tulostuspaikka.add("a = POP(); PUSH((uint32_t)(" + (komento == 145 ? "int8_t" : komento == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (komento >= 153 && komento <= 158) {
                tulostuspaikka.add("a = POP();"); 분기넣기(tulostuspaikka, haara_luettelo, paikka, komento_data.부호두바이트(), "(int32_t)a " + 비교들[komento - 153] + " 0");
            } else if (komento >= 159 && komento <= 166) {
                tulostuspaikka.add("b = POP(); a = POP();"); 분기넣기(tulostuspaikka, haara_luettelo, paikka, komento_data.부호두바이트(), komento >= 165 ? "a " + 비교들[komento - 159] + " b" : "(int32_t)a " + 비교들[komento - 159] + " (int32_t)b");
            } else if (komento == 167 || komento == 200) 분기넣기(tulostuspaikka, haara_luettelo, paikka, komento == 167 ? komento_data.부호두바이트() : komento_data.lukea_KOKONAISLUKU(), null);
            else if (komento == 170 || komento == 171) {
                while (komento_data.paikka % 4 != 0) komento_data.lukea_tavu();
                int oletusarvo = komento_data.lukea_KOKONAISLUKU(); tulostuspaikka.add("a = POP();");
                if (komento == 170) {
                    int 아래 = komento_data.lukea_KOKONAISLUKU(), 위 = komento_data.lukea_KOKONAISLUKU(); long kohde_LASKE = (long)위 - 아래 + 1;
                    if (kohde_LASKE < 1 || kohde_LASKE > (komento_data.data.length - komento_data.paikka) / 4) throw new Käännös_virhe("switch leikata VIRHE");
                    for (long ARVO = 아래; ARVO <= 위; ARVO++) 분기넣기(tulostuspaikka, haara_luettelo, paikka, komento_data.lukea_KOKONAISLUKU(), "(int32_t)a == (" + ARVO + ")");
                } else {
                    int kohde_LASKE = komento_data.lukea_KOKONAISLUKU(), etukamera_data = 0;
                    if (kohde_LASKE < 0 || kohde_LASKE > (komento_data.data.length - komento_data.paikka) / 8) throw new Käännös_virhe("switch Koko VIRHE");
                    for (int 순번 = 0; 순번 < kohde_LASKE; 순번++) {
                        int ARVO = komento_data.lukea_KOKONAISLUKU(); if (순번 > 0 && ARVO <= etukamera_data) throw new Käännös_virhe("switch tilata_ARVO VIRHE"); etukamera_data = ARVO;
                        분기넣기(tulostuspaikka, haara_luettelo, paikka, komento_data.lukea_KOKONAISLUKU(), "(int32_t)a == (" + ARVO + ")");
                    }
                }
                분기넣기(tulostuspaikka, haara_luettelo, paikka, oletusarvo, null);
            } else if (komento == 172 || komento == 176 || komento == 177) tulostuspaikka.add("return " + (komento == 177 ? "0" : "POP()") + ";");
            else if (komento == 178 || komento == 179) {
                menetelmä_viite viite = Luokka_ARVO.viite(komento_data.두바이트()); if (!필드들.containsKey(viite)) throw new Käännös_virhe("알 numero 없는 kentän_arvo");
                tulostuspaikka.add(symboli("init", viite.omistaja_ARVO) + "();"); String kentän_arvo = symboli("field", viite.부분들());
                tulostuspaikka.add(komento == 178 ? "PUSH(" + kentän_arvo + ");" : kentän_arvo + " = POP();");
            } else if (komento == 184) {
                menetelmä_viite viite = Luokka_ARVO.viite(komento_data.두바이트()); if (!함수들.containsKey(viite)) throw new Käännös_virhe("알 numero 없는 funktio_ARVO");
                함수형식 호출형식 = new 함수형식(viite.서술); int kohde_LASKE = 호출형식.argumentit.size();
                tulostuspaikka.add(symboli("init", viite.omistaja_ARVO) + "();"); tulostuspaikka.add("if(sp < " + kohde_LASKE + ") kernel_panic(\"call stack underflow\"); sp -= " + kohde_LASKE + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < kohde_LASKE; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                tulostuspaikka.add("a = " + symboli("method", viite.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.palauttaa_KR.equals("V")) tulostuspaikka.add("PUSH(a);");
            } else if (komento == 182) {
                menetelmä_viite viite = Luokka_ARVO.viite(komento_data.두바이트());
                if (viite.equals(new menetelmä_viite("java/lang/String", "length", "()I"))) tulostuspaikka.add("a = POP(); PUSH(length(a));");
                else if (viite.equals(new menetelmä_viite("java/lang/String", "charAt", "(I)C"))) tulostuspaikka.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Käännös_virhe("가상 funktio_ARVO 호출 미지원");
            } else if (komento == 188) {
                if (komento_data.lukea_tavu() != 10) throw new Käännös_virhe("new int[]만 Tuki_ARVO"); tulostuspaikka.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (komento == 190) tulostuspaikka.add("a = POP(); PUSH(length(a));");
            else if (komento == 196) {
                int tarkenne_ARVO = komento_data.lukea_tavu(), INDEKSI = komento_data.두바이트(); sekki_paikallinen(INDEKSI, paikallinen_muuttuja_LASKE);
                if (tarkenne_ARVO == 21 || tarkenne_ARVO == 25) tulostuspaikka.add("PUSH(l[" + INDEKSI + "]);");
                else if (tarkenne_ARVO == 54 || tarkenne_ARVO == 58) tulostuspaikka.add("l[" + INDEKSI + "] = POP();");
                else if (tarkenne_ARVO == 132) tulostuspaikka.add("l[" + INDEKSI + "] = (uint32_t)l[" + INDEKSI + "] + (uint32_t)(" + komento_data.부호두바이트() + ");");
                else throw new Käännös_virhe("미지원 wide komento");
            } else if (komento == 198 || komento == 199) {
                tulostuspaikka.add("a = POP();"); 분기넣기(tulostuspaikka, haara_luettelo, paikka, komento_data.부호두바이트(), "a " + (komento == 198 ? "==" : "!=") + " 0");
            } else throw new Käännös_virhe(funktio_ARVO.omistaja_ARVO + "." + funktio_ARVO.Nimi + ", tavu_ARVO " + paikka + ": 미지원 komento " + komento);
        }
        if (!경계들.containsAll(haara_luettelo)) throw new Käännös_virhe("komento 경계가 아닌 곳으로 haara");
        tulostuspaikka.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", tulostuspaikka);
    }
    String viedä_menetelmä(String Linkki_symboli, String tavoite, boolean 진입점여부) {
        int sijainti = tavoite.lastIndexOf('.'); if (sijainti < 0 || !Linkki_symboli.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Käännös_virhe("내보내기 Määritä_ARVO VIRHE");
        String omistaja_ARVO = tavoite.substring(0, sijainti).replace('.', '/'), Nimi = tavoite.substring(sijainti + 1); menetelmä_viite valinta_ARVO = null;
        for (menetelmä_viite viite : 함수들.keySet()) if (viite.omistaja_ARVO.equals(omistaja_ARVO) && viite.Nimi.equals(Nimi)) {
            if (valinta_ARVO != null) throw new Käännös_virhe("겹친 내보내기 tavoite"); valinta_ARVO = viite;
        }
        if (valinta_ARVO == null || (함수들.get(valinta_ARVO).pääsy_merkintä_68aed533 & 0x100) != 0) throw new Käännös_virhe("내보낼 함수가 없음 또는 native funktio_ARVO");
        함수형식 muoto_ARVO = new 함수형식(valinta_ARVO.서술);
        if ((진입점여부 && !muoto_ARVO.argumentit.isEmpty()) || !Arrays.asList("V", "I").contains(muoto_ARVO.palauttaa_KR)) throw new Käännös_virhe("aloituskohta_ARVO 또는 C rajattu_alue_ARVO muoto_ARVO VIRHE");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < muoto_ARVO.argumentit.size(); 순번++) {
            if (!muoto_ARVO.argumentit.get(순번).equals("I")) throw new Käännös_virhe("C 경계는 int 인수만 Tuki_ARVO");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (muoto_ARVO.palauttaa_KR.equals("V") ? "void " : "int32_t ") + Linkki_symboli + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symboli("init", valinta_ARVO.omistaja_ARVO) + "(); " + (muoto_ARVO.palauttaa_KR.equals("V") ? "" : "return (int32_t)") + symboli("method", valinta_ARVO.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generoida(String aloituskohta, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<menetelmä_viite, jäsen_data> merkintä_ARVO_962f286b : 함수들.entrySet()) {
            menetelmä_viite viite = merkintä_ARVO_962f286b.getKey(); jäsen_data data = merkintä_ARVO_962f286b.getValue(); 선언들.add(함수원형(viite) + ";");
            if ((data.pääsy_merkintä_68aed533 & 0x100) != 0) {
                String Yhdistä = kone_Funktiot_c3a8e64a.get(viite.Nimi + viite.서술);
                if (!viite.omistaja_ARVO.equals(kone_Luokka) || Yhdistä == null) throw new Käännös_virhe("허용되지 않은 native funktio_ARVO: " + viite.Nimi);
                int kohde_LASKE = new 함수형식(viite.서술).argumentit.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < kohde_LASKE; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Yhdistä + "(" + (kohde_LASKE == 0 ? "void" : String.join(",", Collections.nCopies(kohde_LASKE, "word"))) + ");");
                몸체들.add(함수원형(viite) + " { return " + Yhdistä + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(menetelmä_teksti(viite, data));
        }
        for (Map.Entry<menetelmä_viite, jäsen_data> merkintä_ARVO_962f286b : 필드들.entrySet()) {
            menetelmä_viite viite = merkintä_ARVO_962f286b.getKey(); byte[] vakio_ARVO = merkintä_ARVO_962f286b.getValue().määritteen_arvo.get("ConstantValue");
            String ARVO = vakio_ARVO == null ? "0" : vakio_lauseke(클래스들.get(viite.omistaja_ARVO), new data_Lukija(vakio_ARVO).두바이트());
            필드선언들.add("static word " + symboli("field", viite.부분들()) + " = " + ARVO + ";");
        }
        for (String Nimi : 클래스들.keySet()) {
            String alustaa = symboli("init", Nimi), Tila_ARVO = symboli("state", Nimi);
            선언들.add("static void " + alustaa + "(void);"); 필드선언들.add("static unsigned " + Tila_ARVO + ";");
            menetelmä_viite viite = new menetelmä_viite(Nimi, "<clinit>", "()V");
            몸체들.add("static void " + alustaa + "(void) { if(" + Tila_ARVO + ") return; " + Tila_ARVO + " = 1; " + (함수들.containsKey(viite) ? symboli("method", viite.부분들()) + "(); " : "") + Tila_ARVO + " = 2; }");
        }
        몸체들.add(viedä_menetelmä("java_entry", aloituskohta, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Määritä_ARVO : 내보내기목록) {
            int sijainti = Määritä_ARVO.indexOf('='); if (sijainti < 1) throw new Käännös_virhe("내보내기 Määritä_ARVO VIRHE");
            String Nimi = Määritä_ARVO.substring(0, sijainti); 공개이름.add(Nimi); 몸체들.add(viedä_menetelmä(Nimi, Määritä_ARVO.substring(sijainti + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> merkintä_ARVO_962f286b : 문자열들.entrySet()) {
            String teksti = merkintä_ARVO_962f286b.getKey(); StringBuilder MATRIISI_ARVO = new StringBuilder("static const word " + merkintä_ARVO_962f286b.getValue() + "[] = {" + teksti.length());
            for (int 순번 = 0; 순번 < teksti.length(); 순번++) MATRIISI_ARVO.append(", ").append((int)teksti.charAt(순번));
            문자열선언들.add(MATRIISI_ARVO.append("};").toString());
        }
        String Tuki_ARVO = Files.readString(resurssi_polku.resolve("CLR_Tuki.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(keko_Word_LASKE));
        return 기계원문한국어화(Tuki_ARVO + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String lähdetiedosto, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nimi_taulukko = new HashMap<>();
        for (String syöterivi : Files.readAllLines(resurssi_polku.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] muodostaa_pari_ARVO = syöterivi.split("\t"); nimi_taulukko.put(muodostaa_pari_ARVO[0], muodostaa_pari_ARVO[1]);
        }
        Pattern lohko_lauseke = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = lohko_lauseke.matcher(lähdetiedosto); StringBuffer TULOS = new StringBuffer();
        while (찾개.find()) {
            String Nimi = 찾개.group(), 새이름 = Nimi;
            if (!Nimi.startsWith("//") && !Nimi.startsWith("/*") && !Nimi.startsWith("\"") && !Nimi.startsWith("'") && !공개이름.contains(Nimi)) {
                새이름 = nimi_taulukko.getOrDefault(Nimi, Nimi);
                if (Nimi.matches("a[0-9]+")) 새이름 = "argumentit" + Nimi.substring(1);
                if (Nimi.matches("b[0-9]+")) 새이름 = "haara" + Nimi.substring(1);
                if (범용표기) {
                    StringBuilder merkintätapa_ARVO = new StringBuilder();
                    for (char merkki_ARVO : 새이름.toCharArray()) merkintätapa_ARVO.append(merkki_ARVO < 128 ? Character.toString(merkki_ARVO) : String.format(Locale.ROOT, "\\u%04x", (int)merkki_ARVO));
                    새이름 = merkintätapa_ARVO.toString();
                }
            }
            찾개.appendReplacement(TULOS, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(TULOS); return TULOS.toString();
    }
    String X_86_menetelmä_teksti(menetelmä_viite funktio_ARVO, jäsen_data data, Map<String,String> kone_taulukko, String tavoite) {
        String merkintä_ARVO = symboli("method", funktio_ARVO.부분들());
        List<String> syöterivi = new ArrayList<>();
        if ((data.pääsy_merkintä_68aed533 & 0x100) != 0) {
            String Yhdistä = kone_taulukko.get(funktio_ARVO.Nimi + funktio_ARVO.서술);
            if (!funktio_ARVO.omistaja_ARVO.equals(tavoite.equals("kernel") ? "laite_ARVO" : "käyttäjätila") || Yhdistä == null) throw new Käännös_virhe("허용되지 않은 native funktio_ARVO");
            return ".text\n" + merkintä_ARVO + ":\njmp " + Yhdistä;
        }
        byte[] leipäteksti = data.määritteen_arvo.get("Code"); if (leipäteksti == null) throw new Käännös_virhe("funktio_ARVO 몸체가 없음");
        data_Lukija Lukija_ARVO = new data_Lukija(leipäteksti); Lukija_ARVO.두바이트(); int paikallinen_LASKE = Lukija_ARVO.두바이트();
        data_Lukija komento_data = new data_Lukija(Lukija_ARVO.Luku(Lukija_ARVO.lukea_KOKONAISLUKU()));
        if (Lukija_ARVO.두바이트() != 0) throw new Käännös_virhe("try/catch/finally 미지원");
        함수형식 muoto_ARVO = new 함수형식(funktio_ARVO.서술); if (paikallinen_LASKE < muoto_ARVO.argumentit.size()) throw new Käännös_virhe("매개변수보다 적은 paikallinen_laajuus muuttuja_ARVO");
        Collections.addAll(syöterivi,".text",".globl " + merkintä_ARVO,".type " + merkintä_ARVO + ", @function",merkintä_ARVO + ":","pushl %ebp","movl %esp, %ebp","subl $" + paikallinen_LASKE * 4 + ", %esp");
        for (int 순번 = 0; 순번 < muoto_ARVO.argumentit.size(); 순번++) Collections.addAll(syöterivi,"movl " + (8 + 4 * (muoto_ARVO.argumentit.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Luokka_data Luokka_ARVO = 클래스들.get(funktio_ARVO.omistaja_ARVO); Set<Integer> 경계들 = new HashSet<>(), haara_luettelo = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (komento_data.paikka < komento_data.data.length) {
            int paikka = komento_data.paikka, komento = komento_data.lukea_tavu(); String sijainti = merkintä_ARVO + "_b" + paikka;
            syöterivi.add(sijainti + ":"); 경계들.add(paikka);
            if (komento == 0) syöterivi.add("nop");
            else if (komento == 1) syöterivi.add("pushl $0");
            else if (komento >= 2 && komento <= 8) syöterivi.add("pushl $" + (komento - 3));
            else if (komento == 16 || komento == 17) syöterivi.add("pushl $" + (komento == 16 ? komento_data.부호한바이트() : komento_data.부호두바이트()));
            else if (komento == 18 || komento == 19) {
                int INDEKSI = komento == 18 ? komento_data.lukea_tavu() : komento_data.두바이트();
                syöterivi.add("pushl $" + X_86_vakio(Luokka_ARVO,INDEKSI));
            } else if (komento == 21 || komento == 25 || (komento >= 26 && komento <= 29) || (komento >= 42 && komento <= 45) || komento == 54 || komento == 58 || (komento >= 59 && komento <= 62) || (komento >= 75 && komento <= 78)) {
                boolean lukea_KR = komento < 54; int INDEKSI = komento == 21 || komento == 25 || komento == 54 || komento == 58 ? komento_data.lukea_tavu() : komento - (komento <= 29 ? 26 : komento <= 45 ? 42 : komento <= 62 ? 59 : 75);
                sekki_paikallinen(INDEKSI,paikallinen_LASKE); syöterivi.add((lukea_KR ? "pushl " : "popl ") + "-" + (4 * (INDEKSI + 1)) + "(%ebp)");
            } else if (komento == 46) Collections.addAll(syöterivi,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (komento == 79) Collections.addAll(syöterivi,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (komento == 87 || komento == 88) syöterivi.add("addl $" + (komento == 87 ? 4 : 8) + ", %esp");
            else if (komento >= 89 && komento <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] tilata_luettelo = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[komento - 89]; 순번++) syöterivi.add("popl " + 저장기들[순번]);
                for (int 순번 : tilata_luettelo[komento - 89]) syöterivi.add("pushl " + 저장기들[순번]);
            } else if (komento == 96 || komento == 100 || komento == 104 || komento == 126 || komento == 128 || komento == 130) {
                String leikkaus_ARVO = komento == 96 ? "addl" : komento == 100 ? "subl" : komento == 104 ? "imull" : komento == 126 ? "andl" : komento == 128 ? "orl" : "xorl";
                Collections.addAll(syöterivi,"popl %ecx","popl %eax",leikkaus_ARVO + " %ecx, %eax","pushl %eax");
            } else if (komento == 108 || komento == 112) Collections.addAll(syöterivi,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + sijainti + "_divide","cmpl $0x80000000, %eax","jne " + sijainti + "_divide","xorl %edx, %edx","jmp " + sijainti + "_done",sijainti + "_divide:","cltd","idivl %ecx",sijainti + "_done:","pushl " + (komento == 108 ? "%eax" : "%edx"));
            else if (komento == 116) syöterivi.add("negl (%esp)");
            else if (komento == 120 || komento == 122 || komento == 124) Collections.addAll(syöterivi,"popl %ecx","popl %eax",(komento == 120 ? "sall" : komento == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (komento == 132) {
                int INDEKSI = komento_data.lukea_tavu(), 증가 = komento_data.부호한바이트(); sekki_paikallinen(INDEKSI,paikallinen_LASKE); syöterivi.add("addl $" + 증가 + ", -" + (4 * (INDEKSI + 1)) + "(%ebp)");
            } else if (komento >= 145 && komento <= 147) Collections.addAll(syöterivi,"popl %eax",komento == 145 ? "movsbl %al, %eax" : komento == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (komento >= 153 && komento <= 166) {
                if (komento <= 158) Collections.addAll(syöterivi,"popl %eax","testl %eax, %eax");
                else Collections.addAll(syöterivi,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int kohde_ARVO = paikka + komento_data.부호두바이트(); haara_luettelo.add(kohde_ARVO); syöterivi.add(비교들[komento - (komento <= 158 ? 153 : 159)] + " " + merkintä_ARVO + "_b" + kohde_ARVO);
            } else if (komento == 167 || komento == 200) {
                int kohde_ARVO = paikka + (komento == 167 ? komento_data.부호두바이트() : komento_data.lukea_KOKONAISLUKU()); haara_luettelo.add(kohde_ARVO); syöterivi.add("jmp " + merkintä_ARVO + "_b" + kohde_ARVO);
            } else if (komento == 170 || komento == 171) {
                while (komento_data.paikka % 4 != 0) komento_data.lukea_tavu();
                int oletusarvo = paikka + komento_data.lukea_KOKONAISLUKU(); haara_luettelo.add(oletusarvo); syöterivi.add("popl %eax");
                int kohde_LASKE, 아래 = 0;
                if (komento == 170) { 아래 = komento_data.lukea_KOKONAISLUKU(); int 위 = komento_data.lukea_KOKONAISLUKU(); long kesto_ARVO = (long)위 - 아래 + 1; if (kesto_ARVO < 1 || kesto_ARVO > (komento_data.data.length - komento_data.paikka) / 4) throw new Käännös_virhe("switch leikata VIRHE"); kohde_LASKE = (int)kesto_ARVO; }
                else { kohde_LASKE = komento_data.lukea_KOKONAISLUKU(); if (kohde_LASKE < 0 || kohde_LASKE > (komento_data.data.length - komento_data.paikka) / 8) throw new Käännös_virhe("switch Koko VIRHE"); }
                for (int 순번 = 0; 순번 < kohde_LASKE; 순번++) {
                    int ARVO = komento == 170 ? 아래 + 순번 : komento_data.lukea_KOKONAISLUKU(), kohde_ARVO = paikka + komento_data.lukea_KOKONAISLUKU(); haara_luettelo.add(kohde_ARVO);
                    Collections.addAll(syöterivi,"cmpl $" + ARVO + ", %eax","je " + merkintä_ARVO + "_b" + kohde_ARVO);
                }
                syöterivi.add("jmp " + merkintä_ARVO + "_b" + oletusarvo);
            } else if (komento == 172 || komento == 176 || komento == 177) {
                if (komento != 177) syöterivi.add("popl %eax"); Collections.addAll(syöterivi,"leave","ret");
            } else if (komento == 178 || komento == 179) {
                menetelmä_viite viite = Luokka_ARVO.viite(komento_data.두바이트()); if (!필드들.containsKey(viite)) throw new Käännös_virhe("알 numero 없는 kentän_arvo");
                Collections.addAll(syöterivi,"call " + symboli("init",viite.omistaja_ARVO),(komento == 178 ? "pushl " : "popl ") + symboli("field",viite.부분들()));
            } else if (komento == 184) {
                menetelmä_viite viite = Luokka_ARVO.viite(komento_data.두바이트()); if (!함수들.containsKey(viite)) throw new Käännös_virhe("알 numero 없는 funktio_ARVO");
                함수형식 호출형식 = new 함수형식(viite.서술); Collections.addAll(syöterivi,"call " + symboli("init",viite.omistaja_ARVO),"call " + symboli("method",viite.부분들()));
                if (!호출형식.argumentit.isEmpty()) syöterivi.add("addl $" + 호출형식.argumentit.size() * 4 + ", %esp");
                if (!호출형식.palauttaa_KR.equals("V")) syöterivi.add("pushl %eax");
            } else if (komento == 182) {
                menetelmä_viite viite = Luokka_ARVO.viite(komento_data.두바이트());
                if (viite.equals(new menetelmä_viite("java/lang/String","length","()I"))) Collections.addAll(syöterivi,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (viite.equals(new menetelmä_viite("java/lang/String","charAt","(I)C"))) Collections.addAll(syöterivi,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Käännös_virhe("가상 funktio_ARVO 호출 미지원");
            } else if (komento == 188) {
                if (komento_data.lukea_tavu() != 10) throw new Käännös_virhe("new int[]만 Tuki_ARVO"); Collections.addAll(syöterivi,"popl %eax","call rt_new_array","pushl %eax");
            } else if (komento == 190) Collections.addAll(syöterivi,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (komento == 196) {
                int tarkenne_ARVO = komento_data.lukea_tavu(), INDEKSI = komento_data.두바이트(); sekki_paikallinen(INDEKSI,paikallinen_LASKE);
                if (tarkenne_ARVO == 21 || tarkenne_ARVO == 25 || tarkenne_ARVO == 54 || tarkenne_ARVO == 58) syöterivi.add((tarkenne_ARVO <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEKSI + 1) + "(%ebp)");
                else if (tarkenne_ARVO == 132) syöterivi.add("addl $" + komento_data.부호두바이트() + ", -" + 4 * (INDEKSI + 1) + "(%ebp)");
                else throw new Käännös_virhe("wide komento 미지원");
            } else if (komento == 198 || komento == 199) {
                int kohde_ARVO = paikka + komento_data.부호두바이트(); haara_luettelo.add(kohde_ARVO); Collections.addAll(syöterivi,"popl %eax","testl %eax, %eax",(komento == 198 ? "je " : "jne ") + merkintä_ARVO + "_b" + kohde_ARVO);
            } else throw new Käännös_virhe("미지원 komento: " + komento);
        }
        if (!경계들.containsAll(haara_luettelo)) throw new Käännös_virhe("komento 경계가 아닌 곳으로 haara");
        syöterivi.add(".size " + merkintä_ARVO + ", .-" + merkintä_ARVO); return String.join("\n",syöterivi);
    }
    String X_86_vakio(Luokka_data data, int INDEKSI) {
        if (data.상수종류[INDEKSI] == 3) return data.vakio_data[INDEKSI].toString();
        if (data.상수종류[INDEKSI] == 8) return merkkijono_symboli(data.문자((Integer)data.vakio_data[INDEKSI]));
        throw new Käännös_virhe("정수와 merkkijono_ARVO 상수만 Tuki_ARVO");
    }
    String X_86_kokoonpano(String aloituskohta, List<String> 내보냄, String tavoite) throws IOException {
        Map<String,String> kone_taulukko = new HashMap<>();
        for (String syöterivi : Files.readAllLines(resurssi_polku.resolve("_86_kone_Funktiot.tsv"))) { String[] muodostaa_pari_ARVO = syöterivi.split("\t"); if (muodostaa_pari_ARVO[0].equals(tavoite)) kone_taulukko.put(muodostaa_pari_ARVO[1] + muodostaa_pari_ARVO[2],muodostaa_pari_ARVO[3]); }
        int sijainti = aloituskohta.lastIndexOf('.'); if (sijainti < 0) throw new Käännös_virhe("aloituskohta Määritä_ARVO VIRHE");
        String omistaja_ARVO = aloituskohta.substring(0,sijainti).replace('.','/'), menetelmä_merkintä_nimi = aloituskohta.substring(sijainti + 1); menetelmä_viite aloituskohta_ARVO = null;
        for (String 서술 : Arrays.asList("()I","()V")) { menetelmä_viite viite = new menetelmä_viite(omistaja_ARVO,menetelmä_merkintä_nimi,서술); if (함수들.containsKey(viite)) { if (aloituskohta_ARVO != null) throw new Käännös_virhe("겹친 aloituskohta"); aloituskohta_ARVO = viite; } }
        if (aloituskohta_ARVO == null || (함수들.get(aloituskohta_ARVO).pääsy_merkintä_68aed533 & 0x100) != 0) throw new Käännös_virhe("aloituskohta_ARVO funktio_ARVO muoto_ARVO VIRHE");
        List<String> syöterivi = new ArrayList<>(); syöterivi.add(".code32");
        for (Luokka_data data : 클래스들.values()) {
            String Tila_ARVO = symboli("state",data.Nimi), alustaa = symboli("init",data.Nimi);
            Collections.addAll(syöterivi,".bss",".balign 4",Tila_ARVO + ": .long 0",".text",alustaa + ":","cmpl $0, " + Tila_ARVO,"jne " + alustaa + "_done","movl $1, " + Tila_ARVO);
            menetelmä_viite 초기화참조 = new menetelmä_viite(data.Nimi,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) syöterivi.add("call " + symboli("method",초기화참조.부분들()));
            Collections.addAll(syöterivi,"movl $2, " + Tila_ARVO,alustaa + "_done:","ret");
            for (jäsen_data kentän_arvo : data.kentän_arvo) {
                byte[] vakio_ARVO = kentän_arvo.määritteen_arvo.get("ConstantValue"); String ARVO = vakio_ARVO == null ? "0" : X_86_vakio(data,new data_Lukija(vakio_ARVO).두바이트());
                Collections.addAll(syöterivi,".data",".balign 4",symboli("field",data.Nimi,kentän_arvo.Nimi,kentän_arvo.서술) + ": .long " + ARVO);
            }
            for (jäsen_data funktio_ARVO : data.funktio_ARVO) if (!funktio_ARVO.Nimi.equals("<init>")) syöterivi.add(X_86_menetelmä_teksti(new menetelmä_viite(data.Nimi,funktio_ARVO.Nimi,funktio_ARVO.서술),funktio_ARVO,kone_taulukko,tavoite));
        }
        Collections.addAll(syöterivi,".text",".globl java_entry","java_entry:","call " + symboli("init",aloituskohta_ARVO.omistaja_ARVO),"call " + symboli("method",aloituskohta_ARVO.부분들()));
        if (aloituskohta_ARVO.서술.equals("()V")) syöterivi.add("xorl %eax, %eax"); syöterivi.add("ret");
        for (String Määritä_ARVO : 내보냄) {
            int erotin_ARVO_d8ba4873 = Määritä_ARVO.indexOf('='); if (erotin_ARVO_d8ba4873 < 1) throw new Käännös_virhe("내보내기 Määritä_ARVO VIRHE");
            String ulkoinen_ARVO = Määritä_ARVO.substring(0,erotin_ARVO_d8ba4873), funktio_ARVO = Määritä_ARVO.substring(erotin_ARVO_d8ba4873 + 1); int jako_KR = funktio_ARVO.lastIndexOf('.');
            if (jako_KR < 0 || !ulkoinen_ARVO.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Käännös_virhe("내보내기 symboli VIRHE");
            String Luokka_ARVO = funktio_ARVO.substring(0,jako_KR).replace('.','/'), Nimi = funktio_ARVO.substring(jako_KR + 1); menetelmä_viite valinta_ARVO = null;
            for (menetelmä_viite viite : 함수들.keySet()) if (viite.omistaja_ARVO.equals(Luokka_ARVO) && viite.Nimi.equals(Nimi)) { if (valinta_ARVO != null) throw new Käännös_virhe("겹친 내보내기 tavoite"); valinta_ARVO = viite; }
            if (valinta_ARVO == null) throw new Käännös_virhe("내보낼 함수가 없음");
            Collections.addAll(syöterivi,".text",".globl " + ulkoinen_ARVO,ulkoinen_ARVO + ":","call " + symboli("init",valinta_ARVO.omistaja_ARVO),"jmp " + symboli("method",valinta_ARVO.부분들()));
        }
        syöterivi.add(".section .rodata");
        for (Map.Entry<String,String> merkintä_ARVO_962f286b : 문자열들.entrySet()) {
            Collections.addAll(syöterivi,".balign 4",merkintä_ARVO_962f286b.getValue() + ":",".long " + merkintä_ARVO_962f286b.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char osio_ARVO_7c611f50 : merkintä_ARVO_962f286b.getKey().toCharArray()) 단위들.add(Integer.toString(osio_ARVO_7c611f50)); if (!단위들.isEmpty()) syöterivi.add(".long " + String.join(",",단위들));
        }
        syöterivi.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",syöterivi) + "\n";
    }
    static void Suorita_työkalu(List<String> komento) throws Exception {
        if (new ProcessBuilder(komento).inheritIO().start().waitFor() != 0) throw new Käännös_virhe("kääntää_lähde VIRHE: " + komento.get(0));
    }
    static String data_merkkijono(String teksti) { return "\"" + teksti.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Käännös(List<Path> syöte_luettelo, String tavoite, String aloituskohta, List<String> 내보냄, Path tulostuspaikka, Path resurssi_ARVO) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Luokka_polku = 임시.resolve("classes"); Files.createDirectory(Luokka_polku);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Luokka_polku.toString(),"-sourcepath",Luokka_polku.toString(),"-d",Luokka_polku.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int lähde_LASKE = 0;
            for (Path syöte_ARVO : syöte_luettelo) {
                if (tulostuspaikka.toAbsolutePath().normalize().equals(syöte_ARVO.toAbsolutePath().normalize())) throw new Käännös_virhe("tulostuspaikka 파일과 입력이 같음");
                if (syöte_ARVO.toString().endsWith(".java")) { 자바명령.add(syöte_ARVO.toString()); lähde_LASKE++; }
                else if (syöte_ARVO.toString().endsWith(".class")) 바이트코드.add(syöte_ARVO);
                else throw new Käännös_virhe(".java 또는 .class만 Tuki_ARVO");
            }
            if (lähde_LASKE > 0) Suorita_työkalu(자바명령);
            try (java.util.stream.Stream<Path> polku_luettelo = Files.walk(Luokka_polku)) { polku_luettelo.filter(polku_2 -> polku_2.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 MUUNNA_ARVO = new 기계어미리번역(바이트코드,tavoite.equals("user") ? "user" : "kernel",262144,resurssi_ARVO);
            String kääntää_ARVO = MUUNNA_ARVO.X_86_kokoonpano(aloituskohta,내보냄,tavoite); Files.writeString(임시.resolve("program.s"),kääntää_ARVO,StandardCharsets.UTF_8);
            Path työkalu_toimi = resurssi_ARVO.getParent();
            Suorita_työkalu(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Suorita_työkalu(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),työkalu_toimi.resolve("CLR_Tuki.s").toString()));
            List<String> Yhdistä = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (tavoite.equals("kernel")) Yhdistä.add("-r");
            else {
                Suorita_työkalu(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),työkalu_toimi.resolve(tavoite.equals("user") ? "alku_käyttäjä_ohjelma.s" : "리눅스시작.s").toString()));
                Collections.addAll(Yhdistä,"-e","_start",임시.resolve("start.o").toString());
                if (tavoite.equals("user")) Collections.addAll(Yhdistä,"-T",työkalu_toimi.resolve("käyttäjä_Linkki_Asettelu.ld").toString());
            }
            Collections.addAll(Yhdistä,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Suorita_työkalu(Yhdistä);
            tulostuspaikka = tulostuspaikka.toAbsolutePath(); Files.createDirectories(tulostuspaikka.getParent()); Path julkaista_ARVO = Files.createTempFile(tulostuspaikka.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),julkaista_ARVO,StandardCopyOption.REPLACE_EXISTING); Files.move(julkaista_ARVO,tulostuspaikka,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(julkaista_ARVO); }
            Files.setPosixFilePermissions(tulostuspaikka,java.nio.file.attribute.PosixFilePermissions.fromString(tavoite.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(tulostuspaikka + ".s"),kääntää_ARVO,StandardCharsets.UTF_8);
            List<String> symboli_data = new ArrayList<>(), lähde_data = new ArrayList<>();
            for (menetelmä_viite viite : MUUNNA_ARVO.함수들.keySet()) symboli_data.add(data_merkkijono(symboli("method",viite.부분들())) + ":" + data_merkkijono(viite.omistaja_ARVO + "." + viite.Nimi + viite.서술));
            for (Path syöte_ARVO : syöte_luettelo) {
                byte[] hajautusarvo_Tiedosto = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(syöte_ARVO)); StringBuilder teksti = new StringBuilder(); for (byte ARVO : hajautusarvo_Tiedosto) teksti.append(String.format(Locale.ROOT,"%02x",ARVO & 255));
                lähde_data.add(data_merkkijono(syöte_ARVO.toAbsolutePath().toString()) + ":" + data_merkkijono(teksti.toString()));
            }
            Files.writeString(Paths.get(tulostuspaikka + ".json"),"{\"target\":" + data_merkkijono(tavoite) + ",\"entry\":" + data_merkkijono(aloituskohta) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symboli_data) + "},\"sources\":{" + String.join(",",lähde_data) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> polku_luettelo = Files.walk(임시)) { for (Path polku_2 : (Iterable<Path>)polku_luettelo.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(polku_2); }
        }
    }
    public static void main(String[] argumentit) {
        try {
            String aloituskohta = null, tavoite = "kernel", X_86_kohde = null; Path tulos_polku = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> polku_luettelo = new ArrayList<>();
            for (int 순번 = 0; 순번 < argumentit.length; 순번++) {
                String ARVO = argumentit[순번];
                switch (ARVO) {
                    case "--target": X_86_kohde = argumentit[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Luokka_ARVO.funktio_ARVO -o tulostuspaikka [--target linux|kernel|user] [--profile kernel|user] [--export symboli=Luokka_ARVO.funktio_ARVO] 클래스파일 또는 Java원문"); return;
                    case "--entry": aloituskohta = argumentit[++순번]; break;
                    case "--profile": tavoite = argumentit[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(argumentit[++순번]); break;
                    case "--export": 내보냄.add(argumentit[++순번]); break;
                    case "-o": tulos_polku = Paths.get(argumentit[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (ARVO.startsWith("-")) throw new Käännös_virhe("알 numero 없는 옵션: " + ARVO); polku_luettelo.add(Paths.get(ARVO));
                }
            }
            if (aloituskohta == null || tulos_polku == null || polku_luettelo.isEmpty()) throw new Käännös_virhe("--entry, -o, Luokka_ARVO 파일이 필요합니다");
            Path resurssi_ARVO = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_kohde != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_kohde)) throw new Käännös_virhe("알 numero 없는 Suorita_komento tavoite");
                X_86_Käännös(polku_luettelo,X_86_kohde,aloituskohta,내보냄,tulos_polku,resurssi_ARVO); return;
            }
            String lähdetiedosto = new 기계어미리번역(polku_luettelo, tavoite, 낱말수, resurssi_ARVO).generoida(aloituskohta, 내보냄, 범용표기);
            tulos_polku = tulos_polku.toAbsolutePath(); Files.createDirectories(tulos_polku.getParent());
            Path 임시 = Files.createTempFile(tulos_polku.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, lähdetiedosto, StandardCharsets.UTF_8); Files.move(임시, tulos_polku, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception VIRHE) { System.err.println("kääntää_lähde VIRHE: " + VIRHE.getMessage()); System.exit(1); }
    }
}
