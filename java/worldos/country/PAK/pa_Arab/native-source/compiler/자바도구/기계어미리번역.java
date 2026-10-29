// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java درجہ_قدر 파일에서 독립 ARM64 커널용 C 원문을 만든다. مہمان_b78e430d JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class ترجمہ_نقص extends RuntimeException {
        ترجمہ_نقص(String 설명) { super(설명); }
    }
    static final class کوائف_پڑھن_والا {
        final byte[] کوائف;
        int 위치;
        کوائف_پڑھن_والا(byte[] 입력자료) { کوائف = 입력자료; }
        byte[] 읽기(int لمبائی_قدر) {
            if (لمبائی_قدر < 0 || لمبائی_قدر > کوائف.length - 위치) throw new ترجمہ_نقص("잘린 درجہ_قدر 또는 حکم کوائف");
            byte[] 결과 = Arrays.copyOfRange(کوائف, 위치, 위치 + لمبائی_قدر); 위치 += لمبائی_قدر; return 결과;
        }
        int 한바이트() { if (위치 >= کوائف.length) throw new ترجمہ_نقص("잘린 حکم کوائف"); return کوائف[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class رکن_کوائف {
        final int پہنچ_داخلہ;
        final String ناں, 서술;
        final Map<String, byte[]> وصف_قدر;
        رکن_کوائف(int پہنچ_قدر, String ناں_قدر, String 서술값, Map<String, byte[]> وصف_کوائف) {
            پہنچ_داخلہ = پہنچ_قدر; ناں = ناں_قدر; 서술 = 서술값; وصف_قدر = وصف_کوائف;
        }
    }
    static final class طریقہ_حوالہ implements Comparable<طریقہ_حوالہ> {
        final String مالک_قدر, ناں, 서술;
        طریقہ_حوالہ(String 소유값, String ناں_قدر, String 서술값) { مالک_قدر = 소유값; ناں = ناں_قدر; 서술 = 서술값; }
        String[] 부분들() { return new String[]{مالک_قدر, ناں, 서술}; }
        public int compareTo(طریقہ_حوالہ ہم_سر_قدر) {
            int 비교값 = مالک_قدر.compareTo(ہم_سر_قدر.مالک_قدر);
            if (비교값 == 0) 비교값 = ناں.compareTo(ہم_سر_قدر.ناں);
            return 비교값 == 0 ? 서술.compareTo(ہم_سر_قدر.서술) : 비교값;
        }
        public boolean equals(Object ہم_سر_قدر) { return ہم_سر_قدر instanceof طریقہ_حوالہ && compareTo((طریقہ_حوالہ) ہم_سر_قدر) == 0; }
        public int hashCode() { return Objects.hash(مالک_قدر, ناں, 서술); }
    }
    static final class درجہ_کوائف {
        final int[] 상수종류;
        final Object[] مستقل_کوائف;
        final String ناں;
        final List<رکن_کوائف> قطعہ_قدر, فعل_قدر;
        درجہ_کوائف(Path راہ) throws IOException {
            کوائف_پڑھن_والا پڑھن_والا_قدر = new کوائف_پڑھن_والا(Files.readAllBytes(راہ));
            if (پڑھن_والا_قدر.네바이트() != 0xcafebabe) throw new ترجمہ_نقص("Java درجہ_قدر 표식이 아님");
            پڑھن_والا_قدر.읽기(4);
            int 개수 = پڑھن_والا_قدر.두바이트(); 상수종류 = new int[개수]; مستقل_کوائف = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = پڑھن_والا_قدر.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int لمبائی_قدر = پڑھن_والا_قدر.두바이트();
                        byte[] کریکٹر_بفر = پڑھن_والا_قدر.읽기(لمبائی_قدر), 길이붙인자료 = new byte[لمبائی_قدر + 2];
                        길이붙인자료[0] = (byte)(لمبائی_قدر >> 8); 길이붙인자료[1] = (byte)لمبائی_قدر;
                        System.arraycopy(کریکٹر_بفر, 0, 길이붙인자료, 2, لمبائی_قدر);
                        مستقل_کوائف[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: مستقل_کوائف[순번] = پڑھن_والا_قدر.네바이트(); break;
                    case 4: پڑھن_والا_قدر.읽기(4); break;
                    case 5: case 6: پڑھن_والا_قدر.읽기(8); 순번++; break;
                    case 7: case 8: case 16: مستقل_کوائف[순번] = پڑھن_والا_قدر.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        مستقل_کوائف[순번] = new int[]{پڑھن_والا_قدر.두바이트(), پڑھن_والا_قدر.두바이트()}; break;
                    case 15: مستقل_کوائف[순번] = new int[]{پڑھن_والا_قدر.한바이트(), پڑھن_والا_قدر.두바이트()}; break;
                    default: throw new ترجمہ_نقص("지원하지 않는 مستقل_قدر 종류: " + 종류);
                }
            }
            پڑھن_والا_قدر.두바이트(); ناں = درجہ_ناں(پڑھن_والا_قدر.두바이트());
            if (!درجہ_ناں(پڑھن_والا_قدر.두바이트()).equals("java/lang/Object") || پڑھن_والا_قدر.두바이트() != 0)
                throw new ترجمہ_نقص(ناں + ": 상속 및 인터페이스 미지원");
            قطعہ_قدر = 멤버읽기(پڑھن_والا_قدر); فعل_قدر = 멤버읽기(پڑھن_والا_قدر); 속성읽기(پڑھن_والا_قدر);
            if (پڑھن_والا_قدر.위치 != پڑھن_والا_قدر.کوائف.length) throw new ترجمہ_نقص("درجہ_قدر 뒤에 남은 کوائف");
        }
        String 문자(int اشاریہ) {
            if (اشاریہ < 1 || اشاریہ >= 상수종류.length || 상수종류[اشاریہ] != 1) throw new ترجمہ_نقص("문자 مستقل_قدر اشاریہ نقص");
            return (String) مستقل_کوائف[اشاریہ];
        }
        String درجہ_ناں(int اشاریہ) {
            if (اشاریہ < 1 || اشاریہ >= 상수종류.length || 상수종류[اشاریہ] != 7) throw new ترجمہ_نقص("درجہ_قدر حوالہ نقص");
            return 문자((Integer)مستقل_کوائف[اشاریہ]);
        }
        طریقہ_حوالہ حوالہ(int اشاریہ) {
            if (اشاریہ < 1 || اشاریہ >= 상수종류.length || 상수종류[اشاریہ] < 9 || 상수종류[اشاریہ] > 11) throw new ترجمہ_نقص("멤버 حوالہ نقص");
            int[] جوڑا_قدر = (int[])مستقل_کوائف[اشاریہ], ناں_جوڑا = (int[])مستقل_کوائف[جوڑا_قدر[1]];
            return new طریقہ_حوالہ(درجہ_ناں(جوڑا_قدر[0]), 문자(ناں_جوڑا[0]), 문자(ناں_جوڑا[1]));
        }
        Map<String, byte[]> 속성읽기(کوائف_پڑھن_والا پڑھن_والا_قدر) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = پڑھن_والا_قدر.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String وصف_ناں = 문자(پڑھن_والا_قدر.두바이트()); byte[] قدر = پڑھن_والا_قدر.읽기(پڑھن_والا_قدر.네바이트());
                if (결과.put(وصف_ناں, قدر) != null) throw new ترجمہ_نقص("겹친 وصف_قدر: " + وصف_ناں);
            }
            return 결과;
        }
        List<رکن_کوائف> 멤버읽기(کوائف_پڑھن_والا پڑھن_والا_قدر) {
            List<رکن_کوائف> 결과 = new ArrayList<>(); int 개수 = پڑھن_والا_قدر.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int پہنچ_داخلہ = پڑھن_والا_قدر.두바이트(); String طریقہ_داخلہ_ناں = 문자(پڑھن_والا_قدر.두바이트()), 서술 = 문자(پڑھن_والا_قدر.두바이트());
                결과.add(new رکن_کوائف(پہنچ_داخلہ, طریقہ_داخلہ_ناں, 서술, 속성읽기(پڑھن_والا_قدر)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new ترجمہ_نقص("فعل_قدر 서술 نقص: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new ترجمہ_نقص("فعل_قدر 서술 نقص: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new ترجمہ_نقص("فعل_قدر 서술 نقص: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String انتخاب_قدر = null;
            for (String وضع_قدر : 허용형식) if (서술.startsWith(وضع_قدر, 위치)) { انتخاب_قدر = وضع_قدر; break; }
            if (انتخاب_قدر == null) throw new ترجمہ_نقص("지원하지 않는 ڈیٹا_قسم: " + 서술);
            결과.add(انتخاب_قدر); 위치 += انتخاب_قدر.length();
        }
        return 결과;
    }
    static String علامت(String 종류, String... 부분들) {
        try {
            byte[] ہیش_فائل = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder متن = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) متن.append(String.format(Locale.ROOT, "%02x", ہیش_فائل[순번] & 255));
            return متن.toString();
        } catch (Exception نقص) { throw new ترجمہ_نقص(نقص.toString()); }
    }
    final Map<String, درجہ_کوائف> 클래스들 = new TreeMap<>();
    final Map<طریقہ_حوالہ, رکن_کوائف> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, مشین_درجہ;
    final int 동적기억낱말수;
    final Path ذریعہ_راہ;
    기계어미리번역(List<Path> راہ_فرست, String ہدف, int 낱말수, Path ذریعہ_قدر) throws IOException {
        if ((!ہدف.equals("kernel") && !ہدف.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new ترجمہ_نقص("نفاذ_کرو_حکم ہدف 또는 میموری_قدر 공간 سائز نقص");
        실행대상 = ہدف; 동적기억낱말수 = 낱말수; ذریعہ_راہ = ذریعہ_قدر;
        // 이 이름도 국가별 ماخذ_شجرہ 생성 시 해당 언어로 옮긴다.
        مشین_درجہ = ہدف.equals("kernel") ? "보드" : "صارف";
        for (String لائن : Files.readAllLines(ذریعہ_قدر.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = لائن.split("\t", -1);
            if (부분들.length != 4) throw new ترجمہ_نقص("مشین فعل_قدر کوائف نقص");
            if (부분들[0].equals(ہدف)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path راہ : راہ_فرست) {
            درجہ_کوائف کوائف = new درجہ_کوائف(راہ);
            if (클래스들.put(کوائف.ناں, کوائف) != null) throw new ترجمہ_نقص("중복 درجہ_قدر: " + کوائف.ناں);
            for (رکن_کوائف قطعہ_قدر : کوائف.قطعہ_قدر) {
                if ((قطعہ_قدر.پہنچ_داخلہ & 8) == 0 || 형식읽기(قطعہ_قدر.서술).equals(Collections.singletonList("V"))) throw new ترجمہ_نقص("ساقط_قدر 필드만 مدد_قدر");
                if (필드들.put(new طریقہ_حوالہ(کوائف.ناں, قطعہ_قدر.ناں, قطعہ_قدر.서술), قطعہ_قدر) != null) throw new ترجمہ_نقص("중복 قطعہ_قدر");
            }
            for (رکن_کوائف فعل_قدر : کوائف.فعل_قدر) {
                if (فعل_قدر.ناں.equals("<init>")) continue;
                if ((فعل_قدر.پہنچ_داخلہ & 8) == 0 || (فعل_قدر.پہنچ_داخلہ & (0x20 | 0x400)) != 0) throw new ترجمہ_نقص("ساقط_قدر 비동기화 함수만 مدد_قدر");
                new 함수형식(فعل_قدر.서술);
                if (함수들.put(new طریقہ_حوالہ(کوائف.ناں, فعل_قدر.ناں, فعل_قدر.서술), فعل_قدر) != null) throw new ترجمہ_نقص("중복 فعل_قدر");
            }
        }
    }
    String سٹرنگ_علامت(String متن) { return 문자열들.computeIfAbsent(متن, قدر -> "j_text_" + 문자열들.size()); }
    String مستقل_تاثر(درجہ_کوائف کوائف, int اشاریہ) {
        if (اشاریہ < 1 || اشاریہ >= کوائف.상수종류.length) throw new ترجمہ_نقص("مستقل_قدر اشاریہ تراشہ نقص");
        if (کوائف.상수종류[اشاریہ] == 3) return "(word)(uint32_t)(" + کوائف.مستقل_کوائف[اشاریہ] + ")";
        if (کوائف.상수종류[اشاریہ] == 8) return "(word)" + سٹرنگ_علامت(کوائف.문자((Integer)کوائف.مستقل_کوائف[اشاریہ]));
        throw new ترجمہ_نقص("정수와 سٹرنگ_قدر 상수만 مدد_قدر");
    }
    String 함수원형(طریقہ_حوالہ حوالہ) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(حوالہ.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + علامت("method", حوالہ.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void پڑتال_مقامی(int اشاریہ, int 지역변수수) { if (اشاریہ < 0 || اشاریہ >= 지역변수수) throw new ترجمہ_نقص("مقامی_سکوپ 변수 اشاریہ تراشہ نقص"); }
    void 분기넣기(List<String> 출력, Set<Integer> شاخ_فرست, int 위치, int 이동량, String حالت) {
        int منزل_مقصود_قدر = 위치 + 이동량; شاخ_فرست.add(منزل_مقصود_قدر);
        출력.add((حالت == null ? "" : "if (" + حالت + ") ") + "goto b" + منزل_مقصود_قدر + ";");
    }
    String 함수본문(طریقہ_حوالہ فعل_قدر, رکن_کوائف کوائف) {
        byte[] 본문자료 = کوائف.وصف_قدر.get("Code"); if (본문자료 == null) throw new ترجمہ_نقص("فعل_قدر 몸체가 없음: " + فعل_قدر.ناں);
        کوائف_پڑھن_والا پڑھن_والا_قدر = new کوائف_پڑھن_والا(본문자료); int 쌓임깊이 = پڑھن_والا_قدر.두바이트(), 지역변수수 = پڑھن_والا_قدر.두바이트();
        کوائف_پڑھن_والا حکم_کوائف = new کوائف_پڑھن_والا(پڑھن_والا_قدر.읽기(پڑھن_والا_قدر.네바이트()));
        if (پڑھن_والا_قدر.두바이트() != 0) throw new ترجمہ_نقص("try/catch/finally 미지원");
        함수형식 وضع_قدر = new 함수형식(فعل_قدر.서술); if (지역변수수 < وضع_قدر.인수.size()) throw new ترجمہ_نقص("매개변수보다 적은 مقامی_سکوپ 변수");
        درجہ_کوائف درجہ_قدر = 클래스들.get(فعل_قدر.مالک_قدر);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(فعل_قدر) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < وضع_قدر.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), شاخ_فرست = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (حکم_کوائف.위치 < حکم_کوائف.کوائف.length) {
            int 위치 = حکم_کوائف.위치, حکم = حکم_کوائف.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (حکم == 0) continue;
            if (حکم == 1) 출력.add("PUSH(0);");
            else if (حکم >= 2 && حکم <= 8) 출력.add("PUSH((uint32_t)(" + (حکم - 3) + "));");
            else if (حکم == 16 || حکم == 17) 출력.add("PUSH((uint32_t)(" + (حکم == 16 ? حکم_کوائف.부호한바이트() : حکم_کوائف.부호두바이트()) + "));");
            else if (حکم == 18 || حکم == 19) 출력.add("PUSH(" + مستقل_تاثر(درجہ_قدر, حکم == 18 ? حکم_کوائف.한바이트() : حکم_کوائف.두바이트()) + ");");
            else if (حکم == 21 || حکم == 25 || (حکم >= 26 && حکم <= 29) || (حکم >= 42 && حکم <= 45)) {
                int اشاریہ = حکم == 21 || حکم == 25 ? حکم_کوائف.한바이트() : حکم - (حکم <= 29 ? 26 : 42);
                پڑتال_مقامی(اشاریہ, 지역변수수); 출력.add("PUSH(l[" + اشاریہ + "]);");
            } else if (حکم == 54 || حکم == 58 || (حکم >= 59 && حکم <= 62) || (حکم >= 75 && حکم <= 78)) {
                int اشاریہ = حکم == 54 || حکم == 58 ? حکم_کوائف.한바이트() : حکم - (حکم <= 62 ? 59 : 75);
                پڑتال_مقامی(اشاریہ, 지역변수수); 출력.add("l[" + اشاریہ + "] = POP();");
            } else if (حکم == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (حکم == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (حکم == 87 || حکم == 88) 출력.add(حکم == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (حکم >= 89 && حکم <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ترتیب_فرست = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[حکم - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char قدر : ترتیب_فرست[حکم - 89].toCharArray()) 출력.add("PUSH(" + قدر + ");");
            } else if (حکم == 96 || حکم == 100 || حکم == 104 || حکم == 126 || حکم == 128 || حکم == 130) {
                String عمل_قدر_c96707fb = حکم == 96 ? "+" : حکم == 100 ? "-" : حکم == 104 ? "*" : حکم == 126 ? "&" : حکم == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + عمل_قدر_c96707fb + " (uint32_t)b);");
            } else if (حکم == 108 || حکم == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (حکم == 112 ? 1 : 0) + "));");
            else if (حکم == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (حکم == 120 || حکم == 122 || حکم == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (حکم == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (حکم == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (حکم == 132) {
                int اشاریہ = حکم_کوائف.한바이트(), 증가량 = حکم_کوائف.부호한바이트(); پڑتال_مقامی(اشاریہ, 지역변수수);
                출력.add("l[" + اشاریہ + "] = (uint32_t)l[" + اشاریہ + "] + (uint32_t)(" + 증가량 + ");");
            } else if (حکم >= 145 && حکم <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (حکم == 145 ? "int8_t" : حکم == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (حکم >= 153 && حکم <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, شاخ_فرست, 위치, حکم_کوائف.부호두바이트(), "(int32_t)a " + 비교들[حکم - 153] + " 0");
            } else if (حکم >= 159 && حکم <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, شاخ_فرست, 위치, حکم_کوائف.부호두바이트(), حکم >= 165 ? "a " + 비교들[حکم - 159] + " b" : "(int32_t)a " + 비교들[حکم - 159] + " (int32_t)b");
            } else if (حکم == 167 || حکم == 200) 분기넣기(출력, شاخ_فرست, 위치, حکم == 167 ? حکم_کوائف.부호두바이트() : حکم_کوائف.네바이트(), null);
            else if (حکم == 170 || حکم == 171) {
                while (حکم_کوائف.위치 % 4 != 0) حکم_کوائف.한바이트();
                int طےشدہ_قدر = حکم_کوائف.네바이트(); 출력.add("a = POP();");
                if (حکم == 170) {
                    int 아래 = حکم_کوائف.네바이트(), 위 = حکم_کوائف.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (حکم_کوائف.کوائف.length - حکم_کوائف.위치) / 4) throw new ترجمہ_نقص("switch تراشہ نقص");
                    for (long قدر = 아래; قدر <= 위; قدر++) 분기넣기(출력, شاخ_فرست, 위치, حکم_کوائف.네바이트(), "(int32_t)a == (" + قدر + ")");
                } else {
                    int 개수 = حکم_کوائف.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (حکم_کوائف.کوائف.length - حکم_کوائف.위치) / 8) throw new ترجمہ_نقص("switch سائز نقص");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int قدر = حکم_کوائف.네바이트(); if (순번 > 0 && قدر <= 앞값) throw new ترجمہ_نقص("switch ترتیب_قدر نقص"); 앞값 = قدر;
                        분기넣기(출력, شاخ_فرست, 위치, حکم_کوائف.네바이트(), "(int32_t)a == (" + قدر + ")");
                    }
                }
                분기넣기(출력, شاخ_فرست, 위치, طےشدہ_قدر, null);
            } else if (حکم == 172 || حکم == 176 || حکم == 177) 출력.add("return " + (حکم == 177 ? "0" : "POP()") + ";");
            else if (حکم == 178 || حکم == 179) {
                طریقہ_حوالہ حوالہ = درجہ_قدر.حوالہ(حکم_کوائف.두바이트()); if (!필드들.containsKey(حوالہ)) throw new ترجمہ_نقص("알 수 없는 قطعہ_قدر");
                출력.add(علامت("init", حوالہ.مالک_قدر) + "();"); String قطعہ_قدر = علامت("field", حوالہ.부분들());
                출력.add(حکم == 178 ? "PUSH(" + قطعہ_قدر + ");" : قطعہ_قدر + " = POP();");
            } else if (حکم == 184) {
                طریقہ_حوالہ حوالہ = درجہ_قدر.حوالہ(حکم_کوائف.두바이트()); if (!함수들.containsKey(حوالہ)) throw new ترجمہ_نقص("알 수 없는 فعل_قدر");
                함수형식 호출형식 = new 함수형식(حوالہ.서술); int 개수 = 호출형식.인수.size();
                출력.add(علامت("init", حوالہ.مالک_قدر) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + علامت("method", حوالہ.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (حکم == 182) {
                طریقہ_حوالہ حوالہ = درجہ_قدر.حوالہ(حکم_کوائف.두바이트());
                if (حوالہ.equals(new طریقہ_حوالہ("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (حوالہ.equals(new طریقہ_حوالہ("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new ترجمہ_نقص("가상 فعل_قدر 호출 미지원");
            } else if (حکم == 188) {
                if (حکم_کوائف.한바이트() != 10) throw new ترجمہ_نقص("new int[]만 مدد_قدر"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (حکم == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (حکم == 196) {
                int توسیع_قدر = حکم_کوائف.한바이트(), اشاریہ = حکم_کوائف.두바이트(); پڑتال_مقامی(اشاریہ, 지역변수수);
                if (توسیع_قدر == 21 || توسیع_قدر == 25) 출력.add("PUSH(l[" + اشاریہ + "]);");
                else if (توسیع_قدر == 54 || توسیع_قدر == 58) 출력.add("l[" + اشاریہ + "] = POP();");
                else if (توسیع_قدر == 132) 출력.add("l[" + اشاریہ + "] = (uint32_t)l[" + اشاریہ + "] + (uint32_t)(" + حکم_کوائف.부호두바이트() + ");");
                else throw new ترجمہ_نقص("미지원 wide حکم");
            } else if (حکم == 198 || حکم == 199) {
                출력.add("a = POP();"); 분기넣기(출력, شاخ_فرست, 위치, حکم_کوائف.부호두바이트(), "a " + (حکم == 198 ? "==" : "!=") + " 0");
            } else throw new ترجمہ_نقص(فعل_قدر.مالک_قدر + "." + فعل_قدر.ناں + ", بائٹ_قدر " + 위치 + ": 미지원 حکم " + حکم);
        }
        if (!경계들.containsAll(شاخ_فرست)) throw new ترجمہ_نقص("حکم 경계가 아닌 곳으로 شاخ");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String برآمد_طریقہ(String ربط_علامت, String ہدف, boolean 진입점여부) {
        int 자리 = ہدف.lastIndexOf('.'); if (자리 < 0 || !ربط_علامت.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ترجمہ_نقص("내보내기 지정 نقص");
        String مالک_قدر = ہدف.substring(0, 자리).replace('.', '/'), ناں = ہدف.substring(자리 + 1); طریقہ_حوالہ انتخاب_قدر = null;
        for (طریقہ_حوالہ حوالہ : 함수들.keySet()) if (حوالہ.مالک_قدر.equals(مالک_قدر) && حوالہ.ناں.equals(ناں)) {
            if (انتخاب_قدر != null) throw new ترجمہ_نقص("겹친 내보내기 ہدف"); انتخاب_قدر = حوالہ;
        }
        if (انتخاب_قدر == null || (함수들.get(انتخاب_قدر).پہنچ_داخلہ & 0x100) != 0) throw new ترجمہ_نقص("내보낼 함수가 없음 또는 native فعل_قدر");
        함수형식 وضع_قدر = new 함수형식(انتخاب_قدر.서술);
        if ((진입점여부 && !وضع_قدر.인수.isEmpty()) || !Arrays.asList("V", "I").contains(وضع_قدر.반환)) throw new ترجمہ_نقص("داخلہ_مقام_قدر 또는 C 경계 وضع_قدر نقص");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < وضع_قدر.인수.size(); 순번++) {
            if (!وضع_قدر.인수.get(순번).equals("I")) throw new ترجمہ_نقص("C 경계는 int 인수만 مدد_قدر");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (وضع_قدر.반환.equals("V") ? "void " : "int32_t ") + ربط_علامت + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + علامت("init", انتخاب_قدر.مالک_قدر) + "(); " + (وضع_قدر.반환.equals("V") ? "" : "return (int32_t)") + علامت("method", انتخاب_قدر.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String داخلہ_مقام, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<طریقہ_حوالہ, رکن_کوائف> داخلہ_قدر : 함수들.entrySet()) {
            طریقہ_حوالہ حوالہ = داخلہ_قدر.getKey(); رکن_کوائف کوائف = داخلہ_قدر.getValue(); 선언들.add(함수원형(حوالہ) + ";");
            if ((کوائف.پہنچ_داخلہ & 0x100) != 0) {
                String جڑو = 기계함수들.get(حوالہ.ناں + حوالہ.서술);
                if (!حوالہ.مالک_قدر.equals(مشین_درجہ) || جڑو == null) throw new ترجمہ_نقص("허용되지 않은 native فعل_قدر: " + حوالہ.ناں);
                int 개수 = new 함수형식(حوالہ.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + جڑو + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(حوالہ) + " { return " + جڑو + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(حوالہ, کوائف));
        }
        for (Map.Entry<طریقہ_حوالہ, رکن_کوائف> داخلہ_قدر : 필드들.entrySet()) {
            طریقہ_حوالہ حوالہ = داخلہ_قدر.getKey(); byte[] مستقل_قدر = داخلہ_قدر.getValue().وصف_قدر.get("ConstantValue");
            String قدر = مستقل_قدر == null ? "0" : مستقل_تاثر(클래스들.get(حوالہ.مالک_قدر), new کوائف_پڑھن_والا(مستقل_قدر).두바이트());
            필드선언들.add("static word " + علامت("field", حوالہ.부분들()) + " = " + قدر + ";");
        }
        for (String ناں : 클래스들.keySet()) {
            String آغاز_کرو = علامت("init", ناں), حالت_قدر = علامت("state", ناں);
            선언들.add("static void " + آغاز_کرو + "(void);"); 필드선언들.add("static unsigned " + حالت_قدر + ";");
            طریقہ_حوالہ حوالہ = new طریقہ_حوالہ(ناں, "<clinit>", "()V");
            몸체들.add("static void " + آغاز_کرو + "(void) { if(" + حالت_قدر + ") return; " + حالت_قدر + " = 1; " + (함수들.containsKey(حوالہ) ? علامت("method", حوالہ.부분들()) + "(); " : "") + حالت_قدر + " = 2; }");
        }
        몸체들.add(برآمد_طریقہ("java_entry", داخلہ_مقام, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new ترجمہ_نقص("내보내기 지정 نقص");
            String ناں = 지정.substring(0, 자리); 공개이름.add(ناں); 몸체들.add(برآمد_طریقہ(ناں, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> داخلہ_قدر : 문자열들.entrySet()) {
            String متن = داخلہ_قدر.getKey(); StringBuilder ایرے_قدر = new StringBuilder("static const word " + داخلہ_قدر.getValue() + "[] = {" + متن.length());
            for (int 순번 = 0; 순번 < متن.length(); 순번++) ایرے_قدر.append(", ").append((int)متن.charAt(순번));
            문자열선언들.add(ایرے_قدر.append("};").toString());
        }
        String مدد_قدر = Files.readString(ذریعہ_راہ.resolve("عام_زبان_چلانڑ_لگیان_مدد.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(مدد_قدر + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ماخذ, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ناں_جدول = new HashMap<>();
        for (String لائن : Files.readAllLines(ذریعہ_راہ.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] جوڑا_قدر = لائن.split("\t"); ناں_جدول.put(جوڑا_قدر[0], جوڑا_قدر[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(ماخذ); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String ناں = 찾개.group(), 새이름 = ناں;
            if (!ناں.startsWith("//") && !ناں.startsWith("/*") && !ناں.startsWith("\"") && !ناں.startsWith("'") && !공개이름.contains(ناں)) {
                새이름 = ناں_جدول.getOrDefault(ناں, ناں);
                if (ناں.matches("a[0-9]+")) 새이름 = "인수" + ناں.substring(1);
                if (ناں.matches("b[0-9]+")) 새이름 = "شاخ" + ناں.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char کریکٹر_قدر : 새이름.toCharArray()) 표기.append(کریکٹر_قدر < 128 ? Character.toString(کریکٹر_قدر) : String.format(Locale.ROOT, "\\u%04x", (int)کریکٹر_قدر));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(طریقہ_حوالہ فعل_قدر, رکن_کوائف کوائف, Map<String,String> مشین_جدول, String ہدف) {
        String 표식 = علامت("method", فعل_قدر.부분들());
        List<String> لائن = new ArrayList<>();
        if ((کوائف.پہنچ_داخلہ & 0x100) != 0) {
            String جڑو = مشین_جدول.get(فعل_قدر.ناں + فعل_قدر.서술);
            if (!فعل_قدر.مالک_قدر.equals(ہدف.equals("kernel") ? "آلہ_قدر" : "صارف") || جڑو == null) throw new ترجمہ_نقص("허용되지 않은 native فعل_قدر");
            return ".text\n" + 표식 + ":\njmp " + جڑو;
        }
        byte[] متن_دا_ڈھانچہ = کوائف.وصف_قدر.get("Code"); if (متن_دا_ڈھانچہ == null) throw new ترجمہ_نقص("فعل_قدر 몸체가 없음");
        کوائف_پڑھن_والا پڑھن_والا_قدر = new کوائف_پڑھن_والا(متن_دا_ڈھانچہ); پڑھن_والا_قدر.두바이트(); int 지역수 = پڑھن_والا_قدر.두바이트();
        کوائف_پڑھن_والا حکم_کوائف = new کوائف_پڑھن_والا(پڑھن_والا_قدر.읽기(پڑھن_والا_قدر.네바이트()));
        if (پڑھن_والا_قدر.두바이트() != 0) throw new ترجمہ_نقص("try/catch/finally 미지원");
        함수형식 وضع_قدر = new 함수형식(فعل_قدر.서술); if (지역수 < وضع_قدر.인수.size()) throw new ترجمہ_نقص("매개변수보다 적은 مقامی_سکوپ 변수");
        Collections.addAll(لائن,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < وضع_قدر.인수.size(); 순번++) Collections.addAll(لائن,"movl " + (8 + 4 * (وضع_قدر.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        درجہ_کوائف درجہ_قدر = 클래스들.get(فعل_قدر.مالک_قدر); Set<Integer> 경계들 = new HashSet<>(), شاخ_فرست = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (حکم_کوائف.위치 < حکم_کوائف.کوائف.length) {
            int 위치 = حکم_کوائف.위치, حکم = حکم_کوائف.한바이트(); String 자리 = 표식 + "_b" + 위치;
            لائن.add(자리 + ":"); 경계들.add(위치);
            if (حکم == 0) لائن.add("nop");
            else if (حکم == 1) لائن.add("pushl $0");
            else if (حکم >= 2 && حکم <= 8) لائن.add("pushl $" + (حکم - 3));
            else if (حکم == 16 || حکم == 17) لائن.add("pushl $" + (حکم == 16 ? حکم_کوائف.부호한바이트() : حکم_کوائف.부호두바이트()));
            else if (حکم == 18 || حکم == 19) {
                int اشاریہ = حکم == 18 ? حکم_کوائف.한바이트() : حکم_کوائف.두바이트();
                لائن.add("pushl $" + 엑스상수(درجہ_قدر,اشاریہ));
            } else if (حکم == 21 || حکم == 25 || (حکم >= 26 && حکم <= 29) || (حکم >= 42 && حکم <= 45) || حکم == 54 || حکم == 58 || (حکم >= 59 && حکم <= 62) || (حکم >= 75 && حکم <= 78)) {
                boolean 읽음 = حکم < 54; int اشاریہ = حکم == 21 || حکم == 25 || حکم == 54 || حکم == 58 ? حکم_کوائف.한바이트() : حکم - (حکم <= 29 ? 26 : حکم <= 45 ? 42 : حکم <= 62 ? 59 : 75);
                پڑتال_مقامی(اشاریہ,지역수); لائن.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (اشاریہ + 1)) + "(%ebp)");
            } else if (حکم == 46) Collections.addAll(لائن,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (حکم == 79) Collections.addAll(لائن,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (حکم == 87 || حکم == 88) لائن.add("addl $" + (حکم == 87 ? 4 : 8) + ", %esp");
            else if (حکم >= 89 && حکم <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ترتیب_فرست = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[حکم - 89]; 순번++) لائن.add("popl " + 저장기들[순번]);
                for (int 순번 : ترتیب_فرست[حکم - 89]) لائن.add("pushl " + 저장기들[순번]);
            } else if (حکم == 96 || حکم == 100 || حکم == 104 || حکم == 126 || حکم == 128 || حکم == 130) {
                String عمل_قدر_c96707fb = حکم == 96 ? "addl" : حکم == 100 ? "subl" : حکم == 104 ? "imull" : حکم == 126 ? "andl" : حکم == 128 ? "orl" : "xorl";
                Collections.addAll(لائن,"popl %ecx","popl %eax",عمل_قدر_c96707fb + " %ecx, %eax","pushl %eax");
            } else if (حکم == 108 || حکم == 112) Collections.addAll(لائن,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (حکم == 108 ? "%eax" : "%edx"));
            else if (حکم == 116) لائن.add("negl (%esp)");
            else if (حکم == 120 || حکم == 122 || حکم == 124) Collections.addAll(لائن,"popl %ecx","popl %eax",(حکم == 120 ? "sall" : حکم == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (حکم == 132) {
                int اشاریہ = حکم_کوائف.한바이트(), 증가 = حکم_کوائف.부호한바이트(); پڑتال_مقامی(اشاریہ,지역수); لائن.add("addl $" + 증가 + ", -" + (4 * (اشاریہ + 1)) + "(%ebp)");
            } else if (حکم >= 145 && حکم <= 147) Collections.addAll(لائن,"popl %eax",حکم == 145 ? "movsbl %al, %eax" : حکم == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (حکم >= 153 && حکم <= 166) {
                if (حکم <= 158) Collections.addAll(لائن,"popl %eax","testl %eax, %eax");
                else Collections.addAll(لائن,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int منزل_مقصود_قدر = 위치 + حکم_کوائف.부호두바이트(); شاخ_فرست.add(منزل_مقصود_قدر); لائن.add(비교들[حکم - (حکم <= 158 ? 153 : 159)] + " " + 표식 + "_b" + منزل_مقصود_قدر);
            } else if (حکم == 167 || حکم == 200) {
                int منزل_مقصود_قدر = 위치 + (حکم == 167 ? حکم_کوائف.부호두바이트() : حکم_کوائف.네바이트()); شاخ_فرست.add(منزل_مقصود_قدر); لائن.add("jmp " + 표식 + "_b" + منزل_مقصود_قدر);
            } else if (حکم == 170 || حکم == 171) {
                while (حکم_کوائف.위치 % 4 != 0) حکم_کوائف.한바이트();
                int طےشدہ_قدر = 위치 + حکم_کوائف.네바이트(); شاخ_فرست.add(طےشدہ_قدر); لائن.add("popl %eax");
                int 개수, 아래 = 0;
                if (حکم == 170) { 아래 = حکم_کوائف.네바이트(); int 위 = حکم_کوائف.네바이트(); long لمبائی_قدر = (long)위 - 아래 + 1; if (لمبائی_قدر < 1 || لمبائی_قدر > (حکم_کوائف.کوائف.length - حکم_کوائف.위치) / 4) throw new ترجمہ_نقص("switch تراشہ نقص"); 개수 = (int)لمبائی_قدر; }
                else { 개수 = حکم_کوائف.네바이트(); if (개수 < 0 || 개수 > (حکم_کوائف.کوائف.length - حکم_کوائف.위치) / 8) throw new ترجمہ_نقص("switch سائز نقص"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int قدر = حکم == 170 ? 아래 + 순번 : حکم_کوائف.네바이트(), منزل_مقصود_قدر = 위치 + حکم_کوائف.네바이트(); شاخ_فرست.add(منزل_مقصود_قدر);
                    Collections.addAll(لائن,"cmpl $" + قدر + ", %eax","je " + 표식 + "_b" + منزل_مقصود_قدر);
                }
                لائن.add("jmp " + 표식 + "_b" + طےشدہ_قدر);
            } else if (حکم == 172 || حکم == 176 || حکم == 177) {
                if (حکم != 177) لائن.add("popl %eax"); Collections.addAll(لائن,"leave","ret");
            } else if (حکم == 178 || حکم == 179) {
                طریقہ_حوالہ حوالہ = درجہ_قدر.حوالہ(حکم_کوائف.두바이트()); if (!필드들.containsKey(حوالہ)) throw new ترجمہ_نقص("알 수 없는 قطعہ_قدر");
                Collections.addAll(لائن,"call " + علامت("init",حوالہ.مالک_قدر),(حکم == 178 ? "pushl " : "popl ") + علامت("field",حوالہ.부분들()));
            } else if (حکم == 184) {
                طریقہ_حوالہ حوالہ = درجہ_قدر.حوالہ(حکم_کوائف.두바이트()); if (!함수들.containsKey(حوالہ)) throw new ترجمہ_نقص("알 수 없는 فعل_قدر");
                함수형식 호출형식 = new 함수형식(حوالہ.서술); Collections.addAll(لائن,"call " + علامت("init",حوالہ.مالک_قدر),"call " + علامت("method",حوالہ.부분들()));
                if (!호출형식.인수.isEmpty()) لائن.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) لائن.add("pushl %eax");
            } else if (حکم == 182) {
                طریقہ_حوالہ حوالہ = درجہ_قدر.حوالہ(حکم_کوائف.두바이트());
                if (حوالہ.equals(new طریقہ_حوالہ("java/lang/String","length","()I"))) Collections.addAll(لائن,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (حوالہ.equals(new طریقہ_حوالہ("java/lang/String","charAt","(I)C"))) Collections.addAll(لائن,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new ترجمہ_نقص("가상 فعل_قدر 호출 미지원");
            } else if (حکم == 188) {
                if (حکم_کوائف.한바이트() != 10) throw new ترجمہ_نقص("new int[]만 مدد_قدر"); Collections.addAll(لائن,"popl %eax","call rt_new_array","pushl %eax");
            } else if (حکم == 190) Collections.addAll(لائن,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (حکم == 196) {
                int توسیع_قدر = حکم_کوائف.한바이트(), اشاریہ = حکم_کوائف.두바이트(); پڑتال_مقامی(اشاریہ,지역수);
                if (توسیع_قدر == 21 || توسیع_قدر == 25 || توسیع_قدر == 54 || توسیع_قدر == 58) لائن.add((توسیع_قدر <= 25 ? "pushl " : "popl ") + "-" + 4 * (اشاریہ + 1) + "(%ebp)");
                else if (توسیع_قدر == 132) لائن.add("addl $" + حکم_کوائف.부호두바이트() + ", -" + 4 * (اشاریہ + 1) + "(%ebp)");
                else throw new ترجمہ_نقص("wide حکم 미지원");
            } else if (حکم == 198 || حکم == 199) {
                int منزل_مقصود_قدر = 위치 + حکم_کوائف.부호두바이트(); شاخ_فرست.add(منزل_مقصود_قدر); Collections.addAll(لائن,"popl %eax","testl %eax, %eax",(حکم == 198 ? "je " : "jne ") + 표식 + "_b" + منزل_مقصود_قدر);
            } else throw new ترجمہ_نقص("미지원 حکم: " + حکم);
        }
        if (!경계들.containsAll(شاخ_فرست)) throw new ترجمہ_نقص("حکم 경계가 아닌 곳으로 شاخ");
        لائن.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",لائن);
    }
    String 엑스상수(درجہ_کوائف کوائف, int اشاریہ) {
        if (کوائف.상수종류[اشاریہ] == 3) return کوائف.مستقل_کوائف[اشاریہ].toString();
        if (کوائف.상수종류[اشاریہ] == 8) return سٹرنگ_علامت(کوائف.문자((Integer)کوائف.مستقل_کوائف[اشاریہ]));
        throw new ترجمہ_نقص("정수와 سٹرنگ_قدر 상수만 مدد_قدر");
    }
    String 엑스조립본(String داخلہ_مقام, List<String> 내보냄, String ہدف) throws IOException {
        Map<String,String> مشین_جدول = new HashMap<>();
        for (String لائن : Files.readAllLines(ذریعہ_راہ.resolve("엑스기계함수.tsv"))) { String[] جوڑا_قدر = لائن.split("\t"); if (جوڑا_قدر[0].equals(ہدف)) مشین_جدول.put(جوڑا_قدر[1] + جوڑا_قدر[2],جوڑا_قدر[3]); }
        int 자리 = داخلہ_مقام.lastIndexOf('.'); if (자리 < 0) throw new ترجمہ_نقص("داخلہ_مقام 지정 نقص");
        String مالک_قدر = داخلہ_مقام.substring(0,자리).replace('.','/'), طریقہ_داخلہ_ناں = داخلہ_مقام.substring(자리 + 1); طریقہ_حوالہ داخلہ_مقام_قدر = null;
        for (String 서술 : Arrays.asList("()I","()V")) { طریقہ_حوالہ حوالہ = new طریقہ_حوالہ(مالک_قدر,طریقہ_داخلہ_ناں,서술); if (함수들.containsKey(حوالہ)) { if (داخلہ_مقام_قدر != null) throw new ترجمہ_نقص("겹친 داخلہ_مقام"); داخلہ_مقام_قدر = حوالہ; } }
        if (داخلہ_مقام_قدر == null || (함수들.get(داخلہ_مقام_قدر).پہنچ_داخلہ & 0x100) != 0) throw new ترجمہ_نقص("داخلہ_مقام_قدر فعل_قدر وضع_قدر نقص");
        List<String> لائن = new ArrayList<>(); لائن.add(".code32");
        for (درجہ_کوائف کوائف : 클래스들.values()) {
            String حالت_قدر = علامت("state",کوائف.ناں), آغاز_کرو = علامت("init",کوائف.ناں);
            Collections.addAll(لائن,".bss",".balign 4",حالت_قدر + ": .long 0",".text",آغاز_کرو + ":","cmpl $0, " + حالت_قدر,"jne " + آغاز_کرو + "_done","movl $1, " + حالت_قدر);
            طریقہ_حوالہ 초기화참조 = new طریقہ_حوالہ(کوائف.ناں,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) لائن.add("call " + علامت("method",초기화참조.부분들()));
            Collections.addAll(لائن,"movl $2, " + حالت_قدر,آغاز_کرو + "_done:","ret");
            for (رکن_کوائف قطعہ_قدر : کوائف.قطعہ_قدر) {
                byte[] مستقل_قدر = قطعہ_قدر.وصف_قدر.get("ConstantValue"); String قدر = مستقل_قدر == null ? "0" : 엑스상수(کوائف,new کوائف_پڑھن_والا(مستقل_قدر).두바이트());
                Collections.addAll(لائن,".data",".balign 4",علامت("field",کوائف.ناں,قطعہ_قدر.ناں,قطعہ_قدر.서술) + ": .long " + قدر);
            }
            for (رکن_کوائف فعل_قدر : کوائف.فعل_قدر) if (!فعل_قدر.ناں.equals("<init>")) لائن.add(엑스함수본문(new طریقہ_حوالہ(کوائف.ناں,فعل_قدر.ناں,فعل_قدر.서술),فعل_قدر,مشین_جدول,ہدف));
        }
        Collections.addAll(لائن,".text",".globl java_entry","java_entry:","call " + علامت("init",داخلہ_مقام_قدر.مالک_قدر),"call " + علامت("method",داخلہ_مقام_قدر.부분들()));
        if (داخلہ_مقام_قدر.서술.equals("()V")) لائن.add("xorl %eax, %eax"); لائن.add("ret");
        for (String 지정 : 내보냄) {
            int حد_بندی_کرنڑ_آلا_قدر = 지정.indexOf('='); if (حد_بندی_کرنڑ_آلا_قدر < 1) throw new ترجمہ_نقص("내보내기 지정 نقص");
            String 외부 = 지정.substring(0,حد_بندی_کرنڑ_آلا_قدر), فعل_قدر = 지정.substring(حد_بندی_کرنڑ_آلا_قدر + 1); int 나눔 = فعل_قدر.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ترجمہ_نقص("내보내기 علامت نقص");
            String درجہ_قدر = فعل_قدر.substring(0,나눔).replace('.','/'), ناں = فعل_قدر.substring(나눔 + 1); طریقہ_حوالہ انتخاب_قدر = null;
            for (طریقہ_حوالہ حوالہ : 함수들.keySet()) if (حوالہ.مالک_قدر.equals(درجہ_قدر) && حوالہ.ناں.equals(ناں)) { if (انتخاب_قدر != null) throw new ترجمہ_نقص("겹친 내보내기 ہدف"); انتخاب_قدر = حوالہ; }
            if (انتخاب_قدر == null) throw new ترجمہ_نقص("내보낼 함수가 없음");
            Collections.addAll(لائن,".text",".globl " + 외부,외부 + ":","call " + علامت("init",انتخاب_قدر.مالک_قدر),"jmp " + علامت("method",انتخاب_قدر.부분들()));
        }
        لائن.add(".section .rodata");
        for (Map.Entry<String,String> داخلہ_قدر : 문자열들.entrySet()) {
            Collections.addAll(لائن,".balign 4",داخلہ_قدر.getValue() + ":",".long " + داخلہ_قدر.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char سبق_قدر : داخلہ_قدر.getKey().toCharArray()) 단위들.add(Integer.toString(سبق_قدر)); if (!단위들.isEmpty()) لائن.add(".long " + String.join(",",단위들));
        }
        لائن.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",لائن) + "\n";
    }
    static void نفاذ_کرو_ٹول(List<String> حکم) throws Exception {
        if (new ProcessBuilder(حکم).inheritIO().start().waitFor() != 0) throw new ترجمہ_نقص("تیار_کرو_ماخذ نقص: " + حکم.get(0));
    }
    static String کوائف_سٹرنگ(String متن) { return "\"" + متن.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String ہدف, String داخلہ_مقام, List<String> 내보냄, Path 출력, Path ذریعہ_قدر) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), درجہ_راہ = 임시.resolve("classes"); Files.createDirectory(درجہ_راہ);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",درجہ_راہ.toString(),"-sourcepath",درجہ_راہ.toString(),"-d",درجہ_راہ.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new ترجمہ_نقص("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new ترجمہ_نقص(".java 또는 .class만 مدد_قدر");
            }
            if (원문수 > 0) نفاذ_کرو_ٹول(자바명령);
            try (java.util.stream.Stream<Path> راہ_فرست = Files.walk(درجہ_راہ)) { راہ_فرست.filter(راہ -> راہ.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,ہدف.equals("user") ? "user" : "kernel",262144,ذریعہ_قدر);
            String 조립 = 변환.엑스조립본(داخلہ_مقام,내보냄,ہدف); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = ذریعہ_قدر.getParent();
            نفاذ_کرو_ٹول(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            نفاذ_کرو_ٹول(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("عام_زبان_چلانڑ_لگیان_مدد.s").toString()));
            List<String> جڑو = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (ہدف.equals("kernel")) جڑو.add("-r");
            else {
                نفاذ_کرو_ٹول(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(ہدف.equals("user") ? "مکھ_صارف_ایپ.s" : "리눅스시작.s").toString()));
                Collections.addAll(جڑو,"-e","_start",임시.resolve("start.o").toString());
                if (ہدف.equals("user")) Collections.addAll(جڑو,"-T",도구위치.resolve("صارف_ربط_لے_آؤٹ.ld").toString());
            }
            Collections.addAll(جڑو,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); نفاذ_کرو_ٹول(جڑو);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path چھاپو_قدر = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),چھاپو_قدر,StandardCopyOption.REPLACE_EXISTING); Files.move(چھاپو_قدر,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(چھاپو_قدر); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(ہدف.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> علامت_کوائف = new ArrayList<>(), مآخذ_ڈیٹا = new ArrayList<>();
            for (طریقہ_حوالہ حوالہ : 변환.함수들.keySet()) علامت_کوائف.add(کوائف_سٹرنگ(علامت("method",حوالہ.부분들())) + ":" + کوائف_سٹرنگ(حوالہ.مالک_قدر + "." + حوالہ.ناں + حوالہ.서술));
            for (Path 입력 : 입력들) {
                byte[] ہیش_فائل = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder متن = new StringBuilder(); for (byte قدر : ہیش_فائل) متن.append(String.format(Locale.ROOT,"%02x",قدر & 255));
                مآخذ_ڈیٹا.add(کوائف_سٹرنگ(입력.toAbsolutePath().toString()) + ":" + کوائف_سٹرنگ(متن.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + کوائف_سٹرنگ(ہدف) + ",\"entry\":" + کوائف_سٹرنگ(داخلہ_مقام) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",علامت_کوائف) + "},\"sources\":{" + String.join(",",مآخذ_ڈیٹا) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> راہ_فرست = Files.walk(임시)) { for (Path راہ : (Iterable<Path>)راہ_فرست.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(راہ); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String داخلہ_مقام = null, ہدف = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> راہ_فرست = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String قدر = 인수[순번];
                switch (قدر) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry درجہ_قدر.فعل_قدر -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export علامت=درجہ_قدر.فعل_قدر] 클래스파일 또는 Java원문"); return;
                    case "--entry": داخلہ_مقام = 인수[++순번]; break;
                    case "--profile": ہدف = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (قدر.startsWith("-")) throw new ترجمہ_نقص("알 수 없는 옵션: " + قدر); راہ_فرست.add(Paths.get(قدر));
                }
            }
            if (داخلہ_مقام == null || 출력경로 == null || راہ_فرست.isEmpty()) throw new ترجمہ_نقص("--entry, -o, درجہ_قدر 파일이 필요합니다");
            Path ذریعہ_قدر = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new ترجمہ_نقص("알 수 없는 نفاذ_کرو_حکم ہدف");
                엑스번역(راہ_فرست,엑스대상,داخلہ_مقام,내보냄,출력경로,ذریعہ_قدر); return;
            }
            String ماخذ = new 기계어미리번역(راہ_فرست, ہدف, 낱말수, ذریعہ_قدر).생성(داخلہ_مقام, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ماخذ, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception نقص) { System.err.println("تیار_کرو_ماخذ نقص: " + نقص.getMessage()); System.exit(1); }
    }
}
