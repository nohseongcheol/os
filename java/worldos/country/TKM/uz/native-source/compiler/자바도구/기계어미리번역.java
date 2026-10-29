// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Sinf_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. tashkilotchi JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Tarjima_xato extends RuntimeException {
        Tarjima_xato(String 설명) { super(설명); }
    }
    static final class ma_lumotlar_o_quvchi {
        final byte[] ma_lumotlar;
        int Holati;
        ma_lumotlar_o_quvchi(byte[] 입력자료) { ma_lumotlar = 입력자료; }
        byte[] Oʻqish(int uzunlik_VALUE) {
            if (uzunlik_VALUE < 0 || uzunlik_VALUE > ma_lumotlar.length - Holati) throw new Tarjima_xato("잘린 Sinf_VALUE 또는 Buyruq ma_lumotlar");
            byte[] o_lchov = Arrays.copyOfRange(ma_lumotlar, Holati, Holati + uzunlik_VALUE); Holati += uzunlik_VALUE; return o_lchov;
        }
        int 한바이트() { if (Holati >= ma_lumotlar.length) throw new Tarjima_xato("잘린 Buyruq ma_lumotlar"); return ma_lumotlar[Holati++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class a_zo_ma_lumotlar {
        final int kirish_huquqi_kiritish;
        final String Nomi, 서술;
        final Map<String, byte[]> xususiyat_VALUE;
        a_zo_ma_lumotlar(int kirish_huquqi_VALUE, String nom_VALUE, String 서술값, Map<String, byte[]> xususiyat_ma_lumotlar) {
            kirish_huquqi_kiritish = kirish_huquqi_VALUE; Nomi = nom_VALUE; 서술 = 서술값; xususiyat_VALUE = xususiyat_ma_lumotlar;
        }
    }
    static final class uslub_Ma_lumotnomalar implements Comparable<uslub_Ma_lumotnomalar> {
        final String egasi_VALUE, Nomi, 서술;
        uslub_Ma_lumotnomalar(String 소유값, String nom_VALUE, String 서술값) { egasi_VALUE = 소유값; Nomi = nom_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{egasi_VALUE, Nomi, 서술}; }
        public int compareTo(uslub_Ma_lumotnomalar bir_rangli_VALUE) {
            int Taqqoslama_VALUE = egasi_VALUE.compareTo(bir_rangli_VALUE.egasi_VALUE);
            if (Taqqoslama_VALUE == 0) Taqqoslama_VALUE = Nomi.compareTo(bir_rangli_VALUE.Nomi);
            return Taqqoslama_VALUE == 0 ? 서술.compareTo(bir_rangli_VALUE.서술) : Taqqoslama_VALUE;
        }
        public boolean equals(Object bir_rangli_VALUE) { return bir_rangli_VALUE instanceof uslub_Ma_lumotnomalar && compareTo((uslub_Ma_lumotnomalar) bir_rangli_VALUE) == 0; }
        public int hashCode() { return Objects.hash(egasi_VALUE, Nomi, 서술); }
    }
    static final class Sinf_ma_lumotlar {
        final int[] 상수종류;
        final Object[] konstanta_ma_lumotlar;
        final String Nomi;
        final List<a_zo_ma_lumotlar> ma_lumotlar_maydoni_VALUE, FUNCTION_VALUE;
        Sinf_ma_lumotlar(Path yo_l) throws IOException {
            ma_lumotlar_o_quvchi o_quvchi_VALUE = new ma_lumotlar_o_quvchi(Files.readAllBytes(yo_l));
            if (o_quvchi_VALUE.네바이트() != 0xcafebabe) throw new Tarjima_xato("Java Sinf_VALUE 표식이 아님");
            o_quvchi_VALUE.Oʻqish(4);
            int element_COUNT = o_quvchi_VALUE.두바이트(); 상수종류 = new int[element_COUNT]; konstanta_ma_lumotlar = new Object[element_COUNT];
            for (int 순번 = 1; 순번 < element_COUNT; 순번++) {
                int 종류 = o_quvchi_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int uzunlik_VALUE = o_quvchi_VALUE.두바이트();
                        byte[] belgi_bufer = o_quvchi_VALUE.Oʻqish(uzunlik_VALUE), 길이붙인자료 = new byte[uzunlik_VALUE + 2];
                        길이붙인자료[0] = (byte)(uzunlik_VALUE >> 8); 길이붙인자료[1] = (byte)uzunlik_VALUE;
                        System.arraycopy(belgi_bufer, 0, 길이붙인자료, 2, uzunlik_VALUE);
                        konstanta_ma_lumotlar[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstanta_ma_lumotlar[순번] = o_quvchi_VALUE.네바이트(); break;
                    case 4: o_quvchi_VALUE.Oʻqish(4); break;
                    case 5: case 6: o_quvchi_VALUE.Oʻqish(8); 순번++; break;
                    case 7: case 8: case 16: konstanta_ma_lumotlar[순번] = o_quvchi_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstanta_ma_lumotlar[순번] = new int[]{o_quvchi_VALUE.두바이트(), o_quvchi_VALUE.두바이트()}; break;
                    case 15: konstanta_ma_lumotlar[순번] = new int[]{o_quvchi_VALUE.한바이트(), o_quvchi_VALUE.두바이트()}; break;
                    default: throw new Tarjima_xato("지원하지 않는 konstanta_VALUE 종류: " + 종류);
                }
            }
            o_quvchi_VALUE.두바이트(); Nomi = Sinf_nom(o_quvchi_VALUE.두바이트());
            if (!Sinf_nom(o_quvchi_VALUE.두바이트()).equals("java/lang/Object") || o_quvchi_VALUE.두바이트() != 0)
                throw new Tarjima_xato(Nomi + ": 상속 및 인터페이스 미지원");
            ma_lumotlar_maydoni_VALUE = 멤버읽기(o_quvchi_VALUE); FUNCTION_VALUE = 멤버읽기(o_quvchi_VALUE); 속성읽기(o_quvchi_VALUE);
            if (o_quvchi_VALUE.Holati != o_quvchi_VALUE.ma_lumotlar.length) throw new Tarjima_xato("Sinf_VALUE 뒤에 남은 ma_lumotlar");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Tarjima_xato("문자 konstanta_VALUE INDEX Xato");
            return (String) konstanta_ma_lumotlar[INDEX];
        }
        String Sinf_nom(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Tarjima_xato("Sinf_VALUE Ma_lumotnomalar Xato");
            return 문자((Integer)konstanta_ma_lumotlar[INDEX]);
        }
        uslub_Ma_lumotnomalar Ma_lumotnomalar(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Tarjima_xato("멤버 Ma_lumotnomalar Xato");
            int[] juftlab_ulamoq_VALUE = (int[])konstanta_ma_lumotlar[INDEX], nom_juftlab_ulamoq = (int[])konstanta_ma_lumotlar[juftlab_ulamoq_VALUE[1]];
            return new uslub_Ma_lumotnomalar(Sinf_nom(juftlab_ulamoq_VALUE[0]), 문자(nom_juftlab_ulamoq[0]), 문자(nom_juftlab_ulamoq[1]));
        }
        Map<String, byte[]> 속성읽기(ma_lumotlar_o_quvchi o_quvchi_VALUE) {
            Map<String, byte[]> o_lchov = new LinkedHashMap<>();
            int element_COUNT = o_quvchi_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                String xususiyat_nom = 문자(o_quvchi_VALUE.두바이트()); byte[] VALUE = o_quvchi_VALUE.Oʻqish(o_quvchi_VALUE.네바이트());
                if (o_lchov.put(xususiyat_nom, VALUE) != null) throw new Tarjima_xato("겹친 xususiyat_VALUE: " + xususiyat_nom);
            }
            return o_lchov;
        }
        List<a_zo_ma_lumotlar> 멤버읽기(ma_lumotlar_o_quvchi o_quvchi_VALUE) {
            List<a_zo_ma_lumotlar> o_lchov = new ArrayList<>(); int element_COUNT = o_quvchi_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                int kirish_huquqi_kiritish = o_quvchi_VALUE.두바이트(); String uslub_kiritish_nom = 문자(o_quvchi_VALUE.두바이트()), 서술 = 문자(o_quvchi_VALUE.두바이트());
                o_lchov.add(new a_zo_ma_lumotlar(kirish_huquqi_kiritish, uslub_kiritish_nom, 서술, 속성읽기(o_quvchi_VALUE)));
            }
            return o_lchov;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String qaytarish_o_lchov;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Tarjima_xato("FUNCTION_VALUE 서술 Xato: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Tarjima_xato("FUNCTION_VALUE 서술 Xato: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Tarjima_xato("FUNCTION_VALUE 서술 Xato: " + 서술);
            qaytarish_o_lchov = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> o_lchov = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Holati = 0; Holati < 서술.length();) {
            String tanlanma_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, Holati)) { tanlanma_VALUE = format_VALUE; break; }
            if (tanlanma_VALUE == null) throw new Tarjima_xato("지원하지 않는 ma_lumotlar_turi: " + 서술);
            o_lchov.add(tanlanma_VALUE); Holati += tanlanma_VALUE.length();
        }
        return o_lchov;
    }
    static String ramz(String 종류, String... 부분들) {
        try {
            byte[] tasodifiy_ma_lumot_fayl = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Matn = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Matn.append(String.format(Locale.ROOT, "%02x", tasodifiy_ma_lumot_fayl[순번] & 255));
            return Matn.toString();
        } catch (Exception Xato) { throw new Tarjima_xato(Xato.toString()); }
    }
    final Map<String, Sinf_ma_lumotlar> 클래스들 = new TreeMap<>();
    final Map<uslub_Ma_lumotnomalar, a_zo_ma_lumotlar> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, 기계클래스;
    final int 동적기억낱말수;
    final Path resurs_yo_l;
    기계어미리번역(List<Path> yo_l_Ro_yxat, String nishon, int 낱말수, Path resurs_VALUE) throws IOException {
        if ((!nishon.equals("kernel") && !nishon.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Tarjima_xato("bajarmoq_buyruq nishon 또는 Xotira_VALUE 공간 Hajmi Xato");
        실행대상 = nishon; 동적기억낱말수 = 낱말수; resurs_yo_l = resurs_VALUE;
        // 이 이름도 국가별 manba_daraxt generatsiiyalash 시 해당 언어로 옮긴다.
        기계클래스 = nishon.equals("kernel") ? "yozuv_taxtasi" : "foydalanuvchi";
        for (String satr : Files.readAllLines(resurs_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = satr.split("\t", -1);
            if (부분들.length != 4) throw new Tarjima_xato("기계 FUNCTION_VALUE ma_lumotlar Xato");
            if (부분들[0].equals(nishon)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path yo_l : yo_l_Ro_yxat) {
            Sinf_ma_lumotlar ma_lumotlar = new Sinf_ma_lumotlar(yo_l);
            if (클래스들.put(ma_lumotlar.Nomi, ma_lumotlar) != null) throw new Tarjima_xato("중복 Sinf_VALUE: " + ma_lumotlar.Nomi);
            for (a_zo_ma_lumotlar ma_lumotlar_maydoni_VALUE : ma_lumotlar.ma_lumotlar_maydoni_VALUE) {
                if ((ma_lumotlar_maydoni_VALUE.kirish_huquqi_kiritish & 8) == 0 || 형식읽기(ma_lumotlar_maydoni_VALUE.서술).equals(Collections.singletonList("V"))) throw new Tarjima_xato("statik_VALUE 필드만 madad_VALUE");
                if (필드들.put(new uslub_Ma_lumotnomalar(ma_lumotlar.Nomi, ma_lumotlar_maydoni_VALUE.Nomi, ma_lumotlar_maydoni_VALUE.서술), ma_lumotlar_maydoni_VALUE) != null) throw new Tarjima_xato("중복 ma_lumotlar_maydoni_VALUE");
            }
            for (a_zo_ma_lumotlar FUNCTION_VALUE : ma_lumotlar.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Nomi.equals("<init>")) continue;
                if ((FUNCTION_VALUE.kirish_huquqi_kiritish & 8) == 0 || (FUNCTION_VALUE.kirish_huquqi_kiritish & (0x20 | 0x400)) != 0) throw new Tarjima_xato("statik_VALUE 비동기화 함수만 madad_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new uslub_Ma_lumotnomalar(ma_lumotlar.Nomi, FUNCTION_VALUE.Nomi, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Tarjima_xato("중복 FUNCTION_VALUE");
            }
        }
    }
    String satr_ramz(String Matn) { return 문자열들.computeIfAbsent(Matn, VALUE -> "j_text_" + 문자열들.size()); }
    String konstanta_ifoda(Sinf_ma_lumotlar ma_lumotlar, int INDEX) {
        if (INDEX < 1 || INDEX >= ma_lumotlar.상수종류.length) throw new Tarjima_xato("konstanta_VALUE INDEX klip Xato");
        if (ma_lumotlar.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + ma_lumotlar.konstanta_ma_lumotlar[INDEX] + ")";
        if (ma_lumotlar.상수종류[INDEX] == 8) return "(word)" + satr_ramz(ma_lumotlar.문자((Integer)ma_lumotlar.konstanta_ma_lumotlar[INDEX]));
        throw new Tarjima_xato("정수와 satr_VALUE 상수만 madad_VALUE");
    }
    String 함수원형(uslub_Ma_lumotnomalar Ma_lumotnomalar) {
        List<String> 인수들 = new ArrayList<>(); int element_COUNT = new 함수형식(Ma_lumotnomalar.서술).인수.size();
        for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + ramz("method", Ma_lumotnomalar.부분들()) + "(" + (element_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void chek_mahalliy(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Tarjima_xato("mahalliy_soha 변수 INDEX klip Xato"); }
    void 분기넣기(List<String> 출력, Set<Integer> shox_Ro_yxat, int Holati, int 이동량, String holat) {
        int ko_chirish_joyi_VALUE = Holati + 이동량; shox_Ro_yxat.add(ko_chirish_joyi_VALUE);
        출력.add((holat == null ? "" : "if (" + holat + ") ") + "goto b" + ko_chirish_joyi_VALUE + ";");
    }
    String 함수본문(uslub_Ma_lumotnomalar FUNCTION_VALUE, a_zo_ma_lumotlar ma_lumotlar) {
        byte[] 본문자료 = ma_lumotlar.xususiyat_VALUE.get("Code"); if (본문자료 == null) throw new Tarjima_xato("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Nomi);
        ma_lumotlar_o_quvchi o_quvchi_VALUE = new ma_lumotlar_o_quvchi(본문자료); int 쌓임깊이 = o_quvchi_VALUE.두바이트(), 지역변수수 = o_quvchi_VALUE.두바이트();
        ma_lumotlar_o_quvchi buyruq_ma_lumotlar = new ma_lumotlar_o_quvchi(o_quvchi_VALUE.Oʻqish(o_quvchi_VALUE.네바이트()));
        if (o_quvchi_VALUE.두바이트() != 0) throw new Tarjima_xato("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (지역변수수 < format_VALUE.인수.size()) throw new Tarjima_xato("매개변수보다 적은 mahalliy_soha 변수");
        Sinf_ma_lumotlar Sinf_VALUE = 클래스들.get(FUNCTION_VALUE.egasi_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(FUNCTION_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), shox_Ro_yxat = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (buyruq_ma_lumotlar.Holati < buyruq_ma_lumotlar.ma_lumotlar.length) {
            int Holati = buyruq_ma_lumotlar.Holati, Buyruq = buyruq_ma_lumotlar.한바이트(); 경계들.add(Holati); 출력.add("b" + Holati + ":;");
            if (Buyruq == 0) continue;
            if (Buyruq == 1) 출력.add("PUSH(0);");
            else if (Buyruq >= 2 && Buyruq <= 8) 출력.add("PUSH((uint32_t)(" + (Buyruq - 3) + "));");
            else if (Buyruq == 16 || Buyruq == 17) 출력.add("PUSH((uint32_t)(" + (Buyruq == 16 ? buyruq_ma_lumotlar.부호한바이트() : buyruq_ma_lumotlar.부호두바이트()) + "));");
            else if (Buyruq == 18 || Buyruq == 19) 출력.add("PUSH(" + konstanta_ifoda(Sinf_VALUE, Buyruq == 18 ? buyruq_ma_lumotlar.한바이트() : buyruq_ma_lumotlar.두바이트()) + ");");
            else if (Buyruq == 21 || Buyruq == 25 || (Buyruq >= 26 && Buyruq <= 29) || (Buyruq >= 42 && Buyruq <= 45)) {
                int INDEX = Buyruq == 21 || Buyruq == 25 ? buyruq_ma_lumotlar.한바이트() : Buyruq - (Buyruq <= 29 ? 26 : 42);
                chek_mahalliy(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (Buyruq == 54 || Buyruq == 58 || (Buyruq >= 59 && Buyruq <= 62) || (Buyruq >= 75 && Buyruq <= 78)) {
                int INDEX = Buyruq == 54 || Buyruq == 58 ? buyruq_ma_lumotlar.한바이트() : Buyruq - (Buyruq <= 62 ? 59 : 75);
                chek_mahalliy(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (Buyruq == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Buyruq == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Buyruq == 87 || Buyruq == 88) 출력.add(Buyruq == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Buyruq >= 89 && Buyruq <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] tartib_Ro_yxat = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Buyruq - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : tartib_Ro_yxat[Buyruq - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (Buyruq == 96 || Buyruq == 100 || Buyruq == 104 || Buyruq == 126 || Buyruq == 128 || Buyruq == 130) {
                String jarrohlik_VALUE = Buyruq == 96 ? "+" : Buyruq == 100 ? "-" : Buyruq == 104 ? "*" : Buyruq == 126 ? "&" : Buyruq == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + jarrohlik_VALUE + " (uint32_t)b);");
            } else if (Buyruq == 108 || Buyruq == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Buyruq == 112 ? 1 : 0) + "));");
            else if (Buyruq == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Buyruq == 120 || Buyruq == 122 || Buyruq == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Buyruq == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Buyruq == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Buyruq == 132) {
                int INDEX = buyruq_ma_lumotlar.한바이트(), 증가량 = buyruq_ma_lumotlar.부호한바이트(); chek_mahalliy(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Buyruq >= 145 && Buyruq <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Buyruq == 145 ? "int8_t" : Buyruq == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Buyruq >= 153 && Buyruq <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, shox_Ro_yxat, Holati, buyruq_ma_lumotlar.부호두바이트(), "(int32_t)a " + 비교들[Buyruq - 153] + " 0");
            } else if (Buyruq >= 159 && Buyruq <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, shox_Ro_yxat, Holati, buyruq_ma_lumotlar.부호두바이트(), Buyruq >= 165 ? "a " + 비교들[Buyruq - 159] + " b" : "(int32_t)a " + 비교들[Buyruq - 159] + " (int32_t)b");
            } else if (Buyruq == 167 || Buyruq == 200) 분기넣기(출력, shox_Ro_yxat, Holati, Buyruq == 167 ? buyruq_ma_lumotlar.부호두바이트() : buyruq_ma_lumotlar.네바이트(), null);
            else if (Buyruq == 170 || Buyruq == 171) {
                while (buyruq_ma_lumotlar.Holati % 4 != 0) buyruq_ma_lumotlar.한바이트();
                int sukut_bo_yicha_qiymat = buyruq_ma_lumotlar.네바이트(); 출력.add("a = POP();");
                if (Buyruq == 170) {
                    int 아래 = buyruq_ma_lumotlar.네바이트(), 위 = buyruq_ma_lumotlar.네바이트(); long element_COUNT = (long)위 - 아래 + 1;
                    if (element_COUNT < 1 || element_COUNT > (buyruq_ma_lumotlar.ma_lumotlar.length - buyruq_ma_lumotlar.Holati) / 4) throw new Tarjima_xato("switch klip Xato");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, shox_Ro_yxat, Holati, buyruq_ma_lumotlar.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int element_COUNT = buyruq_ma_lumotlar.네바이트(), old_kamera_ma_lumotlar = 0;
                    if (element_COUNT < 0 || element_COUNT > (buyruq_ma_lumotlar.ma_lumotlar.length - buyruq_ma_lumotlar.Holati) / 8) throw new Tarjima_xato("switch Hajmi Xato");
                    for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                        int VALUE = buyruq_ma_lumotlar.네바이트(); if (순번 > 0 && VALUE <= old_kamera_ma_lumotlar) throw new Tarjima_xato("switch tartib_VALUE Xato"); old_kamera_ma_lumotlar = VALUE;
                        분기넣기(출력, shox_Ro_yxat, Holati, buyruq_ma_lumotlar.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, shox_Ro_yxat, Holati, sukut_bo_yicha_qiymat, null);
            } else if (Buyruq == 172 || Buyruq == 176 || Buyruq == 177) 출력.add("return " + (Buyruq == 177 ? "0" : "POP()") + ";");
            else if (Buyruq == 178 || Buyruq == 179) {
                uslub_Ma_lumotnomalar Ma_lumotnomalar = Sinf_VALUE.Ma_lumotnomalar(buyruq_ma_lumotlar.두바이트()); if (!필드들.containsKey(Ma_lumotnomalar)) throw new Tarjima_xato("알 수 없는 ma_lumotlar_maydoni_VALUE");
                출력.add(ramz("init", Ma_lumotnomalar.egasi_VALUE) + "();"); String ma_lumotlar_maydoni_VALUE = ramz("field", Ma_lumotnomalar.부분들());
                출력.add(Buyruq == 178 ? "PUSH(" + ma_lumotlar_maydoni_VALUE + ");" : ma_lumotlar_maydoni_VALUE + " = POP();");
            } else if (Buyruq == 184) {
                uslub_Ma_lumotnomalar Ma_lumotnomalar = Sinf_VALUE.Ma_lumotnomalar(buyruq_ma_lumotlar.두바이트()); if (!함수들.containsKey(Ma_lumotnomalar)) throw new Tarjima_xato("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Ma_lumotnomalar.서술); int element_COUNT = 호출형식.인수.size();
                출력.add(ramz("init", Ma_lumotnomalar.egasi_VALUE) + "();"); 출력.add("if(sp < " + element_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + element_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < element_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + ramz("method", Ma_lumotnomalar.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.qaytarish_o_lchov.equals("V")) 출력.add("PUSH(a);");
            } else if (Buyruq == 182) {
                uslub_Ma_lumotnomalar Ma_lumotnomalar = Sinf_VALUE.Ma_lumotnomalar(buyruq_ma_lumotlar.두바이트());
                if (Ma_lumotnomalar.equals(new uslub_Ma_lumotnomalar("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Ma_lumotnomalar.equals(new uslub_Ma_lumotnomalar("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Tarjima_xato("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Buyruq == 188) {
                if (buyruq_ma_lumotlar.한바이트() != 10) throw new Tarjima_xato("new int[]만 madad_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Buyruq == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Buyruq == 196) {
                int kengaytma_VALUE = buyruq_ma_lumotlar.한바이트(), INDEX = buyruq_ma_lumotlar.두바이트(); chek_mahalliy(INDEX, 지역변수수);
                if (kengaytma_VALUE == 21 || kengaytma_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (kengaytma_VALUE == 54 || kengaytma_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (kengaytma_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + buyruq_ma_lumotlar.부호두바이트() + ");");
                else throw new Tarjima_xato("미지원 wide Buyruq");
            } else if (Buyruq == 198 || Buyruq == 199) {
                출력.add("a = POP();"); 분기넣기(출력, shox_Ro_yxat, Holati, buyruq_ma_lumotlar.부호두바이트(), "a " + (Buyruq == 198 ? "==" : "!=") + " 0");
            } else throw new Tarjima_xato(FUNCTION_VALUE.egasi_VALUE + "." + FUNCTION_VALUE.Nomi + ", bayt_VALUE " + Holati + ": 미지원 Buyruq " + Buyruq);
        }
        if (!경계들.containsAll(shox_Ro_yxat)) throw new Tarjima_xato("Buyruq 경계가 아닌 곳으로 shox");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String eksport_qilmoq_uslub(String ulash_ramz, String nishon, boolean 진입점여부) {
        int holat_INDEX = nishon.lastIndexOf('.'); if (holat_INDEX < 0 || !ulash_ramz.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tarjima_xato("내보내기 tayinlash_VALUE Xato");
        String egasi_VALUE = nishon.substring(0, holat_INDEX).replace('.', '/'), Nomi = nishon.substring(holat_INDEX + 1); uslub_Ma_lumotnomalar tanlanma_VALUE = null;
        for (uslub_Ma_lumotnomalar Ma_lumotnomalar : 함수들.keySet()) if (Ma_lumotnomalar.egasi_VALUE.equals(egasi_VALUE) && Ma_lumotnomalar.Nomi.equals(Nomi)) {
            if (tanlanma_VALUE != null) throw new Tarjima_xato("겹친 내보내기 nishon"); tanlanma_VALUE = Ma_lumotnomalar;
        }
        if (tanlanma_VALUE == null || (함수들.get(tanlanma_VALUE).kirish_huquqi_kiritish & 0x100) != 0) throw new Tarjima_xato("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 format_VALUE = new 함수형식(tanlanma_VALUE.서술);
        if ((진입점여부 && !format_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.qaytarish_o_lchov)) throw new Tarjima_xato("kiritish_nuqta_VALUE 또는 C 경계 format_VALUE Xato");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) {
            if (!format_VALUE.인수.get(순번).equals("I")) throw new Tarjima_xato("C 경계는 int 인수만 madad_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.qaytarish_o_lchov.equals("V") ? "void " : "int32_t ") + ulash_ramz + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + ramz("init", tanlanma_VALUE.egasi_VALUE) + "(); " + (format_VALUE.qaytarish_o_lchov.equals("V") ? "" : "return (int32_t)") + ramz("method", tanlanma_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generatsiiyalash(String kiritish_nuqta, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<uslub_Ma_lumotnomalar, a_zo_ma_lumotlar> kiritish_VALUE : 함수들.entrySet()) {
            uslub_Ma_lumotnomalar Ma_lumotnomalar = kiritish_VALUE.getKey(); a_zo_ma_lumotlar ma_lumotlar = kiritish_VALUE.getValue(); 선언들.add(함수원형(Ma_lumotnomalar) + ";");
            if ((ma_lumotlar.kirish_huquqi_kiritish & 0x100) != 0) {
                String Ulanish = 기계함수들.get(Ma_lumotnomalar.Nomi + Ma_lumotnomalar.서술);
                if (!Ma_lumotnomalar.egasi_VALUE.equals(기계클래스) || Ulanish == null) throw new Tarjima_xato("허용되지 않은 native FUNCTION_VALUE: " + Ma_lumotnomalar.Nomi);
                int element_COUNT = new 함수형식(Ma_lumotnomalar.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Ulanish + "(" + (element_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(element_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Ma_lumotnomalar) + " { return " + Ulanish + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Ma_lumotnomalar, ma_lumotlar));
        }
        for (Map.Entry<uslub_Ma_lumotnomalar, a_zo_ma_lumotlar> kiritish_VALUE : 필드들.entrySet()) {
            uslub_Ma_lumotnomalar Ma_lumotnomalar = kiritish_VALUE.getKey(); byte[] konstanta_VALUE = kiritish_VALUE.getValue().xususiyat_VALUE.get("ConstantValue");
            String VALUE = konstanta_VALUE == null ? "0" : konstanta_ifoda(클래스들.get(Ma_lumotnomalar.egasi_VALUE), new ma_lumotlar_o_quvchi(konstanta_VALUE).두바이트());
            필드선언들.add("static word " + ramz("field", Ma_lumotnomalar.부분들()) + " = " + VALUE + ";");
        }
        for (String Nomi : 클래스들.keySet()) {
            String ishga_tushirmoq = ramz("init", Nomi), holat_VALUE_e10195a1 = ramz("state", Nomi);
            선언들.add("static void " + ishga_tushirmoq + "(void);"); 필드선언들.add("static unsigned " + holat_VALUE_e10195a1 + ";");
            uslub_Ma_lumotnomalar Ma_lumotnomalar = new uslub_Ma_lumotnomalar(Nomi, "<clinit>", "()V");
            몸체들.add("static void " + ishga_tushirmoq + "(void) { if(" + holat_VALUE_e10195a1 + ") return; " + holat_VALUE_e10195a1 + " = 1; " + (함수들.containsKey(Ma_lumotnomalar) ? ramz("method", Ma_lumotnomalar.부분들()) + "(); " : "") + holat_VALUE_e10195a1 + " = 2; }");
        }
        몸체들.add(eksport_qilmoq_uslub("java_entry", kiritish_nuqta, true)); Set<String> 공개이름 = new HashSet<>();
        for (String tayinlash_VALUE : 내보내기목록) {
            int holat_INDEX = tayinlash_VALUE.indexOf('='); if (holat_INDEX < 1) throw new Tarjima_xato("내보내기 tayinlash_VALUE Xato");
            String Nomi = tayinlash_VALUE.substring(0, holat_INDEX); 공개이름.add(Nomi); 몸체들.add(eksport_qilmoq_uslub(Nomi, tayinlash_VALUE.substring(holat_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> kiritish_VALUE : 문자열들.entrySet()) {
            String Matn = kiritish_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + kiritish_VALUE.getValue() + "[] = {" + Matn.length());
            for (int 순번 = 0; 순번 < Matn.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Matn.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String madad_VALUE = Files.readString(resurs_yo_l.resolve("umumiy_til_ish_jarayoni_madad.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(madad_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String manba, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nom_jadval = new HashMap<>();
        for (String satr : Files.readAllLines(resurs_yo_l.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] juftlab_ulamoq_VALUE = satr.split("\t"); nom_jadval.put(juftlab_ulamoq_VALUE[0], juftlab_ulamoq_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(manba); StringBuffer o_lchov = new StringBuffer();
        while (찾개.find()) {
            String Nomi = 찾개.group(), 새이름 = Nomi;
            if (!Nomi.startsWith("//") && !Nomi.startsWith("/*") && !Nomi.startsWith("\"") && !Nomi.startsWith("'") && !공개이름.contains(Nomi)) {
                새이름 = nom_jadval.getOrDefault(Nomi, Nomi);
                if (Nomi.matches("a[0-9]+")) 새이름 = "인수" + Nomi.substring(1);
                if (Nomi.matches("b[0-9]+")) 새이름 = "shox" + Nomi.substring(1);
                if (범용표기) {
                    StringBuilder notatsiya_VALUE = new StringBuilder();
                    for (char belgi_VALUE : 새이름.toCharArray()) notatsiya_VALUE.append(belgi_VALUE < 128 ? Character.toString(belgi_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)belgi_VALUE));
                    새이름 = notatsiya_VALUE.toString();
                }
            }
            찾개.appendReplacement(o_lchov, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(o_lchov); return o_lchov.toString();
    }
    String 엑스함수본문(uslub_Ma_lumotnomalar FUNCTION_VALUE, a_zo_ma_lumotlar ma_lumotlar, Map<String,String> 기계표, String nishon) {
        String 표식 = ramz("method", FUNCTION_VALUE.부분들());
        List<String> satr = new ArrayList<>();
        if ((ma_lumotlar.kirish_huquqi_kiritish & 0x100) != 0) {
            String Ulanish = 기계표.get(FUNCTION_VALUE.Nomi + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.egasi_VALUE.equals(nishon.equals("kernel") ? "qurilma_VALUE" : "foydalanuvchi") || Ulanish == null) throw new Tarjima_xato("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Ulanish;
        }
        byte[] asosiy_matn = ma_lumotlar.xususiyat_VALUE.get("Code"); if (asosiy_matn == null) throw new Tarjima_xato("FUNCTION_VALUE 몸체가 없음");
        ma_lumotlar_o_quvchi o_quvchi_VALUE = new ma_lumotlar_o_quvchi(asosiy_matn); o_quvchi_VALUE.두바이트(); int mahalliy_COUNT = o_quvchi_VALUE.두바이트();
        ma_lumotlar_o_quvchi buyruq_ma_lumotlar = new ma_lumotlar_o_quvchi(o_quvchi_VALUE.Oʻqish(o_quvchi_VALUE.네바이트()));
        if (o_quvchi_VALUE.두바이트() != 0) throw new Tarjima_xato("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (mahalliy_COUNT < format_VALUE.인수.size()) throw new Tarjima_xato("매개변수보다 적은 mahalliy_soha 변수");
        Collections.addAll(satr,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + mahalliy_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) Collections.addAll(satr,"movl " + (8 + 4 * (format_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Sinf_ma_lumotlar Sinf_VALUE = 클래스들.get(FUNCTION_VALUE.egasi_VALUE); Set<Integer> 경계들 = new HashSet<>(), shox_Ro_yxat = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (buyruq_ma_lumotlar.Holati < buyruq_ma_lumotlar.ma_lumotlar.length) {
            int Holati = buyruq_ma_lumotlar.Holati, Buyruq = buyruq_ma_lumotlar.한바이트(); String holat_INDEX = 표식 + "_b" + Holati;
            satr.add(holat_INDEX + ":"); 경계들.add(Holati);
            if (Buyruq == 0) satr.add("nop");
            else if (Buyruq == 1) satr.add("pushl $0");
            else if (Buyruq >= 2 && Buyruq <= 8) satr.add("pushl $" + (Buyruq - 3));
            else if (Buyruq == 16 || Buyruq == 17) satr.add("pushl $" + (Buyruq == 16 ? buyruq_ma_lumotlar.부호한바이트() : buyruq_ma_lumotlar.부호두바이트()));
            else if (Buyruq == 18 || Buyruq == 19) {
                int INDEX = Buyruq == 18 ? buyruq_ma_lumotlar.한바이트() : buyruq_ma_lumotlar.두바이트();
                satr.add("pushl $" + X_tugmasi_86_konstanta(Sinf_VALUE,INDEX));
            } else if (Buyruq == 21 || Buyruq == 25 || (Buyruq >= 26 && Buyruq <= 29) || (Buyruq >= 42 && Buyruq <= 45) || Buyruq == 54 || Buyruq == 58 || (Buyruq >= 59 && Buyruq <= 62) || (Buyruq >= 75 && Buyruq <= 78)) {
                boolean 읽음 = Buyruq < 54; int INDEX = Buyruq == 21 || Buyruq == 25 || Buyruq == 54 || Buyruq == 58 ? buyruq_ma_lumotlar.한바이트() : Buyruq - (Buyruq <= 29 ? 26 : Buyruq <= 45 ? 42 : Buyruq <= 62 ? 59 : 75);
                chek_mahalliy(INDEX,mahalliy_COUNT); satr.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Buyruq == 46) Collections.addAll(satr,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Buyruq == 79) Collections.addAll(satr,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Buyruq == 87 || Buyruq == 88) satr.add("addl $" + (Buyruq == 87 ? 4 : 8) + ", %esp");
            else if (Buyruq >= 89 && Buyruq <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] tartib_Ro_yxat = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Buyruq - 89]; 순번++) satr.add("popl " + 저장기들[순번]);
                for (int 순번 : tartib_Ro_yxat[Buyruq - 89]) satr.add("pushl " + 저장기들[순번]);
            } else if (Buyruq == 96 || Buyruq == 100 || Buyruq == 104 || Buyruq == 126 || Buyruq == 128 || Buyruq == 130) {
                String jarrohlik_VALUE = Buyruq == 96 ? "addl" : Buyruq == 100 ? "subl" : Buyruq == 104 ? "imull" : Buyruq == 126 ? "andl" : Buyruq == 128 ? "orl" : "xorl";
                Collections.addAll(satr,"popl %ecx","popl %eax",jarrohlik_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Buyruq == 108 || Buyruq == 112) Collections.addAll(satr,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + holat_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + holat_INDEX + "_divide","xorl %edx, %edx","jmp " + holat_INDEX + "_done",holat_INDEX + "_divide:","cltd","idivl %ecx",holat_INDEX + "_done:","pushl " + (Buyruq == 108 ? "%eax" : "%edx"));
            else if (Buyruq == 116) satr.add("negl (%esp)");
            else if (Buyruq == 120 || Buyruq == 122 || Buyruq == 124) Collections.addAll(satr,"popl %ecx","popl %eax",(Buyruq == 120 ? "sall" : Buyruq == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Buyruq == 132) {
                int INDEX = buyruq_ma_lumotlar.한바이트(), 증가 = buyruq_ma_lumotlar.부호한바이트(); chek_mahalliy(INDEX,mahalliy_COUNT); satr.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Buyruq >= 145 && Buyruq <= 147) Collections.addAll(satr,"popl %eax",Buyruq == 145 ? "movsbl %al, %eax" : Buyruq == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Buyruq >= 153 && Buyruq <= 166) {
                if (Buyruq <= 158) Collections.addAll(satr,"popl %eax","testl %eax, %eax");
                else Collections.addAll(satr,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int ko_chirish_joyi_VALUE = Holati + buyruq_ma_lumotlar.부호두바이트(); shox_Ro_yxat.add(ko_chirish_joyi_VALUE); satr.add(비교들[Buyruq - (Buyruq <= 158 ? 153 : 159)] + " " + 표식 + "_b" + ko_chirish_joyi_VALUE);
            } else if (Buyruq == 167 || Buyruq == 200) {
                int ko_chirish_joyi_VALUE = Holati + (Buyruq == 167 ? buyruq_ma_lumotlar.부호두바이트() : buyruq_ma_lumotlar.네바이트()); shox_Ro_yxat.add(ko_chirish_joyi_VALUE); satr.add("jmp " + 표식 + "_b" + ko_chirish_joyi_VALUE);
            } else if (Buyruq == 170 || Buyruq == 171) {
                while (buyruq_ma_lumotlar.Holati % 4 != 0) buyruq_ma_lumotlar.한바이트();
                int sukut_bo_yicha_qiymat = Holati + buyruq_ma_lumotlar.네바이트(); shox_Ro_yxat.add(sukut_bo_yicha_qiymat); satr.add("popl %eax");
                int element_COUNT, 아래 = 0;
                if (Buyruq == 170) { 아래 = buyruq_ma_lumotlar.네바이트(); int 위 = buyruq_ma_lumotlar.네바이트(); long uzunlik_VALUE = (long)위 - 아래 + 1; if (uzunlik_VALUE < 1 || uzunlik_VALUE > (buyruq_ma_lumotlar.ma_lumotlar.length - buyruq_ma_lumotlar.Holati) / 4) throw new Tarjima_xato("switch klip Xato"); element_COUNT = (int)uzunlik_VALUE; }
                else { element_COUNT = buyruq_ma_lumotlar.네바이트(); if (element_COUNT < 0 || element_COUNT > (buyruq_ma_lumotlar.ma_lumotlar.length - buyruq_ma_lumotlar.Holati) / 8) throw new Tarjima_xato("switch Hajmi Xato"); }
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                    int VALUE = Buyruq == 170 ? 아래 + 순번 : buyruq_ma_lumotlar.네바이트(), ko_chirish_joyi_VALUE = Holati + buyruq_ma_lumotlar.네바이트(); shox_Ro_yxat.add(ko_chirish_joyi_VALUE);
                    Collections.addAll(satr,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + ko_chirish_joyi_VALUE);
                }
                satr.add("jmp " + 표식 + "_b" + sukut_bo_yicha_qiymat);
            } else if (Buyruq == 172 || Buyruq == 176 || Buyruq == 177) {
                if (Buyruq != 177) satr.add("popl %eax"); Collections.addAll(satr,"leave","ret");
            } else if (Buyruq == 178 || Buyruq == 179) {
                uslub_Ma_lumotnomalar Ma_lumotnomalar = Sinf_VALUE.Ma_lumotnomalar(buyruq_ma_lumotlar.두바이트()); if (!필드들.containsKey(Ma_lumotnomalar)) throw new Tarjima_xato("알 수 없는 ma_lumotlar_maydoni_VALUE");
                Collections.addAll(satr,"call " + ramz("init",Ma_lumotnomalar.egasi_VALUE),(Buyruq == 178 ? "pushl " : "popl ") + ramz("field",Ma_lumotnomalar.부분들()));
            } else if (Buyruq == 184) {
                uslub_Ma_lumotnomalar Ma_lumotnomalar = Sinf_VALUE.Ma_lumotnomalar(buyruq_ma_lumotlar.두바이트()); if (!함수들.containsKey(Ma_lumotnomalar)) throw new Tarjima_xato("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Ma_lumotnomalar.서술); Collections.addAll(satr,"call " + ramz("init",Ma_lumotnomalar.egasi_VALUE),"call " + ramz("method",Ma_lumotnomalar.부분들()));
                if (!호출형식.인수.isEmpty()) satr.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.qaytarish_o_lchov.equals("V")) satr.add("pushl %eax");
            } else if (Buyruq == 182) {
                uslub_Ma_lumotnomalar Ma_lumotnomalar = Sinf_VALUE.Ma_lumotnomalar(buyruq_ma_lumotlar.두바이트());
                if (Ma_lumotnomalar.equals(new uslub_Ma_lumotnomalar("java/lang/String","length","()I"))) Collections.addAll(satr,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Ma_lumotnomalar.equals(new uslub_Ma_lumotnomalar("java/lang/String","charAt","(I)C"))) Collections.addAll(satr,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Tarjima_xato("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Buyruq == 188) {
                if (buyruq_ma_lumotlar.한바이트() != 10) throw new Tarjima_xato("new int[]만 madad_VALUE"); Collections.addAll(satr,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Buyruq == 190) Collections.addAll(satr,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Buyruq == 196) {
                int kengaytma_VALUE = buyruq_ma_lumotlar.한바이트(), INDEX = buyruq_ma_lumotlar.두바이트(); chek_mahalliy(INDEX,mahalliy_COUNT);
                if (kengaytma_VALUE == 21 || kengaytma_VALUE == 25 || kengaytma_VALUE == 54 || kengaytma_VALUE == 58) satr.add((kengaytma_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (kengaytma_VALUE == 132) satr.add("addl $" + buyruq_ma_lumotlar.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Tarjima_xato("wide Buyruq 미지원");
            } else if (Buyruq == 198 || Buyruq == 199) {
                int ko_chirish_joyi_VALUE = Holati + buyruq_ma_lumotlar.부호두바이트(); shox_Ro_yxat.add(ko_chirish_joyi_VALUE); Collections.addAll(satr,"popl %eax","testl %eax, %eax",(Buyruq == 198 ? "je " : "jne ") + 표식 + "_b" + ko_chirish_joyi_VALUE);
            } else throw new Tarjima_xato("미지원 Buyruq: " + Buyruq);
        }
        if (!경계들.containsAll(shox_Ro_yxat)) throw new Tarjima_xato("Buyruq 경계가 아닌 곳으로 shox");
        satr.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",satr);
    }
    String X_tugmasi_86_konstanta(Sinf_ma_lumotlar ma_lumotlar, int INDEX) {
        if (ma_lumotlar.상수종류[INDEX] == 3) return ma_lumotlar.konstanta_ma_lumotlar[INDEX].toString();
        if (ma_lumotlar.상수종류[INDEX] == 8) return satr_ramz(ma_lumotlar.문자((Integer)ma_lumotlar.konstanta_ma_lumotlar[INDEX]));
        throw new Tarjima_xato("정수와 satr_VALUE 상수만 madad_VALUE");
    }
    String 엑스조립본(String kiritish_nuqta, List<String> 내보냄, String nishon) throws IOException {
        Map<String,String> 기계표 = new HashMap<>();
        for (String satr : Files.readAllLines(resurs_yo_l.resolve("엑스기계함수.tsv"))) { String[] juftlab_ulamoq_VALUE = satr.split("\t"); if (juftlab_ulamoq_VALUE[0].equals(nishon)) 기계표.put(juftlab_ulamoq_VALUE[1] + juftlab_ulamoq_VALUE[2],juftlab_ulamoq_VALUE[3]); }
        int holat_INDEX = kiritish_nuqta.lastIndexOf('.'); if (holat_INDEX < 0) throw new Tarjima_xato("kiritish_nuqta tayinlash_VALUE Xato");
        String egasi_VALUE = kiritish_nuqta.substring(0,holat_INDEX).replace('.','/'), uslub_kiritish_nom = kiritish_nuqta.substring(holat_INDEX + 1); uslub_Ma_lumotnomalar kiritish_nuqta_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { uslub_Ma_lumotnomalar Ma_lumotnomalar = new uslub_Ma_lumotnomalar(egasi_VALUE,uslub_kiritish_nom,서술); if (함수들.containsKey(Ma_lumotnomalar)) { if (kiritish_nuqta_VALUE != null) throw new Tarjima_xato("겹친 kiritish_nuqta"); kiritish_nuqta_VALUE = Ma_lumotnomalar; } }
        if (kiritish_nuqta_VALUE == null || (함수들.get(kiritish_nuqta_VALUE).kirish_huquqi_kiritish & 0x100) != 0) throw new Tarjima_xato("kiritish_nuqta_VALUE FUNCTION_VALUE format_VALUE Xato");
        List<String> satr = new ArrayList<>(); satr.add(".code32");
        for (Sinf_ma_lumotlar ma_lumotlar : 클래스들.values()) {
            String holat_VALUE_e10195a1 = ramz("state",ma_lumotlar.Nomi), ishga_tushirmoq = ramz("init",ma_lumotlar.Nomi);
            Collections.addAll(satr,".bss",".balign 4",holat_VALUE_e10195a1 + ": .long 0",".text",ishga_tushirmoq + ":","cmpl $0, " + holat_VALUE_e10195a1,"jne " + ishga_tushirmoq + "_done","movl $1, " + holat_VALUE_e10195a1);
            uslub_Ma_lumotnomalar 초기화참조 = new uslub_Ma_lumotnomalar(ma_lumotlar.Nomi,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) satr.add("call " + ramz("method",초기화참조.부분들()));
            Collections.addAll(satr,"movl $2, " + holat_VALUE_e10195a1,ishga_tushirmoq + "_done:","ret");
            for (a_zo_ma_lumotlar ma_lumotlar_maydoni_VALUE : ma_lumotlar.ma_lumotlar_maydoni_VALUE) {
                byte[] konstanta_VALUE = ma_lumotlar_maydoni_VALUE.xususiyat_VALUE.get("ConstantValue"); String VALUE = konstanta_VALUE == null ? "0" : X_tugmasi_86_konstanta(ma_lumotlar,new ma_lumotlar_o_quvchi(konstanta_VALUE).두바이트());
                Collections.addAll(satr,".data",".balign 4",ramz("field",ma_lumotlar.Nomi,ma_lumotlar_maydoni_VALUE.Nomi,ma_lumotlar_maydoni_VALUE.서술) + ": .long " + VALUE);
            }
            for (a_zo_ma_lumotlar FUNCTION_VALUE : ma_lumotlar.FUNCTION_VALUE) if (!FUNCTION_VALUE.Nomi.equals("<init>")) satr.add(엑스함수본문(new uslub_Ma_lumotnomalar(ma_lumotlar.Nomi,FUNCTION_VALUE.Nomi,FUNCTION_VALUE.서술),FUNCTION_VALUE,기계표,nishon));
        }
        Collections.addAll(satr,".text",".globl java_entry","java_entry:","call " + ramz("init",kiritish_nuqta_VALUE.egasi_VALUE),"call " + ramz("method",kiritish_nuqta_VALUE.부분들()));
        if (kiritish_nuqta_VALUE.서술.equals("()V")) satr.add("xorl %eax, %eax"); satr.add("ret");
        for (String tayinlash_VALUE : 내보냄) {
            int ajratuvchi_VALUE = tayinlash_VALUE.indexOf('='); if (ajratuvchi_VALUE < 1) throw new Tarjima_xato("내보내기 tayinlash_VALUE Xato");
            String 외부 = tayinlash_VALUE.substring(0,ajratuvchi_VALUE), FUNCTION_VALUE = tayinlash_VALUE.substring(ajratuvchi_VALUE + 1); int boʻlish_o_lchov = FUNCTION_VALUE.lastIndexOf('.');
            if (boʻlish_o_lchov < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tarjima_xato("내보내기 ramz Xato");
            String Sinf_VALUE = FUNCTION_VALUE.substring(0,boʻlish_o_lchov).replace('.','/'), Nomi = FUNCTION_VALUE.substring(boʻlish_o_lchov + 1); uslub_Ma_lumotnomalar tanlanma_VALUE = null;
            for (uslub_Ma_lumotnomalar Ma_lumotnomalar : 함수들.keySet()) if (Ma_lumotnomalar.egasi_VALUE.equals(Sinf_VALUE) && Ma_lumotnomalar.Nomi.equals(Nomi)) { if (tanlanma_VALUE != null) throw new Tarjima_xato("겹친 내보내기 nishon"); tanlanma_VALUE = Ma_lumotnomalar; }
            if (tanlanma_VALUE == null) throw new Tarjima_xato("내보낼 함수가 없음");
            Collections.addAll(satr,".text",".globl " + 외부,외부 + ":","call " + ramz("init",tanlanma_VALUE.egasi_VALUE),"jmp " + ramz("method",tanlanma_VALUE.부분들()));
        }
        satr.add(".section .rodata");
        for (Map.Entry<String,String> kiritish_VALUE : 문자열들.entrySet()) {
            Collections.addAll(satr,".balign 4",kiritish_VALUE.getValue() + ":",".long " + kiritish_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char dars_VALUE : kiritish_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(dars_VALUE)); if (!단위들.isEmpty()) satr.add(".long " + String.join(",",단위들));
        }
        satr.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",satr) + "\n";
    }
    static void bajarmoq_vosita(List<String> Buyruq) throws Exception {
        if (new ProcessBuilder(Buyruq).inheritIO().start().waitFor() != 0) throw new Tarjima_xato("yig_moq_manba Xato: " + Buyruq.get(0));
    }
    static String ma_lumotlar_satr(String Matn) { return "\"" + Matn.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_tugmasi_86_Tarjima(List<Path> 입력들, String nishon, String kiritish_nuqta, List<String> 내보냄, Path 출력, Path resurs_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Sinf_yo_l = 임시.resolve("classes"); Files.createDirectory(Sinf_yo_l);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Sinf_yo_l.toString(),"-sourcepath",Sinf_yo_l.toString(),"-d",Sinf_yo_l.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int manba_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Tarjima_xato("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); manba_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Tarjima_xato(".java 또는 .class만 madad_VALUE");
            }
            if (manba_COUNT > 0) bajarmoq_vosita(자바명령);
            try (java.util.stream.Stream<Path> yo_l_Ro_yxat = Files.walk(Sinf_yo_l)) { yo_l_Ro_yxat.filter(yo_l -> yo_l.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,nishon.equals("user") ? "user" : "kernel",262144,resurs_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(kiritish_nuqta,내보냄,nishon); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path vosita_holat = resurs_VALUE.getParent();
            bajarmoq_vosita(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            bajarmoq_vosita(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),vosita_holat.resolve("umumiy_til_ish_jarayoni_madad.s").toString()));
            List<String> Ulanish = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (nishon.equals("kernel")) Ulanish.add("-r");
            else {
                bajarmoq_vosita(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),vosita_holat.resolve(nishon.equals("user") ? "Start_foydalanuvchi_ilova.s" : "리눅스시작.s").toString()));
                Collections.addAll(Ulanish,"-e","_start",임시.resolve("start.o").toString());
                if (nishon.equals("user")) Collections.addAll(Ulanish,"-T",vosita_holat.resolve("foydalanuvchi_ulash_Maket.ld").toString());
            }
            Collections.addAll(Ulanish,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); bajarmoq_vosita(Ulanish);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path joylash_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),joylash_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(joylash_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(joylash_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(nishon.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> ramz_ma_lumotlar = new ArrayList<>(), boshlang_ich_ma_lumotlar = new ArrayList<>();
            for (uslub_Ma_lumotnomalar Ma_lumotnomalar : CONVERT_VALUE.함수들.keySet()) ramz_ma_lumotlar.add(ma_lumotlar_satr(ramz("method",Ma_lumotnomalar.부분들())) + ":" + ma_lumotlar_satr(Ma_lumotnomalar.egasi_VALUE + "." + Ma_lumotnomalar.Nomi + Ma_lumotnomalar.서술));
            for (Path 입력 : 입력들) {
                byte[] tasodifiy_ma_lumot_fayl = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Matn = new StringBuilder(); for (byte VALUE : tasodifiy_ma_lumot_fayl) Matn.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                boshlang_ich_ma_lumotlar.add(ma_lumotlar_satr(입력.toAbsolutePath().toString()) + ":" + ma_lumotlar_satr(Matn.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + ma_lumotlar_satr(nishon) + ",\"entry\":" + ma_lumotlar_satr(kiritish_nuqta) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",ramz_ma_lumotlar) + "},\"sources\":{" + String.join(",",boshlang_ich_ma_lumotlar) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> yo_l_Ro_yxat = Files.walk(임시)) { for (Path yo_l : (Iterable<Path>)yo_l_Ro_yxat.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(yo_l); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String kiritish_nuqta = null, nishon = "kernel", X_tugmasi_86_maqsad = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> yo_l_Ro_yxat = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": X_tugmasi_86_maqsad = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Sinf_VALUE.FUNCTION_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export ramz=Sinf_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": kiritish_nuqta = 인수[++순번]; break;
                    case "--profile": nishon = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Tarjima_xato("알 수 없는 옵션: " + VALUE); yo_l_Ro_yxat.add(Paths.get(VALUE));
                }
            }
            if (kiritish_nuqta == null || 출력경로 == null || yo_l_Ro_yxat.isEmpty()) throw new Tarjima_xato("--entry, -o, Sinf_VALUE 파일이 필요합니다");
            Path resurs_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_tugmasi_86_maqsad != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_tugmasi_86_maqsad)) throw new Tarjima_xato("알 수 없는 bajarmoq_buyruq nishon");
                X_tugmasi_86_Tarjima(yo_l_Ro_yxat,X_tugmasi_86_maqsad,kiritish_nuqta,내보냄,출력경로,resurs_VALUE); return;
            }
            String manba = new 기계어미리번역(yo_l_Ro_yxat, nishon, 낱말수, resurs_VALUE).generatsiiyalash(kiritish_nuqta, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, manba, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Xato) { System.err.println("yig_moq_manba Xato: " + Xato.getMessage()); System.exit(1); }
    }
}
