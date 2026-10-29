// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java klasa_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. organizator JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Prevođenje_greška extends RuntimeException {
        Prevođenje_greška(String 설명) { super(설명); }
    }
    static final class podaci_Čitač {
        final byte[] podaci;
        int Pozicija;
        podaci_Čitač(byte[] 입력자료) { podaci = 입력자료; }
        byte[] Čitaj(int dužina_VALUE) {
            if (dužina_VALUE < 0 || dužina_VALUE > podaci.length - Pozicija) throw new Prevođenje_greška("잘린 klasa_VALUE 또는 Naredba podaci");
            byte[] mjera = Arrays.copyOfRange(podaci, Pozicija, Pozicija + dužina_VALUE); Pozicija += dužina_VALUE; return mjera;
        }
        int 한바이트() { if (Pozicija >= podaci.length) throw new Prevođenje_greška("잘린 Naredba podaci"); return podaci[Pozicija++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class član_podaci {
        final int pristup_unos;
        final String Naziv, 서술;
        final Map<String, byte[]> atribut_VALUE;
        član_podaci(int pristup_VALUE, String naziv_VALUE, String 서술값, Map<String, byte[]> atribut_podaci) {
            pristup_unos = pristup_VALUE; Naziv = naziv_VALUE; 서술 = 서술값; atribut_VALUE = atribut_podaci;
        }
    }
    static final class metoda_Reference implements Comparable<metoda_Reference> {
        final String vlasnik_VALUE, Naziv, 서술;
        metoda_Reference(String 소유값, String naziv_VALUE, String 서술값) { vlasnik_VALUE = 소유값; Naziv = naziv_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{vlasnik_VALUE, Naziv, 서술}; }
        public int compareTo(metoda_Reference peer_VALUE) {
            int Poređenje_VALUE = vlasnik_VALUE.compareTo(peer_VALUE.vlasnik_VALUE);
            if (Poređenje_VALUE == 0) Poređenje_VALUE = Naziv.compareTo(peer_VALUE.Naziv);
            return Poređenje_VALUE == 0 ? 서술.compareTo(peer_VALUE.서술) : Poređenje_VALUE;
        }
        public boolean equals(Object peer_VALUE) { return peer_VALUE instanceof metoda_Reference && compareTo((metoda_Reference) peer_VALUE) == 0; }
        public int hashCode() { return Objects.hash(vlasnik_VALUE, Naziv, 서술); }
    }
    static final class klasa_podaci {
        final int[] 상수종류;
        final Object[] konstanta_podaci;
        final String Naziv;
        final List<član_podaci> polje_VALUE, FUNCTION_VALUE;
        klasa_podaci(Path Putanja) throws IOException {
            podaci_Čitač Čitač_VALUE = new podaci_Čitač(Files.readAllBytes(Putanja));
            if (Čitač_VALUE.네바이트() != 0xcafebabe) throw new Prevođenje_greška("Java klasa_VALUE 표식이 아님");
            Čitač_VALUE.Čitaj(4);
            int stavka_COUNT = Čitač_VALUE.두바이트(); 상수종류 = new int[stavka_COUNT]; konstanta_podaci = new Object[stavka_COUNT];
            for (int 순번 = 1; 순번 < stavka_COUNT; 순번++) {
                int 종류 = Čitač_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int dužina_VALUE = Čitač_VALUE.두바이트();
                        byte[] znak_bafer = Čitač_VALUE.Čitaj(dužina_VALUE), 길이붙인자료 = new byte[dužina_VALUE + 2];
                        길이붙인자료[0] = (byte)(dužina_VALUE >> 8); 길이붙인자료[1] = (byte)dužina_VALUE;
                        System.arraycopy(znak_bafer, 0, 길이붙인자료, 2, dužina_VALUE);
                        konstanta_podaci[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstanta_podaci[순번] = Čitač_VALUE.네바이트(); break;
                    case 4: Čitač_VALUE.Čitaj(4); break;
                    case 5: case 6: Čitač_VALUE.Čitaj(8); 순번++; break;
                    case 7: case 8: case 16: konstanta_podaci[순번] = Čitač_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstanta_podaci[순번] = new int[]{Čitač_VALUE.두바이트(), Čitač_VALUE.두바이트()}; break;
                    case 15: konstanta_podaci[순번] = new int[]{Čitač_VALUE.한바이트(), Čitač_VALUE.두바이트()}; break;
                    default: throw new Prevođenje_greška("지원하지 않는 konstanta_VALUE 종류: " + 종류);
                }
            }
            Čitač_VALUE.두바이트(); Naziv = naziv_klase(Čitač_VALUE.두바이트());
            if (!naziv_klase(Čitač_VALUE.두바이트()).equals("java/lang/Object") || Čitač_VALUE.두바이트() != 0)
                throw new Prevođenje_greška(Naziv + ": 상속 및 인터페이스 미지원");
            polje_VALUE = 멤버읽기(Čitač_VALUE); FUNCTION_VALUE = 멤버읽기(Čitač_VALUE); 속성읽기(Čitač_VALUE);
            if (Čitač_VALUE.Pozicija != Čitač_VALUE.podaci.length) throw new Prevođenje_greška("klasa_VALUE 뒤에 남은 podaci");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Prevođenje_greška("문자 konstanta_VALUE INDEX GRESKA");
            return (String) konstanta_podaci[INDEX];
        }
        String naziv_klase(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Prevođenje_greška("klasa_VALUE Reference GRESKA");
            return 문자((Integer)konstanta_podaci[INDEX]);
        }
        metoda_Reference Reference(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Prevođenje_greška("멤버 Reference GRESKA");
            int[] Bluetooth_sparivanje_VALUE = (int[])konstanta_podaci[INDEX], naziv_Bluetooth_sparivanje = (int[])konstanta_podaci[Bluetooth_sparivanje_VALUE[1]];
            return new metoda_Reference(naziv_klase(Bluetooth_sparivanje_VALUE[0]), 문자(naziv_Bluetooth_sparivanje[0]), 문자(naziv_Bluetooth_sparivanje[1]));
        }
        Map<String, byte[]> 속성읽기(podaci_Čitač Čitač_VALUE) {
            Map<String, byte[]> mjera = new LinkedHashMap<>();
            int stavka_COUNT = Čitač_VALUE.두바이트();
            for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) {
                String atribut_naziv = 문자(Čitač_VALUE.두바이트()); byte[] VALUE = Čitač_VALUE.Čitaj(Čitač_VALUE.네바이트());
                if (mjera.put(atribut_naziv, VALUE) != null) throw new Prevođenje_greška("겹친 atribut_VALUE: " + atribut_naziv);
            }
            return mjera;
        }
        List<član_podaci> 멤버읽기(podaci_Čitač Čitač_VALUE) {
            List<član_podaci> mjera = new ArrayList<>(); int stavka_COUNT = Čitač_VALUE.두바이트();
            for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) {
                int pristup_unos = Čitač_VALUE.두바이트(); String metoda_unos_naziv = 문자(Čitač_VALUE.두바이트()), 서술 = 문자(Čitač_VALUE.두바이트());
                mjera.add(new član_podaci(pristup_unos, metoda_unos_naziv, 서술, 속성읽기(Čitač_VALUE)));
            }
            return mjera;
        }
    }
    static final class 함수형식 {
        final List<String> Argumenti = new ArrayList<>();
        final String vratiti_mjera;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Prevođenje_greška("FUNCTION_VALUE 서술 GRESKA: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Prevođenje_greška("FUNCTION_VALUE 서술 GRESKA: " + 서술);
            Argumenti.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumenti.contains("V") || 반환들.size() != 1) throw new Prevođenje_greška("FUNCTION_VALUE 서술 GRESKA: " + 서술);
            vratiti_mjera = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> mjera = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Pozicija = 0; Pozicija < 서술.length();) {
            String izbor_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, Pozicija)) { izbor_VALUE = format_VALUE; break; }
            if (izbor_VALUE == null) throw new Prevođenje_greška("지원하지 않는 vrsta_podataka: " + 서술);
            mjera.add(izbor_VALUE); Pozicija += izbor_VALUE.length();
        }
        return mjera;
    }
    static String simbol(String 종류, String... 부분들) {
        try {
            byte[] raspršivanje_fajl = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Tekst = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Tekst.append(String.format(Locale.ROOT, "%02x", raspršivanje_fajl[순번] & 255));
            return Tekst.toString();
        } catch (Exception GRESKA) { throw new Prevođenje_greška(GRESKA.toString()); }
    }
    final Map<String, klasa_podaci> 클래스들 = new TreeMap<>();
    final Map<metoda_Reference, član_podaci> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, mašina_klasa;
    final int 동적기억낱말수;
    final Path resurs_put;
    기계어미리번역(List<Path> put_spisak, String cilj, int 낱말수, Path resurs_VALUE) throws IOException {
        if ((!cilj.equals("kernel") && !cilj.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Prevođenje_greška("Izvrši_komanda cilj 또는 Memorija_VALUE 공간 Veličina GRESKA");
        실행대상 = cilj; 동적기억낱말수 = 낱말수; resurs_put = resurs_VALUE;
        // 이 이름도 국가별 izvor_stablo generirati 시 해당 언어로 옮긴다.
        mašina_klasa = cilj.equals("kernel") ? "ploča" : "korisnik";
        for (String Linija : Files.readAllLines(resurs_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Linija.split("\t", -1);
            if (부분들.length != 4) throw new Prevođenje_greška("mašina FUNCTION_VALUE podaci GRESKA");
            if (부분들[0].equals(cilj)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Putanja : put_spisak) {
            klasa_podaci podaci = new klasa_podaci(Putanja);
            if (클래스들.put(podaci.Naziv, podaci) != null) throw new Prevođenje_greška("중복 klasa_VALUE: " + podaci.Naziv);
            for (član_podaci polje_VALUE : podaci.polje_VALUE) {
                if ((polje_VALUE.pristup_unos & 8) == 0 || 형식읽기(polje_VALUE.서술).equals(Collections.singletonList("V"))) throw new Prevođenje_greška("statični_VALUE 필드만 Podrška_VALUE");
                if (필드들.put(new metoda_Reference(podaci.Naziv, polje_VALUE.Naziv, polje_VALUE.서술), polje_VALUE) != null) throw new Prevođenje_greška("중복 polje_VALUE");
            }
            for (član_podaci FUNCTION_VALUE : podaci.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Naziv.equals("<init>")) continue;
                if ((FUNCTION_VALUE.pristup_unos & 8) == 0 || (FUNCTION_VALUE.pristup_unos & (0x20 | 0x400)) != 0) throw new Prevođenje_greška("statični_VALUE 비동기화 함수만 Podrška_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new metoda_Reference(podaci.Naziv, FUNCTION_VALUE.Naziv, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Prevođenje_greška("중복 FUNCTION_VALUE");
            }
        }
    }
    String string_simbol(String Tekst) { return 문자열들.computeIfAbsent(Tekst, VALUE -> "j_text_" + 문자열들.size()); }
    String konstanta_izraz(klasa_podaci podaci, int INDEX) {
        if (INDEX < 1 || INDEX >= podaci.상수종류.length) throw new Prevođenje_greška("konstanta_VALUE INDEX isječak GRESKA");
        if (podaci.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + podaci.konstanta_podaci[INDEX] + ")";
        if (podaci.상수종류[INDEX] == 8) return "(word)" + string_simbol(podaci.문자((Integer)podaci.konstanta_podaci[INDEX]));
        throw new Prevođenje_greška("정수와 string_VALUE 상수만 Podrška_VALUE");
    }
    String 함수원형(metoda_Reference Reference) {
        List<String> 인수들 = new ArrayList<>(); int stavka_COUNT = new 함수형식(Reference.서술).Argumenti.size();
        for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbol("method", Reference.부분들()) + "(" + (stavka_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void ček_lokalni(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Prevođenje_greška("lokalni_opseg 변수 INDEX isječak GRESKA"); }
    void 분기넣기(List<String> Ispis, Set<Integer> ogranak_spisak, int Pozicija, int 이동량, String uvjet) {
        int odredište_VALUE = Pozicija + 이동량; ogranak_spisak.add(odredište_VALUE);
        Ispis.add((uvjet == null ? "" : "if (" + uvjet + ") ") + "goto b" + odredište_VALUE + ";");
    }
    String metoda_tijelo(metoda_Reference FUNCTION_VALUE, član_podaci podaci) {
        byte[] tijelo_podaci = podaci.atribut_VALUE.get("Code"); if (tijelo_podaci == null) throw new Prevođenje_greška("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Naziv);
        podaci_Čitač Čitač_VALUE = new podaci_Čitač(tijelo_podaci); int 쌓임깊이 = Čitač_VALUE.두바이트(), 지역변수수 = Čitač_VALUE.두바이트();
        podaci_Čitač komanda_podaci = new podaci_Čitač(Čitač_VALUE.Čitaj(Čitač_VALUE.네바이트()));
        if (Čitač_VALUE.두바이트() != 0) throw new Prevođenje_greška("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (지역변수수 < format_VALUE.Argumenti.size()) throw new Prevođenje_greška("매개변수보다 적은 lokalni_opseg 변수");
        klasa_podaci klasa_VALUE = 클래스들.get(FUNCTION_VALUE.vlasnik_VALUE);
        List<String> Ispis = new ArrayList<>(); Ispis.add(함수원형(FUNCTION_VALUE) + " {");
        Ispis.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.Argumenti.size(); 순번++) Ispis.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ogranak_spisak = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (komanda_podaci.Pozicija < komanda_podaci.podaci.length) {
            int Pozicija = komanda_podaci.Pozicija, Naredba = komanda_podaci.한바이트(); 경계들.add(Pozicija); Ispis.add("b" + Pozicija + ":;");
            if (Naredba == 0) continue;
            if (Naredba == 1) Ispis.add("PUSH(0);");
            else if (Naredba >= 2 && Naredba <= 8) Ispis.add("PUSH((uint32_t)(" + (Naredba - 3) + "));");
            else if (Naredba == 16 || Naredba == 17) Ispis.add("PUSH((uint32_t)(" + (Naredba == 16 ? komanda_podaci.부호한바이트() : komanda_podaci.부호두바이트()) + "));");
            else if (Naredba == 18 || Naredba == 19) Ispis.add("PUSH(" + konstanta_izraz(klasa_VALUE, Naredba == 18 ? komanda_podaci.한바이트() : komanda_podaci.두바이트()) + ");");
            else if (Naredba == 21 || Naredba == 25 || (Naredba >= 26 && Naredba <= 29) || (Naredba >= 42 && Naredba <= 45)) {
                int INDEX = Naredba == 21 || Naredba == 25 ? komanda_podaci.한바이트() : Naredba - (Naredba <= 29 ? 26 : 42);
                ček_lokalni(INDEX, 지역변수수); Ispis.add("PUSH(l[" + INDEX + "]);");
            } else if (Naredba == 54 || Naredba == 58 || (Naredba >= 59 && Naredba <= 62) || (Naredba >= 75 && Naredba <= 78)) {
                int INDEX = Naredba == 54 || Naredba == 58 ? komanda_podaci.한바이트() : Naredba - (Naredba <= 62 ? 59 : 75);
                ček_lokalni(INDEX, 지역변수수); Ispis.add("l[" + INDEX + "] = POP();");
            } else if (Naredba == 46) Ispis.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Naredba == 79) Ispis.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Naredba == 87 || Naredba == 88) Ispis.add(Naredba == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Naredba >= 89 && Naredba <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] redoslijed_spisak = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Naredba - 89]; 순번++) Ispis.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : redoslijed_spisak[Naredba - 89].toCharArray()) Ispis.add("PUSH(" + VALUE + ");");
            } else if (Naredba == 96 || Naredba == 100 || Naredba == 104 || Naredba == 126 || Naredba == 128 || Naredba == 130) {
                String operacija_VALUE = Naredba == 96 ? "+" : Naredba == 100 ? "-" : Naredba == 104 ? "*" : Naredba == 126 ? "&" : Naredba == 128 ? "|" : "^";
                Ispis.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operacija_VALUE + " (uint32_t)b);");
            } else if (Naredba == 108 || Naredba == 112) Ispis.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Naredba == 112 ? 1 : 0) + "));");
            else if (Naredba == 116) Ispis.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Naredba == 120 || Naredba == 122 || Naredba == 124) {
                Ispis.add("b = POP(); a = POP();"); Ispis.add("PUSH(" + (Naredba == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Naredba == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Naredba == 132) {
                int INDEX = komanda_podaci.한바이트(), 증가량 = komanda_podaci.부호한바이트(); ček_lokalni(INDEX, 지역변수수);
                Ispis.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Naredba >= 145 && Naredba <= 147) Ispis.add("a = POP(); PUSH((uint32_t)(" + (Naredba == 145 ? "int8_t" : Naredba == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Naredba >= 153 && Naredba <= 158) {
                Ispis.add("a = POP();"); 분기넣기(Ispis, ogranak_spisak, Pozicija, komanda_podaci.부호두바이트(), "(int32_t)a " + 비교들[Naredba - 153] + " 0");
            } else if (Naredba >= 159 && Naredba <= 166) {
                Ispis.add("b = POP(); a = POP();"); 분기넣기(Ispis, ogranak_spisak, Pozicija, komanda_podaci.부호두바이트(), Naredba >= 165 ? "a " + 비교들[Naredba - 159] + " b" : "(int32_t)a " + 비교들[Naredba - 159] + " (int32_t)b");
            } else if (Naredba == 167 || Naredba == 200) 분기넣기(Ispis, ogranak_spisak, Pozicija, Naredba == 167 ? komanda_podaci.부호두바이트() : komanda_podaci.네바이트(), null);
            else if (Naredba == 170 || Naredba == 171) {
                while (komanda_podaci.Pozicija % 4 != 0) komanda_podaci.한바이트();
                int zadana_vrijednost = komanda_podaci.네바이트(); Ispis.add("a = POP();");
                if (Naredba == 170) {
                    int 아래 = komanda_podaci.네바이트(), 위 = komanda_podaci.네바이트(); long stavka_COUNT = (long)위 - 아래 + 1;
                    if (stavka_COUNT < 1 || stavka_COUNT > (komanda_podaci.podaci.length - komanda_podaci.Pozicija) / 4) throw new Prevođenje_greška("switch isječak GRESKA");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Ispis, ogranak_spisak, Pozicija, komanda_podaci.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int stavka_COUNT = komanda_podaci.네바이트(), 앞값 = 0;
                    if (stavka_COUNT < 0 || stavka_COUNT > (komanda_podaci.podaci.length - komanda_podaci.Pozicija) / 8) throw new Prevođenje_greška("switch Veličina GRESKA");
                    for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) {
                        int VALUE = komanda_podaci.네바이트(); if (순번 > 0 && VALUE <= 앞값) throw new Prevođenje_greška("switch redoslijed_VALUE GRESKA"); 앞값 = VALUE;
                        분기넣기(Ispis, ogranak_spisak, Pozicija, komanda_podaci.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Ispis, ogranak_spisak, Pozicija, zadana_vrijednost, null);
            } else if (Naredba == 172 || Naredba == 176 || Naredba == 177) Ispis.add("return " + (Naredba == 177 ? "0" : "POP()") + ";");
            else if (Naredba == 178 || Naredba == 179) {
                metoda_Reference Reference = klasa_VALUE.Reference(komanda_podaci.두바이트()); if (!필드들.containsKey(Reference)) throw new Prevođenje_greška("알 수 없는 polje_VALUE");
                Ispis.add(simbol("init", Reference.vlasnik_VALUE) + "();"); String polje_VALUE = simbol("field", Reference.부분들());
                Ispis.add(Naredba == 178 ? "PUSH(" + polje_VALUE + ");" : polje_VALUE + " = POP();");
            } else if (Naredba == 184) {
                metoda_Reference Reference = klasa_VALUE.Reference(komanda_podaci.두바이트()); if (!함수들.containsKey(Reference)) throw new Prevođenje_greška("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Reference.서술); int stavka_COUNT = 호출형식.Argumenti.size();
                Ispis.add(simbol("init", Reference.vlasnik_VALUE) + "();"); Ispis.add("if(sp < " + stavka_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + stavka_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Ispis.add("a = " + simbol("method", Reference.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.vratiti_mjera.equals("V")) Ispis.add("PUSH(a);");
            } else if (Naredba == 182) {
                metoda_Reference Reference = klasa_VALUE.Reference(komanda_podaci.두바이트());
                if (Reference.equals(new metoda_Reference("java/lang/String", "length", "()I"))) Ispis.add("a = POP(); PUSH(length(a));");
                else if (Reference.equals(new metoda_Reference("java/lang/String", "charAt", "(I)C"))) Ispis.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Prevođenje_greška("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Naredba == 188) {
                if (komanda_podaci.한바이트() != 10) throw new Prevođenje_greška("new int[]만 Podrška_VALUE"); Ispis.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Naredba == 190) Ispis.add("a = POP(); PUSH(length(a));");
            else if (Naredba == 196) {
                int ekstenzija_VALUE = komanda_podaci.한바이트(), INDEX = komanda_podaci.두바이트(); ček_lokalni(INDEX, 지역변수수);
                if (ekstenzija_VALUE == 21 || ekstenzija_VALUE == 25) Ispis.add("PUSH(l[" + INDEX + "]);");
                else if (ekstenzija_VALUE == 54 || ekstenzija_VALUE == 58) Ispis.add("l[" + INDEX + "] = POP();");
                else if (ekstenzija_VALUE == 132) Ispis.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + komanda_podaci.부호두바이트() + ");");
                else throw new Prevođenje_greška("미지원 wide Naredba");
            } else if (Naredba == 198 || Naredba == 199) {
                Ispis.add("a = POP();"); 분기넣기(Ispis, ogranak_spisak, Pozicija, komanda_podaci.부호두바이트(), "a " + (Naredba == 198 ? "==" : "!=") + " 0");
            } else throw new Prevođenje_greška(FUNCTION_VALUE.vlasnik_VALUE + "." + FUNCTION_VALUE.Naziv + ", bajt_VALUE " + Pozicija + ": 미지원 Naredba " + Naredba);
        }
        if (!경계들.containsAll(ogranak_spisak)) throw new Prevođenje_greška("Naredba 경계가 아닌 곳으로 ogranak");
        Ispis.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Ispis);
    }
    String izvesti_metoda(String Veza_simbol, String cilj, boolean 진입점여부) {
        int položaj_INDEX = cilj.lastIndexOf('.'); if (položaj_INDEX < 0 || !Veza_simbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Prevođenje_greška("내보내기 dodijeliti_VALUE GRESKA");
        String vlasnik_VALUE = cilj.substring(0, položaj_INDEX).replace('.', '/'), Naziv = cilj.substring(položaj_INDEX + 1); metoda_Reference izbor_VALUE = null;
        for (metoda_Reference Reference : 함수들.keySet()) if (Reference.vlasnik_VALUE.equals(vlasnik_VALUE) && Reference.Naziv.equals(Naziv)) {
            if (izbor_VALUE != null) throw new Prevođenje_greška("겹친 내보내기 cilj"); izbor_VALUE = Reference;
        }
        if (izbor_VALUE == null || (함수들.get(izbor_VALUE).pristup_unos & 0x100) != 0) throw new Prevođenje_greška("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 format_VALUE = new 함수형식(izbor_VALUE.서술);
        if ((진입점여부 && !format_VALUE.Argumenti.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.vratiti_mjera)) throw new Prevođenje_greška("unos_p_VALUE 또는 C 경계 format_VALUE GRESKA");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.Argumenti.size(); 순번++) {
            if (!format_VALUE.Argumenti.get(순번).equals("I")) throw new Prevođenje_greška("C 경계는 int 인수만 Podrška_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.vratiti_mjera.equals("V") ? "void " : "int32_t ") + Veza_simbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbol("init", izbor_VALUE.vlasnik_VALUE) + "(); " + (format_VALUE.vratiti_mjera.equals("V") ? "" : "return (int32_t)") + simbol("method", izbor_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generirati(String unos_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metoda_Reference, član_podaci> unos_VALUE : 함수들.entrySet()) {
            metoda_Reference Reference = unos_VALUE.getKey(); član_podaci podaci = unos_VALUE.getValue(); 선언들.add(함수원형(Reference) + ";");
            if ((podaci.pristup_unos & 0x100) != 0) {
                String Spoji_se = 기계함수들.get(Reference.Naziv + Reference.서술);
                if (!Reference.vlasnik_VALUE.equals(mašina_klasa) || Spoji_se == null) throw new Prevođenje_greška("허용되지 않은 native FUNCTION_VALUE: " + Reference.Naziv);
                int stavka_COUNT = new 함수형식(Reference.서술).Argumenti.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Spoji_se + "(" + (stavka_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(stavka_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Reference) + " { return " + Spoji_se + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metoda_tijelo(Reference, podaci));
        }
        for (Map.Entry<metoda_Reference, član_podaci> unos_VALUE : 필드들.entrySet()) {
            metoda_Reference Reference = unos_VALUE.getKey(); byte[] konstanta_VALUE = unos_VALUE.getValue().atribut_VALUE.get("ConstantValue");
            String VALUE = konstanta_VALUE == null ? "0" : konstanta_izraz(클래스들.get(Reference.vlasnik_VALUE), new podaci_Čitač(konstanta_VALUE).두바이트());
            필드선언들.add("static word " + simbol("field", Reference.부분들()) + " = " + VALUE + ";");
        }
        for (String Naziv : 클래스들.keySet()) {
            String inicijalizirati = simbol("init", Naziv), stanje_VALUE = simbol("state", Naziv);
            선언들.add("static void " + inicijalizirati + "(void);"); 필드선언들.add("static unsigned " + stanje_VALUE + ";");
            metoda_Reference Reference = new metoda_Reference(Naziv, "<clinit>", "()V");
            몸체들.add("static void " + inicijalizirati + "(void) { if(" + stanje_VALUE + ") return; " + stanje_VALUE + " = 1; " + (함수들.containsKey(Reference) ? simbol("method", Reference.부분들()) + "(); " : "") + stanje_VALUE + " = 2; }");
        }
        몸체들.add(izvesti_metoda("java_entry", unos_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String dodijeliti_VALUE : 내보내기목록) {
            int položaj_INDEX = dodijeliti_VALUE.indexOf('='); if (položaj_INDEX < 1) throw new Prevođenje_greška("내보내기 dodijeliti_VALUE GRESKA");
            String Naziv = dodijeliti_VALUE.substring(0, položaj_INDEX); 공개이름.add(Naziv); 몸체들.add(izvesti_metoda(Naziv, dodijeliti_VALUE.substring(položaj_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> unos_VALUE : 문자열들.entrySet()) {
            String Tekst = unos_VALUE.getKey(); StringBuilder niz_VALUE = new StringBuilder("static const word " + unos_VALUE.getValue() + "[] = {" + Tekst.length());
            for (int 순번 = 0; 순번 < Tekst.length(); 순번++) niz_VALUE.append(", ").append((int)Tekst.charAt(순번));
            문자열선언들.add(niz_VALUE.append("};").toString());
        }
        String Podrška_VALUE = Files.readString(resurs_put.resolve("zajednička_jezička_biblioteka_Podrška.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Podrška_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String IZVOR, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> naziv_tabela = new HashMap<>();
        for (String Linija : Files.readAllLines(resurs_put.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] Bluetooth_sparivanje_VALUE = Linija.split("\t"); naziv_tabela.put(Bluetooth_sparivanje_VALUE[0], Bluetooth_sparivanje_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(IZVOR); StringBuffer mjera = new StringBuffer();
        while (찾개.find()) {
            String Naziv = 찾개.group(), 새이름 = Naziv;
            if (!Naziv.startsWith("//") && !Naziv.startsWith("/*") && !Naziv.startsWith("\"") && !Naziv.startsWith("'") && !공개이름.contains(Naziv)) {
                새이름 = naziv_tabela.getOrDefault(Naziv, Naziv);
                if (Naziv.matches("a[0-9]+")) 새이름 = "Argumenti" + Naziv.substring(1);
                if (Naziv.matches("b[0-9]+")) 새이름 = "ogranak" + Naziv.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char znak_VALUE : 새이름.toCharArray()) 표기.append(znak_VALUE < 128 ? Character.toString(znak_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)znak_VALUE));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(mjera, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(mjera); return mjera.toString();
    }
    String X_86_metoda_tijelo(metoda_Reference FUNCTION_VALUE, član_podaci podaci, Map<String,String> mašina_tabela, String cilj) {
        String 표식 = simbol("method", FUNCTION_VALUE.부분들());
        List<String> Linija = new ArrayList<>();
        if ((podaci.pristup_unos & 0x100) != 0) {
            String Spoji_se = mašina_tabela.get(FUNCTION_VALUE.Naziv + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.vlasnik_VALUE.equals(cilj.equals("kernel") ? "uređaj_VALUE" : "korisnik") || Spoji_se == null) throw new Prevođenje_greška("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Spoji_se;
        }
        byte[] tijelo_teksta = podaci.atribut_VALUE.get("Code"); if (tijelo_teksta == null) throw new Prevođenje_greška("FUNCTION_VALUE 몸체가 없음");
        podaci_Čitač Čitač_VALUE = new podaci_Čitač(tijelo_teksta); Čitač_VALUE.두바이트(); int lokalni_COUNT = Čitač_VALUE.두바이트();
        podaci_Čitač komanda_podaci = new podaci_Čitač(Čitač_VALUE.Čitaj(Čitač_VALUE.네바이트()));
        if (Čitač_VALUE.두바이트() != 0) throw new Prevođenje_greška("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokalni_COUNT < format_VALUE.Argumenti.size()) throw new Prevođenje_greška("매개변수보다 적은 lokalni_opseg 변수");
        Collections.addAll(Linija,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokalni_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.Argumenti.size(); 순번++) Collections.addAll(Linija,"movl " + (8 + 4 * (format_VALUE.Argumenti.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        klasa_podaci klasa_VALUE = 클래스들.get(FUNCTION_VALUE.vlasnik_VALUE); Set<Integer> 경계들 = new HashSet<>(), ogranak_spisak = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (komanda_podaci.Pozicija < komanda_podaci.podaci.length) {
            int Pozicija = komanda_podaci.Pozicija, Naredba = komanda_podaci.한바이트(); String položaj_INDEX = 표식 + "_b" + Pozicija;
            Linija.add(položaj_INDEX + ":"); 경계들.add(Pozicija);
            if (Naredba == 0) Linija.add("nop");
            else if (Naredba == 1) Linija.add("pushl $0");
            else if (Naredba >= 2 && Naredba <= 8) Linija.add("pushl $" + (Naredba - 3));
            else if (Naredba == 16 || Naredba == 17) Linija.add("pushl $" + (Naredba == 16 ? komanda_podaci.부호한바이트() : komanda_podaci.부호두바이트()));
            else if (Naredba == 18 || Naredba == 19) {
                int INDEX = Naredba == 18 ? komanda_podaci.한바이트() : komanda_podaci.두바이트();
                Linija.add("pushl $" + X_86_konstanta(klasa_VALUE,INDEX));
            } else if (Naredba == 21 || Naredba == 25 || (Naredba >= 26 && Naredba <= 29) || (Naredba >= 42 && Naredba <= 45) || Naredba == 54 || Naredba == 58 || (Naredba >= 59 && Naredba <= 62) || (Naredba >= 75 && Naredba <= 78)) {
                boolean 읽음 = Naredba < 54; int INDEX = Naredba == 21 || Naredba == 25 || Naredba == 54 || Naredba == 58 ? komanda_podaci.한바이트() : Naredba - (Naredba <= 29 ? 26 : Naredba <= 45 ? 42 : Naredba <= 62 ? 59 : 75);
                ček_lokalni(INDEX,lokalni_COUNT); Linija.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Naredba == 46) Collections.addAll(Linija,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Naredba == 79) Collections.addAll(Linija,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Naredba == 87 || Naredba == 88) Linija.add("addl $" + (Naredba == 87 ? 4 : 8) + ", %esp");
            else if (Naredba >= 89 && Naredba <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] redoslijed_spisak = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Naredba - 89]; 순번++) Linija.add("popl " + 저장기들[순번]);
                for (int 순번 : redoslijed_spisak[Naredba - 89]) Linija.add("pushl " + 저장기들[순번]);
            } else if (Naredba == 96 || Naredba == 100 || Naredba == 104 || Naredba == 126 || Naredba == 128 || Naredba == 130) {
                String operacija_VALUE = Naredba == 96 ? "addl" : Naredba == 100 ? "subl" : Naredba == 104 ? "imull" : Naredba == 126 ? "andl" : Naredba == 128 ? "orl" : "xorl";
                Collections.addAll(Linija,"popl %ecx","popl %eax",operacija_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Naredba == 108 || Naredba == 112) Collections.addAll(Linija,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + položaj_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + položaj_INDEX + "_divide","xorl %edx, %edx","jmp " + položaj_INDEX + "_done",položaj_INDEX + "_divide:","cltd","idivl %ecx",položaj_INDEX + "_done:","pushl " + (Naredba == 108 ? "%eax" : "%edx"));
            else if (Naredba == 116) Linija.add("negl (%esp)");
            else if (Naredba == 120 || Naredba == 122 || Naredba == 124) Collections.addAll(Linija,"popl %ecx","popl %eax",(Naredba == 120 ? "sall" : Naredba == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Naredba == 132) {
                int INDEX = komanda_podaci.한바이트(), 증가 = komanda_podaci.부호한바이트(); ček_lokalni(INDEX,lokalni_COUNT); Linija.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Naredba >= 145 && Naredba <= 147) Collections.addAll(Linija,"popl %eax",Naredba == 145 ? "movsbl %al, %eax" : Naredba == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Naredba >= 153 && Naredba <= 166) {
                if (Naredba <= 158) Collections.addAll(Linija,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Linija,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int odredište_VALUE = Pozicija + komanda_podaci.부호두바이트(); ogranak_spisak.add(odredište_VALUE); Linija.add(비교들[Naredba - (Naredba <= 158 ? 153 : 159)] + " " + 표식 + "_b" + odredište_VALUE);
            } else if (Naredba == 167 || Naredba == 200) {
                int odredište_VALUE = Pozicija + (Naredba == 167 ? komanda_podaci.부호두바이트() : komanda_podaci.네바이트()); ogranak_spisak.add(odredište_VALUE); Linija.add("jmp " + 표식 + "_b" + odredište_VALUE);
            } else if (Naredba == 170 || Naredba == 171) {
                while (komanda_podaci.Pozicija % 4 != 0) komanda_podaci.한바이트();
                int zadana_vrijednost = Pozicija + komanda_podaci.네바이트(); ogranak_spisak.add(zadana_vrijednost); Linija.add("popl %eax");
                int stavka_COUNT, 아래 = 0;
                if (Naredba == 170) { 아래 = komanda_podaci.네바이트(); int 위 = komanda_podaci.네바이트(); long dužina_VALUE = (long)위 - 아래 + 1; if (dužina_VALUE < 1 || dužina_VALUE > (komanda_podaci.podaci.length - komanda_podaci.Pozicija) / 4) throw new Prevođenje_greška("switch isječak GRESKA"); stavka_COUNT = (int)dužina_VALUE; }
                else { stavka_COUNT = komanda_podaci.네바이트(); if (stavka_COUNT < 0 || stavka_COUNT > (komanda_podaci.podaci.length - komanda_podaci.Pozicija) / 8) throw new Prevođenje_greška("switch Veličina GRESKA"); }
                for (int 순번 = 0; 순번 < stavka_COUNT; 순번++) {
                    int VALUE = Naredba == 170 ? 아래 + 순번 : komanda_podaci.네바이트(), odredište_VALUE = Pozicija + komanda_podaci.네바이트(); ogranak_spisak.add(odredište_VALUE);
                    Collections.addAll(Linija,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + odredište_VALUE);
                }
                Linija.add("jmp " + 표식 + "_b" + zadana_vrijednost);
            } else if (Naredba == 172 || Naredba == 176 || Naredba == 177) {
                if (Naredba != 177) Linija.add("popl %eax"); Collections.addAll(Linija,"leave","ret");
            } else if (Naredba == 178 || Naredba == 179) {
                metoda_Reference Reference = klasa_VALUE.Reference(komanda_podaci.두바이트()); if (!필드들.containsKey(Reference)) throw new Prevođenje_greška("알 수 없는 polje_VALUE");
                Collections.addAll(Linija,"call " + simbol("init",Reference.vlasnik_VALUE),(Naredba == 178 ? "pushl " : "popl ") + simbol("field",Reference.부분들()));
            } else if (Naredba == 184) {
                metoda_Reference Reference = klasa_VALUE.Reference(komanda_podaci.두바이트()); if (!함수들.containsKey(Reference)) throw new Prevođenje_greška("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Reference.서술); Collections.addAll(Linija,"call " + simbol("init",Reference.vlasnik_VALUE),"call " + simbol("method",Reference.부분들()));
                if (!호출형식.Argumenti.isEmpty()) Linija.add("addl $" + 호출형식.Argumenti.size() * 4 + ", %esp");
                if (!호출형식.vratiti_mjera.equals("V")) Linija.add("pushl %eax");
            } else if (Naredba == 182) {
                metoda_Reference Reference = klasa_VALUE.Reference(komanda_podaci.두바이트());
                if (Reference.equals(new metoda_Reference("java/lang/String","length","()I"))) Collections.addAll(Linija,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Reference.equals(new metoda_Reference("java/lang/String","charAt","(I)C"))) Collections.addAll(Linija,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Prevođenje_greška("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Naredba == 188) {
                if (komanda_podaci.한바이트() != 10) throw new Prevođenje_greška("new int[]만 Podrška_VALUE"); Collections.addAll(Linija,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Naredba == 190) Collections.addAll(Linija,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Naredba == 196) {
                int ekstenzija_VALUE = komanda_podaci.한바이트(), INDEX = komanda_podaci.두바이트(); ček_lokalni(INDEX,lokalni_COUNT);
                if (ekstenzija_VALUE == 21 || ekstenzija_VALUE == 25 || ekstenzija_VALUE == 54 || ekstenzija_VALUE == 58) Linija.add((ekstenzija_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (ekstenzija_VALUE == 132) Linija.add("addl $" + komanda_podaci.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Prevođenje_greška("wide Naredba 미지원");
            } else if (Naredba == 198 || Naredba == 199) {
                int odredište_VALUE = Pozicija + komanda_podaci.부호두바이트(); ogranak_spisak.add(odredište_VALUE); Collections.addAll(Linija,"popl %eax","testl %eax, %eax",(Naredba == 198 ? "je " : "jne ") + 표식 + "_b" + odredište_VALUE);
            } else throw new Prevođenje_greška("미지원 Naredba: " + Naredba);
        }
        if (!경계들.containsAll(ogranak_spisak)) throw new Prevođenje_greška("Naredba 경계가 아닌 곳으로 ogranak");
        Linija.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",Linija);
    }
    String X_86_konstanta(klasa_podaci podaci, int INDEX) {
        if (podaci.상수종류[INDEX] == 3) return podaci.konstanta_podaci[INDEX].toString();
        if (podaci.상수종류[INDEX] == 8) return string_simbol(podaci.문자((Integer)podaci.konstanta_podaci[INDEX]));
        throw new Prevođenje_greška("정수와 string_VALUE 상수만 Podrška_VALUE");
    }
    String 엑스조립본(String unos_p, List<String> 내보냄, String cilj) throws IOException {
        Map<String,String> mašina_tabela = new HashMap<>();
        for (String Linija : Files.readAllLines(resurs_put.resolve("엑스기계함수.tsv"))) { String[] Bluetooth_sparivanje_VALUE = Linija.split("\t"); if (Bluetooth_sparivanje_VALUE[0].equals(cilj)) mašina_tabela.put(Bluetooth_sparivanje_VALUE[1] + Bluetooth_sparivanje_VALUE[2],Bluetooth_sparivanje_VALUE[3]); }
        int položaj_INDEX = unos_p.lastIndexOf('.'); if (položaj_INDEX < 0) throw new Prevođenje_greška("unos_p dodijeliti_VALUE GRESKA");
        String vlasnik_VALUE = unos_p.substring(0,položaj_INDEX).replace('.','/'), metoda_unos_naziv = unos_p.substring(položaj_INDEX + 1); metoda_Reference unos_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metoda_Reference Reference = new metoda_Reference(vlasnik_VALUE,metoda_unos_naziv,서술); if (함수들.containsKey(Reference)) { if (unos_p_VALUE != null) throw new Prevođenje_greška("겹친 unos_p"); unos_p_VALUE = Reference; } }
        if (unos_p_VALUE == null || (함수들.get(unos_p_VALUE).pristup_unos & 0x100) != 0) throw new Prevođenje_greška("unos_p_VALUE FUNCTION_VALUE format_VALUE GRESKA");
        List<String> Linija = new ArrayList<>(); Linija.add(".code32");
        for (klasa_podaci podaci : 클래스들.values()) {
            String stanje_VALUE = simbol("state",podaci.Naziv), inicijalizirati = simbol("init",podaci.Naziv);
            Collections.addAll(Linija,".bss",".balign 4",stanje_VALUE + ": .long 0",".text",inicijalizirati + ":","cmpl $0, " + stanje_VALUE,"jne " + inicijalizirati + "_done","movl $1, " + stanje_VALUE);
            metoda_Reference 초기화참조 = new metoda_Reference(podaci.Naziv,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Linija.add("call " + simbol("method",초기화참조.부분들()));
            Collections.addAll(Linija,"movl $2, " + stanje_VALUE,inicijalizirati + "_done:","ret");
            for (član_podaci polje_VALUE : podaci.polje_VALUE) {
                byte[] konstanta_VALUE = polje_VALUE.atribut_VALUE.get("ConstantValue"); String VALUE = konstanta_VALUE == null ? "0" : X_86_konstanta(podaci,new podaci_Čitač(konstanta_VALUE).두바이트());
                Collections.addAll(Linija,".data",".balign 4",simbol("field",podaci.Naziv,polje_VALUE.Naziv,polje_VALUE.서술) + ": .long " + VALUE);
            }
            for (član_podaci FUNCTION_VALUE : podaci.FUNCTION_VALUE) if (!FUNCTION_VALUE.Naziv.equals("<init>")) Linija.add(X_86_metoda_tijelo(new metoda_Reference(podaci.Naziv,FUNCTION_VALUE.Naziv,FUNCTION_VALUE.서술),FUNCTION_VALUE,mašina_tabela,cilj));
        }
        Collections.addAll(Linija,".text",".globl java_entry","java_entry:","call " + simbol("init",unos_p_VALUE.vlasnik_VALUE),"call " + simbol("method",unos_p_VALUE.부분들()));
        if (unos_p_VALUE.서술.equals("()V")) Linija.add("xorl %eax, %eax"); Linija.add("ret");
        for (String dodijeliti_VALUE : 내보냄) {
            int graničnik_VALUE = dodijeliti_VALUE.indexOf('='); if (graničnik_VALUE < 1) throw new Prevođenje_greška("내보내기 dodijeliti_VALUE GRESKA");
            String iz_eksternog_izvora_VALUE = dodijeliti_VALUE.substring(0,graničnik_VALUE), FUNCTION_VALUE = dodijeliti_VALUE.substring(graničnik_VALUE + 1); int dijeljenje_mjera = FUNCTION_VALUE.lastIndexOf('.');
            if (dijeljenje_mjera < 0 || !iz_eksternog_izvora_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Prevođenje_greška("내보내기 simbol GRESKA");
            String klasa_VALUE = FUNCTION_VALUE.substring(0,dijeljenje_mjera).replace('.','/'), Naziv = FUNCTION_VALUE.substring(dijeljenje_mjera + 1); metoda_Reference izbor_VALUE = null;
            for (metoda_Reference Reference : 함수들.keySet()) if (Reference.vlasnik_VALUE.equals(klasa_VALUE) && Reference.Naziv.equals(Naziv)) { if (izbor_VALUE != null) throw new Prevođenje_greška("겹친 내보내기 cilj"); izbor_VALUE = Reference; }
            if (izbor_VALUE == null) throw new Prevođenje_greška("내보낼 함수가 없음");
            Collections.addAll(Linija,".text",".globl " + iz_eksternog_izvora_VALUE,iz_eksternog_izvora_VALUE + ":","call " + simbol("init",izbor_VALUE.vlasnik_VALUE),"jmp " + simbol("method",izbor_VALUE.부분들()));
        }
        Linija.add(".section .rodata");
        for (Map.Entry<String,String> unos_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Linija,".balign 4",unos_VALUE.getValue() + ":",".long " + unos_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lekcija_VALUE : unos_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(lekcija_VALUE)); if (!단위들.isEmpty()) Linija.add(".long " + String.join(",",단위들));
        }
        Linija.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Linija) + "\n";
    }
    static void Izvrši_alatka(List<String> Naredba) throws Exception {
        if (new ProcessBuilder(Naredba).inheritIO().start().waitFor() != 0) throw new Prevođenje_greška("napraviti_izvor GRESKA: " + Naredba.get(0));
    }
    static String podaci_string(String Tekst) { return "\"" + Tekst.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Prevođenje(List<Path> 입력들, String cilj, String unos_p, List<String> 내보냄, Path Ispis, Path resurs_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), klasa_put = 임시.resolve("classes"); Files.createDirectory(klasa_put);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",klasa_put.toString(),"-sourcepath",klasa_put.toString(),"-d",klasa_put.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int izvor_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Ispis.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Prevođenje_greška("Ispis 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); izvor_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Prevođenje_greška(".java 또는 .class만 Podrška_VALUE");
            }
            if (izvor_COUNT > 0) Izvrši_alatka(자바명령);
            try (java.util.stream.Stream<Path> put_spisak = Files.walk(klasa_put)) { put_spisak.filter(Putanja -> Putanja.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,cilj.equals("user") ? "user" : "kernel",262144,resurs_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(unos_p,내보냄,cilj); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path alatka_položaj = resurs_VALUE.getParent();
            Izvrši_alatka(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Izvrši_alatka(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),alatka_položaj.resolve("zajednička_jezička_biblioteka_Podrška.s").toString()));
            List<String> Spoji_se = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (cilj.equals("kernel")) Spoji_se.add("-r");
            else {
                Izvrši_alatka(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),alatka_položaj.resolve(cilj.equals("user") ? "START_korisnik_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(Spoji_se,"-e","_start",임시.resolve("start.o").toString());
                if (cilj.equals("user")) Collections.addAll(Spoji_se,"-T",alatka_položaj.resolve("korisnik_Veza_izgled.ld").toString());
            }
            Collections.addAll(Spoji_se,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Izvrši_alatka(Spoji_se);
            Ispis = Ispis.toAbsolutePath(); Files.createDirectories(Ispis.getParent()); Path objavi_VALUE = Files.createTempFile(Ispis.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),objavi_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(objavi_VALUE,Ispis,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(objavi_VALUE); }
            Files.setPosixFilePermissions(Ispis,java.nio.file.attribute.PosixFilePermissions.fromString(cilj.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Ispis + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbol_podaci = new ArrayList<>(), izvorni_podaci = new ArrayList<>();
            for (metoda_Reference Reference : CONVERT_VALUE.함수들.keySet()) simbol_podaci.add(podaci_string(simbol("method",Reference.부분들())) + ":" + podaci_string(Reference.vlasnik_VALUE + "." + Reference.Naziv + Reference.서술));
            for (Path 입력 : 입력들) {
                byte[] raspršivanje_fajl = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Tekst = new StringBuilder(); for (byte VALUE : raspršivanje_fajl) Tekst.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                izvorni_podaci.add(podaci_string(입력.toAbsolutePath().toString()) + ":" + podaci_string(Tekst.toString()));
            }
            Files.writeString(Paths.get(Ispis + ".json"),"{\"target\":" + podaci_string(cilj) + ",\"entry\":" + podaci_string(unos_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbol_podaci) + "},\"sources\":{" + String.join(",",izvorni_podaci) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> put_spisak = Files.walk(임시)) { for (Path Putanja : (Iterable<Path>)put_spisak.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Putanja); }
        }
    }
    public static void main(String[] Argumenti) {
        try {
            String unos_p = null, cilj = "kernel", X_86_cilj = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> put_spisak = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumenti.length; 순번++) {
                String VALUE = Argumenti[순번];
                switch (VALUE) {
                    case "--target": X_86_cilj = Argumenti[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry klasa_VALUE.FUNCTION_VALUE -o Ispis [--target linux|kernel|user] [--profile kernel|user] [--export simbol=klasa_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": unos_p = Argumenti[++순번]; break;
                    case "--profile": cilj = Argumenti[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumenti[++순번]); break;
                    case "--export": 내보냄.add(Argumenti[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argumenti[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Prevođenje_greška("알 수 없는 옵션: " + VALUE); put_spisak.add(Paths.get(VALUE));
                }
            }
            if (unos_p == null || 출력경로 == null || put_spisak.isEmpty()) throw new Prevođenje_greška("--entry, -o, klasa_VALUE 파일이 필요합니다");
            Path resurs_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_cilj != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_cilj)) throw new Prevođenje_greška("알 수 없는 Izvrši_komanda cilj");
                X_86_Prevođenje(put_spisak,X_86_cilj,unos_p,내보냄,출력경로,resurs_VALUE); return;
            }
            String IZVOR = new 기계어미리번역(put_spisak, cilj, 낱말수, resurs_VALUE).generirati(unos_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, IZVOR, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception GRESKA) { System.err.println("napraviti_izvor GRESKA: " + GRESKA.getMessage()); System.exit(1); }
    }
}
