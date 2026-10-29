// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java akotchijuushi_ajutuu_55654bf1 파일에서 독립 ARM64 커널용 C 원문을 만든다. epiajatü JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class 번역오류 extends RuntimeException {
        번역오류(String 설명) { super(설명); }
    }
    static final class atijaaya_aashaje_erülü {
        final byte[] atijaaya;
        int 위치;
        atijaaya_aashaje_erülü(byte[] 입력자료) { atijaaya = 입력자료; }
        byte[] 읽기(int akaliaa_ajutuu) {
            if (akaliaa_ajutuu < 0 || akaliaa_ajutuu > atijaaya.length - 위치) throw new 번역오류("잘린 akotchijuushi_ajutuu_55654bf1 또는 aluwataaya atijaaya");
            byte[] 결과 = Arrays.copyOfRange(atijaaya, 위치, 위치 + akaliaa_ajutuu); 위치 += akaliaa_ajutuu; return 결과;
        }
        int 한바이트() { if (위치 >= atijaaya.length) throw new 번역오류("잘린 aluwataaya atijaaya"); return atijaaya[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class a_akaajatü_atijaaya {
        final int a_ttaaya_ekeroliaa;
        final String 이름, 서술;
        final Map<String, byte[]> anaajaalaakua_ipa_ajutuu;
        a_akaajatü_atijaaya(int a_ttaaya_ajutuu, String 이름값, String 서술값, Map<String, byte[]> anaajaalaakua_ipa_atijaaya) {
            a_ttaaya_ekeroliaa = a_ttaaya_ajutuu; 이름 = 이름값; 서술 = 서술값; anaajaalaakua_ipa_ajutuu = anaajaalaakua_ipa_atijaaya;
        }
    }
    static final class 함수참조 implements Comparable<함수참조> {
        final String 소유, 이름, 서술;
        함수참조(String 소유값, String 이름값, String 서술값) { 소유 = 소유값; 이름 = 이름값; 서술 = 서술값; }
        String[] 부분들() { return new String[]{소유, 이름, 서술}; }
        public int compareTo(함수참조 wanaawasü_ajutuu) {
            int 비교값 = 소유.compareTo(wanaawasü_ajutuu.소유);
            if (비교값 == 0) 비교값 = 이름.compareTo(wanaawasü_ajutuu.이름);
            return 비교값 == 0 ? 서술.compareTo(wanaawasü_ajutuu.서술) : 비교값;
        }
        public boolean equals(Object wanaawasü_ajutuu) { return wanaawasü_ajutuu instanceof 함수참조 && compareTo((함수참조) wanaawasü_ajutuu) == 0; }
        public int hashCode() { return Objects.hash(소유, 이름, 서술); }
    }
    static final class akotchijuushi_atijaaya {
        final int[] 상수종류;
        final Object[] waneepiajutu_atijaaya;
        final String 이름;
        final List<a_akaajatü_atijaaya> apülajanaa_ajutuu, 함수;
        akotchijuushi_atijaaya(Path wopu_a_ttaaleemüin) throws IOException {
            atijaaya_aashaje_erülü aashaje_erülü_ajutuu = new atijaaya_aashaje_erülü(Files.readAllBytes(wopu_a_ttaaleemüin));
            if (aashaje_erülü_ajutuu.네바이트() != 0xcafebabe) throw new 번역오류("Java akotchijuushi_ajutuu_55654bf1 표식이 아님");
            aashaje_erülü_ajutuu.읽기(4);
            int 개수 = aashaje_erülü_ajutuu.두바이트(); 상수종류 = new int[개수]; waneepiajutu_atijaaya = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = aashaje_erülü_ajutuu.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int akaliaa_ajutuu = aashaje_erülü_ajutuu.두바이트();
                        byte[] jeerü_puuperü = aashaje_erülü_ajutuu.읽기(akaliaa_ajutuu), 길이붙인자료 = new byte[akaliaa_ajutuu + 2];
                        길이붙인자료[0] = (byte)(akaliaa_ajutuu >> 8); 길이붙인자료[1] = (byte)akaliaa_ajutuu;
                        System.arraycopy(jeerü_puuperü, 0, 길이붙인자료, 2, akaliaa_ajutuu);
                        waneepiajutu_atijaaya[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: waneepiajutu_atijaaya[순번] = aashaje_erülü_ajutuu.네바이트(); break;
                    case 4: aashaje_erülü_ajutuu.읽기(4); break;
                    case 5: case 6: aashaje_erülü_ajutuu.읽기(8); 순번++; break;
                    case 7: case 8: case 16: waneepiajutu_atijaaya[순번] = aashaje_erülü_ajutuu.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        waneepiajutu_atijaaya[순번] = new int[]{aashaje_erülü_ajutuu.두바이트(), aashaje_erülü_ajutuu.두바이트()}; break;
                    case 15: waneepiajutu_atijaaya[순번] = new int[]{aashaje_erülü_ajutuu.한바이트(), aashaje_erülü_ajutuu.두바이트()}; break;
                    default: throw new 번역오류("지원하지 않는 waneepiajutu_ajutuu 종류: " + 종류);
                }
            }
            aashaje_erülü_ajutuu.두바이트(); 이름 = 클래스명(aashaje_erülü_ajutuu.두바이트());
            if (!클래스명(aashaje_erülü_ajutuu.두바이트()).equals("java/lang/Object") || aashaje_erülü_ajutuu.두바이트() != 0)
                throw new 번역오류(이름 + ": 상속 및 인터페이스 미지원");
            apülajanaa_ajutuu = 멤버읽기(aashaje_erülü_ajutuu); 함수 = 멤버읽기(aashaje_erülü_ajutuu); 속성읽기(aashaje_erülü_ajutuu);
            if (aashaje_erülü_ajutuu.위치 != aashaje_erülü_ajutuu.atijaaya.length) throw new 번역오류("akotchijuushi_ajutuu_55654bf1 뒤에 남은 atijaaya");
        }
        String 문자(int ee_iyatialujuna) {
            if (ee_iyatialujuna < 1 || ee_iyatialujuna >= 상수종류.length || 상수종류[ee_iyatialujuna] != 1) throw new 번역오류("문자 waneepiajutu_ajutuu ee_iyatialujuna ajachitia");
            return (String) waneepiajutu_atijaaya[ee_iyatialujuna];
        }
        String 클래스명(int ee_iyatialujuna) {
            if (ee_iyatialujuna < 1 || ee_iyatialujuna >= 상수종류.length || 상수종류[ee_iyatialujuna] != 7) throw new 번역오류("akotchijuushi_ajutuu_55654bf1 참조 ajachitia");
            return 문자((Integer)waneepiajutu_atijaaya[ee_iyatialujuna]);
        }
        함수참조 참조(int ee_iyatialujuna) {
            if (ee_iyatialujuna < 1 || ee_iyatialujuna >= 상수종류.length || 상수종류[ee_iyatialujuna] < 9 || 상수종류[ee_iyatialujuna] > 11) throw new 번역오류("멤버 참조 ajachitia");
            int[] 쌍 = (int[])waneepiajutu_atijaaya[ee_iyatialujuna], 이름쌍 = (int[])waneepiajutu_atijaaya[쌍[1]];
            return new 함수참조(클래스명(쌍[0]), 문자(이름쌍[0]), 문자(이름쌍[1]));
        }
        Map<String, byte[]> 속성읽기(atijaaya_aashaje_erülü aashaje_erülü_ajutuu) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = aashaje_erülü_ajutuu.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String 속성이름 = 문자(aashaje_erülü_ajutuu.두바이트()); byte[] ajutuu = aashaje_erülü_ajutuu.읽기(aashaje_erülü_ajutuu.네바이트());
                if (결과.put(속성이름, ajutuu) != null) throw new 번역오류("겹친 anaajaalaakua_ipa_ajutuu: " + 속성이름);
            }
            return 결과;
        }
        List<a_akaajatü_atijaaya> 멤버읽기(atijaaya_aashaje_erülü aashaje_erülü_ajutuu) {
            List<a_akaajatü_atijaaya> 결과 = new ArrayList<>(); int 개수 = aashaje_erülü_ajutuu.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int a_ttaaya_ekeroliaa = aashaje_erülü_ajutuu.두바이트(); String 함수이름 = 문자(aashaje_erülü_ajutuu.두바이트()), 서술 = 문자(aashaje_erülü_ajutuu.두바이트());
                결과.add(new a_akaajatü_atijaaya(a_ttaaya_ekeroliaa, 함수이름, 서술, 속성읽기(aashaje_erülü_ajutuu)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new 번역오류("함수 서술 ajachitia: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new 번역오류("함수 서술 ajachitia: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new 번역오류("함수 서술 ajachitia: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String 선택 = null;
            for (String akua_ipaa_ajutuu : 허용형식) if (서술.startsWith(akua_ipaa_ajutuu, 위치)) { 선택 = akua_ipaa_ajutuu; break; }
            if (선택 == null) throw new 번역오류("지원하지 않는 atijaayakua_ipa: " + 서술);
            결과.add(선택); 위치 += 선택.length();
        }
        return 결과;
    }
    static String 기호(String 종류, String... 부분들) {
        try {
            byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder 글 = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) 글.append(String.format(Locale.ROOT, "%02x", 해시[순번] & 255));
            return 글.toString();
        } catch (Exception ajachitia) { throw new 번역오류(ajachitia.toString()); }
    }
    final Map<String, akotchijuushi_atijaaya> 클래스들 = new TreeMap<>();
    final Map<함수참조, a_akaajatü_atijaaya> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, 기계클래스;
    final int 동적기억낱말수;
    final Path ama_anaajatü_wopu_a_ttaaleemüin;
    기계어미리번역(List<Path> 경로들, String 대상, int 낱말수, Path ama_anaajatü_ajutuu) throws IOException {
        if ((!대상.equals("kernel") && !대상.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new 번역오류("실행 대상 또는 기억 공간 크기 ajachitia");
        실행대상 = 대상; 동적기억낱말수 = 낱말수; ama_anaajatü_wopu_a_ttaaleemüin = ama_anaajatü_ajutuu;
        // 이 이름도 국가별 eejeejetülein_wunu_ulia 생성 시 해당 언어로 옮긴다.
        기계클래스 = 대상.equals("kernel") ? "보드" : "ka_yataayakalü";
        for (String liinia : Files.readAllLines(ama_anaajatü_ajutuu.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = liinia.split("\t", -1);
            if (부분들.length != 4) throw new 번역오류("기계 함수 atijaaya ajachitia");
            if (부분들[0].equals(대상)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path wopu_a_ttaaleemüin : 경로들) {
            akotchijuushi_atijaaya atijaaya = new akotchijuushi_atijaaya(wopu_a_ttaaleemüin);
            if (클래스들.put(atijaaya.이름, atijaaya) != null) throw new 번역오류("중복 akotchijuushi_ajutuu_55654bf1: " + atijaaya.이름);
            for (a_akaajatü_atijaaya apülajanaa_ajutuu : atijaaya.apülajanaa_ajutuu) {
                if ((apülajanaa_ajutuu.a_ttaaya_ekeroliaa & 8) == 0 || 형식읽기(apülajanaa_ajutuu.서술).equals(Collections.singletonList("V"))) throw new 번역오류("jimatüsü_ajutuu 필드만 akaaliijiaa_ajutuu");
                if (필드들.put(new 함수참조(atijaaya.이름, apülajanaa_ajutuu.이름, apülajanaa_ajutuu.서술), apülajanaa_ajutuu) != null) throw new 번역오류("중복 apülajanaa_ajutuu");
            }
            for (a_akaajatü_atijaaya 함수 : atijaaya.함수) {
                if (함수.이름.equals("<init>")) continue;
                if ((함수.a_ttaaya_ekeroliaa & 8) == 0 || (함수.a_ttaaya_ekeroliaa & (0x20 | 0x400)) != 0) throw new 번역오류("jimatüsü_ajutuu 비동기화 함수만 akaaliijiaa_ajutuu");
                new 함수형식(함수.서술);
                if (함수들.put(new 함수참조(atijaaya.이름, 함수.이름, 함수.서술), 함수) != null) throw new 번역오류("중복 함수");
            }
        }
    }
    String 문자열기호(String 글) { return 문자열들.computeIfAbsent(글, ajutuu -> "j_text_" + 문자열들.size()); }
    String waneepiajutu_ajutukumajiaa(akotchijuushi_atijaaya atijaaya, int ee_iyatialujuna) {
        if (ee_iyatialujuna < 1 || ee_iyatialujuna >= atijaaya.상수종류.length) throw new 번역오류("waneepiajutu_ajutuu ee_iyatialujuna külipü_ayaakuaapijana ajachitia");
        if (atijaaya.상수종류[ee_iyatialujuna] == 3) return "(word)(uint32_t)(" + atijaaya.waneepiajutu_atijaaya[ee_iyatialujuna] + ")";
        if (atijaaya.상수종류[ee_iyatialujuna] == 8) return "(word)" + 문자열기호(atijaaya.문자((Integer)atijaaya.waneepiajutu_atijaaya[ee_iyatialujuna]));
        throw new 번역오류("정수와 kaleena_ajutuu 상수만 akaaliijiaa_ajutuu");
    }
    String 함수원형(함수참조 참조) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(참조.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + 기호("method", 참조.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void 지역검사(int ee_iyatialujuna, int 지역변수수) { if (ee_iyatialujuna < 0 || ee_iyatialujuna >= 지역변수수) throw new 번역오류("지역 변수 ee_iyatialujuna külipü_ayaakuaapijana ajachitia"); }
    void 분기넣기(List<String> 출력, Set<Integer> 분기들, int 위치, int 이동량, String mülein) {
        int jalamüinjatü_ajutuu = 위치 + 이동량; 분기들.add(jalamüinjatü_ajutuu);
        출력.add((mülein == null ? "" : "if (" + mülein + ") ") + "goto b" + jalamüinjatü_ajutuu + ";");
    }
    String 함수본문(함수참조 함수, a_akaajatü_atijaaya atijaaya) {
        byte[] 본문자료 = atijaaya.anaajaalaakua_ipa_ajutuu.get("Code"); if (본문자료 == null) throw new 번역오류("함수 몸체가 없음: " + 함수.이름);
        atijaaya_aashaje_erülü aashaje_erülü_ajutuu = new atijaaya_aashaje_erülü(본문자료); int 쌓임깊이 = aashaje_erülü_ajutuu.두바이트(), 지역변수수 = aashaje_erülü_ajutuu.두바이트();
        atijaaya_aashaje_erülü aluwataaya_atijaaya = new atijaaya_aashaje_erülü(aashaje_erülü_ajutuu.읽기(aashaje_erülü_ajutuu.네바이트()));
        if (aashaje_erülü_ajutuu.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 akua_ipaa_ajutuu = new 함수형식(함수.서술); if (지역변수수 < akua_ipaa_ajutuu.인수.size()) throw new 번역오류("매개변수보다 적은 지역 변수");
        akotchijuushi_atijaaya akotchijuushi_ajutuu_55654bf1 = 클래스들.get(함수.소유);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(함수) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < akua_ipaa_ajutuu.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (aluwataaya_atijaaya.위치 < aluwataaya_atijaaya.atijaaya.length) {
            int 위치 = aluwataaya_atijaaya.위치, aluwataaya = aluwataaya_atijaaya.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (aluwataaya == 0) continue;
            if (aluwataaya == 1) 출력.add("PUSH(0);");
            else if (aluwataaya >= 2 && aluwataaya <= 8) 출력.add("PUSH((uint32_t)(" + (aluwataaya - 3) + "));");
            else if (aluwataaya == 16 || aluwataaya == 17) 출력.add("PUSH((uint32_t)(" + (aluwataaya == 16 ? aluwataaya_atijaaya.부호한바이트() : aluwataaya_atijaaya.부호두바이트()) + "));");
            else if (aluwataaya == 18 || aluwataaya == 19) 출력.add("PUSH(" + waneepiajutu_ajutukumajiaa(akotchijuushi_ajutuu_55654bf1, aluwataaya == 18 ? aluwataaya_atijaaya.한바이트() : aluwataaya_atijaaya.두바이트()) + ");");
            else if (aluwataaya == 21 || aluwataaya == 25 || (aluwataaya >= 26 && aluwataaya <= 29) || (aluwataaya >= 42 && aluwataaya <= 45)) {
                int ee_iyatialujuna = aluwataaya == 21 || aluwataaya == 25 ? aluwataaya_atijaaya.한바이트() : aluwataaya - (aluwataaya <= 29 ? 26 : 42);
                지역검사(ee_iyatialujuna, 지역변수수); 출력.add("PUSH(l[" + ee_iyatialujuna + "]);");
            } else if (aluwataaya == 54 || aluwataaya == 58 || (aluwataaya >= 59 && aluwataaya <= 62) || (aluwataaya >= 75 && aluwataaya <= 78)) {
                int ee_iyatialujuna = aluwataaya == 54 || aluwataaya == 58 ? aluwataaya_atijaaya.한바이트() : aluwataaya - (aluwataaya <= 62 ? 59 : 75);
                지역검사(ee_iyatialujuna, 지역변수수); 출력.add("l[" + ee_iyatialujuna + "] = POP();");
            } else if (aluwataaya == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (aluwataaya == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (aluwataaya == 87 || aluwataaya == 88) 출력.add(aluwataaya == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (aluwataaya >= 89 && aluwataaya <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] 순서들 = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[aluwataaya - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char ajutuu : 순서들[aluwataaya - 89].toCharArray()) 출력.add("PUSH(" + ajutuu + ");");
            } else if (aluwataaya == 96 || aluwataaya == 100 || aluwataaya == 104 || aluwataaya == 126 || aluwataaya == 128 || aluwataaya == 130) {
                String akumajiraa_ajutuu = aluwataaya == 96 ? "+" : aluwataaya == 100 ? "-" : aluwataaya == 104 ? "*" : aluwataaya == 126 ? "&" : aluwataaya == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + akumajiraa_ajutuu + " (uint32_t)b);");
            } else if (aluwataaya == 108 || aluwataaya == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (aluwataaya == 112 ? 1 : 0) + "));");
            else if (aluwataaya == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (aluwataaya == 120 || aluwataaya == 122 || aluwataaya == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (aluwataaya == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (aluwataaya == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (aluwataaya == 132) {
                int ee_iyatialujuna = aluwataaya_atijaaya.한바이트(), 증가량 = aluwataaya_atijaaya.부호한바이트(); 지역검사(ee_iyatialujuna, 지역변수수);
                출력.add("l[" + ee_iyatialujuna + "] = (uint32_t)l[" + ee_iyatialujuna + "] + (uint32_t)(" + 증가량 + ");");
            } else if (aluwataaya >= 145 && aluwataaya <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (aluwataaya == 145 ? "int8_t" : aluwataaya == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (aluwataaya >= 153 && aluwataaya <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, 분기들, 위치, aluwataaya_atijaaya.부호두바이트(), "(int32_t)a " + 비교들[aluwataaya - 153] + " 0");
            } else if (aluwataaya >= 159 && aluwataaya <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, 분기들, 위치, aluwataaya_atijaaya.부호두바이트(), aluwataaya >= 165 ? "a " + 비교들[aluwataaya - 159] + " b" : "(int32_t)a " + 비교들[aluwataaya - 159] + " (int32_t)b");
            } else if (aluwataaya == 167 || aluwataaya == 200) 분기넣기(출력, 분기들, 위치, aluwataaya == 167 ? aluwataaya_atijaaya.부호두바이트() : aluwataaya_atijaaya.네바이트(), null);
            else if (aluwataaya == 170 || aluwataaya == 171) {
                while (aluwataaya_atijaaya.위치 % 4 != 0) aluwataaya_atijaaya.한바이트();
                int ajutuu_aneekuushitüjülia = aluwataaya_atijaaya.네바이트(); 출력.add("a = POP();");
                if (aluwataaya == 170) {
                    int 아래 = aluwataaya_atijaaya.네바이트(), 위 = aluwataaya_atijaaya.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (aluwataaya_atijaaya.atijaaya.length - aluwataaya_atijaaya.위치) / 4) throw new 번역오류("switch külipü_ayaakuaapijana ajachitia");
                    for (long ajutuu = 아래; ajutuu <= 위; ajutuu++) 분기넣기(출력, 분기들, 위치, aluwataaya_atijaaya.네바이트(), "(int32_t)a == (" + ajutuu + ")");
                } else {
                    int 개수 = aluwataaya_atijaaya.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (aluwataaya_atijaaya.atijaaya.length - aluwataaya_atijaaya.위치) / 8) throw new 번역오류("switch 크기 ajachitia");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int ajutuu = aluwataaya_atijaaya.네바이트(); if (순번 > 0 && ajutuu <= 앞값) throw new 번역오류("switch anaajiaakua_ipa_ajutuu ajachitia"); 앞값 = ajutuu;
                        분기넣기(출력, 분기들, 위치, aluwataaya_atijaaya.네바이트(), "(int32_t)a == (" + ajutuu + ")");
                    }
                }
                분기넣기(출력, 분기들, 위치, ajutuu_aneekuushitüjülia, null);
            } else if (aluwataaya == 172 || aluwataaya == 176 || aluwataaya == 177) 출력.add("return " + (aluwataaya == 177 ? "0" : "POP()") + ";");
            else if (aluwataaya == 178 || aluwataaya == 179) {
                함수참조 참조 = akotchijuushi_ajutuu_55654bf1.참조(aluwataaya_atijaaya.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 apülajanaa_ajutuu");
                출력.add(기호("init", 참조.소유) + "();"); String apülajanaa_ajutuu = 기호("field", 참조.부분들());
                출력.add(aluwataaya == 178 ? "PUSH(" + apülajanaa_ajutuu + ");" : apülajanaa_ajutuu + " = POP();");
            } else if (aluwataaya == 184) {
                함수참조 참조 = akotchijuushi_ajutuu_55654bf1.참조(aluwataaya_atijaaya.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 함수");
                함수형식 호출형식 = new 함수형식(참조.서술); int 개수 = 호출형식.인수.size();
                출력.add(기호("init", 참조.소유) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + 기호("method", 참조.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (aluwataaya == 182) {
                함수참조 참조 = akotchijuushi_ajutuu_55654bf1.참조(aluwataaya_atijaaya.두바이트());
                if (참조.equals(new 함수참조("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (참조.equals(new 함수참조("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 번역오류("가상 함수 호출 미지원");
            } else if (aluwataaya == 188) {
                if (aluwataaya_atijaaya.한바이트() != 10) throw new 번역오류("new int[]만 akaaliijiaa_ajutuu"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (aluwataaya == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (aluwataaya == 196) {
                int e_irukuu_ajutuu = aluwataaya_atijaaya.한바이트(), ee_iyatialujuna = aluwataaya_atijaaya.두바이트(); 지역검사(ee_iyatialujuna, 지역변수수);
                if (e_irukuu_ajutuu == 21 || e_irukuu_ajutuu == 25) 출력.add("PUSH(l[" + ee_iyatialujuna + "]);");
                else if (e_irukuu_ajutuu == 54 || e_irukuu_ajutuu == 58) 출력.add("l[" + ee_iyatialujuna + "] = POP();");
                else if (e_irukuu_ajutuu == 132) 출력.add("l[" + ee_iyatialujuna + "] = (uint32_t)l[" + ee_iyatialujuna + "] + (uint32_t)(" + aluwataaya_atijaaya.부호두바이트() + ");");
                else throw new 번역오류("미지원 wide aluwataaya");
            } else if (aluwataaya == 198 || aluwataaya == 199) {
                출력.add("a = POP();"); 분기넣기(출력, 분기들, 위치, aluwataaya_atijaaya.부호두바이트(), "a " + (aluwataaya == 198 ? "==" : "!=") + " 0");
            } else throw new 번역오류(함수.소유 + "." + 함수.이름 + ", waai_ajutuu " + 위치 + ": 미지원 aluwataaya " + aluwataaya);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("aluwataaya 경계가 아닌 곳으로 분기");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String 내보낼함수(String 연결기호, String 대상, boolean 진입점여부) {
        int 자리 = 대상.lastIndexOf('.'); if (자리 < 0 || !연결기호.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 지정 ajachitia");
        String 소유 = 대상.substring(0, 자리).replace('.', '/'), 이름 = 대상.substring(자리 + 1); 함수참조 선택 = null;
        for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(소유) && 참조.이름.equals(이름)) {
            if (선택 != null) throw new 번역오류("겹친 내보내기 대상"); 선택 = 참조;
        }
        if (선택 == null || (함수들.get(선택).a_ttaaya_ekeroliaa & 0x100) != 0) throw new 번역오류("내보낼 함수가 없음 또는 native 함수");
        함수형식 akua_ipaa_ajutuu = new 함수형식(선택.서술);
        if ((진입점여부 && !akua_ipaa_ajutuu.인수.isEmpty()) || !Arrays.asList("V", "I").contains(akua_ipaa_ajutuu.반환)) throw new 번역오류("ekeroliaa_o_uchikanain_ajutuu 또는 C 경계 akua_ipaa_ajutuu ajachitia");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < akua_ipaa_ajutuu.인수.size(); 순번++) {
            if (!akua_ipaa_ajutuu.인수.get(순번).equals("I")) throw new 번역오류("C 경계는 int 인수만 akaaliijiaa_ajutuu");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (akua_ipaa_ajutuu.반환.equals("V") ? "void " : "int32_t ") + 연결기호 + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + 기호("init", 선택.소유) + "(); " + (akua_ipaa_ajutuu.반환.equals("V") ? "" : "return (int32_t)") + 기호("method", 선택.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String ekeroliaa_o_uchikanain, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<함수참조, a_akaajatü_atijaaya> ekeroliaa_ajutuu : 함수들.entrySet()) {
            함수참조 참조 = ekeroliaa_ajutuu.getKey(); a_akaajatü_atijaaya atijaaya = ekeroliaa_ajutuu.getValue(); 선언들.add(함수원형(참조) + ";");
            if ((atijaaya.a_ttaaya_ekeroliaa & 0x100) != 0) {
                String a_ataa = 기계함수들.get(참조.이름 + 참조.서술);
                if (!참조.소유.equals(기계클래스) || a_ataa == null) throw new 번역오류("허용되지 않은 native 함수: " + 참조.이름);
                int 개수 = new 함수형식(참조.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + a_ataa + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(참조) + " { return " + a_ataa + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(참조, atijaaya));
        }
        for (Map.Entry<함수참조, a_akaajatü_atijaaya> ekeroliaa_ajutuu : 필드들.entrySet()) {
            함수참조 참조 = ekeroliaa_ajutuu.getKey(); byte[] waneepiajutu_ajutuu = ekeroliaa_ajutuu.getValue().anaajaalaakua_ipa_ajutuu.get("ConstantValue");
            String ajutuu = waneepiajutu_ajutuu == null ? "0" : waneepiajutu_ajutukumajiaa(클래스들.get(참조.소유), new atijaaya_aashaje_erülü(waneepiajutu_ajutuu).두바이트());
            필드선언들.add("static word " + 기호("field", 참조.부분들()) + " = " + ajutuu + ";");
        }
        for (String 이름 : 클래스들.keySet()) {
            String anaajaa = 기호("init", 이름), jamakua_iparülein_ajutuu = 기호("state", 이름);
            선언들.add("static void " + anaajaa + "(void);"); 필드선언들.add("static unsigned " + jamakua_iparülein_ajutuu + ";");
            함수참조 참조 = new 함수참조(이름, "<clinit>", "()V");
            몸체들.add("static void " + anaajaa + "(void) { if(" + jamakua_iparülein_ajutuu + ") return; " + jamakua_iparülein_ajutuu + " = 1; " + (함수들.containsKey(참조) ? 기호("method", 참조.부분들()) + "(); " : "") + jamakua_iparülein_ajutuu + " = 2; }");
        }
        몸체들.add(내보낼함수("java_entry", ekeroliaa_o_uchikanain, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new 번역오류("내보내기 지정 ajachitia");
            String 이름 = 지정.substring(0, 자리); 공개이름.add(이름); 몸체들.add(내보낼함수(이름, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> ekeroliaa_ajutuu : 문자열들.entrySet()) {
            String 글 = ekeroliaa_ajutuu.getKey(); StringBuilder matüriisü_ajutuu = new StringBuilder("static const word " + ekeroliaa_ajutuu.getValue() + "[] = {" + 글.length());
            for (int 순번 = 0; 순번 < 글.length(); 순번++) matüriisü_ajutuu.append(", ").append((int)글.charAt(순번));
            문자열선언들.add(matüriisü_ajutuu.append("};").toString());
        }
        String akaaliijiaa_ajutuu = Files.readString(ama_anaajatü_wopu_a_ttaaleemüin.resolve("실행지원.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(akaaliijiaa_ajutuu + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String eejeejetülein, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> 이름표 = new HashMap<>();
        for (String liinia : Files.readAllLines(ama_anaajatü_wopu_a_ttaaleemüin.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] 쌍 = liinia.split("\t"); 이름표.put(쌍[0], 쌍[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(eejeejetülein); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String 이름 = 찾개.group(), 새이름 = 이름;
            if (!이름.startsWith("//") && !이름.startsWith("/*") && !이름.startsWith("\"") && !이름.startsWith("'") && !공개이름.contains(이름)) {
                새이름 = 이름표.getOrDefault(이름, 이름);
                if (이름.matches("a[0-9]+")) 새이름 = "인수" + 이름.substring(1);
                if (이름.matches("b[0-9]+")) 새이름 = "분기" + 이름.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char jeerü_ajutuu : 새이름.toCharArray()) 표기.append(jeerü_ajutuu < 128 ? Character.toString(jeerü_ajutuu) : String.format(Locale.ROOT, "\\u%04x", (int)jeerü_ajutuu));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(함수참조 함수, a_akaajatü_atijaaya atijaaya, Map<String,String> 기계표, String 대상) {
        String 표식 = 기호("method", 함수.부분들());
        List<String> liinia = new ArrayList<>();
        if ((atijaaya.a_ttaaya_ekeroliaa & 0x100) != 0) {
            String a_ataa = 기계표.get(함수.이름 + 함수.서술);
            if (!함수.소유.equals(대상.equals("kernel") ? "serulaalü_ajutuu" : "ka_yataayakalü") || a_ataa == null) throw new 번역오류("허용되지 않은 native 함수");
            return ".text\n" + 표식 + ":\njmp " + a_ataa;
        }
        byte[] ashajalaa_a_laülaasükalü = atijaaya.anaajaalaakua_ipa_ajutuu.get("Code"); if (ashajalaa_a_laülaasükalü == null) throw new 번역오류("함수 몸체가 없음");
        atijaaya_aashaje_erülü aashaje_erülü_ajutuu = new atijaaya_aashaje_erülü(ashajalaa_a_laülaasükalü); aashaje_erülü_ajutuu.두바이트(); int 지역수 = aashaje_erülü_ajutuu.두바이트();
        atijaaya_aashaje_erülü aluwataaya_atijaaya = new atijaaya_aashaje_erülü(aashaje_erülü_ajutuu.읽기(aashaje_erülü_ajutuu.네바이트()));
        if (aashaje_erülü_ajutuu.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 akua_ipaa_ajutuu = new 함수형식(함수.서술); if (지역수 < akua_ipaa_ajutuu.인수.size()) throw new 번역오류("매개변수보다 적은 지역 변수");
        Collections.addAll(liinia,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < akua_ipaa_ajutuu.인수.size(); 순번++) Collections.addAll(liinia,"movl " + (8 + 4 * (akua_ipaa_ajutuu.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        akotchijuushi_atijaaya akotchijuushi_ajutuu_55654bf1 = 클래스들.get(함수.소유); Set<Integer> 경계들 = new HashSet<>(), 분기들 = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (aluwataaya_atijaaya.위치 < aluwataaya_atijaaya.atijaaya.length) {
            int 위치 = aluwataaya_atijaaya.위치, aluwataaya = aluwataaya_atijaaya.한바이트(); String 자리 = 표식 + "_b" + 위치;
            liinia.add(자리 + ":"); 경계들.add(위치);
            if (aluwataaya == 0) liinia.add("nop");
            else if (aluwataaya == 1) liinia.add("pushl $0");
            else if (aluwataaya >= 2 && aluwataaya <= 8) liinia.add("pushl $" + (aluwataaya - 3));
            else if (aluwataaya == 16 || aluwataaya == 17) liinia.add("pushl $" + (aluwataaya == 16 ? aluwataaya_atijaaya.부호한바이트() : aluwataaya_atijaaya.부호두바이트()));
            else if (aluwataaya == 18 || aluwataaya == 19) {
                int ee_iyatialujuna = aluwataaya == 18 ? aluwataaya_atijaaya.한바이트() : aluwataaya_atijaaya.두바이트();
                liinia.add("pushl $" + 엑스상수(akotchijuushi_ajutuu_55654bf1,ee_iyatialujuna));
            } else if (aluwataaya == 21 || aluwataaya == 25 || (aluwataaya >= 26 && aluwataaya <= 29) || (aluwataaya >= 42 && aluwataaya <= 45) || aluwataaya == 54 || aluwataaya == 58 || (aluwataaya >= 59 && aluwataaya <= 62) || (aluwataaya >= 75 && aluwataaya <= 78)) {
                boolean 읽음 = aluwataaya < 54; int ee_iyatialujuna = aluwataaya == 21 || aluwataaya == 25 || aluwataaya == 54 || aluwataaya == 58 ? aluwataaya_atijaaya.한바이트() : aluwataaya - (aluwataaya <= 29 ? 26 : aluwataaya <= 45 ? 42 : aluwataaya <= 62 ? 59 : 75);
                지역검사(ee_iyatialujuna,지역수); liinia.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (ee_iyatialujuna + 1)) + "(%ebp)");
            } else if (aluwataaya == 46) Collections.addAll(liinia,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (aluwataaya == 79) Collections.addAll(liinia,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (aluwataaya == 87 || aluwataaya == 88) liinia.add("addl $" + (aluwataaya == 87 ? 4 : 8) + ", %esp");
            else if (aluwataaya >= 89 && aluwataaya <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] 순서들 = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[aluwataaya - 89]; 순번++) liinia.add("popl " + 저장기들[순번]);
                for (int 순번 : 순서들[aluwataaya - 89]) liinia.add("pushl " + 저장기들[순번]);
            } else if (aluwataaya == 96 || aluwataaya == 100 || aluwataaya == 104 || aluwataaya == 126 || aluwataaya == 128 || aluwataaya == 130) {
                String akumajiraa_ajutuu = aluwataaya == 96 ? "addl" : aluwataaya == 100 ? "subl" : aluwataaya == 104 ? "imull" : aluwataaya == 126 ? "andl" : aluwataaya == 128 ? "orl" : "xorl";
                Collections.addAll(liinia,"popl %ecx","popl %eax",akumajiraa_ajutuu + " %ecx, %eax","pushl %eax");
            } else if (aluwataaya == 108 || aluwataaya == 112) Collections.addAll(liinia,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (aluwataaya == 108 ? "%eax" : "%edx"));
            else if (aluwataaya == 116) liinia.add("negl (%esp)");
            else if (aluwataaya == 120 || aluwataaya == 122 || aluwataaya == 124) Collections.addAll(liinia,"popl %ecx","popl %eax",(aluwataaya == 120 ? "sall" : aluwataaya == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (aluwataaya == 132) {
                int ee_iyatialujuna = aluwataaya_atijaaya.한바이트(), 증가 = aluwataaya_atijaaya.부호한바이트(); 지역검사(ee_iyatialujuna,지역수); liinia.add("addl $" + 증가 + ", -" + (4 * (ee_iyatialujuna + 1)) + "(%ebp)");
            } else if (aluwataaya >= 145 && aluwataaya <= 147) Collections.addAll(liinia,"popl %eax",aluwataaya == 145 ? "movsbl %al, %eax" : aluwataaya == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (aluwataaya >= 153 && aluwataaya <= 166) {
                if (aluwataaya <= 158) Collections.addAll(liinia,"popl %eax","testl %eax, %eax");
                else Collections.addAll(liinia,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int jalamüinjatü_ajutuu = 위치 + aluwataaya_atijaaya.부호두바이트(); 분기들.add(jalamüinjatü_ajutuu); liinia.add(비교들[aluwataaya - (aluwataaya <= 158 ? 153 : 159)] + " " + 표식 + "_b" + jalamüinjatü_ajutuu);
            } else if (aluwataaya == 167 || aluwataaya == 200) {
                int jalamüinjatü_ajutuu = 위치 + (aluwataaya == 167 ? aluwataaya_atijaaya.부호두바이트() : aluwataaya_atijaaya.네바이트()); 분기들.add(jalamüinjatü_ajutuu); liinia.add("jmp " + 표식 + "_b" + jalamüinjatü_ajutuu);
            } else if (aluwataaya == 170 || aluwataaya == 171) {
                while (aluwataaya_atijaaya.위치 % 4 != 0) aluwataaya_atijaaya.한바이트();
                int ajutuu_aneekuushitüjülia = 위치 + aluwataaya_atijaaya.네바이트(); 분기들.add(ajutuu_aneekuushitüjülia); liinia.add("popl %eax");
                int 개수, 아래 = 0;
                if (aluwataaya == 170) { 아래 = aluwataaya_atijaaya.네바이트(); int 위 = aluwataaya_atijaaya.네바이트(); long akaliaa_ajutuu = (long)위 - 아래 + 1; if (akaliaa_ajutuu < 1 || akaliaa_ajutuu > (aluwataaya_atijaaya.atijaaya.length - aluwataaya_atijaaya.위치) / 4) throw new 번역오류("switch külipü_ayaakuaapijana ajachitia"); 개수 = (int)akaliaa_ajutuu; }
                else { 개수 = aluwataaya_atijaaya.네바이트(); if (개수 < 0 || 개수 > (aluwataaya_atijaaya.atijaaya.length - aluwataaya_atijaaya.위치) / 8) throw new 번역오류("switch 크기 ajachitia"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int ajutuu = aluwataaya == 170 ? 아래 + 순번 : aluwataaya_atijaaya.네바이트(), jalamüinjatü_ajutuu = 위치 + aluwataaya_atijaaya.네바이트(); 분기들.add(jalamüinjatü_ajutuu);
                    Collections.addAll(liinia,"cmpl $" + ajutuu + ", %eax","je " + 표식 + "_b" + jalamüinjatü_ajutuu);
                }
                liinia.add("jmp " + 표식 + "_b" + ajutuu_aneekuushitüjülia);
            } else if (aluwataaya == 172 || aluwataaya == 176 || aluwataaya == 177) {
                if (aluwataaya != 177) liinia.add("popl %eax"); Collections.addAll(liinia,"leave","ret");
            } else if (aluwataaya == 178 || aluwataaya == 179) {
                함수참조 참조 = akotchijuushi_ajutuu_55654bf1.참조(aluwataaya_atijaaya.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 apülajanaa_ajutuu");
                Collections.addAll(liinia,"call " + 기호("init",참조.소유),(aluwataaya == 178 ? "pushl " : "popl ") + 기호("field",참조.부분들()));
            } else if (aluwataaya == 184) {
                함수참조 참조 = akotchijuushi_ajutuu_55654bf1.참조(aluwataaya_atijaaya.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 함수");
                함수형식 호출형식 = new 함수형식(참조.서술); Collections.addAll(liinia,"call " + 기호("init",참조.소유),"call " + 기호("method",참조.부분들()));
                if (!호출형식.인수.isEmpty()) liinia.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) liinia.add("pushl %eax");
            } else if (aluwataaya == 182) {
                함수참조 참조 = akotchijuushi_ajutuu_55654bf1.참조(aluwataaya_atijaaya.두바이트());
                if (참조.equals(new 함수참조("java/lang/String","length","()I"))) Collections.addAll(liinia,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (참조.equals(new 함수참조("java/lang/String","charAt","(I)C"))) Collections.addAll(liinia,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 번역오류("가상 함수 호출 미지원");
            } else if (aluwataaya == 188) {
                if (aluwataaya_atijaaya.한바이트() != 10) throw new 번역오류("new int[]만 akaaliijiaa_ajutuu"); Collections.addAll(liinia,"popl %eax","call rt_new_array","pushl %eax");
            } else if (aluwataaya == 190) Collections.addAll(liinia,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (aluwataaya == 196) {
                int e_irukuu_ajutuu = aluwataaya_atijaaya.한바이트(), ee_iyatialujuna = aluwataaya_atijaaya.두바이트(); 지역검사(ee_iyatialujuna,지역수);
                if (e_irukuu_ajutuu == 21 || e_irukuu_ajutuu == 25 || e_irukuu_ajutuu == 54 || e_irukuu_ajutuu == 58) liinia.add((e_irukuu_ajutuu <= 25 ? "pushl " : "popl ") + "-" + 4 * (ee_iyatialujuna + 1) + "(%ebp)");
                else if (e_irukuu_ajutuu == 132) liinia.add("addl $" + aluwataaya_atijaaya.부호두바이트() + ", -" + 4 * (ee_iyatialujuna + 1) + "(%ebp)");
                else throw new 번역오류("wide aluwataaya 미지원");
            } else if (aluwataaya == 198 || aluwataaya == 199) {
                int jalamüinjatü_ajutuu = 위치 + aluwataaya_atijaaya.부호두바이트(); 분기들.add(jalamüinjatü_ajutuu); Collections.addAll(liinia,"popl %eax","testl %eax, %eax",(aluwataaya == 198 ? "je " : "jne ") + 표식 + "_b" + jalamüinjatü_ajutuu);
            } else throw new 번역오류("미지원 aluwataaya: " + aluwataaya);
        }
        if (!경계들.containsAll(분기들)) throw new 번역오류("aluwataaya 경계가 아닌 곳으로 분기");
        liinia.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",liinia);
    }
    String 엑스상수(akotchijuushi_atijaaya atijaaya, int ee_iyatialujuna) {
        if (atijaaya.상수종류[ee_iyatialujuna] == 3) return atijaaya.waneepiajutu_atijaaya[ee_iyatialujuna].toString();
        if (atijaaya.상수종류[ee_iyatialujuna] == 8) return 문자열기호(atijaaya.문자((Integer)atijaaya.waneepiajutu_atijaaya[ee_iyatialujuna]));
        throw new 번역오류("정수와 kaleena_ajutuu 상수만 akaaliijiaa_ajutuu");
    }
    String 엑스조립본(String ekeroliaa_o_uchikanain, List<String> 내보냄, String 대상) throws IOException {
        Map<String,String> 기계표 = new HashMap<>();
        for (String liinia : Files.readAllLines(ama_anaajatü_wopu_a_ttaaleemüin.resolve("엑스기계함수.tsv"))) { String[] 쌍 = liinia.split("\t"); if (쌍[0].equals(대상)) 기계표.put(쌍[1] + 쌍[2],쌍[3]); }
        int 자리 = ekeroliaa_o_uchikanain.lastIndexOf('.'); if (자리 < 0) throw new 번역오류("ekeroliaa_o_uchikanain 지정 ajachitia");
        String 소유 = ekeroliaa_o_uchikanain.substring(0,자리).replace('.','/'), 함수이름 = ekeroliaa_o_uchikanain.substring(자리 + 1); 함수참조 ekeroliaa_o_uchikanain_ajutuu = null;
        for (String 서술 : Arrays.asList("()I","()V")) { 함수참조 참조 = new 함수참조(소유,함수이름,서술); if (함수들.containsKey(참조)) { if (ekeroliaa_o_uchikanain_ajutuu != null) throw new 번역오류("겹친 ekeroliaa_o_uchikanain"); ekeroliaa_o_uchikanain_ajutuu = 참조; } }
        if (ekeroliaa_o_uchikanain_ajutuu == null || (함수들.get(ekeroliaa_o_uchikanain_ajutuu).a_ttaaya_ekeroliaa & 0x100) != 0) throw new 번역오류("ekeroliaa_o_uchikanain_ajutuu 함수 akua_ipaa_ajutuu ajachitia");
        List<String> liinia = new ArrayList<>(); liinia.add(".code32");
        for (akotchijuushi_atijaaya atijaaya : 클래스들.values()) {
            String jamakua_iparülein_ajutuu = 기호("state",atijaaya.이름), anaajaa = 기호("init",atijaaya.이름);
            Collections.addAll(liinia,".bss",".balign 4",jamakua_iparülein_ajutuu + ": .long 0",".text",anaajaa + ":","cmpl $0, " + jamakua_iparülein_ajutuu,"jne " + anaajaa + "_done","movl $1, " + jamakua_iparülein_ajutuu);
            함수참조 초기화참조 = new 함수참조(atijaaya.이름,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) liinia.add("call " + 기호("method",초기화참조.부분들()));
            Collections.addAll(liinia,"movl $2, " + jamakua_iparülein_ajutuu,anaajaa + "_done:","ret");
            for (a_akaajatü_atijaaya apülajanaa_ajutuu : atijaaya.apülajanaa_ajutuu) {
                byte[] waneepiajutu_ajutuu = apülajanaa_ajutuu.anaajaalaakua_ipa_ajutuu.get("ConstantValue"); String ajutuu = waneepiajutu_ajutuu == null ? "0" : 엑스상수(atijaaya,new atijaaya_aashaje_erülü(waneepiajutu_ajutuu).두바이트());
                Collections.addAll(liinia,".data",".balign 4",기호("field",atijaaya.이름,apülajanaa_ajutuu.이름,apülajanaa_ajutuu.서술) + ": .long " + ajutuu);
            }
            for (a_akaajatü_atijaaya 함수 : atijaaya.함수) if (!함수.이름.equals("<init>")) liinia.add(엑스함수본문(new 함수참조(atijaaya.이름,함수.이름,함수.서술),함수,기계표,대상));
        }
        Collections.addAll(liinia,".text",".globl java_entry","java_entry:","call " + 기호("init",ekeroliaa_o_uchikanain_ajutuu.소유),"call " + 기호("method",ekeroliaa_o_uchikanain_ajutuu.부분들()));
        if (ekeroliaa_o_uchikanain_ajutuu.서술.equals("()V")) liinia.add("xorl %eax, %eax"); liinia.add("ret");
        for (String 지정 : 내보냄) {
            int akatajülu_ajutuu = 지정.indexOf('='); if (akatajülu_ajutuu < 1) throw new 번역오류("내보내기 지정 ajachitia");
            String 외부 = 지정.substring(0,akatajülu_ajutuu), 함수 = 지정.substring(akatajülu_ajutuu + 1); int 나눔 = 함수.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 기호 ajachitia");
            String akotchijuushi_ajutuu_55654bf1 = 함수.substring(0,나눔).replace('.','/'), 이름 = 함수.substring(나눔 + 1); 함수참조 선택 = null;
            for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(akotchijuushi_ajutuu_55654bf1) && 참조.이름.equals(이름)) { if (선택 != null) throw new 번역오류("겹친 내보내기 대상"); 선택 = 참조; }
            if (선택 == null) throw new 번역오류("내보낼 함수가 없음");
            Collections.addAll(liinia,".text",".globl " + 외부,외부 + ":","call " + 기호("init",선택.소유),"jmp " + 기호("method",선택.부분들()));
        }
        liinia.add(".section .rodata");
        for (Map.Entry<String,String> ekeroliaa_ajutuu : 문자열들.entrySet()) {
            Collections.addAll(liinia,".balign 4",ekeroliaa_ajutuu.getValue() + ":",".long " + ekeroliaa_ajutuu.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char 단위 : ekeroliaa_ajutuu.getKey().toCharArray()) 단위들.add(Integer.toString(단위)); if (!단위들.isEmpty()) liinia.add(".long " + String.join(",",단위들));
        }
        liinia.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",liinia) + "\n";
    }
    static void 도구실행(List<String> aluwataaya) throws Exception {
        if (new ProcessBuilder(aluwataaya).inheritIO().start().waitFor() != 0) throw new 번역오류("akompiraajaa_eejeejetülein ajachitia: " + aluwataaya.get(0));
    }
    static String atijaaya_kaleena(String 글) { return "\"" + 글.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String 대상, String ekeroliaa_o_uchikanain, List<String> 내보냄, Path 출력, Path ama_anaajatü_ajutuu) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), akotchijuushi_wopu_a_ttaaleemüin = 임시.resolve("classes"); Files.createDirectory(akotchijuushi_wopu_a_ttaaleemüin);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",akotchijuushi_wopu_a_ttaaleemüin.toString(),"-sourcepath",akotchijuushi_wopu_a_ttaaleemüin.toString(),"-d",akotchijuushi_wopu_a_ttaaleemüin.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new 번역오류("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new 번역오류(".java 또는 .class만 akaaliijiaa_ajutuu");
            }
            if (원문수 > 0) 도구실행(자바명령);
            try (java.util.stream.Stream<Path> 경로들 = Files.walk(akotchijuushi_wopu_a_ttaaleemüin)) { 경로들.filter(wopu_a_ttaaleemüin -> wopu_a_ttaaleemüin.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,대상.equals("user") ? "user" : "kernel",262144,ama_anaajatü_ajutuu);
            String 조립 = 변환.엑스조립본(ekeroliaa_o_uchikanain,내보냄,대상); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = ama_anaajatü_ajutuu.getParent();
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("실행지원.s").toString()));
            List<String> a_ataa = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (대상.equals("kernel")) a_ataa.add("-r");
            else {
                도구실행(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(대상.equals("user") ? "achuwalaa_ka_yataayakalü_akumajiaa.s" : "리눅스시작.s").toString()));
                Collections.addAll(a_ataa,"-e","_start",임시.resolve("start.o").toString());
                if (대상.equals("user")) Collections.addAll(a_ataa,"-T",도구위치.resolve("ka_yataayakalü_wopu_akumajiakuai_pa.ld").toString());
            }
            Collections.addAll(a_ataa,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); 도구실행(a_ataa);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path akusulu_ujaa_ajutuu = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),akusulu_ujaa_ajutuu,StandardCopyOption.REPLACE_EXISTING); Files.move(akusulu_ujaa_ajutuu,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(akusulu_ujaa_ajutuu); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(대상.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> 기호자료 = new ArrayList<>(), eejeejetülein_atijaaya = new ArrayList<>();
            for (함수참조 참조 : 변환.함수들.keySet()) 기호자료.add(atijaaya_kaleena(기호("method",참조.부분들())) + ":" + atijaaya_kaleena(참조.소유 + "." + 참조.이름 + 참조.서술));
            for (Path 입력 : 입력들) {
                byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder 글 = new StringBuilder(); for (byte ajutuu : 해시) 글.append(String.format(Locale.ROOT,"%02x",ajutuu & 255));
                eejeejetülein_atijaaya.add(atijaaya_kaleena(입력.toAbsolutePath().toString()) + ":" + atijaaya_kaleena(글.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + atijaaya_kaleena(대상) + ",\"entry\":" + atijaaya_kaleena(ekeroliaa_o_uchikanain) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",기호자료) + "},\"sources\":{" + String.join(",",eejeejetülein_atijaaya) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> 경로들 = Files.walk(임시)) { for (Path wopu_a_ttaaleemüin : (Iterable<Path>)경로들.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(wopu_a_ttaaleemüin); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String ekeroliaa_o_uchikanain = null, 대상 = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> 경로들 = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String ajutuu = 인수[순번];
                switch (ajutuu) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry akotchijuushi_ajutuu_55654bf1.함수 -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export 기호=akotchijuushi_ajutuu_55654bf1.함수] 클래스파일 또는 Java원문"); return;
                    case "--entry": ekeroliaa_o_uchikanain = 인수[++순번]; break;
                    case "--profile": 대상 = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (ajutuu.startsWith("-")) throw new 번역오류("알 수 없는 옵션: " + ajutuu); 경로들.add(Paths.get(ajutuu));
                }
            }
            if (ekeroliaa_o_uchikanain == null || 출력경로 == null || 경로들.isEmpty()) throw new 번역오류("--entry, -o, akotchijuushi_ajutuu_55654bf1 파일이 필요합니다");
            Path ama_anaajatü_ajutuu = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new 번역오류("알 수 없는 실행 대상");
                엑스번역(경로들,엑스대상,ekeroliaa_o_uchikanain,내보냄,출력경로,ama_anaajatü_ajutuu); return;
            }
            String eejeejetülein = new 기계어미리번역(경로들, 대상, 낱말수, ama_anaajatü_ajutuu).생성(ekeroliaa_o_uchikanain, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, eejeejetülein, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception ajachitia) { System.err.println("akompiraajaa_eejeejetülein ajachitia: " + ajachitia.getMessage()); System.exit(1); }
    }
}
