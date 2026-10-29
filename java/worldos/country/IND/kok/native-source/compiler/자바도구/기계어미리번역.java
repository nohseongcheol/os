// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java वर्ग_मोल_55654bf1 파일에서 독립 ARM64 커널용 C 원문을 만든다. येजमान JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class अणकार_चूक extends RuntimeException {
        अणकार_चूक(String 설명) { super(설명); }
    }
    static final class डेटा_वाचक {
        final byte[] डेटा;
        int स्थिती;
        डेटा_वाचक(byte[] 입력자료) { डेटा = 입력자료; }
        byte[] 읽기(int लांबाय_मोल) {
            if (लांबाय_मोल < 0 || लांबाय_मोल > डेटा.length - स्थिती) throw new अणकार_चूक("잘린 वर्ग_मोल_55654bf1 또는 आदेश डेटा");
            byte[] मेजप = Arrays.copyOfRange(डेटा, स्थिती, स्थिती + लांबाय_मोल); स्थिती += लांबाय_मोल; return मेजप;
        }
        int 한바이트() { if (स्थिती >= डेटा.length) throw new अणकार_चूक("잘린 आदेश डेटा"); return डेटा[स्थिती++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class वांगडी_डेटा {
        final int ऍक्सॅस_प्रवेश;
        final String नांव, 서술;
        final Map<String, byte[]> खाशेलपण_मोल;
        वांगडी_डेटा(int ऍक्सॅस_मोल, String नांव_मोल, String 서술값, Map<String, byte[]> खाशेलपण_डेटा) {
            ऍक्सॅस_प्रवेश = ऍक्सॅस_मोल; नांव = नांव_मोल; 서술 = 서술값; खाशेलपण_मोल = खाशेलपण_डेटा;
        }
    }
    static final class पद्दत_संदर्भ implements Comparable<पद्दत_संदर्भ> {
        final String धनी_मोल, नांव, 서술;
        पद्दत_संदर्भ(String 소유값, String नांव_मोल, String 서술값) { धनी_मोल = 소유값; नांव = नांव_मोल; 서술 = 서술값; }
        String[] 부분들() { return new String[]{धनी_मोल, नांव, 서술}; }
        public int compareTo(पद्दत_संदर्भ पीयर_मोल) {
            int 비교값 = धनी_मोल.compareTo(पीयर_मोल.धनी_मोल);
            if (비교값 == 0) 비교값 = नांव.compareTo(पीयर_मोल.नांव);
            return 비교값 == 0 ? 서술.compareTo(पीयर_मोल.서술) : 비교값;
        }
        public boolean equals(Object पीयर_मोल) { return पीयर_मोल instanceof पद्दत_संदर्भ && compareTo((पद्दत_संदर्भ) पीयर_मोल) == 0; }
        public int hashCode() { return Objects.hash(धनी_मोल, नांव, 서술); }
    }
    static final class वर्ग_डेटा {
        final int[] 상수종류;
        final Object[] अचल_डेटा;
        final String नांव;
        final List<वांगडी_डेटा> फिल्ड_मोल, फंक्शन_मोल;
        वर्ग_डेटा(Path पाथ) throws IOException {
            डेटा_वाचक वाचक_मोल = new डेटा_वाचक(Files.readAllBytes(पाथ));
            if (वाचक_मोल.네바이트() != 0xcafebabe) throw new अणकार_चूक("Java वर्ग_मोल_55654bf1 표식이 아님");
            वाचक_मोल.읽기(4);
            int आयटम_COUNT = वाचक_मोल.두바이트(); 상수종류 = new int[आयटम_COUNT]; अचल_डेटा = new Object[आयटम_COUNT];
            for (int 순번 = 1; 순번 < आयटम_COUNT; 순번++) {
                int 종류 = वाचक_मोल.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int लांबाय_मोल = वाचक_मोल.두바이트();
                        byte[] वर्ण_बफर = वाचक_मोल.읽기(लांबाय_मोल), 길이붙인자료 = new byte[लांबाय_मोल + 2];
                        길이붙인자료[0] = (byte)(लांबाय_मोल >> 8); 길이붙인자료[1] = (byte)लांबाय_मोल;
                        System.arraycopy(वर्ण_बफर, 0, 길이붙인자료, 2, लांबाय_मोल);
                        अचल_डेटा[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: अचल_डेटा[순번] = वाचक_मोल.네바이트(); break;
                    case 4: वाचक_मोल.읽기(4); break;
                    case 5: case 6: वाचक_मोल.읽기(8); 순번++; break;
                    case 7: case 8: case 16: अचल_डेटा[순번] = वाचक_मोल.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        अचल_डेटा[순번] = new int[]{वाचक_मोल.두바이트(), वाचक_मोल.두바이트()}; break;
                    case 15: अचल_डेटा[순번] = new int[]{वाचक_मोल.한바이트(), वाचक_मोल.두바이트()}; break;
                    default: throw new अणकार_चूक("지원하지 않는 अचल_मोल 종류: " + 종류);
                }
            }
            वाचक_मोल.두바이트(); नांव = वर्ग_नांव(वाचक_मोल.두바이트());
            if (!वर्ग_नांव(वाचक_मोल.두바이트()).equals("java/lang/Object") || वाचक_मोल.두바이트() != 0)
                throw new अणकार_चूक(नांव + ": 상속 및 인터페이스 미지원");
            फिल्ड_मोल = 멤버읽기(वाचक_मोल); फंक्शन_मोल = 멤버읽기(वाचक_मोल); 속성읽기(वाचक_मोल);
            if (वाचक_मोल.स्थिती != वाचक_मोल.डेटा.length) throw new अणकार_चूक("वर्ग_मोल_55654bf1 뒤에 남은 डेटा");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new अणकार_चूक("문자 अचल_मोल INDEX चूक");
            return (String) अचल_डेटा[INDEX];
        }
        String वर्ग_नांव(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new अणकार_चूक("वर्ग_मोल_55654bf1 संदर्भ चूक");
            return 문자((Integer)अचल_डेटा[INDEX]);
        }
        पद्दत_संदर्भ संदर्भ(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new अणकार_चूक("멤버 संदर्भ चूक");
            int[] जोडी_करची_मोल = (int[])अचल_डेटा[INDEX], नांव_जोडी_करची = (int[])अचल_डेटा[जोडी_करची_मोल[1]];
            return new पद्दत_संदर्भ(वर्ग_नांव(जोडी_करची_मोल[0]), 문자(नांव_जोडी_करची[0]), 문자(नांव_जोडी_करची[1]));
        }
        Map<String, byte[]> 속성읽기(डेटा_वाचक वाचक_मोल) {
            Map<String, byte[]> मेजप = new LinkedHashMap<>();
            int आयटम_COUNT = वाचक_मोल.두바이트();
            for (int 순번 = 0; 순번 < आयटम_COUNT; 순번++) {
                String खाशेलपण_नांव = 문자(वाचक_मोल.두바이트()); byte[] मोल = वाचक_मोल.읽기(वाचक_मोल.네바이트());
                if (मेजप.put(खाशेलपण_नांव, मोल) != null) throw new अणकार_चूक("겹친 खाशेलपण_मोल: " + खाशेलपण_नांव);
            }
            return मेजप;
        }
        List<वांगडी_डेटा> 멤버읽기(डेटा_वाचक वाचक_मोल) {
            List<वांगडी_डेटा> मेजप = new ArrayList<>(); int आयटम_COUNT = वाचक_मोल.두바이트();
            for (int 순번 = 0; 순번 < आयटम_COUNT; 순번++) {
                int ऍक्सॅस_प्रवेश = वाचक_मोल.두바이트(); String पद्दत_प्रवेश_नांव = 문자(वाचक_मोल.두바이트()), 서술 = 문자(वाचक_मोल.두바이트());
                मेजप.add(new वांगडी_डेटा(ऍक्सॅस_प्रवेश, पद्दत_प्रवेश_नांव, 서술, 속성읽기(वाचक_मोल)));
            }
            return मेजप;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String return_मेजप;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new अणकार_चूक("फंक्शन_मोल 서술 चूक: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new अणकार_चूक("फंक्शन_मोल 서술 चूक: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new अणकार_चूक("फंक्शन_मोल 서술 चूक: " + 서술);
            return_मेजप = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> मेजप = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int स्थिती = 0; स्थिती < 서술.length();) {
            String निवड_मोल = null;
            for (String स्वरूप_मोल : 허용형식) if (서술.startsWith(स्वरूप_मोल, स्थिती)) { निवड_मोल = स्वरूप_मोल; break; }
            if (निवड_मोल == null) throw new अणकार_चूक("지원하지 않는 डेटा_प्रकार: " + 서술);
            मेजप.add(निवड_मोल); स्थिती += निवड_मोल.length();
        }
        return मेजप;
    }
    static String चिन्न(String 종류, String... 부분들) {
        try {
            byte[] हॅश_फायल = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", हॅश_फायल[순번] & 255));
            return SMS.toString();
        } catch (Exception चूक) { throw new अणकार_चूक(चूक.toString()); }
    }
    final Map<String, वर्ग_डेटा> 클래스들 = new TreeMap<>();
    final Map<पद्दत_संदर्भ, वांगडी_डेटा> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, यंत्र_वर्ग;
    final int 동적기억낱말수;
    final Path साधनसामुग्री_पाथ;
    기계어미리번역(List<Path> पाथ_सुची, String लक्ष्य, int 낱말수, Path साधनसामुग्री_मोल) throws IOException {
        if ((!लक्ष्य.equals("kernel") && !लक्ष्य.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new अणकार_चूक("पाळो_दिवचो_आदेश लक्ष्य 또는 मेमरी_मोल 공간 आवाठ चूक");
        실행대상 = लक्ष्य; 동적기억낱말수 = 낱말수; साधनसामुग्री_पाथ = साधनसामुग्री_मोल;
        // 이 이름도 국가별 स्त्रोत_ट्री तयार_करचें 시 해당 언어로 옮긴다.
        यंत्र_वर्ग = लक्ष्य.equals("kernel") ? "बोर्ड" : "उपेगकर्तो";
        for (String रेग : Files.readAllLines(साधनसामुग्री_मोल.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = रेग.split("\t", -1);
            if (부분들.length != 4) throw new अणकार_चूक("यंत्र फंक्शन_मोल डेटा चूक");
            if (부분들[0].equals(लक्ष्य)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path पाथ : पाथ_सुची) {
            वर्ग_डेटा डेटा = new वर्ग_डेटा(पाथ);
            if (클래스들.put(डेटा.नांव, डेटा) != null) throw new अणकार_चूक("중복 वर्ग_मोल_55654bf1: " + डेटा.नांव);
            for (वांगडी_डेटा फिल्ड_मोल : डेटा.फिल्ड_मोल) {
                if ((फिल्ड_मोल.ऍक्सॅस_प्रवेश & 8) == 0 || 형식읽기(फिल्ड_मोल.서술).equals(Collections.singletonList("V"))) throw new अणकार_चूक("थीर_मोल 필드만 तेंको_मोल");
                if (필드들.put(new पद्दत_संदर्भ(डेटा.नांव, फिल्ड_मोल.नांव, फिल्ड_मोल.서술), फिल्ड_मोल) != null) throw new अणकार_चूक("중복 फिल्ड_मोल");
            }
            for (वांगडी_डेटा फंक्शन_मोल : डेटा.फंक्शन_मोल) {
                if (फंक्शन_मोल.नांव.equals("<init>")) continue;
                if ((फंक्शन_मोल.ऍक्सॅस_प्रवेश & 8) == 0 || (फंक्शन_मोल.ऍक्सॅस_प्रवेश & (0x20 | 0x400)) != 0) throw new अणकार_चूक("थीर_मोल 비동기화 함수만 तेंको_मोल");
                new 함수형식(फंक्शन_मोल.서술);
                if (함수들.put(new पद्दत_संदर्भ(डेटा.नांव, फंक्शन_मोल.नांव, फंक्शन_मोल.서술), फंक्शन_मोल) != null) throw new अणकार_चूक("중복 फंक्शन_मोल");
            }
        }
    }
    String स्ट्रिंग_चिन्न(String SMS) { return 문자열들.computeIfAbsent(SMS, मोल -> "j_text_" + 문자열들.size()); }
    String अचल_ऍक्सप्रॅशन(वर्ग_डेटा डेटा, int INDEX) {
        if (INDEX < 1 || INDEX >= डेटा.상수종류.length) throw new अणकार_चूक("अचल_मोल INDEX क्लिप चूक");
        if (डेटा.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + डेटा.अचल_डेटा[INDEX] + ")";
        if (डेटा.상수종류[INDEX] == 8) return "(word)" + स्ट्रिंग_चिन्न(डेटा.문자((Integer)डेटा.अचल_डेटा[INDEX]));
        throw new अणकार_चूक("정수와 स्ट्रिंग_मोल 상수만 तेंको_मोल");
    }
    String 함수원형(पद्दत_संदर्भ संदर्भ) {
        List<String> 인수들 = new ArrayList<>(); int आयटम_COUNT = new 함수형식(संदर्भ.서술).인수.size();
        for (int 순번 = 0; 순번 < आयटम_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + चिन्न("method", संदर्भ.부분들()) + "(" + (आयटम_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void तपासचें_थळावो(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new अणकार_चूक("थळावो_मळ 변수 INDEX क्लिप चूक"); }
    void 분기넣기(List<String> 출력, Set<Integer> शाखा_सुची, int स्थिती, int 이동량, String स्थिती_291ac971) {
        int नियुक्त_स्थान_मोल = स्थिती + 이동량; शाखा_सुची.add(नियुक्त_स्थान_मोल);
        출력.add((स्थिती_291ac971 == null ? "" : "if (" + स्थिती_291ac971 + ") ") + "goto b" + नियुक्त_स्थान_मोल + ";");
    }
    String 함수본문(पद्दत_संदर्भ फंक्शन_मोल, वांगडी_डेटा डेटा) {
        byte[] 본문자료 = डेटा.खाशेलपण_मोल.get("Code"); if (본문자료 == null) throw new अणकार_चूक("फंक्शन_मोल 몸체가 없음: " + फंक्शन_मोल.नांव);
        डेटा_वाचक वाचक_मोल = new डेटा_वाचक(본문자료); int 쌓임깊이 = वाचक_मोल.두바이트(), 지역변수수 = वाचक_मोल.두바이트();
        डेटा_वाचक आदेश_डेटा = new डेटा_वाचक(वाचक_मोल.읽기(वाचक_मोल.네바이트()));
        if (वाचक_मोल.두바이트() != 0) throw new अणकार_चूक("try/catch/finally 미지원");
        함수형식 स्वरूप_मोल = new 함수형식(फंक्शन_मोल.서술); if (지역변수수 < स्वरूप_मोल.인수.size()) throw new अणकार_चूक("매개변수보다 적은 थळावो_मळ 변수");
        वर्ग_डेटा वर्ग_मोल_55654bf1 = 클래스들.get(फंक्शन_मोल.धनी_मोल);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(फंक्शन_मोल) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < स्वरूप_मोल.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), शाखा_सुची = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (आदेश_डेटा.स्थिती < आदेश_डेटा.डेटा.length) {
            int स्थिती = आदेश_डेटा.स्थिती, आदेश = आदेश_डेटा.한바이트(); 경계들.add(स्थिती); 출력.add("b" + स्थिती + ":;");
            if (आदेश == 0) continue;
            if (आदेश == 1) 출력.add("PUSH(0);");
            else if (आदेश >= 2 && आदेश <= 8) 출력.add("PUSH((uint32_t)(" + (आदेश - 3) + "));");
            else if (आदेश == 16 || आदेश == 17) 출력.add("PUSH((uint32_t)(" + (आदेश == 16 ? आदेश_डेटा.부호한바이트() : आदेश_डेटा.부호두바이트()) + "));");
            else if (आदेश == 18 || आदेश == 19) 출력.add("PUSH(" + अचल_ऍक्सप्रॅशन(वर्ग_मोल_55654bf1, आदेश == 18 ? आदेश_डेटा.한바이트() : आदेश_डेटा.두바이트()) + ");");
            else if (आदेश == 21 || आदेश == 25 || (आदेश >= 26 && आदेश <= 29) || (आदेश >= 42 && आदेश <= 45)) {
                int INDEX = आदेश == 21 || आदेश == 25 ? आदेश_डेटा.한바이트() : आदेश - (आदेश <= 29 ? 26 : 42);
                तपासचें_थळावो(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (आदेश == 54 || आदेश == 58 || (आदेश >= 59 && आदेश <= 62) || (आदेश >= 75 && आदेश <= 78)) {
                int INDEX = आदेश == 54 || आदेश == 58 ? आदेश_डेटा.한바이트() : आदेश - (आदेश <= 62 ? 59 : 75);
                तपासचें_थळावो(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (आदेश == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (आदेश == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (आदेश == 87 || आदेश == 88) 출력.add(आदेश == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (आदेश >= 89 && आदेश <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] क्रम_सुची = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[आदेश - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char मोल : क्रम_सुची[आदेश - 89].toCharArray()) 출력.add("PUSH(" + मोल + ");");
            } else if (आदेश == 96 || आदेश == 100 || आदेश == 104 || आदेश == 126 || आदेश == 128 || आदेश == 130) {
                String क्रिया_मोल = आदेश == 96 ? "+" : आदेश == 100 ? "-" : आदेश == 104 ? "*" : आदेश == 126 ? "&" : आदेश == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + क्रिया_मोल + " (uint32_t)b);");
            } else if (आदेश == 108 || आदेश == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (आदेश == 112 ? 1 : 0) + "));");
            else if (आदेश == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (आदेश == 120 || आदेश == 122 || आदेश == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (आदेश == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (आदेश == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (आदेश == 132) {
                int INDEX = आदेश_डेटा.한바이트(), 증가량 = आदेश_डेटा.부호한바이트(); तपासचें_थळावो(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (आदेश >= 145 && आदेश <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (आदेश == 145 ? "int8_t" : आदेश == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (आदेश >= 153 && आदेश <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, शाखा_सुची, स्थिती, आदेश_डेटा.부호두바이트(), "(int32_t)a " + 비교들[आदेश - 153] + " 0");
            } else if (आदेश >= 159 && आदेश <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, शाखा_सुची, स्थिती, आदेश_डेटा.부호두바이트(), आदेश >= 165 ? "a " + 비교들[आदेश - 159] + " b" : "(int32_t)a " + 비교들[आदेश - 159] + " (int32_t)b");
            } else if (आदेश == 167 || आदेश == 200) 분기넣기(출력, शाखा_सुची, स्थिती, आदेश == 167 ? आदेश_डेटा.부호두바이트() : आदेश_डेटा.네바이트(), null);
            else if (आदेश == 170 || आदेश == 171) {
                while (आदेश_डेटा.स्थिती % 4 != 0) आदेश_डेटा.한바이트();
                int डिफॉल्ट_मोल = आदेश_डेटा.네바이트(); 출력.add("a = POP();");
                if (आदेश == 170) {
                    int 아래 = आदेश_डेटा.네바이트(), 위 = आदेश_डेटा.네바이트(); long आयटम_COUNT = (long)위 - 아래 + 1;
                    if (आयटम_COUNT < 1 || आयटम_COUNT > (आदेश_डेटा.डेटा.length - आदेश_डेटा.स्थिती) / 4) throw new अणकार_चूक("switch क्लिप चूक");
                    for (long मोल = 아래; मोल <= 위; मोल++) 분기넣기(출력, शाखा_सुची, स्थिती, आदेश_डेटा.네바이트(), "(int32_t)a == (" + मोल + ")");
                } else {
                    int आयटम_COUNT = आदेश_डेटा.네바이트(), 앞값 = 0;
                    if (आयटम_COUNT < 0 || आयटम_COUNT > (आदेश_डेटा.डेटा.length - आदेश_डेटा.स्थिती) / 8) throw new अणकार_चूक("switch आवाठ चूक");
                    for (int 순번 = 0; 순번 < आयटम_COUNT; 순번++) {
                        int मोल = आदेश_डेटा.네바이트(); if (순번 > 0 && मोल <= 앞값) throw new अणकार_चूक("switch क्रम_मोल चूक"); 앞값 = मोल;
                        분기넣기(출력, शाखा_सुची, स्थिती, आदेश_डेटा.네바이트(), "(int32_t)a == (" + मोल + ")");
                    }
                }
                분기넣기(출력, शाखा_सुची, स्थिती, डिफॉल्ट_मोल, null);
            } else if (आदेश == 172 || आदेश == 176 || आदेश == 177) 출력.add("return " + (आदेश == 177 ? "0" : "POP()") + ";");
            else if (आदेश == 178 || आदेश == 179) {
                पद्दत_संदर्भ संदर्भ = वर्ग_मोल_55654bf1.संदर्भ(आदेश_डेटा.두바이트()); if (!필드들.containsKey(संदर्भ)) throw new अणकार_चूक("알 수 없는 फिल्ड_मोल");
                출력.add(चिन्न("init", संदर्भ.धनी_मोल) + "();"); String फिल्ड_मोल = चिन्न("field", संदर्भ.부분들());
                출력.add(आदेश == 178 ? "PUSH(" + फिल्ड_मोल + ");" : फिल्ड_मोल + " = POP();");
            } else if (आदेश == 184) {
                पद्दत_संदर्भ संदर्भ = वर्ग_मोल_55654bf1.संदर्भ(आदेश_डेटा.두바이트()); if (!함수들.containsKey(संदर्भ)) throw new अणकार_चूक("알 수 없는 फंक्शन_मोल");
                함수형식 호출형식 = new 함수형식(संदर्भ.서술); int आयटम_COUNT = 호출형식.인수.size();
                출력.add(चिन्न("init", संदर्भ.धनी_मोल) + "();"); 출력.add("if(sp < " + आयटम_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + आयटम_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < आयटम_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + चिन्न("method", संदर्भ.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.return_मेजप.equals("V")) 출력.add("PUSH(a);");
            } else if (आदेश == 182) {
                पद्दत_संदर्भ संदर्भ = वर्ग_मोल_55654bf1.संदर्भ(आदेश_डेटा.두바이트());
                if (संदर्भ.equals(new पद्दत_संदर्भ("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (संदर्भ.equals(new पद्दत_संदर्भ("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new अणकार_चूक("가상 फंक्शन_मोल 호출 미지원");
            } else if (आदेश == 188) {
                if (आदेश_डेटा.한바이트() != 10) throw new अणकार_चूक("new int[]만 तेंको_मोल"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (आदेश == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (आदेश == 196) {
                int विस्तार_मोल = आदेश_डेटा.한바이트(), INDEX = आदेश_डेटा.두바이트(); तपासचें_थळावो(INDEX, 지역변수수);
                if (विस्तार_मोल == 21 || विस्तार_मोल == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (विस्तार_मोल == 54 || विस्तार_मोल == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (विस्तार_मोल == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + आदेश_डेटा.부호두바이트() + ");");
                else throw new अणकार_चूक("미지원 wide आदेश");
            } else if (आदेश == 198 || आदेश == 199) {
                출력.add("a = POP();"); 분기넣기(출력, शाखा_सुची, स्थिती, आदेश_डेटा.부호두바이트(), "a " + (आदेश == 198 ? "==" : "!=") + " 0");
            } else throw new अणकार_चूक(फंक्शन_मोल.धनी_मोल + "." + फंक्शन_मोल.नांव + ", बायट_मोल " + स्थिती + ": 미지원 आदेश " + आदेश);
        }
        if (!경계들.containsAll(शाखा_सुची)) throw new अणकार_चूक("आदेश 경계가 아닌 곳으로 शाखा");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String निर्यात_पद्दत(String लिंक_चिन्न, String लक्ष्य, boolean 진입점여부) {
        int स्थिती_INDEX = लक्ष्य.lastIndexOf('.'); if (स्थिती_INDEX < 0 || !लिंक_चिन्न.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new अणकार_चूक("내보내기 지정 चूक");
        String धनी_मोल = लक्ष्य.substring(0, स्थिती_INDEX).replace('.', '/'), नांव = लक्ष्य.substring(स्थिती_INDEX + 1); पद्दत_संदर्भ निवड_मोल = null;
        for (पद्दत_संदर्भ संदर्भ : 함수들.keySet()) if (संदर्भ.धनी_मोल.equals(धनी_मोल) && संदर्भ.नांव.equals(नांव)) {
            if (निवड_मोल != null) throw new अणकार_चूक("겹친 내보내기 लक्ष्य"); निवड_मोल = संदर्भ;
        }
        if (निवड_मोल == null || (함수들.get(निवड_मोल).ऍक्सॅस_प्रवेश & 0x100) != 0) throw new अणकार_चूक("내보낼 함수가 없음 또는 native फंक्शन_मोल");
        함수형식 स्वरूप_मोल = new 함수형식(निवड_मोल.서술);
        if ((진입점여부 && !स्वरूप_मोल.인수.isEmpty()) || !Arrays.asList("V", "I").contains(स्वरूप_मोल.return_मेजप)) throw new अणकार_चूक("प्रवेश_पॉयंट_मोल 또는 C 경계 स्वरूप_मोल चूक");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < स्वरूप_मोल.인수.size(); 순번++) {
            if (!स्वरूप_मोल.인수.get(순번).equals("I")) throw new अणकार_चूक("C 경계는 int 인수만 तेंको_मोल");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (स्वरूप_मोल.return_मेजप.equals("V") ? "void " : "int32_t ") + लिंक_चिन्न + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + चिन्न("init", निवड_मोल.धनी_मोल) + "(); " + (स्वरूप_मोल.return_मेजप.equals("V") ? "" : "return (int32_t)") + चिन्न("method", निवड_मोल.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String तयार_करचें(String प्रवेश_पॉयंट, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<पद्दत_संदर्भ, वांगडी_डेटा> प्रवेश_मोल : 함수들.entrySet()) {
            पद्दत_संदर्भ संदर्भ = प्रवेश_मोल.getKey(); वांगडी_डेटा डेटा = प्रवेश_मोल.getValue(); 선언들.add(함수원형(संदर्भ) + ";");
            if ((डेटा.ऍक्सॅस_प्रवेश & 0x100) != 0) {
                String कनॅक्ट = 기계함수들.get(संदर्भ.नांव + संदर्भ.서술);
                if (!संदर्भ.धनी_मोल.equals(यंत्र_वर्ग) || कनॅक्ट == null) throw new अणकार_चूक("허용되지 않은 native फंक्शन_मोल: " + संदर्भ.नांव);
                int आयटम_COUNT = new 함수형식(संदर्भ.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < आयटम_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + कनॅक्ट + "(" + (आयटम_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(आयटम_COUNT, "word"))) + ");");
                몸체들.add(함수원형(संदर्भ) + " { return " + कनॅक्ट + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(संदर्भ, डेटा));
        }
        for (Map.Entry<पद्दत_संदर्भ, वांगडी_डेटा> प्रवेश_मोल : 필드들.entrySet()) {
            पद्दत_संदर्भ संदर्भ = प्रवेश_मोल.getKey(); byte[] अचल_मोल = प्रवेश_मोल.getValue().खाशेलपण_मोल.get("ConstantValue");
            String मोल = अचल_मोल == null ? "0" : अचल_ऍक्सप्रॅशन(클래스들.get(संदर्भ.धनी_मोल), new डेटा_वाचक(अचल_मोल).두바이트());
            필드선언들.add("static word " + चिन्न("field", संदर्भ.부분들()) + " = " + मोल + ";");
        }
        for (String नांव : 클래스들.keySet()) {
            String प्रारंभ_करचें = चिन्न("init", नांव), स्थिती_मोल_e10195a1 = चिन्न("state", नांव);
            선언들.add("static void " + प्रारंभ_करचें + "(void);"); 필드선언들.add("static unsigned " + स्थिती_मोल_e10195a1 + ";");
            पद्दत_संदर्भ संदर्भ = new पद्दत_संदर्भ(नांव, "<clinit>", "()V");
            몸체들.add("static void " + प्रारंभ_करचें + "(void) { if(" + स्थिती_मोल_e10195a1 + ") return; " + स्थिती_मोल_e10195a1 + " = 1; " + (함수들.containsKey(संदर्भ) ? चिन्न("method", संदर्भ.부분들()) + "(); " : "") + स्थिती_मोल_e10195a1 + " = 2; }");
        }
        몸체들.add(निर्यात_पद्दत("java_entry", प्रवेश_पॉयंट, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int स्थिती_INDEX = 지정.indexOf('='); if (स्थिती_INDEX < 1) throw new अणकार_चूक("내보내기 지정 चूक");
            String नांव = 지정.substring(0, स्थिती_INDEX); 공개이름.add(नांव); 몸체들.add(निर्यात_पद्दत(नांव, 지정.substring(स्थिती_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> प्रवेश_मोल : 문자열들.entrySet()) {
            String SMS = प्रवेश_मोल.getKey(); StringBuilder क्रम_मोल_ed437109 = new StringBuilder("static const word " + प्रवेश_मोल.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) क्रम_मोल_ed437109.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(क्रम_मोल_ed437109.append("};").toString());
        }
        String तेंको_मोल = Files.readString(साधनसामुग्री_पाथ.resolve("सामान्य_भास_रनटायम_तेंको.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(तेंको_मोल + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String स्त्रोत, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> नांव_तकटो = new HashMap<>();
        for (String रेग : Files.readAllLines(साधनसामुग्री_पाथ.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] जोडी_करची_मोल = रेग.split("\t"); नांव_तकटो.put(जोडी_करची_मोल[0], जोडी_करची_मोल[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(स्त्रोत); StringBuffer मेजप = new StringBuffer();
        while (찾개.find()) {
            String नांव = 찾개.group(), 새이름 = नांव;
            if (!नांव.startsWith("//") && !नांव.startsWith("/*") && !नांव.startsWith("\"") && !नांव.startsWith("'") && !공개이름.contains(नांव)) {
                새이름 = नांव_तकटो.getOrDefault(नांव, नांव);
                if (नांव.matches("a[0-9]+")) 새이름 = "인수" + नांव.substring(1);
                if (नांव.matches("b[0-9]+")) 새이름 = "शाखा" + नांव.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char वर्ण_मोल : 새이름.toCharArray()) 표기.append(वर्ण_मोल < 128 ? Character.toString(वर्ण_मोल) : String.format(Locale.ROOT, "\\u%04x", (int)वर्ण_मोल));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(मेजप, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(मेजप); return मेजप.toString();
    }
    String 엑스함수본문(पद्दत_संदर्भ फंक्शन_मोल, वांगडी_डेटा डेटा, Map<String,String> यंत्र_तकटो, String लक्ष्य) {
        String 표식 = चिन्न("method", फंक्शन_मोल.부분들());
        List<String> रेग = new ArrayList<>();
        if ((डेटा.ऍक्सॅस_प्रवेश & 0x100) != 0) {
            String कनॅक्ट = यंत्र_तकटो.get(फंक्शन_मोल.नांव + फंक्शन_मोल.서술);
            if (!फंक्शन_मोल.धनी_मोल.equals(लक्ष्य.equals("kernel") ? "मोबायल_मोल" : "उपेगकर्तो") || कनॅक्ट == null) throw new अणकार_चूक("허용되지 않은 native फंक्शन_मोल");
            return ".text\n" + 표식 + ":\njmp " + कनॅक्ट;
        }
        byte[] देखीचो_उतारो = डेटा.खाशेलपण_मोल.get("Code"); if (देखीचो_उतारो == null) throw new अणकार_चूक("फंक्शन_मोल 몸체가 없음");
        डेटा_वाचक वाचक_मोल = new डेटा_वाचक(देखीचो_उतारो); वाचक_मोल.두바이트(); int थळावो_COUNT = वाचक_मोल.두바이트();
        डेटा_वाचक आदेश_डेटा = new डेटा_वाचक(वाचक_मोल.읽기(वाचक_मोल.네바이트()));
        if (वाचक_मोल.두바이트() != 0) throw new अणकार_चूक("try/catch/finally 미지원");
        함수형식 स्वरूप_मोल = new 함수형식(फंक्शन_मोल.서술); if (थळावो_COUNT < स्वरूप_मोल.인수.size()) throw new अणकार_चूक("매개변수보다 적은 थळावो_मळ 변수");
        Collections.addAll(रेग,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + थळावो_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < स्वरूप_मोल.인수.size(); 순번++) Collections.addAll(रेग,"movl " + (8 + 4 * (स्वरूप_मोल.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        वर्ग_डेटा वर्ग_मोल_55654bf1 = 클래스들.get(फंक्शन_मोल.धनी_मोल); Set<Integer> 경계들 = new HashSet<>(), शाखा_सुची = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (आदेश_डेटा.स्थिती < आदेश_डेटा.डेटा.length) {
            int स्थिती = आदेश_डेटा.स्थिती, आदेश = आदेश_डेटा.한바이트(); String स्थिती_INDEX = 표식 + "_b" + स्थिती;
            रेग.add(स्थिती_INDEX + ":"); 경계들.add(स्थिती);
            if (आदेश == 0) रेग.add("nop");
            else if (आदेश == 1) रेग.add("pushl $0");
            else if (आदेश >= 2 && आदेश <= 8) रेग.add("pushl $" + (आदेश - 3));
            else if (आदेश == 16 || आदेश == 17) रेग.add("pushl $" + (आदेश == 16 ? आदेश_डेटा.부호한바이트() : आदेश_डेटा.부호두바이트()));
            else if (आदेश == 18 || आदेश == 19) {
                int INDEX = आदेश == 18 ? आदेश_डेटा.한바이트() : आदेश_डेटा.두바이트();
                रेग.add("pushl $" + 엑스상수(वर्ग_मोल_55654bf1,INDEX));
            } else if (आदेश == 21 || आदेश == 25 || (आदेश >= 26 && आदेश <= 29) || (आदेश >= 42 && आदेश <= 45) || आदेश == 54 || आदेश == 58 || (आदेश >= 59 && आदेश <= 62) || (आदेश >= 75 && आदेश <= 78)) {
                boolean 읽음 = आदेश < 54; int INDEX = आदेश == 21 || आदेश == 25 || आदेश == 54 || आदेश == 58 ? आदेश_डेटा.한바이트() : आदेश - (आदेश <= 29 ? 26 : आदेश <= 45 ? 42 : आदेश <= 62 ? 59 : 75);
                तपासचें_थळावो(INDEX,थळावो_COUNT); रेग.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (आदेश == 46) Collections.addAll(रेग,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (आदेश == 79) Collections.addAll(रेग,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (आदेश == 87 || आदेश == 88) रेग.add("addl $" + (आदेश == 87 ? 4 : 8) + ", %esp");
            else if (आदेश >= 89 && आदेश <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] क्रम_सुची = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[आदेश - 89]; 순번++) रेग.add("popl " + 저장기들[순번]);
                for (int 순번 : क्रम_सुची[आदेश - 89]) रेग.add("pushl " + 저장기들[순번]);
            } else if (आदेश == 96 || आदेश == 100 || आदेश == 104 || आदेश == 126 || आदेश == 128 || आदेश == 130) {
                String क्रिया_मोल = आदेश == 96 ? "addl" : आदेश == 100 ? "subl" : आदेश == 104 ? "imull" : आदेश == 126 ? "andl" : आदेश == 128 ? "orl" : "xorl";
                Collections.addAll(रेग,"popl %ecx","popl %eax",क्रिया_मोल + " %ecx, %eax","pushl %eax");
            } else if (आदेश == 108 || आदेश == 112) Collections.addAll(रेग,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + स्थिती_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + स्थिती_INDEX + "_divide","xorl %edx, %edx","jmp " + स्थिती_INDEX + "_done",स्थिती_INDEX + "_divide:","cltd","idivl %ecx",स्थिती_INDEX + "_done:","pushl " + (आदेश == 108 ? "%eax" : "%edx"));
            else if (आदेश == 116) रेग.add("negl (%esp)");
            else if (आदेश == 120 || आदेश == 122 || आदेश == 124) Collections.addAll(रेग,"popl %ecx","popl %eax",(आदेश == 120 ? "sall" : आदेश == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (आदेश == 132) {
                int INDEX = आदेश_डेटा.한바이트(), 증가 = आदेश_डेटा.부호한바이트(); तपासचें_थळावो(INDEX,थळावो_COUNT); रेग.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (आदेश >= 145 && आदेश <= 147) Collections.addAll(रेग,"popl %eax",आदेश == 145 ? "movsbl %al, %eax" : आदेश == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (आदेश >= 153 && आदेश <= 166) {
                if (आदेश <= 158) Collections.addAll(रेग,"popl %eax","testl %eax, %eax");
                else Collections.addAll(रेग,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int नियुक्त_स्थान_मोल = स्थिती + आदेश_डेटा.부호두바이트(); शाखा_सुची.add(नियुक्त_स्थान_मोल); रेग.add(비교들[आदेश - (आदेश <= 158 ? 153 : 159)] + " " + 표식 + "_b" + नियुक्त_स्थान_मोल);
            } else if (आदेश == 167 || आदेश == 200) {
                int नियुक्त_स्थान_मोल = स्थिती + (आदेश == 167 ? आदेश_डेटा.부호두바이트() : आदेश_डेटा.네바이트()); शाखा_सुची.add(नियुक्त_स्थान_मोल); रेग.add("jmp " + 표식 + "_b" + नियुक्त_स्थान_मोल);
            } else if (आदेश == 170 || आदेश == 171) {
                while (आदेश_डेटा.स्थिती % 4 != 0) आदेश_डेटा.한바이트();
                int डिफॉल्ट_मोल = स्थिती + आदेश_डेटा.네바이트(); शाखा_सुची.add(डिफॉल्ट_मोल); रेग.add("popl %eax");
                int आयटम_COUNT, 아래 = 0;
                if (आदेश == 170) { 아래 = आदेश_डेटा.네바이트(); int 위 = आदेश_डेटा.네바이트(); long लांबाय_मोल = (long)위 - 아래 + 1; if (लांबाय_मोल < 1 || लांबाय_मोल > (आदेश_डेटा.डेटा.length - आदेश_डेटा.स्थिती) / 4) throw new अणकार_चूक("switch क्लिप चूक"); आयटम_COUNT = (int)लांबाय_मोल; }
                else { आयटम_COUNT = आदेश_डेटा.네바이트(); if (आयटम_COUNT < 0 || आयटम_COUNT > (आदेश_डेटा.डेटा.length - आदेश_डेटा.स्थिती) / 8) throw new अणकार_चूक("switch आवाठ चूक"); }
                for (int 순번 = 0; 순번 < आयटम_COUNT; 순번++) {
                    int मोल = आदेश == 170 ? 아래 + 순번 : आदेश_डेटा.네바이트(), नियुक्त_स्थान_मोल = स्थिती + आदेश_डेटा.네바이트(); शाखा_सुची.add(नियुक्त_स्थान_मोल);
                    Collections.addAll(रेग,"cmpl $" + मोल + ", %eax","je " + 표식 + "_b" + नियुक्त_स्थान_मोल);
                }
                रेग.add("jmp " + 표식 + "_b" + डिफॉल्ट_मोल);
            } else if (आदेश == 172 || आदेश == 176 || आदेश == 177) {
                if (आदेश != 177) रेग.add("popl %eax"); Collections.addAll(रेग,"leave","ret");
            } else if (आदेश == 178 || आदेश == 179) {
                पद्दत_संदर्भ संदर्भ = वर्ग_मोल_55654bf1.संदर्भ(आदेश_डेटा.두바이트()); if (!필드들.containsKey(संदर्भ)) throw new अणकार_चूक("알 수 없는 फिल्ड_मोल");
                Collections.addAll(रेग,"call " + चिन्न("init",संदर्भ.धनी_मोल),(आदेश == 178 ? "pushl " : "popl ") + चिन्न("field",संदर्भ.부분들()));
            } else if (आदेश == 184) {
                पद्दत_संदर्भ संदर्भ = वर्ग_मोल_55654bf1.संदर्भ(आदेश_डेटा.두바이트()); if (!함수들.containsKey(संदर्भ)) throw new अणकार_चूक("알 수 없는 फंक्शन_मोल");
                함수형식 호출형식 = new 함수형식(संदर्भ.서술); Collections.addAll(रेग,"call " + चिन्न("init",संदर्भ.धनी_मोल),"call " + चिन्न("method",संदर्भ.부분들()));
                if (!호출형식.인수.isEmpty()) रेग.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.return_मेजप.equals("V")) रेग.add("pushl %eax");
            } else if (आदेश == 182) {
                पद्दत_संदर्भ संदर्भ = वर्ग_मोल_55654bf1.संदर्भ(आदेश_डेटा.두바이트());
                if (संदर्भ.equals(new पद्दत_संदर्भ("java/lang/String","length","()I"))) Collections.addAll(रेग,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (संदर्भ.equals(new पद्दत_संदर्भ("java/lang/String","charAt","(I)C"))) Collections.addAll(रेग,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new अणकार_चूक("가상 फंक्शन_मोल 호출 미지원");
            } else if (आदेश == 188) {
                if (आदेश_डेटा.한바이트() != 10) throw new अणकार_चूक("new int[]만 तेंको_मोल"); Collections.addAll(रेग,"popl %eax","call rt_new_array","pushl %eax");
            } else if (आदेश == 190) Collections.addAll(रेग,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (आदेश == 196) {
                int विस्तार_मोल = आदेश_डेटा.한바이트(), INDEX = आदेश_डेटा.두바이트(); तपासचें_थळावो(INDEX,थळावो_COUNT);
                if (विस्तार_मोल == 21 || विस्तार_मोल == 25 || विस्तार_मोल == 54 || विस्तार_मोल == 58) रेग.add((विस्तार_मोल <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (विस्तार_मोल == 132) रेग.add("addl $" + आदेश_डेटा.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new अणकार_चूक("wide आदेश 미지원");
            } else if (आदेश == 198 || आदेश == 199) {
                int नियुक्त_स्थान_मोल = स्थिती + आदेश_डेटा.부호두바이트(); शाखा_सुची.add(नियुक्त_स्थान_मोल); Collections.addAll(रेग,"popl %eax","testl %eax, %eax",(आदेश == 198 ? "je " : "jne ") + 표식 + "_b" + नियुक्त_स्थान_मोल);
            } else throw new अणकार_चूक("미지원 आदेश: " + आदेश);
        }
        if (!경계들.containsAll(शाखा_सुची)) throw new अणकार_चूक("आदेश 경계가 아닌 곳으로 शाखा");
        रेग.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",रेग);
    }
    String 엑스상수(वर्ग_डेटा डेटा, int INDEX) {
        if (डेटा.상수종류[INDEX] == 3) return डेटा.अचल_डेटा[INDEX].toString();
        if (डेटा.상수종류[INDEX] == 8) return स्ट्रिंग_चिन्न(डेटा.문자((Integer)डेटा.अचल_डेटा[INDEX]));
        throw new अणकार_चूक("정수와 स्ट्रिंग_मोल 상수만 तेंको_मोल");
    }
    String 엑스조립본(String प्रवेश_पॉयंट, List<String> 내보냄, String लक्ष्य) throws IOException {
        Map<String,String> यंत्र_तकटो = new HashMap<>();
        for (String रेग : Files.readAllLines(साधनसामुग्री_पाथ.resolve("엑스기계함수.tsv"))) { String[] जोडी_करची_मोल = रेग.split("\t"); if (जोडी_करची_मोल[0].equals(लक्ष्य)) यंत्र_तकटो.put(जोडी_करची_मोल[1] + जोडी_करची_मोल[2],जोडी_करची_मोल[3]); }
        int स्थिती_INDEX = प्रवेश_पॉयंट.lastIndexOf('.'); if (स्थिती_INDEX < 0) throw new अणकार_चूक("प्रवेश_पॉयंट 지정 चूक");
        String धनी_मोल = प्रवेश_पॉयंट.substring(0,स्थिती_INDEX).replace('.','/'), पद्दत_प्रवेश_नांव = प्रवेश_पॉयंट.substring(स्थिती_INDEX + 1); पद्दत_संदर्भ प्रवेश_पॉयंट_मोल = null;
        for (String 서술 : Arrays.asList("()I","()V")) { पद्दत_संदर्भ संदर्भ = new पद्दत_संदर्भ(धनी_मोल,पद्दत_प्रवेश_नांव,서술); if (함수들.containsKey(संदर्भ)) { if (प्रवेश_पॉयंट_मोल != null) throw new अणकार_चूक("겹친 प्रवेश_पॉयंट"); प्रवेश_पॉयंट_मोल = संदर्भ; } }
        if (प्रवेश_पॉयंट_मोल == null || (함수들.get(प्रवेश_पॉयंट_मोल).ऍक्सॅस_प्रवेश & 0x100) != 0) throw new अणकार_चूक("प्रवेश_पॉयंट_मोल फंक्शन_मोल स्वरूप_मोल चूक");
        List<String> रेग = new ArrayList<>(); रेग.add(".code32");
        for (वर्ग_डेटा डेटा : 클래스들.values()) {
            String स्थिती_मोल_e10195a1 = चिन्न("state",डेटा.नांव), प्रारंभ_करचें = चिन्न("init",डेटा.नांव);
            Collections.addAll(रेग,".bss",".balign 4",स्थिती_मोल_e10195a1 + ": .long 0",".text",प्रारंभ_करचें + ":","cmpl $0, " + स्थिती_मोल_e10195a1,"jne " + प्रारंभ_करचें + "_done","movl $1, " + स्थिती_मोल_e10195a1);
            पद्दत_संदर्भ 초기화참조 = new पद्दत_संदर्भ(डेटा.नांव,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) रेग.add("call " + चिन्न("method",초기화참조.부분들()));
            Collections.addAll(रेग,"movl $2, " + स्थिती_मोल_e10195a1,प्रारंभ_करचें + "_done:","ret");
            for (वांगडी_डेटा फिल्ड_मोल : डेटा.फिल्ड_मोल) {
                byte[] अचल_मोल = फिल्ड_मोल.खाशेलपण_मोल.get("ConstantValue"); String मोल = अचल_मोल == null ? "0" : 엑스상수(डेटा,new डेटा_वाचक(अचल_मोल).두바이트());
                Collections.addAll(रेग,".data",".balign 4",चिन्न("field",डेटा.नांव,फिल्ड_मोल.नांव,फिल्ड_मोल.서술) + ": .long " + मोल);
            }
            for (वांगडी_डेटा फंक्शन_मोल : डेटा.फंक्शन_मोल) if (!फंक्शन_मोल.नांव.equals("<init>")) रेग.add(엑스함수본문(new पद्दत_संदर्भ(डेटा.नांव,फंक्शन_मोल.नांव,फंक्शन_मोल.서술),फंक्शन_मोल,यंत्र_तकटो,लक्ष्य));
        }
        Collections.addAll(रेग,".text",".globl java_entry","java_entry:","call " + चिन्न("init",प्रवेश_पॉयंट_मोल.धनी_मोल),"call " + चिन्न("method",प्रवेश_पॉयंट_मोल.부분들()));
        if (प्रवेश_पॉयंट_मोल.서술.equals("()V")) रेग.add("xorl %eax, %eax"); रेग.add("ret");
        for (String 지정 : 내보냄) {
            int डिलिमिटर_मोल = 지정.indexOf('='); if (डिलिमिटर_मोल < 1) throw new अणकार_चूक("내보내기 지정 चूक");
            String 외부 = 지정.substring(0,डिलिमिटर_मोल), फंक्शन_मोल = 지정.substring(डिलिमिटर_मोल + 1); int भागाकार_मेजप = फंक्शन_मोल.lastIndexOf('.');
            if (भागाकार_मेजप < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new अणकार_चूक("내보내기 चिन्न चूक");
            String वर्ग_मोल_55654bf1 = फंक्शन_मोल.substring(0,भागाकार_मेजप).replace('.','/'), नांव = फंक्शन_मोल.substring(भागाकार_मेजप + 1); पद्दत_संदर्भ निवड_मोल = null;
            for (पद्दत_संदर्भ संदर्भ : 함수들.keySet()) if (संदर्भ.धनी_मोल.equals(वर्ग_मोल_55654bf1) && संदर्भ.नांव.equals(नांव)) { if (निवड_मोल != null) throw new अणकार_चूक("겹친 내보내기 लक्ष्य"); निवड_मोल = संदर्भ; }
            if (निवड_मोल == null) throw new अणकार_चूक("내보낼 함수가 없음");
            Collections.addAll(रेग,".text",".globl " + 외부,외부 + ":","call " + चिन्न("init",निवड_मोल.धनी_मोल),"jmp " + चिन्न("method",निवड_मोल.부분들()));
        }
        रेग.add(".section .rodata");
        for (Map.Entry<String,String> प्रवेश_मोल : 문자열들.entrySet()) {
            Collections.addAll(रेग,".balign 4",प्रवेश_मोल.getValue() + ":",".long " + प्रवेश_मोल.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char एकक_मोल : प्रवेश_मोल.getKey().toCharArray()) 단위들.add(Integer.toString(एकक_मोल)); if (!단위들.isEmpty()) रेग.add(".long " + String.join(",",단위들));
        }
        रेग.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",रेग) + "\n";
    }
    static void पाळो_दिवचो_साधन(List<String> आदेश) throws Exception {
        if (new ProcessBuilder(आदेश).inheritIO().start().waitFor() != 0) throw new अणकार_चूक("दाळचे_स्त्रोत चूक: " + आदेश.get(0));
    }
    static String डेटा_स्ट्रिंग(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String लक्ष्य, String प्रवेश_पॉयंट, List<String> 내보냄, Path 출력, Path साधनसामुग्री_मोल) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), वर्ग_पाथ = 임시.resolve("classes"); Files.createDirectory(वर्ग_पाथ);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",वर्ग_पाथ.toString(),"-sourcepath",वर्ग_पाथ.toString(),"-d",वर्ग_पाथ.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int स्त्रोत_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new अणकार_चूक("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); स्त्रोत_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new अणकार_चूक(".java 또는 .class만 तेंको_मोल");
            }
            if (स्त्रोत_COUNT > 0) पाळो_दिवचो_साधन(자바명령);
            try (java.util.stream.Stream<Path> पाथ_सुची = Files.walk(वर्ग_पाथ)) { पाथ_सुची.filter(पाथ -> पाथ.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_मोल = new 기계어미리번역(바이트코드,लक्ष्य.equals("user") ? "user" : "kernel",262144,साधनसामुग्री_मोल);
            String 조립 = CONVERT_मोल.엑스조립본(प्रवेश_पॉयंट,내보냄,लक्ष्य); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path साधन_स्थिती = साधनसामुग्री_मोल.getParent();
            पाळो_दिवचो_साधन(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            पाळो_दिवचो_साधन(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),साधन_स्थिती.resolve("सामान्य_भास_रनटायम_तेंको.s").toString()));
            List<String> कनॅक्ट = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (लक्ष्य.equals("kernel")) कनॅक्ट.add("-r");
            else {
                पाळो_दिवचो_साधन(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),साधन_स्थिती.resolve(लक्ष्य.equals("user") ? "Start_उपेगकर्तो_एप्लिकेशन.s" : "리눅스시작.s").toString()));
                Collections.addAll(कनॅक्ट,"-e","_start",임시.resolve("start.o").toString());
                if (लक्ष्य.equals("user")) Collections.addAll(कनॅक्ट,"-T",साधन_स्थिती.resolve("उपेगकर्तो_लिंक_रचणाय.ld").toString());
            }
            Collections.addAll(कनॅक्ट,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); पाळो_दिवचो_साधन(कनॅक्ट);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path उजवाडावचें_मोल = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),उजवाडावचें_मोल,StandardCopyOption.REPLACE_EXISTING); Files.move(उजवाडावचें_मोल,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(उजवाडावचें_मोल); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(लक्ष्य.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> चिन्न_डेटा = new ArrayList<>(), स्त्रोत_डेटा = new ArrayList<>();
            for (पद्दत_संदर्भ संदर्भ : CONVERT_मोल.함수들.keySet()) चिन्न_डेटा.add(डेटा_स्ट्रिंग(चिन्न("method",संदर्भ.부분들())) + ":" + डेटा_स्ट्रिंग(संदर्भ.धनी_मोल + "." + संदर्भ.नांव + संदर्भ.서술));
            for (Path 입력 : 입력들) {
                byte[] हॅश_फायल = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte मोल : हॅश_फायल) SMS.append(String.format(Locale.ROOT,"%02x",मोल & 255));
                स्त्रोत_डेटा.add(डेटा_स्ट्रिंग(입력.toAbsolutePath().toString()) + ":" + डेटा_स्ट्रिंग(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + डेटा_स्ट्रिंग(लक्ष्य) + ",\"entry\":" + डेटा_स्ट्रिंग(प्रवेश_पॉयंट) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",चिन्न_डेटा) + "},\"sources\":{" + String.join(",",स्त्रोत_डेटा) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> पाथ_सुची = Files.walk(임시)) { for (Path पाथ : (Iterable<Path>)पाथ_सुची.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(पाथ); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String प्रवेश_पॉयंट = null, लक्ष्य = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> पाथ_सुची = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String मोल = 인수[순번];
                switch (मोल) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry वर्ग_मोल_55654bf1.फंक्शन_मोल -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export चिन्न=वर्ग_मोल_55654bf1.फंक्शन_मोल] 클래스파일 또는 Java원문"); return;
                    case "--entry": प्रवेश_पॉयंट = 인수[++순번]; break;
                    case "--profile": लक्ष्य = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (मोल.startsWith("-")) throw new अणकार_चूक("알 수 없는 옵션: " + मोल); पाथ_सुची.add(Paths.get(मोल));
                }
            }
            if (प्रवेश_पॉयंट == null || 출력경로 == null || पाथ_सुची.isEmpty()) throw new अणकार_चूक("--entry, -o, वर्ग_मोल_55654bf1 파일이 필요합니다");
            Path साधनसामुग्री_मोल = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new अणकार_चूक("알 수 없는 पाळो_दिवचो_आदेश लक्ष्य");
                엑스번역(पाथ_सुची,엑스대상,प्रवेश_पॉयंट,내보냄,출력경로,साधनसामुग्री_मोल); return;
            }
            String स्त्रोत = new 기계어미리번역(पाथ_सुची, लक्ष्य, 낱말수, साधनसामुग्री_मोल).तयार_करचें(प्रवेश_पॉयंट, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, स्त्रोत, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception चूक) { System.err.println("दाळचे_स्त्रोत चूक: " + चूक.getMessage()); System.exit(1); }
    }
}
