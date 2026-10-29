// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java 클래스 파일에서 독립 ARM64 커널용 C 원문을 만든다. 호스트 JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class 번역오류 extends RuntimeException {
        번역오류(String 설명) { super(설명); }
    }
    static final class 자료읽개 {
        final byte[] 자료;
        int Posición;
        자료읽개(byte[] 입력자료) { 자료 = 입력자료; }
        byte[] Llectura(int 길이) {
            if (길이 < 0 || 길이 > 자료.length - Posición) throw new 번역오류("잘린 클래스 또는 Comandu 자료");
            byte[] 결과 = Arrays.copyOfRange(자료, Posición, Posición + 길이); Posición += 길이; return 결과;
        }
        int 한바이트() { if (Posición >= 자료.length) throw new 번역오류("잘린 Comandu 자료"); return 자료[Posición++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class 멤버자료 {
        final int 접근;
        final String Nome, 서술;
        final Map<String, byte[]> 속성;
        멤버자료(int 접근값, String 이름값, String 서술값, Map<String, byte[]> 속성값) {
            접근 = 접근값; Nome = 이름값; 서술 = 서술값; 속성 = 속성값;
        }
    }
    static final class 함수참조 implements Comparable<함수참조> {
        final String 소유, Nome, 서술;
        함수참조(String 소유값, String 이름값, String 서술값) { 소유 = 소유값; Nome = 이름값; 서술 = 서술값; }
        String[] 부분들() { return new String[]{소유, Nome, 서술}; }
        public int compareTo(함수참조 상대) {
            int 비교값 = 소유.compareTo(상대.소유);
            if (비교값 == 0) 비교값 = Nome.compareTo(상대.Nome);
            return 비교값 == 0 ? 서술.compareTo(상대.서술) : 비교값;
        }
        public boolean equals(Object 상대) { return 상대 instanceof 함수참조 && compareTo((함수참조) 상대) == 0; }
        public int hashCode() { return Objects.hash(소유, Nome, 서술); }
    }
    static final class 클래스자료 {
        final int[] 상수종류;
        final Object[] 상수값;
        final String Nome;
        final List<멤버자료> 필드, 함수;
        클래스자료(Path Camín) throws IOException {
            자료읽개 읽개 = new 자료읽개(Files.readAllBytes(Camín));
            if (읽개.네바이트() != 0xcafebabe) throw new 번역오류("Java 클래스 표식이 아님");
            읽개.Llectura(4);
            int 개수 = 읽개.두바이트(); 상수종류 = new int[개수]; 상수값 = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = 읽개.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int 길이 = 읽개.두바이트();
                        byte[] 문자자료 = 읽개.Llectura(길이), 길이붙인자료 = new byte[길이 + 2];
                        길이붙인자료[0] = (byte)(길이 >> 8); 길이붙인자료[1] = (byte)길이;
                        System.arraycopy(문자자료, 0, 길이붙인자료, 2, 길이);
                        상수값[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: 상수값[순번] = 읽개.네바이트(); break;
                    case 4: 읽개.Llectura(4); break;
                    case 5: case 6: 읽개.Llectura(8); 순번++; break;
                    case 7: case 8: case 16: 상수값[순번] = 읽개.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        상수값[순번] = new int[]{읽개.두바이트(), 읽개.두바이트()}; break;
                    case 15: 상수값[순번] = new int[]{읽개.한바이트(), 읽개.두바이트()}; break;
                    default: throw new 번역오류("지원하지 않는 상수 종류: " + 종류);
                }
            }
            읽개.두바이트(); Nome = 클래스명(읽개.두바이트());
            if (!클래스명(읽개.두바이트()).equals("java/lang/Object") || 읽개.두바이트() != 0)
                throw new 번역오류(Nome + ": 상속 및 인터페이스 미지원");
            필드 = 멤버읽기(읽개); 함수 = 멤버읽기(읽개); 속성읽기(읽개);
            if (읽개.Posición != 읽개.자료.length) throw new 번역오류("클래스 뒤에 남은 자료");
        }
        String 문자(int 번호) {
            if (번호 < 1 || 번호 >= 상수종류.length || 상수종류[번호] != 1) throw new 번역오류("문자 상수 번호 Fallu");
            return (String) 상수값[번호];
        }
        String 클래스명(int 번호) {
            if (번호 < 1 || 번호 >= 상수종류.length || 상수종류[번호] != 7) throw new 번역오류("클래스 참조 Fallu");
            return 문자((Integer)상수값[번호]);
        }
        함수참조 참조(int 번호) {
            if (번호 < 1 || 번호 >= 상수종류.length || 상수종류[번호] < 9 || 상수종류[번호] > 11) throw new 번역오류("멤버 참조 Fallu");
            int[] 쌍 = (int[])상수값[번호], 이름쌍 = (int[])상수값[쌍[1]];
            return new 함수참조(클래스명(쌍[0]), 문자(이름쌍[0]), 문자(이름쌍[1]));
        }
        Map<String, byte[]> 속성읽기(자료읽개 읽개) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = 읽개.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String 속성이름 = 문자(읽개.두바이트()); byte[] 값 = 읽개.Llectura(읽개.네바이트());
                if (결과.put(속성이름, 값) != null) throw new 번역오류("겹친 속성: " + 속성이름);
            }
            return 결과;
        }
        List<멤버자료> 멤버읽기(자료읽개 읽개) {
            List<멤버자료> 결과 = new ArrayList<>(); int 개수 = 읽개.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int 접근 = 읽개.두바이트(); String 함수이름 = 문자(읽개.두바이트()), 서술 = 문자(읽개.두바이트());
                결과.add(new 멤버자료(접근, 함수이름, 서술, 속성읽기(읽개)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> Argumentu = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new 번역오류("함수 서술 Fallu: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new 번역오류("함수 서술 Fallu: " + 서술);
            Argumentu.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumentu.contains("V") || 반환들.size() != 1) throw new 번역오류("함수 서술 Fallu: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Posición = 0; Posición < 서술.length();) {
            String 선택 = null;
            for (String 형식 : 허용형식) if (서술.startsWith(형식, Posición)) { 선택 = 형식; break; }
            if (선택 == null) throw new 번역오류("지원하지 않는 자료형: " + 서술);
            결과.add(선택); Posición += 선택.length();
        }
        return 결과;
    }
    static String 기호(String 종류, String... 부분들) {
        try {
            byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Testu = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Testu.append(String.format(Locale.ROOT, "%02x", 해시[순번] & 255));
            return Testu.toString();
        } catch (Exception Fallu) { throw new 번역오류(Fallu.toString()); }
    }
    final Map<String, 클래스자료> 클래스들 = new TreeMap<>();
    final Map<함수참조, 멤버자료> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, 기계클래스;
    final int 동적기억낱말수;
    final Path 자원경로;
    기계어미리번역(List<Path> 경로들, String 대상, int 낱말수, Path 자원) throws IOException {
        if ((!대상.equals("kernel") && !대상.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new 번역오류("실행 대상 또는 기억 공간 Tamañu Fallu");
        실행대상 = 대상; 동적기억낱말수 = 낱말수; 자원경로 = 자원;
        // 이 이름도 국가별 소스 생성 시 해당 언어로 옮긴다.
        기계클래스 = 대상.equals("kernel") ? "보드" : "사용자";
        for (String Llinia : Files.readAllLines(자원.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Llinia.split("\t", -1);
            if (부분들.length != 4) throw new 번역오류("기계 함수 자료 Fallu");
            if (부분들[0].equals(대상)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Camín : 경로들) {
            클래스자료 자료 = new 클래스자료(Camín);
            if (클래스들.put(자료.Nome, 자료) != null) throw new 번역오류("중복 클래스: " + 자료.Nome);
            for (멤버자료 필드 : 자료.필드) {
                if ((필드.접근 & 8) == 0 || 형식읽기(필드.서술).equals(Collections.singletonList("V"))) throw new 번역오류("정적 필드만 지원");
                if (필드들.put(new 함수참조(자료.Nome, 필드.Nome, 필드.서술), 필드) != null) throw new 번역오류("중복 필드");
            }
            for (멤버자료 함수 : 자료.함수) {
                if (함수.Nome.equals("<init>")) continue;
                if ((함수.접근 & 8) == 0 || (함수.접근 & (0x20 | 0x400)) != 0) throw new 번역오류("정적 비동기화 함수만 지원");
                new 함수형식(함수.서술);
                if (함수들.put(new 함수참조(자료.Nome, 함수.Nome, 함수.서술), 함수) != null) throw new 번역오류("중복 함수");
            }
        }
    }
    String 문자열기호(String Testu) { return 문자열들.computeIfAbsent(Testu, 값 -> "j_text_" + 문자열들.size()); }
    String 상수표현(클래스자료 자료, int 번호) {
        if (번호 < 1 || 번호 >= 자료.상수종류.length) throw new 번역오류("상수 번호 범위 Fallu");
        if (자료.상수종류[번호] == 3) return "(word)(uint32_t)(" + 자료.상수값[번호] + ")";
        if (자료.상수종류[번호] == 8) return "(word)" + 문자열기호(자료.문자((Integer)자료.상수값[번호]));
        throw new 번역오류("정수와 문자열 상수만 지원");
    }
    String 함수원형(함수참조 참조) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(참조.서술).Argumentu.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + 기호("method", 참조.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void 지역검사(int 번호, int 지역변수수) { if (번호 < 0 || 번호 >= 지역변수수) throw new 번역오류("지역 변수 번호 범위 Fallu"); }
    void 분기넣기(List<String> Salida, Set<Integer> 분기들, int Posición, int 이동량, String 조건) {
        int 목적 = Posición + 이동량; 분기들.add(목적);
        Salida.add((조건 == null ? "" : "if (" + 조건 + ") ") + "goto b" + 목적 + ";");
    }
    String 함수본문(함수참조 함수, 멤버자료 자료) {
        byte[] 본문자료 = 자료.속성.get("Code"); if (본문자료 == null) throw new 번역오류("함수 몸체가 없음: " + 함수.Nome);
        자료읽개 읽개 = new 자료읽개(본문자료); int 쌓임깊이 = 읽개.두바이트(), 지역변수수 = 읽개.두바이트();
        자료읽개 명령자료 = new 자료읽개(읽개.Llectura(읽개.네바이트()));
        if (읽개.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 형식 = new 함수형식(함수.서술); if (지역변수수 < 형식.Argumentu.size()) throw new 번역오류("매개변수보다 적은 지역 변수");
        클래스자료 클래스 = 클래스들.get(함수.소유);
        List<String> Salida = new ArrayList<>(); Salida.add(함수원형(함수) + " {");
        Salida.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < 형식.Argumentu.size(); 순번++) Salida.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (명령자료.Posición < 명령자료.자료.length) {
            int Posición = 명령자료.Posición, Comandu = 명령자료.한바이트(); 경계들.add(Posición); Salida.add("b" + Posición + ":;");
            if (Comandu == 0) continue;
            if (Comandu == 1) Salida.add("PUSH(0);");
            else if (Comandu >= 2 && Comandu <= 8) Salida.add("PUSH((uint32_t)(" + (Comandu - 3) + "));");
            else if (Comandu == 16 || Comandu == 17) Salida.add("PUSH((uint32_t)(" + (Comandu == 16 ? 명령자료.부호한바이트() : 명령자료.부호두바이트()) + "));");
            else if (Comandu == 18 || Comandu == 19) Salida.add("PUSH(" + 상수표현(클래스, Comandu == 18 ? 명령자료.한바이트() : 명령자료.두바이트()) + ");");
            else if (Comandu == 21 || Comandu == 25 || (Comandu >= 26 && Comandu <= 29) || (Comandu >= 42 && Comandu <= 45)) {
                int 번호 = Comandu == 21 || Comandu == 25 ? 명령자료.한바이트() : Comandu - (Comandu <= 29 ? 26 : 42);
                지역검사(번호, 지역변수수); Salida.add("PUSH(l[" + 번호 + "]);");
            } else if (Comandu == 54 || Comandu == 58 || (Comandu >= 59 && Comandu <= 62) || (Comandu >= 75 && Comandu <= 78)) {
                int 번호 = Comandu == 54 || Comandu == 58 ? 명령자료.한바이트() : Comandu - (Comandu <= 62 ? 59 : 75);
                지역검사(번호, 지역변수수); Salida.add("l[" + 번호 + "] = POP();");
            } else if (Comandu == 46) Salida.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Comandu == 79) Salida.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Comandu == 87 || Comandu == 88) Salida.add(Comandu == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Comandu >= 89 && Comandu <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] 순서들 = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Comandu - 89]; 순번++) Salida.add("abcd".charAt(순번) + " = POP();");
                for (char 값 : 순서들[Comandu - 89].toCharArray()) Salida.add("PUSH(" + 값 + ");");
            } else if (Comandu == 96 || Comandu == 100 || Comandu == 104 || Comandu == 126 || Comandu == 128 || Comandu == 130) {
                String 연산 = Comandu == 96 ? "+" : Comandu == 100 ? "-" : Comandu == 104 ? "*" : Comandu == 126 ? "&" : Comandu == 128 ? "|" : "^";
                Salida.add("b = POP(); a = POP(); PUSH((uint32_t)a " + 연산 + " (uint32_t)b);");
            } else if (Comandu == 108 || Comandu == 112) Salida.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Comandu == 112 ? 1 : 0) + "));");
            else if (Comandu == 116) Salida.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Comandu == 120 || Comandu == 122 || Comandu == 124) {
                Salida.add("b = POP(); a = POP();"); Salida.add("PUSH(" + (Comandu == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Comandu == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Comandu == 132) {
                int 번호 = 명령자료.한바이트(), 증가량 = 명령자료.부호한바이트(); 지역검사(번호, 지역변수수);
                Salida.add("l[" + 번호 + "] = (uint32_t)l[" + 번호 + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Comandu >= 145 && Comandu <= 147) Salida.add("a = POP(); PUSH((uint32_t)(" + (Comandu == 145 ? "int8_t" : Comandu == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Comandu >= 153 && Comandu <= 158) {
                Salida.add("a = POP();"); 분기넣기(Salida, 분기들, Posición, 명령자료.부호두바이트(), "(int32_t)a " + 비교들[Comandu - 153] + " 0");
            } else if (Comandu >= 159 && Comandu <= 166) {
                Salida.add("b = POP(); a = POP();"); 분기넣기(Salida, 분기들, Posición, 명령자료.부호두바이트(), Comandu >= 165 ? "a " + 비교들[Comandu - 159] + " b" : "(int32_t)a " + 비교들[Comandu - 159] + " (int32_t)b");
            } else if (Comandu == 167 || Comandu == 200) 분기넣기(Salida, 분기들, Posición, Comandu == 167 ? 명령자료.부호두바이트() : 명령자료.네바이트(), null);
            else if (Comandu == 170 || Comandu == 171) {
                while (명령자료.Posición % 4 != 0) 명령자료.한바이트();
                int 기본 = 명령자료.네바이트(); Salida.add("a = POP();");
                if (Comandu == 170) {
                    int 아래 = 명령자료.네바이트(), 위 = 명령자료.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (명령자료.자료.length - 명령자료.Posición) / 4) throw new 번역오류("switch 범위 Fallu");
                    for (long 값 = 아래; 값 <= 위; 값++) 분기넣기(Salida, 분기들, Posición, 명령자료.네바이트(), "(int32_t)a == (" + 값 + ")");
                } else {
                    int 개수 = 명령자료.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (명령자료.자료.length - 명령자료.Posición) / 8) throw new 번역오류("switch Tamañu Fallu");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int 값 = 명령자료.네바이트(); if (순번 > 0 && 값 <= 앞값) throw new 번역오류("switch 순서 Fallu"); 앞값 = 값;
                        분기넣기(Salida, 분기들, Posición, 명령자료.네바이트(), "(int32_t)a == (" + 값 + ")");
                    }
                }
                분기넣기(Salida, 분기들, Posición, 기본, null);
            } else if (Comandu == 172 || Comandu == 176 || Comandu == 177) Salida.add("return " + (Comandu == 177 ? "0" : "POP()") + ";");
            else if (Comandu == 178 || Comandu == 179) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 필드");
                Salida.add(기호("init", 참조.소유) + "();"); String 필드 = 기호("field", 참조.부분들());
                Salida.add(Comandu == 178 ? "PUSH(" + 필드 + ");" : 필드 + " = POP();");
            } else if (Comandu == 184) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 함수");
                함수형식 호출형식 = new 함수형식(참조.서술); int 개수 = 호출형식.Argumentu.size();
                Salida.add(기호("init", 참조.소유) + "();"); Salida.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Salida.add("a = " + 기호("method", 참조.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) Salida.add("PUSH(a);");
            } else if (Comandu == 182) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트());
                if (참조.equals(new 함수참조("java/lang/String", "length", "()I"))) Salida.add("a = POP(); PUSH(length(a));");
                else if (참조.equals(new 함수참조("java/lang/String", "charAt", "(I)C"))) Salida.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 번역오류("가상 함수 호출 미지원");
            } else if (Comandu == 188) {
                if (명령자료.한바이트() != 10) throw new 번역오류("new int[]만 지원"); Salida.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Comandu == 190) Salida.add("a = POP(); PUSH(length(a));");
            else if (Comandu == 196) {
                int 확장 = 명령자료.한바이트(), 번호 = 명령자료.두바이트(); 지역검사(번호, 지역변수수);
                if (확장 == 21 || 확장 == 25) Salida.add("PUSH(l[" + 번호 + "]);");
                else if (확장 == 54 || 확장 == 58) Salida.add("l[" + 번호 + "] = POP();");
                else if (확장 == 132) Salida.add("l[" + 번호 + "] = (uint32_t)l[" + 번호 + "] + (uint32_t)(" + 명령자료.부호두바이트() + ");");
                else throw new 번역오류("미지원 wide Comandu");
            } else if (Comandu == 198 || Comandu == 199) {
                Salida.add("a = POP();"); 분기넣기(Salida, 분기들, Posición, 명령자료.부호두바이트(), "a " + (Comandu == 198 ? "==" : "!=") + " 0");
            } else throw new 번역오류(함수.소유 + "." + 함수.Nome + ", 바이트 " + Posición + ": 미지원 Comandu " + Comandu);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("Comandu 경계가 아닌 곳으로 분기");
        Salida.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Salida);
    }
    String 내보낼함수(String 연결기호, String 대상, boolean 진입점여부) {
        int 자리 = 대상.lastIndexOf('.'); if (자리 < 0 || !연결기호.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 지정 Fallu");
        String 소유 = 대상.substring(0, 자리).replace('.', '/'), Nome = 대상.substring(자리 + 1); 함수참조 선택 = null;
        for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(소유) && 참조.Nome.equals(Nome)) {
            if (선택 != null) throw new 번역오류("겹친 내보내기 대상"); 선택 = 참조;
        }
        if (선택 == null || (함수들.get(선택).접근 & 0x100) != 0) throw new 번역오류("내보낼 함수가 없음 또는 native 함수");
        함수형식 형식 = new 함수형식(선택.서술);
        if ((진입점여부 && !형식.Argumentu.isEmpty()) || !Arrays.asList("V", "I").contains(형식.반환)) throw new 번역오류("진입 또는 C 경계 형식 Fallu");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < 형식.Argumentu.size(); 순번++) {
            if (!형식.Argumentu.get(순번).equals("I")) throw new 번역오류("C 경계는 int 인수만 지원");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (형식.반환.equals("V") ? "void " : "int32_t ") + 연결기호 + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + 기호("init", 선택.소유) + "(); " + (형식.반환.equals("V") ? "" : "return (int32_t)") + 기호("method", 선택.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String 진입점, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<함수참조, 멤버자료> 항목 : 함수들.entrySet()) {
            함수참조 참조 = 항목.getKey(); 멤버자료 자료 = 항목.getValue(); 선언들.add(함수원형(참조) + ";");
            if ((자료.접근 & 0x100) != 0) {
                String Coneutar = 기계함수들.get(참조.Nome + 참조.서술);
                if (!참조.소유.equals(기계클래스) || Coneutar == null) throw new 번역오류("허용되지 않은 native 함수: " + 참조.Nome);
                int 개수 = new 함수형식(참조.서술).Argumentu.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Coneutar + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(참조) + " { return " + Coneutar + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(참조, 자료));
        }
        for (Map.Entry<함수참조, 멤버자료> 항목 : 필드들.entrySet()) {
            함수참조 참조 = 항목.getKey(); byte[] 상수 = 항목.getValue().속성.get("ConstantValue");
            String 값 = 상수 == null ? "0" : 상수표현(클래스들.get(참조.소유), new 자료읽개(상수).두바이트());
            필드선언들.add("static word " + 기호("field", 참조.부분들()) + " = " + 값 + ";");
        }
        for (String Nome : 클래스들.keySet()) {
            String 초기화 = 기호("init", Nome), 상태 = 기호("state", Nome);
            선언들.add("static void " + 초기화 + "(void);"); 필드선언들.add("static unsigned " + 상태 + ";");
            함수참조 참조 = new 함수참조(Nome, "<clinit>", "()V");
            몸체들.add("static void " + 초기화 + "(void) { if(" + 상태 + ") return; " + 상태 + " = 1; " + (함수들.containsKey(참조) ? 기호("method", 참조.부분들()) + "(); " : "") + 상태 + " = 2; }");
        }
        몸체들.add(내보낼함수("java_entry", 진입점, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new 번역오류("내보내기 지정 Fallu");
            String Nome = 지정.substring(0, 자리); 공개이름.add(Nome); 몸체들.add(내보낼함수(Nome, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> 항목 : 문자열들.entrySet()) {
            String Testu = 항목.getKey(); StringBuilder 배열 = new StringBuilder("static const word " + 항목.getValue() + "[] = {" + Testu.length());
            for (int 순번 = 0; 순번 < Testu.length(); 순번++) 배열.append(", ").append((int)Testu.charAt(순번));
            문자열선언들.add(배열.append("};").toString());
        }
        String 지원 = Files.readString(자원경로.resolve("실행지원.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(지원 + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String FONTE, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> 이름표 = new HashMap<>();
        for (String Llinia : Files.readAllLines(자원경로.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] 쌍 = Llinia.split("\t"); 이름표.put(쌍[0], 쌍[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(FONTE); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Nome = 찾개.group(), 새이름 = Nome;
            if (!Nome.startsWith("//") && !Nome.startsWith("/*") && !Nome.startsWith("\"") && !Nome.startsWith("'") && !공개이름.contains(Nome)) {
                새이름 = 이름표.getOrDefault(Nome, Nome);
                if (Nome.matches("a[0-9]+")) 새이름 = "Argumentu" + Nome.substring(1);
                if (Nome.matches("b[0-9]+")) 새이름 = "분기" + Nome.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char 글자 : 새이름.toCharArray()) 표기.append(글자 < 128 ? Character.toString(글자) : String.format(Locale.ROOT, "\\u%04x", (int)글자));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(함수참조 함수, 멤버자료 자료, Map<String,String> 기계표, String 대상) {
        String 표식 = 기호("method", 함수.부분들());
        List<String> Llinia = new ArrayList<>();
        if ((자료.접근 & 0x100) != 0) {
            String Coneutar = 기계표.get(함수.Nome + 함수.서술);
            if (!함수.소유.equals(대상.equals("kernel") ? "장치" : "사용자") || Coneutar == null) throw new 번역오류("허용되지 않은 native 함수");
            return ".text\n" + 표식 + ":\njmp " + Coneutar;
        }
        byte[] 본문 = 자료.속성.get("Code"); if (본문 == null) throw new 번역오류("함수 몸체가 없음");
        자료읽개 읽개 = new 자료읽개(본문); 읽개.두바이트(); int 지역수 = 읽개.두바이트();
        자료읽개 명령자료 = new 자료읽개(읽개.Llectura(읽개.네바이트()));
        if (읽개.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 형식 = new 함수형식(함수.서술); if (지역수 < 형식.Argumentu.size()) throw new 번역오류("매개변수보다 적은 지역 변수");
        Collections.addAll(Llinia,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < 형식.Argumentu.size(); 순번++) Collections.addAll(Llinia,"movl " + (8 + 4 * (형식.Argumentu.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        클래스자료 클래스 = 클래스들.get(함수.소유); Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (명령자료.Posición < 명령자료.자료.length) {
            int Posición = 명령자료.Posición, Comandu = 명령자료.한바이트(); String 자리 = 표식 + "_b" + Posición;
            Llinia.add(자리 + ":"); 경계들.add(Posición);
            if (Comandu == 0) Llinia.add("nop");
            else if (Comandu == 1) Llinia.add("pushl $0");
            else if (Comandu >= 2 && Comandu <= 8) Llinia.add("pushl $" + (Comandu - 3));
            else if (Comandu == 16 || Comandu == 17) Llinia.add("pushl $" + (Comandu == 16 ? 명령자료.부호한바이트() : 명령자료.부호두바이트()));
            else if (Comandu == 18 || Comandu == 19) {
                int 번호 = Comandu == 18 ? 명령자료.한바이트() : 명령자료.두바이트();
                Llinia.add("pushl $" + 엑스상수(클래스,번호));
            } else if (Comandu == 21 || Comandu == 25 || (Comandu >= 26 && Comandu <= 29) || (Comandu >= 42 && Comandu <= 45) || Comandu == 54 || Comandu == 58 || (Comandu >= 59 && Comandu <= 62) || (Comandu >= 75 && Comandu <= 78)) {
                boolean 읽음 = Comandu < 54; int 번호 = Comandu == 21 || Comandu == 25 || Comandu == 54 || Comandu == 58 ? 명령자료.한바이트() : Comandu - (Comandu <= 29 ? 26 : Comandu <= 45 ? 42 : Comandu <= 62 ? 59 : 75);
                지역검사(번호,지역수); Llinia.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (번호 + 1)) + "(%ebp)");
            } else if (Comandu == 46) Collections.addAll(Llinia,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Comandu == 79) Collections.addAll(Llinia,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Comandu == 87 || Comandu == 88) Llinia.add("addl $" + (Comandu == 87 ? 4 : 8) + ", %esp");
            else if (Comandu >= 89 && Comandu <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] 순서들 = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Comandu - 89]; 순번++) Llinia.add("popl " + 저장기들[순번]);
                for (int 순번 : 순서들[Comandu - 89]) Llinia.add("pushl " + 저장기들[순번]);
            } else if (Comandu == 96 || Comandu == 100 || Comandu == 104 || Comandu == 126 || Comandu == 128 || Comandu == 130) {
                String 연산 = Comandu == 96 ? "addl" : Comandu == 100 ? "subl" : Comandu == 104 ? "imull" : Comandu == 126 ? "andl" : Comandu == 128 ? "orl" : "xorl";
                Collections.addAll(Llinia,"popl %ecx","popl %eax",연산 + " %ecx, %eax","pushl %eax");
            } else if (Comandu == 108 || Comandu == 112) Collections.addAll(Llinia,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Comandu == 108 ? "%eax" : "%edx"));
            else if (Comandu == 116) Llinia.add("negl (%esp)");
            else if (Comandu == 120 || Comandu == 122 || Comandu == 124) Collections.addAll(Llinia,"popl %ecx","popl %eax",(Comandu == 120 ? "sall" : Comandu == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Comandu == 132) {
                int 번호 = 명령자료.한바이트(), 증가 = 명령자료.부호한바이트(); 지역검사(번호,지역수); Llinia.add("addl $" + 증가 + ", -" + (4 * (번호 + 1)) + "(%ebp)");
            } else if (Comandu >= 145 && Comandu <= 147) Collections.addAll(Llinia,"popl %eax",Comandu == 145 ? "movsbl %al, %eax" : Comandu == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Comandu >= 153 && Comandu <= 166) {
                if (Comandu <= 158) Collections.addAll(Llinia,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Llinia,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int 목적 = Posición + 명령자료.부호두바이트(); 분기들.add(목적); Llinia.add(비교들[Comandu - (Comandu <= 158 ? 153 : 159)] + " " + 표식 + "_b" + 목적);
            } else if (Comandu == 167 || Comandu == 200) {
                int 목적 = Posición + (Comandu == 167 ? 명령자료.부호두바이트() : 명령자료.네바이트()); 분기들.add(목적); Llinia.add("jmp " + 표식 + "_b" + 목적);
            } else if (Comandu == 170 || Comandu == 171) {
                while (명령자료.Posición % 4 != 0) 명령자료.한바이트();
                int 기본 = Posición + 명령자료.네바이트(); 분기들.add(기본); Llinia.add("popl %eax");
                int 개수, 아래 = 0;
                if (Comandu == 170) { 아래 = 명령자료.네바이트(); int 위 = 명령자료.네바이트(); long 길이 = (long)위 - 아래 + 1; if (길이 < 1 || 길이 > (명령자료.자료.length - 명령자료.Posición) / 4) throw new 번역오류("switch 범위 Fallu"); 개수 = (int)길이; }
                else { 개수 = 명령자료.네바이트(); if (개수 < 0 || 개수 > (명령자료.자료.length - 명령자료.Posición) / 8) throw new 번역오류("switch Tamañu Fallu"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int 값 = Comandu == 170 ? 아래 + 순번 : 명령자료.네바이트(), 목적 = Posición + 명령자료.네바이트(); 분기들.add(목적);
                    Collections.addAll(Llinia,"cmpl $" + 값 + ", %eax","je " + 표식 + "_b" + 목적);
                }
                Llinia.add("jmp " + 표식 + "_b" + 기본);
            } else if (Comandu == 172 || Comandu == 176 || Comandu == 177) {
                if (Comandu != 177) Llinia.add("popl %eax"); Collections.addAll(Llinia,"leave","ret");
            } else if (Comandu == 178 || Comandu == 179) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 필드");
                Collections.addAll(Llinia,"call " + 기호("init",참조.소유),(Comandu == 178 ? "pushl " : "popl ") + 기호("field",참조.부분들()));
            } else if (Comandu == 184) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 함수");
                함수형식 호출형식 = new 함수형식(참조.서술); Collections.addAll(Llinia,"call " + 기호("init",참조.소유),"call " + 기호("method",참조.부분들()));
                if (!호출형식.Argumentu.isEmpty()) Llinia.add("addl $" + 호출형식.Argumentu.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) Llinia.add("pushl %eax");
            } else if (Comandu == 182) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트());
                if (참조.equals(new 함수참조("java/lang/String","length","()I"))) Collections.addAll(Llinia,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (참조.equals(new 함수참조("java/lang/String","charAt","(I)C"))) Collections.addAll(Llinia,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 번역오류("가상 함수 호출 미지원");
            } else if (Comandu == 188) {
                if (명령자료.한바이트() != 10) throw new 번역오류("new int[]만 지원"); Collections.addAll(Llinia,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Comandu == 190) Collections.addAll(Llinia,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Comandu == 196) {
                int 확장 = 명령자료.한바이트(), 번호 = 명령자료.두바이트(); 지역검사(번호,지역수);
                if (확장 == 21 || 확장 == 25 || 확장 == 54 || 확장 == 58) Llinia.add((확장 <= 25 ? "pushl " : "popl ") + "-" + 4 * (번호 + 1) + "(%ebp)");
                else if (확장 == 132) Llinia.add("addl $" + 명령자료.부호두바이트() + ", -" + 4 * (번호 + 1) + "(%ebp)");
                else throw new 번역오류("wide Comandu 미지원");
            } else if (Comandu == 198 || Comandu == 199) {
                int 목적 = Posición + 명령자료.부호두바이트(); 분기들.add(목적); Collections.addAll(Llinia,"popl %eax","testl %eax, %eax",(Comandu == 198 ? "je " : "jne ") + 표식 + "_b" + 목적);
            } else throw new 번역오류("미지원 Comandu: " + Comandu);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("Comandu 경계가 아닌 곳으로 분기");
        Llinia.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",Llinia);
    }
    String 엑스상수(클래스자료 자료, int 번호) {
        if (자료.상수종류[번호] == 3) return 자료.상수값[번호].toString();
        if (자료.상수종류[번호] == 8) return 문자열기호(자료.문자((Integer)자료.상수값[번호]));
        throw new 번역오류("정수와 문자열 상수만 지원");
    }
    String 엑스조립본(String 진입점, List<String> 내보냄, String 대상) throws IOException {
        Map<String,String> 기계표 = new HashMap<>();
        for (String Llinia : Files.readAllLines(자원경로.resolve("엑스기계함수.tsv"))) { String[] 쌍 = Llinia.split("\t"); if (쌍[0].equals(대상)) 기계표.put(쌍[1] + 쌍[2],쌍[3]); }
        int 자리 = 진입점.lastIndexOf('.'); if (자리 < 0) throw new 번역오류("진입점 지정 Fallu");
        String 소유 = 진입점.substring(0,자리).replace('.','/'), 함수이름 = 진입점.substring(자리 + 1); 함수참조 진입 = null;
        for (String 서술 : Arrays.asList("()I","()V")) { 함수참조 참조 = new 함수참조(소유,함수이름,서술); if (함수들.containsKey(참조)) { if (진입 != null) throw new 번역오류("겹친 진입점"); 진입 = 참조; } }
        if (진입 == null || (함수들.get(진입).접근 & 0x100) != 0) throw new 번역오류("진입 함수 형식 Fallu");
        List<String> Llinia = new ArrayList<>(); Llinia.add(".code32");
        for (클래스자료 자료 : 클래스들.values()) {
            String 상태 = 기호("state",자료.Nome), 초기화 = 기호("init",자료.Nome);
            Collections.addAll(Llinia,".bss",".balign 4",상태 + ": .long 0",".text",초기화 + ":","cmpl $0, " + 상태,"jne " + 초기화 + "_done","movl $1, " + 상태);
            함수참조 초기화참조 = new 함수참조(자료.Nome,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Llinia.add("call " + 기호("method",초기화참조.부분들()));
            Collections.addAll(Llinia,"movl $2, " + 상태,초기화 + "_done:","ret");
            for (멤버자료 필드 : 자료.필드) {
                byte[] 상수 = 필드.속성.get("ConstantValue"); String 값 = 상수 == null ? "0" : 엑스상수(자료,new 자료읽개(상수).두바이트());
                Collections.addAll(Llinia,".data",".balign 4",기호("field",자료.Nome,필드.Nome,필드.서술) + ": .long " + 값);
            }
            for (멤버자료 함수 : 자료.함수) if (!함수.Nome.equals("<init>")) Llinia.add(엑스함수본문(new 함수참조(자료.Nome,함수.Nome,함수.서술),함수,기계표,대상));
        }
        Collections.addAll(Llinia,".text",".globl java_entry","java_entry:","call " + 기호("init",진입.소유),"call " + 기호("method",진입.부분들()));
        if (진입.서술.equals("()V")) Llinia.add("xorl %eax, %eax"); Llinia.add("ret");
        for (String 지정 : 내보냄) {
            int 구분 = 지정.indexOf('='); if (구분 < 1) throw new 번역오류("내보내기 지정 Fallu");
            String 외부 = 지정.substring(0,구분), 함수 = 지정.substring(구분 + 1); int 나눔 = 함수.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 기호 Fallu");
            String 클래스 = 함수.substring(0,나눔).replace('.','/'), Nome = 함수.substring(나눔 + 1); 함수참조 선택 = null;
            for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(클래스) && 참조.Nome.equals(Nome)) { if (선택 != null) throw new 번역오류("겹친 내보내기 대상"); 선택 = 참조; }
            if (선택 == null) throw new 번역오류("내보낼 함수가 없음");
            Collections.addAll(Llinia,".text",".globl " + 외부,외부 + ":","call " + 기호("init",선택.소유),"jmp " + 기호("method",선택.부분들()));
        }
        Llinia.add(".section .rodata");
        for (Map.Entry<String,String> 항목 : 문자열들.entrySet()) {
            Collections.addAll(Llinia,".balign 4",항목.getValue() + ":",".long " + 항목.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char 단위 : 항목.getKey().toCharArray()) 단위들.add(Integer.toString(단위)); if (!단위들.isEmpty()) Llinia.add(".long " + String.join(",",단위들));
        }
        Llinia.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Llinia) + "\n";
    }
    static void 도구실행(List<String> Comandu) throws Exception {
        if (new ProcessBuilder(Comandu).inheritIO().start().waitFor() != 0) throw new 번역오류("컴파일 Fallu: " + Comandu.get(0));
    }
    static String 자료문자열(String Testu) { return "\"" + Testu.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String 대상, String 진입점, List<String> 내보냄, Path Salida, Path 자원) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), 클래스경로 = 임시.resolve("classes"); Files.createDirectory(클래스경로);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",클래스경로.toString(),"-sourcepath",클래스경로.toString(),"-d",클래스경로.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (Salida.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new 번역오류("Salida 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new 번역오류(".java 또는 .class만 지원");
            }
            if (원문수 > 0) 도구실행(자바명령);
            try (java.util.stream.Stream<Path> 경로들 = Files.walk(클래스경로)) { 경로들.filter(Camín -> Camín.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,대상.equals("user") ? "user" : "kernel",262144,자원);
            String 조립 = 변환.엑스조립본(진입점,내보냄,대상); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = 자원.getParent();
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("실행지원.s").toString()));
            List<String> Coneutar = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (대상.equals("kernel")) Coneutar.add("-r");
            else {
                도구실행(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(대상.equals("user") ? "사용자시작.s" : "리눅스시작.s").toString()));
                Collections.addAll(Coneutar,"-e","_start",임시.resolve("start.o").toString());
                if (대상.equals("user")) Collections.addAll(Coneutar,"-T",도구위치.resolve("사용자배치.ld").toString());
            }
            Collections.addAll(Coneutar,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); 도구실행(Coneutar);
            Salida = Salida.toAbsolutePath(); Files.createDirectories(Salida.getParent()); Path 게시 = Files.createTempFile(Salida.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),게시,StandardCopyOption.REPLACE_EXISTING); Files.move(게시,Salida,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(게시); }
            Files.setPosixFilePermissions(Salida,java.nio.file.attribute.PosixFilePermissions.fromString(대상.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Salida + ".s"),조립,StandardCharsets.UTF_8);
            List<String> 기호자료 = new ArrayList<>(), 원문자료 = new ArrayList<>();
            for (함수참조 참조 : 변환.함수들.keySet()) 기호자료.add(자료문자열(기호("method",참조.부분들())) + ":" + 자료문자열(참조.소유 + "." + 참조.Nome + 참조.서술));
            for (Path 입력 : 입력들) {
                byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Testu = new StringBuilder(); for (byte 값 : 해시) Testu.append(String.format(Locale.ROOT,"%02x",값 & 255));
                원문자료.add(자료문자열(입력.toAbsolutePath().toString()) + ":" + 자료문자열(Testu.toString()));
            }
            Files.writeString(Paths.get(Salida + ".json"),"{\"target\":" + 자료문자열(대상) + ",\"entry\":" + 자료문자열(진입점) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",기호자료) + "},\"sources\":{" + String.join(",",원문자료) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> 경로들 = Files.walk(임시)) { for (Path Camín : (Iterable<Path>)경로들.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Camín); }
        }
    }
    public static void main(String[] Argumentu) {
        try {
            String 진입점 = null, 대상 = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> 경로들 = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumentu.length; 순번++) {
                String 값 = Argumentu[순번];
                switch (값) {
                    case "--target": 엑스대상 = Argumentu[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry 클래스.함수 -o Salida [--target linux|kernel|user] [--profile kernel|user] [--export 기호=클래스.함수] 클래스파일 또는 Java원문"); return;
                    case "--entry": 진입점 = Argumentu[++순번]; break;
                    case "--profile": 대상 = Argumentu[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumentu[++순번]); break;
                    case "--export": 내보냄.add(Argumentu[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argumentu[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (값.startsWith("-")) throw new 번역오류("알 수 없는 옵션: " + 값); 경로들.add(Paths.get(값));
                }
            }
            if (진입점 == null || 출력경로 == null || 경로들.isEmpty()) throw new 번역오류("--entry, -o, 클래스 파일이 필요합니다");
            Path 자원 = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new 번역오류("알 수 없는 실행 대상");
                엑스번역(경로들,엑스대상,진입점,내보냄,출력경로,자원); return;
            }
            String FONTE = new 기계어미리번역(경로들, 대상, 낱말수, 자원).생성(진입점, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, FONTE, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Fallu) { System.err.println("컴파일 Fallu: " + Fallu.getMessage()); System.exit(1); }
    }
}
