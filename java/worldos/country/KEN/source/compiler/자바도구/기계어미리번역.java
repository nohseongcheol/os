// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java tabaka_thamani_55654bf1 파일에서 독립 ARM64 커널용 C 원문을 만든다. mwenyeji JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Tafsiri_kosa extends RuntimeException {
        Tafsiri_kosa(String 설명) { super(설명); }
    }
    static final class data_msomaji {
        final byte[] data;
        int 위치;
        data_msomaji(byte[] 입력자료) { data = 입력자료; }
        byte[] 읽기(int urefu_thamani) {
            if (urefu_thamani < 0 || urefu_thamani > data.length - 위치) throw new Tafsiri_kosa("잘린 tabaka_thamani_55654bf1 또는 amri data");
            byte[] 결과 = Arrays.copyOfRange(data, 위치, 위치 + urefu_thamani); 위치 += urefu_thamani; return 결과;
        }
        int 한바이트() { if (위치 >= data.length) throw new Tafsiri_kosa("잘린 amri data"); return data[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class mwanachama_data {
        final int fikia_ingizo;
        final String Jina, 서술;
        final Map<String, byte[]> sifa_thamani;
        mwanachama_data(int fikia_thamani, String jina_thamani, String 서술값, Map<String, byte[]> sifa_data) {
            fikia_ingizo = fikia_thamani; Jina = jina_thamani; 서술 = 서술값; sifa_thamani = sifa_data;
        }
    }
    static final class mbinu_Marejeleo implements Comparable<mbinu_Marejeleo> {
        final String mmiliki_thamani, Jina, 서술;
        mbinu_Marejeleo(String 소유값, String jina_thamani, String 서술값) { mmiliki_thamani = 소유값; Jina = jina_thamani; 서술 = 서술값; }
        String[] 부분들() { return new String[]{mmiliki_thamani, Jina, 서술}; }
        public int compareTo(mbinu_Marejeleo kompyuta_rika_thamani) {
            int Kulinganisha_thamani = mmiliki_thamani.compareTo(kompyuta_rika_thamani.mmiliki_thamani);
            if (Kulinganisha_thamani == 0) Kulinganisha_thamani = Jina.compareTo(kompyuta_rika_thamani.Jina);
            return Kulinganisha_thamani == 0 ? 서술.compareTo(kompyuta_rika_thamani.서술) : Kulinganisha_thamani;
        }
        public boolean equals(Object kompyuta_rika_thamani) { return kompyuta_rika_thamani instanceof mbinu_Marejeleo && compareTo((mbinu_Marejeleo) kompyuta_rika_thamani) == 0; }
        public int hashCode() { return Objects.hash(mmiliki_thamani, Jina, 서술); }
    }
    static final class tabaka_data {
        final int[] 상수종류;
        final Object[] kisobadilika_data;
        final String Jina;
        final List<mwanachama_data> uga_thamani, KITENDAKAZI_thamani;
        tabaka_data(Path njia) throws IOException {
            data_msomaji msomaji_thamani = new data_msomaji(Files.readAllBytes(njia));
            if (msomaji_thamani.네바이트() != 0xcafebabe) throw new Tafsiri_kosa("Java tabaka_thamani_55654bf1 표식이 아님");
            msomaji_thamani.읽기(4);
            int 개수 = msomaji_thamani.두바이트(); 상수종류 = new int[개수]; kisobadilika_data = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = msomaji_thamani.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int urefu_thamani = msomaji_thamani.두바이트();
                        byte[] kibambo_bafa = msomaji_thamani.읽기(urefu_thamani), 길이붙인자료 = new byte[urefu_thamani + 2];
                        길이붙인자료[0] = (byte)(urefu_thamani >> 8); 길이붙인자료[1] = (byte)urefu_thamani;
                        System.arraycopy(kibambo_bafa, 0, 길이붙인자료, 2, urefu_thamani);
                        kisobadilika_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: kisobadilika_data[순번] = msomaji_thamani.네바이트(); break;
                    case 4: msomaji_thamani.읽기(4); break;
                    case 5: case 6: msomaji_thamani.읽기(8); 순번++; break;
                    case 7: case 8: case 16: kisobadilika_data[순번] = msomaji_thamani.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        kisobadilika_data[순번] = new int[]{msomaji_thamani.두바이트(), msomaji_thamani.두바이트()}; break;
                    case 15: kisobadilika_data[순번] = new int[]{msomaji_thamani.한바이트(), msomaji_thamani.두바이트()}; break;
                    default: throw new Tafsiri_kosa("지원하지 않는 kisobadilika_thamani 종류: " + 종류);
                }
            }
            msomaji_thamani.두바이트(); Jina = tabaka_jina(msomaji_thamani.두바이트());
            if (!tabaka_jina(msomaji_thamani.두바이트()).equals("java/lang/Object") || msomaji_thamani.두바이트() != 0)
                throw new Tafsiri_kosa(Jina + ": 상속 및 인터페이스 미지원");
            uga_thamani = 멤버읽기(msomaji_thamani); KITENDAKAZI_thamani = 멤버읽기(msomaji_thamani); 속성읽기(msomaji_thamani);
            if (msomaji_thamani.위치 != msomaji_thamani.data.length) throw new Tafsiri_kosa("tabaka_thamani_55654bf1 뒤에 남은 data");
        }
        String 문자(int kielezo) {
            if (kielezo < 1 || kielezo >= 상수종류.length || 상수종류[kielezo] != 1) throw new Tafsiri_kosa("문자 kisobadilika_thamani kielezo kosa");
            return (String) kisobadilika_data[kielezo];
        }
        String tabaka_jina(int kielezo) {
            if (kielezo < 1 || kielezo >= 상수종류.length || 상수종류[kielezo] != 7) throw new Tafsiri_kosa("tabaka_thamani_55654bf1 Marejeleo kosa");
            return 문자((Integer)kisobadilika_data[kielezo]);
        }
        mbinu_Marejeleo Marejeleo(int kielezo) {
            if (kielezo < 1 || kielezo >= 상수종류.length || 상수종류[kielezo] < 9 || 상수종류[kielezo] > 11) throw new Tafsiri_kosa("멤버 Marejeleo kosa");
            int[] unganisha_thamani = (int[])kisobadilika_data[kielezo], jina_unganisha = (int[])kisobadilika_data[unganisha_thamani[1]];
            return new mbinu_Marejeleo(tabaka_jina(unganisha_thamani[0]), 문자(jina_unganisha[0]), 문자(jina_unganisha[1]));
        }
        Map<String, byte[]> 속성읽기(data_msomaji msomaji_thamani) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = msomaji_thamani.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String sifa_jina = 문자(msomaji_thamani.두바이트()); byte[] thamani = msomaji_thamani.읽기(msomaji_thamani.네바이트());
                if (결과.put(sifa_jina, thamani) != null) throw new Tafsiri_kosa("겹친 sifa_thamani: " + sifa_jina);
            }
            return 결과;
        }
        List<mwanachama_data> 멤버읽기(data_msomaji msomaji_thamani) {
            List<mwanachama_data> 결과 = new ArrayList<>(); int 개수 = msomaji_thamani.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int fikia_ingizo = msomaji_thamani.두바이트(); String mbinu_ingizo_jina = 문자(msomaji_thamani.두바이트()), 서술 = 문자(msomaji_thamani.두바이트());
                결과.add(new mwanachama_data(fikia_ingizo, mbinu_ingizo_jina, 서술, 속성읽기(msomaji_thamani)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Tafsiri_kosa("KITENDAKAZI_thamani 서술 kosa: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Tafsiri_kosa("KITENDAKAZI_thamani 서술 kosa: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Tafsiri_kosa("KITENDAKAZI_thamani 서술 kosa: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String uteuzi_thamani = null;
            for (String umbiza_thamani : 허용형식) if (서술.startsWith(umbiza_thamani, 위치)) { uteuzi_thamani = umbiza_thamani; break; }
            if (uteuzi_thamani == null) throw new Tafsiri_kosa("지원하지 않는 aina_ya_data: " + 서술);
            결과.add(uteuzi_thamani); 위치 += uteuzi_thamani.length();
        }
        return 결과;
    }
    static String ishara(String 종류, String... 부분들) {
        try {
            byte[] kali_faili = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", kali_faili[순번] & 255));
            return SMS.toString();
        } catch (Exception kosa) { throw new Tafsiri_kosa(kosa.toString()); }
    }
    final Map<String, tabaka_data> 클래스들 = new TreeMap<>();
    final Map<mbinu_Marejeleo, mwanachama_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, mashine_tabaka;
    final int 동적기억낱말수;
    final Path rasilimali_njia;
    기계어미리번역(List<Path> njia_Orodha, String lengo, int 낱말수, Path rasilimali_thamani) throws IOException {
        if ((!lengo.equals("kernel") && !lengo.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Tafsiri_kosa("tekeleza_amri lengo 또는 kumbukumbu_thamani_603669bd 공간 panga_ukubwa kosa");
        실행대상 = lengo; 동적기억낱말수 = 낱말수; rasilimali_njia = rasilimali_thamani;
        // 이 이름도 국가별 chanzo_mti 생성 시 해당 언어로 옮긴다.
        mashine_tabaka = lengo.equals("kernel") ? "보드" : "mtumiaji";
        for (String laini : Files.readAllLines(rasilimali_thamani.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = laini.split("\t", -1);
            if (부분들.length != 4) throw new Tafsiri_kosa("mashine KITENDAKAZI_thamani data kosa");
            if (부분들[0].equals(lengo)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path njia : njia_Orodha) {
            tabaka_data data = new tabaka_data(njia);
            if (클래스들.put(data.Jina, data) != null) throw new Tafsiri_kosa("중복 tabaka_thamani_55654bf1: " + data.Jina);
            for (mwanachama_data uga_thamani : data.uga_thamani) {
                if ((uga_thamani.fikia_ingizo & 8) == 0 || 형식읽기(uga_thamani.서술).equals(Collections.singletonList("V"))) throw new Tafsiri_kosa("tuli_thamani 필드만 Auni_thamani");
                if (필드들.put(new mbinu_Marejeleo(data.Jina, uga_thamani.Jina, uga_thamani.서술), uga_thamani) != null) throw new Tafsiri_kosa("중복 uga_thamani");
            }
            for (mwanachama_data KITENDAKAZI_thamani : data.KITENDAKAZI_thamani) {
                if (KITENDAKAZI_thamani.Jina.equals("<init>")) continue;
                if ((KITENDAKAZI_thamani.fikia_ingizo & 8) == 0 || (KITENDAKAZI_thamani.fikia_ingizo & (0x20 | 0x400)) != 0) throw new Tafsiri_kosa("tuli_thamani 비동기화 함수만 Auni_thamani");
                new 함수형식(KITENDAKAZI_thamani.서술);
                if (함수들.put(new mbinu_Marejeleo(data.Jina, KITENDAKAZI_thamani.Jina, KITENDAKAZI_thamani.서술), KITENDAKAZI_thamani) != null) throw new Tafsiri_kosa("중복 KITENDAKAZI_thamani");
            }
        }
    }
    String tungo_ishara(String SMS) { return 문자열들.computeIfAbsent(SMS, thamani -> "j_text_" + 문자열들.size()); }
    String kisobadilika_usemi(tabaka_data data, int kielezo) {
        if (kielezo < 1 || kielezo >= data.상수종류.length) throw new Tafsiri_kosa("kisobadilika_thamani kielezo dondoo kosa");
        if (data.상수종류[kielezo] == 3) return "(word)(uint32_t)(" + data.kisobadilika_data[kielezo] + ")";
        if (data.상수종류[kielezo] == 8) return "(word)" + tungo_ishara(data.문자((Integer)data.kisobadilika_data[kielezo]));
        throw new Tafsiri_kosa("정수와 tungo_thamani 상수만 Auni_thamani");
    }
    String 함수원형(mbinu_Marejeleo Marejeleo) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Marejeleo.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + ishara("method", Marejeleo.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void hundi_jirani(int kielezo, int 지역변수수) { if (kielezo < 0 || kielezo >= 지역변수수) throw new Tafsiri_kosa("jirani_upeo 변수 kielezo dondoo kosa"); }
    void 분기넣기(List<String> 출력, Set<Integer> tawi_Orodha, int 위치, int 이동량, String sharti) {
        int fikio_thamani = 위치 + 이동량; tawi_Orodha.add(fikio_thamani);
        출력.add((sharti == null ? "" : "if (" + sharti + ") ") + "goto b" + fikio_thamani + ";");
    }
    String mbinu_kiini(mbinu_Marejeleo KITENDAKAZI_thamani, mwanachama_data data) {
        byte[] kiini_data = data.sifa_thamani.get("Code"); if (kiini_data == null) throw new Tafsiri_kosa("KITENDAKAZI_thamani 몸체가 없음: " + KITENDAKAZI_thamani.Jina);
        data_msomaji msomaji_thamani = new data_msomaji(kiini_data); int 쌓임깊이 = msomaji_thamani.두바이트(), 지역변수수 = msomaji_thamani.두바이트();
        data_msomaji amri_data = new data_msomaji(msomaji_thamani.읽기(msomaji_thamani.네바이트()));
        if (msomaji_thamani.두바이트() != 0) throw new Tafsiri_kosa("try/catch/finally 미지원");
        함수형식 umbiza_thamani = new 함수형식(KITENDAKAZI_thamani.서술); if (지역변수수 < umbiza_thamani.인수.size()) throw new Tafsiri_kosa("매개변수보다 적은 jirani_upeo 변수");
        tabaka_data tabaka_thamani_55654bf1 = 클래스들.get(KITENDAKAZI_thamani.mmiliki_thamani);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(KITENDAKAZI_thamani) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < umbiza_thamani.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), tawi_Orodha = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (amri_data.위치 < amri_data.data.length) {
            int 위치 = amri_data.위치, amri = amri_data.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (amri == 0) continue;
            if (amri == 1) 출력.add("PUSH(0);");
            else if (amri >= 2 && amri <= 8) 출력.add("PUSH((uint32_t)(" + (amri - 3) + "));");
            else if (amri == 16 || amri == 17) 출력.add("PUSH((uint32_t)(" + (amri == 16 ? amri_data.부호한바이트() : amri_data.부호두바이트()) + "));");
            else if (amri == 18 || amri == 19) 출력.add("PUSH(" + kisobadilika_usemi(tabaka_thamani_55654bf1, amri == 18 ? amri_data.한바이트() : amri_data.두바이트()) + ");");
            else if (amri == 21 || amri == 25 || (amri >= 26 && amri <= 29) || (amri >= 42 && amri <= 45)) {
                int kielezo = amri == 21 || amri == 25 ? amri_data.한바이트() : amri - (amri <= 29 ? 26 : 42);
                hundi_jirani(kielezo, 지역변수수); 출력.add("PUSH(l[" + kielezo + "]);");
            } else if (amri == 54 || amri == 58 || (amri >= 59 && amri <= 62) || (amri >= 75 && amri <= 78)) {
                int kielezo = amri == 54 || amri == 58 ? amri_data.한바이트() : amri - (amri <= 62 ? 59 : 75);
                hundi_jirani(kielezo, 지역변수수); 출력.add("l[" + kielezo + "] = POP();");
            } else if (amri == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (amri == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (amri == 87 || amri == 88) 출력.add(amri == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (amri >= 89 && amri <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] mpangilio_Orodha = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[amri - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char thamani : mpangilio_Orodha[amri - 89].toCharArray()) 출력.add("PUSH(" + thamani + ");");
            } else if (amri == 96 || amri == 100 || amri == 104 || amri == 126 || amri == 128 || amri == 130) {
                String upasuaji_thamani = amri == 96 ? "+" : amri == 100 ? "-" : amri == 104 ? "*" : amri == 126 ? "&" : amri == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + upasuaji_thamani + " (uint32_t)b);");
            } else if (amri == 108 || amri == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (amri == 112 ? 1 : 0) + "));");
            else if (amri == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (amri == 120 || amri == 122 || amri == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (amri == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (amri == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (amri == 132) {
                int kielezo = amri_data.한바이트(), 증가량 = amri_data.부호한바이트(); hundi_jirani(kielezo, 지역변수수);
                출력.add("l[" + kielezo + "] = (uint32_t)l[" + kielezo + "] + (uint32_t)(" + 증가량 + ");");
            } else if (amri >= 145 && amri <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (amri == 145 ? "int8_t" : amri == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (amri >= 153 && amri <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, tawi_Orodha, 위치, amri_data.부호두바이트(), "(int32_t)a " + 비교들[amri - 153] + " 0");
            } else if (amri >= 159 && amri <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, tawi_Orodha, 위치, amri_data.부호두바이트(), amri >= 165 ? "a " + 비교들[amri - 159] + " b" : "(int32_t)a " + 비교들[amri - 159] + " (int32_t)b");
            } else if (amri == 167 || amri == 200) 분기넣기(출력, tawi_Orodha, 위치, amri == 167 ? amri_data.부호두바이트() : amri_data.네바이트(), null);
            else if (amri == 170 || amri == 171) {
                while (amri_data.위치 % 4 != 0) amri_data.한바이트();
                int hali_ya_chaguo_msingi = amri_data.네바이트(); 출력.add("a = POP();");
                if (amri == 170) {
                    int 아래 = amri_data.네바이트(), 위 = amri_data.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (amri_data.data.length - amri_data.위치) / 4) throw new Tafsiri_kosa("switch dondoo kosa");
                    for (long thamani = 아래; thamani <= 위; thamani++) 분기넣기(출력, tawi_Orodha, 위치, amri_data.네바이트(), "(int32_t)a == (" + thamani + ")");
                } else {
                    int 개수 = amri_data.네바이트(), mbele_data = 0;
                    if (개수 < 0 || 개수 > (amri_data.data.length - amri_data.위치) / 8) throw new Tafsiri_kosa("switch panga_ukubwa kosa");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int thamani = amri_data.네바이트(); if (순번 > 0 && thamani <= mbele_data) throw new Tafsiri_kosa("switch mpangilio_thamani kosa"); mbele_data = thamani;
                        분기넣기(출력, tawi_Orodha, 위치, amri_data.네바이트(), "(int32_t)a == (" + thamani + ")");
                    }
                }
                분기넣기(출력, tawi_Orodha, 위치, hali_ya_chaguo_msingi, null);
            } else if (amri == 172 || amri == 176 || amri == 177) 출력.add("return " + (amri == 177 ? "0" : "POP()") + ";");
            else if (amri == 178 || amri == 179) {
                mbinu_Marejeleo Marejeleo = tabaka_thamani_55654bf1.Marejeleo(amri_data.두바이트()); if (!필드들.containsKey(Marejeleo)) throw new Tafsiri_kosa("알 수 없는 uga_thamani");
                출력.add(ishara("init", Marejeleo.mmiliki_thamani) + "();"); String uga_thamani = ishara("field", Marejeleo.부분들());
                출력.add(amri == 178 ? "PUSH(" + uga_thamani + ");" : uga_thamani + " = POP();");
            } else if (amri == 184) {
                mbinu_Marejeleo Marejeleo = tabaka_thamani_55654bf1.Marejeleo(amri_data.두바이트()); if (!함수들.containsKey(Marejeleo)) throw new Tafsiri_kosa("알 수 없는 KITENDAKAZI_thamani");
                함수형식 호출형식 = new 함수형식(Marejeleo.서술); int 개수 = 호출형식.인수.size();
                출력.add(ishara("init", Marejeleo.mmiliki_thamani) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + ishara("method", Marejeleo.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (amri == 182) {
                mbinu_Marejeleo Marejeleo = tabaka_thamani_55654bf1.Marejeleo(amri_data.두바이트());
                if (Marejeleo.equals(new mbinu_Marejeleo("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Marejeleo.equals(new mbinu_Marejeleo("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Tafsiri_kosa("가상 KITENDAKAZI_thamani 호출 미지원");
            } else if (amri == 188) {
                if (amri_data.한바이트() != 10) throw new Tafsiri_kosa("new int[]만 Auni_thamani"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (amri == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (amri == 196) {
                int kiendelezi_thamani = amri_data.한바이트(), kielezo = amri_data.두바이트(); hundi_jirani(kielezo, 지역변수수);
                if (kiendelezi_thamani == 21 || kiendelezi_thamani == 25) 출력.add("PUSH(l[" + kielezo + "]);");
                else if (kiendelezi_thamani == 54 || kiendelezi_thamani == 58) 출력.add("l[" + kielezo + "] = POP();");
                else if (kiendelezi_thamani == 132) 출력.add("l[" + kielezo + "] = (uint32_t)l[" + kielezo + "] + (uint32_t)(" + amri_data.부호두바이트() + ");");
                else throw new Tafsiri_kosa("미지원 wide amri");
            } else if (amri == 198 || amri == 199) {
                출력.add("a = POP();"); 분기넣기(출력, tawi_Orodha, 위치, amri_data.부호두바이트(), "a " + (amri == 198 ? "==" : "!=") + " 0");
            } else throw new Tafsiri_kosa(KITENDAKAZI_thamani.mmiliki_thamani + "." + KITENDAKAZI_thamani.Jina + ", baiti_thamani " + 위치 + ": 미지원 amri " + amri);
        }
        if (!경계들.containsAll(tawi_Orodha)) throw new Tafsiri_kosa("amri 경계가 아닌 곳으로 tawi");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String hamisha_mbinu(String Kiungo_ishara, String lengo, boolean 진입점여부) {
        int 자리 = lengo.lastIndexOf('.'); if (자리 < 0 || !Kiungo_ishara.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tafsiri_kosa("내보내기 pangia_thamani kosa");
        String mmiliki_thamani = lengo.substring(0, 자리).replace('.', '/'), Jina = lengo.substring(자리 + 1); mbinu_Marejeleo uteuzi_thamani = null;
        for (mbinu_Marejeleo Marejeleo : 함수들.keySet()) if (Marejeleo.mmiliki_thamani.equals(mmiliki_thamani) && Marejeleo.Jina.equals(Jina)) {
            if (uteuzi_thamani != null) throw new Tafsiri_kosa("겹친 내보내기 lengo"); uteuzi_thamani = Marejeleo;
        }
        if (uteuzi_thamani == null || (함수들.get(uteuzi_thamani).fikia_ingizo & 0x100) != 0) throw new Tafsiri_kosa("내보낼 함수가 없음 또는 native KITENDAKAZI_thamani");
        함수형식 umbiza_thamani = new 함수형식(uteuzi_thamani.서술);
        if ((진입점여부 && !umbiza_thamani.인수.isEmpty()) || !Arrays.asList("V", "I").contains(umbiza_thamani.반환)) throw new Tafsiri_kosa("ingizo_pointi_thamani 또는 C 경계 umbiza_thamani kosa");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < umbiza_thamani.인수.size(); 순번++) {
            if (!umbiza_thamani.인수.get(순번).equals("I")) throw new Tafsiri_kosa("C 경계는 int 인수만 Auni_thamani");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (umbiza_thamani.반환.equals("V") ? "void " : "int32_t ") + Kiungo_ishara + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + ishara("init", uteuzi_thamani.mmiliki_thamani) + "(); " + (umbiza_thamani.반환.equals("V") ? "" : "return (int32_t)") + ishara("method", uteuzi_thamani.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String ingizo_pointi, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<mbinu_Marejeleo, mwanachama_data> ingizo_thamani : 함수들.entrySet()) {
            mbinu_Marejeleo Marejeleo = ingizo_thamani.getKey(); mwanachama_data data = ingizo_thamani.getValue(); 선언들.add(함수원형(Marejeleo) + ";");
            if ((data.fikia_ingizo & 0x100) != 0) {
                String UNGANISHA = 기계함수들.get(Marejeleo.Jina + Marejeleo.서술);
                if (!Marejeleo.mmiliki_thamani.equals(mashine_tabaka) || UNGANISHA == null) throw new Tafsiri_kosa("허용되지 않은 native KITENDAKAZI_thamani: " + Marejeleo.Jina);
                int 개수 = new 함수형식(Marejeleo.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + UNGANISHA + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Marejeleo) + " { return " + UNGANISHA + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(mbinu_kiini(Marejeleo, data));
        }
        for (Map.Entry<mbinu_Marejeleo, mwanachama_data> ingizo_thamani : 필드들.entrySet()) {
            mbinu_Marejeleo Marejeleo = ingizo_thamani.getKey(); byte[] kisobadilika_thamani = ingizo_thamani.getValue().sifa_thamani.get("ConstantValue");
            String thamani = kisobadilika_thamani == null ? "0" : kisobadilika_usemi(클래스들.get(Marejeleo.mmiliki_thamani), new data_msomaji(kisobadilika_thamani).두바이트());
            필드선언들.add("static word " + ishara("field", Marejeleo.부분들()) + " = " + thamani + ";");
        }
        for (String Jina : 클래스들.keySet()) {
            String anzilisha = ishara("init", Jina), hali_thamani = ishara("state", Jina);
            선언들.add("static void " + anzilisha + "(void);"); 필드선언들.add("static unsigned " + hali_thamani + ";");
            mbinu_Marejeleo Marejeleo = new mbinu_Marejeleo(Jina, "<clinit>", "()V");
            몸체들.add("static void " + anzilisha + "(void) { if(" + hali_thamani + ") return; " + hali_thamani + " = 1; " + (함수들.containsKey(Marejeleo) ? ishara("method", Marejeleo.부분들()) + "(); " : "") + hali_thamani + " = 2; }");
        }
        몸체들.add(hamisha_mbinu("java_entry", ingizo_pointi, true)); Set<String> 공개이름 = new HashSet<>();
        for (String pangia_thamani : 내보내기목록) {
            int 자리 = pangia_thamani.indexOf('='); if (자리 < 1) throw new Tafsiri_kosa("내보내기 pangia_thamani kosa");
            String Jina = pangia_thamani.substring(0, 자리); 공개이름.add(Jina); 몸체들.add(hamisha_mbinu(Jina, pangia_thamani.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> ingizo_thamani : 문자열들.entrySet()) {
            String SMS = ingizo_thamani.getKey(); StringBuilder ARRAY_thamani = new StringBuilder("static const word " + ingizo_thamani.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) ARRAY_thamani.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(ARRAY_thamani.append("};").toString());
        }
        String Auni_thamani = Files.readString(rasilimali_njia.resolve("muda_wa_kuendesha_lugha_ya_kawaida_Auni.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Auni_thamani + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String chanzo, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> jina_jedwali = new HashMap<>();
        for (String laini : Files.readAllLines(rasilimali_njia.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] unganisha_thamani = laini.split("\t"); jina_jedwali.put(unganisha_thamani[0], unganisha_thamani[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(chanzo); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Jina = 찾개.group(), 새이름 = Jina;
            if (!Jina.startsWith("//") && !Jina.startsWith("/*") && !Jina.startsWith("\"") && !Jina.startsWith("'") && !공개이름.contains(Jina)) {
                새이름 = jina_jedwali.getOrDefault(Jina, Jina);
                if (Jina.matches("a[0-9]+")) 새이름 = "인수" + Jina.substring(1);
                if (Jina.matches("b[0-9]+")) 새이름 = "tawi" + Jina.substring(1);
                if (범용표기) {
                    StringBuilder nukuu_thamani = new StringBuilder();
                    for (char kibambo_thamani : 새이름.toCharArray()) nukuu_thamani.append(kibambo_thamani < 128 ? Character.toString(kibambo_thamani) : String.format(Locale.ROOT, "\\u%04x", (int)kibambo_thamani));
                    새이름 = nukuu_thamani.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String Kitufe_cha_X_86_mbinu_kiini(mbinu_Marejeleo KITENDAKAZI_thamani, mwanachama_data data, Map<String,String> mashine_jedwali, String lengo) {
        String 표식 = ishara("method", KITENDAKAZI_thamani.부분들());
        List<String> laini = new ArrayList<>();
        if ((data.fikia_ingizo & 0x100) != 0) {
            String UNGANISHA = mashine_jedwali.get(KITENDAKAZI_thamani.Jina + KITENDAKAZI_thamani.서술);
            if (!KITENDAKAZI_thamani.mmiliki_thamani.equals(lengo.equals("kernel") ? "kifaa_thamani" : "mtumiaji") || UNGANISHA == null) throw new Tafsiri_kosa("허용되지 않은 native KITENDAKAZI_thamani");
            return ".text\n" + 표식 + ":\njmp " + UNGANISHA;
        }
        byte[] Matini_kiini = data.sifa_thamani.get("Code"); if (Matini_kiini == null) throw new Tafsiri_kosa("KITENDAKAZI_thamani 몸체가 없음");
        data_msomaji msomaji_thamani = new data_msomaji(Matini_kiini); msomaji_thamani.두바이트(); int 지역수 = msomaji_thamani.두바이트();
        data_msomaji amri_data = new data_msomaji(msomaji_thamani.읽기(msomaji_thamani.네바이트()));
        if (msomaji_thamani.두바이트() != 0) throw new Tafsiri_kosa("try/catch/finally 미지원");
        함수형식 umbiza_thamani = new 함수형식(KITENDAKAZI_thamani.서술); if (지역수 < umbiza_thamani.인수.size()) throw new Tafsiri_kosa("매개변수보다 적은 jirani_upeo 변수");
        Collections.addAll(laini,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < umbiza_thamani.인수.size(); 순번++) Collections.addAll(laini,"movl " + (8 + 4 * (umbiza_thamani.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        tabaka_data tabaka_thamani_55654bf1 = 클래스들.get(KITENDAKAZI_thamani.mmiliki_thamani); Set<Integer> 경계들 = new HashSet<>(), tawi_Orodha = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (amri_data.위치 < amri_data.data.length) {
            int 위치 = amri_data.위치, amri = amri_data.한바이트(); String 자리 = 표식 + "_b" + 위치;
            laini.add(자리 + ":"); 경계들.add(위치);
            if (amri == 0) laini.add("nop");
            else if (amri == 1) laini.add("pushl $0");
            else if (amri >= 2 && amri <= 8) laini.add("pushl $" + (amri - 3));
            else if (amri == 16 || amri == 17) laini.add("pushl $" + (amri == 16 ? amri_data.부호한바이트() : amri_data.부호두바이트()));
            else if (amri == 18 || amri == 19) {
                int kielezo = amri == 18 ? amri_data.한바이트() : amri_data.두바이트();
                laini.add("pushl $" + Kitufe_cha_X_86_kisobadilika(tabaka_thamani_55654bf1,kielezo));
            } else if (amri == 21 || amri == 25 || (amri >= 26 && amri <= 29) || (amri >= 42 && amri <= 45) || amri == 54 || amri == 58 || (amri >= 59 && amri <= 62) || (amri >= 75 && amri <= 78)) {
                boolean 읽음 = amri < 54; int kielezo = amri == 21 || amri == 25 || amri == 54 || amri == 58 ? amri_data.한바이트() : amri - (amri <= 29 ? 26 : amri <= 45 ? 42 : amri <= 62 ? 59 : 75);
                hundi_jirani(kielezo,지역수); laini.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (kielezo + 1)) + "(%ebp)");
            } else if (amri == 46) Collections.addAll(laini,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (amri == 79) Collections.addAll(laini,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (amri == 87 || amri == 88) laini.add("addl $" + (amri == 87 ? 4 : 8) + ", %esp");
            else if (amri >= 89 && amri <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] mpangilio_Orodha = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[amri - 89]; 순번++) laini.add("popl " + 저장기들[순번]);
                for (int 순번 : mpangilio_Orodha[amri - 89]) laini.add("pushl " + 저장기들[순번]);
            } else if (amri == 96 || amri == 100 || amri == 104 || amri == 126 || amri == 128 || amri == 130) {
                String upasuaji_thamani = amri == 96 ? "addl" : amri == 100 ? "subl" : amri == 104 ? "imull" : amri == 126 ? "andl" : amri == 128 ? "orl" : "xorl";
                Collections.addAll(laini,"popl %ecx","popl %eax",upasuaji_thamani + " %ecx, %eax","pushl %eax");
            } else if (amri == 108 || amri == 112) Collections.addAll(laini,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (amri == 108 ? "%eax" : "%edx"));
            else if (amri == 116) laini.add("negl (%esp)");
            else if (amri == 120 || amri == 122 || amri == 124) Collections.addAll(laini,"popl %ecx","popl %eax",(amri == 120 ? "sall" : amri == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (amri == 132) {
                int kielezo = amri_data.한바이트(), 증가 = amri_data.부호한바이트(); hundi_jirani(kielezo,지역수); laini.add("addl $" + 증가 + ", -" + (4 * (kielezo + 1)) + "(%ebp)");
            } else if (amri >= 145 && amri <= 147) Collections.addAll(laini,"popl %eax",amri == 145 ? "movsbl %al, %eax" : amri == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (amri >= 153 && amri <= 166) {
                if (amri <= 158) Collections.addAll(laini,"popl %eax","testl %eax, %eax");
                else Collections.addAll(laini,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int fikio_thamani = 위치 + amri_data.부호두바이트(); tawi_Orodha.add(fikio_thamani); laini.add(비교들[amri - (amri <= 158 ? 153 : 159)] + " " + 표식 + "_b" + fikio_thamani);
            } else if (amri == 167 || amri == 200) {
                int fikio_thamani = 위치 + (amri == 167 ? amri_data.부호두바이트() : amri_data.네바이트()); tawi_Orodha.add(fikio_thamani); laini.add("jmp " + 표식 + "_b" + fikio_thamani);
            } else if (amri == 170 || amri == 171) {
                while (amri_data.위치 % 4 != 0) amri_data.한바이트();
                int hali_ya_chaguo_msingi = 위치 + amri_data.네바이트(); tawi_Orodha.add(hali_ya_chaguo_msingi); laini.add("popl %eax");
                int 개수, 아래 = 0;
                if (amri == 170) { 아래 = amri_data.네바이트(); int 위 = amri_data.네바이트(); long urefu_thamani = (long)위 - 아래 + 1; if (urefu_thamani < 1 || urefu_thamani > (amri_data.data.length - amri_data.위치) / 4) throw new Tafsiri_kosa("switch dondoo kosa"); 개수 = (int)urefu_thamani; }
                else { 개수 = amri_data.네바이트(); if (개수 < 0 || 개수 > (amri_data.data.length - amri_data.위치) / 8) throw new Tafsiri_kosa("switch panga_ukubwa kosa"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int thamani = amri == 170 ? 아래 + 순번 : amri_data.네바이트(), fikio_thamani = 위치 + amri_data.네바이트(); tawi_Orodha.add(fikio_thamani);
                    Collections.addAll(laini,"cmpl $" + thamani + ", %eax","je " + 표식 + "_b" + fikio_thamani);
                }
                laini.add("jmp " + 표식 + "_b" + hali_ya_chaguo_msingi);
            } else if (amri == 172 || amri == 176 || amri == 177) {
                if (amri != 177) laini.add("popl %eax"); Collections.addAll(laini,"leave","ret");
            } else if (amri == 178 || amri == 179) {
                mbinu_Marejeleo Marejeleo = tabaka_thamani_55654bf1.Marejeleo(amri_data.두바이트()); if (!필드들.containsKey(Marejeleo)) throw new Tafsiri_kosa("알 수 없는 uga_thamani");
                Collections.addAll(laini,"call " + ishara("init",Marejeleo.mmiliki_thamani),(amri == 178 ? "pushl " : "popl ") + ishara("field",Marejeleo.부분들()));
            } else if (amri == 184) {
                mbinu_Marejeleo Marejeleo = tabaka_thamani_55654bf1.Marejeleo(amri_data.두바이트()); if (!함수들.containsKey(Marejeleo)) throw new Tafsiri_kosa("알 수 없는 KITENDAKAZI_thamani");
                함수형식 호출형식 = new 함수형식(Marejeleo.서술); Collections.addAll(laini,"call " + ishara("init",Marejeleo.mmiliki_thamani),"call " + ishara("method",Marejeleo.부분들()));
                if (!호출형식.인수.isEmpty()) laini.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) laini.add("pushl %eax");
            } else if (amri == 182) {
                mbinu_Marejeleo Marejeleo = tabaka_thamani_55654bf1.Marejeleo(amri_data.두바이트());
                if (Marejeleo.equals(new mbinu_Marejeleo("java/lang/String","length","()I"))) Collections.addAll(laini,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Marejeleo.equals(new mbinu_Marejeleo("java/lang/String","charAt","(I)C"))) Collections.addAll(laini,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Tafsiri_kosa("가상 KITENDAKAZI_thamani 호출 미지원");
            } else if (amri == 188) {
                if (amri_data.한바이트() != 10) throw new Tafsiri_kosa("new int[]만 Auni_thamani"); Collections.addAll(laini,"popl %eax","call rt_new_array","pushl %eax");
            } else if (amri == 190) Collections.addAll(laini,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (amri == 196) {
                int kiendelezi_thamani = amri_data.한바이트(), kielezo = amri_data.두바이트(); hundi_jirani(kielezo,지역수);
                if (kiendelezi_thamani == 21 || kiendelezi_thamani == 25 || kiendelezi_thamani == 54 || kiendelezi_thamani == 58) laini.add((kiendelezi_thamani <= 25 ? "pushl " : "popl ") + "-" + 4 * (kielezo + 1) + "(%ebp)");
                else if (kiendelezi_thamani == 132) laini.add("addl $" + amri_data.부호두바이트() + ", -" + 4 * (kielezo + 1) + "(%ebp)");
                else throw new Tafsiri_kosa("wide amri 미지원");
            } else if (amri == 198 || amri == 199) {
                int fikio_thamani = 위치 + amri_data.부호두바이트(); tawi_Orodha.add(fikio_thamani); Collections.addAll(laini,"popl %eax","testl %eax, %eax",(amri == 198 ? "je " : "jne ") + 표식 + "_b" + fikio_thamani);
            } else throw new Tafsiri_kosa("미지원 amri: " + amri);
        }
        if (!경계들.containsAll(tawi_Orodha)) throw new Tafsiri_kosa("amri 경계가 아닌 곳으로 tawi");
        laini.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",laini);
    }
    String Kitufe_cha_X_86_kisobadilika(tabaka_data data, int kielezo) {
        if (data.상수종류[kielezo] == 3) return data.kisobadilika_data[kielezo].toString();
        if (data.상수종류[kielezo] == 8) return tungo_ishara(data.문자((Integer)data.kisobadilika_data[kielezo]));
        throw new Tafsiri_kosa("정수와 tungo_thamani 상수만 Auni_thamani");
    }
    String 엑스조립본(String ingizo_pointi, List<String> 내보냄, String lengo) throws IOException {
        Map<String,String> mashine_jedwali = new HashMap<>();
        for (String laini : Files.readAllLines(rasilimali_njia.resolve("엑스기계함수.tsv"))) { String[] unganisha_thamani = laini.split("\t"); if (unganisha_thamani[0].equals(lengo)) mashine_jedwali.put(unganisha_thamani[1] + unganisha_thamani[2],unganisha_thamani[3]); }
        int 자리 = ingizo_pointi.lastIndexOf('.'); if (자리 < 0) throw new Tafsiri_kosa("ingizo_pointi pangia_thamani kosa");
        String mmiliki_thamani = ingizo_pointi.substring(0,자리).replace('.','/'), mbinu_ingizo_jina = ingizo_pointi.substring(자리 + 1); mbinu_Marejeleo ingizo_pointi_thamani = null;
        for (String 서술 : Arrays.asList("()I","()V")) { mbinu_Marejeleo Marejeleo = new mbinu_Marejeleo(mmiliki_thamani,mbinu_ingizo_jina,서술); if (함수들.containsKey(Marejeleo)) { if (ingizo_pointi_thamani != null) throw new Tafsiri_kosa("겹친 ingizo_pointi"); ingizo_pointi_thamani = Marejeleo; } }
        if (ingizo_pointi_thamani == null || (함수들.get(ingizo_pointi_thamani).fikia_ingizo & 0x100) != 0) throw new Tafsiri_kosa("ingizo_pointi_thamani KITENDAKAZI_thamani umbiza_thamani kosa");
        List<String> laini = new ArrayList<>(); laini.add(".code32");
        for (tabaka_data data : 클래스들.values()) {
            String hali_thamani = ishara("state",data.Jina), anzilisha = ishara("init",data.Jina);
            Collections.addAll(laini,".bss",".balign 4",hali_thamani + ": .long 0",".text",anzilisha + ":","cmpl $0, " + hali_thamani,"jne " + anzilisha + "_done","movl $1, " + hali_thamani);
            mbinu_Marejeleo 초기화참조 = new mbinu_Marejeleo(data.Jina,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) laini.add("call " + ishara("method",초기화참조.부분들()));
            Collections.addAll(laini,"movl $2, " + hali_thamani,anzilisha + "_done:","ret");
            for (mwanachama_data uga_thamani : data.uga_thamani) {
                byte[] kisobadilika_thamani = uga_thamani.sifa_thamani.get("ConstantValue"); String thamani = kisobadilika_thamani == null ? "0" : Kitufe_cha_X_86_kisobadilika(data,new data_msomaji(kisobadilika_thamani).두바이트());
                Collections.addAll(laini,".data",".balign 4",ishara("field",data.Jina,uga_thamani.Jina,uga_thamani.서술) + ": .long " + thamani);
            }
            for (mwanachama_data KITENDAKAZI_thamani : data.KITENDAKAZI_thamani) if (!KITENDAKAZI_thamani.Jina.equals("<init>")) laini.add(Kitufe_cha_X_86_mbinu_kiini(new mbinu_Marejeleo(data.Jina,KITENDAKAZI_thamani.Jina,KITENDAKAZI_thamani.서술),KITENDAKAZI_thamani,mashine_jedwali,lengo));
        }
        Collections.addAll(laini,".text",".globl java_entry","java_entry:","call " + ishara("init",ingizo_pointi_thamani.mmiliki_thamani),"call " + ishara("method",ingizo_pointi_thamani.부분들()));
        if (ingizo_pointi_thamani.서술.equals("()V")) laini.add("xorl %eax, %eax"); laini.add("ret");
        for (String pangia_thamani : 내보냄) {
            int kitenganishi_thamani_d8ba4873 = pangia_thamani.indexOf('='); if (kitenganishi_thamani_d8ba4873 < 1) throw new Tafsiri_kosa("내보내기 pangia_thamani kosa");
            String 외부 = pangia_thamani.substring(0,kitenganishi_thamani_d8ba4873), KITENDAKAZI_thamani = pangia_thamani.substring(kitenganishi_thamani_d8ba4873 + 1); int 나눔 = KITENDAKAZI_thamani.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tafsiri_kosa("내보내기 ishara kosa");
            String tabaka_thamani_55654bf1 = KITENDAKAZI_thamani.substring(0,나눔).replace('.','/'), Jina = KITENDAKAZI_thamani.substring(나눔 + 1); mbinu_Marejeleo uteuzi_thamani = null;
            for (mbinu_Marejeleo Marejeleo : 함수들.keySet()) if (Marejeleo.mmiliki_thamani.equals(tabaka_thamani_55654bf1) && Marejeleo.Jina.equals(Jina)) { if (uteuzi_thamani != null) throw new Tafsiri_kosa("겹친 내보내기 lengo"); uteuzi_thamani = Marejeleo; }
            if (uteuzi_thamani == null) throw new Tafsiri_kosa("내보낼 함수가 없음");
            Collections.addAll(laini,".text",".globl " + 외부,외부 + ":","call " + ishara("init",uteuzi_thamani.mmiliki_thamani),"jmp " + ishara("method",uteuzi_thamani.부분들()));
        }
        laini.add(".section .rodata");
        for (Map.Entry<String,String> ingizo_thamani : 문자열들.entrySet()) {
            Collections.addAll(laini,".balign 4",ingizo_thamani.getValue() + ":",".long " + ingizo_thamani.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char funzo_thamani : ingizo_thamani.getKey().toCharArray()) 단위들.add(Integer.toString(funzo_thamani)); if (!단위들.isEmpty()) laini.add(".long " + String.join(",",단위들));
        }
        laini.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",laini) + "\n";
    }
    static void tekeleza_zana(List<String> amri) throws Exception {
        if (new ProcessBuilder(amri).inheritIO().start().waitFor() != 0) throw new Tafsiri_kosa("jenga_chanzo kosa: " + amri.get(0));
    }
    static String data_tungo(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void Kitufe_cha_X_86_Tafsiri(List<Path> 입력들, String lengo, String ingizo_pointi, List<String> 내보냄, Path 출력, Path rasilimali_thamani) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), tabaka_njia = 임시.resolve("classes"); Files.createDirectory(tabaka_njia);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",tabaka_njia.toString(),"-sourcepath",tabaka_njia.toString(),"-d",tabaka_njia.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Tafsiri_kosa("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Tafsiri_kosa(".java 또는 .class만 Auni_thamani");
            }
            if (원문수 > 0) tekeleza_zana(자바명령);
            try (java.util.stream.Stream<Path> njia_Orodha = Files.walk(tabaka_njia)) { njia_Orodha.filter(njia -> njia.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,lengo.equals("user") ? "user" : "kernel",262144,rasilimali_thamani);
            String 조립 = 변환.엑스조립본(ingizo_pointi,내보냄,lengo); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = rasilimali_thamani.getParent();
            tekeleza_zana(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            tekeleza_zana(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("muda_wa_kuendesha_lugha_ya_kawaida_Auni.s").toString()));
            List<String> UNGANISHA = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (lengo.equals("kernel")) UNGANISHA.add("-r");
            else {
                tekeleza_zana(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(lengo.equals("user") ? "Anza_mtumiaji_programu.s" : "리눅스시작.s").toString()));
                Collections.addAll(UNGANISHA,"-e","_start",임시.resolve("start.o").toString());
                if (lengo.equals("user")) Collections.addAll(UNGANISHA,"-T",도구위치.resolve("mtumiaji_Kiungo_Muundo.ld").toString());
            }
            Collections.addAll(UNGANISHA,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); tekeleza_zana(UNGANISHA);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path chapisha_thamani = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),chapisha_thamani,StandardCopyOption.REPLACE_EXISTING); Files.move(chapisha_thamani,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(chapisha_thamani); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(lengo.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> ishara_data = new ArrayList<>(), chanzo_data = new ArrayList<>();
            for (mbinu_Marejeleo Marejeleo : 변환.함수들.keySet()) ishara_data.add(data_tungo(ishara("method",Marejeleo.부분들())) + ":" + data_tungo(Marejeleo.mmiliki_thamani + "." + Marejeleo.Jina + Marejeleo.서술));
            for (Path 입력 : 입력들) {
                byte[] kali_faili = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte thamani : kali_faili) SMS.append(String.format(Locale.ROOT,"%02x",thamani & 255));
                chanzo_data.add(data_tungo(입력.toAbsolutePath().toString()) + ":" + data_tungo(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + data_tungo(lengo) + ",\"entry\":" + data_tungo(ingizo_pointi) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",ishara_data) + "},\"sources\":{" + String.join(",",chanzo_data) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> njia_Orodha = Files.walk(임시)) { for (Path njia : (Iterable<Path>)njia_Orodha.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(njia); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String ingizo_pointi = null, lengo = "kernel", Kitufe_cha_X_86_lengo = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> njia_Orodha = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String thamani = 인수[순번];
                switch (thamani) {
                    case "--target": Kitufe_cha_X_86_lengo = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry tabaka_thamani_55654bf1.KITENDAKAZI_thamani -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export ishara=tabaka_thamani_55654bf1.KITENDAKAZI_thamani] 클래스파일 또는 Java원문"); return;
                    case "--entry": ingizo_pointi = 인수[++순번]; break;
                    case "--profile": lengo = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (thamani.startsWith("-")) throw new Tafsiri_kosa("알 수 없는 옵션: " + thamani); njia_Orodha.add(Paths.get(thamani));
                }
            }
            if (ingizo_pointi == null || 출력경로 == null || njia_Orodha.isEmpty()) throw new Tafsiri_kosa("--entry, -o, tabaka_thamani_55654bf1 파일이 필요합니다");
            Path rasilimali_thamani = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (Kitufe_cha_X_86_lengo != null) {
                if (!Arrays.asList("linux","kernel","user").contains(Kitufe_cha_X_86_lengo)) throw new Tafsiri_kosa("알 수 없는 tekeleza_amri lengo");
                Kitufe_cha_X_86_Tafsiri(njia_Orodha,Kitufe_cha_X_86_lengo,ingizo_pointi,내보냄,출력경로,rasilimali_thamani); return;
            }
            String chanzo = new 기계어미리번역(njia_Orodha, lengo, 낱말수, rasilimali_thamani).생성(ingizo_pointi, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, chanzo, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception kosa) { System.err.println("jenga_chanzo kosa: " + kosa.getMessage()); System.exit(1); }
    }
}
