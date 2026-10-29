// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java ክፍሊ_ዋጋ 파일에서 독립 ARM64 커널용 C 원문을 만든다. አዐንግድ JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class ትርጉም_ጌጋ extends RuntimeException {
        ትርጉም_ጌጋ(String 설명) { super(설명); }
    }
    static final class ሓበሬታ_ኣንባቢ {
        final byte[] ሓበሬታ;
        int 위치;
        ሓበሬታ_ኣንባቢ(byte[] 입력자료) { ሓበሬታ = 입력자료; }
        byte[] 읽기(int ንውሓት_ዋጋ) {
            if (ንውሓት_ዋጋ < 0 || ንውሓት_ዋጋ > ሓበሬታ.length - 위치) throw new ትርጉም_ጌጋ("잘린 ክፍሊ_ዋጋ 또는 ትእዛዝ ሓበሬታ");
            byte[] 결과 = Arrays.copyOfRange(ሓበሬታ, 위치, 위치 + ንውሓት_ዋጋ); 위치 += ንውሓት_ዋጋ; return 결과;
        }
        int 한바이트() { if (위치 >= ሓበሬታ.length) throw new ትርጉም_ጌጋ("잘린 ትእዛዝ ሓበሬታ"); return ሓበሬታ[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class አባል_ሓበሬታ {
        final int ፍቓድ_ምእታው;
        final String ሽም, 서술;
        final Map<String, byte[]> ባህሪ_ዋጋ;
        አባል_ሓበሬታ(int ፍቓድ_ዋጋ_2dd0017b, String ሽም_ዋጋ, String 서술값, Map<String, byte[]> ባህሪ_ሓበሬታ) {
            ፍቓድ_ምእታው = ፍቓድ_ዋጋ_2dd0017b; ሽም = ሽም_ዋጋ; 서술 = 서술값; ባህሪ_ዋጋ = ባህሪ_ሓበሬታ;
        }
    }
    static final class ሜላ_መወከሲ implements Comparable<ሜላ_መወከሲ> {
        final String ወናኒ_ዋጋ, ሽም, 서술;
        ሜላ_መወከሲ(String 소유값, String ሽም_ዋጋ, String 서술값) { ወናኒ_ዋጋ = 소유값; ሽም = ሽም_ዋጋ; 서술 = 서술값; }
        String[] 부분들() { return new String[]{ወናኒ_ዋጋ, ሽም, 서술}; }
        public int compareTo(ሜላ_መወከሲ መዘና_ዋጋ) {
            int 비교값 = ወናኒ_ዋጋ.compareTo(መዘና_ዋጋ.ወናኒ_ዋጋ);
            if (비교값 == 0) 비교값 = ሽም.compareTo(መዘና_ዋጋ.ሽም);
            return 비교값 == 0 ? 서술.compareTo(መዘና_ዋጋ.서술) : 비교값;
        }
        public boolean equals(Object መዘና_ዋጋ) { return መዘና_ዋጋ instanceof ሜላ_መወከሲ && compareTo((ሜላ_መወከሲ) መዘና_ዋጋ) == 0; }
        public int hashCode() { return Objects.hash(ወናኒ_ዋጋ, ሽም, 서술); }
    }
    static final class ክፍሊ_ሓበሬታ {
        final int[] 상수종류;
        final Object[] መረራኽቦ_ሓበሬታ;
        final String ሽም;
        final List<አባል_ሓበሬታ> ሜዳ_ዋጋ, ተግባር_ዋጋ;
        ክፍሊ_ሓበሬታ(Path መገዲ) throws IOException {
            ሓበሬታ_ኣንባቢ ኣንባቢ_ዋጋ = new ሓበሬታ_ኣንባቢ(Files.readAllBytes(መገዲ));
            if (ኣንባቢ_ዋጋ.네바이트() != 0xcafebabe) throw new ትርጉም_ጌጋ("Java ክፍሊ_ዋጋ 표식이 아님");
            ኣንባቢ_ዋጋ.읽기(4);
            int 개수 = ኣንባቢ_ዋጋ.두바이트(); 상수종류 = new int[개수]; መረራኽቦ_ሓበሬታ = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = ኣንባቢ_ዋጋ.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int ንውሓት_ዋጋ = ኣንባቢ_ዋጋ.두바이트();
                        byte[] ፊደል_መዕቖሪ_ማህደር = ኣንባቢ_ዋጋ.읽기(ንውሓት_ዋጋ), 길이붙인자료 = new byte[ንውሓት_ዋጋ + 2];
                        길이붙인자료[0] = (byte)(ንውሓት_ዋጋ >> 8); 길이붙인자료[1] = (byte)ንውሓት_ዋጋ;
                        System.arraycopy(ፊደል_መዕቖሪ_ማህደር, 0, 길이붙인자료, 2, ንውሓት_ዋጋ);
                        መረራኽቦ_ሓበሬታ[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: መረራኽቦ_ሓበሬታ[순번] = ኣንባቢ_ዋጋ.네바이트(); break;
                    case 4: ኣንባቢ_ዋጋ.읽기(4); break;
                    case 5: case 6: ኣንባቢ_ዋጋ.읽기(8); 순번++; break;
                    case 7: case 8: case 16: መረራኽቦ_ሓበሬታ[순번] = ኣንባቢ_ዋጋ.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        መረራኽቦ_ሓበሬታ[순번] = new int[]{ኣንባቢ_ዋጋ.두바이트(), ኣንባቢ_ዋጋ.두바이트()}; break;
                    case 15: መረራኽቦ_ሓበሬታ[순번] = new int[]{ኣንባቢ_ዋጋ.한바이트(), ኣንባቢ_ዋጋ.두바이트()}; break;
                    default: throw new ትርጉም_ጌጋ("지원하지 않는 መረራኽቦ_ዋጋ 종류: " + 종류);
                }
            }
            ኣንባቢ_ዋጋ.두바이트(); ሽም = ክፍሊ_ሽም(ኣንባቢ_ዋጋ.두바이트());
            if (!ክፍሊ_ሽም(ኣንባቢ_ዋጋ.두바이트()).equals("java/lang/Object") || ኣንባቢ_ዋጋ.두바이트() != 0)
                throw new ትርጉም_ጌጋ(ሽም + ": 상속 및 인터페이스 미지원");
            ሜዳ_ዋጋ = 멤버읽기(ኣንባቢ_ዋጋ); ተግባር_ዋጋ = 멤버읽기(ኣንባቢ_ዋጋ); 속성읽기(ኣንባቢ_ዋጋ);
            if (ኣንባቢ_ዋጋ.위치 != ኣንባቢ_ዋጋ.ሓበሬታ.length) throw new ትርጉም_ጌጋ("ክፍሊ_ዋጋ 뒤에 남은 ሓበሬታ");
        }
        String 문자(int መሐበሪ) {
            if (መሐበሪ < 1 || መሐበሪ >= 상수종류.length || 상수종류[መሐበሪ] != 1) throw new ትርጉም_ጌጋ("문자 መረራኽቦ_ዋጋ መሐበሪ ጌጋ");
            return (String) መረራኽቦ_ሓበሬታ[መሐበሪ];
        }
        String ክፍሊ_ሽም(int መሐበሪ) {
            if (መሐበሪ < 1 || መሐበሪ >= 상수종류.length || 상수종류[መሐበሪ] != 7) throw new ትርጉም_ጌጋ("ክፍሊ_ዋጋ መወከሲ ጌጋ");
            return 문자((Integer)መረራኽቦ_ሓበሬታ[መሐበሪ]);
        }
        ሜላ_መወከሲ መወከሲ(int መሐበሪ) {
            if (መሐበሪ < 1 || መሐበሪ >= 상수종류.length || 상수종류[መሐበሪ] < 9 || 상수종류[መሐበሪ] > 11) throw new ትርጉም_ጌጋ("멤버 መወከሲ ጌጋ");
            int[] ኣጻምድ_ዋጋ = (int[])መረራኽቦ_ሓበሬታ[መሐበሪ], ሽም_ኣጻምድ = (int[])መረራኽቦ_ሓበሬታ[ኣጻምድ_ዋጋ[1]];
            return new ሜላ_መወከሲ(ክፍሊ_ሽም(ኣጻምድ_ዋጋ[0]), 문자(ሽም_ኣጻምድ[0]), 문자(ሽም_ኣጻምድ[1]));
        }
        Map<String, byte[]> 속성읽기(ሓበሬታ_ኣንባቢ ኣንባቢ_ዋጋ) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = ኣንባቢ_ዋጋ.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String ባህሪ_ሽም = 문자(ኣንባቢ_ዋጋ.두바이트()); byte[] ዋጋ = ኣንባቢ_ዋጋ.읽기(ኣንባቢ_ዋጋ.네바이트());
                if (결과.put(ባህሪ_ሽም, ዋጋ) != null) throw new ትርጉም_ጌጋ("겹친 ባህሪ_ዋጋ: " + ባህሪ_ሽም);
            }
            return 결과;
        }
        List<አባል_ሓበሬታ> 멤버읽기(ሓበሬታ_ኣንባቢ ኣንባቢ_ዋጋ) {
            List<አባል_ሓበሬታ> 결과 = new ArrayList<>(); int 개수 = ኣንባቢ_ዋጋ.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int ፍቓድ_ምእታው = ኣንባቢ_ዋጋ.두바이트(); String ሜላ_ምእታው_ሽም = 문자(ኣንባቢ_ዋጋ.두바이트()), 서술 = 문자(ኣንባቢ_ዋጋ.두바이트());
                결과.add(new አባል_ሓበሬታ(ፍቓድ_ምእታው, ሜላ_ምእታው_ሽም, 서술, 속성읽기(ኣንባቢ_ዋጋ)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new ትርጉም_ጌጋ("ተግባር_ዋጋ 서술 ጌጋ: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new ትርጉም_ጌጋ("ተግባር_ዋጋ 서술 ጌጋ: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new ትርጉም_ጌጋ("ተግባር_ዋጋ 서술 ጌጋ: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String ምሩጽ_ዋጋ = null;
            for (String ቅረጽ_ዋጋ : 허용형식) if (서술.startsWith(ቅረጽ_ዋጋ, 위치)) { ምሩጽ_ዋጋ = ቅረጽ_ዋጋ; break; }
            if (ምሩጽ_ዋጋ == null) throw new ትርጉም_ጌጋ("지원하지 않는 ናይ_ሓበሬታ_ዓይነት: " + 서술);
            결과.add(ምሩጽ_ዋጋ); 위치 += ምሩጽ_ዋጋ.length();
        }
        return 결과;
    }
    static String ምልክት(String 종류, String... 부분들) {
        try {
            byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder ጽሑፍ = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) ጽሑፍ.append(String.format(Locale.ROOT, "%02x", 해시[순번] & 255));
            return ጽሑፍ.toString();
        } catch (Exception ጌጋ) { throw new ትርጉም_ጌጋ(ጌጋ.toString()); }
    }
    final Map<String, ክፍሊ_ሓበሬታ> 클래스들 = new TreeMap<>();
    final Map<ሜላ_መወከሲ, አባል_ሓበሬታ> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, ማሽን_ክፍሊ;
    final int 동적기억낱말수;
    final Path ሃብቲ_መገዲ;
    기계어미리번역(List<Path> መገዲ_ዝርዝር, String ዕላማ, int 낱말수, Path ሃብቲ_ዋጋ) throws IOException {
        if ((!ዕላማ.equals("kernel") && !ዕላማ.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new ትርጉም_ጌጋ("ተግብር_ትእዛዝ ዕላማ 또는 ማህደር_ዝኽረት_ዋጋ 공간 መጠን ጌጋ");
        실행대상 = ዕላማ; 동적기억낱말수 = 낱말수; ሃብቲ_መገዲ = ሃብቲ_ዋጋ;
        // 이 이름도 국가별 ምንጪ_ገረብ 생성 시 해당 언어로 옮긴다.
        ማሽን_ክፍሊ = ዕላማ.equals("kernel") ? "보드" : "ተጠቃሚ";
        for (String መስመር : Files.readAllLines(ሃብቲ_ዋጋ.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = መስመር.split("\t", -1);
            if (부분들.length != 4) throw new ትርጉም_ጌጋ("ማሽን ተግባር_ዋጋ ሓበሬታ ጌጋ");
            if (부분들[0].equals(ዕላማ)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path መገዲ : መገዲ_ዝርዝር) {
            ክፍሊ_ሓበሬታ ሓበሬታ = new ክፍሊ_ሓበሬታ(መገዲ);
            if (클래스들.put(ሓበሬታ.ሽም, ሓበሬታ) != null) throw new ትርጉም_ጌጋ("중복 ክፍሊ_ዋጋ: " + ሓበሬታ.ሽም);
            for (አባል_ሓበሬታ ሜዳ_ዋጋ : ሓበሬታ.ሜዳ_ዋጋ) {
                if ((ሜዳ_ዋጋ.ፍቓድ_ምእታው & 8) == 0 || 형식읽기(ሜዳ_ዋጋ.서술).equals(Collections.singletonList("V"))) throw new ትርጉም_ጌጋ("ቀዋሚ_ዋጋ 필드만 ሓገዝ_ዋጋ");
                if (필드들.put(new ሜላ_መወከሲ(ሓበሬታ.ሽም, ሜዳ_ዋጋ.ሽም, ሜዳ_ዋጋ.서술), ሜዳ_ዋጋ) != null) throw new ትርጉም_ጌጋ("중복 ሜዳ_ዋጋ");
            }
            for (አባል_ሓበሬታ ተግባር_ዋጋ : ሓበሬታ.ተግባር_ዋጋ) {
                if (ተግባር_ዋጋ.ሽም.equals("<init>")) continue;
                if ((ተግባር_ዋጋ.ፍቓድ_ምእታው & 8) == 0 || (ተግባር_ዋጋ.ፍቓድ_ምእታው & (0x20 | 0x400)) != 0) throw new ትርጉም_ጌጋ("ቀዋሚ_ዋጋ 비동기화 함수만 ሓገዝ_ዋጋ");
                new 함수형식(ተግባር_ዋጋ.서술);
                if (함수들.put(new ሜላ_መወከሲ(ሓበሬታ.ሽም, ተግባር_ዋጋ.ሽም, ተግባር_ዋጋ.서술), ተግባር_ዋጋ) != null) throw new ትርጉም_ጌጋ("중복 ተግባር_ዋጋ");
            }
        }
    }
    String ሕብረ_ቁምፊ_ምልክት(String ጽሑፍ) { return 문자열들.computeIfAbsent(ጽሑፍ, ዋጋ -> "j_text_" + 문자열들.size()); }
    String መረራኽቦ_ሓረግ_ሒሳብ(ክፍሊ_ሓበሬታ ሓበሬታ, int መሐበሪ) {
        if (መሐበሪ < 1 || መሐበሪ >= ሓበሬታ.상수종류.length) throw new ትርጉም_ጌጋ("መረራኽቦ_ዋጋ መሐበሪ ቅንጣብ ጌጋ");
        if (ሓበሬታ.상수종류[መሐበሪ] == 3) return "(word)(uint32_t)(" + ሓበሬታ.መረራኽቦ_ሓበሬታ[መሐበሪ] + ")";
        if (ሓበሬታ.상수종류[መሐበሪ] == 8) return "(word)" + ሕብረ_ቁምፊ_ምልክት(ሓበሬታ.문자((Integer)ሓበሬታ.መረራኽቦ_ሓበሬታ[መሐበሪ]));
        throw new ትርጉም_ጌጋ("정수와 ሕብረ_ቁምፊ_ዋጋ 상수만 ሓገዝ_ዋጋ");
    }
    String 함수원형(ሜላ_መወከሲ መወከሲ) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(መወከሲ.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + ምልክት("method", መወከሲ.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void ፈትሽ_ኣካባብያዊ(int መሐበሪ, int 지역변수수) { if (መሐበሪ < 0 || መሐበሪ >= 지역변수수) throw new ትርጉም_ጌጋ("ኣካባብያዊ_ዕምቆት 변수 መሐበሪ ቅንጣብ ጌጋ"); }
    void 분기넣기(List<String> 출력, Set<Integer> ጨንፈር_ዝርዝር, int 위치, int 이동량, String ኩነታት) {
        int መዓልቦ_ዋጋ = 위치 + 이동량; ጨንፈር_ዝርዝር.add(መዓልቦ_ዋጋ);
        출력.add((ኩነታት == null ? "" : "if (" + ኩነታት + ") ") + "goto b" + መዓልቦ_ዋጋ + ";");
    }
    String 함수본문(ሜላ_መወከሲ ተግባር_ዋጋ, አባል_ሓበሬታ ሓበሬታ) {
        byte[] 본문자료 = ሓበሬታ.ባህሪ_ዋጋ.get("Code"); if (본문자료 == null) throw new ትርጉም_ጌጋ("ተግባር_ዋጋ 몸체가 없음: " + ተግባር_ዋጋ.ሽም);
        ሓበሬታ_ኣንባቢ ኣንባቢ_ዋጋ = new ሓበሬታ_ኣንባቢ(본문자료); int 쌓임깊이 = ኣንባቢ_ዋጋ.두바이트(), 지역변수수 = ኣንባቢ_ዋጋ.두바이트();
        ሓበሬታ_ኣንባቢ ትእዛዝ_ሓበሬታ = new ሓበሬታ_ኣንባቢ(ኣንባቢ_ዋጋ.읽기(ኣንባቢ_ዋጋ.네바이트()));
        if (ኣንባቢ_ዋጋ.두바이트() != 0) throw new ትርጉም_ጌጋ("try/catch/finally 미지원");
        함수형식 ቅረጽ_ዋጋ = new 함수형식(ተግባር_ዋጋ.서술); if (지역변수수 < ቅረጽ_ዋጋ.인수.size()) throw new ትርጉም_ጌጋ("매개변수보다 적은 ኣካባብያዊ_ዕምቆት 변수");
        ክፍሊ_ሓበሬታ ክፍሊ_ዋጋ = 클래스들.get(ተግባር_ዋጋ.ወናኒ_ዋጋ);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(ተግባር_ዋጋ) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < ቅረጽ_ዋጋ.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ጨንፈር_ዝርዝር = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (ትእዛዝ_ሓበሬታ.위치 < ትእዛዝ_ሓበሬታ.ሓበሬታ.length) {
            int 위치 = ትእዛዝ_ሓበሬታ.위치, ትእዛዝ = ትእዛዝ_ሓበሬታ.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (ትእዛዝ == 0) continue;
            if (ትእዛዝ == 1) 출력.add("PUSH(0);");
            else if (ትእዛዝ >= 2 && ትእዛዝ <= 8) 출력.add("PUSH((uint32_t)(" + (ትእዛዝ - 3) + "));");
            else if (ትእዛዝ == 16 || ትእዛዝ == 17) 출력.add("PUSH((uint32_t)(" + (ትእዛዝ == 16 ? ትእዛዝ_ሓበሬታ.부호한바이트() : ትእዛዝ_ሓበሬታ.부호두바이트()) + "));");
            else if (ትእዛዝ == 18 || ትእዛዝ == 19) 출력.add("PUSH(" + መረራኽቦ_ሓረግ_ሒሳብ(ክፍሊ_ዋጋ, ትእዛዝ == 18 ? ትእዛዝ_ሓበሬታ.한바이트() : ትእዛዝ_ሓበሬታ.두바이트()) + ");");
            else if (ትእዛዝ == 21 || ትእዛዝ == 25 || (ትእዛዝ >= 26 && ትእዛዝ <= 29) || (ትእዛዝ >= 42 && ትእዛዝ <= 45)) {
                int መሐበሪ = ትእዛዝ == 21 || ትእዛዝ == 25 ? ትእዛዝ_ሓበሬታ.한바이트() : ትእዛዝ - (ትእዛዝ <= 29 ? 26 : 42);
                ፈትሽ_ኣካባብያዊ(መሐበሪ, 지역변수수); 출력.add("PUSH(l[" + መሐበሪ + "]);");
            } else if (ትእዛዝ == 54 || ትእዛዝ == 58 || (ትእዛዝ >= 59 && ትእዛዝ <= 62) || (ትእዛዝ >= 75 && ትእዛዝ <= 78)) {
                int መሐበሪ = ትእዛዝ == 54 || ትእዛዝ == 58 ? ትእዛዝ_ሓበሬታ.한바이트() : ትእዛዝ - (ትእዛዝ <= 62 ? 59 : 75);
                ፈትሽ_ኣካባብያዊ(መሐበሪ, 지역변수수); 출력.add("l[" + መሐበሪ + "] = POP();");
            } else if (ትእዛዝ == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (ትእዛዝ == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (ትእዛዝ == 87 || ትእዛዝ == 88) 출력.add(ትእዛዝ == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (ትእዛዝ >= 89 && ትእዛዝ <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ተርታ_ዝርዝር = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[ትእዛዝ - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char ዋጋ : ተርታ_ዝርዝር[ትእዛዝ - 89].toCharArray()) 출력.add("PUSH(" + ዋጋ + ");");
            } else if (ትእዛዝ == 96 || ትእዛዝ == 100 || ትእዛዝ == 104 || ትእዛዝ == 126 || ትእዛዝ == 128 || ትእዛዝ == 130) {
                String ስርሒት_ዋጋ = ትእዛዝ == 96 ? "+" : ትእዛዝ == 100 ? "-" : ትእዛዝ == 104 ? "*" : ትእዛዝ == 126 ? "&" : ትእዛዝ == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + ስርሒት_ዋጋ + " (uint32_t)b);");
            } else if (ትእዛዝ == 108 || ትእዛዝ == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (ትእዛዝ == 112 ? 1 : 0) + "));");
            else if (ትእዛዝ == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (ትእዛዝ == 120 || ትእዛዝ == 122 || ትእዛዝ == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (ትእዛዝ == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (ትእዛዝ == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (ትእዛዝ == 132) {
                int መሐበሪ = ትእዛዝ_ሓበሬታ.한바이트(), 증가량 = ትእዛዝ_ሓበሬታ.부호한바이트(); ፈትሽ_ኣካባብያዊ(መሐበሪ, 지역변수수);
                출력.add("l[" + መሐበሪ + "] = (uint32_t)l[" + መሐበሪ + "] + (uint32_t)(" + 증가량 + ");");
            } else if (ትእዛዝ >= 145 && ትእዛዝ <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (ትእዛዝ == 145 ? "int8_t" : ትእዛዝ == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (ትእዛዝ >= 153 && ትእዛዝ <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, ጨንፈር_ዝርዝር, 위치, ትእዛዝ_ሓበሬታ.부호두바이트(), "(int32_t)a " + 비교들[ትእዛዝ - 153] + " 0");
            } else if (ትእዛዝ >= 159 && ትእዛዝ <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, ጨንፈር_ዝርዝር, 위치, ትእዛዝ_ሓበሬታ.부호두바이트(), ትእዛዝ >= 165 ? "a " + 비교들[ትእዛዝ - 159] + " b" : "(int32_t)a " + 비교들[ትእዛዝ - 159] + " (int32_t)b");
            } else if (ትእዛዝ == 167 || ትእዛዝ == 200) 분기넣기(출력, ጨንፈር_ዝርዝር, 위치, ትእዛዝ == 167 ? ትእዛዝ_ሓበሬታ.부호두바이트() : ትእዛዝ_ሓበሬታ.네바이트(), null);
            else if (ትእዛዝ == 170 || ትእዛዝ == 171) {
                while (ትእዛዝ_ሓበሬታ.위치 % 4 != 0) ትእዛዝ_ሓበሬታ.한바이트();
                int ንቡር_ዋጋ = ትእዛዝ_ሓበሬታ.네바이트(); 출력.add("a = POP();");
                if (ትእዛዝ == 170) {
                    int 아래 = ትእዛዝ_ሓበሬታ.네바이트(), 위 = ትእዛዝ_ሓበሬታ.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (ትእዛዝ_ሓበሬታ.ሓበሬታ.length - ትእዛዝ_ሓበሬታ.위치) / 4) throw new ትርጉም_ጌጋ("switch ቅንጣብ ጌጋ");
                    for (long ዋጋ = 아래; ዋጋ <= 위; ዋጋ++) 분기넣기(출력, ጨንፈር_ዝርዝር, 위치, ትእዛዝ_ሓበሬታ.네바이트(), "(int32_t)a == (" + ዋጋ + ")");
                } else {
                    int 개수 = ትእዛዝ_ሓበሬታ.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (ትእዛዝ_ሓበሬታ.ሓበሬታ.length - ትእዛዝ_ሓበሬታ.위치) / 8) throw new ትርጉም_ጌጋ("switch መጠን ጌጋ");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int ዋጋ = ትእዛዝ_ሓበሬታ.네바이트(); if (순번 > 0 && ዋጋ <= 앞값) throw new ትርጉም_ጌጋ("switch ተርታ_ዋጋ ጌጋ"); 앞값 = ዋጋ;
                        분기넣기(출력, ጨንፈር_ዝርዝር, 위치, ትእዛዝ_ሓበሬታ.네바이트(), "(int32_t)a == (" + ዋጋ + ")");
                    }
                }
                분기넣기(출력, ጨንፈር_ዝርዝር, 위치, ንቡር_ዋጋ, null);
            } else if (ትእዛዝ == 172 || ትእዛዝ == 176 || ትእዛዝ == 177) 출력.add("return " + (ትእዛዝ == 177 ? "0" : "POP()") + ";");
            else if (ትእዛዝ == 178 || ትእዛዝ == 179) {
                ሜላ_መወከሲ መወከሲ = ክፍሊ_ዋጋ.መወከሲ(ትእዛዝ_ሓበሬታ.두바이트()); if (!필드들.containsKey(መወከሲ)) throw new ትርጉም_ጌጋ("알 수 없는 ሜዳ_ዋጋ");
                출력.add(ምልክት("init", መወከሲ.ወናኒ_ዋጋ) + "();"); String ሜዳ_ዋጋ = ምልክት("field", መወከሲ.부분들());
                출력.add(ትእዛዝ == 178 ? "PUSH(" + ሜዳ_ዋጋ + ");" : ሜዳ_ዋጋ + " = POP();");
            } else if (ትእዛዝ == 184) {
                ሜላ_መወከሲ መወከሲ = ክፍሊ_ዋጋ.መወከሲ(ትእዛዝ_ሓበሬታ.두바이트()); if (!함수들.containsKey(መወከሲ)) throw new ትርጉም_ጌጋ("알 수 없는 ተግባር_ዋጋ");
                함수형식 호출형식 = new 함수형식(መወከሲ.서술); int 개수 = 호출형식.인수.size();
                출력.add(ምልክት("init", መወከሲ.ወናኒ_ዋጋ) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + ምልክት("method", መወከሲ.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (ትእዛዝ == 182) {
                ሜላ_መወከሲ መወከሲ = ክፍሊ_ዋጋ.መወከሲ(ትእዛዝ_ሓበሬታ.두바이트());
                if (መወከሲ.equals(new ሜላ_መወከሲ("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (መወከሲ.equals(new ሜላ_መወከሲ("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new ትርጉም_ጌጋ("가상 ተግባር_ዋጋ 호출 미지원");
            } else if (ትእዛዝ == 188) {
                if (ትእዛዝ_ሓበሬታ.한바이트() != 10) throw new ትርጉም_ጌጋ("new int[]만 ሓገዝ_ዋጋ"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (ትእዛዝ == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (ትእዛዝ == 196) {
                int ቅጥያ_ዋጋ = ትእዛዝ_ሓበሬታ.한바이트(), መሐበሪ = ትእዛዝ_ሓበሬታ.두바이트(); ፈትሽ_ኣካባብያዊ(መሐበሪ, 지역변수수);
                if (ቅጥያ_ዋጋ == 21 || ቅጥያ_ዋጋ == 25) 출력.add("PUSH(l[" + መሐበሪ + "]);");
                else if (ቅጥያ_ዋጋ == 54 || ቅጥያ_ዋጋ == 58) 출력.add("l[" + መሐበሪ + "] = POP();");
                else if (ቅጥያ_ዋጋ == 132) 출력.add("l[" + መሐበሪ + "] = (uint32_t)l[" + መሐበሪ + "] + (uint32_t)(" + ትእዛዝ_ሓበሬታ.부호두바이트() + ");");
                else throw new ትርጉም_ጌጋ("미지원 wide ትእዛዝ");
            } else if (ትእዛዝ == 198 || ትእዛዝ == 199) {
                출력.add("a = POP();"); 분기넣기(출력, ጨንፈር_ዝርዝር, 위치, ትእዛዝ_ሓበሬታ.부호두바이트(), "a " + (ትእዛዝ == 198 ? "==" : "!=") + " 0");
            } else throw new ትርጉም_ጌጋ(ተግባር_ዋጋ.ወናኒ_ዋጋ + "." + ተግባር_ዋጋ.ሽም + ", ባይት_ዋጋ " + 위치 + ": 미지원 ትእዛዝ " + ትእዛዝ);
        }
        if (!경계들.containsAll(ጨንፈር_ዝርዝር)) throw new ትርጉም_ጌጋ("ትእዛዝ 경계가 아닌 곳으로 ጨንፈር");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String ስደድ_ሜላ(String መጋጠሚ_ምልክት, String ዕላማ, boolean 진입점여부) {
        int 자리 = ዕላማ.lastIndexOf('.'); if (자리 < 0 || !መጋጠሚ_ምልክት.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ትርጉም_ጌጋ("내보내기 지정 ጌጋ");
        String ወናኒ_ዋጋ = ዕላማ.substring(0, 자리).replace('.', '/'), ሽም = ዕላማ.substring(자리 + 1); ሜላ_መወከሲ ምሩጽ_ዋጋ = null;
        for (ሜላ_መወከሲ መወከሲ : 함수들.keySet()) if (መወከሲ.ወናኒ_ዋጋ.equals(ወናኒ_ዋጋ) && መወከሲ.ሽም.equals(ሽም)) {
            if (ምሩጽ_ዋጋ != null) throw new ትርጉም_ጌጋ("겹친 내보내기 ዕላማ"); ምሩጽ_ዋጋ = መወከሲ;
        }
        if (ምሩጽ_ዋጋ == null || (함수들.get(ምሩጽ_ዋጋ).ፍቓድ_ምእታው & 0x100) != 0) throw new ትርጉም_ጌጋ("내보낼 함수가 없음 또는 native ተግባር_ዋጋ");
        함수형식 ቅረጽ_ዋጋ = new 함수형식(ምሩጽ_ዋጋ.서술);
        if ((진입점여부 && !ቅረጽ_ዋጋ.인수.isEmpty()) || !Arrays.asList("V", "I").contains(ቅረጽ_ዋጋ.반환)) throw new ትርጉም_ጌጋ("ምእታው_ነጥቢ_ዋጋ 또는 C 경계 ቅረጽ_ዋጋ ጌጋ");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < ቅረጽ_ዋጋ.인수.size(); 순번++) {
            if (!ቅረጽ_ዋጋ.인수.get(순번).equals("I")) throw new ትርጉም_ጌጋ("C 경계는 int 인수만 ሓገዝ_ዋጋ");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (ቅረጽ_ዋጋ.반환.equals("V") ? "void " : "int32_t ") + መጋጠሚ_ምልክት + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + ምልክት("init", ምሩጽ_ዋጋ.ወናኒ_ዋጋ) + "(); " + (ቅረጽ_ዋጋ.반환.equals("V") ? "" : "return (int32_t)") + ምልክት("method", ምሩጽ_ዋጋ.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String ምእታው_ነጥቢ, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<ሜላ_መወከሲ, አባል_ሓበሬታ> ምእታው_ዋጋ : 함수들.entrySet()) {
            ሜላ_መወከሲ መወከሲ = ምእታው_ዋጋ.getKey(); አባል_ሓበሬታ ሓበሬታ = ምእታው_ዋጋ.getValue(); 선언들.add(함수원형(መወከሲ) + ";");
            if ((ሓበሬታ.ፍቓድ_ምእታው & 0x100) != 0) {
                String ኣላግብ = 기계함수들.get(መወከሲ.ሽም + መወከሲ.서술);
                if (!መወከሲ.ወናኒ_ዋጋ.equals(ማሽን_ክፍሊ) || ኣላግብ == null) throw new ትርጉም_ጌጋ("허용되지 않은 native ተግባር_ዋጋ: " + መወከሲ.ሽም);
                int 개수 = new 함수형식(መወከሲ.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + ኣላግብ + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(መወከሲ) + " { return " + ኣላግብ + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(መወከሲ, ሓበሬታ));
        }
        for (Map.Entry<ሜላ_መወከሲ, አባል_ሓበሬታ> ምእታው_ዋጋ : 필드들.entrySet()) {
            ሜላ_መወከሲ መወከሲ = ምእታው_ዋጋ.getKey(); byte[] መረራኽቦ_ዋጋ = ምእታው_ዋጋ.getValue().ባህሪ_ዋጋ.get("ConstantValue");
            String ዋጋ = መረራኽቦ_ዋጋ == null ? "0" : መረራኽቦ_ሓረግ_ሒሳብ(클래스들.get(መወከሲ.ወናኒ_ዋጋ), new ሓበሬታ_ኣንባቢ(መረራኽቦ_ዋጋ).두바이트());
            필드선언들.add("static word " + ምልክት("field", መወከሲ.부분들()) + " = " + ዋጋ + ";");
        }
        for (String ሽም : 클래스들.keySet()) {
            String ኣተስእ = ምልክት("init", ሽም), ደረጃ_ዋጋ = ምልክት("state", ሽም);
            선언들.add("static void " + ኣተስእ + "(void);"); 필드선언들.add("static unsigned " + ደረጃ_ዋጋ + ";");
            ሜላ_መወከሲ መወከሲ = new ሜላ_መወከሲ(ሽም, "<clinit>", "()V");
            몸체들.add("static void " + ኣተስእ + "(void) { if(" + ደረጃ_ዋጋ + ") return; " + ደረጃ_ዋጋ + " = 1; " + (함수들.containsKey(መወከሲ) ? ምልክት("method", መወከሲ.부분들()) + "(); " : "") + ደረጃ_ዋጋ + " = 2; }");
        }
        몸체들.add(ስደድ_ሜላ("java_entry", ምእታው_ነጥቢ, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new ትርጉም_ጌጋ("내보내기 지정 ጌጋ");
            String ሽም = 지정.substring(0, 자리); 공개이름.add(ሽም); 몸체들.add(ስደድ_ሜላ(ሽም, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> ምእታው_ዋጋ : 문자열들.entrySet()) {
            String ጽሑፍ = ምእታው_ዋጋ.getKey(); StringBuilder ተርታ_ዋጋ_ed437109 = new StringBuilder("static const word " + ምእታው_ዋጋ.getValue() + "[] = {" + ጽሑፍ.length());
            for (int 순번 = 0; 순번 < ጽሑፍ.length(); 순번++) ተርታ_ዋጋ_ed437109.append(", ").append((int)ጽሑፍ.charAt(순번));
            문자열선언들.add(ተርታ_ዋጋ_ed437109.append("};").toString());
        }
        String ሓገዝ_ዋጋ = Files.readString(ሃብቲ_መገዲ.resolve("ግዜ_ስራሕ_ናይ_ሓባር_ቛንቛ_ሓገዝ.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(ሓገዝ_ዋጋ + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ምንጪ, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ሽም_ሰሌዳ = new HashMap<>();
        for (String መስመር : Files.readAllLines(ሃብቲ_መገዲ.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] ኣጻምድ_ዋጋ = መስመር.split("\t"); ሽም_ሰሌዳ.put(ኣጻምድ_ዋጋ[0], ኣጻምድ_ዋጋ[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(ምንጪ); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String ሽም = 찾개.group(), 새이름 = ሽም;
            if (!ሽም.startsWith("//") && !ሽም.startsWith("/*") && !ሽም.startsWith("\"") && !ሽም.startsWith("'") && !공개이름.contains(ሽም)) {
                새이름 = ሽም_ሰሌዳ.getOrDefault(ሽም, ሽም);
                if (ሽም.matches("a[0-9]+")) 새이름 = "인수" + ሽም.substring(1);
                if (ሽም.matches("b[0-9]+")) 새이름 = "ጨንፈር" + ሽም.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char ፊደል_ዋጋ : 새이름.toCharArray()) 표기.append(ፊደል_ዋጋ < 128 ? Character.toString(ፊደል_ዋጋ) : String.format(Locale.ROOT, "\\u%04x", (int)ፊደል_ዋጋ));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(ሜላ_መወከሲ ተግባር_ዋጋ, አባል_ሓበሬታ ሓበሬታ, Map<String,String> ማሽን_ሰሌዳ, String ዕላማ) {
        String 표식 = ምልክት("method", ተግባር_ዋጋ.부분들());
        List<String> መስመር = new ArrayList<>();
        if ((ሓበሬታ.ፍቓድ_ምእታው & 0x100) != 0) {
            String ኣላግብ = ማሽን_ሰሌዳ.get(ተግባር_ዋጋ.ሽም + ተግባር_ዋጋ.서술);
            if (!ተግባር_ዋጋ.ወናኒ_ዋጋ.equals(ዕላማ.equals("kernel") ? "መሳርሒ_ዋጋ" : "ተጠቃሚ") || ኣላግብ == null) throw new ትርጉም_ጌጋ("허용되지 않은 native ተግባር_ዋጋ");
            return ".text\n" + 표식 + ":\njmp " + ኣላግብ;
        }
        byte[] ዋና_ጽሑፍ = ሓበሬታ.ባህሪ_ዋጋ.get("Code"); if (ዋና_ጽሑፍ == null) throw new ትርጉም_ጌጋ("ተግባር_ዋጋ 몸체가 없음");
        ሓበሬታ_ኣንባቢ ኣንባቢ_ዋጋ = new ሓበሬታ_ኣንባቢ(ዋና_ጽሑፍ); ኣንባቢ_ዋጋ.두바이트(); int 지역수 = ኣንባቢ_ዋጋ.두바이트();
        ሓበሬታ_ኣንባቢ ትእዛዝ_ሓበሬታ = new ሓበሬታ_ኣንባቢ(ኣንባቢ_ዋጋ.읽기(ኣንባቢ_ዋጋ.네바이트()));
        if (ኣንባቢ_ዋጋ.두바이트() != 0) throw new ትርጉም_ጌጋ("try/catch/finally 미지원");
        함수형식 ቅረጽ_ዋጋ = new 함수형식(ተግባር_ዋጋ.서술); if (지역수 < ቅረጽ_ዋጋ.인수.size()) throw new ትርጉም_ጌጋ("매개변수보다 적은 ኣካባብያዊ_ዕምቆት 변수");
        Collections.addAll(መስመር,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < ቅረጽ_ዋጋ.인수.size(); 순번++) Collections.addAll(መስመር,"movl " + (8 + 4 * (ቅረጽ_ዋጋ.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        ክፍሊ_ሓበሬታ ክፍሊ_ዋጋ = 클래스들.get(ተግባር_ዋጋ.ወናኒ_ዋጋ); Set<Integer> 경계들 = new HashSet<>(), ጨንፈር_ዝርዝር = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (ትእዛዝ_ሓበሬታ.위치 < ትእዛዝ_ሓበሬታ.ሓበሬታ.length) {
            int 위치 = ትእዛዝ_ሓበሬታ.위치, ትእዛዝ = ትእዛዝ_ሓበሬታ.한바이트(); String 자리 = 표식 + "_b" + 위치;
            መስመር.add(자리 + ":"); 경계들.add(위치);
            if (ትእዛዝ == 0) መስመር.add("nop");
            else if (ትእዛዝ == 1) መስመር.add("pushl $0");
            else if (ትእዛዝ >= 2 && ትእዛዝ <= 8) መስመር.add("pushl $" + (ትእዛዝ - 3));
            else if (ትእዛዝ == 16 || ትእዛዝ == 17) መስመር.add("pushl $" + (ትእዛዝ == 16 ? ትእዛዝ_ሓበሬታ.부호한바이트() : ትእዛዝ_ሓበሬታ.부호두바이트()));
            else if (ትእዛዝ == 18 || ትእዛዝ == 19) {
                int መሐበሪ = ትእዛዝ == 18 ? ትእዛዝ_ሓበሬታ.한바이트() : ትእዛዝ_ሓበሬታ.두바이트();
                መስመር.add("pushl $" + 엑스상수(ክፍሊ_ዋጋ,መሐበሪ));
            } else if (ትእዛዝ == 21 || ትእዛዝ == 25 || (ትእዛዝ >= 26 && ትእዛዝ <= 29) || (ትእዛዝ >= 42 && ትእዛዝ <= 45) || ትእዛዝ == 54 || ትእዛዝ == 58 || (ትእዛዝ >= 59 && ትእዛዝ <= 62) || (ትእዛዝ >= 75 && ትእዛዝ <= 78)) {
                boolean 읽음 = ትእዛዝ < 54; int መሐበሪ = ትእዛዝ == 21 || ትእዛዝ == 25 || ትእዛዝ == 54 || ትእዛዝ == 58 ? ትእዛዝ_ሓበሬታ.한바이트() : ትእዛዝ - (ትእዛዝ <= 29 ? 26 : ትእዛዝ <= 45 ? 42 : ትእዛዝ <= 62 ? 59 : 75);
                ፈትሽ_ኣካባብያዊ(መሐበሪ,지역수); መስመር.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (መሐበሪ + 1)) + "(%ebp)");
            } else if (ትእዛዝ == 46) Collections.addAll(መስመር,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (ትእዛዝ == 79) Collections.addAll(መስመር,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (ትእዛዝ == 87 || ትእዛዝ == 88) መስመር.add("addl $" + (ትእዛዝ == 87 ? 4 : 8) + ", %esp");
            else if (ትእዛዝ >= 89 && ትእዛዝ <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ተርታ_ዝርዝር = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[ትእዛዝ - 89]; 순번++) መስመር.add("popl " + 저장기들[순번]);
                for (int 순번 : ተርታ_ዝርዝር[ትእዛዝ - 89]) መስመር.add("pushl " + 저장기들[순번]);
            } else if (ትእዛዝ == 96 || ትእዛዝ == 100 || ትእዛዝ == 104 || ትእዛዝ == 126 || ትእዛዝ == 128 || ትእዛዝ == 130) {
                String ስርሒት_ዋጋ = ትእዛዝ == 96 ? "addl" : ትእዛዝ == 100 ? "subl" : ትእዛዝ == 104 ? "imull" : ትእዛዝ == 126 ? "andl" : ትእዛዝ == 128 ? "orl" : "xorl";
                Collections.addAll(መስመር,"popl %ecx","popl %eax",ስርሒት_ዋጋ + " %ecx, %eax","pushl %eax");
            } else if (ትእዛዝ == 108 || ትእዛዝ == 112) Collections.addAll(መስመር,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (ትእዛዝ == 108 ? "%eax" : "%edx"));
            else if (ትእዛዝ == 116) መስመር.add("negl (%esp)");
            else if (ትእዛዝ == 120 || ትእዛዝ == 122 || ትእዛዝ == 124) Collections.addAll(መስመር,"popl %ecx","popl %eax",(ትእዛዝ == 120 ? "sall" : ትእዛዝ == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (ትእዛዝ == 132) {
                int መሐበሪ = ትእዛዝ_ሓበሬታ.한바이트(), 증가 = ትእዛዝ_ሓበሬታ.부호한바이트(); ፈትሽ_ኣካባብያዊ(መሐበሪ,지역수); መስመር.add("addl $" + 증가 + ", -" + (4 * (መሐበሪ + 1)) + "(%ebp)");
            } else if (ትእዛዝ >= 145 && ትእዛዝ <= 147) Collections.addAll(መስመር,"popl %eax",ትእዛዝ == 145 ? "movsbl %al, %eax" : ትእዛዝ == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (ትእዛዝ >= 153 && ትእዛዝ <= 166) {
                if (ትእዛዝ <= 158) Collections.addAll(መስመር,"popl %eax","testl %eax, %eax");
                else Collections.addAll(መስመር,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int መዓልቦ_ዋጋ = 위치 + ትእዛዝ_ሓበሬታ.부호두바이트(); ጨንፈር_ዝርዝር.add(መዓልቦ_ዋጋ); መስመር.add(비교들[ትእዛዝ - (ትእዛዝ <= 158 ? 153 : 159)] + " " + 표식 + "_b" + መዓልቦ_ዋጋ);
            } else if (ትእዛዝ == 167 || ትእዛዝ == 200) {
                int መዓልቦ_ዋጋ = 위치 + (ትእዛዝ == 167 ? ትእዛዝ_ሓበሬታ.부호두바이트() : ትእዛዝ_ሓበሬታ.네바이트()); ጨንፈር_ዝርዝር.add(መዓልቦ_ዋጋ); መስመር.add("jmp " + 표식 + "_b" + መዓልቦ_ዋጋ);
            } else if (ትእዛዝ == 170 || ትእዛዝ == 171) {
                while (ትእዛዝ_ሓበሬታ.위치 % 4 != 0) ትእዛዝ_ሓበሬታ.한바이트();
                int ንቡር_ዋጋ = 위치 + ትእዛዝ_ሓበሬታ.네바이트(); ጨንፈር_ዝርዝር.add(ንቡር_ዋጋ); መስመር.add("popl %eax");
                int 개수, 아래 = 0;
                if (ትእዛዝ == 170) { 아래 = ትእዛዝ_ሓበሬታ.네바이트(); int 위 = ትእዛዝ_ሓበሬታ.네바이트(); long ንውሓት_ዋጋ = (long)위 - 아래 + 1; if (ንውሓት_ዋጋ < 1 || ንውሓት_ዋጋ > (ትእዛዝ_ሓበሬታ.ሓበሬታ.length - ትእዛዝ_ሓበሬታ.위치) / 4) throw new ትርጉም_ጌጋ("switch ቅንጣብ ጌጋ"); 개수 = (int)ንውሓት_ዋጋ; }
                else { 개수 = ትእዛዝ_ሓበሬታ.네바이트(); if (개수 < 0 || 개수 > (ትእዛዝ_ሓበሬታ.ሓበሬታ.length - ትእዛዝ_ሓበሬታ.위치) / 8) throw new ትርጉም_ጌጋ("switch መጠን ጌጋ"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int ዋጋ = ትእዛዝ == 170 ? 아래 + 순번 : ትእዛዝ_ሓበሬታ.네바이트(), መዓልቦ_ዋጋ = 위치 + ትእዛዝ_ሓበሬታ.네바이트(); ጨንፈር_ዝርዝር.add(መዓልቦ_ዋጋ);
                    Collections.addAll(መስመር,"cmpl $" + ዋጋ + ", %eax","je " + 표식 + "_b" + መዓልቦ_ዋጋ);
                }
                መስመር.add("jmp " + 표식 + "_b" + ንቡር_ዋጋ);
            } else if (ትእዛዝ == 172 || ትእዛዝ == 176 || ትእዛዝ == 177) {
                if (ትእዛዝ != 177) መስመር.add("popl %eax"); Collections.addAll(መስመር,"leave","ret");
            } else if (ትእዛዝ == 178 || ትእዛዝ == 179) {
                ሜላ_መወከሲ መወከሲ = ክፍሊ_ዋጋ.መወከሲ(ትእዛዝ_ሓበሬታ.두바이트()); if (!필드들.containsKey(መወከሲ)) throw new ትርጉም_ጌጋ("알 수 없는 ሜዳ_ዋጋ");
                Collections.addAll(መስመር,"call " + ምልክት("init",መወከሲ.ወናኒ_ዋጋ),(ትእዛዝ == 178 ? "pushl " : "popl ") + ምልክት("field",መወከሲ.부분들()));
            } else if (ትእዛዝ == 184) {
                ሜላ_መወከሲ መወከሲ = ክፍሊ_ዋጋ.መወከሲ(ትእዛዝ_ሓበሬታ.두바이트()); if (!함수들.containsKey(መወከሲ)) throw new ትርጉም_ጌጋ("알 수 없는 ተግባር_ዋጋ");
                함수형식 호출형식 = new 함수형식(መወከሲ.서술); Collections.addAll(መስመር,"call " + ምልክት("init",መወከሲ.ወናኒ_ዋጋ),"call " + ምልክት("method",መወከሲ.부분들()));
                if (!호출형식.인수.isEmpty()) መስመር.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) መስመር.add("pushl %eax");
            } else if (ትእዛዝ == 182) {
                ሜላ_መወከሲ መወከሲ = ክፍሊ_ዋጋ.መወከሲ(ትእዛዝ_ሓበሬታ.두바이트());
                if (መወከሲ.equals(new ሜላ_መወከሲ("java/lang/String","length","()I"))) Collections.addAll(መስመር,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (መወከሲ.equals(new ሜላ_መወከሲ("java/lang/String","charAt","(I)C"))) Collections.addAll(መስመር,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new ትርጉም_ጌጋ("가상 ተግባር_ዋጋ 호출 미지원");
            } else if (ትእዛዝ == 188) {
                if (ትእዛዝ_ሓበሬታ.한바이트() != 10) throw new ትርጉም_ጌጋ("new int[]만 ሓገዝ_ዋጋ"); Collections.addAll(መስመር,"popl %eax","call rt_new_array","pushl %eax");
            } else if (ትእዛዝ == 190) Collections.addAll(መስመር,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (ትእዛዝ == 196) {
                int ቅጥያ_ዋጋ = ትእዛዝ_ሓበሬታ.한바이트(), መሐበሪ = ትእዛዝ_ሓበሬታ.두바이트(); ፈትሽ_ኣካባብያዊ(መሐበሪ,지역수);
                if (ቅጥያ_ዋጋ == 21 || ቅጥያ_ዋጋ == 25 || ቅጥያ_ዋጋ == 54 || ቅጥያ_ዋጋ == 58) መስመር.add((ቅጥያ_ዋጋ <= 25 ? "pushl " : "popl ") + "-" + 4 * (መሐበሪ + 1) + "(%ebp)");
                else if (ቅጥያ_ዋጋ == 132) መስመር.add("addl $" + ትእዛዝ_ሓበሬታ.부호두바이트() + ", -" + 4 * (መሐበሪ + 1) + "(%ebp)");
                else throw new ትርጉም_ጌጋ("wide ትእዛዝ 미지원");
            } else if (ትእዛዝ == 198 || ትእዛዝ == 199) {
                int መዓልቦ_ዋጋ = 위치 + ትእዛዝ_ሓበሬታ.부호두바이트(); ጨንፈር_ዝርዝር.add(መዓልቦ_ዋጋ); Collections.addAll(መስመር,"popl %eax","testl %eax, %eax",(ትእዛዝ == 198 ? "je " : "jne ") + 표식 + "_b" + መዓልቦ_ዋጋ);
            } else throw new ትርጉም_ጌጋ("미지원 ትእዛዝ: " + ትእዛዝ);
        }
        if (!경계들.containsAll(ጨንፈር_ዝርዝር)) throw new ትርጉም_ጌጋ("ትእዛዝ 경계가 아닌 곳으로 ጨንፈር");
        መስመር.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",መስመር);
    }
    String 엑스상수(ክፍሊ_ሓበሬታ ሓበሬታ, int መሐበሪ) {
        if (ሓበሬታ.상수종류[መሐበሪ] == 3) return ሓበሬታ.መረራኽቦ_ሓበሬታ[መሐበሪ].toString();
        if (ሓበሬታ.상수종류[መሐበሪ] == 8) return ሕብረ_ቁምፊ_ምልክት(ሓበሬታ.문자((Integer)ሓበሬታ.መረራኽቦ_ሓበሬታ[መሐበሪ]));
        throw new ትርጉም_ጌጋ("정수와 ሕብረ_ቁምፊ_ዋጋ 상수만 ሓገዝ_ዋጋ");
    }
    String 엑스조립본(String ምእታው_ነጥቢ, List<String> 내보냄, String ዕላማ) throws IOException {
        Map<String,String> ማሽን_ሰሌዳ = new HashMap<>();
        for (String መስመር : Files.readAllLines(ሃብቲ_መገዲ.resolve("엑스기계함수.tsv"))) { String[] ኣጻምድ_ዋጋ = መስመር.split("\t"); if (ኣጻምድ_ዋጋ[0].equals(ዕላማ)) ማሽን_ሰሌዳ.put(ኣጻምድ_ዋጋ[1] + ኣጻምድ_ዋጋ[2],ኣጻምድ_ዋጋ[3]); }
        int 자리 = ምእታው_ነጥቢ.lastIndexOf('.'); if (자리 < 0) throw new ትርጉም_ጌጋ("ምእታው_ነጥቢ 지정 ጌጋ");
        String ወናኒ_ዋጋ = ምእታው_ነጥቢ.substring(0,자리).replace('.','/'), ሜላ_ምእታው_ሽም = ምእታው_ነጥቢ.substring(자리 + 1); ሜላ_መወከሲ ምእታው_ነጥቢ_ዋጋ = null;
        for (String 서술 : Arrays.asList("()I","()V")) { ሜላ_መወከሲ መወከሲ = new ሜላ_መወከሲ(ወናኒ_ዋጋ,ሜላ_ምእታው_ሽም,서술); if (함수들.containsKey(መወከሲ)) { if (ምእታው_ነጥቢ_ዋጋ != null) throw new ትርጉም_ጌጋ("겹친 ምእታው_ነጥቢ"); ምእታው_ነጥቢ_ዋጋ = መወከሲ; } }
        if (ምእታው_ነጥቢ_ዋጋ == null || (함수들.get(ምእታው_ነጥቢ_ዋጋ).ፍቓድ_ምእታው & 0x100) != 0) throw new ትርጉም_ጌጋ("ምእታው_ነጥቢ_ዋጋ ተግባር_ዋጋ ቅረጽ_ዋጋ ጌጋ");
        List<String> መስመር = new ArrayList<>(); መስመር.add(".code32");
        for (ክፍሊ_ሓበሬታ ሓበሬታ : 클래스들.values()) {
            String ደረጃ_ዋጋ = ምልክት("state",ሓበሬታ.ሽም), ኣተስእ = ምልክት("init",ሓበሬታ.ሽም);
            Collections.addAll(መስመር,".bss",".balign 4",ደረጃ_ዋጋ + ": .long 0",".text",ኣተስእ + ":","cmpl $0, " + ደረጃ_ዋጋ,"jne " + ኣተስእ + "_done","movl $1, " + ደረጃ_ዋጋ);
            ሜላ_መወከሲ 초기화참조 = new ሜላ_መወከሲ(ሓበሬታ.ሽም,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) መስመር.add("call " + ምልክት("method",초기화참조.부분들()));
            Collections.addAll(መስመር,"movl $2, " + ደረጃ_ዋጋ,ኣተስእ + "_done:","ret");
            for (አባል_ሓበሬታ ሜዳ_ዋጋ : ሓበሬታ.ሜዳ_ዋጋ) {
                byte[] መረራኽቦ_ዋጋ = ሜዳ_ዋጋ.ባህሪ_ዋጋ.get("ConstantValue"); String ዋጋ = መረራኽቦ_ዋጋ == null ? "0" : 엑스상수(ሓበሬታ,new ሓበሬታ_ኣንባቢ(መረራኽቦ_ዋጋ).두바이트());
                Collections.addAll(መስመር,".data",".balign 4",ምልክት("field",ሓበሬታ.ሽም,ሜዳ_ዋጋ.ሽም,ሜዳ_ዋጋ.서술) + ": .long " + ዋጋ);
            }
            for (አባል_ሓበሬታ ተግባር_ዋጋ : ሓበሬታ.ተግባር_ዋጋ) if (!ተግባር_ዋጋ.ሽም.equals("<init>")) መስመር.add(엑스함수본문(new ሜላ_መወከሲ(ሓበሬታ.ሽም,ተግባር_ዋጋ.ሽም,ተግባር_ዋጋ.서술),ተግባር_ዋጋ,ማሽን_ሰሌዳ,ዕላማ));
        }
        Collections.addAll(መስመር,".text",".globl java_entry","java_entry:","call " + ምልክት("init",ምእታው_ነጥቢ_ዋጋ.ወናኒ_ዋጋ),"call " + ምልክት("method",ምእታው_ነጥቢ_ዋጋ.부분들()));
        if (ምእታው_ነጥቢ_ዋጋ.서술.equals("()V")) መስመር.add("xorl %eax, %eax"); መስመር.add("ret");
        for (String 지정 : 내보냄) {
            int ደራቲ_ዋጋ = 지정.indexOf('='); if (ደራቲ_ዋጋ < 1) throw new ትርጉም_ጌጋ("내보내기 지정 ጌጋ");
            String 외부 = 지정.substring(0,ደራቲ_ዋጋ), ተግባር_ዋጋ = 지정.substring(ደራቲ_ዋጋ + 1); int 나눔 = ተግባር_ዋጋ.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ትርጉም_ጌጋ("내보내기 ምልክት ጌጋ");
            String ክፍሊ_ዋጋ = ተግባር_ዋጋ.substring(0,나눔).replace('.','/'), ሽም = ተግባር_ዋጋ.substring(나눔 + 1); ሜላ_መወከሲ ምሩጽ_ዋጋ = null;
            for (ሜላ_መወከሲ መወከሲ : 함수들.keySet()) if (መወከሲ.ወናኒ_ዋጋ.equals(ክፍሊ_ዋጋ) && መወከሲ.ሽም.equals(ሽም)) { if (ምሩጽ_ዋጋ != null) throw new ትርጉም_ጌጋ("겹친 내보내기 ዕላማ"); ምሩጽ_ዋጋ = መወከሲ; }
            if (ምሩጽ_ዋጋ == null) throw new ትርጉም_ጌጋ("내보낼 함수가 없음");
            Collections.addAll(መስመር,".text",".globl " + 외부,외부 + ":","call " + ምልክት("init",ምሩጽ_ዋጋ.ወናኒ_ዋጋ),"jmp " + ምልክት("method",ምሩጽ_ዋጋ.부분들()));
        }
        መስመር.add(".section .rodata");
        for (Map.Entry<String,String> ምእታው_ዋጋ : 문자열들.entrySet()) {
            Collections.addAll(መስመር,".balign 4",ምእታው_ዋጋ.getValue() + ":",".long " + ምእታው_ዋጋ.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char ትምህርቲ_ዋጋ : ምእታው_ዋጋ.getKey().toCharArray()) 단위들.add(Integer.toString(ትምህርቲ_ዋጋ)); if (!단위들.isEmpty()) መስመር.add(".long " + String.join(",",단위들));
        }
        መስመር.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",መስመር) + "\n";
    }
    static void ተግብር_መሳርሒ(List<String> ትእዛዝ) throws Exception {
        if (new ProcessBuilder(ትእዛዝ).inheritIO().start().waitFor() != 0) throw new ትርጉም_ጌጋ("ህነጽ_ምንጪ ጌጋ: " + ትእዛዝ.get(0));
    }
    static String ሓበሬታ_ሕብረ_ቁምፊ(String ጽሑፍ) { return "\"" + ጽሑፍ.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String ዕላማ, String ምእታው_ነጥቢ, List<String> 내보냄, Path 출력, Path ሃብቲ_ዋጋ) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), ክፍሊ_መገዲ = 임시.resolve("classes"); Files.createDirectory(ክፍሊ_መገዲ);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",ክፍሊ_መገዲ.toString(),"-sourcepath",ክፍሊ_መገዲ.toString(),"-d",ክፍሊ_መገዲ.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new ትርጉም_ጌጋ("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new ትርጉም_ጌጋ(".java 또는 .class만 ሓገዝ_ዋጋ");
            }
            if (원문수 > 0) ተግብር_መሳርሒ(자바명령);
            try (java.util.stream.Stream<Path> መገዲ_ዝርዝር = Files.walk(ክፍሊ_መገዲ)) { መገዲ_ዝርዝር.filter(መገዲ -> መገዲ.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,ዕላማ.equals("user") ? "user" : "kernel",262144,ሃብቲ_ዋጋ);
            String 조립 = 변환.엑스조립본(ምእታው_ነጥቢ,내보냄,ዕላማ); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = ሃብቲ_ዋጋ.getParent();
            ተግብር_መሳርሒ(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            ተግብር_መሳርሒ(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("ግዜ_ስራሕ_ናይ_ሓባር_ቛንቛ_ሓገዝ.s").toString()));
            List<String> ኣላግብ = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (ዕላማ.equals("kernel")) ኣላግብ.add("-r");
            else {
                ተግብር_መሳርሒ(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(ዕላማ.equals("user") ? "ጀምር_ተጠቃሚ_መተግበሪ.s" : "리눅스시작.s").toString()));
                Collections.addAll(ኣላግብ,"-e","_start",임시.resolve("start.o").toString());
                if (ዕላማ.equals("user")) Collections.addAll(ኣላግብ,"-T",도구위치.resolve("ተጠቃሚ_መጋጠሚ_ኣቀማምጣ.ld").toString());
            }
            Collections.addAll(ኣላግብ,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); ተግብር_መሳርሒ(ኣላግብ);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path ሓትም_ዋጋ = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),ሓትም_ዋጋ,StandardCopyOption.REPLACE_EXISTING); Files.move(ሓትም_ዋጋ,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(ሓትም_ዋጋ); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(ዕላማ.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> ምልክት_ሓበሬታ = new ArrayList<>(), ፍልፍል_ሓበሬታ = new ArrayList<>();
            for (ሜላ_መወከሲ መወከሲ : 변환.함수들.keySet()) ምልክት_ሓበሬታ.add(ሓበሬታ_ሕብረ_ቁምፊ(ምልክት("method",መወከሲ.부분들())) + ":" + ሓበሬታ_ሕብረ_ቁምፊ(መወከሲ.ወናኒ_ዋጋ + "." + መወከሲ.ሽም + መወከሲ.서술));
            for (Path 입력 : 입력들) {
                byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder ጽሑፍ = new StringBuilder(); for (byte ዋጋ : 해시) ጽሑፍ.append(String.format(Locale.ROOT,"%02x",ዋጋ & 255));
                ፍልፍል_ሓበሬታ.add(ሓበሬታ_ሕብረ_ቁምፊ(입력.toAbsolutePath().toString()) + ":" + ሓበሬታ_ሕብረ_ቁምፊ(ጽሑፍ.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + ሓበሬታ_ሕብረ_ቁምፊ(ዕላማ) + ",\"entry\":" + ሓበሬታ_ሕብረ_ቁምፊ(ምእታው_ነጥቢ) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",ምልክት_ሓበሬታ) + "},\"sources\":{" + String.join(",",ፍልፍል_ሓበሬታ) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> መገዲ_ዝርዝር = Files.walk(임시)) { for (Path መገዲ : (Iterable<Path>)መገዲ_ዝርዝር.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(መገዲ); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String ምእታው_ነጥቢ = null, ዕላማ = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> መገዲ_ዝርዝር = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String ዋጋ = 인수[순번];
                switch (ዋጋ) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry ክፍሊ_ዋጋ.ተግባር_ዋጋ -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export ምልክት=ክፍሊ_ዋጋ.ተግባር_ዋጋ] 클래스파일 또는 Java원문"); return;
                    case "--entry": ምእታው_ነጥቢ = 인수[++순번]; break;
                    case "--profile": ዕላማ = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (ዋጋ.startsWith("-")) throw new ትርጉም_ጌጋ("알 수 없는 옵션: " + ዋጋ); መገዲ_ዝርዝር.add(Paths.get(ዋጋ));
                }
            }
            if (ምእታው_ነጥቢ == null || 출력경로 == null || መገዲ_ዝርዝር.isEmpty()) throw new ትርጉም_ጌጋ("--entry, -o, ክፍሊ_ዋጋ 파일이 필요합니다");
            Path ሃብቲ_ዋጋ = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new ትርጉም_ጌጋ("알 수 없는 ተግብር_ትእዛዝ ዕላማ");
                엑스번역(መገዲ_ዝርዝር,엑스대상,ምእታው_ነጥቢ,내보냄,출력경로,ሃብቲ_ዋጋ); return;
            }
            String ምንጪ = new 기계어미리번역(መገዲ_ዝርዝር, ዕላማ, 낱말수, ሃብቲ_ዋጋ).생성(ምእታው_ነጥቢ, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ምንጪ, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception ጌጋ) { System.err.println("ህነጽ_ምንጪ ጌጋ: " + ጌጋ.getMessage()); System.exit(1); }
    }
}
