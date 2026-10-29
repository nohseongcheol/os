// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java klassi_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Traduzzjoni_żball extends RuntimeException {
        Traduzzjoni_żball(String 설명) { super(설명); }
    }
    static final class data_Qarrej {
        final byte[] data;
        int pożizzjoni;
        data_Qarrej(byte[] 입력자료) { data = 입력자료; }
        byte[] 읽기(int tul_VALUE) {
            if (tul_VALUE < 0 || tul_VALUE > data.length - pożizzjoni) throw new Traduzzjoni_żball("잘린 klassi_VALUE 또는 kmand data");
            byte[] miżura = Arrays.copyOfRange(data, pożizzjoni, pożizzjoni + tul_VALUE); pożizzjoni += tul_VALUE; return miżura;
        }
        int 한바이트() { if (pożizzjoni >= data.length) throw new Traduzzjoni_żball("잘린 kmand data"); return data[pożizzjoni++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class membru_data {
        final int aċċess_entrata;
        final String isem, 서술;
        final Map<String, byte[]> attribut_VALUE;
        membru_data(int aċċess_VALUE, String isem_VALUE, String 서술값, Map<String, byte[]> attribut_data) {
            aċċess_entrata = aċċess_VALUE; isem = isem_VALUE; 서술 = 서술값; attribut_VALUE = attribut_data;
        }
    }
    static final class metodu_Referenza implements Comparable<metodu_Referenza> {
        final String propjetarju_VALUE, isem, 서술;
        metodu_Referenza(String 소유값, String isem_VALUE, String 서술값) { propjetarju_VALUE = 소유값; isem = isem_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{propjetarju_VALUE, isem, 서술}; }
        public int compareTo(metodu_Referenza peer_VALUE) {
            int 비교값 = propjetarju_VALUE.compareTo(peer_VALUE.propjetarju_VALUE);
            if (비교값 == 0) 비교값 = isem.compareTo(peer_VALUE.isem);
            return 비교값 == 0 ? 서술.compareTo(peer_VALUE.서술) : 비교값;
        }
        public boolean equals(Object peer_VALUE) { return peer_VALUE instanceof metodu_Referenza && compareTo((metodu_Referenza) peer_VALUE) == 0; }
        public int hashCode() { return Objects.hash(propjetarju_VALUE, isem, 서술); }
    }
    static final class klassi_data {
        final int[] 상수종류;
        final Object[] valur_fiss_data;
        final String isem;
        final List<membru_data> qasam_VALUE, FUNCTION_VALUE;
        klassi_data(Path mogħdija) throws IOException {
            data_Qarrej Qarrej_VALUE = new data_Qarrej(Files.readAllBytes(mogħdija));
            if (Qarrej_VALUE.네바이트() != 0xcafebabe) throw new Traduzzjoni_żball("Java klassi_VALUE 표식이 아님");
            Qarrej_VALUE.읽기(4);
            int element_COUNT = Qarrej_VALUE.두바이트(); 상수종류 = new int[element_COUNT]; valur_fiss_data = new Object[element_COUNT];
            for (int 순번 = 1; 순번 < element_COUNT; 순번++) {
                int 종류 = Qarrej_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int tul_VALUE = Qarrej_VALUE.두바이트();
                        byte[] karattru_bafer = Qarrej_VALUE.읽기(tul_VALUE), 길이붙인자료 = new byte[tul_VALUE + 2];
                        길이붙인자료[0] = (byte)(tul_VALUE >> 8); 길이붙인자료[1] = (byte)tul_VALUE;
                        System.arraycopy(karattru_bafer, 0, 길이붙인자료, 2, tul_VALUE);
                        valur_fiss_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: valur_fiss_data[순번] = Qarrej_VALUE.네바이트(); break;
                    case 4: Qarrej_VALUE.읽기(4); break;
                    case 5: case 6: Qarrej_VALUE.읽기(8); 순번++; break;
                    case 7: case 8: case 16: valur_fiss_data[순번] = Qarrej_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        valur_fiss_data[순번] = new int[]{Qarrej_VALUE.두바이트(), Qarrej_VALUE.두바이트()}; break;
                    case 15: valur_fiss_data[순번] = new int[]{Qarrej_VALUE.한바이트(), Qarrej_VALUE.두바이트()}; break;
                    default: throw new Traduzzjoni_żball("지원하지 않는 valur_fiss_VALUE 종류: " + 종류);
                }
            }
            Qarrej_VALUE.두바이트(); isem = klassi_isem(Qarrej_VALUE.두바이트());
            if (!klassi_isem(Qarrej_VALUE.두바이트()).equals("java/lang/Object") || Qarrej_VALUE.두바이트() != 0)
                throw new Traduzzjoni_żball(isem + ": 상속 및 인터페이스 미지원");
            qasam_VALUE = 멤버읽기(Qarrej_VALUE); FUNCTION_VALUE = 멤버읽기(Qarrej_VALUE); 속성읽기(Qarrej_VALUE);
            if (Qarrej_VALUE.pożizzjoni != Qarrej_VALUE.data.length) throw new Traduzzjoni_żball("klassi_VALUE 뒤에 남은 data");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Traduzzjoni_żball("문자 valur_fiss_VALUE INDEX żball");
            return (String) valur_fiss_data[INDEX];
        }
        String klassi_isem(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Traduzzjoni_żball("klassi_VALUE Referenza żball");
            return 문자((Integer)valur_fiss_data[INDEX]);
        }
        metodu_Referenza Referenza(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Traduzzjoni_żball("멤버 Referenza żball");
            int[] par_VALUE = (int[])valur_fiss_data[INDEX], isem_par = (int[])valur_fiss_data[par_VALUE[1]];
            return new metodu_Referenza(klassi_isem(par_VALUE[0]), 문자(isem_par[0]), 문자(isem_par[1]));
        }
        Map<String, byte[]> 속성읽기(data_Qarrej Qarrej_VALUE) {
            Map<String, byte[]> miżura = new LinkedHashMap<>();
            int element_COUNT = Qarrej_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                String attribut_isem = 문자(Qarrej_VALUE.두바이트()); byte[] VALUE = Qarrej_VALUE.읽기(Qarrej_VALUE.네바이트());
                if (miżura.put(attribut_isem, VALUE) != null) throw new Traduzzjoni_żball("겹친 attribut_VALUE: " + attribut_isem);
            }
            return miżura;
        }
        List<membru_data> 멤버읽기(data_Qarrej Qarrej_VALUE) {
            List<membru_data> miżura = new ArrayList<>(); int element_COUNT = Qarrej_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                int aċċess_entrata = Qarrej_VALUE.두바이트(); String metodu_entrata_isem = 문자(Qarrej_VALUE.두바이트()), 서술 = 문자(Qarrej_VALUE.두바이트());
                miżura.add(new membru_data(aċċess_entrata, metodu_entrata_isem, 서술, 속성읽기(Qarrej_VALUE)));
            }
            return miżura;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Traduzzjoni_żball("FUNCTION_VALUE 서술 żball: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Traduzzjoni_żball("FUNCTION_VALUE 서술 żball: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Traduzzjoni_żball("FUNCTION_VALUE 서술 żball: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> miżura = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int pożizzjoni = 0; pożizzjoni < 서술.length();) {
            String għażla_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, pożizzjoni)) { għażla_VALUE = format_VALUE; break; }
            if (għażla_VALUE == null) throw new Traduzzjoni_żball("지원하지 않는 tip_ta_data: " + 서술);
            miżura.add(għażla_VALUE); pożizzjoni += għażla_VALUE.length();
        }
        return miżura;
    }
    static String simbolu(String 종류, String... 부분들) {
        try {
            byte[] hash_fajl = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", hash_fajl[순번] & 255));
            return SMS.toString();
        } catch (Exception żball) { throw new Traduzzjoni_żball(żball.toString()); }
    }
    final Map<String, klassi_data> 클래스들 = new TreeMap<>();
    final Map<metodu_Referenza, membru_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, kompjuter_klassi;
    final int 동적기억낱말수;
    final Path riżorsa_mogħdija;
    기계어미리번역(List<Path> mogħdija_Lista, String mira, int 낱말수, Path riżorsa_VALUE) throws IOException {
        if ((!mira.equals("kernel") && !mira.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Traduzzjoni_żball("eżegwixxa_kmand mira 또는 Memorja_VALUE 공간 daqqas żball");
        실행대상 = mira; 동적기억낱말수 = 낱말수; riżorsa_mogħdija = riżorsa_VALUE;
        // 이 이름도 국가별 sors_siġra iġġenera 시 해당 언어로 옮긴다.
        kompjuter_klassi = mira.equals("kernel") ? "bord" : "utent";
        for (String linja : Files.readAllLines(riżorsa_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = linja.split("\t", -1);
            if (부분들.length != 4) throw new Traduzzjoni_żball("kompjuter FUNCTION_VALUE data żball");
            if (부분들[0].equals(mira)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path mogħdija : mogħdija_Lista) {
            klassi_data data = new klassi_data(mogħdija);
            if (클래스들.put(data.isem, data) != null) throw new Traduzzjoni_żball("중복 klassi_VALUE: " + data.isem);
            for (membru_data qasam_VALUE : data.qasam_VALUE) {
                if ((qasam_VALUE.aċċess_entrata & 8) == 0 || 형식읽기(qasam_VALUE.서술).equals(Collections.singletonList("V"))) throw new Traduzzjoni_żball("statiku_VALUE 필드만 Appoġġ_VALUE");
                if (필드들.put(new metodu_Referenza(data.isem, qasam_VALUE.isem, qasam_VALUE.서술), qasam_VALUE) != null) throw new Traduzzjoni_żball("중복 qasam_VALUE");
            }
            for (membru_data FUNCTION_VALUE : data.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.isem.equals("<init>")) continue;
                if ((FUNCTION_VALUE.aċċess_entrata & 8) == 0 || (FUNCTION_VALUE.aċċess_entrata & (0x20 | 0x400)) != 0) throw new Traduzzjoni_żball("statiku_VALUE 비동기화 함수만 Appoġġ_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new metodu_Referenza(data.isem, FUNCTION_VALUE.isem, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Traduzzjoni_żball("중복 FUNCTION_VALUE");
            }
        }
    }
    String string_simbolu(String SMS) { return 문자열들.computeIfAbsent(SMS, VALUE -> "j_text_" + 문자열들.size()); }
    String valur_fiss_espressjoni(klassi_data data, int INDEX) {
        if (INDEX < 1 || INDEX >= data.상수종류.length) throw new Traduzzjoni_żball("valur_fiss_VALUE INDEX klipp żball");
        if (data.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + data.valur_fiss_data[INDEX] + ")";
        if (data.상수종류[INDEX] == 8) return "(word)" + string_simbolu(data.문자((Integer)data.valur_fiss_data[INDEX]));
        throw new Traduzzjoni_żball("정수와 string_VALUE 상수만 Appoġġ_VALUE");
    }
    String 함수원형(metodu_Referenza Referenza) {
        List<String> 인수들 = new ArrayList<>(); int element_COUNT = new 함수형식(Referenza.서술).인수.size();
        for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbolu("method", Referenza.부분들()) + "(" + (element_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void ċekk_lokali(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Traduzzjoni_żball("lokali_ambitu 변수 INDEX klipp żball"); }
    void 분기넣기(List<String> 출력, Set<Integer> fergħa_Lista, int pożizzjoni, int 이동량, String kondizzjoni) {
        int destinazzjoni_VALUE = pożizzjoni + 이동량; fergħa_Lista.add(destinazzjoni_VALUE);
        출력.add((kondizzjoni == null ? "" : "if (" + kondizzjoni + ") ") + "goto b" + destinazzjoni_VALUE + ";");
    }
    String 함수본문(metodu_Referenza FUNCTION_VALUE, membru_data data) {
        byte[] 본문자료 = data.attribut_VALUE.get("Code"); if (본문자료 == null) throw new Traduzzjoni_żball("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.isem);
        data_Qarrej Qarrej_VALUE = new data_Qarrej(본문자료); int 쌓임깊이 = Qarrej_VALUE.두바이트(), 지역변수수 = Qarrej_VALUE.두바이트();
        data_Qarrej kmand_data = new data_Qarrej(Qarrej_VALUE.읽기(Qarrej_VALUE.네바이트()));
        if (Qarrej_VALUE.두바이트() != 0) throw new Traduzzjoni_żball("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (지역변수수 < format_VALUE.인수.size()) throw new Traduzzjoni_żball("매개변수보다 적은 lokali_ambitu 변수");
        klassi_data klassi_VALUE = 클래스들.get(FUNCTION_VALUE.propjetarju_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(FUNCTION_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), fergħa_Lista = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (kmand_data.pożizzjoni < kmand_data.data.length) {
            int pożizzjoni = kmand_data.pożizzjoni, kmand = kmand_data.한바이트(); 경계들.add(pożizzjoni); 출력.add("b" + pożizzjoni + ":;");
            if (kmand == 0) continue;
            if (kmand == 1) 출력.add("PUSH(0);");
            else if (kmand >= 2 && kmand <= 8) 출력.add("PUSH((uint32_t)(" + (kmand - 3) + "));");
            else if (kmand == 16 || kmand == 17) 출력.add("PUSH((uint32_t)(" + (kmand == 16 ? kmand_data.부호한바이트() : kmand_data.부호두바이트()) + "));");
            else if (kmand == 18 || kmand == 19) 출력.add("PUSH(" + valur_fiss_espressjoni(klassi_VALUE, kmand == 18 ? kmand_data.한바이트() : kmand_data.두바이트()) + ");");
            else if (kmand == 21 || kmand == 25 || (kmand >= 26 && kmand <= 29) || (kmand >= 42 && kmand <= 45)) {
                int INDEX = kmand == 21 || kmand == 25 ? kmand_data.한바이트() : kmand - (kmand <= 29 ? 26 : 42);
                ċekk_lokali(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (kmand == 54 || kmand == 58 || (kmand >= 59 && kmand <= 62) || (kmand >= 75 && kmand <= 78)) {
                int INDEX = kmand == 54 || kmand == 58 ? kmand_data.한바이트() : kmand - (kmand <= 62 ? 59 : 75);
                ċekk_lokali(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (kmand == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (kmand == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (kmand == 87 || kmand == 88) 출력.add(kmand == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (kmand >= 89 && kmand <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ordni_Lista = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[kmand - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : ordni_Lista[kmand - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (kmand == 96 || kmand == 100 || kmand == 104 || kmand == 126 || kmand == 128 || kmand == 130) {
                String operazzjoni_VALUE = kmand == 96 ? "+" : kmand == 100 ? "-" : kmand == 104 ? "*" : kmand == 126 ? "&" : kmand == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operazzjoni_VALUE + " (uint32_t)b);");
            } else if (kmand == 108 || kmand == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (kmand == 112 ? 1 : 0) + "));");
            else if (kmand == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (kmand == 120 || kmand == 122 || kmand == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (kmand == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (kmand == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (kmand == 132) {
                int INDEX = kmand_data.한바이트(), 증가량 = kmand_data.부호한바이트(); ċekk_lokali(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (kmand >= 145 && kmand <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (kmand == 145 ? "int8_t" : kmand == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (kmand >= 153 && kmand <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, fergħa_Lista, pożizzjoni, kmand_data.부호두바이트(), "(int32_t)a " + 비교들[kmand - 153] + " 0");
            } else if (kmand >= 159 && kmand <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, fergħa_Lista, pożizzjoni, kmand_data.부호두바이트(), kmand >= 165 ? "a " + 비교들[kmand - 159] + " b" : "(int32_t)a " + 비교들[kmand - 159] + " (int32_t)b");
            } else if (kmand == 167 || kmand == 200) 분기넣기(출력, fergħa_Lista, pożizzjoni, kmand == 167 ? kmand_data.부호두바이트() : kmand_data.네바이트(), null);
            else if (kmand == 170 || kmand == 171) {
                while (kmand_data.pożizzjoni % 4 != 0) kmand_data.한바이트();
                int valur_default = kmand_data.네바이트(); 출력.add("a = POP();");
                if (kmand == 170) {
                    int 아래 = kmand_data.네바이트(), 위 = kmand_data.네바이트(); long element_COUNT = (long)위 - 아래 + 1;
                    if (element_COUNT < 1 || element_COUNT > (kmand_data.data.length - kmand_data.pożizzjoni) / 4) throw new Traduzzjoni_żball("switch klipp żball");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, fergħa_Lista, pożizzjoni, kmand_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int element_COUNT = kmand_data.네바이트(), 앞값 = 0;
                    if (element_COUNT < 0 || element_COUNT > (kmand_data.data.length - kmand_data.pożizzjoni) / 8) throw new Traduzzjoni_żball("switch daqqas żball");
                    for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                        int VALUE = kmand_data.네바이트(); if (순번 > 0 && VALUE <= 앞값) throw new Traduzzjoni_żball("switch ordni_VALUE żball"); 앞값 = VALUE;
                        분기넣기(출력, fergħa_Lista, pożizzjoni, kmand_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, fergħa_Lista, pożizzjoni, valur_default, null);
            } else if (kmand == 172 || kmand == 176 || kmand == 177) 출력.add("return " + (kmand == 177 ? "0" : "POP()") + ";");
            else if (kmand == 178 || kmand == 179) {
                metodu_Referenza Referenza = klassi_VALUE.Referenza(kmand_data.두바이트()); if (!필드들.containsKey(Referenza)) throw new Traduzzjoni_żball("알 수 없는 qasam_VALUE");
                출력.add(simbolu("init", Referenza.propjetarju_VALUE) + "();"); String qasam_VALUE = simbolu("field", Referenza.부분들());
                출력.add(kmand == 178 ? "PUSH(" + qasam_VALUE + ");" : qasam_VALUE + " = POP();");
            } else if (kmand == 184) {
                metodu_Referenza Referenza = klassi_VALUE.Referenza(kmand_data.두바이트()); if (!함수들.containsKey(Referenza)) throw new Traduzzjoni_żball("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Referenza.서술); int element_COUNT = 호출형식.인수.size();
                출력.add(simbolu("init", Referenza.propjetarju_VALUE) + "();"); 출력.add("if(sp < " + element_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + element_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < element_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + simbolu("method", Referenza.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (kmand == 182) {
                metodu_Referenza Referenza = klassi_VALUE.Referenza(kmand_data.두바이트());
                if (Referenza.equals(new metodu_Referenza("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Referenza.equals(new metodu_Referenza("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Traduzzjoni_żball("가상 FUNCTION_VALUE 호출 미지원");
            } else if (kmand == 188) {
                if (kmand_data.한바이트() != 10) throw new Traduzzjoni_żball("new int[]만 Appoġġ_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (kmand == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (kmand == 196) {
                int estensjoni_VALUE = kmand_data.한바이트(), INDEX = kmand_data.두바이트(); ċekk_lokali(INDEX, 지역변수수);
                if (estensjoni_VALUE == 21 || estensjoni_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (estensjoni_VALUE == 54 || estensjoni_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (estensjoni_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + kmand_data.부호두바이트() + ");");
                else throw new Traduzzjoni_żball("미지원 wide kmand");
            } else if (kmand == 198 || kmand == 199) {
                출력.add("a = POP();"); 분기넣기(출력, fergħa_Lista, pożizzjoni, kmand_data.부호두바이트(), "a " + (kmand == 198 ? "==" : "!=") + " 0");
            } else throw new Traduzzjoni_żball(FUNCTION_VALUE.propjetarju_VALUE + "." + FUNCTION_VALUE.isem + ", byte_VALUE " + pożizzjoni + ": 미지원 kmand " + kmand);
        }
        if (!경계들.containsAll(fergħa_Lista)) throw new Traduzzjoni_żball("kmand 경계가 아닌 곳으로 fergħa");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String esporta_metodu(String Link_simbolu, String mira, boolean 진입점여부) {
        int pożizzjoni_INDEX = mira.lastIndexOf('.'); if (pożizzjoni_INDEX < 0 || !Link_simbolu.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Traduzzjoni_żball("내보내기 assenja_VALUE żball");
        String propjetarju_VALUE = mira.substring(0, pożizzjoni_INDEX).replace('.', '/'), isem = mira.substring(pożizzjoni_INDEX + 1); metodu_Referenza għażla_VALUE = null;
        for (metodu_Referenza Referenza : 함수들.keySet()) if (Referenza.propjetarju_VALUE.equals(propjetarju_VALUE) && Referenza.isem.equals(isem)) {
            if (għażla_VALUE != null) throw new Traduzzjoni_żball("겹친 내보내기 mira"); għażla_VALUE = Referenza;
        }
        if (għażla_VALUE == null || (함수들.get(għażla_VALUE).aċċess_entrata & 0x100) != 0) throw new Traduzzjoni_żball("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 format_VALUE = new 함수형식(għażla_VALUE.서술);
        if ((진입점여부 && !format_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.반환)) throw new Traduzzjoni_żball("entrata_punt_VALUE 또는 C 경계 format_VALUE żball");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) {
            if (!format_VALUE.인수.get(순번).equals("I")) throw new Traduzzjoni_żball("C 경계는 int 인수만 Appoġġ_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.반환.equals("V") ? "void " : "int32_t ") + Link_simbolu + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbolu("init", għażla_VALUE.propjetarju_VALUE) + "(); " + (format_VALUE.반환.equals("V") ? "" : "return (int32_t)") + simbolu("method", għażla_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String iġġenera(String entrata_punt, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metodu_Referenza, membru_data> entrata_VALUE : 함수들.entrySet()) {
            metodu_Referenza Referenza = entrata_VALUE.getKey(); membru_data data = entrata_VALUE.getValue(); 선언들.add(함수원형(Referenza) + ";");
            if ((data.aċċess_entrata & 0x100) != 0) {
                String AQBAD = 기계함수들.get(Referenza.isem + Referenza.서술);
                if (!Referenza.propjetarju_VALUE.equals(kompjuter_klassi) || AQBAD == null) throw new Traduzzjoni_żball("허용되지 않은 native FUNCTION_VALUE: " + Referenza.isem);
                int element_COUNT = new 함수형식(Referenza.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + AQBAD + "(" + (element_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(element_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Referenza) + " { return " + AQBAD + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Referenza, data));
        }
        for (Map.Entry<metodu_Referenza, membru_data> entrata_VALUE : 필드들.entrySet()) {
            metodu_Referenza Referenza = entrata_VALUE.getKey(); byte[] valur_fiss_VALUE = entrata_VALUE.getValue().attribut_VALUE.get("ConstantValue");
            String VALUE = valur_fiss_VALUE == null ? "0" : valur_fiss_espressjoni(클래스들.get(Referenza.propjetarju_VALUE), new data_Qarrej(valur_fiss_VALUE).두바이트());
            필드선언들.add("static word " + simbolu("field", Referenza.부분들()) + " = " + VALUE + ";");
        }
        for (String isem : 클래스들.keySet()) {
            String inizjala = simbolu("init", isem), stat_VALUE = simbolu("state", isem);
            선언들.add("static void " + inizjala + "(void);"); 필드선언들.add("static unsigned " + stat_VALUE + ";");
            metodu_Referenza Referenza = new metodu_Referenza(isem, "<clinit>", "()V");
            몸체들.add("static void " + inizjala + "(void) { if(" + stat_VALUE + ") return; " + stat_VALUE + " = 1; " + (함수들.containsKey(Referenza) ? simbolu("method", Referenza.부분들()) + "(); " : "") + stat_VALUE + " = 2; }");
        }
        몸체들.add(esporta_metodu("java_entry", entrata_punt, true)); Set<String> 공개이름 = new HashSet<>();
        for (String assenja_VALUE : 내보내기목록) {
            int pożizzjoni_INDEX = assenja_VALUE.indexOf('='); if (pożizzjoni_INDEX < 1) throw new Traduzzjoni_żball("내보내기 assenja_VALUE żball");
            String isem = assenja_VALUE.substring(0, pożizzjoni_INDEX); 공개이름.add(isem); 몸체들.add(esporta_metodu(isem, assenja_VALUE.substring(pożizzjoni_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> entrata_VALUE : 문자열들.entrySet()) {
            String SMS = entrata_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + entrata_VALUE.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) ARRAY_VALUE.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Appoġġ_VALUE = Files.readString(riżorsa_mogħdija.resolve("tħaddim_tal_lingwa_komuni_Appoġġ.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Appoġġ_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String sors, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> isem_tabella = new HashMap<>();
        for (String linja : Files.readAllLines(riżorsa_mogħdija.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] par_VALUE = linja.split("\t"); isem_tabella.put(par_VALUE[0], par_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(sors); StringBuffer miżura = new StringBuffer();
        while (찾개.find()) {
            String isem = 찾개.group(), 새이름 = isem;
            if (!isem.startsWith("//") && !isem.startsWith("/*") && !isem.startsWith("\"") && !isem.startsWith("'") && !공개이름.contains(isem)) {
                새이름 = isem_tabella.getOrDefault(isem, isem);
                if (isem.matches("a[0-9]+")) 새이름 = "인수" + isem.substring(1);
                if (isem.matches("b[0-9]+")) 새이름 = "fergħa" + isem.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char karattru_VALUE : 새이름.toCharArray()) 표기.append(karattru_VALUE < 128 ? Character.toString(karattru_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)karattru_VALUE));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(miżura, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(miżura); return miżura.toString();
    }
    String 엑스함수본문(metodu_Referenza FUNCTION_VALUE, membru_data data, Map<String,String> kompjuter_tabella, String mira) {
        String 표식 = simbolu("method", FUNCTION_VALUE.부분들());
        List<String> linja = new ArrayList<>();
        if ((data.aċċess_entrata & 0x100) != 0) {
            String AQBAD = kompjuter_tabella.get(FUNCTION_VALUE.isem + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.propjetarju_VALUE.equals(mira.equals("kernel") ? "mowbajl_VALUE" : "utent") || AQBAD == null) throw new Traduzzjoni_żball("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + 표식 + ":\njmp " + AQBAD;
        }
        byte[] il_korp_tat_test = data.attribut_VALUE.get("Code"); if (il_korp_tat_test == null) throw new Traduzzjoni_żball("FUNCTION_VALUE 몸체가 없음");
        data_Qarrej Qarrej_VALUE = new data_Qarrej(il_korp_tat_test); Qarrej_VALUE.두바이트(); int lokali_COUNT = Qarrej_VALUE.두바이트();
        data_Qarrej kmand_data = new data_Qarrej(Qarrej_VALUE.읽기(Qarrej_VALUE.네바이트()));
        if (Qarrej_VALUE.두바이트() != 0) throw new Traduzzjoni_żball("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokali_COUNT < format_VALUE.인수.size()) throw new Traduzzjoni_żball("매개변수보다 적은 lokali_ambitu 변수");
        Collections.addAll(linja,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokali_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) Collections.addAll(linja,"movl " + (8 + 4 * (format_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        klassi_data klassi_VALUE = 클래스들.get(FUNCTION_VALUE.propjetarju_VALUE); Set<Integer> 경계들 = new HashSet<>(), fergħa_Lista = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (kmand_data.pożizzjoni < kmand_data.data.length) {
            int pożizzjoni = kmand_data.pożizzjoni, kmand = kmand_data.한바이트(); String pożizzjoni_INDEX = 표식 + "_b" + pożizzjoni;
            linja.add(pożizzjoni_INDEX + ":"); 경계들.add(pożizzjoni);
            if (kmand == 0) linja.add("nop");
            else if (kmand == 1) linja.add("pushl $0");
            else if (kmand >= 2 && kmand <= 8) linja.add("pushl $" + (kmand - 3));
            else if (kmand == 16 || kmand == 17) linja.add("pushl $" + (kmand == 16 ? kmand_data.부호한바이트() : kmand_data.부호두바이트()));
            else if (kmand == 18 || kmand == 19) {
                int INDEX = kmand == 18 ? kmand_data.한바이트() : kmand_data.두바이트();
                linja.add("pushl $" + 엑스상수(klassi_VALUE,INDEX));
            } else if (kmand == 21 || kmand == 25 || (kmand >= 26 && kmand <= 29) || (kmand >= 42 && kmand <= 45) || kmand == 54 || kmand == 58 || (kmand >= 59 && kmand <= 62) || (kmand >= 75 && kmand <= 78)) {
                boolean 읽음 = kmand < 54; int INDEX = kmand == 21 || kmand == 25 || kmand == 54 || kmand == 58 ? kmand_data.한바이트() : kmand - (kmand <= 29 ? 26 : kmand <= 45 ? 42 : kmand <= 62 ? 59 : 75);
                ċekk_lokali(INDEX,lokali_COUNT); linja.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (kmand == 46) Collections.addAll(linja,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (kmand == 79) Collections.addAll(linja,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (kmand == 87 || kmand == 88) linja.add("addl $" + (kmand == 87 ? 4 : 8) + ", %esp");
            else if (kmand >= 89 && kmand <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ordni_Lista = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[kmand - 89]; 순번++) linja.add("popl " + 저장기들[순번]);
                for (int 순번 : ordni_Lista[kmand - 89]) linja.add("pushl " + 저장기들[순번]);
            } else if (kmand == 96 || kmand == 100 || kmand == 104 || kmand == 126 || kmand == 128 || kmand == 130) {
                String operazzjoni_VALUE = kmand == 96 ? "addl" : kmand == 100 ? "subl" : kmand == 104 ? "imull" : kmand == 126 ? "andl" : kmand == 128 ? "orl" : "xorl";
                Collections.addAll(linja,"popl %ecx","popl %eax",operazzjoni_VALUE + " %ecx, %eax","pushl %eax");
            } else if (kmand == 108 || kmand == 112) Collections.addAll(linja,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + pożizzjoni_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + pożizzjoni_INDEX + "_divide","xorl %edx, %edx","jmp " + pożizzjoni_INDEX + "_done",pożizzjoni_INDEX + "_divide:","cltd","idivl %ecx",pożizzjoni_INDEX + "_done:","pushl " + (kmand == 108 ? "%eax" : "%edx"));
            else if (kmand == 116) linja.add("negl (%esp)");
            else if (kmand == 120 || kmand == 122 || kmand == 124) Collections.addAll(linja,"popl %ecx","popl %eax",(kmand == 120 ? "sall" : kmand == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (kmand == 132) {
                int INDEX = kmand_data.한바이트(), 증가 = kmand_data.부호한바이트(); ċekk_lokali(INDEX,lokali_COUNT); linja.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (kmand >= 145 && kmand <= 147) Collections.addAll(linja,"popl %eax",kmand == 145 ? "movsbl %al, %eax" : kmand == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (kmand >= 153 && kmand <= 166) {
                if (kmand <= 158) Collections.addAll(linja,"popl %eax","testl %eax, %eax");
                else Collections.addAll(linja,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int destinazzjoni_VALUE = pożizzjoni + kmand_data.부호두바이트(); fergħa_Lista.add(destinazzjoni_VALUE); linja.add(비교들[kmand - (kmand <= 158 ? 153 : 159)] + " " + 표식 + "_b" + destinazzjoni_VALUE);
            } else if (kmand == 167 || kmand == 200) {
                int destinazzjoni_VALUE = pożizzjoni + (kmand == 167 ? kmand_data.부호두바이트() : kmand_data.네바이트()); fergħa_Lista.add(destinazzjoni_VALUE); linja.add("jmp " + 표식 + "_b" + destinazzjoni_VALUE);
            } else if (kmand == 170 || kmand == 171) {
                while (kmand_data.pożizzjoni % 4 != 0) kmand_data.한바이트();
                int valur_default = pożizzjoni + kmand_data.네바이트(); fergħa_Lista.add(valur_default); linja.add("popl %eax");
                int element_COUNT, 아래 = 0;
                if (kmand == 170) { 아래 = kmand_data.네바이트(); int 위 = kmand_data.네바이트(); long tul_VALUE = (long)위 - 아래 + 1; if (tul_VALUE < 1 || tul_VALUE > (kmand_data.data.length - kmand_data.pożizzjoni) / 4) throw new Traduzzjoni_żball("switch klipp żball"); element_COUNT = (int)tul_VALUE; }
                else { element_COUNT = kmand_data.네바이트(); if (element_COUNT < 0 || element_COUNT > (kmand_data.data.length - kmand_data.pożizzjoni) / 8) throw new Traduzzjoni_żball("switch daqqas żball"); }
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                    int VALUE = kmand == 170 ? 아래 + 순번 : kmand_data.네바이트(), destinazzjoni_VALUE = pożizzjoni + kmand_data.네바이트(); fergħa_Lista.add(destinazzjoni_VALUE);
                    Collections.addAll(linja,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + destinazzjoni_VALUE);
                }
                linja.add("jmp " + 표식 + "_b" + valur_default);
            } else if (kmand == 172 || kmand == 176 || kmand == 177) {
                if (kmand != 177) linja.add("popl %eax"); Collections.addAll(linja,"leave","ret");
            } else if (kmand == 178 || kmand == 179) {
                metodu_Referenza Referenza = klassi_VALUE.Referenza(kmand_data.두바이트()); if (!필드들.containsKey(Referenza)) throw new Traduzzjoni_żball("알 수 없는 qasam_VALUE");
                Collections.addAll(linja,"call " + simbolu("init",Referenza.propjetarju_VALUE),(kmand == 178 ? "pushl " : "popl ") + simbolu("field",Referenza.부분들()));
            } else if (kmand == 184) {
                metodu_Referenza Referenza = klassi_VALUE.Referenza(kmand_data.두바이트()); if (!함수들.containsKey(Referenza)) throw new Traduzzjoni_żball("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Referenza.서술); Collections.addAll(linja,"call " + simbolu("init",Referenza.propjetarju_VALUE),"call " + simbolu("method",Referenza.부분들()));
                if (!호출형식.인수.isEmpty()) linja.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) linja.add("pushl %eax");
            } else if (kmand == 182) {
                metodu_Referenza Referenza = klassi_VALUE.Referenza(kmand_data.두바이트());
                if (Referenza.equals(new metodu_Referenza("java/lang/String","length","()I"))) Collections.addAll(linja,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Referenza.equals(new metodu_Referenza("java/lang/String","charAt","(I)C"))) Collections.addAll(linja,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Traduzzjoni_żball("가상 FUNCTION_VALUE 호출 미지원");
            } else if (kmand == 188) {
                if (kmand_data.한바이트() != 10) throw new Traduzzjoni_żball("new int[]만 Appoġġ_VALUE"); Collections.addAll(linja,"popl %eax","call rt_new_array","pushl %eax");
            } else if (kmand == 190) Collections.addAll(linja,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (kmand == 196) {
                int estensjoni_VALUE = kmand_data.한바이트(), INDEX = kmand_data.두바이트(); ċekk_lokali(INDEX,lokali_COUNT);
                if (estensjoni_VALUE == 21 || estensjoni_VALUE == 25 || estensjoni_VALUE == 54 || estensjoni_VALUE == 58) linja.add((estensjoni_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (estensjoni_VALUE == 132) linja.add("addl $" + kmand_data.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Traduzzjoni_żball("wide kmand 미지원");
            } else if (kmand == 198 || kmand == 199) {
                int destinazzjoni_VALUE = pożizzjoni + kmand_data.부호두바이트(); fergħa_Lista.add(destinazzjoni_VALUE); Collections.addAll(linja,"popl %eax","testl %eax, %eax",(kmand == 198 ? "je " : "jne ") + 표식 + "_b" + destinazzjoni_VALUE);
            } else throw new Traduzzjoni_żball("미지원 kmand: " + kmand);
        }
        if (!경계들.containsAll(fergħa_Lista)) throw new Traduzzjoni_żball("kmand 경계가 아닌 곳으로 fergħa");
        linja.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",linja);
    }
    String 엑스상수(klassi_data data, int INDEX) {
        if (data.상수종류[INDEX] == 3) return data.valur_fiss_data[INDEX].toString();
        if (data.상수종류[INDEX] == 8) return string_simbolu(data.문자((Integer)data.valur_fiss_data[INDEX]));
        throw new Traduzzjoni_żball("정수와 string_VALUE 상수만 Appoġġ_VALUE");
    }
    String 엑스조립본(String entrata_punt, List<String> 내보냄, String mira) throws IOException {
        Map<String,String> kompjuter_tabella = new HashMap<>();
        for (String linja : Files.readAllLines(riżorsa_mogħdija.resolve("엑스기계함수.tsv"))) { String[] par_VALUE = linja.split("\t"); if (par_VALUE[0].equals(mira)) kompjuter_tabella.put(par_VALUE[1] + par_VALUE[2],par_VALUE[3]); }
        int pożizzjoni_INDEX = entrata_punt.lastIndexOf('.'); if (pożizzjoni_INDEX < 0) throw new Traduzzjoni_żball("entrata_punt assenja_VALUE żball");
        String propjetarju_VALUE = entrata_punt.substring(0,pożizzjoni_INDEX).replace('.','/'), metodu_entrata_isem = entrata_punt.substring(pożizzjoni_INDEX + 1); metodu_Referenza entrata_punt_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metodu_Referenza Referenza = new metodu_Referenza(propjetarju_VALUE,metodu_entrata_isem,서술); if (함수들.containsKey(Referenza)) { if (entrata_punt_VALUE != null) throw new Traduzzjoni_żball("겹친 entrata_punt"); entrata_punt_VALUE = Referenza; } }
        if (entrata_punt_VALUE == null || (함수들.get(entrata_punt_VALUE).aċċess_entrata & 0x100) != 0) throw new Traduzzjoni_żball("entrata_punt_VALUE FUNCTION_VALUE format_VALUE żball");
        List<String> linja = new ArrayList<>(); linja.add(".code32");
        for (klassi_data data : 클래스들.values()) {
            String stat_VALUE = simbolu("state",data.isem), inizjala = simbolu("init",data.isem);
            Collections.addAll(linja,".bss",".balign 4",stat_VALUE + ": .long 0",".text",inizjala + ":","cmpl $0, " + stat_VALUE,"jne " + inizjala + "_done","movl $1, " + stat_VALUE);
            metodu_Referenza 초기화참조 = new metodu_Referenza(data.isem,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) linja.add("call " + simbolu("method",초기화참조.부분들()));
            Collections.addAll(linja,"movl $2, " + stat_VALUE,inizjala + "_done:","ret");
            for (membru_data qasam_VALUE : data.qasam_VALUE) {
                byte[] valur_fiss_VALUE = qasam_VALUE.attribut_VALUE.get("ConstantValue"); String VALUE = valur_fiss_VALUE == null ? "0" : 엑스상수(data,new data_Qarrej(valur_fiss_VALUE).두바이트());
                Collections.addAll(linja,".data",".balign 4",simbolu("field",data.isem,qasam_VALUE.isem,qasam_VALUE.서술) + ": .long " + VALUE);
            }
            for (membru_data FUNCTION_VALUE : data.FUNCTION_VALUE) if (!FUNCTION_VALUE.isem.equals("<init>")) linja.add(엑스함수본문(new metodu_Referenza(data.isem,FUNCTION_VALUE.isem,FUNCTION_VALUE.서술),FUNCTION_VALUE,kompjuter_tabella,mira));
        }
        Collections.addAll(linja,".text",".globl java_entry","java_entry:","call " + simbolu("init",entrata_punt_VALUE.propjetarju_VALUE),"call " + simbolu("method",entrata_punt_VALUE.부분들()));
        if (entrata_punt_VALUE.서술.equals("()V")) linja.add("xorl %eax, %eax"); linja.add("ret");
        for (String assenja_VALUE : 내보냄) {
            int delimitatur_VALUE = assenja_VALUE.indexOf('='); if (delimitatur_VALUE < 1) throw new Traduzzjoni_żball("내보내기 assenja_VALUE żball");
            String 외부 = assenja_VALUE.substring(0,delimitatur_VALUE), FUNCTION_VALUE = assenja_VALUE.substring(delimitatur_VALUE + 1); int diviżjoni_miżura = FUNCTION_VALUE.lastIndexOf('.');
            if (diviżjoni_miżura < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Traduzzjoni_żball("내보내기 simbolu żball");
            String klassi_VALUE = FUNCTION_VALUE.substring(0,diviżjoni_miżura).replace('.','/'), isem = FUNCTION_VALUE.substring(diviżjoni_miżura + 1); metodu_Referenza għażla_VALUE = null;
            for (metodu_Referenza Referenza : 함수들.keySet()) if (Referenza.propjetarju_VALUE.equals(klassi_VALUE) && Referenza.isem.equals(isem)) { if (għażla_VALUE != null) throw new Traduzzjoni_żball("겹친 내보내기 mira"); għażla_VALUE = Referenza; }
            if (għażla_VALUE == null) throw new Traduzzjoni_żball("내보낼 함수가 없음");
            Collections.addAll(linja,".text",".globl " + 외부,외부 + ":","call " + simbolu("init",għażla_VALUE.propjetarju_VALUE),"jmp " + simbolu("method",għażla_VALUE.부분들()));
        }
        linja.add(".section .rodata");
        for (Map.Entry<String,String> entrata_VALUE : 문자열들.entrySet()) {
            Collections.addAll(linja,".balign 4",entrata_VALUE.getValue() + ":",".long " + entrata_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lezzjoni_VALUE : entrata_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(lezzjoni_VALUE)); if (!단위들.isEmpty()) linja.add(".long " + String.join(",",단위들));
        }
        linja.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",linja) + "\n";
    }
    static void eżegwixxa_għodda(List<String> kmand) throws Exception {
        if (new ProcessBuilder(kmand).inheritIO().start().waitFor() != 0) throw new Traduzzjoni_żball("bena_sors żball: " + kmand.get(0));
    }
    static String data_string(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String mira, String entrata_punt, List<String> 내보냄, Path 출력, Path riżorsa_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), klassi_mogħdija = 임시.resolve("classes"); Files.createDirectory(klassi_mogħdija);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",klassi_mogħdija.toString(),"-sourcepath",klassi_mogħdija.toString(),"-d",klassi_mogħdija.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int sors_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Traduzzjoni_żball("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); sors_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Traduzzjoni_żball(".java 또는 .class만 Appoġġ_VALUE");
            }
            if (sors_COUNT > 0) eżegwixxa_għodda(자바명령);
            try (java.util.stream.Stream<Path> mogħdija_Lista = Files.walk(klassi_mogħdija)) { mogħdija_Lista.filter(mogħdija -> mogħdija.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,mira.equals("user") ? "user" : "kernel",262144,riżorsa_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(entrata_punt,내보냄,mira); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path għodda_pożizzjoni = riżorsa_VALUE.getParent();
            eżegwixxa_għodda(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            eżegwixxa_għodda(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),għodda_pożizzjoni.resolve("tħaddim_tal_lingwa_komuni_Appoġġ.s").toString()));
            List<String> AQBAD = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (mira.equals("kernel")) AQBAD.add("-r");
            else {
                eżegwixxa_għodda(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),għodda_pożizzjoni.resolve(mira.equals("user") ? "Bidu_utent_programm.s" : "리눅스시작.s").toString()));
                Collections.addAll(AQBAD,"-e","_start",임시.resolve("start.o").toString());
                if (mira.equals("user")) Collections.addAll(AQBAD,"-T",għodda_pożizzjoni.resolve("utent_Link_Tqassim.ld").toString());
            }
            Collections.addAll(AQBAD,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); eżegwixxa_għodda(AQBAD);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path ppubblika_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),ppubblika_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(ppubblika_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(ppubblika_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(mira.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbolu_data = new ArrayList<>(), data_sors = new ArrayList<>();
            for (metodu_Referenza Referenza : CONVERT_VALUE.함수들.keySet()) simbolu_data.add(data_string(simbolu("method",Referenza.부분들())) + ":" + data_string(Referenza.propjetarju_VALUE + "." + Referenza.isem + Referenza.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_fajl = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte VALUE : hash_fajl) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                data_sors.add(data_string(입력.toAbsolutePath().toString()) + ":" + data_string(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + data_string(mira) + ",\"entry\":" + data_string(entrata_punt) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbolu_data) + "},\"sources\":{" + String.join(",",data_sors) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> mogħdija_Lista = Files.walk(임시)) { for (Path mogħdija : (Iterable<Path>)mogħdija_Lista.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(mogħdija); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String entrata_punt = null, mira = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> mogħdija_Lista = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry klassi_VALUE.FUNCTION_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export simbolu=klassi_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": entrata_punt = 인수[++순번]; break;
                    case "--profile": mira = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Traduzzjoni_żball("알 수 없는 옵션: " + VALUE); mogħdija_Lista.add(Paths.get(VALUE));
                }
            }
            if (entrata_punt == null || 출력경로 == null || mogħdija_Lista.isEmpty()) throw new Traduzzjoni_żball("--entry, -o, klassi_VALUE 파일이 필요합니다");
            Path riżorsa_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Traduzzjoni_żball("알 수 없는 eżegwixxa_kmand mira");
                엑스번역(mogħdija_Lista,엑스대상,entrata_punt,내보냄,출력경로,riżorsa_VALUE); return;
            }
            String sors = new 기계어미리번역(mogħdija_Lista, mira, 낱말수, riżorsa_VALUE).iġġenera(entrata_punt, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, sors, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception żball) { System.err.println("bena_sors żball: " + żball.getMessage()); System.exit(1); }
    }
}
