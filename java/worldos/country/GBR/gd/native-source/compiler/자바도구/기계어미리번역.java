// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java clas_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. òstair JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class eadar_theangachadh_mearachd extends RuntimeException {
        eadar_theangachadh_mearachd(String 설명) { super(설명); }
    }
    static final class dàta_Leughadair {
        final byte[] dàta;
        int suidhich;
        dàta_Leughadair(byte[] 입력자료) { dàta = 입력자료; }
        byte[] 읽기(int faid_VALUE) {
            if (faid_VALUE < 0 || faid_VALUE > dàta.length - suidhich) throw new eadar_theangachadh_mearachd("잘린 clas_VALUE 또는 àithne dàta");
            byte[] tomhas = Arrays.copyOfRange(dàta, suidhich, suidhich + faid_VALUE); suidhich += faid_VALUE; return tomhas;
        }
        int 한바이트() { if (suidhich >= dàta.length) throw new eadar_theangachadh_mearachd("잘린 àithne dàta"); return dàta[suidhich++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class ball_dàta {
        final int inntrigeadh_cur_a_steach;
        final String Ainm, 서술;
        final Map<String, byte[]> buadh_VALUE;
        ball_dàta(int inntrigeadh_VALUE, String ainm_VALUE, String 서술값, Map<String, byte[]> buadh_dàta) {
            inntrigeadh_cur_a_steach = inntrigeadh_VALUE; Ainm = ainm_VALUE; 서술 = 서술값; buadh_VALUE = buadh_dàta;
        }
    }
    static final class dòigh_fiosrachadh implements Comparable<dòigh_fiosrachadh> {
        final String sealbhadair_VALUE, Ainm, 서술;
        dòigh_fiosrachadh(String 소유값, String ainm_VALUE, String 서술값) { sealbhadair_VALUE = 소유값; Ainm = ainm_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{sealbhadair_VALUE, Ainm, 서술}; }
        public int compareTo(dòigh_fiosrachadh seise_VALUE) {
            int 비교값 = sealbhadair_VALUE.compareTo(seise_VALUE.sealbhadair_VALUE);
            if (비교값 == 0) 비교값 = Ainm.compareTo(seise_VALUE.Ainm);
            return 비교값 == 0 ? 서술.compareTo(seise_VALUE.서술) : 비교값;
        }
        public boolean equals(Object seise_VALUE) { return seise_VALUE instanceof dòigh_fiosrachadh && compareTo((dòigh_fiosrachadh) seise_VALUE) == 0; }
        public int hashCode() { return Objects.hash(sealbhadair_VALUE, Ainm, 서술); }
    }
    static final class clas_dàta {
        final int[] 상수종류;
        final Object[] cunbhalachan_dàta;
        final String Ainm;
        final List<ball_dàta> raon_VALUE, FUNCTION_VALUE;
        clas_dàta(Path Slighe) throws IOException {
            dàta_Leughadair Leughadair_VALUE = new dàta_Leughadair(Files.readAllBytes(Slighe));
            if (Leughadair_VALUE.네바이트() != 0xcafebabe) throw new eadar_theangachadh_mearachd("Java clas_VALUE 표식이 아님");
            Leughadair_VALUE.읽기(4);
            int nì_COUNT = Leughadair_VALUE.두바이트(); 상수종류 = new int[nì_COUNT]; cunbhalachan_dàta = new Object[nì_COUNT];
            for (int 순번 = 1; 순번 < nì_COUNT; 순번++) {
                int 종류 = Leughadair_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int faid_VALUE = Leughadair_VALUE.두바이트();
                        byte[] caractar_bufair = Leughadair_VALUE.읽기(faid_VALUE), 길이붙인자료 = new byte[faid_VALUE + 2];
                        길이붙인자료[0] = (byte)(faid_VALUE >> 8); 길이붙인자료[1] = (byte)faid_VALUE;
                        System.arraycopy(caractar_bufair, 0, 길이붙인자료, 2, faid_VALUE);
                        cunbhalachan_dàta[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: cunbhalachan_dàta[순번] = Leughadair_VALUE.네바이트(); break;
                    case 4: Leughadair_VALUE.읽기(4); break;
                    case 5: case 6: Leughadair_VALUE.읽기(8); 순번++; break;
                    case 7: case 8: case 16: cunbhalachan_dàta[순번] = Leughadair_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        cunbhalachan_dàta[순번] = new int[]{Leughadair_VALUE.두바이트(), Leughadair_VALUE.두바이트()}; break;
                    case 15: cunbhalachan_dàta[순번] = new int[]{Leughadair_VALUE.한바이트(), Leughadair_VALUE.두바이트()}; break;
                    default: throw new eadar_theangachadh_mearachd("지원하지 않는 cunbhalachan_VALUE 종류: " + 종류);
                }
            }
            Leughadair_VALUE.두바이트(); Ainm = clas_ainm(Leughadair_VALUE.두바이트());
            if (!clas_ainm(Leughadair_VALUE.두바이트()).equals("java/lang/Object") || Leughadair_VALUE.두바이트() != 0)
                throw new eadar_theangachadh_mearachd(Ainm + ": 상속 및 인터페이스 미지원");
            raon_VALUE = 멤버읽기(Leughadair_VALUE); FUNCTION_VALUE = 멤버읽기(Leughadair_VALUE); 속성읽기(Leughadair_VALUE);
            if (Leughadair_VALUE.suidhich != Leughadair_VALUE.dàta.length) throw new eadar_theangachadh_mearachd("clas_VALUE 뒤에 남은 dàta");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new eadar_theangachadh_mearachd("문자 cunbhalachan_VALUE INDEX Mearachd");
            return (String) cunbhalachan_dàta[INDEX];
        }
        String clas_ainm(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new eadar_theangachadh_mearachd("clas_VALUE fiosrachadh Mearachd");
            return 문자((Integer)cunbhalachan_dàta[INDEX]);
        }
        dòigh_fiosrachadh fiosrachadh(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new eadar_theangachadh_mearachd("멤버 fiosrachadh Mearachd");
            int[] paidhrich_VALUE = (int[])cunbhalachan_dàta[INDEX], ainm_paidhrich = (int[])cunbhalachan_dàta[paidhrich_VALUE[1]];
            return new dòigh_fiosrachadh(clas_ainm(paidhrich_VALUE[0]), 문자(ainm_paidhrich[0]), 문자(ainm_paidhrich[1]));
        }
        Map<String, byte[]> 속성읽기(dàta_Leughadair Leughadair_VALUE) {
            Map<String, byte[]> tomhas = new LinkedHashMap<>();
            int nì_COUNT = Leughadair_VALUE.두바이트();
            for (int 순번 = 0; 순번 < nì_COUNT; 순번++) {
                String buadh_ainm = 문자(Leughadair_VALUE.두바이트()); byte[] VALUE = Leughadair_VALUE.읽기(Leughadair_VALUE.네바이트());
                if (tomhas.put(buadh_ainm, VALUE) != null) throw new eadar_theangachadh_mearachd("겹친 buadh_VALUE: " + buadh_ainm);
            }
            return tomhas;
        }
        List<ball_dàta> 멤버읽기(dàta_Leughadair Leughadair_VALUE) {
            List<ball_dàta> tomhas = new ArrayList<>(); int nì_COUNT = Leughadair_VALUE.두바이트();
            for (int 순번 = 0; 순번 < nì_COUNT; 순번++) {
                int inntrigeadh_cur_a_steach = Leughadair_VALUE.두바이트(); String dòigh_cur_a_steach_ainm = 문자(Leughadair_VALUE.두바이트()), 서술 = 문자(Leughadair_VALUE.두바이트());
                tomhas.add(new ball_dàta(inntrigeadh_cur_a_steach, dòigh_cur_a_steach_ainm, 서술, 속성읽기(Leughadair_VALUE)));
            }
            return tomhas;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String return_tomhas;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new eadar_theangachadh_mearachd("FUNCTION_VALUE 서술 Mearachd: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new eadar_theangachadh_mearachd("FUNCTION_VALUE 서술 Mearachd: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new eadar_theangachadh_mearachd("FUNCTION_VALUE 서술 Mearachd: " + 서술);
            return_tomhas = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> tomhas = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int suidhich = 0; suidhich < 서술.length();) {
            String taghadh_VALUE = null;
            for (String fòrmat_VALUE : 허용형식) if (서술.startsWith(fòrmat_VALUE, suidhich)) { taghadh_VALUE = fòrmat_VALUE; break; }
            if (taghadh_VALUE == null) throw new eadar_theangachadh_mearachd("지원하지 않는 seòrsa_an_dàta: " + 서술);
            tomhas.add(taghadh_VALUE); suidhich += taghadh_VALUE.length();
        }
        return tomhas;
    }
    static String samhla(String 종류, String... 부분들) {
        try {
            byte[] hais_faidhle = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", hais_faidhle[순번] & 255));
            return SMS.toString();
        } catch (Exception Mearachd) { throw new eadar_theangachadh_mearachd(Mearachd.toString()); }
    }
    final Map<String, clas_dàta> 클래스들 = new TreeMap<>();
    final Map<dòigh_fiosrachadh, ball_dàta> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, inneal_clas;
    final int 동적기억낱말수;
    final Path goireas_slighe;
    기계어미리번역(List<Path> slighe_Liosta, String targaid, int 낱말수, Path goireas_VALUE) throws IOException {
        if ((!targaid.equals("kernel") && !targaid.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new eadar_theangachadh_mearachd("gnìomhaich_àithne targaid 또는 cuimhne_VALUE 공간 atharraich_am_meud Mearachd");
        실행대상 = targaid; 동적기억낱말수 = 낱말수; goireas_slighe = goireas_VALUE;
        // 이 이름도 국가별 tùs_craobh gin 시 해당 언어로 옮긴다.
        inneal_clas = targaid.equals("kernel") ? "bòrd" : "cleachdaiche";
        for (String loidhne : Files.readAllLines(goireas_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = loidhne.split("\t", -1);
            if (부분들.length != 4) throw new eadar_theangachadh_mearachd("inneal FUNCTION_VALUE dàta Mearachd");
            if (부분들[0].equals(targaid)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Slighe : slighe_Liosta) {
            clas_dàta dàta = new clas_dàta(Slighe);
            if (클래스들.put(dàta.Ainm, dàta) != null) throw new eadar_theangachadh_mearachd("중복 clas_VALUE: " + dàta.Ainm);
            for (ball_dàta raon_VALUE : dàta.raon_VALUE) {
                if ((raon_VALUE.inntrigeadh_cur_a_steach & 8) == 0 || 형식읽기(raon_VALUE.서술).equals(Collections.singletonList("V"))) throw new eadar_theangachadh_mearachd("stadaigeach_VALUE 필드만 taic_VALUE");
                if (필드들.put(new dòigh_fiosrachadh(dàta.Ainm, raon_VALUE.Ainm, raon_VALUE.서술), raon_VALUE) != null) throw new eadar_theangachadh_mearachd("중복 raon_VALUE");
            }
            for (ball_dàta FUNCTION_VALUE : dàta.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Ainm.equals("<init>")) continue;
                if ((FUNCTION_VALUE.inntrigeadh_cur_a_steach & 8) == 0 || (FUNCTION_VALUE.inntrigeadh_cur_a_steach & (0x20 | 0x400)) != 0) throw new eadar_theangachadh_mearachd("stadaigeach_VALUE 비동기화 함수만 taic_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new dòigh_fiosrachadh(dàta.Ainm, FUNCTION_VALUE.Ainm, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new eadar_theangachadh_mearachd("중복 FUNCTION_VALUE");
            }
        }
    }
    String sreang_samhla(String SMS) { return 문자열들.computeIfAbsent(SMS, VALUE -> "j_text_" + 문자열들.size()); }
    String cunbhalachan_eas_preisean(clas_dàta dàta, int INDEX) {
        if (INDEX < 1 || INDEX >= dàta.상수종류.length) throw new eadar_theangachadh_mearachd("cunbhalachan_VALUE INDEX cliop Mearachd");
        if (dàta.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + dàta.cunbhalachan_dàta[INDEX] + ")";
        if (dàta.상수종류[INDEX] == 8) return "(word)" + sreang_samhla(dàta.문자((Integer)dàta.cunbhalachan_dàta[INDEX]));
        throw new eadar_theangachadh_mearachd("정수와 sreang_VALUE 상수만 taic_VALUE");
    }
    String 함수원형(dòigh_fiosrachadh fiosrachadh) {
        List<String> 인수들 = new ArrayList<>(); int nì_COUNT = new 함수형식(fiosrachadh.서술).인수.size();
        for (int 순번 = 0; 순번 < nì_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + samhla("method", fiosrachadh.부분들()) + "(" + (nì_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void seic_ionadail(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new eadar_theangachadh_mearachd("ionadail_sgòp 변수 INDEX cliop Mearachd"); }
    void 분기넣기(List<String> 출력, Set<Integer> meur_Liosta, int suidhich, int 이동량, String cumha) {
        int ceann_uidhe_VALUE = suidhich + 이동량; meur_Liosta.add(ceann_uidhe_VALUE);
        출력.add((cumha == null ? "" : "if (" + cumha + ") ") + "goto b" + ceann_uidhe_VALUE + ";");
    }
    String 함수본문(dòigh_fiosrachadh FUNCTION_VALUE, ball_dàta dàta) {
        byte[] 본문자료 = dàta.buadh_VALUE.get("Code"); if (본문자료 == null) throw new eadar_theangachadh_mearachd("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Ainm);
        dàta_Leughadair Leughadair_VALUE = new dàta_Leughadair(본문자료); int 쌓임깊이 = Leughadair_VALUE.두바이트(), 지역변수수 = Leughadair_VALUE.두바이트();
        dàta_Leughadair àithne_dàta = new dàta_Leughadair(Leughadair_VALUE.읽기(Leughadair_VALUE.네바이트()));
        if (Leughadair_VALUE.두바이트() != 0) throw new eadar_theangachadh_mearachd("try/catch/finally 미지원");
        함수형식 fòrmat_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (지역변수수 < fòrmat_VALUE.인수.size()) throw new eadar_theangachadh_mearachd("매개변수보다 적은 ionadail_sgòp 변수");
        clas_dàta clas_VALUE = 클래스들.get(FUNCTION_VALUE.sealbhadair_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(FUNCTION_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < fòrmat_VALUE.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), meur_Liosta = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (àithne_dàta.suidhich < àithne_dàta.dàta.length) {
            int suidhich = àithne_dàta.suidhich, àithne = àithne_dàta.한바이트(); 경계들.add(suidhich); 출력.add("b" + suidhich + ":;");
            if (àithne == 0) continue;
            if (àithne == 1) 출력.add("PUSH(0);");
            else if (àithne >= 2 && àithne <= 8) 출력.add("PUSH((uint32_t)(" + (àithne - 3) + "));");
            else if (àithne == 16 || àithne == 17) 출력.add("PUSH((uint32_t)(" + (àithne == 16 ? àithne_dàta.부호한바이트() : àithne_dàta.부호두바이트()) + "));");
            else if (àithne == 18 || àithne == 19) 출력.add("PUSH(" + cunbhalachan_eas_preisean(clas_VALUE, àithne == 18 ? àithne_dàta.한바이트() : àithne_dàta.두바이트()) + ");");
            else if (àithne == 21 || àithne == 25 || (àithne >= 26 && àithne <= 29) || (àithne >= 42 && àithne <= 45)) {
                int INDEX = àithne == 21 || àithne == 25 ? àithne_dàta.한바이트() : àithne - (àithne <= 29 ? 26 : 42);
                seic_ionadail(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (àithne == 54 || àithne == 58 || (àithne >= 59 && àithne <= 62) || (àithne >= 75 && àithne <= 78)) {
                int INDEX = àithne == 54 || àithne == 58 ? àithne_dàta.한바이트() : àithne - (àithne <= 62 ? 59 : 75);
                seic_ionadail(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (àithne == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (àithne == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (àithne == 87 || àithne == 88) 출력.add(àithne == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (àithne >= 89 && àithne <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] òrdugh_Liosta = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[àithne - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : òrdugh_Liosta[àithne - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (àithne == 96 || àithne == 100 || àithne == 104 || àithne == 126 || àithne == 128 || àithne == 130) {
                String obrachadh_VALUE = àithne == 96 ? "+" : àithne == 100 ? "-" : àithne == 104 ? "*" : àithne == 126 ? "&" : àithne == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + obrachadh_VALUE + " (uint32_t)b);");
            } else if (àithne == 108 || àithne == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (àithne == 112 ? 1 : 0) + "));");
            else if (àithne == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (àithne == 120 || àithne == 122 || àithne == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (àithne == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (àithne == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (àithne == 132) {
                int INDEX = àithne_dàta.한바이트(), 증가량 = àithne_dàta.부호한바이트(); seic_ionadail(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (àithne >= 145 && àithne <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (àithne == 145 ? "int8_t" : àithne == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (àithne >= 153 && àithne <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, meur_Liosta, suidhich, àithne_dàta.부호두바이트(), "(int32_t)a " + 비교들[àithne - 153] + " 0");
            } else if (àithne >= 159 && àithne <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, meur_Liosta, suidhich, àithne_dàta.부호두바이트(), àithne >= 165 ? "a " + 비교들[àithne - 159] + " b" : "(int32_t)a " + 비교들[àithne - 159] + " (int32_t)b");
            } else if (àithne == 167 || àithne == 200) 분기넣기(출력, meur_Liosta, suidhich, àithne == 167 ? àithne_dàta.부호두바이트() : àithne_dàta.네바이트(), null);
            else if (àithne == 170 || àithne == 171) {
                while (àithne_dàta.suidhich % 4 != 0) àithne_dàta.한바이트();
                int luach_bunaiteach = àithne_dàta.네바이트(); 출력.add("a = POP();");
                if (àithne == 170) {
                    int 아래 = àithne_dàta.네바이트(), 위 = àithne_dàta.네바이트(); long nì_COUNT = (long)위 - 아래 + 1;
                    if (nì_COUNT < 1 || nì_COUNT > (àithne_dàta.dàta.length - àithne_dàta.suidhich) / 4) throw new eadar_theangachadh_mearachd("switch cliop Mearachd");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, meur_Liosta, suidhich, àithne_dàta.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int nì_COUNT = àithne_dàta.네바이트(), 앞값 = 0;
                    if (nì_COUNT < 0 || nì_COUNT > (àithne_dàta.dàta.length - àithne_dàta.suidhich) / 8) throw new eadar_theangachadh_mearachd("switch atharraich_am_meud Mearachd");
                    for (int 순번 = 0; 순번 < nì_COUNT; 순번++) {
                        int VALUE = àithne_dàta.네바이트(); if (순번 > 0 && VALUE <= 앞값) throw new eadar_theangachadh_mearachd("switch òrdugh_VALUE Mearachd"); 앞값 = VALUE;
                        분기넣기(출력, meur_Liosta, suidhich, àithne_dàta.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, meur_Liosta, suidhich, luach_bunaiteach, null);
            } else if (àithne == 172 || àithne == 176 || àithne == 177) 출력.add("return " + (àithne == 177 ? "0" : "POP()") + ";");
            else if (àithne == 178 || àithne == 179) {
                dòigh_fiosrachadh fiosrachadh = clas_VALUE.fiosrachadh(àithne_dàta.두바이트()); if (!필드들.containsKey(fiosrachadh)) throw new eadar_theangachadh_mearachd("알 수 없는 raon_VALUE");
                출력.add(samhla("init", fiosrachadh.sealbhadair_VALUE) + "();"); String raon_VALUE = samhla("field", fiosrachadh.부분들());
                출력.add(àithne == 178 ? "PUSH(" + raon_VALUE + ");" : raon_VALUE + " = POP();");
            } else if (àithne == 184) {
                dòigh_fiosrachadh fiosrachadh = clas_VALUE.fiosrachadh(àithne_dàta.두바이트()); if (!함수들.containsKey(fiosrachadh)) throw new eadar_theangachadh_mearachd("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(fiosrachadh.서술); int nì_COUNT = 호출형식.인수.size();
                출력.add(samhla("init", fiosrachadh.sealbhadair_VALUE) + "();"); 출력.add("if(sp < " + nì_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + nì_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < nì_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + samhla("method", fiosrachadh.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.return_tomhas.equals("V")) 출력.add("PUSH(a);");
            } else if (àithne == 182) {
                dòigh_fiosrachadh fiosrachadh = clas_VALUE.fiosrachadh(àithne_dàta.두바이트());
                if (fiosrachadh.equals(new dòigh_fiosrachadh("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (fiosrachadh.equals(new dòigh_fiosrachadh("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new eadar_theangachadh_mearachd("가상 FUNCTION_VALUE 호출 미지원");
            } else if (àithne == 188) {
                if (àithne_dàta.한바이트() != 10) throw new eadar_theangachadh_mearachd("new int[]만 taic_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (àithne == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (àithne == 196) {
                int leudachan_VALUE = àithne_dàta.한바이트(), INDEX = àithne_dàta.두바이트(); seic_ionadail(INDEX, 지역변수수);
                if (leudachan_VALUE == 21 || leudachan_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (leudachan_VALUE == 54 || leudachan_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (leudachan_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + àithne_dàta.부호두바이트() + ");");
                else throw new eadar_theangachadh_mearachd("미지원 wide àithne");
            } else if (àithne == 198 || àithne == 199) {
                출력.add("a = POP();"); 분기넣기(출력, meur_Liosta, suidhich, àithne_dàta.부호두바이트(), "a " + (àithne == 198 ? "==" : "!=") + " 0");
            } else throw new eadar_theangachadh_mearachd(FUNCTION_VALUE.sealbhadair_VALUE + "." + FUNCTION_VALUE.Ainm + ", baidht_VALUE " + suidhich + ": 미지원 àithne " + àithne);
        }
        if (!경계들.containsAll(meur_Liosta)) throw new eadar_theangachadh_mearachd("àithne 경계가 아닌 곳으로 meur");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String às_phortaich_dòigh(String ceangal_samhla, String targaid, boolean 진입점여부) {
        int suidhich_INDEX = targaid.lastIndexOf('.'); if (suidhich_INDEX < 0 || !ceangal_samhla.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new eadar_theangachadh_mearachd("내보내기 지정 Mearachd");
        String sealbhadair_VALUE = targaid.substring(0, suidhich_INDEX).replace('.', '/'), Ainm = targaid.substring(suidhich_INDEX + 1); dòigh_fiosrachadh taghadh_VALUE = null;
        for (dòigh_fiosrachadh fiosrachadh : 함수들.keySet()) if (fiosrachadh.sealbhadair_VALUE.equals(sealbhadair_VALUE) && fiosrachadh.Ainm.equals(Ainm)) {
            if (taghadh_VALUE != null) throw new eadar_theangachadh_mearachd("겹친 내보내기 targaid"); taghadh_VALUE = fiosrachadh;
        }
        if (taghadh_VALUE == null || (함수들.get(taghadh_VALUE).inntrigeadh_cur_a_steach & 0x100) != 0) throw new eadar_theangachadh_mearachd("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 fòrmat_VALUE = new 함수형식(taghadh_VALUE.서술);
        if ((진입점여부 && !fòrmat_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(fòrmat_VALUE.return_tomhas)) throw new eadar_theangachadh_mearachd("cur_a_steach_puing_VALUE 또는 C 경계 fòrmat_VALUE Mearachd");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < fòrmat_VALUE.인수.size(); 순번++) {
            if (!fòrmat_VALUE.인수.get(순번).equals("I")) throw new eadar_theangachadh_mearachd("C 경계는 int 인수만 taic_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (fòrmat_VALUE.return_tomhas.equals("V") ? "void " : "int32_t ") + ceangal_samhla + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + samhla("init", taghadh_VALUE.sealbhadair_VALUE) + "(); " + (fòrmat_VALUE.return_tomhas.equals("V") ? "" : "return (int32_t)") + samhla("method", taghadh_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String gin(String cur_a_steach_puing, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<dòigh_fiosrachadh, ball_dàta> cur_a_steach_VALUE : 함수들.entrySet()) {
            dòigh_fiosrachadh fiosrachadh = cur_a_steach_VALUE.getKey(); ball_dàta dàta = cur_a_steach_VALUE.getValue(); 선언들.add(함수원형(fiosrachadh) + ";");
            if ((dàta.inntrigeadh_cur_a_steach & 0x100) != 0) {
                String CONNECT = 기계함수들.get(fiosrachadh.Ainm + fiosrachadh.서술);
                if (!fiosrachadh.sealbhadair_VALUE.equals(inneal_clas) || CONNECT == null) throw new eadar_theangachadh_mearachd("허용되지 않은 native FUNCTION_VALUE: " + fiosrachadh.Ainm);
                int nì_COUNT = new 함수형식(fiosrachadh.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < nì_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + CONNECT + "(" + (nì_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(nì_COUNT, "word"))) + ");");
                몸체들.add(함수원형(fiosrachadh) + " { return " + CONNECT + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(fiosrachadh, dàta));
        }
        for (Map.Entry<dòigh_fiosrachadh, ball_dàta> cur_a_steach_VALUE : 필드들.entrySet()) {
            dòigh_fiosrachadh fiosrachadh = cur_a_steach_VALUE.getKey(); byte[] cunbhalachan_VALUE = cur_a_steach_VALUE.getValue().buadh_VALUE.get("ConstantValue");
            String VALUE = cunbhalachan_VALUE == null ? "0" : cunbhalachan_eas_preisean(클래스들.get(fiosrachadh.sealbhadair_VALUE), new dàta_Leughadair(cunbhalachan_VALUE).두바이트());
            필드선언들.add("static word " + samhla("field", fiosrachadh.부분들()) + " = " + VALUE + ";");
        }
        for (String Ainm : 클래스들.keySet()) {
            String ro_shuidhich = samhla("init", Ainm), cor_VALUE = samhla("state", Ainm);
            선언들.add("static void " + ro_shuidhich + "(void);"); 필드선언들.add("static unsigned " + cor_VALUE + ";");
            dòigh_fiosrachadh fiosrachadh = new dòigh_fiosrachadh(Ainm, "<clinit>", "()V");
            몸체들.add("static void " + ro_shuidhich + "(void) { if(" + cor_VALUE + ") return; " + cor_VALUE + " = 1; " + (함수들.containsKey(fiosrachadh) ? samhla("method", fiosrachadh.부분들()) + "(); " : "") + cor_VALUE + " = 2; }");
        }
        몸체들.add(às_phortaich_dòigh("java_entry", cur_a_steach_puing, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int suidhich_INDEX = 지정.indexOf('='); if (suidhich_INDEX < 1) throw new eadar_theangachadh_mearachd("내보내기 지정 Mearachd");
            String Ainm = 지정.substring(0, suidhich_INDEX); 공개이름.add(Ainm); 몸체들.add(às_phortaich_dòigh(Ainm, 지정.substring(suidhich_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> cur_a_steach_VALUE : 문자열들.entrySet()) {
            String SMS = cur_a_steach_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + cur_a_steach_VALUE.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) ARRAY_VALUE.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String taic_VALUE = Files.readString(goireas_slighe.resolve("Common_Language_Runtime_taic.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(taic_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String tùs, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ainm_clàr = new HashMap<>();
        for (String loidhne : Files.readAllLines(goireas_slighe.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] paidhrich_VALUE = loidhne.split("\t"); ainm_clàr.put(paidhrich_VALUE[0], paidhrich_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(tùs); StringBuffer tomhas = new StringBuffer();
        while (찾개.find()) {
            String Ainm = 찾개.group(), 새이름 = Ainm;
            if (!Ainm.startsWith("//") && !Ainm.startsWith("/*") && !Ainm.startsWith("\"") && !Ainm.startsWith("'") && !공개이름.contains(Ainm)) {
                새이름 = ainm_clàr.getOrDefault(Ainm, Ainm);
                if (Ainm.matches("a[0-9]+")) 새이름 = "인수" + Ainm.substring(1);
                if (Ainm.matches("b[0-9]+")) 새이름 = "meur" + Ainm.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char caractar_VALUE : 새이름.toCharArray()) 표기.append(caractar_VALUE < 128 ? Character.toString(caractar_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)caractar_VALUE));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(tomhas, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(tomhas); return tomhas.toString();
    }
    String 엑스함수본문(dòigh_fiosrachadh FUNCTION_VALUE, ball_dàta dàta, Map<String,String> inneal_clàr, String targaid) {
        String 표식 = samhla("method", FUNCTION_VALUE.부분들());
        List<String> loidhne = new ArrayList<>();
        if ((dàta.inntrigeadh_cur_a_steach & 0x100) != 0) {
            String CONNECT = inneal_clàr.get(FUNCTION_VALUE.Ainm + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.sealbhadair_VALUE.equals(targaid.equals("kernel") ? "uidheam_VALUE" : "cleachdaiche") || CONNECT == null) throw new eadar_theangachadh_mearachd("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + 표식 + ":\njmp " + CONNECT;
        }
        byte[] bodhaig_an_teacsa = dàta.buadh_VALUE.get("Code"); if (bodhaig_an_teacsa == null) throw new eadar_theangachadh_mearachd("FUNCTION_VALUE 몸체가 없음");
        dàta_Leughadair Leughadair_VALUE = new dàta_Leughadair(bodhaig_an_teacsa); Leughadair_VALUE.두바이트(); int ionadail_COUNT = Leughadair_VALUE.두바이트();
        dàta_Leughadair àithne_dàta = new dàta_Leughadair(Leughadair_VALUE.읽기(Leughadair_VALUE.네바이트()));
        if (Leughadair_VALUE.두바이트() != 0) throw new eadar_theangachadh_mearachd("try/catch/finally 미지원");
        함수형식 fòrmat_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (ionadail_COUNT < fòrmat_VALUE.인수.size()) throw new eadar_theangachadh_mearachd("매개변수보다 적은 ionadail_sgòp 변수");
        Collections.addAll(loidhne,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + ionadail_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < fòrmat_VALUE.인수.size(); 순번++) Collections.addAll(loidhne,"movl " + (8 + 4 * (fòrmat_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        clas_dàta clas_VALUE = 클래스들.get(FUNCTION_VALUE.sealbhadair_VALUE); Set<Integer> 경계들 = new HashSet<>(), meur_Liosta = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (àithne_dàta.suidhich < àithne_dàta.dàta.length) {
            int suidhich = àithne_dàta.suidhich, àithne = àithne_dàta.한바이트(); String suidhich_INDEX = 표식 + "_b" + suidhich;
            loidhne.add(suidhich_INDEX + ":"); 경계들.add(suidhich);
            if (àithne == 0) loidhne.add("nop");
            else if (àithne == 1) loidhne.add("pushl $0");
            else if (àithne >= 2 && àithne <= 8) loidhne.add("pushl $" + (àithne - 3));
            else if (àithne == 16 || àithne == 17) loidhne.add("pushl $" + (àithne == 16 ? àithne_dàta.부호한바이트() : àithne_dàta.부호두바이트()));
            else if (àithne == 18 || àithne == 19) {
                int INDEX = àithne == 18 ? àithne_dàta.한바이트() : àithne_dàta.두바이트();
                loidhne.add("pushl $" + 엑스상수(clas_VALUE,INDEX));
            } else if (àithne == 21 || àithne == 25 || (àithne >= 26 && àithne <= 29) || (àithne >= 42 && àithne <= 45) || àithne == 54 || àithne == 58 || (àithne >= 59 && àithne <= 62) || (àithne >= 75 && àithne <= 78)) {
                boolean 읽음 = àithne < 54; int INDEX = àithne == 21 || àithne == 25 || àithne == 54 || àithne == 58 ? àithne_dàta.한바이트() : àithne - (àithne <= 29 ? 26 : àithne <= 45 ? 42 : àithne <= 62 ? 59 : 75);
                seic_ionadail(INDEX,ionadail_COUNT); loidhne.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (àithne == 46) Collections.addAll(loidhne,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (àithne == 79) Collections.addAll(loidhne,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (àithne == 87 || àithne == 88) loidhne.add("addl $" + (àithne == 87 ? 4 : 8) + ", %esp");
            else if (àithne >= 89 && àithne <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] òrdugh_Liosta = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[àithne - 89]; 순번++) loidhne.add("popl " + 저장기들[순번]);
                for (int 순번 : òrdugh_Liosta[àithne - 89]) loidhne.add("pushl " + 저장기들[순번]);
            } else if (àithne == 96 || àithne == 100 || àithne == 104 || àithne == 126 || àithne == 128 || àithne == 130) {
                String obrachadh_VALUE = àithne == 96 ? "addl" : àithne == 100 ? "subl" : àithne == 104 ? "imull" : àithne == 126 ? "andl" : àithne == 128 ? "orl" : "xorl";
                Collections.addAll(loidhne,"popl %ecx","popl %eax",obrachadh_VALUE + " %ecx, %eax","pushl %eax");
            } else if (àithne == 108 || àithne == 112) Collections.addAll(loidhne,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + suidhich_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + suidhich_INDEX + "_divide","xorl %edx, %edx","jmp " + suidhich_INDEX + "_done",suidhich_INDEX + "_divide:","cltd","idivl %ecx",suidhich_INDEX + "_done:","pushl " + (àithne == 108 ? "%eax" : "%edx"));
            else if (àithne == 116) loidhne.add("negl (%esp)");
            else if (àithne == 120 || àithne == 122 || àithne == 124) Collections.addAll(loidhne,"popl %ecx","popl %eax",(àithne == 120 ? "sall" : àithne == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (àithne == 132) {
                int INDEX = àithne_dàta.한바이트(), 증가 = àithne_dàta.부호한바이트(); seic_ionadail(INDEX,ionadail_COUNT); loidhne.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (àithne >= 145 && àithne <= 147) Collections.addAll(loidhne,"popl %eax",àithne == 145 ? "movsbl %al, %eax" : àithne == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (àithne >= 153 && àithne <= 166) {
                if (àithne <= 158) Collections.addAll(loidhne,"popl %eax","testl %eax, %eax");
                else Collections.addAll(loidhne,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int ceann_uidhe_VALUE = suidhich + àithne_dàta.부호두바이트(); meur_Liosta.add(ceann_uidhe_VALUE); loidhne.add(비교들[àithne - (àithne <= 158 ? 153 : 159)] + " " + 표식 + "_b" + ceann_uidhe_VALUE);
            } else if (àithne == 167 || àithne == 200) {
                int ceann_uidhe_VALUE = suidhich + (àithne == 167 ? àithne_dàta.부호두바이트() : àithne_dàta.네바이트()); meur_Liosta.add(ceann_uidhe_VALUE); loidhne.add("jmp " + 표식 + "_b" + ceann_uidhe_VALUE);
            } else if (àithne == 170 || àithne == 171) {
                while (àithne_dàta.suidhich % 4 != 0) àithne_dàta.한바이트();
                int luach_bunaiteach = suidhich + àithne_dàta.네바이트(); meur_Liosta.add(luach_bunaiteach); loidhne.add("popl %eax");
                int nì_COUNT, 아래 = 0;
                if (àithne == 170) { 아래 = àithne_dàta.네바이트(); int 위 = àithne_dàta.네바이트(); long faid_VALUE = (long)위 - 아래 + 1; if (faid_VALUE < 1 || faid_VALUE > (àithne_dàta.dàta.length - àithne_dàta.suidhich) / 4) throw new eadar_theangachadh_mearachd("switch cliop Mearachd"); nì_COUNT = (int)faid_VALUE; }
                else { nì_COUNT = àithne_dàta.네바이트(); if (nì_COUNT < 0 || nì_COUNT > (àithne_dàta.dàta.length - àithne_dàta.suidhich) / 8) throw new eadar_theangachadh_mearachd("switch atharraich_am_meud Mearachd"); }
                for (int 순번 = 0; 순번 < nì_COUNT; 순번++) {
                    int VALUE = àithne == 170 ? 아래 + 순번 : àithne_dàta.네바이트(), ceann_uidhe_VALUE = suidhich + àithne_dàta.네바이트(); meur_Liosta.add(ceann_uidhe_VALUE);
                    Collections.addAll(loidhne,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + ceann_uidhe_VALUE);
                }
                loidhne.add("jmp " + 표식 + "_b" + luach_bunaiteach);
            } else if (àithne == 172 || àithne == 176 || àithne == 177) {
                if (àithne != 177) loidhne.add("popl %eax"); Collections.addAll(loidhne,"leave","ret");
            } else if (àithne == 178 || àithne == 179) {
                dòigh_fiosrachadh fiosrachadh = clas_VALUE.fiosrachadh(àithne_dàta.두바이트()); if (!필드들.containsKey(fiosrachadh)) throw new eadar_theangachadh_mearachd("알 수 없는 raon_VALUE");
                Collections.addAll(loidhne,"call " + samhla("init",fiosrachadh.sealbhadair_VALUE),(àithne == 178 ? "pushl " : "popl ") + samhla("field",fiosrachadh.부분들()));
            } else if (àithne == 184) {
                dòigh_fiosrachadh fiosrachadh = clas_VALUE.fiosrachadh(àithne_dàta.두바이트()); if (!함수들.containsKey(fiosrachadh)) throw new eadar_theangachadh_mearachd("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(fiosrachadh.서술); Collections.addAll(loidhne,"call " + samhla("init",fiosrachadh.sealbhadair_VALUE),"call " + samhla("method",fiosrachadh.부분들()));
                if (!호출형식.인수.isEmpty()) loidhne.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.return_tomhas.equals("V")) loidhne.add("pushl %eax");
            } else if (àithne == 182) {
                dòigh_fiosrachadh fiosrachadh = clas_VALUE.fiosrachadh(àithne_dàta.두바이트());
                if (fiosrachadh.equals(new dòigh_fiosrachadh("java/lang/String","length","()I"))) Collections.addAll(loidhne,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (fiosrachadh.equals(new dòigh_fiosrachadh("java/lang/String","charAt","(I)C"))) Collections.addAll(loidhne,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new eadar_theangachadh_mearachd("가상 FUNCTION_VALUE 호출 미지원");
            } else if (àithne == 188) {
                if (àithne_dàta.한바이트() != 10) throw new eadar_theangachadh_mearachd("new int[]만 taic_VALUE"); Collections.addAll(loidhne,"popl %eax","call rt_new_array","pushl %eax");
            } else if (àithne == 190) Collections.addAll(loidhne,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (àithne == 196) {
                int leudachan_VALUE = àithne_dàta.한바이트(), INDEX = àithne_dàta.두바이트(); seic_ionadail(INDEX,ionadail_COUNT);
                if (leudachan_VALUE == 21 || leudachan_VALUE == 25 || leudachan_VALUE == 54 || leudachan_VALUE == 58) loidhne.add((leudachan_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (leudachan_VALUE == 132) loidhne.add("addl $" + àithne_dàta.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new eadar_theangachadh_mearachd("wide àithne 미지원");
            } else if (àithne == 198 || àithne == 199) {
                int ceann_uidhe_VALUE = suidhich + àithne_dàta.부호두바이트(); meur_Liosta.add(ceann_uidhe_VALUE); Collections.addAll(loidhne,"popl %eax","testl %eax, %eax",(àithne == 198 ? "je " : "jne ") + 표식 + "_b" + ceann_uidhe_VALUE);
            } else throw new eadar_theangachadh_mearachd("미지원 àithne: " + àithne);
        }
        if (!경계들.containsAll(meur_Liosta)) throw new eadar_theangachadh_mearachd("àithne 경계가 아닌 곳으로 meur");
        loidhne.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",loidhne);
    }
    String 엑스상수(clas_dàta dàta, int INDEX) {
        if (dàta.상수종류[INDEX] == 3) return dàta.cunbhalachan_dàta[INDEX].toString();
        if (dàta.상수종류[INDEX] == 8) return sreang_samhla(dàta.문자((Integer)dàta.cunbhalachan_dàta[INDEX]));
        throw new eadar_theangachadh_mearachd("정수와 sreang_VALUE 상수만 taic_VALUE");
    }
    String 엑스조립본(String cur_a_steach_puing, List<String> 내보냄, String targaid) throws IOException {
        Map<String,String> inneal_clàr = new HashMap<>();
        for (String loidhne : Files.readAllLines(goireas_slighe.resolve("엑스기계함수.tsv"))) { String[] paidhrich_VALUE = loidhne.split("\t"); if (paidhrich_VALUE[0].equals(targaid)) inneal_clàr.put(paidhrich_VALUE[1] + paidhrich_VALUE[2],paidhrich_VALUE[3]); }
        int suidhich_INDEX = cur_a_steach_puing.lastIndexOf('.'); if (suidhich_INDEX < 0) throw new eadar_theangachadh_mearachd("cur_a_steach_puing 지정 Mearachd");
        String sealbhadair_VALUE = cur_a_steach_puing.substring(0,suidhich_INDEX).replace('.','/'), dòigh_cur_a_steach_ainm = cur_a_steach_puing.substring(suidhich_INDEX + 1); dòigh_fiosrachadh cur_a_steach_puing_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { dòigh_fiosrachadh fiosrachadh = new dòigh_fiosrachadh(sealbhadair_VALUE,dòigh_cur_a_steach_ainm,서술); if (함수들.containsKey(fiosrachadh)) { if (cur_a_steach_puing_VALUE != null) throw new eadar_theangachadh_mearachd("겹친 cur_a_steach_puing"); cur_a_steach_puing_VALUE = fiosrachadh; } }
        if (cur_a_steach_puing_VALUE == null || (함수들.get(cur_a_steach_puing_VALUE).inntrigeadh_cur_a_steach & 0x100) != 0) throw new eadar_theangachadh_mearachd("cur_a_steach_puing_VALUE FUNCTION_VALUE fòrmat_VALUE Mearachd");
        List<String> loidhne = new ArrayList<>(); loidhne.add(".code32");
        for (clas_dàta dàta : 클래스들.values()) {
            String cor_VALUE = samhla("state",dàta.Ainm), ro_shuidhich = samhla("init",dàta.Ainm);
            Collections.addAll(loidhne,".bss",".balign 4",cor_VALUE + ": .long 0",".text",ro_shuidhich + ":","cmpl $0, " + cor_VALUE,"jne " + ro_shuidhich + "_done","movl $1, " + cor_VALUE);
            dòigh_fiosrachadh 초기화참조 = new dòigh_fiosrachadh(dàta.Ainm,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) loidhne.add("call " + samhla("method",초기화참조.부분들()));
            Collections.addAll(loidhne,"movl $2, " + cor_VALUE,ro_shuidhich + "_done:","ret");
            for (ball_dàta raon_VALUE : dàta.raon_VALUE) {
                byte[] cunbhalachan_VALUE = raon_VALUE.buadh_VALUE.get("ConstantValue"); String VALUE = cunbhalachan_VALUE == null ? "0" : 엑스상수(dàta,new dàta_Leughadair(cunbhalachan_VALUE).두바이트());
                Collections.addAll(loidhne,".data",".balign 4",samhla("field",dàta.Ainm,raon_VALUE.Ainm,raon_VALUE.서술) + ": .long " + VALUE);
            }
            for (ball_dàta FUNCTION_VALUE : dàta.FUNCTION_VALUE) if (!FUNCTION_VALUE.Ainm.equals("<init>")) loidhne.add(엑스함수본문(new dòigh_fiosrachadh(dàta.Ainm,FUNCTION_VALUE.Ainm,FUNCTION_VALUE.서술),FUNCTION_VALUE,inneal_clàr,targaid));
        }
        Collections.addAll(loidhne,".text",".globl java_entry","java_entry:","call " + samhla("init",cur_a_steach_puing_VALUE.sealbhadair_VALUE),"call " + samhla("method",cur_a_steach_puing_VALUE.부분들()));
        if (cur_a_steach_puing_VALUE.서술.equals("()V")) loidhne.add("xorl %eax, %eax"); loidhne.add("ret");
        for (String 지정 : 내보냄) {
            int comharra_crìche_VALUE = 지정.indexOf('='); if (comharra_crìche_VALUE < 1) throw new eadar_theangachadh_mearachd("내보내기 지정 Mearachd");
            String 외부 = 지정.substring(0,comharra_crìche_VALUE), FUNCTION_VALUE = 지정.substring(comharra_crìche_VALUE + 1); int roinneadh_tomhas = FUNCTION_VALUE.lastIndexOf('.');
            if (roinneadh_tomhas < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new eadar_theangachadh_mearachd("내보내기 samhla Mearachd");
            String clas_VALUE = FUNCTION_VALUE.substring(0,roinneadh_tomhas).replace('.','/'), Ainm = FUNCTION_VALUE.substring(roinneadh_tomhas + 1); dòigh_fiosrachadh taghadh_VALUE = null;
            for (dòigh_fiosrachadh fiosrachadh : 함수들.keySet()) if (fiosrachadh.sealbhadair_VALUE.equals(clas_VALUE) && fiosrachadh.Ainm.equals(Ainm)) { if (taghadh_VALUE != null) throw new eadar_theangachadh_mearachd("겹친 내보내기 targaid"); taghadh_VALUE = fiosrachadh; }
            if (taghadh_VALUE == null) throw new eadar_theangachadh_mearachd("내보낼 함수가 없음");
            Collections.addAll(loidhne,".text",".globl " + 외부,외부 + ":","call " + samhla("init",taghadh_VALUE.sealbhadair_VALUE),"jmp " + samhla("method",taghadh_VALUE.부분들()));
        }
        loidhne.add(".section .rodata");
        for (Map.Entry<String,String> cur_a_steach_VALUE : 문자열들.entrySet()) {
            Collections.addAll(loidhne,".balign 4",cur_a_steach_VALUE.getValue() + ":",".long " + cur_a_steach_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char leasan_VALUE : cur_a_steach_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(leasan_VALUE)); if (!단위들.isEmpty()) loidhne.add(".long " + String.join(",",단위들));
        }
        loidhne.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",loidhne) + "\n";
    }
    static void gnìomhaich_inneal(List<String> àithne) throws Exception {
        if (new ProcessBuilder(àithne).inheritIO().start().waitFor() != 0) throw new eadar_theangachadh_mearachd("tog_tùs Mearachd: " + àithne.get(0));
    }
    static String dàta_sreang(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String targaid, String cur_a_steach_puing, List<String> 내보냄, Path 출력, Path goireas_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), clas_slighe = 임시.resolve("classes"); Files.createDirectory(clas_slighe);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",clas_slighe.toString(),"-sourcepath",clas_slighe.toString(),"-d",clas_slighe.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int tùs_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new eadar_theangachadh_mearachd("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); tùs_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new eadar_theangachadh_mearachd(".java 또는 .class만 taic_VALUE");
            }
            if (tùs_COUNT > 0) gnìomhaich_inneal(자바명령);
            try (java.util.stream.Stream<Path> slighe_Liosta = Files.walk(clas_slighe)) { slighe_Liosta.filter(Slighe -> Slighe.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,targaid.equals("user") ? "user" : "kernel",262144,goireas_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(cur_a_steach_puing,내보냄,targaid); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path inneal_suidhich = goireas_VALUE.getParent();
            gnìomhaich_inneal(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            gnìomhaich_inneal(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),inneal_suidhich.resolve("Common_Language_Runtime_taic.s").toString()));
            List<String> CONNECT = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (targaid.equals("kernel")) CONNECT.add("-r");
            else {
                gnìomhaich_inneal(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),inneal_suidhich.resolve(targaid.equals("user") ? "Start_cleachdaiche_ap.s" : "리눅스시작.s").toString()));
                Collections.addAll(CONNECT,"-e","_start",임시.resolve("start.o").toString());
                if (targaid.equals("user")) Collections.addAll(CONNECT,"-T",inneal_suidhich.resolve("cleachdaiche_ceangal_co_dhealbhachd.ld").toString());
            }
            Collections.addAll(CONNECT,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); gnìomhaich_inneal(CONNECT);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path foillsich_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),foillsich_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(foillsich_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(foillsich_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(targaid.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> samhla_dàta = new ArrayList<>(), tùs_dàta = new ArrayList<>();
            for (dòigh_fiosrachadh fiosrachadh : CONVERT_VALUE.함수들.keySet()) samhla_dàta.add(dàta_sreang(samhla("method",fiosrachadh.부분들())) + ":" + dàta_sreang(fiosrachadh.sealbhadair_VALUE + "." + fiosrachadh.Ainm + fiosrachadh.서술));
            for (Path 입력 : 입력들) {
                byte[] hais_faidhle = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte VALUE : hais_faidhle) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                tùs_dàta.add(dàta_sreang(입력.toAbsolutePath().toString()) + ":" + dàta_sreang(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + dàta_sreang(targaid) + ",\"entry\":" + dàta_sreang(cur_a_steach_puing) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",samhla_dàta) + "},\"sources\":{" + String.join(",",tùs_dàta) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> slighe_Liosta = Files.walk(임시)) { for (Path Slighe : (Iterable<Path>)slighe_Liosta.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Slighe); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String cur_a_steach_puing = null, targaid = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> slighe_Liosta = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry clas_VALUE.FUNCTION_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export samhla=clas_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": cur_a_steach_puing = 인수[++순번]; break;
                    case "--profile": targaid = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new eadar_theangachadh_mearachd("알 수 없는 옵션: " + VALUE); slighe_Liosta.add(Paths.get(VALUE));
                }
            }
            if (cur_a_steach_puing == null || 출력경로 == null || slighe_Liosta.isEmpty()) throw new eadar_theangachadh_mearachd("--entry, -o, clas_VALUE 파일이 필요합니다");
            Path goireas_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new eadar_theangachadh_mearachd("알 수 없는 gnìomhaich_àithne targaid");
                엑스번역(slighe_Liosta,엑스대상,cur_a_steach_puing,내보냄,출력경로,goireas_VALUE); return;
            }
            String tùs = new 기계어미리번역(slighe_Liosta, targaid, 낱말수, goireas_VALUE).gin(cur_a_steach_puing, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, tùs, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Mearachd) { System.err.println("tog_tùs Mearachd: " + Mearachd.getMessage()); System.exit(1); }
    }
}
