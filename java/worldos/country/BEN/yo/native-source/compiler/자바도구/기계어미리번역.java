// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java ọ̀wọ́_iye 파일에서 독립 ARM64 커널용 C 원문을 만든다. olùpèsè JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Ìtumọ̀_àṣìṣe extends RuntimeException {
        Ìtumọ̀_àṣìṣe(String 설명) { super(설명); }
    }
    static final class détà_akàwé {
        final byte[] détà;
        int 위치;
        détà_akàwé(byte[] 입력자료) { détà = 입력자료; }
        byte[] Kàá(int gígùn_iye) {
            if (gígùn_iye < 0 || gígùn_iye > détà.length - 위치) throw new Ìtumọ̀_àṣìṣe("잘린 ọ̀wọ́_iye 또는 Àṣẹ détà");
            byte[] 결과 = Arrays.copyOfRange(détà, 위치, 위치 + gígùn_iye); 위치 += gígùn_iye; return 결과;
        }
        int 한바이트() { if (위치 >= détà.length) throw new Ìtumọ̀_àṣìṣe("잘린 Àṣẹ détà"); return détà[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class ọmọ_ẹgbẹ́_détà {
        final int wáyè_sí_ìgbéwọlé;
        final String Orúkọ, 서술;
        final Map<String, byte[]> àwòmọ́_iye;
        ọmọ_ẹgbẹ́_détà(int wáyè_sí_iye, String orúkọ_iye, String 서술값, Map<String, byte[]> àwòmọ́_détà) {
            wáyè_sí_ìgbéwọlé = wáyè_sí_iye; Orúkọ = orúkọ_iye; 서술 = 서술값; àwòmọ́_iye = àwòmọ́_détà;
        }
    }
    static final class ìlànà_Ìtọ́ka implements Comparable<ìlànà_Ìtọ́ka> {
        final String Oníǹkan_iye, Orúkọ, 서술;
        ìlànà_Ìtọ́ka(String 소유값, String orúkọ_iye, String 서술값) { Oníǹkan_iye = 소유값; Orúkọ = orúkọ_iye; 서술 = 서술값; }
        String[] 부분들() { return new String[]{Oníǹkan_iye, Orúkọ, 서술}; }
        public int compareTo(ìlànà_Ìtọ́ka ọ̀gbà_iye) {
            int 비교값 = Oníǹkan_iye.compareTo(ọ̀gbà_iye.Oníǹkan_iye);
            if (비교값 == 0) 비교값 = Orúkọ.compareTo(ọ̀gbà_iye.Orúkọ);
            return 비교값 == 0 ? 서술.compareTo(ọ̀gbà_iye.서술) : 비교값;
        }
        public boolean equals(Object ọ̀gbà_iye) { return ọ̀gbà_iye instanceof ìlànà_Ìtọ́ka && compareTo((ìlànà_Ìtọ́ka) ọ̀gbà_iye) == 0; }
        public int hashCode() { return Objects.hash(Oníǹkan_iye, Orúkọ, 서술); }
    }
    static final class ọ̀wọ́_détà {
        final int[] 상수종류;
        final Object[] aláìṣeéyípadà_détà;
        final String Orúkọ;
        final List<ọmọ_ẹgbẹ́_détà> àayè_wúnrẹ̀n_iye, ÀKÀNṢEFỌMÚLÀ_iye;
        ọ̀wọ́_détà(Path ọ̀nà) throws IOException {
            détà_akàwé akàwé_iye = new détà_akàwé(Files.readAllBytes(ọ̀nà));
            if (akàwé_iye.네바이트() != 0xcafebabe) throw new Ìtumọ̀_àṣìṣe("Java ọ̀wọ́_iye 표식이 아님");
            akàwé_iye.Kàá(4);
            int 개수 = akàwé_iye.두바이트(); 상수종류 = new int[개수]; aláìṣeéyípadà_détà = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = akàwé_iye.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int gígùn_iye = akàwé_iye.두바이트();
                        byte[] ẹyọ_ọ̀rọ̀_àká = akàwé_iye.Kàá(gígùn_iye), 길이붙인자료 = new byte[gígùn_iye + 2];
                        길이붙인자료[0] = (byte)(gígùn_iye >> 8); 길이붙인자료[1] = (byte)gígùn_iye;
                        System.arraycopy(ẹyọ_ọ̀rọ̀_àká, 0, 길이붙인자료, 2, gígùn_iye);
                        aláìṣeéyípadà_détà[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: aláìṣeéyípadà_détà[순번] = akàwé_iye.네바이트(); break;
                    case 4: akàwé_iye.Kàá(4); break;
                    case 5: case 6: akàwé_iye.Kàá(8); 순번++; break;
                    case 7: case 8: case 16: aláìṣeéyípadà_détà[순번] = akàwé_iye.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        aláìṣeéyípadà_détà[순번] = new int[]{akàwé_iye.두바이트(), akàwé_iye.두바이트()}; break;
                    case 15: aláìṣeéyípadà_détà[순번] = new int[]{akàwé_iye.한바이트(), akàwé_iye.두바이트()}; break;
                    default: throw new Ìtumọ̀_àṣìṣe("지원하지 않는 aláìṣeéyípadà_iye 종류: " + 종류);
                }
            }
            akàwé_iye.두바이트(); Orúkọ = ọ̀wọ́_orúkọ(akàwé_iye.두바이트());
            if (!ọ̀wọ́_orúkọ(akàwé_iye.두바이트()).equals("java/lang/Object") || akàwé_iye.두바이트() != 0)
                throw new Ìtumọ̀_àṣìṣe(Orúkọ + ": 상속 및 인터페이스 미지원");
            àayè_wúnrẹ̀n_iye = 멤버읽기(akàwé_iye); ÀKÀNṢEFỌMÚLÀ_iye = 멤버읽기(akàwé_iye); 속성읽기(akàwé_iye);
            if (akàwé_iye.위치 != akàwé_iye.détà.length) throw new Ìtumọ̀_àṣìṣe("ọ̀wọ́_iye 뒤에 남은 détà");
        }
        String 문자(int wá_atọ̀ka_àkóónú) {
            if (wá_atọ̀ka_àkóónú < 1 || wá_atọ̀ka_àkóónú >= 상수종류.length || 상수종류[wá_atọ̀ka_àkóónú] != 1) throw new Ìtumọ̀_àṣìṣe("문자 aláìṣeéyípadà_iye wá_atọ̀ka_àkóónú àṣìṣe");
            return (String) aláìṣeéyípadà_détà[wá_atọ̀ka_àkóónú];
        }
        String ọ̀wọ́_orúkọ(int wá_atọ̀ka_àkóónú) {
            if (wá_atọ̀ka_àkóónú < 1 || wá_atọ̀ka_àkóónú >= 상수종류.length || 상수종류[wá_atọ̀ka_àkóónú] != 7) throw new Ìtumọ̀_àṣìṣe("ọ̀wọ́_iye Ìtọ́ka àṣìṣe");
            return 문자((Integer)aláìṣeéyípadà_détà[wá_atọ̀ka_àkóónú]);
        }
        ìlànà_Ìtọ́ka Ìtọ́ka(int wá_atọ̀ka_àkóónú) {
            if (wá_atọ̀ka_àkóónú < 1 || wá_atọ̀ka_àkóónú >= 상수종류.length || 상수종류[wá_atọ̀ka_àkóónú] < 9 || 상수종류[wá_atọ̀ka_àkóónú] > 11) throw new Ìtumọ̀_àṣìṣe("멤버 Ìtọ́ka àṣìṣe");
            int[] ṣàsopọ̀_iye = (int[])aláìṣeéyípadà_détà[wá_atọ̀ka_àkóónú], orúkọ_ṣàsopọ̀ = (int[])aláìṣeéyípadà_détà[ṣàsopọ̀_iye[1]];
            return new ìlànà_Ìtọ́ka(ọ̀wọ́_orúkọ(ṣàsopọ̀_iye[0]), 문자(orúkọ_ṣàsopọ̀[0]), 문자(orúkọ_ṣàsopọ̀[1]));
        }
        Map<String, byte[]> 속성읽기(détà_akàwé akàwé_iye) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = akàwé_iye.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String àwòmọ́_orúkọ = 문자(akàwé_iye.두바이트()); byte[] iye = akàwé_iye.Kàá(akàwé_iye.네바이트());
                if (결과.put(àwòmọ́_orúkọ, iye) != null) throw new Ìtumọ̀_àṣìṣe("겹친 àwòmọ́_iye: " + àwòmọ́_orúkọ);
            }
            return 결과;
        }
        List<ọmọ_ẹgbẹ́_détà> 멤버읽기(détà_akàwé akàwé_iye) {
            List<ọmọ_ẹgbẹ́_détà> 결과 = new ArrayList<>(); int 개수 = akàwé_iye.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int wáyè_sí_ìgbéwọlé = akàwé_iye.두바이트(); String ìlànà_ìgbéwọlé_orúkọ = 문자(akàwé_iye.두바이트()), 서술 = 문자(akàwé_iye.두바이트());
                결과.add(new ọmọ_ẹgbẹ́_détà(wáyè_sí_ìgbéwọlé, ìlànà_ìgbéwọlé_orúkọ, 서술, 속성읽기(akàwé_iye)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Ìtumọ̀_àṣìṣe("ÀKÀNṢEFỌMÚLÀ_iye 서술 àṣìṣe: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Ìtumọ̀_àṣìṣe("ÀKÀNṢEFỌMÚLÀ_iye 서술 àṣìṣe: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Ìtumọ̀_àṣìṣe("ÀKÀNṢEFỌMÚLÀ_iye 서술 àṣìṣe: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String ẹ̀yàn_iye = null;
            for (String ìgúnrégé_iye : 허용형식) if (서술.startsWith(ìgúnrégé_iye, 위치)) { ẹ̀yàn_iye = ìgúnrégé_iye; break; }
            if (ẹ̀yàn_iye == null) throw new Ìtumọ̀_àṣìṣe("지원하지 않는 ẹ̀yà_détà: " + 서술);
            결과.add(ẹ̀yàn_iye); 위치 += ẹ̀yàn_iye.length();
        }
        return 결과;
    }
    static String àmì(String 종류, String... 부분들) {
        try {
            byte[] burú_fáìlì = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", burú_fáìlì[순번] & 255));
            return SMS.toString();
        } catch (Exception àṣìṣe) { throw new Ìtumọ̀_àṣìṣe(àṣìṣe.toString()); }
    }
    final Map<String, ọ̀wọ́_détà> 클래스들 = new TreeMap<>();
    final Map<ìlànà_Ìtọ́ka, ọmọ_ẹgbẹ́_détà> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, maṣíìnì_ọ̀wọ́;
    final int 동적기억낱말수;
    final Path ohun_àmúlò_ọ̀nà;
    기계어미리번역(List<Path> ọ̀nà_Àtòkọ, String àfojúsùn, int 낱말수, Path ohun_àmúlò_iye) throws IOException {
        if ((!àfojúsùn.equals("kernel") && !àfojúsùn.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Ìtumọ̀_àṣìṣe("ṣiṣẹ́_àṣẹ àfojúsùn 또는 ibi_ìpamọ́_iye 공간 Ìwọ̀n àṣìṣe");
        실행대상 = àfojúsùn; 동적기억낱말수 = 낱말수; ohun_àmúlò_ọ̀nà = ohun_àmúlò_iye;
        // 이 이름도 국가별 orísun_ètò_afigijúwe 생성 시 해당 언어로 옮긴다.
        maṣíìnì_ọ̀wọ́ = àfojúsùn.equals("kernel") ? "보드" : "aṣàmúlò";
        for (String ìlà : Files.readAllLines(ohun_àmúlò_iye.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = ìlà.split("\t", -1);
            if (부분들.length != 4) throw new Ìtumọ̀_àṣìṣe("maṣíìnì ÀKÀNṢEFỌMÚLÀ_iye détà àṣìṣe");
            if (부분들[0].equals(àfojúsùn)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path ọ̀nà : ọ̀nà_Àtòkọ) {
            ọ̀wọ́_détà détà = new ọ̀wọ́_détà(ọ̀nà);
            if (클래스들.put(détà.Orúkọ, détà) != null) throw new Ìtumọ̀_àṣìṣe("중복 ọ̀wọ́_iye: " + détà.Orúkọ);
            for (ọmọ_ẹgbẹ́_détà àayè_wúnrẹ̀n_iye : détà.àayè_wúnrẹ̀n_iye) {
                if ((àayè_wúnrẹ̀n_iye.wáyè_sí_ìgbéwọlé & 8) == 0 || 형식읽기(àayè_wúnrẹ̀n_iye.서술).equals(Collections.singletonList("V"))) throw new Ìtumọ̀_àṣìṣe("ìdágún_iye 필드만 àtìlẹ́yìn_iye");
                if (필드들.put(new ìlànà_Ìtọ́ka(détà.Orúkọ, àayè_wúnrẹ̀n_iye.Orúkọ, àayè_wúnrẹ̀n_iye.서술), àayè_wúnrẹ̀n_iye) != null) throw new Ìtumọ̀_àṣìṣe("중복 àayè_wúnrẹ̀n_iye");
            }
            for (ọmọ_ẹgbẹ́_détà ÀKÀNṢEFỌMÚLÀ_iye : détà.ÀKÀNṢEFỌMÚLÀ_iye) {
                if (ÀKÀNṢEFỌMÚLÀ_iye.Orúkọ.equals("<init>")) continue;
                if ((ÀKÀNṢEFỌMÚLÀ_iye.wáyè_sí_ìgbéwọlé & 8) == 0 || (ÀKÀNṢEFỌMÚLÀ_iye.wáyè_sí_ìgbéwọlé & (0x20 | 0x400)) != 0) throw new Ìtumọ̀_àṣìṣe("ìdágún_iye 비동기화 함수만 àtìlẹ́yìn_iye");
                new 함수형식(ÀKÀNṢEFỌMÚLÀ_iye.서술);
                if (함수들.put(new ìlànà_Ìtọ́ka(détà.Orúkọ, ÀKÀNṢEFỌMÚLÀ_iye.Orúkọ, ÀKÀNṢEFỌMÚLÀ_iye.서술), ÀKÀNṢEFỌMÚLÀ_iye) != null) throw new Ìtumọ̀_àṣìṣe("중복 ÀKÀNṢEFỌMÚLÀ_iye");
            }
        }
    }
    String fọ́nrán_àmì(String SMS) { return 문자열들.computeIfAbsent(SMS, iye -> "j_text_" + 문자열들.size()); }
    String aláìṣeéyípadà_ìsọ̀rọ̀sí(ọ̀wọ́_détà détà, int wá_atọ̀ka_àkóónú) {
        if (wá_atọ̀ka_àkóónú < 1 || wá_atọ̀ka_àkóónú >= détà.상수종류.length) throw new Ìtumọ̀_àṣìṣe("aláìṣeéyípadà_iye wá_atọ̀ka_àkóónú ní_ṣókí àṣìṣe");
        if (détà.상수종류[wá_atọ̀ka_àkóónú] == 3) return "(word)(uint32_t)(" + détà.aláìṣeéyípadà_détà[wá_atọ̀ka_àkóónú] + ")";
        if (détà.상수종류[wá_atọ̀ka_àkóónú] == 8) return "(word)" + fọ́nrán_àmì(détà.문자((Integer)détà.aláìṣeéyípadà_détà[wá_atọ̀ka_àkóónú]));
        throw new Ìtumọ̀_àṣìṣe("정수와 fọ́nrán_iye 상수만 àtìlẹ́yìn_iye");
    }
    String 함수원형(ìlànà_Ìtọ́ka Ìtọ́ka) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Ìtọ́ka.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + àmì("method", Ìtọ́ka.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void ṣàyẹ̀wò_agbègbè(int wá_atọ̀ka_àkóónú, int 지역변수수) { if (wá_atọ̀ka_àkóónú < 0 || wá_atọ̀ka_àkóónú >= 지역변수수) throw new Ìtumọ̀_àṣìṣe("agbègbè_sàkání 변수 wá_atọ̀ka_àkóónú ní_ṣókí àṣìṣe"); }
    void 분기넣기(List<String> 출력, Set<Integer> ẹ̀ka_Àtòkọ, int 위치, int 이동량, String kání) {
        int èbúté_iye = 위치 + 이동량; ẹ̀ka_Àtòkọ.add(èbúté_iye);
        출력.add((kání == null ? "" : "if (" + kání + ") ") + "goto b" + èbúté_iye + ";");
    }
    String 함수본문(ìlànà_Ìtọ́ka ÀKÀNṢEFỌMÚLÀ_iye, ọmọ_ẹgbẹ́_détà détà) {
        byte[] 본문자료 = détà.àwòmọ́_iye.get("Code"); if (본문자료 == null) throw new Ìtumọ̀_àṣìṣe("ÀKÀNṢEFỌMÚLÀ_iye 몸체가 없음: " + ÀKÀNṢEFỌMÚLÀ_iye.Orúkọ);
        détà_akàwé akàwé_iye = new détà_akàwé(본문자료); int 쌓임깊이 = akàwé_iye.두바이트(), 지역변수수 = akàwé_iye.두바이트();
        détà_akàwé àṣẹ_détà = new détà_akàwé(akàwé_iye.Kàá(akàwé_iye.네바이트()));
        if (akàwé_iye.두바이트() != 0) throw new Ìtumọ̀_àṣìṣe("try/catch/finally 미지원");
        함수형식 ìgúnrégé_iye = new 함수형식(ÀKÀNṢEFỌMÚLÀ_iye.서술); if (지역변수수 < ìgúnrégé_iye.인수.size()) throw new Ìtumọ̀_àṣìṣe("매개변수보다 적은 agbègbè_sàkání 변수");
        ọ̀wọ́_détà ọ̀wọ́_iye = 클래스들.get(ÀKÀNṢEFỌMÚLÀ_iye.Oníǹkan_iye);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(ÀKÀNṢEFỌMÚLÀ_iye) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < ìgúnrégé_iye.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ẹ̀ka_Àtòkọ = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (àṣẹ_détà.위치 < àṣẹ_détà.détà.length) {
            int 위치 = àṣẹ_détà.위치, Àṣẹ = àṣẹ_détà.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (Àṣẹ == 0) continue;
            if (Àṣẹ == 1) 출력.add("PUSH(0);");
            else if (Àṣẹ >= 2 && Àṣẹ <= 8) 출력.add("PUSH((uint32_t)(" + (Àṣẹ - 3) + "));");
            else if (Àṣẹ == 16 || Àṣẹ == 17) 출력.add("PUSH((uint32_t)(" + (Àṣẹ == 16 ? àṣẹ_détà.부호한바이트() : àṣẹ_détà.부호두바이트()) + "));");
            else if (Àṣẹ == 18 || Àṣẹ == 19) 출력.add("PUSH(" + aláìṣeéyípadà_ìsọ̀rọ̀sí(ọ̀wọ́_iye, Àṣẹ == 18 ? àṣẹ_détà.한바이트() : àṣẹ_détà.두바이트()) + ");");
            else if (Àṣẹ == 21 || Àṣẹ == 25 || (Àṣẹ >= 26 && Àṣẹ <= 29) || (Àṣẹ >= 42 && Àṣẹ <= 45)) {
                int wá_atọ̀ka_àkóónú = Àṣẹ == 21 || Àṣẹ == 25 ? àṣẹ_détà.한바이트() : Àṣẹ - (Àṣẹ <= 29 ? 26 : 42);
                ṣàyẹ̀wò_agbègbè(wá_atọ̀ka_àkóónú, 지역변수수); 출력.add("PUSH(l[" + wá_atọ̀ka_àkóónú + "]);");
            } else if (Àṣẹ == 54 || Àṣẹ == 58 || (Àṣẹ >= 59 && Àṣẹ <= 62) || (Àṣẹ >= 75 && Àṣẹ <= 78)) {
                int wá_atọ̀ka_àkóónú = Àṣẹ == 54 || Àṣẹ == 58 ? àṣẹ_détà.한바이트() : Àṣẹ - (Àṣẹ <= 62 ? 59 : 75);
                ṣàyẹ̀wò_agbègbè(wá_atọ̀ka_àkóónú, 지역변수수); 출력.add("l[" + wá_atọ̀ka_àkóónú + "] = POP();");
            } else if (Àṣẹ == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Àṣẹ == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Àṣẹ == 87 || Àṣẹ == 88) 출력.add(Àṣẹ == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Àṣẹ >= 89 && Àṣẹ <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ìtodátà_Àtòkọ = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Àṣẹ - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char iye : ìtodátà_Àtòkọ[Àṣẹ - 89].toCharArray()) 출력.add("PUSH(" + iye + ");");
            } else if (Àṣẹ == 96 || Àṣẹ == 100 || Àṣẹ == 104 || Àṣẹ == 126 || Àṣẹ == 128 || Àṣẹ == 130) {
                String ìmú_ṣiṣẹ́_iye = Àṣẹ == 96 ? "+" : Àṣẹ == 100 ? "-" : Àṣẹ == 104 ? "*" : Àṣẹ == 126 ? "&" : Àṣẹ == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + ìmú_ṣiṣẹ́_iye + " (uint32_t)b);");
            } else if (Àṣẹ == 108 || Àṣẹ == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Àṣẹ == 112 ? 1 : 0) + "));");
            else if (Àṣẹ == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Àṣẹ == 120 || Àṣẹ == 122 || Àṣẹ == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Àṣẹ == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Àṣẹ == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Àṣẹ == 132) {
                int wá_atọ̀ka_àkóónú = àṣẹ_détà.한바이트(), 증가량 = àṣẹ_détà.부호한바이트(); ṣàyẹ̀wò_agbègbè(wá_atọ̀ka_àkóónú, 지역변수수);
                출력.add("l[" + wá_atọ̀ka_àkóónú + "] = (uint32_t)l[" + wá_atọ̀ka_àkóónú + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Àṣẹ >= 145 && Àṣẹ <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Àṣẹ == 145 ? "int8_t" : Àṣẹ == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Àṣẹ >= 153 && Àṣẹ <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, ẹ̀ka_Àtòkọ, 위치, àṣẹ_détà.부호두바이트(), "(int32_t)a " + 비교들[Àṣẹ - 153] + " 0");
            } else if (Àṣẹ >= 159 && Àṣẹ <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, ẹ̀ka_Àtòkọ, 위치, àṣẹ_détà.부호두바이트(), Àṣẹ >= 165 ? "a " + 비교들[Àṣẹ - 159] + " b" : "(int32_t)a " + 비교들[Àṣẹ - 159] + " (int32_t)b");
            } else if (Àṣẹ == 167 || Àṣẹ == 200) 분기넣기(출력, ẹ̀ka_Àtòkọ, 위치, Àṣẹ == 167 ? àṣẹ_détà.부호두바이트() : àṣẹ_détà.네바이트(), null);
            else if (Àṣẹ == 170 || Àṣẹ == 171) {
                while (àṣẹ_détà.위치 % 4 != 0) àṣẹ_détà.한바이트();
                int àdáwọ̀ = àṣẹ_détà.네바이트(); 출력.add("a = POP();");
                if (Àṣẹ == 170) {
                    int 아래 = àṣẹ_détà.네바이트(), 위 = àṣẹ_détà.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (àṣẹ_détà.détà.length - àṣẹ_détà.위치) / 4) throw new Ìtumọ̀_àṣìṣe("switch ní_ṣókí àṣìṣe");
                    for (long iye = 아래; iye <= 위; iye++) 분기넣기(출력, ẹ̀ka_Àtòkọ, 위치, àṣẹ_détà.네바이트(), "(int32_t)a == (" + iye + ")");
                } else {
                    int 개수 = àṣẹ_détà.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (àṣẹ_détà.détà.length - àṣẹ_détà.위치) / 8) throw new Ìtumọ̀_àṣìṣe("switch Ìwọ̀n àṣìṣe");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int iye = àṣẹ_détà.네바이트(); if (순번 > 0 && iye <= 앞값) throw new Ìtumọ̀_àṣìṣe("switch ìtodátà_iye àṣìṣe"); 앞값 = iye;
                        분기넣기(출력, ẹ̀ka_Àtòkọ, 위치, àṣẹ_détà.네바이트(), "(int32_t)a == (" + iye + ")");
                    }
                }
                분기넣기(출력, ẹ̀ka_Àtòkọ, 위치, àdáwọ̀, null);
            } else if (Àṣẹ == 172 || Àṣẹ == 176 || Àṣẹ == 177) 출력.add("return " + (Àṣẹ == 177 ? "0" : "POP()") + ";");
            else if (Àṣẹ == 178 || Àṣẹ == 179) {
                ìlànà_Ìtọ́ka Ìtọ́ka = ọ̀wọ́_iye.Ìtọ́ka(àṣẹ_détà.두바이트()); if (!필드들.containsKey(Ìtọ́ka)) throw new Ìtumọ̀_àṣìṣe("알 수 없는 àayè_wúnrẹ̀n_iye");
                출력.add(àmì("init", Ìtọ́ka.Oníǹkan_iye) + "();"); String àayè_wúnrẹ̀n_iye = àmì("field", Ìtọ́ka.부분들());
                출력.add(Àṣẹ == 178 ? "PUSH(" + àayè_wúnrẹ̀n_iye + ");" : àayè_wúnrẹ̀n_iye + " = POP();");
            } else if (Àṣẹ == 184) {
                ìlànà_Ìtọ́ka Ìtọ́ka = ọ̀wọ́_iye.Ìtọ́ka(àṣẹ_détà.두바이트()); if (!함수들.containsKey(Ìtọ́ka)) throw new Ìtumọ̀_àṣìṣe("알 수 없는 ÀKÀNṢEFỌMÚLÀ_iye");
                함수형식 호출형식 = new 함수형식(Ìtọ́ka.서술); int 개수 = 호출형식.인수.size();
                출력.add(àmì("init", Ìtọ́ka.Oníǹkan_iye) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + àmì("method", Ìtọ́ka.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Àṣẹ == 182) {
                ìlànà_Ìtọ́ka Ìtọ́ka = ọ̀wọ́_iye.Ìtọ́ka(àṣẹ_détà.두바이트());
                if (Ìtọ́ka.equals(new ìlànà_Ìtọ́ka("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Ìtọ́ka.equals(new ìlànà_Ìtọ́ka("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Ìtumọ̀_àṣìṣe("가상 ÀKÀNṢEFỌMÚLÀ_iye 호출 미지원");
            } else if (Àṣẹ == 188) {
                if (àṣẹ_détà.한바이트() != 10) throw new Ìtumọ̀_àṣìṣe("new int[]만 àtìlẹ́yìn_iye"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Àṣẹ == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Àṣẹ == 196) {
                int Àfikún_iye = àṣẹ_détà.한바이트(), wá_atọ̀ka_àkóónú = àṣẹ_détà.두바이트(); ṣàyẹ̀wò_agbègbè(wá_atọ̀ka_àkóónú, 지역변수수);
                if (Àfikún_iye == 21 || Àfikún_iye == 25) 출력.add("PUSH(l[" + wá_atọ̀ka_àkóónú + "]);");
                else if (Àfikún_iye == 54 || Àfikún_iye == 58) 출력.add("l[" + wá_atọ̀ka_àkóónú + "] = POP();");
                else if (Àfikún_iye == 132) 출력.add("l[" + wá_atọ̀ka_àkóónú + "] = (uint32_t)l[" + wá_atọ̀ka_àkóónú + "] + (uint32_t)(" + àṣẹ_détà.부호두바이트() + ");");
                else throw new Ìtumọ̀_àṣìṣe("미지원 wide Àṣẹ");
            } else if (Àṣẹ == 198 || Àṣẹ == 199) {
                출력.add("a = POP();"); 분기넣기(출력, ẹ̀ka_Àtòkọ, 위치, àṣẹ_détà.부호두바이트(), "a " + (Àṣẹ == 198 ? "==" : "!=") + " 0");
            } else throw new Ìtumọ̀_àṣìṣe(ÀKÀNṢEFỌMÚLÀ_iye.Oníǹkan_iye + "." + ÀKÀNṢEFỌMÚLÀ_iye.Orúkọ + ", báìtì_iye " + 위치 + ": 미지원 Àṣẹ " + Àṣẹ);
        }
        if (!경계들.containsAll(ẹ̀ka_Àtòkọ)) throw new Ìtumọ̀_àṣìṣe("Àṣẹ 경계가 아닌 곳으로 ẹ̀ka");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String ṣàgbéjáde_ìlànà(String ṣàsopọ̀_àmì, String àfojúsùn, boolean 진입점여부) {
        int 자리 = àfojúsùn.lastIndexOf('.'); if (자리 < 0 || !ṣàsopọ̀_àmì.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Ìtumọ̀_àṣìṣe("내보내기 지정 àṣìṣe");
        String Oníǹkan_iye = àfojúsùn.substring(0, 자리).replace('.', '/'), Orúkọ = àfojúsùn.substring(자리 + 1); ìlànà_Ìtọ́ka ẹ̀yàn_iye = null;
        for (ìlànà_Ìtọ́ka Ìtọ́ka : 함수들.keySet()) if (Ìtọ́ka.Oníǹkan_iye.equals(Oníǹkan_iye) && Ìtọ́ka.Orúkọ.equals(Orúkọ)) {
            if (ẹ̀yàn_iye != null) throw new Ìtumọ̀_àṣìṣe("겹친 내보내기 àfojúsùn"); ẹ̀yàn_iye = Ìtọ́ka;
        }
        if (ẹ̀yàn_iye == null || (함수들.get(ẹ̀yàn_iye).wáyè_sí_ìgbéwọlé & 0x100) != 0) throw new Ìtumọ̀_àṣìṣe("내보낼 함수가 없음 또는 native ÀKÀNṢEFỌMÚLÀ_iye");
        함수형식 ìgúnrégé_iye = new 함수형식(ẹ̀yàn_iye.서술);
        if ((진입점여부 && !ìgúnrégé_iye.인수.isEmpty()) || !Arrays.asList("V", "I").contains(ìgúnrégé_iye.반환)) throw new Ìtumọ̀_àṣìṣe("ìgbéwọlé_kókó_iye 또는 C 경계 ìgúnrégé_iye àṣìṣe");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < ìgúnrégé_iye.인수.size(); 순번++) {
            if (!ìgúnrégé_iye.인수.get(순번).equals("I")) throw new Ìtumọ̀_àṣìṣe("C 경계는 int 인수만 àtìlẹ́yìn_iye");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (ìgúnrégé_iye.반환.equals("V") ? "void " : "int32_t ") + ṣàsopọ̀_àmì + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + àmì("init", ẹ̀yàn_iye.Oníǹkan_iye) + "(); " + (ìgúnrégé_iye.반환.equals("V") ? "" : "return (int32_t)") + àmì("method", ẹ̀yàn_iye.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String ìgbéwọlé_kókó, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<ìlànà_Ìtọ́ka, ọmọ_ẹgbẹ́_détà> ìgbéwọlé_iye : 함수들.entrySet()) {
            ìlànà_Ìtọ́ka Ìtọ́ka = ìgbéwọlé_iye.getKey(); ọmọ_ẹgbẹ́_détà détà = ìgbéwọlé_iye.getValue(); 선언들.add(함수원형(Ìtọ́ka) + ";");
            if ((détà.wáyè_sí_ìgbéwọlé & 0x100) != 0) {
                String Darapọ̀ = 기계함수들.get(Ìtọ́ka.Orúkọ + Ìtọ́ka.서술);
                if (!Ìtọ́ka.Oníǹkan_iye.equals(maṣíìnì_ọ̀wọ́) || Darapọ̀ == null) throw new Ìtumọ̀_àṣìṣe("허용되지 않은 native ÀKÀNṢEFỌMÚLÀ_iye: " + Ìtọ́ka.Orúkọ);
                int 개수 = new 함수형식(Ìtọ́ka.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Darapọ̀ + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Ìtọ́ka) + " { return " + Darapọ̀ + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Ìtọ́ka, détà));
        }
        for (Map.Entry<ìlànà_Ìtọ́ka, ọmọ_ẹgbẹ́_détà> ìgbéwọlé_iye : 필드들.entrySet()) {
            ìlànà_Ìtọ́ka Ìtọ́ka = ìgbéwọlé_iye.getKey(); byte[] aláìṣeéyípadà_iye = ìgbéwọlé_iye.getValue().àwòmọ́_iye.get("ConstantValue");
            String iye = aláìṣeéyípadà_iye == null ? "0" : aláìṣeéyípadà_ìsọ̀rọ̀sí(클래스들.get(Ìtọ́ka.Oníǹkan_iye), new détà_akàwé(aláìṣeéyípadà_iye).두바이트());
            필드선언들.add("static word " + àmì("field", Ìtọ́ka.부분들()) + " = " + iye + ";");
        }
        for (String Orúkọ : 클래스들.keySet()) {
            String pàjùbà = àmì("init", Orúkọ), ipò_iye = àmì("state", Orúkọ);
            선언들.add("static void " + pàjùbà + "(void);"); 필드선언들.add("static unsigned " + ipò_iye + ";");
            ìlànà_Ìtọ́ka Ìtọ́ka = new ìlànà_Ìtọ́ka(Orúkọ, "<clinit>", "()V");
            몸체들.add("static void " + pàjùbà + "(void) { if(" + ipò_iye + ") return; " + ipò_iye + " = 1; " + (함수들.containsKey(Ìtọ́ka) ? àmì("method", Ìtọ́ka.부분들()) + "(); " : "") + ipò_iye + " = 2; }");
        }
        몸체들.add(ṣàgbéjáde_ìlànà("java_entry", ìgbéwọlé_kókó, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new Ìtumọ̀_àṣìṣe("내보내기 지정 àṣìṣe");
            String Orúkọ = 지정.substring(0, 자리); 공개이름.add(Orúkọ); 몸체들.add(ṣàgbéjáde_ìlànà(Orúkọ, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> ìgbéwọlé_iye : 문자열들.entrySet()) {
            String SMS = ìgbéwọlé_iye.getKey(); StringBuilder ÀRÉÈ_iye = new StringBuilder("static const word " + ìgbéwọlé_iye.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) ÀRÉÈ_iye.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(ÀRÉÈ_iye.append("};").toString());
        }
        String àtìlẹ́yìn_iye = Files.readString(ohun_àmúlò_ọ̀nà.resolve("àkókò_iṣẹ́_èdè_tówọ́pọ̀_àtìlẹ́yìn.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(àtìlẹ́yìn_iye + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String orísun, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> orúkọ_atọ́ka = new HashMap<>();
        for (String ìlà : Files.readAllLines(ohun_àmúlò_ọ̀nà.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] ṣàsopọ̀_iye = ìlà.split("\t"); orúkọ_atọ́ka.put(ṣàsopọ̀_iye[0], ṣàsopọ̀_iye[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(orísun); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Orúkọ = 찾개.group(), 새이름 = Orúkọ;
            if (!Orúkọ.startsWith("//") && !Orúkọ.startsWith("/*") && !Orúkọ.startsWith("\"") && !Orúkọ.startsWith("'") && !공개이름.contains(Orúkọ)) {
                새이름 = orúkọ_atọ́ka.getOrDefault(Orúkọ, Orúkọ);
                if (Orúkọ.matches("a[0-9]+")) 새이름 = "인수" + Orúkọ.substring(1);
                if (Orúkọ.matches("b[0-9]+")) 새이름 = "ẹ̀ka" + Orúkọ.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char ẹyọ_ọ̀rọ̀_iye : 새이름.toCharArray()) 표기.append(ẹyọ_ọ̀rọ̀_iye < 128 ? Character.toString(ẹyọ_ọ̀rọ̀_iye) : String.format(Locale.ROOT, "\\u%04x", (int)ẹyọ_ọ̀rọ̀_iye));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(ìlànà_Ìtọ́ka ÀKÀNṢEFỌMÚLÀ_iye, ọmọ_ẹgbẹ́_détà détà, Map<String,String> maṣíìnì_atọ́ka, String àfojúsùn) {
        String 표식 = àmì("method", ÀKÀNṢEFỌMÚLÀ_iye.부분들());
        List<String> ìlà = new ArrayList<>();
        if ((détà.wáyè_sí_ìgbéwọlé & 0x100) != 0) {
            String Darapọ̀ = maṣíìnì_atọ́ka.get(ÀKÀNṢEFỌMÚLÀ_iye.Orúkọ + ÀKÀNṢEFỌMÚLÀ_iye.서술);
            if (!ÀKÀNṢEFỌMÚLÀ_iye.Oníǹkan_iye.equals(àfojúsùn.equals("kernel") ? "ohun_èlò_iye" : "aṣàmúlò") || Darapọ̀ == null) throw new Ìtumọ̀_àṣìṣe("허용되지 않은 native ÀKÀNṢEFỌMÚLÀ_iye");
            return ".text\n" + 표식 + ":\njmp " + Darapọ̀;
        }
        byte[] kókó_ọ̀rọ̀_ìkọ = détà.àwòmọ́_iye.get("Code"); if (kókó_ọ̀rọ̀_ìkọ == null) throw new Ìtumọ̀_àṣìṣe("ÀKÀNṢEFỌMÚLÀ_iye 몸체가 없음");
        détà_akàwé akàwé_iye = new détà_akàwé(kókó_ọ̀rọ̀_ìkọ); akàwé_iye.두바이트(); int 지역수 = akàwé_iye.두바이트();
        détà_akàwé àṣẹ_détà = new détà_akàwé(akàwé_iye.Kàá(akàwé_iye.네바이트()));
        if (akàwé_iye.두바이트() != 0) throw new Ìtumọ̀_àṣìṣe("try/catch/finally 미지원");
        함수형식 ìgúnrégé_iye = new 함수형식(ÀKÀNṢEFỌMÚLÀ_iye.서술); if (지역수 < ìgúnrégé_iye.인수.size()) throw new Ìtumọ̀_àṣìṣe("매개변수보다 적은 agbègbè_sàkání 변수");
        Collections.addAll(ìlà,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < ìgúnrégé_iye.인수.size(); 순번++) Collections.addAll(ìlà,"movl " + (8 + 4 * (ìgúnrégé_iye.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        ọ̀wọ́_détà ọ̀wọ́_iye = 클래스들.get(ÀKÀNṢEFỌMÚLÀ_iye.Oníǹkan_iye); Set<Integer> 경계들 = new HashSet<>(), ẹ̀ka_Àtòkọ = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (àṣẹ_détà.위치 < àṣẹ_détà.détà.length) {
            int 위치 = àṣẹ_détà.위치, Àṣẹ = àṣẹ_détà.한바이트(); String 자리 = 표식 + "_b" + 위치;
            ìlà.add(자리 + ":"); 경계들.add(위치);
            if (Àṣẹ == 0) ìlà.add("nop");
            else if (Àṣẹ == 1) ìlà.add("pushl $0");
            else if (Àṣẹ >= 2 && Àṣẹ <= 8) ìlà.add("pushl $" + (Àṣẹ - 3));
            else if (Àṣẹ == 16 || Àṣẹ == 17) ìlà.add("pushl $" + (Àṣẹ == 16 ? àṣẹ_détà.부호한바이트() : àṣẹ_détà.부호두바이트()));
            else if (Àṣẹ == 18 || Àṣẹ == 19) {
                int wá_atọ̀ka_àkóónú = Àṣẹ == 18 ? àṣẹ_détà.한바이트() : àṣẹ_détà.두바이트();
                ìlà.add("pushl $" + 엑스상수(ọ̀wọ́_iye,wá_atọ̀ka_àkóónú));
            } else if (Àṣẹ == 21 || Àṣẹ == 25 || (Àṣẹ >= 26 && Àṣẹ <= 29) || (Àṣẹ >= 42 && Àṣẹ <= 45) || Àṣẹ == 54 || Àṣẹ == 58 || (Àṣẹ >= 59 && Àṣẹ <= 62) || (Àṣẹ >= 75 && Àṣẹ <= 78)) {
                boolean 읽음 = Àṣẹ < 54; int wá_atọ̀ka_àkóónú = Àṣẹ == 21 || Àṣẹ == 25 || Àṣẹ == 54 || Àṣẹ == 58 ? àṣẹ_détà.한바이트() : Àṣẹ - (Àṣẹ <= 29 ? 26 : Àṣẹ <= 45 ? 42 : Àṣẹ <= 62 ? 59 : 75);
                ṣàyẹ̀wò_agbègbè(wá_atọ̀ka_àkóónú,지역수); ìlà.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (wá_atọ̀ka_àkóónú + 1)) + "(%ebp)");
            } else if (Àṣẹ == 46) Collections.addAll(ìlà,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Àṣẹ == 79) Collections.addAll(ìlà,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Àṣẹ == 87 || Àṣẹ == 88) ìlà.add("addl $" + (Àṣẹ == 87 ? 4 : 8) + ", %esp");
            else if (Àṣẹ >= 89 && Àṣẹ <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ìtodátà_Àtòkọ = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Àṣẹ - 89]; 순번++) ìlà.add("popl " + 저장기들[순번]);
                for (int 순번 : ìtodátà_Àtòkọ[Àṣẹ - 89]) ìlà.add("pushl " + 저장기들[순번]);
            } else if (Àṣẹ == 96 || Àṣẹ == 100 || Àṣẹ == 104 || Àṣẹ == 126 || Àṣẹ == 128 || Àṣẹ == 130) {
                String ìmú_ṣiṣẹ́_iye = Àṣẹ == 96 ? "addl" : Àṣẹ == 100 ? "subl" : Àṣẹ == 104 ? "imull" : Àṣẹ == 126 ? "andl" : Àṣẹ == 128 ? "orl" : "xorl";
                Collections.addAll(ìlà,"popl %ecx","popl %eax",ìmú_ṣiṣẹ́_iye + " %ecx, %eax","pushl %eax");
            } else if (Àṣẹ == 108 || Àṣẹ == 112) Collections.addAll(ìlà,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Àṣẹ == 108 ? "%eax" : "%edx"));
            else if (Àṣẹ == 116) ìlà.add("negl (%esp)");
            else if (Àṣẹ == 120 || Àṣẹ == 122 || Àṣẹ == 124) Collections.addAll(ìlà,"popl %ecx","popl %eax",(Àṣẹ == 120 ? "sall" : Àṣẹ == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Àṣẹ == 132) {
                int wá_atọ̀ka_àkóónú = àṣẹ_détà.한바이트(), 증가 = àṣẹ_détà.부호한바이트(); ṣàyẹ̀wò_agbègbè(wá_atọ̀ka_àkóónú,지역수); ìlà.add("addl $" + 증가 + ", -" + (4 * (wá_atọ̀ka_àkóónú + 1)) + "(%ebp)");
            } else if (Àṣẹ >= 145 && Àṣẹ <= 147) Collections.addAll(ìlà,"popl %eax",Àṣẹ == 145 ? "movsbl %al, %eax" : Àṣẹ == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Àṣẹ >= 153 && Àṣẹ <= 166) {
                if (Àṣẹ <= 158) Collections.addAll(ìlà,"popl %eax","testl %eax, %eax");
                else Collections.addAll(ìlà,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int èbúté_iye = 위치 + àṣẹ_détà.부호두바이트(); ẹ̀ka_Àtòkọ.add(èbúté_iye); ìlà.add(비교들[Àṣẹ - (Àṣẹ <= 158 ? 153 : 159)] + " " + 표식 + "_b" + èbúté_iye);
            } else if (Àṣẹ == 167 || Àṣẹ == 200) {
                int èbúté_iye = 위치 + (Àṣẹ == 167 ? àṣẹ_détà.부호두바이트() : àṣẹ_détà.네바이트()); ẹ̀ka_Àtòkọ.add(èbúté_iye); ìlà.add("jmp " + 표식 + "_b" + èbúté_iye);
            } else if (Àṣẹ == 170 || Àṣẹ == 171) {
                while (àṣẹ_détà.위치 % 4 != 0) àṣẹ_détà.한바이트();
                int àdáwọ̀ = 위치 + àṣẹ_détà.네바이트(); ẹ̀ka_Àtòkọ.add(àdáwọ̀); ìlà.add("popl %eax");
                int 개수, 아래 = 0;
                if (Àṣẹ == 170) { 아래 = àṣẹ_détà.네바이트(); int 위 = àṣẹ_détà.네바이트(); long gígùn_iye = (long)위 - 아래 + 1; if (gígùn_iye < 1 || gígùn_iye > (àṣẹ_détà.détà.length - àṣẹ_détà.위치) / 4) throw new Ìtumọ̀_àṣìṣe("switch ní_ṣókí àṣìṣe"); 개수 = (int)gígùn_iye; }
                else { 개수 = àṣẹ_détà.네바이트(); if (개수 < 0 || 개수 > (àṣẹ_détà.détà.length - àṣẹ_détà.위치) / 8) throw new Ìtumọ̀_àṣìṣe("switch Ìwọ̀n àṣìṣe"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int iye = Àṣẹ == 170 ? 아래 + 순번 : àṣẹ_détà.네바이트(), èbúté_iye = 위치 + àṣẹ_détà.네바이트(); ẹ̀ka_Àtòkọ.add(èbúté_iye);
                    Collections.addAll(ìlà,"cmpl $" + iye + ", %eax","je " + 표식 + "_b" + èbúté_iye);
                }
                ìlà.add("jmp " + 표식 + "_b" + àdáwọ̀);
            } else if (Àṣẹ == 172 || Àṣẹ == 176 || Àṣẹ == 177) {
                if (Àṣẹ != 177) ìlà.add("popl %eax"); Collections.addAll(ìlà,"leave","ret");
            } else if (Àṣẹ == 178 || Àṣẹ == 179) {
                ìlànà_Ìtọ́ka Ìtọ́ka = ọ̀wọ́_iye.Ìtọ́ka(àṣẹ_détà.두바이트()); if (!필드들.containsKey(Ìtọ́ka)) throw new Ìtumọ̀_àṣìṣe("알 수 없는 àayè_wúnrẹ̀n_iye");
                Collections.addAll(ìlà,"call " + àmì("init",Ìtọ́ka.Oníǹkan_iye),(Àṣẹ == 178 ? "pushl " : "popl ") + àmì("field",Ìtọ́ka.부분들()));
            } else if (Àṣẹ == 184) {
                ìlànà_Ìtọ́ka Ìtọ́ka = ọ̀wọ́_iye.Ìtọ́ka(àṣẹ_détà.두바이트()); if (!함수들.containsKey(Ìtọ́ka)) throw new Ìtumọ̀_àṣìṣe("알 수 없는 ÀKÀNṢEFỌMÚLÀ_iye");
                함수형식 호출형식 = new 함수형식(Ìtọ́ka.서술); Collections.addAll(ìlà,"call " + àmì("init",Ìtọ́ka.Oníǹkan_iye),"call " + àmì("method",Ìtọ́ka.부분들()));
                if (!호출형식.인수.isEmpty()) ìlà.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) ìlà.add("pushl %eax");
            } else if (Àṣẹ == 182) {
                ìlànà_Ìtọ́ka Ìtọ́ka = ọ̀wọ́_iye.Ìtọ́ka(àṣẹ_détà.두바이트());
                if (Ìtọ́ka.equals(new ìlànà_Ìtọ́ka("java/lang/String","length","()I"))) Collections.addAll(ìlà,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Ìtọ́ka.equals(new ìlànà_Ìtọ́ka("java/lang/String","charAt","(I)C"))) Collections.addAll(ìlà,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Ìtumọ̀_àṣìṣe("가상 ÀKÀNṢEFỌMÚLÀ_iye 호출 미지원");
            } else if (Àṣẹ == 188) {
                if (àṣẹ_détà.한바이트() != 10) throw new Ìtumọ̀_àṣìṣe("new int[]만 àtìlẹ́yìn_iye"); Collections.addAll(ìlà,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Àṣẹ == 190) Collections.addAll(ìlà,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Àṣẹ == 196) {
                int Àfikún_iye = àṣẹ_détà.한바이트(), wá_atọ̀ka_àkóónú = àṣẹ_détà.두바이트(); ṣàyẹ̀wò_agbègbè(wá_atọ̀ka_àkóónú,지역수);
                if (Àfikún_iye == 21 || Àfikún_iye == 25 || Àfikún_iye == 54 || Àfikún_iye == 58) ìlà.add((Àfikún_iye <= 25 ? "pushl " : "popl ") + "-" + 4 * (wá_atọ̀ka_àkóónú + 1) + "(%ebp)");
                else if (Àfikún_iye == 132) ìlà.add("addl $" + àṣẹ_détà.부호두바이트() + ", -" + 4 * (wá_atọ̀ka_àkóónú + 1) + "(%ebp)");
                else throw new Ìtumọ̀_àṣìṣe("wide Àṣẹ 미지원");
            } else if (Àṣẹ == 198 || Àṣẹ == 199) {
                int èbúté_iye = 위치 + àṣẹ_détà.부호두바이트(); ẹ̀ka_Àtòkọ.add(èbúté_iye); Collections.addAll(ìlà,"popl %eax","testl %eax, %eax",(Àṣẹ == 198 ? "je " : "jne ") + 표식 + "_b" + èbúté_iye);
            } else throw new Ìtumọ̀_àṣìṣe("미지원 Àṣẹ: " + Àṣẹ);
        }
        if (!경계들.containsAll(ẹ̀ka_Àtòkọ)) throw new Ìtumọ̀_àṣìṣe("Àṣẹ 경계가 아닌 곳으로 ẹ̀ka");
        ìlà.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",ìlà);
    }
    String 엑스상수(ọ̀wọ́_détà détà, int wá_atọ̀ka_àkóónú) {
        if (détà.상수종류[wá_atọ̀ka_àkóónú] == 3) return détà.aláìṣeéyípadà_détà[wá_atọ̀ka_àkóónú].toString();
        if (détà.상수종류[wá_atọ̀ka_àkóónú] == 8) return fọ́nrán_àmì(détà.문자((Integer)détà.aláìṣeéyípadà_détà[wá_atọ̀ka_àkóónú]));
        throw new Ìtumọ̀_àṣìṣe("정수와 fọ́nrán_iye 상수만 àtìlẹ́yìn_iye");
    }
    String 엑스조립본(String ìgbéwọlé_kókó, List<String> 내보냄, String àfojúsùn) throws IOException {
        Map<String,String> maṣíìnì_atọ́ka = new HashMap<>();
        for (String ìlà : Files.readAllLines(ohun_àmúlò_ọ̀nà.resolve("엑스기계함수.tsv"))) { String[] ṣàsopọ̀_iye = ìlà.split("\t"); if (ṣàsopọ̀_iye[0].equals(àfojúsùn)) maṣíìnì_atọ́ka.put(ṣàsopọ̀_iye[1] + ṣàsopọ̀_iye[2],ṣàsopọ̀_iye[3]); }
        int 자리 = ìgbéwọlé_kókó.lastIndexOf('.'); if (자리 < 0) throw new Ìtumọ̀_àṣìṣe("ìgbéwọlé_kókó 지정 àṣìṣe");
        String Oníǹkan_iye = ìgbéwọlé_kókó.substring(0,자리).replace('.','/'), ìlànà_ìgbéwọlé_orúkọ = ìgbéwọlé_kókó.substring(자리 + 1); ìlànà_Ìtọ́ka ìgbéwọlé_kókó_iye = null;
        for (String 서술 : Arrays.asList("()I","()V")) { ìlànà_Ìtọ́ka Ìtọ́ka = new ìlànà_Ìtọ́ka(Oníǹkan_iye,ìlànà_ìgbéwọlé_orúkọ,서술); if (함수들.containsKey(Ìtọ́ka)) { if (ìgbéwọlé_kókó_iye != null) throw new Ìtumọ̀_àṣìṣe("겹친 ìgbéwọlé_kókó"); ìgbéwọlé_kókó_iye = Ìtọ́ka; } }
        if (ìgbéwọlé_kókó_iye == null || (함수들.get(ìgbéwọlé_kókó_iye).wáyè_sí_ìgbéwọlé & 0x100) != 0) throw new Ìtumọ̀_àṣìṣe("ìgbéwọlé_kókó_iye ÀKÀNṢEFỌMÚLÀ_iye ìgúnrégé_iye àṣìṣe");
        List<String> ìlà = new ArrayList<>(); ìlà.add(".code32");
        for (ọ̀wọ́_détà détà : 클래스들.values()) {
            String ipò_iye = àmì("state",détà.Orúkọ), pàjùbà = àmì("init",détà.Orúkọ);
            Collections.addAll(ìlà,".bss",".balign 4",ipò_iye + ": .long 0",".text",pàjùbà + ":","cmpl $0, " + ipò_iye,"jne " + pàjùbà + "_done","movl $1, " + ipò_iye);
            ìlànà_Ìtọ́ka 초기화참조 = new ìlànà_Ìtọ́ka(détà.Orúkọ,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) ìlà.add("call " + àmì("method",초기화참조.부분들()));
            Collections.addAll(ìlà,"movl $2, " + ipò_iye,pàjùbà + "_done:","ret");
            for (ọmọ_ẹgbẹ́_détà àayè_wúnrẹ̀n_iye : détà.àayè_wúnrẹ̀n_iye) {
                byte[] aláìṣeéyípadà_iye = àayè_wúnrẹ̀n_iye.àwòmọ́_iye.get("ConstantValue"); String iye = aláìṣeéyípadà_iye == null ? "0" : 엑스상수(détà,new détà_akàwé(aláìṣeéyípadà_iye).두바이트());
                Collections.addAll(ìlà,".data",".balign 4",àmì("field",détà.Orúkọ,àayè_wúnrẹ̀n_iye.Orúkọ,àayè_wúnrẹ̀n_iye.서술) + ": .long " + iye);
            }
            for (ọmọ_ẹgbẹ́_détà ÀKÀNṢEFỌMÚLÀ_iye : détà.ÀKÀNṢEFỌMÚLÀ_iye) if (!ÀKÀNṢEFỌMÚLÀ_iye.Orúkọ.equals("<init>")) ìlà.add(엑스함수본문(new ìlànà_Ìtọ́ka(détà.Orúkọ,ÀKÀNṢEFỌMÚLÀ_iye.Orúkọ,ÀKÀNṢEFỌMÚLÀ_iye.서술),ÀKÀNṢEFỌMÚLÀ_iye,maṣíìnì_atọ́ka,àfojúsùn));
        }
        Collections.addAll(ìlà,".text",".globl java_entry","java_entry:","call " + àmì("init",ìgbéwọlé_kókó_iye.Oníǹkan_iye),"call " + àmì("method",ìgbéwọlé_kókó_iye.부분들()));
        if (ìgbéwọlé_kókó_iye.서술.equals("()V")) ìlà.add("xorl %eax, %eax"); ìlà.add("ret");
        for (String 지정 : 내보냄) {
            int àmí_ìdá_iye = 지정.indexOf('='); if (àmí_ìdá_iye < 1) throw new Ìtumọ̀_àṣìṣe("내보내기 지정 àṣìṣe");
            String 외부 = 지정.substring(0,àmí_ìdá_iye), ÀKÀNṢEFỌMÚLÀ_iye = 지정.substring(àmí_ìdá_iye + 1); int 나눔 = ÀKÀNṢEFỌMÚLÀ_iye.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Ìtumọ̀_àṣìṣe("내보내기 àmì àṣìṣe");
            String ọ̀wọ́_iye = ÀKÀNṢEFỌMÚLÀ_iye.substring(0,나눔).replace('.','/'), Orúkọ = ÀKÀNṢEFỌMÚLÀ_iye.substring(나눔 + 1); ìlànà_Ìtọ́ka ẹ̀yàn_iye = null;
            for (ìlànà_Ìtọ́ka Ìtọ́ka : 함수들.keySet()) if (Ìtọ́ka.Oníǹkan_iye.equals(ọ̀wọ́_iye) && Ìtọ́ka.Orúkọ.equals(Orúkọ)) { if (ẹ̀yàn_iye != null) throw new Ìtumọ̀_àṣìṣe("겹친 내보내기 àfojúsùn"); ẹ̀yàn_iye = Ìtọ́ka; }
            if (ẹ̀yàn_iye == null) throw new Ìtumọ̀_àṣìṣe("내보낼 함수가 없음");
            Collections.addAll(ìlà,".text",".globl " + 외부,외부 + ":","call " + àmì("init",ẹ̀yàn_iye.Oníǹkan_iye),"jmp " + àmì("method",ẹ̀yàn_iye.부분들()));
        }
        ìlà.add(".section .rodata");
        for (Map.Entry<String,String> ìgbéwọlé_iye : 문자열들.entrySet()) {
            Collections.addAll(ìlà,".balign 4",ìgbéwọlé_iye.getValue() + ":",".long " + ìgbéwọlé_iye.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char ìkẹ́kọ̀ọ́_iye : ìgbéwọlé_iye.getKey().toCharArray()) 단위들.add(Integer.toString(ìkẹ́kọ̀ọ́_iye)); if (!단위들.isEmpty()) ìlà.add(".long " + String.join(",",단위들));
        }
        ìlà.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",ìlà) + "\n";
    }
    static void ṣiṣẹ́_irinṣẹ́(List<String> Àṣẹ) throws Exception {
        if (new ProcessBuilder(Àṣẹ).inheritIO().start().waitFor() != 0) throw new Ìtumọ̀_àṣìṣe("ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun àṣìṣe: " + Àṣẹ.get(0));
    }
    static String détà_fọ́nrán(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String àfojúsùn, String ìgbéwọlé_kókó, List<String> 내보냄, Path 출력, Path ohun_àmúlò_iye) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), ọ̀wọ́_ọ̀nà = 임시.resolve("classes"); Files.createDirectory(ọ̀wọ́_ọ̀nà);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",ọ̀wọ́_ọ̀nà.toString(),"-sourcepath",ọ̀wọ́_ọ̀nà.toString(),"-d",ọ̀wọ́_ọ̀nà.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Ìtumọ̀_àṣìṣe("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Ìtumọ̀_àṣìṣe(".java 또는 .class만 àtìlẹ́yìn_iye");
            }
            if (원문수 > 0) ṣiṣẹ́_irinṣẹ́(자바명령);
            try (java.util.stream.Stream<Path> ọ̀nà_Àtòkọ = Files.walk(ọ̀wọ́_ọ̀nà)) { ọ̀nà_Àtòkọ.filter(ọ̀nà -> ọ̀nà.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,àfojúsùn.equals("user") ? "user" : "kernel",262144,ohun_àmúlò_iye);
            String 조립 = 변환.엑스조립본(ìgbéwọlé_kókó,내보냄,àfojúsùn); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = ohun_àmúlò_iye.getParent();
            ṣiṣẹ́_irinṣẹ́(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            ṣiṣẹ́_irinṣẹ́(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("àkókò_iṣẹ́_èdè_tówọ́pọ̀_àtìlẹ́yìn.s").toString()));
            List<String> Darapọ̀ = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (àfojúsùn.equals("kernel")) Darapọ̀.add("-r");
            else {
                ṣiṣẹ́_irinṣẹ́(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(àfojúsùn.equals("user") ? "bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò.s" : "리눅스시작.s").toString()));
                Collections.addAll(Darapọ̀,"-e","_start",임시.resolve("start.o").toString());
                if (àfojúsùn.equals("user")) Collections.addAll(Darapọ̀,"-T",도구위치.resolve("aṣàmúlò_ṣàsopọ̀_ètò_ìrísí.ld").toString());
            }
            Collections.addAll(Darapọ̀,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); ṣiṣẹ́_irinṣẹ́(Darapọ̀);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path gbéjáde_iye = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),gbéjáde_iye,StandardCopyOption.REPLACE_EXISTING); Files.move(gbéjáde_iye,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(gbéjáde_iye); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(àfojúsùn.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> àmì_détà = new ArrayList<>(), détà_orísun = new ArrayList<>();
            for (ìlànà_Ìtọ́ka Ìtọ́ka : 변환.함수들.keySet()) àmì_détà.add(détà_fọ́nrán(àmì("method",Ìtọ́ka.부분들())) + ":" + détà_fọ́nrán(Ìtọ́ka.Oníǹkan_iye + "." + Ìtọ́ka.Orúkọ + Ìtọ́ka.서술));
            for (Path 입력 : 입력들) {
                byte[] burú_fáìlì = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte iye : burú_fáìlì) SMS.append(String.format(Locale.ROOT,"%02x",iye & 255));
                détà_orísun.add(détà_fọ́nrán(입력.toAbsolutePath().toString()) + ":" + détà_fọ́nrán(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + détà_fọ́nrán(àfojúsùn) + ",\"entry\":" + détà_fọ́nrán(ìgbéwọlé_kókó) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",àmì_détà) + "},\"sources\":{" + String.join(",",détà_orísun) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> ọ̀nà_Àtòkọ = Files.walk(임시)) { for (Path ọ̀nà : (Iterable<Path>)ọ̀nà_Àtòkọ.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(ọ̀nà); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String ìgbéwọlé_kókó = null, àfojúsùn = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> ọ̀nà_Àtòkọ = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String iye = 인수[순번];
                switch (iye) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry ọ̀wọ́_iye.ÀKÀNṢEFỌMÚLÀ_iye -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export àmì=ọ̀wọ́_iye.ÀKÀNṢEFỌMÚLÀ_iye] 클래스파일 또는 Java원문"); return;
                    case "--entry": ìgbéwọlé_kókó = 인수[++순번]; break;
                    case "--profile": àfojúsùn = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (iye.startsWith("-")) throw new Ìtumọ̀_àṣìṣe("알 수 없는 옵션: " + iye); ọ̀nà_Àtòkọ.add(Paths.get(iye));
                }
            }
            if (ìgbéwọlé_kókó == null || 출력경로 == null || ọ̀nà_Àtòkọ.isEmpty()) throw new Ìtumọ̀_àṣìṣe("--entry, -o, ọ̀wọ́_iye 파일이 필요합니다");
            Path ohun_àmúlò_iye = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Ìtumọ̀_àṣìṣe("알 수 없는 ṣiṣẹ́_àṣẹ àfojúsùn");
                엑스번역(ọ̀nà_Àtòkọ,엑스대상,ìgbéwọlé_kókó,내보냄,출력경로,ohun_àmúlò_iye); return;
            }
            String orísun = new 기계어미리번역(ọ̀nà_Àtòkọ, àfojúsùn, 낱말수, ohun_àmúlò_iye).생성(ìgbéwọlé_kókó, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, orísun, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception àṣìṣe) { System.err.println("ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun àṣìṣe: " + àṣìṣe.getMessage()); System.exit(1); }
    }
}
