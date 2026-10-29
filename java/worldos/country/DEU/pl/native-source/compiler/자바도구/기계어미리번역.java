// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Klasa_WARTOŚĆ 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class translacja_błąd extends RuntimeException {
        translacja_błąd(String 설명) { super(설명); }
    }
    static final class dane_Czytnik {
        final byte[] dane;
        int pozycja;
        dane_Czytnik(byte[] wejście_dane) { dane = wejście_dane; }
        byte[] Odczyt(int długość_WARTOŚĆ) {
            if (długość_WARTOŚĆ < 0 || długość_WARTOŚĆ > dane.length - pozycja) throw new translacja_błąd("잘린 Klasa_WARTOŚĆ 또는 polecenie dane");
            byte[] WYNIK = Arrays.copyOfRange(dane, pozycja, pozycja + długość_WARTOŚĆ); pozycja += długość_WARTOŚĆ; return WYNIK;
        }
        int 한바이트() { if (pozycja >= dane.length) throw new translacja_błąd("잘린 polecenie dane"); return dane[pozycja++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class członek_dane {
        final int dostęp_wpis;
        final String Nazwa, 서술;
        final Map<String, byte[]> wartość_atrybutu;
        członek_dane(int dostęp_WARTOŚĆ, String nazwa_WARTOŚĆ, String deskryptor_dane, Map<String, byte[]> atrybut_dane) {
            dostęp_wpis = dostęp_WARTOŚĆ; Nazwa = nazwa_WARTOŚĆ; 서술 = deskryptor_dane; wartość_atrybutu = atrybut_dane;
        }
    }
    static final class metoda_odwołanie implements Comparable<metoda_odwołanie> {
        final String właściciel_WARTOŚĆ, Nazwa, 서술;
        metoda_odwołanie(String 소유값, String nazwa_WARTOŚĆ, String deskryptor_dane) { właściciel_WARTOŚĆ = 소유값; Nazwa = nazwa_WARTOŚĆ; 서술 = deskryptor_dane; }
        String[] 부분들() { return new String[]{właściciel_WARTOŚĆ, Nazwa, 서술}; }
        public int compareTo(metoda_odwołanie węzeł_równorzędny_WARTOŚĆ) {
            int Porównanie_WARTOŚĆ = właściciel_WARTOŚĆ.compareTo(węzeł_równorzędny_WARTOŚĆ.właściciel_WARTOŚĆ);
            if (Porównanie_WARTOŚĆ == 0) Porównanie_WARTOŚĆ = Nazwa.compareTo(węzeł_równorzędny_WARTOŚĆ.Nazwa);
            return Porównanie_WARTOŚĆ == 0 ? 서술.compareTo(węzeł_równorzędny_WARTOŚĆ.서술) : Porównanie_WARTOŚĆ;
        }
        public boolean equals(Object węzeł_równorzędny_WARTOŚĆ) { return węzeł_równorzędny_WARTOŚĆ instanceof metoda_odwołanie && compareTo((metoda_odwołanie) węzeł_równorzędny_WARTOŚĆ) == 0; }
        public int hashCode() { return Objects.hash(właściciel_WARTOŚĆ, Nazwa, 서술); }
    }
    static final class Klasa_dane {
        final int[] stała_Rodzaj;
        final Object[] stała_dane;
        final String Nazwa;
        final List<członek_dane> wartość_pola, FUNKCJA_WARTOŚĆ;
        Klasa_dane(Path ścieżka_2) throws IOException {
            dane_Czytnik Czytnik_WARTOŚĆ = new dane_Czytnik(Files.readAllBytes(ścieżka_2));
            if (Czytnik_WARTOŚĆ.네바이트() != 0xcafebabe) throw new translacja_błąd("Java Klasa_WARTOŚĆ 표식이 아님");
            Czytnik_WARTOŚĆ.Odczyt(4);
            int towar_ILE_LICZB = Czytnik_WARTOŚĆ.두바이트(); stała_Rodzaj = new int[towar_ILE_LICZB]; stała_dane = new Object[towar_ILE_LICZB];
            for (int 순번 = 1; 순번 < towar_ILE_LICZB; 순번++) {
                int Rodzaj_WARTOŚĆ = Czytnik_WARTOŚĆ.한바이트(); stała_Rodzaj[순번] = Rodzaj_WARTOŚĆ;
                switch (Rodzaj_WARTOŚĆ) {
                    case 1:
                        int długość_WARTOŚĆ = Czytnik_WARTOŚĆ.두바이트();
                        byte[] znak_bufor = Czytnik_WARTOŚĆ.Odczyt(długość_WARTOŚĆ), 길이붙인자료 = new byte[długość_WARTOŚĆ + 2];
                        길이붙인자료[0] = (byte)(długość_WARTOŚĆ >> 8); 길이붙인자료[1] = (byte)długość_WARTOŚĆ;
                        System.arraycopy(znak_bufor, 0, 길이붙인자료, 2, długość_WARTOŚĆ);
                        stała_dane[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: stała_dane[순번] = Czytnik_WARTOŚĆ.네바이트(); break;
                    case 4: Czytnik_WARTOŚĆ.Odczyt(4); break;
                    case 5: case 6: Czytnik_WARTOŚĆ.Odczyt(8); 순번++; break;
                    case 7: case 8: case 16: stała_dane[순번] = Czytnik_WARTOŚĆ.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        stała_dane[순번] = new int[]{Czytnik_WARTOŚĆ.두바이트(), Czytnik_WARTOŚĆ.두바이트()}; break;
                    case 15: stała_dane[순번] = new int[]{Czytnik_WARTOŚĆ.한바이트(), Czytnik_WARTOŚĆ.두바이트()}; break;
                    default: throw new translacja_błąd("지원하지 않는 stała_WARTOŚĆ Rodzaj_WARTOŚĆ: " + Rodzaj_WARTOŚĆ);
                }
            }
            Czytnik_WARTOŚĆ.두바이트(); Nazwa = nazwa_klasy(Czytnik_WARTOŚĆ.두바이트());
            if (!nazwa_klasy(Czytnik_WARTOŚĆ.두바이트()).equals("java/lang/Object") || Czytnik_WARTOŚĆ.두바이트() != 0)
                throw new translacja_błąd(Nazwa + ": 상속 및 인터페이스 미지원");
            wartość_pola = 멤버읽기(Czytnik_WARTOŚĆ); FUNKCJA_WARTOŚĆ = 멤버읽기(Czytnik_WARTOŚĆ); 속성읽기(Czytnik_WARTOŚĆ);
            if (Czytnik_WARTOŚĆ.pozycja != Czytnik_WARTOŚĆ.dane.length) throw new translacja_błąd("Klasa_WARTOŚĆ 뒤에 남은 dane");
        }
        String 문자(int INDEKS) {
            if (INDEKS < 1 || INDEKS >= stała_Rodzaj.length || stała_Rodzaj[INDEKS] != 1) throw new translacja_błąd("문자 stała_WARTOŚĆ INDEKS błąd");
            return (String) stała_dane[INDEKS];
        }
        String nazwa_klasy(int INDEKS) {
            if (INDEKS < 1 || INDEKS >= stała_Rodzaj.length || stała_Rodzaj[INDEKS] != 7) throw new translacja_błąd("Klasa_WARTOŚĆ odwołanie błąd");
            return 문자((Integer)stała_dane[INDEKS]);
        }
        metoda_odwołanie odwołanie(int INDEKS) {
            if (INDEKS < 1 || INDEKS >= stała_Rodzaj.length || stała_Rodzaj[INDEKS] < 9 || stała_Rodzaj[INDEKS] > 11) throw new translacja_błąd("멤버 odwołanie błąd");
            int[] parować_WARTOŚĆ = (int[])stała_dane[INDEKS], nazwa_parować = (int[])stała_dane[parować_WARTOŚĆ[1]];
            return new metoda_odwołanie(nazwa_klasy(parować_WARTOŚĆ[0]), 문자(nazwa_parować[0]), 문자(nazwa_parować[1]));
        }
        Map<String, byte[]> 속성읽기(dane_Czytnik Czytnik_WARTOŚĆ) {
            Map<String, byte[]> WYNIK = new LinkedHashMap<>();
            int towar_ILE_LICZB = Czytnik_WARTOŚĆ.두바이트();
            for (int 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) {
                String atrybut_nazwa = 문자(Czytnik_WARTOŚĆ.두바이트()); byte[] WARTOŚĆ = Czytnik_WARTOŚĆ.Odczyt(Czytnik_WARTOŚĆ.네바이트());
                if (WYNIK.put(atrybut_nazwa, WARTOŚĆ) != null) throw new translacja_błąd("겹친 wartość_atrybutu: " + atrybut_nazwa);
            }
            return WYNIK;
        }
        List<członek_dane> 멤버읽기(dane_Czytnik Czytnik_WARTOŚĆ) {
            List<członek_dane> WYNIK = new ArrayList<>(); int towar_ILE_LICZB = Czytnik_WARTOŚĆ.두바이트();
            for (int 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) {
                int dostęp_wpis = Czytnik_WARTOŚĆ.두바이트(); String metoda_wpis_nazwa = 문자(Czytnik_WARTOŚĆ.두바이트()), 서술 = 문자(Czytnik_WARTOŚĆ.두바이트());
                WYNIK.add(new członek_dane(dostęp_wpis, metoda_wpis_nazwa, 서술, 속성읽기(Czytnik_WARTOŚĆ)));
            }
            return WYNIK;
        }
    }
    static final class metoda_deskryptor {
        final List<String> argumenty = new ArrayList<>();
        final String Zwrot_KR;
        metoda_deskryptor(String 서술) {
            if (!서술.startsWith("(")) throw new translacja_błąd("FUNKCJA_WARTOŚĆ 서술 błąd: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new translacja_błąd("FUNKCJA_WARTOŚĆ 서술 błąd: " + 서술);
            argumenty.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (argumenty.contains("V") || 반환들.size() != 1) throw new translacja_błąd("FUNKCJA_WARTOŚĆ 서술 błąd: " + 서술);
            Zwrot_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> WYNIK = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int pozycja = 0; pozycja < 서술.length();) {
            String zaznaczenie_WARTOŚĆ = null;
            for (String format_WARTOŚĆ : 허용형식) if (서술.startsWith(format_WARTOŚĆ, pozycja)) { zaznaczenie_WARTOŚĆ = format_WARTOŚĆ; break; }
            if (zaznaczenie_WARTOŚĆ == null) throw new translacja_błąd("지원하지 않는 typ_danych: " + 서술);
            WYNIK.add(zaznaczenie_WARTOŚĆ); pozycja += zaznaczenie_WARTOŚĆ.length();
        }
        return WYNIK;
    }
    static String symbol(String Rodzaj_WARTOŚĆ, String... 부분들) {
        try {
            byte[] skrót_Plik = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder tekst = new StringBuilder("j_" + Rodzaj_WARTOŚĆ + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) tekst.append(String.format(Locale.ROOT, "%02x", skrót_Plik[순번] & 255));
            return tekst.toString();
        } catch (Exception błąd) { throw new translacja_błąd(błąd.toString()); }
    }
    final Map<String, Klasa_dane> 클래스들 = new TreeMap<>();
    final Map<metoda_odwołanie, członek_dane> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), maszyna_Functions_c3a8e64a = new LinkedHashMap<>();
    final String wykonanie_cel, maszyna_Klasa;
    final int sterta_Word_ILE_LICZB;
    final Path zasób_ścieżka;
    기계어미리번역(List<Path> ścieżka_Lista, String wartość_docelowa, int 낱말수, Path zasób_WARTOŚĆ) throws IOException {
        if ((!wartość_docelowa.equals("kernel") && !wartość_docelowa.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new translacja_błąd("Wykonaj_polecenie wartość_docelowa 또는 Pamięć_WARTOŚĆ ADRES_region Rozmiar błąd");
        wykonanie_cel = wartość_docelowa; sterta_Word_ILE_LICZB = 낱말수; zasób_ścieżka = zasób_WARTOŚĆ;
        // 이 이름도 국가별 źródło_drzewo generować 시 해당 언어로 옮긴다.
        maszyna_Klasa = wartość_docelowa.equals("kernel") ? "Tablica" : "przestrzeń_użytkownika";
        for (String wiersz_wejścia : Files.readAllLines(zasób_WARTOŚĆ.resolve("maszyna_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = wiersz_wejścia.split("\t", -1);
            if (부분들.length != 4) throw new translacja_błąd("maszyna FUNKCJA_WARTOŚĆ dane błąd");
            if (부분들[0].equals(wartość_docelowa)) maszyna_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path ścieżka_2 : ścieżka_Lista) {
            Klasa_dane dane = new Klasa_dane(ścieżka_2);
            if (클래스들.put(dane.Nazwa, dane) != null) throw new translacja_błąd("중복 Klasa_WARTOŚĆ: " + dane.Nazwa);
            for (członek_dane wartość_pola : dane.wartość_pola) {
                if ((wartość_pola.dostęp_wpis & 8) == 0 || 형식읽기(wartość_pola.서술).equals(Collections.singletonList("V"))) throw new translacja_błąd("statyczny_WARTOŚĆ 필드만 wsparcie_WARTOŚĆ");
                if (필드들.put(new metoda_odwołanie(dane.Nazwa, wartość_pola.Nazwa, wartość_pola.서술), wartość_pola) != null) throw new translacja_błąd("중복 wartość_pola");
            }
            for (członek_dane FUNKCJA_WARTOŚĆ : dane.FUNKCJA_WARTOŚĆ) {
                if (FUNKCJA_WARTOŚĆ.Nazwa.equals("<init>")) continue;
                if ((FUNKCJA_WARTOŚĆ.dostęp_wpis & 8) == 0 || (FUNKCJA_WARTOŚĆ.dostęp_wpis & (0x20 | 0x400)) != 0) throw new translacja_błąd("statyczny_WARTOŚĆ 비동기화 함수만 wsparcie_WARTOŚĆ");
                new metoda_deskryptor(FUNKCJA_WARTOŚĆ.서술);
                if (함수들.put(new metoda_odwołanie(dane.Nazwa, FUNKCJA_WARTOŚĆ.Nazwa, FUNKCJA_WARTOŚĆ.서술), FUNKCJA_WARTOŚĆ) != null) throw new translacja_błąd("중복 FUNKCJA_WARTOŚĆ");
            }
        }
    }
    String ciąg_symbol(String tekst) { return 문자열들.computeIfAbsent(tekst, WARTOŚĆ -> "j_text_" + 문자열들.size()); }
    String wyrażenie_stałe(Klasa_dane dane, int INDEKS) {
        if (INDEKS < 1 || INDEKS >= dane.stała_Rodzaj.length) throw new translacja_błąd("stała_WARTOŚĆ INDEKS obcinać błąd");
        if (dane.stała_Rodzaj[INDEKS] == 3) return "(word)(uint32_t)(" + dane.stała_dane[INDEKS] + ")";
        if (dane.stała_Rodzaj[INDEKS] == 8) return "(word)" + ciąg_symbol(dane.문자((Integer)dane.stała_dane[INDEKS]));
        throw new translacja_błąd("정수와 ciąg_WARTOŚĆ 상수만 wsparcie_WARTOŚĆ");
    }
    String metoda_prototyp(metoda_odwołanie odwołanie) {
        List<String> 인수들 = new ArrayList<>(); int towar_ILE_LICZB = new metoda_deskryptor(odwołanie.서술).argumenty.size();
        for (int 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symbol("method", odwołanie.부분들()) + "(" + (towar_ILE_LICZB == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void czek_lokalny(int INDEKS, int zmienna_lokalna_ILE_LICZB) { if (INDEKS < 0 || INDEKS >= zmienna_lokalna_ILE_LICZB) throw new translacja_błąd("lokalny_Scope zmienna_WARTOŚĆ INDEKS obcinać błąd"); }
    void 분기넣기(List<String> pozycja_wyjścia, Set<Integer> gałąź_Lista, int pozycja, int 이동량, String choroba) {
        int cel_WARTOŚĆ = pozycja + 이동량; gałąź_Lista.add(cel_WARTOŚĆ);
        pozycja_wyjścia.add((choroba == null ? "" : "if (" + choroba + ") ") + "goto b" + cel_WARTOŚĆ + ";");
    }
    String treść_metody(metoda_odwołanie FUNKCJA_WARTOŚĆ, członek_dane dane) {
        byte[] treść_dane = dane.wartość_atrybutu.get("Code"); if (treść_dane == null) throw new translacja_błąd("FUNKCJA_WARTOŚĆ 몸체가 없음: " + FUNKCJA_WARTOŚĆ.Nazwa);
        dane_Czytnik Czytnik_WARTOŚĆ = new dane_Czytnik(treść_dane); int 쌓임깊이 = Czytnik_WARTOŚĆ.두바이트(), zmienna_lokalna_ILE_LICZB = Czytnik_WARTOŚĆ.두바이트();
        dane_Czytnik polecenie_dane = new dane_Czytnik(Czytnik_WARTOŚĆ.Odczyt(Czytnik_WARTOŚĆ.네바이트()));
        if (Czytnik_WARTOŚĆ.두바이트() != 0) throw new translacja_błąd("try/catch/finally 미지원");
        metoda_deskryptor format_WARTOŚĆ = new metoda_deskryptor(FUNKCJA_WARTOŚĆ.서술); if (zmienna_lokalna_ILE_LICZB < format_WARTOŚĆ.argumenty.size()) throw new translacja_błąd("매개변수보다 적은 lokalny_Scope zmienna_WARTOŚĆ");
        Klasa_dane Klasa_WARTOŚĆ = 클래스들.get(FUNKCJA_WARTOŚĆ.właściciel_WARTOŚĆ);
        List<String> pozycja_wyjścia = new ArrayList<>(); pozycja_wyjścia.add(metoda_prototyp(FUNKCJA_WARTOŚĆ) + " {");
        pozycja_wyjścia.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(zmienna_lokalna_ILE_LICZB, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_WARTOŚĆ.argumenty.size(); 순번++) pozycja_wyjścia.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), gałąź_Lista = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (polecenie_dane.pozycja < polecenie_dane.dane.length) {
            int pozycja = polecenie_dane.pozycja, polecenie = polecenie_dane.한바이트(); 경계들.add(pozycja); pozycja_wyjścia.add("b" + pozycja + ":;");
            if (polecenie == 0) continue;
            if (polecenie == 1) pozycja_wyjścia.add("PUSH(0);");
            else if (polecenie >= 2 && polecenie <= 8) pozycja_wyjścia.add("PUSH((uint32_t)(" + (polecenie - 3) + "));");
            else if (polecenie == 16 || polecenie == 17) pozycja_wyjścia.add("PUSH((uint32_t)(" + (polecenie == 16 ? polecenie_dane.부호한바이트() : polecenie_dane.부호두바이트()) + "));");
            else if (polecenie == 18 || polecenie == 19) pozycja_wyjścia.add("PUSH(" + wyrażenie_stałe(Klasa_WARTOŚĆ, polecenie == 18 ? polecenie_dane.한바이트() : polecenie_dane.두바이트()) + ");");
            else if (polecenie == 21 || polecenie == 25 || (polecenie >= 26 && polecenie <= 29) || (polecenie >= 42 && polecenie <= 45)) {
                int INDEKS = polecenie == 21 || polecenie == 25 ? polecenie_dane.한바이트() : polecenie - (polecenie <= 29 ? 26 : 42);
                czek_lokalny(INDEKS, zmienna_lokalna_ILE_LICZB); pozycja_wyjścia.add("PUSH(l[" + INDEKS + "]);");
            } else if (polecenie == 54 || polecenie == 58 || (polecenie >= 59 && polecenie <= 62) || (polecenie >= 75 && polecenie <= 78)) {
                int INDEKS = polecenie == 54 || polecenie == 58 ? polecenie_dane.한바이트() : polecenie - (polecenie <= 62 ? 59 : 75);
                czek_lokalny(INDEKS, zmienna_lokalna_ILE_LICZB); pozycja_wyjścia.add("l[" + INDEKS + "] = POP();");
            } else if (polecenie == 46) pozycja_wyjścia.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (polecenie == 79) pozycja_wyjścia.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (polecenie == 87 || polecenie == 88) pozycja_wyjścia.add(polecenie == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (polecenie >= 89 && polecenie <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] zamówić_Lista = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[polecenie - 89]; 순번++) pozycja_wyjścia.add("abcd".charAt(순번) + " = POP();");
                for (char WARTOŚĆ : zamówić_Lista[polecenie - 89].toCharArray()) pozycja_wyjścia.add("PUSH(" + WARTOŚĆ + ");");
            } else if (polecenie == 96 || polecenie == 100 || polecenie == 104 || polecenie == 126 || polecenie == 128 || polecenie == 130) {
                String zabieg_WARTOŚĆ = polecenie == 96 ? "+" : polecenie == 100 ? "-" : polecenie == 104 ? "*" : polecenie == 126 ? "&" : polecenie == 128 ? "|" : "^";
                pozycja_wyjścia.add("b = POP(); a = POP(); PUSH((uint32_t)a " + zabieg_WARTOŚĆ + " (uint32_t)b);");
            } else if (polecenie == 108 || polecenie == 112) pozycja_wyjścia.add("b = POP(); a = POP(); PUSH(divide(a,b," + (polecenie == 112 ? 1 : 0) + "));");
            else if (polecenie == 116) pozycja_wyjścia.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (polecenie == 120 || polecenie == 122 || polecenie == 124) {
                pozycja_wyjścia.add("b = POP(); a = POP();"); pozycja_wyjścia.add("PUSH(" + (polecenie == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (polecenie == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (polecenie == 132) {
                int INDEKS = polecenie_dane.한바이트(), przyrost_ilość = polecenie_dane.부호한바이트(); czek_lokalny(INDEKS, zmienna_lokalna_ILE_LICZB);
                pozycja_wyjścia.add("l[" + INDEKS + "] = (uint32_t)l[" + INDEKS + "] + (uint32_t)(" + przyrost_ilość + ");");
            } else if (polecenie >= 145 && polecenie <= 147) pozycja_wyjścia.add("a = POP(); PUSH((uint32_t)(" + (polecenie == 145 ? "int8_t" : polecenie == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (polecenie >= 153 && polecenie <= 158) {
                pozycja_wyjścia.add("a = POP();"); 분기넣기(pozycja_wyjścia, gałąź_Lista, pozycja, polecenie_dane.부호두바이트(), "(int32_t)a " + 비교들[polecenie - 153] + " 0");
            } else if (polecenie >= 159 && polecenie <= 166) {
                pozycja_wyjścia.add("b = POP(); a = POP();"); 분기넣기(pozycja_wyjścia, gałąź_Lista, pozycja, polecenie_dane.부호두바이트(), polecenie >= 165 ? "a " + 비교들[polecenie - 159] + " b" : "(int32_t)a " + 비교들[polecenie - 159] + " (int32_t)b");
            } else if (polecenie == 167 || polecenie == 200) 분기넣기(pozycja_wyjścia, gałąź_Lista, pozycja, polecenie == 167 ? polecenie_dane.부호두바이트() : polecenie_dane.네바이트(), null);
            else if (polecenie == 170 || polecenie == 171) {
                while (polecenie_dane.pozycja % 4 != 0) polecenie_dane.한바이트();
                int wartość_domyślna = polecenie_dane.네바이트(); pozycja_wyjścia.add("a = POP();");
                if (polecenie == 170) {
                    int 아래 = polecenie_dane.네바이트(), 위 = polecenie_dane.네바이트(); long towar_ILE_LICZB = (long)위 - 아래 + 1;
                    if (towar_ILE_LICZB < 1 || towar_ILE_LICZB > (polecenie_dane.dane.length - polecenie_dane.pozycja) / 4) throw new translacja_błąd("switch obcinać błąd");
                    for (long WARTOŚĆ = 아래; WARTOŚĆ <= 위; WARTOŚĆ++) 분기넣기(pozycja_wyjścia, gałąź_Lista, pozycja, polecenie_dane.네바이트(), "(int32_t)a == (" + WARTOŚĆ + ")");
                } else {
                    int towar_ILE_LICZB = polecenie_dane.네바이트(), przód_dane = 0;
                    if (towar_ILE_LICZB < 0 || towar_ILE_LICZB > (polecenie_dane.dane.length - polecenie_dane.pozycja) / 8) throw new translacja_błąd("switch Rozmiar błąd");
                    for (int 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) {
                        int WARTOŚĆ = polecenie_dane.네바이트(); if (순번 > 0 && WARTOŚĆ <= przód_dane) throw new translacja_błąd("switch zamówić_WARTOŚĆ błąd"); przód_dane = WARTOŚĆ;
                        분기넣기(pozycja_wyjścia, gałąź_Lista, pozycja, polecenie_dane.네바이트(), "(int32_t)a == (" + WARTOŚĆ + ")");
                    }
                }
                분기넣기(pozycja_wyjścia, gałąź_Lista, pozycja, wartość_domyślna, null);
            } else if (polecenie == 172 || polecenie == 176 || polecenie == 177) pozycja_wyjścia.add("return " + (polecenie == 177 ? "0" : "POP()") + ";");
            else if (polecenie == 178 || polecenie == 179) {
                metoda_odwołanie odwołanie = Klasa_WARTOŚĆ.odwołanie(polecenie_dane.두바이트()); if (!필드들.containsKey(odwołanie)) throw new translacja_błąd("알 identyfikator 없는 wartość_pola");
                pozycja_wyjścia.add(symbol("init", odwołanie.właściciel_WARTOŚĆ) + "();"); String wartość_pola = symbol("field", odwołanie.부분들());
                pozycja_wyjścia.add(polecenie == 178 ? "PUSH(" + wartość_pola + ");" : wartość_pola + " = POP();");
            } else if (polecenie == 184) {
                metoda_odwołanie odwołanie = Klasa_WARTOŚĆ.odwołanie(polecenie_dane.두바이트()); if (!함수들.containsKey(odwołanie)) throw new translacja_błąd("알 identyfikator 없는 FUNKCJA_WARTOŚĆ");
                metoda_deskryptor 호출형식 = new metoda_deskryptor(odwołanie.서술); int towar_ILE_LICZB = 호출형식.argumenty.size();
                pozycja_wyjścia.add(symbol("init", odwołanie.właściciel_WARTOŚĆ) + "();"); pozycja_wyjścia.add("if(sp < " + towar_ILE_LICZB + ") kernel_panic(\"call stack underflow\"); sp -= " + towar_ILE_LICZB + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                pozycja_wyjścia.add("a = " + symbol("method", odwołanie.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.Zwrot_KR.equals("V")) pozycja_wyjścia.add("PUSH(a);");
            } else if (polecenie == 182) {
                metoda_odwołanie odwołanie = Klasa_WARTOŚĆ.odwołanie(polecenie_dane.두바이트());
                if (odwołanie.equals(new metoda_odwołanie("java/lang/String", "length", "()I"))) pozycja_wyjścia.add("a = POP(); PUSH(length(a));");
                else if (odwołanie.equals(new metoda_odwołanie("java/lang/String", "charAt", "(I)C"))) pozycja_wyjścia.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new translacja_błąd("가상 FUNKCJA_WARTOŚĆ 호출 미지원");
            } else if (polecenie == 188) {
                if (polecenie_dane.한바이트() != 10) throw new translacja_błąd("new int[]만 wsparcie_WARTOŚĆ"); pozycja_wyjścia.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (polecenie == 190) pozycja_wyjścia.add("a = POP(); PUSH(length(a));");
            else if (polecenie == 196) {
                int rozszerzenie_WARTOŚĆ = polecenie_dane.한바이트(), INDEKS = polecenie_dane.두바이트(); czek_lokalny(INDEKS, zmienna_lokalna_ILE_LICZB);
                if (rozszerzenie_WARTOŚĆ == 21 || rozszerzenie_WARTOŚĆ == 25) pozycja_wyjścia.add("PUSH(l[" + INDEKS + "]);");
                else if (rozszerzenie_WARTOŚĆ == 54 || rozszerzenie_WARTOŚĆ == 58) pozycja_wyjścia.add("l[" + INDEKS + "] = POP();");
                else if (rozszerzenie_WARTOŚĆ == 132) pozycja_wyjścia.add("l[" + INDEKS + "] = (uint32_t)l[" + INDEKS + "] + (uint32_t)(" + polecenie_dane.부호두바이트() + ");");
                else throw new translacja_błąd("미지원 wide polecenie");
            } else if (polecenie == 198 || polecenie == 199) {
                pozycja_wyjścia.add("a = POP();"); 분기넣기(pozycja_wyjścia, gałąź_Lista, pozycja, polecenie_dane.부호두바이트(), "a " + (polecenie == 198 ? "==" : "!=") + " 0");
            } else throw new translacja_błąd(FUNKCJA_WARTOŚĆ.właściciel_WARTOŚĆ + "." + FUNKCJA_WARTOŚĆ.Nazwa + ", bajt_WARTOŚĆ " + pozycja + ": 미지원 polecenie " + polecenie);
        }
        if (!경계들.containsAll(gałąź_Lista)) throw new translacja_błąd("polecenie 경계가 아닌 곳으로 gałąź_22e01337");
        pozycja_wyjścia.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", pozycja_wyjścia);
    }
    String eksportować_metoda(String Link_symbol, String wartość_docelowa, boolean 진입점여부) {
        int indeks_pozycji = wartość_docelowa.lastIndexOf('.'); if (indeks_pozycji < 0 || !Link_symbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new translacja_błąd("내보내기 Przypisz_WARTOŚĆ błąd");
        String właściciel_WARTOŚĆ = wartość_docelowa.substring(0, indeks_pozycji).replace('.', '/'), Nazwa = wartość_docelowa.substring(indeks_pozycji + 1); metoda_odwołanie zaznaczenie_WARTOŚĆ = null;
        for (metoda_odwołanie odwołanie : 함수들.keySet()) if (odwołanie.właściciel_WARTOŚĆ.equals(właściciel_WARTOŚĆ) && odwołanie.Nazwa.equals(Nazwa)) {
            if (zaznaczenie_WARTOŚĆ != null) throw new translacja_błąd("겹친 내보내기 wartość_docelowa"); zaznaczenie_WARTOŚĆ = odwołanie;
        }
        if (zaznaczenie_WARTOŚĆ == null || (함수들.get(zaznaczenie_WARTOŚĆ).dostęp_wpis & 0x100) != 0) throw new translacja_błąd("내보낼 함수가 없음 또는 native FUNKCJA_WARTOŚĆ");
        metoda_deskryptor format_WARTOŚĆ = new metoda_deskryptor(zaznaczenie_WARTOŚĆ.서술);
        if ((진입점여부 && !format_WARTOŚĆ.argumenty.isEmpty()) || !Arrays.asList("V", "I").contains(format_WARTOŚĆ.Zwrot_KR)) throw new translacja_błąd("punkt_wejścia_WARTOŚĆ 또는 C granica_WARTOŚĆ format_WARTOŚĆ błąd");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_WARTOŚĆ.argumenty.size(); 순번++) {
            if (!format_WARTOŚĆ.argumenty.get(순번).equals("I")) throw new translacja_błąd("C 경계는 int 인수만 wsparcie_WARTOŚĆ");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_WARTOŚĆ.Zwrot_KR.equals("V") ? "void " : "int32_t ") + Link_symbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symbol("init", zaznaczenie_WARTOŚĆ.właściciel_WARTOŚĆ) + "(); " + (format_WARTOŚĆ.Zwrot_KR.equals("V") ? "" : "return (int32_t)") + symbol("method", zaznaczenie_WARTOŚĆ.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generować(String punkt_wejścia, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metoda_odwołanie, członek_dane> wpis_WARTOŚĆ : 함수들.entrySet()) {
            metoda_odwołanie odwołanie = wpis_WARTOŚĆ.getKey(); członek_dane dane = wpis_WARTOŚĆ.getValue(); 선언들.add(metoda_prototyp(odwołanie) + ";");
            if ((dane.dostęp_wpis & 0x100) != 0) {
                String Połącz = maszyna_Functions_c3a8e64a.get(odwołanie.Nazwa + odwołanie.서술);
                if (!odwołanie.właściciel_WARTOŚĆ.equals(maszyna_Klasa) || Połącz == null) throw new translacja_błąd("허용되지 않은 native FUNKCJA_WARTOŚĆ: " + odwołanie.Nazwa);
                int towar_ILE_LICZB = new metoda_deskryptor(odwołanie.서술).argumenty.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Połącz + "(" + (towar_ILE_LICZB == 0 ? "void" : String.join(",", Collections.nCopies(towar_ILE_LICZB, "word"))) + ");");
                몸체들.add(metoda_prototyp(odwołanie) + " { return " + Połącz + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(treść_metody(odwołanie, dane));
        }
        for (Map.Entry<metoda_odwołanie, członek_dane> wpis_WARTOŚĆ : 필드들.entrySet()) {
            metoda_odwołanie odwołanie = wpis_WARTOŚĆ.getKey(); byte[] stała_WARTOŚĆ = wpis_WARTOŚĆ.getValue().wartość_atrybutu.get("ConstantValue");
            String WARTOŚĆ = stała_WARTOŚĆ == null ? "0" : wyrażenie_stałe(클래스들.get(odwołanie.właściciel_WARTOŚĆ), new dane_Czytnik(stała_WARTOŚĆ).두바이트());
            필드선언들.add("static word " + symbol("field", odwołanie.부분들()) + " = " + WARTOŚĆ + ";");
        }
        for (String Nazwa : 클래스들.keySet()) {
            String inicjuj = symbol("init", Nazwa), Stan_WARTOŚĆ = symbol("state", Nazwa);
            선언들.add("static void " + inicjuj + "(void);"); 필드선언들.add("static unsigned " + Stan_WARTOŚĆ + ";");
            metoda_odwołanie odwołanie = new metoda_odwołanie(Nazwa, "<clinit>", "()V");
            몸체들.add("static void " + inicjuj + "(void) { if(" + Stan_WARTOŚĆ + ") return; " + Stan_WARTOŚĆ + " = 1; " + (함수들.containsKey(odwołanie) ? symbol("method", odwołanie.부분들()) + "(); " : "") + Stan_WARTOŚĆ + " = 2; }");
        }
        몸체들.add(eksportować_metoda("java_entry", punkt_wejścia, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Przypisz_WARTOŚĆ : 내보내기목록) {
            int indeks_pozycji = Przypisz_WARTOŚĆ.indexOf('='); if (indeks_pozycji < 1) throw new translacja_błąd("내보내기 Przypisz_WARTOŚĆ błąd");
            String Nazwa = Przypisz_WARTOŚĆ.substring(0, indeks_pozycji); 공개이름.add(Nazwa); 몸체들.add(eksportować_metoda(Nazwa, Przypisz_WARTOŚĆ.substring(indeks_pozycji + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> wpis_WARTOŚĆ : 문자열들.entrySet()) {
            String tekst = wpis_WARTOŚĆ.getKey(); StringBuilder TABLICA_WARTOŚĆ = new StringBuilder("static const word " + wpis_WARTOŚĆ.getValue() + "[] = {" + tekst.length());
            for (int 순번 = 0; 순번 < tekst.length(); 순번++) TABLICA_WARTOŚĆ.append(", ").append((int)tekst.charAt(순번));
            문자열선언들.add(TABLICA_WARTOŚĆ.append("};").toString());
        }
        String wsparcie_WARTOŚĆ = Files.readString(zasób_ścieżka.resolve("CLR_wsparcie.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(sterta_Word_ILE_LICZB));
        return 기계원문한국어화(wsparcie_WARTOŚĆ + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String plik_źródłowy, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nazwa_tabela = new HashMap<>();
        for (String wiersz_wejścia : Files.readAllLines(zasób_ścieżka.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] parować_WARTOŚĆ = wiersz_wejścia.split("\t"); nazwa_tabela.put(parować_WARTOŚĆ[0], parować_WARTOŚĆ[1]);
        }
        Pattern fragment_wyrażenie = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = fragment_wyrażenie.matcher(plik_źródłowy); StringBuffer WYNIK = new StringBuffer();
        while (찾개.find()) {
            String Nazwa = 찾개.group(), 새이름 = Nazwa;
            if (!Nazwa.startsWith("//") && !Nazwa.startsWith("/*") && !Nazwa.startsWith("\"") && !Nazwa.startsWith("'") && !공개이름.contains(Nazwa)) {
                새이름 = nazwa_tabela.getOrDefault(Nazwa, Nazwa);
                if (Nazwa.matches("a[0-9]+")) 새이름 = "argumenty" + Nazwa.substring(1);
                if (Nazwa.matches("b[0-9]+")) 새이름 = "gałąź_22e01337" + Nazwa.substring(1);
                if (범용표기) {
                    StringBuilder notacja_WARTOŚĆ = new StringBuilder();
                    for (char znak_WARTOŚĆ : 새이름.toCharArray()) notacja_WARTOŚĆ.append(znak_WARTOŚĆ < 128 ? Character.toString(znak_WARTOŚĆ) : String.format(Locale.ROOT, "\\u%04x", (int)znak_WARTOŚĆ));
                    새이름 = notacja_WARTOŚĆ.toString();
                }
            }
            찾개.appendReplacement(WYNIK, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(WYNIK); return WYNIK.toString();
    }
    String X_86_treść_metody(metoda_odwołanie FUNKCJA_WARTOŚĆ, członek_dane dane, Map<String,String> maszyna_tabela, String wartość_docelowa) {
        String pisak_WARTOŚĆ = symbol("method", FUNKCJA_WARTOŚĆ.부분들());
        List<String> wiersz_wejścia = new ArrayList<>();
        if ((dane.dostęp_wpis & 0x100) != 0) {
            String Połącz = maszyna_tabela.get(FUNKCJA_WARTOŚĆ.Nazwa + FUNKCJA_WARTOŚĆ.서술);
            if (!FUNKCJA_WARTOŚĆ.właściciel_WARTOŚĆ.equals(wartość_docelowa.equals("kernel") ? "urządzenie_WARTOŚĆ" : "przestrzeń_użytkownika") || Połącz == null) throw new translacja_błąd("허용되지 않은 native FUNKCJA_WARTOŚĆ");
            return ".text\n" + pisak_WARTOŚĆ + ":\njmp " + Połącz;
        }
        byte[] tekst_podstawowy = dane.wartość_atrybutu.get("Code"); if (tekst_podstawowy == null) throw new translacja_błąd("FUNKCJA_WARTOŚĆ 몸체가 없음");
        dane_Czytnik Czytnik_WARTOŚĆ = new dane_Czytnik(tekst_podstawowy); Czytnik_WARTOŚĆ.두바이트(); int lokalny_ILE_LICZB = Czytnik_WARTOŚĆ.두바이트();
        dane_Czytnik polecenie_dane = new dane_Czytnik(Czytnik_WARTOŚĆ.Odczyt(Czytnik_WARTOŚĆ.네바이트()));
        if (Czytnik_WARTOŚĆ.두바이트() != 0) throw new translacja_błąd("try/catch/finally 미지원");
        metoda_deskryptor format_WARTOŚĆ = new metoda_deskryptor(FUNKCJA_WARTOŚĆ.서술); if (lokalny_ILE_LICZB < format_WARTOŚĆ.argumenty.size()) throw new translacja_błąd("매개변수보다 적은 lokalny_Scope zmienna_WARTOŚĆ");
        Collections.addAll(wiersz_wejścia,".text",".globl " + pisak_WARTOŚĆ,".type " + pisak_WARTOŚĆ + ", @function",pisak_WARTOŚĆ + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokalny_ILE_LICZB * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_WARTOŚĆ.argumenty.size(); 순번++) Collections.addAll(wiersz_wejścia,"movl " + (8 + 4 * (format_WARTOŚĆ.argumenty.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Klasa_dane Klasa_WARTOŚĆ = 클래스들.get(FUNKCJA_WARTOŚĆ.właściciel_WARTOŚĆ); Set<Integer> 경계들 = new HashSet<>(), gałąź_Lista = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (polecenie_dane.pozycja < polecenie_dane.dane.length) {
            int pozycja = polecenie_dane.pozycja, polecenie = polecenie_dane.한바이트(); String indeks_pozycji = pisak_WARTOŚĆ + "_b" + pozycja;
            wiersz_wejścia.add(indeks_pozycji + ":"); 경계들.add(pozycja);
            if (polecenie == 0) wiersz_wejścia.add("nop");
            else if (polecenie == 1) wiersz_wejścia.add("pushl $0");
            else if (polecenie >= 2 && polecenie <= 8) wiersz_wejścia.add("pushl $" + (polecenie - 3));
            else if (polecenie == 16 || polecenie == 17) wiersz_wejścia.add("pushl $" + (polecenie == 16 ? polecenie_dane.부호한바이트() : polecenie_dane.부호두바이트()));
            else if (polecenie == 18 || polecenie == 19) {
                int INDEKS = polecenie == 18 ? polecenie_dane.한바이트() : polecenie_dane.두바이트();
                wiersz_wejścia.add("pushl $" + X_86_stała(Klasa_WARTOŚĆ,INDEKS));
            } else if (polecenie == 21 || polecenie == 25 || (polecenie >= 26 && polecenie <= 29) || (polecenie >= 42 && polecenie <= 45) || polecenie == 54 || polecenie == 58 || (polecenie >= 59 && polecenie <= 62) || (polecenie >= 75 && polecenie <= 78)) {
                boolean 읽음 = polecenie < 54; int INDEKS = polecenie == 21 || polecenie == 25 || polecenie == 54 || polecenie == 58 ? polecenie_dane.한바이트() : polecenie - (polecenie <= 29 ? 26 : polecenie <= 45 ? 42 : polecenie <= 62 ? 59 : 75);
                czek_lokalny(INDEKS,lokalny_ILE_LICZB); wiersz_wejścia.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEKS + 1)) + "(%ebp)");
            } else if (polecenie == 46) Collections.addAll(wiersz_wejścia,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (polecenie == 79) Collections.addAll(wiersz_wejścia,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (polecenie == 87 || polecenie == 88) wiersz_wejścia.add("addl $" + (polecenie == 87 ? 4 : 8) + ", %esp");
            else if (polecenie >= 89 && polecenie <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] zamówić_Lista = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[polecenie - 89]; 순번++) wiersz_wejścia.add("popl " + 저장기들[순번]);
                for (int 순번 : zamówić_Lista[polecenie - 89]) wiersz_wejścia.add("pushl " + 저장기들[순번]);
            } else if (polecenie == 96 || polecenie == 100 || polecenie == 104 || polecenie == 126 || polecenie == 128 || polecenie == 130) {
                String zabieg_WARTOŚĆ = polecenie == 96 ? "addl" : polecenie == 100 ? "subl" : polecenie == 104 ? "imull" : polecenie == 126 ? "andl" : polecenie == 128 ? "orl" : "xorl";
                Collections.addAll(wiersz_wejścia,"popl %ecx","popl %eax",zabieg_WARTOŚĆ + " %ecx, %eax","pushl %eax");
            } else if (polecenie == 108 || polecenie == 112) Collections.addAll(wiersz_wejścia,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + indeks_pozycji + "_divide","cmpl $0x80000000, %eax","jne " + indeks_pozycji + "_divide","xorl %edx, %edx","jmp " + indeks_pozycji + "_done",indeks_pozycji + "_divide:","cltd","idivl %ecx",indeks_pozycji + "_done:","pushl " + (polecenie == 108 ? "%eax" : "%edx"));
            else if (polecenie == 116) wiersz_wejścia.add("negl (%esp)");
            else if (polecenie == 120 || polecenie == 122 || polecenie == 124) Collections.addAll(wiersz_wejścia,"popl %ecx","popl %eax",(polecenie == 120 ? "sall" : polecenie == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (polecenie == 132) {
                int INDEKS = polecenie_dane.한바이트(), przyrost_WARTOŚĆ = polecenie_dane.부호한바이트(); czek_lokalny(INDEKS,lokalny_ILE_LICZB); wiersz_wejścia.add("addl $" + przyrost_WARTOŚĆ + ", -" + (4 * (INDEKS + 1)) + "(%ebp)");
            } else if (polecenie >= 145 && polecenie <= 147) Collections.addAll(wiersz_wejścia,"popl %eax",polecenie == 145 ? "movsbl %al, %eax" : polecenie == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (polecenie >= 153 && polecenie <= 166) {
                if (polecenie <= 158) Collections.addAll(wiersz_wejścia,"popl %eax","testl %eax, %eax");
                else Collections.addAll(wiersz_wejścia,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int cel_WARTOŚĆ = pozycja + polecenie_dane.부호두바이트(); gałąź_Lista.add(cel_WARTOŚĆ); wiersz_wejścia.add(비교들[polecenie - (polecenie <= 158 ? 153 : 159)] + " " + pisak_WARTOŚĆ + "_b" + cel_WARTOŚĆ);
            } else if (polecenie == 167 || polecenie == 200) {
                int cel_WARTOŚĆ = pozycja + (polecenie == 167 ? polecenie_dane.부호두바이트() : polecenie_dane.네바이트()); gałąź_Lista.add(cel_WARTOŚĆ); wiersz_wejścia.add("jmp " + pisak_WARTOŚĆ + "_b" + cel_WARTOŚĆ);
            } else if (polecenie == 170 || polecenie == 171) {
                while (polecenie_dane.pozycja % 4 != 0) polecenie_dane.한바이트();
                int wartość_domyślna = pozycja + polecenie_dane.네바이트(); gałąź_Lista.add(wartość_domyślna); wiersz_wejścia.add("popl %eax");
                int towar_ILE_LICZB, 아래 = 0;
                if (polecenie == 170) { 아래 = polecenie_dane.네바이트(); int 위 = polecenie_dane.네바이트(); long długość_WARTOŚĆ = (long)위 - 아래 + 1; if (długość_WARTOŚĆ < 1 || długość_WARTOŚĆ > (polecenie_dane.dane.length - polecenie_dane.pozycja) / 4) throw new translacja_błąd("switch obcinać błąd"); towar_ILE_LICZB = (int)długość_WARTOŚĆ; }
                else { towar_ILE_LICZB = polecenie_dane.네바이트(); if (towar_ILE_LICZB < 0 || towar_ILE_LICZB > (polecenie_dane.dane.length - polecenie_dane.pozycja) / 8) throw new translacja_błąd("switch Rozmiar błąd"); }
                for (int 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) {
                    int WARTOŚĆ = polecenie == 170 ? 아래 + 순번 : polecenie_dane.네바이트(), cel_WARTOŚĆ = pozycja + polecenie_dane.네바이트(); gałąź_Lista.add(cel_WARTOŚĆ);
                    Collections.addAll(wiersz_wejścia,"cmpl $" + WARTOŚĆ + ", %eax","je " + pisak_WARTOŚĆ + "_b" + cel_WARTOŚĆ);
                }
                wiersz_wejścia.add("jmp " + pisak_WARTOŚĆ + "_b" + wartość_domyślna);
            } else if (polecenie == 172 || polecenie == 176 || polecenie == 177) {
                if (polecenie != 177) wiersz_wejścia.add("popl %eax"); Collections.addAll(wiersz_wejścia,"leave","ret");
            } else if (polecenie == 178 || polecenie == 179) {
                metoda_odwołanie odwołanie = Klasa_WARTOŚĆ.odwołanie(polecenie_dane.두바이트()); if (!필드들.containsKey(odwołanie)) throw new translacja_błąd("알 identyfikator 없는 wartość_pola");
                Collections.addAll(wiersz_wejścia,"call " + symbol("init",odwołanie.właściciel_WARTOŚĆ),(polecenie == 178 ? "pushl " : "popl ") + symbol("field",odwołanie.부분들()));
            } else if (polecenie == 184) {
                metoda_odwołanie odwołanie = Klasa_WARTOŚĆ.odwołanie(polecenie_dane.두바이트()); if (!함수들.containsKey(odwołanie)) throw new translacja_błąd("알 identyfikator 없는 FUNKCJA_WARTOŚĆ");
                metoda_deskryptor 호출형식 = new metoda_deskryptor(odwołanie.서술); Collections.addAll(wiersz_wejścia,"call " + symbol("init",odwołanie.właściciel_WARTOŚĆ),"call " + symbol("method",odwołanie.부분들()));
                if (!호출형식.argumenty.isEmpty()) wiersz_wejścia.add("addl $" + 호출형식.argumenty.size() * 4 + ", %esp");
                if (!호출형식.Zwrot_KR.equals("V")) wiersz_wejścia.add("pushl %eax");
            } else if (polecenie == 182) {
                metoda_odwołanie odwołanie = Klasa_WARTOŚĆ.odwołanie(polecenie_dane.두바이트());
                if (odwołanie.equals(new metoda_odwołanie("java/lang/String","length","()I"))) Collections.addAll(wiersz_wejścia,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (odwołanie.equals(new metoda_odwołanie("java/lang/String","charAt","(I)C"))) Collections.addAll(wiersz_wejścia,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new translacja_błąd("가상 FUNKCJA_WARTOŚĆ 호출 미지원");
            } else if (polecenie == 188) {
                if (polecenie_dane.한바이트() != 10) throw new translacja_błąd("new int[]만 wsparcie_WARTOŚĆ"); Collections.addAll(wiersz_wejścia,"popl %eax","call rt_new_array","pushl %eax");
            } else if (polecenie == 190) Collections.addAll(wiersz_wejścia,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (polecenie == 196) {
                int rozszerzenie_WARTOŚĆ = polecenie_dane.한바이트(), INDEKS = polecenie_dane.두바이트(); czek_lokalny(INDEKS,lokalny_ILE_LICZB);
                if (rozszerzenie_WARTOŚĆ == 21 || rozszerzenie_WARTOŚĆ == 25 || rozszerzenie_WARTOŚĆ == 54 || rozszerzenie_WARTOŚĆ == 58) wiersz_wejścia.add((rozszerzenie_WARTOŚĆ <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEKS + 1) + "(%ebp)");
                else if (rozszerzenie_WARTOŚĆ == 132) wiersz_wejścia.add("addl $" + polecenie_dane.부호두바이트() + ", -" + 4 * (INDEKS + 1) + "(%ebp)");
                else throw new translacja_błąd("wide polecenie 미지원");
            } else if (polecenie == 198 || polecenie == 199) {
                int cel_WARTOŚĆ = pozycja + polecenie_dane.부호두바이트(); gałąź_Lista.add(cel_WARTOŚĆ); Collections.addAll(wiersz_wejścia,"popl %eax","testl %eax, %eax",(polecenie == 198 ? "je " : "jne ") + pisak_WARTOŚĆ + "_b" + cel_WARTOŚĆ);
            } else throw new translacja_błąd("미지원 polecenie: " + polecenie);
        }
        if (!경계들.containsAll(gałąź_Lista)) throw new translacja_błąd("polecenie 경계가 아닌 곳으로 gałąź_22e01337");
        wiersz_wejścia.add(".size " + pisak_WARTOŚĆ + ", .-" + pisak_WARTOŚĆ); return String.join("\n",wiersz_wejścia);
    }
    String X_86_stała(Klasa_dane dane, int INDEKS) {
        if (dane.stała_Rodzaj[INDEKS] == 3) return dane.stała_dane[INDEKS].toString();
        if (dane.stała_Rodzaj[INDEKS] == 8) return ciąg_symbol(dane.문자((Integer)dane.stała_dane[INDEKS]));
        throw new translacja_błąd("정수와 ciąg_WARTOŚĆ 상수만 wsparcie_WARTOŚĆ");
    }
    String X_86_zestaw(String punkt_wejścia, List<String> 내보냄, String wartość_docelowa) throws IOException {
        Map<String,String> maszyna_tabela = new HashMap<>();
        for (String wiersz_wejścia : Files.readAllLines(zasób_ścieżka.resolve("_86_maszyna_Functions.tsv"))) { String[] parować_WARTOŚĆ = wiersz_wejścia.split("\t"); if (parować_WARTOŚĆ[0].equals(wartość_docelowa)) maszyna_tabela.put(parować_WARTOŚĆ[1] + parować_WARTOŚĆ[2],parować_WARTOŚĆ[3]); }
        int indeks_pozycji = punkt_wejścia.lastIndexOf('.'); if (indeks_pozycji < 0) throw new translacja_błąd("punkt_wejścia Przypisz_WARTOŚĆ błąd");
        String właściciel_WARTOŚĆ = punkt_wejścia.substring(0,indeks_pozycji).replace('.','/'), metoda_wpis_nazwa = punkt_wejścia.substring(indeks_pozycji + 1); metoda_odwołanie punkt_wejścia_WARTOŚĆ = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metoda_odwołanie odwołanie = new metoda_odwołanie(właściciel_WARTOŚĆ,metoda_wpis_nazwa,서술); if (함수들.containsKey(odwołanie)) { if (punkt_wejścia_WARTOŚĆ != null) throw new translacja_błąd("겹친 punkt_wejścia"); punkt_wejścia_WARTOŚĆ = odwołanie; } }
        if (punkt_wejścia_WARTOŚĆ == null || (함수들.get(punkt_wejścia_WARTOŚĆ).dostęp_wpis & 0x100) != 0) throw new translacja_błąd("punkt_wejścia_WARTOŚĆ FUNKCJA_WARTOŚĆ format_WARTOŚĆ błąd");
        List<String> wiersz_wejścia = new ArrayList<>(); wiersz_wejścia.add(".code32");
        for (Klasa_dane dane : 클래스들.values()) {
            String Stan_WARTOŚĆ = symbol("state",dane.Nazwa), inicjuj = symbol("init",dane.Nazwa);
            Collections.addAll(wiersz_wejścia,".bss",".balign 4",Stan_WARTOŚĆ + ": .long 0",".text",inicjuj + ":","cmpl $0, " + Stan_WARTOŚĆ,"jne " + inicjuj + "_done","movl $1, " + Stan_WARTOŚĆ);
            metoda_odwołanie inicjator_odwołanie = new metoda_odwołanie(dane.Nazwa,"<clinit>","()V"); if (함수들.containsKey(inicjator_odwołanie)) wiersz_wejścia.add("call " + symbol("method",inicjator_odwołanie.부분들()));
            Collections.addAll(wiersz_wejścia,"movl $2, " + Stan_WARTOŚĆ,inicjuj + "_done:","ret");
            for (członek_dane wartość_pola : dane.wartość_pola) {
                byte[] stała_WARTOŚĆ = wartość_pola.wartość_atrybutu.get("ConstantValue"); String WARTOŚĆ = stała_WARTOŚĆ == null ? "0" : X_86_stała(dane,new dane_Czytnik(stała_WARTOŚĆ).두바이트());
                Collections.addAll(wiersz_wejścia,".data",".balign 4",symbol("field",dane.Nazwa,wartość_pola.Nazwa,wartość_pola.서술) + ": .long " + WARTOŚĆ);
            }
            for (członek_dane FUNKCJA_WARTOŚĆ : dane.FUNKCJA_WARTOŚĆ) if (!FUNKCJA_WARTOŚĆ.Nazwa.equals("<init>")) wiersz_wejścia.add(X_86_treść_metody(new metoda_odwołanie(dane.Nazwa,FUNKCJA_WARTOŚĆ.Nazwa,FUNKCJA_WARTOŚĆ.서술),FUNKCJA_WARTOŚĆ,maszyna_tabela,wartość_docelowa));
        }
        Collections.addAll(wiersz_wejścia,".text",".globl java_entry","java_entry:","call " + symbol("init",punkt_wejścia_WARTOŚĆ.właściciel_WARTOŚĆ),"call " + symbol("method",punkt_wejścia_WARTOŚĆ.부분들()));
        if (punkt_wejścia_WARTOŚĆ.서술.equals("()V")) wiersz_wejścia.add("xorl %eax, %eax"); wiersz_wejścia.add("ret");
        for (String Przypisz_WARTOŚĆ : 내보냄) {
            int ogranicznik_WARTOŚĆ = Przypisz_WARTOŚĆ.indexOf('='); if (ogranicznik_WARTOŚĆ < 1) throw new translacja_błąd("내보내기 Przypisz_WARTOŚĆ błąd");
            String zewnętrzny_WARTOŚĆ = Przypisz_WARTOŚĆ.substring(0,ogranicznik_WARTOŚĆ), FUNKCJA_WARTOŚĆ = Przypisz_WARTOŚĆ.substring(ogranicznik_WARTOŚĆ + 1); int Dywizja_KR = FUNKCJA_WARTOŚĆ.lastIndexOf('.');
            if (Dywizja_KR < 0 || !zewnętrzny_WARTOŚĆ.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new translacja_błąd("내보내기 symbol błąd");
            String Klasa_WARTOŚĆ = FUNKCJA_WARTOŚĆ.substring(0,Dywizja_KR).replace('.','/'), Nazwa = FUNKCJA_WARTOŚĆ.substring(Dywizja_KR + 1); metoda_odwołanie zaznaczenie_WARTOŚĆ = null;
            for (metoda_odwołanie odwołanie : 함수들.keySet()) if (odwołanie.właściciel_WARTOŚĆ.equals(Klasa_WARTOŚĆ) && odwołanie.Nazwa.equals(Nazwa)) { if (zaznaczenie_WARTOŚĆ != null) throw new translacja_błąd("겹친 내보내기 wartość_docelowa"); zaznaczenie_WARTOŚĆ = odwołanie; }
            if (zaznaczenie_WARTOŚĆ == null) throw new translacja_błąd("내보낼 함수가 없음");
            Collections.addAll(wiersz_wejścia,".text",".globl " + zewnętrzny_WARTOŚĆ,zewnętrzny_WARTOŚĆ + ":","call " + symbol("init",zaznaczenie_WARTOŚĆ.właściciel_WARTOŚĆ),"jmp " + symbol("method",zaznaczenie_WARTOŚĆ.부분들()));
        }
        wiersz_wejścia.add(".section .rodata");
        for (Map.Entry<String,String> wpis_WARTOŚĆ : 문자열들.entrySet()) {
            Collections.addAll(wiersz_wejścia,".balign 4",wpis_WARTOŚĆ.getValue() + ":",".long " + wpis_WARTOŚĆ.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lekcja_WARTOŚĆ : wpis_WARTOŚĆ.getKey().toCharArray()) 단위들.add(Integer.toString(lekcja_WARTOŚĆ)); if (!단위들.isEmpty()) wiersz_wejścia.add(".long " + String.join(",",단위들));
        }
        wiersz_wejścia.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",wiersz_wejścia) + "\n";
    }
    static void Wykonaj_narzędzie(List<String> polecenie) throws Exception {
        if (new ProcessBuilder(polecenie).inheritIO().start().waitFor() != 0) throw new translacja_błąd("kompilować_źródło błąd: " + polecenie.get(0));
    }
    static String dane_ciąg(String tekst) { return "\"" + tekst.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_translacja(List<Path> wejście_Lista, String wartość_docelowa, String punkt_wejścia, List<String> 내보냄, Path pozycja_wyjścia, Path zasób_WARTOŚĆ) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Klasa_ścieżka = 임시.resolve("classes"); Files.createDirectory(Klasa_ścieżka);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Klasa_ścieżka.toString(),"-sourcepath",Klasa_ścieżka.toString(),"-d",Klasa_ścieżka.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int źródło_ILE_LICZB = 0;
            for (Path wejście_WARTOŚĆ : wejście_Lista) {
                if (pozycja_wyjścia.toAbsolutePath().normalize().equals(wejście_WARTOŚĆ.toAbsolutePath().normalize())) throw new translacja_błąd("pozycja_wyjścia 파일과 입력이 같음");
                if (wejście_WARTOŚĆ.toString().endsWith(".java")) { 자바명령.add(wejście_WARTOŚĆ.toString()); źródło_ILE_LICZB++; }
                else if (wejście_WARTOŚĆ.toString().endsWith(".class")) 바이트코드.add(wejście_WARTOŚĆ);
                else throw new translacja_błąd(".java 또는 .class만 wsparcie_WARTOŚĆ");
            }
            if (źródło_ILE_LICZB > 0) Wykonaj_narzędzie(자바명령);
            try (java.util.stream.Stream<Path> ścieżka_Lista = Files.walk(Klasa_ścieżka)) { ścieżka_Lista.filter(ścieżka_2 -> ścieżka_2.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 KONWERTUJ_WARTOŚĆ = new 기계어미리번역(바이트코드,wartość_docelowa.equals("user") ? "user" : "kernel",262144,zasób_WARTOŚĆ);
            String asemblować_WARTOŚĆ = KONWERTUJ_WARTOŚĆ.X_86_zestaw(punkt_wejścia,내보냄,wartość_docelowa); Files.writeString(임시.resolve("program.s"),asemblować_WARTOŚĆ,StandardCharsets.UTF_8);
            Path narzędzie_stanowisko = zasób_WARTOŚĆ.getParent();
            Wykonaj_narzędzie(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Wykonaj_narzędzie(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),narzędzie_stanowisko.resolve("CLR_wsparcie.s").toString()));
            List<String> Połącz = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (wartość_docelowa.equals("kernel")) Połącz.add("-r");
            else {
                Wykonaj_narzędzie(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),narzędzie_stanowisko.resolve(wartość_docelowa.equals("user") ? "START_użytkownik_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(Połącz,"-e","_start",임시.resolve("start.o").toString());
                if (wartość_docelowa.equals("user")) Collections.addAll(Połącz,"-T",narzędzie_stanowisko.resolve("użytkownik_Link_Układ.ld").toString());
            }
            Collections.addAll(Połącz,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Wykonaj_narzędzie(Połącz);
            pozycja_wyjścia = pozycja_wyjścia.toAbsolutePath(); Files.createDirectories(pozycja_wyjścia.getParent()); Path publikować_WARTOŚĆ = Files.createTempFile(pozycja_wyjścia.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publikować_WARTOŚĆ,StandardCopyOption.REPLACE_EXISTING); Files.move(publikować_WARTOŚĆ,pozycja_wyjścia,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publikować_WARTOŚĆ); }
            Files.setPosixFilePermissions(pozycja_wyjścia,java.nio.file.attribute.PosixFilePermissions.fromString(wartość_docelowa.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(pozycja_wyjścia + ".s"),asemblować_WARTOŚĆ,StandardCharsets.UTF_8);
            List<String> symbol_dane = new ArrayList<>(), dane_źródłowe = new ArrayList<>();
            for (metoda_odwołanie odwołanie : KONWERTUJ_WARTOŚĆ.함수들.keySet()) symbol_dane.add(dane_ciąg(symbol("method",odwołanie.부분들())) + ":" + dane_ciąg(odwołanie.właściciel_WARTOŚĆ + "." + odwołanie.Nazwa + odwołanie.서술));
            for (Path wejście_WARTOŚĆ : wejście_Lista) {
                byte[] skrót_Plik = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(wejście_WARTOŚĆ)); StringBuilder tekst = new StringBuilder(); for (byte WARTOŚĆ : skrót_Plik) tekst.append(String.format(Locale.ROOT,"%02x",WARTOŚĆ & 255));
                dane_źródłowe.add(dane_ciąg(wejście_WARTOŚĆ.toAbsolutePath().toString()) + ":" + dane_ciąg(tekst.toString()));
            }
            Files.writeString(Paths.get(pozycja_wyjścia + ".json"),"{\"target\":" + dane_ciąg(wartość_docelowa) + ",\"entry\":" + dane_ciąg(punkt_wejścia) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbol_dane) + "},\"sources\":{" + String.join(",",dane_źródłowe) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> ścieżka_Lista = Files.walk(임시)) { for (Path ścieżka_2 : (Iterable<Path>)ścieżka_Lista.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(ścieżka_2); }
        }
    }
    public static void main(String[] argumenty) {
        try {
            String punkt_wejścia = null, wartość_docelowa = "kernel", X_86_cel = null; Path produkt_wyjściowy_ścieżka = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> ścieżka_Lista = new ArrayList<>();
            for (int 순번 = 0; 순번 < argumenty.length; 순번++) {
                String WARTOŚĆ = argumenty[순번];
                switch (WARTOŚĆ) {
                    case "--target": X_86_cel = argumenty[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Klasa_WARTOŚĆ.FUNKCJA_WARTOŚĆ -o pozycja_wyjścia [--target linux|kernel|user] [--profile kernel|user] [--export symbol=Klasa_WARTOŚĆ.FUNKCJA_WARTOŚĆ] 클래스파일 또는 Java원문"); return;
                    case "--entry": punkt_wejścia = argumenty[++순번]; break;
                    case "--profile": wartość_docelowa = argumenty[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(argumenty[++순번]); break;
                    case "--export": 내보냄.add(argumenty[++순번]); break;
                    case "-o": produkt_wyjściowy_ścieżka = Paths.get(argumenty[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (WARTOŚĆ.startsWith("-")) throw new translacja_błąd("알 identyfikator 없는 옵션: " + WARTOŚĆ); ścieżka_Lista.add(Paths.get(WARTOŚĆ));
                }
            }
            if (punkt_wejścia == null || produkt_wyjściowy_ścieżka == null || ścieżka_Lista.isEmpty()) throw new translacja_błąd("--entry, -o, Klasa_WARTOŚĆ 파일이 필요합니다");
            Path zasób_WARTOŚĆ = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_cel != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_cel)) throw new translacja_błąd("알 identyfikator 없는 Wykonaj_polecenie wartość_docelowa");
                X_86_translacja(ścieżka_Lista,X_86_cel,punkt_wejścia,내보냄,produkt_wyjściowy_ścieżka,zasób_WARTOŚĆ); return;
            }
            String plik_źródłowy = new 기계어미리번역(ścieżka_Lista, wartość_docelowa, 낱말수, zasób_WARTOŚĆ).generować(punkt_wejścia, 내보냄, 범용표기);
            produkt_wyjściowy_ścieżka = produkt_wyjściowy_ścieżka.toAbsolutePath(); Files.createDirectories(produkt_wyjściowy_ścieżka.getParent());
            Path 임시 = Files.createTempFile(produkt_wyjściowy_ścieżka.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, plik_źródłowy, StandardCharsets.UTF_8); Files.move(임시, produkt_wyjściowy_ścieżka, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception błąd) { System.err.println("kompilować_źródło błąd: " + błąd.getMessage()); System.exit(1); }
    }
}
