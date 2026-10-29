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
        int 위치;
        자료읽개(byte[] 입력자료) { 자료 = 입력자료; }
        byte[] Okuma(int 길이) {
            if (길이 < 0 || 길이 > 자료.length - 위치) throw new 번역오류("잘린 클래스 또는 Komut 자료");
            byte[] 결과 = Arrays.copyOfRange(자료, 위치, 위치 + 길이); 위치 += 길이; return 결과;
        }
        int 한바이트() { if (위치 >= 자료.length) throw new 번역오류("잘린 Komut 자료"); return 자료[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class 멤버자료 {
        final int 접근;
        final String İsim, 서술;
        final Map<String, byte[]> 속성;
        멤버자료(int 접근값, String 이름값, String 서술값, Map<String, byte[]> 속성값) {
            접근 = 접근값; İsim = 이름값; 서술 = 서술값; 속성 = 속성값;
        }
    }
    static final class 함수참조 implements Comparable<함수참조> {
        final String 소유, İsim, 서술;
        함수참조(String 소유값, String 이름값, String 서술값) { 소유 = 소유값; İsim = 이름값; 서술 = 서술값; }
        String[] 부분들() { return new String[]{소유, İsim, 서술}; }
        public int compareTo(함수참조 상대) {
            int 비교값 = 소유.compareTo(상대.소유);
            if (비교값 == 0) 비교값 = İsim.compareTo(상대.İsim);
            return 비교값 == 0 ? 서술.compareTo(상대.서술) : 비교값;
        }
        public boolean equals(Object 상대) { return 상대 instanceof 함수참조 && compareTo((함수참조) 상대) == 0; }
        public int hashCode() { return Objects.hash(소유, İsim, 서술); }
    }
    static final class 클래스자료 {
        final int[] 상수종류;
        final Object[] 상수값;
        final String İsim;
        final List<멤버자료> 필드, 함수;
        클래스자료(Path Yolçıq) throws IOException {
            자료읽개 읽개 = new 자료읽개(Files.readAllBytes(Yolçıq));
            if (읽개.네바이트() != 0xcafebabe) throw new 번역오류("Java 클래스 표식이 아님");
            읽개.Okuma(4);
            int 개수 = 읽개.두바이트(); 상수종류 = new int[개수]; 상수값 = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = 읽개.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int 길이 = 읽개.두바이트();
                        byte[] 문자자료 = 읽개.Okuma(길이), 길이붙인자료 = new byte[길이 + 2];
                        길이붙인자료[0] = (byte)(길이 >> 8); 길이붙인자료[1] = (byte)길이;
                        System.arraycopy(문자자료, 0, 길이붙인자료, 2, 길이);
                        상수값[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: 상수값[순번] = 읽개.네바이트(); break;
                    case 4: 읽개.Okuma(4); break;
                    case 5: case 6: 읽개.Okuma(8); 순번++; break;
                    case 7: case 8: case 16: 상수값[순번] = 읽개.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        상수값[순번] = new int[]{읽개.두바이트(), 읽개.두바이트()}; break;
                    case 15: 상수값[순번] = new int[]{읽개.한바이트(), 읽개.두바이트()}; break;
                    default: throw new 번역오류("지원하지 않는 상수 종류: " + 종류);
                }
            }
            읽개.두바이트(); İsim = 클래스명(읽개.두바이트());
            if (!클래스명(읽개.두바이트()).equals("java/lang/Object") || 읽개.두바이트() != 0)
                throw new 번역오류(İsim + ": 상속 및 인터페이스 미지원");
            필드 = 멤버읽기(읽개); 함수 = 멤버읽기(읽개); 속성읽기(읽개);
            if (읽개.위치 != 읽개.자료.length) throw new 번역오류("클래스 뒤에 남은 자료");
        }
        String 문자(int 번호) {
            if (번호 < 1 || 번호 >= 상수종류.length || 상수종류[번호] != 1) throw new 번역오류("문자 상수 번호 Hata");
            return (String) 상수값[번호];
        }
        String 클래스명(int 번호) {
            if (번호 < 1 || 번호 >= 상수종류.length || 상수종류[번호] != 7) throw new 번역오류("클래스 참조 Hata");
            return 문자((Integer)상수값[번호]);
        }
        함수참조 참조(int 번호) {
            if (번호 < 1 || 번호 >= 상수종류.length || 상수종류[번호] < 9 || 상수종류[번호] > 11) throw new 번역오류("멤버 참조 Hata");
            int[] 쌍 = (int[])상수값[번호], 이름쌍 = (int[])상수값[쌍[1]];
            return new 함수참조(클래스명(쌍[0]), 문자(이름쌍[0]), 문자(이름쌍[1]));
        }
        Map<String, byte[]> 속성읽기(자료읽개 읽개) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = 읽개.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String 속성이름 = 문자(읽개.두바이트()); byte[] 값 = 읽개.Okuma(읽개.네바이트());
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
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new 번역오류("함수 서술 Hata: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new 번역오류("함수 서술 Hata: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new 번역오류("함수 서술 Hata: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String 선택 = null;
            for (String 형식 : 허용형식) if (서술.startsWith(형식, 위치)) { 선택 = 형식; break; }
            if (선택 == null) throw new 번역오류("지원하지 않는 자료형: " + 서술);
            결과.add(선택); 위치 += 선택.length();
        }
        return 결과;
    }
    static String 기호(String 종류, String... 부분들) {
        try {
            byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Metin = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Metin.append(String.format(Locale.ROOT, "%02x", 해시[순번] & 255));
            return Metin.toString();
        } catch (Exception Hata) { throw new 번역오류(Hata.toString()); }
    }
    final Map<String, 클래스자료> 클래스들 = new TreeMap<>();
    final Map<함수참조, 멤버자료> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, 기계클래스;
    final int 동적기억낱말수;
    final Path 자원경로;
    기계어미리번역(List<Path> 경로들, String 대상, int 낱말수, Path 자원) throws IOException {
        if ((!대상.equals("kernel") && !대상.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new 번역오류("실행 대상 또는 기억 공간 Boyut Hata");
        실행대상 = 대상; 동적기억낱말수 = 낱말수; 자원경로 = 자원;
        // 이 이름도 국가별 소스 생성 시 해당 언어로 옮긴다.
        기계클래스 = 대상.equals("kernel") ? "보드" : "사용자";
        for (String 줄 : Files.readAllLines(자원.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = 줄.split("\t", -1);
            if (부분들.length != 4) throw new 번역오류("기계 함수 자료 Hata");
            if (부분들[0].equals(대상)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Yolçıq : 경로들) {
            클래스자료 자료 = new 클래스자료(Yolçıq);
            if (클래스들.put(자료.İsim, 자료) != null) throw new 번역오류("중복 클래스: " + 자료.İsim);
            for (멤버자료 필드 : 자료.필드) {
                if ((필드.접근 & 8) == 0 || 형식읽기(필드.서술).equals(Collections.singletonList("V"))) throw new 번역오류("정적 필드만 지원");
                if (필드들.put(new 함수참조(자료.İsim, 필드.İsim, 필드.서술), 필드) != null) throw new 번역오류("중복 필드");
            }
            for (멤버자료 함수 : 자료.함수) {
                if (함수.İsim.equals("<init>")) continue;
                if ((함수.접근 & 8) == 0 || (함수.접근 & (0x20 | 0x400)) != 0) throw new 번역오류("정적 비동기화 함수만 지원");
                new 함수형식(함수.서술);
                if (함수들.put(new 함수참조(자료.İsim, 함수.İsim, 함수.서술), 함수) != null) throw new 번역오류("중복 함수");
            }
        }
    }
    String 문자열기호(String Metin) { return 문자열들.computeIfAbsent(Metin, 값 -> "j_text_" + 문자열들.size()); }
    String 상수표현(클래스자료 자료, int 번호) {
        if (번호 < 1 || 번호 >= 자료.상수종류.length) throw new 번역오류("상수 번호 범위 Hata");
        if (자료.상수종류[번호] == 3) return "(word)(uint32_t)(" + 자료.상수값[번호] + ")";
        if (자료.상수종류[번호] == 8) return "(word)" + 문자열기호(자료.문자((Integer)자료.상수값[번호]));
        throw new 번역오류("정수와 문자열 상수만 지원");
    }
    String 함수원형(함수참조 참조) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(참조.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + 기호("method", 참조.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void 지역검사(int 번호, int 지역변수수) { if (번호 < 0 || 번호 >= 지역변수수) throw new 번역오류("지역 변수 번호 범위 Hata"); }
    void 분기넣기(List<String> 출력, Set<Integer> 분기들, int 위치, int 이동량, String 조건) {
        int 목적 = 위치 + 이동량; 분기들.add(목적);
        출력.add((조건 == null ? "" : "if (" + 조건 + ") ") + "goto b" + 목적 + ";");
    }
    String 함수본문(함수참조 함수, 멤버자료 자료) {
        byte[] 본문자료 = 자료.속성.get("Code"); if (본문자료 == null) throw new 번역오류("함수 몸체가 없음: " + 함수.İsim);
        자료읽개 읽개 = new 자료읽개(본문자료); int 쌓임깊이 = 읽개.두바이트(), 지역변수수 = 읽개.두바이트();
        자료읽개 명령자료 = new 자료읽개(읽개.Okuma(읽개.네바이트()));
        if (읽개.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 형식 = new 함수형식(함수.서술); if (지역변수수 < 형식.인수.size()) throw new 번역오류("매개변수보다 적은 지역 변수");
        클래스자료 클래스 = 클래스들.get(함수.소유);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(함수) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < 형식.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (명령자료.위치 < 명령자료.자료.length) {
            int 위치 = 명령자료.위치, Komut = 명령자료.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (Komut == 0) continue;
            if (Komut == 1) 출력.add("PUSH(0);");
            else if (Komut >= 2 && Komut <= 8) 출력.add("PUSH((uint32_t)(" + (Komut - 3) + "));");
            else if (Komut == 16 || Komut == 17) 출력.add("PUSH((uint32_t)(" + (Komut == 16 ? 명령자료.부호한바이트() : 명령자료.부호두바이트()) + "));");
            else if (Komut == 18 || Komut == 19) 출력.add("PUSH(" + 상수표현(클래스, Komut == 18 ? 명령자료.한바이트() : 명령자료.두바이트()) + ");");
            else if (Komut == 21 || Komut == 25 || (Komut >= 26 && Komut <= 29) || (Komut >= 42 && Komut <= 45)) {
                int 번호 = Komut == 21 || Komut == 25 ? 명령자료.한바이트() : Komut - (Komut <= 29 ? 26 : 42);
                지역검사(번호, 지역변수수); 출력.add("PUSH(l[" + 번호 + "]);");
            } else if (Komut == 54 || Komut == 58 || (Komut >= 59 && Komut <= 62) || (Komut >= 75 && Komut <= 78)) {
                int 번호 = Komut == 54 || Komut == 58 ? 명령자료.한바이트() : Komut - (Komut <= 62 ? 59 : 75);
                지역검사(번호, 지역변수수); 출력.add("l[" + 번호 + "] = POP();");
            } else if (Komut == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Komut == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Komut == 87 || Komut == 88) 출력.add(Komut == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Komut >= 89 && Komut <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] 순서들 = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Komut - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char 값 : 순서들[Komut - 89].toCharArray()) 출력.add("PUSH(" + 값 + ");");
            } else if (Komut == 96 || Komut == 100 || Komut == 104 || Komut == 126 || Komut == 128 || Komut == 130) {
                String 연산 = Komut == 96 ? "+" : Komut == 100 ? "-" : Komut == 104 ? "*" : Komut == 126 ? "&" : Komut == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + 연산 + " (uint32_t)b);");
            } else if (Komut == 108 || Komut == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Komut == 112 ? 1 : 0) + "));");
            else if (Komut == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Komut == 120 || Komut == 122 || Komut == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Komut == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Komut == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Komut == 132) {
                int 번호 = 명령자료.한바이트(), 증가량 = 명령자료.부호한바이트(); 지역검사(번호, 지역변수수);
                출력.add("l[" + 번호 + "] = (uint32_t)l[" + 번호 + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Komut >= 145 && Komut <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Komut == 145 ? "int8_t" : Komut == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Komut >= 153 && Komut <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, 분기들, 위치, 명령자료.부호두바이트(), "(int32_t)a " + 비교들[Komut - 153] + " 0");
            } else if (Komut >= 159 && Komut <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, 분기들, 위치, 명령자료.부호두바이트(), Komut >= 165 ? "a " + 비교들[Komut - 159] + " b" : "(int32_t)a " + 비교들[Komut - 159] + " (int32_t)b");
            } else if (Komut == 167 || Komut == 200) 분기넣기(출력, 분기들, 위치, Komut == 167 ? 명령자료.부호두바이트() : 명령자료.네바이트(), null);
            else if (Komut == 170 || Komut == 171) {
                while (명령자료.위치 % 4 != 0) 명령자료.한바이트();
                int 기본 = 명령자료.네바이트(); 출력.add("a = POP();");
                if (Komut == 170) {
                    int 아래 = 명령자료.네바이트(), 위 = 명령자료.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (명령자료.자료.length - 명령자료.위치) / 4) throw new 번역오류("switch 범위 Hata");
                    for (long 값 = 아래; 값 <= 위; 값++) 분기넣기(출력, 분기들, 위치, 명령자료.네바이트(), "(int32_t)a == (" + 값 + ")");
                } else {
                    int 개수 = 명령자료.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (명령자료.자료.length - 명령자료.위치) / 8) throw new 번역오류("switch Boyut Hata");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int 값 = 명령자료.네바이트(); if (순번 > 0 && 값 <= 앞값) throw new 번역오류("switch 순서 Hata"); 앞값 = 값;
                        분기넣기(출력, 분기들, 위치, 명령자료.네바이트(), "(int32_t)a == (" + 값 + ")");
                    }
                }
                분기넣기(출력, 분기들, 위치, 기본, null);
            } else if (Komut == 172 || Komut == 176 || Komut == 177) 출력.add("return " + (Komut == 177 ? "0" : "POP()") + ";");
            else if (Komut == 178 || Komut == 179) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 필드");
                출력.add(기호("init", 참조.소유) + "();"); String 필드 = 기호("field", 참조.부분들());
                출력.add(Komut == 178 ? "PUSH(" + 필드 + ");" : 필드 + " = POP();");
            } else if (Komut == 184) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 함수");
                함수형식 호출형식 = new 함수형식(참조.서술); int 개수 = 호출형식.인수.size();
                출력.add(기호("init", 참조.소유) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + 기호("method", 참조.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Komut == 182) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트());
                if (참조.equals(new 함수참조("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (참조.equals(new 함수참조("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 번역오류("가상 함수 호출 미지원");
            } else if (Komut == 188) {
                if (명령자료.한바이트() != 10) throw new 번역오류("new int[]만 지원"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Komut == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Komut == 196) {
                int 확장 = 명령자료.한바이트(), 번호 = 명령자료.두바이트(); 지역검사(번호, 지역변수수);
                if (확장 == 21 || 확장 == 25) 출력.add("PUSH(l[" + 번호 + "]);");
                else if (확장 == 54 || 확장 == 58) 출력.add("l[" + 번호 + "] = POP();");
                else if (확장 == 132) 출력.add("l[" + 번호 + "] = (uint32_t)l[" + 번호 + "] + (uint32_t)(" + 명령자료.부호두바이트() + ");");
                else throw new 번역오류("미지원 wide Komut");
            } else if (Komut == 198 || Komut == 199) {
                출력.add("a = POP();"); 분기넣기(출력, 분기들, 위치, 명령자료.부호두바이트(), "a " + (Komut == 198 ? "==" : "!=") + " 0");
            } else throw new 번역오류(함수.소유 + "." + 함수.İsim + ", 바이트 " + 위치 + ": 미지원 Komut " + Komut);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("Komut 경계가 아닌 곳으로 분기");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String 내보낼함수(String 연결기호, String 대상, boolean 진입점여부) {
        int 자리 = 대상.lastIndexOf('.'); if (자리 < 0 || !연결기호.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 지정 Hata");
        String 소유 = 대상.substring(0, 자리).replace('.', '/'), İsim = 대상.substring(자리 + 1); 함수참조 선택 = null;
        for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(소유) && 참조.İsim.equals(İsim)) {
            if (선택 != null) throw new 번역오류("겹친 내보내기 대상"); 선택 = 참조;
        }
        if (선택 == null || (함수들.get(선택).접근 & 0x100) != 0) throw new 번역오류("내보낼 함수가 없음 또는 native 함수");
        함수형식 형식 = new 함수형식(선택.서술);
        if ((진입점여부 && !형식.인수.isEmpty()) || !Arrays.asList("V", "I").contains(형식.반환)) throw new 번역오류("진입 또는 C 경계 형식 Hata");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < 형식.인수.size(); 순번++) {
            if (!형식.인수.get(순번).equals("I")) throw new 번역오류("C 경계는 int 인수만 지원");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (형식.반환.equals("V") ? "void " : "int32_t ") + 연결기호 + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + 기호("init", 선택.소유) + "(); " + (형식.반환.equals("V") ? "" : "return (int32_t)") + 기호("method", 선택.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String 진입점, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<함수참조, 멤버자료> 항목 : 함수들.entrySet()) {
            함수참조 참조 = 항목.getKey(); 멤버자료 자료 = 항목.getValue(); 선언들.add(함수원형(참조) + ";");
            if ((자료.접근 & 0x100) != 0) {
                String Bağlan = 기계함수들.get(참조.İsim + 참조.서술);
                if (!참조.소유.equals(기계클래스) || Bağlan == null) throw new 번역오류("허용되지 않은 native 함수: " + 참조.İsim);
                int 개수 = new 함수형식(참조.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Bağlan + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(참조) + " { return " + Bağlan + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(참조, 자료));
        }
        for (Map.Entry<함수참조, 멤버자료> 항목 : 필드들.entrySet()) {
            함수참조 참조 = 항목.getKey(); byte[] 상수 = 항목.getValue().속성.get("ConstantValue");
            String 값 = 상수 == null ? "0" : 상수표현(클래스들.get(참조.소유), new 자료읽개(상수).두바이트());
            필드선언들.add("static word " + 기호("field", 참조.부분들()) + " = " + 값 + ";");
        }
        for (String İsim : 클래스들.keySet()) {
            String 초기화 = 기호("init", İsim), 상태 = 기호("state", İsim);
            선언들.add("static void " + 초기화 + "(void);"); 필드선언들.add("static unsigned " + 상태 + ";");
            함수참조 참조 = new 함수참조(İsim, "<clinit>", "()V");
            몸체들.add("static void " + 초기화 + "(void) { if(" + 상태 + ") return; " + 상태 + " = 1; " + (함수들.containsKey(참조) ? 기호("method", 참조.부분들()) + "(); " : "") + 상태 + " = 2; }");
        }
        몸체들.add(내보낼함수("java_entry", 진입점, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new 번역오류("내보내기 지정 Hata");
            String İsim = 지정.substring(0, 자리); 공개이름.add(İsim); 몸체들.add(내보낼함수(İsim, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> 항목 : 문자열들.entrySet()) {
            String Metin = 항목.getKey(); StringBuilder 배열 = new StringBuilder("static const word " + 항목.getValue() + "[] = {" + Metin.length());
            for (int 순번 = 0; 순번 < Metin.length(); 순번++) 배열.append(", ").append((int)Metin.charAt(순번));
            문자열선언들.add(배열.append("};").toString());
        }
        String 지원 = Files.readString(자원경로.resolve("실행지원.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(지원 + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String Kaynak, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> 이름표 = new HashMap<>();
        for (String 줄 : Files.readAllLines(자원경로.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] 쌍 = 줄.split("\t"); 이름표.put(쌍[0], 쌍[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(Kaynak); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String İsim = 찾개.group(), 새이름 = İsim;
            if (!İsim.startsWith("//") && !İsim.startsWith("/*") && !İsim.startsWith("\"") && !İsim.startsWith("'") && !공개이름.contains(İsim)) {
                새이름 = 이름표.getOrDefault(İsim, İsim);
                if (İsim.matches("a[0-9]+")) 새이름 = "인수" + İsim.substring(1);
                if (İsim.matches("b[0-9]+")) 새이름 = "분기" + İsim.substring(1);
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
        List<String> 줄 = new ArrayList<>();
        if ((자료.접근 & 0x100) != 0) {
            String Bağlan = 기계표.get(함수.İsim + 함수.서술);
            if (!함수.소유.equals(대상.equals("kernel") ? "장치" : "사용자") || Bağlan == null) throw new 번역오류("허용되지 않은 native 함수");
            return ".text\n" + 표식 + ":\njmp " + Bağlan;
        }
        byte[] 본문 = 자료.속성.get("Code"); if (본문 == null) throw new 번역오류("함수 몸체가 없음");
        자료읽개 읽개 = new 자료읽개(본문); 읽개.두바이트(); int 지역수 = 읽개.두바이트();
        자료읽개 명령자료 = new 자료읽개(읽개.Okuma(읽개.네바이트()));
        if (읽개.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 형식 = new 함수형식(함수.서술); if (지역수 < 형식.인수.size()) throw new 번역오류("매개변수보다 적은 지역 변수");
        Collections.addAll(줄,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < 형식.인수.size(); 순번++) Collections.addAll(줄,"movl " + (8 + 4 * (형식.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        클래스자료 클래스 = 클래스들.get(함수.소유); Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (명령자료.위치 < 명령자료.자료.length) {
            int 위치 = 명령자료.위치, Komut = 명령자료.한바이트(); String 자리 = 표식 + "_b" + 위치;
            줄.add(자리 + ":"); 경계들.add(위치);
            if (Komut == 0) 줄.add("nop");
            else if (Komut == 1) 줄.add("pushl $0");
            else if (Komut >= 2 && Komut <= 8) 줄.add("pushl $" + (Komut - 3));
            else if (Komut == 16 || Komut == 17) 줄.add("pushl $" + (Komut == 16 ? 명령자료.부호한바이트() : 명령자료.부호두바이트()));
            else if (Komut == 18 || Komut == 19) {
                int 번호 = Komut == 18 ? 명령자료.한바이트() : 명령자료.두바이트();
                줄.add("pushl $" + 엑스상수(클래스,번호));
            } else if (Komut == 21 || Komut == 25 || (Komut >= 26 && Komut <= 29) || (Komut >= 42 && Komut <= 45) || Komut == 54 || Komut == 58 || (Komut >= 59 && Komut <= 62) || (Komut >= 75 && Komut <= 78)) {
                boolean 읽음 = Komut < 54; int 번호 = Komut == 21 || Komut == 25 || Komut == 54 || Komut == 58 ? 명령자료.한바이트() : Komut - (Komut <= 29 ? 26 : Komut <= 45 ? 42 : Komut <= 62 ? 59 : 75);
                지역검사(번호,지역수); 줄.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (번호 + 1)) + "(%ebp)");
            } else if (Komut == 46) Collections.addAll(줄,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Komut == 79) Collections.addAll(줄,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Komut == 87 || Komut == 88) 줄.add("addl $" + (Komut == 87 ? 4 : 8) + ", %esp");
            else if (Komut >= 89 && Komut <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] 순서들 = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Komut - 89]; 순번++) 줄.add("popl " + 저장기들[순번]);
                for (int 순번 : 순서들[Komut - 89]) 줄.add("pushl " + 저장기들[순번]);
            } else if (Komut == 96 || Komut == 100 || Komut == 104 || Komut == 126 || Komut == 128 || Komut == 130) {
                String 연산 = Komut == 96 ? "addl" : Komut == 100 ? "subl" : Komut == 104 ? "imull" : Komut == 126 ? "andl" : Komut == 128 ? "orl" : "xorl";
                Collections.addAll(줄,"popl %ecx","popl %eax",연산 + " %ecx, %eax","pushl %eax");
            } else if (Komut == 108 || Komut == 112) Collections.addAll(줄,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Komut == 108 ? "%eax" : "%edx"));
            else if (Komut == 116) 줄.add("negl (%esp)");
            else if (Komut == 120 || Komut == 122 || Komut == 124) Collections.addAll(줄,"popl %ecx","popl %eax",(Komut == 120 ? "sall" : Komut == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Komut == 132) {
                int 번호 = 명령자료.한바이트(), 증가 = 명령자료.부호한바이트(); 지역검사(번호,지역수); 줄.add("addl $" + 증가 + ", -" + (4 * (번호 + 1)) + "(%ebp)");
            } else if (Komut >= 145 && Komut <= 147) Collections.addAll(줄,"popl %eax",Komut == 145 ? "movsbl %al, %eax" : Komut == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Komut >= 153 && Komut <= 166) {
                if (Komut <= 158) Collections.addAll(줄,"popl %eax","testl %eax, %eax");
                else Collections.addAll(줄,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int 목적 = 위치 + 명령자료.부호두바이트(); 분기들.add(목적); 줄.add(비교들[Komut - (Komut <= 158 ? 153 : 159)] + " " + 표식 + "_b" + 목적);
            } else if (Komut == 167 || Komut == 200) {
                int 목적 = 위치 + (Komut == 167 ? 명령자료.부호두바이트() : 명령자료.네바이트()); 분기들.add(목적); 줄.add("jmp " + 표식 + "_b" + 목적);
            } else if (Komut == 170 || Komut == 171) {
                while (명령자료.위치 % 4 != 0) 명령자료.한바이트();
                int 기본 = 위치 + 명령자료.네바이트(); 분기들.add(기본); 줄.add("popl %eax");
                int 개수, 아래 = 0;
                if (Komut == 170) { 아래 = 명령자료.네바이트(); int 위 = 명령자료.네바이트(); long 길이 = (long)위 - 아래 + 1; if (길이 < 1 || 길이 > (명령자료.자료.length - 명령자료.위치) / 4) throw new 번역오류("switch 범위 Hata"); 개수 = (int)길이; }
                else { 개수 = 명령자료.네바이트(); if (개수 < 0 || 개수 > (명령자료.자료.length - 명령자료.위치) / 8) throw new 번역오류("switch Boyut Hata"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int 값 = Komut == 170 ? 아래 + 순번 : 명령자료.네바이트(), 목적 = 위치 + 명령자료.네바이트(); 분기들.add(목적);
                    Collections.addAll(줄,"cmpl $" + 값 + ", %eax","je " + 표식 + "_b" + 목적);
                }
                줄.add("jmp " + 표식 + "_b" + 기본);
            } else if (Komut == 172 || Komut == 176 || Komut == 177) {
                if (Komut != 177) 줄.add("popl %eax"); Collections.addAll(줄,"leave","ret");
            } else if (Komut == 178 || Komut == 179) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 필드");
                Collections.addAll(줄,"call " + 기호("init",참조.소유),(Komut == 178 ? "pushl " : "popl ") + 기호("field",참조.부분들()));
            } else if (Komut == 184) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 함수");
                함수형식 호출형식 = new 함수형식(참조.서술); Collections.addAll(줄,"call " + 기호("init",참조.소유),"call " + 기호("method",참조.부분들()));
                if (!호출형식.인수.isEmpty()) 줄.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) 줄.add("pushl %eax");
            } else if (Komut == 182) {
                함수참조 참조 = 클래스.참조(명령자료.두바이트());
                if (참조.equals(new 함수참조("java/lang/String","length","()I"))) Collections.addAll(줄,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (참조.equals(new 함수참조("java/lang/String","charAt","(I)C"))) Collections.addAll(줄,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 번역오류("가상 함수 호출 미지원");
            } else if (Komut == 188) {
                if (명령자료.한바이트() != 10) throw new 번역오류("new int[]만 지원"); Collections.addAll(줄,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Komut == 190) Collections.addAll(줄,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Komut == 196) {
                int 확장 = 명령자료.한바이트(), 번호 = 명령자료.두바이트(); 지역검사(번호,지역수);
                if (확장 == 21 || 확장 == 25 || 확장 == 54 || 확장 == 58) 줄.add((확장 <= 25 ? "pushl " : "popl ") + "-" + 4 * (번호 + 1) + "(%ebp)");
                else if (확장 == 132) 줄.add("addl $" + 명령자료.부호두바이트() + ", -" + 4 * (번호 + 1) + "(%ebp)");
                else throw new 번역오류("wide Komut 미지원");
            } else if (Komut == 198 || Komut == 199) {
                int 목적 = 위치 + 명령자료.부호두바이트(); 분기들.add(목적); Collections.addAll(줄,"popl %eax","testl %eax, %eax",(Komut == 198 ? "je " : "jne ") + 표식 + "_b" + 목적);
            } else throw new 번역오류("미지원 Komut: " + Komut);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("Komut 경계가 아닌 곳으로 분기");
        줄.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",줄);
    }
    String 엑스상수(클래스자료 자료, int 번호) {
        if (자료.상수종류[번호] == 3) return 자료.상수값[번호].toString();
        if (자료.상수종류[번호] == 8) return 문자열기호(자료.문자((Integer)자료.상수값[번호]));
        throw new 번역오류("정수와 문자열 상수만 지원");
    }
    String 엑스조립본(String 진입점, List<String> 내보냄, String 대상) throws IOException {
        Map<String,String> 기계표 = new HashMap<>();
        for (String 줄 : Files.readAllLines(자원경로.resolve("엑스기계함수.tsv"))) { String[] 쌍 = 줄.split("\t"); if (쌍[0].equals(대상)) 기계표.put(쌍[1] + 쌍[2],쌍[3]); }
        int 자리 = 진입점.lastIndexOf('.'); if (자리 < 0) throw new 번역오류("진입점 지정 Hata");
        String 소유 = 진입점.substring(0,자리).replace('.','/'), 함수이름 = 진입점.substring(자리 + 1); 함수참조 진입 = null;
        for (String 서술 : Arrays.asList("()I","()V")) { 함수참조 참조 = new 함수참조(소유,함수이름,서술); if (함수들.containsKey(참조)) { if (진입 != null) throw new 번역오류("겹친 진입점"); 진입 = 참조; } }
        if (진입 == null || (함수들.get(진입).접근 & 0x100) != 0) throw new 번역오류("진입 함수 형식 Hata");
        List<String> 줄 = new ArrayList<>(); 줄.add(".code32");
        for (클래스자료 자료 : 클래스들.values()) {
            String 상태 = 기호("state",자료.İsim), 초기화 = 기호("init",자료.İsim);
            Collections.addAll(줄,".bss",".balign 4",상태 + ": .long 0",".text",초기화 + ":","cmpl $0, " + 상태,"jne " + 초기화 + "_done","movl $1, " + 상태);
            함수참조 초기화참조 = new 함수참조(자료.İsim,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) 줄.add("call " + 기호("method",초기화참조.부분들()));
            Collections.addAll(줄,"movl $2, " + 상태,초기화 + "_done:","ret");
            for (멤버자료 필드 : 자료.필드) {
                byte[] 상수 = 필드.속성.get("ConstantValue"); String 값 = 상수 == null ? "0" : 엑스상수(자료,new 자료읽개(상수).두바이트());
                Collections.addAll(줄,".data",".balign 4",기호("field",자료.İsim,필드.İsim,필드.서술) + ": .long " + 값);
            }
            for (멤버자료 함수 : 자료.함수) if (!함수.İsim.equals("<init>")) 줄.add(엑스함수본문(new 함수참조(자료.İsim,함수.İsim,함수.서술),함수,기계표,대상));
        }
        Collections.addAll(줄,".text",".globl java_entry","java_entry:","call " + 기호("init",진입.소유),"call " + 기호("method",진입.부분들()));
        if (진입.서술.equals("()V")) 줄.add("xorl %eax, %eax"); 줄.add("ret");
        for (String 지정 : 내보냄) {
            int 구분 = 지정.indexOf('='); if (구분 < 1) throw new 번역오류("내보내기 지정 Hata");
            String 외부 = 지정.substring(0,구분), 함수 = 지정.substring(구분 + 1); int 나눔 = 함수.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 기호 Hata");
            String 클래스 = 함수.substring(0,나눔).replace('.','/'), İsim = 함수.substring(나눔 + 1); 함수참조 선택 = null;
            for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(클래스) && 참조.İsim.equals(İsim)) { if (선택 != null) throw new 번역오류("겹친 내보내기 대상"); 선택 = 참조; }
            if (선택 == null) throw new 번역오류("내보낼 함수가 없음");
            Collections.addAll(줄,".text",".globl " + 외부,외부 + ":","call " + 기호("init",선택.소유),"jmp " + 기호("method",선택.부분들()));
        }
        줄.add(".section .rodata");
        for (Map.Entry<String,String> 항목 : 문자열들.entrySet()) {
            Collections.addAll(줄,".balign 4",항목.getValue() + ":",".long " + 항목.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char 단위 : 항목.getKey().toCharArray()) 단위들.add(Integer.toString(단위)); if (!단위들.isEmpty()) 줄.add(".long " + String.join(",",단위들));
        }
        줄.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",줄) + "\n";
    }
    static void 도구실행(List<String> Komut) throws Exception {
        if (new ProcessBuilder(Komut).inheritIO().start().waitFor() != 0) throw new 번역오류("컴파일 Hata: " + Komut.get(0));
    }
    static String 자료문자열(String Metin) { return "\"" + Metin.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String 대상, String 진입점, List<String> 내보냄, Path 출력, Path 자원) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), 클래스경로 = 임시.resolve("classes"); Files.createDirectory(클래스경로);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",클래스경로.toString(),"-sourcepath",클래스경로.toString(),"-d",클래스경로.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new 번역오류("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new 번역오류(".java 또는 .class만 지원");
            }
            if (원문수 > 0) 도구실행(자바명령);
            try (java.util.stream.Stream<Path> 경로들 = Files.walk(클래스경로)) { 경로들.filter(Yolçıq -> Yolçıq.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,대상.equals("user") ? "user" : "kernel",262144,자원);
            String 조립 = 변환.엑스조립본(진입점,내보냄,대상); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = 자원.getParent();
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("실행지원.s").toString()));
            List<String> Bağlan = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (대상.equals("kernel")) Bağlan.add("-r");
            else {
                도구실행(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(대상.equals("user") ? "사용자시작.s" : "리눅스시작.s").toString()));
                Collections.addAll(Bağlan,"-e","_start",임시.resolve("start.o").toString());
                if (대상.equals("user")) Collections.addAll(Bağlan,"-T",도구위치.resolve("사용자배치.ld").toString());
            }
            Collections.addAll(Bağlan,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); 도구실행(Bağlan);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path 게시 = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),게시,StandardCopyOption.REPLACE_EXISTING); Files.move(게시,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(게시); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(대상.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> 기호자료 = new ArrayList<>(), 원문자료 = new ArrayList<>();
            for (함수참조 참조 : 변환.함수들.keySet()) 기호자료.add(자료문자열(기호("method",참조.부분들())) + ":" + 자료문자열(참조.소유 + "." + 참조.İsim + 참조.서술));
            for (Path 입력 : 입력들) {
                byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Metin = new StringBuilder(); for (byte 값 : 해시) Metin.append(String.format(Locale.ROOT,"%02x",값 & 255));
                원문자료.add(자료문자열(입력.toAbsolutePath().toString()) + ":" + 자료문자열(Metin.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + 자료문자열(대상) + ",\"entry\":" + 자료문자열(진입점) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",기호자료) + "},\"sources\":{" + String.join(",",원문자료) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> 경로들 = Files.walk(임시)) { for (Path Yolçıq : (Iterable<Path>)경로들.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Yolçıq); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String 진입점 = null, 대상 = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> 경로들 = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String 값 = 인수[순번];
                switch (값) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry 클래스.함수 -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export 기호=클래스.함수] 클래스파일 또는 Java원문"); return;
                    case "--entry": 진입점 = 인수[++순번]; break;
                    case "--profile": 대상 = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
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
            String Kaynak = new 기계어미리번역(경로들, 대상, 낱말수, 자원).생성(진입점, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, Kaynak, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Hata) { System.err.println("컴파일 Hata: " + Hata.getMessage()); System.exit(1); }
    }
}
