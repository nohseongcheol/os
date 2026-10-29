// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java پاړکى_ارزښت 파일에서 독립 ARM64 커널용 C 원문을 만든다. کوربه JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class 번역오류 extends RuntimeException {
        번역오류(String 설명) { super(설명); }
    }
    static final class اومتوک_لوستونکی {
        final byte[] اومتوک;
        int ځای;
        اومتوک_لوستونکی(byte[] 입력자료) { اومتوک = 입력자료; }
        byte[] لوستل(int اوږدوالى_ارزښت) {
            if (اوږدوالى_ارزښت < 0 || اوږدوالى_ارزښت > اومتوک.length - ځای) throw new 번역오류("잘린 پاړکى_ارزښت 또는 بولۍ اومتوک");
            byte[] 결과 = Arrays.copyOfRange(اومتوک, ځای, ځای + اوږدوالى_ارزښت); ځای += اوږدوالى_ارزښت; return 결과;
        }
        int 한바이트() { if (ځای >= اومتوک.length) throw new 번역오류("잘린 بولۍ اومتوک"); return اومتوک[ځای++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class شمېره_اومتوک {
        final int رسى_ننوت;
        final String نوم, 서술;
        final Map<String, byte[]> ځانتیا_ارزښت;
        شمېره_اومتوک(int رسى_ارزښت, String 이름값, String 서술값, Map<String, byte[]> ځانتیا_اومتوک) {
            رسى_ننوت = رسى_ارزښت; نوم = 이름값; 서술 = 서술값; ځانتیا_ارزښت = ځانتیا_اومتوک;
        }
    }
    static final class 함수참조 implements Comparable<함수참조> {
        final String 소유, نوم, 서술;
        함수참조(String 소유값, String 이름값, String 서술값) { 소유 = 소유값; نوم = 이름값; 서술 = 서술값; }
        String[] 부분들() { return new String[]{소유, نوم, 서술}; }
        public int compareTo(함수참조 جوړه_ارزښت) {
            int 비교값 = 소유.compareTo(جوړه_ارزښت.소유);
            if (비교값 == 0) 비교값 = نوم.compareTo(جوړه_ارزښت.نوم);
            return 비교값 == 0 ? 서술.compareTo(جوړه_ارزښت.서술) : 비교값;
        }
        public boolean equals(Object جوړه_ارزښت) { return جوړه_ارزښت instanceof 함수참조 && compareTo((함수참조) جوړه_ارزښت) == 0; }
        public int hashCode() { return Objects.hash(소유, نوم, 서술); }
    }
    static final class پاړکى_اومتوک {
        final int[] 상수종류;
        final Object[] درېدلى_اومتوک;
        final String نوم;
        final List<شمېره_اومتوک> ډګر_ارزښت, 함수;
        پاړکى_اومتوک(Path يونلور) throws IOException {
            اومتوک_لوستونکی لوستونکی_ارزښت = new اومتوک_لوستونکی(Files.readAllBytes(يونلور));
            if (لوستونکی_ارزښت.네바이트() != 0xcafebabe) throw new 번역오류("Java پاړکى_ارزښت 표식이 아님");
            لوستونکی_ارزښت.لوستل(4);
            int 개수 = لوستونکی_ارزښت.두바이트(); 상수종류 = new int[개수]; درېدلى_اومتوک = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = لوستونکی_ارزښت.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int اوږدوالى_ارزښت = لوستونکی_ارزښت.두바이트();
                        byte[] لوښه_لنډیاد = لوستونکی_ارزښت.لوستل(اوږدوالى_ارزښت), 길이붙인자료 = new byte[اوږدوالى_ارزښت + 2];
                        길이붙인자료[0] = (byte)(اوږدوالى_ارزښت >> 8); 길이붙인자료[1] = (byte)اوږدوالى_ارزښت;
                        System.arraycopy(لوښه_لنډیاد, 0, 길이붙인자료, 2, اوږدوالى_ارزښت);
                        درېدلى_اومتوک[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: درېدلى_اومتوک[순번] = لوستونکی_ارزښت.네바이트(); break;
                    case 4: لوستونکی_ارزښت.لوستل(4); break;
                    case 5: case 6: لوستونکی_ارزښت.لوستل(8); 순번++; break;
                    case 7: case 8: case 16: درېدلى_اومتوک[순번] = لوستونکی_ارزښت.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        درېدلى_اومتوک[순번] = new int[]{لوستونکی_ارزښت.두바이트(), لوستونکی_ارزښت.두바이트()}; break;
                    case 15: درېدلى_اومتوک[순번] = new int[]{لوستونکی_ارزښت.한바이트(), لوستونکی_ارزښت.두바이트()}; break;
                    default: throw new 번역오류("지원하지 않는 درېدلى_ارزښت 종류: " + 종류);
                }
            }
            لوستونکی_ارزښت.두바이트(); نوم = 클래스명(لوستونکی_ارزښت.두바이트());
            if (!클래스명(لوستونکی_ارزښت.두바이트()).equals("java/lang/Object") || لوستونکی_ارزښت.두바이트() != 0)
                throw new 번역오류(نوم + ": 상속 및 인터페이스 미지원");
            ډګر_ارزښت = 멤버읽기(لوستونکی_ارزښت); 함수 = 멤버읽기(لوستونکی_ارزښت); 속성읽기(لوستونکی_ارزښت);
            if (لوستونکی_ارزښت.ځای != لوستونکی_ارزښت.اومتوک.length) throw new 번역오류("پاړکى_ارزښت 뒤에 남은 اومتوک");
        }
        String 문자(int لړیال) {
            if (لړیال < 1 || لړیال >= 상수종류.length || 상수종류[لړیال] != 1) throw new 번역오류("문자 درېدلى_ارزښت لړیال تېروتنه");
            return (String) درېدلى_اومتوک[لړیال];
        }
        String 클래스명(int لړیال) {
            if (لړیال < 1 || لړیال >= 상수종류.length || 상수종류[لړیال] != 7) throw new 번역오류("پاړکى_ارزښت 참조 تېروتنه");
            return 문자((Integer)درېدلى_اومتوک[لړیال]);
        }
        함수참조 참조(int لړیال) {
            if (لړیال < 1 || لړیال >= 상수종류.length || 상수종류[لړیال] < 9 || 상수종류[لړیال] > 11) throw new 번역오류("멤버 참조 تېروتنه");
            int[] 쌍 = (int[])درېدلى_اومتوک[لړیال], 이름쌍 = (int[])درېدلى_اومتوک[쌍[1]];
            return new 함수참조(클래스명(쌍[0]), 문자(이름쌍[0]), 문자(이름쌍[1]));
        }
        Map<String, byte[]> 속성읽기(اومتوک_لوستونکی لوستونکی_ارزښت) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = لوستونکی_ارزښت.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String 속성이름 = 문자(لوستونکی_ارزښت.두바이트()); byte[] ارزښت = لوستونکی_ارزښت.لوستل(لوستونکی_ارزښت.네바이트());
                if (결과.put(속성이름, ارزښت) != null) throw new 번역오류("겹친 ځانتیا_ارزښت: " + 속성이름);
            }
            return 결과;
        }
        List<شمېره_اومتوک> 멤버읽기(اومتوک_لوستونکی لوستونکی_ارزښت) {
            List<شمېره_اومتوک> 결과 = new ArrayList<>(); int 개수 = لوستونکی_ارزښت.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int رسى_ننوت = لوستونکی_ارزښت.두바이트(); String 함수이름 = 문자(لوستونکی_ارزښت.두바이트()), 서술 = 문자(لوستونکی_ارزښت.두바이트());
                결과.add(new شمېره_اومتوک(رسى_ننوت, 함수이름, 서술, 속성읽기(لوستونکی_ارزښت)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new 번역오류("함수 서술 تېروتنه: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new 번역오류("함수 서술 تېروتنه: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new 번역오류("함수 서술 تېروتنه: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int ځای = 0; ځای < 서술.length();) {
            String 선택 = null;
            for (String بڼه_ارزښت : 허용형식) if (서술.startsWith(بڼه_ارزښت, ځای)) { 선택 = بڼه_ارزښت; break; }
            if (선택 == null) throw new 번역오류("지원하지 않는 اومتوک_ډول: " + 서술);
            결과.add(선택); ځای += 선택.length();
        }
        return 결과;
    }
    static String 기호(String 종류, String... 부분들) {
        try {
            byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder ليکنه = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) ليکنه.append(String.format(Locale.ROOT, "%02x", 해시[순번] & 255));
            return ليکنه.toString();
        } catch (Exception تېروتنه) { throw new 번역오류(تېروتنه.toString()); }
    }
    final Map<String, پاړکى_اومتوک> 클래스들 = new TreeMap<>();
    final Map<함수참조, شمېره_اومتوک> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, 기계클래스;
    final int 동적기억낱말수;
    final Path سرچينه_يونلور;
    기계어미리번역(List<Path> 경로들, String 대상, int 낱말수, Path سرچينه_ارزښت) throws IOException {
        if ((!대상.equals("kernel") && !대상.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new 번역오류("실행 대상 또는 기억 공간 کچ تېروتنه");
        실행대상 = 대상; 동적기억낱말수 = 낱말수; سرچينه_يونلور = سرچينه_ارزښت;
        // 이 이름도 국가별 سرچینه_ونه 생성 시 해당 언어로 옮긴다.
        기계클래스 = 대상.equals("kernel") ? "보드" : "کارن";
        for (String ليکه : Files.readAllLines(سرچينه_ارزښت.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = ليکه.split("\t", -1);
            if (부분들.length != 4) throw new 번역오류("기계 함수 اومتوک تېروتنه");
            if (부분들[0].equals(대상)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path يونلور : 경로들) {
            پاړکى_اومتوک اومتوک = new پاړکى_اومتوک(يونلور);
            if (클래스들.put(اومتوک.نوم, اومتوک) != null) throw new 번역오류("중복 پاړکى_ارزښت: " + اومتوک.نوم);
            for (شمېره_اومتوک ډګر_ارزښت : اومتوک.ډګر_ارزښت) {
                if ((ډګر_ارزښت.رسى_ننوت & 8) == 0 || 형식읽기(ډګر_ارزښت.서술).equals(Collections.singletonList("V"))) throw new 번역오류("ولاړ_ارزښت 필드만 ملاتړ_ارزښت");
                if (필드들.put(new 함수참조(اومتوک.نوم, ډګر_ارزښت.نوم, ډګر_ارزښت.서술), ډګر_ارزښت) != null) throw new 번역오류("중복 ډګر_ارزښت");
            }
            for (شمېره_اومتوک 함수 : اومتوک.함수) {
                if (함수.نوم.equals("<init>")) continue;
                if ((함수.رسى_ننوت & 8) == 0 || (함수.رسى_ننوت & (0x20 | 0x400)) != 0) throw new 번역오류("ولاړ_ارزښت 비동기화 함수만 ملاتړ_ارزښت");
                new 함수형식(함수.서술);
                if (함수들.put(new 함수참조(اومتوک.نوم, 함수.نوم, 함수.서술), 함수) != null) throw new 번역오류("중복 함수");
            }
        }
    }
    String 문자열기호(String ليکنه) { return 문자열들.computeIfAbsent(ليکنه, ارزښت -> "j_text_" + 문자열들.size()); }
    String درېدلى_څرګندنه(پاړکى_اومتوک اومتوک, int لړیال) {
        if (لړیال < 1 || لړیال >= اومتوک.상수종류.length) throw new 번역오류("درېدلى_ارزښت لړیال ټوټه تېروتنه");
        if (اومتوک.상수종류[لړیال] == 3) return "(word)(uint32_t)(" + اومتوک.درېدلى_اومتوک[لړیال] + ")";
        if (اومتوک.상수종류[لړیال] == 8) return "(word)" + 문자열기호(اومتوک.문자((Integer)اومتوک.درېدلى_اومتوک[لړیال]));
        throw new 번역오류("정수와 مزى_ارزښت_6ca8363c 상수만 ملاتړ_ارزښت");
    }
    String 함수원형(함수참조 참조) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(참조.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + 기호("method", 참조.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void 지역검사(int لړیال, int 지역변수수) { if (لړیال < 0 || لړیال >= 지역변수수) throw new 번역오류("지역 변수 لړیال ټوټه تېروتنه"); }
    void 분기넣기(List<String> 출력, Set<Integer> 분기들, int ځای, int 이동량, String آړ) {
        int موخه_ارزښت = ځای + 이동량; 분기들.add(موخه_ارزښت);
        출력.add((آړ == null ? "" : "if (" + آړ + ") ") + "goto b" + موخه_ارزښت + ";");
    }
    String 함수본문(함수참조 함수, شمېره_اومتوک اومتوک) {
        byte[] 본문자료 = اومتوک.ځانتیا_ارزښت.get("Code"); if (본문자료 == null) throw new 번역오류("함수 몸체가 없음: " + 함수.نوم);
        اومتوک_لوستونکی لوستونکی_ارزښت = new اومتوک_لوستونکی(본문자료); int 쌓임깊이 = لوستونکی_ارزښت.두바이트(), 지역변수수 = لوستونکی_ارزښت.두바이트();
        اومتوک_لوستونکی بولۍ_اومتوک = new اومتوک_لوستونکی(لوستونکی_ارزښت.لوستل(لوستونکی_ارزښت.네바이트()));
        if (لوستونکی_ارزښت.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 بڼه_ارزښت = new 함수형식(함수.서술); if (지역변수수 < بڼه_ارزښت.인수.size()) throw new 번역오류("매개변수보다 적은 지역 변수");
        پاړکى_اومتوک پاړکى_ارزښت = 클래스들.get(함수.소유);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(함수) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < بڼه_ارزښت.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (بولۍ_اومتوک.ځای < بولۍ_اومتوک.اومتوک.length) {
            int ځای = بولۍ_اومتوک.ځای, بولۍ = بولۍ_اومتوک.한바이트(); 경계들.add(ځای); 출력.add("b" + ځای + ":;");
            if (بولۍ == 0) continue;
            if (بولۍ == 1) 출력.add("PUSH(0);");
            else if (بولۍ >= 2 && بولۍ <= 8) 출력.add("PUSH((uint32_t)(" + (بولۍ - 3) + "));");
            else if (بولۍ == 16 || بولۍ == 17) 출력.add("PUSH((uint32_t)(" + (بولۍ == 16 ? بولۍ_اومتوک.부호한바이트() : بولۍ_اومتوک.부호두바이트()) + "));");
            else if (بولۍ == 18 || بولۍ == 19) 출력.add("PUSH(" + درېدلى_څرګندنه(پاړکى_ارزښت, بولۍ == 18 ? بولۍ_اومتوک.한바이트() : بولۍ_اومتوک.두바이트()) + ");");
            else if (بولۍ == 21 || بولۍ == 25 || (بولۍ >= 26 && بولۍ <= 29) || (بولۍ >= 42 && بولۍ <= 45)) {
                int لړیال = بولۍ == 21 || بولۍ == 25 ? بولۍ_اومتوک.한바이트() : بولۍ - (بولۍ <= 29 ? 26 : 42);
                지역검사(لړیال, 지역변수수); 출력.add("PUSH(l[" + لړیال + "]);");
            } else if (بولۍ == 54 || بولۍ == 58 || (بولۍ >= 59 && بولۍ <= 62) || (بولۍ >= 75 && بولۍ <= 78)) {
                int لړیال = بولۍ == 54 || بولۍ == 58 ? بولۍ_اومتوک.한바이트() : بولۍ - (بولۍ <= 62 ? 59 : 75);
                지역검사(لړیال, 지역변수수); 출력.add("l[" + لړیال + "] = POP();");
            } else if (بولۍ == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (بولۍ == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (بولۍ == 87 || بولۍ == 88) 출력.add(بولۍ == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (بولۍ >= 89 && بولۍ <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] 순서들 = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[بولۍ - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char ارزښت : 순서들[بولۍ - 89].toCharArray()) 출력.add("PUSH(" + ارزښت + ");");
            } else if (بولۍ == 96 || بولۍ == 100 || بولۍ == 104 || بولۍ == 126 || بولۍ == 128 || بولۍ == 130) {
                String چلښت_ارزښت = بولۍ == 96 ? "+" : بولۍ == 100 ? "-" : بولۍ == 104 ? "*" : بولۍ == 126 ? "&" : بولۍ == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + چلښت_ارزښت + " (uint32_t)b);");
            } else if (بولۍ == 108 || بولۍ == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (بولۍ == 112 ? 1 : 0) + "));");
            else if (بولۍ == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (بولۍ == 120 || بولۍ == 122 || بولۍ == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (بولۍ == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (بولۍ == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (بولۍ == 132) {
                int لړیال = بولۍ_اومتوک.한바이트(), 증가량 = بولۍ_اومتوک.부호한바이트(); 지역검사(لړیال, 지역변수수);
                출력.add("l[" + لړیال + "] = (uint32_t)l[" + لړیال + "] + (uint32_t)(" + 증가량 + ");");
            } else if (بولۍ >= 145 && بولۍ <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (بولۍ == 145 ? "int8_t" : بولۍ == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (بولۍ >= 153 && بولۍ <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, 분기들, ځای, بولۍ_اومتوک.부호두바이트(), "(int32_t)a " + 비교들[بولۍ - 153] + " 0");
            } else if (بولۍ >= 159 && بولۍ <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, 분기들, ځای, بولۍ_اومتوک.부호두바이트(), بولۍ >= 165 ? "a " + 비교들[بولۍ - 159] + " b" : "(int32_t)a " + 비교들[بولۍ - 159] + " (int32_t)b");
            } else if (بولۍ == 167 || بولۍ == 200) 분기넣기(출력, 분기들, ځای, بولۍ == 167 ? بولۍ_اومتوک.부호두바이트() : بولۍ_اومتوک.네바이트(), null);
            else if (بولۍ == 170 || بولۍ == 171) {
                while (بولۍ_اومتوک.ځای % 4 != 0) بولۍ_اومتوک.한바이트();
                int تلواله_ارزښت = بولۍ_اومتوک.네바이트(); 출력.add("a = POP();");
                if (بولۍ == 170) {
                    int 아래 = بولۍ_اومتوک.네바이트(), 위 = بولۍ_اومتوک.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (بولۍ_اومتوک.اومتوک.length - بولۍ_اومتوک.ځای) / 4) throw new 번역오류("switch ټوټه تېروتنه");
                    for (long ارزښت = 아래; ارزښت <= 위; ارزښت++) 분기넣기(출력, 분기들, ځای, بولۍ_اومتوک.네바이트(), "(int32_t)a == (" + ارزښت + ")");
                } else {
                    int 개수 = بولۍ_اومتوک.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (بولۍ_اومتوک.اومتوک.length - بولۍ_اومتوک.ځای) / 8) throw new 번역오류("switch کچ تېروتنه");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int ارزښت = بولۍ_اومتوک.네바이트(); if (순번 > 0 && ارزښت <= 앞값) throw new 번역오류("switch اڼن_اوډون_ارزښت تېروتنه"); 앞값 = ارزښت;
                        분기넣기(출력, 분기들, ځای, بولۍ_اومتوک.네바이트(), "(int32_t)a == (" + ارزښت + ")");
                    }
                }
                분기넣기(출력, 분기들, ځای, تلواله_ارزښت, null);
            } else if (بولۍ == 172 || بولۍ == 176 || بولۍ == 177) 출력.add("return " + (بولۍ == 177 ? "0" : "POP()") + ";");
            else if (بولۍ == 178 || بولۍ == 179) {
                함수참조 참조 = پاړکى_ارزښت.참조(بولۍ_اومتوک.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 ډګر_ارزښت");
                출력.add(기호("init", 참조.소유) + "();"); String ډګر_ارزښت = 기호("field", 참조.부분들());
                출력.add(بولۍ == 178 ? "PUSH(" + ډګر_ارزښت + ");" : ډګر_ارزښت + " = POP();");
            } else if (بولۍ == 184) {
                함수참조 참조 = پاړکى_ارزښت.참조(بولۍ_اومتوک.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 함수");
                함수형식 호출형식 = new 함수형식(참조.서술); int 개수 = 호출형식.인수.size();
                출력.add(기호("init", 참조.소유) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + 기호("method", 참조.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (بولۍ == 182) {
                함수참조 참조 = پاړکى_ارزښت.참조(بولۍ_اومتوک.두바이트());
                if (참조.equals(new 함수참조("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (참조.equals(new 함수참조("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 번역오류("가상 함수 호출 미지원");
            } else if (بولۍ == 188) {
                if (بولۍ_اومتوک.한바이트() != 10) throw new 번역오류("new int[]만 ملاتړ_ارزښت"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (بولۍ == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (بولۍ == 196) {
                int شاتاړى_ارزښت = بولۍ_اومتوک.한바이트(), لړیال = بولۍ_اومتوک.두바이트(); 지역검사(لړیال, 지역변수수);
                if (شاتاړى_ارزښت == 21 || شاتاړى_ارزښت == 25) 출력.add("PUSH(l[" + لړیال + "]);");
                else if (شاتاړى_ارزښت == 54 || شاتاړى_ارزښت == 58) 출력.add("l[" + لړیال + "] = POP();");
                else if (شاتاړى_ارزښت == 132) 출력.add("l[" + لړیال + "] = (uint32_t)l[" + لړیال + "] + (uint32_t)(" + بولۍ_اومتوک.부호두바이트() + ");");
                else throw new 번역오류("미지원 wide بولۍ");
            } else if (بولۍ == 198 || بولۍ == 199) {
                출력.add("a = POP();"); 분기넣기(출력, 분기들, ځای, بولۍ_اومتوک.부호두바이트(), "a " + (بولۍ == 198 ? "==" : "!=") + " 0");
            } else throw new 번역오류(함수.소유 + "." + 함수.نوم + ", بايټ_ارزښت " + ځای + ": 미지원 بولۍ " + بولۍ);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("بولۍ 경계가 아닌 곳으로 분기");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String 내보낼함수(String 연결기호, String 대상, boolean 진입점여부) {
        int 자리 = 대상.lastIndexOf('.'); if (자리 < 0 || !연결기호.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 지정 تېروتنه");
        String 소유 = 대상.substring(0, 자리).replace('.', '/'), نوم = 대상.substring(자리 + 1); 함수참조 선택 = null;
        for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(소유) && 참조.نوم.equals(نوم)) {
            if (선택 != null) throw new 번역오류("겹친 내보내기 대상"); 선택 = 참조;
        }
        if (선택 == null || (함수들.get(선택).رسى_ننوت & 0x100) != 0) throw new 번역오류("내보낼 함수가 없음 또는 native 함수");
        함수형식 بڼه_ارزښت = new 함수형식(선택.서술);
        if ((진입점여부 && !بڼه_ارزښت.인수.isEmpty()) || !Arrays.asList("V", "I").contains(بڼه_ارزښت.반환)) throw new 번역오류("ننوت_ټکى_ارزښت 또는 C 경계 بڼه_ارزښت تېروتنه");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < بڼه_ارزښت.인수.size(); 순번++) {
            if (!بڼه_ارزښت.인수.get(순번).equals("I")) throw new 번역오류("C 경계는 int 인수만 ملاتړ_ارزښت");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (بڼه_ارزښت.반환.equals("V") ? "void " : "int32_t ") + 연결기호 + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + 기호("init", 선택.소유) + "(); " + (بڼه_ارزښت.반환.equals("V") ? "" : "return (int32_t)") + 기호("method", 선택.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String ننوت_ټکى, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<함수참조, شمېره_اومتوک> ننوت_ارزښت : 함수들.entrySet()) {
            함수참조 참조 = ننوت_ارزښت.getKey(); شمېره_اومتوک اومتوک = ننوت_ارزښت.getValue(); 선언들.add(함수원형(참조) + ";");
            if ((اومتوک.رسى_ننوت & 0x100) != 0) {
                String نښلېدل = 기계함수들.get(참조.نوم + 참조.서술);
                if (!참조.소유.equals(기계클래스) || نښلېدل == null) throw new 번역오류("허용되지 않은 native 함수: " + 참조.نوم);
                int 개수 = new 함수형식(참조.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + نښلېدل + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(참조) + " { return " + نښلېدل + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(참조, اومتوک));
        }
        for (Map.Entry<함수참조, شمېره_اومتوک> ننوت_ارزښت : 필드들.entrySet()) {
            함수참조 참조 = ننوت_ارزښت.getKey(); byte[] درېدلى_ارزښت = ننوت_ارزښت.getValue().ځانتیا_ارزښت.get("ConstantValue");
            String ارزښت = درېدلى_ارزښت == null ? "0" : درېدلى_څرګندنه(클래스들.get(참조.소유), new اومتوک_لوستونکی(درېدلى_ارزښت).두바이트());
            필드선언들.add("static word " + 기호("field", 참조.부분들()) + " = " + ارزښت + ";");
        }
        for (String نوم : 클래스들.keySet()) {
            String تيارى = 기호("init", نوم), انکړ_ارزښت = 기호("state", نوم);
            선언들.add("static void " + تيارى + "(void);"); 필드선언들.add("static unsigned " + انکړ_ارزښت + ";");
            함수참조 참조 = new 함수참조(نوم, "<clinit>", "()V");
            몸체들.add("static void " + تيارى + "(void) { if(" + انکړ_ارزښت + ") return; " + انکړ_ارزښت + " = 1; " + (함수들.containsKey(참조) ? 기호("method", 참조.부분들()) + "(); " : "") + انکړ_ارزښت + " = 2; }");
        }
        몸체들.add(내보낼함수("java_entry", ننوت_ټکى, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new 번역오류("내보내기 지정 تېروتنه");
            String نوم = 지정.substring(0, 자리); 공개이름.add(نوم); 몸체들.add(내보낼함수(نوم, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> ننوت_ارزښت : 문자열들.entrySet()) {
            String ليکنه = ننوت_ارزښت.getKey(); StringBuilder لړوند_ارزښت = new StringBuilder("static const word " + ننوت_ارزښت.getValue() + "[] = {" + ليکنه.length());
            for (int 순번 = 0; 순번 < ليکنه.length(); 순번++) لړوند_ارزښت.append(", ").append((int)ليکنه.charAt(순번));
            문자열선언들.add(لړوند_ارزښت.append("};").toString());
        }
        String ملاتړ_ارزښت = Files.readString(سرچينه_يونلور.resolve("실행지원.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(ملاتړ_ارزښت + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String سرچينه, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> 이름표 = new HashMap<>();
        for (String ليکه : Files.readAllLines(سرچينه_يونلور.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] 쌍 = ليکه.split("\t"); 이름표.put(쌍[0], 쌍[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(سرچينه); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String نوم = 찾개.group(), 새이름 = نوم;
            if (!نوم.startsWith("//") && !نوم.startsWith("/*") && !نوم.startsWith("\"") && !نوم.startsWith("'") && !공개이름.contains(نوم)) {
                새이름 = 이름표.getOrDefault(نوم, نوم);
                if (نوم.matches("a[0-9]+")) 새이름 = "인수" + نوم.substring(1);
                if (نوم.matches("b[0-9]+")) 새이름 = "분기" + نوم.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char لوښه_ارزښت : 새이름.toCharArray()) 표기.append(لوښه_ارزښت < 128 ? Character.toString(لوښه_ارزښت) : String.format(Locale.ROOT, "\\u%04x", (int)لوښه_ارزښت));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(함수참조 함수, شمېره_اومتوک اومتوک, Map<String,String> 기계표, String 대상) {
        String 표식 = 기호("method", 함수.부분들());
        List<String> ليکه = new ArrayList<>();
        if ((اومتوک.رسى_ننوت & 0x100) != 0) {
            String نښلېدل = 기계표.get(함수.نوم + 함수.서술);
            if (!함수.소유.equals(대상.equals("kernel") ? "وزله_ارزښت" : "کارن") || نښلېدل == null) throw new 번역오류("허용되지 않은 native 함수");
            return ".text\n" + 표식 + ":\njmp " + نښلېدل;
        }
        byte[] تنه_متن = اومتوک.ځانتیا_ارزښت.get("Code"); if (تنه_متن == null) throw new 번역오류("함수 몸체가 없음");
        اومتوک_لوستونکی لوستونکی_ارزښت = new اومتوک_لوستونکی(تنه_متن); لوستونکی_ارزښت.두바이트(); int 지역수 = لوستونکی_ارزښت.두바이트();
        اومتوک_لوستونکی بولۍ_اومتوک = new اومتوک_لوستونکی(لوستونکی_ارزښت.لوستل(لوستونکی_ارزښت.네바이트()));
        if (لوستونکی_ارزښت.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 بڼه_ارزښت = new 함수형식(함수.서술); if (지역수 < بڼه_ارزښت.인수.size()) throw new 번역오류("매개변수보다 적은 지역 변수");
        Collections.addAll(ليکه,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < بڼه_ارزښت.인수.size(); 순번++) Collections.addAll(ليکه,"movl " + (8 + 4 * (بڼه_ارزښت.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        پاړکى_اومتوک پاړکى_ارزښت = 클래스들.get(함수.소유); Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (بولۍ_اومتوک.ځای < بولۍ_اومتوک.اومتوک.length) {
            int ځای = بولۍ_اومتوک.ځای, بولۍ = بولۍ_اومتوک.한바이트(); String 자리 = 표식 + "_b" + ځای;
            ليکه.add(자리 + ":"); 경계들.add(ځای);
            if (بولۍ == 0) ليکه.add("nop");
            else if (بولۍ == 1) ليکه.add("pushl $0");
            else if (بولۍ >= 2 && بولۍ <= 8) ليکه.add("pushl $" + (بولۍ - 3));
            else if (بولۍ == 16 || بولۍ == 17) ليکه.add("pushl $" + (بولۍ == 16 ? بولۍ_اومتوک.부호한바이트() : بولۍ_اومتوک.부호두바이트()));
            else if (بولۍ == 18 || بولۍ == 19) {
                int لړیال = بولۍ == 18 ? بولۍ_اومتوک.한바이트() : بولۍ_اومتوک.두바이트();
                ليکه.add("pushl $" + 엑스상수(پاړکى_ارزښت,لړیال));
            } else if (بولۍ == 21 || بولۍ == 25 || (بولۍ >= 26 && بولۍ <= 29) || (بولۍ >= 42 && بولۍ <= 45) || بولۍ == 54 || بولۍ == 58 || (بولۍ >= 59 && بولۍ <= 62) || (بولۍ >= 75 && بولۍ <= 78)) {
                boolean 읽음 = بولۍ < 54; int لړیال = بولۍ == 21 || بولۍ == 25 || بولۍ == 54 || بولۍ == 58 ? بولۍ_اومتوک.한바이트() : بولۍ - (بولۍ <= 29 ? 26 : بولۍ <= 45 ? 42 : بولۍ <= 62 ? 59 : 75);
                지역검사(لړیال,지역수); ليکه.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (لړیال + 1)) + "(%ebp)");
            } else if (بولۍ == 46) Collections.addAll(ليکه,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (بولۍ == 79) Collections.addAll(ليکه,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (بولۍ == 87 || بولۍ == 88) ليکه.add("addl $" + (بولۍ == 87 ? 4 : 8) + ", %esp");
            else if (بولۍ >= 89 && بولۍ <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] 순서들 = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[بولۍ - 89]; 순번++) ليکه.add("popl " + 저장기들[순번]);
                for (int 순번 : 순서들[بولۍ - 89]) ليکه.add("pushl " + 저장기들[순번]);
            } else if (بولۍ == 96 || بولۍ == 100 || بولۍ == 104 || بولۍ == 126 || بولۍ == 128 || بولۍ == 130) {
                String چلښت_ارزښت = بولۍ == 96 ? "addl" : بولۍ == 100 ? "subl" : بولۍ == 104 ? "imull" : بولۍ == 126 ? "andl" : بولۍ == 128 ? "orl" : "xorl";
                Collections.addAll(ليکه,"popl %ecx","popl %eax",چلښت_ارزښت + " %ecx, %eax","pushl %eax");
            } else if (بولۍ == 108 || بولۍ == 112) Collections.addAll(ليکه,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (بولۍ == 108 ? "%eax" : "%edx"));
            else if (بولۍ == 116) ليکه.add("negl (%esp)");
            else if (بولۍ == 120 || بولۍ == 122 || بولۍ == 124) Collections.addAll(ليکه,"popl %ecx","popl %eax",(بولۍ == 120 ? "sall" : بولۍ == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (بولۍ == 132) {
                int لړیال = بولۍ_اومتوک.한바이트(), 증가 = بولۍ_اومتوک.부호한바이트(); 지역검사(لړیال,지역수); ليکه.add("addl $" + 증가 + ", -" + (4 * (لړیال + 1)) + "(%ebp)");
            } else if (بولۍ >= 145 && بولۍ <= 147) Collections.addAll(ليکه,"popl %eax",بولۍ == 145 ? "movsbl %al, %eax" : بولۍ == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (بولۍ >= 153 && بولۍ <= 166) {
                if (بولۍ <= 158) Collections.addAll(ليکه,"popl %eax","testl %eax, %eax");
                else Collections.addAll(ليکه,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int موخه_ارزښت = ځای + بولۍ_اومتوک.부호두바이트(); 분기들.add(موخه_ارزښت); ليکه.add(비교들[بولۍ - (بولۍ <= 158 ? 153 : 159)] + " " + 표식 + "_b" + موخه_ارزښت);
            } else if (بولۍ == 167 || بولۍ == 200) {
                int موخه_ارزښت = ځای + (بولۍ == 167 ? بولۍ_اومتوک.부호두바이트() : بولۍ_اومتوک.네바이트()); 분기들.add(موخه_ارزښت); ليکه.add("jmp " + 표식 + "_b" + موخه_ارزښت);
            } else if (بولۍ == 170 || بولۍ == 171) {
                while (بولۍ_اومتوک.ځای % 4 != 0) بولۍ_اومتوک.한바이트();
                int تلواله_ارزښت = ځای + بولۍ_اومتوک.네바이트(); 분기들.add(تلواله_ارزښت); ليکه.add("popl %eax");
                int 개수, 아래 = 0;
                if (بولۍ == 170) { 아래 = بولۍ_اومتوک.네바이트(); int 위 = بولۍ_اومتوک.네바이트(); long اوږدوالى_ارزښت = (long)위 - 아래 + 1; if (اوږدوالى_ارزښت < 1 || اوږدوالى_ارزښت > (بولۍ_اومتوک.اومتوک.length - بولۍ_اومتوک.ځای) / 4) throw new 번역오류("switch ټوټه تېروتنه"); 개수 = (int)اوږدوالى_ارزښت; }
                else { 개수 = بولۍ_اومتوک.네바이트(); if (개수 < 0 || 개수 > (بولۍ_اومتوک.اومتوک.length - بولۍ_اومتوک.ځای) / 8) throw new 번역오류("switch کچ تېروتنه"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int ارزښت = بولۍ == 170 ? 아래 + 순번 : بولۍ_اومتوک.네바이트(), موخه_ارزښت = ځای + بولۍ_اومتوک.네바이트(); 분기들.add(موخه_ارزښت);
                    Collections.addAll(ليکه,"cmpl $" + ارزښت + ", %eax","je " + 표식 + "_b" + موخه_ارزښت);
                }
                ليکه.add("jmp " + 표식 + "_b" + تلواله_ارزښت);
            } else if (بولۍ == 172 || بولۍ == 176 || بولۍ == 177) {
                if (بولۍ != 177) ليکه.add("popl %eax"); Collections.addAll(ليکه,"leave","ret");
            } else if (بولۍ == 178 || بولۍ == 179) {
                함수참조 참조 = پاړکى_ارزښت.참조(بولۍ_اومتوک.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 ډګر_ارزښت");
                Collections.addAll(ليکه,"call " + 기호("init",참조.소유),(بولۍ == 178 ? "pushl " : "popl ") + 기호("field",참조.부분들()));
            } else if (بولۍ == 184) {
                함수참조 참조 = پاړکى_ارزښت.참조(بولۍ_اومتوک.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 함수");
                함수형식 호출형식 = new 함수형식(참조.서술); Collections.addAll(ليکه,"call " + 기호("init",참조.소유),"call " + 기호("method",참조.부분들()));
                if (!호출형식.인수.isEmpty()) ليکه.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) ليکه.add("pushl %eax");
            } else if (بولۍ == 182) {
                함수참조 참조 = پاړکى_ارزښت.참조(بولۍ_اومتوک.두바이트());
                if (참조.equals(new 함수참조("java/lang/String","length","()I"))) Collections.addAll(ليکه,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (참조.equals(new 함수참조("java/lang/String","charAt","(I)C"))) Collections.addAll(ليکه,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 번역오류("가상 함수 호출 미지원");
            } else if (بولۍ == 188) {
                if (بولۍ_اومتوک.한바이트() != 10) throw new 번역오류("new int[]만 ملاتړ_ارزښت"); Collections.addAll(ليکه,"popl %eax","call rt_new_array","pushl %eax");
            } else if (بولۍ == 190) Collections.addAll(ليکه,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (بولۍ == 196) {
                int شاتاړى_ارزښت = بولۍ_اومتوک.한바이트(), لړیال = بولۍ_اومتوک.두바이트(); 지역검사(لړیال,지역수);
                if (شاتاړى_ارزښت == 21 || شاتاړى_ارزښت == 25 || شاتاړى_ارزښت == 54 || شاتاړى_ارزښت == 58) ليکه.add((شاتاړى_ارزښت <= 25 ? "pushl " : "popl ") + "-" + 4 * (لړیال + 1) + "(%ebp)");
                else if (شاتاړى_ارزښت == 132) ليکه.add("addl $" + بولۍ_اومتوک.부호두바이트() + ", -" + 4 * (لړیال + 1) + "(%ebp)");
                else throw new 번역오류("wide بولۍ 미지원");
            } else if (بولۍ == 198 || بولۍ == 199) {
                int موخه_ارزښت = ځای + بولۍ_اومتوک.부호두바이트(); 분기들.add(موخه_ارزښت); Collections.addAll(ليکه,"popl %eax","testl %eax, %eax",(بولۍ == 198 ? "je " : "jne ") + 표식 + "_b" + موخه_ارزښت);
            } else throw new 번역오류("미지원 بولۍ: " + بولۍ);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("بولۍ 경계가 아닌 곳으로 분기");
        ليکه.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",ليکه);
    }
    String 엑스상수(پاړکى_اومتوک اومتوک, int لړیال) {
        if (اومتوک.상수종류[لړیال] == 3) return اومتوک.درېدلى_اومتوک[لړیال].toString();
        if (اومتوک.상수종류[لړیال] == 8) return 문자열기호(اومتوک.문자((Integer)اومتوک.درېدلى_اومتوک[لړیال]));
        throw new 번역오류("정수와 مزى_ارزښت_6ca8363c 상수만 ملاتړ_ارزښت");
    }
    String 엑스조립본(String ننوت_ټکى, List<String> 내보냄, String 대상) throws IOException {
        Map<String,String> 기계표 = new HashMap<>();
        for (String ليکه : Files.readAllLines(سرچينه_يونلور.resolve("엑스기계함수.tsv"))) { String[] 쌍 = ليکه.split("\t"); if (쌍[0].equals(대상)) 기계표.put(쌍[1] + 쌍[2],쌍[3]); }
        int 자리 = ننوت_ټکى.lastIndexOf('.'); if (자리 < 0) throw new 번역오류("ننوت_ټکى 지정 تېروتنه");
        String 소유 = ننوت_ټکى.substring(0,자리).replace('.','/'), 함수이름 = ننوت_ټکى.substring(자리 + 1); 함수참조 ننوت_ټکى_ارزښت = null;
        for (String 서술 : Arrays.asList("()I","()V")) { 함수참조 참조 = new 함수참조(소유,함수이름,서술); if (함수들.containsKey(참조)) { if (ننوت_ټکى_ارزښت != null) throw new 번역오류("겹친 ننوت_ټکى"); ننوت_ټکى_ارزښت = 참조; } }
        if (ننوت_ټکى_ارزښت == null || (함수들.get(ننوت_ټکى_ارزښت).رسى_ننوت & 0x100) != 0) throw new 번역오류("ننوت_ټکى_ارزښت 함수 بڼه_ارزښت تېروتنه");
        List<String> ليکه = new ArrayList<>(); ليکه.add(".code32");
        for (پاړکى_اومتوک اومتوک : 클래스들.values()) {
            String انکړ_ارزښت = 기호("state",اومتوک.نوم), تيارى = 기호("init",اومتوک.نوم);
            Collections.addAll(ليکه,".bss",".balign 4",انکړ_ارزښت + ": .long 0",".text",تيارى + ":","cmpl $0, " + انکړ_ارزښت,"jne " + تيارى + "_done","movl $1, " + انکړ_ارزښت);
            함수참조 초기화참조 = new 함수참조(اومتوک.نوم,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) ليکه.add("call " + 기호("method",초기화참조.부분들()));
            Collections.addAll(ليکه,"movl $2, " + انکړ_ارزښت,تيارى + "_done:","ret");
            for (شمېره_اومتوک ډګر_ارزښت : اومتوک.ډګر_ارزښت) {
                byte[] درېدلى_ارزښت = ډګر_ارزښت.ځانتیا_ارزښت.get("ConstantValue"); String ارزښت = درېدلى_ارزښت == null ? "0" : 엑스상수(اومتوک,new اومتوک_لوستونکی(درېدلى_ارزښت).두바이트());
                Collections.addAll(ليکه,".data",".balign 4",기호("field",اومتوک.نوم,ډګر_ارزښت.نوم,ډګر_ارزښت.서술) + ": .long " + ارزښت);
            }
            for (شمېره_اومتوک 함수 : اومتوک.함수) if (!함수.نوم.equals("<init>")) ليکه.add(엑스함수본문(new 함수참조(اومتوک.نوم,함수.نوم,함수.서술),함수,기계표,대상));
        }
        Collections.addAll(ليکه,".text",".globl java_entry","java_entry:","call " + 기호("init",ننوت_ټکى_ارزښت.소유),"call " + 기호("method",ننوت_ټکى_ارزښت.부분들()));
        if (ننوت_ټکى_ارزښت.서술.equals("()V")) ليکه.add("xorl %eax, %eax"); ليکه.add("ret");
        for (String 지정 : 내보냄) {
            int راچاپېرل_ارزښت = 지정.indexOf('='); if (راچاپېرل_ارزښت < 1) throw new 번역오류("내보내기 지정 تېروتنه");
            String 외부 = 지정.substring(0,راچاپېرل_ارزښت), 함수 = 지정.substring(راچاپېرل_ارزښت + 1); int 나눔 = 함수.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 기호 تېروتنه");
            String پاړکى_ارزښت = 함수.substring(0,나눔).replace('.','/'), نوم = 함수.substring(나눔 + 1); 함수참조 선택 = null;
            for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(پاړکى_ارزښت) && 참조.نوم.equals(نوم)) { if (선택 != null) throw new 번역오류("겹친 내보내기 대상"); 선택 = 참조; }
            if (선택 == null) throw new 번역오류("내보낼 함수가 없음");
            Collections.addAll(ليکه,".text",".globl " + 외부,외부 + ":","call " + 기호("init",선택.소유),"jmp " + 기호("method",선택.부분들()));
        }
        ليکه.add(".section .rodata");
        for (Map.Entry<String,String> ننوت_ارزښت : 문자열들.entrySet()) {
            Collections.addAll(ليکه,".balign 4",ننوت_ارزښت.getValue() + ":",".long " + ننوت_ارزښت.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char 단위 : ننوت_ارزښت.getKey().toCharArray()) 단위들.add(Integer.toString(단위)); if (!단위들.isEmpty()) ليکه.add(".long " + String.join(",",단위들));
        }
        ليکه.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",ليکه) + "\n";
    }
    static void 도구실행(List<String> بولۍ) throws Exception {
        if (new ProcessBuilder(بولۍ).inheritIO().start().waitFor() != 0) throw new 번역오류("جوړول_سرچینه تېروتنه: " + بولۍ.get(0));
    }
    static String اومتوک_مزى(String ليکنه) { return "\"" + ليکنه.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String 대상, String ننوت_ټکى, List<String> 내보냄, Path 출력, Path سرچينه_ارزښت) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), پاړکى_يونلور = 임시.resolve("classes"); Files.createDirectory(پاړکى_يونلور);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",پاړکى_يونلور.toString(),"-sourcepath",پاړکى_يونلور.toString(),"-d",پاړکى_يونلور.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new 번역오류("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new 번역오류(".java 또는 .class만 ملاتړ_ارزښت");
            }
            if (원문수 > 0) 도구실행(자바명령);
            try (java.util.stream.Stream<Path> 경로들 = Files.walk(پاړکى_يونلور)) { 경로들.filter(يونلور -> يونلور.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,대상.equals("user") ? "user" : "kernel",262144,سرچينه_ارزښت);
            String 조립 = 변환.엑스조립본(ننوت_ټکى,내보냄,대상); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = سرچينه_ارزښت.getParent();
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("실행지원.s").toString()));
            List<String> نښلېدل = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (대상.equals("kernel")) نښلېدل.add("-r");
            else {
                도구실행(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(대상.equals("user") ? "پيل_کارن_کاريال.s" : "리눅스시작.s").toString()));
                Collections.addAll(نښلېدل,"-e","_start",임시.resolve("start.o").toString());
                if (대상.equals("user")) Collections.addAll(نښلېدل,"-T",도구위치.resolve("کارن_پيوند_هډوانه.ld").toString());
            }
            Collections.addAll(نښلېدل,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); 도구실행(نښلېدل);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path خپرېدا_ارزښت = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),خپرېدا_ارزښت,StandardCopyOption.REPLACE_EXISTING); Files.move(خپرېدا_ارزښت,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(خپرېدا_ارزښت); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(대상.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> 기호자료 = new ArrayList<>(), سرچینه_اومتوک = new ArrayList<>();
            for (함수참조 참조 : 변환.함수들.keySet()) 기호자료.add(اومتوک_مزى(기호("method",참조.부분들())) + ":" + اومتوک_مزى(참조.소유 + "." + 참조.نوم + 참조.서술));
            for (Path 입력 : 입력들) {
                byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder ليکنه = new StringBuilder(); for (byte ارزښت : 해시) ليکنه.append(String.format(Locale.ROOT,"%02x",ارزښت & 255));
                سرچینه_اومتوک.add(اومتوک_مزى(입력.toAbsolutePath().toString()) + ":" + اومتوک_مزى(ليکنه.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + اومتوک_مزى(대상) + ",\"entry\":" + اومتوک_مزى(ننوت_ټکى) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",기호자료) + "},\"sources\":{" + String.join(",",سرچینه_اومتوک) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> 경로들 = Files.walk(임시)) { for (Path يونلور : (Iterable<Path>)경로들.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(يونلور); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String ننوت_ټکى = null, 대상 = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> 경로들 = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String ارزښت = 인수[순번];
                switch (ارزښت) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry پاړکى_ارزښت.함수 -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export 기호=پاړکى_ارزښت.함수] 클래스파일 또는 Java원문"); return;
                    case "--entry": ننوت_ټکى = 인수[++순번]; break;
                    case "--profile": 대상 = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (ارزښت.startsWith("-")) throw new 번역오류("알 수 없는 옵션: " + ارزښت); 경로들.add(Paths.get(ارزښت));
                }
            }
            if (ننوت_ټکى == null || 출력경로 == null || 경로들.isEmpty()) throw new 번역오류("--entry, -o, پاړکى_ارزښت 파일이 필요합니다");
            Path سرچينه_ارزښت = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new 번역오류("알 수 없는 실행 대상");
                엑스번역(경로들,엑스대상,ننوت_ټکى,내보냄,출력경로,سرچينه_ارزښت); return;
            }
            String سرچينه = new 기계어미리번역(경로들, 대상, 낱말수, سرچينه_ارزښت).생성(ننوت_ټکى, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, سرچينه, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception تېروتنه) { System.err.println("جوړول_سرچینه تېروتنه: " + تېروتنه.getMessage()); System.exit(1); }
    }
}
