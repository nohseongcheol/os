// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java fedde_njaru 파일에서 독립 ARM64 커널용 C 원문을 만든다. njaatigi JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class 번역오류 extends RuntimeException {
        번역오류(String 설명) { super(설명); }
    }
    static final class keɓe_Tarirgal {
        final byte[] keɓe;
        int 위치;
        keɓe_Tarirgal(byte[] 입력자료) { keɓe = 입력자료; }
        byte[] 읽기(int njuuteendi_njaru) {
            if (njuuteendi_njaru < 0 || njuuteendi_njaru > keɓe.length - 위치) throw new 번역오류("잘린 fedde_njaru 또는 ginol keɓe");
            byte[] 결과 = Arrays.copyOfRange(keɓe, 위치, 위치 + njuuteendi_njaru); 위치 += njuuteendi_njaru; return 결과;
        }
        int 한바이트() { if (위치 >= keɓe.length) throw new 번역오류("잘린 ginol keɓe"); return keɓe[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class tergal_keɓe {
        final int naatde_naatnugol;
        final String innde, 서술;
        final Map<String, byte[]> mbaadi_njaru;
        tergal_keɓe(int naatde_njaru, String innde_njaru, String 서술값, Map<String, byte[]> mbaadi_keɓe) {
            naatde_naatnugol = naatde_njaru; innde = innde_njaru; 서술 = 서술값; mbaadi_njaru = mbaadi_keɓe;
        }
    }
    static final class 함수참조 implements Comparable<함수참조> {
        final String 소유, innde, 서술;
        함수참조(String 소유값, String innde_njaru, String 서술값) { 소유 = 소유값; innde = innde_njaru; 서술 = 서술값; }
        String[] 부분들() { return new String[]{소유, innde, 서술}; }
        public int compareTo(함수참조 giƴiraaɗo_njaru) {
            int 비교값 = 소유.compareTo(giƴiraaɗo_njaru.소유);
            if (비교값 == 0) 비교값 = innde.compareTo(giƴiraaɗo_njaru.innde);
            return 비교값 == 0 ? 서술.compareTo(giƴiraaɗo_njaru.서술) : 비교값;
        }
        public boolean equals(Object giƴiraaɗo_njaru) { return giƴiraaɗo_njaru instanceof 함수참조 && compareTo((함수참조) giƴiraaɗo_njaru) == 0; }
        public int hashCode() { return Objects.hash(소유, innde, 서술); }
    }
    static final class fedde_keɓe {
        final int[] 상수종류;
        final Object[] 상수값;
        final String innde;
        final List<tergal_keɓe> suudu_njaru, juɓɓol_njaru;
        fedde_keɓe(Path laawol) throws IOException {
            keɓe_Tarirgal Tarirgal_njaru = new keɓe_Tarirgal(Files.readAllBytes(laawol));
            if (Tarirgal_njaru.네바이트() != 0xcafebabe) throw new 번역오류("Java fedde_njaru 표식이 아님");
            Tarirgal_njaru.읽기(4);
            int 개수 = Tarirgal_njaru.두바이트(); 상수종류 = new int[개수]; 상수값 = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = Tarirgal_njaru.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int njuuteendi_njaru = Tarirgal_njaru.두바이트();
                        byte[] alkulal_resordu_sabbordu = Tarirgal_njaru.읽기(njuuteendi_njaru), 길이붙인자료 = new byte[njuuteendi_njaru + 2];
                        길이붙인자료[0] = (byte)(njuuteendi_njaru >> 8); 길이붙인자료[1] = (byte)njuuteendi_njaru;
                        System.arraycopy(alkulal_resordu_sabbordu, 0, 길이붙인자료, 2, njuuteendi_njaru);
                        상수값[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: 상수값[순번] = Tarirgal_njaru.네바이트(); break;
                    case 4: Tarirgal_njaru.읽기(4); break;
                    case 5: case 6: Tarirgal_njaru.읽기(8); 순번++; break;
                    case 7: case 8: case 16: 상수값[순번] = Tarirgal_njaru.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        상수값[순번] = new int[]{Tarirgal_njaru.두바이트(), Tarirgal_njaru.두바이트()}; break;
                    case 15: 상수값[순번] = new int[]{Tarirgal_njaru.한바이트(), Tarirgal_njaru.두바이트()}; break;
                    default: throw new 번역오류("지원하지 않는 상수 종류: " + 종류);
                }
            }
            Tarirgal_njaru.두바이트(); innde = fedde_innde(Tarirgal_njaru.두바이트());
            if (!fedde_innde(Tarirgal_njaru.두바이트()).equals("java/lang/Object") || Tarirgal_njaru.두바이트() != 0)
                throw new 번역오류(innde + ": 상속 및 인터페이스 미지원");
            suudu_njaru = 멤버읽기(Tarirgal_njaru); juɓɓol_njaru = 멤버읽기(Tarirgal_njaru); 속성읽기(Tarirgal_njaru);
            if (Tarirgal_njaru.위치 != Tarirgal_njaru.keɓe.length) throw new 번역오류("fedde_njaru 뒤에 남은 keɓe");
        }
        String 문자(int joopirdu) {
            if (joopirdu < 1 || joopirdu >= 상수종류.length || 상수종류[joopirdu] != 1) throw new 번역오류("문자 상수 joopirdu juumre");
            return (String) 상수값[joopirdu];
        }
        String fedde_innde(int joopirdu) {
            if (joopirdu < 1 || joopirdu >= 상수종류.length || 상수종류[joopirdu] != 7) throw new 번역오류("fedde_njaru 참조 juumre");
            return 문자((Integer)상수값[joopirdu]);
        }
        함수참조 참조(int joopirdu) {
            if (joopirdu < 1 || joopirdu >= 상수종류.length || 상수종류[joopirdu] < 9 || 상수종류[joopirdu] > 11) throw new 번역오류("멤버 참조 juumre");
            int[] linngondirde_njaru = (int[])상수값[joopirdu], innde_linngondirde = (int[])상수값[linngondirde_njaru[1]];
            return new 함수참조(fedde_innde(linngondirde_njaru[0]), 문자(innde_linngondirde[0]), 문자(innde_linngondirde[1]));
        }
        Map<String, byte[]> 속성읽기(keɓe_Tarirgal Tarirgal_njaru) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = Tarirgal_njaru.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String mbaadi_innde = 문자(Tarirgal_njaru.두바이트()); byte[] njaru = Tarirgal_njaru.읽기(Tarirgal_njaru.네바이트());
                if (결과.put(mbaadi_innde, njaru) != null) throw new 번역오류("겹친 mbaadi_njaru: " + mbaadi_innde);
            }
            return 결과;
        }
        List<tergal_keɓe> 멤버읽기(keɓe_Tarirgal Tarirgal_njaru) {
            List<tergal_keɓe> 결과 = new ArrayList<>(); int 개수 = Tarirgal_njaru.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int naatde_naatnugol = Tarirgal_njaru.두바이트(); String 함수이름 = 문자(Tarirgal_njaru.두바이트()), 서술 = 문자(Tarirgal_njaru.두바이트());
                결과.add(new tergal_keɓe(naatde_naatnugol, 함수이름, 서술, 속성읽기(Tarirgal_njaru)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new 번역오류("juɓɓol_njaru 서술 juumre: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new 번역오류("juɓɓol_njaru 서술 juumre: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new 번역오류("juɓɓol_njaru 서술 juumre: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String cuɓal_njaru = null;
            for (String formaa_njaru : 허용형식) if (서술.startsWith(formaa_njaru, 위치)) { cuɓal_njaru = formaa_njaru; break; }
            if (cuɓal_njaru == null) throw new 번역오류("지원하지 않는 fannu_keɓe: " + 서술);
            결과.add(cuɓal_njaru); 위치 += cuɓal_njaru.length();
        }
        return 결과;
    }
    static String 기호(String 종류, String... 부분들) {
        try {
            byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder binndi = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) binndi.append(String.format(Locale.ROOT, "%02x", 해시[순번] & 255));
            return binndi.toString();
        } catch (Exception juumre) { throw new 번역오류(juumre.toString()); }
    }
    final Map<String, fedde_keɓe> 클래스들 = new TreeMap<>();
    final Map<함수참조, tergal_keɓe> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, 기계클래스;
    final int 동적기억낱말수;
    final Path wallitorde_laawol;
    기계어미리번역(List<Path> laawol_Doggol, String faandaare, int 낱말수, Path wallitorde_njaru) throws IOException {
        if ((!faandaare.equals("kernel") && !faandaare.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new 번역오류("실행 faandaare 또는 teskordu_njaru 공간 waylude_etannde juumre");
        실행대상 = faandaare; 동적기억낱말수 = 낱말수; wallitorde_laawol = wallitorde_njaru;
        // 이 이름도 국가별 sewnde_lekki 생성 시 해당 언어로 옮긴다.
        기계클래스 = faandaare.equals("kernel") ? "보드" : "kuutoro";
        for (String diidol : Files.readAllLines(wallitorde_njaru.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = diidol.split("\t", -1);
            if (부분들.length != 4) throw new 번역오류("기계 juɓɓol_njaru keɓe juumre");
            if (부분들[0].equals(faandaare)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path laawol : laawol_Doggol) {
            fedde_keɓe keɓe = new fedde_keɓe(laawol);
            if (클래스들.put(keɓe.innde, keɓe) != null) throw new 번역오류("중복 fedde_njaru: " + keɓe.innde);
            for (tergal_keɓe suudu_njaru : keɓe.suudu_njaru) {
                if ((suudu_njaru.naatde_naatnugol & 8) == 0 || 형식읽기(suudu_njaru.서술).equals(Collections.singletonList("V"))) throw new 번역오류("ñiiɓ_njaru 필드만 ballital_njaru");
                if (필드들.put(new 함수참조(keɓe.innde, suudu_njaru.innde, suudu_njaru.서술), suudu_njaru) != null) throw new 번역오류("중복 suudu_njaru");
            }
            for (tergal_keɓe juɓɓol_njaru : keɓe.juɓɓol_njaru) {
                if (juɓɓol_njaru.innde.equals("<init>")) continue;
                if ((juɓɓol_njaru.naatde_naatnugol & 8) == 0 || (juɓɓol_njaru.naatde_naatnugol & (0x20 | 0x400)) != 0) throw new 번역오류("ñiiɓ_njaru 비동기화 함수만 ballital_njaru");
                new 함수형식(juɓɓol_njaru.서술);
                if (함수들.put(new 함수참조(keɓe.innde, juɓɓol_njaru.innde, juɓɓol_njaru.서술), juɓɓol_njaru) != null) throw new 번역오류("중복 juɓɓol_njaru");
            }
        }
    }
    String 문자열기호(String binndi) { return 문자열들.computeIfAbsent(binndi, njaru -> "j_text_" + 문자열들.size()); }
    String 상수표현(fedde_keɓe keɓe, int joopirdu) {
        if (joopirdu < 1 || joopirdu >= keɓe.상수종류.length) throw new 번역오류("상수 joopirdu kilip juumre");
        if (keɓe.상수종류[joopirdu] == 3) return "(word)(uint32_t)(" + keɓe.상수값[joopirdu] + ")";
        if (keɓe.상수종류[joopirdu] == 8) return "(word)" + 문자열기호(keɓe.문자((Integer)keɓe.상수값[joopirdu]));
        throw new 번역오류("정수와 ɓoggol_njaru 상수만 ballital_njaru");
    }
    String 함수원형(함수참조 참조) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(참조.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + 기호("method", 참조.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void sek_nokkuwal(int joopirdu, int 지역변수수) { if (joopirdu < 0 || joopirdu >= 지역변수수) throw new 번역오류("nokkuwal_njaajeendi 변수 joopirdu kilip juumre"); }
    void 분기넣기(List<String> 출력, Set<Integer> 분기들, int 위치, int 이동량, String ngonka) {
        int tiindaare_njaru = 위치 + 이동량; 분기들.add(tiindaare_njaru);
        출력.add((ngonka == null ? "" : "if (" + ngonka + ") ") + "goto b" + tiindaare_njaru + ";");
    }
    String 함수본문(함수참조 juɓɓol_njaru, tergal_keɓe keɓe) {
        byte[] 본문자료 = keɓe.mbaadi_njaru.get("Code"); if (본문자료 == null) throw new 번역오류("juɓɓol_njaru 몸체가 없음: " + juɓɓol_njaru.innde);
        keɓe_Tarirgal Tarirgal_njaru = new keɓe_Tarirgal(본문자료); int 쌓임깊이 = Tarirgal_njaru.두바이트(), 지역변수수 = Tarirgal_njaru.두바이트();
        keɓe_Tarirgal ginol_keɓe = new keɓe_Tarirgal(Tarirgal_njaru.읽기(Tarirgal_njaru.네바이트()));
        if (Tarirgal_njaru.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 formaa_njaru = new 함수형식(juɓɓol_njaru.서술); if (지역변수수 < formaa_njaru.인수.size()) throw new 번역오류("매개변수보다 적은 nokkuwal_njaajeendi 변수");
        fedde_keɓe fedde_njaru = 클래스들.get(juɓɓol_njaru.소유);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(juɓɓol_njaru) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formaa_njaru.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (ginol_keɓe.위치 < ginol_keɓe.keɓe.length) {
            int 위치 = ginol_keɓe.위치, ginol = ginol_keɓe.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (ginol == 0) continue;
            if (ginol == 1) 출력.add("PUSH(0);");
            else if (ginol >= 2 && ginol <= 8) 출력.add("PUSH((uint32_t)(" + (ginol - 3) + "));");
            else if (ginol == 16 || ginol == 17) 출력.add("PUSH((uint32_t)(" + (ginol == 16 ? ginol_keɓe.부호한바이트() : ginol_keɓe.부호두바이트()) + "));");
            else if (ginol == 18 || ginol == 19) 출력.add("PUSH(" + 상수표현(fedde_njaru, ginol == 18 ? ginol_keɓe.한바이트() : ginol_keɓe.두바이트()) + ");");
            else if (ginol == 21 || ginol == 25 || (ginol >= 26 && ginol <= 29) || (ginol >= 42 && ginol <= 45)) {
                int joopirdu = ginol == 21 || ginol == 25 ? ginol_keɓe.한바이트() : ginol - (ginol <= 29 ? 26 : 42);
                sek_nokkuwal(joopirdu, 지역변수수); 출력.add("PUSH(l[" + joopirdu + "]);");
            } else if (ginol == 54 || ginol == 58 || (ginol >= 59 && ginol <= 62) || (ginol >= 75 && ginol <= 78)) {
                int joopirdu = ginol == 54 || ginol == 58 ? ginol_keɓe.한바이트() : ginol - (ginol <= 62 ? 59 : 75);
                sek_nokkuwal(joopirdu, 지역변수수); 출력.add("l[" + joopirdu + "] = POP();");
            } else if (ginol == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (ginol == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (ginol == 87 || ginol == 88) 출력.add(ginol == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (ginol >= 89 && ginol <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] deggondiral_Doggol = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[ginol - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char njaru : deggondiral_Doggol[ginol - 89].toCharArray()) 출력.add("PUSH(" + njaru + ");");
            } else if (ginol == 96 || ginol == 100 || ginol == 104 || ginol == 126 || ginol == 128 || ginol == 130) {
                String hiisoore_njaru = ginol == 96 ? "+" : ginol == 100 ? "-" : ginol == 104 ? "*" : ginol == 126 ? "&" : ginol == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + hiisoore_njaru + " (uint32_t)b);");
            } else if (ginol == 108 || ginol == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (ginol == 112 ? 1 : 0) + "));");
            else if (ginol == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (ginol == 120 || ginol == 122 || ginol == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (ginol == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (ginol == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (ginol == 132) {
                int joopirdu = ginol_keɓe.한바이트(), 증가량 = ginol_keɓe.부호한바이트(); sek_nokkuwal(joopirdu, 지역변수수);
                출력.add("l[" + joopirdu + "] = (uint32_t)l[" + joopirdu + "] + (uint32_t)(" + 증가량 + ");");
            } else if (ginol >= 145 && ginol <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (ginol == 145 ? "int8_t" : ginol == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (ginol >= 153 && ginol <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, 분기들, 위치, ginol_keɓe.부호두바이트(), "(int32_t)a " + 비교들[ginol - 153] + " 0");
            } else if (ginol >= 159 && ginol <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, 분기들, 위치, ginol_keɓe.부호두바이트(), ginol >= 165 ? "a " + 비교들[ginol - 159] + " b" : "(int32_t)a " + 비교들[ginol - 159] + " (int32_t)b");
            } else if (ginol == 167 || ginol == 200) 분기넣기(출력, 분기들, 위치, ginol == 167 ? ginol_keɓe.부호두바이트() : ginol_keɓe.네바이트(), null);
            else if (ginol == 170 || ginol == 171) {
                while (ginol_keɓe.위치 % 4 != 0) ginol_keɓe.한바이트();
                int lasli_njaru = ginol_keɓe.네바이트(); 출력.add("a = POP();");
                if (ginol == 170) {
                    int 아래 = ginol_keɓe.네바이트(), 위 = ginol_keɓe.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (ginol_keɓe.keɓe.length - ginol_keɓe.위치) / 4) throw new 번역오류("switch kilip juumre");
                    for (long njaru = 아래; njaru <= 위; njaru++) 분기넣기(출력, 분기들, 위치, ginol_keɓe.네바이트(), "(int32_t)a == (" + njaru + ")");
                } else {
                    int 개수 = ginol_keɓe.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (ginol_keɓe.keɓe.length - ginol_keɓe.위치) / 8) throw new 번역오류("switch waylude_etannde juumre");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int njaru = ginol_keɓe.네바이트(); if (순번 > 0 && njaru <= 앞값) throw new 번역오류("switch deggondiral_njaru juumre"); 앞값 = njaru;
                        분기넣기(출력, 분기들, 위치, ginol_keɓe.네바이트(), "(int32_t)a == (" + njaru + ")");
                    }
                }
                분기넣기(출력, 분기들, 위치, lasli_njaru, null);
            } else if (ginol == 172 || ginol == 176 || ginol == 177) 출력.add("return " + (ginol == 177 ? "0" : "POP()") + ";");
            else if (ginol == 178 || ginol == 179) {
                함수참조 참조 = fedde_njaru.참조(ginol_keɓe.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 suudu_njaru");
                출력.add(기호("init", 참조.소유) + "();"); String suudu_njaru = 기호("field", 참조.부분들());
                출력.add(ginol == 178 ? "PUSH(" + suudu_njaru + ");" : suudu_njaru + " = POP();");
            } else if (ginol == 184) {
                함수참조 참조 = fedde_njaru.참조(ginol_keɓe.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 juɓɓol_njaru");
                함수형식 호출형식 = new 함수형식(참조.서술); int 개수 = 호출형식.인수.size();
                출력.add(기호("init", 참조.소유) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + 기호("method", 참조.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (ginol == 182) {
                함수참조 참조 = fedde_njaru.참조(ginol_keɓe.두바이트());
                if (참조.equals(new 함수참조("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (참조.equals(new 함수참조("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 번역오류("가상 juɓɓol_njaru 호출 미지원");
            } else if (ginol == 188) {
                if (ginol_keɓe.한바이트() != 10) throw new 번역오류("new int[]만 ballital_njaru"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (ginol == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (ginol == 196) {
                int timmital_njaru = ginol_keɓe.한바이트(), joopirdu = ginol_keɓe.두바이트(); sek_nokkuwal(joopirdu, 지역변수수);
                if (timmital_njaru == 21 || timmital_njaru == 25) 출력.add("PUSH(l[" + joopirdu + "]);");
                else if (timmital_njaru == 54 || timmital_njaru == 58) 출력.add("l[" + joopirdu + "] = POP();");
                else if (timmital_njaru == 132) 출력.add("l[" + joopirdu + "] = (uint32_t)l[" + joopirdu + "] + (uint32_t)(" + ginol_keɓe.부호두바이트() + ");");
                else throw new 번역오류("미지원 wide ginol");
            } else if (ginol == 198 || ginol == 199) {
                출력.add("a = POP();"); 분기넣기(출력, 분기들, 위치, ginol_keɓe.부호두바이트(), "a " + (ginol == 198 ? "==" : "!=") + " 0");
            } else throw new 번역오류(juɓɓol_njaru.소유 + "." + juɓɓol_njaru.innde + ", oktee_njaru " + 위치 + ": 미지원 ginol " + ginol);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("ginol 경계가 아닌 곳으로 분기");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String 내보낼함수(String 연결기호, String faandaare, boolean 진입점여부) {
        int 자리 = faandaare.lastIndexOf('.'); if (자리 < 0 || !연결기호.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 지정 juumre");
        String 소유 = faandaare.substring(0, 자리).replace('.', '/'), innde = faandaare.substring(자리 + 1); 함수참조 cuɓal_njaru = null;
        for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(소유) && 참조.innde.equals(innde)) {
            if (cuɓal_njaru != null) throw new 번역오류("겹친 내보내기 faandaare"); cuɓal_njaru = 참조;
        }
        if (cuɓal_njaru == null || (함수들.get(cuɓal_njaru).naatde_naatnugol & 0x100) != 0) throw new 번역오류("내보낼 함수가 없음 또는 native juɓɓol_njaru");
        함수형식 formaa_njaru = new 함수형식(cuɓal_njaru.서술);
        if ((진입점여부 && !formaa_njaru.인수.isEmpty()) || !Arrays.asList("V", "I").contains(formaa_njaru.반환)) throw new 번역오류("naatnugol_toɓɓere_njaru 또는 C 경계 formaa_njaru juumre");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formaa_njaru.인수.size(); 순번++) {
            if (!formaa_njaru.인수.get(순번).equals("I")) throw new 번역오류("C 경계는 int 인수만 ballital_njaru");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formaa_njaru.반환.equals("V") ? "void " : "int32_t ") + 연결기호 + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + 기호("init", cuɓal_njaru.소유) + "(); " + (formaa_njaru.반환.equals("V") ? "" : "return (int32_t)") + 기호("method", cuɓal_njaru.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String naatnugol_toɓɓere, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<함수참조, tergal_keɓe> naatnugol_njaru : 함수들.entrySet()) {
            함수참조 참조 = naatnugol_njaru.getKey(); tergal_keɓe keɓe = naatnugol_njaru.getValue(); 선언들.add(함수원형(참조) + ";");
            if ((keɓe.naatde_naatnugol & 0x100) != 0) {
                String seŋaade = 기계함수들.get(참조.innde + 참조.서술);
                if (!참조.소유.equals(기계클래스) || seŋaade == null) throw new 번역오류("허용되지 않은 native juɓɓol_njaru: " + 참조.innde);
                int 개수 = new 함수형식(참조.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + seŋaade + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(참조) + " { return " + seŋaade + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(참조, keɓe));
        }
        for (Map.Entry<함수참조, tergal_keɓe> naatnugol_njaru : 필드들.entrySet()) {
            함수참조 참조 = naatnugol_njaru.getKey(); byte[] 상수 = naatnugol_njaru.getValue().mbaadi_njaru.get("ConstantValue");
            String njaru = 상수 == null ? "0" : 상수표현(클래스들.get(참조.소유), new keɓe_Tarirgal(상수).두바이트());
            필드선언들.add("static word " + 기호("field", 참조.부분들()) + " = " + njaru + ";");
        }
        for (String innde : 클래스들.keySet()) {
            String ɓamtinde = 기호("init", innde), ngonka_njaru = 기호("state", innde);
            선언들.add("static void " + ɓamtinde + "(void);"); 필드선언들.add("static unsigned " + ngonka_njaru + ";");
            함수참조 참조 = new 함수참조(innde, "<clinit>", "()V");
            몸체들.add("static void " + ɓamtinde + "(void) { if(" + ngonka_njaru + ") return; " + ngonka_njaru + " = 1; " + (함수들.containsKey(참조) ? 기호("method", 참조.부분들()) + "(); " : "") + ngonka_njaru + " = 2; }");
        }
        몸체들.add(내보낼함수("java_entry", naatnugol_toɓɓere, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new 번역오류("내보내기 지정 juumre");
            String innde = 지정.substring(0, 자리); 공개이름.add(innde); 몸체들.add(내보낼함수(innde, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> naatnugol_njaru : 문자열들.entrySet()) {
            String binndi = naatnugol_njaru.getKey(); StringBuilder 배열 = new StringBuilder("static const word " + naatnugol_njaru.getValue() + "[] = {" + binndi.length());
            for (int 순번 = 0; 순번 < binndi.length(); 순번++) 배열.append(", ").append((int)binndi.charAt(순번));
            문자열선언들.add(배열.append("};").toString());
        }
        String ballital_njaru = Files.readString(wallitorde_laawol.resolve("실행지원.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(ballital_njaru + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String sewnde, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> innde_taabal = new HashMap<>();
        for (String diidol : Files.readAllLines(wallitorde_laawol.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] linngondirde_njaru = diidol.split("\t"); innde_taabal.put(linngondirde_njaru[0], linngondirde_njaru[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(sewnde); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String innde = 찾개.group(), 새이름 = innde;
            if (!innde.startsWith("//") && !innde.startsWith("/*") && !innde.startsWith("\"") && !innde.startsWith("'") && !공개이름.contains(innde)) {
                새이름 = innde_taabal.getOrDefault(innde, innde);
                if (innde.matches("a[0-9]+")) 새이름 = "인수" + innde.substring(1);
                if (innde.matches("b[0-9]+")) 새이름 = "분기" + innde.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char alkulal_njaru : 새이름.toCharArray()) 표기.append(alkulal_njaru < 128 ? Character.toString(alkulal_njaru) : String.format(Locale.ROOT, "\\u%04x", (int)alkulal_njaru));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(함수참조 juɓɓol_njaru, tergal_keɓe keɓe, Map<String,String> 기계표, String faandaare) {
        String 표식 = 기호("method", juɓɓol_njaru.부분들());
        List<String> diidol = new ArrayList<>();
        if ((keɓe.naatde_naatnugol & 0x100) != 0) {
            String seŋaade = 기계표.get(juɓɓol_njaru.innde + juɓɓol_njaru.서술);
            if (!juɓɓol_njaru.소유.equals(faandaare.equals("kernel") ? "kaɓirgal_njaru" : "kuutoro") || seŋaade == null) throw new 번역오류("허용되지 않은 native juɓɓol_njaru");
            return ".text\n" + 표식 + ":\njmp " + seŋaade;
        }
        byte[] 본문 = keɓe.mbaadi_njaru.get("Code"); if (본문 == null) throw new 번역오류("juɓɓol_njaru 몸체가 없음");
        keɓe_Tarirgal Tarirgal_njaru = new keɓe_Tarirgal(본문); Tarirgal_njaru.두바이트(); int 지역수 = Tarirgal_njaru.두바이트();
        keɓe_Tarirgal ginol_keɓe = new keɓe_Tarirgal(Tarirgal_njaru.읽기(Tarirgal_njaru.네바이트()));
        if (Tarirgal_njaru.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 formaa_njaru = new 함수형식(juɓɓol_njaru.서술); if (지역수 < formaa_njaru.인수.size()) throw new 번역오류("매개변수보다 적은 nokkuwal_njaajeendi 변수");
        Collections.addAll(diidol,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formaa_njaru.인수.size(); 순번++) Collections.addAll(diidol,"movl " + (8 + 4 * (formaa_njaru.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        fedde_keɓe fedde_njaru = 클래스들.get(juɓɓol_njaru.소유); Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (ginol_keɓe.위치 < ginol_keɓe.keɓe.length) {
            int 위치 = ginol_keɓe.위치, ginol = ginol_keɓe.한바이트(); String 자리 = 표식 + "_b" + 위치;
            diidol.add(자리 + ":"); 경계들.add(위치);
            if (ginol == 0) diidol.add("nop");
            else if (ginol == 1) diidol.add("pushl $0");
            else if (ginol >= 2 && ginol <= 8) diidol.add("pushl $" + (ginol - 3));
            else if (ginol == 16 || ginol == 17) diidol.add("pushl $" + (ginol == 16 ? ginol_keɓe.부호한바이트() : ginol_keɓe.부호두바이트()));
            else if (ginol == 18 || ginol == 19) {
                int joopirdu = ginol == 18 ? ginol_keɓe.한바이트() : ginol_keɓe.두바이트();
                diidol.add("pushl $" + 엑스상수(fedde_njaru,joopirdu));
            } else if (ginol == 21 || ginol == 25 || (ginol >= 26 && ginol <= 29) || (ginol >= 42 && ginol <= 45) || ginol == 54 || ginol == 58 || (ginol >= 59 && ginol <= 62) || (ginol >= 75 && ginol <= 78)) {
                boolean 읽음 = ginol < 54; int joopirdu = ginol == 21 || ginol == 25 || ginol == 54 || ginol == 58 ? ginol_keɓe.한바이트() : ginol - (ginol <= 29 ? 26 : ginol <= 45 ? 42 : ginol <= 62 ? 59 : 75);
                sek_nokkuwal(joopirdu,지역수); diidol.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (joopirdu + 1)) + "(%ebp)");
            } else if (ginol == 46) Collections.addAll(diidol,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (ginol == 79) Collections.addAll(diidol,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (ginol == 87 || ginol == 88) diidol.add("addl $" + (ginol == 87 ? 4 : 8) + ", %esp");
            else if (ginol >= 89 && ginol <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] deggondiral_Doggol = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[ginol - 89]; 순번++) diidol.add("popl " + 저장기들[순번]);
                for (int 순번 : deggondiral_Doggol[ginol - 89]) diidol.add("pushl " + 저장기들[순번]);
            } else if (ginol == 96 || ginol == 100 || ginol == 104 || ginol == 126 || ginol == 128 || ginol == 130) {
                String hiisoore_njaru = ginol == 96 ? "addl" : ginol == 100 ? "subl" : ginol == 104 ? "imull" : ginol == 126 ? "andl" : ginol == 128 ? "orl" : "xorl";
                Collections.addAll(diidol,"popl %ecx","popl %eax",hiisoore_njaru + " %ecx, %eax","pushl %eax");
            } else if (ginol == 108 || ginol == 112) Collections.addAll(diidol,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (ginol == 108 ? "%eax" : "%edx"));
            else if (ginol == 116) diidol.add("negl (%esp)");
            else if (ginol == 120 || ginol == 122 || ginol == 124) Collections.addAll(diidol,"popl %ecx","popl %eax",(ginol == 120 ? "sall" : ginol == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (ginol == 132) {
                int joopirdu = ginol_keɓe.한바이트(), 증가 = ginol_keɓe.부호한바이트(); sek_nokkuwal(joopirdu,지역수); diidol.add("addl $" + 증가 + ", -" + (4 * (joopirdu + 1)) + "(%ebp)");
            } else if (ginol >= 145 && ginol <= 147) Collections.addAll(diidol,"popl %eax",ginol == 145 ? "movsbl %al, %eax" : ginol == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (ginol >= 153 && ginol <= 166) {
                if (ginol <= 158) Collections.addAll(diidol,"popl %eax","testl %eax, %eax");
                else Collections.addAll(diidol,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int tiindaare_njaru = 위치 + ginol_keɓe.부호두바이트(); 분기들.add(tiindaare_njaru); diidol.add(비교들[ginol - (ginol <= 158 ? 153 : 159)] + " " + 표식 + "_b" + tiindaare_njaru);
            } else if (ginol == 167 || ginol == 200) {
                int tiindaare_njaru = 위치 + (ginol == 167 ? ginol_keɓe.부호두바이트() : ginol_keɓe.네바이트()); 분기들.add(tiindaare_njaru); diidol.add("jmp " + 표식 + "_b" + tiindaare_njaru);
            } else if (ginol == 170 || ginol == 171) {
                while (ginol_keɓe.위치 % 4 != 0) ginol_keɓe.한바이트();
                int lasli_njaru = 위치 + ginol_keɓe.네바이트(); 분기들.add(lasli_njaru); diidol.add("popl %eax");
                int 개수, 아래 = 0;
                if (ginol == 170) { 아래 = ginol_keɓe.네바이트(); int 위 = ginol_keɓe.네바이트(); long njuuteendi_njaru = (long)위 - 아래 + 1; if (njuuteendi_njaru < 1 || njuuteendi_njaru > (ginol_keɓe.keɓe.length - ginol_keɓe.위치) / 4) throw new 번역오류("switch kilip juumre"); 개수 = (int)njuuteendi_njaru; }
                else { 개수 = ginol_keɓe.네바이트(); if (개수 < 0 || 개수 > (ginol_keɓe.keɓe.length - ginol_keɓe.위치) / 8) throw new 번역오류("switch waylude_etannde juumre"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int njaru = ginol == 170 ? 아래 + 순번 : ginol_keɓe.네바이트(), tiindaare_njaru = 위치 + ginol_keɓe.네바이트(); 분기들.add(tiindaare_njaru);
                    Collections.addAll(diidol,"cmpl $" + njaru + ", %eax","je " + 표식 + "_b" + tiindaare_njaru);
                }
                diidol.add("jmp " + 표식 + "_b" + lasli_njaru);
            } else if (ginol == 172 || ginol == 176 || ginol == 177) {
                if (ginol != 177) diidol.add("popl %eax"); Collections.addAll(diidol,"leave","ret");
            } else if (ginol == 178 || ginol == 179) {
                함수참조 참조 = fedde_njaru.참조(ginol_keɓe.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 suudu_njaru");
                Collections.addAll(diidol,"call " + 기호("init",참조.소유),(ginol == 178 ? "pushl " : "popl ") + 기호("field",참조.부분들()));
            } else if (ginol == 184) {
                함수참조 참조 = fedde_njaru.참조(ginol_keɓe.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 juɓɓol_njaru");
                함수형식 호출형식 = new 함수형식(참조.서술); Collections.addAll(diidol,"call " + 기호("init",참조.소유),"call " + 기호("method",참조.부분들()));
                if (!호출형식.인수.isEmpty()) diidol.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) diidol.add("pushl %eax");
            } else if (ginol == 182) {
                함수참조 참조 = fedde_njaru.참조(ginol_keɓe.두바이트());
                if (참조.equals(new 함수참조("java/lang/String","length","()I"))) Collections.addAll(diidol,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (참조.equals(new 함수참조("java/lang/String","charAt","(I)C"))) Collections.addAll(diidol,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 번역오류("가상 juɓɓol_njaru 호출 미지원");
            } else if (ginol == 188) {
                if (ginol_keɓe.한바이트() != 10) throw new 번역오류("new int[]만 ballital_njaru"); Collections.addAll(diidol,"popl %eax","call rt_new_array","pushl %eax");
            } else if (ginol == 190) Collections.addAll(diidol,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (ginol == 196) {
                int timmital_njaru = ginol_keɓe.한바이트(), joopirdu = ginol_keɓe.두바이트(); sek_nokkuwal(joopirdu,지역수);
                if (timmital_njaru == 21 || timmital_njaru == 25 || timmital_njaru == 54 || timmital_njaru == 58) diidol.add((timmital_njaru <= 25 ? "pushl " : "popl ") + "-" + 4 * (joopirdu + 1) + "(%ebp)");
                else if (timmital_njaru == 132) diidol.add("addl $" + ginol_keɓe.부호두바이트() + ", -" + 4 * (joopirdu + 1) + "(%ebp)");
                else throw new 번역오류("wide ginol 미지원");
            } else if (ginol == 198 || ginol == 199) {
                int tiindaare_njaru = 위치 + ginol_keɓe.부호두바이트(); 분기들.add(tiindaare_njaru); Collections.addAll(diidol,"popl %eax","testl %eax, %eax",(ginol == 198 ? "je " : "jne ") + 표식 + "_b" + tiindaare_njaru);
            } else throw new 번역오류("미지원 ginol: " + ginol);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("ginol 경계가 아닌 곳으로 분기");
        diidol.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",diidol);
    }
    String 엑스상수(fedde_keɓe keɓe, int joopirdu) {
        if (keɓe.상수종류[joopirdu] == 3) return keɓe.상수값[joopirdu].toString();
        if (keɓe.상수종류[joopirdu] == 8) return 문자열기호(keɓe.문자((Integer)keɓe.상수값[joopirdu]));
        throw new 번역오류("정수와 ɓoggol_njaru 상수만 ballital_njaru");
    }
    String 엑스조립본(String naatnugol_toɓɓere, List<String> 내보냄, String faandaare) throws IOException {
        Map<String,String> 기계표 = new HashMap<>();
        for (String diidol : Files.readAllLines(wallitorde_laawol.resolve("엑스기계함수.tsv"))) { String[] linngondirde_njaru = diidol.split("\t"); if (linngondirde_njaru[0].equals(faandaare)) 기계표.put(linngondirde_njaru[1] + linngondirde_njaru[2],linngondirde_njaru[3]); }
        int 자리 = naatnugol_toɓɓere.lastIndexOf('.'); if (자리 < 0) throw new 번역오류("naatnugol_toɓɓere 지정 juumre");
        String 소유 = naatnugol_toɓɓere.substring(0,자리).replace('.','/'), 함수이름 = naatnugol_toɓɓere.substring(자리 + 1); 함수참조 naatnugol_toɓɓere_njaru = null;
        for (String 서술 : Arrays.asList("()I","()V")) { 함수참조 참조 = new 함수참조(소유,함수이름,서술); if (함수들.containsKey(참조)) { if (naatnugol_toɓɓere_njaru != null) throw new 번역오류("겹친 naatnugol_toɓɓere"); naatnugol_toɓɓere_njaru = 참조; } }
        if (naatnugol_toɓɓere_njaru == null || (함수들.get(naatnugol_toɓɓere_njaru).naatde_naatnugol & 0x100) != 0) throw new 번역오류("naatnugol_toɓɓere_njaru juɓɓol_njaru formaa_njaru juumre");
        List<String> diidol = new ArrayList<>(); diidol.add(".code32");
        for (fedde_keɓe keɓe : 클래스들.values()) {
            String ngonka_njaru = 기호("state",keɓe.innde), ɓamtinde = 기호("init",keɓe.innde);
            Collections.addAll(diidol,".bss",".balign 4",ngonka_njaru + ": .long 0",".text",ɓamtinde + ":","cmpl $0, " + ngonka_njaru,"jne " + ɓamtinde + "_done","movl $1, " + ngonka_njaru);
            함수참조 초기화참조 = new 함수참조(keɓe.innde,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) diidol.add("call " + 기호("method",초기화참조.부분들()));
            Collections.addAll(diidol,"movl $2, " + ngonka_njaru,ɓamtinde + "_done:","ret");
            for (tergal_keɓe suudu_njaru : keɓe.suudu_njaru) {
                byte[] 상수 = suudu_njaru.mbaadi_njaru.get("ConstantValue"); String njaru = 상수 == null ? "0" : 엑스상수(keɓe,new keɓe_Tarirgal(상수).두바이트());
                Collections.addAll(diidol,".data",".balign 4",기호("field",keɓe.innde,suudu_njaru.innde,suudu_njaru.서술) + ": .long " + njaru);
            }
            for (tergal_keɓe juɓɓol_njaru : keɓe.juɓɓol_njaru) if (!juɓɓol_njaru.innde.equals("<init>")) diidol.add(엑스함수본문(new 함수참조(keɓe.innde,juɓɓol_njaru.innde,juɓɓol_njaru.서술),juɓɓol_njaru,기계표,faandaare));
        }
        Collections.addAll(diidol,".text",".globl java_entry","java_entry:","call " + 기호("init",naatnugol_toɓɓere_njaru.소유),"call " + 기호("method",naatnugol_toɓɓere_njaru.부분들()));
        if (naatnugol_toɓɓere_njaru.서술.equals("()V")) diidol.add("xorl %eax, %eax"); diidol.add("ret");
        for (String 지정 : 내보냄) {
            int 구분 = 지정.indexOf('='); if (구분 < 1) throw new 번역오류("내보내기 지정 juumre");
            String 외부 = 지정.substring(0,구분), juɓɓol_njaru = 지정.substring(구분 + 1); int 나눔 = juɓɓol_njaru.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 기호 juumre");
            String fedde_njaru = juɓɓol_njaru.substring(0,나눔).replace('.','/'), innde = juɓɓol_njaru.substring(나눔 + 1); 함수참조 cuɓal_njaru = null;
            for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(fedde_njaru) && 참조.innde.equals(innde)) { if (cuɓal_njaru != null) throw new 번역오류("겹친 내보내기 faandaare"); cuɓal_njaru = 참조; }
            if (cuɓal_njaru == null) throw new 번역오류("내보낼 함수가 없음");
            Collections.addAll(diidol,".text",".globl " + 외부,외부 + ":","call " + 기호("init",cuɓal_njaru.소유),"jmp " + 기호("method",cuɓal_njaru.부분들()));
        }
        diidol.add(".section .rodata");
        for (Map.Entry<String,String> naatnugol_njaru : 문자열들.entrySet()) {
            Collections.addAll(diidol,".balign 4",naatnugol_njaru.getValue() + ":",".long " + naatnugol_njaru.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char ngootoñ_njaru : naatnugol_njaru.getKey().toCharArray()) 단위들.add(Integer.toString(ngootoñ_njaru)); if (!단위들.isEmpty()) diidol.add(".long " + String.join(",",단위들));
        }
        diidol.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",diidol) + "\n";
    }
    static void 도구실행(List<String> ginol) throws Exception {
        if (new ProcessBuilder(ginol).inheritIO().start().waitFor() != 0) throw new 번역오류("tafde_sewnde juumre: " + ginol.get(0));
    }
    static String keɓe_ɓoggol(String binndi) { return "\"" + binndi.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String faandaare, String naatnugol_toɓɓere, List<String> 내보냄, Path 출력, Path wallitorde_njaru) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), fedde_laawol = 임시.resolve("classes"); Files.createDirectory(fedde_laawol);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",fedde_laawol.toString(),"-sourcepath",fedde_laawol.toString(),"-d",fedde_laawol.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new 번역오류("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new 번역오류(".java 또는 .class만 ballital_njaru");
            }
            if (원문수 > 0) 도구실행(자바명령);
            try (java.util.stream.Stream<Path> laawol_Doggol = Files.walk(fedde_laawol)) { laawol_Doggol.filter(laawol -> laawol.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,faandaare.equals("user") ? "user" : "kernel",262144,wallitorde_njaru);
            String 조립 = 변환.엑스조립본(naatnugol_toɓɓere,내보냄,faandaare); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = wallitorde_njaru.getParent();
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("실행지원.s").toString()));
            List<String> seŋaade = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (faandaare.equals("kernel")) seŋaade.add("-r");
            else {
                도구실행(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(faandaare.equals("user") ? "huɓɓude_kuutoro_tafirde.s" : "리눅스시작.s").toString()));
                Collections.addAll(seŋaade,"-e","_start",임시.resolve("start.o").toString());
                if (faandaare.equals("user")) Collections.addAll(seŋaade,"-T",도구위치.resolve("kuutoro_jokkere_lelngo.ld").toString());
            }
            Collections.addAll(seŋaade,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); 도구실행(seŋaade);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path saaktude_njaru = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),saaktude_njaru,StandardCopyOption.REPLACE_EXISTING); Files.move(saaktude_njaru,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(saaktude_njaru); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(faandaare.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> 기호자료 = new ArrayList<>(), sewnde_keɓe = new ArrayList<>();
            for (함수참조 참조 : 변환.함수들.keySet()) 기호자료.add(keɓe_ɓoggol(기호("method",참조.부분들())) + ":" + keɓe_ɓoggol(참조.소유 + "." + 참조.innde + 참조.서술));
            for (Path 입력 : 입력들) {
                byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder binndi = new StringBuilder(); for (byte njaru : 해시) binndi.append(String.format(Locale.ROOT,"%02x",njaru & 255));
                sewnde_keɓe.add(keɓe_ɓoggol(입력.toAbsolutePath().toString()) + ":" + keɓe_ɓoggol(binndi.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + keɓe_ɓoggol(faandaare) + ",\"entry\":" + keɓe_ɓoggol(naatnugol_toɓɓere) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",기호자료) + "},\"sources\":{" + String.join(",",sewnde_keɓe) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> laawol_Doggol = Files.walk(임시)) { for (Path laawol : (Iterable<Path>)laawol_Doggol.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(laawol); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String naatnugol_toɓɓere = null, faandaare = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> laawol_Doggol = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String njaru = 인수[순번];
                switch (njaru) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry fedde_njaru.juɓɓol_njaru -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export 기호=fedde_njaru.juɓɓol_njaru] 클래스파일 또는 Java원문"); return;
                    case "--entry": naatnugol_toɓɓere = 인수[++순번]; break;
                    case "--profile": faandaare = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (njaru.startsWith("-")) throw new 번역오류("알 수 없는 옵션: " + njaru); laawol_Doggol.add(Paths.get(njaru));
                }
            }
            if (naatnugol_toɓɓere == null || 출력경로 == null || laawol_Doggol.isEmpty()) throw new 번역오류("--entry, -o, fedde_njaru 파일이 필요합니다");
            Path wallitorde_njaru = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new 번역오류("알 수 없는 실행 faandaare");
                엑스번역(laawol_Doggol,엑스대상,naatnugol_toɓɓere,내보냄,출력경로,wallitorde_njaru); return;
            }
            String sewnde = new 기계어미리번역(laawol_Doggol, faandaare, 낱말수, wallitorde_njaru).생성(naatnugol_toɓɓere, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, sewnde, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception juumre) { System.err.println("tafde_sewnde juumre: " + juumre.getMessage()); System.exit(1); }
    }
}
