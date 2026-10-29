// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java መደብ_እሴት 파일에서 독립 ARM64 커널용 C 원문을 만든다. አዘጋጅ_b78e430d JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class ትርጉም_ስህተት extends RuntimeException {
        ትርጉም_ስህተት(String 설명) { super(설명); }
    }
    static final class ውሂብ_አንባቢ {
        final byte[] ውሂብ;
        int አካባቢ;
        ውሂብ_አንባቢ(byte[] 입력자료) { ውሂብ = 입력자료; }
        byte[] ማንበቢያ(int ርዝመት_እሴት) {
            if (ርዝመት_እሴት < 0 || ርዝመት_እሴት > ውሂብ.length - አካባቢ) throw new ትርጉም_ስህተት("잘린 መደብ_እሴት 또는 ትእዛዝ ውሂብ");
            byte[] ልኬት = Arrays.copyOfRange(ውሂብ, አካባቢ, አካባቢ + ርዝመት_እሴት); አካባቢ += ርዝመት_እሴት; return ልኬት;
        }
        int 한바이트() { if (አካባቢ >= ውሂብ.length) throw new ትርጉም_ስህተት("잘린 ትእዛዝ ውሂብ"); return ውሂብ[አካባቢ++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class አባል_ውሂብ {
        final int መዳረሻ_ምዝግብ;
        final String ስም, 서술;
        final Map<String, byte[]> ዓይነታ_እሴት;
        አባል_ውሂብ(int መዳረሻ_እሴት, String ስም_እሴት, String 서술값, Map<String, byte[]> ዓይነታ_ውሂብ) {
            መዳረሻ_ምዝግብ = መዳረሻ_እሴት; ስም = ስም_እሴት; 서술 = 서술값; ዓይነታ_እሴት = ዓይነታ_ውሂብ;
        }
    }
    static final class ስልት_ማጣቀሻ implements Comparable<ስልት_ማጣቀሻ> {
        final String ባለቤት_እሴት, ስም, 서술;
        ስልት_ማጣቀሻ(String 소유값, String ስም_እሴት, String 서술값) { ባለቤት_እሴት = 소유값; ስም = ስም_እሴት; 서술 = 서술값; }
        String[] 부분들() { return new String[]{ባለቤት_እሴት, ስም, 서술}; }
        public int compareTo(ስልት_ማጣቀሻ አቻ_እሴት) {
            int ንጽጽር_እሴት = ባለቤት_እሴት.compareTo(አቻ_እሴት.ባለቤት_እሴት);
            if (ንጽጽር_እሴት == 0) ንጽጽር_እሴት = ስም.compareTo(አቻ_እሴት.ስም);
            return ንጽጽር_እሴት == 0 ? 서술.compareTo(አቻ_እሴት.서술) : ንጽጽር_እሴት;
        }
        public boolean equals(Object አቻ_እሴት) { return አቻ_እሴት instanceof ስልት_ማጣቀሻ && compareTo((ስልት_ማጣቀሻ) አቻ_እሴት) == 0; }
        public int hashCode() { return Objects.hash(ባለቤት_እሴት, ስም, 서술); }
    }
    static final class መደብ_ውሂብ {
        final int[] 상수종류;
        final Object[] ቋሚ_ውሂብ;
        final String ስም;
        final List<አባል_ውሂብ> መስክ_እሴት, ተግባር_እሴት;
        መደብ_ውሂብ(Path መተላለፊያ) throws IOException {
            ውሂብ_አንባቢ አንባቢ_እሴት = new ውሂብ_አንባቢ(Files.readAllBytes(መተላለፊያ));
            if (አንባቢ_እሴት.네바이트() != 0xcafebabe) throw new ትርጉም_ስህተት("Java መደብ_እሴት 표식이 아님");
            አንባቢ_እሴት.ማንበቢያ(4);
            int 개수 = አንባቢ_እሴት.두바이트(); 상수종류 = new int[개수]; ቋሚ_ውሂብ = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = አንባቢ_እሴት.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int ርዝመት_እሴት = አንባቢ_እሴት.두바이트();
                        byte[] ቁምፊ_ቋት = አንባቢ_እሴት.ማንበቢያ(ርዝመት_እሴት), 길이붙인자료 = new byte[ርዝመት_እሴት + 2];
                        길이붙인자료[0] = (byte)(ርዝመት_እሴት >> 8); 길이붙인자료[1] = (byte)ርዝመት_እሴት;
                        System.arraycopy(ቁምፊ_ቋት, 0, 길이붙인자료, 2, ርዝመት_እሴት);
                        ቋሚ_ውሂብ[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: ቋሚ_ውሂብ[순번] = አንባቢ_እሴት.네바이트(); break;
                    case 4: አንባቢ_እሴት.ማንበቢያ(4); break;
                    case 5: case 6: አንባቢ_እሴት.ማንበቢያ(8); 순번++; break;
                    case 7: case 8: case 16: ቋሚ_ውሂብ[순번] = አንባቢ_እሴት.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        ቋሚ_ውሂብ[순번] = new int[]{አንባቢ_እሴት.두바이트(), አንባቢ_እሴት.두바이트()}; break;
                    case 15: ቋሚ_ውሂብ[순번] = new int[]{አንባቢ_እሴት.한바이트(), አንባቢ_እሴት.두바이트()}; break;
                    default: throw new ትርጉም_ስህተት("지원하지 않는 ቋሚ_እሴት 종류: " + 종류);
                }
            }
            አንባቢ_እሴት.두바이트(); ስም = መደብ_ስም(አንባቢ_እሴት.두바이트());
            if (!መደብ_ስም(አንባቢ_እሴት.두바이트()).equals("java/lang/Object") || አንባቢ_እሴት.두바이트() != 0)
                throw new ትርጉም_ስህተት(ስም + ": 상속 및 인터페이스 미지원");
            መስክ_እሴት = 멤버읽기(አንባቢ_እሴት); ተግባር_እሴት = 멤버읽기(አንባቢ_እሴት); 속성읽기(አንባቢ_እሴት);
            if (አንባቢ_እሴት.አካባቢ != አንባቢ_እሴት.ውሂብ.length) throw new ትርጉም_ስህተት("መደብ_እሴት 뒤에 남은 ውሂብ");
        }
        String 문자(int መረጃ_ጠቆመ) {
            if (መረጃ_ጠቆመ < 1 || መረጃ_ጠቆመ >= 상수종류.length || 상수종류[መረጃ_ጠቆመ] != 1) throw new ትርጉም_ስህተት("문자 ቋሚ_እሴት መረጃ_ጠቆመ ስህተት");
            return (String) ቋሚ_ውሂብ[መረጃ_ጠቆመ];
        }
        String መደብ_ስም(int መረጃ_ጠቆመ) {
            if (መረጃ_ጠቆመ < 1 || መረጃ_ጠቆመ >= 상수종류.length || 상수종류[መረጃ_ጠቆመ] != 7) throw new ትርጉም_ስህተት("መደብ_እሴት ማጣቀሻ ስህተት");
            return 문자((Integer)ቋሚ_ውሂብ[መረጃ_ጠቆመ]);
        }
        ስልት_ማጣቀሻ ማጣቀሻ(int መረጃ_ጠቆመ) {
            if (መረጃ_ጠቆመ < 1 || መረጃ_ጠቆመ >= 상수종류.length || 상수종류[መረጃ_ጠቆመ] < 9 || 상수종류[መረጃ_ጠቆመ] > 11) throw new ትርጉም_ስህተት("멤버 ማጣቀሻ ስህተት");
            int[] አገጣጥም_እሴት = (int[])ቋሚ_ውሂብ[መረጃ_ጠቆመ], ስም_አገጣጥም = (int[])ቋሚ_ውሂብ[አገጣጥም_እሴት[1]];
            return new ስልት_ማጣቀሻ(መደብ_ስም(አገጣጥም_እሴት[0]), 문자(ስም_አገጣጥም[0]), 문자(ስም_አገጣጥም[1]));
        }
        Map<String, byte[]> 속성읽기(ውሂብ_አንባቢ አንባቢ_እሴት) {
            Map<String, byte[]> ልኬት = new LinkedHashMap<>();
            int 개수 = አንባቢ_እሴት.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String ዓይነታ_ስም = 문자(አንባቢ_እሴት.두바이트()); byte[] እሴት = አንባቢ_እሴት.ማንበቢያ(አንባቢ_እሴት.네바이트());
                if (ልኬት.put(ዓይነታ_ስም, እሴት) != null) throw new ትርጉም_ስህተት("겹친 ዓይነታ_እሴት: " + ዓይነታ_ስም);
            }
            return ልኬት;
        }
        List<አባል_ውሂብ> 멤버읽기(ውሂብ_አንባቢ አንባቢ_እሴት) {
            List<አባል_ውሂብ> ልኬት = new ArrayList<>(); int 개수 = አንባቢ_እሴት.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int መዳረሻ_ምዝግብ = አንባቢ_እሴት.두바이트(); String ስልት_ምዝግብ_ስም = 문자(አንባቢ_እሴት.두바이트()), 서술 = 문자(አንባቢ_እሴት.두바이트());
                ልኬት.add(new አባል_ውሂብ(መዳረሻ_ምዝግብ, ስልት_ምዝግብ_ስም, 서술, 속성읽기(አንባቢ_እሴት)));
            }
            return ልኬት;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new ትርጉም_ስህተት("ተግባር_እሴት 서술 ስህተት: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new ትርጉም_ስህተት("ተግባር_እሴት 서술 ስህተት: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new ትርጉም_ስህተት("ተግባር_እሴት 서술 ስህተት: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> ልኬት = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int አካባቢ = 0; አካባቢ < 서술.length();) {
            String የተመረጠ_እሴት = null;
            for (String ቅርጸት_እሴት : 허용형식) if (서술.startsWith(ቅርጸት_እሴት, አካባቢ)) { የተመረጠ_እሴት = ቅርጸት_እሴት; break; }
            if (የተመረጠ_እሴት == null) throw new ትርጉም_ስህተት("지원하지 않는 የውሂብ_ዓይነት: " + 서술);
            ልኬት.add(የተመረጠ_እሴት); አካባቢ += የተመረጠ_እሴት.length();
        }
        return ልኬት;
    }
    static String ምልክት_ad6f1a96(String 종류, String... 부분들) {
        try {
            byte[] ሃሽ_ፋይል = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder ጽሁፍ = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) ጽሁፍ.append(String.format(Locale.ROOT, "%02x", ሃሽ_ፋይል[순번] & 255));
            return ጽሁፍ.toString();
        } catch (Exception ስህተት) { throw new ትርጉም_ስህተት(ስህተት.toString()); }
    }
    final Map<String, መደብ_ውሂብ> 클래스들 = new TreeMap<>();
    final Map<ስልት_ማጣቀሻ, አባል_ውሂብ> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, ማሽን_መደብ;
    final int 동적기억낱말수;
    final Path ሃብት_ዱካ;
    기계어미리번역(List<Path> ዱካ_ዝርዝር, String ዓላማ, int 낱말수, Path ሃብት_እሴት) throws IOException {
        if ((!ዓላማ.equals("kernel") && !ዓላማ.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new ትርጉም_ስህተት("ፈጽም_ትእዛዝ ዓላማ 또는 ማስቀመጫ_እሴት 공간 መጠን ስህተት");
        실행대상 = ዓላማ; 동적기억낱말수 = 낱말수; ሃብት_ዱካ = ሃብት_እሴት;
        // 이 이름도 국가별 ምንጭ_ዛፍ አዘጋጅ 시 해당 언어로 옮긴다.
        ማሽን_መደብ = ዓላማ.equals("kernel") ? "ቦርድ" : "ተጠቃሚ";
        for (String መስመር : Files.readAllLines(ሃብት_እሴት.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = መስመር.split("\t", -1);
            if (부분들.length != 4) throw new ትርጉም_ስህተት("ማሽን ተግባር_እሴት ውሂብ ስህተት");
            if (부분들[0].equals(ዓላማ)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path መተላለፊያ : ዱካ_ዝርዝር) {
            መደብ_ውሂብ ውሂብ = new መደብ_ውሂብ(መተላለፊያ);
            if (클래스들.put(ውሂብ.ስም, ውሂብ) != null) throw new ትርጉም_ስህተት("중복 መደብ_እሴት: " + ውሂብ.ስም);
            for (አባል_ውሂብ መስክ_እሴት : ውሂብ.መስክ_እሴት) {
                if ((መስክ_እሴት.መዳረሻ_ምዝግብ & 8) == 0 || 형식읽기(መስክ_እሴት.서술).equals(Collections.singletonList("V"))) throw new ትርጉም_ስህተት("አይንቀሳቀሴ_እሴት 필드만 ድገፍ_እሴት");
                if (필드들.put(new ስልት_ማጣቀሻ(ውሂብ.ስም, መስክ_እሴት.ስም, መስክ_እሴት.서술), መስክ_እሴት) != null) throw new ትርጉም_ስህተት("중복 መስክ_እሴት");
            }
            for (አባል_ውሂብ ተግባር_እሴት : ውሂብ.ተግባር_እሴት) {
                if (ተግባር_እሴት.ስም.equals("<init>")) continue;
                if ((ተግባር_እሴት.መዳረሻ_ምዝግብ & 8) == 0 || (ተግባር_እሴት.መዳረሻ_ምዝግብ & (0x20 | 0x400)) != 0) throw new ትርጉም_ስህተት("አይንቀሳቀሴ_እሴት 비동기화 함수만 ድገፍ_እሴት");
                new 함수형식(ተግባር_እሴት.서술);
                if (함수들.put(new ስልት_ማጣቀሻ(ውሂብ.ስም, ተግባር_እሴት.ስም, ተግባር_እሴት.서술), ተግባር_እሴት) != null) throw new ትርጉም_ስህተት("중복 ተግባር_እሴት");
            }
        }
    }
    String ኅብረቁምፊ_ምልክት(String ጽሁፍ) { return 문자열들.computeIfAbsent(ጽሁፍ, እሴት -> "j_text_" + 문자열들.size()); }
    String ቋሚ_የሒሳብ_ሓረግ(መደብ_ውሂብ ውሂብ, int መረጃ_ጠቆመ) {
        if (መረጃ_ጠቆመ < 1 || መረጃ_ጠቆመ >= ውሂብ.상수종류.length) throw new ትርጉም_ስህተት("ቋሚ_እሴት መረጃ_ጠቆመ ቅንጥብ ስህተት");
        if (ውሂብ.상수종류[መረጃ_ጠቆመ] == 3) return "(word)(uint32_t)(" + ውሂብ.ቋሚ_ውሂብ[መረጃ_ጠቆመ] + ")";
        if (ውሂብ.상수종류[መረጃ_ጠቆመ] == 8) return "(word)" + ኅብረቁምፊ_ምልክት(ውሂብ.문자((Integer)ውሂብ.ቋሚ_ውሂብ[መረጃ_ጠቆመ]));
        throw new ትርጉም_ስህተት("정수와 ኅብረቁምፊ_እሴት 상수만 ድገፍ_እሴት");
    }
    String 함수원형(ስልት_ማጣቀሻ ማጣቀሻ) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(ማጣቀሻ.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + ምልክት_ad6f1a96("method", ማጣቀሻ.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void ቼክ_የአካባቢ(int መረጃ_ጠቆመ, int 지역변수수) { if (መረጃ_ጠቆመ < 0 || መረጃ_ጠቆመ >= 지역변수수) throw new ትርጉም_ስህተት("የአካባቢ_ስፋት 변수 መረጃ_ጠቆመ ቅንጥብ ስህተት"); }
    void 분기넣기(List<String> ውጤት, Set<Integer> ቅርንጫፍ_ዝርዝር, int አካባቢ, int 이동량, String ሁኔታ) {
        int መድረሻ_እሴት = አካባቢ + 이동량; ቅርንጫፍ_ዝርዝር.add(መድረሻ_እሴት);
        ውጤት.add((ሁኔታ == null ? "" : "if (" + ሁኔታ + ") ") + "goto b" + መድረሻ_እሴት + ";");
    }
    String ስልት_አካል(ስልት_ማጣቀሻ ተግባር_እሴት, አባል_ውሂብ ውሂብ) {
        byte[] አካል_ውሂብ = ውሂብ.ዓይነታ_እሴት.get("Code"); if (አካል_ውሂብ == null) throw new ትርጉም_ስህተት("ተግባር_እሴት 몸체가 없음: " + ተግባር_እሴት.ስም);
        ውሂብ_አንባቢ አንባቢ_እሴት = new ውሂብ_አንባቢ(አካል_ውሂብ); int 쌓임깊이 = አንባቢ_እሴት.두바이트(), 지역변수수 = አንባቢ_እሴት.두바이트();
        ውሂብ_አንባቢ ትእዛዝ_ውሂብ = new ውሂብ_አንባቢ(አንባቢ_እሴት.ማንበቢያ(አንባቢ_እሴት.네바이트()));
        if (አንባቢ_እሴት.두바이트() != 0) throw new ትርጉም_ስህተት("try/catch/finally 미지원");
        함수형식 ቅርጸት_እሴት = new 함수형식(ተግባር_እሴት.서술); if (지역변수수 < ቅርጸት_እሴት.인수.size()) throw new ትርጉም_ስህተት("매개변수보다 적은 የአካባቢ_ስፋት 변수");
        መደብ_ውሂብ መደብ_እሴት = 클래스들.get(ተግባር_እሴት.ባለቤት_እሴት);
        List<String> ውጤት = new ArrayList<>(); ውጤት.add(함수원형(ተግባር_እሴት) + " {");
        ውጤት.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < ቅርጸት_እሴት.인수.size(); 순번++) ውጤት.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ቅርንጫፍ_ዝርዝር = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (ትእዛዝ_ውሂብ.አካባቢ < ትእዛዝ_ውሂብ.ውሂብ.length) {
            int አካባቢ = ትእዛዝ_ውሂብ.አካባቢ, ትእዛዝ = ትእዛዝ_ውሂብ.한바이트(); 경계들.add(አካባቢ); ውጤት.add("b" + አካባቢ + ":;");
            if (ትእዛዝ == 0) continue;
            if (ትእዛዝ == 1) ውጤት.add("PUSH(0);");
            else if (ትእዛዝ >= 2 && ትእዛዝ <= 8) ውጤት.add("PUSH((uint32_t)(" + (ትእዛዝ - 3) + "));");
            else if (ትእዛዝ == 16 || ትእዛዝ == 17) ውጤት.add("PUSH((uint32_t)(" + (ትእዛዝ == 16 ? ትእዛዝ_ውሂብ.부호한바이트() : ትእዛዝ_ውሂብ.부호두바이트()) + "));");
            else if (ትእዛዝ == 18 || ትእዛዝ == 19) ውጤት.add("PUSH(" + ቋሚ_የሒሳብ_ሓረግ(መደብ_እሴት, ትእዛዝ == 18 ? ትእዛዝ_ውሂብ.한바이트() : ትእዛዝ_ውሂብ.두바이트()) + ");");
            else if (ትእዛዝ == 21 || ትእዛዝ == 25 || (ትእዛዝ >= 26 && ትእዛዝ <= 29) || (ትእዛዝ >= 42 && ትእዛዝ <= 45)) {
                int መረጃ_ጠቆመ = ትእዛዝ == 21 || ትእዛዝ == 25 ? ትእዛዝ_ውሂብ.한바이트() : ትእዛዝ - (ትእዛዝ <= 29 ? 26 : 42);
                ቼክ_የአካባቢ(መረጃ_ጠቆመ, 지역변수수); ውጤት.add("PUSH(l[" + መረጃ_ጠቆመ + "]);");
            } else if (ትእዛዝ == 54 || ትእዛዝ == 58 || (ትእዛዝ >= 59 && ትእዛዝ <= 62) || (ትእዛዝ >= 75 && ትእዛዝ <= 78)) {
                int መረጃ_ጠቆመ = ትእዛዝ == 54 || ትእዛዝ == 58 ? ትእዛዝ_ውሂብ.한바이트() : ትእዛዝ - (ትእዛዝ <= 62 ? 59 : 75);
                ቼክ_የአካባቢ(መረጃ_ጠቆመ, 지역변수수); ውጤት.add("l[" + መረጃ_ጠቆመ + "] = POP();");
            } else if (ትእዛዝ == 46) ውጤት.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (ትእዛዝ == 79) ውጤት.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (ትእዛዝ == 87 || ትእዛዝ == 88) ውጤት.add(ትእዛዝ == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (ትእዛዝ >= 89 && ትእዛዝ <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ቅደም_ተከተል_ዝርዝር = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[ትእዛዝ - 89]; 순번++) ውጤት.add("abcd".charAt(순번) + " = POP();");
                for (char እሴት : ቅደም_ተከተል_ዝርዝር[ትእዛዝ - 89].toCharArray()) ውጤት.add("PUSH(" + እሴት + ");");
            } else if (ትእዛዝ == 96 || ትእዛዝ == 100 || ትእዛዝ == 104 || ትእዛዝ == 126 || ትእዛዝ == 128 || ትእዛዝ == 130) {
                String ክወና_እሴት = ትእዛዝ == 96 ? "+" : ትእዛዝ == 100 ? "-" : ትእዛዝ == 104 ? "*" : ትእዛዝ == 126 ? "&" : ትእዛዝ == 128 ? "|" : "^";
                ውጤት.add("b = POP(); a = POP(); PUSH((uint32_t)a " + ክወና_እሴት + " (uint32_t)b);");
            } else if (ትእዛዝ == 108 || ትእዛዝ == 112) ውጤት.add("b = POP(); a = POP(); PUSH(divide(a,b," + (ትእዛዝ == 112 ? 1 : 0) + "));");
            else if (ትእዛዝ == 116) ውጤት.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (ትእዛዝ == 120 || ትእዛዝ == 122 || ትእዛዝ == 124) {
                ውጤት.add("b = POP(); a = POP();"); ውጤት.add("PUSH(" + (ትእዛዝ == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (ትእዛዝ == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (ትእዛዝ == 132) {
                int መረጃ_ጠቆመ = ትእዛዝ_ውሂብ.한바이트(), 증가량 = ትእዛዝ_ውሂብ.부호한바이트(); ቼክ_የአካባቢ(መረጃ_ጠቆመ, 지역변수수);
                ውጤት.add("l[" + መረጃ_ጠቆመ + "] = (uint32_t)l[" + መረጃ_ጠቆመ + "] + (uint32_t)(" + 증가량 + ");");
            } else if (ትእዛዝ >= 145 && ትእዛዝ <= 147) ውጤት.add("a = POP(); PUSH((uint32_t)(" + (ትእዛዝ == 145 ? "int8_t" : ትእዛዝ == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (ትእዛዝ >= 153 && ትእዛዝ <= 158) {
                ውጤት.add("a = POP();"); 분기넣기(ውጤት, ቅርንጫፍ_ዝርዝር, አካባቢ, ትእዛዝ_ውሂብ.부호두바이트(), "(int32_t)a " + 비교들[ትእዛዝ - 153] + " 0");
            } else if (ትእዛዝ >= 159 && ትእዛዝ <= 166) {
                ውጤት.add("b = POP(); a = POP();"); 분기넣기(ውጤት, ቅርንጫፍ_ዝርዝር, አካባቢ, ትእዛዝ_ውሂብ.부호두바이트(), ትእዛዝ >= 165 ? "a " + 비교들[ትእዛዝ - 159] + " b" : "(int32_t)a " + 비교들[ትእዛዝ - 159] + " (int32_t)b");
            } else if (ትእዛዝ == 167 || ትእዛዝ == 200) 분기넣기(ውጤት, ቅርንጫፍ_ዝርዝር, አካባቢ, ትእዛዝ == 167 ? ትእዛዝ_ውሂብ.부호두바이트() : ትእዛዝ_ውሂብ.네바이트(), null);
            else if (ትእዛዝ == 170 || ትእዛዝ == 171) {
                while (ትእዛዝ_ውሂብ.አካባቢ % 4 != 0) ትእዛዝ_ውሂብ.한바이트();
                int ነባሪ_እሴት = ትእዛዝ_ውሂብ.네바이트(); ውጤት.add("a = POP();");
                if (ትእዛዝ == 170) {
                    int 아래 = ትእዛዝ_ውሂብ.네바이트(), 위 = ትእዛዝ_ውሂብ.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (ትእዛዝ_ውሂብ.ውሂብ.length - ትእዛዝ_ውሂብ.አካባቢ) / 4) throw new ትርጉም_ስህተት("switch ቅንጥብ ስህተት");
                    for (long እሴት = 아래; እሴት <= 위; እሴት++) 분기넣기(ውጤት, ቅርንጫፍ_ዝርዝር, አካባቢ, ትእዛዝ_ውሂብ.네바이트(), "(int32_t)a == (" + እሴት + ")");
                } else {
                    int 개수 = ትእዛዝ_ውሂብ.네바이트(), ፊት_ውሂብ = 0;
                    if (개수 < 0 || 개수 > (ትእዛዝ_ውሂብ.ውሂብ.length - ትእዛዝ_ውሂብ.አካባቢ) / 8) throw new ትርጉም_ስህተት("switch መጠን ስህተት");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int እሴት = ትእዛዝ_ውሂብ.네바이트(); if (순번 > 0 && እሴት <= ፊት_ውሂብ) throw new ትርጉም_ስህተት("switch ቅደም_ተከተል_እሴት ስህተት"); ፊት_ውሂብ = እሴት;
                        분기넣기(ውጤት, ቅርንጫፍ_ዝርዝር, አካባቢ, ትእዛዝ_ውሂብ.네바이트(), "(int32_t)a == (" + እሴት + ")");
                    }
                }
                분기넣기(ውጤት, ቅርንጫፍ_ዝርዝር, አካባቢ, ነባሪ_እሴት, null);
            } else if (ትእዛዝ == 172 || ትእዛዝ == 176 || ትእዛዝ == 177) ውጤት.add("return " + (ትእዛዝ == 177 ? "0" : "POP()") + ";");
            else if (ትእዛዝ == 178 || ትእዛዝ == 179) {
                ስልት_ማጣቀሻ ማጣቀሻ = መደብ_እሴት.ማጣቀሻ(ትእዛዝ_ውሂብ.두바이트()); if (!필드들.containsKey(ማጣቀሻ)) throw new ትርጉም_ስህተት("알 수 없는 መስክ_እሴት");
                ውጤት.add(ምልክት_ad6f1a96("init", ማጣቀሻ.ባለቤት_እሴት) + "();"); String መስክ_እሴት = ምልክት_ad6f1a96("field", ማጣቀሻ.부분들());
                ውጤት.add(ትእዛዝ == 178 ? "PUSH(" + መስክ_እሴት + ");" : መስክ_እሴት + " = POP();");
            } else if (ትእዛዝ == 184) {
                ስልት_ማጣቀሻ ማጣቀሻ = መደብ_እሴት.ማጣቀሻ(ትእዛዝ_ውሂብ.두바이트()); if (!함수들.containsKey(ማጣቀሻ)) throw new ትርጉም_ስህተት("알 수 없는 ተግባር_እሴት");
                함수형식 호출형식 = new 함수형식(ማጣቀሻ.서술); int 개수 = 호출형식.인수.size();
                ውጤት.add(ምልክት_ad6f1a96("init", ማጣቀሻ.ባለቤት_እሴት) + "();"); ውጤት.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                ውጤት.add("a = " + ምልክት_ad6f1a96("method", ማጣቀሻ.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) ውጤት.add("PUSH(a);");
            } else if (ትእዛዝ == 182) {
                ስልት_ማጣቀሻ ማጣቀሻ = መደብ_እሴት.ማጣቀሻ(ትእዛዝ_ውሂብ.두바이트());
                if (ማጣቀሻ.equals(new ስልት_ማጣቀሻ("java/lang/String", "length", "()I"))) ውጤት.add("a = POP(); PUSH(length(a));");
                else if (ማጣቀሻ.equals(new ስልት_ማጣቀሻ("java/lang/String", "charAt", "(I)C"))) ውጤት.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new ትርጉም_ስህተት("가상 ተግባር_እሴት 호출 미지원");
            } else if (ትእዛዝ == 188) {
                if (ትእዛዝ_ውሂብ.한바이트() != 10) throw new ትርጉም_ስህተት("new int[]만 ድገፍ_እሴት"); ውጤት.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (ትእዛዝ == 190) ውጤት.add("a = POP(); PUSH(length(a));");
            else if (ትእዛዝ == 196) {
                int ቅጥያ_እሴት = ትእዛዝ_ውሂብ.한바이트(), መረጃ_ጠቆመ = ትእዛዝ_ውሂብ.두바이트(); ቼክ_የአካባቢ(መረጃ_ጠቆመ, 지역변수수);
                if (ቅጥያ_እሴት == 21 || ቅጥያ_እሴት == 25) ውጤት.add("PUSH(l[" + መረጃ_ጠቆመ + "]);");
                else if (ቅጥያ_እሴት == 54 || ቅጥያ_እሴት == 58) ውጤት.add("l[" + መረጃ_ጠቆመ + "] = POP();");
                else if (ቅጥያ_እሴት == 132) ውጤት.add("l[" + መረጃ_ጠቆመ + "] = (uint32_t)l[" + መረጃ_ጠቆመ + "] + (uint32_t)(" + ትእዛዝ_ውሂብ.부호두바이트() + ");");
                else throw new ትርጉም_ስህተት("미지원 wide ትእዛዝ");
            } else if (ትእዛዝ == 198 || ትእዛዝ == 199) {
                ውጤት.add("a = POP();"); 분기넣기(ውጤት, ቅርንጫፍ_ዝርዝር, አካባቢ, ትእዛዝ_ውሂብ.부호두바이트(), "a " + (ትእዛዝ == 198 ? "==" : "!=") + " 0");
            } else throw new ትርጉም_ስህተት(ተግባር_እሴት.ባለቤት_እሴት + "." + ተግባር_እሴት.ስም + ", ባይት_እሴት " + አካባቢ + ": 미지원 ትእዛዝ " + ትእዛዝ);
        }
        if (!경계들.containsAll(ቅርንጫፍ_ዝርዝር)) throw new ትርጉም_ስህተት("ትእዛዝ 경계가 아닌 곳으로 ቅርንጫፍ");
        ውጤት.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", ውጤት);
    }
    String አስወጣ_ስልት(String አገናኝ_ምልክት, String ዓላማ, boolean 진입점여부) {
        int በቦታ_አስቀመጠ_መረጃ_ጠቆመ = ዓላማ.lastIndexOf('.'); if (በቦታ_አስቀመጠ_መረጃ_ጠቆመ < 0 || !አገናኝ_ምልክት.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ትርጉም_ስህተት("내보내기 지정 ስህተት");
        String ባለቤት_እሴት = ዓላማ.substring(0, በቦታ_አስቀመጠ_መረጃ_ጠቆመ).replace('.', '/'), ስም = ዓላማ.substring(በቦታ_አስቀመጠ_መረጃ_ጠቆመ + 1); ስልት_ማጣቀሻ የተመረጠ_እሴት = null;
        for (ስልት_ማጣቀሻ ማጣቀሻ : 함수들.keySet()) if (ማጣቀሻ.ባለቤት_እሴት.equals(ባለቤት_እሴት) && ማጣቀሻ.ስም.equals(ስም)) {
            if (የተመረጠ_እሴት != null) throw new ትርጉም_ስህተት("겹친 내보내기 ዓላማ"); የተመረጠ_እሴት = ማጣቀሻ;
        }
        if (የተመረጠ_እሴት == null || (함수들.get(የተመረጠ_እሴት).መዳረሻ_ምዝግብ & 0x100) != 0) throw new ትርጉም_ስህተት("내보낼 함수가 없음 또는 native ተግባር_እሴት");
        함수형식 ቅርጸት_እሴት = new 함수형식(የተመረጠ_እሴት.서술);
        if ((진입점여부 && !ቅርጸት_እሴት.인수.isEmpty()) || !Arrays.asList("V", "I").contains(ቅርጸት_እሴት.반환)) throw new ትርጉም_ስህተት("ምዝግብ_ቦታ_እሴት 또는 C 경계 ቅርጸት_እሴት ስህተት");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < ቅርጸት_እሴት.인수.size(); 순번++) {
            if (!ቅርጸት_እሴት.인수.get(순번).equals("I")) throw new ትርጉም_ስህተት("C 경계는 int 인수만 ድገፍ_እሴት");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (ቅርጸት_እሴት.반환.equals("V") ? "void " : "int32_t ") + አገናኝ_ምልክት + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + ምልክት_ad6f1a96("init", የተመረጠ_እሴት.ባለቤት_እሴት) + "(); " + (ቅርጸት_እሴት.반환.equals("V") ? "" : "return (int32_t)") + ምልክት_ad6f1a96("method", የተመረጠ_እሴት.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String አዘጋጅ(String ምዝግብ_ቦታ, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<ስልት_ማጣቀሻ, አባል_ውሂብ> ምዝግብ_እሴት : 함수들.entrySet()) {
            ስልት_ማጣቀሻ ማጣቀሻ = ምዝግብ_እሴት.getKey(); አባል_ውሂብ ውሂብ = ምዝግብ_እሴት.getValue(); 선언들.add(함수원형(ማጣቀሻ) + ";");
            if ((ውሂብ.መዳረሻ_ምዝግብ & 0x100) != 0) {
                String መገናኛ = 기계함수들.get(ማጣቀሻ.ስም + ማጣቀሻ.서술);
                if (!ማጣቀሻ.ባለቤት_እሴት.equals(ማሽን_መደብ) || መገናኛ == null) throw new ትርጉም_ስህተት("허용되지 않은 native ተግባር_እሴት: " + ማጣቀሻ.ስም);
                int 개수 = new 함수형식(ማጣቀሻ.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + መገናኛ + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(ማጣቀሻ) + " { return " + መገናኛ + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(ስልት_አካል(ማጣቀሻ, ውሂብ));
        }
        for (Map.Entry<ስልት_ማጣቀሻ, አባል_ውሂብ> ምዝግብ_እሴት : 필드들.entrySet()) {
            ስልት_ማጣቀሻ ማጣቀሻ = ምዝግብ_እሴት.getKey(); byte[] ቋሚ_እሴት = ምዝግብ_እሴት.getValue().ዓይነታ_እሴት.get("ConstantValue");
            String እሴት = ቋሚ_እሴት == null ? "0" : ቋሚ_የሒሳብ_ሓረግ(클래스들.get(ማጣቀሻ.ባለቤት_እሴት), new ውሂብ_አንባቢ(ቋሚ_እሴት).두바이트());
            필드선언들.add("static word " + ምልክት_ad6f1a96("field", ማጣቀሻ.부분들()) + " = " + እሴት + ";");
        }
        for (String ስም : 클래스들.keySet()) {
            String ጀምር = ምልክት_ad6f1a96("init", ስም), ዞን_እሴት = ምልክት_ad6f1a96("state", ስም);
            선언들.add("static void " + ጀምር + "(void);"); 필드선언들.add("static unsigned " + ዞን_እሴት + ";");
            ስልት_ማጣቀሻ ማጣቀሻ = new ስልት_ማጣቀሻ(ስም, "<clinit>", "()V");
            몸체들.add("static void " + ጀምር + "(void) { if(" + ዞን_እሴት + ") return; " + ዞን_እሴት + " = 1; " + (함수들.containsKey(ማጣቀሻ) ? ምልክት_ad6f1a96("method", ማጣቀሻ.부분들()) + "(); " : "") + ዞን_እሴት + " = 2; }");
        }
        몸체들.add(አስወጣ_ስልት("java_entry", ምዝግብ_ቦታ, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int በቦታ_አስቀመጠ_መረጃ_ጠቆመ = 지정.indexOf('='); if (በቦታ_አስቀመጠ_መረጃ_ጠቆመ < 1) throw new ትርጉም_ስህተት("내보내기 지정 ስህተት");
            String ስም = 지정.substring(0, በቦታ_አስቀመጠ_መረጃ_ጠቆመ); 공개이름.add(ስም); 몸체들.add(አስወጣ_ስልት(ስም, 지정.substring(በቦታ_አስቀመጠ_መረጃ_ጠቆመ + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> ምዝግብ_እሴት : 문자열들.entrySet()) {
            String ጽሁፍ = ምዝግብ_እሴት.getKey(); StringBuilder ድርድር_እሴት = new StringBuilder("static const word " + ምዝግብ_እሴት.getValue() + "[] = {" + ጽሁፍ.length());
            for (int 순번 = 0; 순번 < ጽሁፍ.length(); 순번++) ድርድር_እሴት.append(", ").append((int)ጽሁፍ.charAt(순번));
            문자열선언들.add(ድርድር_እሴት.append("};").toString());
        }
        String ድገፍ_እሴት = Files.readString(ሃብት_ዱካ.resolve("የጋራ_ቋንቋ_ማስኬጃ_ጊዜ_ድገፍ.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(ድገፍ_እሴት + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ምንጭ, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ስም_ሰንጠረዥ = new HashMap<>();
        for (String መስመር : Files.readAllLines(ሃብት_ዱካ.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] አገጣጥም_እሴት = መስመር.split("\t"); ስም_ሰንጠረዥ.put(አገጣጥም_እሴት[0], አገጣጥም_እሴት[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(ምንጭ); StringBuffer ልኬት = new StringBuffer();
        while (찾개.find()) {
            String ስም = 찾개.group(), 새이름 = ስም;
            if (!ስም.startsWith("//") && !ስም.startsWith("/*") && !ስም.startsWith("\"") && !ስም.startsWith("'") && !공개이름.contains(ስም)) {
                새이름 = ስም_ሰንጠረዥ.getOrDefault(ስም, ስም);
                if (ስም.matches("a[0-9]+")) 새이름 = "인수" + ስም.substring(1);
                if (ስም.matches("b[0-9]+")) 새이름 = "ቅርንጫፍ" + ስም.substring(1);
                if (범용표기) {
                    StringBuilder አጻጻፍ_እሴት = new StringBuilder();
                    for (char ቁምፊ_እሴት : 새이름.toCharArray()) አጻጻፍ_እሴት.append(ቁምፊ_እሴት < 128 ? Character.toString(ቁምፊ_እሴት) : String.format(Locale.ROOT, "\\u%04x", (int)ቁምፊ_እሴት));
                    새이름 = አጻጻፍ_እሴት.toString();
                }
            }
            찾개.appendReplacement(ልኬት, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(ልኬት); return ልኬት.toString();
    }
    String 엑스함수본문(ስልት_ማጣቀሻ ተግባር_እሴት, አባል_ውሂብ ውሂብ, Map<String,String> ማሽን_ሰንጠረዥ, String ዓላማ) {
        String 표식 = ምልክት_ad6f1a96("method", ተግባር_እሴት.부분들());
        List<String> መስመር = new ArrayList<>();
        if ((ውሂብ.መዳረሻ_ምዝግብ & 0x100) != 0) {
            String መገናኛ = ማሽን_ሰንጠረዥ.get(ተግባር_እሴት.ስም + ተግባር_እሴት.서술);
            if (!ተግባር_እሴት.ባለቤት_እሴት.equals(ዓላማ.equals("kernel") ? "መሳሪያ_እሴት" : "ተጠቃሚ") || መገናኛ == null) throw new ትርጉም_ስህተት("허용되지 않은 native ተግባር_እሴት");
            return ".text\n" + 표식 + ":\njmp " + መገናኛ;
        }
        byte[] የጽሁፍ_አካል = ውሂብ.ዓይነታ_እሴት.get("Code"); if (የጽሁፍ_አካል == null) throw new ትርጉም_ስህተት("ተግባር_እሴት 몸체가 없음");
        ውሂብ_አንባቢ አንባቢ_እሴት = new ውሂብ_አንባቢ(የጽሁፍ_አካል); አንባቢ_እሴት.두바이트(); int 지역수 = አንባቢ_እሴት.두바이트();
        ውሂብ_አንባቢ ትእዛዝ_ውሂብ = new ውሂብ_አንባቢ(አንባቢ_እሴት.ማንበቢያ(አንባቢ_እሴት.네바이트()));
        if (አንባቢ_እሴት.두바이트() != 0) throw new ትርጉም_ስህተት("try/catch/finally 미지원");
        함수형식 ቅርጸት_እሴት = new 함수형식(ተግባር_እሴት.서술); if (지역수 < ቅርጸት_እሴት.인수.size()) throw new ትርጉም_ስህተት("매개변수보다 적은 የአካባቢ_ስፋት 변수");
        Collections.addAll(መስመር,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < ቅርጸት_እሴት.인수.size(); 순번++) Collections.addAll(መስመር,"movl " + (8 + 4 * (ቅርጸት_እሴት.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        መደብ_ውሂብ መደብ_እሴት = 클래스들.get(ተግባር_እሴት.ባለቤት_እሴት); Set<Integer> 경계들 = new HashSet<>(), ቅርንጫፍ_ዝርዝር = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (ትእዛዝ_ውሂብ.አካባቢ < ትእዛዝ_ውሂብ.ውሂብ.length) {
            int አካባቢ = ትእዛዝ_ውሂብ.አካባቢ, ትእዛዝ = ትእዛዝ_ውሂብ.한바이트(); String በቦታ_አስቀመጠ_መረጃ_ጠቆመ = 표식 + "_b" + አካባቢ;
            መስመር.add(በቦታ_አስቀመጠ_መረጃ_ጠቆመ + ":"); 경계들.add(አካባቢ);
            if (ትእዛዝ == 0) መስመር.add("nop");
            else if (ትእዛዝ == 1) መስመር.add("pushl $0");
            else if (ትእዛዝ >= 2 && ትእዛዝ <= 8) መስመር.add("pushl $" + (ትእዛዝ - 3));
            else if (ትእዛዝ == 16 || ትእዛዝ == 17) መስመር.add("pushl $" + (ትእዛዝ == 16 ? ትእዛዝ_ውሂብ.부호한바이트() : ትእዛዝ_ውሂብ.부호두바이트()));
            else if (ትእዛዝ == 18 || ትእዛዝ == 19) {
                int መረጃ_ጠቆመ = ትእዛዝ == 18 ? ትእዛዝ_ውሂብ.한바이트() : ትእዛዝ_ውሂብ.두바이트();
                መስመር.add("pushl $" + 엑스상수(መደብ_እሴት,መረጃ_ጠቆመ));
            } else if (ትእዛዝ == 21 || ትእዛዝ == 25 || (ትእዛዝ >= 26 && ትእዛዝ <= 29) || (ትእዛዝ >= 42 && ትእዛዝ <= 45) || ትእዛዝ == 54 || ትእዛዝ == 58 || (ትእዛዝ >= 59 && ትእዛዝ <= 62) || (ትእዛዝ >= 75 && ትእዛዝ <= 78)) {
                boolean 읽음 = ትእዛዝ < 54; int መረጃ_ጠቆመ = ትእዛዝ == 21 || ትእዛዝ == 25 || ትእዛዝ == 54 || ትእዛዝ == 58 ? ትእዛዝ_ውሂብ.한바이트() : ትእዛዝ - (ትእዛዝ <= 29 ? 26 : ትእዛዝ <= 45 ? 42 : ትእዛዝ <= 62 ? 59 : 75);
                ቼክ_የአካባቢ(መረጃ_ጠቆመ,지역수); መስመር.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (መረጃ_ጠቆመ + 1)) + "(%ebp)");
            } else if (ትእዛዝ == 46) Collections.addAll(መስመር,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (ትእዛዝ == 79) Collections.addAll(መስመር,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (ትእዛዝ == 87 || ትእዛዝ == 88) መስመር.add("addl $" + (ትእዛዝ == 87 ? 4 : 8) + ", %esp");
            else if (ትእዛዝ >= 89 && ትእዛዝ <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ቅደም_ተከተል_ዝርዝር = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[ትእዛዝ - 89]; 순번++) መስመር.add("popl " + 저장기들[순번]);
                for (int 순번 : ቅደም_ተከተል_ዝርዝር[ትእዛዝ - 89]) መስመር.add("pushl " + 저장기들[순번]);
            } else if (ትእዛዝ == 96 || ትእዛዝ == 100 || ትእዛዝ == 104 || ትእዛዝ == 126 || ትእዛዝ == 128 || ትእዛዝ == 130) {
                String ክወና_እሴት = ትእዛዝ == 96 ? "addl" : ትእዛዝ == 100 ? "subl" : ትእዛዝ == 104 ? "imull" : ትእዛዝ == 126 ? "andl" : ትእዛዝ == 128 ? "orl" : "xorl";
                Collections.addAll(መስመር,"popl %ecx","popl %eax",ክወና_እሴት + " %ecx, %eax","pushl %eax");
            } else if (ትእዛዝ == 108 || ትእዛዝ == 112) Collections.addAll(መስመር,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + በቦታ_አስቀመጠ_መረጃ_ጠቆመ + "_divide","cmpl $0x80000000, %eax","jne " + በቦታ_አስቀመጠ_መረጃ_ጠቆመ + "_divide","xorl %edx, %edx","jmp " + በቦታ_አስቀመጠ_መረጃ_ጠቆመ + "_done",በቦታ_አስቀመጠ_መረጃ_ጠቆመ + "_divide:","cltd","idivl %ecx",በቦታ_አስቀመጠ_መረጃ_ጠቆመ + "_done:","pushl " + (ትእዛዝ == 108 ? "%eax" : "%edx"));
            else if (ትእዛዝ == 116) መስመር.add("negl (%esp)");
            else if (ትእዛዝ == 120 || ትእዛዝ == 122 || ትእዛዝ == 124) Collections.addAll(መስመር,"popl %ecx","popl %eax",(ትእዛዝ == 120 ? "sall" : ትእዛዝ == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (ትእዛዝ == 132) {
                int መረጃ_ጠቆመ = ትእዛዝ_ውሂብ.한바이트(), 증가 = ትእዛዝ_ውሂብ.부호한바이트(); ቼክ_የአካባቢ(መረጃ_ጠቆመ,지역수); መስመር.add("addl $" + 증가 + ", -" + (4 * (መረጃ_ጠቆመ + 1)) + "(%ebp)");
            } else if (ትእዛዝ >= 145 && ትእዛዝ <= 147) Collections.addAll(መስመር,"popl %eax",ትእዛዝ == 145 ? "movsbl %al, %eax" : ትእዛዝ == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (ትእዛዝ >= 153 && ትእዛዝ <= 166) {
                if (ትእዛዝ <= 158) Collections.addAll(መስመር,"popl %eax","testl %eax, %eax");
                else Collections.addAll(መስመር,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int መድረሻ_እሴት = አካባቢ + ትእዛዝ_ውሂብ.부호두바이트(); ቅርንጫፍ_ዝርዝር.add(መድረሻ_እሴት); መስመር.add(비교들[ትእዛዝ - (ትእዛዝ <= 158 ? 153 : 159)] + " " + 표식 + "_b" + መድረሻ_እሴት);
            } else if (ትእዛዝ == 167 || ትእዛዝ == 200) {
                int መድረሻ_እሴት = አካባቢ + (ትእዛዝ == 167 ? ትእዛዝ_ውሂብ.부호두바이트() : ትእዛዝ_ውሂብ.네바이트()); ቅርንጫፍ_ዝርዝር.add(መድረሻ_እሴት); መስመር.add("jmp " + 표식 + "_b" + መድረሻ_እሴት);
            } else if (ትእዛዝ == 170 || ትእዛዝ == 171) {
                while (ትእዛዝ_ውሂብ.አካባቢ % 4 != 0) ትእዛዝ_ውሂብ.한바이트();
                int ነባሪ_እሴት = አካባቢ + ትእዛዝ_ውሂብ.네바이트(); ቅርንጫፍ_ዝርዝር.add(ነባሪ_እሴት); መስመር.add("popl %eax");
                int 개수, 아래 = 0;
                if (ትእዛዝ == 170) { 아래 = ትእዛዝ_ውሂብ.네바이트(); int 위 = ትእዛዝ_ውሂብ.네바이트(); long ርዝመት_እሴት = (long)위 - 아래 + 1; if (ርዝመት_እሴት < 1 || ርዝመት_እሴት > (ትእዛዝ_ውሂብ.ውሂብ.length - ትእዛዝ_ውሂብ.አካባቢ) / 4) throw new ትርጉም_ስህተት("switch ቅንጥብ ስህተት"); 개수 = (int)ርዝመት_እሴት; }
                else { 개수 = ትእዛዝ_ውሂብ.네바이트(); if (개수 < 0 || 개수 > (ትእዛዝ_ውሂብ.ውሂብ.length - ትእዛዝ_ውሂብ.አካባቢ) / 8) throw new ትርጉም_ስህተት("switch መጠን ስህተት"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int እሴት = ትእዛዝ == 170 ? 아래 + 순번 : ትእዛዝ_ውሂብ.네바이트(), መድረሻ_እሴት = አካባቢ + ትእዛዝ_ውሂብ.네바이트(); ቅርንጫፍ_ዝርዝር.add(መድረሻ_እሴት);
                    Collections.addAll(መስመር,"cmpl $" + እሴት + ", %eax","je " + 표식 + "_b" + መድረሻ_እሴት);
                }
                መስመር.add("jmp " + 표식 + "_b" + ነባሪ_እሴት);
            } else if (ትእዛዝ == 172 || ትእዛዝ == 176 || ትእዛዝ == 177) {
                if (ትእዛዝ != 177) መስመር.add("popl %eax"); Collections.addAll(መስመር,"leave","ret");
            } else if (ትእዛዝ == 178 || ትእዛዝ == 179) {
                ስልት_ማጣቀሻ ማጣቀሻ = መደብ_እሴት.ማጣቀሻ(ትእዛዝ_ውሂብ.두바이트()); if (!필드들.containsKey(ማጣቀሻ)) throw new ትርጉም_ስህተት("알 수 없는 መስክ_እሴት");
                Collections.addAll(መስመር,"call " + ምልክት_ad6f1a96("init",ማጣቀሻ.ባለቤት_እሴት),(ትእዛዝ == 178 ? "pushl " : "popl ") + ምልክት_ad6f1a96("field",ማጣቀሻ.부분들()));
            } else if (ትእዛዝ == 184) {
                ስልት_ማጣቀሻ ማጣቀሻ = መደብ_እሴት.ማጣቀሻ(ትእዛዝ_ውሂብ.두바이트()); if (!함수들.containsKey(ማጣቀሻ)) throw new ትርጉም_ስህተት("알 수 없는 ተግባር_እሴት");
                함수형식 호출형식 = new 함수형식(ማጣቀሻ.서술); Collections.addAll(መስመር,"call " + ምልክት_ad6f1a96("init",ማጣቀሻ.ባለቤት_እሴት),"call " + ምልክት_ad6f1a96("method",ማጣቀሻ.부분들()));
                if (!호출형식.인수.isEmpty()) መስመር.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) መስመር.add("pushl %eax");
            } else if (ትእዛዝ == 182) {
                ስልት_ማጣቀሻ ማጣቀሻ = መደብ_እሴት.ማጣቀሻ(ትእዛዝ_ውሂብ.두바이트());
                if (ማጣቀሻ.equals(new ስልት_ማጣቀሻ("java/lang/String","length","()I"))) Collections.addAll(መስመር,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (ማጣቀሻ.equals(new ስልት_ማጣቀሻ("java/lang/String","charAt","(I)C"))) Collections.addAll(መስመር,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new ትርጉም_ስህተት("가상 ተግባር_እሴት 호출 미지원");
            } else if (ትእዛዝ == 188) {
                if (ትእዛዝ_ውሂብ.한바이트() != 10) throw new ትርጉም_ስህተት("new int[]만 ድገፍ_እሴት"); Collections.addAll(መስመር,"popl %eax","call rt_new_array","pushl %eax");
            } else if (ትእዛዝ == 190) Collections.addAll(መስመር,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (ትእዛዝ == 196) {
                int ቅጥያ_እሴት = ትእዛዝ_ውሂብ.한바이트(), መረጃ_ጠቆመ = ትእዛዝ_ውሂብ.두바이트(); ቼክ_የአካባቢ(መረጃ_ጠቆመ,지역수);
                if (ቅጥያ_እሴት == 21 || ቅጥያ_እሴት == 25 || ቅጥያ_እሴት == 54 || ቅጥያ_እሴት == 58) መስመር.add((ቅጥያ_እሴት <= 25 ? "pushl " : "popl ") + "-" + 4 * (መረጃ_ጠቆመ + 1) + "(%ebp)");
                else if (ቅጥያ_እሴት == 132) መስመር.add("addl $" + ትእዛዝ_ውሂብ.부호두바이트() + ", -" + 4 * (መረጃ_ጠቆመ + 1) + "(%ebp)");
                else throw new ትርጉም_ስህተት("wide ትእዛዝ 미지원");
            } else if (ትእዛዝ == 198 || ትእዛዝ == 199) {
                int መድረሻ_እሴት = አካባቢ + ትእዛዝ_ውሂብ.부호두바이트(); ቅርንጫፍ_ዝርዝር.add(መድረሻ_እሴት); Collections.addAll(መስመር,"popl %eax","testl %eax, %eax",(ትእዛዝ == 198 ? "je " : "jne ") + 표식 + "_b" + መድረሻ_እሴት);
            } else throw new ትርጉም_ስህተት("미지원 ትእዛዝ: " + ትእዛዝ);
        }
        if (!경계들.containsAll(ቅርንጫፍ_ዝርዝር)) throw new ትርጉም_ስህተት("ትእዛዝ 경계가 아닌 곳으로 ቅርንጫፍ");
        መስመር.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",መስመር);
    }
    String 엑스상수(መደብ_ውሂብ ውሂብ, int መረጃ_ጠቆመ) {
        if (ውሂብ.상수종류[መረጃ_ጠቆመ] == 3) return ውሂብ.ቋሚ_ውሂብ[መረጃ_ጠቆመ].toString();
        if (ውሂብ.상수종류[መረጃ_ጠቆመ] == 8) return ኅብረቁምፊ_ምልክት(ውሂብ.문자((Integer)ውሂብ.ቋሚ_ውሂብ[መረጃ_ጠቆመ]));
        throw new ትርጉም_ስህተት("정수와 ኅብረቁምፊ_እሴት 상수만 ድገፍ_እሴት");
    }
    String 엑스조립본(String ምዝግብ_ቦታ, List<String> 내보냄, String ዓላማ) throws IOException {
        Map<String,String> ማሽን_ሰንጠረዥ = new HashMap<>();
        for (String መስመር : Files.readAllLines(ሃብት_ዱካ.resolve("엑스기계함수.tsv"))) { String[] አገጣጥም_እሴት = መስመር.split("\t"); if (አገጣጥም_እሴት[0].equals(ዓላማ)) ማሽን_ሰንጠረዥ.put(አገጣጥም_እሴት[1] + አገጣጥም_እሴት[2],አገጣጥም_እሴት[3]); }
        int በቦታ_አስቀመጠ_መረጃ_ጠቆመ = ምዝግብ_ቦታ.lastIndexOf('.'); if (በቦታ_አስቀመጠ_መረጃ_ጠቆመ < 0) throw new ትርጉም_ስህተት("ምዝግብ_ቦታ 지정 ስህተት");
        String ባለቤት_እሴት = ምዝግብ_ቦታ.substring(0,በቦታ_አስቀመጠ_መረጃ_ጠቆመ).replace('.','/'), ስልት_ምዝግብ_ስም = ምዝግብ_ቦታ.substring(በቦታ_አስቀመጠ_መረጃ_ጠቆመ + 1); ስልት_ማጣቀሻ ምዝግብ_ቦታ_እሴት = null;
        for (String 서술 : Arrays.asList("()I","()V")) { ስልት_ማጣቀሻ ማጣቀሻ = new ስልት_ማጣቀሻ(ባለቤት_እሴት,ስልት_ምዝግብ_ስም,서술); if (함수들.containsKey(ማጣቀሻ)) { if (ምዝግብ_ቦታ_እሴት != null) throw new ትርጉም_ስህተት("겹친 ምዝግብ_ቦታ"); ምዝግብ_ቦታ_እሴት = ማጣቀሻ; } }
        if (ምዝግብ_ቦታ_እሴት == null || (함수들.get(ምዝግብ_ቦታ_እሴት).መዳረሻ_ምዝግብ & 0x100) != 0) throw new ትርጉም_ስህተት("ምዝግብ_ቦታ_እሴት ተግባር_እሴት ቅርጸት_እሴት ስህተት");
        List<String> መስመር = new ArrayList<>(); መስመር.add(".code32");
        for (መደብ_ውሂብ ውሂብ : 클래스들.values()) {
            String ዞን_እሴት = ምልክት_ad6f1a96("state",ውሂብ.ስም), ጀምር = ምልክት_ad6f1a96("init",ውሂብ.ስም);
            Collections.addAll(መስመር,".bss",".balign 4",ዞን_እሴት + ": .long 0",".text",ጀምር + ":","cmpl $0, " + ዞን_እሴት,"jne " + ጀምር + "_done","movl $1, " + ዞን_እሴት);
            ስልት_ማጣቀሻ 초기화참조 = new ስልት_ማጣቀሻ(ውሂብ.ስም,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) መስመር.add("call " + ምልክት_ad6f1a96("method",초기화참조.부분들()));
            Collections.addAll(መስመር,"movl $2, " + ዞን_እሴት,ጀምር + "_done:","ret");
            for (አባል_ውሂብ መስክ_እሴት : ውሂብ.መስክ_እሴት) {
                byte[] ቋሚ_እሴት = መስክ_እሴት.ዓይነታ_እሴት.get("ConstantValue"); String እሴት = ቋሚ_እሴት == null ? "0" : 엑스상수(ውሂብ,new ውሂብ_አንባቢ(ቋሚ_እሴት).두바이트());
                Collections.addAll(መስመር,".data",".balign 4",ምልክት_ad6f1a96("field",ውሂብ.ስም,መስክ_እሴት.ስም,መስክ_እሴት.서술) + ": .long " + እሴት);
            }
            for (አባል_ውሂብ ተግባር_እሴት : ውሂብ.ተግባር_እሴት) if (!ተግባር_እሴት.ስም.equals("<init>")) መስመር.add(엑스함수본문(new ስልት_ማጣቀሻ(ውሂብ.ስም,ተግባር_እሴት.ስም,ተግባር_እሴት.서술),ተግባር_እሴት,ማሽን_ሰንጠረዥ,ዓላማ));
        }
        Collections.addAll(መስመር,".text",".globl java_entry","java_entry:","call " + ምልክት_ad6f1a96("init",ምዝግብ_ቦታ_እሴት.ባለቤት_እሴት),"call " + ምልክት_ad6f1a96("method",ምዝግብ_ቦታ_እሴት.부분들()));
        if (ምዝግብ_ቦታ_እሴት.서술.equals("()V")) መስመር.add("xorl %eax, %eax"); መስመር.add("ret");
        for (String 지정 : 내보냄) {
            int ገዳቢ_እሴት = 지정.indexOf('='); if (ገዳቢ_እሴት < 1) throw new ትርጉም_ስህተት("내보내기 지정 ስህተት");
            String 외부 = 지정.substring(0,ገዳቢ_እሴት), ተግባር_እሴት = 지정.substring(ገዳቢ_እሴት + 1); int ማካፈል_ልኬት = ተግባር_እሴት.lastIndexOf('.');
            if (ማካፈል_ልኬት < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ትርጉም_ስህተት("내보내기 ምልክት_ad6f1a96 ስህተት");
            String መደብ_እሴት = ተግባር_እሴት.substring(0,ማካፈል_ልኬት).replace('.','/'), ስም = ተግባር_እሴት.substring(ማካፈል_ልኬት + 1); ስልት_ማጣቀሻ የተመረጠ_እሴት = null;
            for (ስልት_ማጣቀሻ ማጣቀሻ : 함수들.keySet()) if (ማጣቀሻ.ባለቤት_እሴት.equals(መደብ_እሴት) && ማጣቀሻ.ስም.equals(ስም)) { if (የተመረጠ_እሴት != null) throw new ትርጉም_ስህተት("겹친 내보내기 ዓላማ"); የተመረጠ_እሴት = ማጣቀሻ; }
            if (የተመረጠ_እሴት == null) throw new ትርጉም_ስህተት("내보낼 함수가 없음");
            Collections.addAll(መስመር,".text",".globl " + 외부,외부 + ":","call " + ምልክት_ad6f1a96("init",የተመረጠ_እሴት.ባለቤት_እሴት),"jmp " + ምልክት_ad6f1a96("method",የተመረጠ_እሴት.부분들()));
        }
        መስመር.add(".section .rodata");
        for (Map.Entry<String,String> ምዝግብ_እሴት : 문자열들.entrySet()) {
            Collections.addAll(መስመር,".balign 4",ምዝግብ_እሴት.getValue() + ":",".long " + ምዝግብ_እሴት.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char አሀዶች_እሴት : ምዝግብ_እሴት.getKey().toCharArray()) 단위들.add(Integer.toString(አሀዶች_እሴት)); if (!단위들.isEmpty()) መስመር.add(".long " + String.join(",",단위들));
        }
        መስመር.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",መስመር) + "\n";
    }
    static void ፈጽም_መሳሪያ(List<String> ትእዛዝ) throws Exception {
        if (new ProcessBuilder(ትእዛዝ).inheritIO().start().waitFor() != 0) throw new ትርጉም_ስህተት("መገንባት_ምንጭ ስህተት: " + ትእዛዝ.get(0));
    }
    static String ውሂብ_ኅብረቁምፊ(String ጽሁፍ) { return "\"" + ጽሁፍ.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String ዓላማ, String ምዝግብ_ቦታ, List<String> 내보냄, Path ውጤት, Path ሃብት_እሴት) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), መደብ_ዱካ = 임시.resolve("classes"); Files.createDirectory(መደብ_ዱካ);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",መደብ_ዱካ.toString(),"-sourcepath",መደብ_ዱካ.toString(),"-d",መደብ_ዱካ.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (ውጤት.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new ትርጉም_ስህተት("ውጤት 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new ትርጉም_ስህተት(".java 또는 .class만 ድገፍ_እሴት");
            }
            if (원문수 > 0) ፈጽም_መሳሪያ(자바명령);
            try (java.util.stream.Stream<Path> ዱካ_ዝርዝር = Files.walk(መደብ_ዱካ)) { ዱካ_ዝርዝር.filter(መተላለፊያ -> መተላለፊያ.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,ዓላማ.equals("user") ? "user" : "kernel",262144,ሃብት_እሴት);
            String 조립 = 변환.엑스조립본(ምዝግብ_ቦታ,내보냄,ዓላማ); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path መሳሪያ_በቦታ_አስቀመጠ = ሃብት_እሴት.getParent();
            ፈጽም_መሳሪያ(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            ፈጽም_መሳሪያ(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),መሳሪያ_በቦታ_አስቀመጠ.resolve("የጋራ_ቋንቋ_ማስኬጃ_ጊዜ_ድገፍ.s").toString()));
            List<String> መገናኛ = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (ዓላማ.equals("kernel")) መገናኛ.add("-r");
            else {
                ፈጽም_መሳሪያ(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),መሳሪያ_በቦታ_አስቀመጠ.resolve(ዓላማ.equals("user") ? "ጀምር_ተጠቃሚ_ፕሮግራም.s" : "리눅스시작.s").toString()));
                Collections.addAll(መገናኛ,"-e","_start",임시.resolve("start.o").toString());
                if (ዓላማ.equals("user")) Collections.addAll(መገናኛ,"-T",መሳሪያ_በቦታ_አስቀመጠ.resolve("ተጠቃሚ_አገናኝ_አሰሳ.ld").toString());
            }
            Collections.addAll(መገናኛ,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); ፈጽም_መሳሪያ(መገናኛ);
            ውጤት = ውጤት.toAbsolutePath(); Files.createDirectories(ውጤት.getParent()); Path አትም_እሴት = Files.createTempFile(ውጤት.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),አትም_እሴት,StandardCopyOption.REPLACE_EXISTING); Files.move(አትም_እሴት,ውጤት,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(አትም_እሴት); }
            Files.setPosixFilePermissions(ውጤት,java.nio.file.attribute.PosixFilePermissions.fromString(ዓላማ.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(ውጤት + ".s"),조립,StandardCharsets.UTF_8);
            List<String> ምልክት_ውሂብ = new ArrayList<>(), የምንጭ_ውሂብ = new ArrayList<>();
            for (ስልት_ማጣቀሻ ማጣቀሻ : 변환.함수들.keySet()) ምልክት_ውሂብ.add(ውሂብ_ኅብረቁምፊ(ምልክት_ad6f1a96("method",ማጣቀሻ.부분들())) + ":" + ውሂብ_ኅብረቁምፊ(ማጣቀሻ.ባለቤት_እሴት + "." + ማጣቀሻ.ስም + ማጣቀሻ.서술));
            for (Path 입력 : 입력들) {
                byte[] ሃሽ_ፋይል = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder ጽሁፍ = new StringBuilder(); for (byte እሴት : ሃሽ_ፋይል) ጽሁፍ.append(String.format(Locale.ROOT,"%02x",እሴት & 255));
                የምንጭ_ውሂብ.add(ውሂብ_ኅብረቁምፊ(입력.toAbsolutePath().toString()) + ":" + ውሂብ_ኅብረቁምፊ(ጽሁፍ.toString()));
            }
            Files.writeString(Paths.get(ውጤት + ".json"),"{\"target\":" + ውሂብ_ኅብረቁምፊ(ዓላማ) + ",\"entry\":" + ውሂብ_ኅብረቁምፊ(ምዝግብ_ቦታ) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",ምልክት_ውሂብ) + "},\"sources\":{" + String.join(",",የምንጭ_ውሂብ) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> ዱካ_ዝርዝር = Files.walk(임시)) { for (Path መተላለፊያ : (Iterable<Path>)ዱካ_ዝርዝር.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(መተላለፊያ); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String ምዝግብ_ቦታ = null, ዓላማ = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> ዱካ_ዝርዝር = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String እሴት = 인수[순번];
                switch (እሴት) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry መደብ_እሴት.ተግባር_እሴት -o ውጤት [--target linux|kernel|user] [--profile kernel|user] [--export ምልክት_ad6f1a96=መደብ_እሴት.ተግባር_እሴት] 클래스파일 또는 Java원문"); return;
                    case "--entry": ምዝግብ_ቦታ = 인수[++순번]; break;
                    case "--profile": ዓላማ = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (እሴት.startsWith("-")) throw new ትርጉም_ስህተት("알 수 없는 옵션: " + እሴት); ዱካ_ዝርዝር.add(Paths.get(እሴት));
                }
            }
            if (ምዝግብ_ቦታ == null || 출력경로 == null || ዱካ_ዝርዝር.isEmpty()) throw new ትርጉም_ስህተት("--entry, -o, መደብ_እሴት 파일이 필요합니다");
            Path ሃብት_እሴት = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new ትርጉም_ስህተት("알 수 없는 ፈጽም_ትእዛዝ ዓላማ");
                엑스번역(ዱካ_ዝርዝር,엑스대상,ምዝግብ_ቦታ,내보냄,출력경로,ሃብት_እሴት); return;
            }
            String ምንጭ = new 기계어미리번역(ዱካ_ዝርዝር, ዓላማ, 낱말수, ሃብት_እሴት).አዘጋጅ(ምዝግብ_ቦታ, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ምንጭ, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception ስህተት) { System.err.println("መገንባት_ምንጭ ስህተት: " + ስህተት.getMessage()); System.exit(1); }
    }
}
