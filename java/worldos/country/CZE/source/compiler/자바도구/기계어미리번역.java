// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Třída_HODNOTA 파일에서 독립 ARM64 커널용 C 원문을 만든다. hostit JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class převod_chyba extends RuntimeException {
        převod_chyba(String 설명) { super(설명); }
    }
    static final class data_Čtenář {
        final byte[] data;
        int pozice;
        data_Čtenář(byte[] vstup_data) { data = vstup_data; }
        byte[] Čtení(int délka_HODNOTA) {
            if (délka_HODNOTA < 0 || délka_HODNOTA > data.length - pozice) throw new převod_chyba("잘린 Třída_HODNOTA 또는 příkaz data");
            byte[] VÝSLEDEK = Arrays.copyOfRange(data, pozice, pozice + délka_HODNOTA); pozice += délka_HODNOTA; return VÝSLEDEK;
        }
        int 한바이트() { if (pozice >= data.length) throw new převod_chyba("잘린 příkaz data"); return data[pozice++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class člen_data {
        final int přístup_položka;
        final String Název, 서술;
        final Map<String, byte[]> hodnota_atributu;
        člen_data(int přístup_HODNOTA, String název_HODNOTA, String popisovač_data, Map<String, byte[]> atribut_data) {
            přístup_položka = přístup_HODNOTA; Název = název_HODNOTA; 서술 = popisovač_data; hodnota_atributu = atribut_data;
        }
    }
    static final class metoda_odkaz implements Comparable<metoda_odkaz> {
        final String vlastník_HODNOTA, Název, 서술;
        metoda_odkaz(String 소유값, String název_HODNOTA, String popisovač_data) { vlastník_HODNOTA = 소유값; Název = název_HODNOTA; 서술 = popisovač_data; }
        String[] 부분들() { return new String[]{vlastník_HODNOTA, Název, 서술}; }
        public int compareTo(metoda_odkaz partner_HODNOTA) {
            int Porovnání_HODNOTA = vlastník_HODNOTA.compareTo(partner_HODNOTA.vlastník_HODNOTA);
            if (Porovnání_HODNOTA == 0) Porovnání_HODNOTA = Název.compareTo(partner_HODNOTA.Název);
            return Porovnání_HODNOTA == 0 ? 서술.compareTo(partner_HODNOTA.서술) : Porovnání_HODNOTA;
        }
        public boolean equals(Object partner_HODNOTA) { return partner_HODNOTA instanceof metoda_odkaz && compareTo((metoda_odkaz) partner_HODNOTA) == 0; }
        public int hashCode() { return Objects.hash(vlastník_HODNOTA, Název, 서술); }
    }
    static final class Třída_data {
        final int[] konstanta_Druh;
        final Object[] konstanta_data;
        final String Název;
        final List<člen_data> hodnota_pole, funkce_HODNOTA;
        Třída_data(Path cesta_2) throws IOException {
            data_Čtenář Čtenář_HODNOTA = new data_Čtenář(Files.readAllBytes(cesta_2));
            if (Čtenář_HODNOTA.네바이트() != 0xcafebabe) throw new převod_chyba("Java Třída_HODNOTA 표식이 아님");
            Čtenář_HODNOTA.Čtení(4);
            int zboží_POČET = Čtenář_HODNOTA.두바이트(); konstanta_Druh = new int[zboží_POČET]; konstanta_data = new Object[zboží_POČET];
            for (int 순번 = 1; 순번 < zboží_POČET; 순번++) {
                int Druh_HODNOTA = Čtenář_HODNOTA.한바이트(); konstanta_Druh[순번] = Druh_HODNOTA;
                switch (Druh_HODNOTA) {
                    case 1:
                        int délka_HODNOTA = Čtenář_HODNOTA.두바이트();
                        byte[] znak_zásobník = Čtenář_HODNOTA.Čtení(délka_HODNOTA), 길이붙인자료 = new byte[délka_HODNOTA + 2];
                        길이붙인자료[0] = (byte)(délka_HODNOTA >> 8); 길이붙인자료[1] = (byte)délka_HODNOTA;
                        System.arraycopy(znak_zásobník, 0, 길이붙인자료, 2, délka_HODNOTA);
                        konstanta_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstanta_data[순번] = Čtenář_HODNOTA.네바이트(); break;
                    case 4: Čtenář_HODNOTA.Čtení(4); break;
                    case 5: case 6: Čtenář_HODNOTA.Čtení(8); 순번++; break;
                    case 7: case 8: case 16: konstanta_data[순번] = Čtenář_HODNOTA.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstanta_data[순번] = new int[]{Čtenář_HODNOTA.두바이트(), Čtenář_HODNOTA.두바이트()}; break;
                    case 15: konstanta_data[순번] = new int[]{Čtenář_HODNOTA.한바이트(), Čtenář_HODNOTA.두바이트()}; break;
                    default: throw new převod_chyba("지원하지 않는 konstanta_HODNOTA Druh_HODNOTA: " + Druh_HODNOTA);
                }
            }
            Čtenář_HODNOTA.두바이트(); Název = název_třídy(Čtenář_HODNOTA.두바이트());
            if (!název_třídy(Čtenář_HODNOTA.두바이트()).equals("java/lang/Object") || Čtenář_HODNOTA.두바이트() != 0)
                throw new převod_chyba(Název + ": 상속 및 인터페이스 미지원");
            hodnota_pole = 멤버읽기(Čtenář_HODNOTA); funkce_HODNOTA = 멤버읽기(Čtenář_HODNOTA); 속성읽기(Čtenář_HODNOTA);
            if (Čtenář_HODNOTA.pozice != Čtenář_HODNOTA.data.length) throw new převod_chyba("Třída_HODNOTA 뒤에 남은 data");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= konstanta_Druh.length || konstanta_Druh[INDEX] != 1) throw new převod_chyba("문자 konstanta_HODNOTA INDEX chyba");
            return (String) konstanta_data[INDEX];
        }
        String název_třídy(int INDEX) {
            if (INDEX < 1 || INDEX >= konstanta_Druh.length || konstanta_Druh[INDEX] != 7) throw new převod_chyba("Třída_HODNOTA odkaz chyba");
            return 문자((Integer)konstanta_data[INDEX]);
        }
        metoda_odkaz odkaz(int INDEX) {
            if (INDEX < 1 || INDEX >= konstanta_Druh.length || konstanta_Druh[INDEX] < 9 || konstanta_Druh[INDEX] > 11) throw new převod_chyba("멤버 odkaz chyba");
            int[] spárovat_HODNOTA = (int[])konstanta_data[INDEX], název_spárovat = (int[])konstanta_data[spárovat_HODNOTA[1]];
            return new metoda_odkaz(název_třídy(spárovat_HODNOTA[0]), 문자(název_spárovat[0]), 문자(název_spárovat[1]));
        }
        Map<String, byte[]> 속성읽기(data_Čtenář Čtenář_HODNOTA) {
            Map<String, byte[]> VÝSLEDEK = new LinkedHashMap<>();
            int zboží_POČET = Čtenář_HODNOTA.두바이트();
            for (int 순번 = 0; 순번 < zboží_POČET; 순번++) {
                String atribut_název = 문자(Čtenář_HODNOTA.두바이트()); byte[] HODNOTA = Čtenář_HODNOTA.Čtení(Čtenář_HODNOTA.네바이트());
                if (VÝSLEDEK.put(atribut_název, HODNOTA) != null) throw new převod_chyba("겹친 hodnota_atributu: " + atribut_název);
            }
            return VÝSLEDEK;
        }
        List<člen_data> 멤버읽기(data_Čtenář Čtenář_HODNOTA) {
            List<člen_data> VÝSLEDEK = new ArrayList<>(); int zboží_POČET = Čtenář_HODNOTA.두바이트();
            for (int 순번 = 0; 순번 < zboží_POČET; 순번++) {
                int přístup_položka = Čtenář_HODNOTA.두바이트(); String metoda_položka_název = 문자(Čtenář_HODNOTA.두바이트()), 서술 = 문자(Čtenář_HODNOTA.두바이트());
                VÝSLEDEK.add(new člen_data(přístup_položka, metoda_položka_název, 서술, 속성읽기(Čtenář_HODNOTA)));
            }
            return VÝSLEDEK;
        }
    }
    static final class metoda_popisovač {
        final List<String> argumenty = new ArrayList<>();
        final String Vratka_KV;
        metoda_popisovač(String 서술) {
            if (!서술.startsWith("(")) throw new převod_chyba("funkce_HODNOTA 서술 chyba: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new převod_chyba("funkce_HODNOTA 서술 chyba: " + 서술);
            argumenty.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (argumenty.contains("V") || 반환들.size() != 1) throw new převod_chyba("funkce_HODNOTA 서술 chyba: " + 서술);
            Vratka_KV = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> VÝSLEDEK = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int pozice = 0; pozice < 서술.length();) {
            String výběr_HODNOTA = null;
            for (String formát_HODNOTA : 허용형식) if (서술.startsWith(formát_HODNOTA, pozice)) { výběr_HODNOTA = formát_HODNOTA; break; }
            if (výběr_HODNOTA == null) throw new převod_chyba("지원하지 않는 datový_typ: " + 서술);
            VÝSLEDEK.add(výběr_HODNOTA); pozice += výběr_HODNOTA.length();
        }
        return VÝSLEDEK;
    }
    static String symbol(String Druh_HODNOTA, String... 부분들) {
        try {
            byte[] hodnota_hash_Soubor = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder text = new StringBuilder("j_" + Druh_HODNOTA + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) text.append(String.format(Locale.ROOT, "%02x", hodnota_hash_Soubor[순번] & 255));
            return text.toString();
        } catch (Exception chyba) { throw new převod_chyba(chyba.toString()); }
    }
    final Map<String, Třída_data> 클래스들 = new TreeMap<>();
    final Map<metoda_odkaz, člen_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), počítač_Functions_c3a8e64a = new LinkedHashMap<>();
    final String spuštění_cíl, počítač_Třída;
    final int halda_počet_slov;
    final Path zdroj_cesta;
    기계어미리번역(List<Path> cesta_Seznam, String cílová_úroveň, int 낱말수, Path zdroj_HODNOTA) throws IOException {
        if ((!cílová_úroveň.equals("kernel") && !cílová_úroveň.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new převod_chyba("Provést_příkaz cílová_úroveň 또는 Paměť_HODNOTA ODKAZ_oblast Velikost chyba");
        spuštění_cíl = cílová_úroveň; halda_počet_slov = 낱말수; zdroj_cesta = zdroj_HODNOTA;
        // 이 이름도 국가별 zdroj_strom generovat 시 해당 언어로 옮긴다.
        počítač_Třída = cílová_úroveň.equals("kernel") ? "Panel" : "uživatelský_prostor";
        for (String vstupní_řádek : Files.readAllLines(zdroj_HODNOTA.resolve("počítač_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = vstupní_řádek.split("\t", -1);
            if (부분들.length != 4) throw new převod_chyba("počítač funkce_HODNOTA data chyba");
            if (부분들[0].equals(cílová_úroveň)) počítač_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path cesta_2 : cesta_Seznam) {
            Třída_data data = new Třída_data(cesta_2);
            if (클래스들.put(data.Název, data) != null) throw new převod_chyba("중복 Třída_HODNOTA: " + data.Název);
            for (člen_data hodnota_pole : data.hodnota_pole) {
                if ((hodnota_pole.přístup_položka & 8) == 0 || 형식읽기(hodnota_pole.서술).equals(Collections.singletonList("V"))) throw new převod_chyba("statický_HODNOTA 필드만 vzpěra_HODNOTA");
                if (필드들.put(new metoda_odkaz(data.Název, hodnota_pole.Název, hodnota_pole.서술), hodnota_pole) != null) throw new převod_chyba("중복 hodnota_pole");
            }
            for (člen_data funkce_HODNOTA : data.funkce_HODNOTA) {
                if (funkce_HODNOTA.Název.equals("<init>")) continue;
                if ((funkce_HODNOTA.přístup_položka & 8) == 0 || (funkce_HODNOTA.přístup_položka & (0x20 | 0x400)) != 0) throw new převod_chyba("statický_HODNOTA 비동기화 함수만 vzpěra_HODNOTA");
                new metoda_popisovač(funkce_HODNOTA.서술);
                if (함수들.put(new metoda_odkaz(data.Název, funkce_HODNOTA.Název, funkce_HODNOTA.서술), funkce_HODNOTA) != null) throw new převod_chyba("중복 funkce_HODNOTA");
            }
        }
    }
    String řetězec_symbol(String text) { return 문자열들.computeIfAbsent(text, HODNOTA -> "j_text_" + 문자열들.size()); }
    String konstanta_výraz(Třída_data data, int INDEX) {
        if (INDEX < 1 || INDEX >= data.konstanta_Druh.length) throw new převod_chyba("konstanta_HODNOTA INDEX oříznout chyba");
        if (data.konstanta_Druh[INDEX] == 3) return "(word)(uint32_t)(" + data.konstanta_data[INDEX] + ")";
        if (data.konstanta_Druh[INDEX] == 8) return "(word)" + řetězec_symbol(data.문자((Integer)data.konstanta_data[INDEX]));
        throw new převod_chyba("정수와 řetězec_HODNOTA 상수만 vzpěra_HODNOTA");
    }
    String metoda_prototyp(metoda_odkaz odkaz) {
        List<String> 인수들 = new ArrayList<>(); int zboží_POČET = new metoda_popisovač(odkaz.서술).argumenty.size();
        for (int 순번 = 0; 순번 < zboží_POČET; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symbol("method", odkaz.부분들()) + "(" + (zboží_POČET == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void šek_místní(int INDEX, int místní_proměnná_POČET) { if (INDEX < 0 || INDEX >= místní_proměnná_POČET) throw new převod_chyba("místní_obor proměnná_HODNOTA INDEX oříznout chyba"); }
    void 분기넣기(List<String> výstupní_pozice, Set<Integer> větev_Seznam, int pozice, int 이동량, String podmínka) {
        int cíl_HODNOTA = pozice + 이동량; větev_Seznam.add(cíl_HODNOTA);
        výstupní_pozice.add((podmínka == null ? "" : "if (" + podmínka + ") ") + "goto b" + cíl_HODNOTA + ";");
    }
    String tělo_metody(metoda_odkaz funkce_HODNOTA, člen_data data) {
        byte[] text_zprávy_data = data.hodnota_atributu.get("Code"); if (text_zprávy_data == null) throw new převod_chyba("funkce_HODNOTA 몸체가 없음: " + funkce_HODNOTA.Název);
        data_Čtenář Čtenář_HODNOTA = new data_Čtenář(text_zprávy_data); int 쌓임깊이 = Čtenář_HODNOTA.두바이트(), místní_proměnná_POČET = Čtenář_HODNOTA.두바이트();
        data_Čtenář příkaz_data = new data_Čtenář(Čtenář_HODNOTA.Čtení(Čtenář_HODNOTA.네바이트()));
        if (Čtenář_HODNOTA.두바이트() != 0) throw new převod_chyba("try/catch/finally 미지원");
        metoda_popisovač formát_HODNOTA = new metoda_popisovač(funkce_HODNOTA.서술); if (místní_proměnná_POČET < formát_HODNOTA.argumenty.size()) throw new převod_chyba("매개변수보다 적은 místní_obor proměnná_HODNOTA");
        Třída_data Třída_HODNOTA = 클래스들.get(funkce_HODNOTA.vlastník_HODNOTA);
        List<String> výstupní_pozice = new ArrayList<>(); výstupní_pozice.add(metoda_prototyp(funkce_HODNOTA) + " {");
        výstupní_pozice.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(místní_proměnná_POČET, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formát_HODNOTA.argumenty.size(); 순번++) výstupní_pozice.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), větev_Seznam = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (příkaz_data.pozice < příkaz_data.data.length) {
            int pozice = příkaz_data.pozice, příkaz = příkaz_data.한바이트(); 경계들.add(pozice); výstupní_pozice.add("b" + pozice + ":;");
            if (příkaz == 0) continue;
            if (příkaz == 1) výstupní_pozice.add("PUSH(0);");
            else if (příkaz >= 2 && příkaz <= 8) výstupní_pozice.add("PUSH((uint32_t)(" + (příkaz - 3) + "));");
            else if (příkaz == 16 || příkaz == 17) výstupní_pozice.add("PUSH((uint32_t)(" + (příkaz == 16 ? příkaz_data.부호한바이트() : příkaz_data.부호두바이트()) + "));");
            else if (příkaz == 18 || příkaz == 19) výstupní_pozice.add("PUSH(" + konstanta_výraz(Třída_HODNOTA, příkaz == 18 ? příkaz_data.한바이트() : příkaz_data.두바이트()) + ");");
            else if (příkaz == 21 || příkaz == 25 || (příkaz >= 26 && příkaz <= 29) || (příkaz >= 42 && příkaz <= 45)) {
                int INDEX = příkaz == 21 || příkaz == 25 ? příkaz_data.한바이트() : příkaz - (příkaz <= 29 ? 26 : 42);
                šek_místní(INDEX, místní_proměnná_POČET); výstupní_pozice.add("PUSH(l[" + INDEX + "]);");
            } else if (příkaz == 54 || příkaz == 58 || (příkaz >= 59 && příkaz <= 62) || (příkaz >= 75 && příkaz <= 78)) {
                int INDEX = příkaz == 54 || příkaz == 58 ? příkaz_data.한바이트() : příkaz - (příkaz <= 62 ? 59 : 75);
                šek_místní(INDEX, místní_proměnná_POČET); výstupní_pozice.add("l[" + INDEX + "] = POP();");
            } else if (příkaz == 46) výstupní_pozice.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (příkaz == 79) výstupní_pozice.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (příkaz == 87 || příkaz == 88) výstupní_pozice.add(příkaz == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (příkaz >= 89 && příkaz <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] pořadí_Seznam = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[příkaz - 89]; 순번++) výstupní_pozice.add("abcd".charAt(순번) + " = POP();");
                for (char HODNOTA : pořadí_Seznam[příkaz - 89].toCharArray()) výstupní_pozice.add("PUSH(" + HODNOTA + ");");
            } else if (příkaz == 96 || příkaz == 100 || příkaz == 104 || příkaz == 126 || příkaz == 128 || příkaz == 130) {
                String operace_HODNOTA = příkaz == 96 ? "+" : příkaz == 100 ? "-" : příkaz == 104 ? "*" : příkaz == 126 ? "&" : příkaz == 128 ? "|" : "^";
                výstupní_pozice.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operace_HODNOTA + " (uint32_t)b);");
            } else if (příkaz == 108 || příkaz == 112) výstupní_pozice.add("b = POP(); a = POP(); PUSH(divide(a,b," + (příkaz == 112 ? 1 : 0) + "));");
            else if (příkaz == 116) výstupní_pozice.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (příkaz == 120 || příkaz == 122 || příkaz == 124) {
                výstupní_pozice.add("b = POP(); a = POP();"); výstupní_pozice.add("PUSH(" + (příkaz == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (příkaz == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (příkaz == 132) {
                int INDEX = příkaz_data.한바이트(), 증가량 = příkaz_data.부호한바이트(); šek_místní(INDEX, místní_proměnná_POČET);
                výstupní_pozice.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (příkaz >= 145 && příkaz <= 147) výstupní_pozice.add("a = POP(); PUSH((uint32_t)(" + (příkaz == 145 ? "int8_t" : příkaz == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (příkaz >= 153 && příkaz <= 158) {
                výstupní_pozice.add("a = POP();"); 분기넣기(výstupní_pozice, větev_Seznam, pozice, příkaz_data.부호두바이트(), "(int32_t)a " + 비교들[příkaz - 153] + " 0");
            } else if (příkaz >= 159 && příkaz <= 166) {
                výstupní_pozice.add("b = POP(); a = POP();"); 분기넣기(výstupní_pozice, větev_Seznam, pozice, příkaz_data.부호두바이트(), příkaz >= 165 ? "a " + 비교들[příkaz - 159] + " b" : "(int32_t)a " + 비교들[příkaz - 159] + " (int32_t)b");
            } else if (příkaz == 167 || příkaz == 200) 분기넣기(výstupní_pozice, větev_Seznam, pozice, příkaz == 167 ? příkaz_data.부호두바이트() : příkaz_data.네바이트(), null);
            else if (příkaz == 170 || příkaz == 171) {
                while (příkaz_data.pozice % 4 != 0) příkaz_data.한바이트();
                int výchozí_hodnota = příkaz_data.네바이트(); výstupní_pozice.add("a = POP();");
                if (příkaz == 170) {
                    int 아래 = příkaz_data.네바이트(), 위 = příkaz_data.네바이트(); long zboží_POČET = (long)위 - 아래 + 1;
                    if (zboží_POČET < 1 || zboží_POČET > (příkaz_data.data.length - příkaz_data.pozice) / 4) throw new převod_chyba("switch oříznout chyba");
                    for (long HODNOTA = 아래; HODNOTA <= 위; HODNOTA++) 분기넣기(výstupní_pozice, větev_Seznam, pozice, příkaz_data.네바이트(), "(int32_t)a == (" + HODNOTA + ")");
                } else {
                    int zboží_POČET = příkaz_data.네바이트(), přední_fotoaparát_data = 0;
                    if (zboží_POČET < 0 || zboží_POČET > (příkaz_data.data.length - příkaz_data.pozice) / 8) throw new převod_chyba("switch Velikost chyba");
                    for (int 순번 = 0; 순번 < zboží_POČET; 순번++) {
                        int HODNOTA = příkaz_data.네바이트(); if (순번 > 0 && HODNOTA <= přední_fotoaparát_data) throw new převod_chyba("switch pořadí_HODNOTA chyba"); přední_fotoaparát_data = HODNOTA;
                        분기넣기(výstupní_pozice, větev_Seznam, pozice, příkaz_data.네바이트(), "(int32_t)a == (" + HODNOTA + ")");
                    }
                }
                분기넣기(výstupní_pozice, větev_Seznam, pozice, výchozí_hodnota, null);
            } else if (příkaz == 172 || příkaz == 176 || příkaz == 177) výstupní_pozice.add("return " + (příkaz == 177 ? "0" : "POP()") + ";");
            else if (příkaz == 178 || příkaz == 179) {
                metoda_odkaz odkaz = Třída_HODNOTA.odkaz(příkaz_data.두바이트()); if (!필드들.containsKey(odkaz)) throw new převod_chyba("알 číslo 없는 hodnota_pole");
                výstupní_pozice.add(symbol("init", odkaz.vlastník_HODNOTA) + "();"); String hodnota_pole = symbol("field", odkaz.부분들());
                výstupní_pozice.add(příkaz == 178 ? "PUSH(" + hodnota_pole + ");" : hodnota_pole + " = POP();");
            } else if (příkaz == 184) {
                metoda_odkaz odkaz = Třída_HODNOTA.odkaz(příkaz_data.두바이트()); if (!함수들.containsKey(odkaz)) throw new převod_chyba("알 číslo 없는 funkce_HODNOTA");
                metoda_popisovač 호출형식 = new metoda_popisovač(odkaz.서술); int zboží_POČET = 호출형식.argumenty.size();
                výstupní_pozice.add(symbol("init", odkaz.vlastník_HODNOTA) + "();"); výstupní_pozice.add("if(sp < " + zboží_POČET + ") kernel_panic(\"call stack underflow\"); sp -= " + zboží_POČET + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < zboží_POČET; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                výstupní_pozice.add("a = " + symbol("method", odkaz.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.Vratka_KV.equals("V")) výstupní_pozice.add("PUSH(a);");
            } else if (příkaz == 182) {
                metoda_odkaz odkaz = Třída_HODNOTA.odkaz(příkaz_data.두바이트());
                if (odkaz.equals(new metoda_odkaz("java/lang/String", "length", "()I"))) výstupní_pozice.add("a = POP(); PUSH(length(a));");
                else if (odkaz.equals(new metoda_odkaz("java/lang/String", "charAt", "(I)C"))) výstupní_pozice.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new převod_chyba("가상 funkce_HODNOTA 호출 미지원");
            } else if (příkaz == 188) {
                if (příkaz_data.한바이트() != 10) throw new převod_chyba("new int[]만 vzpěra_HODNOTA"); výstupní_pozice.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (příkaz == 190) výstupní_pozice.add("a = POP(); PUSH(length(a));");
            else if (příkaz == 196) {
                int přípona_HODNOTA = příkaz_data.한바이트(), INDEX = příkaz_data.두바이트(); šek_místní(INDEX, místní_proměnná_POČET);
                if (přípona_HODNOTA == 21 || přípona_HODNOTA == 25) výstupní_pozice.add("PUSH(l[" + INDEX + "]);");
                else if (přípona_HODNOTA == 54 || přípona_HODNOTA == 58) výstupní_pozice.add("l[" + INDEX + "] = POP();");
                else if (přípona_HODNOTA == 132) výstupní_pozice.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + příkaz_data.부호두바이트() + ");");
                else throw new převod_chyba("미지원 wide příkaz");
            } else if (příkaz == 198 || příkaz == 199) {
                výstupní_pozice.add("a = POP();"); 분기넣기(výstupní_pozice, větev_Seznam, pozice, příkaz_data.부호두바이트(), "a " + (příkaz == 198 ? "==" : "!=") + " 0");
            } else throw new převod_chyba(funkce_HODNOTA.vlastník_HODNOTA + "." + funkce_HODNOTA.Název + ", bajt_HODNOTA " + pozice + ": 미지원 příkaz " + příkaz);
        }
        if (!경계들.containsAll(větev_Seznam)) throw new převod_chyba("příkaz 경계가 아닌 곳으로 větev");
        výstupní_pozice.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", výstupní_pozice);
    }
    String exportovat_metoda(String Odkaz_symbol, String cílová_úroveň, boolean 진입점여부) {
        int poziční_index = cílová_úroveň.lastIndexOf('.'); if (poziční_index < 0 || !Odkaz_symbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new převod_chyba("내보내기 Přiřadit_HODNOTA chyba");
        String vlastník_HODNOTA = cílová_úroveň.substring(0, poziční_index).replace('.', '/'), Název = cílová_úroveň.substring(poziční_index + 1); metoda_odkaz výběr_HODNOTA = null;
        for (metoda_odkaz odkaz : 함수들.keySet()) if (odkaz.vlastník_HODNOTA.equals(vlastník_HODNOTA) && odkaz.Název.equals(Název)) {
            if (výběr_HODNOTA != null) throw new převod_chyba("겹친 내보내기 cílová_úroveň"); výběr_HODNOTA = odkaz;
        }
        if (výběr_HODNOTA == null || (함수들.get(výběr_HODNOTA).přístup_položka & 0x100) != 0) throw new převod_chyba("내보낼 함수가 없음 또는 native funkce_HODNOTA");
        metoda_popisovač formát_HODNOTA = new metoda_popisovač(výběr_HODNOTA.서술);
        if ((진입점여부 && !formát_HODNOTA.argumenty.isEmpty()) || !Arrays.asList("V", "I").contains(formát_HODNOTA.Vratka_KV)) throw new převod_chyba("vstupní_bod_HODNOTA 또는 C mez_HODNOTA formát_HODNOTA chyba");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formát_HODNOTA.argumenty.size(); 순번++) {
            if (!formát_HODNOTA.argumenty.get(순번).equals("I")) throw new převod_chyba("C 경계는 int 인수만 vzpěra_HODNOTA");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formát_HODNOTA.Vratka_KV.equals("V") ? "void " : "int32_t ") + Odkaz_symbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symbol("init", výběr_HODNOTA.vlastník_HODNOTA) + "(); " + (formát_HODNOTA.Vratka_KV.equals("V") ? "" : "return (int32_t)") + symbol("method", výběr_HODNOTA.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generovat(String vstupní_bod, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metoda_odkaz, člen_data> položka_HODNOTA : 함수들.entrySet()) {
            metoda_odkaz odkaz = položka_HODNOTA.getKey(); člen_data data = položka_HODNOTA.getValue(); 선언들.add(metoda_prototyp(odkaz) + ";");
            if ((data.přístup_položka & 0x100) != 0) {
                String Připojit = počítač_Functions_c3a8e64a.get(odkaz.Název + odkaz.서술);
                if (!odkaz.vlastník_HODNOTA.equals(počítač_Třída) || Připojit == null) throw new převod_chyba("허용되지 않은 native funkce_HODNOTA: " + odkaz.Název);
                int zboží_POČET = new metoda_popisovač(odkaz.서술).argumenty.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < zboží_POČET; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Připojit + "(" + (zboží_POČET == 0 ? "void" : String.join(",", Collections.nCopies(zboží_POČET, "word"))) + ");");
                몸체들.add(metoda_prototyp(odkaz) + " { return " + Připojit + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(tělo_metody(odkaz, data));
        }
        for (Map.Entry<metoda_odkaz, člen_data> položka_HODNOTA : 필드들.entrySet()) {
            metoda_odkaz odkaz = položka_HODNOTA.getKey(); byte[] konstanta_HODNOTA = položka_HODNOTA.getValue().hodnota_atributu.get("ConstantValue");
            String HODNOTA = konstanta_HODNOTA == null ? "0" : konstanta_výraz(클래스들.get(odkaz.vlastník_HODNOTA), new data_Čtenář(konstanta_HODNOTA).두바이트());
            필드선언들.add("static word " + symbol("field", odkaz.부분들()) + " = " + HODNOTA + ";");
        }
        for (String Název : 클래스들.keySet()) {
            String inicializovat = symbol("init", Název), Stav_HODNOTA = symbol("state", Název);
            선언들.add("static void " + inicializovat + "(void);"); 필드선언들.add("static unsigned " + Stav_HODNOTA + ";");
            metoda_odkaz odkaz = new metoda_odkaz(Název, "<clinit>", "()V");
            몸체들.add("static void " + inicializovat + "(void) { if(" + Stav_HODNOTA + ") return; " + Stav_HODNOTA + " = 1; " + (함수들.containsKey(odkaz) ? symbol("method", odkaz.부분들()) + "(); " : "") + Stav_HODNOTA + " = 2; }");
        }
        몸체들.add(exportovat_metoda("java_entry", vstupní_bod, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Přiřadit_HODNOTA : 내보내기목록) {
            int poziční_index = Přiřadit_HODNOTA.indexOf('='); if (poziční_index < 1) throw new převod_chyba("내보내기 Přiřadit_HODNOTA chyba");
            String Název = Přiřadit_HODNOTA.substring(0, poziční_index); 공개이름.add(Název); 몸체들.add(exportovat_metoda(Název, Přiřadit_HODNOTA.substring(poziční_index + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> položka_HODNOTA : 문자열들.entrySet()) {
            String text = položka_HODNOTA.getKey(); StringBuilder pole_HODNOTA = new StringBuilder("static const word " + položka_HODNOTA.getValue() + "[] = {" + text.length());
            for (int 순번 = 0; 순번 < text.length(); 순번++) pole_HODNOTA.append(", ").append((int)text.charAt(순번));
            문자열선언들.add(pole_HODNOTA.append("};").toString());
        }
        String vzpěra_HODNOTA = Files.readString(zdroj_cesta.resolve("CLR_vzpěra.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(halda_počet_slov));
        return 기계원문한국어화(vzpěra_HODNOTA + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String zdrojový_soubor, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> název_tabulka = new HashMap<>();
        for (String vstupní_řádek : Files.readAllLines(zdroj_cesta.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] spárovat_HODNOTA = vstupní_řádek.split("\t"); název_tabulka.put(spárovat_HODNOTA[0], spárovat_HODNOTA[1]);
        }
        Pattern blok_dat_výraz = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = blok_dat_výraz.matcher(zdrojový_soubor); StringBuffer VÝSLEDEK = new StringBuffer();
        while (찾개.find()) {
            String Název = 찾개.group(), 새이름 = Název;
            if (!Název.startsWith("//") && !Název.startsWith("/*") && !Název.startsWith("\"") && !Název.startsWith("'") && !공개이름.contains(Název)) {
                새이름 = název_tabulka.getOrDefault(Název, Název);
                if (Název.matches("a[0-9]+")) 새이름 = "argumenty" + Název.substring(1);
                if (Název.matches("b[0-9]+")) 새이름 = "větev" + Název.substring(1);
                if (범용표기) {
                    StringBuilder notace_HODNOTA = new StringBuilder();
                    for (char znak_HODNOTA : 새이름.toCharArray()) notace_HODNOTA.append(znak_HODNOTA < 128 ? Character.toString(znak_HODNOTA) : String.format(Locale.ROOT, "\\u%04x", (int)znak_HODNOTA));
                    새이름 = notace_HODNOTA.toString();
                }
            }
            찾개.appendReplacement(VÝSLEDEK, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(VÝSLEDEK); return VÝSLEDEK.toString();
    }
    String X_86_tělo_metody(metoda_odkaz funkce_HODNOTA, člen_data data, Map<String,String> počítač_tabulka, String cílová_úroveň) {
        String značka_HODNOTA_7e8f90bd = symbol("method", funkce_HODNOTA.부분들());
        List<String> vstupní_řádek = new ArrayList<>();
        if ((data.přístup_položka & 0x100) != 0) {
            String Připojit = počítač_tabulka.get(funkce_HODNOTA.Název + funkce_HODNOTA.서술);
            if (!funkce_HODNOTA.vlastník_HODNOTA.equals(cílová_úroveň.equals("kernel") ? "mobilní_HODNOTA" : "uživatelský_prostor") || Připojit == null) throw new převod_chyba("허용되지 않은 native funkce_HODNOTA");
            return ".text\n" + značka_HODNOTA_7e8f90bd + ":\njmp " + Připojit;
        }
        byte[] základní_text = data.hodnota_atributu.get("Code"); if (základní_text == null) throw new převod_chyba("funkce_HODNOTA 몸체가 없음");
        data_Čtenář Čtenář_HODNOTA = new data_Čtenář(základní_text); Čtenář_HODNOTA.두바이트(); int místní_POČET = Čtenář_HODNOTA.두바이트();
        data_Čtenář příkaz_data = new data_Čtenář(Čtenář_HODNOTA.Čtení(Čtenář_HODNOTA.네바이트()));
        if (Čtenář_HODNOTA.두바이트() != 0) throw new převod_chyba("try/catch/finally 미지원");
        metoda_popisovač formát_HODNOTA = new metoda_popisovač(funkce_HODNOTA.서술); if (místní_POČET < formát_HODNOTA.argumenty.size()) throw new převod_chyba("매개변수보다 적은 místní_obor proměnná_HODNOTA");
        Collections.addAll(vstupní_řádek,".text",".globl " + značka_HODNOTA_7e8f90bd,".type " + značka_HODNOTA_7e8f90bd + ", @function",značka_HODNOTA_7e8f90bd + ":","pushl %ebp","movl %esp, %ebp","subl $" + místní_POČET * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formát_HODNOTA.argumenty.size(); 순번++) Collections.addAll(vstupní_řádek,"movl " + (8 + 4 * (formát_HODNOTA.argumenty.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Třída_data Třída_HODNOTA = 클래스들.get(funkce_HODNOTA.vlastník_HODNOTA); Set<Integer> 경계들 = new HashSet<>(), větev_Seznam = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (příkaz_data.pozice < příkaz_data.data.length) {
            int pozice = příkaz_data.pozice, příkaz = příkaz_data.한바이트(); String poziční_index = značka_HODNOTA_7e8f90bd + "_b" + pozice;
            vstupní_řádek.add(poziční_index + ":"); 경계들.add(pozice);
            if (příkaz == 0) vstupní_řádek.add("nop");
            else if (příkaz == 1) vstupní_řádek.add("pushl $0");
            else if (příkaz >= 2 && příkaz <= 8) vstupní_řádek.add("pushl $" + (příkaz - 3));
            else if (příkaz == 16 || příkaz == 17) vstupní_řádek.add("pushl $" + (příkaz == 16 ? příkaz_data.부호한바이트() : příkaz_data.부호두바이트()));
            else if (příkaz == 18 || příkaz == 19) {
                int INDEX = příkaz == 18 ? příkaz_data.한바이트() : příkaz_data.두바이트();
                vstupní_řádek.add("pushl $" + X_86_konstanta(Třída_HODNOTA,INDEX));
            } else if (příkaz == 21 || příkaz == 25 || (příkaz >= 26 && příkaz <= 29) || (příkaz >= 42 && příkaz <= 45) || příkaz == 54 || příkaz == 58 || (příkaz >= 59 && příkaz <= 62) || (příkaz >= 75 && příkaz <= 78)) {
                boolean 읽음 = příkaz < 54; int INDEX = příkaz == 21 || příkaz == 25 || příkaz == 54 || příkaz == 58 ? příkaz_data.한바이트() : příkaz - (příkaz <= 29 ? 26 : příkaz <= 45 ? 42 : příkaz <= 62 ? 59 : 75);
                šek_místní(INDEX,místní_POČET); vstupní_řádek.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (příkaz == 46) Collections.addAll(vstupní_řádek,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (příkaz == 79) Collections.addAll(vstupní_řádek,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (příkaz == 87 || příkaz == 88) vstupní_řádek.add("addl $" + (příkaz == 87 ? 4 : 8) + ", %esp");
            else if (příkaz >= 89 && příkaz <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] pořadí_Seznam = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[příkaz - 89]; 순번++) vstupní_řádek.add("popl " + 저장기들[순번]);
                for (int 순번 : pořadí_Seznam[příkaz - 89]) vstupní_řádek.add("pushl " + 저장기들[순번]);
            } else if (příkaz == 96 || příkaz == 100 || příkaz == 104 || příkaz == 126 || příkaz == 128 || příkaz == 130) {
                String operace_HODNOTA = příkaz == 96 ? "addl" : příkaz == 100 ? "subl" : příkaz == 104 ? "imull" : příkaz == 126 ? "andl" : příkaz == 128 ? "orl" : "xorl";
                Collections.addAll(vstupní_řádek,"popl %ecx","popl %eax",operace_HODNOTA + " %ecx, %eax","pushl %eax");
            } else if (příkaz == 108 || příkaz == 112) Collections.addAll(vstupní_řádek,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + poziční_index + "_divide","cmpl $0x80000000, %eax","jne " + poziční_index + "_divide","xorl %edx, %edx","jmp " + poziční_index + "_done",poziční_index + "_divide:","cltd","idivl %ecx",poziční_index + "_done:","pushl " + (příkaz == 108 ? "%eax" : "%edx"));
            else if (příkaz == 116) vstupní_řádek.add("negl (%esp)");
            else if (příkaz == 120 || příkaz == 122 || příkaz == 124) Collections.addAll(vstupní_řádek,"popl %ecx","popl %eax",(příkaz == 120 ? "sall" : příkaz == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (příkaz == 132) {
                int INDEX = příkaz_data.한바이트(), 증가 = příkaz_data.부호한바이트(); šek_místní(INDEX,místní_POČET); vstupní_řádek.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (příkaz >= 145 && příkaz <= 147) Collections.addAll(vstupní_řádek,"popl %eax",příkaz == 145 ? "movsbl %al, %eax" : příkaz == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (příkaz >= 153 && příkaz <= 166) {
                if (příkaz <= 158) Collections.addAll(vstupní_řádek,"popl %eax","testl %eax, %eax");
                else Collections.addAll(vstupní_řádek,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int cíl_HODNOTA = pozice + příkaz_data.부호두바이트(); větev_Seznam.add(cíl_HODNOTA); vstupní_řádek.add(비교들[příkaz - (příkaz <= 158 ? 153 : 159)] + " " + značka_HODNOTA_7e8f90bd + "_b" + cíl_HODNOTA);
            } else if (příkaz == 167 || příkaz == 200) {
                int cíl_HODNOTA = pozice + (příkaz == 167 ? příkaz_data.부호두바이트() : příkaz_data.네바이트()); větev_Seznam.add(cíl_HODNOTA); vstupní_řádek.add("jmp " + značka_HODNOTA_7e8f90bd + "_b" + cíl_HODNOTA);
            } else if (příkaz == 170 || příkaz == 171) {
                while (příkaz_data.pozice % 4 != 0) příkaz_data.한바이트();
                int výchozí_hodnota = pozice + příkaz_data.네바이트(); větev_Seznam.add(výchozí_hodnota); vstupní_řádek.add("popl %eax");
                int zboží_POČET, 아래 = 0;
                if (příkaz == 170) { 아래 = příkaz_data.네바이트(); int 위 = příkaz_data.네바이트(); long délka_HODNOTA = (long)위 - 아래 + 1; if (délka_HODNOTA < 1 || délka_HODNOTA > (příkaz_data.data.length - příkaz_data.pozice) / 4) throw new převod_chyba("switch oříznout chyba"); zboží_POČET = (int)délka_HODNOTA; }
                else { zboží_POČET = příkaz_data.네바이트(); if (zboží_POČET < 0 || zboží_POČET > (příkaz_data.data.length - příkaz_data.pozice) / 8) throw new převod_chyba("switch Velikost chyba"); }
                for (int 순번 = 0; 순번 < zboží_POČET; 순번++) {
                    int HODNOTA = příkaz == 170 ? 아래 + 순번 : příkaz_data.네바이트(), cíl_HODNOTA = pozice + příkaz_data.네바이트(); větev_Seznam.add(cíl_HODNOTA);
                    Collections.addAll(vstupní_řádek,"cmpl $" + HODNOTA + ", %eax","je " + značka_HODNOTA_7e8f90bd + "_b" + cíl_HODNOTA);
                }
                vstupní_řádek.add("jmp " + značka_HODNOTA_7e8f90bd + "_b" + výchozí_hodnota);
            } else if (příkaz == 172 || příkaz == 176 || příkaz == 177) {
                if (příkaz != 177) vstupní_řádek.add("popl %eax"); Collections.addAll(vstupní_řádek,"leave","ret");
            } else if (příkaz == 178 || příkaz == 179) {
                metoda_odkaz odkaz = Třída_HODNOTA.odkaz(příkaz_data.두바이트()); if (!필드들.containsKey(odkaz)) throw new převod_chyba("알 číslo 없는 hodnota_pole");
                Collections.addAll(vstupní_řádek,"call " + symbol("init",odkaz.vlastník_HODNOTA),(příkaz == 178 ? "pushl " : "popl ") + symbol("field",odkaz.부분들()));
            } else if (příkaz == 184) {
                metoda_odkaz odkaz = Třída_HODNOTA.odkaz(příkaz_data.두바이트()); if (!함수들.containsKey(odkaz)) throw new převod_chyba("알 číslo 없는 funkce_HODNOTA");
                metoda_popisovač 호출형식 = new metoda_popisovač(odkaz.서술); Collections.addAll(vstupní_řádek,"call " + symbol("init",odkaz.vlastník_HODNOTA),"call " + symbol("method",odkaz.부분들()));
                if (!호출형식.argumenty.isEmpty()) vstupní_řádek.add("addl $" + 호출형식.argumenty.size() * 4 + ", %esp");
                if (!호출형식.Vratka_KV.equals("V")) vstupní_řádek.add("pushl %eax");
            } else if (příkaz == 182) {
                metoda_odkaz odkaz = Třída_HODNOTA.odkaz(příkaz_data.두바이트());
                if (odkaz.equals(new metoda_odkaz("java/lang/String","length","()I"))) Collections.addAll(vstupní_řádek,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (odkaz.equals(new metoda_odkaz("java/lang/String","charAt","(I)C"))) Collections.addAll(vstupní_řádek,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new převod_chyba("가상 funkce_HODNOTA 호출 미지원");
            } else if (příkaz == 188) {
                if (příkaz_data.한바이트() != 10) throw new převod_chyba("new int[]만 vzpěra_HODNOTA"); Collections.addAll(vstupní_řádek,"popl %eax","call rt_new_array","pushl %eax");
            } else if (příkaz == 190) Collections.addAll(vstupní_řádek,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (příkaz == 196) {
                int přípona_HODNOTA = příkaz_data.한바이트(), INDEX = příkaz_data.두바이트(); šek_místní(INDEX,místní_POČET);
                if (přípona_HODNOTA == 21 || přípona_HODNOTA == 25 || přípona_HODNOTA == 54 || přípona_HODNOTA == 58) vstupní_řádek.add((přípona_HODNOTA <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (přípona_HODNOTA == 132) vstupní_řádek.add("addl $" + příkaz_data.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new převod_chyba("wide příkaz 미지원");
            } else if (příkaz == 198 || příkaz == 199) {
                int cíl_HODNOTA = pozice + příkaz_data.부호두바이트(); větev_Seznam.add(cíl_HODNOTA); Collections.addAll(vstupní_řádek,"popl %eax","testl %eax, %eax",(příkaz == 198 ? "je " : "jne ") + značka_HODNOTA_7e8f90bd + "_b" + cíl_HODNOTA);
            } else throw new převod_chyba("미지원 příkaz: " + příkaz);
        }
        if (!경계들.containsAll(větev_Seznam)) throw new převod_chyba("příkaz 경계가 아닌 곳으로 větev");
        vstupní_řádek.add(".size " + značka_HODNOTA_7e8f90bd + ", .-" + značka_HODNOTA_7e8f90bd); return String.join("\n",vstupní_řádek);
    }
    String X_86_konstanta(Třída_data data, int INDEX) {
        if (data.konstanta_Druh[INDEX] == 3) return data.konstanta_data[INDEX].toString();
        if (data.konstanta_Druh[INDEX] == 8) return řetězec_symbol(data.문자((Integer)data.konstanta_data[INDEX]));
        throw new převod_chyba("정수와 řetězec_HODNOTA 상수만 vzpěra_HODNOTA");
    }
    String X_86_montáž(String vstupní_bod, List<String> 내보냄, String cílová_úroveň) throws IOException {
        Map<String,String> počítač_tabulka = new HashMap<>();
        for (String vstupní_řádek : Files.readAllLines(zdroj_cesta.resolve("_86_počítač_Functions.tsv"))) { String[] spárovat_HODNOTA = vstupní_řádek.split("\t"); if (spárovat_HODNOTA[0].equals(cílová_úroveň)) počítač_tabulka.put(spárovat_HODNOTA[1] + spárovat_HODNOTA[2],spárovat_HODNOTA[3]); }
        int poziční_index = vstupní_bod.lastIndexOf('.'); if (poziční_index < 0) throw new převod_chyba("vstupní_bod Přiřadit_HODNOTA chyba");
        String vlastník_HODNOTA = vstupní_bod.substring(0,poziční_index).replace('.','/'), metoda_položka_název = vstupní_bod.substring(poziční_index + 1); metoda_odkaz vstupní_bod_HODNOTA = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metoda_odkaz odkaz = new metoda_odkaz(vlastník_HODNOTA,metoda_položka_název,서술); if (함수들.containsKey(odkaz)) { if (vstupní_bod_HODNOTA != null) throw new převod_chyba("겹친 vstupní_bod"); vstupní_bod_HODNOTA = odkaz; } }
        if (vstupní_bod_HODNOTA == null || (함수들.get(vstupní_bod_HODNOTA).přístup_položka & 0x100) != 0) throw new převod_chyba("vstupní_bod_HODNOTA funkce_HODNOTA formát_HODNOTA chyba");
        List<String> vstupní_řádek = new ArrayList<>(); vstupní_řádek.add(".code32");
        for (Třída_data data : 클래스들.values()) {
            String Stav_HODNOTA = symbol("state",data.Název), inicializovat = symbol("init",data.Název);
            Collections.addAll(vstupní_řádek,".bss",".balign 4",Stav_HODNOTA + ": .long 0",".text",inicializovat + ":","cmpl $0, " + Stav_HODNOTA,"jne " + inicializovat + "_done","movl $1, " + Stav_HODNOTA);
            metoda_odkaz inicializátor_odkaz = new metoda_odkaz(data.Název,"<clinit>","()V"); if (함수들.containsKey(inicializátor_odkaz)) vstupní_řádek.add("call " + symbol("method",inicializátor_odkaz.부분들()));
            Collections.addAll(vstupní_řádek,"movl $2, " + Stav_HODNOTA,inicializovat + "_done:","ret");
            for (člen_data hodnota_pole : data.hodnota_pole) {
                byte[] konstanta_HODNOTA = hodnota_pole.hodnota_atributu.get("ConstantValue"); String HODNOTA = konstanta_HODNOTA == null ? "0" : X_86_konstanta(data,new data_Čtenář(konstanta_HODNOTA).두바이트());
                Collections.addAll(vstupní_řádek,".data",".balign 4",symbol("field",data.Název,hodnota_pole.Název,hodnota_pole.서술) + ": .long " + HODNOTA);
            }
            for (člen_data funkce_HODNOTA : data.funkce_HODNOTA) if (!funkce_HODNOTA.Název.equals("<init>")) vstupní_řádek.add(X_86_tělo_metody(new metoda_odkaz(data.Název,funkce_HODNOTA.Název,funkce_HODNOTA.서술),funkce_HODNOTA,počítač_tabulka,cílová_úroveň));
        }
        Collections.addAll(vstupní_řádek,".text",".globl java_entry","java_entry:","call " + symbol("init",vstupní_bod_HODNOTA.vlastník_HODNOTA),"call " + symbol("method",vstupní_bod_HODNOTA.부분들()));
        if (vstupní_bod_HODNOTA.서술.equals("()V")) vstupní_řádek.add("xorl %eax, %eax"); vstupní_řádek.add("ret");
        for (String Přiřadit_HODNOTA : 내보냄) {
            int oddělovač_HODNOTA_d8ba4873 = Přiřadit_HODNOTA.indexOf('='); if (oddělovač_HODNOTA_d8ba4873 < 1) throw new převod_chyba("내보내기 Přiřadit_HODNOTA chyba");
            String externí_HODNOTA = Přiřadit_HODNOTA.substring(0,oddělovač_HODNOTA_d8ba4873), funkce_HODNOTA = Přiřadit_HODNOTA.substring(oddělovač_HODNOTA_d8ba4873 + 1); int podíl_KV = funkce_HODNOTA.lastIndexOf('.');
            if (podíl_KV < 0 || !externí_HODNOTA.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new převod_chyba("내보내기 symbol chyba");
            String Třída_HODNOTA = funkce_HODNOTA.substring(0,podíl_KV).replace('.','/'), Název = funkce_HODNOTA.substring(podíl_KV + 1); metoda_odkaz výběr_HODNOTA = null;
            for (metoda_odkaz odkaz : 함수들.keySet()) if (odkaz.vlastník_HODNOTA.equals(Třída_HODNOTA) && odkaz.Název.equals(Název)) { if (výběr_HODNOTA != null) throw new převod_chyba("겹친 내보내기 cílová_úroveň"); výběr_HODNOTA = odkaz; }
            if (výběr_HODNOTA == null) throw new převod_chyba("내보낼 함수가 없음");
            Collections.addAll(vstupní_řádek,".text",".globl " + externí_HODNOTA,externí_HODNOTA + ":","call " + symbol("init",výběr_HODNOTA.vlastník_HODNOTA),"jmp " + symbol("method",výběr_HODNOTA.부분들()));
        }
        vstupní_řádek.add(".section .rodata");
        for (Map.Entry<String,String> položka_HODNOTA : 문자열들.entrySet()) {
            Collections.addAll(vstupní_řádek,".balign 4",položka_HODNOTA.getValue() + ":",".long " + položka_HODNOTA.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lekce_HODNOTA : položka_HODNOTA.getKey().toCharArray()) 단위들.add(Integer.toString(lekce_HODNOTA)); if (!단위들.isEmpty()) vstupní_řádek.add(".long " + String.join(",",단위들));
        }
        vstupní_řádek.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",vstupní_řádek) + "\n";
    }
    static void Provést_nástroj(List<String> příkaz) throws Exception {
        if (new ProcessBuilder(příkaz).inheritIO().start().waitFor() != 0) throw new převod_chyba("kompilovat_zdroj chyba: " + příkaz.get(0));
    }
    static String data_řetězec(String text) { return "\"" + text.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_převod(List<Path> vstup_Seznam, String cílová_úroveň, String vstupní_bod, List<String> 내보냄, Path výstupní_pozice, Path zdroj_HODNOTA) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Třída_cesta = 임시.resolve("classes"); Files.createDirectory(Třída_cesta);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Třída_cesta.toString(),"-sourcepath",Třída_cesta.toString(),"-d",Třída_cesta.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int zdroj_POČET = 0;
            for (Path vstup_HODNOTA : vstup_Seznam) {
                if (výstupní_pozice.toAbsolutePath().normalize().equals(vstup_HODNOTA.toAbsolutePath().normalize())) throw new převod_chyba("výstupní_pozice 파일과 입력이 같음");
                if (vstup_HODNOTA.toString().endsWith(".java")) { 자바명령.add(vstup_HODNOTA.toString()); zdroj_POČET++; }
                else if (vstup_HODNOTA.toString().endsWith(".class")) 바이트코드.add(vstup_HODNOTA);
                else throw new převod_chyba(".java 또는 .class만 vzpěra_HODNOTA");
            }
            if (zdroj_POČET > 0) Provést_nástroj(자바명령);
            try (java.util.stream.Stream<Path> cesta_Seznam = Files.walk(Třída_cesta)) { cesta_Seznam.filter(cesta_2 -> cesta_2.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_HODNOTA = new 기계어미리번역(바이트코드,cílová_úroveň.equals("user") ? "user" : "kernel",262144,zdroj_HODNOTA);
            String sestavit_HODNOTA = CONVERT_HODNOTA.X_86_montáž(vstupní_bod,내보냄,cílová_úroveň); Files.writeString(임시.resolve("program.s"),sestavit_HODNOTA,StandardCharsets.UTF_8);
            Path nástroj_pozice = zdroj_HODNOTA.getParent();
            Provést_nástroj(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Provést_nástroj(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),nástroj_pozice.resolve("CLR_vzpěra.s").toString()));
            List<String> Připojit = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (cílová_úroveň.equals("kernel")) Připojit.add("-r");
            else {
                Provést_nástroj(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),nástroj_pozice.resolve(cílová_úroveň.equals("user") ? "START_uživatel_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(Připojit,"-e","_start",임시.resolve("start.o").toString());
                if (cílová_úroveň.equals("user")) Collections.addAll(Připojit,"-T",nástroj_pozice.resolve("uživatel_Odkaz_Navigace.ld").toString());
            }
            Collections.addAll(Připojit,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Provést_nástroj(Připojit);
            výstupní_pozice = výstupní_pozice.toAbsolutePath(); Files.createDirectories(výstupní_pozice.getParent()); Path publikovat_HODNOTA = Files.createTempFile(výstupní_pozice.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publikovat_HODNOTA,StandardCopyOption.REPLACE_EXISTING); Files.move(publikovat_HODNOTA,výstupní_pozice,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publikovat_HODNOTA); }
            Files.setPosixFilePermissions(výstupní_pozice,java.nio.file.attribute.PosixFilePermissions.fromString(cílová_úroveň.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(výstupní_pozice + ".s"),sestavit_HODNOTA,StandardCharsets.UTF_8);
            List<String> symbol_data = new ArrayList<>(), zdroj_data = new ArrayList<>();
            for (metoda_odkaz odkaz : CONVERT_HODNOTA.함수들.keySet()) symbol_data.add(data_řetězec(symbol("method",odkaz.부분들())) + ":" + data_řetězec(odkaz.vlastník_HODNOTA + "." + odkaz.Název + odkaz.서술));
            for (Path vstup_HODNOTA : vstup_Seznam) {
                byte[] hodnota_hash_Soubor = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(vstup_HODNOTA)); StringBuilder text = new StringBuilder(); for (byte HODNOTA : hodnota_hash_Soubor) text.append(String.format(Locale.ROOT,"%02x",HODNOTA & 255));
                zdroj_data.add(data_řetězec(vstup_HODNOTA.toAbsolutePath().toString()) + ":" + data_řetězec(text.toString()));
            }
            Files.writeString(Paths.get(výstupní_pozice + ".json"),"{\"target\":" + data_řetězec(cílová_úroveň) + ",\"entry\":" + data_řetězec(vstupní_bod) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbol_data) + "},\"sources\":{" + String.join(",",zdroj_data) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> cesta_Seznam = Files.walk(임시)) { for (Path cesta_2 : (Iterable<Path>)cesta_Seznam.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(cesta_2); }
        }
    }
    public static void main(String[] argumenty) {
        try {
            String vstupní_bod = null, cílová_úroveň = "kernel", X_86_cíl = null; Path výstup_cesta = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> cesta_Seznam = new ArrayList<>();
            for (int 순번 = 0; 순번 < argumenty.length; 순번++) {
                String HODNOTA = argumenty[순번];
                switch (HODNOTA) {
                    case "--target": X_86_cíl = argumenty[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Třída_HODNOTA.funkce_HODNOTA -o výstupní_pozice [--target linux|kernel|user] [--profile kernel|user] [--export symbol=Třída_HODNOTA.funkce_HODNOTA] 클래스파일 또는 Java원문"); return;
                    case "--entry": vstupní_bod = argumenty[++순번]; break;
                    case "--profile": cílová_úroveň = argumenty[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(argumenty[++순번]); break;
                    case "--export": 내보냄.add(argumenty[++순번]); break;
                    case "-o": výstup_cesta = Paths.get(argumenty[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (HODNOTA.startsWith("-")) throw new převod_chyba("알 číslo 없는 옵션: " + HODNOTA); cesta_Seznam.add(Paths.get(HODNOTA));
                }
            }
            if (vstupní_bod == null || výstup_cesta == null || cesta_Seznam.isEmpty()) throw new převod_chyba("--entry, -o, Třída_HODNOTA 파일이 필요합니다");
            Path zdroj_HODNOTA = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_cíl != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_cíl)) throw new převod_chyba("알 číslo 없는 Provést_příkaz cílová_úroveň");
                X_86_převod(cesta_Seznam,X_86_cíl,vstupní_bod,내보냄,výstup_cesta,zdroj_HODNOTA); return;
            }
            String zdrojový_soubor = new 기계어미리번역(cesta_Seznam, cílová_úroveň, 낱말수, zdroj_HODNOTA).generovat(vstupní_bod, 내보냄, 범용표기);
            výstup_cesta = výstup_cesta.toAbsolutePath(); Files.createDirectories(výstup_cesta.getParent());
            Path 임시 = Files.createTempFile(výstup_cesta.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, zdrojový_soubor, StandardCharsets.UTF_8); Files.move(임시, výstup_cesta, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception chyba) { System.err.println("kompilovat_zdroj chyba: " + chyba.getMessage()); System.exit(1); }
    }
}
