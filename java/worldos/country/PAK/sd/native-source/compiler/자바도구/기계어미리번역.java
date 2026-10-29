// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java درجو_قدر 파일에서 독립 ARM64 커널용 C 원문을 만든다. مهمان JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class ترجمو_نقص extends RuntimeException {
        ترجمو_نقص(String 설명) { super(설명); }
    }
    static final class ڪوائف_ريڊر {
        final byte[] ڪوائف;
        int 위치;
        ڪوائف_ريڊر(byte[] 입력자료) { ڪوائف = 입력자료; }
        byte[] 읽기(int لمبائي_قدر) {
            if (لمبائي_قدر < 0 || لمبائي_قدر > ڪوائف.length - 위치) throw new ترجمو_نقص("잘린 درجو_قدر 또는 حڪم ڪوائف");
            byte[] 결과 = Arrays.copyOfRange(ڪوائف, 위치, 위치 + لمبائي_قدر); 위치 += لمبائي_قدر; return 결과;
        }
        int 한바이트() { if (위치 >= ڪوائف.length) throw new ترجمو_نقص("잘린 حڪم ڪوائف"); return ڪوائف[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class رڪن_ڪوائف {
        final int پهچ_داخلا;
        final String نالو, 서술;
        final Map<String, byte[]> منسوب_ڪرڻ_قدر;
        رڪن_ڪوائف(int پهچ_قدر, String نالو_قدر, String 서술값, Map<String, byte[]> منسوب_ڪرڻ_ڪوائف) {
            پهچ_داخلا = پهچ_قدر; نالو = نالو_قدر; 서술 = 서술값; منسوب_ڪرڻ_قدر = منسوب_ڪرڻ_ڪوائف;
        }
    }
    static final class طريقو_حوالو implements Comparable<طريقو_حوالو> {
        final String مالڪ_قدر, نالو, 서술;
        طريقو_حوالو(String 소유값, String نالو_قدر, String 서술값) { مالڪ_قدر = 소유값; نالو = نالو_قدر; 서술 = 서술값; }
        String[] 부분들() { return new String[]{مالڪ_قدر, نالو, 서술}; }
        public int compareTo(طريقو_حوالو همعصر_قدر) {
            int 비교값 = مالڪ_قدر.compareTo(همعصر_قدر.مالڪ_قدر);
            if (비교값 == 0) 비교값 = نالو.compareTo(همعصر_قدر.نالو);
            return 비교값 == 0 ? 서술.compareTo(همعصر_قدر.서술) : 비교값;
        }
        public boolean equals(Object همعصر_قدر) { return همعصر_قدر instanceof طريقو_حوالو && compareTo((طريقو_حوالو) همعصر_قدر) == 0; }
        public int hashCode() { return Objects.hash(مالڪ_قدر, نالو, 서술); }
    }
    static final class درجو_ڪوائف {
        final int[] 상수종류;
        final Object[] لاڳاتار_جزو_ڪوائف;
        final String نالو;
        final List<رڪن_ڪوائف> قطعه_قدر, فعل_قدر;
        درجو_ڪوائف(Path راههه) throws IOException {
            ڪوائف_ريڊر ريڊر_قدر = new ڪوائف_ريڊر(Files.readAllBytes(راههه));
            if (ريڊر_قدر.네바이트() != 0xcafebabe) throw new ترجمو_نقص("Java درجو_قدر 표식이 아님");
            ريڊر_قدر.읽기(4);
            int 개수 = ريڊر_قدر.두바이트(); 상수종류 = new int[개수]; لاڳاتار_جزو_ڪوائف = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = ريڊر_قدر.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int لمبائي_قدر = ريڊر_قدر.두바이트();
                        byte[] ڪريڪٽر_بفر = ريڊر_قدر.읽기(لمبائي_قدر), 길이붙인자료 = new byte[لمبائي_قدر + 2];
                        길이붙인자료[0] = (byte)(لمبائي_قدر >> 8); 길이붙인자료[1] = (byte)لمبائي_قدر;
                        System.arraycopy(ڪريڪٽر_بفر, 0, 길이붙인자료, 2, لمبائي_قدر);
                        لاڳاتار_جزو_ڪوائف[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: لاڳاتار_جزو_ڪوائف[순번] = ريڊر_قدر.네바이트(); break;
                    case 4: ريڊر_قدر.읽기(4); break;
                    case 5: case 6: ريڊر_قدر.읽기(8); 순번++; break;
                    case 7: case 8: case 16: لاڳاتار_جزو_ڪوائف[순번] = ريڊر_قدر.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        لاڳاتار_جزو_ڪوائف[순번] = new int[]{ريڊر_قدر.두바이트(), ريڊر_قدر.두바이트()}; break;
                    case 15: لاڳاتار_جزو_ڪوائف[순번] = new int[]{ريڊر_قدر.한바이트(), ريڊر_قدر.두바이트()}; break;
                    default: throw new ترجمو_نقص("지원하지 않는 لاڳاتار_جزو_قدر 종류: " + 종류);
                }
            }
            ريڊر_قدر.두바이트(); نالو = درجو_نالو(ريڊر_قدر.두바이트());
            if (!درجو_نالو(ريڊر_قدر.두바이트()).equals("java/lang/Object") || ريڊر_قدر.두바이트() != 0)
                throw new ترجمو_نقص(نالو + ": 상속 및 인터페이스 미지원");
            قطعه_قدر = 멤버읽기(ريڊر_قدر); فعل_قدر = 멤버읽기(ريڊر_قدر); 속성읽기(ريڊر_قدر);
            if (ريڊر_قدر.위치 != ريڊر_قدر.ڪوائف.length) throw new ترجمو_نقص("درجو_قدر 뒤에 남은 ڪوائف");
        }
        String 문자(int ابتدائي) {
            if (ابتدائي < 1 || ابتدائي >= 상수종류.length || 상수종류[ابتدائي] != 1) throw new ترجمو_نقص("문자 لاڳاتار_جزو_قدر ابتدائي نقص");
            return (String) لاڳاتار_جزو_ڪوائف[ابتدائي];
        }
        String درجو_نالو(int ابتدائي) {
            if (ابتدائي < 1 || ابتدائي >= 상수종류.length || 상수종류[ابتدائي] != 7) throw new ترجمو_نقص("درجو_قدر حوالو نقص");
            return 문자((Integer)لاڳاتار_جزو_ڪوائف[ابتدائي]);
        }
        طريقو_حوالو حوالو(int ابتدائي) {
            if (ابتدائي < 1 || ابتدائي >= 상수종류.length || 상수종류[ابتدائي] < 9 || 상수종류[ابتدائي] > 11) throw new ترجمو_نقص("멤버 حوالو نقص");
            int[] جوڙو_قدر = (int[])لاڳاتار_جزو_ڪوائف[ابتدائي], نالو_جوڙو = (int[])لاڳاتار_جزو_ڪوائف[جوڙو_قدر[1]];
            return new طريقو_حوالو(درجو_نالو(جوڙو_قدر[0]), 문자(نالو_جوڙو[0]), 문자(نالو_جوڙو[1]));
        }
        Map<String, byte[]> 속성읽기(ڪوائف_ريڊر ريڊر_قدر) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = ريڊر_قدر.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String منسوب_ڪرڻ_نالو = 문자(ريڊر_قدر.두바이트()); byte[] قدر = ريڊر_قدر.읽기(ريڊر_قدر.네바이트());
                if (결과.put(منسوب_ڪرڻ_نالو, قدر) != null) throw new ترجمو_نقص("겹친 منسوب_ڪرڻ_قدر: " + منسوب_ڪرڻ_نالو);
            }
            return 결과;
        }
        List<رڪن_ڪوائف> 멤버읽기(ڪوائف_ريڊر ريڊر_قدر) {
            List<رڪن_ڪوائف> 결과 = new ArrayList<>(); int 개수 = ريڊر_قدر.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int پهچ_داخلا = ريڊر_قدر.두바이트(); String طريقو_داخلا_نالو = 문자(ريڊر_قدر.두바이트()), 서술 = 문자(ريڊر_قدر.두바이트());
                결과.add(new رڪن_ڪوائف(پهچ_داخلا, طريقو_داخلا_نالو, 서술, 속성읽기(ريڊر_قدر)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new ترجمو_نقص("فعل_قدر 서술 نقص: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new ترجمو_نقص("فعل_قدر 서술 نقص: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new ترجمو_نقص("فعل_قدر 서술 نقص: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String چونڊ_قدر = null;
            for (String وضع_قدر : 허용형식) if (서술.startsWith(وضع_قدر, 위치)) { چونڊ_قدر = وضع_قدر; break; }
            if (چونڊ_قدر == null) throw new ترجمو_نقص("지원하지 않는 ڊيٽا_قسم: " + 서술);
            결과.add(چونڊ_قدر); 위치 += چونڊ_قدر.length();
        }
        return 결과;
    }
    static String نشاني(String 종류, String... 부분들) {
        try {
            byte[] هيش_فائل = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder متن = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) متن.append(String.format(Locale.ROOT, "%02x", هيش_فائل[순번] & 255));
            return متن.toString();
        } catch (Exception نقص) { throw new ترجمو_نقص(نقص.toString()); }
    }
    final Map<String, درجو_ڪوائف> 클래스들 = new TreeMap<>();
    final Map<طريقو_حوالو, رڪن_ڪوائف> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, مشين_درجو;
    final int 동적기억낱말수;
    final Path ذريعو_راههه;
    기계어미리번역(List<Path> راههه_فهرست, String هدف, int 낱말수, Path ذريعو_قدر) throws IOException {
        if ((!هدف.equals("kernel") && !هدف.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new ترجمو_نقص("تعميل_ڪرڻ_حڪم هدف 또는 ميموري_قدر 공간 سائيز نقص");
        실행대상 = هدف; 동적기억낱말수 = 낱말수; ذريعو_راههه = ذريعو_قدر;
        // 이 이름도 국가별 ماخذ_شجرو 생성 시 해당 언어로 옮긴다.
        مشين_درجو = هدف.equals("kernel") ? "보드" : "صارف";
        for (String لڪير : Files.readAllLines(ذريعو_قدر.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = لڪير.split("\t", -1);
            if (부분들.length != 4) throw new ترجمو_نقص("مشين فعل_قدر ڪوائف نقص");
            if (부분들[0].equals(هدف)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path راههه : راههه_فهرست) {
            درجو_ڪوائف ڪوائف = new درجو_ڪوائف(راههه);
            if (클래스들.put(ڪوائف.نالو, ڪوائف) != null) throw new ترجمو_نقص("중복 درجو_قدر: " + ڪوائف.نالو);
            for (رڪن_ڪوائف قطعه_قدر : ڪوائف.قطعه_قدر) {
                if ((قطعه_قدر.پهچ_داخلا & 8) == 0 || 형식읽기(قطعه_قدر.서술).equals(Collections.singletonList("V"))) throw new ترجمو_نقص("ساقط_قدر 필드만 معاونت_قدر");
                if (필드들.put(new طريقو_حوالو(ڪوائف.نالو, قطعه_قدر.نالو, قطعه_قدر.서술), قطعه_قدر) != null) throw new ترجمو_نقص("중복 قطعه_قدر");
            }
            for (رڪن_ڪوائف فعل_قدر : ڪوائف.فعل_قدر) {
                if (فعل_قدر.نالو.equals("<init>")) continue;
                if ((فعل_قدر.پهچ_داخلا & 8) == 0 || (فعل_قدر.پهچ_داخلا & (0x20 | 0x400)) != 0) throw new ترجمو_نقص("ساقط_قدر 비동기화 함수만 معاونت_قدر");
                new 함수형식(فعل_قدر.서술);
                if (함수들.put(new طريقو_حوالو(ڪوائف.نالو, فعل_قدر.نالو, فعل_قدر.서술), فعل_قدر) != null) throw new ترجمو_نقص("중복 فعل_قدر");
            }
        }
    }
    String اسٽرنگ_نشاني(String متن) { return 문자열들.computeIfAbsent(متن, قدر -> "j_text_" + 문자열들.size()); }
    String لاڳاتار_جزو_اظهار(درجو_ڪوائف ڪوائف, int ابتدائي) {
        if (ابتدائي < 1 || ابتدائي >= ڪوائف.상수종류.length) throw new ترجمو_نقص("لاڳاتار_جزو_قدر ابتدائي تراشه نقص");
        if (ڪوائف.상수종류[ابتدائي] == 3) return "(word)(uint32_t)(" + ڪوائف.لاڳاتار_جزو_ڪوائف[ابتدائي] + ")";
        if (ڪوائف.상수종류[ابتدائي] == 8) return "(word)" + اسٽرنگ_نشاني(ڪوائف.문자((Integer)ڪوائف.لاڳاتار_جزو_ڪوائف[ابتدائي]));
        throw new ترجمو_نقص("정수와 اسٽرنگ_قدر 상수만 معاونت_قدر");
    }
    String 함수원형(طريقو_حوالو حوالو) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(حوالو.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + نشاني("method", حوالو.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void پڙتال_ڪريو_مقامي(int ابتدائي, int 지역변수수) { if (ابتدائي < 0 || ابتدائي >= 지역변수수) throw new ترجمو_نقص("مقامي_اسڪوپ 변수 ابتدائي تراشه نقص"); }
    void 분기넣기(List<String> 출력, Set<Integer> شاخ_فهرست, int 위치, int 이동량, String حالت) {
        int منزل_مقصود_قدر = 위치 + 이동량; شاخ_فهرست.add(منزل_مقصود_قدر);
        출력.add((حالت == null ? "" : "if (" + حالت + ") ") + "goto b" + منزل_مقصود_قدر + ";");
    }
    String 함수본문(طريقو_حوالو فعل_قدر, رڪن_ڪوائف ڪوائف) {
        byte[] 본문자료 = ڪوائف.منسوب_ڪرڻ_قدر.get("Code"); if (본문자료 == null) throw new ترجمو_نقص("فعل_قدر 몸체가 없음: " + فعل_قدر.نالو);
        ڪوائف_ريڊر ريڊر_قدر = new ڪوائف_ريڊر(본문자료); int 쌓임깊이 = ريڊر_قدر.두바이트(), 지역변수수 = ريڊر_قدر.두바이트();
        ڪوائف_ريڊر حڪم_ڪوائف = new ڪوائف_ريڊر(ريڊر_قدر.읽기(ريڊر_قدر.네바이트()));
        if (ريڊر_قدر.두바이트() != 0) throw new ترجمو_نقص("try/catch/finally 미지원");
        함수형식 وضع_قدر = new 함수형식(فعل_قدر.서술); if (지역변수수 < وضع_قدر.인수.size()) throw new ترجمو_نقص("매개변수보다 적은 مقامي_اسڪوپ 변수");
        درجو_ڪوائف درجو_قدر = 클래스들.get(فعل_قدر.مالڪ_قدر);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(فعل_قدر) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < وضع_قدر.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), شاخ_فهرست = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (حڪم_ڪوائف.위치 < حڪم_ڪوائف.ڪوائف.length) {
            int 위치 = حڪم_ڪوائف.위치, حڪم = حڪم_ڪوائف.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (حڪم == 0) continue;
            if (حڪم == 1) 출력.add("PUSH(0);");
            else if (حڪم >= 2 && حڪم <= 8) 출력.add("PUSH((uint32_t)(" + (حڪم - 3) + "));");
            else if (حڪم == 16 || حڪم == 17) 출력.add("PUSH((uint32_t)(" + (حڪم == 16 ? حڪم_ڪوائف.부호한바이트() : حڪم_ڪوائف.부호두바이트()) + "));");
            else if (حڪم == 18 || حڪم == 19) 출력.add("PUSH(" + لاڳاتار_جزو_اظهار(درجو_قدر, حڪم == 18 ? حڪم_ڪوائف.한바이트() : حڪم_ڪوائف.두바이트()) + ");");
            else if (حڪم == 21 || حڪم == 25 || (حڪم >= 26 && حڪم <= 29) || (حڪم >= 42 && حڪم <= 45)) {
                int ابتدائي = حڪم == 21 || حڪم == 25 ? حڪم_ڪوائف.한바이트() : حڪم - (حڪم <= 29 ? 26 : 42);
                پڙتال_ڪريو_مقامي(ابتدائي, 지역변수수); 출력.add("PUSH(l[" + ابتدائي + "]);");
            } else if (حڪم == 54 || حڪم == 58 || (حڪم >= 59 && حڪم <= 62) || (حڪم >= 75 && حڪم <= 78)) {
                int ابتدائي = حڪم == 54 || حڪم == 58 ? حڪم_ڪوائف.한바이트() : حڪم - (حڪم <= 62 ? 59 : 75);
                پڙتال_ڪريو_مقامي(ابتدائي, 지역변수수); 출력.add("l[" + ابتدائي + "] = POP();");
            } else if (حڪم == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (حڪم == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (حڪم == 87 || حڪم == 88) 출력.add(حڪم == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (حڪم >= 89 && حڪم <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ترتيب_فهرست = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[حڪم - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char قدر : ترتيب_فهرست[حڪم - 89].toCharArray()) 출력.add("PUSH(" + قدر + ");");
            } else if (حڪم == 96 || حڪم == 100 || حڪم == 104 || حڪم == 126 || حڪم == 128 || حڪم == 130) {
                String عمل_قدر_c96707fb = حڪم == 96 ? "+" : حڪم == 100 ? "-" : حڪم == 104 ? "*" : حڪم == 126 ? "&" : حڪم == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + عمل_قدر_c96707fb + " (uint32_t)b);");
            } else if (حڪم == 108 || حڪم == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (حڪم == 112 ? 1 : 0) + "));");
            else if (حڪم == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (حڪم == 120 || حڪم == 122 || حڪم == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (حڪم == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (حڪم == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (حڪم == 132) {
                int ابتدائي = حڪم_ڪوائف.한바이트(), 증가량 = حڪم_ڪوائف.부호한바이트(); پڙتال_ڪريو_مقامي(ابتدائي, 지역변수수);
                출력.add("l[" + ابتدائي + "] = (uint32_t)l[" + ابتدائي + "] + (uint32_t)(" + 증가량 + ");");
            } else if (حڪم >= 145 && حڪم <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (حڪم == 145 ? "int8_t" : حڪم == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (حڪم >= 153 && حڪم <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, شاخ_فهرست, 위치, حڪم_ڪوائف.부호두바이트(), "(int32_t)a " + 비교들[حڪم - 153] + " 0");
            } else if (حڪم >= 159 && حڪم <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, شاخ_فهرست, 위치, حڪم_ڪوائف.부호두바이트(), حڪم >= 165 ? "a " + 비교들[حڪم - 159] + " b" : "(int32_t)a " + 비교들[حڪم - 159] + " (int32_t)b");
            } else if (حڪم == 167 || حڪم == 200) 분기넣기(출력, شاخ_فهرست, 위치, حڪم == 167 ? حڪم_ڪوائف.부호두바이트() : حڪم_ڪوائف.네바이트(), null);
            else if (حڪم == 170 || حڪم == 171) {
                while (حڪم_ڪوائف.위치 % 4 != 0) حڪم_ڪوائف.한바이트();
                int طئي_ٿيل_ملهه = حڪم_ڪوائف.네바이트(); 출력.add("a = POP();");
                if (حڪم == 170) {
                    int 아래 = حڪم_ڪوائف.네바이트(), 위 = حڪم_ڪوائف.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (حڪم_ڪوائف.ڪوائف.length - حڪم_ڪوائف.위치) / 4) throw new ترجمو_نقص("switch تراشه نقص");
                    for (long قدر = 아래; قدر <= 위; قدر++) 분기넣기(출력, شاخ_فهرست, 위치, حڪم_ڪوائف.네바이트(), "(int32_t)a == (" + قدر + ")");
                } else {
                    int 개수 = حڪم_ڪوائف.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (حڪم_ڪوائف.ڪوائف.length - حڪم_ڪوائف.위치) / 8) throw new ترجمو_نقص("switch سائيز نقص");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int قدر = حڪم_ڪوائف.네바이트(); if (순번 > 0 && قدر <= 앞값) throw new ترجمو_نقص("switch ترتيب_قدر نقص"); 앞값 = قدر;
                        분기넣기(출력, شاخ_فهرست, 위치, حڪم_ڪوائف.네바이트(), "(int32_t)a == (" + قدر + ")");
                    }
                }
                분기넣기(출력, شاخ_فهرست, 위치, طئي_ٿيل_ملهه, null);
            } else if (حڪم == 172 || حڪم == 176 || حڪم == 177) 출력.add("return " + (حڪم == 177 ? "0" : "POP()") + ";");
            else if (حڪم == 178 || حڪم == 179) {
                طريقو_حوالو حوالو = درجو_قدر.حوالو(حڪم_ڪوائف.두바이트()); if (!필드들.containsKey(حوالو)) throw new ترجمو_نقص("알 수 없는 قطعه_قدر");
                출력.add(نشاني("init", حوالو.مالڪ_قدر) + "();"); String قطعه_قدر = نشاني("field", حوالو.부분들());
                출력.add(حڪم == 178 ? "PUSH(" + قطعه_قدر + ");" : قطعه_قدر + " = POP();");
            } else if (حڪم == 184) {
                طريقو_حوالو حوالو = درجو_قدر.حوالو(حڪم_ڪوائف.두바이트()); if (!함수들.containsKey(حوالو)) throw new ترجمو_نقص("알 수 없는 فعل_قدر");
                함수형식 호출형식 = new 함수형식(حوالو.서술); int 개수 = 호출형식.인수.size();
                출력.add(نشاني("init", حوالو.مالڪ_قدر) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + نشاني("method", حوالو.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (حڪم == 182) {
                طريقو_حوالو حوالو = درجو_قدر.حوالو(حڪم_ڪوائف.두바이트());
                if (حوالو.equals(new طريقو_حوالو("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (حوالو.equals(new طريقو_حوالو("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new ترجمو_نقص("가상 فعل_قدر 호출 미지원");
            } else if (حڪم == 188) {
                if (حڪم_ڪوائف.한바이트() != 10) throw new ترجمو_نقص("new int[]만 معاونت_قدر"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (حڪم == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (حڪم == 196) {
                int واڌ_قدر = حڪم_ڪوائف.한바이트(), ابتدائي = حڪم_ڪوائف.두바이트(); پڙتال_ڪريو_مقامي(ابتدائي, 지역변수수);
                if (واڌ_قدر == 21 || واڌ_قدر == 25) 출력.add("PUSH(l[" + ابتدائي + "]);");
                else if (واڌ_قدر == 54 || واڌ_قدر == 58) 출력.add("l[" + ابتدائي + "] = POP();");
                else if (واڌ_قدر == 132) 출력.add("l[" + ابتدائي + "] = (uint32_t)l[" + ابتدائي + "] + (uint32_t)(" + حڪم_ڪوائف.부호두바이트() + ");");
                else throw new ترجمو_نقص("미지원 wide حڪم");
            } else if (حڪم == 198 || حڪم == 199) {
                출력.add("a = POP();"); 분기넣기(출력, شاخ_فهرست, 위치, حڪم_ڪوائف.부호두바이트(), "a " + (حڪم == 198 ? "==" : "!=") + " 0");
            } else throw new ترجمو_نقص(فعل_قدر.مالڪ_قدر + "." + فعل_قدر.نالو + ", بائٽ_قدر " + 위치 + ": 미지원 حڪم " + حڪم);
        }
        if (!경계들.containsAll(شاخ_فهرست)) throw new ترجمو_نقص("حڪم 경계가 아닌 곳으로 شاخ");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String برآمد_طريقو(String ڪڙي_نشاني, String هدف, boolean 진입점여부) {
        int 자리 = هدف.lastIndexOf('.'); if (자리 < 0 || !ڪڙي_نشاني.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ترجمو_نقص("내보내기 지정 نقص");
        String مالڪ_قدر = هدف.substring(0, 자리).replace('.', '/'), نالو = هدف.substring(자리 + 1); طريقو_حوالو چونڊ_قدر = null;
        for (طريقو_حوالو حوالو : 함수들.keySet()) if (حوالو.مالڪ_قدر.equals(مالڪ_قدر) && حوالو.نالو.equals(نالو)) {
            if (چونڊ_قدر != null) throw new ترجمو_نقص("겹친 내보내기 هدف"); چونڊ_قدر = حوالو;
        }
        if (چونڊ_قدر == null || (함수들.get(چونڊ_قدر).پهچ_داخلا & 0x100) != 0) throw new ترجمو_نقص("내보낼 함수가 없음 또는 native فعل_قدر");
        함수형식 وضع_قدر = new 함수형식(چونڊ_قدر.서술);
        if ((진입점여부 && !وضع_قدر.인수.isEmpty()) || !Arrays.asList("V", "I").contains(وضع_قدر.반환)) throw new ترجمو_نقص("داخلا_هنڌ_قدر 또는 C 경계 وضع_قدر نقص");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < وضع_قدر.인수.size(); 순번++) {
            if (!وضع_قدر.인수.get(순번).equals("I")) throw new ترجمو_نقص("C 경계는 int 인수만 معاونت_قدر");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (وضع_قدر.반환.equals("V") ? "void " : "int32_t ") + ڪڙي_نشاني + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + نشاني("init", چونڊ_قدر.مالڪ_قدر) + "(); " + (وضع_قدر.반환.equals("V") ? "" : "return (int32_t)") + نشاني("method", چونڊ_قدر.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String داخلا_هنڌ, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<طريقو_حوالو, رڪن_ڪوائف> داخلا_قدر : 함수들.entrySet()) {
            طريقو_حوالو حوالو = داخلا_قدر.getKey(); رڪن_ڪوائف ڪوائف = داخلا_قدر.getValue(); 선언들.add(함수원형(حوالو) + ";");
            if ((ڪوائف.پهچ_داخلا & 0x100) != 0) {
                String ڪنيڪٽ = 기계함수들.get(حوالو.نالو + حوالو.서술);
                if (!حوالو.مالڪ_قدر.equals(مشين_درجو) || ڪنيڪٽ == null) throw new ترجمو_نقص("허용되지 않은 native فعل_قدر: " + حوالو.نالو);
                int 개수 = new 함수형식(حوالو.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + ڪنيڪٽ + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(حوالو) + " { return " + ڪنيڪٽ + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(حوالو, ڪوائف));
        }
        for (Map.Entry<طريقو_حوالو, رڪن_ڪوائف> داخلا_قدر : 필드들.entrySet()) {
            طريقو_حوالو حوالو = داخلا_قدر.getKey(); byte[] لاڳاتار_جزو_قدر = داخلا_قدر.getValue().منسوب_ڪرڻ_قدر.get("ConstantValue");
            String قدر = لاڳاتار_جزو_قدر == null ? "0" : لاڳاتار_جزو_اظهار(클래스들.get(حوالو.مالڪ_قدر), new ڪوائف_ريڊر(لاڳاتار_جزو_قدر).두바이트());
            필드선언들.add("static word " + نشاني("field", حوالو.부분들()) + " = " + قدر + ";");
        }
        for (String نالو : 클래스들.keySet()) {
            String شروع_ڪريو = نشاني("init", نالو), حالت_قدر = نشاني("state", نالو);
            선언들.add("static void " + شروع_ڪريو + "(void);"); 필드선언들.add("static unsigned " + حالت_قدر + ";");
            طريقو_حوالو حوالو = new طريقو_حوالو(نالو, "<clinit>", "()V");
            몸체들.add("static void " + شروع_ڪريو + "(void) { if(" + حالت_قدر + ") return; " + حالت_قدر + " = 1; " + (함수들.containsKey(حوالو) ? نشاني("method", حوالو.부분들()) + "(); " : "") + حالت_قدر + " = 2; }");
        }
        몸체들.add(برآمد_طريقو("java_entry", داخلا_هنڌ, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new ترجمو_نقص("내보내기 지정 نقص");
            String نالو = 지정.substring(0, 자리); 공개이름.add(نالو); 몸체들.add(برآمد_طريقو(نالو, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> داخلا_قدر : 문자열들.entrySet()) {
            String متن = داخلا_قدر.getKey(); StringBuilder ترتيب_قدر_ed437109 = new StringBuilder("static const word " + داخلا_قدر.getValue() + "[] = {" + متن.length());
            for (int 순번 = 0; 순번 < متن.length(); 순번++) ترتيب_قدر_ed437109.append(", ").append((int)متن.charAt(순번));
            문자열선언들.add(ترتيب_قدر_ed437109.append("};").toString());
        }
        String معاونت_قدر = Files.readString(ذريعو_راههه.resolve("عام_ٻولي_جو_رن_ٽائيم_معاونت.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(معاونت_قدر + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ماخذ, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> نالو_جدول = new HashMap<>();
        for (String لڪير : Files.readAllLines(ذريعو_راههه.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] جوڙو_قدر = لڪير.split("\t"); نالو_جدول.put(جوڙو_قدر[0], جوڙو_قدر[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(ماخذ); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String نالو = 찾개.group(), 새이름 = نالو;
            if (!نالو.startsWith("//") && !نالو.startsWith("/*") && !نالو.startsWith("\"") && !نالو.startsWith("'") && !공개이름.contains(نالو)) {
                새이름 = نالو_جدول.getOrDefault(نالو, نالو);
                if (نالو.matches("a[0-9]+")) 새이름 = "인수" + نالو.substring(1);
                if (نالو.matches("b[0-9]+")) 새이름 = "شاخ" + نالو.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char ڪريڪٽر_قدر : 새이름.toCharArray()) 표기.append(ڪريڪٽر_قدر < 128 ? Character.toString(ڪريڪٽر_قدر) : String.format(Locale.ROOT, "\\u%04x", (int)ڪريڪٽر_قدر));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(طريقو_حوالو فعل_قدر, رڪن_ڪوائف ڪوائف, Map<String,String> مشين_جدول, String هدف) {
        String 표식 = نشاني("method", فعل_قدر.부분들());
        List<String> لڪير = new ArrayList<>();
        if ((ڪوائف.پهچ_داخلا & 0x100) != 0) {
            String ڪنيڪٽ = مشين_جدول.get(فعل_قدر.نالو + فعل_قدر.서술);
            if (!فعل_قدر.مالڪ_قدر.equals(هدف.equals("kernel") ? "آلو_قدر" : "صارف") || ڪنيڪٽ == null) throw new ترجمو_نقص("허용되지 않은 native فعل_قدر");
            return ".text\n" + 표식 + ":\njmp " + ڪنيڪٽ;
        }
        byte[] باڊي_متن = ڪوائف.منسوب_ڪرڻ_قدر.get("Code"); if (باڊي_متن == null) throw new ترجمو_نقص("فعل_قدر 몸체가 없음");
        ڪوائف_ريڊر ريڊر_قدر = new ڪوائف_ريڊر(باڊي_متن); ريڊر_قدر.두바이트(); int 지역수 = ريڊر_قدر.두바이트();
        ڪوائف_ريڊر حڪم_ڪوائف = new ڪوائف_ريڊر(ريڊر_قدر.읽기(ريڊر_قدر.네바이트()));
        if (ريڊر_قدر.두바이트() != 0) throw new ترجمو_نقص("try/catch/finally 미지원");
        함수형식 وضع_قدر = new 함수형식(فعل_قدر.서술); if (지역수 < وضع_قدر.인수.size()) throw new ترجمو_نقص("매개변수보다 적은 مقامي_اسڪوپ 변수");
        Collections.addAll(لڪير,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < وضع_قدر.인수.size(); 순번++) Collections.addAll(لڪير,"movl " + (8 + 4 * (وضع_قدر.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        درجو_ڪوائف درجو_قدر = 클래스들.get(فعل_قدر.مالڪ_قدر); Set<Integer> 경계들 = new HashSet<>(), شاخ_فهرست = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (حڪم_ڪوائف.위치 < حڪم_ڪوائف.ڪوائف.length) {
            int 위치 = حڪم_ڪوائف.위치, حڪم = حڪم_ڪوائف.한바이트(); String 자리 = 표식 + "_b" + 위치;
            لڪير.add(자리 + ":"); 경계들.add(위치);
            if (حڪم == 0) لڪير.add("nop");
            else if (حڪم == 1) لڪير.add("pushl $0");
            else if (حڪم >= 2 && حڪم <= 8) لڪير.add("pushl $" + (حڪم - 3));
            else if (حڪم == 16 || حڪم == 17) لڪير.add("pushl $" + (حڪم == 16 ? حڪم_ڪوائف.부호한바이트() : حڪم_ڪوائف.부호두바이트()));
            else if (حڪم == 18 || حڪم == 19) {
                int ابتدائي = حڪم == 18 ? حڪم_ڪوائف.한바이트() : حڪم_ڪوائف.두바이트();
                لڪير.add("pushl $" + 엑스상수(درجو_قدر,ابتدائي));
            } else if (حڪم == 21 || حڪم == 25 || (حڪم >= 26 && حڪم <= 29) || (حڪم >= 42 && حڪم <= 45) || حڪم == 54 || حڪم == 58 || (حڪم >= 59 && حڪم <= 62) || (حڪم >= 75 && حڪم <= 78)) {
                boolean 읽음 = حڪم < 54; int ابتدائي = حڪم == 21 || حڪم == 25 || حڪم == 54 || حڪم == 58 ? حڪم_ڪوائف.한바이트() : حڪم - (حڪم <= 29 ? 26 : حڪم <= 45 ? 42 : حڪم <= 62 ? 59 : 75);
                پڙتال_ڪريو_مقامي(ابتدائي,지역수); لڪير.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (ابتدائي + 1)) + "(%ebp)");
            } else if (حڪم == 46) Collections.addAll(لڪير,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (حڪم == 79) Collections.addAll(لڪير,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (حڪم == 87 || حڪم == 88) لڪير.add("addl $" + (حڪم == 87 ? 4 : 8) + ", %esp");
            else if (حڪم >= 89 && حڪم <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ترتيب_فهرست = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[حڪم - 89]; 순번++) لڪير.add("popl " + 저장기들[순번]);
                for (int 순번 : ترتيب_فهرست[حڪم - 89]) لڪير.add("pushl " + 저장기들[순번]);
            } else if (حڪم == 96 || حڪم == 100 || حڪم == 104 || حڪم == 126 || حڪم == 128 || حڪم == 130) {
                String عمل_قدر_c96707fb = حڪم == 96 ? "addl" : حڪم == 100 ? "subl" : حڪم == 104 ? "imull" : حڪم == 126 ? "andl" : حڪم == 128 ? "orl" : "xorl";
                Collections.addAll(لڪير,"popl %ecx","popl %eax",عمل_قدر_c96707fb + " %ecx, %eax","pushl %eax");
            } else if (حڪم == 108 || حڪم == 112) Collections.addAll(لڪير,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (حڪم == 108 ? "%eax" : "%edx"));
            else if (حڪم == 116) لڪير.add("negl (%esp)");
            else if (حڪم == 120 || حڪم == 122 || حڪم == 124) Collections.addAll(لڪير,"popl %ecx","popl %eax",(حڪم == 120 ? "sall" : حڪم == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (حڪم == 132) {
                int ابتدائي = حڪم_ڪوائف.한바이트(), 증가 = حڪم_ڪوائف.부호한바이트(); پڙتال_ڪريو_مقامي(ابتدائي,지역수); لڪير.add("addl $" + 증가 + ", -" + (4 * (ابتدائي + 1)) + "(%ebp)");
            } else if (حڪم >= 145 && حڪم <= 147) Collections.addAll(لڪير,"popl %eax",حڪم == 145 ? "movsbl %al, %eax" : حڪم == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (حڪم >= 153 && حڪم <= 166) {
                if (حڪم <= 158) Collections.addAll(لڪير,"popl %eax","testl %eax, %eax");
                else Collections.addAll(لڪير,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int منزل_مقصود_قدر = 위치 + حڪم_ڪوائف.부호두바이트(); شاخ_فهرست.add(منزل_مقصود_قدر); لڪير.add(비교들[حڪم - (حڪم <= 158 ? 153 : 159)] + " " + 표식 + "_b" + منزل_مقصود_قدر);
            } else if (حڪم == 167 || حڪم == 200) {
                int منزل_مقصود_قدر = 위치 + (حڪم == 167 ? حڪم_ڪوائف.부호두바이트() : حڪم_ڪوائف.네바이트()); شاخ_فهرست.add(منزل_مقصود_قدر); لڪير.add("jmp " + 표식 + "_b" + منزل_مقصود_قدر);
            } else if (حڪم == 170 || حڪم == 171) {
                while (حڪم_ڪوائف.위치 % 4 != 0) حڪم_ڪوائف.한바이트();
                int طئي_ٿيل_ملهه = 위치 + حڪم_ڪوائف.네바이트(); شاخ_فهرست.add(طئي_ٿيل_ملهه); لڪير.add("popl %eax");
                int 개수, 아래 = 0;
                if (حڪم == 170) { 아래 = حڪم_ڪوائف.네바이트(); int 위 = حڪم_ڪوائف.네바이트(); long لمبائي_قدر = (long)위 - 아래 + 1; if (لمبائي_قدر < 1 || لمبائي_قدر > (حڪم_ڪوائف.ڪوائف.length - حڪم_ڪوائف.위치) / 4) throw new ترجمو_نقص("switch تراشه نقص"); 개수 = (int)لمبائي_قدر; }
                else { 개수 = حڪم_ڪوائف.네바이트(); if (개수 < 0 || 개수 > (حڪم_ڪوائف.ڪوائف.length - حڪم_ڪوائف.위치) / 8) throw new ترجمو_نقص("switch سائيز نقص"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int قدر = حڪم == 170 ? 아래 + 순번 : حڪم_ڪوائف.네바이트(), منزل_مقصود_قدر = 위치 + حڪم_ڪوائف.네바이트(); شاخ_فهرست.add(منزل_مقصود_قدر);
                    Collections.addAll(لڪير,"cmpl $" + قدر + ", %eax","je " + 표식 + "_b" + منزل_مقصود_قدر);
                }
                لڪير.add("jmp " + 표식 + "_b" + طئي_ٿيل_ملهه);
            } else if (حڪم == 172 || حڪم == 176 || حڪم == 177) {
                if (حڪم != 177) لڪير.add("popl %eax"); Collections.addAll(لڪير,"leave","ret");
            } else if (حڪم == 178 || حڪم == 179) {
                طريقو_حوالو حوالو = درجو_قدر.حوالو(حڪم_ڪوائف.두바이트()); if (!필드들.containsKey(حوالو)) throw new ترجمو_نقص("알 수 없는 قطعه_قدر");
                Collections.addAll(لڪير,"call " + نشاني("init",حوالو.مالڪ_قدر),(حڪم == 178 ? "pushl " : "popl ") + نشاني("field",حوالو.부분들()));
            } else if (حڪم == 184) {
                طريقو_حوالو حوالو = درجو_قدر.حوالو(حڪم_ڪوائف.두바이트()); if (!함수들.containsKey(حوالو)) throw new ترجمو_نقص("알 수 없는 فعل_قدر");
                함수형식 호출형식 = new 함수형식(حوالو.서술); Collections.addAll(لڪير,"call " + نشاني("init",حوالو.مالڪ_قدر),"call " + نشاني("method",حوالو.부분들()));
                if (!호출형식.인수.isEmpty()) لڪير.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) لڪير.add("pushl %eax");
            } else if (حڪم == 182) {
                طريقو_حوالو حوالو = درجو_قدر.حوالو(حڪم_ڪوائف.두바이트());
                if (حوالو.equals(new طريقو_حوالو("java/lang/String","length","()I"))) Collections.addAll(لڪير,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (حوالو.equals(new طريقو_حوالو("java/lang/String","charAt","(I)C"))) Collections.addAll(لڪير,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new ترجمو_نقص("가상 فعل_قدر 호출 미지원");
            } else if (حڪم == 188) {
                if (حڪم_ڪوائف.한바이트() != 10) throw new ترجمو_نقص("new int[]만 معاونت_قدر"); Collections.addAll(لڪير,"popl %eax","call rt_new_array","pushl %eax");
            } else if (حڪم == 190) Collections.addAll(لڪير,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (حڪم == 196) {
                int واڌ_قدر = حڪم_ڪوائف.한바이트(), ابتدائي = حڪم_ڪوائف.두바이트(); پڙتال_ڪريو_مقامي(ابتدائي,지역수);
                if (واڌ_قدر == 21 || واڌ_قدر == 25 || واڌ_قدر == 54 || واڌ_قدر == 58) لڪير.add((واڌ_قدر <= 25 ? "pushl " : "popl ") + "-" + 4 * (ابتدائي + 1) + "(%ebp)");
                else if (واڌ_قدر == 132) لڪير.add("addl $" + حڪم_ڪوائف.부호두바이트() + ", -" + 4 * (ابتدائي + 1) + "(%ebp)");
                else throw new ترجمو_نقص("wide حڪم 미지원");
            } else if (حڪم == 198 || حڪم == 199) {
                int منزل_مقصود_قدر = 위치 + حڪم_ڪوائف.부호두바이트(); شاخ_فهرست.add(منزل_مقصود_قدر); Collections.addAll(لڪير,"popl %eax","testl %eax, %eax",(حڪم == 198 ? "je " : "jne ") + 표식 + "_b" + منزل_مقصود_قدر);
            } else throw new ترجمو_نقص("미지원 حڪم: " + حڪم);
        }
        if (!경계들.containsAll(شاخ_فهرست)) throw new ترجمو_نقص("حڪم 경계가 아닌 곳으로 شاخ");
        لڪير.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",لڪير);
    }
    String 엑스상수(درجو_ڪوائف ڪوائف, int ابتدائي) {
        if (ڪوائف.상수종류[ابتدائي] == 3) return ڪوائف.لاڳاتار_جزو_ڪوائف[ابتدائي].toString();
        if (ڪوائف.상수종류[ابتدائي] == 8) return اسٽرنگ_نشاني(ڪوائف.문자((Integer)ڪوائف.لاڳاتار_جزو_ڪوائف[ابتدائي]));
        throw new ترجمو_نقص("정수와 اسٽرنگ_قدر 상수만 معاونت_قدر");
    }
    String 엑스조립본(String داخلا_هنڌ, List<String> 내보냄, String هدف) throws IOException {
        Map<String,String> مشين_جدول = new HashMap<>();
        for (String لڪير : Files.readAllLines(ذريعو_راههه.resolve("엑스기계함수.tsv"))) { String[] جوڙو_قدر = لڪير.split("\t"); if (جوڙو_قدر[0].equals(هدف)) مشين_جدول.put(جوڙو_قدر[1] + جوڙو_قدر[2],جوڙو_قدر[3]); }
        int 자리 = داخلا_هنڌ.lastIndexOf('.'); if (자리 < 0) throw new ترجمو_نقص("داخلا_هنڌ 지정 نقص");
        String مالڪ_قدر = داخلا_هنڌ.substring(0,자리).replace('.','/'), طريقو_داخلا_نالو = داخلا_هنڌ.substring(자리 + 1); طريقو_حوالو داخلا_هنڌ_قدر = null;
        for (String 서술 : Arrays.asList("()I","()V")) { طريقو_حوالو حوالو = new طريقو_حوالو(مالڪ_قدر,طريقو_داخلا_نالو,서술); if (함수들.containsKey(حوالو)) { if (داخلا_هنڌ_قدر != null) throw new ترجمو_نقص("겹친 داخلا_هنڌ"); داخلا_هنڌ_قدر = حوالو; } }
        if (داخلا_هنڌ_قدر == null || (함수들.get(داخلا_هنڌ_قدر).پهچ_داخلا & 0x100) != 0) throw new ترجمو_نقص("داخلا_هنڌ_قدر فعل_قدر وضع_قدر نقص");
        List<String> لڪير = new ArrayList<>(); لڪير.add(".code32");
        for (درجو_ڪوائف ڪوائف : 클래스들.values()) {
            String حالت_قدر = نشاني("state",ڪوائف.نالو), شروع_ڪريو = نشاني("init",ڪوائف.نالو);
            Collections.addAll(لڪير,".bss",".balign 4",حالت_قدر + ": .long 0",".text",شروع_ڪريو + ":","cmpl $0, " + حالت_قدر,"jne " + شروع_ڪريو + "_done","movl $1, " + حالت_قدر);
            طريقو_حوالو 초기화참조 = new طريقو_حوالو(ڪوائف.نالو,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) لڪير.add("call " + نشاني("method",초기화참조.부분들()));
            Collections.addAll(لڪير,"movl $2, " + حالت_قدر,شروع_ڪريو + "_done:","ret");
            for (رڪن_ڪوائف قطعه_قدر : ڪوائف.قطعه_قدر) {
                byte[] لاڳاتار_جزو_قدر = قطعه_قدر.منسوب_ڪرڻ_قدر.get("ConstantValue"); String قدر = لاڳاتار_جزو_قدر == null ? "0" : 엑스상수(ڪوائف,new ڪوائف_ريڊر(لاڳاتار_جزو_قدر).두바이트());
                Collections.addAll(لڪير,".data",".balign 4",نشاني("field",ڪوائف.نالو,قطعه_قدر.نالو,قطعه_قدر.서술) + ": .long " + قدر);
            }
            for (رڪن_ڪوائف فعل_قدر : ڪوائف.فعل_قدر) if (!فعل_قدر.نالو.equals("<init>")) لڪير.add(엑스함수본문(new طريقو_حوالو(ڪوائف.نالو,فعل_قدر.نالو,فعل_قدر.서술),فعل_قدر,مشين_جدول,هدف));
        }
        Collections.addAll(لڪير,".text",".globl java_entry","java_entry:","call " + نشاني("init",داخلا_هنڌ_قدر.مالڪ_قدر),"call " + نشاني("method",داخلا_هنڌ_قدر.부분들()));
        if (داخلا_هنڌ_قدر.서술.equals("()V")) لڪير.add("xorl %eax, %eax"); لڪير.add("ret");
        for (String 지정 : 내보냄) {
            int حد_مقرر_ڪرڻ_وارو_قدر = 지정.indexOf('='); if (حد_مقرر_ڪرڻ_وارو_قدر < 1) throw new ترجمو_نقص("내보내기 지정 نقص");
            String 외부 = 지정.substring(0,حد_مقرر_ڪرڻ_وارو_قدر), فعل_قدر = 지정.substring(حد_مقرر_ڪرڻ_وارو_قدر + 1); int 나눔 = فعل_قدر.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ترجمو_نقص("내보내기 نشاني نقص");
            String درجو_قدر = فعل_قدر.substring(0,나눔).replace('.','/'), نالو = فعل_قدر.substring(나눔 + 1); طريقو_حوالو چونڊ_قدر = null;
            for (طريقو_حوالو حوالو : 함수들.keySet()) if (حوالو.مالڪ_قدر.equals(درجو_قدر) && حوالو.نالو.equals(نالو)) { if (چونڊ_قدر != null) throw new ترجمو_نقص("겹친 내보내기 هدف"); چونڊ_قدر = حوالو; }
            if (چونڊ_قدر == null) throw new ترجمو_نقص("내보낼 함수가 없음");
            Collections.addAll(لڪير,".text",".globl " + 외부,외부 + ":","call " + نشاني("init",چونڊ_قدر.مالڪ_قدر),"jmp " + نشاني("method",چونڊ_قدر.부분들()));
        }
        لڪير.add(".section .rodata");
        for (Map.Entry<String,String> داخلا_قدر : 문자열들.entrySet()) {
            Collections.addAll(لڪير,".balign 4",داخلا_قدر.getValue() + ":",".long " + داخلا_قدر.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char سبق_قدر : داخلا_قدر.getKey().toCharArray()) 단위들.add(Integer.toString(سبق_قدر)); if (!단위들.isEmpty()) لڪير.add(".long " + String.join(",",단위들));
        }
        لڪير.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",لڪير) + "\n";
    }
    static void تعميل_ڪرڻ_ٽول(List<String> حڪم) throws Exception {
        if (new ProcessBuilder(حڪم).inheritIO().start().waitFor() != 0) throw new ترجمو_نقص("گڏ_ڪريو_ماخذ نقص: " + حڪم.get(0));
    }
    static String ڪوائف_اسٽرنگ(String متن) { return "\"" + متن.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String هدف, String داخلا_هنڌ, List<String> 내보냄, Path 출력, Path ذريعو_قدر) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), درجو_راههه = 임시.resolve("classes"); Files.createDirectory(درجو_راههه);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",درجو_راههه.toString(),"-sourcepath",درجو_راههه.toString(),"-d",درجو_راههه.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new ترجمو_نقص("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new ترجمو_نقص(".java 또는 .class만 معاونت_قدر");
            }
            if (원문수 > 0) تعميل_ڪرڻ_ٽول(자바명령);
            try (java.util.stream.Stream<Path> راههه_فهرست = Files.walk(درجو_راههه)) { راههه_فهرست.filter(راههه -> راههه.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,هدف.equals("user") ? "user" : "kernel",262144,ذريعو_قدر);
            String 조립 = 변환.엑스조립본(داخلا_هنڌ,내보냄,هدف); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = ذريعو_قدر.getParent();
            تعميل_ڪرڻ_ٽول(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            تعميل_ڪرڻ_ٽول(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("عام_ٻولي_جو_رن_ٽائيم_معاونت.s").toString()));
            List<String> ڪنيڪٽ = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (هدف.equals("kernel")) ڪنيڪٽ.add("-r");
            else {
                تعميل_ڪرڻ_ٽول(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(هدف.equals("user") ? "شروع_صارف_ائپ.s" : "리눅스시작.s").toString()));
                Collections.addAll(ڪنيڪٽ,"-e","_start",임시.resolve("start.o").toString());
                if (هدف.equals("user")) Collections.addAll(ڪنيڪٽ,"-T",도구위치.resolve("صارف_ڪڙي_لي_آئوٽ.ld").toString());
            }
            Collections.addAll(ڪنيڪٽ,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); تعميل_ڪرڻ_ٽول(ڪنيڪٽ);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path چاپيو_قدر = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),چاپيو_قدر,StandardCopyOption.REPLACE_EXISTING); Files.move(چاپيو_قدر,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(چاپيو_قدر); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(هدف.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> نشاني_ڪوائف = new ArrayList<>(), وسيلي_واري_ڊيٽا = new ArrayList<>();
            for (طريقو_حوالو حوالو : 변환.함수들.keySet()) نشاني_ڪوائف.add(ڪوائف_اسٽرنگ(نشاني("method",حوالو.부분들())) + ":" + ڪوائف_اسٽرنگ(حوالو.مالڪ_قدر + "." + حوالو.نالو + حوالو.서술));
            for (Path 입력 : 입력들) {
                byte[] هيش_فائل = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder متن = new StringBuilder(); for (byte قدر : هيش_فائل) متن.append(String.format(Locale.ROOT,"%02x",قدر & 255));
                وسيلي_واري_ڊيٽا.add(ڪوائف_اسٽرنگ(입력.toAbsolutePath().toString()) + ":" + ڪوائف_اسٽرنگ(متن.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + ڪوائف_اسٽرنگ(هدف) + ",\"entry\":" + ڪوائف_اسٽرنگ(داخلا_هنڌ) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",نشاني_ڪوائف) + "},\"sources\":{" + String.join(",",وسيلي_واري_ڊيٽا) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> راههه_فهرست = Files.walk(임시)) { for (Path راههه : (Iterable<Path>)راههه_فهرست.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(راههه); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String داخلا_هنڌ = null, هدف = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> راههه_فهرست = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String قدر = 인수[순번];
                switch (قدر) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry درجو_قدر.فعل_قدر -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export نشاني=درجو_قدر.فعل_قدر] 클래스파일 또는 Java원문"); return;
                    case "--entry": داخلا_هنڌ = 인수[++순번]; break;
                    case "--profile": هدف = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (قدر.startsWith("-")) throw new ترجمو_نقص("알 수 없는 옵션: " + قدر); راههه_فهرست.add(Paths.get(قدر));
                }
            }
            if (داخلا_هنڌ == null || 출력경로 == null || راههه_فهرست.isEmpty()) throw new ترجمو_نقص("--entry, -o, درجو_قدر 파일이 필요합니다");
            Path ذريعو_قدر = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new ترجمو_نقص("알 수 없는 تعميل_ڪرڻ_حڪم هدف");
                엑스번역(راههه_فهرست,엑스대상,داخلا_هنڌ,내보냄,출력경로,ذريعو_قدر); return;
            }
            String ماخذ = new 기계어미리번역(راههه_فهرست, هدف, 낱말수, ذريعو_قدر).생성(داخلا_هنڌ, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ماخذ, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception نقص) { System.err.println("گڏ_ڪريو_ماخذ نقص: " + نقص.getMessage()); System.exit(1); }
    }
}
