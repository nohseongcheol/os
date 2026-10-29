// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java kategorya_VALUE_55654bf1 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Translation_error extends RuntimeException {
        Translation_error(String 설명) { super(설명); }
    }
    static final class data_Tagabasa {
        final byte[] data;
        int posisyon;
        data_Tagabasa(byte[] 입력자료) { data = 입력자료; }
        byte[] 읽기(int haba_VALUE) {
            if (haba_VALUE < 0 || haba_VALUE > data.length - posisyon) throw new Translation_error("잘린 kategorya_VALUE_55654bf1 또는 utos data");
            byte[] sukat = Arrays.copyOfRange(data, posisyon, posisyon + haba_VALUE); posisyon += haba_VALUE; return sukat;
        }
        int 한바이트() { if (posisyon >= data.length) throw new Translation_error("잘린 utos data"); return data[posisyon++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class miyembro_data {
        final int access_pagpasok;
        final String pangalan, 서술;
        final Map<String, byte[]> katangian_VALUE;
        miyembro_data(int access_VALUE, String pangalan_VALUE, String 서술값, Map<String, byte[]> katangian_data) {
            access_pagpasok = access_VALUE; pangalan = pangalan_VALUE; 서술 = 서술값; katangian_VALUE = katangian_data;
        }
    }
    static final class pamamaraan_Sanggunian implements Comparable<pamamaraan_Sanggunian> {
        final String may_ari_VALUE, pangalan, 서술;
        pamamaraan_Sanggunian(String 소유값, String pangalan_VALUE, String 서술값) { may_ari_VALUE = 소유값; pangalan = pangalan_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{may_ari_VALUE, pangalan, 서술}; }
        public int compareTo(pamamaraan_Sanggunian peer_VALUE) {
            int Paghahambing_VALUE = may_ari_VALUE.compareTo(peer_VALUE.may_ari_VALUE);
            if (Paghahambing_VALUE == 0) Paghahambing_VALUE = pangalan.compareTo(peer_VALUE.pangalan);
            return Paghahambing_VALUE == 0 ? 서술.compareTo(peer_VALUE.서술) : Paghahambing_VALUE;
        }
        public boolean equals(Object peer_VALUE) { return peer_VALUE instanceof pamamaraan_Sanggunian && compareTo((pamamaraan_Sanggunian) peer_VALUE) == 0; }
        public int hashCode() { return Objects.hash(may_ari_VALUE, pangalan, 서술); }
    }
    static final class kategorya_data {
        final int[] 상수종류;
        final Object[] constant_data;
        final String pangalan;
        final List<miyembro_data> field_VALUE, pormula_VALUE;
        kategorya_data(Path path) throws IOException {
            data_Tagabasa Tagabasa_VALUE = new data_Tagabasa(Files.readAllBytes(path));
            if (Tagabasa_VALUE.네바이트() != 0xcafebabe) throw new Translation_error("Java kategorya_VALUE_55654bf1 표식이 아님");
            Tagabasa_VALUE.읽기(4);
            int item_COUNT = Tagabasa_VALUE.두바이트(); 상수종류 = new int[item_COUNT]; constant_data = new Object[item_COUNT];
            for (int 순번 = 1; 순번 < item_COUNT; 순번++) {
                int 종류 = Tagabasa_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int haba_VALUE = Tagabasa_VALUE.두바이트();
                        byte[] karakter_buffer = Tagabasa_VALUE.읽기(haba_VALUE), 길이붙인자료 = new byte[haba_VALUE + 2];
                        길이붙인자료[0] = (byte)(haba_VALUE >> 8); 길이붙인자료[1] = (byte)haba_VALUE;
                        System.arraycopy(karakter_buffer, 0, 길이붙인자료, 2, haba_VALUE);
                        constant_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: constant_data[순번] = Tagabasa_VALUE.네바이트(); break;
                    case 4: Tagabasa_VALUE.읽기(4); break;
                    case 5: case 6: Tagabasa_VALUE.읽기(8); 순번++; break;
                    case 7: case 8: case 16: constant_data[순번] = Tagabasa_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        constant_data[순번] = new int[]{Tagabasa_VALUE.두바이트(), Tagabasa_VALUE.두바이트()}; break;
                    case 15: constant_data[순번] = new int[]{Tagabasa_VALUE.한바이트(), Tagabasa_VALUE.두바이트()}; break;
                    default: throw new Translation_error("지원하지 않는 constant_VALUE 종류: " + 종류);
                }
            }
            Tagabasa_VALUE.두바이트(); pangalan = kategorya_pangalan(Tagabasa_VALUE.두바이트());
            if (!kategorya_pangalan(Tagabasa_VALUE.두바이트()).equals("java/lang/Object") || Tagabasa_VALUE.두바이트() != 0)
                throw new Translation_error(pangalan + ": 상속 및 인터페이스 미지원");
            field_VALUE = 멤버읽기(Tagabasa_VALUE); pormula_VALUE = 멤버읽기(Tagabasa_VALUE); 속성읽기(Tagabasa_VALUE);
            if (Tagabasa_VALUE.posisyon != Tagabasa_VALUE.data.length) throw new Translation_error("kategorya_VALUE_55654bf1 뒤에 남은 data");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Translation_error("문자 constant_VALUE INDEX error");
            return (String) constant_data[INDEX];
        }
        String kategorya_pangalan(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Translation_error("kategorya_VALUE_55654bf1 Sanggunian error");
            return 문자((Integer)constant_data[INDEX]);
        }
        pamamaraan_Sanggunian Sanggunian(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Translation_error("멤버 Sanggunian error");
            int[] ipares_VALUE = (int[])constant_data[INDEX], pangalan_ipares = (int[])constant_data[ipares_VALUE[1]];
            return new pamamaraan_Sanggunian(kategorya_pangalan(ipares_VALUE[0]), 문자(pangalan_ipares[0]), 문자(pangalan_ipares[1]));
        }
        Map<String, byte[]> 속성읽기(data_Tagabasa Tagabasa_VALUE) {
            Map<String, byte[]> sukat = new LinkedHashMap<>();
            int item_COUNT = Tagabasa_VALUE.두바이트();
            for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                String katangian_pangalan = 문자(Tagabasa_VALUE.두바이트()); byte[] VALUE = Tagabasa_VALUE.읽기(Tagabasa_VALUE.네바이트());
                if (sukat.put(katangian_pangalan, VALUE) != null) throw new Translation_error("겹친 katangian_VALUE: " + katangian_pangalan);
            }
            return sukat;
        }
        List<miyembro_data> 멤버읽기(data_Tagabasa Tagabasa_VALUE) {
            List<miyembro_data> sukat = new ArrayList<>(); int item_COUNT = Tagabasa_VALUE.두바이트();
            for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                int access_pagpasok = Tagabasa_VALUE.두바이트(); String pamamaraan_pagpasok_pangalan = 문자(Tagabasa_VALUE.두바이트()), 서술 = 문자(Tagabasa_VALUE.두바이트());
                sukat.add(new miyembro_data(access_pagpasok, pamamaraan_pagpasok_pangalan, 서술, 속성읽기(Tagabasa_VALUE)));
            }
            return sukat;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Translation_error("pormula_VALUE 서술 error: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Translation_error("pormula_VALUE 서술 error: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Translation_error("pormula_VALUE 서술 error: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> sukat = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int posisyon = 0; posisyon < 서술.length();) {
            String seleksyon_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, posisyon)) { seleksyon_VALUE = format_VALUE; break; }
            if (seleksyon_VALUE == null) throw new Translation_error("지원하지 않는 uri_ng_data: " + 서술);
            sukat.add(seleksyon_VALUE); posisyon += seleksyon_VALUE.length();
        }
        return sukat;
    }
    static String simbolo(String 종류, String... 부분들) {
        try {
            byte[] hash_file = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", hash_file[순번] & 255));
            return SMS.toString();
        } catch (Exception error) { throw new Translation_error(error.toString()); }
    }
    final Map<String, kategorya_data> 클래스들 = new TreeMap<>();
    final Map<pamamaraan_Sanggunian, miyembro_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, machine_kategorya;
    final int 동적기억낱말수;
    final Path resource_path;
    기계어미리번역(List<Path> path_list, String layunin, int 낱말수, Path resource_VALUE) throws IOException {
        if ((!layunin.equals("kernel") && !layunin.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Translation_error("Mag_execute_utos layunin 또는 Memory_VALUE 공간 sukat_82232621 error");
        실행대상 = layunin; 동적기억낱말수 = 낱말수; resource_path = resource_VALUE;
        // 이 이름도 국가별 pinagmulan_balangkas mag_generate 시 해당 언어로 옮긴다.
        machine_kategorya = layunin.equals("kernel") ? "board" : "gumagamit";
        for (String linya : Files.readAllLines(resource_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = linya.split("\t", -1);
            if (부분들.length != 4) throw new Translation_error("machine pormula_VALUE data error");
            if (부분들[0].equals(layunin)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path path : path_list) {
            kategorya_data data = new kategorya_data(path);
            if (클래스들.put(data.pangalan, data) != null) throw new Translation_error("중복 kategorya_VALUE_55654bf1: " + data.pangalan);
            for (miyembro_data field_VALUE : data.field_VALUE) {
                if ((field_VALUE.access_pagpasok & 8) == 0 || 형식읽기(field_VALUE.서술).equals(Collections.singletonList("V"))) throw new Translation_error("hindi_nababago_VALUE 필드만 Suporta_VALUE");
                if (필드들.put(new pamamaraan_Sanggunian(data.pangalan, field_VALUE.pangalan, field_VALUE.서술), field_VALUE) != null) throw new Translation_error("중복 field_VALUE");
            }
            for (miyembro_data pormula_VALUE : data.pormula_VALUE) {
                if (pormula_VALUE.pangalan.equals("<init>")) continue;
                if ((pormula_VALUE.access_pagpasok & 8) == 0 || (pormula_VALUE.access_pagpasok & (0x20 | 0x400)) != 0) throw new Translation_error("hindi_nababago_VALUE 비동기화 함수만 Suporta_VALUE");
                new 함수형식(pormula_VALUE.서술);
                if (함수들.put(new pamamaraan_Sanggunian(data.pangalan, pormula_VALUE.pangalan, pormula_VALUE.서술), pormula_VALUE) != null) throw new Translation_error("중복 pormula_VALUE");
            }
        }
    }
    String string_simbolo(String SMS) { return 문자열들.computeIfAbsent(SMS, VALUE -> "j_text_" + 문자열들.size()); }
    String constant_expression(kategorya_data data, int INDEX) {
        if (INDEX < 1 || INDEX >= data.상수종류.length) throw new Translation_error("constant_VALUE INDEX clip error");
        if (data.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + data.constant_data[INDEX] + ")";
        if (data.상수종류[INDEX] == 8) return "(word)" + string_simbolo(data.문자((Integer)data.constant_data[INDEX]));
        throw new Translation_error("정수와 string_VALUE 상수만 Suporta_VALUE");
    }
    String 함수원형(pamamaraan_Sanggunian Sanggunian) {
        List<String> 인수들 = new ArrayList<>(); int item_COUNT = new 함수형식(Sanggunian.서술).인수.size();
        for (int 순번 = 0; 순번 < item_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbolo("method", Sanggunian.부분들()) + "(" + (item_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void tseke_lokal(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Translation_error("lokal_lawak 변수 INDEX clip error"); }
    void 분기넣기(List<String> 출력, Set<Integer> sanga_list, int posisyon, int 이동량, String kondisyon) {
        int patutunguhan_VALUE = posisyon + 이동량; sanga_list.add(patutunguhan_VALUE);
        출력.add((kondisyon == null ? "" : "if (" + kondisyon + ") ") + "goto b" + patutunguhan_VALUE + ";");
    }
    String pamamaraan_katawan(pamamaraan_Sanggunian pormula_VALUE, miyembro_data data) {
        byte[] katawan_data = data.katangian_VALUE.get("Code"); if (katawan_data == null) throw new Translation_error("pormula_VALUE 몸체가 없음: " + pormula_VALUE.pangalan);
        data_Tagabasa Tagabasa_VALUE = new data_Tagabasa(katawan_data); int 쌓임깊이 = Tagabasa_VALUE.두바이트(), 지역변수수 = Tagabasa_VALUE.두바이트();
        data_Tagabasa utos_data = new data_Tagabasa(Tagabasa_VALUE.읽기(Tagabasa_VALUE.네바이트()));
        if (Tagabasa_VALUE.두바이트() != 0) throw new Translation_error("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(pormula_VALUE.서술); if (지역변수수 < format_VALUE.인수.size()) throw new Translation_error("매개변수보다 적은 lokal_lawak 변수");
        kategorya_data kategorya_VALUE_55654bf1 = 클래스들.get(pormula_VALUE.may_ari_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(pormula_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), sanga_list = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (utos_data.posisyon < utos_data.data.length) {
            int posisyon = utos_data.posisyon, utos = utos_data.한바이트(); 경계들.add(posisyon); 출력.add("b" + posisyon + ":;");
            if (utos == 0) continue;
            if (utos == 1) 출력.add("PUSH(0);");
            else if (utos >= 2 && utos <= 8) 출력.add("PUSH((uint32_t)(" + (utos - 3) + "));");
            else if (utos == 16 || utos == 17) 출력.add("PUSH((uint32_t)(" + (utos == 16 ? utos_data.부호한바이트() : utos_data.부호두바이트()) + "));");
            else if (utos == 18 || utos == 19) 출력.add("PUSH(" + constant_expression(kategorya_VALUE_55654bf1, utos == 18 ? utos_data.한바이트() : utos_data.두바이트()) + ");");
            else if (utos == 21 || utos == 25 || (utos >= 26 && utos <= 29) || (utos >= 42 && utos <= 45)) {
                int INDEX = utos == 21 || utos == 25 ? utos_data.한바이트() : utos - (utos <= 29 ? 26 : 42);
                tseke_lokal(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (utos == 54 || utos == 58 || (utos >= 59 && utos <= 62) || (utos >= 75 && utos <= 78)) {
                int INDEX = utos == 54 || utos == 58 ? utos_data.한바이트() : utos - (utos <= 62 ? 59 : 75);
                tseke_lokal(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (utos == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (utos == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (utos == 87 || utos == 88) 출력.add(utos == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (utos >= 89 && utos <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] pagkakasunud_sunod_list = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[utos - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : pagkakasunud_sunod_list[utos - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (utos == 96 || utos == 100 || utos == 104 || utos == 126 || utos == 128 || utos == 130) {
                String operasyon_VALUE = utos == 96 ? "+" : utos == 100 ? "-" : utos == 104 ? "*" : utos == 126 ? "&" : utos == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operasyon_VALUE + " (uint32_t)b);");
            } else if (utos == 108 || utos == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (utos == 112 ? 1 : 0) + "));");
            else if (utos == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (utos == 120 || utos == 122 || utos == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (utos == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (utos == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (utos == 132) {
                int INDEX = utos_data.한바이트(), 증가량 = utos_data.부호한바이트(); tseke_lokal(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (utos >= 145 && utos <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (utos == 145 ? "int8_t" : utos == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (utos >= 153 && utos <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, sanga_list, posisyon, utos_data.부호두바이트(), "(int32_t)a " + 비교들[utos - 153] + " 0");
            } else if (utos >= 159 && utos <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, sanga_list, posisyon, utos_data.부호두바이트(), utos >= 165 ? "a " + 비교들[utos - 159] + " b" : "(int32_t)a " + 비교들[utos - 159] + " (int32_t)b");
            } else if (utos == 167 || utos == 200) 분기넣기(출력, sanga_list, posisyon, utos == 167 ? utos_data.부호두바이트() : utos_data.네바이트(), null);
            else if (utos == 170 || utos == 171) {
                while (utos_data.posisyon % 4 != 0) utos_data.한바이트();
                int value_ng_default = utos_data.네바이트(); 출력.add("a = POP();");
                if (utos == 170) {
                    int 아래 = utos_data.네바이트(), 위 = utos_data.네바이트(); long item_COUNT = (long)위 - 아래 + 1;
                    if (item_COUNT < 1 || item_COUNT > (utos_data.data.length - utos_data.posisyon) / 4) throw new Translation_error("switch clip error");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, sanga_list, posisyon, utos_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int item_COUNT = utos_data.네바이트(), nasa_harap_data = 0;
                    if (item_COUNT < 0 || item_COUNT > (utos_data.data.length - utos_data.posisyon) / 8) throw new Translation_error("switch sukat_82232621 error");
                    for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                        int VALUE = utos_data.네바이트(); if (순번 > 0 && VALUE <= nasa_harap_data) throw new Translation_error("switch pagkakasunud_sunod_VALUE error"); nasa_harap_data = VALUE;
                        분기넣기(출력, sanga_list, posisyon, utos_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, sanga_list, posisyon, value_ng_default, null);
            } else if (utos == 172 || utos == 176 || utos == 177) 출력.add("return " + (utos == 177 ? "0" : "POP()") + ";");
            else if (utos == 178 || utos == 179) {
                pamamaraan_Sanggunian Sanggunian = kategorya_VALUE_55654bf1.Sanggunian(utos_data.두바이트()); if (!필드들.containsKey(Sanggunian)) throw new Translation_error("알 수 없는 field_VALUE");
                출력.add(simbolo("init", Sanggunian.may_ari_VALUE) + "();"); String field_VALUE = simbolo("field", Sanggunian.부분들());
                출력.add(utos == 178 ? "PUSH(" + field_VALUE + ");" : field_VALUE + " = POP();");
            } else if (utos == 184) {
                pamamaraan_Sanggunian Sanggunian = kategorya_VALUE_55654bf1.Sanggunian(utos_data.두바이트()); if (!함수들.containsKey(Sanggunian)) throw new Translation_error("알 수 없는 pormula_VALUE");
                함수형식 호출형식 = new 함수형식(Sanggunian.서술); int item_COUNT = 호출형식.인수.size();
                출력.add(simbolo("init", Sanggunian.may_ari_VALUE) + "();"); 출력.add("if(sp < " + item_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + item_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < item_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + simbolo("method", Sanggunian.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (utos == 182) {
                pamamaraan_Sanggunian Sanggunian = kategorya_VALUE_55654bf1.Sanggunian(utos_data.두바이트());
                if (Sanggunian.equals(new pamamaraan_Sanggunian("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Sanggunian.equals(new pamamaraan_Sanggunian("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Translation_error("가상 pormula_VALUE 호출 미지원");
            } else if (utos == 188) {
                if (utos_data.한바이트() != 10) throw new Translation_error("new int[]만 Suporta_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (utos == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (utos == 196) {
                int extension_VALUE = utos_data.한바이트(), INDEX = utos_data.두바이트(); tseke_lokal(INDEX, 지역변수수);
                if (extension_VALUE == 21 || extension_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (extension_VALUE == 54 || extension_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (extension_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + utos_data.부호두바이트() + ");");
                else throw new Translation_error("미지원 wide utos");
            } else if (utos == 198 || utos == 199) {
                출력.add("a = POP();"); 분기넣기(출력, sanga_list, posisyon, utos_data.부호두바이트(), "a " + (utos == 198 ? "==" : "!=") + " 0");
            } else throw new Translation_error(pormula_VALUE.may_ari_VALUE + "." + pormula_VALUE.pangalan + ", byte_VALUE " + posisyon + ": 미지원 utos " + utos);
        }
        if (!경계들.containsAll(sanga_list)) throw new Translation_error("utos 경계가 아닌 곳으로 sanga");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String export_pamamaraan(String Link_simbolo, String layunin, boolean 진입점여부) {
        int posisyon_INDEX = layunin.lastIndexOf('.'); if (posisyon_INDEX < 0 || !Link_simbolo.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Translation_error("내보내기 italaga_VALUE error");
        String may_ari_VALUE = layunin.substring(0, posisyon_INDEX).replace('.', '/'), pangalan = layunin.substring(posisyon_INDEX + 1); pamamaraan_Sanggunian seleksyon_VALUE = null;
        for (pamamaraan_Sanggunian Sanggunian : 함수들.keySet()) if (Sanggunian.may_ari_VALUE.equals(may_ari_VALUE) && Sanggunian.pangalan.equals(pangalan)) {
            if (seleksyon_VALUE != null) throw new Translation_error("겹친 내보내기 layunin"); seleksyon_VALUE = Sanggunian;
        }
        if (seleksyon_VALUE == null || (함수들.get(seleksyon_VALUE).access_pagpasok & 0x100) != 0) throw new Translation_error("내보낼 함수가 없음 또는 native pormula_VALUE");
        함수형식 format_VALUE = new 함수형식(seleksyon_VALUE.서술);
        if ((진입점여부 && !format_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.반환)) throw new Translation_error("pagpasok_point_VALUE 또는 C 경계 format_VALUE error");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) {
            if (!format_VALUE.인수.get(순번).equals("I")) throw new Translation_error("C 경계는 int 인수만 Suporta_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.반환.equals("V") ? "void " : "int32_t ") + Link_simbolo + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbolo("init", seleksyon_VALUE.may_ari_VALUE) + "(); " + (format_VALUE.반환.equals("V") ? "" : "return (int32_t)") + simbolo("method", seleksyon_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String mag_generate(String pagpasok_point, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<pamamaraan_Sanggunian, miyembro_data> pagpasok_VALUE : 함수들.entrySet()) {
            pamamaraan_Sanggunian Sanggunian = pagpasok_VALUE.getKey(); miyembro_data data = pagpasok_VALUE.getValue(); 선언들.add(함수원형(Sanggunian) + ";");
            if ((data.access_pagpasok & 0x100) != 0) {
                String CONNECT = 기계함수들.get(Sanggunian.pangalan + Sanggunian.서술);
                if (!Sanggunian.may_ari_VALUE.equals(machine_kategorya) || CONNECT == null) throw new Translation_error("허용되지 않은 native pormula_VALUE: " + Sanggunian.pangalan);
                int item_COUNT = new 함수형식(Sanggunian.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < item_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + CONNECT + "(" + (item_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(item_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Sanggunian) + " { return " + CONNECT + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(pamamaraan_katawan(Sanggunian, data));
        }
        for (Map.Entry<pamamaraan_Sanggunian, miyembro_data> pagpasok_VALUE : 필드들.entrySet()) {
            pamamaraan_Sanggunian Sanggunian = pagpasok_VALUE.getKey(); byte[] constant_VALUE = pagpasok_VALUE.getValue().katangian_VALUE.get("ConstantValue");
            String VALUE = constant_VALUE == null ? "0" : constant_expression(클래스들.get(Sanggunian.may_ari_VALUE), new data_Tagabasa(constant_VALUE).두바이트());
            필드선언들.add("static word " + simbolo("field", Sanggunian.부분들()) + " = " + VALUE + ";");
        }
        for (String pangalan : 클래스들.keySet()) {
            String magsimula = simbolo("init", pangalan), katayuan_VALUE = simbolo("state", pangalan);
            선언들.add("static void " + magsimula + "(void);"); 필드선언들.add("static unsigned " + katayuan_VALUE + ";");
            pamamaraan_Sanggunian Sanggunian = new pamamaraan_Sanggunian(pangalan, "<clinit>", "()V");
            몸체들.add("static void " + magsimula + "(void) { if(" + katayuan_VALUE + ") return; " + katayuan_VALUE + " = 1; " + (함수들.containsKey(Sanggunian) ? simbolo("method", Sanggunian.부분들()) + "(); " : "") + katayuan_VALUE + " = 2; }");
        }
        몸체들.add(export_pamamaraan("java_entry", pagpasok_point, true)); Set<String> 공개이름 = new HashSet<>();
        for (String italaga_VALUE : 내보내기목록) {
            int posisyon_INDEX = italaga_VALUE.indexOf('='); if (posisyon_INDEX < 1) throw new Translation_error("내보내기 italaga_VALUE error");
            String pangalan = italaga_VALUE.substring(0, posisyon_INDEX); 공개이름.add(pangalan); 몸체들.add(export_pamamaraan(pangalan, italaga_VALUE.substring(posisyon_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> pagpasok_VALUE : 문자열들.entrySet()) {
            String SMS = pagpasok_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + pagpasok_VALUE.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) ARRAY_VALUE.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Suporta_VALUE = Files.readString(resource_path.resolve("common_language_runtime_Suporta.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Suporta_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String pinagmulan, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> pangalan_talahanayan = new HashMap<>();
        for (String linya : Files.readAllLines(resource_path.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] ipares_VALUE = linya.split("\t"); pangalan_talahanayan.put(ipares_VALUE[0], ipares_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(pinagmulan); StringBuffer sukat = new StringBuffer();
        while (찾개.find()) {
            String pangalan = 찾개.group(), 새이름 = pangalan;
            if (!pangalan.startsWith("//") && !pangalan.startsWith("/*") && !pangalan.startsWith("\"") && !pangalan.startsWith("'") && !공개이름.contains(pangalan)) {
                새이름 = pangalan_talahanayan.getOrDefault(pangalan, pangalan);
                if (pangalan.matches("a[0-9]+")) 새이름 = "인수" + pangalan.substring(1);
                if (pangalan.matches("b[0-9]+")) 새이름 = "sanga" + pangalan.substring(1);
                if (범용표기) {
                    StringBuilder notation_VALUE = new StringBuilder();
                    for (char karakter_VALUE : 새이름.toCharArray()) notation_VALUE.append(karakter_VALUE < 128 ? Character.toString(karakter_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)karakter_VALUE));
                    새이름 = notation_VALUE.toString();
                }
            }
            찾개.appendReplacement(sukat, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(sukat); return sukat.toString();
    }
    String X_button_86_pamamaraan_katawan(pamamaraan_Sanggunian pormula_VALUE, miyembro_data data, Map<String,String> machine_talahanayan, String layunin) {
        String 표식 = simbolo("method", pormula_VALUE.부분들());
        List<String> linya = new ArrayList<>();
        if ((data.access_pagpasok & 0x100) != 0) {
            String CONNECT = machine_talahanayan.get(pormula_VALUE.pangalan + pormula_VALUE.서술);
            if (!pormula_VALUE.may_ari_VALUE.equals(layunin.equals("kernel") ? "device_VALUE" : "gumagamit") || CONNECT == null) throw new Translation_error("허용되지 않은 native pormula_VALUE");
            return ".text\n" + 표식 + ":\njmp " + CONNECT;
        }
        byte[] teksto_ng_nilalaman = data.katangian_VALUE.get("Code"); if (teksto_ng_nilalaman == null) throw new Translation_error("pormula_VALUE 몸체가 없음");
        data_Tagabasa Tagabasa_VALUE = new data_Tagabasa(teksto_ng_nilalaman); Tagabasa_VALUE.두바이트(); int lokal_COUNT = Tagabasa_VALUE.두바이트();
        data_Tagabasa utos_data = new data_Tagabasa(Tagabasa_VALUE.읽기(Tagabasa_VALUE.네바이트()));
        if (Tagabasa_VALUE.두바이트() != 0) throw new Translation_error("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(pormula_VALUE.서술); if (lokal_COUNT < format_VALUE.인수.size()) throw new Translation_error("매개변수보다 적은 lokal_lawak 변수");
        Collections.addAll(linya,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) Collections.addAll(linya,"movl " + (8 + 4 * (format_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        kategorya_data kategorya_VALUE_55654bf1 = 클래스들.get(pormula_VALUE.may_ari_VALUE); Set<Integer> 경계들 = new HashSet<>(), sanga_list = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (utos_data.posisyon < utos_data.data.length) {
            int posisyon = utos_data.posisyon, utos = utos_data.한바이트(); String posisyon_INDEX = 표식 + "_b" + posisyon;
            linya.add(posisyon_INDEX + ":"); 경계들.add(posisyon);
            if (utos == 0) linya.add("nop");
            else if (utos == 1) linya.add("pushl $0");
            else if (utos >= 2 && utos <= 8) linya.add("pushl $" + (utos - 3));
            else if (utos == 16 || utos == 17) linya.add("pushl $" + (utos == 16 ? utos_data.부호한바이트() : utos_data.부호두바이트()));
            else if (utos == 18 || utos == 19) {
                int INDEX = utos == 18 ? utos_data.한바이트() : utos_data.두바이트();
                linya.add("pushl $" + X_button_86_constant(kategorya_VALUE_55654bf1,INDEX));
            } else if (utos == 21 || utos == 25 || (utos >= 26 && utos <= 29) || (utos >= 42 && utos <= 45) || utos == 54 || utos == 58 || (utos >= 59 && utos <= 62) || (utos >= 75 && utos <= 78)) {
                boolean 읽음 = utos < 54; int INDEX = utos == 21 || utos == 25 || utos == 54 || utos == 58 ? utos_data.한바이트() : utos - (utos <= 29 ? 26 : utos <= 45 ? 42 : utos <= 62 ? 59 : 75);
                tseke_lokal(INDEX,lokal_COUNT); linya.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (utos == 46) Collections.addAll(linya,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (utos == 79) Collections.addAll(linya,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (utos == 87 || utos == 88) linya.add("addl $" + (utos == 87 ? 4 : 8) + ", %esp");
            else if (utos >= 89 && utos <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] pagkakasunud_sunod_list = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[utos - 89]; 순번++) linya.add("popl " + 저장기들[순번]);
                for (int 순번 : pagkakasunud_sunod_list[utos - 89]) linya.add("pushl " + 저장기들[순번]);
            } else if (utos == 96 || utos == 100 || utos == 104 || utos == 126 || utos == 128 || utos == 130) {
                String operasyon_VALUE = utos == 96 ? "addl" : utos == 100 ? "subl" : utos == 104 ? "imull" : utos == 126 ? "andl" : utos == 128 ? "orl" : "xorl";
                Collections.addAll(linya,"popl %ecx","popl %eax",operasyon_VALUE + " %ecx, %eax","pushl %eax");
            } else if (utos == 108 || utos == 112) Collections.addAll(linya,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + posisyon_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + posisyon_INDEX + "_divide","xorl %edx, %edx","jmp " + posisyon_INDEX + "_done",posisyon_INDEX + "_divide:","cltd","idivl %ecx",posisyon_INDEX + "_done:","pushl " + (utos == 108 ? "%eax" : "%edx"));
            else if (utos == 116) linya.add("negl (%esp)");
            else if (utos == 120 || utos == 122 || utos == 124) Collections.addAll(linya,"popl %ecx","popl %eax",(utos == 120 ? "sall" : utos == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (utos == 132) {
                int INDEX = utos_data.한바이트(), 증가 = utos_data.부호한바이트(); tseke_lokal(INDEX,lokal_COUNT); linya.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (utos >= 145 && utos <= 147) Collections.addAll(linya,"popl %eax",utos == 145 ? "movsbl %al, %eax" : utos == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (utos >= 153 && utos <= 166) {
                if (utos <= 158) Collections.addAll(linya,"popl %eax","testl %eax, %eax");
                else Collections.addAll(linya,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int patutunguhan_VALUE = posisyon + utos_data.부호두바이트(); sanga_list.add(patutunguhan_VALUE); linya.add(비교들[utos - (utos <= 158 ? 153 : 159)] + " " + 표식 + "_b" + patutunguhan_VALUE);
            } else if (utos == 167 || utos == 200) {
                int patutunguhan_VALUE = posisyon + (utos == 167 ? utos_data.부호두바이트() : utos_data.네바이트()); sanga_list.add(patutunguhan_VALUE); linya.add("jmp " + 표식 + "_b" + patutunguhan_VALUE);
            } else if (utos == 170 || utos == 171) {
                while (utos_data.posisyon % 4 != 0) utos_data.한바이트();
                int value_ng_default = posisyon + utos_data.네바이트(); sanga_list.add(value_ng_default); linya.add("popl %eax");
                int item_COUNT, 아래 = 0;
                if (utos == 170) { 아래 = utos_data.네바이트(); int 위 = utos_data.네바이트(); long haba_VALUE = (long)위 - 아래 + 1; if (haba_VALUE < 1 || haba_VALUE > (utos_data.data.length - utos_data.posisyon) / 4) throw new Translation_error("switch clip error"); item_COUNT = (int)haba_VALUE; }
                else { item_COUNT = utos_data.네바이트(); if (item_COUNT < 0 || item_COUNT > (utos_data.data.length - utos_data.posisyon) / 8) throw new Translation_error("switch sukat_82232621 error"); }
                for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                    int VALUE = utos == 170 ? 아래 + 순번 : utos_data.네바이트(), patutunguhan_VALUE = posisyon + utos_data.네바이트(); sanga_list.add(patutunguhan_VALUE);
                    Collections.addAll(linya,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + patutunguhan_VALUE);
                }
                linya.add("jmp " + 표식 + "_b" + value_ng_default);
            } else if (utos == 172 || utos == 176 || utos == 177) {
                if (utos != 177) linya.add("popl %eax"); Collections.addAll(linya,"leave","ret");
            } else if (utos == 178 || utos == 179) {
                pamamaraan_Sanggunian Sanggunian = kategorya_VALUE_55654bf1.Sanggunian(utos_data.두바이트()); if (!필드들.containsKey(Sanggunian)) throw new Translation_error("알 수 없는 field_VALUE");
                Collections.addAll(linya,"call " + simbolo("init",Sanggunian.may_ari_VALUE),(utos == 178 ? "pushl " : "popl ") + simbolo("field",Sanggunian.부분들()));
            } else if (utos == 184) {
                pamamaraan_Sanggunian Sanggunian = kategorya_VALUE_55654bf1.Sanggunian(utos_data.두바이트()); if (!함수들.containsKey(Sanggunian)) throw new Translation_error("알 수 없는 pormula_VALUE");
                함수형식 호출형식 = new 함수형식(Sanggunian.서술); Collections.addAll(linya,"call " + simbolo("init",Sanggunian.may_ari_VALUE),"call " + simbolo("method",Sanggunian.부분들()));
                if (!호출형식.인수.isEmpty()) linya.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) linya.add("pushl %eax");
            } else if (utos == 182) {
                pamamaraan_Sanggunian Sanggunian = kategorya_VALUE_55654bf1.Sanggunian(utos_data.두바이트());
                if (Sanggunian.equals(new pamamaraan_Sanggunian("java/lang/String","length","()I"))) Collections.addAll(linya,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Sanggunian.equals(new pamamaraan_Sanggunian("java/lang/String","charAt","(I)C"))) Collections.addAll(linya,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Translation_error("가상 pormula_VALUE 호출 미지원");
            } else if (utos == 188) {
                if (utos_data.한바이트() != 10) throw new Translation_error("new int[]만 Suporta_VALUE"); Collections.addAll(linya,"popl %eax","call rt_new_array","pushl %eax");
            } else if (utos == 190) Collections.addAll(linya,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (utos == 196) {
                int extension_VALUE = utos_data.한바이트(), INDEX = utos_data.두바이트(); tseke_lokal(INDEX,lokal_COUNT);
                if (extension_VALUE == 21 || extension_VALUE == 25 || extension_VALUE == 54 || extension_VALUE == 58) linya.add((extension_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (extension_VALUE == 132) linya.add("addl $" + utos_data.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Translation_error("wide utos 미지원");
            } else if (utos == 198 || utos == 199) {
                int patutunguhan_VALUE = posisyon + utos_data.부호두바이트(); sanga_list.add(patutunguhan_VALUE); Collections.addAll(linya,"popl %eax","testl %eax, %eax",(utos == 198 ? "je " : "jne ") + 표식 + "_b" + patutunguhan_VALUE);
            } else throw new Translation_error("미지원 utos: " + utos);
        }
        if (!경계들.containsAll(sanga_list)) throw new Translation_error("utos 경계가 아닌 곳으로 sanga");
        linya.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",linya);
    }
    String X_button_86_constant(kategorya_data data, int INDEX) {
        if (data.상수종류[INDEX] == 3) return data.constant_data[INDEX].toString();
        if (data.상수종류[INDEX] == 8) return string_simbolo(data.문자((Integer)data.constant_data[INDEX]));
        throw new Translation_error("정수와 string_VALUE 상수만 Suporta_VALUE");
    }
    String 엑스조립본(String pagpasok_point, List<String> 내보냄, String layunin) throws IOException {
        Map<String,String> machine_talahanayan = new HashMap<>();
        for (String linya : Files.readAllLines(resource_path.resolve("엑스기계함수.tsv"))) { String[] ipares_VALUE = linya.split("\t"); if (ipares_VALUE[0].equals(layunin)) machine_talahanayan.put(ipares_VALUE[1] + ipares_VALUE[2],ipares_VALUE[3]); }
        int posisyon_INDEX = pagpasok_point.lastIndexOf('.'); if (posisyon_INDEX < 0) throw new Translation_error("pagpasok_point italaga_VALUE error");
        String may_ari_VALUE = pagpasok_point.substring(0,posisyon_INDEX).replace('.','/'), pamamaraan_pagpasok_pangalan = pagpasok_point.substring(posisyon_INDEX + 1); pamamaraan_Sanggunian pagpasok_point_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { pamamaraan_Sanggunian Sanggunian = new pamamaraan_Sanggunian(may_ari_VALUE,pamamaraan_pagpasok_pangalan,서술); if (함수들.containsKey(Sanggunian)) { if (pagpasok_point_VALUE != null) throw new Translation_error("겹친 pagpasok_point"); pagpasok_point_VALUE = Sanggunian; } }
        if (pagpasok_point_VALUE == null || (함수들.get(pagpasok_point_VALUE).access_pagpasok & 0x100) != 0) throw new Translation_error("pagpasok_point_VALUE pormula_VALUE format_VALUE error");
        List<String> linya = new ArrayList<>(); linya.add(".code32");
        for (kategorya_data data : 클래스들.values()) {
            String katayuan_VALUE = simbolo("state",data.pangalan), magsimula = simbolo("init",data.pangalan);
            Collections.addAll(linya,".bss",".balign 4",katayuan_VALUE + ": .long 0",".text",magsimula + ":","cmpl $0, " + katayuan_VALUE,"jne " + magsimula + "_done","movl $1, " + katayuan_VALUE);
            pamamaraan_Sanggunian 초기화참조 = new pamamaraan_Sanggunian(data.pangalan,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) linya.add("call " + simbolo("method",초기화참조.부분들()));
            Collections.addAll(linya,"movl $2, " + katayuan_VALUE,magsimula + "_done:","ret");
            for (miyembro_data field_VALUE : data.field_VALUE) {
                byte[] constant_VALUE = field_VALUE.katangian_VALUE.get("ConstantValue"); String VALUE = constant_VALUE == null ? "0" : X_button_86_constant(data,new data_Tagabasa(constant_VALUE).두바이트());
                Collections.addAll(linya,".data",".balign 4",simbolo("field",data.pangalan,field_VALUE.pangalan,field_VALUE.서술) + ": .long " + VALUE);
            }
            for (miyembro_data pormula_VALUE : data.pormula_VALUE) if (!pormula_VALUE.pangalan.equals("<init>")) linya.add(X_button_86_pamamaraan_katawan(new pamamaraan_Sanggunian(data.pangalan,pormula_VALUE.pangalan,pormula_VALUE.서술),pormula_VALUE,machine_talahanayan,layunin));
        }
        Collections.addAll(linya,".text",".globl java_entry","java_entry:","call " + simbolo("init",pagpasok_point_VALUE.may_ari_VALUE),"call " + simbolo("method",pagpasok_point_VALUE.부분들()));
        if (pagpasok_point_VALUE.서술.equals("()V")) linya.add("xorl %eax, %eax"); linya.add("ret");
        for (String italaga_VALUE : 내보냄) {
            int panghiwalay_VALUE = italaga_VALUE.indexOf('='); if (panghiwalay_VALUE < 1) throw new Translation_error("내보내기 italaga_VALUE error");
            String 외부 = italaga_VALUE.substring(0,panghiwalay_VALUE), pormula_VALUE = italaga_VALUE.substring(panghiwalay_VALUE + 1); int division_sukat = pormula_VALUE.lastIndexOf('.');
            if (division_sukat < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Translation_error("내보내기 simbolo error");
            String kategorya_VALUE_55654bf1 = pormula_VALUE.substring(0,division_sukat).replace('.','/'), pangalan = pormula_VALUE.substring(division_sukat + 1); pamamaraan_Sanggunian seleksyon_VALUE = null;
            for (pamamaraan_Sanggunian Sanggunian : 함수들.keySet()) if (Sanggunian.may_ari_VALUE.equals(kategorya_VALUE_55654bf1) && Sanggunian.pangalan.equals(pangalan)) { if (seleksyon_VALUE != null) throw new Translation_error("겹친 내보내기 layunin"); seleksyon_VALUE = Sanggunian; }
            if (seleksyon_VALUE == null) throw new Translation_error("내보낼 함수가 없음");
            Collections.addAll(linya,".text",".globl " + 외부,외부 + ":","call " + simbolo("init",seleksyon_VALUE.may_ari_VALUE),"jmp " + simbolo("method",seleksyon_VALUE.부분들()));
        }
        linya.add(".section .rodata");
        for (Map.Entry<String,String> pagpasok_VALUE : 문자열들.entrySet()) {
            Collections.addAll(linya,".balign 4",pagpasok_VALUE.getValue() + ":",".long " + pagpasok_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char aralin_VALUE : pagpasok_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(aralin_VALUE)); if (!단위들.isEmpty()) linya.add(".long " + String.join(",",단위들));
        }
        linya.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",linya) + "\n";
    }
    static void Mag_execute_tool(List<String> utos) throws Exception {
        if (new ProcessBuilder(utos).inheritIO().start().waitFor() != 0) throw new Translation_error("bumuo_pinagmulan error: " + utos.get(0));
    }
    static String data_string(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_button_86_Translation(List<Path> 입력들, String layunin, String pagpasok_point, List<String> 내보냄, Path 출력, Path resource_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), kategorya_path = 임시.resolve("classes"); Files.createDirectory(kategorya_path);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",kategorya_path.toString(),"-sourcepath",kategorya_path.toString(),"-d",kategorya_path.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int pinagmulan_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Translation_error("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); pinagmulan_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Translation_error(".java 또는 .class만 Suporta_VALUE");
            }
            if (pinagmulan_COUNT > 0) Mag_execute_tool(자바명령);
            try (java.util.stream.Stream<Path> path_list = Files.walk(kategorya_path)) { path_list.filter(path -> path.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,layunin.equals("user") ? "user" : "kernel",262144,resource_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(pagpasok_point,내보냄,layunin); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path tool_posisyon = resource_VALUE.getParent();
            Mag_execute_tool(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Mag_execute_tool(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),tool_posisyon.resolve("common_language_runtime_Suporta.s").toString()));
            List<String> CONNECT = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (layunin.equals("kernel")) CONNECT.add("-r");
            else {
                Mag_execute_tool(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),tool_posisyon.resolve(layunin.equals("user") ? "Start_gumagamit_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(CONNECT,"-e","_start",임시.resolve("start.o").toString());
                if (layunin.equals("user")) Collections.addAll(CONNECT,"-T",tool_posisyon.resolve("gumagamit_Link_Layout.ld").toString());
            }
            Collections.addAll(CONNECT,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Mag_execute_tool(CONNECT);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path ilathala_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),ilathala_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(ilathala_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(ilathala_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(layunin.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbolo_data = new ArrayList<>(), pinagmulan_ng_data = new ArrayList<>();
            for (pamamaraan_Sanggunian Sanggunian : CONVERT_VALUE.함수들.keySet()) simbolo_data.add(data_string(simbolo("method",Sanggunian.부분들())) + ":" + data_string(Sanggunian.may_ari_VALUE + "." + Sanggunian.pangalan + Sanggunian.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_file = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte VALUE : hash_file) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                pinagmulan_ng_data.add(data_string(입력.toAbsolutePath().toString()) + ":" + data_string(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + data_string(layunin) + ",\"entry\":" + data_string(pagpasok_point) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbolo_data) + "},\"sources\":{" + String.join(",",pinagmulan_ng_data) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> path_list = Files.walk(임시)) { for (Path path : (Iterable<Path>)path_list.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(path); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String pagpasok_point = null, layunin = "kernel", X_button_86_target = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> path_list = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": X_button_86_target = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry kategorya_VALUE_55654bf1.pormula_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export simbolo=kategorya_VALUE_55654bf1.pormula_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": pagpasok_point = 인수[++순번]; break;
                    case "--profile": layunin = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Translation_error("알 수 없는 옵션: " + VALUE); path_list.add(Paths.get(VALUE));
                }
            }
            if (pagpasok_point == null || 출력경로 == null || path_list.isEmpty()) throw new Translation_error("--entry, -o, kategorya_VALUE_55654bf1 파일이 필요합니다");
            Path resource_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_button_86_target != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_button_86_target)) throw new Translation_error("알 수 없는 Mag_execute_utos layunin");
                X_button_86_Translation(path_list,X_button_86_target,pagpasok_point,내보냄,출력경로,resource_VALUE); return;
            }
            String pinagmulan = new 기계어미리번역(path_list, layunin, 낱말수, resource_VALUE).mag_generate(pagpasok_point, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, pinagmulan, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception error) { System.err.println("bumuo_pinagmulan error: " + error.getMessage()); System.exit(1); }
    }
}
