// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java класа_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. вдоми JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Превод_грешка extends RuntimeException {
        Превод_грешка(String 설명) { super(설명); }
    }
    static final class податоци_Читач {
        final byte[] податоци;
        int Позиција;
        податоци_Читач(byte[] 입력자료) { податоци = 입력자료; }
        byte[] Читај(int должина_VALUE) {
            if (должина_VALUE < 0 || должина_VALUE > податоци.length - Позиција) throw new Превод_грешка("잘린 класа_VALUE 또는 Команда податоци");
            byte[] мерка = Arrays.copyOfRange(податоци, Позиција, Позиција + должина_VALUE); Позиција += должина_VALUE; return мерка;
        }
        int 한바이트() { if (Позиција >= податоци.length) throw new Превод_грешка("잘린 Команда податоци"); return податоци[Позиција++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class член_податоци {
        final int пристап_внес;
        final String Име, 서술;
        final Map<String, byte[]> атрибут_VALUE;
        член_податоци(int пристап_VALUE, String име_VALUE, String 서술값, Map<String, byte[]> атрибут_податоци) {
            пристап_внес = пристап_VALUE; Име = име_VALUE; 서술 = 서술값; атрибут_VALUE = атрибут_податоци;
        }
    }
    static final class метод_Референци implements Comparable<метод_Референци> {
        final String сопственик_VALUE, Име, 서술;
        метод_Референци(String 소유값, String име_VALUE, String 서술값) { сопственик_VALUE = 소유값; Име = име_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{сопственик_VALUE, Име, 서술}; }
        public int compareTo(метод_Референци рамноправен_уред_VALUE) {
            int Споредба_VALUE = сопственик_VALUE.compareTo(рамноправен_уред_VALUE.сопственик_VALUE);
            if (Споредба_VALUE == 0) Споредба_VALUE = Име.compareTo(рамноправен_уред_VALUE.Име);
            return Споредба_VALUE == 0 ? 서술.compareTo(рамноправен_уред_VALUE.서술) : Споредба_VALUE;
        }
        public boolean equals(Object рамноправен_уред_VALUE) { return рамноправен_уред_VALUE instanceof метод_Референци && compareTo((метод_Референци) рамноправен_уред_VALUE) == 0; }
        public int hashCode() { return Objects.hash(сопственик_VALUE, Име, 서술); }
    }
    static final class класа_податоци {
        final int[] 상수종류;
        final Object[] константа_податоци;
        final String Име;
        final List<член_податоци> поле_VALUE, ФУНКЦИЈА_VALUE;
        класа_податоци(Path ПАТЕКА) throws IOException {
            податоци_Читач Читач_VALUE = new податоци_Читач(Files.readAllBytes(ПАТЕКА));
            if (Читач_VALUE.네바이트() != 0xcafebabe) throw new Превод_грешка("Java класа_VALUE 표식이 아님");
            Читач_VALUE.Читај(4);
            int ставка_COUNT = Читач_VALUE.두바이트(); 상수종류 = new int[ставка_COUNT]; константа_податоци = new Object[ставка_COUNT];
            for (int 순번 = 1; 순번 < ставка_COUNT; 순번++) {
                int 종류 = Читач_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int должина_VALUE = Читач_VALUE.두바이트();
                        byte[] знак_меѓумеморија = Читач_VALUE.Читај(должина_VALUE), 길이붙인자료 = new byte[должина_VALUE + 2];
                        길이붙인자료[0] = (byte)(должина_VALUE >> 8); 길이붙인자료[1] = (byte)должина_VALUE;
                        System.arraycopy(знак_меѓумеморија, 0, 길이붙인자료, 2, должина_VALUE);
                        константа_податоци[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: константа_податоци[순번] = Читач_VALUE.네바이트(); break;
                    case 4: Читач_VALUE.Читај(4); break;
                    case 5: case 6: Читач_VALUE.Читај(8); 순번++; break;
                    case 7: case 8: case 16: константа_податоци[순번] = Читач_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        константа_податоци[순번] = new int[]{Читач_VALUE.두바이트(), Читач_VALUE.두바이트()}; break;
                    case 15: константа_податоци[순번] = new int[]{Читач_VALUE.한바이트(), Читач_VALUE.두바이트()}; break;
                    default: throw new Превод_грешка("지원하지 않는 константа_VALUE 종류: " + 종류);
                }
            }
            Читач_VALUE.두바이트(); Име = класа_име(Читач_VALUE.두바이트());
            if (!класа_име(Читач_VALUE.두바이트()).equals("java/lang/Object") || Читач_VALUE.두바이트() != 0)
                throw new Превод_грешка(Име + ": 상속 및 인터페이스 미지원");
            поле_VALUE = 멤버읽기(Читач_VALUE); ФУНКЦИЈА_VALUE = 멤버읽기(Читач_VALUE); 속성읽기(Читач_VALUE);
            if (Читач_VALUE.Позиција != Читач_VALUE.податоци.length) throw new Превод_грешка("класа_VALUE 뒤에 남은 податоци");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Превод_грешка("문자 константа_VALUE INDEX ГРЕШКА");
            return (String) константа_податоци[INDEX];
        }
        String класа_име(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Превод_грешка("класа_VALUE Референци ГРЕШКА");
            return 문자((Integer)константа_податоци[INDEX]);
        }
        метод_Референци Референци(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Превод_грешка("멤버 Референци ГРЕШКА");
            int[] спари_VALUE = (int[])константа_податоци[INDEX], име_спари = (int[])константа_податоци[спари_VALUE[1]];
            return new метод_Референци(класа_име(спари_VALUE[0]), 문자(име_спари[0]), 문자(име_спари[1]));
        }
        Map<String, byte[]> 속성읽기(податоци_Читач Читач_VALUE) {
            Map<String, byte[]> мерка = new LinkedHashMap<>();
            int ставка_COUNT = Читач_VALUE.두바이트();
            for (int 순번 = 0; 순번 < ставка_COUNT; 순번++) {
                String атрибут_име = 문자(Читач_VALUE.두바이트()); byte[] VALUE = Читач_VALUE.Читај(Читач_VALUE.네바이트());
                if (мерка.put(атрибут_име, VALUE) != null) throw new Превод_грешка("겹친 атрибут_VALUE: " + атрибут_име);
            }
            return мерка;
        }
        List<член_податоци> 멤버읽기(податоци_Читач Читач_VALUE) {
            List<член_податоци> мерка = new ArrayList<>(); int ставка_COUNT = Читач_VALUE.두바이트();
            for (int 순번 = 0; 순번 < ставка_COUNT; 순번++) {
                int пристап_внес = Читач_VALUE.두바이트(); String метод_внес_име = 문자(Читач_VALUE.두바이트()), 서술 = 문자(Читач_VALUE.두바이트());
                мерка.add(new член_податоци(пристап_внес, метод_внес_име, 서술, 속성읽기(Читач_VALUE)));
            }
            return мерка;
        }
    }
    static final class 함수형식 {
        final List<String> Аргументи = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Превод_грешка("ФУНКЦИЈА_VALUE 서술 ГРЕШКА: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Превод_грешка("ФУНКЦИЈА_VALUE 서술 ГРЕШКА: " + 서술);
            Аргументи.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Аргументи.contains("V") || 반환들.size() != 1) throw new Превод_грешка("ФУНКЦИЈА_VALUE 서술 ГРЕШКА: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> мерка = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Позиција = 0; Позиција < 서술.length();) {
            String селекција_VALUE = null;
            for (String формат_VALUE : 허용형식) if (서술.startsWith(формат_VALUE, Позиција)) { селекција_VALUE = формат_VALUE; break; }
            if (селекција_VALUE == null) throw new Превод_грешка("지원하지 않는 тип_податоци: " + 서술);
            мерка.add(селекција_VALUE); Позиција += селекција_VALUE.length();
        }
        return мерка;
    }
    static String симбол(String 종류, String... 부분들) {
        try {
            byte[] хаш_датотека = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Текст = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Текст.append(String.format(Locale.ROOT, "%02x", хаш_датотека[순번] & 255));
            return Текст.toString();
        } catch (Exception ГРЕШКА) { throw new Превод_грешка(ГРЕШКА.toString()); }
    }
    final Map<String, класа_податоци> 클래스들 = new TreeMap<>();
    final Map<метод_Референци, член_податоци> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, машина_класа;
    final int 동적기억낱말수;
    final Path извор_патека;
    기계어미리번역(List<Path> патека_Список, String цел, int 낱말수, Path извор_VALUE) throws IOException {
        if ((!цел.equals("kernel") && !цел.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Превод_грешка("Изврши_наредба цел 또는 Меморија_VALUE 공간 Големина ГРЕШКА");
        실행대상 = цел; 동적기억낱말수 = 낱말수; извор_патека = извор_VALUE;
        // 이 이름도 국가별 извор_дрво генерира 시 해당 언어로 옮긴다.
        машина_класа = цел.equals("kernel") ? "табла" : "корисник";
        for (String ред : Files.readAllLines(извор_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = ред.split("\t", -1);
            if (부분들.length != 4) throw new Превод_грешка("машина ФУНКЦИЈА_VALUE податоци ГРЕШКА");
            if (부분들[0].equals(цел)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path ПАТЕКА : патека_Список) {
            класа_податоци податоци = new класа_податоци(ПАТЕКА);
            if (클래스들.put(податоци.Име, податоци) != null) throw new Превод_грешка("중복 класа_VALUE: " + податоци.Име);
            for (член_податоци поле_VALUE : податоци.поле_VALUE) {
                if ((поле_VALUE.пристап_внес & 8) == 0 || 형식읽기(поле_VALUE.서술).equals(Collections.singletonList("V"))) throw new Превод_грешка("статичен_VALUE 필드만 Поддршка_VALUE");
                if (필드들.put(new метод_Референци(податоци.Име, поле_VALUE.Име, поле_VALUE.서술), поле_VALUE) != null) throw new Превод_грешка("중복 поле_VALUE");
            }
            for (член_податоци ФУНКЦИЈА_VALUE : податоци.ФУНКЦИЈА_VALUE) {
                if (ФУНКЦИЈА_VALUE.Име.equals("<init>")) continue;
                if ((ФУНКЦИЈА_VALUE.пристап_внес & 8) == 0 || (ФУНКЦИЈА_VALUE.пристап_внес & (0x20 | 0x400)) != 0) throw new Превод_грешка("статичен_VALUE 비동기화 함수만 Поддршка_VALUE");
                new 함수형식(ФУНКЦИЈА_VALUE.서술);
                if (함수들.put(new метод_Референци(податоци.Име, ФУНКЦИЈА_VALUE.Име, ФУНКЦИЈА_VALUE.서술), ФУНКЦИЈА_VALUE) != null) throw new Превод_грешка("중복 ФУНКЦИЈА_VALUE");
            }
        }
    }
    String низа_симбол(String Текст) { return 문자열들.computeIfAbsent(Текст, VALUE -> "j_text_" + 문자열들.size()); }
    String константа_израз(класа_податоци податоци, int INDEX) {
        if (INDEX < 1 || INDEX >= податоци.상수종류.length) throw new Превод_грешка("константа_VALUE INDEX клип ГРЕШКА");
        if (податоци.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + податоци.константа_податоци[INDEX] + ")";
        if (податоци.상수종류[INDEX] == 8) return "(word)" + низа_симбол(податоци.문자((Integer)податоци.константа_податоци[INDEX]));
        throw new Превод_грешка("정수와 низа_VALUE_6ca8363c 상수만 Поддршка_VALUE");
    }
    String 함수원형(метод_Референци Референци) {
        List<String> 인수들 = new ArrayList<>(); int ставка_COUNT = new 함수형식(Референци.서술).Аргументи.size();
        for (int 순번 = 0; 순번 < ставка_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + симбол("method", Референци.부분들()) + "(" + (ставка_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void провери_локален(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Превод_грешка("локален_обем 변수 INDEX клип ГРЕШКА"); }
    void 분기넣기(List<String> 출력, Set<Integer> гранка_Список, int Позиција, int 이동량, String услов) {
        int одредиште_VALUE = Позиција + 이동량; гранка_Список.add(одредиште_VALUE);
        출력.add((услов == null ? "" : "if (" + услов + ") ") + "goto b" + одредиште_VALUE + ";");
    }
    String метод_тело(метод_Референци ФУНКЦИЈА_VALUE, член_податоци податоци) {
        byte[] тело_податоци = податоци.атрибут_VALUE.get("Code"); if (тело_податоци == null) throw new Превод_грешка("ФУНКЦИЈА_VALUE 몸체가 없음: " + ФУНКЦИЈА_VALUE.Име);
        податоци_Читач Читач_VALUE = new податоци_Читач(тело_податоци); int 쌓임깊이 = Читач_VALUE.두바이트(), 지역변수수 = Читач_VALUE.두바이트();
        податоци_Читач наредба_податоци = new податоци_Читач(Читач_VALUE.Читај(Читач_VALUE.네바이트()));
        if (Читач_VALUE.두바이트() != 0) throw new Превод_грешка("try/catch/finally 미지원");
        함수형식 формат_VALUE = new 함수형식(ФУНКЦИЈА_VALUE.서술); if (지역변수수 < формат_VALUE.Аргументи.size()) throw new Превод_грешка("매개변수보다 적은 локален_обем 변수");
        класа_податоци класа_VALUE = 클래스들.get(ФУНКЦИЈА_VALUE.сопственик_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(ФУНКЦИЈА_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < формат_VALUE.Аргументи.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), гранка_Список = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (наредба_податоци.Позиција < наредба_податоци.податоци.length) {
            int Позиција = наредба_податоци.Позиција, Команда = наредба_податоци.한바이트(); 경계들.add(Позиција); 출력.add("b" + Позиција + ":;");
            if (Команда == 0) continue;
            if (Команда == 1) 출력.add("PUSH(0);");
            else if (Команда >= 2 && Команда <= 8) 출력.add("PUSH((uint32_t)(" + (Команда - 3) + "));");
            else if (Команда == 16 || Команда == 17) 출력.add("PUSH((uint32_t)(" + (Команда == 16 ? наредба_податоци.부호한바이트() : наредба_податоци.부호두바이트()) + "));");
            else if (Команда == 18 || Команда == 19) 출력.add("PUSH(" + константа_израз(класа_VALUE, Команда == 18 ? наредба_податоци.한바이트() : наредба_податоци.두바이트()) + ");");
            else if (Команда == 21 || Команда == 25 || (Команда >= 26 && Команда <= 29) || (Команда >= 42 && Команда <= 45)) {
                int INDEX = Команда == 21 || Команда == 25 ? наредба_податоци.한바이트() : Команда - (Команда <= 29 ? 26 : 42);
                провери_локален(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (Команда == 54 || Команда == 58 || (Команда >= 59 && Команда <= 62) || (Команда >= 75 && Команда <= 78)) {
                int INDEX = Команда == 54 || Команда == 58 ? наредба_податоци.한바이트() : Команда - (Команда <= 62 ? 59 : 75);
                провери_локален(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (Команда == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Команда == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Команда == 87 || Команда == 88) 출력.add(Команда == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Команда >= 89 && Команда <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] редослед_Список = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Команда - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : редослед_Список[Команда - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (Команда == 96 || Команда == 100 || Команда == 104 || Команда == 126 || Команда == 128 || Команда == 130) {
                String операција_VALUE = Команда == 96 ? "+" : Команда == 100 ? "-" : Команда == 104 ? "*" : Команда == 126 ? "&" : Команда == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + операција_VALUE + " (uint32_t)b);");
            } else if (Команда == 108 || Команда == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Команда == 112 ? 1 : 0) + "));");
            else if (Команда == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Команда == 120 || Команда == 122 || Команда == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Команда == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Команда == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Команда == 132) {
                int INDEX = наредба_податоци.한바이트(), 증가량 = наредба_податоци.부호한바이트(); провери_локален(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Команда >= 145 && Команда <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Команда == 145 ? "int8_t" : Команда == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Команда >= 153 && Команда <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, гранка_Список, Позиција, наредба_податоци.부호두바이트(), "(int32_t)a " + 비교들[Команда - 153] + " 0");
            } else if (Команда >= 159 && Команда <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, гранка_Список, Позиција, наредба_податоци.부호두바이트(), Команда >= 165 ? "a " + 비교들[Команда - 159] + " b" : "(int32_t)a " + 비교들[Команда - 159] + " (int32_t)b");
            } else if (Команда == 167 || Команда == 200) 분기넣기(출력, гранка_Список, Позиција, Команда == 167 ? наредба_податоци.부호두바이트() : наредба_податоци.네바이트(), null);
            else if (Команда == 170 || Команда == 171) {
                while (наредба_податоци.Позиција % 4 != 0) наредба_податоци.한바이트();
                int стандардна_вредност = наредба_податоци.네바이트(); 출력.add("a = POP();");
                if (Команда == 170) {
                    int 아래 = наредба_податоци.네바이트(), 위 = наредба_податоци.네바이트(); long ставка_COUNT = (long)위 - 아래 + 1;
                    if (ставка_COUNT < 1 || ставка_COUNT > (наредба_податоци.податоци.length - наредба_податоци.Позиција) / 4) throw new Превод_грешка("switch клип ГРЕШКА");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, гранка_Список, Позиција, наредба_податоци.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int ставка_COUNT = наредба_податоци.네바이트(), предна_податоци = 0;
                    if (ставка_COUNT < 0 || ставка_COUNT > (наредба_податоци.податоци.length - наредба_податоци.Позиција) / 8) throw new Превод_грешка("switch Големина ГРЕШКА");
                    for (int 순번 = 0; 순번 < ставка_COUNT; 순번++) {
                        int VALUE = наредба_податоци.네바이트(); if (순번 > 0 && VALUE <= предна_податоци) throw new Превод_грешка("switch редослед_VALUE ГРЕШКА"); предна_податоци = VALUE;
                        분기넣기(출력, гранка_Список, Позиција, наредба_податоци.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, гранка_Список, Позиција, стандардна_вредност, null);
            } else if (Команда == 172 || Команда == 176 || Команда == 177) 출력.add("return " + (Команда == 177 ? "0" : "POP()") + ";");
            else if (Команда == 178 || Команда == 179) {
                метод_Референци Референци = класа_VALUE.Референци(наредба_податоци.두바이트()); if (!필드들.containsKey(Референци)) throw new Превод_грешка("알 수 없는 поле_VALUE");
                출력.add(симбол("init", Референци.сопственик_VALUE) + "();"); String поле_VALUE = симбол("field", Референци.부분들());
                출력.add(Команда == 178 ? "PUSH(" + поле_VALUE + ");" : поле_VALUE + " = POP();");
            } else if (Команда == 184) {
                метод_Референци Референци = класа_VALUE.Референци(наредба_податоци.두바이트()); if (!함수들.containsKey(Референци)) throw new Превод_грешка("알 수 없는 ФУНКЦИЈА_VALUE");
                함수형식 호출형식 = new 함수형식(Референци.서술); int ставка_COUNT = 호출형식.Аргументи.size();
                출력.add(симбол("init", Референци.сопственик_VALUE) + "();"); 출력.add("if(sp < " + ставка_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + ставка_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < ставка_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + симбол("method", Референци.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Команда == 182) {
                метод_Референци Референци = класа_VALUE.Референци(наредба_податоци.두바이트());
                if (Референци.equals(new метод_Референци("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Референци.equals(new метод_Референци("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Превод_грешка("가상 ФУНКЦИЈА_VALUE 호출 미지원");
            } else if (Команда == 188) {
                if (наредба_податоци.한바이트() != 10) throw new Превод_грешка("new int[]만 Поддршка_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Команда == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Команда == 196) {
                int наставка_VALUE = наредба_податоци.한바이트(), INDEX = наредба_податоци.두바이트(); провери_локален(INDEX, 지역변수수);
                if (наставка_VALUE == 21 || наставка_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (наставка_VALUE == 54 || наставка_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (наставка_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + наредба_податоци.부호두바이트() + ");");
                else throw new Превод_грешка("미지원 wide Команда");
            } else if (Команда == 198 || Команда == 199) {
                출력.add("a = POP();"); 분기넣기(출력, гранка_Список, Позиција, наредба_податоци.부호두바이트(), "a " + (Команда == 198 ? "==" : "!=") + " 0");
            } else throw new Превод_грешка(ФУНКЦИЈА_VALUE.сопственик_VALUE + "." + ФУНКЦИЈА_VALUE.Име + ", бајт_VALUE " + Позиција + ": 미지원 Команда " + Команда);
        }
        if (!경계들.containsAll(гранка_Список)) throw new Превод_грешка("Команда 경계가 아닌 곳으로 гранка");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String извези_метод(String Врска_симбол, String цел, boolean 진입점여부) {
        int позиционирање_INDEX = цел.lastIndexOf('.'); if (позиционирање_INDEX < 0 || !Врска_симбол.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Превод_грешка("내보내기 доделува_VALUE ГРЕШКА");
        String сопственик_VALUE = цел.substring(0, позиционирање_INDEX).replace('.', '/'), Име = цел.substring(позиционирање_INDEX + 1); метод_Референци селекција_VALUE = null;
        for (метод_Референци Референци : 함수들.keySet()) if (Референци.сопственик_VALUE.equals(сопственик_VALUE) && Референци.Име.equals(Име)) {
            if (селекција_VALUE != null) throw new Превод_грешка("겹친 내보내기 цел"); селекција_VALUE = Референци;
        }
        if (селекција_VALUE == null || (함수들.get(селекција_VALUE).пристап_внес & 0x100) != 0) throw new Превод_грешка("내보낼 함수가 없음 또는 native ФУНКЦИЈА_VALUE");
        함수형식 формат_VALUE = new 함수형식(селекција_VALUE.서술);
        if ((진입점여부 && !формат_VALUE.Аргументи.isEmpty()) || !Arrays.asList("V", "I").contains(формат_VALUE.반환)) throw new Превод_грешка("внес_поен_VALUE 또는 C 경계 формат_VALUE ГРЕШКА");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < формат_VALUE.Аргументи.size(); 순번++) {
            if (!формат_VALUE.Аргументи.get(순번).equals("I")) throw new Превод_грешка("C 경계는 int 인수만 Поддршка_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (формат_VALUE.반환.equals("V") ? "void " : "int32_t ") + Врска_симбол + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + симбол("init", селекција_VALUE.сопственик_VALUE) + "(); " + (формат_VALUE.반환.equals("V") ? "" : "return (int32_t)") + симбол("method", селекција_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String генерира(String внес_поен, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<метод_Референци, член_податоци> внес_VALUE : 함수들.entrySet()) {
            метод_Референци Референци = внес_VALUE.getKey(); член_податоци податоци = внес_VALUE.getValue(); 선언들.add(함수원형(Референци) + ";");
            if ((податоци.пристап_внес & 0x100) != 0) {
                String Врзи_се = 기계함수들.get(Референци.Име + Референци.서술);
                if (!Референци.сопственик_VALUE.equals(машина_класа) || Врзи_се == null) throw new Превод_грешка("허용되지 않은 native ФУНКЦИЈА_VALUE: " + Референци.Име);
                int ставка_COUNT = new 함수형식(Референци.서술).Аргументи.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < ставка_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Врзи_се + "(" + (ставка_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(ставка_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Референци) + " { return " + Врзи_се + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(метод_тело(Референци, податоци));
        }
        for (Map.Entry<метод_Референци, член_податоци> внес_VALUE : 필드들.entrySet()) {
            метод_Референци Референци = внес_VALUE.getKey(); byte[] константа_VALUE = внес_VALUE.getValue().атрибут_VALUE.get("ConstantValue");
            String VALUE = константа_VALUE == null ? "0" : константа_израз(클래스들.get(Референци.сопственик_VALUE), new податоци_Читач(константа_VALUE).두바이트());
            필드선언들.add("static word " + симбол("field", Референци.부분들()) + " = " + VALUE + ";");
        }
        for (String Име : 클래스들.keySet()) {
            String иницијализирај = симбол("init", Име), статус_VALUE = симбол("state", Име);
            선언들.add("static void " + иницијализирај + "(void);"); 필드선언들.add("static unsigned " + статус_VALUE + ";");
            метод_Референци Референци = new метод_Референци(Име, "<clinit>", "()V");
            몸체들.add("static void " + иницијализирај + "(void) { if(" + статус_VALUE + ") return; " + статус_VALUE + " = 1; " + (함수들.containsKey(Референци) ? симбол("method", Референци.부분들()) + "(); " : "") + статус_VALUE + " = 2; }");
        }
        몸체들.add(извези_метод("java_entry", внес_поен, true)); Set<String> 공개이름 = new HashSet<>();
        for (String доделува_VALUE : 내보내기목록) {
            int позиционирање_INDEX = доделува_VALUE.indexOf('='); if (позиционирање_INDEX < 1) throw new Превод_грешка("내보내기 доделува_VALUE ГРЕШКА");
            String Име = доделува_VALUE.substring(0, позиционирање_INDEX); 공개이름.add(Име); 몸체들.add(извези_метод(Име, доделува_VALUE.substring(позиционирање_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> внес_VALUE : 문자열들.entrySet()) {
            String Текст = внес_VALUE.getKey(); StringBuilder низа_VALUE = new StringBuilder("static const word " + внес_VALUE.getValue() + "[] = {" + Текст.length());
            for (int 순번 = 0; 순번 < Текст.length(); 순번++) низа_VALUE.append(", ").append((int)Текст.charAt(순번));
            문자열선언들.add(низа_VALUE.append("};").toString());
        }
        String Поддршка_VALUE = Files.readString(извор_патека.resolve("заеднички_јазик_за_време_на_извршување_Поддршка.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Поддршка_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ИЗВОР, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> име_табела = new HashMap<>();
        for (String ред : Files.readAllLines(извор_патека.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] спари_VALUE = ред.split("\t"); име_табела.put(спари_VALUE[0], спари_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(ИЗВОР); StringBuffer мерка = new StringBuffer();
        while (찾개.find()) {
            String Име = 찾개.group(), 새이름 = Име;
            if (!Име.startsWith("//") && !Име.startsWith("/*") && !Име.startsWith("\"") && !Име.startsWith("'") && !공개이름.contains(Име)) {
                새이름 = име_табела.getOrDefault(Име, Име);
                if (Име.matches("a[0-9]+")) 새이름 = "Аргументи" + Име.substring(1);
                if (Име.matches("b[0-9]+")) 새이름 = "гранка" + Име.substring(1);
                if (범용표기) {
                    StringBuilder нотација_VALUE = new StringBuilder();
                    for (char знак_VALUE : 새이름.toCharArray()) нотација_VALUE.append(знак_VALUE < 128 ? Character.toString(знак_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)знак_VALUE));
                    새이름 = нотација_VALUE.toString();
                }
            }
            찾개.appendReplacement(мерка, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(мерка); return мерка.toString();
    }
    String 엑스함수본문(метод_Референци ФУНКЦИЈА_VALUE, член_податоци податоци, Map<String,String> машина_табела, String цел) {
        String 표식 = симбол("method", ФУНКЦИЈА_VALUE.부분들());
        List<String> ред = new ArrayList<>();
        if ((податоци.пристап_внес & 0x100) != 0) {
            String Врзи_се = машина_табела.get(ФУНКЦИЈА_VALUE.Име + ФУНКЦИЈА_VALUE.서술);
            if (!ФУНКЦИЈА_VALUE.сопственик_VALUE.equals(цел.equals("kernel") ? "уред_VALUE" : "корисник") || Врзи_се == null) throw new Превод_грешка("허용되지 않은 native ФУНКЦИЈА_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Врзи_се;
        }
        byte[] основен_текст = податоци.атрибут_VALUE.get("Code"); if (основен_текст == null) throw new Превод_грешка("ФУНКЦИЈА_VALUE 몸체가 없음");
        податоци_Читач Читач_VALUE = new податоци_Читач(основен_текст); Читач_VALUE.두바이트(); int локален_COUNT = Читач_VALUE.두바이트();
        податоци_Читач наредба_податоци = new податоци_Читач(Читач_VALUE.Читај(Читач_VALUE.네바이트()));
        if (Читач_VALUE.두바이트() != 0) throw new Превод_грешка("try/catch/finally 미지원");
        함수형식 формат_VALUE = new 함수형식(ФУНКЦИЈА_VALUE.서술); if (локален_COUNT < формат_VALUE.Аргументи.size()) throw new Превод_грешка("매개변수보다 적은 локален_обем 변수");
        Collections.addAll(ред,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + локален_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < формат_VALUE.Аргументи.size(); 순번++) Collections.addAll(ред,"movl " + (8 + 4 * (формат_VALUE.Аргументи.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        класа_податоци класа_VALUE = 클래스들.get(ФУНКЦИЈА_VALUE.сопственик_VALUE); Set<Integer> 경계들 = new HashSet<>(), гранка_Список = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (наредба_податоци.Позиција < наредба_податоци.податоци.length) {
            int Позиција = наредба_податоци.Позиција, Команда = наредба_податоци.한바이트(); String позиционирање_INDEX = 표식 + "_b" + Позиција;
            ред.add(позиционирање_INDEX + ":"); 경계들.add(Позиција);
            if (Команда == 0) ред.add("nop");
            else if (Команда == 1) ред.add("pushl $0");
            else if (Команда >= 2 && Команда <= 8) ред.add("pushl $" + (Команда - 3));
            else if (Команда == 16 || Команда == 17) ред.add("pushl $" + (Команда == 16 ? наредба_податоци.부호한바이트() : наредба_податоци.부호두바이트()));
            else if (Команда == 18 || Команда == 19) {
                int INDEX = Команда == 18 ? наредба_податоци.한바이트() : наредба_податоци.두바이트();
                ред.add("pushl $" + 엑스상수(класа_VALUE,INDEX));
            } else if (Команда == 21 || Команда == 25 || (Команда >= 26 && Команда <= 29) || (Команда >= 42 && Команда <= 45) || Команда == 54 || Команда == 58 || (Команда >= 59 && Команда <= 62) || (Команда >= 75 && Команда <= 78)) {
                boolean 읽음 = Команда < 54; int INDEX = Команда == 21 || Команда == 25 || Команда == 54 || Команда == 58 ? наредба_податоци.한바이트() : Команда - (Команда <= 29 ? 26 : Команда <= 45 ? 42 : Команда <= 62 ? 59 : 75);
                провери_локален(INDEX,локален_COUNT); ред.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Команда == 46) Collections.addAll(ред,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Команда == 79) Collections.addAll(ред,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Команда == 87 || Команда == 88) ред.add("addl $" + (Команда == 87 ? 4 : 8) + ", %esp");
            else if (Команда >= 89 && Команда <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] редослед_Список = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Команда - 89]; 순번++) ред.add("popl " + 저장기들[순번]);
                for (int 순번 : редослед_Список[Команда - 89]) ред.add("pushl " + 저장기들[순번]);
            } else if (Команда == 96 || Команда == 100 || Команда == 104 || Команда == 126 || Команда == 128 || Команда == 130) {
                String операција_VALUE = Команда == 96 ? "addl" : Команда == 100 ? "subl" : Команда == 104 ? "imull" : Команда == 126 ? "andl" : Команда == 128 ? "orl" : "xorl";
                Collections.addAll(ред,"popl %ecx","popl %eax",операција_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Команда == 108 || Команда == 112) Collections.addAll(ред,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + позиционирање_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + позиционирање_INDEX + "_divide","xorl %edx, %edx","jmp " + позиционирање_INDEX + "_done",позиционирање_INDEX + "_divide:","cltd","idivl %ecx",позиционирање_INDEX + "_done:","pushl " + (Команда == 108 ? "%eax" : "%edx"));
            else if (Команда == 116) ред.add("negl (%esp)");
            else if (Команда == 120 || Команда == 122 || Команда == 124) Collections.addAll(ред,"popl %ecx","popl %eax",(Команда == 120 ? "sall" : Команда == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Команда == 132) {
                int INDEX = наредба_податоци.한바이트(), 증가 = наредба_податоци.부호한바이트(); провери_локален(INDEX,локален_COUNT); ред.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Команда >= 145 && Команда <= 147) Collections.addAll(ред,"popl %eax",Команда == 145 ? "movsbl %al, %eax" : Команда == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Команда >= 153 && Команда <= 166) {
                if (Команда <= 158) Collections.addAll(ред,"popl %eax","testl %eax, %eax");
                else Collections.addAll(ред,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int одредиште_VALUE = Позиција + наредба_податоци.부호두바이트(); гранка_Список.add(одредиште_VALUE); ред.add(비교들[Команда - (Команда <= 158 ? 153 : 159)] + " " + 표식 + "_b" + одредиште_VALUE);
            } else if (Команда == 167 || Команда == 200) {
                int одредиште_VALUE = Позиција + (Команда == 167 ? наредба_податоци.부호두바이트() : наредба_податоци.네바이트()); гранка_Список.add(одредиште_VALUE); ред.add("jmp " + 표식 + "_b" + одредиште_VALUE);
            } else if (Команда == 170 || Команда == 171) {
                while (наредба_податоци.Позиција % 4 != 0) наредба_податоци.한바이트();
                int стандардна_вредност = Позиција + наредба_податоци.네바이트(); гранка_Список.add(стандардна_вредност); ред.add("popl %eax");
                int ставка_COUNT, 아래 = 0;
                if (Команда == 170) { 아래 = наредба_податоци.네바이트(); int 위 = наредба_податоци.네바이트(); long должина_VALUE = (long)위 - 아래 + 1; if (должина_VALUE < 1 || должина_VALUE > (наредба_податоци.податоци.length - наредба_податоци.Позиција) / 4) throw new Превод_грешка("switch клип ГРЕШКА"); ставка_COUNT = (int)должина_VALUE; }
                else { ставка_COUNT = наредба_податоци.네바이트(); if (ставка_COUNT < 0 || ставка_COUNT > (наредба_податоци.податоци.length - наредба_податоци.Позиција) / 8) throw new Превод_грешка("switch Големина ГРЕШКА"); }
                for (int 순번 = 0; 순번 < ставка_COUNT; 순번++) {
                    int VALUE = Команда == 170 ? 아래 + 순번 : наредба_податоци.네바이트(), одредиште_VALUE = Позиција + наредба_податоци.네바이트(); гранка_Список.add(одредиште_VALUE);
                    Collections.addAll(ред,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + одредиште_VALUE);
                }
                ред.add("jmp " + 표식 + "_b" + стандардна_вредност);
            } else if (Команда == 172 || Команда == 176 || Команда == 177) {
                if (Команда != 177) ред.add("popl %eax"); Collections.addAll(ред,"leave","ret");
            } else if (Команда == 178 || Команда == 179) {
                метод_Референци Референци = класа_VALUE.Референци(наредба_податоци.두바이트()); if (!필드들.containsKey(Референци)) throw new Превод_грешка("알 수 없는 поле_VALUE");
                Collections.addAll(ред,"call " + симбол("init",Референци.сопственик_VALUE),(Команда == 178 ? "pushl " : "popl ") + симбол("field",Референци.부분들()));
            } else if (Команда == 184) {
                метод_Референци Референци = класа_VALUE.Референци(наредба_податоци.두바이트()); if (!함수들.containsKey(Референци)) throw new Превод_грешка("알 수 없는 ФУНКЦИЈА_VALUE");
                함수형식 호출형식 = new 함수형식(Референци.서술); Collections.addAll(ред,"call " + симбол("init",Референци.сопственик_VALUE),"call " + симбол("method",Референци.부분들()));
                if (!호출형식.Аргументи.isEmpty()) ред.add("addl $" + 호출형식.Аргументи.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) ред.add("pushl %eax");
            } else if (Команда == 182) {
                метод_Референци Референци = класа_VALUE.Референци(наредба_податоци.두바이트());
                if (Референци.equals(new метод_Референци("java/lang/String","length","()I"))) Collections.addAll(ред,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Референци.equals(new метод_Референци("java/lang/String","charAt","(I)C"))) Collections.addAll(ред,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Превод_грешка("가상 ФУНКЦИЈА_VALUE 호출 미지원");
            } else if (Команда == 188) {
                if (наредба_податоци.한바이트() != 10) throw new Превод_грешка("new int[]만 Поддршка_VALUE"); Collections.addAll(ред,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Команда == 190) Collections.addAll(ред,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Команда == 196) {
                int наставка_VALUE = наредба_податоци.한바이트(), INDEX = наредба_податоци.두바이트(); провери_локален(INDEX,локален_COUNT);
                if (наставка_VALUE == 21 || наставка_VALUE == 25 || наставка_VALUE == 54 || наставка_VALUE == 58) ред.add((наставка_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (наставка_VALUE == 132) ред.add("addl $" + наредба_податоци.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Превод_грешка("wide Команда 미지원");
            } else if (Команда == 198 || Команда == 199) {
                int одредиште_VALUE = Позиција + наредба_податоци.부호두바이트(); гранка_Список.add(одредиште_VALUE); Collections.addAll(ред,"popl %eax","testl %eax, %eax",(Команда == 198 ? "je " : "jne ") + 표식 + "_b" + одредиште_VALUE);
            } else throw new Превод_грешка("미지원 Команда: " + Команда);
        }
        if (!경계들.containsAll(гранка_Список)) throw new Превод_грешка("Команда 경계가 아닌 곳으로 гранка");
        ред.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",ред);
    }
    String 엑스상수(класа_податоци податоци, int INDEX) {
        if (податоци.상수종류[INDEX] == 3) return податоци.константа_податоци[INDEX].toString();
        if (податоци.상수종류[INDEX] == 8) return низа_симбол(податоци.문자((Integer)податоци.константа_податоци[INDEX]));
        throw new Превод_грешка("정수와 низа_VALUE_6ca8363c 상수만 Поддршка_VALUE");
    }
    String 엑스조립본(String внес_поен, List<String> 내보냄, String цел) throws IOException {
        Map<String,String> машина_табела = new HashMap<>();
        for (String ред : Files.readAllLines(извор_патека.resolve("엑스기계함수.tsv"))) { String[] спари_VALUE = ред.split("\t"); if (спари_VALUE[0].equals(цел)) машина_табела.put(спари_VALUE[1] + спари_VALUE[2],спари_VALUE[3]); }
        int позиционирање_INDEX = внес_поен.lastIndexOf('.'); if (позиционирање_INDEX < 0) throw new Превод_грешка("внес_поен доделува_VALUE ГРЕШКА");
        String сопственик_VALUE = внес_поен.substring(0,позиционирање_INDEX).replace('.','/'), метод_внес_име = внес_поен.substring(позиционирање_INDEX + 1); метод_Референци внес_поен_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { метод_Референци Референци = new метод_Референци(сопственик_VALUE,метод_внес_име,서술); if (함수들.containsKey(Референци)) { if (внес_поен_VALUE != null) throw new Превод_грешка("겹친 внес_поен"); внес_поен_VALUE = Референци; } }
        if (внес_поен_VALUE == null || (함수들.get(внес_поен_VALUE).пристап_внес & 0x100) != 0) throw new Превод_грешка("внес_поен_VALUE ФУНКЦИЈА_VALUE формат_VALUE ГРЕШКА");
        List<String> ред = new ArrayList<>(); ред.add(".code32");
        for (класа_податоци податоци : 클래스들.values()) {
            String статус_VALUE = симбол("state",податоци.Име), иницијализирај = симбол("init",податоци.Име);
            Collections.addAll(ред,".bss",".balign 4",статус_VALUE + ": .long 0",".text",иницијализирај + ":","cmpl $0, " + статус_VALUE,"jne " + иницијализирај + "_done","movl $1, " + статус_VALUE);
            метод_Референци 초기화참조 = new метод_Референци(податоци.Име,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) ред.add("call " + симбол("method",초기화참조.부분들()));
            Collections.addAll(ред,"movl $2, " + статус_VALUE,иницијализирај + "_done:","ret");
            for (член_податоци поле_VALUE : податоци.поле_VALUE) {
                byte[] константа_VALUE = поле_VALUE.атрибут_VALUE.get("ConstantValue"); String VALUE = константа_VALUE == null ? "0" : 엑스상수(податоци,new податоци_Читач(константа_VALUE).두바이트());
                Collections.addAll(ред,".data",".balign 4",симбол("field",податоци.Име,поле_VALUE.Име,поле_VALUE.서술) + ": .long " + VALUE);
            }
            for (член_податоци ФУНКЦИЈА_VALUE : податоци.ФУНКЦИЈА_VALUE) if (!ФУНКЦИЈА_VALUE.Име.equals("<init>")) ред.add(엑스함수본문(new метод_Референци(податоци.Име,ФУНКЦИЈА_VALUE.Име,ФУНКЦИЈА_VALUE.서술),ФУНКЦИЈА_VALUE,машина_табела,цел));
        }
        Collections.addAll(ред,".text",".globl java_entry","java_entry:","call " + симбол("init",внес_поен_VALUE.сопственик_VALUE),"call " + симбол("method",внес_поен_VALUE.부분들()));
        if (внес_поен_VALUE.서술.equals("()V")) ред.add("xorl %eax, %eax"); ред.add("ret");
        for (String доделува_VALUE : 내보냄) {
            int разделник_VALUE_d8ba4873 = доделува_VALUE.indexOf('='); if (разделник_VALUE_d8ba4873 < 1) throw new Превод_грешка("내보내기 доделува_VALUE ГРЕШКА");
            String 외부 = доделува_VALUE.substring(0,разделник_VALUE_d8ba4873), ФУНКЦИЈА_VALUE = доделува_VALUE.substring(разделник_VALUE_d8ba4873 + 1); int делење_мерка = ФУНКЦИЈА_VALUE.lastIndexOf('.');
            if (делење_мерка < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Превод_грешка("내보내기 симбол ГРЕШКА");
            String класа_VALUE = ФУНКЦИЈА_VALUE.substring(0,делење_мерка).replace('.','/'), Име = ФУНКЦИЈА_VALUE.substring(делење_мерка + 1); метод_Референци селекција_VALUE = null;
            for (метод_Референци Референци : 함수들.keySet()) if (Референци.сопственик_VALUE.equals(класа_VALUE) && Референци.Име.equals(Име)) { if (селекција_VALUE != null) throw new Превод_грешка("겹친 내보내기 цел"); селекција_VALUE = Референци; }
            if (селекција_VALUE == null) throw new Превод_грешка("내보낼 함수가 없음");
            Collections.addAll(ред,".text",".globl " + 외부,외부 + ":","call " + симбол("init",селекција_VALUE.сопственик_VALUE),"jmp " + симбол("method",селекција_VALUE.부분들()));
        }
        ред.add(".section .rodata");
        for (Map.Entry<String,String> внес_VALUE : 문자열들.entrySet()) {
            Collections.addAll(ред,".balign 4",внес_VALUE.getValue() + ":",".long " + внес_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char единици_VALUE : внес_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(единици_VALUE)); if (!단위들.isEmpty()) ред.add(".long " + String.join(",",단위들));
        }
        ред.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",ред) + "\n";
    }
    static void Изврши_алатка(List<String> Команда) throws Exception {
        if (new ProcessBuilder(Команда).inheritIO().start().waitFor() != 0) throw new Превод_грешка("изгради_извор ГРЕШКА: " + Команда.get(0));
    }
    static String податоци_низа_f6a582f0(String Текст) { return "\"" + Текст.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String цел, String внес_поен, List<String> 내보냄, Path 출력, Path извор_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), класа_патека = 임시.resolve("classes"); Files.createDirectory(класа_патека);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",класа_патека.toString(),"-sourcepath",класа_патека.toString(),"-d",класа_патека.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int извор_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Превод_грешка("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); извор_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Превод_грешка(".java 또는 .class만 Поддршка_VALUE");
            }
            if (извор_COUNT > 0) Изврши_алатка(자바명령);
            try (java.util.stream.Stream<Path> патека_Список = Files.walk(класа_патека)) { патека_Список.filter(ПАТЕКА -> ПАТЕКА.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,цел.equals("user") ? "user" : "kernel",262144,извор_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(внес_поен,내보냄,цел); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path алатка_позиционирање = извор_VALUE.getParent();
            Изврши_алатка(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Изврши_алатка(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),алатка_позиционирање.resolve("заеднички_јазик_за_време_на_извршување_Поддршка.s").toString()));
            List<String> Врзи_се = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (цел.equals("kernel")) Врзи_се.add("-r");
            else {
                Изврши_алатка(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),алатка_позиционирање.resolve(цел.equals("user") ? "Start_корисник_програма.s" : "리눅스시작.s").toString()));
                Collections.addAll(Врзи_се,"-e","_start",임시.resolve("start.o").toString());
                if (цел.equals("user")) Collections.addAll(Врзи_се,"-T",алатка_позиционирање.resolve("корисник_Врска_Распоред.ld").toString());
            }
            Collections.addAll(Врзи_се,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Изврши_алатка(Врзи_се);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path објави_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),објави_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(објави_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(објави_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(цел.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> симбол_податоци = new ArrayList<>(), изворни_податоци = new ArrayList<>();
            for (метод_Референци Референци : CONVERT_VALUE.함수들.keySet()) симбол_податоци.add(податоци_низа_f6a582f0(симбол("method",Референци.부분들())) + ":" + податоци_низа_f6a582f0(Референци.сопственик_VALUE + "." + Референци.Име + Референци.서술));
            for (Path 입력 : 입력들) {
                byte[] хаш_датотека = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Текст = new StringBuilder(); for (byte VALUE : хаш_датотека) Текст.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                изворни_податоци.add(податоци_низа_f6a582f0(입력.toAbsolutePath().toString()) + ":" + податоци_низа_f6a582f0(Текст.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + податоци_низа_f6a582f0(цел) + ",\"entry\":" + податоци_низа_f6a582f0(внес_поен) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",симбол_податоци) + "},\"sources\":{" + String.join(",",изворни_податоци) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> патека_Список = Files.walk(임시)) { for (Path ПАТЕКА : (Iterable<Path>)патека_Список.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(ПАТЕКА); }
        }
    }
    public static void main(String[] Аргументи) {
        try {
            String внес_поен = null, цел = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> патека_Список = new ArrayList<>();
            for (int 순번 = 0; 순번 < Аргументи.length; 순번++) {
                String VALUE = Аргументи[순번];
                switch (VALUE) {
                    case "--target": 엑스대상 = Аргументи[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry класа_VALUE.ФУНКЦИЈА_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export симбол=класа_VALUE.ФУНКЦИЈА_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": внес_поен = Аргументи[++순번]; break;
                    case "--profile": цел = Аргументи[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Аргументи[++순번]); break;
                    case "--export": 내보냄.add(Аргументи[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Аргументи[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Превод_грешка("알 수 없는 옵션: " + VALUE); патека_Список.add(Paths.get(VALUE));
                }
            }
            if (внес_поен == null || 출력경로 == null || патека_Список.isEmpty()) throw new Превод_грешка("--entry, -o, класа_VALUE 파일이 필요합니다");
            Path извор_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Превод_грешка("알 수 없는 Изврши_наредба цел");
                엑스번역(патека_Список,엑스대상,внес_поен,내보냄,출력경로,извор_VALUE); return;
            }
            String ИЗВОР = new 기계어미리번역(патека_Список, цел, 낱말수, извор_VALUE).генерира(внес_поен, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ИЗВОР, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception ГРЕШКА) { System.err.println("изгради_извор ГРЕШКА: " + ГРЕШКА.getMessage()); System.exit(1); }
    }
}
