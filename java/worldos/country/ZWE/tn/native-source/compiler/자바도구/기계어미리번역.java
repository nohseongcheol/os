// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java mofuta_Boleng 파일에서 독립 ARM64 커널용 C 원문을 만든다. pinagare JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Thanolo_phoso extends RuntimeException {
        Thanolo_phoso(String 설명) { super(설명); }
    }
    static final class tshedimosetso_mmuisi {
        final byte[] tshedimosetso;
        int 위치;
        tshedimosetso_mmuisi(byte[] 입력자료) { tshedimosetso = 입력자료; }
        byte[] 읽기(int boleele_Boleng) {
            if (boleele_Boleng < 0 || boleele_Boleng > tshedimosetso.length - 위치) throw new Thanolo_phoso("잘린 mofuta_Boleng 또는 Taelo tshedimosetso");
            byte[] 결과 = Arrays.copyOfRange(tshedimosetso, 위치, 위치 + boleele_Boleng); 위치 += boleele_Boleng; return 결과;
        }
        int 한바이트() { if (위치 >= tshedimosetso.length) throw new Thanolo_phoso("잘린 Taelo tshedimosetso"); return tshedimosetso[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class karolo_tshedimosetso {
        final int letlelesega_tsenyo;
        final String leina, 서술;
        final Map<String, byte[]> nonofo_Boleng;
        karolo_tshedimosetso(int letlelesega_Boleng, String leina_Boleng, String 서술값, Map<String, byte[]> nonofo_tshedimosetso) {
            letlelesega_tsenyo = letlelesega_Boleng; leina = leina_Boleng; 서술 = 서술값; nonofo_Boleng = nonofo_tshedimosetso;
        }
    }
    static final class mokgwa_Tshupiso implements Comparable<mokgwa_Tshupiso> {
        final String mong_Boleng, leina, 서술;
        mokgwa_Tshupiso(String 소유값, String leina_Boleng, String 서술값) { mong_Boleng = 소유값; leina = leina_Boleng; 서술 = 서술값; }
        String[] 부분들() { return new String[]{mong_Boleng, leina, 서술}; }
        public int compareTo(mokgwa_Tshupiso semphato_Boleng) {
            int 비교값 = mong_Boleng.compareTo(semphato_Boleng.mong_Boleng);
            if (비교값 == 0) 비교값 = leina.compareTo(semphato_Boleng.leina);
            return 비교값 == 0 ? 서술.compareTo(semphato_Boleng.서술) : 비교값;
        }
        public boolean equals(Object semphato_Boleng) { return semphato_Boleng instanceof mokgwa_Tshupiso && compareTo((mokgwa_Tshupiso) semphato_Boleng) == 0; }
        public int hashCode() { return Objects.hash(mong_Boleng, leina, 서술); }
    }
    static final class mofuta_tshedimosetso {
        final int[] 상수종류;
        final Object[] tlhomameng_tshedimosetso;
        final String leina;
        final List<karolo_tshedimosetso> lefelo_Boleng, TIRISO_Boleng;
        mofuta_tshedimosetso(Path tsela) throws IOException {
            tshedimosetso_mmuisi mmuisi_Boleng = new tshedimosetso_mmuisi(Files.readAllBytes(tsela));
            if (mmuisi_Boleng.네바이트() != 0xcafebabe) throw new Thanolo_phoso("Java mofuta_Boleng 표식이 아님");
            mmuisi_Boleng.읽기(4);
            int 개수 = mmuisi_Boleng.두바이트(); 상수종류 = new int[개수]; tlhomameng_tshedimosetso = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = mmuisi_Boleng.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int boleele_Boleng = mmuisi_Boleng.두바이트();
                        byte[] Letshwao_kemelwa = mmuisi_Boleng.읽기(boleele_Boleng), 길이붙인자료 = new byte[boleele_Boleng + 2];
                        길이붙인자료[0] = (byte)(boleele_Boleng >> 8); 길이붙인자료[1] = (byte)boleele_Boleng;
                        System.arraycopy(Letshwao_kemelwa, 0, 길이붙인자료, 2, boleele_Boleng);
                        tlhomameng_tshedimosetso[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: tlhomameng_tshedimosetso[순번] = mmuisi_Boleng.네바이트(); break;
                    case 4: mmuisi_Boleng.읽기(4); break;
                    case 5: case 6: mmuisi_Boleng.읽기(8); 순번++; break;
                    case 7: case 8: case 16: tlhomameng_tshedimosetso[순번] = mmuisi_Boleng.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        tlhomameng_tshedimosetso[순번] = new int[]{mmuisi_Boleng.두바이트(), mmuisi_Boleng.두바이트()}; break;
                    case 15: tlhomameng_tshedimosetso[순번] = new int[]{mmuisi_Boleng.한바이트(), mmuisi_Boleng.두바이트()}; break;
                    default: throw new Thanolo_phoso("지원하지 않는 tlhomameng_Boleng 종류: " + 종류);
                }
            }
            mmuisi_Boleng.두바이트(); leina = mofuta_leina(mmuisi_Boleng.두바이트());
            if (!mofuta_leina(mmuisi_Boleng.두바이트()).equals("java/lang/Object") || mmuisi_Boleng.두바이트() != 0)
                throw new Thanolo_phoso(leina + ": 상속 및 인터페이스 미지원");
            lefelo_Boleng = 멤버읽기(mmuisi_Boleng); TIRISO_Boleng = 멤버읽기(mmuisi_Boleng); 속성읽기(mmuisi_Boleng);
            if (mmuisi_Boleng.위치 != mmuisi_Boleng.tshedimosetso.length) throw new Thanolo_phoso("mofuta_Boleng 뒤에 남은 tshedimosetso");
        }
        String 문자(int tshupane) {
            if (tshupane < 1 || tshupane >= 상수종류.length || 상수종류[tshupane] != 1) throw new Thanolo_phoso("문자 tlhomameng_Boleng tshupane phoso");
            return (String) tlhomameng_tshedimosetso[tshupane];
        }
        String mofuta_leina(int tshupane) {
            if (tshupane < 1 || tshupane >= 상수종류.length || 상수종류[tshupane] != 7) throw new Thanolo_phoso("mofuta_Boleng Tshupiso phoso");
            return 문자((Integer)tlhomameng_tshedimosetso[tshupane]);
        }
        mokgwa_Tshupiso Tshupiso(int tshupane) {
            if (tshupane < 1 || tshupane >= 상수종류.length || 상수종류[tshupane] < 9 || 상수종류[tshupane] > 11) throw new Thanolo_phoso("멤버 Tshupiso phoso");
            int[] pana_Boleng = (int[])tlhomameng_tshedimosetso[tshupane], leina_pana = (int[])tlhomameng_tshedimosetso[pana_Boleng[1]];
            return new mokgwa_Tshupiso(mofuta_leina(pana_Boleng[0]), 문자(leina_pana[0]), 문자(leina_pana[1]));
        }
        Map<String, byte[]> 속성읽기(tshedimosetso_mmuisi mmuisi_Boleng) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = mmuisi_Boleng.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String nonofo_leina = 문자(mmuisi_Boleng.두바이트()); byte[] Boleng = mmuisi_Boleng.읽기(mmuisi_Boleng.네바이트());
                if (결과.put(nonofo_leina, Boleng) != null) throw new Thanolo_phoso("겹친 nonofo_Boleng: " + nonofo_leina);
            }
            return 결과;
        }
        List<karolo_tshedimosetso> 멤버읽기(tshedimosetso_mmuisi mmuisi_Boleng) {
            List<karolo_tshedimosetso> 결과 = new ArrayList<>(); int 개수 = mmuisi_Boleng.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int letlelesega_tsenyo = mmuisi_Boleng.두바이트(); String mokgwa_tsenyo_leina = 문자(mmuisi_Boleng.두바이트()), 서술 = 문자(mmuisi_Boleng.두바이트());
                결과.add(new karolo_tshedimosetso(letlelesega_tsenyo, mokgwa_tsenyo_leina, 서술, 속성읽기(mmuisi_Boleng)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Thanolo_phoso("TIRISO_Boleng 서술 phoso: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Thanolo_phoso("TIRISO_Boleng 서술 phoso: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Thanolo_phoso("TIRISO_Boleng 서술 phoso: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String tlhopho_Boleng = null;
            for (String fometa_Boleng : 허용형식) if (서술.startsWith(fometa_Boleng, 위치)) { tlhopho_Boleng = fometa_Boleng; break; }
            if (tlhopho_Boleng == null) throw new Thanolo_phoso("지원하지 않는 mofutatshedimosetso: " + 서술);
            결과.add(tlhopho_Boleng); 위치 += tlhopho_Boleng.length();
        }
        return 결과;
    }
    static String letshwao(String 종류, String... 부분들) {
        try {
            byte[] heše_faele = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", heše_faele[순번] & 255));
            return SMS.toString();
        } catch (Exception phoso) { throw new Thanolo_phoso(phoso.toString()); }
    }
    final Map<String, mofuta_tshedimosetso> 클래스들 = new TreeMap<>();
    final Map<mokgwa_Tshupiso, karolo_tshedimosetso> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, motšhine_mofuta;
    final int 동적기억낱말수;
    final Path sediriswa_tsela;
    기계어미리번역(List<Path> tsela_lenaane, String setotwa, int 낱말수, Path sediriswa_Boleng) throws IOException {
        if ((!setotwa.equals("kernel") && !setotwa.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Thanolo_phoso("diragatsa_Taelo setotwa 또는 memori_Boleng 공간 lekanya phoso");
        실행대상 = setotwa; 동적기억낱말수 = 낱말수; sediriswa_tsela = sediriswa_Boleng;
        // 이 이름도 국가별 Motswedi_sebopego_sa_tshedimosetso 생성 시 해당 언어로 옮긴다.
        motšhine_mofuta = setotwa.equals("kernel") ? "보드" : "modirisi";
        for (String Mola : Files.readAllLines(sediriswa_Boleng.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Mola.split("\t", -1);
            if (부분들.length != 4) throw new Thanolo_phoso("motšhine TIRISO_Boleng tshedimosetso phoso");
            if (부분들[0].equals(setotwa)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path tsela : tsela_lenaane) {
            mofuta_tshedimosetso tshedimosetso = new mofuta_tshedimosetso(tsela);
            if (클래스들.put(tshedimosetso.leina, tshedimosetso) != null) throw new Thanolo_phoso("중복 mofuta_Boleng: " + tshedimosetso.leina);
            for (karolo_tshedimosetso lefelo_Boleng : tshedimosetso.lefelo_Boleng) {
                if ((lefelo_Boleng.letlelesega_tsenyo & 8) == 0 || 형식읽기(lefelo_Boleng.서술).equals(Collections.singletonList("V"))) throw new Thanolo_phoso("e_e_emeng_Boleng 필드만 Thuso_Boleng");
                if (필드들.put(new mokgwa_Tshupiso(tshedimosetso.leina, lefelo_Boleng.leina, lefelo_Boleng.서술), lefelo_Boleng) != null) throw new Thanolo_phoso("중복 lefelo_Boleng");
            }
            for (karolo_tshedimosetso TIRISO_Boleng : tshedimosetso.TIRISO_Boleng) {
                if (TIRISO_Boleng.leina.equals("<init>")) continue;
                if ((TIRISO_Boleng.letlelesega_tsenyo & 8) == 0 || (TIRISO_Boleng.letlelesega_tsenyo & (0x20 | 0x400)) != 0) throw new Thanolo_phoso("e_e_emeng_Boleng 비동기화 함수만 Thuso_Boleng");
                new 함수형식(TIRISO_Boleng.서술);
                if (함수들.put(new mokgwa_Tshupiso(tshedimosetso.leina, TIRISO_Boleng.leina, TIRISO_Boleng.서술), TIRISO_Boleng) != null) throw new Thanolo_phoso("중복 TIRISO_Boleng");
            }
        }
    }
    String dikwalwa_letshwao(String SMS) { return 문자열들.computeIfAbsent(SMS, Boleng -> "j_text_" + 문자열들.size()); }
    String tlhomameng_Tlhaloso(mofuta_tshedimosetso tshedimosetso, int tshupane) {
        if (tshupane < 1 || tshupane >= tshedimosetso.상수종류.length) throw new Thanolo_phoso("tlhomameng_Boleng tshupane faelekhutshwe_ya_media phoso");
        if (tshedimosetso.상수종류[tshupane] == 3) return "(word)(uint32_t)(" + tshedimosetso.tlhomameng_tshedimosetso[tshupane] + ")";
        if (tshedimosetso.상수종류[tshupane] == 8) return "(word)" + dikwalwa_letshwao(tshedimosetso.문자((Integer)tshedimosetso.tlhomameng_tshedimosetso[tshupane]));
        throw new Thanolo_phoso("정수와 dikwalwa_Boleng 상수만 Thuso_Boleng");
    }
    String 함수원형(mokgwa_Tshupiso Tshupiso) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Tshupiso.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + letshwao("method", Tshupiso.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void tlhola_e_e_gaufi(int tshupane, int 지역변수수) { if (tshupane < 0 || tshupane >= 지역변수수) throw new Thanolo_phoso("e_e_gaufi_Mothamo 변수 tshupane faelekhutshwe_ya_media phoso"); }
    void 분기넣기(List<String> 출력, Set<Integer> lekala_lenaane, int 위치, int 이동량, String boemo) {
        int bogorogelo_Boleng = 위치 + 이동량; lekala_lenaane.add(bogorogelo_Boleng);
        출력.add((boemo == null ? "" : "if (" + boemo + ") ") + "goto b" + bogorogelo_Boleng + ";");
    }
    String 함수본문(mokgwa_Tshupiso TIRISO_Boleng, karolo_tshedimosetso tshedimosetso) {
        byte[] 본문자료 = tshedimosetso.nonofo_Boleng.get("Code"); if (본문자료 == null) throw new Thanolo_phoso("TIRISO_Boleng 몸체가 없음: " + TIRISO_Boleng.leina);
        tshedimosetso_mmuisi mmuisi_Boleng = new tshedimosetso_mmuisi(본문자료); int 쌓임깊이 = mmuisi_Boleng.두바이트(), 지역변수수 = mmuisi_Boleng.두바이트();
        tshedimosetso_mmuisi Taelo_tshedimosetso = new tshedimosetso_mmuisi(mmuisi_Boleng.읽기(mmuisi_Boleng.네바이트()));
        if (mmuisi_Boleng.두바이트() != 0) throw new Thanolo_phoso("try/catch/finally 미지원");
        함수형식 fometa_Boleng = new 함수형식(TIRISO_Boleng.서술); if (지역변수수 < fometa_Boleng.인수.size()) throw new Thanolo_phoso("매개변수보다 적은 e_e_gaufi_Mothamo 변수");
        mofuta_tshedimosetso mofuta_Boleng = 클래스들.get(TIRISO_Boleng.mong_Boleng);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(TIRISO_Boleng) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < fometa_Boleng.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), lekala_lenaane = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (Taelo_tshedimosetso.위치 < Taelo_tshedimosetso.tshedimosetso.length) {
            int 위치 = Taelo_tshedimosetso.위치, Taelo = Taelo_tshedimosetso.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (Taelo == 0) continue;
            if (Taelo == 1) 출력.add("PUSH(0);");
            else if (Taelo >= 2 && Taelo <= 8) 출력.add("PUSH((uint32_t)(" + (Taelo - 3) + "));");
            else if (Taelo == 16 || Taelo == 17) 출력.add("PUSH((uint32_t)(" + (Taelo == 16 ? Taelo_tshedimosetso.부호한바이트() : Taelo_tshedimosetso.부호두바이트()) + "));");
            else if (Taelo == 18 || Taelo == 19) 출력.add("PUSH(" + tlhomameng_Tlhaloso(mofuta_Boleng, Taelo == 18 ? Taelo_tshedimosetso.한바이트() : Taelo_tshedimosetso.두바이트()) + ");");
            else if (Taelo == 21 || Taelo == 25 || (Taelo >= 26 && Taelo <= 29) || (Taelo >= 42 && Taelo <= 45)) {
                int tshupane = Taelo == 21 || Taelo == 25 ? Taelo_tshedimosetso.한바이트() : Taelo - (Taelo <= 29 ? 26 : 42);
                tlhola_e_e_gaufi(tshupane, 지역변수수); 출력.add("PUSH(l[" + tshupane + "]);");
            } else if (Taelo == 54 || Taelo == 58 || (Taelo >= 59 && Taelo <= 62) || (Taelo >= 75 && Taelo <= 78)) {
                int tshupane = Taelo == 54 || Taelo == 58 ? Taelo_tshedimosetso.한바이트() : Taelo - (Taelo <= 62 ? 59 : 75);
                tlhola_e_e_gaufi(tshupane, 지역변수수); 출력.add("l[" + tshupane + "] = POP();");
            } else if (Taelo == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Taelo == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Taelo == 87 || Taelo == 88) 출력.add(Taelo == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Taelo >= 89 && Taelo <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] thulaganyo_lenaane = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Taelo - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char Boleng : thulaganyo_lenaane[Taelo - 89].toCharArray()) 출력.add("PUSH(" + Boleng + ");");
            } else if (Taelo == 96 || Taelo == 100 || Taelo == 104 || Taelo == 126 || Taelo == 128 || Taelo == 130) {
                String tiro_Boleng = Taelo == 96 ? "+" : Taelo == 100 ? "-" : Taelo == 104 ? "*" : Taelo == 126 ? "&" : Taelo == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + tiro_Boleng + " (uint32_t)b);");
            } else if (Taelo == 108 || Taelo == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Taelo == 112 ? 1 : 0) + "));");
            else if (Taelo == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Taelo == 120 || Taelo == 122 || Taelo == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Taelo == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Taelo == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Taelo == 132) {
                int tshupane = Taelo_tshedimosetso.한바이트(), 증가량 = Taelo_tshedimosetso.부호한바이트(); tlhola_e_e_gaufi(tshupane, 지역변수수);
                출력.add("l[" + tshupane + "] = (uint32_t)l[" + tshupane + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Taelo >= 145 && Taelo <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Taelo == 145 ? "int8_t" : Taelo == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Taelo >= 153 && Taelo <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, lekala_lenaane, 위치, Taelo_tshedimosetso.부호두바이트(), "(int32_t)a " + 비교들[Taelo - 153] + " 0");
            } else if (Taelo >= 159 && Taelo <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, lekala_lenaane, 위치, Taelo_tshedimosetso.부호두바이트(), Taelo >= 165 ? "a " + 비교들[Taelo - 159] + " b" : "(int32_t)a " + 비교들[Taelo - 159] + " (int32_t)b");
            } else if (Taelo == 167 || Taelo == 200) 분기넣기(출력, lekala_lenaane, 위치, Taelo == 167 ? Taelo_tshedimosetso.부호두바이트() : Taelo_tshedimosetso.네바이트(), null);
            else if (Taelo == 170 || Taelo == 171) {
                while (Taelo_tshedimosetso.위치 % 4 != 0) Taelo_tshedimosetso.한바이트();
                int boleng_jo_bo_rulaganyeditsweng_ruri = Taelo_tshedimosetso.네바이트(); 출력.add("a = POP();");
                if (Taelo == 170) {
                    int 아래 = Taelo_tshedimosetso.네바이트(), 위 = Taelo_tshedimosetso.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (Taelo_tshedimosetso.tshedimosetso.length - Taelo_tshedimosetso.위치) / 4) throw new Thanolo_phoso("switch faelekhutshwe_ya_media phoso");
                    for (long Boleng = 아래; Boleng <= 위; Boleng++) 분기넣기(출력, lekala_lenaane, 위치, Taelo_tshedimosetso.네바이트(), "(int32_t)a == (" + Boleng + ")");
                } else {
                    int 개수 = Taelo_tshedimosetso.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (Taelo_tshedimosetso.tshedimosetso.length - Taelo_tshedimosetso.위치) / 8) throw new Thanolo_phoso("switch lekanya phoso");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int Boleng = Taelo_tshedimosetso.네바이트(); if (순번 > 0 && Boleng <= 앞값) throw new Thanolo_phoso("switch thulaganyo_Boleng phoso"); 앞값 = Boleng;
                        분기넣기(출력, lekala_lenaane, 위치, Taelo_tshedimosetso.네바이트(), "(int32_t)a == (" + Boleng + ")");
                    }
                }
                분기넣기(출력, lekala_lenaane, 위치, boleng_jo_bo_rulaganyeditsweng_ruri, null);
            } else if (Taelo == 172 || Taelo == 176 || Taelo == 177) 출력.add("return " + (Taelo == 177 ? "0" : "POP()") + ";");
            else if (Taelo == 178 || Taelo == 179) {
                mokgwa_Tshupiso Tshupiso = mofuta_Boleng.Tshupiso(Taelo_tshedimosetso.두바이트()); if (!필드들.containsKey(Tshupiso)) throw new Thanolo_phoso("알 수 없는 lefelo_Boleng");
                출력.add(letshwao("init", Tshupiso.mong_Boleng) + "();"); String lefelo_Boleng = letshwao("field", Tshupiso.부분들());
                출력.add(Taelo == 178 ? "PUSH(" + lefelo_Boleng + ");" : lefelo_Boleng + " = POP();");
            } else if (Taelo == 184) {
                mokgwa_Tshupiso Tshupiso = mofuta_Boleng.Tshupiso(Taelo_tshedimosetso.두바이트()); if (!함수들.containsKey(Tshupiso)) throw new Thanolo_phoso("알 수 없는 TIRISO_Boleng");
                함수형식 호출형식 = new 함수형식(Tshupiso.서술); int 개수 = 호출형식.인수.size();
                출력.add(letshwao("init", Tshupiso.mong_Boleng) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + letshwao("method", Tshupiso.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Taelo == 182) {
                mokgwa_Tshupiso Tshupiso = mofuta_Boleng.Tshupiso(Taelo_tshedimosetso.두바이트());
                if (Tshupiso.equals(new mokgwa_Tshupiso("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Tshupiso.equals(new mokgwa_Tshupiso("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Thanolo_phoso("가상 TIRISO_Boleng 호출 미지원");
            } else if (Taelo == 188) {
                if (Taelo_tshedimosetso.한바이트() != 10) throw new Thanolo_phoso("new int[]만 Thuso_Boleng"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Taelo == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Taelo == 196) {
                int katoloso_Boleng = Taelo_tshedimosetso.한바이트(), tshupane = Taelo_tshedimosetso.두바이트(); tlhola_e_e_gaufi(tshupane, 지역변수수);
                if (katoloso_Boleng == 21 || katoloso_Boleng == 25) 출력.add("PUSH(l[" + tshupane + "]);");
                else if (katoloso_Boleng == 54 || katoloso_Boleng == 58) 출력.add("l[" + tshupane + "] = POP();");
                else if (katoloso_Boleng == 132) 출력.add("l[" + tshupane + "] = (uint32_t)l[" + tshupane + "] + (uint32_t)(" + Taelo_tshedimosetso.부호두바이트() + ");");
                else throw new Thanolo_phoso("미지원 wide Taelo");
            } else if (Taelo == 198 || Taelo == 199) {
                출력.add("a = POP();"); 분기넣기(출력, lekala_lenaane, 위치, Taelo_tshedimosetso.부호두바이트(), "a " + (Taelo == 198 ? "==" : "!=") + " 0");
            } else throw new Thanolo_phoso(TIRISO_Boleng.mong_Boleng + "." + TIRISO_Boleng.leina + ", baete_Boleng " + 위치 + ": 미지원 Taelo " + Taelo);
        }
        if (!경계들.containsAll(lekala_lenaane)) throw new Thanolo_phoso("Taelo 경계가 아닌 곳으로 lekala");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String romelantle_mokgwa(String Kgokagano_letshwao, String setotwa, boolean 진입점여부) {
        int 자리 = setotwa.lastIndexOf('.'); if (자리 < 0 || !Kgokagano_letshwao.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Thanolo_phoso("내보내기 abela_Boleng phoso");
        String mong_Boleng = setotwa.substring(0, 자리).replace('.', '/'), leina = setotwa.substring(자리 + 1); mokgwa_Tshupiso tlhopho_Boleng = null;
        for (mokgwa_Tshupiso Tshupiso : 함수들.keySet()) if (Tshupiso.mong_Boleng.equals(mong_Boleng) && Tshupiso.leina.equals(leina)) {
            if (tlhopho_Boleng != null) throw new Thanolo_phoso("겹친 내보내기 setotwa"); tlhopho_Boleng = Tshupiso;
        }
        if (tlhopho_Boleng == null || (함수들.get(tlhopho_Boleng).letlelesega_tsenyo & 0x100) != 0) throw new Thanolo_phoso("내보낼 함수가 없음 또는 native TIRISO_Boleng");
        함수형식 fometa_Boleng = new 함수형식(tlhopho_Boleng.서술);
        if ((진입점여부 && !fometa_Boleng.인수.isEmpty()) || !Arrays.asList("V", "I").contains(fometa_Boleng.반환)) throw new Thanolo_phoso("tsenyo_ntlha_Boleng 또는 C 경계 fometa_Boleng phoso");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < fometa_Boleng.인수.size(); 순번++) {
            if (!fometa_Boleng.인수.get(순번).equals("I")) throw new Thanolo_phoso("C 경계는 int 인수만 Thuso_Boleng");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (fometa_Boleng.반환.equals("V") ? "void " : "int32_t ") + Kgokagano_letshwao + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + letshwao("init", tlhopho_Boleng.mong_Boleng) + "(); " + (fometa_Boleng.반환.equals("V") ? "" : "return (int32_t)") + letshwao("method", tlhopho_Boleng.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String tsenyo_ntlha, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<mokgwa_Tshupiso, karolo_tshedimosetso> tsenyo_Boleng : 함수들.entrySet()) {
            mokgwa_Tshupiso Tshupiso = tsenyo_Boleng.getKey(); karolo_tshedimosetso tshedimosetso = tsenyo_Boleng.getValue(); 선언들.add(함수원형(Tshupiso) + ";");
            if ((tshedimosetso.letlelesega_tsenyo & 0x100) != 0) {
                String Golaganya = 기계함수들.get(Tshupiso.leina + Tshupiso.서술);
                if (!Tshupiso.mong_Boleng.equals(motšhine_mofuta) || Golaganya == null) throw new Thanolo_phoso("허용되지 않은 native TIRISO_Boleng: " + Tshupiso.leina);
                int 개수 = new 함수형식(Tshupiso.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Golaganya + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Tshupiso) + " { return " + Golaganya + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Tshupiso, tshedimosetso));
        }
        for (Map.Entry<mokgwa_Tshupiso, karolo_tshedimosetso> tsenyo_Boleng : 필드들.entrySet()) {
            mokgwa_Tshupiso Tshupiso = tsenyo_Boleng.getKey(); byte[] tlhomameng_Boleng = tsenyo_Boleng.getValue().nonofo_Boleng.get("ConstantValue");
            String Boleng = tlhomameng_Boleng == null ? "0" : tlhomameng_Tlhaloso(클래스들.get(Tshupiso.mong_Boleng), new tshedimosetso_mmuisi(tlhomameng_Boleng).두바이트());
            필드선언들.add("static word " + letshwao("field", Tshupiso.부분들()) + " = " + Boleng + ";");
        }
        for (String leina : 클래스들.keySet()) {
            String go_baakanyetsa_tiriso = letshwao("init", leina), kemo_Boleng = letshwao("state", leina);
            선언들.add("static void " + go_baakanyetsa_tiriso + "(void);"); 필드선언들.add("static unsigned " + kemo_Boleng + ";");
            mokgwa_Tshupiso Tshupiso = new mokgwa_Tshupiso(leina, "<clinit>", "()V");
            몸체들.add("static void " + go_baakanyetsa_tiriso + "(void) { if(" + kemo_Boleng + ") return; " + kemo_Boleng + " = 1; " + (함수들.containsKey(Tshupiso) ? letshwao("method", Tshupiso.부분들()) + "(); " : "") + kemo_Boleng + " = 2; }");
        }
        몸체들.add(romelantle_mokgwa("java_entry", tsenyo_ntlha, true)); Set<String> 공개이름 = new HashSet<>();
        for (String abela_Boleng : 내보내기목록) {
            int 자리 = abela_Boleng.indexOf('='); if (자리 < 1) throw new Thanolo_phoso("내보내기 abela_Boleng phoso");
            String leina = abela_Boleng.substring(0, 자리); 공개이름.add(leina); 몸체들.add(romelantle_mokgwa(leina, abela_Boleng.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> tsenyo_Boleng : 문자열들.entrySet()) {
            String SMS = tsenyo_Boleng.getKey(); StringBuilder setlhopha_Boleng_ed437109 = new StringBuilder("static const word " + tsenyo_Boleng.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) setlhopha_Boleng_ed437109.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(setlhopha_Boleng_ed437109.append("};").toString());
        }
        String Thuso_Boleng = Files.readString(sediriswa_tsela.resolve("nakotsamaiso_ya_puo_e_e_tlwaelegileng_Thuso.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Thuso_Boleng + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String Motswedi, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> leina_lenaneothalo = new HashMap<>();
        for (String Mola : Files.readAllLines(sediriswa_tsela.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] pana_Boleng = Mola.split("\t"); leina_lenaneothalo.put(pana_Boleng[0], pana_Boleng[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(Motswedi); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String leina = 찾개.group(), 새이름 = leina;
            if (!leina.startsWith("//") && !leina.startsWith("/*") && !leina.startsWith("\"") && !leina.startsWith("'") && !공개이름.contains(leina)) {
                새이름 = leina_lenaneothalo.getOrDefault(leina, leina);
                if (leina.matches("a[0-9]+")) 새이름 = "인수" + leina.substring(1);
                if (leina.matches("b[0-9]+")) 새이름 = "lekala" + leina.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char Letshwao_Boleng : 새이름.toCharArray()) 표기.append(Letshwao_Boleng < 128 ? Character.toString(Letshwao_Boleng) : String.format(Locale.ROOT, "\\u%04x", (int)Letshwao_Boleng));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(mokgwa_Tshupiso TIRISO_Boleng, karolo_tshedimosetso tshedimosetso, Map<String,String> motšhine_lenaneothalo, String setotwa) {
        String 표식 = letshwao("method", TIRISO_Boleng.부분들());
        List<String> Mola = new ArrayList<>();
        if ((tshedimosetso.letlelesega_tsenyo & 0x100) != 0) {
            String Golaganya = motšhine_lenaneothalo.get(TIRISO_Boleng.leina + TIRISO_Boleng.서술);
            if (!TIRISO_Boleng.mong_Boleng.equals(setotwa.equals("kernel") ? "mobaele_Boleng" : "modirisi") || Golaganya == null) throw new Thanolo_phoso("허용되지 않은 native TIRISO_Boleng");
            return ".text\n" + 표식 + ":\njmp " + Golaganya;
        }
        byte[] diteng_tsa_mokwalo = tshedimosetso.nonofo_Boleng.get("Code"); if (diteng_tsa_mokwalo == null) throw new Thanolo_phoso("TIRISO_Boleng 몸체가 없음");
        tshedimosetso_mmuisi mmuisi_Boleng = new tshedimosetso_mmuisi(diteng_tsa_mokwalo); mmuisi_Boleng.두바이트(); int 지역수 = mmuisi_Boleng.두바이트();
        tshedimosetso_mmuisi Taelo_tshedimosetso = new tshedimosetso_mmuisi(mmuisi_Boleng.읽기(mmuisi_Boleng.네바이트()));
        if (mmuisi_Boleng.두바이트() != 0) throw new Thanolo_phoso("try/catch/finally 미지원");
        함수형식 fometa_Boleng = new 함수형식(TIRISO_Boleng.서술); if (지역수 < fometa_Boleng.인수.size()) throw new Thanolo_phoso("매개변수보다 적은 e_e_gaufi_Mothamo 변수");
        Collections.addAll(Mola,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < fometa_Boleng.인수.size(); 순번++) Collections.addAll(Mola,"movl " + (8 + 4 * (fometa_Boleng.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        mofuta_tshedimosetso mofuta_Boleng = 클래스들.get(TIRISO_Boleng.mong_Boleng); Set<Integer> 경계들 = new HashSet<>(), lekala_lenaane = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (Taelo_tshedimosetso.위치 < Taelo_tshedimosetso.tshedimosetso.length) {
            int 위치 = Taelo_tshedimosetso.위치, Taelo = Taelo_tshedimosetso.한바이트(); String 자리 = 표식 + "_b" + 위치;
            Mola.add(자리 + ":"); 경계들.add(위치);
            if (Taelo == 0) Mola.add("nop");
            else if (Taelo == 1) Mola.add("pushl $0");
            else if (Taelo >= 2 && Taelo <= 8) Mola.add("pushl $" + (Taelo - 3));
            else if (Taelo == 16 || Taelo == 17) Mola.add("pushl $" + (Taelo == 16 ? Taelo_tshedimosetso.부호한바이트() : Taelo_tshedimosetso.부호두바이트()));
            else if (Taelo == 18 || Taelo == 19) {
                int tshupane = Taelo == 18 ? Taelo_tshedimosetso.한바이트() : Taelo_tshedimosetso.두바이트();
                Mola.add("pushl $" + 엑스상수(mofuta_Boleng,tshupane));
            } else if (Taelo == 21 || Taelo == 25 || (Taelo >= 26 && Taelo <= 29) || (Taelo >= 42 && Taelo <= 45) || Taelo == 54 || Taelo == 58 || (Taelo >= 59 && Taelo <= 62) || (Taelo >= 75 && Taelo <= 78)) {
                boolean 읽음 = Taelo < 54; int tshupane = Taelo == 21 || Taelo == 25 || Taelo == 54 || Taelo == 58 ? Taelo_tshedimosetso.한바이트() : Taelo - (Taelo <= 29 ? 26 : Taelo <= 45 ? 42 : Taelo <= 62 ? 59 : 75);
                tlhola_e_e_gaufi(tshupane,지역수); Mola.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (tshupane + 1)) + "(%ebp)");
            } else if (Taelo == 46) Collections.addAll(Mola,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Taelo == 79) Collections.addAll(Mola,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Taelo == 87 || Taelo == 88) Mola.add("addl $" + (Taelo == 87 ? 4 : 8) + ", %esp");
            else if (Taelo >= 89 && Taelo <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] thulaganyo_lenaane = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Taelo - 89]; 순번++) Mola.add("popl " + 저장기들[순번]);
                for (int 순번 : thulaganyo_lenaane[Taelo - 89]) Mola.add("pushl " + 저장기들[순번]);
            } else if (Taelo == 96 || Taelo == 100 || Taelo == 104 || Taelo == 126 || Taelo == 128 || Taelo == 130) {
                String tiro_Boleng = Taelo == 96 ? "addl" : Taelo == 100 ? "subl" : Taelo == 104 ? "imull" : Taelo == 126 ? "andl" : Taelo == 128 ? "orl" : "xorl";
                Collections.addAll(Mola,"popl %ecx","popl %eax",tiro_Boleng + " %ecx, %eax","pushl %eax");
            } else if (Taelo == 108 || Taelo == 112) Collections.addAll(Mola,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Taelo == 108 ? "%eax" : "%edx"));
            else if (Taelo == 116) Mola.add("negl (%esp)");
            else if (Taelo == 120 || Taelo == 122 || Taelo == 124) Collections.addAll(Mola,"popl %ecx","popl %eax",(Taelo == 120 ? "sall" : Taelo == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Taelo == 132) {
                int tshupane = Taelo_tshedimosetso.한바이트(), 증가 = Taelo_tshedimosetso.부호한바이트(); tlhola_e_e_gaufi(tshupane,지역수); Mola.add("addl $" + 증가 + ", -" + (4 * (tshupane + 1)) + "(%ebp)");
            } else if (Taelo >= 145 && Taelo <= 147) Collections.addAll(Mola,"popl %eax",Taelo == 145 ? "movsbl %al, %eax" : Taelo == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Taelo >= 153 && Taelo <= 166) {
                if (Taelo <= 158) Collections.addAll(Mola,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Mola,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int bogorogelo_Boleng = 위치 + Taelo_tshedimosetso.부호두바이트(); lekala_lenaane.add(bogorogelo_Boleng); Mola.add(비교들[Taelo - (Taelo <= 158 ? 153 : 159)] + " " + 표식 + "_b" + bogorogelo_Boleng);
            } else if (Taelo == 167 || Taelo == 200) {
                int bogorogelo_Boleng = 위치 + (Taelo == 167 ? Taelo_tshedimosetso.부호두바이트() : Taelo_tshedimosetso.네바이트()); lekala_lenaane.add(bogorogelo_Boleng); Mola.add("jmp " + 표식 + "_b" + bogorogelo_Boleng);
            } else if (Taelo == 170 || Taelo == 171) {
                while (Taelo_tshedimosetso.위치 % 4 != 0) Taelo_tshedimosetso.한바이트();
                int boleng_jo_bo_rulaganyeditsweng_ruri = 위치 + Taelo_tshedimosetso.네바이트(); lekala_lenaane.add(boleng_jo_bo_rulaganyeditsweng_ruri); Mola.add("popl %eax");
                int 개수, 아래 = 0;
                if (Taelo == 170) { 아래 = Taelo_tshedimosetso.네바이트(); int 위 = Taelo_tshedimosetso.네바이트(); long boleele_Boleng = (long)위 - 아래 + 1; if (boleele_Boleng < 1 || boleele_Boleng > (Taelo_tshedimosetso.tshedimosetso.length - Taelo_tshedimosetso.위치) / 4) throw new Thanolo_phoso("switch faelekhutshwe_ya_media phoso"); 개수 = (int)boleele_Boleng; }
                else { 개수 = Taelo_tshedimosetso.네바이트(); if (개수 < 0 || 개수 > (Taelo_tshedimosetso.tshedimosetso.length - Taelo_tshedimosetso.위치) / 8) throw new Thanolo_phoso("switch lekanya phoso"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int Boleng = Taelo == 170 ? 아래 + 순번 : Taelo_tshedimosetso.네바이트(), bogorogelo_Boleng = 위치 + Taelo_tshedimosetso.네바이트(); lekala_lenaane.add(bogorogelo_Boleng);
                    Collections.addAll(Mola,"cmpl $" + Boleng + ", %eax","je " + 표식 + "_b" + bogorogelo_Boleng);
                }
                Mola.add("jmp " + 표식 + "_b" + boleng_jo_bo_rulaganyeditsweng_ruri);
            } else if (Taelo == 172 || Taelo == 176 || Taelo == 177) {
                if (Taelo != 177) Mola.add("popl %eax"); Collections.addAll(Mola,"leave","ret");
            } else if (Taelo == 178 || Taelo == 179) {
                mokgwa_Tshupiso Tshupiso = mofuta_Boleng.Tshupiso(Taelo_tshedimosetso.두바이트()); if (!필드들.containsKey(Tshupiso)) throw new Thanolo_phoso("알 수 없는 lefelo_Boleng");
                Collections.addAll(Mola,"call " + letshwao("init",Tshupiso.mong_Boleng),(Taelo == 178 ? "pushl " : "popl ") + letshwao("field",Tshupiso.부분들()));
            } else if (Taelo == 184) {
                mokgwa_Tshupiso Tshupiso = mofuta_Boleng.Tshupiso(Taelo_tshedimosetso.두바이트()); if (!함수들.containsKey(Tshupiso)) throw new Thanolo_phoso("알 수 없는 TIRISO_Boleng");
                함수형식 호출형식 = new 함수형식(Tshupiso.서술); Collections.addAll(Mola,"call " + letshwao("init",Tshupiso.mong_Boleng),"call " + letshwao("method",Tshupiso.부분들()));
                if (!호출형식.인수.isEmpty()) Mola.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) Mola.add("pushl %eax");
            } else if (Taelo == 182) {
                mokgwa_Tshupiso Tshupiso = mofuta_Boleng.Tshupiso(Taelo_tshedimosetso.두바이트());
                if (Tshupiso.equals(new mokgwa_Tshupiso("java/lang/String","length","()I"))) Collections.addAll(Mola,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Tshupiso.equals(new mokgwa_Tshupiso("java/lang/String","charAt","(I)C"))) Collections.addAll(Mola,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Thanolo_phoso("가상 TIRISO_Boleng 호출 미지원");
            } else if (Taelo == 188) {
                if (Taelo_tshedimosetso.한바이트() != 10) throw new Thanolo_phoso("new int[]만 Thuso_Boleng"); Collections.addAll(Mola,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Taelo == 190) Collections.addAll(Mola,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Taelo == 196) {
                int katoloso_Boleng = Taelo_tshedimosetso.한바이트(), tshupane = Taelo_tshedimosetso.두바이트(); tlhola_e_e_gaufi(tshupane,지역수);
                if (katoloso_Boleng == 21 || katoloso_Boleng == 25 || katoloso_Boleng == 54 || katoloso_Boleng == 58) Mola.add((katoloso_Boleng <= 25 ? "pushl " : "popl ") + "-" + 4 * (tshupane + 1) + "(%ebp)");
                else if (katoloso_Boleng == 132) Mola.add("addl $" + Taelo_tshedimosetso.부호두바이트() + ", -" + 4 * (tshupane + 1) + "(%ebp)");
                else throw new Thanolo_phoso("wide Taelo 미지원");
            } else if (Taelo == 198 || Taelo == 199) {
                int bogorogelo_Boleng = 위치 + Taelo_tshedimosetso.부호두바이트(); lekala_lenaane.add(bogorogelo_Boleng); Collections.addAll(Mola,"popl %eax","testl %eax, %eax",(Taelo == 198 ? "je " : "jne ") + 표식 + "_b" + bogorogelo_Boleng);
            } else throw new Thanolo_phoso("미지원 Taelo: " + Taelo);
        }
        if (!경계들.containsAll(lekala_lenaane)) throw new Thanolo_phoso("Taelo 경계가 아닌 곳으로 lekala");
        Mola.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",Mola);
    }
    String 엑스상수(mofuta_tshedimosetso tshedimosetso, int tshupane) {
        if (tshedimosetso.상수종류[tshupane] == 3) return tshedimosetso.tlhomameng_tshedimosetso[tshupane].toString();
        if (tshedimosetso.상수종류[tshupane] == 8) return dikwalwa_letshwao(tshedimosetso.문자((Integer)tshedimosetso.tlhomameng_tshedimosetso[tshupane]));
        throw new Thanolo_phoso("정수와 dikwalwa_Boleng 상수만 Thuso_Boleng");
    }
    String 엑스조립본(String tsenyo_ntlha, List<String> 내보냄, String setotwa) throws IOException {
        Map<String,String> motšhine_lenaneothalo = new HashMap<>();
        for (String Mola : Files.readAllLines(sediriswa_tsela.resolve("엑스기계함수.tsv"))) { String[] pana_Boleng = Mola.split("\t"); if (pana_Boleng[0].equals(setotwa)) motšhine_lenaneothalo.put(pana_Boleng[1] + pana_Boleng[2],pana_Boleng[3]); }
        int 자리 = tsenyo_ntlha.lastIndexOf('.'); if (자리 < 0) throw new Thanolo_phoso("tsenyo_ntlha abela_Boleng phoso");
        String mong_Boleng = tsenyo_ntlha.substring(0,자리).replace('.','/'), mokgwa_tsenyo_leina = tsenyo_ntlha.substring(자리 + 1); mokgwa_Tshupiso tsenyo_ntlha_Boleng = null;
        for (String 서술 : Arrays.asList("()I","()V")) { mokgwa_Tshupiso Tshupiso = new mokgwa_Tshupiso(mong_Boleng,mokgwa_tsenyo_leina,서술); if (함수들.containsKey(Tshupiso)) { if (tsenyo_ntlha_Boleng != null) throw new Thanolo_phoso("겹친 tsenyo_ntlha"); tsenyo_ntlha_Boleng = Tshupiso; } }
        if (tsenyo_ntlha_Boleng == null || (함수들.get(tsenyo_ntlha_Boleng).letlelesega_tsenyo & 0x100) != 0) throw new Thanolo_phoso("tsenyo_ntlha_Boleng TIRISO_Boleng fometa_Boleng phoso");
        List<String> Mola = new ArrayList<>(); Mola.add(".code32");
        for (mofuta_tshedimosetso tshedimosetso : 클래스들.values()) {
            String kemo_Boleng = letshwao("state",tshedimosetso.leina), go_baakanyetsa_tiriso = letshwao("init",tshedimosetso.leina);
            Collections.addAll(Mola,".bss",".balign 4",kemo_Boleng + ": .long 0",".text",go_baakanyetsa_tiriso + ":","cmpl $0, " + kemo_Boleng,"jne " + go_baakanyetsa_tiriso + "_done","movl $1, " + kemo_Boleng);
            mokgwa_Tshupiso 초기화참조 = new mokgwa_Tshupiso(tshedimosetso.leina,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Mola.add("call " + letshwao("method",초기화참조.부분들()));
            Collections.addAll(Mola,"movl $2, " + kemo_Boleng,go_baakanyetsa_tiriso + "_done:","ret");
            for (karolo_tshedimosetso lefelo_Boleng : tshedimosetso.lefelo_Boleng) {
                byte[] tlhomameng_Boleng = lefelo_Boleng.nonofo_Boleng.get("ConstantValue"); String Boleng = tlhomameng_Boleng == null ? "0" : 엑스상수(tshedimosetso,new tshedimosetso_mmuisi(tlhomameng_Boleng).두바이트());
                Collections.addAll(Mola,".data",".balign 4",letshwao("field",tshedimosetso.leina,lefelo_Boleng.leina,lefelo_Boleng.서술) + ": .long " + Boleng);
            }
            for (karolo_tshedimosetso TIRISO_Boleng : tshedimosetso.TIRISO_Boleng) if (!TIRISO_Boleng.leina.equals("<init>")) Mola.add(엑스함수본문(new mokgwa_Tshupiso(tshedimosetso.leina,TIRISO_Boleng.leina,TIRISO_Boleng.서술),TIRISO_Boleng,motšhine_lenaneothalo,setotwa));
        }
        Collections.addAll(Mola,".text",".globl java_entry","java_entry:","call " + letshwao("init",tsenyo_ntlha_Boleng.mong_Boleng),"call " + letshwao("method",tsenyo_ntlha_Boleng.부분들()));
        if (tsenyo_ntlha_Boleng.서술.equals("()V")) Mola.add("xorl %eax, %eax"); Mola.add("ret");
        for (String abela_Boleng : 내보냄) {
            int sekgaoganyi_Boleng = abela_Boleng.indexOf('='); if (sekgaoganyi_Boleng < 1) throw new Thanolo_phoso("내보내기 abela_Boleng phoso");
            String 외부 = abela_Boleng.substring(0,sekgaoganyi_Boleng), TIRISO_Boleng = abela_Boleng.substring(sekgaoganyi_Boleng + 1); int 나눔 = TIRISO_Boleng.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Thanolo_phoso("내보내기 letshwao phoso");
            String mofuta_Boleng = TIRISO_Boleng.substring(0,나눔).replace('.','/'), leina = TIRISO_Boleng.substring(나눔 + 1); mokgwa_Tshupiso tlhopho_Boleng = null;
            for (mokgwa_Tshupiso Tshupiso : 함수들.keySet()) if (Tshupiso.mong_Boleng.equals(mofuta_Boleng) && Tshupiso.leina.equals(leina)) { if (tlhopho_Boleng != null) throw new Thanolo_phoso("겹친 내보내기 setotwa"); tlhopho_Boleng = Tshupiso; }
            if (tlhopho_Boleng == null) throw new Thanolo_phoso("내보낼 함수가 없음");
            Collections.addAll(Mola,".text",".globl " + 외부,외부 + ":","call " + letshwao("init",tlhopho_Boleng.mong_Boleng),"jmp " + letshwao("method",tlhopho_Boleng.부분들()));
        }
        Mola.add(".section .rodata");
        for (Map.Entry<String,String> tsenyo_Boleng : 문자열들.entrySet()) {
            Collections.addAll(Mola,".balign 4",tsenyo_Boleng.getValue() + ":",".long " + tsenyo_Boleng.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char thuto_Boleng : tsenyo_Boleng.getKey().toCharArray()) 단위들.add(Integer.toString(thuto_Boleng)); if (!단위들.isEmpty()) Mola.add(".long " + String.join(",",단위들));
        }
        Mola.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Mola) + "\n";
    }
    static void diragatsa_sediriswa(List<String> Taelo) throws Exception {
        if (new ProcessBuilder(Taelo).inheritIO().start().waitFor() != 0) throw new Thanolo_phoso("aga_Motswedi phoso: " + Taelo.get(0));
    }
    static String tshedimosetso_dikwalwa(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String setotwa, String tsenyo_ntlha, List<String> 내보냄, Path 출력, Path sediriswa_Boleng) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), mofuta_tsela = 임시.resolve("classes"); Files.createDirectory(mofuta_tsela);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",mofuta_tsela.toString(),"-sourcepath",mofuta_tsela.toString(),"-d",mofuta_tsela.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Thanolo_phoso("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Thanolo_phoso(".java 또는 .class만 Thuso_Boleng");
            }
            if (원문수 > 0) diragatsa_sediriswa(자바명령);
            try (java.util.stream.Stream<Path> tsela_lenaane = Files.walk(mofuta_tsela)) { tsela_lenaane.filter(tsela -> tsela.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,setotwa.equals("user") ? "user" : "kernel",262144,sediriswa_Boleng);
            String 조립 = 변환.엑스조립본(tsenyo_ntlha,내보냄,setotwa); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = sediriswa_Boleng.getParent();
            diragatsa_sediriswa(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            diragatsa_sediriswa(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("nakotsamaiso_ya_puo_e_e_tlwaelegileng_Thuso.s").toString()));
            List<String> Golaganya = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (setotwa.equals("kernel")) Golaganya.add("-r");
            else {
                diragatsa_sediriswa(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(setotwa.equals("user") ? "simolola_modirisi_Tiriso.s" : "리눅스시작.s").toString()));
                Collections.addAll(Golaganya,"-e","_start",임시.resolve("start.o").toString());
                if (setotwa.equals("user")) Collections.addAll(Golaganya,"-T",도구위치.resolve("modirisi_Kgokagano_Boalo.ld").toString());
            }
            Collections.addAll(Golaganya,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); diragatsa_sediriswa(Golaganya);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path phasalatsa_Boleng = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),phasalatsa_Boleng,StandardCopyOption.REPLACE_EXISTING); Files.move(phasalatsa_Boleng,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(phasalatsa_Boleng); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(setotwa.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> letshwao_tshedimosetso = new ArrayList<>(), tshedimosetsomotswedi = new ArrayList<>();
            for (mokgwa_Tshupiso Tshupiso : 변환.함수들.keySet()) letshwao_tshedimosetso.add(tshedimosetso_dikwalwa(letshwao("method",Tshupiso.부분들())) + ":" + tshedimosetso_dikwalwa(Tshupiso.mong_Boleng + "." + Tshupiso.leina + Tshupiso.서술));
            for (Path 입력 : 입력들) {
                byte[] heše_faele = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte Boleng : heše_faele) SMS.append(String.format(Locale.ROOT,"%02x",Boleng & 255));
                tshedimosetsomotswedi.add(tshedimosetso_dikwalwa(입력.toAbsolutePath().toString()) + ":" + tshedimosetso_dikwalwa(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + tshedimosetso_dikwalwa(setotwa) + ",\"entry\":" + tshedimosetso_dikwalwa(tsenyo_ntlha) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",letshwao_tshedimosetso) + "},\"sources\":{" + String.join(",",tshedimosetsomotswedi) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> tsela_lenaane = Files.walk(임시)) { for (Path tsela : (Iterable<Path>)tsela_lenaane.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(tsela); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String tsenyo_ntlha = null, setotwa = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> tsela_lenaane = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String Boleng = 인수[순번];
                switch (Boleng) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry mofuta_Boleng.TIRISO_Boleng -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export letshwao=mofuta_Boleng.TIRISO_Boleng] 클래스파일 또는 Java원문"); return;
                    case "--entry": tsenyo_ntlha = 인수[++순번]; break;
                    case "--profile": setotwa = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (Boleng.startsWith("-")) throw new Thanolo_phoso("알 수 없는 옵션: " + Boleng); tsela_lenaane.add(Paths.get(Boleng));
                }
            }
            if (tsenyo_ntlha == null || 출력경로 == null || tsela_lenaane.isEmpty()) throw new Thanolo_phoso("--entry, -o, mofuta_Boleng 파일이 필요합니다");
            Path sediriswa_Boleng = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Thanolo_phoso("알 수 없는 diragatsa_Taelo setotwa");
                엑스번역(tsela_lenaane,엑스대상,tsenyo_ntlha,내보냄,출력경로,sediriswa_Boleng); return;
            }
            String Motswedi = new 기계어미리번역(tsela_lenaane, setotwa, 낱말수, sediriswa_Boleng).생성(tsenyo_ntlha, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, Motswedi, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception phoso) { System.err.println("aga_Motswedi phoso: " + phoso.getMessage()); System.exit(1); }
    }
}
