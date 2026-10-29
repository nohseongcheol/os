// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java icyiciro_agaciro_55654bf1 파일에서 독립 ARM64 커널용 C 원문을 만든다. gucumbikira JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Isemura_ikosa extends RuntimeException {
        Isemura_ikosa(String 설명) { super(설명); }
    }
    static final class amakurushingiro_Musomyi {
        final byte[] amakurushingiro;
        int 위치;
        amakurushingiro_Musomyi(byte[] 입력자료) { amakurushingiro = 입력자료; }
        byte[] 읽기(int uburebure_agaciro) {
            if (uburebure_agaciro < 0 || uburebure_agaciro > amakurushingiro.length - 위치) throw new Isemura_ikosa("잘린 icyiciro_agaciro_55654bf1 또는 Icyo_wifuza amakurushingiro");
            byte[] 결과 = Arrays.copyOfRange(amakurushingiro, 위치, 위치 + uburebure_agaciro); 위치 += uburebure_agaciro; return 결과;
        }
        int 한바이트() { if (위치 >= amakurushingiro.length) throw new Isemura_ikosa("잘린 Icyo_wifuza amakurushingiro"); return amakurushingiro[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class ugize_itsinda_amakurushingiro {
        final int kwinjira_icyinjizwa;
        final String Izina, 서술;
        final Map<String, byte[]> ikiranga_agaciro;
        ugize_itsinda_amakurushingiro(int kwinjira_agaciro, String izina_agaciro, String 서술값, Map<String, byte[]> ikiranga_amakurushingiro) {
            kwinjira_icyinjizwa = kwinjira_agaciro; Izina = izina_agaciro; 서술 = 서술값; ikiranga_agaciro = ikiranga_amakurushingiro;
        }
    }
    static final class uburyo_Indanga implements Comparable<uburyo_Indanga> {
        final String nyirayo_agaciro, Izina, 서술;
        uburyo_Indanga(String 소유값, String izina_agaciro, String 서술값) { nyirayo_agaciro = 소유값; Izina = izina_agaciro; 서술 = 서술값; }
        String[] 부분들() { return new String[]{nyirayo_agaciro, Izina, 서술}; }
        public int compareTo(uburyo_Indanga Mugenzi_agaciro) {
            int 비교값 = nyirayo_agaciro.compareTo(Mugenzi_agaciro.nyirayo_agaciro);
            if (비교값 == 0) 비교값 = Izina.compareTo(Mugenzi_agaciro.Izina);
            return 비교값 == 0 ? 서술.compareTo(Mugenzi_agaciro.서술) : 비교값;
        }
        public boolean equals(Object Mugenzi_agaciro) { return Mugenzi_agaciro instanceof uburyo_Indanga && compareTo((uburyo_Indanga) Mugenzi_agaciro) == 0; }
        public int hashCode() { return Objects.hash(nyirayo_agaciro, Izina, 서술); }
    }
    static final class icyiciro_amakurushingiro {
        final int[] 상수종류;
        final Object[] kidahinduka_amakurushingiro;
        final String Izina;
        final List<ugize_itsinda_amakurushingiro> umwanya_agaciro_0f39cf1c, FUNCTION_agaciro;
        icyiciro_amakurushingiro(Path Inzira) throws IOException {
            amakurushingiro_Musomyi Musomyi_agaciro = new amakurushingiro_Musomyi(Files.readAllBytes(Inzira));
            if (Musomyi_agaciro.네바이트() != 0xcafebabe) throw new Isemura_ikosa("Java icyiciro_agaciro_55654bf1 표식이 아님");
            Musomyi_agaciro.읽기(4);
            int 개수 = Musomyi_agaciro.두바이트(); 상수종류 = new int[개수]; kidahinduka_amakurushingiro = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = Musomyi_agaciro.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int uburebure_agaciro = Musomyi_agaciro.두바이트();
                        byte[] inyuguti_ububiko_gateganyo = Musomyi_agaciro.읽기(uburebure_agaciro), 길이붙인자료 = new byte[uburebure_agaciro + 2];
                        길이붙인자료[0] = (byte)(uburebure_agaciro >> 8); 길이붙인자료[1] = (byte)uburebure_agaciro;
                        System.arraycopy(inyuguti_ububiko_gateganyo, 0, 길이붙인자료, 2, uburebure_agaciro);
                        kidahinduka_amakurushingiro[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: kidahinduka_amakurushingiro[순번] = Musomyi_agaciro.네바이트(); break;
                    case 4: Musomyi_agaciro.읽기(4); break;
                    case 5: case 6: Musomyi_agaciro.읽기(8); 순번++; break;
                    case 7: case 8: case 16: kidahinduka_amakurushingiro[순번] = Musomyi_agaciro.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        kidahinduka_amakurushingiro[순번] = new int[]{Musomyi_agaciro.두바이트(), Musomyi_agaciro.두바이트()}; break;
                    case 15: kidahinduka_amakurushingiro[순번] = new int[]{Musomyi_agaciro.한바이트(), Musomyi_agaciro.두바이트()}; break;
                    default: throw new Isemura_ikosa("지원하지 않는 kidahinduka_agaciro 종류: " + 종류);
                }
            }
            Musomyi_agaciro.두바이트(); Izina = icyiciro_izina(Musomyi_agaciro.두바이트());
            if (!icyiciro_izina(Musomyi_agaciro.두바이트()).equals("java/lang/Object") || Musomyi_agaciro.두바이트() != 0)
                throw new Isemura_ikosa(Izina + ": 상속 및 인터페이스 미지원");
            umwanya_agaciro_0f39cf1c = 멤버읽기(Musomyi_agaciro); FUNCTION_agaciro = 멤버읽기(Musomyi_agaciro); 속성읽기(Musomyi_agaciro);
            if (Musomyi_agaciro.위치 != Musomyi_agaciro.amakurushingiro.length) throw new Isemura_ikosa("icyiciro_agaciro_55654bf1 뒤에 남은 amakurushingiro");
        }
        String 문자(int umugerekashakiro) {
            if (umugerekashakiro < 1 || umugerekashakiro >= 상수종류.length || 상수종류[umugerekashakiro] != 1) throw new Isemura_ikosa("문자 kidahinduka_agaciro umugerekashakiro IKOSA");
            return (String) kidahinduka_amakurushingiro[umugerekashakiro];
        }
        String icyiciro_izina(int umugerekashakiro) {
            if (umugerekashakiro < 1 || umugerekashakiro >= 상수종류.length || 상수종류[umugerekashakiro] != 7) throw new Isemura_ikosa("icyiciro_agaciro_55654bf1 Indanga IKOSA");
            return 문자((Integer)kidahinduka_amakurushingiro[umugerekashakiro]);
        }
        uburyo_Indanga Indanga(int umugerekashakiro) {
            if (umugerekashakiro < 1 || umugerekashakiro >= 상수종류.length || 상수종류[umugerekashakiro] < 9 || 상수종류[umugerekashakiro] > 11) throw new Isemura_ikosa("멤버 Indanga IKOSA");
            int[] guhuza_burutusi_agaciro = (int[])kidahinduka_amakurushingiro[umugerekashakiro], izina_guhuza_burutusi = (int[])kidahinduka_amakurushingiro[guhuza_burutusi_agaciro[1]];
            return new uburyo_Indanga(icyiciro_izina(guhuza_burutusi_agaciro[0]), 문자(izina_guhuza_burutusi[0]), 문자(izina_guhuza_burutusi[1]));
        }
        Map<String, byte[]> 속성읽기(amakurushingiro_Musomyi Musomyi_agaciro) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = Musomyi_agaciro.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String ikiranga_izina = 문자(Musomyi_agaciro.두바이트()); byte[] agaciro = Musomyi_agaciro.읽기(Musomyi_agaciro.네바이트());
                if (결과.put(ikiranga_izina, agaciro) != null) throw new Isemura_ikosa("겹친 ikiranga_agaciro: " + ikiranga_izina);
            }
            return 결과;
        }
        List<ugize_itsinda_amakurushingiro> 멤버읽기(amakurushingiro_Musomyi Musomyi_agaciro) {
            List<ugize_itsinda_amakurushingiro> 결과 = new ArrayList<>(); int 개수 = Musomyi_agaciro.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int kwinjira_icyinjizwa = Musomyi_agaciro.두바이트(); String uburyo_icyinjizwa_izina = 문자(Musomyi_agaciro.두바이트()), 서술 = 문자(Musomyi_agaciro.두바이트());
                결과.add(new ugize_itsinda_amakurushingiro(kwinjira_icyinjizwa, uburyo_icyinjizwa_izina, 서술, 속성읽기(Musomyi_agaciro)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Isemura_ikosa("FUNCTION_agaciro 서술 IKOSA: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Isemura_ikosa("FUNCTION_agaciro 서술 IKOSA: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Isemura_ikosa("FUNCTION_agaciro 서술 IKOSA: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String ihitamo_agaciro = null;
            for (String imiterere_agaciro : 허용형식) if (서술.startsWith(imiterere_agaciro, 위치)) { ihitamo_agaciro = imiterere_agaciro; break; }
            if (ihitamo_agaciro == null) throw new Isemura_ikosa("지원하지 않는 ubwoko_bw_amakurushingiro: " + 서술);
            결과.add(ihitamo_agaciro); 위치 += ihitamo_agaciro.length();
        }
        return 결과;
    }
    static String ikimenyetso(String 종류, String... 부분들) {
        try {
            byte[] hashi_dosiye = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Umwandiko = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Umwandiko.append(String.format(Locale.ROOT, "%02x", hashi_dosiye[순번] & 255));
            return Umwandiko.toString();
        } catch (Exception IKOSA) { throw new Isemura_ikosa(IKOSA.toString()); }
    }
    final Map<String, icyiciro_amakurushingiro> 클래스들 = new TreeMap<>();
    final Map<uburyo_Indanga, ugize_itsinda_amakurushingiro> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, imashini_icyiciro;
    final int 동적기억낱말수;
    final Path umutungo_inzira;
    기계어미리번역(List<Path> inzira_Urutonde, String gusimbuza_igishya, int 낱말수, Path umutungo_agaciro) throws IOException {
        if ((!gusimbuza_igishya.equals("kernel") && !gusimbuza_igishya.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Isemura_ikosa("gukora_ibwiriza gusimbuza_igishya 또는 ububiko_agaciro 공간 Ingano IKOSA");
        실행대상 = gusimbuza_igishya; 동적기억낱말수 = 낱말수; umutungo_inzira = umutungo_agaciro;
        // 이 이름도 국가별 inkomoko_igiti 생성 시 해당 언어로 옮긴다.
        imashini_icyiciro = gusimbuza_igishya.equals("kernel") ? "보드" : "ukoresha";
        for (String umurongo : Files.readAllLines(umutungo_agaciro.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = umurongo.split("\t", -1);
            if (부분들.length != 4) throw new Isemura_ikosa("imashini FUNCTION_agaciro amakurushingiro IKOSA");
            if (부분들[0].equals(gusimbuza_igishya)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Inzira : inzira_Urutonde) {
            icyiciro_amakurushingiro amakurushingiro = new icyiciro_amakurushingiro(Inzira);
            if (클래스들.put(amakurushingiro.Izina, amakurushingiro) != null) throw new Isemura_ikosa("중복 icyiciro_agaciro_55654bf1: " + amakurushingiro.Izina);
            for (ugize_itsinda_amakurushingiro umwanya_agaciro_0f39cf1c : amakurushingiro.umwanya_agaciro_0f39cf1c) {
                if ((umwanya_agaciro_0f39cf1c.kwinjira_icyinjizwa & 8) == 0 || 형식읽기(umwanya_agaciro_0f39cf1c.서술).equals(Collections.singletonList("V"))) throw new Isemura_ikosa("kitayega_agaciro 필드만 Ubufasha_agaciro");
                if (필드들.put(new uburyo_Indanga(amakurushingiro.Izina, umwanya_agaciro_0f39cf1c.Izina, umwanya_agaciro_0f39cf1c.서술), umwanya_agaciro_0f39cf1c) != null) throw new Isemura_ikosa("중복 umwanya_agaciro_0f39cf1c");
            }
            for (ugize_itsinda_amakurushingiro FUNCTION_agaciro : amakurushingiro.FUNCTION_agaciro) {
                if (FUNCTION_agaciro.Izina.equals("<init>")) continue;
                if ((FUNCTION_agaciro.kwinjira_icyinjizwa & 8) == 0 || (FUNCTION_agaciro.kwinjira_icyinjizwa & (0x20 | 0x400)) != 0) throw new Isemura_ikosa("kitayega_agaciro 비동기화 함수만 Ubufasha_agaciro");
                new 함수형식(FUNCTION_agaciro.서술);
                if (함수들.put(new uburyo_Indanga(amakurushingiro.Izina, FUNCTION_agaciro.Izina, FUNCTION_agaciro.서술), FUNCTION_agaciro) != null) throw new Isemura_ikosa("중복 FUNCTION_agaciro");
            }
        }
    }
    String igicenteruro_ikimenyetso(String Umwandiko) { return 문자열들.computeIfAbsent(Umwandiko, agaciro -> "j_text_" + 문자열들.size()); }
    String kidahinduka_imvugo(icyiciro_amakurushingiro amakurushingiro, int umugerekashakiro) {
        if (umugerekashakiro < 1 || umugerekashakiro >= amakurushingiro.상수종류.length) throw new Isemura_ikosa("kidahinduka_agaciro umugerekashakiro kiripu IKOSA");
        if (amakurushingiro.상수종류[umugerekashakiro] == 3) return "(word)(uint32_t)(" + amakurushingiro.kidahinduka_amakurushingiro[umugerekashakiro] + ")";
        if (amakurushingiro.상수종류[umugerekashakiro] == 8) return "(word)" + igicenteruro_ikimenyetso(amakurushingiro.문자((Integer)amakurushingiro.kidahinduka_amakurushingiro[umugerekashakiro]));
        throw new Isemura_ikosa("정수와 igicenteruro_agaciro 상수만 Ubufasha_agaciro");
    }
    String 함수원형(uburyo_Indanga Indanga) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Indanga.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + ikimenyetso("method", Indanga.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void sheki_mu_gace(int umugerekashakiro, int 지역변수수) { if (umugerekashakiro < 0 || umugerekashakiro >= 지역변수수) throw new Isemura_ikosa("mu_gace_urwego 변수 umugerekashakiro kiripu IKOSA"); }
    void 분기넣기(List<String> 출력, Set<Integer> ishami_Urutonde, int 위치, int 이동량, String icyangombwa) {
        int aho_ijya_agaciro = 위치 + 이동량; ishami_Urutonde.add(aho_ijya_agaciro);
        출력.add((icyangombwa == null ? "" : "if (" + icyangombwa + ") ") + "goto b" + aho_ijya_agaciro + ";");
    }
    String 함수본문(uburyo_Indanga FUNCTION_agaciro, ugize_itsinda_amakurushingiro amakurushingiro) {
        byte[] 본문자료 = amakurushingiro.ikiranga_agaciro.get("Code"); if (본문자료 == null) throw new Isemura_ikosa("FUNCTION_agaciro 몸체가 없음: " + FUNCTION_agaciro.Izina);
        amakurushingiro_Musomyi Musomyi_agaciro = new amakurushingiro_Musomyi(본문자료); int 쌓임깊이 = Musomyi_agaciro.두바이트(), 지역변수수 = Musomyi_agaciro.두바이트();
        amakurushingiro_Musomyi ibwiriza_amakurushingiro = new amakurushingiro_Musomyi(Musomyi_agaciro.읽기(Musomyi_agaciro.네바이트()));
        if (Musomyi_agaciro.두바이트() != 0) throw new Isemura_ikosa("try/catch/finally 미지원");
        함수형식 imiterere_agaciro = new 함수형식(FUNCTION_agaciro.서술); if (지역변수수 < imiterere_agaciro.인수.size()) throw new Isemura_ikosa("매개변수보다 적은 mu_gace_urwego 변수");
        icyiciro_amakurushingiro icyiciro_agaciro_55654bf1 = 클래스들.get(FUNCTION_agaciro.nyirayo_agaciro);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(FUNCTION_agaciro) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < imiterere_agaciro.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ishami_Urutonde = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (ibwiriza_amakurushingiro.위치 < ibwiriza_amakurushingiro.amakurushingiro.length) {
            int 위치 = ibwiriza_amakurushingiro.위치, Icyo_wifuza = ibwiriza_amakurushingiro.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (Icyo_wifuza == 0) continue;
            if (Icyo_wifuza == 1) 출력.add("PUSH(0);");
            else if (Icyo_wifuza >= 2 && Icyo_wifuza <= 8) 출력.add("PUSH((uint32_t)(" + (Icyo_wifuza - 3) + "));");
            else if (Icyo_wifuza == 16 || Icyo_wifuza == 17) 출력.add("PUSH((uint32_t)(" + (Icyo_wifuza == 16 ? ibwiriza_amakurushingiro.부호한바이트() : ibwiriza_amakurushingiro.부호두바이트()) + "));");
            else if (Icyo_wifuza == 18 || Icyo_wifuza == 19) 출력.add("PUSH(" + kidahinduka_imvugo(icyiciro_agaciro_55654bf1, Icyo_wifuza == 18 ? ibwiriza_amakurushingiro.한바이트() : ibwiriza_amakurushingiro.두바이트()) + ");");
            else if (Icyo_wifuza == 21 || Icyo_wifuza == 25 || (Icyo_wifuza >= 26 && Icyo_wifuza <= 29) || (Icyo_wifuza >= 42 && Icyo_wifuza <= 45)) {
                int umugerekashakiro = Icyo_wifuza == 21 || Icyo_wifuza == 25 ? ibwiriza_amakurushingiro.한바이트() : Icyo_wifuza - (Icyo_wifuza <= 29 ? 26 : 42);
                sheki_mu_gace(umugerekashakiro, 지역변수수); 출력.add("PUSH(l[" + umugerekashakiro + "]);");
            } else if (Icyo_wifuza == 54 || Icyo_wifuza == 58 || (Icyo_wifuza >= 59 && Icyo_wifuza <= 62) || (Icyo_wifuza >= 75 && Icyo_wifuza <= 78)) {
                int umugerekashakiro = Icyo_wifuza == 54 || Icyo_wifuza == 58 ? ibwiriza_amakurushingiro.한바이트() : Icyo_wifuza - (Icyo_wifuza <= 62 ? 59 : 75);
                sheki_mu_gace(umugerekashakiro, 지역변수수); 출력.add("l[" + umugerekashakiro + "] = POP();");
            } else if (Icyo_wifuza == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Icyo_wifuza == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Icyo_wifuza == 87 || Icyo_wifuza == 88) 출력.add(Icyo_wifuza == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Icyo_wifuza >= 89 && Icyo_wifuza <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] umujyo_Urutonde = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Icyo_wifuza - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char agaciro : umujyo_Urutonde[Icyo_wifuza - 89].toCharArray()) 출력.add("PUSH(" + agaciro + ");");
            } else if (Icyo_wifuza == 96 || Icyo_wifuza == 100 || Icyo_wifuza == 104 || Icyo_wifuza == 126 || Icyo_wifuza == 128 || Icyo_wifuza == 130) {
                String igikorwa_agaciro = Icyo_wifuza == 96 ? "+" : Icyo_wifuza == 100 ? "-" : Icyo_wifuza == 104 ? "*" : Icyo_wifuza == 126 ? "&" : Icyo_wifuza == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + igikorwa_agaciro + " (uint32_t)b);");
            } else if (Icyo_wifuza == 108 || Icyo_wifuza == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Icyo_wifuza == 112 ? 1 : 0) + "));");
            else if (Icyo_wifuza == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Icyo_wifuza == 120 || Icyo_wifuza == 122 || Icyo_wifuza == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Icyo_wifuza == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Icyo_wifuza == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Icyo_wifuza == 132) {
                int umugerekashakiro = ibwiriza_amakurushingiro.한바이트(), 증가량 = ibwiriza_amakurushingiro.부호한바이트(); sheki_mu_gace(umugerekashakiro, 지역변수수);
                출력.add("l[" + umugerekashakiro + "] = (uint32_t)l[" + umugerekashakiro + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Icyo_wifuza >= 145 && Icyo_wifuza <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Icyo_wifuza == 145 ? "int8_t" : Icyo_wifuza == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Icyo_wifuza >= 153 && Icyo_wifuza <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, ishami_Urutonde, 위치, ibwiriza_amakurushingiro.부호두바이트(), "(int32_t)a " + 비교들[Icyo_wifuza - 153] + " 0");
            } else if (Icyo_wifuza >= 159 && Icyo_wifuza <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, ishami_Urutonde, 위치, ibwiriza_amakurushingiro.부호두바이트(), Icyo_wifuza >= 165 ? "a " + 비교들[Icyo_wifuza - 159] + " b" : "(int32_t)a " + 비교들[Icyo_wifuza - 159] + " (int32_t)b");
            } else if (Icyo_wifuza == 167 || Icyo_wifuza == 200) 분기넣기(출력, ishami_Urutonde, 위치, Icyo_wifuza == 167 ? ibwiriza_amakurushingiro.부호두바이트() : ibwiriza_amakurushingiro.네바이트(), null);
            else if (Icyo_wifuza == 170 || Icyo_wifuza == 171) {
                while (ibwiriza_amakurushingiro.위치 % 4 != 0) ibwiriza_amakurushingiro.한바이트();
                int agaciro_gasanzweho = ibwiriza_amakurushingiro.네바이트(); 출력.add("a = POP();");
                if (Icyo_wifuza == 170) {
                    int 아래 = ibwiriza_amakurushingiro.네바이트(), 위 = ibwiriza_amakurushingiro.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (ibwiriza_amakurushingiro.amakurushingiro.length - ibwiriza_amakurushingiro.위치) / 4) throw new Isemura_ikosa("switch kiripu IKOSA");
                    for (long agaciro = 아래; agaciro <= 위; agaciro++) 분기넣기(출력, ishami_Urutonde, 위치, ibwiriza_amakurushingiro.네바이트(), "(int32_t)a == (" + agaciro + ")");
                } else {
                    int 개수 = ibwiriza_amakurushingiro.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (ibwiriza_amakurushingiro.amakurushingiro.length - ibwiriza_amakurushingiro.위치) / 8) throw new Isemura_ikosa("switch Ingano IKOSA");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int agaciro = ibwiriza_amakurushingiro.네바이트(); if (순번 > 0 && agaciro <= 앞값) throw new Isemura_ikosa("switch umujyo_agaciro IKOSA"); 앞값 = agaciro;
                        분기넣기(출력, ishami_Urutonde, 위치, ibwiriza_amakurushingiro.네바이트(), "(int32_t)a == (" + agaciro + ")");
                    }
                }
                분기넣기(출력, ishami_Urutonde, 위치, agaciro_gasanzweho, null);
            } else if (Icyo_wifuza == 172 || Icyo_wifuza == 176 || Icyo_wifuza == 177) 출력.add("return " + (Icyo_wifuza == 177 ? "0" : "POP()") + ";");
            else if (Icyo_wifuza == 178 || Icyo_wifuza == 179) {
                uburyo_Indanga Indanga = icyiciro_agaciro_55654bf1.Indanga(ibwiriza_amakurushingiro.두바이트()); if (!필드들.containsKey(Indanga)) throw new Isemura_ikosa("알 수 없는 umwanya_agaciro_0f39cf1c");
                출력.add(ikimenyetso("init", Indanga.nyirayo_agaciro) + "();"); String umwanya_agaciro_0f39cf1c = ikimenyetso("field", Indanga.부분들());
                출력.add(Icyo_wifuza == 178 ? "PUSH(" + umwanya_agaciro_0f39cf1c + ");" : umwanya_agaciro_0f39cf1c + " = POP();");
            } else if (Icyo_wifuza == 184) {
                uburyo_Indanga Indanga = icyiciro_agaciro_55654bf1.Indanga(ibwiriza_amakurushingiro.두바이트()); if (!함수들.containsKey(Indanga)) throw new Isemura_ikosa("알 수 없는 FUNCTION_agaciro");
                함수형식 호출형식 = new 함수형식(Indanga.서술); int 개수 = 호출형식.인수.size();
                출력.add(ikimenyetso("init", Indanga.nyirayo_agaciro) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + ikimenyetso("method", Indanga.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Icyo_wifuza == 182) {
                uburyo_Indanga Indanga = icyiciro_agaciro_55654bf1.Indanga(ibwiriza_amakurushingiro.두바이트());
                if (Indanga.equals(new uburyo_Indanga("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Indanga.equals(new uburyo_Indanga("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Isemura_ikosa("가상 FUNCTION_agaciro 호출 미지원");
            } else if (Icyo_wifuza == 188) {
                if (ibwiriza_amakurushingiro.한바이트() != 10) throw new Isemura_ikosa("new int[]만 Ubufasha_agaciro"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Icyo_wifuza == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Icyo_wifuza == 196) {
                int umugereka_agaciro = ibwiriza_amakurushingiro.한바이트(), umugerekashakiro = ibwiriza_amakurushingiro.두바이트(); sheki_mu_gace(umugerekashakiro, 지역변수수);
                if (umugereka_agaciro == 21 || umugereka_agaciro == 25) 출력.add("PUSH(l[" + umugerekashakiro + "]);");
                else if (umugereka_agaciro == 54 || umugereka_agaciro == 58) 출력.add("l[" + umugerekashakiro + "] = POP();");
                else if (umugereka_agaciro == 132) 출력.add("l[" + umugerekashakiro + "] = (uint32_t)l[" + umugerekashakiro + "] + (uint32_t)(" + ibwiriza_amakurushingiro.부호두바이트() + ");");
                else throw new Isemura_ikosa("미지원 wide Icyo_wifuza");
            } else if (Icyo_wifuza == 198 || Icyo_wifuza == 199) {
                출력.add("a = POP();"); 분기넣기(출력, ishami_Urutonde, 위치, ibwiriza_amakurushingiro.부호두바이트(), "a " + (Icyo_wifuza == 198 ? "==" : "!=") + " 0");
            } else throw new Isemura_ikosa(FUNCTION_agaciro.nyirayo_agaciro + "." + FUNCTION_agaciro.Izina + ", bayiti_agaciro " + 위치 + ": 미지원 Icyo_wifuza " + Icyo_wifuza);
        }
        if (!경계들.containsAll(ishami_Urutonde)) throw new Isemura_ikosa("Icyo_wifuza 경계가 아닌 곳으로 ishami");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String kwimura_uburyo(String Ihuza_ikimenyetso, String gusimbuza_igishya, boolean 진입점여부) {
        int 자리 = gusimbuza_igishya.lastIndexOf('.'); if (자리 < 0 || !Ihuza_ikimenyetso.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Isemura_ikosa("내보내기 지정 IKOSA");
        String nyirayo_agaciro = gusimbuza_igishya.substring(0, 자리).replace('.', '/'), Izina = gusimbuza_igishya.substring(자리 + 1); uburyo_Indanga ihitamo_agaciro = null;
        for (uburyo_Indanga Indanga : 함수들.keySet()) if (Indanga.nyirayo_agaciro.equals(nyirayo_agaciro) && Indanga.Izina.equals(Izina)) {
            if (ihitamo_agaciro != null) throw new Isemura_ikosa("겹친 내보내기 gusimbuza_igishya"); ihitamo_agaciro = Indanga;
        }
        if (ihitamo_agaciro == null || (함수들.get(ihitamo_agaciro).kwinjira_icyinjizwa & 0x100) != 0) throw new Isemura_ikosa("내보낼 함수가 없음 또는 native FUNCTION_agaciro");
        함수형식 imiterere_agaciro = new 함수형식(ihitamo_agaciro.서술);
        if ((진입점여부 && !imiterere_agaciro.인수.isEmpty()) || !Arrays.asList("V", "I").contains(imiterere_agaciro.반환)) throw new Isemura_ikosa("icyinjizwa_inota_agaciro 또는 C 경계 imiterere_agaciro IKOSA");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < imiterere_agaciro.인수.size(); 순번++) {
            if (!imiterere_agaciro.인수.get(순번).equals("I")) throw new Isemura_ikosa("C 경계는 int 인수만 Ubufasha_agaciro");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (imiterere_agaciro.반환.equals("V") ? "void " : "int32_t ") + Ihuza_ikimenyetso + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + ikimenyetso("init", ihitamo_agaciro.nyirayo_agaciro) + "(); " + (imiterere_agaciro.반환.equals("V") ? "" : "return (int32_t)") + ikimenyetso("method", ihitamo_agaciro.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String icyinjizwa_inota, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<uburyo_Indanga, ugize_itsinda_amakurushingiro> icyinjizwa_agaciro : 함수들.entrySet()) {
            uburyo_Indanga Indanga = icyinjizwa_agaciro.getKey(); ugize_itsinda_amakurushingiro amakurushingiro = icyinjizwa_agaciro.getValue(); 선언들.add(함수원형(Indanga) + ";");
            if ((amakurushingiro.kwinjira_icyinjizwa & 0x100) != 0) {
                String Guhuza = 기계함수들.get(Indanga.Izina + Indanga.서술);
                if (!Indanga.nyirayo_agaciro.equals(imashini_icyiciro) || Guhuza == null) throw new Isemura_ikosa("허용되지 않은 native FUNCTION_agaciro: " + Indanga.Izina);
                int 개수 = new 함수형식(Indanga.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Guhuza + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Indanga) + " { return " + Guhuza + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Indanga, amakurushingiro));
        }
        for (Map.Entry<uburyo_Indanga, ugize_itsinda_amakurushingiro> icyinjizwa_agaciro : 필드들.entrySet()) {
            uburyo_Indanga Indanga = icyinjizwa_agaciro.getKey(); byte[] kidahinduka_agaciro = icyinjizwa_agaciro.getValue().ikiranga_agaciro.get("ConstantValue");
            String agaciro = kidahinduka_agaciro == null ? "0" : kidahinduka_imvugo(클래스들.get(Indanga.nyirayo_agaciro), new amakurushingiro_Musomyi(kidahinduka_agaciro).두바이트());
            필드선언들.add("static word " + ikimenyetso("field", Indanga.부분들()) + " = " + agaciro + ";");
        }
        for (String Izina : 클래스들.keySet()) {
            String gutangiza = ikimenyetso("init", Izina), imimerere_agaciro = ikimenyetso("state", Izina);
            선언들.add("static void " + gutangiza + "(void);"); 필드선언들.add("static unsigned " + imimerere_agaciro + ";");
            uburyo_Indanga Indanga = new uburyo_Indanga(Izina, "<clinit>", "()V");
            몸체들.add("static void " + gutangiza + "(void) { if(" + imimerere_agaciro + ") return; " + imimerere_agaciro + " = 1; " + (함수들.containsKey(Indanga) ? ikimenyetso("method", Indanga.부분들()) + "(); " : "") + imimerere_agaciro + " = 2; }");
        }
        몸체들.add(kwimura_uburyo("java_entry", icyinjizwa_inota, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new Isemura_ikosa("내보내기 지정 IKOSA");
            String Izina = 지정.substring(0, 자리); 공개이름.add(Izina); 몸체들.add(kwimura_uburyo(Izina, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> icyinjizwa_agaciro : 문자열들.entrySet()) {
            String Umwandiko = icyinjizwa_agaciro.getKey(); StringBuilder ARRAY_agaciro = new StringBuilder("static const word " + icyinjizwa_agaciro.getValue() + "[] = {" + Umwandiko.length());
            for (int 순번 = 0; 순번 < Umwandiko.length(); 순번++) ARRAY_agaciro.append(", ").append((int)Umwandiko.charAt(순번));
            문자열선언들.add(ARRAY_agaciro.append("};").toString());
        }
        String Ubufasha_agaciro = Files.readString(umutungo_inzira.resolve("igihe_ururimi_rukorwamo_Ubufasha.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Ubufasha_agaciro + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String Inkomoko, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> izina_imbonerahamwe = new HashMap<>();
        for (String umurongo : Files.readAllLines(umutungo_inzira.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] guhuza_burutusi_agaciro = umurongo.split("\t"); izina_imbonerahamwe.put(guhuza_burutusi_agaciro[0], guhuza_burutusi_agaciro[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(Inkomoko); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Izina = 찾개.group(), 새이름 = Izina;
            if (!Izina.startsWith("//") && !Izina.startsWith("/*") && !Izina.startsWith("\"") && !Izina.startsWith("'") && !공개이름.contains(Izina)) {
                새이름 = izina_imbonerahamwe.getOrDefault(Izina, Izina);
                if (Izina.matches("a[0-9]+")) 새이름 = "인수" + Izina.substring(1);
                if (Izina.matches("b[0-9]+")) 새이름 = "ishami" + Izina.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char inyuguti_agaciro : 새이름.toCharArray()) 표기.append(inyuguti_agaciro < 128 ? Character.toString(inyuguti_agaciro) : String.format(Locale.ROOT, "\\u%04x", (int)inyuguti_agaciro));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(uburyo_Indanga FUNCTION_agaciro, ugize_itsinda_amakurushingiro amakurushingiro, Map<String,String> imashini_imbonerahamwe, String gusimbuza_igishya) {
        String 표식 = ikimenyetso("method", FUNCTION_agaciro.부분들());
        List<String> umurongo = new ArrayList<>();
        if ((amakurushingiro.kwinjira_icyinjizwa & 0x100) != 0) {
            String Guhuza = imashini_imbonerahamwe.get(FUNCTION_agaciro.Izina + FUNCTION_agaciro.서술);
            if (!FUNCTION_agaciro.nyirayo_agaciro.equals(gusimbuza_igishya.equals("kernel") ? "igendanwa_agaciro" : "ukoresha") || Guhuza == null) throw new Isemura_ikosa("허용되지 않은 native FUNCTION_agaciro");
            return ".text\n" + 표식 + ":\njmp " + Guhuza;
        }
        byte[] igihimba_cy_umwandiko = amakurushingiro.ikiranga_agaciro.get("Code"); if (igihimba_cy_umwandiko == null) throw new Isemura_ikosa("FUNCTION_agaciro 몸체가 없음");
        amakurushingiro_Musomyi Musomyi_agaciro = new amakurushingiro_Musomyi(igihimba_cy_umwandiko); Musomyi_agaciro.두바이트(); int 지역수 = Musomyi_agaciro.두바이트();
        amakurushingiro_Musomyi ibwiriza_amakurushingiro = new amakurushingiro_Musomyi(Musomyi_agaciro.읽기(Musomyi_agaciro.네바이트()));
        if (Musomyi_agaciro.두바이트() != 0) throw new Isemura_ikosa("try/catch/finally 미지원");
        함수형식 imiterere_agaciro = new 함수형식(FUNCTION_agaciro.서술); if (지역수 < imiterere_agaciro.인수.size()) throw new Isemura_ikosa("매개변수보다 적은 mu_gace_urwego 변수");
        Collections.addAll(umurongo,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < imiterere_agaciro.인수.size(); 순번++) Collections.addAll(umurongo,"movl " + (8 + 4 * (imiterere_agaciro.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        icyiciro_amakurushingiro icyiciro_agaciro_55654bf1 = 클래스들.get(FUNCTION_agaciro.nyirayo_agaciro); Set<Integer> 경계들 = new HashSet<>(), ishami_Urutonde = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (ibwiriza_amakurushingiro.위치 < ibwiriza_amakurushingiro.amakurushingiro.length) {
            int 위치 = ibwiriza_amakurushingiro.위치, Icyo_wifuza = ibwiriza_amakurushingiro.한바이트(); String 자리 = 표식 + "_b" + 위치;
            umurongo.add(자리 + ":"); 경계들.add(위치);
            if (Icyo_wifuza == 0) umurongo.add("nop");
            else if (Icyo_wifuza == 1) umurongo.add("pushl $0");
            else if (Icyo_wifuza >= 2 && Icyo_wifuza <= 8) umurongo.add("pushl $" + (Icyo_wifuza - 3));
            else if (Icyo_wifuza == 16 || Icyo_wifuza == 17) umurongo.add("pushl $" + (Icyo_wifuza == 16 ? ibwiriza_amakurushingiro.부호한바이트() : ibwiriza_amakurushingiro.부호두바이트()));
            else if (Icyo_wifuza == 18 || Icyo_wifuza == 19) {
                int umugerekashakiro = Icyo_wifuza == 18 ? ibwiriza_amakurushingiro.한바이트() : ibwiriza_amakurushingiro.두바이트();
                umurongo.add("pushl $" + 엑스상수(icyiciro_agaciro_55654bf1,umugerekashakiro));
            } else if (Icyo_wifuza == 21 || Icyo_wifuza == 25 || (Icyo_wifuza >= 26 && Icyo_wifuza <= 29) || (Icyo_wifuza >= 42 && Icyo_wifuza <= 45) || Icyo_wifuza == 54 || Icyo_wifuza == 58 || (Icyo_wifuza >= 59 && Icyo_wifuza <= 62) || (Icyo_wifuza >= 75 && Icyo_wifuza <= 78)) {
                boolean 읽음 = Icyo_wifuza < 54; int umugerekashakiro = Icyo_wifuza == 21 || Icyo_wifuza == 25 || Icyo_wifuza == 54 || Icyo_wifuza == 58 ? ibwiriza_amakurushingiro.한바이트() : Icyo_wifuza - (Icyo_wifuza <= 29 ? 26 : Icyo_wifuza <= 45 ? 42 : Icyo_wifuza <= 62 ? 59 : 75);
                sheki_mu_gace(umugerekashakiro,지역수); umurongo.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (umugerekashakiro + 1)) + "(%ebp)");
            } else if (Icyo_wifuza == 46) Collections.addAll(umurongo,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Icyo_wifuza == 79) Collections.addAll(umurongo,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Icyo_wifuza == 87 || Icyo_wifuza == 88) umurongo.add("addl $" + (Icyo_wifuza == 87 ? 4 : 8) + ", %esp");
            else if (Icyo_wifuza >= 89 && Icyo_wifuza <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] umujyo_Urutonde = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Icyo_wifuza - 89]; 순번++) umurongo.add("popl " + 저장기들[순번]);
                for (int 순번 : umujyo_Urutonde[Icyo_wifuza - 89]) umurongo.add("pushl " + 저장기들[순번]);
            } else if (Icyo_wifuza == 96 || Icyo_wifuza == 100 || Icyo_wifuza == 104 || Icyo_wifuza == 126 || Icyo_wifuza == 128 || Icyo_wifuza == 130) {
                String igikorwa_agaciro = Icyo_wifuza == 96 ? "addl" : Icyo_wifuza == 100 ? "subl" : Icyo_wifuza == 104 ? "imull" : Icyo_wifuza == 126 ? "andl" : Icyo_wifuza == 128 ? "orl" : "xorl";
                Collections.addAll(umurongo,"popl %ecx","popl %eax",igikorwa_agaciro + " %ecx, %eax","pushl %eax");
            } else if (Icyo_wifuza == 108 || Icyo_wifuza == 112) Collections.addAll(umurongo,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Icyo_wifuza == 108 ? "%eax" : "%edx"));
            else if (Icyo_wifuza == 116) umurongo.add("negl (%esp)");
            else if (Icyo_wifuza == 120 || Icyo_wifuza == 122 || Icyo_wifuza == 124) Collections.addAll(umurongo,"popl %ecx","popl %eax",(Icyo_wifuza == 120 ? "sall" : Icyo_wifuza == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Icyo_wifuza == 132) {
                int umugerekashakiro = ibwiriza_amakurushingiro.한바이트(), 증가 = ibwiriza_amakurushingiro.부호한바이트(); sheki_mu_gace(umugerekashakiro,지역수); umurongo.add("addl $" + 증가 + ", -" + (4 * (umugerekashakiro + 1)) + "(%ebp)");
            } else if (Icyo_wifuza >= 145 && Icyo_wifuza <= 147) Collections.addAll(umurongo,"popl %eax",Icyo_wifuza == 145 ? "movsbl %al, %eax" : Icyo_wifuza == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Icyo_wifuza >= 153 && Icyo_wifuza <= 166) {
                if (Icyo_wifuza <= 158) Collections.addAll(umurongo,"popl %eax","testl %eax, %eax");
                else Collections.addAll(umurongo,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int aho_ijya_agaciro = 위치 + ibwiriza_amakurushingiro.부호두바이트(); ishami_Urutonde.add(aho_ijya_agaciro); umurongo.add(비교들[Icyo_wifuza - (Icyo_wifuza <= 158 ? 153 : 159)] + " " + 표식 + "_b" + aho_ijya_agaciro);
            } else if (Icyo_wifuza == 167 || Icyo_wifuza == 200) {
                int aho_ijya_agaciro = 위치 + (Icyo_wifuza == 167 ? ibwiriza_amakurushingiro.부호두바이트() : ibwiriza_amakurushingiro.네바이트()); ishami_Urutonde.add(aho_ijya_agaciro); umurongo.add("jmp " + 표식 + "_b" + aho_ijya_agaciro);
            } else if (Icyo_wifuza == 170 || Icyo_wifuza == 171) {
                while (ibwiriza_amakurushingiro.위치 % 4 != 0) ibwiriza_amakurushingiro.한바이트();
                int agaciro_gasanzweho = 위치 + ibwiriza_amakurushingiro.네바이트(); ishami_Urutonde.add(agaciro_gasanzweho); umurongo.add("popl %eax");
                int 개수, 아래 = 0;
                if (Icyo_wifuza == 170) { 아래 = ibwiriza_amakurushingiro.네바이트(); int 위 = ibwiriza_amakurushingiro.네바이트(); long uburebure_agaciro = (long)위 - 아래 + 1; if (uburebure_agaciro < 1 || uburebure_agaciro > (ibwiriza_amakurushingiro.amakurushingiro.length - ibwiriza_amakurushingiro.위치) / 4) throw new Isemura_ikosa("switch kiripu IKOSA"); 개수 = (int)uburebure_agaciro; }
                else { 개수 = ibwiriza_amakurushingiro.네바이트(); if (개수 < 0 || 개수 > (ibwiriza_amakurushingiro.amakurushingiro.length - ibwiriza_amakurushingiro.위치) / 8) throw new Isemura_ikosa("switch Ingano IKOSA"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int agaciro = Icyo_wifuza == 170 ? 아래 + 순번 : ibwiriza_amakurushingiro.네바이트(), aho_ijya_agaciro = 위치 + ibwiriza_amakurushingiro.네바이트(); ishami_Urutonde.add(aho_ijya_agaciro);
                    Collections.addAll(umurongo,"cmpl $" + agaciro + ", %eax","je " + 표식 + "_b" + aho_ijya_agaciro);
                }
                umurongo.add("jmp " + 표식 + "_b" + agaciro_gasanzweho);
            } else if (Icyo_wifuza == 172 || Icyo_wifuza == 176 || Icyo_wifuza == 177) {
                if (Icyo_wifuza != 177) umurongo.add("popl %eax"); Collections.addAll(umurongo,"leave","ret");
            } else if (Icyo_wifuza == 178 || Icyo_wifuza == 179) {
                uburyo_Indanga Indanga = icyiciro_agaciro_55654bf1.Indanga(ibwiriza_amakurushingiro.두바이트()); if (!필드들.containsKey(Indanga)) throw new Isemura_ikosa("알 수 없는 umwanya_agaciro_0f39cf1c");
                Collections.addAll(umurongo,"call " + ikimenyetso("init",Indanga.nyirayo_agaciro),(Icyo_wifuza == 178 ? "pushl " : "popl ") + ikimenyetso("field",Indanga.부분들()));
            } else if (Icyo_wifuza == 184) {
                uburyo_Indanga Indanga = icyiciro_agaciro_55654bf1.Indanga(ibwiriza_amakurushingiro.두바이트()); if (!함수들.containsKey(Indanga)) throw new Isemura_ikosa("알 수 없는 FUNCTION_agaciro");
                함수형식 호출형식 = new 함수형식(Indanga.서술); Collections.addAll(umurongo,"call " + ikimenyetso("init",Indanga.nyirayo_agaciro),"call " + ikimenyetso("method",Indanga.부분들()));
                if (!호출형식.인수.isEmpty()) umurongo.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) umurongo.add("pushl %eax");
            } else if (Icyo_wifuza == 182) {
                uburyo_Indanga Indanga = icyiciro_agaciro_55654bf1.Indanga(ibwiriza_amakurushingiro.두바이트());
                if (Indanga.equals(new uburyo_Indanga("java/lang/String","length","()I"))) Collections.addAll(umurongo,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Indanga.equals(new uburyo_Indanga("java/lang/String","charAt","(I)C"))) Collections.addAll(umurongo,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Isemura_ikosa("가상 FUNCTION_agaciro 호출 미지원");
            } else if (Icyo_wifuza == 188) {
                if (ibwiriza_amakurushingiro.한바이트() != 10) throw new Isemura_ikosa("new int[]만 Ubufasha_agaciro"); Collections.addAll(umurongo,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Icyo_wifuza == 190) Collections.addAll(umurongo,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Icyo_wifuza == 196) {
                int umugereka_agaciro = ibwiriza_amakurushingiro.한바이트(), umugerekashakiro = ibwiriza_amakurushingiro.두바이트(); sheki_mu_gace(umugerekashakiro,지역수);
                if (umugereka_agaciro == 21 || umugereka_agaciro == 25 || umugereka_agaciro == 54 || umugereka_agaciro == 58) umurongo.add((umugereka_agaciro <= 25 ? "pushl " : "popl ") + "-" + 4 * (umugerekashakiro + 1) + "(%ebp)");
                else if (umugereka_agaciro == 132) umurongo.add("addl $" + ibwiriza_amakurushingiro.부호두바이트() + ", -" + 4 * (umugerekashakiro + 1) + "(%ebp)");
                else throw new Isemura_ikosa("wide Icyo_wifuza 미지원");
            } else if (Icyo_wifuza == 198 || Icyo_wifuza == 199) {
                int aho_ijya_agaciro = 위치 + ibwiriza_amakurushingiro.부호두바이트(); ishami_Urutonde.add(aho_ijya_agaciro); Collections.addAll(umurongo,"popl %eax","testl %eax, %eax",(Icyo_wifuza == 198 ? "je " : "jne ") + 표식 + "_b" + aho_ijya_agaciro);
            } else throw new Isemura_ikosa("미지원 Icyo_wifuza: " + Icyo_wifuza);
        }
        if (!경계들.containsAll(ishami_Urutonde)) throw new Isemura_ikosa("Icyo_wifuza 경계가 아닌 곳으로 ishami");
        umurongo.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",umurongo);
    }
    String 엑스상수(icyiciro_amakurushingiro amakurushingiro, int umugerekashakiro) {
        if (amakurushingiro.상수종류[umugerekashakiro] == 3) return amakurushingiro.kidahinduka_amakurushingiro[umugerekashakiro].toString();
        if (amakurushingiro.상수종류[umugerekashakiro] == 8) return igicenteruro_ikimenyetso(amakurushingiro.문자((Integer)amakurushingiro.kidahinduka_amakurushingiro[umugerekashakiro]));
        throw new Isemura_ikosa("정수와 igicenteruro_agaciro 상수만 Ubufasha_agaciro");
    }
    String 엑스조립본(String icyinjizwa_inota, List<String> 내보냄, String gusimbuza_igishya) throws IOException {
        Map<String,String> imashini_imbonerahamwe = new HashMap<>();
        for (String umurongo : Files.readAllLines(umutungo_inzira.resolve("엑스기계함수.tsv"))) { String[] guhuza_burutusi_agaciro = umurongo.split("\t"); if (guhuza_burutusi_agaciro[0].equals(gusimbuza_igishya)) imashini_imbonerahamwe.put(guhuza_burutusi_agaciro[1] + guhuza_burutusi_agaciro[2],guhuza_burutusi_agaciro[3]); }
        int 자리 = icyinjizwa_inota.lastIndexOf('.'); if (자리 < 0) throw new Isemura_ikosa("icyinjizwa_inota 지정 IKOSA");
        String nyirayo_agaciro = icyinjizwa_inota.substring(0,자리).replace('.','/'), uburyo_icyinjizwa_izina = icyinjizwa_inota.substring(자리 + 1); uburyo_Indanga icyinjizwa_inota_agaciro = null;
        for (String 서술 : Arrays.asList("()I","()V")) { uburyo_Indanga Indanga = new uburyo_Indanga(nyirayo_agaciro,uburyo_icyinjizwa_izina,서술); if (함수들.containsKey(Indanga)) { if (icyinjizwa_inota_agaciro != null) throw new Isemura_ikosa("겹친 icyinjizwa_inota"); icyinjizwa_inota_agaciro = Indanga; } }
        if (icyinjizwa_inota_agaciro == null || (함수들.get(icyinjizwa_inota_agaciro).kwinjira_icyinjizwa & 0x100) != 0) throw new Isemura_ikosa("icyinjizwa_inota_agaciro FUNCTION_agaciro imiterere_agaciro IKOSA");
        List<String> umurongo = new ArrayList<>(); umurongo.add(".code32");
        for (icyiciro_amakurushingiro amakurushingiro : 클래스들.values()) {
            String imimerere_agaciro = ikimenyetso("state",amakurushingiro.Izina), gutangiza = ikimenyetso("init",amakurushingiro.Izina);
            Collections.addAll(umurongo,".bss",".balign 4",imimerere_agaciro + ": .long 0",".text",gutangiza + ":","cmpl $0, " + imimerere_agaciro,"jne " + gutangiza + "_done","movl $1, " + imimerere_agaciro);
            uburyo_Indanga 초기화참조 = new uburyo_Indanga(amakurushingiro.Izina,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) umurongo.add("call " + ikimenyetso("method",초기화참조.부분들()));
            Collections.addAll(umurongo,"movl $2, " + imimerere_agaciro,gutangiza + "_done:","ret");
            for (ugize_itsinda_amakurushingiro umwanya_agaciro_0f39cf1c : amakurushingiro.umwanya_agaciro_0f39cf1c) {
                byte[] kidahinduka_agaciro = umwanya_agaciro_0f39cf1c.ikiranga_agaciro.get("ConstantValue"); String agaciro = kidahinduka_agaciro == null ? "0" : 엑스상수(amakurushingiro,new amakurushingiro_Musomyi(kidahinduka_agaciro).두바이트());
                Collections.addAll(umurongo,".data",".balign 4",ikimenyetso("field",amakurushingiro.Izina,umwanya_agaciro_0f39cf1c.Izina,umwanya_agaciro_0f39cf1c.서술) + ": .long " + agaciro);
            }
            for (ugize_itsinda_amakurushingiro FUNCTION_agaciro : amakurushingiro.FUNCTION_agaciro) if (!FUNCTION_agaciro.Izina.equals("<init>")) umurongo.add(엑스함수본문(new uburyo_Indanga(amakurushingiro.Izina,FUNCTION_agaciro.Izina,FUNCTION_agaciro.서술),FUNCTION_agaciro,imashini_imbonerahamwe,gusimbuza_igishya));
        }
        Collections.addAll(umurongo,".text",".globl java_entry","java_entry:","call " + ikimenyetso("init",icyinjizwa_inota_agaciro.nyirayo_agaciro),"call " + ikimenyetso("method",icyinjizwa_inota_agaciro.부분들()));
        if (icyinjizwa_inota_agaciro.서술.equals("()V")) umurongo.add("xorl %eax, %eax"); umurongo.add("ret");
        for (String 지정 : 내보냄) {
            int mutandukanya_agaciro_d8ba4873 = 지정.indexOf('='); if (mutandukanya_agaciro_d8ba4873 < 1) throw new Isemura_ikosa("내보내기 지정 IKOSA");
            String 외부 = 지정.substring(0,mutandukanya_agaciro_d8ba4873), FUNCTION_agaciro = 지정.substring(mutandukanya_agaciro_d8ba4873 + 1); int 나눔 = FUNCTION_agaciro.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Isemura_ikosa("내보내기 ikimenyetso IKOSA");
            String icyiciro_agaciro_55654bf1 = FUNCTION_agaciro.substring(0,나눔).replace('.','/'), Izina = FUNCTION_agaciro.substring(나눔 + 1); uburyo_Indanga ihitamo_agaciro = null;
            for (uburyo_Indanga Indanga : 함수들.keySet()) if (Indanga.nyirayo_agaciro.equals(icyiciro_agaciro_55654bf1) && Indanga.Izina.equals(Izina)) { if (ihitamo_agaciro != null) throw new Isemura_ikosa("겹친 내보내기 gusimbuza_igishya"); ihitamo_agaciro = Indanga; }
            if (ihitamo_agaciro == null) throw new Isemura_ikosa("내보낼 함수가 없음");
            Collections.addAll(umurongo,".text",".globl " + 외부,외부 + ":","call " + ikimenyetso("init",ihitamo_agaciro.nyirayo_agaciro),"jmp " + ikimenyetso("method",ihitamo_agaciro.부분들()));
        }
        umurongo.add(".section .rodata");
        for (Map.Entry<String,String> icyinjizwa_agaciro : 문자열들.entrySet()) {
            Collections.addAll(umurongo,".balign 4",icyinjizwa_agaciro.getValue() + ":",".long " + icyinjizwa_agaciro.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char ibinyabumwe_agaciro : icyinjizwa_agaciro.getKey().toCharArray()) 단위들.add(Integer.toString(ibinyabumwe_agaciro)); if (!단위들.isEmpty()) umurongo.add(".long " + String.join(",",단위들));
        }
        umurongo.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",umurongo) + "\n";
    }
    static void gukora_igikoresho(List<String> Icyo_wifuza) throws Exception {
        if (new ProcessBuilder(Icyo_wifuza).inheritIO().start().waitFor() != 0) throw new Isemura_ikosa("gusohora_inkomoko IKOSA: " + Icyo_wifuza.get(0));
    }
    static String amakurushingiro_igicenteruro(String Umwandiko) { return "\"" + Umwandiko.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String gusimbuza_igishya, String icyinjizwa_inota, List<String> 내보냄, Path 출력, Path umutungo_agaciro) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), icyiciro_inzira = 임시.resolve("classes"); Files.createDirectory(icyiciro_inzira);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",icyiciro_inzira.toString(),"-sourcepath",icyiciro_inzira.toString(),"-d",icyiciro_inzira.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Isemura_ikosa("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Isemura_ikosa(".java 또는 .class만 Ubufasha_agaciro");
            }
            if (원문수 > 0) gukora_igikoresho(자바명령);
            try (java.util.stream.Stream<Path> inzira_Urutonde = Files.walk(icyiciro_inzira)) { inzira_Urutonde.filter(Inzira -> Inzira.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,gusimbuza_igishya.equals("user") ? "user" : "kernel",262144,umutungo_agaciro);
            String 조립 = 변환.엑스조립본(icyinjizwa_inota,내보냄,gusimbuza_igishya); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = umutungo_agaciro.getParent();
            gukora_igikoresho(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            gukora_igikoresho(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("igihe_ururimi_rukorwamo_Ubufasha.s").toString()));
            List<String> Guhuza = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (gusimbuza_igishya.equals("kernel")) Guhuza.add("-r");
            else {
                gukora_igikoresho(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(gusimbuza_igishya.equals("user") ? "Itangira_ukoresha_porogaramu.s" : "리눅스시작.s").toString()));
                Collections.addAll(Guhuza,"-e","_start",임시.resolve("start.o").toString());
                if (gusimbuza_igishya.equals("user")) Collections.addAll(Guhuza,"-T",도구위치.resolve("ukoresha_Ihuza_Imimerere.ld").toString());
            }
            Collections.addAll(Guhuza,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); gukora_igikoresho(Guhuza);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path gutangaza_agaciro = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),gutangaza_agaciro,StandardCopyOption.REPLACE_EXISTING); Files.move(gutangaza_agaciro,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(gutangaza_agaciro); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(gusimbuza_igishya.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> ikimenyetso_amakurushingiro = new ArrayList<>(), ahavuye_amakuru = new ArrayList<>();
            for (uburyo_Indanga Indanga : 변환.함수들.keySet()) ikimenyetso_amakurushingiro.add(amakurushingiro_igicenteruro(ikimenyetso("method",Indanga.부분들())) + ":" + amakurushingiro_igicenteruro(Indanga.nyirayo_agaciro + "." + Indanga.Izina + Indanga.서술));
            for (Path 입력 : 입력들) {
                byte[] hashi_dosiye = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Umwandiko = new StringBuilder(); for (byte agaciro : hashi_dosiye) Umwandiko.append(String.format(Locale.ROOT,"%02x",agaciro & 255));
                ahavuye_amakuru.add(amakurushingiro_igicenteruro(입력.toAbsolutePath().toString()) + ":" + amakurushingiro_igicenteruro(Umwandiko.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + amakurushingiro_igicenteruro(gusimbuza_igishya) + ",\"entry\":" + amakurushingiro_igicenteruro(icyinjizwa_inota) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",ikimenyetso_amakurushingiro) + "},\"sources\":{" + String.join(",",ahavuye_amakuru) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> inzira_Urutonde = Files.walk(임시)) { for (Path Inzira : (Iterable<Path>)inzira_Urutonde.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Inzira); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String icyinjizwa_inota = null, gusimbuza_igishya = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> inzira_Urutonde = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String agaciro = 인수[순번];
                switch (agaciro) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry icyiciro_agaciro_55654bf1.FUNCTION_agaciro -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export ikimenyetso=icyiciro_agaciro_55654bf1.FUNCTION_agaciro] 클래스파일 또는 Java원문"); return;
                    case "--entry": icyinjizwa_inota = 인수[++순번]; break;
                    case "--profile": gusimbuza_igishya = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (agaciro.startsWith("-")) throw new Isemura_ikosa("알 수 없는 옵션: " + agaciro); inzira_Urutonde.add(Paths.get(agaciro));
                }
            }
            if (icyinjizwa_inota == null || 출력경로 == null || inzira_Urutonde.isEmpty()) throw new Isemura_ikosa("--entry, -o, icyiciro_agaciro_55654bf1 파일이 필요합니다");
            Path umutungo_agaciro = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Isemura_ikosa("알 수 없는 gukora_ibwiriza gusimbuza_igishya");
                엑스번역(inzira_Urutonde,엑스대상,icyinjizwa_inota,내보냄,출력경로,umutungo_agaciro); return;
            }
            String Inkomoko = new 기계어미리번역(inzira_Urutonde, gusimbuza_igishya, 낱말수, umutungo_agaciro).생성(icyinjizwa_inota, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, Inkomoko, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception IKOSA) { System.err.println("gusohora_inkomoko IKOSA: " + IKOSA.getMessage()); System.exit(1); }
    }
}
