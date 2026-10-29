// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java uhlobo_inani 파일에서 독립 ARM64 커널용 C 원문을 만든다. singatha JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Ukuhumusha_iphutha extends RuntimeException {
        Ukuhumusha_iphutha(String 설명) { super(설명); }
    }
    static final class imininingwane_umfundi {
        final byte[] imininingwane;
        int 위치;
        imininingwane_umfundi(byte[] 입력자료) { imininingwane = 입력자료; }
        byte[] Funda(int ubude_inani) {
            if (ubude_inani < 0 || ubude_inani > imininingwane.length - 위치) throw new Ukuhumusha_iphutha("잘린 uhlobo_inani 또는 Umlayelo imininingwane");
            byte[] 결과 = Arrays.copyOfRange(imininingwane, 위치, 위치 + ubude_inani); 위치 += ubude_inani; return 결과;
        }
        int 한바이트() { if (위치 >= imininingwane.length) throw new Ukuhumusha_iphutha("잘린 Umlayelo imininingwane"); return imininingwane[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class ilungu_imininingwane {
        final int ungeno_okufakwayo;
        final String Igama, 서술;
        final Map<String, byte[]> isibaluli_inani;
        ilungu_imininingwane(int ungeno_inani, String igama_inani, String 서술값, Map<String, byte[]> isibaluli_imininingwane) {
            ungeno_okufakwayo = ungeno_inani; Igama = igama_inani; 서술 = 서술값; isibaluli_inani = isibaluli_imininingwane;
        }
    }
    static final class indlela_Ireferensi implements Comparable<indlela_Ireferensi> {
        final String umnikazi_inani, Igama, 서술;
        indlela_Ireferensi(String 소유값, String igama_inani, String 서술값) { umnikazi_inani = 소유값; Igama = igama_inani; 서술 = 서술값; }
        String[] 부분들() { return new String[]{umnikazi_inani, Igama, 서술}; }
        public int compareTo(indlela_Ireferensi untanga_inani) {
            int 비교값 = umnikazi_inani.compareTo(untanga_inani.umnikazi_inani);
            if (비교값 == 0) 비교값 = Igama.compareTo(untanga_inani.Igama);
            return 비교값 == 0 ? 서술.compareTo(untanga_inani.서술) : 비교값;
        }
        public boolean equals(Object untanga_inani) { return untanga_inani instanceof indlela_Ireferensi && compareTo((indlela_Ireferensi) untanga_inani) == 0; }
        public int hashCode() { return Objects.hash(umnikazi_inani, Igama, 서술); }
    }
    static final class uhlobo_imininingwane {
        final int[] 상수종류;
        final Object[] okungaguquki_imininingwane;
        final String Igama;
        final List<ilungu_imininingwane> inkundla_indawana_inani, umsebenzi_inani;
        uhlobo_imininingwane(Path Indlela_2) throws IOException {
            imininingwane_umfundi umfundi_inani = new imininingwane_umfundi(Files.readAllBytes(Indlela_2));
            if (umfundi_inani.네바이트() != 0xcafebabe) throw new Ukuhumusha_iphutha("Java uhlobo_inani 표식이 아님");
            umfundi_inani.Funda(4);
            int 개수 = umfundi_inani.두바이트(); 상수종류 = new int[개수]; okungaguquki_imininingwane = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = umfundi_inani.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int ubude_inani = umfundi_inani.두바이트();
                        byte[] uhlamvusimo_isikhumbulo_sesikhana = umfundi_inani.Funda(ubude_inani), 길이붙인자료 = new byte[ubude_inani + 2];
                        길이붙인자료[0] = (byte)(ubude_inani >> 8); 길이붙인자료[1] = (byte)ubude_inani;
                        System.arraycopy(uhlamvusimo_isikhumbulo_sesikhana, 0, 길이붙인자료, 2, ubude_inani);
                        okungaguquki_imininingwane[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: okungaguquki_imininingwane[순번] = umfundi_inani.네바이트(); break;
                    case 4: umfundi_inani.Funda(4); break;
                    case 5: case 6: umfundi_inani.Funda(8); 순번++; break;
                    case 7: case 8: case 16: okungaguquki_imininingwane[순번] = umfundi_inani.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        okungaguquki_imininingwane[순번] = new int[]{umfundi_inani.두바이트(), umfundi_inani.두바이트()}; break;
                    case 15: okungaguquki_imininingwane[순번] = new int[]{umfundi_inani.한바이트(), umfundi_inani.두바이트()}; break;
                    default: throw new Ukuhumusha_iphutha("지원하지 않는 okungaguquki_inani 종류: " + 종류);
                }
            }
            umfundi_inani.두바이트(); Igama = uhlobo_igama(umfundi_inani.두바이트());
            if (!uhlobo_igama(umfundi_inani.두바이트()).equals("java/lang/Object") || umfundi_inani.두바이트() != 0)
                throw new Ukuhumusha_iphutha(Igama + ": 상속 및 인터페이스 미지원");
            inkundla_indawana_inani = 멤버읽기(umfundi_inani); umsebenzi_inani = 멤버읽기(umfundi_inani); 속성읽기(umfundi_inani);
            if (umfundi_inani.위치 != umfundi_inani.imininingwane.length) throw new Ukuhumusha_iphutha("uhlobo_inani 뒤에 남은 imininingwane");
        }
        String 문자(int thola_inkomba) {
            if (thola_inkomba < 1 || thola_inkomba >= 상수종류.length || 상수종류[thola_inkomba] != 1) throw new Ukuhumusha_iphutha("문자 okungaguquki_inani thola_inkomba Iphutha");
            return (String) okungaguquki_imininingwane[thola_inkomba];
        }
        String uhlobo_igama(int thola_inkomba) {
            if (thola_inkomba < 1 || thola_inkomba >= 상수종류.length || 상수종류[thola_inkomba] != 7) throw new Ukuhumusha_iphutha("uhlobo_inani Ireferensi Iphutha");
            return 문자((Integer)okungaguquki_imininingwane[thola_inkomba]);
        }
        indlela_Ireferensi Ireferensi(int thola_inkomba) {
            if (thola_inkomba < 1 || thola_inkomba >= 상수종류.length || 상수종류[thola_inkomba] < 9 || 상수종류[thola_inkomba] > 11) throw new Ukuhumusha_iphutha("멤버 Ireferensi Iphutha");
            int[] okubili_inani = (int[])okungaguquki_imininingwane[thola_inkomba], igama_okubili = (int[])okungaguquki_imininingwane[okubili_inani[1]];
            return new indlela_Ireferensi(uhlobo_igama(okubili_inani[0]), 문자(igama_okubili[0]), 문자(igama_okubili[1]));
        }
        Map<String, byte[]> 속성읽기(imininingwane_umfundi umfundi_inani) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = umfundi_inani.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String isibaluli_igama = 문자(umfundi_inani.두바이트()); byte[] inani = umfundi_inani.Funda(umfundi_inani.네바이트());
                if (결과.put(isibaluli_igama, inani) != null) throw new Ukuhumusha_iphutha("겹친 isibaluli_inani: " + isibaluli_igama);
            }
            return 결과;
        }
        List<ilungu_imininingwane> 멤버읽기(imininingwane_umfundi umfundi_inani) {
            List<ilungu_imininingwane> 결과 = new ArrayList<>(); int 개수 = umfundi_inani.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int ungeno_okufakwayo = umfundi_inani.두바이트(); String indlela_okufakwayo_igama = 문자(umfundi_inani.두바이트()), 서술 = 문자(umfundi_inani.두바이트());
                결과.add(new ilungu_imininingwane(ungeno_okufakwayo, indlela_okufakwayo_igama, 서술, 속성읽기(umfundi_inani)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Ukuhumusha_iphutha("umsebenzi_inani 서술 Iphutha: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Ukuhumusha_iphutha("umsebenzi_inani 서술 Iphutha: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Ukuhumusha_iphutha("umsebenzi_inani 서술 Iphutha: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String okukhethiwe_inani = null;
            for (String misa_inani : 허용형식) if (서술.startsWith(misa_inani, 위치)) { okukhethiwe_inani = misa_inani; break; }
            if (okukhethiwe_inani == null) throw new Ukuhumusha_iphutha("지원하지 않는 uhlobo_lwemininingwane: " + 서술);
            결과.add(okukhethiwe_inani); 위치 += okukhethiwe_inani.length();
        }
        return 결과;
    }
    static String uphawu_ad6f1a96(String 종류, String... 부분들) {
        try {
            byte[] i_hash_ifayela = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Itekisi = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Itekisi.append(String.format(Locale.ROOT, "%02x", i_hash_ifayela[순번] & 255));
            return Itekisi.toString();
        } catch (Exception Iphutha) { throw new Ukuhumusha_iphutha(Iphutha.toString()); }
    }
    final Map<String, uhlobo_imininingwane> 클래스들 = new TreeMap<>();
    final Map<indlela_Ireferensi, ilungu_imininingwane> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, umshini_uhlobo;
    final int 동적기억낱말수;
    final Path insiza_umzila;
    기계어미리번역(List<Path> umzila_Uhlu, String impokophelo, int 낱말수, Path insiza_inani) throws IOException {
        if ((!impokophelo.equals("kernel") && !impokophelo.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Ukuhumusha_iphutha("yenza_umyalo impokophelo 또는 inkumbulo_inani 공간 Ubungako Iphutha");
        실행대상 = impokophelo; 동적기억낱말수 = 낱말수; insiza_umzila = insiza_inani;
        // 이 이름도 국가별 umthombo_isihlahla 생성 시 해당 언어로 옮긴다.
        umshini_uhlobo = impokophelo.equals("kernel") ? "보드" : "umsebenzisi";
        for (String umugqa : Files.readAllLines(insiza_inani.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = umugqa.split("\t", -1);
            if (부분들.length != 4) throw new Ukuhumusha_iphutha("umshini umsebenzi_inani imininingwane Iphutha");
            if (부분들[0].equals(impokophelo)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Indlela_2 : umzila_Uhlu) {
            uhlobo_imininingwane imininingwane = new uhlobo_imininingwane(Indlela_2);
            if (클래스들.put(imininingwane.Igama, imininingwane) != null) throw new Ukuhumusha_iphutha("중복 uhlobo_inani: " + imininingwane.Igama);
            for (ilungu_imininingwane inkundla_indawana_inani : imininingwane.inkundla_indawana_inani) {
                if ((inkundla_indawana_inani.ungeno_okufakwayo & 8) == 0 || 형식읽기(inkundla_indawana_inani.서술).equals(Collections.singletonList("V"))) throw new Ukuhumusha_iphutha("ngaguquki_inani 필드만 uxhaso_inani");
                if (필드들.put(new indlela_Ireferensi(imininingwane.Igama, inkundla_indawana_inani.Igama, inkundla_indawana_inani.서술), inkundla_indawana_inani) != null) throw new Ukuhumusha_iphutha("중복 inkundla_indawana_inani");
            }
            for (ilungu_imininingwane umsebenzi_inani : imininingwane.umsebenzi_inani) {
                if (umsebenzi_inani.Igama.equals("<init>")) continue;
                if ((umsebenzi_inani.ungeno_okufakwayo & 8) == 0 || (umsebenzi_inani.ungeno_okufakwayo & (0x20 | 0x400)) != 0) throw new Ukuhumusha_iphutha("ngaguquki_inani 비동기화 함수만 uxhaso_inani");
                new 함수형식(umsebenzi_inani.서술);
                if (함수들.put(new indlela_Ireferensi(imininingwane.Igama, umsebenzi_inani.Igama, umsebenzi_inani.서술), umsebenzi_inani) != null) throw new Ukuhumusha_iphutha("중복 umsebenzi_inani");
            }
        }
    }
    String uchunge_uphawu(String Itekisi) { return 문자열들.computeIfAbsent(Itekisi, inani -> "j_text_" + 문자열들.size()); }
    String okungaguquki_ukusho(uhlobo_imininingwane imininingwane, int thola_inkomba) {
        if (thola_inkomba < 1 || thola_inkomba >= imininingwane.상수종류.length) throw new Ukuhumusha_iphutha("okungaguquki_inani thola_inkomba isiqeshana Iphutha");
        if (imininingwane.상수종류[thola_inkomba] == 3) return "(word)(uint32_t)(" + imininingwane.okungaguquki_imininingwane[thola_inkomba] + ")";
        if (imininingwane.상수종류[thola_inkomba] == 8) return "(word)" + uchunge_uphawu(imininingwane.문자((Integer)imininingwane.okungaguquki_imininingwane[thola_inkomba]));
        throw new Ukuhumusha_iphutha("정수와 uchunge_inani 상수만 uxhaso_inani");
    }
    String 함수원형(indlela_Ireferensi Ireferensi) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Ireferensi.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + uphawu_ad6f1a96("method", Ireferensi.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void hlola_endaweni(int thola_inkomba, int 지역변수수) { if (thola_inkomba < 0 || thola_inkomba >= 지역변수수) throw new Ukuhumusha_iphutha("endaweni_umklamo 변수 thola_inkomba isiqeshana Iphutha"); }
    void 분기넣기(List<String> 출력, Set<Integer> igatsha_Uhlu, int 위치, int 이동량, String isimo) {
        int isikhumulo_inani = 위치 + 이동량; igatsha_Uhlu.add(isikhumulo_inani);
        출력.add((isimo == null ? "" : "if (" + isimo + ") ") + "goto b" + isikhumulo_inani + ";");
    }
    String 함수본문(indlela_Ireferensi umsebenzi_inani, ilungu_imininingwane imininingwane) {
        byte[] 본문자료 = imininingwane.isibaluli_inani.get("Code"); if (본문자료 == null) throw new Ukuhumusha_iphutha("umsebenzi_inani 몸체가 없음: " + umsebenzi_inani.Igama);
        imininingwane_umfundi umfundi_inani = new imininingwane_umfundi(본문자료); int 쌓임깊이 = umfundi_inani.두바이트(), 지역변수수 = umfundi_inani.두바이트();
        imininingwane_umfundi umyalo_imininingwane = new imininingwane_umfundi(umfundi_inani.Funda(umfundi_inani.네바이트()));
        if (umfundi_inani.두바이트() != 0) throw new Ukuhumusha_iphutha("try/catch/finally 미지원");
        함수형식 misa_inani = new 함수형식(umsebenzi_inani.서술); if (지역변수수 < misa_inani.인수.size()) throw new Ukuhumusha_iphutha("매개변수보다 적은 endaweni_umklamo 변수");
        uhlobo_imininingwane uhlobo_inani = 클래스들.get(umsebenzi_inani.umnikazi_inani);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(umsebenzi_inani) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < misa_inani.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), igatsha_Uhlu = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (umyalo_imininingwane.위치 < umyalo_imininingwane.imininingwane.length) {
            int 위치 = umyalo_imininingwane.위치, Umlayelo = umyalo_imininingwane.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (Umlayelo == 0) continue;
            if (Umlayelo == 1) 출력.add("PUSH(0);");
            else if (Umlayelo >= 2 && Umlayelo <= 8) 출력.add("PUSH((uint32_t)(" + (Umlayelo - 3) + "));");
            else if (Umlayelo == 16 || Umlayelo == 17) 출력.add("PUSH((uint32_t)(" + (Umlayelo == 16 ? umyalo_imininingwane.부호한바이트() : umyalo_imininingwane.부호두바이트()) + "));");
            else if (Umlayelo == 18 || Umlayelo == 19) 출력.add("PUSH(" + okungaguquki_ukusho(uhlobo_inani, Umlayelo == 18 ? umyalo_imininingwane.한바이트() : umyalo_imininingwane.두바이트()) + ");");
            else if (Umlayelo == 21 || Umlayelo == 25 || (Umlayelo >= 26 && Umlayelo <= 29) || (Umlayelo >= 42 && Umlayelo <= 45)) {
                int thola_inkomba = Umlayelo == 21 || Umlayelo == 25 ? umyalo_imininingwane.한바이트() : Umlayelo - (Umlayelo <= 29 ? 26 : 42);
                hlola_endaweni(thola_inkomba, 지역변수수); 출력.add("PUSH(l[" + thola_inkomba + "]);");
            } else if (Umlayelo == 54 || Umlayelo == 58 || (Umlayelo >= 59 && Umlayelo <= 62) || (Umlayelo >= 75 && Umlayelo <= 78)) {
                int thola_inkomba = Umlayelo == 54 || Umlayelo == 58 ? umyalo_imininingwane.한바이트() : Umlayelo - (Umlayelo <= 62 ? 59 : 75);
                hlola_endaweni(thola_inkomba, 지역변수수); 출력.add("l[" + thola_inkomba + "] = POP();");
            } else if (Umlayelo == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Umlayelo == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Umlayelo == 87 || Umlayelo == 88) 출력.add(Umlayelo == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Umlayelo >= 89 && Umlayelo <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ukuhleleka_Uhlu = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Umlayelo - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char inani : ukuhleleka_Uhlu[Umlayelo - 89].toCharArray()) 출력.add("PUSH(" + inani + ");");
            } else if (Umlayelo == 96 || Umlayelo == 100 || Umlayelo == 104 || Umlayelo == 126 || Umlayelo == 128 || Umlayelo == 130) {
                String umsebenzi_inani_c96707fb = Umlayelo == 96 ? "+" : Umlayelo == 100 ? "-" : Umlayelo == 104 ? "*" : Umlayelo == 126 ? "&" : Umlayelo == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + umsebenzi_inani_c96707fb + " (uint32_t)b);");
            } else if (Umlayelo == 108 || Umlayelo == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Umlayelo == 112 ? 1 : 0) + "));");
            else if (Umlayelo == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Umlayelo == 120 || Umlayelo == 122 || Umlayelo == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Umlayelo == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Umlayelo == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Umlayelo == 132) {
                int thola_inkomba = umyalo_imininingwane.한바이트(), 증가량 = umyalo_imininingwane.부호한바이트(); hlola_endaweni(thola_inkomba, 지역변수수);
                출력.add("l[" + thola_inkomba + "] = (uint32_t)l[" + thola_inkomba + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Umlayelo >= 145 && Umlayelo <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Umlayelo == 145 ? "int8_t" : Umlayelo == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Umlayelo >= 153 && Umlayelo <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, igatsha_Uhlu, 위치, umyalo_imininingwane.부호두바이트(), "(int32_t)a " + 비교들[Umlayelo - 153] + " 0");
            } else if (Umlayelo >= 159 && Umlayelo <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, igatsha_Uhlu, 위치, umyalo_imininingwane.부호두바이트(), Umlayelo >= 165 ? "a " + 비교들[Umlayelo - 159] + " b" : "(int32_t)a " + 비교들[Umlayelo - 159] + " (int32_t)b");
            } else if (Umlayelo == 167 || Umlayelo == 200) 분기넣기(출력, igatsha_Uhlu, 위치, Umlayelo == 167 ? umyalo_imininingwane.부호두바이트() : umyalo_imininingwane.네바이트(), null);
            else if (Umlayelo == 170 || Umlayelo == 171) {
                while (umyalo_imininingwane.위치 % 4 != 0) umyalo_imininingwane.한바이트();
                int inani_elimisiwe = umyalo_imininingwane.네바이트(); 출력.add("a = POP();");
                if (Umlayelo == 170) {
                    int 아래 = umyalo_imininingwane.네바이트(), 위 = umyalo_imininingwane.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (umyalo_imininingwane.imininingwane.length - umyalo_imininingwane.위치) / 4) throw new Ukuhumusha_iphutha("switch isiqeshana Iphutha");
                    for (long inani = 아래; inani <= 위; inani++) 분기넣기(출력, igatsha_Uhlu, 위치, umyalo_imininingwane.네바이트(), "(int32_t)a == (" + inani + ")");
                } else {
                    int 개수 = umyalo_imininingwane.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (umyalo_imininingwane.imininingwane.length - umyalo_imininingwane.위치) / 8) throw new Ukuhumusha_iphutha("switch Ubungako Iphutha");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int inani = umyalo_imininingwane.네바이트(); if (순번 > 0 && inani <= 앞값) throw new Ukuhumusha_iphutha("switch ukuhleleka_inani Iphutha"); 앞값 = inani;
                        분기넣기(출력, igatsha_Uhlu, 위치, umyalo_imininingwane.네바이트(), "(int32_t)a == (" + inani + ")");
                    }
                }
                분기넣기(출력, igatsha_Uhlu, 위치, inani_elimisiwe, null);
            } else if (Umlayelo == 172 || Umlayelo == 176 || Umlayelo == 177) 출력.add("return " + (Umlayelo == 177 ? "0" : "POP()") + ";");
            else if (Umlayelo == 178 || Umlayelo == 179) {
                indlela_Ireferensi Ireferensi = uhlobo_inani.Ireferensi(umyalo_imininingwane.두바이트()); if (!필드들.containsKey(Ireferensi)) throw new Ukuhumusha_iphutha("알 수 없는 inkundla_indawana_inani");
                출력.add(uphawu_ad6f1a96("init", Ireferensi.umnikazi_inani) + "();"); String inkundla_indawana_inani = uphawu_ad6f1a96("field", Ireferensi.부분들());
                출력.add(Umlayelo == 178 ? "PUSH(" + inkundla_indawana_inani + ");" : inkundla_indawana_inani + " = POP();");
            } else if (Umlayelo == 184) {
                indlela_Ireferensi Ireferensi = uhlobo_inani.Ireferensi(umyalo_imininingwane.두바이트()); if (!함수들.containsKey(Ireferensi)) throw new Ukuhumusha_iphutha("알 수 없는 umsebenzi_inani");
                함수형식 호출형식 = new 함수형식(Ireferensi.서술); int 개수 = 호출형식.인수.size();
                출력.add(uphawu_ad6f1a96("init", Ireferensi.umnikazi_inani) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + uphawu_ad6f1a96("method", Ireferensi.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Umlayelo == 182) {
                indlela_Ireferensi Ireferensi = uhlobo_inani.Ireferensi(umyalo_imininingwane.두바이트());
                if (Ireferensi.equals(new indlela_Ireferensi("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Ireferensi.equals(new indlela_Ireferensi("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Ukuhumusha_iphutha("가상 umsebenzi_inani 호출 미지원");
            } else if (Umlayelo == 188) {
                if (umyalo_imininingwane.한바이트() != 10) throw new Ukuhumusha_iphutha("new int[]만 uxhaso_inani"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Umlayelo == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Umlayelo == 196) {
                int iselulo_inani = umyalo_imininingwane.한바이트(), thola_inkomba = umyalo_imininingwane.두바이트(); hlola_endaweni(thola_inkomba, 지역변수수);
                if (iselulo_inani == 21 || iselulo_inani == 25) 출력.add("PUSH(l[" + thola_inkomba + "]);");
                else if (iselulo_inani == 54 || iselulo_inani == 58) 출력.add("l[" + thola_inkomba + "] = POP();");
                else if (iselulo_inani == 132) 출력.add("l[" + thola_inkomba + "] = (uint32_t)l[" + thola_inkomba + "] + (uint32_t)(" + umyalo_imininingwane.부호두바이트() + ");");
                else throw new Ukuhumusha_iphutha("미지원 wide Umlayelo");
            } else if (Umlayelo == 198 || Umlayelo == 199) {
                출력.add("a = POP();"); 분기넣기(출력, igatsha_Uhlu, 위치, umyalo_imininingwane.부호두바이트(), "a " + (Umlayelo == 198 ? "==" : "!=") + " 0");
            } else throw new Ukuhumusha_iphutha(umsebenzi_inani.umnikazi_inani + "." + umsebenzi_inani.Igama + ", ibhayithi_inani " + 위치 + ": 미지원 Umlayelo " + Umlayelo);
        }
        if (!경계들.containsAll(igatsha_Uhlu)) throw new Ukuhumusha_iphutha("Umlayelo 경계가 아닌 곳으로 igatsha");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String thekelisa_indlela(String xhuma_uphawu, String impokophelo, boolean 진입점여부) {
        int 자리 = impokophelo.lastIndexOf('.'); if (자리 < 0 || !xhuma_uphawu.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Ukuhumusha_iphutha("내보내기 yabela_inani Iphutha");
        String umnikazi_inani = impokophelo.substring(0, 자리).replace('.', '/'), Igama = impokophelo.substring(자리 + 1); indlela_Ireferensi okukhethiwe_inani = null;
        for (indlela_Ireferensi Ireferensi : 함수들.keySet()) if (Ireferensi.umnikazi_inani.equals(umnikazi_inani) && Ireferensi.Igama.equals(Igama)) {
            if (okukhethiwe_inani != null) throw new Ukuhumusha_iphutha("겹친 내보내기 impokophelo"); okukhethiwe_inani = Ireferensi;
        }
        if (okukhethiwe_inani == null || (함수들.get(okukhethiwe_inani).ungeno_okufakwayo & 0x100) != 0) throw new Ukuhumusha_iphutha("내보낼 함수가 없음 또는 native umsebenzi_inani");
        함수형식 misa_inani = new 함수형식(okukhethiwe_inani.서술);
        if ((진입점여부 && !misa_inani.인수.isEmpty()) || !Arrays.asList("V", "I").contains(misa_inani.반환)) throw new Ukuhumusha_iphutha("okufakwayo_iphoyinti_inani 또는 C 경계 misa_inani Iphutha");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < misa_inani.인수.size(); 순번++) {
            if (!misa_inani.인수.get(순번).equals("I")) throw new Ukuhumusha_iphutha("C 경계는 int 인수만 uxhaso_inani");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (misa_inani.반환.equals("V") ? "void " : "int32_t ") + xhuma_uphawu + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + uphawu_ad6f1a96("init", okukhethiwe_inani.umnikazi_inani) + "(); " + (misa_inani.반환.equals("V") ? "" : "return (int32_t)") + uphawu_ad6f1a96("method", okukhethiwe_inani.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String okufakwayo_iphoyinti, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<indlela_Ireferensi, ilungu_imininingwane> okufakwayo_inani : 함수들.entrySet()) {
            indlela_Ireferensi Ireferensi = okufakwayo_inani.getKey(); ilungu_imininingwane imininingwane = okufakwayo_inani.getValue(); 선언들.add(함수원형(Ireferensi) + ";");
            if ((imininingwane.ungeno_okufakwayo & 0x100) != 0) {
                String Xhumanisa = 기계함수들.get(Ireferensi.Igama + Ireferensi.서술);
                if (!Ireferensi.umnikazi_inani.equals(umshini_uhlobo) || Xhumanisa == null) throw new Ukuhumusha_iphutha("허용되지 않은 native umsebenzi_inani: " + Ireferensi.Igama);
                int 개수 = new 함수형식(Ireferensi.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Xhumanisa + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Ireferensi) + " { return " + Xhumanisa + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Ireferensi, imininingwane));
        }
        for (Map.Entry<indlela_Ireferensi, ilungu_imininingwane> okufakwayo_inani : 필드들.entrySet()) {
            indlela_Ireferensi Ireferensi = okufakwayo_inani.getKey(); byte[] okungaguquki_inani = okufakwayo_inani.getValue().isibaluli_inani.get("ConstantValue");
            String inani = okungaguquki_inani == null ? "0" : okungaguquki_ukusho(클래스들.get(Ireferensi.umnikazi_inani), new imininingwane_umfundi(okungaguquki_inani).두바이트());
            필드선언들.add("static word " + uphawu_ad6f1a96("field", Ireferensi.부분들()) + " = " + inani + ";");
        }
        for (String Igama : 클래스들.keySet()) {
            String qalisa = uphawu_ad6f1a96("init", Igama), isimo_inani = uphawu_ad6f1a96("state", Igama);
            선언들.add("static void " + qalisa + "(void);"); 필드선언들.add("static unsigned " + isimo_inani + ";");
            indlela_Ireferensi Ireferensi = new indlela_Ireferensi(Igama, "<clinit>", "()V");
            몸체들.add("static void " + qalisa + "(void) { if(" + isimo_inani + ") return; " + isimo_inani + " = 1; " + (함수들.containsKey(Ireferensi) ? uphawu_ad6f1a96("method", Ireferensi.부분들()) + "(); " : "") + isimo_inani + " = 2; }");
        }
        몸체들.add(thekelisa_indlela("java_entry", okufakwayo_iphoyinti, true)); Set<String> 공개이름 = new HashSet<>();
        for (String yabela_inani : 내보내기목록) {
            int 자리 = yabela_inani.indexOf('='); if (자리 < 1) throw new Ukuhumusha_iphutha("내보내기 yabela_inani Iphutha");
            String Igama = yabela_inani.substring(0, 자리); 공개이름.add(Igama); 몸체들.add(thekelisa_indlela(Igama, yabela_inani.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> okufakwayo_inani : 문자열들.entrySet()) {
            String Itekisi = okufakwayo_inani.getKey(); StringBuilder AMALUNGU_AFANAYO_inani = new StringBuilder("static const word " + okufakwayo_inani.getValue() + "[] = {" + Itekisi.length());
            for (int 순번 = 0; 순번 < Itekisi.length(); 순번++) AMALUNGU_AFANAYO_inani.append(", ").append((int)Itekisi.charAt(순번));
            문자열선언들.add(AMALUNGU_AFANAYO_inani.append("};").toString());
        }
        String uxhaso_inani = Files.readString(insiza_umzila.resolve("isikhathi_sokusebenza_solimi_esivamile_uxhaso.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(uxhaso_inani + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String umthombo, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> igama_ithebula = new HashMap<>();
        for (String umugqa : Files.readAllLines(insiza_umzila.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] okubili_inani = umugqa.split("\t"); igama_ithebula.put(okubili_inani[0], okubili_inani[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(umthombo); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Igama = 찾개.group(), 새이름 = Igama;
            if (!Igama.startsWith("//") && !Igama.startsWith("/*") && !Igama.startsWith("\"") && !Igama.startsWith("'") && !공개이름.contains(Igama)) {
                새이름 = igama_ithebula.getOrDefault(Igama, Igama);
                if (Igama.matches("a[0-9]+")) 새이름 = "인수" + Igama.substring(1);
                if (Igama.matches("b[0-9]+")) 새이름 = "igatsha" + Igama.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char uhlamvusimo_inani : 새이름.toCharArray()) 표기.append(uhlamvusimo_inani < 128 ? Character.toString(uhlamvusimo_inani) : String.format(Locale.ROOT, "\\u%04x", (int)uhlamvusimo_inani));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(indlela_Ireferensi umsebenzi_inani, ilungu_imininingwane imininingwane, Map<String,String> umshini_ithebula, String impokophelo) {
        String 표식 = uphawu_ad6f1a96("method", umsebenzi_inani.부분들());
        List<String> umugqa = new ArrayList<>();
        if ((imininingwane.ungeno_okufakwayo & 0x100) != 0) {
            String Xhumanisa = umshini_ithebula.get(umsebenzi_inani.Igama + umsebenzi_inani.서술);
            if (!umsebenzi_inani.umnikazi_inani.equals(impokophelo.equals("kernel") ? "idivayisi_inani" : "umsebenzisi") || Xhumanisa == null) throw new Ukuhumusha_iphutha("허용되지 않은 native umsebenzi_inani");
            return ".text\n" + 표식 + ":\njmp " + Xhumanisa;
        }
        byte[] umzimba_wombhalo = imininingwane.isibaluli_inani.get("Code"); if (umzimba_wombhalo == null) throw new Ukuhumusha_iphutha("umsebenzi_inani 몸체가 없음");
        imininingwane_umfundi umfundi_inani = new imininingwane_umfundi(umzimba_wombhalo); umfundi_inani.두바이트(); int 지역수 = umfundi_inani.두바이트();
        imininingwane_umfundi umyalo_imininingwane = new imininingwane_umfundi(umfundi_inani.Funda(umfundi_inani.네바이트()));
        if (umfundi_inani.두바이트() != 0) throw new Ukuhumusha_iphutha("try/catch/finally 미지원");
        함수형식 misa_inani = new 함수형식(umsebenzi_inani.서술); if (지역수 < misa_inani.인수.size()) throw new Ukuhumusha_iphutha("매개변수보다 적은 endaweni_umklamo 변수");
        Collections.addAll(umugqa,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < misa_inani.인수.size(); 순번++) Collections.addAll(umugqa,"movl " + (8 + 4 * (misa_inani.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        uhlobo_imininingwane uhlobo_inani = 클래스들.get(umsebenzi_inani.umnikazi_inani); Set<Integer> 경계들 = new HashSet<>(), igatsha_Uhlu = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (umyalo_imininingwane.위치 < umyalo_imininingwane.imininingwane.length) {
            int 위치 = umyalo_imininingwane.위치, Umlayelo = umyalo_imininingwane.한바이트(); String 자리 = 표식 + "_b" + 위치;
            umugqa.add(자리 + ":"); 경계들.add(위치);
            if (Umlayelo == 0) umugqa.add("nop");
            else if (Umlayelo == 1) umugqa.add("pushl $0");
            else if (Umlayelo >= 2 && Umlayelo <= 8) umugqa.add("pushl $" + (Umlayelo - 3));
            else if (Umlayelo == 16 || Umlayelo == 17) umugqa.add("pushl $" + (Umlayelo == 16 ? umyalo_imininingwane.부호한바이트() : umyalo_imininingwane.부호두바이트()));
            else if (Umlayelo == 18 || Umlayelo == 19) {
                int thola_inkomba = Umlayelo == 18 ? umyalo_imininingwane.한바이트() : umyalo_imininingwane.두바이트();
                umugqa.add("pushl $" + 엑스상수(uhlobo_inani,thola_inkomba));
            } else if (Umlayelo == 21 || Umlayelo == 25 || (Umlayelo >= 26 && Umlayelo <= 29) || (Umlayelo >= 42 && Umlayelo <= 45) || Umlayelo == 54 || Umlayelo == 58 || (Umlayelo >= 59 && Umlayelo <= 62) || (Umlayelo >= 75 && Umlayelo <= 78)) {
                boolean 읽음 = Umlayelo < 54; int thola_inkomba = Umlayelo == 21 || Umlayelo == 25 || Umlayelo == 54 || Umlayelo == 58 ? umyalo_imininingwane.한바이트() : Umlayelo - (Umlayelo <= 29 ? 26 : Umlayelo <= 45 ? 42 : Umlayelo <= 62 ? 59 : 75);
                hlola_endaweni(thola_inkomba,지역수); umugqa.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (thola_inkomba + 1)) + "(%ebp)");
            } else if (Umlayelo == 46) Collections.addAll(umugqa,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Umlayelo == 79) Collections.addAll(umugqa,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Umlayelo == 87 || Umlayelo == 88) umugqa.add("addl $" + (Umlayelo == 87 ? 4 : 8) + ", %esp");
            else if (Umlayelo >= 89 && Umlayelo <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ukuhleleka_Uhlu = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Umlayelo - 89]; 순번++) umugqa.add("popl " + 저장기들[순번]);
                for (int 순번 : ukuhleleka_Uhlu[Umlayelo - 89]) umugqa.add("pushl " + 저장기들[순번]);
            } else if (Umlayelo == 96 || Umlayelo == 100 || Umlayelo == 104 || Umlayelo == 126 || Umlayelo == 128 || Umlayelo == 130) {
                String umsebenzi_inani_c96707fb = Umlayelo == 96 ? "addl" : Umlayelo == 100 ? "subl" : Umlayelo == 104 ? "imull" : Umlayelo == 126 ? "andl" : Umlayelo == 128 ? "orl" : "xorl";
                Collections.addAll(umugqa,"popl %ecx","popl %eax",umsebenzi_inani_c96707fb + " %ecx, %eax","pushl %eax");
            } else if (Umlayelo == 108 || Umlayelo == 112) Collections.addAll(umugqa,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Umlayelo == 108 ? "%eax" : "%edx"));
            else if (Umlayelo == 116) umugqa.add("negl (%esp)");
            else if (Umlayelo == 120 || Umlayelo == 122 || Umlayelo == 124) Collections.addAll(umugqa,"popl %ecx","popl %eax",(Umlayelo == 120 ? "sall" : Umlayelo == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Umlayelo == 132) {
                int thola_inkomba = umyalo_imininingwane.한바이트(), 증가 = umyalo_imininingwane.부호한바이트(); hlola_endaweni(thola_inkomba,지역수); umugqa.add("addl $" + 증가 + ", -" + (4 * (thola_inkomba + 1)) + "(%ebp)");
            } else if (Umlayelo >= 145 && Umlayelo <= 147) Collections.addAll(umugqa,"popl %eax",Umlayelo == 145 ? "movsbl %al, %eax" : Umlayelo == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Umlayelo >= 153 && Umlayelo <= 166) {
                if (Umlayelo <= 158) Collections.addAll(umugqa,"popl %eax","testl %eax, %eax");
                else Collections.addAll(umugqa,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int isikhumulo_inani = 위치 + umyalo_imininingwane.부호두바이트(); igatsha_Uhlu.add(isikhumulo_inani); umugqa.add(비교들[Umlayelo - (Umlayelo <= 158 ? 153 : 159)] + " " + 표식 + "_b" + isikhumulo_inani);
            } else if (Umlayelo == 167 || Umlayelo == 200) {
                int isikhumulo_inani = 위치 + (Umlayelo == 167 ? umyalo_imininingwane.부호두바이트() : umyalo_imininingwane.네바이트()); igatsha_Uhlu.add(isikhumulo_inani); umugqa.add("jmp " + 표식 + "_b" + isikhumulo_inani);
            } else if (Umlayelo == 170 || Umlayelo == 171) {
                while (umyalo_imininingwane.위치 % 4 != 0) umyalo_imininingwane.한바이트();
                int inani_elimisiwe = 위치 + umyalo_imininingwane.네바이트(); igatsha_Uhlu.add(inani_elimisiwe); umugqa.add("popl %eax");
                int 개수, 아래 = 0;
                if (Umlayelo == 170) { 아래 = umyalo_imininingwane.네바이트(); int 위 = umyalo_imininingwane.네바이트(); long ubude_inani = (long)위 - 아래 + 1; if (ubude_inani < 1 || ubude_inani > (umyalo_imininingwane.imininingwane.length - umyalo_imininingwane.위치) / 4) throw new Ukuhumusha_iphutha("switch isiqeshana Iphutha"); 개수 = (int)ubude_inani; }
                else { 개수 = umyalo_imininingwane.네바이트(); if (개수 < 0 || 개수 > (umyalo_imininingwane.imininingwane.length - umyalo_imininingwane.위치) / 8) throw new Ukuhumusha_iphutha("switch Ubungako Iphutha"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int inani = Umlayelo == 170 ? 아래 + 순번 : umyalo_imininingwane.네바이트(), isikhumulo_inani = 위치 + umyalo_imininingwane.네바이트(); igatsha_Uhlu.add(isikhumulo_inani);
                    Collections.addAll(umugqa,"cmpl $" + inani + ", %eax","je " + 표식 + "_b" + isikhumulo_inani);
                }
                umugqa.add("jmp " + 표식 + "_b" + inani_elimisiwe);
            } else if (Umlayelo == 172 || Umlayelo == 176 || Umlayelo == 177) {
                if (Umlayelo != 177) umugqa.add("popl %eax"); Collections.addAll(umugqa,"leave","ret");
            } else if (Umlayelo == 178 || Umlayelo == 179) {
                indlela_Ireferensi Ireferensi = uhlobo_inani.Ireferensi(umyalo_imininingwane.두바이트()); if (!필드들.containsKey(Ireferensi)) throw new Ukuhumusha_iphutha("알 수 없는 inkundla_indawana_inani");
                Collections.addAll(umugqa,"call " + uphawu_ad6f1a96("init",Ireferensi.umnikazi_inani),(Umlayelo == 178 ? "pushl " : "popl ") + uphawu_ad6f1a96("field",Ireferensi.부분들()));
            } else if (Umlayelo == 184) {
                indlela_Ireferensi Ireferensi = uhlobo_inani.Ireferensi(umyalo_imininingwane.두바이트()); if (!함수들.containsKey(Ireferensi)) throw new Ukuhumusha_iphutha("알 수 없는 umsebenzi_inani");
                함수형식 호출형식 = new 함수형식(Ireferensi.서술); Collections.addAll(umugqa,"call " + uphawu_ad6f1a96("init",Ireferensi.umnikazi_inani),"call " + uphawu_ad6f1a96("method",Ireferensi.부분들()));
                if (!호출형식.인수.isEmpty()) umugqa.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) umugqa.add("pushl %eax");
            } else if (Umlayelo == 182) {
                indlela_Ireferensi Ireferensi = uhlobo_inani.Ireferensi(umyalo_imininingwane.두바이트());
                if (Ireferensi.equals(new indlela_Ireferensi("java/lang/String","length","()I"))) Collections.addAll(umugqa,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Ireferensi.equals(new indlela_Ireferensi("java/lang/String","charAt","(I)C"))) Collections.addAll(umugqa,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Ukuhumusha_iphutha("가상 umsebenzi_inani 호출 미지원");
            } else if (Umlayelo == 188) {
                if (umyalo_imininingwane.한바이트() != 10) throw new Ukuhumusha_iphutha("new int[]만 uxhaso_inani"); Collections.addAll(umugqa,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Umlayelo == 190) Collections.addAll(umugqa,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Umlayelo == 196) {
                int iselulo_inani = umyalo_imininingwane.한바이트(), thola_inkomba = umyalo_imininingwane.두바이트(); hlola_endaweni(thola_inkomba,지역수);
                if (iselulo_inani == 21 || iselulo_inani == 25 || iselulo_inani == 54 || iselulo_inani == 58) umugqa.add((iselulo_inani <= 25 ? "pushl " : "popl ") + "-" + 4 * (thola_inkomba + 1) + "(%ebp)");
                else if (iselulo_inani == 132) umugqa.add("addl $" + umyalo_imininingwane.부호두바이트() + ", -" + 4 * (thola_inkomba + 1) + "(%ebp)");
                else throw new Ukuhumusha_iphutha("wide Umlayelo 미지원");
            } else if (Umlayelo == 198 || Umlayelo == 199) {
                int isikhumulo_inani = 위치 + umyalo_imininingwane.부호두바이트(); igatsha_Uhlu.add(isikhumulo_inani); Collections.addAll(umugqa,"popl %eax","testl %eax, %eax",(Umlayelo == 198 ? "je " : "jne ") + 표식 + "_b" + isikhumulo_inani);
            } else throw new Ukuhumusha_iphutha("미지원 Umlayelo: " + Umlayelo);
        }
        if (!경계들.containsAll(igatsha_Uhlu)) throw new Ukuhumusha_iphutha("Umlayelo 경계가 아닌 곳으로 igatsha");
        umugqa.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",umugqa);
    }
    String 엑스상수(uhlobo_imininingwane imininingwane, int thola_inkomba) {
        if (imininingwane.상수종류[thola_inkomba] == 3) return imininingwane.okungaguquki_imininingwane[thola_inkomba].toString();
        if (imininingwane.상수종류[thola_inkomba] == 8) return uchunge_uphawu(imininingwane.문자((Integer)imininingwane.okungaguquki_imininingwane[thola_inkomba]));
        throw new Ukuhumusha_iphutha("정수와 uchunge_inani 상수만 uxhaso_inani");
    }
    String 엑스조립본(String okufakwayo_iphoyinti, List<String> 내보냄, String impokophelo) throws IOException {
        Map<String,String> umshini_ithebula = new HashMap<>();
        for (String umugqa : Files.readAllLines(insiza_umzila.resolve("엑스기계함수.tsv"))) { String[] okubili_inani = umugqa.split("\t"); if (okubili_inani[0].equals(impokophelo)) umshini_ithebula.put(okubili_inani[1] + okubili_inani[2],okubili_inani[3]); }
        int 자리 = okufakwayo_iphoyinti.lastIndexOf('.'); if (자리 < 0) throw new Ukuhumusha_iphutha("okufakwayo_iphoyinti yabela_inani Iphutha");
        String umnikazi_inani = okufakwayo_iphoyinti.substring(0,자리).replace('.','/'), indlela_okufakwayo_igama = okufakwayo_iphoyinti.substring(자리 + 1); indlela_Ireferensi okufakwayo_iphoyinti_inani = null;
        for (String 서술 : Arrays.asList("()I","()V")) { indlela_Ireferensi Ireferensi = new indlela_Ireferensi(umnikazi_inani,indlela_okufakwayo_igama,서술); if (함수들.containsKey(Ireferensi)) { if (okufakwayo_iphoyinti_inani != null) throw new Ukuhumusha_iphutha("겹친 okufakwayo_iphoyinti"); okufakwayo_iphoyinti_inani = Ireferensi; } }
        if (okufakwayo_iphoyinti_inani == null || (함수들.get(okufakwayo_iphoyinti_inani).ungeno_okufakwayo & 0x100) != 0) throw new Ukuhumusha_iphutha("okufakwayo_iphoyinti_inani umsebenzi_inani misa_inani Iphutha");
        List<String> umugqa = new ArrayList<>(); umugqa.add(".code32");
        for (uhlobo_imininingwane imininingwane : 클래스들.values()) {
            String isimo_inani = uphawu_ad6f1a96("state",imininingwane.Igama), qalisa = uphawu_ad6f1a96("init",imininingwane.Igama);
            Collections.addAll(umugqa,".bss",".balign 4",isimo_inani + ": .long 0",".text",qalisa + ":","cmpl $0, " + isimo_inani,"jne " + qalisa + "_done","movl $1, " + isimo_inani);
            indlela_Ireferensi 초기화참조 = new indlela_Ireferensi(imininingwane.Igama,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) umugqa.add("call " + uphawu_ad6f1a96("method",초기화참조.부분들()));
            Collections.addAll(umugqa,"movl $2, " + isimo_inani,qalisa + "_done:","ret");
            for (ilungu_imininingwane inkundla_indawana_inani : imininingwane.inkundla_indawana_inani) {
                byte[] okungaguquki_inani = inkundla_indawana_inani.isibaluli_inani.get("ConstantValue"); String inani = okungaguquki_inani == null ? "0" : 엑스상수(imininingwane,new imininingwane_umfundi(okungaguquki_inani).두바이트());
                Collections.addAll(umugqa,".data",".balign 4",uphawu_ad6f1a96("field",imininingwane.Igama,inkundla_indawana_inani.Igama,inkundla_indawana_inani.서술) + ": .long " + inani);
            }
            for (ilungu_imininingwane umsebenzi_inani : imininingwane.umsebenzi_inani) if (!umsebenzi_inani.Igama.equals("<init>")) umugqa.add(엑스함수본문(new indlela_Ireferensi(imininingwane.Igama,umsebenzi_inani.Igama,umsebenzi_inani.서술),umsebenzi_inani,umshini_ithebula,impokophelo));
        }
        Collections.addAll(umugqa,".text",".globl java_entry","java_entry:","call " + uphawu_ad6f1a96("init",okufakwayo_iphoyinti_inani.umnikazi_inani),"call " + uphawu_ad6f1a96("method",okufakwayo_iphoyinti_inani.부분들()));
        if (okufakwayo_iphoyinti_inani.서술.equals("()V")) umugqa.add("xorl %eax, %eax"); umugqa.add("ret");
        for (String yabela_inani : 내보냄) {
            int okunqandayo_inani = yabela_inani.indexOf('='); if (okunqandayo_inani < 1) throw new Ukuhumusha_iphutha("내보내기 yabela_inani Iphutha");
            String 외부 = yabela_inani.substring(0,okunqandayo_inani), umsebenzi_inani = yabela_inani.substring(okunqandayo_inani + 1); int 나눔 = umsebenzi_inani.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Ukuhumusha_iphutha("내보내기 uphawu_ad6f1a96 Iphutha");
            String uhlobo_inani = umsebenzi_inani.substring(0,나눔).replace('.','/'), Igama = umsebenzi_inani.substring(나눔 + 1); indlela_Ireferensi okukhethiwe_inani = null;
            for (indlela_Ireferensi Ireferensi : 함수들.keySet()) if (Ireferensi.umnikazi_inani.equals(uhlobo_inani) && Ireferensi.Igama.equals(Igama)) { if (okukhethiwe_inani != null) throw new Ukuhumusha_iphutha("겹친 내보내기 impokophelo"); okukhethiwe_inani = Ireferensi; }
            if (okukhethiwe_inani == null) throw new Ukuhumusha_iphutha("내보낼 함수가 없음");
            Collections.addAll(umugqa,".text",".globl " + 외부,외부 + ":","call " + uphawu_ad6f1a96("init",okukhethiwe_inani.umnikazi_inani),"jmp " + uphawu_ad6f1a96("method",okukhethiwe_inani.부분들()));
        }
        umugqa.add(".section .rodata");
        for (Map.Entry<String,String> okufakwayo_inani : 문자열들.entrySet()) {
            Collections.addAll(umugqa,".balign 4",okufakwayo_inani.getValue() + ":",".long " + okufakwayo_inani.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char isifundo_inani : okufakwayo_inani.getKey().toCharArray()) 단위들.add(Integer.toString(isifundo_inani)); if (!단위들.isEmpty()) umugqa.add(".long " + String.join(",",단위들));
        }
        umugqa.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",umugqa) + "\n";
    }
    static void yenza_ithuluzi(List<String> Umlayelo) throws Exception {
        if (new ProcessBuilder(Umlayelo).inheritIO().start().waitFor() != 0) throw new Ukuhumusha_iphutha("akha_umthombo Iphutha: " + Umlayelo.get(0));
    }
    static String imininingwane_uchunge(String Itekisi) { return "\"" + Itekisi.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String impokophelo, String okufakwayo_iphoyinti, List<String> 내보냄, Path 출력, Path insiza_inani) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), uhlobo_umzila = 임시.resolve("classes"); Files.createDirectory(uhlobo_umzila);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",uhlobo_umzila.toString(),"-sourcepath",uhlobo_umzila.toString(),"-d",uhlobo_umzila.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Ukuhumusha_iphutha("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Ukuhumusha_iphutha(".java 또는 .class만 uxhaso_inani");
            }
            if (원문수 > 0) yenza_ithuluzi(자바명령);
            try (java.util.stream.Stream<Path> umzila_Uhlu = Files.walk(uhlobo_umzila)) { umzila_Uhlu.filter(Indlela_2 -> Indlela_2.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,impokophelo.equals("user") ? "user" : "kernel",262144,insiza_inani);
            String 조립 = 변환.엑스조립본(okufakwayo_iphoyinti,내보냄,impokophelo); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = insiza_inani.getParent();
            yenza_ithuluzi(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            yenza_ithuluzi(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("isikhathi_sokusebenza_solimi_esivamile_uxhaso.s").toString()));
            List<String> Xhumanisa = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (impokophelo.equals("kernel")) Xhumanisa.add("-r");
            else {
                yenza_ithuluzi(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(impokophelo.equals("user") ? "qala_umsebenzisi_i_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Xhumanisa,"-e","_start",임시.resolve("start.o").toString());
                if (impokophelo.equals("user")) Collections.addAll(Xhumanisa,"-T",도구위치.resolve("umsebenzisi_xhuma_I_layout.ld").toString());
            }
            Collections.addAll(Xhumanisa,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); yenza_ithuluzi(Xhumanisa);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path shicilela_inani = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),shicilela_inani,StandardCopyOption.REPLACE_EXISTING); Files.move(shicilela_inani,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(shicilela_inani); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(impokophelo.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> uphawu_imininingwane = new ArrayList<>(), imininingwane_yomthombo = new ArrayList<>();
            for (indlela_Ireferensi Ireferensi : 변환.함수들.keySet()) uphawu_imininingwane.add(imininingwane_uchunge(uphawu_ad6f1a96("method",Ireferensi.부분들())) + ":" + imininingwane_uchunge(Ireferensi.umnikazi_inani + "." + Ireferensi.Igama + Ireferensi.서술));
            for (Path 입력 : 입력들) {
                byte[] i_hash_ifayela = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Itekisi = new StringBuilder(); for (byte inani : i_hash_ifayela) Itekisi.append(String.format(Locale.ROOT,"%02x",inani & 255));
                imininingwane_yomthombo.add(imininingwane_uchunge(입력.toAbsolutePath().toString()) + ":" + imininingwane_uchunge(Itekisi.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + imininingwane_uchunge(impokophelo) + ",\"entry\":" + imininingwane_uchunge(okufakwayo_iphoyinti) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",uphawu_imininingwane) + "},\"sources\":{" + String.join(",",imininingwane_yomthombo) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> umzila_Uhlu = Files.walk(임시)) { for (Path Indlela_2 : (Iterable<Path>)umzila_Uhlu.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Indlela_2); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String okufakwayo_iphoyinti = null, impokophelo = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> umzila_Uhlu = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String inani = 인수[순번];
                switch (inani) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry uhlobo_inani.umsebenzi_inani -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export uphawu_ad6f1a96=uhlobo_inani.umsebenzi_inani] 클래스파일 또는 Java원문"); return;
                    case "--entry": okufakwayo_iphoyinti = 인수[++순번]; break;
                    case "--profile": impokophelo = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (inani.startsWith("-")) throw new Ukuhumusha_iphutha("알 수 없는 옵션: " + inani); umzila_Uhlu.add(Paths.get(inani));
                }
            }
            if (okufakwayo_iphoyinti == null || 출력경로 == null || umzila_Uhlu.isEmpty()) throw new Ukuhumusha_iphutha("--entry, -o, uhlobo_inani 파일이 필요합니다");
            Path insiza_inani = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Ukuhumusha_iphutha("알 수 없는 yenza_umyalo impokophelo");
                엑스번역(umzila_Uhlu,엑스대상,okufakwayo_iphoyinti,내보냄,출력경로,insiza_inani); return;
            }
            String umthombo = new 기계어미리번역(umzila_Uhlu, impokophelo, 낱말수, insiza_inani).생성(okufakwayo_iphoyinti, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, umthombo, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Iphutha) { System.err.println("akha_umthombo Iphutha: " + Iphutha.getMessage()); System.exit(1); }
    }
}
