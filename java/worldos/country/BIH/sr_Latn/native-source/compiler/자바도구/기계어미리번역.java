// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Razred_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Prevođenje_greška extends RuntimeException {
        Prevođenje_greška(String 설명) { super(설명); }
    }
    static final class podaci_Čitač {
        final byte[] podaci;
        int pozicija;
        podaci_Čitač(byte[] 입력자료) { podaci = 입력자료; }
        byte[] 읽기(int 길이) {
            if (길이 < 0 || 길이 > podaci.length - pozicija) throw new Prevođenje_greška("잘린 Razred_VALUE 또는 komanda podaci");
            byte[] KR = Arrays.copyOfRange(podaci, pozicija, pozicija + 길이); pozicija += 길이; return KR;
        }
        int 한바이트() { if (pozicija >= podaci.length) throw new Prevođenje_greška("잘린 komanda podaci"); return podaci[pozicija++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class član_podaci {
        final int pristup_stavka;
        final String ime, 서술;
        final Map<String, byte[]> atribut_VALUE;
        član_podaci(int pristup_VALUE, String ime_VALUE, String 서술값, Map<String, byte[]> atribut_podaci) {
            pristup_stavka = pristup_VALUE; ime = ime_VALUE; 서술 = 서술값; atribut_VALUE = atribut_podaci;
        }
    }
    static final class metod_referenca implements Comparable<metod_referenca> {
        final String vlasnik_VALUE, ime, 서술;
        metod_referenca(String 소유값, String ime_VALUE, String 서술값) { vlasnik_VALUE = 소유값; ime = ime_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{vlasnik_VALUE, ime, 서술}; }
        public int compareTo(metod_referenca ravnopravni_uređaj_VALUE) {
            int Poređenje_VALUE = vlasnik_VALUE.compareTo(ravnopravni_uređaj_VALUE.vlasnik_VALUE);
            if (Poređenje_VALUE == 0) Poređenje_VALUE = ime.compareTo(ravnopravni_uređaj_VALUE.ime);
            return Poređenje_VALUE == 0 ? 서술.compareTo(ravnopravni_uređaj_VALUE.서술) : Poređenje_VALUE;
        }
        public boolean equals(Object ravnopravni_uređaj_VALUE) { return ravnopravni_uređaj_VALUE instanceof metod_referenca && compareTo((metod_referenca) ravnopravni_uređaj_VALUE) == 0; }
        public int hashCode() { return Objects.hash(vlasnik_VALUE, ime, 서술); }
    }
    static final class Razred_podaci {
        final int[] 상수종류;
        final Object[] konstanta_podaci;
        final String ime;
        final List<član_podaci> vrednost_polja, FUNCTION_VALUE;
        Razred_podaci(Path putanja) throws IOException {
            podaci_Čitač Čitač_VALUE = new podaci_Čitač(Files.readAllBytes(putanja));
            if (Čitač_VALUE.네바이트() != 0xcafebabe) throw new Prevođenje_greška("Java Razred_VALUE 표식이 아님");
            Čitač_VALUE.읽기(4);
            int stavka_COUNT = Čitač_VALUE.두바이트(); 상수종류 = new int[stavka_COUNT]; konstanta_podaci = new Object[stavka_COUNT];
            for (int 순번 = 1; 순번 < stavka_COUNT; 순번++) {
                int 종류 = Čitač_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int 길이 = Čitač_VALUE.두바이트();
                        byte[] znak_bafer = Čitač_VALUE.읽기(길이), 길이붙인자료 = new byte[길이 + 2];
                        길이붙인자료[0] = (byte)(길이 >> 8); 길이붙인자료[1] = (byte)길이;
                        System.arraycopy(znak_bafer, 0, 길이붙인자료, 2, 길이);
                        konstanta_podaci[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstanta_podaci[순번] = Čitač_VALUE.네바이트(); break;
                    case 4: Čitač_VALUE.읽기(4); break;
                    case 5: case 6: Čitač_VALUE.읽기(8); 순번++; break;
                    case 7: case 8: case 16: konstanta_podaci[순번] = Čitač_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstanta_podaci[순번] = new int[]{Čitač_VALUE.두바이트(), Čitač_VALUE.두바이트()}; break;
                    case 15: konstanta_podaci[순번] = new int[]{Čitač_VALUE.한바이트(), Čitač_VALUE.두바이트()}; break;
                    default: throw new Prevođenje_greška("지원하지 않는 konstanta_VALUE 종류: " + 종류);
                }
            }
            Čitač_VALUE.두바이트(); ime = ime_klase(Čitač_VALUE.두바이트());
            if (!ime_klase(Čitač_VALUE.두바이트()).equals("java/lang/Object") || Čitač_VALUE.두바이트() != 0)
                throw new Prevođenje_greška(ime + ": 상속 및 인터페이스 미지원");
            vrednost_polja = 멤버읽기(Čitač_VALUE); FUNCTION_VALUE = 멤버읽기(Čitač_VALUE); 속성읽기(Čitač_VALUE);
            if (Čitač_VALUE.pozicija != Čitač_VALUE.podaci.length) throw new Prevođenje_greška("Razred_VALUE 뒤에 남은 podaci");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Prevođenje_greška("문자 konstanta_VALUE INDEX greška");
            return (String) konstanta_podaci[INDEX];
        }
        String ime_klase(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Prevođenje_greška("Razred_VALUE referenca greška");
            return 문자((Integer)konstanta_podaci[INDEX]);
        }
        metod_referenca referenca(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Prevođenje_greška("멤버 referenca greška");
            int[] upariti_VALUE = (int[])konstanta_podaci[INDEX], ime_upariti = (int[])konstanta_podaci[upariti_VALUE[1]];
            return new metod_referenca(ime_klase(upariti_VALUE[0]), 문자(ime_upariti[0]), 문자(ime_upariti[1]));
        }
        Map<String, byte[]> 속성읽기(podaci_Čitač Čitač_VALUE) {
            Map<String, byte[]> KR = new LinkedHashMap<>();
            int stavka_COUNT = Čitač_VALUE.두바이트();
            for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) {
                String atribut_ime = 문자(Čitač_VALUE.두바이트()); byte[] VALUE = Čitač_VALUE.읽기(Čitač_VALUE.네바이트());
                if (KR.put(atribut_ime, VALUE) != null) throw new Prevođenje_greška("겹친 atribut_VALUE: " + atribut_ime);
            }
            return KR;
        }
        List<član_podaci> 멤버읽기(podaci_Čitač Čitač_VALUE) {
            List<član_podaci> KR = new ArrayList<>(); int stavka_COUNT = Čitač_VALUE.두바이트();
            for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) {
                int pristup_stavka = Čitač_VALUE.두바이트(); String metod_stavka_ime = 문자(Čitač_VALUE.두바이트()), 서술 = 문자(Čitač_VALUE.두바이트());
                KR.add(new član_podaci(pristup_stavka, metod_stavka_ime, 서술, 속성읽기(Čitač_VALUE)));
            }
            return KR;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String vratiti_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Prevođenje_greška("FUNCTION_VALUE 서술 greška: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Prevođenje_greška("FUNCTION_VALUE 서술 greška: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Prevođenje_greška("FUNCTION_VALUE 서술 greška: " + 서술);
            vratiti_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> KR = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int pozicija = 0; pozicija < 서술.length();) {
            String izbor_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, pozicija)) { izbor_VALUE = format_VALUE; break; }
            if (izbor_VALUE == null) throw new Prevođenje_greška("지원하지 않는 tip_podataka: " + 서술);
            KR.add(izbor_VALUE); pozicija += izbor_VALUE.length();
        }
        return KR;
    }
    static String simbol(String 종류, String... 부분들) {
        try {
            byte[] heš_Datoteka = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", heš_Datoteka[순번] & 255));
            return SMS.toString();
        } catch (Exception greška) { throw new Prevođenje_greška(greška.toString()); }
    }
    final Map<String, Razred_podaci> 클래스들 = new TreeMap<>();
    final Map<metod_referenca, član_podaci> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), računar_Azure_Functions_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, računar_Razred;
    final int 동적기억낱말수;
    final Path resurs_putanja;
    기계어미리번역(List<Path> putanja_Lista, String cilj, int 낱말수, Path resurs_VALUE) throws IOException {
        if ((!cilj.equals("kernel") && !cilj.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Prevođenje_greška("Izvrši_komanda cilj 또는 Memorija_VALUE adresa_oblast promeniti_veličinu greška");
        실행대상 = cilj; 동적기억낱말수 = 낱말수; resurs_putanja = resurs_VALUE;
        // 이 이름도 국가별 izvor_stablo generisati 시 해당 언어로 옮긴다.
        računar_Razred = cilj.equals("kernel") ? "Tabla" : "korisnik";
        for (String red : Files.readAllLines(resurs_VALUE.resolve("računar_Azure_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = red.split("\t", -1);
            if (부분들.length != 4) throw new Prevođenje_greška("računar FUNCTION_VALUE podaci greška");
            if (부분들[0].equals(cilj)) računar_Azure_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path putanja : putanja_Lista) {
            Razred_podaci podaci = new Razred_podaci(putanja);
            if (클래스들.put(podaci.ime, podaci) != null) throw new Prevođenje_greška("중복 Razred_VALUE: " + podaci.ime);
            for (član_podaci vrednost_polja : podaci.vrednost_polja) {
                if ((vrednost_polja.pristup_stavka & 8) == 0 || 형식읽기(vrednost_polja.서술).equals(Collections.singletonList("V"))) throw new Prevođenje_greška("정적 필드만 Podrška_VALUE");
                if (필드들.put(new metod_referenca(podaci.ime, vrednost_polja.ime, vrednost_polja.서술), vrednost_polja) != null) throw new Prevođenje_greška("중복 vrednost_polja");
            }
            for (član_podaci FUNCTION_VALUE : podaci.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.ime.equals("<init>")) continue;
                if ((FUNCTION_VALUE.pristup_stavka & 8) == 0 || (FUNCTION_VALUE.pristup_stavka & (0x20 | 0x400)) != 0) throw new Prevođenje_greška("정적 비동기화 함수만 Podrška_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new metod_referenca(podaci.ime, FUNCTION_VALUE.ime, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Prevođenje_greška("중복 FUNCTION_VALUE");
            }
        }
    }
    String niska_simbol(String SMS) { return 문자열들.computeIfAbsent(SMS, VALUE -> "j_text_" + 문자열들.size()); }
    String konstanta_izraz(Razred_podaci podaci, int INDEX) {
        if (INDEX < 1 || INDEX >= podaci.상수종류.length) throw new Prevođenje_greška("konstanta_VALUE INDEX klip greška");
        if (podaci.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + podaci.konstanta_podaci[INDEX] + ")";
        if (podaci.상수종류[INDEX] == 8) return "(word)" + niska_simbol(podaci.문자((Integer)podaci.konstanta_podaci[INDEX]));
        throw new Prevođenje_greška("정수와 niska_VALUE 상수만 Podrška_VALUE");
    }
    String 함수원형(metod_referenca referenca) {
        List<String> 인수들 = new ArrayList<>(); int stavka_COUNT = new 함수형식(referenca.서술).인수.size();
        for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbol("method", referenca.부분들()) + "(" + (stavka_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void proveriti_lokalni(int INDEX, int lokalni_promenljiva_COUNT) { if (INDEX < 0 || INDEX >= lokalni_promenljiva_COUNT) throw new Prevođenje_greška("lokalni_skup promenljiva_VALUE INDEX klip greška"); }
    void 분기넣기(List<String> 출력, Set<Integer> grana_Lista, int pozicija, int 이동량, String stanje) {
        int odredište_VALUE = pozicija + 이동량; grana_Lista.add(odredište_VALUE);
        출력.add((stanje == null ? "" : "if (" + stanje + ") ") + "goto b" + odredište_VALUE + ";");
    }
    String metod_telo(metod_referenca FUNCTION_VALUE, član_podaci podaci) {
        byte[] telo_podaci = podaci.atribut_VALUE.get("Code"); if (telo_podaci == null) throw new Prevođenje_greška("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.ime);
        podaci_Čitač Čitač_VALUE = new podaci_Čitač(telo_podaci); int 쌓임깊이 = Čitač_VALUE.두바이트(), lokalni_promenljiva_COUNT = Čitač_VALUE.두바이트();
        podaci_Čitač komanda_podaci = new podaci_Čitač(Čitač_VALUE.읽기(Čitač_VALUE.네바이트()));
        if (Čitač_VALUE.두바이트() != 0) throw new Prevođenje_greška("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokalni_promenljiva_COUNT < format_VALUE.인수.size()) throw new Prevođenje_greška("매개변수보다 적은 lokalni_skup promenljiva_VALUE");
        Razred_podaci Razred_VALUE = 클래스들.get(FUNCTION_VALUE.vlasnik_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(FUNCTION_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(lokalni_promenljiva_COUNT, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), grana_Lista = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (komanda_podaci.pozicija < komanda_podaci.podaci.length) {
            int pozicija = komanda_podaci.pozicija, komanda = komanda_podaci.한바이트(); 경계들.add(pozicija); 출력.add("b" + pozicija + ":;");
            if (komanda == 0) continue;
            if (komanda == 1) 출력.add("PUSH(0);");
            else if (komanda >= 2 && komanda <= 8) 출력.add("PUSH((uint32_t)(" + (komanda - 3) + "));");
            else if (komanda == 16 || komanda == 17) 출력.add("PUSH((uint32_t)(" + (komanda == 16 ? komanda_podaci.부호한바이트() : komanda_podaci.부호두바이트()) + "));");
            else if (komanda == 18 || komanda == 19) 출력.add("PUSH(" + konstanta_izraz(Razred_VALUE, komanda == 18 ? komanda_podaci.한바이트() : komanda_podaci.두바이트()) + ");");
            else if (komanda == 21 || komanda == 25 || (komanda >= 26 && komanda <= 29) || (komanda >= 42 && komanda <= 45)) {
                int INDEX = komanda == 21 || komanda == 25 ? komanda_podaci.한바이트() : komanda - (komanda <= 29 ? 26 : 42);
                proveriti_lokalni(INDEX, lokalni_promenljiva_COUNT); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (komanda == 54 || komanda == 58 || (komanda >= 59 && komanda <= 62) || (komanda >= 75 && komanda <= 78)) {
                int INDEX = komanda == 54 || komanda == 58 ? komanda_podaci.한바이트() : komanda - (komanda <= 62 ? 59 : 75);
                proveriti_lokalni(INDEX, lokalni_promenljiva_COUNT); 출력.add("l[" + INDEX + "] = POP();");
            } else if (komanda == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (komanda == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (komanda == 87 || komanda == 88) 출력.add(komanda == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (komanda >= 89 && komanda <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] poručiti_Lista = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[komanda - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : poručiti_Lista[komanda - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (komanda == 96 || komanda == 100 || komanda == 104 || komanda == 126 || komanda == 128 || komanda == 130) {
                String operacija_VALUE = komanda == 96 ? "+" : komanda == 100 ? "-" : komanda == 104 ? "*" : komanda == 126 ? "&" : komanda == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operacija_VALUE + " (uint32_t)b);");
            } else if (komanda == 108 || komanda == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (komanda == 112 ? 1 : 0) + "));");
            else if (komanda == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (komanda == 120 || komanda == 122 || komanda == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (komanda == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (komanda == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (komanda == 132) {
                int INDEX = komanda_podaci.한바이트(), 증가량 = komanda_podaci.부호한바이트(); proveriti_lokalni(INDEX, lokalni_promenljiva_COUNT);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (komanda >= 145 && komanda <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (komanda == 145 ? "int8_t" : komanda == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (komanda >= 153 && komanda <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, grana_Lista, pozicija, komanda_podaci.부호두바이트(), "(int32_t)a " + 비교들[komanda - 153] + " 0");
            } else if (komanda >= 159 && komanda <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, grana_Lista, pozicija, komanda_podaci.부호두바이트(), komanda >= 165 ? "a " + 비교들[komanda - 159] + " b" : "(int32_t)a " + 비교들[komanda - 159] + " (int32_t)b");
            } else if (komanda == 167 || komanda == 200) 분기넣기(출력, grana_Lista, pozicija, komanda == 167 ? komanda_podaci.부호두바이트() : komanda_podaci.네바이트(), null);
            else if (komanda == 170 || komanda == 171) {
                while (komanda_podaci.pozicija % 4 != 0) komanda_podaci.한바이트();
                int podrazumevana_vrednost = komanda_podaci.네바이트(); 출력.add("a = POP();");
                if (komanda == 170) {
                    int 아래 = komanda_podaci.네바이트(), 위 = komanda_podaci.네바이트(); long stavka_COUNT = (long)위 - 아래 + 1;
                    if (stavka_COUNT < 1 || stavka_COUNT > (komanda_podaci.podaci.length - komanda_podaci.pozicija) / 4) throw new Prevođenje_greška("switch klip greška");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, grana_Lista, pozicija, komanda_podaci.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int stavka_COUNT = komanda_podaci.네바이트(), čeona_kamera_podaci = 0;
                    if (stavka_COUNT < 0 || stavka_COUNT > (komanda_podaci.podaci.length - komanda_podaci.pozicija) / 8) throw new Prevođenje_greška("switch promeniti_veličinu greška");
                    for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) {
                        int VALUE = komanda_podaci.네바이트(); if (순번 > 0 && VALUE <= čeona_kamera_podaci) throw new Prevođenje_greška("switch poručiti_VALUE greška"); čeona_kamera_podaci = VALUE;
                        분기넣기(출력, grana_Lista, pozicija, komanda_podaci.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, grana_Lista, pozicija, podrazumevana_vrednost, null);
            } else if (komanda == 172 || komanda == 176 || komanda == 177) 출력.add("return " + (komanda == 177 ? "0" : "POP()") + ";");
            else if (komanda == 178 || komanda == 179) {
                metod_referenca referenca = Razred_VALUE.referenca(komanda_podaci.두바이트()); if (!필드들.containsKey(referenca)) throw new Prevođenje_greška("알 수 없는 vrednost_polja");
                출력.add(simbol("init", referenca.vlasnik_VALUE) + "();"); String vrednost_polja = simbol("field", referenca.부분들());
                출력.add(komanda == 178 ? "PUSH(" + vrednost_polja + ");" : vrednost_polja + " = POP();");
            } else if (komanda == 184) {
                metod_referenca referenca = Razred_VALUE.referenca(komanda_podaci.두바이트()); if (!함수들.containsKey(referenca)) throw new Prevođenje_greška("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(referenca.서술); int stavka_COUNT = 호출형식.인수.size();
                출력.add(simbol("init", referenca.vlasnik_VALUE) + "();"); 출력.add("if(sp < " + stavka_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + stavka_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + simbol("method", referenca.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.vratiti_KR.equals("V")) 출력.add("PUSH(a);");
            } else if (komanda == 182) {
                metod_referenca referenca = Razred_VALUE.referenca(komanda_podaci.두바이트());
                if (referenca.equals(new metod_referenca("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (referenca.equals(new metod_referenca("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Prevođenje_greška("가상 FUNCTION_VALUE 호출 미지원");
            } else if (komanda == 188) {
                if (komanda_podaci.한바이트() != 10) throw new Prevođenje_greška("new int[]만 Podrška_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (komanda == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (komanda == 196) {
                int ekstenzija_VALUE = komanda_podaci.한바이트(), INDEX = komanda_podaci.두바이트(); proveriti_lokalni(INDEX, lokalni_promenljiva_COUNT);
                if (ekstenzija_VALUE == 21 || ekstenzija_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (ekstenzija_VALUE == 54 || ekstenzija_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (ekstenzija_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + komanda_podaci.부호두바이트() + ");");
                else throw new Prevođenje_greška("미지원 wide komanda");
            } else if (komanda == 198 || komanda == 199) {
                출력.add("a = POP();"); 분기넣기(출력, grana_Lista, pozicija, komanda_podaci.부호두바이트(), "a " + (komanda == 198 ? "==" : "!=") + " 0");
            } else throw new Prevođenje_greška(FUNCTION_VALUE.vlasnik_VALUE + "." + FUNCTION_VALUE.ime + ", bajt_VALUE " + pozicija + ": 미지원 komanda " + komanda);
        }
        if (!경계들.containsAll(grana_Lista)) throw new Prevođenje_greška("komanda 경계가 아닌 곳으로 grana");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String izvesti_metod(String Veza_simbol, String cilj, boolean 진입점여부) {
        int indeks_pozicije = cilj.lastIndexOf('.'); if (indeks_pozicije < 0 || !Veza_simbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Prevođenje_greška("내보내기 Dodeli_VALUE greška");
        String vlasnik_VALUE = cilj.substring(0, indeks_pozicije).replace('.', '/'), ime = cilj.substring(indeks_pozicije + 1); metod_referenca izbor_VALUE = null;
        for (metod_referenca referenca : 함수들.keySet()) if (referenca.vlasnik_VALUE.equals(vlasnik_VALUE) && referenca.ime.equals(ime)) {
            if (izbor_VALUE != null) throw new Prevođenje_greška("겹친 내보내기 cilj"); izbor_VALUE = referenca;
        }
        if (izbor_VALUE == null || (함수들.get(izbor_VALUE).pristup_stavka & 0x100) != 0) throw new Prevođenje_greška("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 format_VALUE = new 함수형식(izbor_VALUE.서술);
        if ((진입점여부 && !format_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.vratiti_KR)) throw new Prevođenje_greška("stavka_p_VALUE 또는 C 경계 format_VALUE greška");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) {
            if (!format_VALUE.인수.get(순번).equals("I")) throw new Prevođenje_greška("C 경계는 int 인수만 Podrška_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.vratiti_KR.equals("V") ? "void " : "int32_t ") + Veza_simbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbol("init", izbor_VALUE.vlasnik_VALUE) + "(); " + (format_VALUE.vratiti_KR.equals("V") ? "" : "return (int32_t)") + simbol("method", izbor_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generisati(String stavka_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metod_referenca, član_podaci> stavka_VALUE : 함수들.entrySet()) {
            metod_referenca referenca = stavka_VALUE.getKey(); član_podaci podaci = stavka_VALUE.getValue(); 선언들.add(함수원형(referenca) + ";");
            if ((podaci.pristup_stavka & 0x100) != 0) {
                String veze = računar_Azure_Functions_c3a8e64a.get(referenca.ime + referenca.서술);
                if (!referenca.vlasnik_VALUE.equals(računar_Razred) || veze == null) throw new Prevođenje_greška("허용되지 않은 native FUNCTION_VALUE: " + referenca.ime);
                int stavka_COUNT = new 함수형식(referenca.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + veze + "(" + (stavka_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(stavka_COUNT, "word"))) + ");");
                몸체들.add(함수원형(referenca) + " { return " + veze + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metod_telo(referenca, podaci));
        }
        for (Map.Entry<metod_referenca, član_podaci> stavka_VALUE : 필드들.entrySet()) {
            metod_referenca referenca = stavka_VALUE.getKey(); byte[] konstanta_VALUE = stavka_VALUE.getValue().atribut_VALUE.get("ConstantValue");
            String VALUE = konstanta_VALUE == null ? "0" : konstanta_izraz(클래스들.get(referenca.vlasnik_VALUE), new podaci_Čitač(konstanta_VALUE).두바이트());
            필드선언들.add("static word " + simbol("field", referenca.부분들()) + " = " + VALUE + ";");
        }
        for (String ime : 클래스들.keySet()) {
            String 초기화 = simbol("init", ime), Status_VALUE = simbol("state", ime);
            선언들.add("static void " + 초기화 + "(void);"); 필드선언들.add("static unsigned " + Status_VALUE + ";");
            metod_referenca referenca = new metod_referenca(ime, "<clinit>", "()V");
            몸체들.add("static void " + 초기화 + "(void) { if(" + Status_VALUE + ") return; " + Status_VALUE + " = 1; " + (함수들.containsKey(referenca) ? simbol("method", referenca.부분들()) + "(); " : "") + Status_VALUE + " = 2; }");
        }
        몸체들.add(izvesti_metod("java_entry", stavka_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Dodeli_VALUE : 내보내기목록) {
            int indeks_pozicije = Dodeli_VALUE.indexOf('='); if (indeks_pozicije < 1) throw new Prevođenje_greška("내보내기 Dodeli_VALUE greška");
            String ime = Dodeli_VALUE.substring(0, indeks_pozicije); 공개이름.add(ime); 몸체들.add(izvesti_metod(ime, Dodeli_VALUE.substring(indeks_pozicije + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> stavka_VALUE : 문자열들.entrySet()) {
            String SMS = stavka_VALUE.getKey(); StringBuilder niz_VALUE = new StringBuilder("static const word " + stavka_VALUE.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) niz_VALUE.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(niz_VALUE.append("};").toString());
        }
        String Podrška_VALUE = Files.readString(resurs_putanja.resolve("CLR_komponenta_Podrška.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Podrška_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String izvor, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ime_tabela = new HashMap<>();
        for (String red : Files.readAllLines(resurs_putanja.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] upariti_VALUE = red.split("\t"); ime_tabela.put(upariti_VALUE[0], upariti_VALUE[1]);
        }
        Pattern odlomak_izraz = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = odlomak_izraz.matcher(izvor); StringBuffer KR = new StringBuffer();
        while (찾개.find()) {
            String ime = 찾개.group(), 새이름 = ime;
            if (!ime.startsWith("//") && !ime.startsWith("/*") && !ime.startsWith("\"") && !ime.startsWith("'") && !공개이름.contains(ime)) {
                새이름 = ime_tabela.getOrDefault(ime, ime);
                if (ime.matches("a[0-9]+")) 새이름 = "인수" + ime.substring(1);
                if (ime.matches("b[0-9]+")) 새이름 = "grana" + ime.substring(1);
                if (범용표기) {
                    StringBuilder notacija_VALUE = new StringBuilder();
                    for (char znak_VALUE : 새이름.toCharArray()) notacija_VALUE.append(znak_VALUE < 128 ? Character.toString(znak_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)znak_VALUE));
                    새이름 = notacija_VALUE.toString();
                }
            }
            찾개.appendReplacement(KR, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(KR); return KR.toString();
    }
    String X_86_metod_telo(metod_referenca FUNCTION_VALUE, član_podaci podaci, Map<String,String> računar_tabela, String cilj) {
        String označivač_VALUE = simbol("method", FUNCTION_VALUE.부분들());
        List<String> red = new ArrayList<>();
        if ((podaci.pristup_stavka & 0x100) != 0) {
            String veze = računar_tabela.get(FUNCTION_VALUE.ime + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.vlasnik_VALUE.equals(cilj.equals("kernel") ? "uređaj_VALUE" : "korisnik") || veze == null) throw new Prevođenje_greška("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + označivač_VALUE + ":\njmp " + veze;
        }
        byte[] telo_teksta = podaci.atribut_VALUE.get("Code"); if (telo_teksta == null) throw new Prevođenje_greška("FUNCTION_VALUE 몸체가 없음");
        podaci_Čitač Čitač_VALUE = new podaci_Čitač(telo_teksta); Čitač_VALUE.두바이트(); int lokalni_COUNT = Čitač_VALUE.두바이트();
        podaci_Čitač komanda_podaci = new podaci_Čitač(Čitač_VALUE.읽기(Čitač_VALUE.네바이트()));
        if (Čitač_VALUE.두바이트() != 0) throw new Prevođenje_greška("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokalni_COUNT < format_VALUE.인수.size()) throw new Prevođenje_greška("매개변수보다 적은 lokalni_skup promenljiva_VALUE");
        Collections.addAll(red,".text",".globl " + označivač_VALUE,".type " + označivač_VALUE + ", @function",označivač_VALUE + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokalni_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) Collections.addAll(red,"movl " + (8 + 4 * (format_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Razred_podaci Razred_VALUE = 클래스들.get(FUNCTION_VALUE.vlasnik_VALUE); Set<Integer> 경계들 = new HashSet<>(), grana_Lista = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (komanda_podaci.pozicija < komanda_podaci.podaci.length) {
            int pozicija = komanda_podaci.pozicija, komanda = komanda_podaci.한바이트(); String indeks_pozicije = označivač_VALUE + "_b" + pozicija;
            red.add(indeks_pozicije + ":"); 경계들.add(pozicija);
            if (komanda == 0) red.add("nop");
            else if (komanda == 1) red.add("pushl $0");
            else if (komanda >= 2 && komanda <= 8) red.add("pushl $" + (komanda - 3));
            else if (komanda == 16 || komanda == 17) red.add("pushl $" + (komanda == 16 ? komanda_podaci.부호한바이트() : komanda_podaci.부호두바이트()));
            else if (komanda == 18 || komanda == 19) {
                int INDEX = komanda == 18 ? komanda_podaci.한바이트() : komanda_podaci.두바이트();
                red.add("pushl $" + X_86_konstanta(Razred_VALUE,INDEX));
            } else if (komanda == 21 || komanda == 25 || (komanda >= 26 && komanda <= 29) || (komanda >= 42 && komanda <= 45) || komanda == 54 || komanda == 58 || (komanda >= 59 && komanda <= 62) || (komanda >= 75 && komanda <= 78)) {
                boolean 읽음 = komanda < 54; int INDEX = komanda == 21 || komanda == 25 || komanda == 54 || komanda == 58 ? komanda_podaci.한바이트() : komanda - (komanda <= 29 ? 26 : komanda <= 45 ? 42 : komanda <= 62 ? 59 : 75);
                proveriti_lokalni(INDEX,lokalni_COUNT); red.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (komanda == 46) Collections.addAll(red,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (komanda == 79) Collections.addAll(red,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (komanda == 87 || komanda == 88) red.add("addl $" + (komanda == 87 ? 4 : 8) + ", %esp");
            else if (komanda >= 89 && komanda <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] poručiti_Lista = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[komanda - 89]; 순번++) red.add("popl " + 저장기들[순번]);
                for (int 순번 : poručiti_Lista[komanda - 89]) red.add("pushl " + 저장기들[순번]);
            } else if (komanda == 96 || komanda == 100 || komanda == 104 || komanda == 126 || komanda == 128 || komanda == 130) {
                String operacija_VALUE = komanda == 96 ? "addl" : komanda == 100 ? "subl" : komanda == 104 ? "imull" : komanda == 126 ? "andl" : komanda == 128 ? "orl" : "xorl";
                Collections.addAll(red,"popl %ecx","popl %eax",operacija_VALUE + " %ecx, %eax","pushl %eax");
            } else if (komanda == 108 || komanda == 112) Collections.addAll(red,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + indeks_pozicije + "_divide","cmpl $0x80000000, %eax","jne " + indeks_pozicije + "_divide","xorl %edx, %edx","jmp " + indeks_pozicije + "_done",indeks_pozicije + "_divide:","cltd","idivl %ecx",indeks_pozicije + "_done:","pushl " + (komanda == 108 ? "%eax" : "%edx"));
            else if (komanda == 116) red.add("negl (%esp)");
            else if (komanda == 120 || komanda == 122 || komanda == 124) Collections.addAll(red,"popl %ecx","popl %eax",(komanda == 120 ? "sall" : komanda == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (komanda == 132) {
                int INDEX = komanda_podaci.한바이트(), 증가 = komanda_podaci.부호한바이트(); proveriti_lokalni(INDEX,lokalni_COUNT); red.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (komanda >= 145 && komanda <= 147) Collections.addAll(red,"popl %eax",komanda == 145 ? "movsbl %al, %eax" : komanda == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (komanda >= 153 && komanda <= 166) {
                if (komanda <= 158) Collections.addAll(red,"popl %eax","testl %eax, %eax");
                else Collections.addAll(red,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int odredište_VALUE = pozicija + komanda_podaci.부호두바이트(); grana_Lista.add(odredište_VALUE); red.add(비교들[komanda - (komanda <= 158 ? 153 : 159)] + " " + označivač_VALUE + "_b" + odredište_VALUE);
            } else if (komanda == 167 || komanda == 200) {
                int odredište_VALUE = pozicija + (komanda == 167 ? komanda_podaci.부호두바이트() : komanda_podaci.네바이트()); grana_Lista.add(odredište_VALUE); red.add("jmp " + označivač_VALUE + "_b" + odredište_VALUE);
            } else if (komanda == 170 || komanda == 171) {
                while (komanda_podaci.pozicija % 4 != 0) komanda_podaci.한바이트();
                int podrazumevana_vrednost = pozicija + komanda_podaci.네바이트(); grana_Lista.add(podrazumevana_vrednost); red.add("popl %eax");
                int stavka_COUNT, 아래 = 0;
                if (komanda == 170) { 아래 = komanda_podaci.네바이트(); int 위 = komanda_podaci.네바이트(); long 길이 = (long)위 - 아래 + 1; if (길이 < 1 || 길이 > (komanda_podaci.podaci.length - komanda_podaci.pozicija) / 4) throw new Prevođenje_greška("switch klip greška"); stavka_COUNT = (int)길이; }
                else { stavka_COUNT = komanda_podaci.네바이트(); if (stavka_COUNT < 0 || stavka_COUNT > (komanda_podaci.podaci.length - komanda_podaci.pozicija) / 8) throw new Prevođenje_greška("switch promeniti_veličinu greška"); }
                for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) {
                    int VALUE = komanda == 170 ? 아래 + 순번 : komanda_podaci.네바이트(), odredište_VALUE = pozicija + komanda_podaci.네바이트(); grana_Lista.add(odredište_VALUE);
                    Collections.addAll(red,"cmpl $" + VALUE + ", %eax","je " + označivač_VALUE + "_b" + odredište_VALUE);
                }
                red.add("jmp " + označivač_VALUE + "_b" + podrazumevana_vrednost);
            } else if (komanda == 172 || komanda == 176 || komanda == 177) {
                if (komanda != 177) red.add("popl %eax"); Collections.addAll(red,"leave","ret");
            } else if (komanda == 178 || komanda == 179) {
                metod_referenca referenca = Razred_VALUE.referenca(komanda_podaci.두바이트()); if (!필드들.containsKey(referenca)) throw new Prevođenje_greška("알 수 없는 vrednost_polja");
                Collections.addAll(red,"call " + simbol("init",referenca.vlasnik_VALUE),(komanda == 178 ? "pushl " : "popl ") + simbol("field",referenca.부분들()));
            } else if (komanda == 184) {
                metod_referenca referenca = Razred_VALUE.referenca(komanda_podaci.두바이트()); if (!함수들.containsKey(referenca)) throw new Prevođenje_greška("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(referenca.서술); Collections.addAll(red,"call " + simbol("init",referenca.vlasnik_VALUE),"call " + simbol("method",referenca.부분들()));
                if (!호출형식.인수.isEmpty()) red.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.vratiti_KR.equals("V")) red.add("pushl %eax");
            } else if (komanda == 182) {
                metod_referenca referenca = Razred_VALUE.referenca(komanda_podaci.두바이트());
                if (referenca.equals(new metod_referenca("java/lang/String","length","()I"))) Collections.addAll(red,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (referenca.equals(new metod_referenca("java/lang/String","charAt","(I)C"))) Collections.addAll(red,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Prevođenje_greška("가상 FUNCTION_VALUE 호출 미지원");
            } else if (komanda == 188) {
                if (komanda_podaci.한바이트() != 10) throw new Prevođenje_greška("new int[]만 Podrška_VALUE"); Collections.addAll(red,"popl %eax","call rt_new_array","pushl %eax");
            } else if (komanda == 190) Collections.addAll(red,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (komanda == 196) {
                int ekstenzija_VALUE = komanda_podaci.한바이트(), INDEX = komanda_podaci.두바이트(); proveriti_lokalni(INDEX,lokalni_COUNT);
                if (ekstenzija_VALUE == 21 || ekstenzija_VALUE == 25 || ekstenzija_VALUE == 54 || ekstenzija_VALUE == 58) red.add((ekstenzija_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (ekstenzija_VALUE == 132) red.add("addl $" + komanda_podaci.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Prevođenje_greška("wide komanda 미지원");
            } else if (komanda == 198 || komanda == 199) {
                int odredište_VALUE = pozicija + komanda_podaci.부호두바이트(); grana_Lista.add(odredište_VALUE); Collections.addAll(red,"popl %eax","testl %eax, %eax",(komanda == 198 ? "je " : "jne ") + označivač_VALUE + "_b" + odredište_VALUE);
            } else throw new Prevođenje_greška("미지원 komanda: " + komanda);
        }
        if (!경계들.containsAll(grana_Lista)) throw new Prevođenje_greška("komanda 경계가 아닌 곳으로 grana");
        red.add(".size " + označivač_VALUE + ", .-" + označivač_VALUE); return String.join("\n",red);
    }
    String X_86_konstanta(Razred_podaci podaci, int INDEX) {
        if (podaci.상수종류[INDEX] == 3) return podaci.konstanta_podaci[INDEX].toString();
        if (podaci.상수종류[INDEX] == 8) return niska_simbol(podaci.문자((Integer)podaci.konstanta_podaci[INDEX]));
        throw new Prevođenje_greška("정수와 niska_VALUE 상수만 Podrška_VALUE");
    }
    String X_86_sklop(String stavka_p, List<String> 내보냄, String cilj) throws IOException {
        Map<String,String> računar_tabela = new HashMap<>();
        for (String red : Files.readAllLines(resurs_putanja.resolve("_86_računar_Azure_Functions.tsv"))) { String[] upariti_VALUE = red.split("\t"); if (upariti_VALUE[0].equals(cilj)) računar_tabela.put(upariti_VALUE[1] + upariti_VALUE[2],upariti_VALUE[3]); }
        int indeks_pozicije = stavka_p.lastIndexOf('.'); if (indeks_pozicije < 0) throw new Prevođenje_greška("stavka_p Dodeli_VALUE greška");
        String vlasnik_VALUE = stavka_p.substring(0,indeks_pozicije).replace('.','/'), metod_stavka_ime = stavka_p.substring(indeks_pozicije + 1); metod_referenca stavka_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metod_referenca referenca = new metod_referenca(vlasnik_VALUE,metod_stavka_ime,서술); if (함수들.containsKey(referenca)) { if (stavka_p_VALUE != null) throw new Prevođenje_greška("겹친 stavka_p"); stavka_p_VALUE = referenca; } }
        if (stavka_p_VALUE == null || (함수들.get(stavka_p_VALUE).pristup_stavka & 0x100) != 0) throw new Prevođenje_greška("stavka_p_VALUE FUNCTION_VALUE format_VALUE greška");
        List<String> red = new ArrayList<>(); red.add(".code32");
        for (Razred_podaci podaci : 클래스들.values()) {
            String Status_VALUE = simbol("state",podaci.ime), 초기화 = simbol("init",podaci.ime);
            Collections.addAll(red,".bss",".balign 4",Status_VALUE + ": .long 0",".text",초기화 + ":","cmpl $0, " + Status_VALUE,"jne " + 초기화 + "_done","movl $1, " + Status_VALUE);
            metod_referenca 초기화참조 = new metod_referenca(podaci.ime,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) red.add("call " + simbol("method",초기화참조.부분들()));
            Collections.addAll(red,"movl $2, " + Status_VALUE,초기화 + "_done:","ret");
            for (član_podaci vrednost_polja : podaci.vrednost_polja) {
                byte[] konstanta_VALUE = vrednost_polja.atribut_VALUE.get("ConstantValue"); String VALUE = konstanta_VALUE == null ? "0" : X_86_konstanta(podaci,new podaci_Čitač(konstanta_VALUE).두바이트());
                Collections.addAll(red,".data",".balign 4",simbol("field",podaci.ime,vrednost_polja.ime,vrednost_polja.서술) + ": .long " + VALUE);
            }
            for (član_podaci FUNCTION_VALUE : podaci.FUNCTION_VALUE) if (!FUNCTION_VALUE.ime.equals("<init>")) red.add(X_86_metod_telo(new metod_referenca(podaci.ime,FUNCTION_VALUE.ime,FUNCTION_VALUE.서술),FUNCTION_VALUE,računar_tabela,cilj));
        }
        Collections.addAll(red,".text",".globl java_entry","java_entry:","call " + simbol("init",stavka_p_VALUE.vlasnik_VALUE),"call " + simbol("method",stavka_p_VALUE.부분들()));
        if (stavka_p_VALUE.서술.equals("()V")) red.add("xorl %eax, %eax"); red.add("ret");
        for (String Dodeli_VALUE : 내보냄) {
            int znak_za_razgraničavanje_VALUE = Dodeli_VALUE.indexOf('='); if (znak_za_razgraničavanje_VALUE < 1) throw new Prevođenje_greška("내보내기 Dodeli_VALUE greška");
            String spoljni_VALUE = Dodeli_VALUE.substring(0,znak_za_razgraničavanje_VALUE), FUNCTION_VALUE = Dodeli_VALUE.substring(znak_za_razgraničavanje_VALUE + 1); int deljenje_KR = FUNCTION_VALUE.lastIndexOf('.');
            if (deljenje_KR < 0 || !spoljni_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Prevođenje_greška("내보내기 simbol greška");
            String Razred_VALUE = FUNCTION_VALUE.substring(0,deljenje_KR).replace('.','/'), ime = FUNCTION_VALUE.substring(deljenje_KR + 1); metod_referenca izbor_VALUE = null;
            for (metod_referenca referenca : 함수들.keySet()) if (referenca.vlasnik_VALUE.equals(Razred_VALUE) && referenca.ime.equals(ime)) { if (izbor_VALUE != null) throw new Prevođenje_greška("겹친 내보내기 cilj"); izbor_VALUE = referenca; }
            if (izbor_VALUE == null) throw new Prevođenje_greška("내보낼 함수가 없음");
            Collections.addAll(red,".text",".globl " + spoljni_VALUE,spoljni_VALUE + ":","call " + simbol("init",izbor_VALUE.vlasnik_VALUE),"jmp " + simbol("method",izbor_VALUE.부분들()));
        }
        red.add(".section .rodata");
        for (Map.Entry<String,String> stavka_VALUE : 문자열들.entrySet()) {
            Collections.addAll(red,".balign 4",stavka_VALUE.getValue() + ":",".long " + stavka_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lekcija_VALUE : stavka_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(lekcija_VALUE)); if (!단위들.isEmpty()) red.add(".long " + String.join(",",단위들));
        }
        red.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",red) + "\n";
    }
    static void Izvrši_alatka(List<String> komanda) throws Exception {
        if (new ProcessBuilder(komanda).inheritIO().start().waitFor() != 0) throw new Prevođenje_greška("kompajlirati_izvor greška: " + komanda.get(0));
    }
    static String podaci_niska(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Prevođenje(List<Path> 입력들, String cilj, String stavka_p, List<String> 내보냄, Path 출력, Path resurs_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Razred_putanja = 임시.resolve("classes"); Files.createDirectory(Razred_putanja);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Razred_putanja.toString(),"-sourcepath",Razred_putanja.toString(),"-d",Razred_putanja.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int izvor_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Prevođenje_greška("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); izvor_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Prevođenje_greška(".java 또는 .class만 Podrška_VALUE");
            }
            if (izvor_COUNT > 0) Izvrši_alatka(자바명령);
            try (java.util.stream.Stream<Path> putanja_Lista = Files.walk(Razred_putanja)) { putanja_Lista.filter(putanja -> putanja.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,cilj.equals("user") ? "user" : "kernel",262144,resurs_VALUE);
            String 조립 = CONVERT_VALUE.X_86_sklop(stavka_p,내보냄,cilj); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path alatka_pozicija = resurs_VALUE.getParent();
            Izvrši_alatka(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Izvrši_alatka(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),alatka_pozicija.resolve("CLR_komponenta_Podrška.s").toString()));
            List<String> veze = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (cilj.equals("kernel")) veze.add("-r");
            else {
                Izvrši_alatka(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),alatka_pozicija.resolve(cilj.equals("user") ? "START_korisnik_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(veze,"-e","_start",임시.resolve("start.o").toString());
                if (cilj.equals("user")) Collections.addAll(veze,"-T",alatka_pozicija.resolve("korisnik_Veza_Raspored.ld").toString());
            }
            Collections.addAll(veze,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Izvrši_alatka(veze);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path objavi_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),objavi_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(objavi_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(objavi_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(cilj.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbol_podaci = new ArrayList<>(), izvor_podaci = new ArrayList<>();
            for (metod_referenca referenca : CONVERT_VALUE.함수들.keySet()) simbol_podaci.add(podaci_niska(simbol("method",referenca.부분들())) + ":" + podaci_niska(referenca.vlasnik_VALUE + "." + referenca.ime + referenca.서술));
            for (Path 입력 : 입력들) {
                byte[] heš_Datoteka = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte VALUE : heš_Datoteka) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                izvor_podaci.add(podaci_niska(입력.toAbsolutePath().toString()) + ":" + podaci_niska(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + podaci_niska(cilj) + ",\"entry\":" + podaci_niska(stavka_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbol_podaci) + "},\"sources\":{" + String.join(",",izvor_podaci) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> putanja_Lista = Files.walk(임시)) { for (Path putanja : (Iterable<Path>)putanja_Lista.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(putanja); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String stavka_p = null, cilj = "kernel", X_86_cilj = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> putanja_Lista = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": X_86_cilj = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Razred_VALUE.FUNCTION_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export simbol=Razred_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": stavka_p = 인수[++순번]; break;
                    case "--profile": cilj = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Prevođenje_greška("알 수 없는 옵션: " + VALUE); putanja_Lista.add(Paths.get(VALUE));
                }
            }
            if (stavka_p == null || 출력경로 == null || putanja_Lista.isEmpty()) throw new Prevođenje_greška("--entry, -o, Razred_VALUE 파일이 필요합니다");
            Path resurs_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_cilj != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_cilj)) throw new Prevođenje_greška("알 수 없는 Izvrši_komanda cilj");
                X_86_Prevođenje(putanja_Lista,X_86_cilj,stavka_p,내보냄,출력경로,resurs_VALUE); return;
            }
            String izvor = new 기계어미리번역(putanja_Lista, cilj, 낱말수, resurs_VALUE).generisati(stavka_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, izvor, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception greška) { System.err.println("kompajlirati_izvor greška: " + greška.getMessage()); System.exit(1); }
    }
}
