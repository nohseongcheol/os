// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Clasă_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. gazdă JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Traducere_eroare extends RuntimeException {
        Traducere_eroare(String 설명) { super(설명); }
    }
    static final class date_Reader {
        final byte[] date;
        int Poziție;
        date_Reader(byte[] 입력자료) { date = 입력자료; }
        byte[] Citire(int lungime_VALUE) {
            if (lungime_VALUE < 0 || lungime_VALUE > date.length - Poziție) throw new Traducere_eroare("잘린 Clasă_VALUE 또는 Comandă date");
            byte[] KR = Arrays.copyOfRange(date, Poziție, Poziție + lungime_VALUE); Poziție += lungime_VALUE; return KR;
        }
        int 한바이트() { if (Poziție >= date.length) throw new Traducere_eroare("잘린 Comandă date"); return date[Poziție++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class membru_date {
        final int acces_intrare;
        final String Nume, 서술;
        final Map<String, byte[]> atribut_VALUE;
        membru_date(int acces_VALUE, String nume_VALUE, String 서술값, Map<String, byte[]> atribut_date) {
            acces_intrare = acces_VALUE; Nume = nume_VALUE; 서술 = 서술값; atribut_VALUE = atribut_date;
        }
    }
    static final class metodă_referință implements Comparable<metodă_referință> {
        final String proprietar_VALUE, Nume, 서술;
        metodă_referință(String 소유값, String nume_VALUE, String 서술값) { proprietar_VALUE = 소유값; Nume = nume_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{proprietar_VALUE, Nume, 서술}; }
        public int compareTo(metodă_referință pereche_VALUE) {
            int Comparație_VALUE = proprietar_VALUE.compareTo(pereche_VALUE.proprietar_VALUE);
            if (Comparație_VALUE == 0) Comparație_VALUE = Nume.compareTo(pereche_VALUE.Nume);
            return Comparație_VALUE == 0 ? 서술.compareTo(pereche_VALUE.서술) : Comparație_VALUE;
        }
        public boolean equals(Object pereche_VALUE) { return pereche_VALUE instanceof metodă_referință && compareTo((metodă_referință) pereche_VALUE) == 0; }
        public int hashCode() { return Objects.hash(proprietar_VALUE, Nume, 서술); }
    }
    static final class Clasă_date {
        final int[] 상수종류;
        final Object[] constantă_date;
        final String Nume;
        final List<membru_date> valoare_câmp, funcție_VALUE;
        Clasă_date(Path Cale) throws IOException {
            date_Reader Reader_VALUE = new date_Reader(Files.readAllBytes(Cale));
            if (Reader_VALUE.네바이트() != 0xcafebabe) throw new Traducere_eroare("Java Clasă_VALUE 표식이 아님");
            Reader_VALUE.Citire(4);
            int element_COUNT = Reader_VALUE.두바이트(); 상수종류 = new int[element_COUNT]; constantă_date = new Object[element_COUNT];
            for (int 순번 = 1; 순번 < element_COUNT; 순번++) {
                int 종류 = Reader_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int lungime_VALUE = Reader_VALUE.두바이트();
                        byte[] caracter_tampon = Reader_VALUE.Citire(lungime_VALUE), 길이붙인자료 = new byte[lungime_VALUE + 2];
                        길이붙인자료[0] = (byte)(lungime_VALUE >> 8); 길이붙인자료[1] = (byte)lungime_VALUE;
                        System.arraycopy(caracter_tampon, 0, 길이붙인자료, 2, lungime_VALUE);
                        constantă_date[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: constantă_date[순번] = Reader_VALUE.네바이트(); break;
                    case 4: Reader_VALUE.Citire(4); break;
                    case 5: case 6: Reader_VALUE.Citire(8); 순번++; break;
                    case 7: case 8: case 16: constantă_date[순번] = Reader_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        constantă_date[순번] = new int[]{Reader_VALUE.두바이트(), Reader_VALUE.두바이트()}; break;
                    case 15: constantă_date[순번] = new int[]{Reader_VALUE.한바이트(), Reader_VALUE.두바이트()}; break;
                    default: throw new Traducere_eroare("지원하지 않는 constantă_VALUE 종류: " + 종류);
                }
            }
            Reader_VALUE.두바이트(); Nume = nume_de_clasă(Reader_VALUE.두바이트());
            if (!nume_de_clasă(Reader_VALUE.두바이트()).equals("java/lang/Object") || Reader_VALUE.두바이트() != 0)
                throw new Traducere_eroare(Nume + ": 상속 및 인터페이스 미지원");
            valoare_câmp = 멤버읽기(Reader_VALUE); funcție_VALUE = 멤버읽기(Reader_VALUE); 속성읽기(Reader_VALUE);
            if (Reader_VALUE.Poziție != Reader_VALUE.date.length) throw new Traducere_eroare("Clasă_VALUE 뒤에 남은 date");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Traducere_eroare("문자 constantă_VALUE INDEX eroare");
            return (String) constantă_date[INDEX];
        }
        String nume_de_clasă(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Traducere_eroare("Clasă_VALUE referință eroare");
            return 문자((Integer)constantă_date[INDEX]);
        }
        metodă_referință referință(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Traducere_eroare("멤버 referință eroare");
            int[] asocia_VALUE = (int[])constantă_date[INDEX], nume_asocia = (int[])constantă_date[asocia_VALUE[1]];
            return new metodă_referință(nume_de_clasă(asocia_VALUE[0]), 문자(nume_asocia[0]), 문자(nume_asocia[1]));
        }
        Map<String, byte[]> 속성읽기(date_Reader Reader_VALUE) {
            Map<String, byte[]> KR = new LinkedHashMap<>();
            int element_COUNT = Reader_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                String atribut_nume = 문자(Reader_VALUE.두바이트()); byte[] VALUE = Reader_VALUE.Citire(Reader_VALUE.네바이트());
                if (KR.put(atribut_nume, VALUE) != null) throw new Traducere_eroare("겹친 atribut_VALUE: " + atribut_nume);
            }
            return KR;
        }
        List<membru_date> 멤버읽기(date_Reader Reader_VALUE) {
            List<membru_date> KR = new ArrayList<>(); int element_COUNT = Reader_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                int acces_intrare = Reader_VALUE.두바이트(); String metodă_intrare_nume = 문자(Reader_VALUE.두바이트()), 서술 = 문자(Reader_VALUE.두바이트());
                KR.add(new membru_date(acces_intrare, metodă_intrare_nume, 서술, 속성읽기(Reader_VALUE)));
            }
            return KR;
        }
    }
    static final class 함수형식 {
        final List<String> Argumente = new ArrayList<>();
        final String restitui_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Traducere_eroare("funcție_VALUE 서술 eroare: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Traducere_eroare("funcție_VALUE 서술 eroare: " + 서술);
            Argumente.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumente.contains("V") || 반환들.size() != 1) throw new Traducere_eroare("funcție_VALUE 서술 eroare: " + 서술);
            restitui_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> KR = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Poziție = 0; Poziție < 서술.length();) {
            String selecție_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, Poziție)) { selecție_VALUE = format_VALUE; break; }
            if (selecție_VALUE == null) throw new Traducere_eroare("지원하지 않는 tip_de_date: " + 서술);
            KR.add(selecție_VALUE); Poziție += selecție_VALUE.length();
        }
        return KR;
    }
    static String simbol(String 종류, String... 부분들) {
        try {
            byte[] cod_hash_Fișier = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", cod_hash_Fișier[순번] & 255));
            return SMS.toString();
        } catch (Exception eroare) { throw new Traducere_eroare(eroare.toString()); }
    }
    final Map<String, Clasă_date> 클래스들 = new TreeMap<>();
    final Map<metodă_referință, membru_date> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), mașină_Functions_c3a8e64a = new LinkedHashMap<>();
    final String executare_țintă, mașină_Clasă;
    final int 동적기억낱말수;
    final Path resursă_cale;
    기계어미리번역(List<Path> cale_Listă, String țintă, int 낱말수, Path resursă_VALUE) throws IOException {
        if ((!țintă.equals("kernel") && !țintă.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Traducere_eroare("executa_comandă țintă 또는 Memorie_VALUE adresa_regiune Mărime eroare");
        executare_țintă = țintă; 동적기억낱말수 = 낱말수; resursă_cale = resursă_VALUE;
        // 이 이름도 국가별 sursă_arborescență genera 시 해당 언어로 옮긴다.
        mașină_Clasă = țintă.equals("kernel") ? "Avizier" : "utilizator";
        for (String Linie : Files.readAllLines(resursă_VALUE.resolve("mașină_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Linie.split("\t", -1);
            if (부분들.length != 4) throw new Traducere_eroare("mașină funcție_VALUE date eroare");
            if (부분들[0].equals(țintă)) mașină_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Cale : cale_Listă) {
            Clasă_date date = new Clasă_date(Cale);
            if (클래스들.put(date.Nume, date) != null) throw new Traducere_eroare("중복 Clasă_VALUE: " + date.Nume);
            for (membru_date valoare_câmp : date.valoare_câmp) {
                if ((valoare_câmp.acces_intrare & 8) == 0 || 형식읽기(valoare_câmp.서술).equals(Collections.singletonList("V"))) throw new Traducere_eroare("정적 필드만 suport_VALUE");
                if (필드들.put(new metodă_referință(date.Nume, valoare_câmp.Nume, valoare_câmp.서술), valoare_câmp) != null) throw new Traducere_eroare("중복 valoare_câmp");
            }
            for (membru_date funcție_VALUE : date.funcție_VALUE) {
                if (funcție_VALUE.Nume.equals("<init>")) continue;
                if ((funcție_VALUE.acces_intrare & 8) == 0 || (funcție_VALUE.acces_intrare & (0x20 | 0x400)) != 0) throw new Traducere_eroare("정적 비동기화 함수만 suport_VALUE");
                new 함수형식(funcție_VALUE.서술);
                if (함수들.put(new metodă_referință(date.Nume, funcție_VALUE.Nume, funcție_VALUE.서술), funcție_VALUE) != null) throw new Traducere_eroare("중복 funcție_VALUE");
            }
        }
    }
    String șir_simbol(String SMS) { return 문자열들.computeIfAbsent(SMS, VALUE -> "j_text_" + 문자열들.size()); }
    String constantă_expresie(Clasă_date date, int INDEX) {
        if (INDEX < 1 || INDEX >= date.상수종류.length) throw new Traducere_eroare("constantă_VALUE INDEX clip eroare");
        if (date.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + date.constantă_date[INDEX] + ")";
        if (date.상수종류[INDEX] == 8) return "(word)" + șir_simbol(date.문자((Integer)date.constantă_date[INDEX]));
        throw new Traducere_eroare("정수와 șir_VALUE 상수만 suport_VALUE");
    }
    String 함수원형(metodă_referință referință) {
        List<String> 인수들 = new ArrayList<>(); int element_COUNT = new 함수형식(referință.서술).Argumente.size();
        for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbol("method", referință.부분들()) + "(" + (element_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void verifica_local(int INDEX, int local_variabilă_COUNT) { if (INDEX < 0 || INDEX >= local_variabilă_COUNT) throw new Traducere_eroare("local_gamă variabilă_VALUE INDEX clip eroare"); }
    void 분기넣기(List<String> Rezultat, Set<Integer> ramură_Listă, int Poziție, int 이동량, String condiție) {
        int destinație_VALUE = Poziție + 이동량; ramură_Listă.add(destinație_VALUE);
        Rezultat.add((condiție == null ? "" : "if (" + condiție + ") ") + "goto b" + destinație_VALUE + ";");
    }
    String metodă_corp(metodă_referință funcție_VALUE, membru_date date) {
        byte[] corp_date = date.atribut_VALUE.get("Code"); if (corp_date == null) throw new Traducere_eroare("funcție_VALUE 몸체가 없음: " + funcție_VALUE.Nume);
        date_Reader Reader_VALUE = new date_Reader(corp_date); int 쌓임깊이 = Reader_VALUE.두바이트(), local_variabilă_COUNT = Reader_VALUE.두바이트();
        date_Reader comandă_date = new date_Reader(Reader_VALUE.Citire(Reader_VALUE.네바이트()));
        if (Reader_VALUE.두바이트() != 0) throw new Traducere_eroare("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(funcție_VALUE.서술); if (local_variabilă_COUNT < format_VALUE.Argumente.size()) throw new Traducere_eroare("매개변수보다 적은 local_gamă variabilă_VALUE");
        Clasă_date Clasă_VALUE = 클래스들.get(funcție_VALUE.proprietar_VALUE);
        List<String> Rezultat = new ArrayList<>(); Rezultat.add(함수원형(funcție_VALUE) + " {");
        Rezultat.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(local_variabilă_COUNT, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.Argumente.size(); 순번++) Rezultat.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ramură_Listă = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (comandă_date.Poziție < comandă_date.date.length) {
            int Poziție = comandă_date.Poziție, Comandă = comandă_date.한바이트(); 경계들.add(Poziție); Rezultat.add("b" + Poziție + ":;");
            if (Comandă == 0) continue;
            if (Comandă == 1) Rezultat.add("PUSH(0);");
            else if (Comandă >= 2 && Comandă <= 8) Rezultat.add("PUSH((uint32_t)(" + (Comandă - 3) + "));");
            else if (Comandă == 16 || Comandă == 17) Rezultat.add("PUSH((uint32_t)(" + (Comandă == 16 ? comandă_date.부호한바이트() : comandă_date.부호두바이트()) + "));");
            else if (Comandă == 18 || Comandă == 19) Rezultat.add("PUSH(" + constantă_expresie(Clasă_VALUE, Comandă == 18 ? comandă_date.한바이트() : comandă_date.두바이트()) + ");");
            else if (Comandă == 21 || Comandă == 25 || (Comandă >= 26 && Comandă <= 29) || (Comandă >= 42 && Comandă <= 45)) {
                int INDEX = Comandă == 21 || Comandă == 25 ? comandă_date.한바이트() : Comandă - (Comandă <= 29 ? 26 : 42);
                verifica_local(INDEX, local_variabilă_COUNT); Rezultat.add("PUSH(l[" + INDEX + "]);");
            } else if (Comandă == 54 || Comandă == 58 || (Comandă >= 59 && Comandă <= 62) || (Comandă >= 75 && Comandă <= 78)) {
                int INDEX = Comandă == 54 || Comandă == 58 ? comandă_date.한바이트() : Comandă - (Comandă <= 62 ? 59 : 75);
                verifica_local(INDEX, local_variabilă_COUNT); Rezultat.add("l[" + INDEX + "] = POP();");
            } else if (Comandă == 46) Rezultat.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Comandă == 79) Rezultat.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Comandă == 87 || Comandă == 88) Rezultat.add(Comandă == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Comandă >= 89 && Comandă <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ordine_Listă = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Comandă - 89]; 순번++) Rezultat.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : ordine_Listă[Comandă - 89].toCharArray()) Rezultat.add("PUSH(" + VALUE + ");");
            } else if (Comandă == 96 || Comandă == 100 || Comandă == 104 || Comandă == 126 || Comandă == 128 || Comandă == 130) {
                String operație_VALUE = Comandă == 96 ? "+" : Comandă == 100 ? "-" : Comandă == 104 ? "*" : Comandă == 126 ? "&" : Comandă == 128 ? "|" : "^";
                Rezultat.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operație_VALUE + " (uint32_t)b);");
            } else if (Comandă == 108 || Comandă == 112) Rezultat.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Comandă == 112 ? 1 : 0) + "));");
            else if (Comandă == 116) Rezultat.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Comandă == 120 || Comandă == 122 || Comandă == 124) {
                Rezultat.add("b = POP(); a = POP();"); Rezultat.add("PUSH(" + (Comandă == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Comandă == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Comandă == 132) {
                int INDEX = comandă_date.한바이트(), increment_sumă = comandă_date.부호한바이트(); verifica_local(INDEX, local_variabilă_COUNT);
                Rezultat.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + increment_sumă + ");");
            } else if (Comandă >= 145 && Comandă <= 147) Rezultat.add("a = POP(); PUSH((uint32_t)(" + (Comandă == 145 ? "int8_t" : Comandă == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Comandă >= 153 && Comandă <= 158) {
                Rezultat.add("a = POP();"); 분기넣기(Rezultat, ramură_Listă, Poziție, comandă_date.부호두바이트(), "(int32_t)a " + 비교들[Comandă - 153] + " 0");
            } else if (Comandă >= 159 && Comandă <= 166) {
                Rezultat.add("b = POP(); a = POP();"); 분기넣기(Rezultat, ramură_Listă, Poziție, comandă_date.부호두바이트(), Comandă >= 165 ? "a " + 비교들[Comandă - 159] + " b" : "(int32_t)a " + 비교들[Comandă - 159] + " (int32_t)b");
            } else if (Comandă == 167 || Comandă == 200) 분기넣기(Rezultat, ramură_Listă, Poziție, Comandă == 167 ? comandă_date.부호두바이트() : comandă_date.네바이트(), null);
            else if (Comandă == 170 || Comandă == 171) {
                while (comandă_date.Poziție % 4 != 0) comandă_date.한바이트();
                int valoare_implicită = comandă_date.네바이트(); Rezultat.add("a = POP();");
                if (Comandă == 170) {
                    int 아래 = comandă_date.네바이트(), 위 = comandă_date.네바이트(); long element_COUNT = (long)위 - 아래 + 1;
                    if (element_COUNT < 1 || element_COUNT > (comandă_date.date.length - comandă_date.Poziție) / 4) throw new Traducere_eroare("switch clip eroare");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Rezultat, ramură_Listă, Poziție, comandă_date.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int element_COUNT = comandă_date.네바이트(), frontală_date = 0;
                    if (element_COUNT < 0 || element_COUNT > (comandă_date.date.length - comandă_date.Poziție) / 8) throw new Traducere_eroare("switch Mărime eroare");
                    for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                        int VALUE = comandă_date.네바이트(); if (순번 > 0 && VALUE <= frontală_date) throw new Traducere_eroare("switch ordine_VALUE eroare"); frontală_date = VALUE;
                        분기넣기(Rezultat, ramură_Listă, Poziție, comandă_date.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Rezultat, ramură_Listă, Poziție, valoare_implicită, null);
            } else if (Comandă == 172 || Comandă == 176 || Comandă == 177) Rezultat.add("return " + (Comandă == 177 ? "0" : "POP()") + ";");
            else if (Comandă == 178 || Comandă == 179) {
                metodă_referință referință = Clasă_VALUE.referință(comandă_date.두바이트()); if (!필드들.containsKey(referință)) throw new Traducere_eroare("알 수 없는 valoare_câmp");
                Rezultat.add(simbol("init", referință.proprietar_VALUE) + "();"); String valoare_câmp = simbol("field", referință.부분들());
                Rezultat.add(Comandă == 178 ? "PUSH(" + valoare_câmp + ");" : valoare_câmp + " = POP();");
            } else if (Comandă == 184) {
                metodă_referință referință = Clasă_VALUE.referință(comandă_date.두바이트()); if (!함수들.containsKey(referință)) throw new Traducere_eroare("알 수 없는 funcție_VALUE");
                함수형식 호출형식 = new 함수형식(referință.서술); int element_COUNT = 호출형식.Argumente.size();
                Rezultat.add(simbol("init", referință.proprietar_VALUE) + "();"); Rezultat.add("if(sp < " + element_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + element_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < element_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Rezultat.add("a = " + simbol("method", referință.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.restitui_KR.equals("V")) Rezultat.add("PUSH(a);");
            } else if (Comandă == 182) {
                metodă_referință referință = Clasă_VALUE.referință(comandă_date.두바이트());
                if (referință.equals(new metodă_referință("java/lang/String", "length", "()I"))) Rezultat.add("a = POP(); PUSH(length(a));");
                else if (referință.equals(new metodă_referință("java/lang/String", "charAt", "(I)C"))) Rezultat.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Traducere_eroare("가상 funcție_VALUE 호출 미지원");
            } else if (Comandă == 188) {
                if (comandă_date.한바이트() != 10) throw new Traducere_eroare("new int[]만 suport_VALUE"); Rezultat.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Comandă == 190) Rezultat.add("a = POP(); PUSH(length(a));");
            else if (Comandă == 196) {
                int extensie_VALUE = comandă_date.한바이트(), INDEX = comandă_date.두바이트(); verifica_local(INDEX, local_variabilă_COUNT);
                if (extensie_VALUE == 21 || extensie_VALUE == 25) Rezultat.add("PUSH(l[" + INDEX + "]);");
                else if (extensie_VALUE == 54 || extensie_VALUE == 58) Rezultat.add("l[" + INDEX + "] = POP();");
                else if (extensie_VALUE == 132) Rezultat.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + comandă_date.부호두바이트() + ");");
                else throw new Traducere_eroare("미지원 wide Comandă");
            } else if (Comandă == 198 || Comandă == 199) {
                Rezultat.add("a = POP();"); 분기넣기(Rezultat, ramură_Listă, Poziție, comandă_date.부호두바이트(), "a " + (Comandă == 198 ? "==" : "!=") + " 0");
            } else throw new Traducere_eroare(funcție_VALUE.proprietar_VALUE + "." + funcție_VALUE.Nume + ", byte_VALUE " + Poziție + ": 미지원 Comandă " + Comandă);
        }
        if (!경계들.containsAll(ramură_Listă)) throw new Traducere_eroare("Comandă 경계가 아닌 곳으로 ramură");
        Rezultat.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Rezultat);
    }
    String exporta_metodă(String Link_simbol, String țintă, boolean 진입점여부) {
        int index_de_poziție = țintă.lastIndexOf('.'); if (index_de_poziție < 0 || !Link_simbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Traducere_eroare("내보내기 atribui_VALUE eroare");
        String proprietar_VALUE = țintă.substring(0, index_de_poziție).replace('.', '/'), Nume = țintă.substring(index_de_poziție + 1); metodă_referință selecție_VALUE = null;
        for (metodă_referință referință : 함수들.keySet()) if (referință.proprietar_VALUE.equals(proprietar_VALUE) && referință.Nume.equals(Nume)) {
            if (selecție_VALUE != null) throw new Traducere_eroare("겹친 내보내기 țintă"); selecție_VALUE = referință;
        }
        if (selecție_VALUE == null || (함수들.get(selecție_VALUE).acces_intrare & 0x100) != 0) throw new Traducere_eroare("내보낼 함수가 없음 또는 native funcție_VALUE");
        함수형식 format_VALUE = new 함수형식(selecție_VALUE.서술);
        if ((진입점여부 && !format_VALUE.Argumente.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.restitui_KR)) throw new Traducere_eroare("intrare_p_VALUE 또는 C 경계 format_VALUE eroare");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.Argumente.size(); 순번++) {
            if (!format_VALUE.Argumente.get(순번).equals("I")) throw new Traducere_eroare("C 경계는 int 인수만 suport_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.restitui_KR.equals("V") ? "void " : "int32_t ") + Link_simbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbol("init", selecție_VALUE.proprietar_VALUE) + "(); " + (format_VALUE.restitui_KR.equals("V") ? "" : "return (int32_t)") + simbol("method", selecție_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String genera(String intrare_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metodă_referință, membru_date> intrare_VALUE : 함수들.entrySet()) {
            metodă_referință referință = intrare_VALUE.getKey(); membru_date date = intrare_VALUE.getValue(); 선언들.add(함수원형(referință) + ";");
            if ((date.acces_intrare & 0x100) != 0) {
                String Conectează = mașină_Functions_c3a8e64a.get(referință.Nume + referință.서술);
                if (!referință.proprietar_VALUE.equals(mașină_Clasă) || Conectează == null) throw new Traducere_eroare("허용되지 않은 native funcție_VALUE: " + referință.Nume);
                int element_COUNT = new 함수형식(referință.서술).Argumente.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Conectează + "(" + (element_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(element_COUNT, "word"))) + ");");
                몸체들.add(함수원형(referință) + " { return " + Conectează + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metodă_corp(referință, date));
        }
        for (Map.Entry<metodă_referință, membru_date> intrare_VALUE : 필드들.entrySet()) {
            metodă_referință referință = intrare_VALUE.getKey(); byte[] constantă_VALUE = intrare_VALUE.getValue().atribut_VALUE.get("ConstantValue");
            String VALUE = constantă_VALUE == null ? "0" : constantă_expresie(클래스들.get(referință.proprietar_VALUE), new date_Reader(constantă_VALUE).두바이트());
            필드선언들.add("static word " + simbol("field", referință.부분들()) + " = " + VALUE + ";");
        }
        for (String Nume : 클래스들.keySet()) {
            String 초기화 = simbol("init", Nume), Stare_VALUE = simbol("state", Nume);
            선언들.add("static void " + 초기화 + "(void);"); 필드선언들.add("static unsigned " + Stare_VALUE + ";");
            metodă_referință referință = new metodă_referință(Nume, "<clinit>", "()V");
            몸체들.add("static void " + 초기화 + "(void) { if(" + Stare_VALUE + ") return; " + Stare_VALUE + " = 1; " + (함수들.containsKey(referință) ? simbol("method", referință.부분들()) + "(); " : "") + Stare_VALUE + " = 2; }");
        }
        몸체들.add(exporta_metodă("java_entry", intrare_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String atribui_VALUE : 내보내기목록) {
            int index_de_poziție = atribui_VALUE.indexOf('='); if (index_de_poziție < 1) throw new Traducere_eroare("내보내기 atribui_VALUE eroare");
            String Nume = atribui_VALUE.substring(0, index_de_poziție); 공개이름.add(Nume); 몸체들.add(exporta_metodă(Nume, atribui_VALUE.substring(index_de_poziție + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> intrare_VALUE : 문자열들.entrySet()) {
            String SMS = intrare_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + intrare_VALUE.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) ARRAY_VALUE.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String suport_VALUE = Files.readString(resursă_cale.resolve("CLR_suport.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(suport_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String SURSĂ, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nume_tabel = new HashMap<>();
        for (String Linie : Files.readAllLines(resursă_cale.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] asocia_VALUE = Linie.split("\t"); nume_tabel.put(asocia_VALUE[0], asocia_VALUE[1]);
        }
        Pattern bloc_expresie = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = bloc_expresie.matcher(SURSĂ); StringBuffer KR = new StringBuffer();
        while (찾개.find()) {
            String Nume = 찾개.group(), 새이름 = Nume;
            if (!Nume.startsWith("//") && !Nume.startsWith("/*") && !Nume.startsWith("\"") && !Nume.startsWith("'") && !공개이름.contains(Nume)) {
                새이름 = nume_tabel.getOrDefault(Nume, Nume);
                if (Nume.matches("a[0-9]+")) 새이름 = "Argumente" + Nume.substring(1);
                if (Nume.matches("b[0-9]+")) 새이름 = "ramură" + Nume.substring(1);
                if (범용표기) {
                    StringBuilder notație_VALUE = new StringBuilder();
                    for (char caracter_VALUE : 새이름.toCharArray()) notație_VALUE.append(caracter_VALUE < 128 ? Character.toString(caracter_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)caracter_VALUE));
                    새이름 = notație_VALUE.toString();
                }
            }
            찾개.appendReplacement(KR, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(KR); return KR.toString();
    }
    String X_86_metodă_corp(metodă_referință funcție_VALUE, membru_date date, Map<String,String> mașină_tabel, String țintă) {
        String marcaj_VALUE = simbol("method", funcție_VALUE.부분들());
        List<String> Linie = new ArrayList<>();
        if ((date.acces_intrare & 0x100) != 0) {
            String Conectează = mașină_tabel.get(funcție_VALUE.Nume + funcție_VALUE.서술);
            if (!funcție_VALUE.proprietar_VALUE.equals(țintă.equals("kernel") ? "mobil_VALUE" : "utilizator") || Conectează == null) throw new Traducere_eroare("허용되지 않은 native funcție_VALUE");
            return ".text\n" + marcaj_VALUE + ":\njmp " + Conectează;
        }
        byte[] text_corp = date.atribut_VALUE.get("Code"); if (text_corp == null) throw new Traducere_eroare("funcție_VALUE 몸체가 없음");
        date_Reader Reader_VALUE = new date_Reader(text_corp); Reader_VALUE.두바이트(); int local_COUNT = Reader_VALUE.두바이트();
        date_Reader comandă_date = new date_Reader(Reader_VALUE.Citire(Reader_VALUE.네바이트()));
        if (Reader_VALUE.두바이트() != 0) throw new Traducere_eroare("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(funcție_VALUE.서술); if (local_COUNT < format_VALUE.Argumente.size()) throw new Traducere_eroare("매개변수보다 적은 local_gamă variabilă_VALUE");
        Collections.addAll(Linie,".text",".globl " + marcaj_VALUE,".type " + marcaj_VALUE + ", @function",marcaj_VALUE + ":","pushl %ebp","movl %esp, %ebp","subl $" + local_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.Argumente.size(); 순번++) Collections.addAll(Linie,"movl " + (8 + 4 * (format_VALUE.Argumente.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Clasă_date Clasă_VALUE = 클래스들.get(funcție_VALUE.proprietar_VALUE); Set<Integer> 경계들 = new HashSet<>(), ramură_Listă = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (comandă_date.Poziție < comandă_date.date.length) {
            int Poziție = comandă_date.Poziție, Comandă = comandă_date.한바이트(); String index_de_poziție = marcaj_VALUE + "_b" + Poziție;
            Linie.add(index_de_poziție + ":"); 경계들.add(Poziție);
            if (Comandă == 0) Linie.add("nop");
            else if (Comandă == 1) Linie.add("pushl $0");
            else if (Comandă >= 2 && Comandă <= 8) Linie.add("pushl $" + (Comandă - 3));
            else if (Comandă == 16 || Comandă == 17) Linie.add("pushl $" + (Comandă == 16 ? comandă_date.부호한바이트() : comandă_date.부호두바이트()));
            else if (Comandă == 18 || Comandă == 19) {
                int INDEX = Comandă == 18 ? comandă_date.한바이트() : comandă_date.두바이트();
                Linie.add("pushl $" + X_86_constantă(Clasă_VALUE,INDEX));
            } else if (Comandă == 21 || Comandă == 25 || (Comandă >= 26 && Comandă <= 29) || (Comandă >= 42 && Comandă <= 45) || Comandă == 54 || Comandă == 58 || (Comandă >= 59 && Comandă <= 62) || (Comandă >= 75 && Comandă <= 78)) {
                boolean 읽음 = Comandă < 54; int INDEX = Comandă == 21 || Comandă == 25 || Comandă == 54 || Comandă == 58 ? comandă_date.한바이트() : Comandă - (Comandă <= 29 ? 26 : Comandă <= 45 ? 42 : Comandă <= 62 ? 59 : 75);
                verifica_local(INDEX,local_COUNT); Linie.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Comandă == 46) Collections.addAll(Linie,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Comandă == 79) Collections.addAll(Linie,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Comandă == 87 || Comandă == 88) Linie.add("addl $" + (Comandă == 87 ? 4 : 8) + ", %esp");
            else if (Comandă >= 89 && Comandă <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ordine_Listă = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Comandă - 89]; 순번++) Linie.add("popl " + 저장기들[순번]);
                for (int 순번 : ordine_Listă[Comandă - 89]) Linie.add("pushl " + 저장기들[순번]);
            } else if (Comandă == 96 || Comandă == 100 || Comandă == 104 || Comandă == 126 || Comandă == 128 || Comandă == 130) {
                String operație_VALUE = Comandă == 96 ? "addl" : Comandă == 100 ? "subl" : Comandă == 104 ? "imull" : Comandă == 126 ? "andl" : Comandă == 128 ? "orl" : "xorl";
                Collections.addAll(Linie,"popl %ecx","popl %eax",operație_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Comandă == 108 || Comandă == 112) Collections.addAll(Linie,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + index_de_poziție + "_divide","cmpl $0x80000000, %eax","jne " + index_de_poziție + "_divide","xorl %edx, %edx","jmp " + index_de_poziție + "_done",index_de_poziție + "_divide:","cltd","idivl %ecx",index_de_poziție + "_done:","pushl " + (Comandă == 108 ? "%eax" : "%edx"));
            else if (Comandă == 116) Linie.add("negl (%esp)");
            else if (Comandă == 120 || Comandă == 122 || Comandă == 124) Collections.addAll(Linie,"popl %ecx","popl %eax",(Comandă == 120 ? "sall" : Comandă == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Comandă == 132) {
                int INDEX = comandă_date.한바이트(), increment_VALUE = comandă_date.부호한바이트(); verifica_local(INDEX,local_COUNT); Linie.add("addl $" + increment_VALUE + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Comandă >= 145 && Comandă <= 147) Collections.addAll(Linie,"popl %eax",Comandă == 145 ? "movsbl %al, %eax" : Comandă == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Comandă >= 153 && Comandă <= 166) {
                if (Comandă <= 158) Collections.addAll(Linie,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Linie,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int destinație_VALUE = Poziție + comandă_date.부호두바이트(); ramură_Listă.add(destinație_VALUE); Linie.add(비교들[Comandă - (Comandă <= 158 ? 153 : 159)] + " " + marcaj_VALUE + "_b" + destinație_VALUE);
            } else if (Comandă == 167 || Comandă == 200) {
                int destinație_VALUE = Poziție + (Comandă == 167 ? comandă_date.부호두바이트() : comandă_date.네바이트()); ramură_Listă.add(destinație_VALUE); Linie.add("jmp " + marcaj_VALUE + "_b" + destinație_VALUE);
            } else if (Comandă == 170 || Comandă == 171) {
                while (comandă_date.Poziție % 4 != 0) comandă_date.한바이트();
                int valoare_implicită = Poziție + comandă_date.네바이트(); ramură_Listă.add(valoare_implicită); Linie.add("popl %eax");
                int element_COUNT, 아래 = 0;
                if (Comandă == 170) { 아래 = comandă_date.네바이트(); int 위 = comandă_date.네바이트(); long lungime_VALUE = (long)위 - 아래 + 1; if (lungime_VALUE < 1 || lungime_VALUE > (comandă_date.date.length - comandă_date.Poziție) / 4) throw new Traducere_eroare("switch clip eroare"); element_COUNT = (int)lungime_VALUE; }
                else { element_COUNT = comandă_date.네바이트(); if (element_COUNT < 0 || element_COUNT > (comandă_date.date.length - comandă_date.Poziție) / 8) throw new Traducere_eroare("switch Mărime eroare"); }
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                    int VALUE = Comandă == 170 ? 아래 + 순번 : comandă_date.네바이트(), destinație_VALUE = Poziție + comandă_date.네바이트(); ramură_Listă.add(destinație_VALUE);
                    Collections.addAll(Linie,"cmpl $" + VALUE + ", %eax","je " + marcaj_VALUE + "_b" + destinație_VALUE);
                }
                Linie.add("jmp " + marcaj_VALUE + "_b" + valoare_implicită);
            } else if (Comandă == 172 || Comandă == 176 || Comandă == 177) {
                if (Comandă != 177) Linie.add("popl %eax"); Collections.addAll(Linie,"leave","ret");
            } else if (Comandă == 178 || Comandă == 179) {
                metodă_referință referință = Clasă_VALUE.referință(comandă_date.두바이트()); if (!필드들.containsKey(referință)) throw new Traducere_eroare("알 수 없는 valoare_câmp");
                Collections.addAll(Linie,"call " + simbol("init",referință.proprietar_VALUE),(Comandă == 178 ? "pushl " : "popl ") + simbol("field",referință.부분들()));
            } else if (Comandă == 184) {
                metodă_referință referință = Clasă_VALUE.referință(comandă_date.두바이트()); if (!함수들.containsKey(referință)) throw new Traducere_eroare("알 수 없는 funcție_VALUE");
                함수형식 호출형식 = new 함수형식(referință.서술); Collections.addAll(Linie,"call " + simbol("init",referință.proprietar_VALUE),"call " + simbol("method",referință.부분들()));
                if (!호출형식.Argumente.isEmpty()) Linie.add("addl $" + 호출형식.Argumente.size() * 4 + ", %esp");
                if (!호출형식.restitui_KR.equals("V")) Linie.add("pushl %eax");
            } else if (Comandă == 182) {
                metodă_referință referință = Clasă_VALUE.referință(comandă_date.두바이트());
                if (referință.equals(new metodă_referință("java/lang/String","length","()I"))) Collections.addAll(Linie,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (referință.equals(new metodă_referință("java/lang/String","charAt","(I)C"))) Collections.addAll(Linie,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Traducere_eroare("가상 funcție_VALUE 호출 미지원");
            } else if (Comandă == 188) {
                if (comandă_date.한바이트() != 10) throw new Traducere_eroare("new int[]만 suport_VALUE"); Collections.addAll(Linie,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Comandă == 190) Collections.addAll(Linie,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Comandă == 196) {
                int extensie_VALUE = comandă_date.한바이트(), INDEX = comandă_date.두바이트(); verifica_local(INDEX,local_COUNT);
                if (extensie_VALUE == 21 || extensie_VALUE == 25 || extensie_VALUE == 54 || extensie_VALUE == 58) Linie.add((extensie_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (extensie_VALUE == 132) Linie.add("addl $" + comandă_date.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Traducere_eroare("wide Comandă 미지원");
            } else if (Comandă == 198 || Comandă == 199) {
                int destinație_VALUE = Poziție + comandă_date.부호두바이트(); ramură_Listă.add(destinație_VALUE); Collections.addAll(Linie,"popl %eax","testl %eax, %eax",(Comandă == 198 ? "je " : "jne ") + marcaj_VALUE + "_b" + destinație_VALUE);
            } else throw new Traducere_eroare("미지원 Comandă: " + Comandă);
        }
        if (!경계들.containsAll(ramură_Listă)) throw new Traducere_eroare("Comandă 경계가 아닌 곳으로 ramură");
        Linie.add(".size " + marcaj_VALUE + ", .-" + marcaj_VALUE); return String.join("\n",Linie);
    }
    String X_86_constantă(Clasă_date date, int INDEX) {
        if (date.상수종류[INDEX] == 3) return date.constantă_date[INDEX].toString();
        if (date.상수종류[INDEX] == 8) return șir_simbol(date.문자((Integer)date.constantă_date[INDEX]));
        throw new Traducere_eroare("정수와 șir_VALUE 상수만 suport_VALUE");
    }
    String X_86_asamblare(String intrare_p, List<String> 내보냄, String țintă) throws IOException {
        Map<String,String> mașină_tabel = new HashMap<>();
        for (String Linie : Files.readAllLines(resursă_cale.resolve("_86_mașină_Functions.tsv"))) { String[] asocia_VALUE = Linie.split("\t"); if (asocia_VALUE[0].equals(țintă)) mașină_tabel.put(asocia_VALUE[1] + asocia_VALUE[2],asocia_VALUE[3]); }
        int index_de_poziție = intrare_p.lastIndexOf('.'); if (index_de_poziție < 0) throw new Traducere_eroare("intrare_p atribui_VALUE eroare");
        String proprietar_VALUE = intrare_p.substring(0,index_de_poziție).replace('.','/'), metodă_intrare_nume = intrare_p.substring(index_de_poziție + 1); metodă_referință intrare_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metodă_referință referință = new metodă_referință(proprietar_VALUE,metodă_intrare_nume,서술); if (함수들.containsKey(referință)) { if (intrare_p_VALUE != null) throw new Traducere_eroare("겹친 intrare_p"); intrare_p_VALUE = referință; } }
        if (intrare_p_VALUE == null || (함수들.get(intrare_p_VALUE).acces_intrare & 0x100) != 0) throw new Traducere_eroare("intrare_p_VALUE funcție_VALUE format_VALUE eroare");
        List<String> Linie = new ArrayList<>(); Linie.add(".code32");
        for (Clasă_date date : 클래스들.values()) {
            String Stare_VALUE = simbol("state",date.Nume), 초기화 = simbol("init",date.Nume);
            Collections.addAll(Linie,".bss",".balign 4",Stare_VALUE + ": .long 0",".text",초기화 + ":","cmpl $0, " + Stare_VALUE,"jne " + 초기화 + "_done","movl $1, " + Stare_VALUE);
            metodă_referință 초기화참조 = new metodă_referință(date.Nume,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Linie.add("call " + simbol("method",초기화참조.부분들()));
            Collections.addAll(Linie,"movl $2, " + Stare_VALUE,초기화 + "_done:","ret");
            for (membru_date valoare_câmp : date.valoare_câmp) {
                byte[] constantă_VALUE = valoare_câmp.atribut_VALUE.get("ConstantValue"); String VALUE = constantă_VALUE == null ? "0" : X_86_constantă(date,new date_Reader(constantă_VALUE).두바이트());
                Collections.addAll(Linie,".data",".balign 4",simbol("field",date.Nume,valoare_câmp.Nume,valoare_câmp.서술) + ": .long " + VALUE);
            }
            for (membru_date funcție_VALUE : date.funcție_VALUE) if (!funcție_VALUE.Nume.equals("<init>")) Linie.add(X_86_metodă_corp(new metodă_referință(date.Nume,funcție_VALUE.Nume,funcție_VALUE.서술),funcție_VALUE,mașină_tabel,țintă));
        }
        Collections.addAll(Linie,".text",".globl java_entry","java_entry:","call " + simbol("init",intrare_p_VALUE.proprietar_VALUE),"call " + simbol("method",intrare_p_VALUE.부분들()));
        if (intrare_p_VALUE.서술.equals("()V")) Linie.add("xorl %eax, %eax"); Linie.add("ret");
        for (String atribui_VALUE : 내보냄) {
            int delimitator_VALUE = atribui_VALUE.indexOf('='); if (delimitator_VALUE < 1) throw new Traducere_eroare("내보내기 atribui_VALUE eroare");
            String extern_VALUE = atribui_VALUE.substring(0,delimitator_VALUE), funcție_VALUE = atribui_VALUE.substring(delimitator_VALUE + 1); int divizie_KR = funcție_VALUE.lastIndexOf('.');
            if (divizie_KR < 0 || !extern_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Traducere_eroare("내보내기 simbol eroare");
            String Clasă_VALUE = funcție_VALUE.substring(0,divizie_KR).replace('.','/'), Nume = funcție_VALUE.substring(divizie_KR + 1); metodă_referință selecție_VALUE = null;
            for (metodă_referință referință : 함수들.keySet()) if (referință.proprietar_VALUE.equals(Clasă_VALUE) && referință.Nume.equals(Nume)) { if (selecție_VALUE != null) throw new Traducere_eroare("겹친 내보내기 țintă"); selecție_VALUE = referință; }
            if (selecție_VALUE == null) throw new Traducere_eroare("내보낼 함수가 없음");
            Collections.addAll(Linie,".text",".globl " + extern_VALUE,extern_VALUE + ":","call " + simbol("init",selecție_VALUE.proprietar_VALUE),"jmp " + simbol("method",selecție_VALUE.부분들()));
        }
        Linie.add(".section .rodata");
        for (Map.Entry<String,String> intrare_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Linie,".balign 4",intrare_VALUE.getValue() + ":",".long " + intrare_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lecție_VALUE : intrare_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(lecție_VALUE)); if (!단위들.isEmpty()) Linie.add(".long " + String.join(",",단위들));
        }
        Linie.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Linie) + "\n";
    }
    static void executa_instrument(List<String> Comandă) throws Exception {
        if (new ProcessBuilder(Comandă).inheritIO().start().waitFor() != 0) throw new Traducere_eroare("compilare_sursă eroare: " + Comandă.get(0));
    }
    static String date_șir(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Traducere(List<Path> 입력들, String țintă, String intrare_p, List<String> 내보냄, Path Rezultat, Path resursă_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Clasă_cale = 임시.resolve("classes"); Files.createDirectory(Clasă_cale);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Clasă_cale.toString(),"-sourcepath",Clasă_cale.toString(),"-d",Clasă_cale.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int sursă_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Rezultat.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Traducere_eroare("Rezultat 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); sursă_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Traducere_eroare(".java 또는 .class만 suport_VALUE");
            }
            if (sursă_COUNT > 0) executa_instrument(자바명령);
            try (java.util.stream.Stream<Path> cale_Listă = Files.walk(Clasă_cale)) { cale_Listă.filter(Cale -> Cale.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,țintă.equals("user") ? "user" : "kernel",262144,resursă_VALUE);
            String 조립 = CONVERT_VALUE.X_86_asamblare(intrare_p,내보냄,țintă); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path instrument_poziție = resursă_VALUE.getParent();
            executa_instrument(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            executa_instrument(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),instrument_poziție.resolve("CLR_suport.s").toString()));
            List<String> Conectează = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (țintă.equals("kernel")) Conectează.add("-r");
            else {
                executa_instrument(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),instrument_poziție.resolve(țintă.equals("user") ? "buta_utilizator_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(Conectează,"-e","_start",임시.resolve("start.o").toString());
                if (țintă.equals("user")) Collections.addAll(Conectează,"-T",instrument_poziție.resolve("utilizator_Link_Aspect.ld").toString());
            }
            Collections.addAll(Conectează,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); executa_instrument(Conectează);
            Rezultat = Rezultat.toAbsolutePath(); Files.createDirectories(Rezultat.getParent()); Path publica_VALUE = Files.createTempFile(Rezultat.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publica_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(publica_VALUE,Rezultat,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publica_VALUE); }
            Files.setPosixFilePermissions(Rezultat,java.nio.file.attribute.PosixFilePermissions.fromString(țintă.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Rezultat + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbol_date = new ArrayList<>(), sursă_date = new ArrayList<>();
            for (metodă_referință referință : CONVERT_VALUE.함수들.keySet()) simbol_date.add(date_șir(simbol("method",referință.부분들())) + ":" + date_șir(referință.proprietar_VALUE + "." + referință.Nume + referință.서술));
            for (Path 입력 : 입력들) {
                byte[] cod_hash_Fișier = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte VALUE : cod_hash_Fișier) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                sursă_date.add(date_șir(입력.toAbsolutePath().toString()) + ":" + date_șir(SMS.toString()));
            }
            Files.writeString(Paths.get(Rezultat + ".json"),"{\"target\":" + date_șir(țintă) + ",\"entry\":" + date_șir(intrare_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbol_date) + "},\"sources\":{" + String.join(",",sursă_date) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> cale_Listă = Files.walk(임시)) { for (Path Cale : (Iterable<Path>)cale_Listă.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Cale); }
        }
    }
    public static void main(String[] Argumente) {
        try {
            String intrare_p = null, țintă = "kernel", X_86_țintă = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> cale_Listă = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumente.length; 순번++) {
                String VALUE = Argumente[순번];
                switch (VALUE) {
                    case "--target": X_86_țintă = Argumente[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Clasă_VALUE.funcție_VALUE -o Rezultat [--target linux|kernel|user] [--profile kernel|user] [--export simbol=Clasă_VALUE.funcție_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": intrare_p = Argumente[++순번]; break;
                    case "--profile": țintă = Argumente[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumente[++순번]); break;
                    case "--export": 내보냄.add(Argumente[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argumente[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Traducere_eroare("알 수 없는 옵션: " + VALUE); cale_Listă.add(Paths.get(VALUE));
                }
            }
            if (intrare_p == null || 출력경로 == null || cale_Listă.isEmpty()) throw new Traducere_eroare("--entry, -o, Clasă_VALUE 파일이 필요합니다");
            Path resursă_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_țintă != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_țintă)) throw new Traducere_eroare("알 수 없는 executa_comandă țintă");
                X_86_Traducere(cale_Listă,X_86_țintă,intrare_p,내보냄,출력경로,resursă_VALUE); return;
            }
            String SURSĂ = new 기계어미리번역(cale_Listă, țintă, 낱말수, resursă_VALUE).genera(intrare_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, SURSĂ, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception eroare) { System.err.println("compilare_sursă eroare: " + eroare.getMessage()); System.exit(1); }
    }
}
