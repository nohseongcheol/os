// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java lekcia_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. hostiteľ JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Preklad_Chyba extends RuntimeException {
        Preklad_Chyba(String 설명) { super(설명); }
    }
    static final class údaje_Čítačka {
        final byte[] údaje;
        int Pozícia;
        údaje_Čítačka(byte[] vstup_údaje) { údaje = vstup_údaje; }
        byte[] Čítanie(int dĺžka_VALUE) {
            if (dĺžka_VALUE < 0 || dĺžka_VALUE > údaje.length - Pozícia) throw new Preklad_Chyba("잘린 lekcia_VALUE 또는 Príkaz údaje");
            byte[] KR = Arrays.copyOfRange(údaje, Pozícia, Pozícia + dĺžka_VALUE); Pozícia += dĺžka_VALUE; return KR;
        }
        int 한바이트() { if (Pozícia >= údaje.length) throw new Preklad_Chyba("잘린 Príkaz údaje"); return údaje[Pozícia++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class člen_údaje {
        final int prístup_položka;
        final String Názov, 서술;
        final Map<String, byte[]> atribút_VALUE;
        člen_údaje(int prístup_VALUE, String názov_VALUE, String 서술값, Map<String, byte[]> atribút_údaje) {
            prístup_položka = prístup_VALUE; Názov = názov_VALUE; 서술 = 서술값; atribút_VALUE = atribút_údaje;
        }
    }
    static final class metóda_zdroj implements Comparable<metóda_zdroj> {
        final String vlastník_VALUE, Názov, 서술;
        metóda_zdroj(String 소유값, String názov_VALUE, String 서술값) { vlastník_VALUE = 소유값; Názov = názov_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{vlastník_VALUE, Názov, 서술}; }
        public int compareTo(metóda_zdroj partnerský_uzol_VALUE) {
            int Porovnanie_VALUE = vlastník_VALUE.compareTo(partnerský_uzol_VALUE.vlastník_VALUE);
            if (Porovnanie_VALUE == 0) Porovnanie_VALUE = Názov.compareTo(partnerský_uzol_VALUE.Názov);
            return Porovnanie_VALUE == 0 ? 서술.compareTo(partnerský_uzol_VALUE.서술) : Porovnanie_VALUE;
        }
        public boolean equals(Object partnerský_uzol_VALUE) { return partnerský_uzol_VALUE instanceof metóda_zdroj && compareTo((metóda_zdroj) partnerský_uzol_VALUE) == 0; }
        public int hashCode() { return Objects.hash(vlastník_VALUE, Názov, 서술); }
    }
    static final class lekcia_údaje {
        final int[] 상수종류;
        final Object[] konštanta_údaje;
        final String Názov;
        final List<člen_údaje> hodnota_poľa, funkcia_VALUE;
        lekcia_údaje(Path Cesta) throws IOException {
            údaje_Čítačka Čítačka_VALUE = new údaje_Čítačka(Files.readAllBytes(Cesta));
            if (Čítačka_VALUE.네바이트() != 0xcafebabe) throw new Preklad_Chyba("Java lekcia_VALUE 표식이 아님");
            Čítačka_VALUE.Čítanie(4);
            int položka_COUNT = Čítačka_VALUE.두바이트(); 상수종류 = new int[položka_COUNT]; konštanta_údaje = new Object[položka_COUNT];
            for (int 순번 = 1; 순번 < položka_COUNT; 순번++) {
                int 종류 = Čítačka_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int dĺžka_VALUE = Čítačka_VALUE.두바이트();
                        byte[] znak_medzipamäť = Čítačka_VALUE.Čítanie(dĺžka_VALUE), 길이붙인자료 = new byte[dĺžka_VALUE + 2];
                        길이붙인자료[0] = (byte)(dĺžka_VALUE >> 8); 길이붙인자료[1] = (byte)dĺžka_VALUE;
                        System.arraycopy(znak_medzipamäť, 0, 길이붙인자료, 2, dĺžka_VALUE);
                        konštanta_údaje[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konštanta_údaje[순번] = Čítačka_VALUE.네바이트(); break;
                    case 4: Čítačka_VALUE.Čítanie(4); break;
                    case 5: case 6: Čítačka_VALUE.Čítanie(8); 순번++; break;
                    case 7: case 8: case 16: konštanta_údaje[순번] = Čítačka_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konštanta_údaje[순번] = new int[]{Čítačka_VALUE.두바이트(), Čítačka_VALUE.두바이트()}; break;
                    case 15: konštanta_údaje[순번] = new int[]{Čítačka_VALUE.한바이트(), Čítačka_VALUE.두바이트()}; break;
                    default: throw new Preklad_Chyba("지원하지 않는 konštanta_VALUE 종류: " + 종류);
                }
            }
            Čítačka_VALUE.두바이트(); Názov = názov_triedy(Čítačka_VALUE.두바이트());
            if (!názov_triedy(Čítačka_VALUE.두바이트()).equals("java/lang/Object") || Čítačka_VALUE.두바이트() != 0)
                throw new Preklad_Chyba(Názov + ": 상속 및 인터페이스 미지원");
            hodnota_poľa = 멤버읽기(Čítačka_VALUE); funkcia_VALUE = 멤버읽기(Čítačka_VALUE); 속성읽기(Čítačka_VALUE);
            if (Čítačka_VALUE.Pozícia != Čítačka_VALUE.údaje.length) throw new Preklad_Chyba("lekcia_VALUE 뒤에 남은 údaje");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Preklad_Chyba("문자 konštanta_VALUE INDEX chyba");
            return (String) konštanta_údaje[INDEX];
        }
        String názov_triedy(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Preklad_Chyba("lekcia_VALUE zdroj chyba");
            return 문자((Integer)konštanta_údaje[INDEX]);
        }
        metóda_zdroj zdroj(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Preklad_Chyba("멤버 zdroj chyba");
            int[] párovať_VALUE = (int[])konštanta_údaje[INDEX], názov_párovať = (int[])konštanta_údaje[párovať_VALUE[1]];
            return new metóda_zdroj(názov_triedy(párovať_VALUE[0]), 문자(názov_párovať[0]), 문자(názov_párovať[1]));
        }
        Map<String, byte[]> 속성읽기(údaje_Čítačka Čítačka_VALUE) {
            Map<String, byte[]> KR = new LinkedHashMap<>();
            int položka_COUNT = Čítačka_VALUE.두바이트();
            for (int 순번 = 0; 순번 < položka_COUNT; 순번++) {
                String atribút_názov = 문자(Čítačka_VALUE.두바이트()); byte[] VALUE = Čítačka_VALUE.Čítanie(Čítačka_VALUE.네바이트());
                if (KR.put(atribút_názov, VALUE) != null) throw new Preklad_Chyba("겹친 atribút_VALUE: " + atribút_názov);
            }
            return KR;
        }
        List<člen_údaje> 멤버읽기(údaje_Čítačka Čítačka_VALUE) {
            List<člen_údaje> KR = new ArrayList<>(); int položka_COUNT = Čítačka_VALUE.두바이트();
            for (int 순번 = 0; 순번 < položka_COUNT; 순번++) {
                int prístup_položka = Čítačka_VALUE.두바이트(); String metóda_položka_názov = 문자(Čítačka_VALUE.두바이트()), 서술 = 문자(Čítačka_VALUE.두바이트());
                KR.add(new člen_údaje(prístup_položka, metóda_položka_názov, 서술, 속성읽기(Čítačka_VALUE)));
            }
            return KR;
        }
    }
    static final class 함수형식 {
        final List<String> Argumenty = new ArrayList<>();
        final String vrátiť_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Preklad_Chyba("funkcia_VALUE 서술 chyba: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Preklad_Chyba("funkcia_VALUE 서술 chyba: " + 서술);
            Argumenty.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumenty.contains("V") || 반환들.size() != 1) throw new Preklad_Chyba("funkcia_VALUE 서술 chyba: " + 서술);
            vrátiť_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> KR = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Pozícia = 0; Pozícia < 서술.length();) {
            String výber_VALUE = null;
            for (String formát_VALUE : 허용형식) if (서술.startsWith(formát_VALUE, Pozícia)) { výber_VALUE = formát_VALUE; break; }
            if (výber_VALUE == null) throw new Preklad_Chyba("지원하지 않는 typ_údajov: " + 서술);
            KR.add(výber_VALUE); Pozícia += výber_VALUE.length();
        }
        return KR;
    }
    static String symbol(String 종류, String... 부분들) {
        try {
            byte[] hodnota_hash_Súbor = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Spracovanie_textu = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Spracovanie_textu.append(String.format(Locale.ROOT, "%02x", hodnota_hash_Súbor[순번] & 255));
            return Spracovanie_textu.toString();
        } catch (Exception chyba) { throw new Preklad_Chyba(chyba.toString()); }
    }
    final Map<String, lekcia_údaje> 클래스들 = new TreeMap<>();
    final Map<metóda_zdroj, člen_údaje> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), počítač_Azure_Functions_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, počítač_lekcia;
    final int halda_Word_COUNT;
    final Path zdroj_cesta;
    기계어미리번역(List<Path> cesta_Zoznam, String cieľová_hodnota, int 낱말수, Path zdroj_VALUE) throws IOException {
        if ((!cieľová_hodnota.equals("kernel") && !cieľová_hodnota.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Preklad_Chyba("Vykonať_príkaz cieľová_hodnota 또는 Pamäť_VALUE adresa_oblasť Veľkosť chyba");
        실행대상 = cieľová_hodnota; halda_Word_COUNT = 낱말수; zdroj_cesta = zdroj_VALUE;
        // 이 이름도 국가별 zdroj_strom generovať 시 해당 언어로 옮긴다.
        počítač_lekcia = cieľová_hodnota.equals("kernel") ? "Panel" : "používateľ";
        for (String riadok : Files.readAllLines(zdroj_VALUE.resolve("počítač_Azure_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = riadok.split("\t", -1);
            if (부분들.length != 4) throw new Preklad_Chyba("počítač_5eb260fa funkcia_VALUE údaje chyba");
            if (부분들[0].equals(cieľová_hodnota)) počítač_Azure_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Cesta : cesta_Zoznam) {
            lekcia_údaje údaje = new lekcia_údaje(Cesta);
            if (클래스들.put(údaje.Názov, údaje) != null) throw new Preklad_Chyba("중복 lekcia_VALUE: " + údaje.Názov);
            for (člen_údaje hodnota_poľa : údaje.hodnota_poľa) {
                if ((hodnota_poľa.prístup_položka & 8) == 0 || 형식읽기(hodnota_poľa.서술).equals(Collections.singletonList("V"))) throw new Preklad_Chyba("정적 필드만 Podpora_VALUE");
                if (필드들.put(new metóda_zdroj(údaje.Názov, hodnota_poľa.Názov, hodnota_poľa.서술), hodnota_poľa) != null) throw new Preklad_Chyba("중복 hodnota_poľa");
            }
            for (člen_údaje funkcia_VALUE : údaje.funkcia_VALUE) {
                if (funkcia_VALUE.Názov.equals("<init>")) continue;
                if ((funkcia_VALUE.prístup_položka & 8) == 0 || (funkcia_VALUE.prístup_položka & (0x20 | 0x400)) != 0) throw new Preklad_Chyba("정적 비동기화 함수만 Podpora_VALUE");
                new 함수형식(funkcia_VALUE.서술);
                if (함수들.put(new metóda_zdroj(údaje.Názov, funkcia_VALUE.Názov, funkcia_VALUE.서술), funkcia_VALUE) != null) throw new Preklad_Chyba("중복 funkcia_VALUE");
            }
        }
    }
    String reťazec_symbol(String Spracovanie_textu) { return 문자열들.computeIfAbsent(Spracovanie_textu, VALUE -> "j_text_" + 문자열들.size()); }
    String konštanta_výraz(lekcia_údaje údaje, int INDEX) {
        if (INDEX < 1 || INDEX >= údaje.상수종류.length) throw new Preklad_Chyba("konštanta_VALUE INDEX klip chyba");
        if (údaje.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + údaje.konštanta_údaje[INDEX] + ")";
        if (údaje.상수종류[INDEX] == 8) return "(word)" + reťazec_symbol(údaje.문자((Integer)údaje.konštanta_údaje[INDEX]));
        throw new Preklad_Chyba("정수와 reťazec_VALUE 상수만 Podpora_VALUE");
    }
    String 함수원형(metóda_zdroj zdroj) {
        List<String> 인수들 = new ArrayList<>(); int položka_COUNT = new 함수형식(zdroj.서술).Argumenty.size();
        for (int 순번 = 0; 순번 < položka_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symbol("method", zdroj.부분들()) + "(" + (položka_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void skontrolovať_miestny(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Preklad_Chyba("miestny_Rozsah 변수 INDEX klip chyba"); }
    void 분기넣기(List<String> Výstup, Set<Integer> vetva_Zoznam, int Pozícia, int 이동량, String podmienka) {
        int cieľ_VALUE = Pozícia + 이동량; vetva_Zoznam.add(cieľ_VALUE);
        Výstup.add((podmienka == null ? "" : "if (" + podmienka + ") ") + "goto b" + cieľ_VALUE + ";");
    }
    String metóda_telo_správy(metóda_zdroj funkcia_VALUE, člen_údaje údaje) {
        byte[] telo_správy_údaje = údaje.atribút_VALUE.get("Code"); if (telo_správy_údaje == null) throw new Preklad_Chyba("funkcia_VALUE 몸체가 없음: " + funkcia_VALUE.Názov);
        údaje_Čítačka Čítačka_VALUE = new údaje_Čítačka(telo_správy_údaje); int 쌓임깊이 = Čítačka_VALUE.두바이트(), 지역변수수 = Čítačka_VALUE.두바이트();
        údaje_Čítačka príkaz_údaje = new údaje_Čítačka(Čítačka_VALUE.Čítanie(Čítačka_VALUE.네바이트()));
        if (Čítačka_VALUE.두바이트() != 0) throw new Preklad_Chyba("try/catch/finally 미지원");
        함수형식 formát_VALUE = new 함수형식(funkcia_VALUE.서술); if (지역변수수 < formát_VALUE.Argumenty.size()) throw new Preklad_Chyba("매개변수보다 적은 miestny_Rozsah 변수");
        lekcia_údaje lekcia_VALUE = 클래스들.get(funkcia_VALUE.vlastník_VALUE);
        List<String> Výstup = new ArrayList<>(); Výstup.add(함수원형(funkcia_VALUE) + " {");
        Výstup.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formát_VALUE.Argumenty.size(); 순번++) Výstup.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), vetva_Zoznam = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (príkaz_údaje.Pozícia < príkaz_údaje.údaje.length) {
            int Pozícia = príkaz_údaje.Pozícia, Príkaz = príkaz_údaje.한바이트(); 경계들.add(Pozícia); Výstup.add("b" + Pozícia + ":;");
            if (Príkaz == 0) continue;
            if (Príkaz == 1) Výstup.add("PUSH(0);");
            else if (Príkaz >= 2 && Príkaz <= 8) Výstup.add("PUSH((uint32_t)(" + (Príkaz - 3) + "));");
            else if (Príkaz == 16 || Príkaz == 17) Výstup.add("PUSH((uint32_t)(" + (Príkaz == 16 ? príkaz_údaje.부호한바이트() : príkaz_údaje.부호두바이트()) + "));");
            else if (Príkaz == 18 || Príkaz == 19) Výstup.add("PUSH(" + konštanta_výraz(lekcia_VALUE, Príkaz == 18 ? príkaz_údaje.한바이트() : príkaz_údaje.두바이트()) + ");");
            else if (Príkaz == 21 || Príkaz == 25 || (Príkaz >= 26 && Príkaz <= 29) || (Príkaz >= 42 && Príkaz <= 45)) {
                int INDEX = Príkaz == 21 || Príkaz == 25 ? príkaz_údaje.한바이트() : Príkaz - (Príkaz <= 29 ? 26 : 42);
                skontrolovať_miestny(INDEX, 지역변수수); Výstup.add("PUSH(l[" + INDEX + "]);");
            } else if (Príkaz == 54 || Príkaz == 58 || (Príkaz >= 59 && Príkaz <= 62) || (Príkaz >= 75 && Príkaz <= 78)) {
                int INDEX = Príkaz == 54 || Príkaz == 58 ? príkaz_údaje.한바이트() : Príkaz - (Príkaz <= 62 ? 59 : 75);
                skontrolovať_miestny(INDEX, 지역변수수); Výstup.add("l[" + INDEX + "] = POP();");
            } else if (Príkaz == 46) Výstup.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Príkaz == 79) Výstup.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Príkaz == 87 || Príkaz == 88) Výstup.add(Príkaz == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Príkaz >= 89 && Príkaz <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] poradie_Zoznam = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Príkaz - 89]; 순번++) Výstup.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : poradie_Zoznam[Príkaz - 89].toCharArray()) Výstup.add("PUSH(" + VALUE + ");");
            } else if (Príkaz == 96 || Príkaz == 100 || Príkaz == 104 || Príkaz == 126 || Príkaz == 128 || Príkaz == 130) {
                String operácia_VALUE = Príkaz == 96 ? "+" : Príkaz == 100 ? "-" : Príkaz == 104 ? "*" : Príkaz == 126 ? "&" : Príkaz == 128 ? "|" : "^";
                Výstup.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operácia_VALUE + " (uint32_t)b);");
            } else if (Príkaz == 108 || Príkaz == 112) Výstup.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Príkaz == 112 ? 1 : 0) + "));");
            else if (Príkaz == 116) Výstup.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Príkaz == 120 || Príkaz == 122 || Príkaz == 124) {
                Výstup.add("b = POP(); a = POP();"); Výstup.add("PUSH(" + (Príkaz == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Príkaz == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Príkaz == 132) {
                int INDEX = príkaz_údaje.한바이트(), prírastok_suma = príkaz_údaje.부호한바이트(); skontrolovať_miestny(INDEX, 지역변수수);
                Výstup.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + prírastok_suma + ");");
            } else if (Príkaz >= 145 && Príkaz <= 147) Výstup.add("a = POP(); PUSH((uint32_t)(" + (Príkaz == 145 ? "int8_t" : Príkaz == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Príkaz >= 153 && Príkaz <= 158) {
                Výstup.add("a = POP();"); 분기넣기(Výstup, vetva_Zoznam, Pozícia, príkaz_údaje.부호두바이트(), "(int32_t)a " + 비교들[Príkaz - 153] + " 0");
            } else if (Príkaz >= 159 && Príkaz <= 166) {
                Výstup.add("b = POP(); a = POP();"); 분기넣기(Výstup, vetva_Zoznam, Pozícia, príkaz_údaje.부호두바이트(), Príkaz >= 165 ? "a " + 비교들[Príkaz - 159] + " b" : "(int32_t)a " + 비교들[Príkaz - 159] + " (int32_t)b");
            } else if (Príkaz == 167 || Príkaz == 200) 분기넣기(Výstup, vetva_Zoznam, Pozícia, Príkaz == 167 ? príkaz_údaje.부호두바이트() : príkaz_údaje.네바이트(), null);
            else if (Príkaz == 170 || Príkaz == 171) {
                while (príkaz_údaje.Pozícia % 4 != 0) príkaz_údaje.한바이트();
                int predvolená_hodnota = príkaz_údaje.네바이트(); Výstup.add("a = POP();");
                if (Príkaz == 170) {
                    int 아래 = príkaz_údaje.네바이트(), 위 = príkaz_údaje.네바이트(); long položka_COUNT = (long)위 - 아래 + 1;
                    if (položka_COUNT < 1 || položka_COUNT > (príkaz_údaje.údaje.length - príkaz_údaje.Pozícia) / 4) throw new Preklad_Chyba("switch klip chyba");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Výstup, vetva_Zoznam, Pozícia, príkaz_údaje.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int položka_COUNT = príkaz_údaje.네바이트(), predný_údaje = 0;
                    if (položka_COUNT < 0 || položka_COUNT > (príkaz_údaje.údaje.length - príkaz_údaje.Pozícia) / 8) throw new Preklad_Chyba("switch Veľkosť chyba");
                    for (int 순번 = 0; 순번 < položka_COUNT; 순번++) {
                        int VALUE = príkaz_údaje.네바이트(); if (순번 > 0 && VALUE <= predný_údaje) throw new Preklad_Chyba("switch poradie_VALUE chyba"); predný_údaje = VALUE;
                        분기넣기(Výstup, vetva_Zoznam, Pozícia, príkaz_údaje.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Výstup, vetva_Zoznam, Pozícia, predvolená_hodnota, null);
            } else if (Príkaz == 172 || Príkaz == 176 || Príkaz == 177) Výstup.add("return " + (Príkaz == 177 ? "0" : "POP()") + ";");
            else if (Príkaz == 178 || Príkaz == 179) {
                metóda_zdroj zdroj = lekcia_VALUE.zdroj(príkaz_údaje.두바이트()); if (!필드들.containsKey(zdroj)) throw new Preklad_Chyba("알 수 없는 hodnota_poľa");
                Výstup.add(symbol("init", zdroj.vlastník_VALUE) + "();"); String hodnota_poľa = symbol("field", zdroj.부분들());
                Výstup.add(Príkaz == 178 ? "PUSH(" + hodnota_poľa + ");" : hodnota_poľa + " = POP();");
            } else if (Príkaz == 184) {
                metóda_zdroj zdroj = lekcia_VALUE.zdroj(príkaz_údaje.두바이트()); if (!함수들.containsKey(zdroj)) throw new Preklad_Chyba("알 수 없는 funkcia_VALUE");
                함수형식 호출형식 = new 함수형식(zdroj.서술); int položka_COUNT = 호출형식.Argumenty.size();
                Výstup.add(symbol("init", zdroj.vlastník_VALUE) + "();"); Výstup.add("if(sp < " + položka_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + položka_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < položka_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Výstup.add("a = " + symbol("method", zdroj.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.vrátiť_KR.equals("V")) Výstup.add("PUSH(a);");
            } else if (Príkaz == 182) {
                metóda_zdroj zdroj = lekcia_VALUE.zdroj(príkaz_údaje.두바이트());
                if (zdroj.equals(new metóda_zdroj("java/lang/String", "length", "()I"))) Výstup.add("a = POP(); PUSH(length(a));");
                else if (zdroj.equals(new metóda_zdroj("java/lang/String", "charAt", "(I)C"))) Výstup.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Preklad_Chyba("가상 funkcia_VALUE 호출 미지원");
            } else if (Príkaz == 188) {
                if (príkaz_údaje.한바이트() != 10) throw new Preklad_Chyba("new int[]만 Podpora_VALUE"); Výstup.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Príkaz == 190) Výstup.add("a = POP(); PUSH(length(a));");
            else if (Príkaz == 196) {
                int prípona_VALUE = príkaz_údaje.한바이트(), INDEX = príkaz_údaje.두바이트(); skontrolovať_miestny(INDEX, 지역변수수);
                if (prípona_VALUE == 21 || prípona_VALUE == 25) Výstup.add("PUSH(l[" + INDEX + "]);");
                else if (prípona_VALUE == 54 || prípona_VALUE == 58) Výstup.add("l[" + INDEX + "] = POP();");
                else if (prípona_VALUE == 132) Výstup.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + príkaz_údaje.부호두바이트() + ");");
                else throw new Preklad_Chyba("미지원 wide Príkaz");
            } else if (Príkaz == 198 || Príkaz == 199) {
                Výstup.add("a = POP();"); 분기넣기(Výstup, vetva_Zoznam, Pozícia, príkaz_údaje.부호두바이트(), "a " + (Príkaz == 198 ? "==" : "!=") + " 0");
            } else throw new Preklad_Chyba(funkcia_VALUE.vlastník_VALUE + "." + funkcia_VALUE.Názov + ", Byte_VALUE " + Pozícia + ": 미지원 Príkaz " + Príkaz);
        }
        if (!경계들.containsAll(vetva_Zoznam)) throw new Preklad_Chyba("Príkaz 경계가 아닌 곳으로 vetva");
        Výstup.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Výstup);
    }
    String exportovať_metóda(String odkaz_symbol, String cieľová_hodnota, boolean 진입점여부) {
        int pozičný_index = cieľová_hodnota.lastIndexOf('.'); if (pozičný_index < 0 || !odkaz_symbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Preklad_Chyba("내보내기 Priradiť_VALUE chyba");
        String vlastník_VALUE = cieľová_hodnota.substring(0, pozičný_index).replace('.', '/'), Názov = cieľová_hodnota.substring(pozičný_index + 1); metóda_zdroj výber_VALUE = null;
        for (metóda_zdroj zdroj : 함수들.keySet()) if (zdroj.vlastník_VALUE.equals(vlastník_VALUE) && zdroj.Názov.equals(Názov)) {
            if (výber_VALUE != null) throw new Preklad_Chyba("겹친 내보내기 cieľová_hodnota"); výber_VALUE = zdroj;
        }
        if (výber_VALUE == null || (함수들.get(výber_VALUE).prístup_položka & 0x100) != 0) throw new Preklad_Chyba("내보낼 함수가 없음 또는 native funkcia_VALUE");
        함수형식 formát_VALUE = new 함수형식(výber_VALUE.서술);
        if ((진입점여부 && !formát_VALUE.Argumenty.isEmpty()) || !Arrays.asList("V", "I").contains(formát_VALUE.vrátiť_KR)) throw new Preklad_Chyba("položka_bod_VALUE 또는 C 경계 formát_VALUE chyba");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formát_VALUE.Argumenty.size(); 순번++) {
            if (!formát_VALUE.Argumenty.get(순번).equals("I")) throw new Preklad_Chyba("C 경계는 int 인수만 Podpora_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formát_VALUE.vrátiť_KR.equals("V") ? "void " : "int32_t ") + odkaz_symbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symbol("init", výber_VALUE.vlastník_VALUE) + "(); " + (formát_VALUE.vrátiť_KR.equals("V") ? "" : "return (int32_t)") + symbol("method", výber_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generovať(String položka_bod, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metóda_zdroj, člen_údaje> položka_VALUE : 함수들.entrySet()) {
            metóda_zdroj zdroj = položka_VALUE.getKey(); člen_údaje údaje = položka_VALUE.getValue(); 선언들.add(함수원형(zdroj) + ";");
            if ((údaje.prístup_položka & 0x100) != 0) {
                String Pripojiť = počítač_Azure_Functions_c3a8e64a.get(zdroj.Názov + zdroj.서술);
                if (!zdroj.vlastník_VALUE.equals(počítač_lekcia) || Pripojiť == null) throw new Preklad_Chyba("허용되지 않은 native funkcia_VALUE: " + zdroj.Názov);
                int položka_COUNT = new 함수형식(zdroj.서술).Argumenty.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < položka_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Pripojiť + "(" + (položka_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(položka_COUNT, "word"))) + ");");
                몸체들.add(함수원형(zdroj) + " { return " + Pripojiť + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metóda_telo_správy(zdroj, údaje));
        }
        for (Map.Entry<metóda_zdroj, člen_údaje> položka_VALUE : 필드들.entrySet()) {
            metóda_zdroj zdroj = položka_VALUE.getKey(); byte[] konštanta_VALUE = položka_VALUE.getValue().atribút_VALUE.get("ConstantValue");
            String VALUE = konštanta_VALUE == null ? "0" : konštanta_výraz(클래스들.get(zdroj.vlastník_VALUE), new údaje_Čítačka(konštanta_VALUE).두바이트());
            필드선언들.add("static word " + symbol("field", zdroj.부분들()) + " = " + VALUE + ";");
        }
        for (String Názov : 클래스들.keySet()) {
            String incializovať = symbol("init", Názov), Stav_VALUE = symbol("state", Názov);
            선언들.add("static void " + incializovať + "(void);"); 필드선언들.add("static unsigned " + Stav_VALUE + ";");
            metóda_zdroj zdroj = new metóda_zdroj(Názov, "<clinit>", "()V");
            몸체들.add("static void " + incializovať + "(void) { if(" + Stav_VALUE + ") return; " + Stav_VALUE + " = 1; " + (함수들.containsKey(zdroj) ? symbol("method", zdroj.부분들()) + "(); " : "") + Stav_VALUE + " = 2; }");
        }
        몸체들.add(exportovať_metóda("java_entry", položka_bod, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Priradiť_VALUE : 내보내기목록) {
            int pozičný_index = Priradiť_VALUE.indexOf('='); if (pozičný_index < 1) throw new Preklad_Chyba("내보내기 Priradiť_VALUE chyba");
            String Názov = Priradiť_VALUE.substring(0, pozičný_index); 공개이름.add(Názov); 몸체들.add(exportovať_metóda(Názov, Priradiť_VALUE.substring(pozičný_index + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> položka_VALUE : 문자열들.entrySet()) {
            String Spracovanie_textu = položka_VALUE.getKey(); StringBuilder pole_VALUE = new StringBuilder("static const word " + položka_VALUE.getValue() + "[] = {" + Spracovanie_textu.length());
            for (int 순번 = 0; 순번 < Spracovanie_textu.length(); 순번++) pole_VALUE.append(", ").append((int)Spracovanie_textu.charAt(순번));
            문자열선언들.add(pole_VALUE.append("};").toString());
        }
        String Podpora_VALUE = Files.readString(zdroj_cesta.resolve("CLR_Podpora.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(halda_Word_COUNT));
        return 기계원문한국어화(Podpora_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ZDROJ, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> názov_tabuľka = new HashMap<>();
        for (String riadok : Files.readAllLines(zdroj_cesta.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] párovať_VALUE = riadok.split("\t"); názov_tabuľka.put(párovať_VALUE[0], párovať_VALUE[1]);
        }
        Pattern blok_údajov_výraz = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = blok_údajov_výraz.matcher(ZDROJ); StringBuffer KR = new StringBuffer();
        while (찾개.find()) {
            String Názov = 찾개.group(), 새이름 = Názov;
            if (!Názov.startsWith("//") && !Názov.startsWith("/*") && !Názov.startsWith("\"") && !Názov.startsWith("'") && !공개이름.contains(Názov)) {
                새이름 = názov_tabuľka.getOrDefault(Názov, Názov);
                if (Názov.matches("a[0-9]+")) 새이름 = "Argumenty" + Názov.substring(1);
                if (Názov.matches("b[0-9]+")) 새이름 = "vetva" + Názov.substring(1);
                if (범용표기) {
                    StringBuilder zápis_VALUE = new StringBuilder();
                    for (char znak_VALUE : 새이름.toCharArray()) zápis_VALUE.append(znak_VALUE < 128 ? Character.toString(znak_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)znak_VALUE));
                    새이름 = zápis_VALUE.toString();
                }
            }
            찾개.appendReplacement(KR, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(KR); return KR.toString();
    }
    String X_86_metóda_telo_správy(metóda_zdroj funkcia_VALUE, člen_údaje údaje, Map<String,String> počítač_tabuľka, String cieľová_hodnota) {
        String fixka_VALUE = symbol("method", funkcia_VALUE.부분들());
        List<String> riadok = new ArrayList<>();
        if ((údaje.prístup_položka & 0x100) != 0) {
            String Pripojiť = počítač_tabuľka.get(funkcia_VALUE.Názov + funkcia_VALUE.서술);
            if (!funkcia_VALUE.vlastník_VALUE.equals(cieľová_hodnota.equals("kernel") ? "telefón_VALUE" : "používateľ") || Pripojiť == null) throw new Preklad_Chyba("허용되지 않은 native funkcia_VALUE");
            return ".text\n" + fixka_VALUE + ":\njmp " + Pripojiť;
        }
        byte[] základný_text = údaje.atribút_VALUE.get("Code"); if (základný_text == null) throw new Preklad_Chyba("funkcia_VALUE 몸체가 없음");
        údaje_Čítačka Čítačka_VALUE = new údaje_Čítačka(základný_text); Čítačka_VALUE.두바이트(); int miestny_COUNT = Čítačka_VALUE.두바이트();
        údaje_Čítačka príkaz_údaje = new údaje_Čítačka(Čítačka_VALUE.Čítanie(Čítačka_VALUE.네바이트()));
        if (Čítačka_VALUE.두바이트() != 0) throw new Preklad_Chyba("try/catch/finally 미지원");
        함수형식 formát_VALUE = new 함수형식(funkcia_VALUE.서술); if (miestny_COUNT < formát_VALUE.Argumenty.size()) throw new Preklad_Chyba("매개변수보다 적은 miestny_Rozsah 변수");
        Collections.addAll(riadok,".text",".globl " + fixka_VALUE,".type " + fixka_VALUE + ", @function",fixka_VALUE + ":","pushl %ebp","movl %esp, %ebp","subl $" + miestny_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formát_VALUE.Argumenty.size(); 순번++) Collections.addAll(riadok,"movl " + (8 + 4 * (formát_VALUE.Argumenty.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        lekcia_údaje lekcia_VALUE = 클래스들.get(funkcia_VALUE.vlastník_VALUE); Set<Integer> 경계들 = new HashSet<>(), vetva_Zoznam = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (príkaz_údaje.Pozícia < príkaz_údaje.údaje.length) {
            int Pozícia = príkaz_údaje.Pozícia, Príkaz = príkaz_údaje.한바이트(); String pozičný_index = fixka_VALUE + "_b" + Pozícia;
            riadok.add(pozičný_index + ":"); 경계들.add(Pozícia);
            if (Príkaz == 0) riadok.add("nop");
            else if (Príkaz == 1) riadok.add("pushl $0");
            else if (Príkaz >= 2 && Príkaz <= 8) riadok.add("pushl $" + (Príkaz - 3));
            else if (Príkaz == 16 || Príkaz == 17) riadok.add("pushl $" + (Príkaz == 16 ? príkaz_údaje.부호한바이트() : príkaz_údaje.부호두바이트()));
            else if (Príkaz == 18 || Príkaz == 19) {
                int INDEX = Príkaz == 18 ? príkaz_údaje.한바이트() : príkaz_údaje.두바이트();
                riadok.add("pushl $" + X_86_konštanta(lekcia_VALUE,INDEX));
            } else if (Príkaz == 21 || Príkaz == 25 || (Príkaz >= 26 && Príkaz <= 29) || (Príkaz >= 42 && Príkaz <= 45) || Príkaz == 54 || Príkaz == 58 || (Príkaz >= 59 && Príkaz <= 62) || (Príkaz >= 75 && Príkaz <= 78)) {
                boolean 읽음 = Príkaz < 54; int INDEX = Príkaz == 21 || Príkaz == 25 || Príkaz == 54 || Príkaz == 58 ? príkaz_údaje.한바이트() : Príkaz - (Príkaz <= 29 ? 26 : Príkaz <= 45 ? 42 : Príkaz <= 62 ? 59 : 75);
                skontrolovať_miestny(INDEX,miestny_COUNT); riadok.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Príkaz == 46) Collections.addAll(riadok,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Príkaz == 79) Collections.addAll(riadok,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Príkaz == 87 || Príkaz == 88) riadok.add("addl $" + (Príkaz == 87 ? 4 : 8) + ", %esp");
            else if (Príkaz >= 89 && Príkaz <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] poradie_Zoznam = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Príkaz - 89]; 순번++) riadok.add("popl " + 저장기들[순번]);
                for (int 순번 : poradie_Zoznam[Príkaz - 89]) riadok.add("pushl " + 저장기들[순번]);
            } else if (Príkaz == 96 || Príkaz == 100 || Príkaz == 104 || Príkaz == 126 || Príkaz == 128 || Príkaz == 130) {
                String operácia_VALUE = Príkaz == 96 ? "addl" : Príkaz == 100 ? "subl" : Príkaz == 104 ? "imull" : Príkaz == 126 ? "andl" : Príkaz == 128 ? "orl" : "xorl";
                Collections.addAll(riadok,"popl %ecx","popl %eax",operácia_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Príkaz == 108 || Príkaz == 112) Collections.addAll(riadok,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + pozičný_index + "_divide","cmpl $0x80000000, %eax","jne " + pozičný_index + "_divide","xorl %edx, %edx","jmp " + pozičný_index + "_done",pozičný_index + "_divide:","cltd","idivl %ecx",pozičný_index + "_done:","pushl " + (Príkaz == 108 ? "%eax" : "%edx"));
            else if (Príkaz == 116) riadok.add("negl (%esp)");
            else if (Príkaz == 120 || Príkaz == 122 || Príkaz == 124) Collections.addAll(riadok,"popl %ecx","popl %eax",(Príkaz == 120 ? "sall" : Príkaz == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Príkaz == 132) {
                int INDEX = príkaz_údaje.한바이트(), prírastok_VALUE = príkaz_údaje.부호한바이트(); skontrolovať_miestny(INDEX,miestny_COUNT); riadok.add("addl $" + prírastok_VALUE + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Príkaz >= 145 && Príkaz <= 147) Collections.addAll(riadok,"popl %eax",Príkaz == 145 ? "movsbl %al, %eax" : Príkaz == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Príkaz >= 153 && Príkaz <= 166) {
                if (Príkaz <= 158) Collections.addAll(riadok,"popl %eax","testl %eax, %eax");
                else Collections.addAll(riadok,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int cieľ_VALUE = Pozícia + príkaz_údaje.부호두바이트(); vetva_Zoznam.add(cieľ_VALUE); riadok.add(비교들[Príkaz - (Príkaz <= 158 ? 153 : 159)] + " " + fixka_VALUE + "_b" + cieľ_VALUE);
            } else if (Príkaz == 167 || Príkaz == 200) {
                int cieľ_VALUE = Pozícia + (Príkaz == 167 ? príkaz_údaje.부호두바이트() : príkaz_údaje.네바이트()); vetva_Zoznam.add(cieľ_VALUE); riadok.add("jmp " + fixka_VALUE + "_b" + cieľ_VALUE);
            } else if (Príkaz == 170 || Príkaz == 171) {
                while (príkaz_údaje.Pozícia % 4 != 0) príkaz_údaje.한바이트();
                int predvolená_hodnota = Pozícia + príkaz_údaje.네바이트(); vetva_Zoznam.add(predvolená_hodnota); riadok.add("popl %eax");
                int položka_COUNT, 아래 = 0;
                if (Príkaz == 170) { 아래 = príkaz_údaje.네바이트(); int 위 = príkaz_údaje.네바이트(); long dĺžka_VALUE = (long)위 - 아래 + 1; if (dĺžka_VALUE < 1 || dĺžka_VALUE > (príkaz_údaje.údaje.length - príkaz_údaje.Pozícia) / 4) throw new Preklad_Chyba("switch klip chyba"); položka_COUNT = (int)dĺžka_VALUE; }
                else { položka_COUNT = príkaz_údaje.네바이트(); if (položka_COUNT < 0 || položka_COUNT > (príkaz_údaje.údaje.length - príkaz_údaje.Pozícia) / 8) throw new Preklad_Chyba("switch Veľkosť chyba"); }
                for (int 순번 = 0; 순번 < položka_COUNT; 순번++) {
                    int VALUE = Príkaz == 170 ? 아래 + 순번 : príkaz_údaje.네바이트(), cieľ_VALUE = Pozícia + príkaz_údaje.네바이트(); vetva_Zoznam.add(cieľ_VALUE);
                    Collections.addAll(riadok,"cmpl $" + VALUE + ", %eax","je " + fixka_VALUE + "_b" + cieľ_VALUE);
                }
                riadok.add("jmp " + fixka_VALUE + "_b" + predvolená_hodnota);
            } else if (Príkaz == 172 || Príkaz == 176 || Príkaz == 177) {
                if (Príkaz != 177) riadok.add("popl %eax"); Collections.addAll(riadok,"leave","ret");
            } else if (Príkaz == 178 || Príkaz == 179) {
                metóda_zdroj zdroj = lekcia_VALUE.zdroj(príkaz_údaje.두바이트()); if (!필드들.containsKey(zdroj)) throw new Preklad_Chyba("알 수 없는 hodnota_poľa");
                Collections.addAll(riadok,"call " + symbol("init",zdroj.vlastník_VALUE),(Príkaz == 178 ? "pushl " : "popl ") + symbol("field",zdroj.부분들()));
            } else if (Príkaz == 184) {
                metóda_zdroj zdroj = lekcia_VALUE.zdroj(príkaz_údaje.두바이트()); if (!함수들.containsKey(zdroj)) throw new Preklad_Chyba("알 수 없는 funkcia_VALUE");
                함수형식 호출형식 = new 함수형식(zdroj.서술); Collections.addAll(riadok,"call " + symbol("init",zdroj.vlastník_VALUE),"call " + symbol("method",zdroj.부분들()));
                if (!호출형식.Argumenty.isEmpty()) riadok.add("addl $" + 호출형식.Argumenty.size() * 4 + ", %esp");
                if (!호출형식.vrátiť_KR.equals("V")) riadok.add("pushl %eax");
            } else if (Príkaz == 182) {
                metóda_zdroj zdroj = lekcia_VALUE.zdroj(príkaz_údaje.두바이트());
                if (zdroj.equals(new metóda_zdroj("java/lang/String","length","()I"))) Collections.addAll(riadok,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (zdroj.equals(new metóda_zdroj("java/lang/String","charAt","(I)C"))) Collections.addAll(riadok,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Preklad_Chyba("가상 funkcia_VALUE 호출 미지원");
            } else if (Príkaz == 188) {
                if (príkaz_údaje.한바이트() != 10) throw new Preklad_Chyba("new int[]만 Podpora_VALUE"); Collections.addAll(riadok,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Príkaz == 190) Collections.addAll(riadok,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Príkaz == 196) {
                int prípona_VALUE = príkaz_údaje.한바이트(), INDEX = príkaz_údaje.두바이트(); skontrolovať_miestny(INDEX,miestny_COUNT);
                if (prípona_VALUE == 21 || prípona_VALUE == 25 || prípona_VALUE == 54 || prípona_VALUE == 58) riadok.add((prípona_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (prípona_VALUE == 132) riadok.add("addl $" + príkaz_údaje.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Preklad_Chyba("wide Príkaz 미지원");
            } else if (Príkaz == 198 || Príkaz == 199) {
                int cieľ_VALUE = Pozícia + príkaz_údaje.부호두바이트(); vetva_Zoznam.add(cieľ_VALUE); Collections.addAll(riadok,"popl %eax","testl %eax, %eax",(Príkaz == 198 ? "je " : "jne ") + fixka_VALUE + "_b" + cieľ_VALUE);
            } else throw new Preklad_Chyba("미지원 Príkaz: " + Príkaz);
        }
        if (!경계들.containsAll(vetva_Zoznam)) throw new Preklad_Chyba("Príkaz 경계가 아닌 곳으로 vetva");
        riadok.add(".size " + fixka_VALUE + ", .-" + fixka_VALUE); return String.join("\n",riadok);
    }
    String X_86_konštanta(lekcia_údaje údaje, int INDEX) {
        if (údaje.상수종류[INDEX] == 3) return údaje.konštanta_údaje[INDEX].toString();
        if (údaje.상수종류[INDEX] == 8) return reťazec_symbol(údaje.문자((Integer)údaje.konštanta_údaje[INDEX]));
        throw new Preklad_Chyba("정수와 reťazec_VALUE 상수만 Podpora_VALUE");
    }
    String X_86_zostava(String položka_bod, List<String> 내보냄, String cieľová_hodnota) throws IOException {
        Map<String,String> počítač_tabuľka = new HashMap<>();
        for (String riadok : Files.readAllLines(zdroj_cesta.resolve("_86_počítač_Azure_Functions.tsv"))) { String[] párovať_VALUE = riadok.split("\t"); if (párovať_VALUE[0].equals(cieľová_hodnota)) počítač_tabuľka.put(párovať_VALUE[1] + párovať_VALUE[2],párovať_VALUE[3]); }
        int pozičný_index = položka_bod.lastIndexOf('.'); if (pozičný_index < 0) throw new Preklad_Chyba("položka_bod Priradiť_VALUE chyba");
        String vlastník_VALUE = položka_bod.substring(0,pozičný_index).replace('.','/'), metóda_položka_názov = položka_bod.substring(pozičný_index + 1); metóda_zdroj položka_bod_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metóda_zdroj zdroj = new metóda_zdroj(vlastník_VALUE,metóda_položka_názov,서술); if (함수들.containsKey(zdroj)) { if (položka_bod_VALUE != null) throw new Preklad_Chyba("겹친 položka_bod"); položka_bod_VALUE = zdroj; } }
        if (položka_bod_VALUE == null || (함수들.get(položka_bod_VALUE).prístup_položka & 0x100) != 0) throw new Preklad_Chyba("položka_bod_VALUE funkcia_VALUE formát_VALUE chyba");
        List<String> riadok = new ArrayList<>(); riadok.add(".code32");
        for (lekcia_údaje údaje : 클래스들.values()) {
            String Stav_VALUE = symbol("state",údaje.Názov), incializovať = symbol("init",údaje.Názov);
            Collections.addAll(riadok,".bss",".balign 4",Stav_VALUE + ": .long 0",".text",incializovať + ":","cmpl $0, " + Stav_VALUE,"jne " + incializovať + "_done","movl $1, " + Stav_VALUE);
            metóda_zdroj 초기화참조 = new metóda_zdroj(údaje.Názov,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) riadok.add("call " + symbol("method",초기화참조.부분들()));
            Collections.addAll(riadok,"movl $2, " + Stav_VALUE,incializovať + "_done:","ret");
            for (člen_údaje hodnota_poľa : údaje.hodnota_poľa) {
                byte[] konštanta_VALUE = hodnota_poľa.atribút_VALUE.get("ConstantValue"); String VALUE = konštanta_VALUE == null ? "0" : X_86_konštanta(údaje,new údaje_Čítačka(konštanta_VALUE).두바이트());
                Collections.addAll(riadok,".data",".balign 4",symbol("field",údaje.Názov,hodnota_poľa.Názov,hodnota_poľa.서술) + ": .long " + VALUE);
            }
            for (člen_údaje funkcia_VALUE : údaje.funkcia_VALUE) if (!funkcia_VALUE.Názov.equals("<init>")) riadok.add(X_86_metóda_telo_správy(new metóda_zdroj(údaje.Názov,funkcia_VALUE.Názov,funkcia_VALUE.서술),funkcia_VALUE,počítač_tabuľka,cieľová_hodnota));
        }
        Collections.addAll(riadok,".text",".globl java_entry","java_entry:","call " + symbol("init",položka_bod_VALUE.vlastník_VALUE),"call " + symbol("method",položka_bod_VALUE.부분들()));
        if (položka_bod_VALUE.서술.equals("()V")) riadok.add("xorl %eax, %eax"); riadok.add("ret");
        for (String Priradiť_VALUE : 내보냄) {
            int oddeľovač_VALUE_d8ba4873 = Priradiť_VALUE.indexOf('='); if (oddeľovač_VALUE_d8ba4873 < 1) throw new Preklad_Chyba("내보내기 Priradiť_VALUE chyba");
            String externý_VALUE = Priradiť_VALUE.substring(0,oddeľovač_VALUE_d8ba4873), funkcia_VALUE = Priradiť_VALUE.substring(oddeľovač_VALUE_d8ba4873 + 1); int delenie_KR = funkcia_VALUE.lastIndexOf('.');
            if (delenie_KR < 0 || !externý_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Preklad_Chyba("내보내기 symbol chyba");
            String lekcia_VALUE = funkcia_VALUE.substring(0,delenie_KR).replace('.','/'), Názov = funkcia_VALUE.substring(delenie_KR + 1); metóda_zdroj výber_VALUE = null;
            for (metóda_zdroj zdroj : 함수들.keySet()) if (zdroj.vlastník_VALUE.equals(lekcia_VALUE) && zdroj.Názov.equals(Názov)) { if (výber_VALUE != null) throw new Preklad_Chyba("겹친 내보내기 cieľová_hodnota"); výber_VALUE = zdroj; }
            if (výber_VALUE == null) throw new Preklad_Chyba("내보낼 함수가 없음");
            Collections.addAll(riadok,".text",".globl " + externý_VALUE,externý_VALUE + ":","call " + symbol("init",výber_VALUE.vlastník_VALUE),"jmp " + symbol("method",výber_VALUE.부분들()));
        }
        riadok.add(".section .rodata");
        for (Map.Entry<String,String> položka_VALUE : 문자열들.entrySet()) {
            Collections.addAll(riadok,".balign 4",položka_VALUE.getValue() + ":",".long " + položka_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lekcia_VALUE_7c611f50 : položka_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(lekcia_VALUE_7c611f50)); if (!단위들.isEmpty()) riadok.add(".long " + String.join(",",단위들));
        }
        riadok.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",riadok) + "\n";
    }
    static void Vykonať_nástroj(List<String> Príkaz) throws Exception {
        if (new ProcessBuilder(Príkaz).inheritIO().start().waitFor() != 0) throw new Preklad_Chyba("kompilovať_zdroj chyba: " + Príkaz.get(0));
    }
    static String údaje_reťazec(String Spracovanie_textu) { return "\"" + Spracovanie_textu.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Preklad(List<Path> vstup_Zoznam, String cieľová_hodnota, String položka_bod, List<String> 내보냄, Path Výstup, Path zdroj_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), lekcia_cesta = 임시.resolve("classes"); Files.createDirectory(lekcia_cesta);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",lekcia_cesta.toString(),"-sourcepath",lekcia_cesta.toString(),"-d",lekcia_cesta.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int zdroj_COUNT_5c1457a1 = 0;
            for (Path vstup_VALUE : vstup_Zoznam) {
                if (Výstup.toAbsolutePath().normalize().equals(vstup_VALUE.toAbsolutePath().normalize())) throw new Preklad_Chyba("Výstup 파일과 입력이 같음");
                if (vstup_VALUE.toString().endsWith(".java")) { 자바명령.add(vstup_VALUE.toString()); zdroj_COUNT_5c1457a1++; }
                else if (vstup_VALUE.toString().endsWith(".class")) 바이트코드.add(vstup_VALUE);
                else throw new Preklad_Chyba(".java 또는 .class만 Podpora_VALUE");
            }
            if (zdroj_COUNT_5c1457a1 > 0) Vykonať_nástroj(자바명령);
            try (java.util.stream.Stream<Path> cesta_Zoznam = Files.walk(lekcia_cesta)) { cesta_Zoznam.filter(Cesta -> Cesta.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,cieľová_hodnota.equals("user") ? "user" : "kernel",262144,zdroj_VALUE);
            String skompilovať_VALUE = CONVERT_VALUE.X_86_zostava(položka_bod,내보냄,cieľová_hodnota); Files.writeString(임시.resolve("program.s"),skompilovať_VALUE,StandardCharsets.UTF_8);
            Path nástroj_pozícia = zdroj_VALUE.getParent();
            Vykonať_nástroj(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Vykonať_nástroj(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),nástroj_pozícia.resolve("CLR_Podpora.s").toString()));
            List<String> Pripojiť = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (cieľová_hodnota.equals("kernel")) Pripojiť.add("-r");
            else {
                Vykonať_nástroj(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),nástroj_pozícia.resolve(cieľová_hodnota.equals("user") ? "START_používateľ_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(Pripojiť,"-e","_start",임시.resolve("start.o").toString());
                if (cieľová_hodnota.equals("user")) Collections.addAll(Pripojiť,"-T",nástroj_pozícia.resolve("používateľ_odkaz_Navigácia.ld").toString());
            }
            Collections.addAll(Pripojiť,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Vykonať_nástroj(Pripojiť);
            Výstup = Výstup.toAbsolutePath(); Files.createDirectories(Výstup.getParent()); Path publikovať_VALUE = Files.createTempFile(Výstup.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publikovať_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(publikovať_VALUE,Výstup,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publikovať_VALUE); }
            Files.setPosixFilePermissions(Výstup,java.nio.file.attribute.PosixFilePermissions.fromString(cieľová_hodnota.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Výstup + ".s"),skompilovať_VALUE,StandardCharsets.UTF_8);
            List<String> symbol_údaje = new ArrayList<>(), zdrojové_údaje = new ArrayList<>();
            for (metóda_zdroj zdroj : CONVERT_VALUE.함수들.keySet()) symbol_údaje.add(údaje_reťazec(symbol("method",zdroj.부분들())) + ":" + údaje_reťazec(zdroj.vlastník_VALUE + "." + zdroj.Názov + zdroj.서술));
            for (Path vstup_VALUE : vstup_Zoznam) {
                byte[] hodnota_hash_Súbor = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(vstup_VALUE)); StringBuilder Spracovanie_textu = new StringBuilder(); for (byte VALUE : hodnota_hash_Súbor) Spracovanie_textu.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                zdrojové_údaje.add(údaje_reťazec(vstup_VALUE.toAbsolutePath().toString()) + ":" + údaje_reťazec(Spracovanie_textu.toString()));
            }
            Files.writeString(Paths.get(Výstup + ".json"),"{\"target\":" + údaje_reťazec(cieľová_hodnota) + ",\"entry\":" + údaje_reťazec(položka_bod) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbol_údaje) + "},\"sources\":{" + String.join(",",zdrojové_údaje) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> cesta_Zoznam = Files.walk(임시)) { for (Path Cesta : (Iterable<Path>)cesta_Zoznam.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Cesta); }
        }
    }
    public static void main(String[] Argumenty) {
        try {
            String položka_bod = null, cieľová_hodnota = "kernel", X_86_cieľ = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> cesta_Zoznam = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumenty.length; 순번++) {
                String VALUE = Argumenty[순번];
                switch (VALUE) {
                    case "--target": X_86_cieľ = Argumenty[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry lekcia_VALUE.funkcia_VALUE -o Výstup [--target linux|kernel|user] [--profile kernel|user] [--export symbol=lekcia_VALUE.funkcia_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": položka_bod = Argumenty[++순번]; break;
                    case "--profile": cieľová_hodnota = Argumenty[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumenty[++순번]); break;
                    case "--export": 내보냄.add(Argumenty[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argumenty[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Preklad_Chyba("알 수 없는 옵션: " + VALUE); cesta_Zoznam.add(Paths.get(VALUE));
                }
            }
            if (položka_bod == null || 출력경로 == null || cesta_Zoznam.isEmpty()) throw new Preklad_Chyba("--entry, -o, lekcia_VALUE 파일이 필요합니다");
            Path zdroj_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_cieľ != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_cieľ)) throw new Preklad_Chyba("알 수 없는 Vykonať_príkaz cieľová_hodnota");
                X_86_Preklad(cesta_Zoznam,X_86_cieľ,položka_bod,내보냄,출력경로,zdroj_VALUE); return;
            }
            String ZDROJ = new 기계어미리번역(cesta_Zoznam, cieľová_hodnota, 낱말수, zdroj_VALUE).generovať(položka_bod, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ZDROJ, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception chyba) { System.err.println("kompilovať_zdroj chyba: " + chyba.getMessage()); System.exit(1); }
    }
}
