// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java класс_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. хост JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Тәрҗемә_итү_хата extends RuntimeException {
        Тәрҗемә_итү_хата(String 설명) { super(설명); }
    }
    static final class мәгълүмат_укучы {
        final byte[] мәгълүмат;
        int урнаштыру;
        мәгълүмат_укучы(byte[] 입력자료) { мәгълүмат = 입력자료; }
        byte[] 읽기(int озынлык_VALUE) {
            if (озынлык_VALUE < 0 || озынлык_VALUE > мәгълүмат.length - урнаштыру) throw new Тәрҗемә_итү_хата("잘린 класс_VALUE 또는 команда мәгълүмат");
            byte[] үлчәм = Arrays.copyOfRange(мәгълүмат, урнаштыру, урнаштыру + озынлык_VALUE); урнаштыру += озынлык_VALUE; return үлчәм;
        }
        int 한바이트() { if (урнаштыру >= мәгълүмат.length) throw new Тәрҗемә_итү_хата("잘린 команда мәгълүмат"); return мәгълүмат[урнаштыру++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class бүлек_мәгълүмат {
        final int керү_кертү;
        final String исем, 서술;
        final Map<String, byte[]> аергыч_VALUE_286d43f0;
        бүлек_мәгълүмат(int керү_VALUE, String исем_VALUE, String 서술값, Map<String, byte[]> аергыч_мәгълүмат) {
            керү_кертү = керү_VALUE; исем = исем_VALUE; 서술 = 서술값; аергыч_VALUE_286d43f0 = аергыч_мәгълүмат;
        }
    }
    static final class ысул_Белешмәлекләр implements Comparable<ысул_Белешмәлекләр> {
        final String биләүче_VALUE, исем, 서술;
        ысул_Белешмәлекләр(String 소유값, String исем_VALUE, String 서술값) { биләүче_VALUE = 소유값; исем = исем_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{биләүче_VALUE, исем, 서술}; }
        public int compareTo(ысул_Белешмәлекләр тиңдәш_VALUE) {
            int 비교값 = биләүче_VALUE.compareTo(тиңдәш_VALUE.биләүче_VALUE);
            if (비교값 == 0) 비교값 = исем.compareTo(тиңдәш_VALUE.исем);
            return 비교값 == 0 ? 서술.compareTo(тиңдәш_VALUE.서술) : 비교값;
        }
        public boolean equals(Object тиңдәш_VALUE) { return тиңдәш_VALUE instanceof ысул_Белешмәлекләр && compareTo((ысул_Белешмәлекләр) тиңдәш_VALUE) == 0; }
        public int hashCode() { return Objects.hash(биләүче_VALUE, исем, 서술); }
    }
    static final class класс_мәгълүмат {
        final int[] 상수종류;
        final Object[] константа_мәгълүмат;
        final String исем;
        final List<бүлек_мәгълүмат> кыр_VALUE, ФУНКЦИЯ_VALUE;
        класс_мәгълүмат(Path Yul) throws IOException {
            мәгълүмат_укучы укучы_VALUE = new мәгълүмат_укучы(Files.readAllBytes(Yul));
            if (укучы_VALUE.네바이트() != 0xcafebabe) throw new Тәрҗемә_итү_хата("Java класс_VALUE 표식이 아님");
            укучы_VALUE.읽기(4);
            int элемент_COUNT = укучы_VALUE.두바이트(); 상수종류 = new int[элемент_COUNT]; константа_мәгълүмат = new Object[элемент_COUNT];
            for (int 순번 = 1; 순번 < элемент_COUNT; 순번++) {
                int 종류 = укучы_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int озынлык_VALUE = укучы_VALUE.두바이트();
                        byte[] символ_буфер = укучы_VALUE.읽기(озынлык_VALUE), 길이붙인자료 = new byte[озынлык_VALUE + 2];
                        길이붙인자료[0] = (byte)(озынлык_VALUE >> 8); 길이붙인자료[1] = (byte)озынлык_VALUE;
                        System.arraycopy(символ_буфер, 0, 길이붙인자료, 2, озынлык_VALUE);
                        константа_мәгълүмат[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: константа_мәгълүмат[순번] = укучы_VALUE.네바이트(); break;
                    case 4: укучы_VALUE.읽기(4); break;
                    case 5: case 6: укучы_VALUE.읽기(8); 순번++; break;
                    case 7: case 8: case 16: константа_мәгълүмат[순번] = укучы_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        константа_мәгълүмат[순번] = new int[]{укучы_VALUE.두바이트(), укучы_VALUE.두바이트()}; break;
                    case 15: константа_мәгълүмат[순번] = new int[]{укучы_VALUE.한바이트(), укучы_VALUE.두바이트()}; break;
                    default: throw new Тәрҗемә_итү_хата("지원하지 않는 константа_VALUE 종류: " + 종류);
                }
            }
            укучы_VALUE.두바이트(); исем = класс_исем(укучы_VALUE.두바이트());
            if (!класс_исем(укучы_VALUE.두바이트()).equals("java/lang/Object") || укучы_VALUE.두바이트() != 0)
                throw new Тәрҗемә_итү_хата(исем + ": 상속 및 인터페이스 미지원");
            кыр_VALUE = 멤버읽기(укучы_VALUE); ФУНКЦИЯ_VALUE = 멤버읽기(укучы_VALUE); 속성읽기(укучы_VALUE);
            if (укучы_VALUE.урнаштыру != укучы_VALUE.мәгълүмат.length) throw new Тәрҗемә_итү_хата("класс_VALUE 뒤에 남은 мәгълүмат");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Тәрҗемә_итү_хата("문자 константа_VALUE INDEX Хата");
            return (String) константа_мәгълүмат[INDEX];
        }
        String класс_исем(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Тәрҗемә_итү_хата("класс_VALUE Белешмәлекләр Хата");
            return 문자((Integer)константа_мәгълүмат[INDEX]);
        }
        ысул_Белешмәлекләр Белешмәлекләр(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Тәрҗемә_итү_хата("멤버 Белешмәлекләр Хата");
            int[] тоташтыру_VALUE = (int[])константа_мәгълүмат[INDEX], исем_тоташтыру = (int[])константа_мәгълүмат[тоташтыру_VALUE[1]];
            return new ысул_Белешмәлекләр(класс_исем(тоташтыру_VALUE[0]), 문자(исем_тоташтыру[0]), 문자(исем_тоташтыру[1]));
        }
        Map<String, byte[]> 속성읽기(мәгълүмат_укучы укучы_VALUE) {
            Map<String, byte[]> үлчәм = new LinkedHashMap<>();
            int элемент_COUNT = укучы_VALUE.두바이트();
            for (int 순번 = 0; 순번 < элемент_COUNT; 순번++) {
                String аергыч_исем = 문자(укучы_VALUE.두바이트()); byte[] VALUE = укучы_VALUE.읽기(укучы_VALUE.네바이트());
                if (үлчәм.put(аергыч_исем, VALUE) != null) throw new Тәрҗемә_итү_хата("겹친 аергыч_VALUE_286d43f0: " + аергыч_исем);
            }
            return үлчәм;
        }
        List<бүлек_мәгълүмат> 멤버읽기(мәгълүмат_укучы укучы_VALUE) {
            List<бүлек_мәгълүмат> үлчәм = new ArrayList<>(); int элемент_COUNT = укучы_VALUE.두바이트();
            for (int 순번 = 0; 순번 < элемент_COUNT; 순번++) {
                int керү_кертү = укучы_VALUE.두바이트(); String ысул_кертү_исем = 문자(укучы_VALUE.두바이트()), 서술 = 문자(укучы_VALUE.두바이트());
                үлчәм.add(new бүлек_мәгълүмат(керү_кертү, ысул_кертү_исем, 서술, 속성읽기(укучы_VALUE)));
            }
            return үлчәм;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String кайтару_үлчәм;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Тәрҗемә_итү_хата("ФУНКЦИЯ_VALUE 서술 Хата: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Тәрҗемә_итү_хата("ФУНКЦИЯ_VALUE 서술 Хата: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Тәрҗемә_итү_хата("ФУНКЦИЯ_VALUE 서술 Хата: " + 서술);
            кайтару_үлчәм = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> үлчәм = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int урнаштыру = 0; урнаштыру < 서술.length();) {
            String тамгаланган_өлеш_VALUE = null;
            for (String формат_VALUE : 허용형식) if (서술.startsWith(формат_VALUE, урнаштыру)) { тамгаланган_өлеш_VALUE = формат_VALUE; break; }
            if (тамгаланган_өлеш_VALUE == null) throw new Тәрҗемә_итү_хата("지원하지 않는 мәгълүмат_төре: " + 서술);
            үлчәм.add(тамгаланган_өлеш_VALUE); урнаштыру += тамгаланган_өлеш_VALUE.length();
        }
        return үлчәм;
    }
    static String символ(String 종류, String... 부분들) {
        try {
            byte[] Хәш_файл = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Mäten = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Mäten.append(String.format(Locale.ROOT, "%02x", Хәш_файл[순번] & 255));
            return Mäten.toString();
        } catch (Exception Хата) { throw new Тәрҗемә_итү_хата(Хата.toString()); }
    }
    final Map<String, класс_мәгълүмат> 클래스들 = new TreeMap<>();
    final Map<ысул_Белешмәлекләр, бүлек_мәгълүмат> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, машина_класс;
    final int 동적기억낱말수;
    final Path ресурс_юл;
    기계어미리번역(List<Path> юл_Исемлек_4d1a5003, String максат_кыйммәт, int 낱말수, Path ресурс_VALUE) throws IOException {
        if ((!максат_кыйммәт.equals("kernel") && !максат_кыйммәт.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Тәрҗемә_итү_хата("үтәргә_команда максат_кыйммәт 또는 Хәтер_VALUE 공간 үлчәмен_үзгәртү Хата");
        실행대상 = максат_кыйммәт; 동적기억낱말수 = 낱말수; ресурс_юл = ресурс_VALUE;
        // 이 이름도 국가별 чыганак_агач булдыру 시 해당 언어로 옮긴다.
        машина_класс = максат_кыйммәт.equals("kernel") ? "такта" : "кулланучы";
        for (String юл : Files.readAllLines(ресурс_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = юл.split("\t", -1);
            if (부분들.length != 4) throw new Тәрҗемә_итү_хата("машина ФУНКЦИЯ_VALUE мәгълүмат Хата");
            if (부분들[0].equals(максат_кыйммәт)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Yul : юл_Исемлек_4d1a5003) {
            класс_мәгълүмат мәгълүмат = new класс_мәгълүмат(Yul);
            if (클래스들.put(мәгълүмат.исем, мәгълүмат) != null) throw new Тәрҗемә_итү_хата("중복 класс_VALUE: " + мәгълүмат.исем);
            for (бүлек_мәгълүмат кыр_VALUE : мәгълүмат.кыр_VALUE) {
                if ((кыр_VALUE.керү_кертү & 8) == 0 || 형식읽기(кыр_VALUE.서술).equals(Collections.singletonList("V"))) throw new Тәрҗемә_итү_хата("статик_VALUE 필드만 ярдәм_VALUE");
                if (필드들.put(new ысул_Белешмәлекләр(мәгълүмат.исем, кыр_VALUE.исем, кыр_VALUE.서술), кыр_VALUE) != null) throw new Тәрҗемә_итү_хата("중복 кыр_VALUE");
            }
            for (бүлек_мәгълүмат ФУНКЦИЯ_VALUE : мәгълүмат.ФУНКЦИЯ_VALUE) {
                if (ФУНКЦИЯ_VALUE.исем.equals("<init>")) continue;
                if ((ФУНКЦИЯ_VALUE.керү_кертү & 8) == 0 || (ФУНКЦИЯ_VALUE.керү_кертү & (0x20 | 0x400)) != 0) throw new Тәрҗемә_итү_хата("статик_VALUE 비동기화 함수만 ярдәм_VALUE");
                new 함수형식(ФУНКЦИЯ_VALUE.서술);
                if (함수들.put(new ысул_Белешмәлекләр(мәгълүмат.исем, ФУНКЦИЯ_VALUE.исем, ФУНКЦИЯ_VALUE.서술), ФУНКЦИЯ_VALUE) != null) throw new Тәрҗемә_итү_хата("중복 ФУНКЦИЯ_VALUE");
            }
        }
    }
    String юл_символ(String Mäten) { return 문자열들.computeIfAbsent(Mäten, VALUE -> "j_text_" + 문자열들.size()); }
    String константа_аңлатма(класс_мәгълүмат мәгълүмат, int INDEX) {
        if (INDEX < 1 || INDEX >= мәгълүмат.상수종류.length) throw new Тәрҗемә_итү_хата("константа_VALUE INDEX клип Хата");
        if (мәгълүмат.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + мәгълүмат.константа_мәгълүмат[INDEX] + ")";
        if (мәгълүмат.상수종류[INDEX] == 8) return "(word)" + юл_символ(мәгълүмат.문자((Integer)мәгълүмат.константа_мәгълүмат[INDEX]));
        throw new Тәрҗемә_итү_хата("정수와 юл_VALUE_6ca8363c 상수만 ярдәм_VALUE");
    }
    String 함수원형(ысул_Белешмәлекләр Белешмәлекләр) {
        List<String> 인수들 = new ArrayList<>(); int элемент_COUNT = new 함수형식(Белешмәлекләр.서술).인수.size();
        for (int 순번 = 0; 순번 < элемент_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + символ("method", Белешмәлекләр.부분들()) + "(" + (элемент_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void чек_локаль(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Тәрҗемә_итү_хата("локаль_даирә 변수 INDEX клип Хата"); }
    void 분기넣기(List<String> 출력, Set<Integer> тармак_Исемлек, int урнаштыру, int 이동량, String шарт) {
        int күчерү_урыны_VALUE = урнаштыру + 이동량; тармак_Исемлек.add(күчерү_урыны_VALUE);
        출력.add((шарт == null ? "" : "if (" + шарт + ") ") + "goto b" + күчерү_урыны_VALUE + ";");
    }
    String 함수본문(ысул_Белешмәлекләр ФУНКЦИЯ_VALUE, бүлек_мәгълүмат мәгълүмат) {
        byte[] 본문자료 = мәгълүмат.аергыч_VALUE_286d43f0.get("Code"); if (본문자료 == null) throw new Тәрҗемә_итү_хата("ФУНКЦИЯ_VALUE 몸체가 없음: " + ФУНКЦИЯ_VALUE.исем);
        мәгълүмат_укучы укучы_VALUE = new мәгълүмат_укучы(본문자료); int 쌓임깊이 = укучы_VALUE.두바이트(), 지역변수수 = укучы_VALUE.두바이트();
        мәгълүмат_укучы команда_мәгълүмат = new мәгълүмат_укучы(укучы_VALUE.읽기(укучы_VALUE.네바이트()));
        if (укучы_VALUE.두바이트() != 0) throw new Тәрҗемә_итү_хата("try/catch/finally 미지원");
        함수형식 формат_VALUE = new 함수형식(ФУНКЦИЯ_VALUE.서술); if (지역변수수 < формат_VALUE.인수.size()) throw new Тәрҗемә_итү_хата("매개변수보다 적은 локаль_даирә 변수");
        класс_мәгълүмат класс_VALUE = 클래스들.get(ФУНКЦИЯ_VALUE.биләүче_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(ФУНКЦИЯ_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < формат_VALUE.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), тармак_Исемлек = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (команда_мәгълүмат.урнаштыру < команда_мәгълүмат.мәгълүмат.length) {
            int урнаштыру = команда_мәгълүмат.урнаштыру, команда = команда_мәгълүмат.한바이트(); 경계들.add(урнаштыру); 출력.add("b" + урнаштыру + ":;");
            if (команда == 0) continue;
            if (команда == 1) 출력.add("PUSH(0);");
            else if (команда >= 2 && команда <= 8) 출력.add("PUSH((uint32_t)(" + (команда - 3) + "));");
            else if (команда == 16 || команда == 17) 출력.add("PUSH((uint32_t)(" + (команда == 16 ? команда_мәгълүмат.부호한바이트() : команда_мәгълүмат.부호두바이트()) + "));");
            else if (команда == 18 || команда == 19) 출력.add("PUSH(" + константа_аңлатма(класс_VALUE, команда == 18 ? команда_мәгълүмат.한바이트() : команда_мәгълүмат.두바이트()) + ");");
            else if (команда == 21 || команда == 25 || (команда >= 26 && команда <= 29) || (команда >= 42 && команда <= 45)) {
                int INDEX = команда == 21 || команда == 25 ? команда_мәгълүмат.한바이트() : команда - (команда <= 29 ? 26 : 42);
                чек_локаль(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (команда == 54 || команда == 58 || (команда >= 59 && команда <= 62) || (команда >= 75 && команда <= 78)) {
                int INDEX = команда == 54 || команда == 58 ? команда_мәгълүмат.한바이트() : команда - (команда <= 62 ? 59 : 75);
                чек_локаль(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (команда == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (команда == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (команда == 87 || команда == 88) 출력.add(команда == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (команда >= 89 && команда <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] тәртипкә_салу_Исемлек = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[команда - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : тәртипкә_салу_Исемлек[команда - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (команда == 96 || команда == 100 || команда == 104 || команда == 126 || команда == 128 || команда == 130) {
                String гамәл_VALUE = команда == 96 ? "+" : команда == 100 ? "-" : команда == 104 ? "*" : команда == 126 ? "&" : команда == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + гамәл_VALUE + " (uint32_t)b);");
            } else if (команда == 108 || команда == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (команда == 112 ? 1 : 0) + "));");
            else if (команда == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (команда == 120 || команда == 122 || команда == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (команда == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (команда == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (команда == 132) {
                int INDEX = команда_мәгълүмат.한바이트(), 증가량 = команда_мәгълүмат.부호한바이트(); чек_локаль(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (команда >= 145 && команда <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (команда == 145 ? "int8_t" : команда == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (команда >= 153 && команда <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, тармак_Исемлек, урнаштыру, команда_мәгълүмат.부호두바이트(), "(int32_t)a " + 비교들[команда - 153] + " 0");
            } else if (команда >= 159 && команда <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, тармак_Исемлек, урнаштыру, команда_мәгълүмат.부호두바이트(), команда >= 165 ? "a " + 비교들[команда - 159] + " b" : "(int32_t)a " + 비교들[команда - 159] + " (int32_t)b");
            } else if (команда == 167 || команда == 200) 분기넣기(출력, тармак_Исемлек, урнаштыру, команда == 167 ? команда_мәгълүмат.부호두바이트() : команда_мәгълүмат.네바이트(), null);
            else if (команда == 170 || команда == 171) {
                while (команда_мәгълүмат.урнаштыру % 4 != 0) команда_мәгълүмат.한바이트();
                int килешенгәнчә_кыйммәт = команда_мәгълүмат.네바이트(); 출력.add("a = POP();");
                if (команда == 170) {
                    int 아래 = команда_мәгълүмат.네바이트(), 위 = команда_мәгълүмат.네바이트(); long элемент_COUNT = (long)위 - 아래 + 1;
                    if (элемент_COUNT < 1 || элемент_COUNT > (команда_мәгълүмат.мәгълүмат.length - команда_мәгълүмат.урнаштыру) / 4) throw new Тәрҗемә_итү_хата("switch клип Хата");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, тармак_Исемлек, урнаштыру, команда_мәгълүмат.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int элемент_COUNT = команда_мәгълүмат.네바이트(), 앞값 = 0;
                    if (элемент_COUNT < 0 || элемент_COUNT > (команда_мәгълүмат.мәгълүмат.length - команда_мәгълүмат.урнаштыру) / 8) throw new Тәрҗемә_итү_хата("switch үлчәмен_үзгәртү Хата");
                    for (int 순번 = 0; 순번 < элемент_COUNT; 순번++) {
                        int VALUE = команда_мәгълүмат.네바이트(); if (순번 > 0 && VALUE <= 앞값) throw new Тәрҗемә_итү_хата("switch тәртипкә_салу_VALUE Хата"); 앞값 = VALUE;
                        분기넣기(출력, тармак_Исемлек, урнаштыру, команда_мәгълүмат.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, тармак_Исемлек, урнаштыру, килешенгәнчә_кыйммәт, null);
            } else if (команда == 172 || команда == 176 || команда == 177) 출력.add("return " + (команда == 177 ? "0" : "POP()") + ";");
            else if (команда == 178 || команда == 179) {
                ысул_Белешмәлекләр Белешмәлекләр = класс_VALUE.Белешмәлекләр(команда_мәгълүмат.두바이트()); if (!필드들.containsKey(Белешмәлекләр)) throw new Тәрҗемә_итү_хата("알 수 없는 кыр_VALUE");
                출력.add(символ("init", Белешмәлекләр.биләүче_VALUE) + "();"); String кыр_VALUE = символ("field", Белешмәлекләр.부분들());
                출력.add(команда == 178 ? "PUSH(" + кыр_VALUE + ");" : кыр_VALUE + " = POP();");
            } else if (команда == 184) {
                ысул_Белешмәлекләр Белешмәлекләр = класс_VALUE.Белешмәлекләр(команда_мәгълүмат.두바이트()); if (!함수들.containsKey(Белешмәлекләр)) throw new Тәрҗемә_итү_хата("알 수 없는 ФУНКЦИЯ_VALUE");
                함수형식 호출형식 = new 함수형식(Белешмәлекләр.서술); int элемент_COUNT = 호출형식.인수.size();
                출력.add(символ("init", Белешмәлекләр.биләүче_VALUE) + "();"); 출력.add("if(sp < " + элемент_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + элемент_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < элемент_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + символ("method", Белешмәлекләр.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.кайтару_үлчәм.equals("V")) 출력.add("PUSH(a);");
            } else if (команда == 182) {
                ысул_Белешмәлекләр Белешмәлекләр = класс_VALUE.Белешмәлекләр(команда_мәгълүмат.두바이트());
                if (Белешмәлекләр.equals(new ысул_Белешмәлекләр("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Белешмәлекләр.equals(new ысул_Белешмәлекләр("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Тәрҗемә_итү_хата("가상 ФУНКЦИЯ_VALUE 호출 미지원");
            } else if (команда == 188) {
                if (команда_мәгълүмат.한바이트() != 10) throw new Тәрҗемә_итү_хата("new int[]만 ярдәм_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (команда == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (команда == 196) {
                int өстәмә_VALUE = команда_мәгълүмат.한바이트(), INDEX = команда_мәгълүмат.두바이트(); чек_локаль(INDEX, 지역변수수);
                if (өстәмә_VALUE == 21 || өстәмә_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (өстәмә_VALUE == 54 || өстәмә_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (өстәмә_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + команда_мәгълүмат.부호두바이트() + ");");
                else throw new Тәрҗемә_итү_хата("미지원 wide команда");
            } else if (команда == 198 || команда == 199) {
                출력.add("a = POP();"); 분기넣기(출력, тармак_Исемлек, урнаштыру, команда_мәгълүмат.부호두바이트(), "a " + (команда == 198 ? "==" : "!=") + " 0");
            } else throw new Тәрҗемә_итү_хата(ФУНКЦИЯ_VALUE.биләүче_VALUE + "." + ФУНКЦИЯ_VALUE.исем + ", байт_VALUE " + урнаштыру + ": 미지원 команда " + команда);
        }
        if (!경계들.containsAll(тармак_Исемлек)) throw new Тәрҗемә_итү_хата("команда 경계가 아닌 곳으로 тармак");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String экспортлау_ысул(String бәйләү_символ, String максат_кыйммәт, boolean 진입점여부) {
        int урнаштыру_INDEX = максат_кыйммәт.lastIndexOf('.'); if (урнаштыру_INDEX < 0 || !бәйләү_символ.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Тәрҗемә_итү_хата("내보내기 지정 Хата");
        String биләүче_VALUE = максат_кыйммәт.substring(0, урнаштыру_INDEX).replace('.', '/'), исем = максат_кыйммәт.substring(урнаштыру_INDEX + 1); ысул_Белешмәлекләр тамгаланган_өлеш_VALUE = null;
        for (ысул_Белешмәлекләр Белешмәлекләр : 함수들.keySet()) if (Белешмәлекләр.биләүче_VALUE.equals(биләүче_VALUE) && Белешмәлекләр.исем.equals(исем)) {
            if (тамгаланган_өлеш_VALUE != null) throw new Тәрҗемә_итү_хата("겹친 내보내기 максат_кыйммәт"); тамгаланган_өлеш_VALUE = Белешмәлекләр;
        }
        if (тамгаланган_өлеш_VALUE == null || (함수들.get(тамгаланган_өлеш_VALUE).керү_кертү & 0x100) != 0) throw new Тәрҗемә_итү_хата("내보낼 함수가 없음 또는 native ФУНКЦИЯ_VALUE");
        함수형식 формат_VALUE = new 함수형식(тамгаланган_өлеш_VALUE.서술);
        if ((진입점여부 && !формат_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(формат_VALUE.кайтару_үлчәм)) throw new Тәрҗемә_итү_хата("кертү_балл_VALUE 또는 C 경계 формат_VALUE Хата");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < формат_VALUE.인수.size(); 순번++) {
            if (!формат_VALUE.인수.get(순번).equals("I")) throw new Тәрҗемә_итү_хата("C 경계는 int 인수만 ярдәм_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (формат_VALUE.кайтару_үлчәм.equals("V") ? "void " : "int32_t ") + бәйләү_символ + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + символ("init", тамгаланган_өлеш_VALUE.биләүче_VALUE) + "(); " + (формат_VALUE.кайтару_үлчәм.equals("V") ? "" : "return (int32_t)") + символ("method", тамгаланган_өлеш_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String булдыру(String кертү_балл, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<ысул_Белешмәлекләр, бүлек_мәгълүмат> кертү_VALUE : 함수들.entrySet()) {
            ысул_Белешмәлекләр Белешмәлекләр = кертү_VALUE.getKey(); бүлек_мәгълүмат мәгълүмат = кертү_VALUE.getValue(); 선언들.add(함수원형(Белешмәлекләр) + ";");
            if ((мәгълүмат.керү_кертү & 0x100) != 0) {
                String ялгау = 기계함수들.get(Белешмәлекләр.исем + Белешмәлекләр.서술);
                if (!Белешмәлекләр.биләүче_VALUE.equals(машина_класс) || ялгау == null) throw new Тәрҗемә_итү_хата("허용되지 않은 native ФУНКЦИЯ_VALUE: " + Белешмәлекләр.исем);
                int элемент_COUNT = new 함수형식(Белешмәлекләр.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < элемент_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + ялгау + "(" + (элемент_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(элемент_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Белешмәлекләр) + " { return " + ялгау + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Белешмәлекләр, мәгълүмат));
        }
        for (Map.Entry<ысул_Белешмәлекләр, бүлек_мәгълүмат> кертү_VALUE : 필드들.entrySet()) {
            ысул_Белешмәлекләр Белешмәлекләр = кертү_VALUE.getKey(); byte[] константа_VALUE = кертү_VALUE.getValue().аергыч_VALUE_286d43f0.get("ConstantValue");
            String VALUE = константа_VALUE == null ? "0" : константа_аңлатма(클래스들.get(Белешмәлекләр.биләүче_VALUE), new мәгълүмат_укучы(константа_VALUE).두바이트());
            필드선언들.add("static word " + символ("field", Белешмәлекләр.부분들()) + " = " + VALUE + ";");
        }
        for (String исем : 클래스들.keySet()) {
            String инициализацияләү = символ("init", исем), халәт_VALUE = символ("state", исем);
            선언들.add("static void " + инициализацияләү + "(void);"); 필드선언들.add("static unsigned " + халәт_VALUE + ";");
            ысул_Белешмәлекләр Белешмәлекләр = new ысул_Белешмәлекләр(исем, "<clinit>", "()V");
            몸체들.add("static void " + инициализацияләү + "(void) { if(" + халәт_VALUE + ") return; " + халәт_VALUE + " = 1; " + (함수들.containsKey(Белешмәлекләр) ? символ("method", Белешмәлекләр.부분들()) + "(); " : "") + халәт_VALUE + " = 2; }");
        }
        몸체들.add(экспортлау_ысул("java_entry", кертү_балл, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int урнаштыру_INDEX = 지정.indexOf('='); if (урнаштыру_INDEX < 1) throw new Тәрҗемә_итү_хата("내보내기 지정 Хата");
            String исем = 지정.substring(0, урнаштыру_INDEX); 공개이름.add(исем); 몸체들.add(экспортлау_ысул(исем, 지정.substring(урнаштыру_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> кертү_VALUE : 문자열들.entrySet()) {
            String Mäten = кертү_VALUE.getKey(); StringBuilder МАССИВ_VALUE = new StringBuilder("static const word " + кертү_VALUE.getValue() + "[] = {" + Mäten.length());
            for (int 순번 = 0; 순번 < Mäten.length(); 순번++) МАССИВ_VALUE.append(", ").append((int)Mäten.charAt(순번));
            문자열선언들.add(МАССИВ_VALUE.append("};").toString());
        }
        String ярдәм_VALUE = Files.readString(ресурс_юл.resolve("CLR_мохите_ярдәм.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(ярдәм_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String чыганак, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> исем_таблица = new HashMap<>();
        for (String юл : Files.readAllLines(ресурс_юл.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] тоташтыру_VALUE = юл.split("\t"); исем_таблица.put(тоташтыру_VALUE[0], тоташтыру_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(чыганак); StringBuffer үлчәм = new StringBuffer();
        while (찾개.find()) {
            String исем = 찾개.group(), 새이름 = исем;
            if (!исем.startsWith("//") && !исем.startsWith("/*") && !исем.startsWith("\"") && !исем.startsWith("'") && !공개이름.contains(исем)) {
                새이름 = исем_таблица.getOrDefault(исем, исем);
                if (исем.matches("a[0-9]+")) 새이름 = "인수" + исем.substring(1);
                if (исем.matches("b[0-9]+")) 새이름 = "тармак" + исем.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char символ_VALUE_068c2631 : 새이름.toCharArray()) 표기.append(символ_VALUE_068c2631 < 128 ? Character.toString(символ_VALUE_068c2631) : String.format(Locale.ROOT, "\\u%04x", (int)символ_VALUE_068c2631));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(үлчәм, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(үлчәм); return үлчәм.toString();
    }
    String 엑스함수본문(ысул_Белешмәлекләр ФУНКЦИЯ_VALUE, бүлек_мәгълүмат мәгълүмат, Map<String,String> машина_таблица, String максат_кыйммәт) {
        String 표식 = символ("method", ФУНКЦИЯ_VALUE.부분들());
        List<String> юл = new ArrayList<>();
        if ((мәгълүмат.керү_кертү & 0x100) != 0) {
            String ялгау = машина_таблица.get(ФУНКЦИЯ_VALUE.исем + ФУНКЦИЯ_VALUE.서술);
            if (!ФУНКЦИЯ_VALUE.биләүче_VALUE.equals(максат_кыйммәт.equals("kernel") ? "мобиль_VALUE" : "кулланучы") || ялгау == null) throw new Тәрҗемә_итү_хата("허용되지 않은 native ФУНКЦИЯ_VALUE");
            return ".text\n" + 표식 + ":\njmp " + ялгау;
        }
        byte[] төп_текст = мәгълүмат.аергыч_VALUE_286d43f0.get("Code"); if (төп_текст == null) throw new Тәрҗемә_итү_хата("ФУНКЦИЯ_VALUE 몸체가 없음");
        мәгълүмат_укучы укучы_VALUE = new мәгълүмат_укучы(төп_текст); укучы_VALUE.두바이트(); int локаль_COUNT = укучы_VALUE.두바이트();
        мәгълүмат_укучы команда_мәгълүмат = new мәгълүмат_укучы(укучы_VALUE.읽기(укучы_VALUE.네바이트()));
        if (укучы_VALUE.두바이트() != 0) throw new Тәрҗемә_итү_хата("try/catch/finally 미지원");
        함수형식 формат_VALUE = new 함수형식(ФУНКЦИЯ_VALUE.서술); if (локаль_COUNT < формат_VALUE.인수.size()) throw new Тәрҗемә_итү_хата("매개변수보다 적은 локаль_даирә 변수");
        Collections.addAll(юл,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + локаль_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < формат_VALUE.인수.size(); 순번++) Collections.addAll(юл,"movl " + (8 + 4 * (формат_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        класс_мәгълүмат класс_VALUE = 클래스들.get(ФУНКЦИЯ_VALUE.биләүче_VALUE); Set<Integer> 경계들 = new HashSet<>(), тармак_Исемлек = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (команда_мәгълүмат.урнаштыру < команда_мәгълүмат.мәгълүмат.length) {
            int урнаштыру = команда_мәгълүмат.урнаштыру, команда = команда_мәгълүмат.한바이트(); String урнаштыру_INDEX = 표식 + "_b" + урнаштыру;
            юл.add(урнаштыру_INDEX + ":"); 경계들.add(урнаштыру);
            if (команда == 0) юл.add("nop");
            else if (команда == 1) юл.add("pushl $0");
            else if (команда >= 2 && команда <= 8) юл.add("pushl $" + (команда - 3));
            else if (команда == 16 || команда == 17) юл.add("pushl $" + (команда == 16 ? команда_мәгълүмат.부호한바이트() : команда_мәгълүмат.부호두바이트()));
            else if (команда == 18 || команда == 19) {
                int INDEX = команда == 18 ? команда_мәгълүмат.한바이트() : команда_мәгълүмат.두바이트();
                юл.add("pushl $" + 엑스상수(класс_VALUE,INDEX));
            } else if (команда == 21 || команда == 25 || (команда >= 26 && команда <= 29) || (команда >= 42 && команда <= 45) || команда == 54 || команда == 58 || (команда >= 59 && команда <= 62) || (команда >= 75 && команда <= 78)) {
                boolean 읽음 = команда < 54; int INDEX = команда == 21 || команда == 25 || команда == 54 || команда == 58 ? команда_мәгълүмат.한바이트() : команда - (команда <= 29 ? 26 : команда <= 45 ? 42 : команда <= 62 ? 59 : 75);
                чек_локаль(INDEX,локаль_COUNT); юл.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (команда == 46) Collections.addAll(юл,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (команда == 79) Collections.addAll(юл,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (команда == 87 || команда == 88) юл.add("addl $" + (команда == 87 ? 4 : 8) + ", %esp");
            else if (команда >= 89 && команда <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] тәртипкә_салу_Исемлек = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[команда - 89]; 순번++) юл.add("popl " + 저장기들[순번]);
                for (int 순번 : тәртипкә_салу_Исемлек[команда - 89]) юл.add("pushl " + 저장기들[순번]);
            } else if (команда == 96 || команда == 100 || команда == 104 || команда == 126 || команда == 128 || команда == 130) {
                String гамәл_VALUE = команда == 96 ? "addl" : команда == 100 ? "subl" : команда == 104 ? "imull" : команда == 126 ? "andl" : команда == 128 ? "orl" : "xorl";
                Collections.addAll(юл,"popl %ecx","popl %eax",гамәл_VALUE + " %ecx, %eax","pushl %eax");
            } else if (команда == 108 || команда == 112) Collections.addAll(юл,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + урнаштыру_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + урнаштыру_INDEX + "_divide","xorl %edx, %edx","jmp " + урнаштыру_INDEX + "_done",урнаштыру_INDEX + "_divide:","cltd","idivl %ecx",урнаштыру_INDEX + "_done:","pushl " + (команда == 108 ? "%eax" : "%edx"));
            else if (команда == 116) юл.add("negl (%esp)");
            else if (команда == 120 || команда == 122 || команда == 124) Collections.addAll(юл,"popl %ecx","popl %eax",(команда == 120 ? "sall" : команда == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (команда == 132) {
                int INDEX = команда_мәгълүмат.한바이트(), 증가 = команда_мәгълүмат.부호한바이트(); чек_локаль(INDEX,локаль_COUNT); юл.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (команда >= 145 && команда <= 147) Collections.addAll(юл,"popl %eax",команда == 145 ? "movsbl %al, %eax" : команда == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (команда >= 153 && команда <= 166) {
                if (команда <= 158) Collections.addAll(юл,"popl %eax","testl %eax, %eax");
                else Collections.addAll(юл,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int күчерү_урыны_VALUE = урнаштыру + команда_мәгълүмат.부호두바이트(); тармак_Исемлек.add(күчерү_урыны_VALUE); юл.add(비교들[команда - (команда <= 158 ? 153 : 159)] + " " + 표식 + "_b" + күчерү_урыны_VALUE);
            } else if (команда == 167 || команда == 200) {
                int күчерү_урыны_VALUE = урнаштыру + (команда == 167 ? команда_мәгълүмат.부호두바이트() : команда_мәгълүмат.네바이트()); тармак_Исемлек.add(күчерү_урыны_VALUE); юл.add("jmp " + 표식 + "_b" + күчерү_урыны_VALUE);
            } else if (команда == 170 || команда == 171) {
                while (команда_мәгълүмат.урнаштыру % 4 != 0) команда_мәгълүмат.한바이트();
                int килешенгәнчә_кыйммәт = урнаштыру + команда_мәгълүмат.네바이트(); тармак_Исемлек.add(килешенгәнчә_кыйммәт); юл.add("popl %eax");
                int элемент_COUNT, 아래 = 0;
                if (команда == 170) { 아래 = команда_мәгълүмат.네바이트(); int 위 = команда_мәгълүмат.네바이트(); long озынлык_VALUE = (long)위 - 아래 + 1; if (озынлык_VALUE < 1 || озынлык_VALUE > (команда_мәгълүмат.мәгълүмат.length - команда_мәгълүмат.урнаштыру) / 4) throw new Тәрҗемә_итү_хата("switch клип Хата"); элемент_COUNT = (int)озынлык_VALUE; }
                else { элемент_COUNT = команда_мәгълүмат.네바이트(); if (элемент_COUNT < 0 || элемент_COUNT > (команда_мәгълүмат.мәгълүмат.length - команда_мәгълүмат.урнаштыру) / 8) throw new Тәрҗемә_итү_хата("switch үлчәмен_үзгәртү Хата"); }
                for (int 순번 = 0; 순번 < элемент_COUNT; 순번++) {
                    int VALUE = команда == 170 ? 아래 + 순번 : команда_мәгълүмат.네바이트(), күчерү_урыны_VALUE = урнаштыру + команда_мәгълүмат.네바이트(); тармак_Исемлек.add(күчерү_урыны_VALUE);
                    Collections.addAll(юл,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + күчерү_урыны_VALUE);
                }
                юл.add("jmp " + 표식 + "_b" + килешенгәнчә_кыйммәт);
            } else if (команда == 172 || команда == 176 || команда == 177) {
                if (команда != 177) юл.add("popl %eax"); Collections.addAll(юл,"leave","ret");
            } else if (команда == 178 || команда == 179) {
                ысул_Белешмәлекләр Белешмәлекләр = класс_VALUE.Белешмәлекләр(команда_мәгълүмат.두바이트()); if (!필드들.containsKey(Белешмәлекләр)) throw new Тәрҗемә_итү_хата("알 수 없는 кыр_VALUE");
                Collections.addAll(юл,"call " + символ("init",Белешмәлекләр.биләүче_VALUE),(команда == 178 ? "pushl " : "popl ") + символ("field",Белешмәлекләр.부분들()));
            } else if (команда == 184) {
                ысул_Белешмәлекләр Белешмәлекләр = класс_VALUE.Белешмәлекләр(команда_мәгълүмат.두바이트()); if (!함수들.containsKey(Белешмәлекләр)) throw new Тәрҗемә_итү_хата("알 수 없는 ФУНКЦИЯ_VALUE");
                함수형식 호출형식 = new 함수형식(Белешмәлекләр.서술); Collections.addAll(юл,"call " + символ("init",Белешмәлекләр.биләүче_VALUE),"call " + символ("method",Белешмәлекләр.부분들()));
                if (!호출형식.인수.isEmpty()) юл.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.кайтару_үлчәм.equals("V")) юл.add("pushl %eax");
            } else if (команда == 182) {
                ысул_Белешмәлекләр Белешмәлекләр = класс_VALUE.Белешмәлекләр(команда_мәгълүмат.두바이트());
                if (Белешмәлекләр.equals(new ысул_Белешмәлекләр("java/lang/String","length","()I"))) Collections.addAll(юл,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Белешмәлекләр.equals(new ысул_Белешмәлекләр("java/lang/String","charAt","(I)C"))) Collections.addAll(юл,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Тәрҗемә_итү_хата("가상 ФУНКЦИЯ_VALUE 호출 미지원");
            } else if (команда == 188) {
                if (команда_мәгълүмат.한바이트() != 10) throw new Тәрҗемә_итү_хата("new int[]만 ярдәм_VALUE"); Collections.addAll(юл,"popl %eax","call rt_new_array","pushl %eax");
            } else if (команда == 190) Collections.addAll(юл,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (команда == 196) {
                int өстәмә_VALUE = команда_мәгълүмат.한바이트(), INDEX = команда_мәгълүмат.두바이트(); чек_локаль(INDEX,локаль_COUNT);
                if (өстәмә_VALUE == 21 || өстәмә_VALUE == 25 || өстәмә_VALUE == 54 || өстәмә_VALUE == 58) юл.add((өстәмә_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (өстәмә_VALUE == 132) юл.add("addl $" + команда_мәгълүмат.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Тәрҗемә_итү_хата("wide команда 미지원");
            } else if (команда == 198 || команда == 199) {
                int күчерү_урыны_VALUE = урнаштыру + команда_мәгълүмат.부호두바이트(); тармак_Исемлек.add(күчерү_урыны_VALUE); Collections.addAll(юл,"popl %eax","testl %eax, %eax",(команда == 198 ? "je " : "jne ") + 표식 + "_b" + күчерү_урыны_VALUE);
            } else throw new Тәрҗемә_итү_хата("미지원 команда: " + команда);
        }
        if (!경계들.containsAll(тармак_Исемлек)) throw new Тәрҗемә_итү_хата("команда 경계가 아닌 곳으로 тармак");
        юл.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",юл);
    }
    String 엑스상수(класс_мәгълүмат мәгълүмат, int INDEX) {
        if (мәгълүмат.상수종류[INDEX] == 3) return мәгълүмат.константа_мәгълүмат[INDEX].toString();
        if (мәгълүмат.상수종류[INDEX] == 8) return юл_символ(мәгълүмат.문자((Integer)мәгълүмат.константа_мәгълүмат[INDEX]));
        throw new Тәрҗемә_итү_хата("정수와 юл_VALUE_6ca8363c 상수만 ярдәм_VALUE");
    }
    String 엑스조립본(String кертү_балл, List<String> 내보냄, String максат_кыйммәт) throws IOException {
        Map<String,String> машина_таблица = new HashMap<>();
        for (String юл : Files.readAllLines(ресурс_юл.resolve("엑스기계함수.tsv"))) { String[] тоташтыру_VALUE = юл.split("\t"); if (тоташтыру_VALUE[0].equals(максат_кыйммәт)) машина_таблица.put(тоташтыру_VALUE[1] + тоташтыру_VALUE[2],тоташтыру_VALUE[3]); }
        int урнаштыру_INDEX = кертү_балл.lastIndexOf('.'); if (урнаштыру_INDEX < 0) throw new Тәрҗемә_итү_хата("кертү_балл 지정 Хата");
        String биләүче_VALUE = кертү_балл.substring(0,урнаштыру_INDEX).replace('.','/'), ысул_кертү_исем = кертү_балл.substring(урнаштыру_INDEX + 1); ысул_Белешмәлекләр кертү_балл_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { ысул_Белешмәлекләр Белешмәлекләр = new ысул_Белешмәлекләр(биләүче_VALUE,ысул_кертү_исем,서술); if (함수들.containsKey(Белешмәлекләр)) { if (кертү_балл_VALUE != null) throw new Тәрҗемә_итү_хата("겹친 кертү_балл"); кертү_балл_VALUE = Белешмәлекләр; } }
        if (кертү_балл_VALUE == null || (함수들.get(кертү_балл_VALUE).керү_кертү & 0x100) != 0) throw new Тәрҗемә_итү_хата("кертү_балл_VALUE ФУНКЦИЯ_VALUE формат_VALUE Хата");
        List<String> юл = new ArrayList<>(); юл.add(".code32");
        for (класс_мәгълүмат мәгълүмат : 클래스들.values()) {
            String халәт_VALUE = символ("state",мәгълүмат.исем), инициализацияләү = символ("init",мәгълүмат.исем);
            Collections.addAll(юл,".bss",".balign 4",халәт_VALUE + ": .long 0",".text",инициализацияләү + ":","cmpl $0, " + халәт_VALUE,"jne " + инициализацияләү + "_done","movl $1, " + халәт_VALUE);
            ысул_Белешмәлекләр 초기화참조 = new ысул_Белешмәлекләр(мәгълүмат.исем,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) юл.add("call " + символ("method",초기화참조.부분들()));
            Collections.addAll(юл,"movl $2, " + халәт_VALUE,инициализацияләү + "_done:","ret");
            for (бүлек_мәгълүмат кыр_VALUE : мәгълүмат.кыр_VALUE) {
                byte[] константа_VALUE = кыр_VALUE.аергыч_VALUE_286d43f0.get("ConstantValue"); String VALUE = константа_VALUE == null ? "0" : 엑스상수(мәгълүмат,new мәгълүмат_укучы(константа_VALUE).두바이트());
                Collections.addAll(юл,".data",".balign 4",символ("field",мәгълүмат.исем,кыр_VALUE.исем,кыр_VALUE.서술) + ": .long " + VALUE);
            }
            for (бүлек_мәгълүмат ФУНКЦИЯ_VALUE : мәгълүмат.ФУНКЦИЯ_VALUE) if (!ФУНКЦИЯ_VALUE.исем.equals("<init>")) юл.add(엑스함수본문(new ысул_Белешмәлекләр(мәгълүмат.исем,ФУНКЦИЯ_VALUE.исем,ФУНКЦИЯ_VALUE.서술),ФУНКЦИЯ_VALUE,машина_таблица,максат_кыйммәт));
        }
        Collections.addAll(юл,".text",".globl java_entry","java_entry:","call " + символ("init",кертү_балл_VALUE.биләүче_VALUE),"call " + символ("method",кертү_балл_VALUE.부분들()));
        if (кертү_балл_VALUE.서술.equals("()V")) юл.add("xorl %eax, %eax"); юл.add("ret");
        for (String 지정 : 내보냄) {
            int аергыч_VALUE_d8ba4873 = 지정.indexOf('='); if (аергыч_VALUE_d8ba4873 < 1) throw new Тәрҗемә_итү_хата("내보내기 지정 Хата");
            String 외부 = 지정.substring(0,аергыч_VALUE_d8ba4873), ФУНКЦИЯ_VALUE = 지정.substring(аергыч_VALUE_d8ba4873 + 1); int бүлү_үлчәм = ФУНКЦИЯ_VALUE.lastIndexOf('.');
            if (бүлү_үлчәм < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Тәрҗемә_итү_хата("내보내기 символ Хата");
            String класс_VALUE = ФУНКЦИЯ_VALUE.substring(0,бүлү_үлчәм).replace('.','/'), исем = ФУНКЦИЯ_VALUE.substring(бүлү_үлчәм + 1); ысул_Белешмәлекләр тамгаланган_өлеш_VALUE = null;
            for (ысул_Белешмәлекләр Белешмәлекләр : 함수들.keySet()) if (Белешмәлекләр.биләүче_VALUE.equals(класс_VALUE) && Белешмәлекләр.исем.equals(исем)) { if (тамгаланган_өлеш_VALUE != null) throw new Тәрҗемә_итү_хата("겹친 내보내기 максат_кыйммәт"); тамгаланган_өлеш_VALUE = Белешмәлекләр; }
            if (тамгаланган_өлеш_VALUE == null) throw new Тәрҗемә_итү_хата("내보낼 함수가 없음");
            Collections.addAll(юл,".text",".globl " + 외부,외부 + ":","call " + символ("init",тамгаланган_өлеш_VALUE.биләүче_VALUE),"jmp " + символ("method",тамгаланган_өлеш_VALUE.부분들()));
        }
        юл.add(".section .rodata");
        for (Map.Entry<String,String> кертү_VALUE : 문자열들.entrySet()) {
            Collections.addAll(юл,".balign 4",кертү_VALUE.getValue() + ":",".long " + кертү_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char дәрес_VALUE : кертү_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(дәрес_VALUE)); if (!단위들.isEmpty()) юл.add(".long " + String.join(",",단위들));
        }
        юл.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",юл) + "\n";
    }
    static void үтәргә_чара(List<String> команда) throws Exception {
        if (new ProcessBuilder(команда).inheritIO().start().waitFor() != 0) throw new Тәрҗемә_итү_хата("төзү_чыганак Хата: " + команда.get(0));
    }
    static String мәгълүмат_юл(String Mäten) { return "\"" + Mäten.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String максат_кыйммәт, String кертү_балл, List<String> 내보냄, Path 출력, Path ресурс_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), класс_юл = 임시.resolve("classes"); Files.createDirectory(класс_юл);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",класс_юл.toString(),"-sourcepath",класс_юл.toString(),"-d",класс_юл.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int чыганак_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Тәрҗемә_итү_хата("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); чыганак_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Тәрҗемә_итү_хата(".java 또는 .class만 ярдәм_VALUE");
            }
            if (чыганак_COUNT > 0) үтәргә_чара(자바명령);
            try (java.util.stream.Stream<Path> юл_Исемлек_4d1a5003 = Files.walk(класс_юл)) { юл_Исемлек_4d1a5003.filter(Yul -> Yul.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,максат_кыйммәт.equals("user") ? "user" : "kernel",262144,ресурс_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(кертү_балл,내보냄,максат_кыйммәт); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path чара_урнаштыру = ресурс_VALUE.getParent();
            үтәргә_чара(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            үтәргә_чара(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),чара_урнаштыру.resolve("CLR_мохите_ярдәм.s").toString()));
            List<String> ялгау = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (максат_кыйммәт.equals("kernel")) ялгау.add("-r");
            else {
                үтәргә_чара(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),чара_урнаштыру.resolve(максат_кыйммәт.equals("user") ? "Start_кулланучы_кушымта.s" : "리눅스시작.s").toString()));
                Collections.addAll(ялгау,"-e","_start",임시.resolve("start.o").toString());
                if (максат_кыйммәт.equals("user")) Collections.addAll(ялгау,"-T",чара_урнаштыру.resolve("кулланучы_бәйләү_план.ld").toString());
            }
            Collections.addAll(ялгау,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); үтәргә_чара(ялгау);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path нәшер_итү_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),нәшер_итү_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(нәшер_итү_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(нәшер_итү_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(максат_кыйммәт.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> символ_мәгълүмат = new ArrayList<>(), чыганак_мәгълүмат = new ArrayList<>();
            for (ысул_Белешмәлекләр Белешмәлекләр : CONVERT_VALUE.함수들.keySet()) символ_мәгълүмат.add(мәгълүмат_юл(символ("method",Белешмәлекләр.부분들())) + ":" + мәгълүмат_юл(Белешмәлекләр.биләүче_VALUE + "." + Белешмәлекләр.исем + Белешмәлекләр.서술));
            for (Path 입력 : 입력들) {
                byte[] Хәш_файл = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Mäten = new StringBuilder(); for (byte VALUE : Хәш_файл) Mäten.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                чыганак_мәгълүмат.add(мәгълүмат_юл(입력.toAbsolutePath().toString()) + ":" + мәгълүмат_юл(Mäten.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + мәгълүмат_юл(максат_кыйммәт) + ",\"entry\":" + мәгълүмат_юл(кертү_балл) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",символ_мәгълүмат) + "},\"sources\":{" + String.join(",",чыганак_мәгълүмат) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> юл_Исемлек_4d1a5003 = Files.walk(임시)) { for (Path Yul : (Iterable<Path>)юл_Исемлек_4d1a5003.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Yul); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String кертү_балл = null, максат_кыйммәт = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> юл_Исемлек_4d1a5003 = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry класс_VALUE.ФУНКЦИЯ_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export символ=класс_VALUE.ФУНКЦИЯ_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": кертү_балл = 인수[++순번]; break;
                    case "--profile": максат_кыйммәт = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Тәрҗемә_итү_хата("알 수 없는 옵션: " + VALUE); юл_Исемлек_4d1a5003.add(Paths.get(VALUE));
                }
            }
            if (кертү_балл == null || 출력경로 == null || юл_Исемлек_4d1a5003.isEmpty()) throw new Тәрҗемә_итү_хата("--entry, -o, класс_VALUE 파일이 필요합니다");
            Path ресурс_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Тәрҗемә_итү_хата("알 수 없는 үтәргә_команда максат_кыйммәт");
                엑스번역(юл_Исемлек_4d1a5003,엑스대상,кертү_балл,내보냄,출력경로,ресурс_VALUE); return;
            }
            String чыганак = new 기계어미리번역(юл_Исемлек_4d1a5003, максат_кыйммәт, 낱말수, ресурс_VALUE).булдыру(кертү_балл, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, чыганак, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Хата) { System.err.println("төзү_чыганак Хата: " + Хата.getMessage()); System.exit(1); }
    }
}
