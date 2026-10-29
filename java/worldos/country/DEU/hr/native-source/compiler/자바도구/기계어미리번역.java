// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java poduka_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. domaćin JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Prevođenje_pogreška extends RuntimeException {
        Prevođenje_pogreška(String 설명) { super(설명); }
    }
    static final class podaci_Čitač {
        final byte[] podaci;
        int Položaj;
        podaci_Čitač(byte[] 입력자료) { podaci = 입력자료; }
        byte[] Čitaj(int 길이) {
            if (길이 < 0 || 길이 > podaci.length - Položaj) throw new Prevođenje_pogreška("잘린 poduka_VALUE 또는 Naredba podaci");
            byte[] REZULTAT = Arrays.copyOfRange(podaci, Položaj, Položaj + 길이); Položaj += 길이; return REZULTAT;
        }
        int 한바이트() { if (Položaj >= podaci.length) throw new Prevođenje_pogreška("잘린 Naredba podaci"); return podaci[Položaj++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class član_podaci {
        final int pristup_unos;
        final String Ime, 서술;
        final Map<String, byte[]> atribut_VALUE;
        član_podaci(int pristup_VALUE, String naziv_VALUE, String 서술값, Map<String, byte[]> atribut_podaci) {
            pristup_unos = pristup_VALUE; Ime = naziv_VALUE; 서술 = 서술값; atribut_VALUE = atribut_podaci;
        }
    }
    static final class postupak_Reference implements Comparable<postupak_Reference> {
        final String vlasnik_VALUE, Ime, 서술;
        postupak_Reference(String 소유값, String naziv_VALUE, String 서술값) { vlasnik_VALUE = 소유값; Ime = naziv_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{vlasnik_VALUE, Ime, 서술}; }
        public int compareTo(postupak_Reference ravnopravan_član_VALUE) {
            int Usporedba_VALUE = vlasnik_VALUE.compareTo(ravnopravan_član_VALUE.vlasnik_VALUE);
            if (Usporedba_VALUE == 0) Usporedba_VALUE = Ime.compareTo(ravnopravan_član_VALUE.Ime);
            return Usporedba_VALUE == 0 ? 서술.compareTo(ravnopravan_član_VALUE.서술) : Usporedba_VALUE;
        }
        public boolean equals(Object ravnopravan_član_VALUE) { return ravnopravan_član_VALUE instanceof postupak_Reference && compareTo((postupak_Reference) ravnopravan_član_VALUE) == 0; }
        public int hashCode() { return Objects.hash(vlasnik_VALUE, Ime, 서술); }
    }
    static final class poduka_podaci {
        final int[] 상수종류;
        final Object[] konstanta_podaci;
        final String Ime;
        final List<član_podaci> vrijednost_polja, FUNCTION_VALUE;
        poduka_podaci(Path PUTANJA) throws IOException {
            podaci_Čitač Čitač_VALUE = new podaci_Čitač(Files.readAllBytes(PUTANJA));
            if (Čitač_VALUE.네바이트() != 0xcafebabe) throw new Prevođenje_pogreška("Java poduka_VALUE 표식이 아님");
            Čitač_VALUE.Čitaj(4);
            int artikl_COUNT = Čitač_VALUE.두바이트(); 상수종류 = new int[artikl_COUNT]; konstanta_podaci = new Object[artikl_COUNT];
            for (int 순번 = 1; 순번 < artikl_COUNT; 순번++) {
                int 종류 = Čitač_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int 길이 = Čitač_VALUE.두바이트();
                        byte[] znak_međuspremnik = Čitač_VALUE.Čitaj(길이), 길이붙인자료 = new byte[길이 + 2];
                        길이붙인자료[0] = (byte)(길이 >> 8); 길이붙인자료[1] = (byte)길이;
                        System.arraycopy(znak_međuspremnik, 0, 길이붙인자료, 2, 길이);
                        konstanta_podaci[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstanta_podaci[순번] = Čitač_VALUE.네바이트(); break;
                    case 4: Čitač_VALUE.Čitaj(4); break;
                    case 5: case 6: Čitač_VALUE.Čitaj(8); 순번++; break;
                    case 7: case 8: case 16: konstanta_podaci[순번] = Čitač_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstanta_podaci[순번] = new int[]{Čitač_VALUE.두바이트(), Čitač_VALUE.두바이트()}; break;
                    case 15: konstanta_podaci[순번] = new int[]{Čitač_VALUE.한바이트(), Čitač_VALUE.두바이트()}; break;
                    default: throw new Prevođenje_pogreška("지원하지 않는 konstanta_VALUE 종류: " + 종류);
                }
            }
            Čitač_VALUE.두바이트(); Ime = naziv_klase(Čitač_VALUE.두바이트());
            if (!naziv_klase(Čitač_VALUE.두바이트()).equals("java/lang/Object") || Čitač_VALUE.두바이트() != 0)
                throw new Prevođenje_pogreška(Ime + ": 상속 및 인터페이스 미지원");
            vrijednost_polja = 멤버읽기(Čitač_VALUE); FUNCTION_VALUE = 멤버읽기(Čitač_VALUE); 속성읽기(Čitač_VALUE);
            if (Čitač_VALUE.Položaj != Čitač_VALUE.podaci.length) throw new Prevođenje_pogreška("poduka_VALUE 뒤에 남은 podaci");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Prevođenje_pogreška("문자 konstanta_VALUE INDEX GREŠKA");
            return (String) konstanta_podaci[INDEX];
        }
        String naziv_klase(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Prevođenje_pogreška("poduka_VALUE Reference GREŠKA");
            return 문자((Integer)konstanta_podaci[INDEX]);
        }
        postupak_Reference Reference(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Prevođenje_pogreška("멤버 Reference GREŠKA");
            int[] upariti_VALUE = (int[])konstanta_podaci[INDEX], naziv_upariti = (int[])konstanta_podaci[upariti_VALUE[1]];
            return new postupak_Reference(naziv_klase(upariti_VALUE[0]), 문자(naziv_upariti[0]), 문자(naziv_upariti[1]));
        }
        Map<String, byte[]> 속성읽기(podaci_Čitač Čitač_VALUE) {
            Map<String, byte[]> REZULTAT = new LinkedHashMap<>();
            int artikl_COUNT = Čitač_VALUE.두바이트();
            for (int 순번 = 0; 순번 < artikl_COUNT; 순번++) {
                String atribut_naziv = 문자(Čitač_VALUE.두바이트()); byte[] VALUE = Čitač_VALUE.Čitaj(Čitač_VALUE.네바이트());
                if (REZULTAT.put(atribut_naziv, VALUE) != null) throw new Prevođenje_pogreška("겹친 atribut_VALUE: " + atribut_naziv);
            }
            return REZULTAT;
        }
        List<član_podaci> 멤버읽기(podaci_Čitač Čitač_VALUE) {
            List<član_podaci> REZULTAT = new ArrayList<>(); int artikl_COUNT = Čitač_VALUE.두바이트();
            for (int 순번 = 0; 순번 < artikl_COUNT; 순번++) {
                int pristup_unos = Čitač_VALUE.두바이트(); String postupak_unos_naziv = 문자(Čitač_VALUE.두바이트()), 서술 = 문자(Čitač_VALUE.두바이트());
                REZULTAT.add(new član_podaci(pristup_unos, postupak_unos_naziv, 서술, 속성읽기(Čitač_VALUE)));
            }
            return REZULTAT;
        }
    }
    static final class 함수형식 {
        final List<String> Argumenti = new ArrayList<>();
        final String vratiti_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Prevođenje_pogreška("FUNCTION_VALUE 서술 GREŠKA: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Prevođenje_pogreška("FUNCTION_VALUE 서술 GREŠKA: " + 서술);
            Argumenti.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumenti.contains("V") || 반환들.size() != 1) throw new Prevođenje_pogreška("FUNCTION_VALUE 서술 GREŠKA: " + 서술);
            vratiti_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> REZULTAT = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Položaj = 0; Položaj < 서술.length();) {
            String odabir_VALUE = null;
            for (String oblik_VALUE : 허용형식) if (서술.startsWith(oblik_VALUE, Položaj)) { odabir_VALUE = oblik_VALUE; break; }
            if (odabir_VALUE == null) throw new Prevođenje_pogreška("지원하지 않는 vrsta_podataka: " + 서술);
            REZULTAT.add(odabir_VALUE); Položaj += odabir_VALUE.length();
        }
        return REZULTAT;
    }
    static String simbol(String 종류, String... 부분들) {
        try {
            byte[] raspršivanje_Datoteka = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Tekst = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Tekst.append(String.format(Locale.ROOT, "%02x", raspršivanje_Datoteka[순번] & 255));
            return Tekst.toString();
        } catch (Exception GREŠKA) { throw new Prevođenje_pogreška(GREŠKA.toString()); }
    }
    final Map<String, poduka_podaci> 클래스들 = new TreeMap<>();
    final Map<postupak_Reference, član_podaci> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), stroj_Azure_Functions_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, stroj_poduka;
    final int 동적기억낱말수;
    final Path resurs_put;
    기계어미리번역(List<Path> put_Popis, String cilj, int 낱말수, Path resurs_VALUE) throws IOException {
        if ((!cilj.equals("kernel") && !cilj.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Prevođenje_pogreška("Izvrši_naredba cilj 또는 Memorija_VALUE adresa_regije Veličina GREŠKA");
        실행대상 = cilj; 동적기억낱말수 = 낱말수; resurs_put = resurs_VALUE;
        // 이 이름도 국가별 izvor_stablo generirati 시 해당 언어로 옮긴다.
        stroj_poduka = cilj.equals("kernel") ? "pano" : "korisnik";
        for (String red : Files.readAllLines(resurs_VALUE.resolve("stroj_Azure_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = red.split("\t", -1);
            if (부분들.length != 4) throw new Prevođenje_pogreška("stroj FUNCTION_VALUE podaci GREŠKA");
            if (부분들[0].equals(cilj)) stroj_Azure_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path PUTANJA : put_Popis) {
            poduka_podaci podaci = new poduka_podaci(PUTANJA);
            if (클래스들.put(podaci.Ime, podaci) != null) throw new Prevođenje_pogreška("중복 poduka_VALUE: " + podaci.Ime);
            for (član_podaci vrijednost_polja : podaci.vrijednost_polja) {
                if ((vrijednost_polja.pristup_unos & 8) == 0 || 형식읽기(vrijednost_polja.서술).equals(Collections.singletonList("V"))) throw new Prevođenje_pogreška("정적 필드만 Podrška_VALUE");
                if (필드들.put(new postupak_Reference(podaci.Ime, vrijednost_polja.Ime, vrijednost_polja.서술), vrijednost_polja) != null) throw new Prevođenje_pogreška("중복 vrijednost_polja");
            }
            for (član_podaci FUNCTION_VALUE : podaci.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Ime.equals("<init>")) continue;
                if ((FUNCTION_VALUE.pristup_unos & 8) == 0 || (FUNCTION_VALUE.pristup_unos & (0x20 | 0x400)) != 0) throw new Prevođenje_pogreška("정적 비동기화 함수만 Podrška_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new postupak_Reference(podaci.Ime, FUNCTION_VALUE.Ime, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Prevođenje_pogreška("중복 FUNCTION_VALUE");
            }
        }
    }
    String niz_simbol(String Tekst) { return 문자열들.computeIfAbsent(Tekst, VALUE -> "j_text_" + 문자열들.size()); }
    String konstanta_izraz(poduka_podaci podaci, int INDEX) {
        if (INDEX < 1 || INDEX >= podaci.상수종류.length) throw new Prevođenje_pogreška("konstanta_VALUE INDEX isječak GREŠKA");
        if (podaci.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + podaci.konstanta_podaci[INDEX] + ")";
        if (podaci.상수종류[INDEX] == 8) return "(word)" + niz_simbol(podaci.문자((Integer)podaci.konstanta_podaci[INDEX]));
        throw new Prevođenje_pogreška("정수와 niz_VALUE 상수만 Podrška_VALUE");
    }
    String 함수원형(postupak_Reference Reference) {
        List<String> 인수들 = new ArrayList<>(); int artikl_COUNT = new 함수형식(Reference.서술).Argumenti.size();
        for (int 순번 = 0; 순번 < artikl_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbol("method", Reference.부분들()) + "(" + (artikl_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void 지역검사(int INDEX, int lokalno_varijabla_COUNT) { if (INDEX < 0 || INDEX >= lokalno_varijabla_COUNT) throw new Prevođenje_pogreška("lokalno_doseg varijabla_VALUE INDEX isječak GREŠKA"); }
    void 분기넣기(List<String> Izlaz, Set<Integer> grana_Popis, int Položaj, int 이동량, String uvjet) {
        int odredište_VALUE = Položaj + 이동량; grana_Popis.add(odredište_VALUE);
        Izlaz.add((uvjet == null ? "" : "if (" + uvjet + ") ") + "goto b" + odredište_VALUE + ";");
    }
    String postupak_tijelo(postupak_Reference FUNCTION_VALUE, član_podaci podaci) {
        byte[] tijelo_podaci = podaci.atribut_VALUE.get("Code"); if (tijelo_podaci == null) throw new Prevođenje_pogreška("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Ime);
        podaci_Čitač Čitač_VALUE = new podaci_Čitač(tijelo_podaci); int 쌓임깊이 = Čitač_VALUE.두바이트(), lokalno_varijabla_COUNT = Čitač_VALUE.두바이트();
        podaci_Čitač naredba_podaci = new podaci_Čitač(Čitač_VALUE.Čitaj(Čitač_VALUE.네바이트()));
        if (Čitač_VALUE.두바이트() != 0) throw new Prevođenje_pogreška("try/catch/finally 미지원");
        함수형식 oblik_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokalno_varijabla_COUNT < oblik_VALUE.Argumenti.size()) throw new Prevođenje_pogreška("매개변수보다 적은 lokalno_doseg varijabla_VALUE");
        poduka_podaci poduka_VALUE = 클래스들.get(FUNCTION_VALUE.vlasnik_VALUE);
        List<String> Izlaz = new ArrayList<>(); Izlaz.add(함수원형(FUNCTION_VALUE) + " {");
        Izlaz.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(lokalno_varijabla_COUNT, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < oblik_VALUE.Argumenti.size(); 순번++) Izlaz.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), grana_Popis = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (naredba_podaci.Položaj < naredba_podaci.podaci.length) {
            int Položaj = naredba_podaci.Položaj, Naredba = naredba_podaci.한바이트(); 경계들.add(Položaj); Izlaz.add("b" + Položaj + ":;");
            if (Naredba == 0) continue;
            if (Naredba == 1) Izlaz.add("PUSH(0);");
            else if (Naredba >= 2 && Naredba <= 8) Izlaz.add("PUSH((uint32_t)(" + (Naredba - 3) + "));");
            else if (Naredba == 16 || Naredba == 17) Izlaz.add("PUSH((uint32_t)(" + (Naredba == 16 ? naredba_podaci.부호한바이트() : naredba_podaci.부호두바이트()) + "));");
            else if (Naredba == 18 || Naredba == 19) Izlaz.add("PUSH(" + konstanta_izraz(poduka_VALUE, Naredba == 18 ? naredba_podaci.한바이트() : naredba_podaci.두바이트()) + ");");
            else if (Naredba == 21 || Naredba == 25 || (Naredba >= 26 && Naredba <= 29) || (Naredba >= 42 && Naredba <= 45)) {
                int INDEX = Naredba == 21 || Naredba == 25 ? naredba_podaci.한바이트() : Naredba - (Naredba <= 29 ? 26 : 42);
                지역검사(INDEX, lokalno_varijabla_COUNT); Izlaz.add("PUSH(l[" + INDEX + "]);");
            } else if (Naredba == 54 || Naredba == 58 || (Naredba >= 59 && Naredba <= 62) || (Naredba >= 75 && Naredba <= 78)) {
                int INDEX = Naredba == 54 || Naredba == 58 ? naredba_podaci.한바이트() : Naredba - (Naredba <= 62 ? 59 : 75);
                지역검사(INDEX, lokalno_varijabla_COUNT); Izlaz.add("l[" + INDEX + "] = POP();");
            } else if (Naredba == 46) Izlaz.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Naredba == 79) Izlaz.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Naredba == 87 || Naredba == 88) Izlaz.add(Naredba == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Naredba >= 89 && Naredba <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] narudžba_Popis = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Naredba - 89]; 순번++) Izlaz.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : narudžba_Popis[Naredba - 89].toCharArray()) Izlaz.add("PUSH(" + VALUE + ");");
            } else if (Naredba == 96 || Naredba == 100 || Naredba == 104 || Naredba == 126 || Naredba == 128 || Naredba == 130) {
                String operacija_VALUE = Naredba == 96 ? "+" : Naredba == 100 ? "-" : Naredba == 104 ? "*" : Naredba == 126 ? "&" : Naredba == 128 ? "|" : "^";
                Izlaz.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operacija_VALUE + " (uint32_t)b);");
            } else if (Naredba == 108 || Naredba == 112) Izlaz.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Naredba == 112 ? 1 : 0) + "));");
            else if (Naredba == 116) Izlaz.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Naredba == 120 || Naredba == 122 || Naredba == 124) {
                Izlaz.add("b = POP(); a = POP();"); Izlaz.add("PUSH(" + (Naredba == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Naredba == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Naredba == 132) {
                int INDEX = naredba_podaci.한바이트(), inkrement_iznos = naredba_podaci.부호한바이트(); 지역검사(INDEX, lokalno_varijabla_COUNT);
                Izlaz.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + inkrement_iznos + ");");
            } else if (Naredba >= 145 && Naredba <= 147) Izlaz.add("a = POP(); PUSH((uint32_t)(" + (Naredba == 145 ? "int8_t" : Naredba == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Naredba >= 153 && Naredba <= 158) {
                Izlaz.add("a = POP();"); 분기넣기(Izlaz, grana_Popis, Položaj, naredba_podaci.부호두바이트(), "(int32_t)a " + 비교들[Naredba - 153] + " 0");
            } else if (Naredba >= 159 && Naredba <= 166) {
                Izlaz.add("b = POP(); a = POP();"); 분기넣기(Izlaz, grana_Popis, Položaj, naredba_podaci.부호두바이트(), Naredba >= 165 ? "a " + 비교들[Naredba - 159] + " b" : "(int32_t)a " + 비교들[Naredba - 159] + " (int32_t)b");
            } else if (Naredba == 167 || Naredba == 200) 분기넣기(Izlaz, grana_Popis, Položaj, Naredba == 167 ? naredba_podaci.부호두바이트() : naredba_podaci.네바이트(), null);
            else if (Naredba == 170 || Naredba == 171) {
                while (naredba_podaci.Položaj % 4 != 0) naredba_podaci.한바이트();
                int zadana_vrijednost = naredba_podaci.네바이트(); Izlaz.add("a = POP();");
                if (Naredba == 170) {
                    int 아래 = naredba_podaci.네바이트(), 위 = naredba_podaci.네바이트(); long artikl_COUNT = (long)위 - 아래 + 1;
                    if (artikl_COUNT < 1 || artikl_COUNT > (naredba_podaci.podaci.length - naredba_podaci.Položaj) / 4) throw new Prevođenje_pogreška("switch isječak GREŠKA");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Izlaz, grana_Popis, Položaj, naredba_podaci.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int artikl_COUNT = naredba_podaci.네바이트(), prednja_podaci = 0;
                    if (artikl_COUNT < 0 || artikl_COUNT > (naredba_podaci.podaci.length - naredba_podaci.Položaj) / 8) throw new Prevođenje_pogreška("switch Veličina GREŠKA");
                    for (int 순번 = 0; 순번 < artikl_COUNT; 순번++) {
                        int VALUE = naredba_podaci.네바이트(); if (순번 > 0 && VALUE <= prednja_podaci) throw new Prevođenje_pogreška("switch narudžba_VALUE GREŠKA"); prednja_podaci = VALUE;
                        분기넣기(Izlaz, grana_Popis, Položaj, naredba_podaci.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Izlaz, grana_Popis, Položaj, zadana_vrijednost, null);
            } else if (Naredba == 172 || Naredba == 176 || Naredba == 177) Izlaz.add("return " + (Naredba == 177 ? "0" : "POP()") + ";");
            else if (Naredba == 178 || Naredba == 179) {
                postupak_Reference Reference = poduka_VALUE.Reference(naredba_podaci.두바이트()); if (!필드들.containsKey(Reference)) throw new Prevođenje_pogreška("알 수 없는 vrijednost_polja");
                Izlaz.add(simbol("init", Reference.vlasnik_VALUE) + "();"); String vrijednost_polja = simbol("field", Reference.부분들());
                Izlaz.add(Naredba == 178 ? "PUSH(" + vrijednost_polja + ");" : vrijednost_polja + " = POP();");
            } else if (Naredba == 184) {
                postupak_Reference Reference = poduka_VALUE.Reference(naredba_podaci.두바이트()); if (!함수들.containsKey(Reference)) throw new Prevođenje_pogreška("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Reference.서술); int artikl_COUNT = 호출형식.Argumenti.size();
                Izlaz.add(simbol("init", Reference.vlasnik_VALUE) + "();"); Izlaz.add("if(sp < " + artikl_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + artikl_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < artikl_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Izlaz.add("a = " + simbol("method", Reference.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.vratiti_KR.equals("V")) Izlaz.add("PUSH(a);");
            } else if (Naredba == 182) {
                postupak_Reference Reference = poduka_VALUE.Reference(naredba_podaci.두바이트());
                if (Reference.equals(new postupak_Reference("java/lang/String", "length", "()I"))) Izlaz.add("a = POP(); PUSH(length(a));");
                else if (Reference.equals(new postupak_Reference("java/lang/String", "charAt", "(I)C"))) Izlaz.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Prevođenje_pogreška("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Naredba == 188) {
                if (naredba_podaci.한바이트() != 10) throw new Prevođenje_pogreška("new int[]만 Podrška_VALUE"); Izlaz.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Naredba == 190) Izlaz.add("a = POP(); PUSH(length(a));");
            else if (Naredba == 196) {
                int nastavak_VALUE = naredba_podaci.한바이트(), INDEX = naredba_podaci.두바이트(); 지역검사(INDEX, lokalno_varijabla_COUNT);
                if (nastavak_VALUE == 21 || nastavak_VALUE == 25) Izlaz.add("PUSH(l[" + INDEX + "]);");
                else if (nastavak_VALUE == 54 || nastavak_VALUE == 58) Izlaz.add("l[" + INDEX + "] = POP();");
                else if (nastavak_VALUE == 132) Izlaz.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + naredba_podaci.부호두바이트() + ");");
                else throw new Prevođenje_pogreška("미지원 wide Naredba");
            } else if (Naredba == 198 || Naredba == 199) {
                Izlaz.add("a = POP();"); 분기넣기(Izlaz, grana_Popis, Položaj, naredba_podaci.부호두바이트(), "a " + (Naredba == 198 ? "==" : "!=") + " 0");
            } else throw new Prevođenje_pogreška(FUNCTION_VALUE.vlasnik_VALUE + "." + FUNCTION_VALUE.Ime + ", bajt_VALUE " + Položaj + ": 미지원 Naredba " + Naredba);
        }
        if (!경계들.containsAll(grana_Popis)) throw new Prevođenje_pogreška("Naredba 경계가 아닌 곳으로 grana");
        Izlaz.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Izlaz);
    }
    String izvezi_postupak(String veza_simbol, String cilj, boolean 진입점여부) {
        int indeks_položaja = cilj.lastIndexOf('.'); if (indeks_položaja < 0 || !veza_simbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Prevođenje_pogreška("내보내기 Dodijeli_VALUE GREŠKA");
        String vlasnik_VALUE = cilj.substring(0, indeks_položaja).replace('.', '/'), Ime = cilj.substring(indeks_položaja + 1); postupak_Reference odabir_VALUE = null;
        for (postupak_Reference Reference : 함수들.keySet()) if (Reference.vlasnik_VALUE.equals(vlasnik_VALUE) && Reference.Ime.equals(Ime)) {
            if (odabir_VALUE != null) throw new Prevođenje_pogreška("겹친 내보내기 cilj"); odabir_VALUE = Reference;
        }
        if (odabir_VALUE == null || (함수들.get(odabir_VALUE).pristup_unos & 0x100) != 0) throw new Prevođenje_pogreška("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 oblik_VALUE = new 함수형식(odabir_VALUE.서술);
        if ((진입점여부 && !oblik_VALUE.Argumenti.isEmpty()) || !Arrays.asList("V", "I").contains(oblik_VALUE.vratiti_KR)) throw new Prevođenje_pogreška("unos_p_VALUE 또는 C 경계 oblik_VALUE GREŠKA");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < oblik_VALUE.Argumenti.size(); 순번++) {
            if (!oblik_VALUE.Argumenti.get(순번).equals("I")) throw new Prevođenje_pogreška("C 경계는 int 인수만 Podrška_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (oblik_VALUE.vratiti_KR.equals("V") ? "void " : "int32_t ") + veza_simbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbol("init", odabir_VALUE.vlasnik_VALUE) + "(); " + (oblik_VALUE.vratiti_KR.equals("V") ? "" : "return (int32_t)") + simbol("method", odabir_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generirati(String unos_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<postupak_Reference, član_podaci> unos_VALUE : 함수들.entrySet()) {
            postupak_Reference Reference = unos_VALUE.getKey(); član_podaci podaci = unos_VALUE.getValue(); 선언들.add(함수원형(Reference) + ";");
            if ((podaci.pristup_unos & 0x100) != 0) {
                String Spoji_se = stroj_Azure_Functions_c3a8e64a.get(Reference.Ime + Reference.서술);
                if (!Reference.vlasnik_VALUE.equals(stroj_poduka) || Spoji_se == null) throw new Prevođenje_pogreška("허용되지 않은 native FUNCTION_VALUE: " + Reference.Ime);
                int artikl_COUNT = new 함수형식(Reference.서술).Argumenti.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < artikl_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Spoji_se + "(" + (artikl_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(artikl_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Reference) + " { return " + Spoji_se + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(postupak_tijelo(Reference, podaci));
        }
        for (Map.Entry<postupak_Reference, član_podaci> unos_VALUE : 필드들.entrySet()) {
            postupak_Reference Reference = unos_VALUE.getKey(); byte[] konstanta_VALUE = unos_VALUE.getValue().atribut_VALUE.get("ConstantValue");
            String VALUE = konstanta_VALUE == null ? "0" : konstanta_izraz(클래스들.get(Reference.vlasnik_VALUE), new podaci_Čitač(konstanta_VALUE).두바이트());
            필드선언들.add("static word " + simbol("field", Reference.부분들()) + " = " + VALUE + ";");
        }
        for (String Ime : 클래스들.keySet()) {
            String 초기화 = simbol("init", Ime), Stanje_VALUE = simbol("state", Ime);
            선언들.add("static void " + 초기화 + "(void);"); 필드선언들.add("static unsigned " + Stanje_VALUE + ";");
            postupak_Reference Reference = new postupak_Reference(Ime, "<clinit>", "()V");
            몸체들.add("static void " + 초기화 + "(void) { if(" + Stanje_VALUE + ") return; " + Stanje_VALUE + " = 1; " + (함수들.containsKey(Reference) ? simbol("method", Reference.부분들()) + "(); " : "") + Stanje_VALUE + " = 2; }");
        }
        몸체들.add(izvezi_postupak("java_entry", unos_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Dodijeli_VALUE : 내보내기목록) {
            int indeks_položaja = Dodijeli_VALUE.indexOf('='); if (indeks_položaja < 1) throw new Prevođenje_pogreška("내보내기 Dodijeli_VALUE GREŠKA");
            String Ime = Dodijeli_VALUE.substring(0, indeks_položaja); 공개이름.add(Ime); 몸체들.add(izvezi_postupak(Ime, Dodijeli_VALUE.substring(indeks_položaja + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> unos_VALUE : 문자열들.entrySet()) {
            String Tekst = unos_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + unos_VALUE.getValue() + "[] = {" + Tekst.length());
            for (int 순번 = 0; 순번 < Tekst.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Tekst.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Podrška_VALUE = Files.readString(resurs_put.resolve("CLR_Podrška.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Podrška_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String IZVOR, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> naziv_tablica = new HashMap<>();
        for (String red : Files.readAllLines(resurs_put.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] upariti_VALUE = red.split("\t"); naziv_tablica.put(upariti_VALUE[0], upariti_VALUE[1]);
        }
        Pattern blok_izraz = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = blok_izraz.matcher(IZVOR); StringBuffer REZULTAT = new StringBuffer();
        while (찾개.find()) {
            String Ime = 찾개.group(), 새이름 = Ime;
            if (!Ime.startsWith("//") && !Ime.startsWith("/*") && !Ime.startsWith("\"") && !Ime.startsWith("'") && !공개이름.contains(Ime)) {
                새이름 = naziv_tablica.getOrDefault(Ime, Ime);
                if (Ime.matches("a[0-9]+")) 새이름 = "Argumenti" + Ime.substring(1);
                if (Ime.matches("b[0-9]+")) 새이름 = "grana" + Ime.substring(1);
                if (범용표기) {
                    StringBuilder notacija_VALUE = new StringBuilder();
                    for (char znak_VALUE : 새이름.toCharArray()) notacija_VALUE.append(znak_VALUE < 128 ? Character.toString(znak_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)znak_VALUE));
                    새이름 = notacija_VALUE.toString();
                }
            }
            찾개.appendReplacement(REZULTAT, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(REZULTAT); return REZULTAT.toString();
    }
    String X_86_postupak_tijelo(postupak_Reference FUNCTION_VALUE, član_podaci podaci, Map<String,String> stroj_tablica, String cilj) {
        String marker_VALUE = simbol("method", FUNCTION_VALUE.부분들());
        List<String> red = new ArrayList<>();
        if ((podaci.pristup_unos & 0x100) != 0) {
            String Spoji_se = stroj_tablica.get(FUNCTION_VALUE.Ime + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.vlasnik_VALUE.equals(cilj.equals("kernel") ? "uređaj_VALUE" : "korisnik") || Spoji_se == null) throw new Prevođenje_pogreška("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + marker_VALUE + ":\njmp " + Spoji_se;
        }
        byte[] tijelo_teksta = podaci.atribut_VALUE.get("Code"); if (tijelo_teksta == null) throw new Prevođenje_pogreška("FUNCTION_VALUE 몸체가 없음");
        podaci_Čitač Čitač_VALUE = new podaci_Čitač(tijelo_teksta); Čitač_VALUE.두바이트(); int lokalno_COUNT = Čitač_VALUE.두바이트();
        podaci_Čitač naredba_podaci = new podaci_Čitač(Čitač_VALUE.Čitaj(Čitač_VALUE.네바이트()));
        if (Čitač_VALUE.두바이트() != 0) throw new Prevođenje_pogreška("try/catch/finally 미지원");
        함수형식 oblik_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokalno_COUNT < oblik_VALUE.Argumenti.size()) throw new Prevođenje_pogreška("매개변수보다 적은 lokalno_doseg varijabla_VALUE");
        Collections.addAll(red,".text",".globl " + marker_VALUE,".type " + marker_VALUE + ", @function",marker_VALUE + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokalno_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < oblik_VALUE.Argumenti.size(); 순번++) Collections.addAll(red,"movl " + (8 + 4 * (oblik_VALUE.Argumenti.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        poduka_podaci poduka_VALUE = 클래스들.get(FUNCTION_VALUE.vlasnik_VALUE); Set<Integer> 경계들 = new HashSet<>(), grana_Popis = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (naredba_podaci.Položaj < naredba_podaci.podaci.length) {
            int Položaj = naredba_podaci.Položaj, Naredba = naredba_podaci.한바이트(); String indeks_položaja = marker_VALUE + "_b" + Položaj;
            red.add(indeks_položaja + ":"); 경계들.add(Položaj);
            if (Naredba == 0) red.add("nop");
            else if (Naredba == 1) red.add("pushl $0");
            else if (Naredba >= 2 && Naredba <= 8) red.add("pushl $" + (Naredba - 3));
            else if (Naredba == 16 || Naredba == 17) red.add("pushl $" + (Naredba == 16 ? naredba_podaci.부호한바이트() : naredba_podaci.부호두바이트()));
            else if (Naredba == 18 || Naredba == 19) {
                int INDEX = Naredba == 18 ? naredba_podaci.한바이트() : naredba_podaci.두바이트();
                red.add("pushl $" + X_86_konstanta(poduka_VALUE,INDEX));
            } else if (Naredba == 21 || Naredba == 25 || (Naredba >= 26 && Naredba <= 29) || (Naredba >= 42 && Naredba <= 45) || Naredba == 54 || Naredba == 58 || (Naredba >= 59 && Naredba <= 62) || (Naredba >= 75 && Naredba <= 78)) {
                boolean 읽음 = Naredba < 54; int INDEX = Naredba == 21 || Naredba == 25 || Naredba == 54 || Naredba == 58 ? naredba_podaci.한바이트() : Naredba - (Naredba <= 29 ? 26 : Naredba <= 45 ? 42 : Naredba <= 62 ? 59 : 75);
                지역검사(INDEX,lokalno_COUNT); red.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Naredba == 46) Collections.addAll(red,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Naredba == 79) Collections.addAll(red,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Naredba == 87 || Naredba == 88) red.add("addl $" + (Naredba == 87 ? 4 : 8) + ", %esp");
            else if (Naredba >= 89 && Naredba <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] narudžba_Popis = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Naredba - 89]; 순번++) red.add("popl " + 저장기들[순번]);
                for (int 순번 : narudžba_Popis[Naredba - 89]) red.add("pushl " + 저장기들[순번]);
            } else if (Naredba == 96 || Naredba == 100 || Naredba == 104 || Naredba == 126 || Naredba == 128 || Naredba == 130) {
                String operacija_VALUE = Naredba == 96 ? "addl" : Naredba == 100 ? "subl" : Naredba == 104 ? "imull" : Naredba == 126 ? "andl" : Naredba == 128 ? "orl" : "xorl";
                Collections.addAll(red,"popl %ecx","popl %eax",operacija_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Naredba == 108 || Naredba == 112) Collections.addAll(red,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + indeks_položaja + "_divide","cmpl $0x80000000, %eax","jne " + indeks_položaja + "_divide","xorl %edx, %edx","jmp " + indeks_položaja + "_done",indeks_položaja + "_divide:","cltd","idivl %ecx",indeks_položaja + "_done:","pushl " + (Naredba == 108 ? "%eax" : "%edx"));
            else if (Naredba == 116) red.add("negl (%esp)");
            else if (Naredba == 120 || Naredba == 122 || Naredba == 124) Collections.addAll(red,"popl %ecx","popl %eax",(Naredba == 120 ? "sall" : Naredba == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Naredba == 132) {
                int INDEX = naredba_podaci.한바이트(), inkrement_VALUE = naredba_podaci.부호한바이트(); 지역검사(INDEX,lokalno_COUNT); red.add("addl $" + inkrement_VALUE + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Naredba >= 145 && Naredba <= 147) Collections.addAll(red,"popl %eax",Naredba == 145 ? "movsbl %al, %eax" : Naredba == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Naredba >= 153 && Naredba <= 166) {
                if (Naredba <= 158) Collections.addAll(red,"popl %eax","testl %eax, %eax");
                else Collections.addAll(red,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int odredište_VALUE = Položaj + naredba_podaci.부호두바이트(); grana_Popis.add(odredište_VALUE); red.add(비교들[Naredba - (Naredba <= 158 ? 153 : 159)] + " " + marker_VALUE + "_b" + odredište_VALUE);
            } else if (Naredba == 167 || Naredba == 200) {
                int odredište_VALUE = Položaj + (Naredba == 167 ? naredba_podaci.부호두바이트() : naredba_podaci.네바이트()); grana_Popis.add(odredište_VALUE); red.add("jmp " + marker_VALUE + "_b" + odredište_VALUE);
            } else if (Naredba == 170 || Naredba == 171) {
                while (naredba_podaci.Položaj % 4 != 0) naredba_podaci.한바이트();
                int zadana_vrijednost = Položaj + naredba_podaci.네바이트(); grana_Popis.add(zadana_vrijednost); red.add("popl %eax");
                int artikl_COUNT, 아래 = 0;
                if (Naredba == 170) { 아래 = naredba_podaci.네바이트(); int 위 = naredba_podaci.네바이트(); long 길이 = (long)위 - 아래 + 1; if (길이 < 1 || 길이 > (naredba_podaci.podaci.length - naredba_podaci.Položaj) / 4) throw new Prevođenje_pogreška("switch isječak GREŠKA"); artikl_COUNT = (int)길이; }
                else { artikl_COUNT = naredba_podaci.네바이트(); if (artikl_COUNT < 0 || artikl_COUNT > (naredba_podaci.podaci.length - naredba_podaci.Položaj) / 8) throw new Prevođenje_pogreška("switch Veličina GREŠKA"); }
                for (int 순번 = 0; 순번 < artikl_COUNT; 순번++) {
                    int VALUE = Naredba == 170 ? 아래 + 순번 : naredba_podaci.네바이트(), odredište_VALUE = Položaj + naredba_podaci.네바이트(); grana_Popis.add(odredište_VALUE);
                    Collections.addAll(red,"cmpl $" + VALUE + ", %eax","je " + marker_VALUE + "_b" + odredište_VALUE);
                }
                red.add("jmp " + marker_VALUE + "_b" + zadana_vrijednost);
            } else if (Naredba == 172 || Naredba == 176 || Naredba == 177) {
                if (Naredba != 177) red.add("popl %eax"); Collections.addAll(red,"leave","ret");
            } else if (Naredba == 178 || Naredba == 179) {
                postupak_Reference Reference = poduka_VALUE.Reference(naredba_podaci.두바이트()); if (!필드들.containsKey(Reference)) throw new Prevođenje_pogreška("알 수 없는 vrijednost_polja");
                Collections.addAll(red,"call " + simbol("init",Reference.vlasnik_VALUE),(Naredba == 178 ? "pushl " : "popl ") + simbol("field",Reference.부분들()));
            } else if (Naredba == 184) {
                postupak_Reference Reference = poduka_VALUE.Reference(naredba_podaci.두바이트()); if (!함수들.containsKey(Reference)) throw new Prevođenje_pogreška("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Reference.서술); Collections.addAll(red,"call " + simbol("init",Reference.vlasnik_VALUE),"call " + simbol("method",Reference.부분들()));
                if (!호출형식.Argumenti.isEmpty()) red.add("addl $" + 호출형식.Argumenti.size() * 4 + ", %esp");
                if (!호출형식.vratiti_KR.equals("V")) red.add("pushl %eax");
            } else if (Naredba == 182) {
                postupak_Reference Reference = poduka_VALUE.Reference(naredba_podaci.두바이트());
                if (Reference.equals(new postupak_Reference("java/lang/String","length","()I"))) Collections.addAll(red,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Reference.equals(new postupak_Reference("java/lang/String","charAt","(I)C"))) Collections.addAll(red,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Prevođenje_pogreška("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Naredba == 188) {
                if (naredba_podaci.한바이트() != 10) throw new Prevođenje_pogreška("new int[]만 Podrška_VALUE"); Collections.addAll(red,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Naredba == 190) Collections.addAll(red,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Naredba == 196) {
                int nastavak_VALUE = naredba_podaci.한바이트(), INDEX = naredba_podaci.두바이트(); 지역검사(INDEX,lokalno_COUNT);
                if (nastavak_VALUE == 21 || nastavak_VALUE == 25 || nastavak_VALUE == 54 || nastavak_VALUE == 58) red.add((nastavak_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (nastavak_VALUE == 132) red.add("addl $" + naredba_podaci.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Prevođenje_pogreška("wide Naredba 미지원");
            } else if (Naredba == 198 || Naredba == 199) {
                int odredište_VALUE = Položaj + naredba_podaci.부호두바이트(); grana_Popis.add(odredište_VALUE); Collections.addAll(red,"popl %eax","testl %eax, %eax",(Naredba == 198 ? "je " : "jne ") + marker_VALUE + "_b" + odredište_VALUE);
            } else throw new Prevođenje_pogreška("미지원 Naredba: " + Naredba);
        }
        if (!경계들.containsAll(grana_Popis)) throw new Prevođenje_pogreška("Naredba 경계가 아닌 곳으로 grana");
        red.add(".size " + marker_VALUE + ", .-" + marker_VALUE); return String.join("\n",red);
    }
    String X_86_konstanta(poduka_podaci podaci, int INDEX) {
        if (podaci.상수종류[INDEX] == 3) return podaci.konstanta_podaci[INDEX].toString();
        if (podaci.상수종류[INDEX] == 8) return niz_simbol(podaci.문자((Integer)podaci.konstanta_podaci[INDEX]));
        throw new Prevođenje_pogreška("정수와 niz_VALUE 상수만 Podrška_VALUE");
    }
    String X_86_sklop(String unos_p, List<String> 내보냄, String cilj) throws IOException {
        Map<String,String> stroj_tablica = new HashMap<>();
        for (String red : Files.readAllLines(resurs_put.resolve("_86_stroj_Azure_Functions.tsv"))) { String[] upariti_VALUE = red.split("\t"); if (upariti_VALUE[0].equals(cilj)) stroj_tablica.put(upariti_VALUE[1] + upariti_VALUE[2],upariti_VALUE[3]); }
        int indeks_položaja = unos_p.lastIndexOf('.'); if (indeks_položaja < 0) throw new Prevođenje_pogreška("unos_p Dodijeli_VALUE GREŠKA");
        String vlasnik_VALUE = unos_p.substring(0,indeks_položaja).replace('.','/'), postupak_unos_naziv = unos_p.substring(indeks_položaja + 1); postupak_Reference unos_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { postupak_Reference Reference = new postupak_Reference(vlasnik_VALUE,postupak_unos_naziv,서술); if (함수들.containsKey(Reference)) { if (unos_p_VALUE != null) throw new Prevođenje_pogreška("겹친 unos_p"); unos_p_VALUE = Reference; } }
        if (unos_p_VALUE == null || (함수들.get(unos_p_VALUE).pristup_unos & 0x100) != 0) throw new Prevođenje_pogreška("unos_p_VALUE FUNCTION_VALUE oblik_VALUE GREŠKA");
        List<String> red = new ArrayList<>(); red.add(".code32");
        for (poduka_podaci podaci : 클래스들.values()) {
            String Stanje_VALUE = simbol("state",podaci.Ime), 초기화 = simbol("init",podaci.Ime);
            Collections.addAll(red,".bss",".balign 4",Stanje_VALUE + ": .long 0",".text",초기화 + ":","cmpl $0, " + Stanje_VALUE,"jne " + 초기화 + "_done","movl $1, " + Stanje_VALUE);
            postupak_Reference 초기화참조 = new postupak_Reference(podaci.Ime,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) red.add("call " + simbol("method",초기화참조.부분들()));
            Collections.addAll(red,"movl $2, " + Stanje_VALUE,초기화 + "_done:","ret");
            for (član_podaci vrijednost_polja : podaci.vrijednost_polja) {
                byte[] konstanta_VALUE = vrijednost_polja.atribut_VALUE.get("ConstantValue"); String VALUE = konstanta_VALUE == null ? "0" : X_86_konstanta(podaci,new podaci_Čitač(konstanta_VALUE).두바이트());
                Collections.addAll(red,".data",".balign 4",simbol("field",podaci.Ime,vrijednost_polja.Ime,vrijednost_polja.서술) + ": .long " + VALUE);
            }
            for (član_podaci FUNCTION_VALUE : podaci.FUNCTION_VALUE) if (!FUNCTION_VALUE.Ime.equals("<init>")) red.add(X_86_postupak_tijelo(new postupak_Reference(podaci.Ime,FUNCTION_VALUE.Ime,FUNCTION_VALUE.서술),FUNCTION_VALUE,stroj_tablica,cilj));
        }
        Collections.addAll(red,".text",".globl java_entry","java_entry:","call " + simbol("init",unos_p_VALUE.vlasnik_VALUE),"call " + simbol("method",unos_p_VALUE.부분들()));
        if (unos_p_VALUE.서술.equals("()V")) red.add("xorl %eax, %eax"); red.add("ret");
        for (String Dodijeli_VALUE : 내보냄) {
            int graničnik_VALUE = Dodijeli_VALUE.indexOf('='); if (graničnik_VALUE < 1) throw new Prevođenje_pogreška("내보내기 Dodijeli_VALUE GREŠKA");
            String vanjski_VALUE = Dodijeli_VALUE.substring(0,graničnik_VALUE), FUNCTION_VALUE = Dodijeli_VALUE.substring(graničnik_VALUE + 1); int odjel_KR = FUNCTION_VALUE.lastIndexOf('.');
            if (odjel_KR < 0 || !vanjski_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Prevođenje_pogreška("내보내기 simbol GREŠKA");
            String poduka_VALUE = FUNCTION_VALUE.substring(0,odjel_KR).replace('.','/'), Ime = FUNCTION_VALUE.substring(odjel_KR + 1); postupak_Reference odabir_VALUE = null;
            for (postupak_Reference Reference : 함수들.keySet()) if (Reference.vlasnik_VALUE.equals(poduka_VALUE) && Reference.Ime.equals(Ime)) { if (odabir_VALUE != null) throw new Prevođenje_pogreška("겹친 내보내기 cilj"); odabir_VALUE = Reference; }
            if (odabir_VALUE == null) throw new Prevođenje_pogreška("내보낼 함수가 없음");
            Collections.addAll(red,".text",".globl " + vanjski_VALUE,vanjski_VALUE + ":","call " + simbol("init",odabir_VALUE.vlasnik_VALUE),"jmp " + simbol("method",odabir_VALUE.부분들()));
        }
        red.add(".section .rodata");
        for (Map.Entry<String,String> unos_VALUE : 문자열들.entrySet()) {
            Collections.addAll(red,".balign 4",unos_VALUE.getValue() + ":",".long " + unos_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lekcija_VALUE : unos_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(lekcija_VALUE)); if (!단위들.isEmpty()) red.add(".long " + String.join(",",단위들));
        }
        red.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",red) + "\n";
    }
    static void Izvrši_alat(List<String> Naredba) throws Exception {
        if (new ProcessBuilder(Naredba).inheritIO().start().waitFor() != 0) throw new Prevođenje_pogreška("programski_prevesti_izvor GREŠKA: " + Naredba.get(0));
    }
    static String podaci_niz(String Tekst) { return "\"" + Tekst.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Prevođenje(List<Path> 입력들, String cilj, String unos_p, List<String> 내보냄, Path Izlaz, Path resurs_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), poduka_put = 임시.resolve("classes"); Files.createDirectory(poduka_put);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",poduka_put.toString(),"-sourcepath",poduka_put.toString(),"-d",poduka_put.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int izvor_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Izlaz.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Prevođenje_pogreška("Izlaz 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); izvor_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Prevođenje_pogreška(".java 또는 .class만 Podrška_VALUE");
            }
            if (izvor_COUNT > 0) Izvrši_alat(자바명령);
            try (java.util.stream.Stream<Path> put_Popis = Files.walk(poduka_put)) { put_Popis.filter(PUTANJA -> PUTANJA.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,cilj.equals("user") ? "user" : "kernel",262144,resurs_VALUE);
            String 조립 = CONVERT_VALUE.X_86_sklop(unos_p,내보냄,cilj); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path alat_položaj = resurs_VALUE.getParent();
            Izvrši_alat(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Izvrši_alat(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),alat_položaj.resolve("CLR_Podrška.s").toString()));
            List<String> Spoji_se = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (cilj.equals("kernel")) Spoji_se.add("-r");
            else {
                Izvrši_alat(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),alat_položaj.resolve(cilj.equals("user") ? "START_korisnik_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(Spoji_se,"-e","_start",임시.resolve("start.o").toString());
                if (cilj.equals("user")) Collections.addAll(Spoji_se,"-T",alat_položaj.resolve("korisnik_veza_Raspored.ld").toString());
            }
            Collections.addAll(Spoji_se,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Izvrši_alat(Spoji_se);
            Izlaz = Izlaz.toAbsolutePath(); Files.createDirectories(Izlaz.getParent()); Path objavi_VALUE = Files.createTempFile(Izlaz.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),objavi_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(objavi_VALUE,Izlaz,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(objavi_VALUE); }
            Files.setPosixFilePermissions(Izlaz,java.nio.file.attribute.PosixFilePermissions.fromString(cilj.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Izlaz + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbol_podaci = new ArrayList<>(), izvor_podaci = new ArrayList<>();
            for (postupak_Reference Reference : CONVERT_VALUE.함수들.keySet()) simbol_podaci.add(podaci_niz(simbol("method",Reference.부분들())) + ":" + podaci_niz(Reference.vlasnik_VALUE + "." + Reference.Ime + Reference.서술));
            for (Path 입력 : 입력들) {
                byte[] raspršivanje_Datoteka = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Tekst = new StringBuilder(); for (byte VALUE : raspršivanje_Datoteka) Tekst.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                izvor_podaci.add(podaci_niz(입력.toAbsolutePath().toString()) + ":" + podaci_niz(Tekst.toString()));
            }
            Files.writeString(Paths.get(Izlaz + ".json"),"{\"target\":" + podaci_niz(cilj) + ",\"entry\":" + podaci_niz(unos_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbol_podaci) + "},\"sources\":{" + String.join(",",izvor_podaci) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> put_Popis = Files.walk(임시)) { for (Path PUTANJA : (Iterable<Path>)put_Popis.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(PUTANJA); }
        }
    }
    public static void main(String[] Argumenti) {
        try {
            String unos_p = null, cilj = "kernel", X_86_cilj = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> put_Popis = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumenti.length; 순번++) {
                String VALUE = Argumenti[순번];
                switch (VALUE) {
                    case "--target": X_86_cilj = Argumenti[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry poduka_VALUE.FUNCTION_VALUE -o Izlaz [--target linux|kernel|user] [--profile kernel|user] [--export simbol=poduka_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": unos_p = Argumenti[++순번]; break;
                    case "--profile": cilj = Argumenti[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumenti[++순번]); break;
                    case "--export": 내보냄.add(Argumenti[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argumenti[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Prevođenje_pogreška("알 수 없는 옵션: " + VALUE); put_Popis.add(Paths.get(VALUE));
                }
            }
            if (unos_p == null || 출력경로 == null || put_Popis.isEmpty()) throw new Prevođenje_pogreška("--entry, -o, poduka_VALUE 파일이 필요합니다");
            Path resurs_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_cilj != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_cilj)) throw new Prevođenje_pogreška("알 수 없는 Izvrši_naredba cilj");
                X_86_Prevođenje(put_Popis,X_86_cilj,unos_p,내보냄,출력경로,resurs_VALUE); return;
            }
            String IZVOR = new 기계어미리번역(put_Popis, cilj, 낱말수, resurs_VALUE).generirati(unos_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, IZVOR, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception GREŠKA) { System.err.println("programski_prevesti_izvor GREŠKA: " + GREŠKA.getMessage()); System.exit(1); }
    }
}
