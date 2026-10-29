// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Razred_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. gostiti JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class 번역오류 extends RuntimeException {
        번역오류(String 설명) { super(설명); }
    }
    static final class podatki_bralec {
        final byte[] podatki;
        int Položaj;
        podatki_bralec(byte[] 입력자료) { podatki = 입력자료; }
        byte[] Branje(int 길이) {
            if (길이 < 0 || 길이 > podatki.length - Položaj) throw new 번역오류("잘린 Razred_VALUE 또는 Ukaz podatki");
            byte[] REZULTAT = Arrays.copyOfRange(podatki, Položaj, Položaj + 길이); Položaj += 길이; return REZULTAT;
        }
        int 한바이트() { if (Položaj >= podatki.length) throw new 번역오류("잘린 Ukaz podatki"); return podatki[Položaj++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class član_podatki {
        final int dostop_vnos;
        final String Ime, 서술;
        final Map<String, byte[]> atribut_VALUE;
        član_podatki(int dostop_VALUE, String ime_VALUE, String 서술값, Map<String, byte[]> atribut_podatki) {
            dostop_vnos = dostop_VALUE; Ime = ime_VALUE; 서술 = 서술값; atribut_VALUE = atribut_podatki;
        }
    }
    static final class metoda_Gradiva implements Comparable<metoda_Gradiva> {
        final String lastnik_VALUE, Ime, 서술;
        metoda_Gradiva(String 소유값, String ime_VALUE, String 서술값) { lastnik_VALUE = 소유값; Ime = ime_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{lastnik_VALUE, Ime, 서술}; }
        public int compareTo(metoda_Gradiva enakovreden_VALUE) {
            int Primerjava_VALUE = lastnik_VALUE.compareTo(enakovreden_VALUE.lastnik_VALUE);
            if (Primerjava_VALUE == 0) Primerjava_VALUE = Ime.compareTo(enakovreden_VALUE.Ime);
            return Primerjava_VALUE == 0 ? 서술.compareTo(enakovreden_VALUE.서술) : Primerjava_VALUE;
        }
        public boolean equals(Object enakovreden_VALUE) { return enakovreden_VALUE instanceof metoda_Gradiva && compareTo((metoda_Gradiva) enakovreden_VALUE) == 0; }
        public int hashCode() { return Objects.hash(lastnik_VALUE, Ime, 서술); }
    }
    static final class Razred_podatki {
        final int[] 상수종류;
        final Object[] konstanta_podatki;
        final String Ime;
        final List<član_podatki> polje_VALUE, FUNCTION_VALUE;
        Razred_podatki(Path POT) throws IOException {
            podatki_bralec bralec_VALUE = new podatki_bralec(Files.readAllBytes(POT));
            if (bralec_VALUE.네바이트() != 0xcafebabe) throw new 번역오류("Java Razred_VALUE 표식이 아님");
            bralec_VALUE.Branje(4);
            int element_COUNT = bralec_VALUE.두바이트(); 상수종류 = new int[element_COUNT]; konstanta_podatki = new Object[element_COUNT];
            for (int 순번 = 1; 순번 < element_COUNT; 순번++) {
                int 종류 = bralec_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int 길이 = bralec_VALUE.두바이트();
                        byte[] znak_medpomnilnik = bralec_VALUE.Branje(길이), 길이붙인자료 = new byte[길이 + 2];
                        길이붙인자료[0] = (byte)(길이 >> 8); 길이붙인자료[1] = (byte)길이;
                        System.arraycopy(znak_medpomnilnik, 0, 길이붙인자료, 2, 길이);
                        konstanta_podatki[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstanta_podatki[순번] = bralec_VALUE.네바이트(); break;
                    case 4: bralec_VALUE.Branje(4); break;
                    case 5: case 6: bralec_VALUE.Branje(8); 순번++; break;
                    case 7: case 8: case 16: konstanta_podatki[순번] = bralec_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstanta_podatki[순번] = new int[]{bralec_VALUE.두바이트(), bralec_VALUE.두바이트()}; break;
                    case 15: konstanta_podatki[순번] = new int[]{bralec_VALUE.한바이트(), bralec_VALUE.두바이트()}; break;
                    default: throw new 번역오류("지원하지 않는 konstanta_VALUE 종류: " + 종류);
                }
            }
            bralec_VALUE.두바이트(); Ime = ime_razreda(bralec_VALUE.두바이트());
            if (!ime_razreda(bralec_VALUE.두바이트()).equals("java/lang/Object") || bralec_VALUE.두바이트() != 0)
                throw new 번역오류(Ime + ": 상속 및 인터페이스 미지원");
            polje_VALUE = 멤버읽기(bralec_VALUE); FUNCTION_VALUE = 멤버읽기(bralec_VALUE); 속성읽기(bralec_VALUE);
            if (bralec_VALUE.Položaj != bralec_VALUE.podatki.length) throw new 번역오류("Razred_VALUE 뒤에 남은 podatki");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new 번역오류("문자 konstanta_VALUE INDEX NAPAKA");
            return (String) konstanta_podatki[INDEX];
        }
        String ime_razreda(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new 번역오류("Razred_VALUE Gradiva NAPAKA");
            return 문자((Integer)konstanta_podatki[INDEX]);
        }
        metoda_Gradiva Gradiva(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new 번역오류("멤버 Gradiva NAPAKA");
            int[] seznaniti_VALUE = (int[])konstanta_podatki[INDEX], ime_seznaniti = (int[])konstanta_podatki[seznaniti_VALUE[1]];
            return new metoda_Gradiva(ime_razreda(seznaniti_VALUE[0]), 문자(ime_seznaniti[0]), 문자(ime_seznaniti[1]));
        }
        Map<String, byte[]> 속성읽기(podatki_bralec bralec_VALUE) {
            Map<String, byte[]> REZULTAT = new LinkedHashMap<>();
            int element_COUNT = bralec_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                String atribut_ime = 문자(bralec_VALUE.두바이트()); byte[] VALUE = bralec_VALUE.Branje(bralec_VALUE.네바이트());
                if (REZULTAT.put(atribut_ime, VALUE) != null) throw new 번역오류("겹친 atribut_VALUE: " + atribut_ime);
            }
            return REZULTAT;
        }
        List<član_podatki> 멤버읽기(podatki_bralec bralec_VALUE) {
            List<član_podatki> REZULTAT = new ArrayList<>(); int element_COUNT = bralec_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                int dostop_vnos = bralec_VALUE.두바이트(); String metoda_vnos_ime = 문자(bralec_VALUE.두바이트()), 서술 = 문자(bralec_VALUE.두바이트());
                REZULTAT.add(new član_podatki(dostop_vnos, metoda_vnos_ime, 서술, 속성읽기(bralec_VALUE)));
            }
            return REZULTAT;
        }
    }
    static final class 함수형식 {
        final List<String> Argumenti = new ArrayList<>();
        final String vrni_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new 번역오류("FUNCTION_VALUE 서술 NAPAKA: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new 번역오류("FUNCTION_VALUE 서술 NAPAKA: " + 서술);
            Argumenti.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumenti.contains("V") || 반환들.size() != 1) throw new 번역오류("FUNCTION_VALUE 서술 NAPAKA: " + 서술);
            vrni_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> REZULTAT = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Položaj = 0; Položaj < 서술.length();) {
            String izbor_VALUE = null;
            for (String oblika_VALUE : 허용형식) if (서술.startsWith(oblika_VALUE, Položaj)) { izbor_VALUE = oblika_VALUE; break; }
            if (izbor_VALUE == null) throw new 번역오류("지원하지 않는 vrsta_podatkov: " + 서술);
            REZULTAT.add(izbor_VALUE); Položaj += izbor_VALUE.length();
        }
        return REZULTAT;
    }
    static String simbol(String 종류, String... 부분들) {
        try {
            byte[] zgoščena_vrednost_Datoteka = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Besedilo = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Besedilo.append(String.format(Locale.ROOT, "%02x", zgoščena_vrednost_Datoteka[순번] & 255));
            return Besedilo.toString();
        } catch (Exception NAPAKA) { throw new 번역오류(NAPAKA.toString()); }
    }
    final Map<String, Razred_podatki> 클래스들 = new TreeMap<>();
    final Map<metoda_Gradiva, član_podatki> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), računalnik_Azure_Functions_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, računalnik_Razred;
    final int kopica_Word_COUNT;
    final Path vir_pot;
    기계어미리번역(List<Path> pot_Seznam, String tarča, int 낱말수, Path vir_VALUE) throws IOException {
        if ((!tarča.equals("kernel") && !tarča.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new 번역오류("Izvedi_ukaz tarča 또는 pomnilnik_VALUE naslov_območje Velikost NAPAKA");
        실행대상 = tarča; kopica_Word_COUNT = 낱말수; vir_pot = vir_VALUE;
        // 이 이름도 국가별 vir_drevo ustvariti 시 해당 언어로 옮긴다.
        računalnik_Razred = tarča.equals("kernel") ? "Tabla" : "uporabnik";
        for (String Črtni : Files.readAllLines(vir_VALUE.resolve("računalnik_Azure_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Črtni.split("\t", -1);
            if (부분들.length != 4) throw new 번역오류("računalnik FUNCTION_VALUE podatki NAPAKA");
            if (부분들[0].equals(tarča)) računalnik_Azure_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path POT : pot_Seznam) {
            Razred_podatki podatki = new Razred_podatki(POT);
            if (클래스들.put(podatki.Ime, podatki) != null) throw new 번역오류("중복 Razred_VALUE: " + podatki.Ime);
            for (član_podatki polje_VALUE : podatki.polje_VALUE) {
                if ((polje_VALUE.dostop_vnos & 8) == 0 || 형식읽기(polje_VALUE.서술).equals(Collections.singletonList("V"))) throw new 번역오류("statičen_VALUE 필드만 Podpora_VALUE");
                if (필드들.put(new metoda_Gradiva(podatki.Ime, polje_VALUE.Ime, polje_VALUE.서술), polje_VALUE) != null) throw new 번역오류("중복 polje_VALUE");
            }
            for (član_podatki FUNCTION_VALUE : podatki.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Ime.equals("<init>")) continue;
                if ((FUNCTION_VALUE.dostop_vnos & 8) == 0 || (FUNCTION_VALUE.dostop_vnos & (0x20 | 0x400)) != 0) throw new 번역오류("statičen_VALUE 비동기화 함수만 Podpora_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new metoda_Gradiva(podatki.Ime, FUNCTION_VALUE.Ime, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new 번역오류("중복 FUNCTION_VALUE");
            }
        }
    }
    String niz_simbol(String Besedilo) { return 문자열들.computeIfAbsent(Besedilo, VALUE -> "j_text_" + 문자열들.size()); }
    String konstanta_izraz(Razred_podatki podatki, int INDEX) {
        if (INDEX < 1 || INDEX >= podatki.상수종류.length) throw new 번역오류("konstanta_VALUE INDEX izrezek NAPAKA");
        if (podatki.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + podatki.konstanta_podatki[INDEX] + ")";
        if (podatki.상수종류[INDEX] == 8) return "(word)" + niz_simbol(podatki.문자((Integer)podatki.konstanta_podatki[INDEX]));
        throw new 번역오류("정수와 niz_VALUE 상수만 Podpora_VALUE");
    }
    String 함수원형(metoda_Gradiva Gradiva) {
        List<String> 인수들 = new ArrayList<>(); int element_COUNT = new 함수형식(Gradiva.서술).Argumenti.size();
        for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbol("method", Gradiva.부분들()) + "(" + (element_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void preveriti_lokalen_krajeven(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new 번역오류("lokalen_krajeven_obseg 변수 INDEX izrezek NAPAKA"); }
    void 분기넣기(List<String> Izpis, Set<Integer> veja_Seznam, int Položaj, int 이동량, String pogoj) {
        int cilj_VALUE = Položaj + 이동량; veja_Seznam.add(cilj_VALUE);
        Izpis.add((pogoj == null ? "" : "if (" + pogoj + ") ") + "goto b" + cilj_VALUE + ";");
    }
    String metoda_telo(metoda_Gradiva FUNCTION_VALUE, član_podatki podatki) {
        byte[] telo_podatki = podatki.atribut_VALUE.get("Code"); if (telo_podatki == null) throw new 번역오류("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Ime);
        podatki_bralec bralec_VALUE = new podatki_bralec(telo_podatki); int 쌓임깊이 = bralec_VALUE.두바이트(), 지역변수수 = bralec_VALUE.두바이트();
        podatki_bralec ukaz_podatki = new podatki_bralec(bralec_VALUE.Branje(bralec_VALUE.네바이트()));
        if (bralec_VALUE.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 oblika_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (지역변수수 < oblika_VALUE.Argumenti.size()) throw new 번역오류("매개변수보다 적은 lokalen_krajeven_obseg 변수");
        Razred_podatki Razred_VALUE = 클래스들.get(FUNCTION_VALUE.lastnik_VALUE);
        List<String> Izpis = new ArrayList<>(); Izpis.add(함수원형(FUNCTION_VALUE) + " {");
        Izpis.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < oblika_VALUE.Argumenti.size(); 순번++) Izpis.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), veja_Seznam = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (ukaz_podatki.Položaj < ukaz_podatki.podatki.length) {
            int Položaj = ukaz_podatki.Položaj, Ukaz = ukaz_podatki.한바이트(); 경계들.add(Položaj); Izpis.add("b" + Položaj + ":;");
            if (Ukaz == 0) continue;
            if (Ukaz == 1) Izpis.add("PUSH(0);");
            else if (Ukaz >= 2 && Ukaz <= 8) Izpis.add("PUSH((uint32_t)(" + (Ukaz - 3) + "));");
            else if (Ukaz == 16 || Ukaz == 17) Izpis.add("PUSH((uint32_t)(" + (Ukaz == 16 ? ukaz_podatki.부호한바이트() : ukaz_podatki.부호두바이트()) + "));");
            else if (Ukaz == 18 || Ukaz == 19) Izpis.add("PUSH(" + konstanta_izraz(Razred_VALUE, Ukaz == 18 ? ukaz_podatki.한바이트() : ukaz_podatki.두바이트()) + ");");
            else if (Ukaz == 21 || Ukaz == 25 || (Ukaz >= 26 && Ukaz <= 29) || (Ukaz >= 42 && Ukaz <= 45)) {
                int INDEX = Ukaz == 21 || Ukaz == 25 ? ukaz_podatki.한바이트() : Ukaz - (Ukaz <= 29 ? 26 : 42);
                preveriti_lokalen_krajeven(INDEX, 지역변수수); Izpis.add("PUSH(l[" + INDEX + "]);");
            } else if (Ukaz == 54 || Ukaz == 58 || (Ukaz >= 59 && Ukaz <= 62) || (Ukaz >= 75 && Ukaz <= 78)) {
                int INDEX = Ukaz == 54 || Ukaz == 58 ? ukaz_podatki.한바이트() : Ukaz - (Ukaz <= 62 ? 59 : 75);
                preveriti_lokalen_krajeven(INDEX, 지역변수수); Izpis.add("l[" + INDEX + "] = POP();");
            } else if (Ukaz == 46) Izpis.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Ukaz == 79) Izpis.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Ukaz == 87 || Ukaz == 88) Izpis.add(Ukaz == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Ukaz >= 89 && Ukaz <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] naročilo_Seznam = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Ukaz - 89]; 순번++) Izpis.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : naročilo_Seznam[Ukaz - 89].toCharArray()) Izpis.add("PUSH(" + VALUE + ");");
            } else if (Ukaz == 96 || Ukaz == 100 || Ukaz == 104 || Ukaz == 126 || Ukaz == 128 || Ukaz == 130) {
                String postopek_VALUE = Ukaz == 96 ? "+" : Ukaz == 100 ? "-" : Ukaz == 104 ? "*" : Ukaz == 126 ? "&" : Ukaz == 128 ? "|" : "^";
                Izpis.add("b = POP(); a = POP(); PUSH((uint32_t)a " + postopek_VALUE + " (uint32_t)b);");
            } else if (Ukaz == 108 || Ukaz == 112) Izpis.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Ukaz == 112 ? 1 : 0) + "));");
            else if (Ukaz == 116) Izpis.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Ukaz == 120 || Ukaz == 122 || Ukaz == 124) {
                Izpis.add("b = POP(); a = POP();"); Izpis.add("PUSH(" + (Ukaz == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Ukaz == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Ukaz == 132) {
                int INDEX = ukaz_podatki.한바이트(), 증가량 = ukaz_podatki.부호한바이트(); preveriti_lokalen_krajeven(INDEX, 지역변수수);
                Izpis.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Ukaz >= 145 && Ukaz <= 147) Izpis.add("a = POP(); PUSH((uint32_t)(" + (Ukaz == 145 ? "int8_t" : Ukaz == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Ukaz >= 153 && Ukaz <= 158) {
                Izpis.add("a = POP();"); 분기넣기(Izpis, veja_Seznam, Položaj, ukaz_podatki.부호두바이트(), "(int32_t)a " + 비교들[Ukaz - 153] + " 0");
            } else if (Ukaz >= 159 && Ukaz <= 166) {
                Izpis.add("b = POP(); a = POP();"); 분기넣기(Izpis, veja_Seznam, Položaj, ukaz_podatki.부호두바이트(), Ukaz >= 165 ? "a " + 비교들[Ukaz - 159] + " b" : "(int32_t)a " + 비교들[Ukaz - 159] + " (int32_t)b");
            } else if (Ukaz == 167 || Ukaz == 200) 분기넣기(Izpis, veja_Seznam, Položaj, Ukaz == 167 ? ukaz_podatki.부호두바이트() : ukaz_podatki.네바이트(), null);
            else if (Ukaz == 170 || Ukaz == 171) {
                while (ukaz_podatki.Položaj % 4 != 0) ukaz_podatki.한바이트();
                int privzeta_vrednost = ukaz_podatki.네바이트(); Izpis.add("a = POP();");
                if (Ukaz == 170) {
                    int 아래 = ukaz_podatki.네바이트(), 위 = ukaz_podatki.네바이트(); long element_COUNT = (long)위 - 아래 + 1;
                    if (element_COUNT < 1 || element_COUNT > (ukaz_podatki.podatki.length - ukaz_podatki.Položaj) / 4) throw new 번역오류("switch izrezek NAPAKA");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Izpis, veja_Seznam, Položaj, ukaz_podatki.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int element_COUNT = ukaz_podatki.네바이트(), sprednja_podatki = 0;
                    if (element_COUNT < 0 || element_COUNT > (ukaz_podatki.podatki.length - ukaz_podatki.Položaj) / 8) throw new 번역오류("switch Velikost NAPAKA");
                    for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                        int VALUE = ukaz_podatki.네바이트(); if (순번 > 0 && VALUE <= sprednja_podatki) throw new 번역오류("switch naročilo_VALUE NAPAKA"); sprednja_podatki = VALUE;
                        분기넣기(Izpis, veja_Seznam, Položaj, ukaz_podatki.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Izpis, veja_Seznam, Položaj, privzeta_vrednost, null);
            } else if (Ukaz == 172 || Ukaz == 176 || Ukaz == 177) Izpis.add("return " + (Ukaz == 177 ? "0" : "POP()") + ";");
            else if (Ukaz == 178 || Ukaz == 179) {
                metoda_Gradiva Gradiva = Razred_VALUE.Gradiva(ukaz_podatki.두바이트()); if (!필드들.containsKey(Gradiva)) throw new 번역오류("알 수 없는 polje_VALUE");
                Izpis.add(simbol("init", Gradiva.lastnik_VALUE) + "();"); String polje_VALUE = simbol("field", Gradiva.부분들());
                Izpis.add(Ukaz == 178 ? "PUSH(" + polje_VALUE + ");" : polje_VALUE + " = POP();");
            } else if (Ukaz == 184) {
                metoda_Gradiva Gradiva = Razred_VALUE.Gradiva(ukaz_podatki.두바이트()); if (!함수들.containsKey(Gradiva)) throw new 번역오류("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Gradiva.서술); int element_COUNT = 호출형식.Argumenti.size();
                Izpis.add(simbol("init", Gradiva.lastnik_VALUE) + "();"); Izpis.add("if(sp < " + element_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + element_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < element_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Izpis.add("a = " + simbol("method", Gradiva.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.vrni_KR.equals("V")) Izpis.add("PUSH(a);");
            } else if (Ukaz == 182) {
                metoda_Gradiva Gradiva = Razred_VALUE.Gradiva(ukaz_podatki.두바이트());
                if (Gradiva.equals(new metoda_Gradiva("java/lang/String", "length", "()I"))) Izpis.add("a = POP(); PUSH(length(a));");
                else if (Gradiva.equals(new metoda_Gradiva("java/lang/String", "charAt", "(I)C"))) Izpis.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 번역오류("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Ukaz == 188) {
                if (ukaz_podatki.한바이트() != 10) throw new 번역오류("new int[]만 Podpora_VALUE"); Izpis.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Ukaz == 190) Izpis.add("a = POP(); PUSH(length(a));");
            else if (Ukaz == 196) {
                int pripona_VALUE = ukaz_podatki.한바이트(), INDEX = ukaz_podatki.두바이트(); preveriti_lokalen_krajeven(INDEX, 지역변수수);
                if (pripona_VALUE == 21 || pripona_VALUE == 25) Izpis.add("PUSH(l[" + INDEX + "]);");
                else if (pripona_VALUE == 54 || pripona_VALUE == 58) Izpis.add("l[" + INDEX + "] = POP();");
                else if (pripona_VALUE == 132) Izpis.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + ukaz_podatki.부호두바이트() + ");");
                else throw new 번역오류("미지원 wide Ukaz");
            } else if (Ukaz == 198 || Ukaz == 199) {
                Izpis.add("a = POP();"); 분기넣기(Izpis, veja_Seznam, Položaj, ukaz_podatki.부호두바이트(), "a " + (Ukaz == 198 ? "==" : "!=") + " 0");
            } else throw new 번역오류(FUNCTION_VALUE.lastnik_VALUE + "." + FUNCTION_VALUE.Ime + ", bajt_VALUE " + Položaj + ": 미지원 Ukaz " + Ukaz);
        }
        if (!경계들.containsAll(veja_Seznam)) throw new 번역오류("Ukaz 경계가 아닌 곳으로 veja");
        Izpis.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Izpis);
    }
    String izvoziti_metoda(String Povezava_simbol, String tarča, boolean 진입점여부) {
        int kazalec_mesta = tarča.lastIndexOf('.'); if (kazalec_mesta < 0 || !Povezava_simbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 Dodeli_VALUE NAPAKA");
        String lastnik_VALUE = tarča.substring(0, kazalec_mesta).replace('.', '/'), Ime = tarča.substring(kazalec_mesta + 1); metoda_Gradiva izbor_VALUE = null;
        for (metoda_Gradiva Gradiva : 함수들.keySet()) if (Gradiva.lastnik_VALUE.equals(lastnik_VALUE) && Gradiva.Ime.equals(Ime)) {
            if (izbor_VALUE != null) throw new 번역오류("겹친 내보내기 tarča"); izbor_VALUE = Gradiva;
        }
        if (izbor_VALUE == null || (함수들.get(izbor_VALUE).dostop_vnos & 0x100) != 0) throw new 번역오류("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 oblika_VALUE = new 함수형식(izbor_VALUE.서술);
        if ((진입점여부 && !oblika_VALUE.Argumenti.isEmpty()) || !Arrays.asList("V", "I").contains(oblika_VALUE.vrni_KR)) throw new 번역오류("vnos_p_VALUE 또는 C 경계 oblika_VALUE NAPAKA");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < oblika_VALUE.Argumenti.size(); 순번++) {
            if (!oblika_VALUE.Argumenti.get(순번).equals("I")) throw new 번역오류("C 경계는 int 인수만 Podpora_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (oblika_VALUE.vrni_KR.equals("V") ? "void " : "int32_t ") + Povezava_simbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbol("init", izbor_VALUE.lastnik_VALUE) + "(); " + (oblika_VALUE.vrni_KR.equals("V") ? "" : "return (int32_t)") + simbol("method", izbor_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String ustvariti(String vnos_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metoda_Gradiva, član_podatki> vnos_VALUE : 함수들.entrySet()) {
            metoda_Gradiva Gradiva = vnos_VALUE.getKey(); član_podatki podatki = vnos_VALUE.getValue(); 선언들.add(함수원형(Gradiva) + ";");
            if ((podatki.dostop_vnos & 0x100) != 0) {
                String Poveži = računalnik_Azure_Functions_c3a8e64a.get(Gradiva.Ime + Gradiva.서술);
                if (!Gradiva.lastnik_VALUE.equals(računalnik_Razred) || Poveži == null) throw new 번역오류("허용되지 않은 native FUNCTION_VALUE: " + Gradiva.Ime);
                int element_COUNT = new 함수형식(Gradiva.서술).Argumenti.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Poveži + "(" + (element_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(element_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Gradiva) + " { return " + Poveži + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metoda_telo(Gradiva, podatki));
        }
        for (Map.Entry<metoda_Gradiva, član_podatki> vnos_VALUE : 필드들.entrySet()) {
            metoda_Gradiva Gradiva = vnos_VALUE.getKey(); byte[] konstanta_VALUE = vnos_VALUE.getValue().atribut_VALUE.get("ConstantValue");
            String VALUE = konstanta_VALUE == null ? "0" : konstanta_izraz(클래스들.get(Gradiva.lastnik_VALUE), new podatki_bralec(konstanta_VALUE).두바이트());
            필드선언들.add("static word " + simbol("field", Gradiva.부분들()) + " = " + VALUE + ";");
        }
        for (String Ime : 클래스들.keySet()) {
            String inicializirati = simbol("init", Ime), stanje_VALUE = simbol("state", Ime);
            선언들.add("static void " + inicializirati + "(void);"); 필드선언들.add("static unsigned " + stanje_VALUE + ";");
            metoda_Gradiva Gradiva = new metoda_Gradiva(Ime, "<clinit>", "()V");
            몸체들.add("static void " + inicializirati + "(void) { if(" + stanje_VALUE + ") return; " + stanje_VALUE + " = 1; " + (함수들.containsKey(Gradiva) ? simbol("method", Gradiva.부분들()) + "(); " : "") + stanje_VALUE + " = 2; }");
        }
        몸체들.add(izvoziti_metoda("java_entry", vnos_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Dodeli_VALUE : 내보내기목록) {
            int kazalec_mesta = Dodeli_VALUE.indexOf('='); if (kazalec_mesta < 1) throw new 번역오류("내보내기 Dodeli_VALUE NAPAKA");
            String Ime = Dodeli_VALUE.substring(0, kazalec_mesta); 공개이름.add(Ime); 몸체들.add(izvoziti_metoda(Ime, Dodeli_VALUE.substring(kazalec_mesta + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> vnos_VALUE : 문자열들.entrySet()) {
            String Besedilo = vnos_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + vnos_VALUE.getValue() + "[] = {" + Besedilo.length());
            for (int 순번 = 0; 순번 < Besedilo.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Besedilo.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Podpora_VALUE = Files.readString(vir_pot.resolve("skupni_jezikovni_izvajalnik_Podpora.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(kopica_Word_COUNT));
        return 기계원문한국어화(Podpora_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String VIR, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ime_tabela = new HashMap<>();
        for (String Črtni : Files.readAllLines(vir_pot.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] seznaniti_VALUE = Črtni.split("\t"); ime_tabela.put(seznaniti_VALUE[0], seznaniti_VALUE[1]);
        }
        Pattern košček_izraz = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = košček_izraz.matcher(VIR); StringBuffer REZULTAT = new StringBuffer();
        while (찾개.find()) {
            String Ime = 찾개.group(), 새이름 = Ime;
            if (!Ime.startsWith("//") && !Ime.startsWith("/*") && !Ime.startsWith("\"") && !Ime.startsWith("'") && !공개이름.contains(Ime)) {
                새이름 = ime_tabela.getOrDefault(Ime, Ime);
                if (Ime.matches("a[0-9]+")) 새이름 = "Argumenti" + Ime.substring(1);
                if (Ime.matches("b[0-9]+")) 새이름 = "veja" + Ime.substring(1);
                if (범용표기) {
                    StringBuilder zapis_VALUE = new StringBuilder();
                    for (char znak_VALUE : 새이름.toCharArray()) zapis_VALUE.append(znak_VALUE < 128 ? Character.toString(znak_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)znak_VALUE));
                    새이름 = zapis_VALUE.toString();
                }
            }
            찾개.appendReplacement(REZULTAT, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(REZULTAT); return REZULTAT.toString();
    }
    String X_86_metoda_telo(metoda_Gradiva FUNCTION_VALUE, član_podatki podatki, Map<String,String> računalnik_tabela, String tarča) {
        String oznaka_VALUE_7e8f90bd = simbol("method", FUNCTION_VALUE.부분들());
        List<String> Črtni = new ArrayList<>();
        if ((podatki.dostop_vnos & 0x100) != 0) {
            String Poveži = računalnik_tabela.get(FUNCTION_VALUE.Ime + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.lastnik_VALUE.equals(tarča.equals("kernel") ? "naprava_VALUE" : "uporabnik") || Poveži == null) throw new 번역오류("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + oznaka_VALUE_7e8f90bd + ":\njmp " + Poveži;
        }
        byte[] telo_besedila = podatki.atribut_VALUE.get("Code"); if (telo_besedila == null) throw new 번역오류("FUNCTION_VALUE 몸체가 없음");
        podatki_bralec bralec_VALUE = new podatki_bralec(telo_besedila); bralec_VALUE.두바이트(); int lokalen_krajeven_COUNT = bralec_VALUE.두바이트();
        podatki_bralec ukaz_podatki = new podatki_bralec(bralec_VALUE.Branje(bralec_VALUE.네바이트()));
        if (bralec_VALUE.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 oblika_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokalen_krajeven_COUNT < oblika_VALUE.Argumenti.size()) throw new 번역오류("매개변수보다 적은 lokalen_krajeven_obseg 변수");
        Collections.addAll(Črtni,".text",".globl " + oznaka_VALUE_7e8f90bd,".type " + oznaka_VALUE_7e8f90bd + ", @function",oznaka_VALUE_7e8f90bd + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokalen_krajeven_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < oblika_VALUE.Argumenti.size(); 순번++) Collections.addAll(Črtni,"movl " + (8 + 4 * (oblika_VALUE.Argumenti.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Razred_podatki Razred_VALUE = 클래스들.get(FUNCTION_VALUE.lastnik_VALUE); Set<Integer> 경계들 = new HashSet<>(), veja_Seznam = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (ukaz_podatki.Položaj < ukaz_podatki.podatki.length) {
            int Položaj = ukaz_podatki.Položaj, Ukaz = ukaz_podatki.한바이트(); String kazalec_mesta = oznaka_VALUE_7e8f90bd + "_b" + Položaj;
            Črtni.add(kazalec_mesta + ":"); 경계들.add(Položaj);
            if (Ukaz == 0) Črtni.add("nop");
            else if (Ukaz == 1) Črtni.add("pushl $0");
            else if (Ukaz >= 2 && Ukaz <= 8) Črtni.add("pushl $" + (Ukaz - 3));
            else if (Ukaz == 16 || Ukaz == 17) Črtni.add("pushl $" + (Ukaz == 16 ? ukaz_podatki.부호한바이트() : ukaz_podatki.부호두바이트()));
            else if (Ukaz == 18 || Ukaz == 19) {
                int INDEX = Ukaz == 18 ? ukaz_podatki.한바이트() : ukaz_podatki.두바이트();
                Črtni.add("pushl $" + X_86_konstanta(Razred_VALUE,INDEX));
            } else if (Ukaz == 21 || Ukaz == 25 || (Ukaz >= 26 && Ukaz <= 29) || (Ukaz >= 42 && Ukaz <= 45) || Ukaz == 54 || Ukaz == 58 || (Ukaz >= 59 && Ukaz <= 62) || (Ukaz >= 75 && Ukaz <= 78)) {
                boolean 읽음 = Ukaz < 54; int INDEX = Ukaz == 21 || Ukaz == 25 || Ukaz == 54 || Ukaz == 58 ? ukaz_podatki.한바이트() : Ukaz - (Ukaz <= 29 ? 26 : Ukaz <= 45 ? 42 : Ukaz <= 62 ? 59 : 75);
                preveriti_lokalen_krajeven(INDEX,lokalen_krajeven_COUNT); Črtni.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Ukaz == 46) Collections.addAll(Črtni,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Ukaz == 79) Collections.addAll(Črtni,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Ukaz == 87 || Ukaz == 88) Črtni.add("addl $" + (Ukaz == 87 ? 4 : 8) + ", %esp");
            else if (Ukaz >= 89 && Ukaz <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] naročilo_Seznam = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Ukaz - 89]; 순번++) Črtni.add("popl " + 저장기들[순번]);
                for (int 순번 : naročilo_Seznam[Ukaz - 89]) Črtni.add("pushl " + 저장기들[순번]);
            } else if (Ukaz == 96 || Ukaz == 100 || Ukaz == 104 || Ukaz == 126 || Ukaz == 128 || Ukaz == 130) {
                String postopek_VALUE = Ukaz == 96 ? "addl" : Ukaz == 100 ? "subl" : Ukaz == 104 ? "imull" : Ukaz == 126 ? "andl" : Ukaz == 128 ? "orl" : "xorl";
                Collections.addAll(Črtni,"popl %ecx","popl %eax",postopek_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Ukaz == 108 || Ukaz == 112) Collections.addAll(Črtni,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + kazalec_mesta + "_divide","cmpl $0x80000000, %eax","jne " + kazalec_mesta + "_divide","xorl %edx, %edx","jmp " + kazalec_mesta + "_done",kazalec_mesta + "_divide:","cltd","idivl %ecx",kazalec_mesta + "_done:","pushl " + (Ukaz == 108 ? "%eax" : "%edx"));
            else if (Ukaz == 116) Črtni.add("negl (%esp)");
            else if (Ukaz == 120 || Ukaz == 122 || Ukaz == 124) Collections.addAll(Črtni,"popl %ecx","popl %eax",(Ukaz == 120 ? "sall" : Ukaz == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Ukaz == 132) {
                int INDEX = ukaz_podatki.한바이트(), 증가 = ukaz_podatki.부호한바이트(); preveriti_lokalen_krajeven(INDEX,lokalen_krajeven_COUNT); Črtni.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Ukaz >= 145 && Ukaz <= 147) Collections.addAll(Črtni,"popl %eax",Ukaz == 145 ? "movsbl %al, %eax" : Ukaz == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Ukaz >= 153 && Ukaz <= 166) {
                if (Ukaz <= 158) Collections.addAll(Črtni,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Črtni,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int cilj_VALUE = Položaj + ukaz_podatki.부호두바이트(); veja_Seznam.add(cilj_VALUE); Črtni.add(비교들[Ukaz - (Ukaz <= 158 ? 153 : 159)] + " " + oznaka_VALUE_7e8f90bd + "_b" + cilj_VALUE);
            } else if (Ukaz == 167 || Ukaz == 200) {
                int cilj_VALUE = Položaj + (Ukaz == 167 ? ukaz_podatki.부호두바이트() : ukaz_podatki.네바이트()); veja_Seznam.add(cilj_VALUE); Črtni.add("jmp " + oznaka_VALUE_7e8f90bd + "_b" + cilj_VALUE);
            } else if (Ukaz == 170 || Ukaz == 171) {
                while (ukaz_podatki.Položaj % 4 != 0) ukaz_podatki.한바이트();
                int privzeta_vrednost = Položaj + ukaz_podatki.네바이트(); veja_Seznam.add(privzeta_vrednost); Črtni.add("popl %eax");
                int element_COUNT, 아래 = 0;
                if (Ukaz == 170) { 아래 = ukaz_podatki.네바이트(); int 위 = ukaz_podatki.네바이트(); long 길이 = (long)위 - 아래 + 1; if (길이 < 1 || 길이 > (ukaz_podatki.podatki.length - ukaz_podatki.Položaj) / 4) throw new 번역오류("switch izrezek NAPAKA"); element_COUNT = (int)길이; }
                else { element_COUNT = ukaz_podatki.네바이트(); if (element_COUNT < 0 || element_COUNT > (ukaz_podatki.podatki.length - ukaz_podatki.Položaj) / 8) throw new 번역오류("switch Velikost NAPAKA"); }
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                    int VALUE = Ukaz == 170 ? 아래 + 순번 : ukaz_podatki.네바이트(), cilj_VALUE = Položaj + ukaz_podatki.네바이트(); veja_Seznam.add(cilj_VALUE);
                    Collections.addAll(Črtni,"cmpl $" + VALUE + ", %eax","je " + oznaka_VALUE_7e8f90bd + "_b" + cilj_VALUE);
                }
                Črtni.add("jmp " + oznaka_VALUE_7e8f90bd + "_b" + privzeta_vrednost);
            } else if (Ukaz == 172 || Ukaz == 176 || Ukaz == 177) {
                if (Ukaz != 177) Črtni.add("popl %eax"); Collections.addAll(Črtni,"leave","ret");
            } else if (Ukaz == 178 || Ukaz == 179) {
                metoda_Gradiva Gradiva = Razred_VALUE.Gradiva(ukaz_podatki.두바이트()); if (!필드들.containsKey(Gradiva)) throw new 번역오류("알 수 없는 polje_VALUE");
                Collections.addAll(Črtni,"call " + simbol("init",Gradiva.lastnik_VALUE),(Ukaz == 178 ? "pushl " : "popl ") + simbol("field",Gradiva.부분들()));
            } else if (Ukaz == 184) {
                metoda_Gradiva Gradiva = Razred_VALUE.Gradiva(ukaz_podatki.두바이트()); if (!함수들.containsKey(Gradiva)) throw new 번역오류("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Gradiva.서술); Collections.addAll(Črtni,"call " + simbol("init",Gradiva.lastnik_VALUE),"call " + simbol("method",Gradiva.부분들()));
                if (!호출형식.Argumenti.isEmpty()) Črtni.add("addl $" + 호출형식.Argumenti.size() * 4 + ", %esp");
                if (!호출형식.vrni_KR.equals("V")) Črtni.add("pushl %eax");
            } else if (Ukaz == 182) {
                metoda_Gradiva Gradiva = Razred_VALUE.Gradiva(ukaz_podatki.두바이트());
                if (Gradiva.equals(new metoda_Gradiva("java/lang/String","length","()I"))) Collections.addAll(Črtni,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Gradiva.equals(new metoda_Gradiva("java/lang/String","charAt","(I)C"))) Collections.addAll(Črtni,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 번역오류("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Ukaz == 188) {
                if (ukaz_podatki.한바이트() != 10) throw new 번역오류("new int[]만 Podpora_VALUE"); Collections.addAll(Črtni,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Ukaz == 190) Collections.addAll(Črtni,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Ukaz == 196) {
                int pripona_VALUE = ukaz_podatki.한바이트(), INDEX = ukaz_podatki.두바이트(); preveriti_lokalen_krajeven(INDEX,lokalen_krajeven_COUNT);
                if (pripona_VALUE == 21 || pripona_VALUE == 25 || pripona_VALUE == 54 || pripona_VALUE == 58) Črtni.add((pripona_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (pripona_VALUE == 132) Črtni.add("addl $" + ukaz_podatki.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new 번역오류("wide Ukaz 미지원");
            } else if (Ukaz == 198 || Ukaz == 199) {
                int cilj_VALUE = Položaj + ukaz_podatki.부호두바이트(); veja_Seznam.add(cilj_VALUE); Collections.addAll(Črtni,"popl %eax","testl %eax, %eax",(Ukaz == 198 ? "je " : "jne ") + oznaka_VALUE_7e8f90bd + "_b" + cilj_VALUE);
            } else throw new 번역오류("미지원 Ukaz: " + Ukaz);
        }
        if (!경계들.containsAll(veja_Seznam)) throw new 번역오류("Ukaz 경계가 아닌 곳으로 veja");
        Črtni.add(".size " + oznaka_VALUE_7e8f90bd + ", .-" + oznaka_VALUE_7e8f90bd); return String.join("\n",Črtni);
    }
    String X_86_konstanta(Razred_podatki podatki, int INDEX) {
        if (podatki.상수종류[INDEX] == 3) return podatki.konstanta_podatki[INDEX].toString();
        if (podatki.상수종류[INDEX] == 8) return niz_simbol(podatki.문자((Integer)podatki.konstanta_podatki[INDEX]));
        throw new 번역오류("정수와 niz_VALUE 상수만 Podpora_VALUE");
    }
    String X_86_zbir(String vnos_p, List<String> 내보냄, String tarča) throws IOException {
        Map<String,String> računalnik_tabela = new HashMap<>();
        for (String Črtni : Files.readAllLines(vir_pot.resolve("_86_računalnik_Azure_Functions.tsv"))) { String[] seznaniti_VALUE = Črtni.split("\t"); if (seznaniti_VALUE[0].equals(tarča)) računalnik_tabela.put(seznaniti_VALUE[1] + seznaniti_VALUE[2],seznaniti_VALUE[3]); }
        int kazalec_mesta = vnos_p.lastIndexOf('.'); if (kazalec_mesta < 0) throw new 번역오류("vnos_p Dodeli_VALUE NAPAKA");
        String lastnik_VALUE = vnos_p.substring(0,kazalec_mesta).replace('.','/'), metoda_vnos_ime = vnos_p.substring(kazalec_mesta + 1); metoda_Gradiva vnos_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metoda_Gradiva Gradiva = new metoda_Gradiva(lastnik_VALUE,metoda_vnos_ime,서술); if (함수들.containsKey(Gradiva)) { if (vnos_p_VALUE != null) throw new 번역오류("겹친 vnos_p"); vnos_p_VALUE = Gradiva; } }
        if (vnos_p_VALUE == null || (함수들.get(vnos_p_VALUE).dostop_vnos & 0x100) != 0) throw new 번역오류("vnos_p_VALUE FUNCTION_VALUE oblika_VALUE NAPAKA");
        List<String> Črtni = new ArrayList<>(); Črtni.add(".code32");
        for (Razred_podatki podatki : 클래스들.values()) {
            String stanje_VALUE = simbol("state",podatki.Ime), inicializirati = simbol("init",podatki.Ime);
            Collections.addAll(Črtni,".bss",".balign 4",stanje_VALUE + ": .long 0",".text",inicializirati + ":","cmpl $0, " + stanje_VALUE,"jne " + inicializirati + "_done","movl $1, " + stanje_VALUE);
            metoda_Gradiva 초기화참조 = new metoda_Gradiva(podatki.Ime,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Črtni.add("call " + simbol("method",초기화참조.부분들()));
            Collections.addAll(Črtni,"movl $2, " + stanje_VALUE,inicializirati + "_done:","ret");
            for (član_podatki polje_VALUE : podatki.polje_VALUE) {
                byte[] konstanta_VALUE = polje_VALUE.atribut_VALUE.get("ConstantValue"); String VALUE = konstanta_VALUE == null ? "0" : X_86_konstanta(podatki,new podatki_bralec(konstanta_VALUE).두바이트());
                Collections.addAll(Črtni,".data",".balign 4",simbol("field",podatki.Ime,polje_VALUE.Ime,polje_VALUE.서술) + ": .long " + VALUE);
            }
            for (član_podatki FUNCTION_VALUE : podatki.FUNCTION_VALUE) if (!FUNCTION_VALUE.Ime.equals("<init>")) Črtni.add(X_86_metoda_telo(new metoda_Gradiva(podatki.Ime,FUNCTION_VALUE.Ime,FUNCTION_VALUE.서술),FUNCTION_VALUE,računalnik_tabela,tarča));
        }
        Collections.addAll(Črtni,".text",".globl java_entry","java_entry:","call " + simbol("init",vnos_p_VALUE.lastnik_VALUE),"call " + simbol("method",vnos_p_VALUE.부분들()));
        if (vnos_p_VALUE.서술.equals("()V")) Črtni.add("xorl %eax, %eax"); Črtni.add("ret");
        for (String Dodeli_VALUE : 내보냄) {
            int ločilo_VALUE_d8ba4873 = Dodeli_VALUE.indexOf('='); if (ločilo_VALUE_d8ba4873 < 1) throw new 번역오류("내보내기 Dodeli_VALUE NAPAKA");
            String zunanji_VALUE = Dodeli_VALUE.substring(0,ločilo_VALUE_d8ba4873), FUNCTION_VALUE = Dodeli_VALUE.substring(ločilo_VALUE_d8ba4873 + 1); int sektor_KR = FUNCTION_VALUE.lastIndexOf('.');
            if (sektor_KR < 0 || !zunanji_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 simbol NAPAKA");
            String Razred_VALUE = FUNCTION_VALUE.substring(0,sektor_KR).replace('.','/'), Ime = FUNCTION_VALUE.substring(sektor_KR + 1); metoda_Gradiva izbor_VALUE = null;
            for (metoda_Gradiva Gradiva : 함수들.keySet()) if (Gradiva.lastnik_VALUE.equals(Razred_VALUE) && Gradiva.Ime.equals(Ime)) { if (izbor_VALUE != null) throw new 번역오류("겹친 내보내기 tarča"); izbor_VALUE = Gradiva; }
            if (izbor_VALUE == null) throw new 번역오류("내보낼 함수가 없음");
            Collections.addAll(Črtni,".text",".globl " + zunanji_VALUE,zunanji_VALUE + ":","call " + simbol("init",izbor_VALUE.lastnik_VALUE),"jmp " + simbol("method",izbor_VALUE.부분들()));
        }
        Črtni.add(".section .rodata");
        for (Map.Entry<String,String> vnos_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Črtni,".balign 4",vnos_VALUE.getValue() + ":",".long " + vnos_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char enota_VALUE : vnos_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(enota_VALUE)); if (!단위들.isEmpty()) Črtni.add(".long " + String.join(",",단위들));
        }
        Črtni.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Črtni) + "\n";
    }
    static void Izvedi_orodje(List<String> Ukaz) throws Exception {
        if (new ProcessBuilder(Ukaz).inheritIO().start().waitFor() != 0) throw new 번역오류("prevajati_vir NAPAKA: " + Ukaz.get(0));
    }
    static String podatki_niz(String Besedilo) { return "\"" + Besedilo.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Prevod(List<Path> 입력들, String tarča, String vnos_p, List<String> 내보냄, Path Izpis, Path vir_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Razred_pot = 임시.resolve("classes"); Files.createDirectory(Razred_pot);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Razred_pot.toString(),"-sourcepath",Razred_pot.toString(),"-d",Razred_pot.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int vir_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Izpis.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new 번역오류("Izpis 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); vir_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new 번역오류(".java 또는 .class만 Podpora_VALUE");
            }
            if (vir_COUNT > 0) Izvedi_orodje(자바명령);
            try (java.util.stream.Stream<Path> pot_Seznam = Files.walk(Razred_pot)) { pot_Seznam.filter(POT -> POT.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,tarča.equals("user") ? "user" : "kernel",262144,vir_VALUE);
            String sestaviti_VALUE = CONVERT_VALUE.X_86_zbir(vnos_p,내보냄,tarča); Files.writeString(임시.resolve("program.s"),sestaviti_VALUE,StandardCharsets.UTF_8);
            Path orodje_položaj = vir_VALUE.getParent();
            Izvedi_orodje(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Izvedi_orodje(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),orodje_položaj.resolve("skupni_jezikovni_izvajalnik_Podpora.s").toString()));
            List<String> Poveži = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (tarča.equals("kernel")) Poveži.add("-r");
            else {
                Izvedi_orodje(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),orodje_položaj.resolve(tarča.equals("user") ? "Start_uporabnik_aplikacija.s" : "리눅스시작.s").toString()));
                Collections.addAll(Poveži,"-e","_start",임시.resolve("start.o").toString());
                if (tarča.equals("user")) Collections.addAll(Poveži,"-T",orodje_položaj.resolve("uporabnik_Povezava_Krmarjenje.ld").toString());
            }
            Collections.addAll(Poveži,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Izvedi_orodje(Poveži);
            Izpis = Izpis.toAbsolutePath(); Files.createDirectories(Izpis.getParent()); Path objaviti_VALUE = Files.createTempFile(Izpis.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),objaviti_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(objaviti_VALUE,Izpis,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(objaviti_VALUE); }
            Files.setPosixFilePermissions(Izpis,java.nio.file.attribute.PosixFilePermissions.fromString(tarča.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Izpis + ".s"),sestaviti_VALUE,StandardCharsets.UTF_8);
            List<String> simbol_podatki = new ArrayList<>(), vir_podatki = new ArrayList<>();
            for (metoda_Gradiva Gradiva : CONVERT_VALUE.함수들.keySet()) simbol_podatki.add(podatki_niz(simbol("method",Gradiva.부분들())) + ":" + podatki_niz(Gradiva.lastnik_VALUE + "." + Gradiva.Ime + Gradiva.서술));
            for (Path 입력 : 입력들) {
                byte[] zgoščena_vrednost_Datoteka = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Besedilo = new StringBuilder(); for (byte VALUE : zgoščena_vrednost_Datoteka) Besedilo.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                vir_podatki.add(podatki_niz(입력.toAbsolutePath().toString()) + ":" + podatki_niz(Besedilo.toString()));
            }
            Files.writeString(Paths.get(Izpis + ".json"),"{\"target\":" + podatki_niz(tarča) + ",\"entry\":" + podatki_niz(vnos_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbol_podatki) + "},\"sources\":{" + String.join(",",vir_podatki) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> pot_Seznam = Files.walk(임시)) { for (Path POT : (Iterable<Path>)pot_Seznam.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(POT); }
        }
    }
    public static void main(String[] Argumenti) {
        try {
            String vnos_p = null, tarča = "kernel", X_86_cilj = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> pot_Seznam = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumenti.length; 순번++) {
                String VALUE = Argumenti[순번];
                switch (VALUE) {
                    case "--target": X_86_cilj = Argumenti[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Razred_VALUE.FUNCTION_VALUE -o Izpis [--target linux|kernel|user] [--profile kernel|user] [--export simbol=Razred_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": vnos_p = Argumenti[++순번]; break;
                    case "--profile": tarča = Argumenti[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumenti[++순번]); break;
                    case "--export": 내보냄.add(Argumenti[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argumenti[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new 번역오류("알 수 없는 옵션: " + VALUE); pot_Seznam.add(Paths.get(VALUE));
                }
            }
            if (vnos_p == null || 출력경로 == null || pot_Seznam.isEmpty()) throw new 번역오류("--entry, -o, Razred_VALUE 파일이 필요합니다");
            Path vir_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_cilj != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_cilj)) throw new 번역오류("알 수 없는 Izvedi_ukaz tarča");
                X_86_Prevod(pot_Seznam,X_86_cilj,vnos_p,내보냄,출력경로,vir_VALUE); return;
            }
            String VIR = new 기계어미리번역(pot_Seznam, tarča, 낱말수, vir_VALUE).ustvariti(vnos_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, VIR, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception NAPAKA) { System.err.println("prevajati_vir NAPAKA: " + NAPAKA.getMessage()); System.exit(1); }
    }
}
