// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java legoro_boleng_55654bf1 파일에서 독립 ARM64 커널용 C 원문을 만든다. go_nea_ditirelo JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Phetolelo_phošo extends RuntimeException {
        Phetolelo_phošo(String 설명) { super(설명); }
    }
    static final class data_mmadi {
        final byte[] data;
        int 위치;
        data_mmadi(byte[] 입력자료) { data = 입력자료; }
        byte[] Bala(int botelele_boleng) {
            if (botelele_boleng < 0 || botelele_boleng > data.length - 위치) throw new Phetolelo_phošo("잘린 legoro_boleng_55654bf1 또는 Taelo data");
            byte[] 결과 = Arrays.copyOfRange(data, 위치, 위치 + botelele_boleng); 위치 += botelele_boleng; return 결과;
        }
        int 한바이트() { if (위치 >= data.length) throw new Phetolelo_phošo("잘린 Taelo data"); return data[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class setho_data {
        final int fihlelela_go_tsenya_tshedimošo;
        final String Leina, 서술;
        final Map<String, byte[]> tlhaodi_ya_faele_boleng;
        setho_data(int fihlelela_boleng, String leina_boleng, String 서술값, Map<String, byte[]> tlhaodi_ya_faele_data) {
            fihlelela_go_tsenya_tshedimošo = fihlelela_boleng; Leina = leina_boleng; 서술 = 서술값; tlhaodi_ya_faele_boleng = tlhaodi_ya_faele_data;
        }
    }
    static final class mokgwa_Dipadišo implements Comparable<mokgwa_Dipadišo> {
        final String mong_boleng, Leina, 서술;
        mokgwa_Dipadišo(String 소유값, String leina_boleng, String 서술값) { mong_boleng = 소유값; Leina = leina_boleng; 서술 = 서술값; }
        String[] 부분들() { return new String[]{mong_boleng, Leina, 서술}; }
        public int compareTo(mokgwa_Dipadišo sedirišwa_sa_legoro_le_tee_boleng) {
            int 비교값 = mong_boleng.compareTo(sedirišwa_sa_legoro_le_tee_boleng.mong_boleng);
            if (비교값 == 0) 비교값 = Leina.compareTo(sedirišwa_sa_legoro_le_tee_boleng.Leina);
            return 비교값 == 0 ? 서술.compareTo(sedirišwa_sa_legoro_le_tee_boleng.서술) : 비교값;
        }
        public boolean equals(Object sedirišwa_sa_legoro_le_tee_boleng) { return sedirišwa_sa_legoro_le_tee_boleng instanceof mokgwa_Dipadišo && compareTo((mokgwa_Dipadišo) sedirišwa_sa_legoro_le_tee_boleng) == 0; }
        public int hashCode() { return Objects.hash(mong_boleng, Leina, 서술); }
    }
    static final class legoro_data {
        final int[] 상수종류;
        final Object[] ya_go_se_fetoge_data;
        final String Leina;
        final List<setho_data> lefelwana_boleng, TIRO_boleng;
        legoro_data(Path Tsejana) throws IOException {
            data_mmadi mmadi_boleng = new data_mmadi(Files.readAllBytes(Tsejana));
            if (mmadi_boleng.네바이트() != 0xcafebabe) throw new Phetolelo_phošo("Java legoro_boleng_55654bf1 표식이 아님");
            mmadi_boleng.Bala(4);
            int 개수 = mmadi_boleng.두바이트(); 상수종류 = new int[개수]; ya_go_se_fetoge_data = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = mmadi_boleng.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int botelele_boleng = mmadi_boleng.두바이트();
                        byte[] tlhaka_pafara = mmadi_boleng.Bala(botelele_boleng), 길이붙인자료 = new byte[botelele_boleng + 2];
                        길이붙인자료[0] = (byte)(botelele_boleng >> 8); 길이붙인자료[1] = (byte)botelele_boleng;
                        System.arraycopy(tlhaka_pafara, 0, 길이붙인자료, 2, botelele_boleng);
                        ya_go_se_fetoge_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: ya_go_se_fetoge_data[순번] = mmadi_boleng.네바이트(); break;
                    case 4: mmadi_boleng.Bala(4); break;
                    case 5: case 6: mmadi_boleng.Bala(8); 순번++; break;
                    case 7: case 8: case 16: ya_go_se_fetoge_data[순번] = mmadi_boleng.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        ya_go_se_fetoge_data[순번] = new int[]{mmadi_boleng.두바이트(), mmadi_boleng.두바이트()}; break;
                    case 15: ya_go_se_fetoge_data[순번] = new int[]{mmadi_boleng.한바이트(), mmadi_boleng.두바이트()}; break;
                    default: throw new Phetolelo_phošo("지원하지 않는 ya_go_se_fetoge_boleng 종류: " + 종류);
                }
            }
            mmadi_boleng.두바이트(); Leina = legoro_leina(mmadi_boleng.두바이트());
            if (!legoro_leina(mmadi_boleng.두바이트()).equals("java/lang/Object") || mmadi_boleng.두바이트() != 0)
                throw new Phetolelo_phošo(Leina + ": 상속 및 인터페이스 미지원");
            lefelwana_boleng = 멤버읽기(mmadi_boleng); TIRO_boleng = 멤버읽기(mmadi_boleng); 속성읽기(mmadi_boleng);
            if (mmadi_boleng.위치 != mmadi_boleng.data.length) throw new Phetolelo_phošo("legoro_boleng_55654bf1 뒤에 남은 data");
        }
        String 문자(int lokela) {
            if (lokela < 1 || lokela >= 상수종류.length || 상수종류[lokela] != 1) throw new Phetolelo_phošo("문자 ya_go_se_fetoge_boleng lokela Phošo");
            return (String) ya_go_se_fetoge_data[lokela];
        }
        String legoro_leina(int lokela) {
            if (lokela < 1 || lokela >= 상수종류.length || 상수종류[lokela] != 7) throw new Phetolelo_phošo("legoro_boleng_55654bf1 Dipadišo Phošo");
            return 문자((Integer)ya_go_se_fetoge_data[lokela]);
        }
        mokgwa_Dipadišo Dipadišo(int lokela) {
            if (lokela < 1 || lokela >= 상수종류.length || 상수종류[lokela] < 9 || 상수종류[lokela] > 11) throw new Phetolelo_phošo("멤버 Dipadišo Phošo");
            int[] phera_boleng = (int[])ya_go_se_fetoge_data[lokela], leina_phera = (int[])ya_go_se_fetoge_data[phera_boleng[1]];
            return new mokgwa_Dipadišo(legoro_leina(phera_boleng[0]), 문자(leina_phera[0]), 문자(leina_phera[1]));
        }
        Map<String, byte[]> 속성읽기(data_mmadi mmadi_boleng) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = mmadi_boleng.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String tlhaodi_ya_faele_leina = 문자(mmadi_boleng.두바이트()); byte[] boleng = mmadi_boleng.Bala(mmadi_boleng.네바이트());
                if (결과.put(tlhaodi_ya_faele_leina, boleng) != null) throw new Phetolelo_phošo("겹친 tlhaodi_ya_faele_boleng: " + tlhaodi_ya_faele_leina);
            }
            return 결과;
        }
        List<setho_data> 멤버읽기(data_mmadi mmadi_boleng) {
            List<setho_data> 결과 = new ArrayList<>(); int 개수 = mmadi_boleng.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int fihlelela_go_tsenya_tshedimošo = mmadi_boleng.두바이트(); String mokgwa_go_tsenya_tshedimošo_leina = 문자(mmadi_boleng.두바이트()), 서술 = 문자(mmadi_boleng.두바이트());
                결과.add(new setho_data(fihlelela_go_tsenya_tshedimošo, mokgwa_go_tsenya_tshedimošo_leina, 서술, 속성읽기(mmadi_boleng)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Phetolelo_phošo("TIRO_boleng 서술 Phošo: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Phetolelo_phošo("TIRO_boleng 서술 Phošo: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Phetolelo_phošo("TIRO_boleng 서술 Phošo: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String kgetho_boleng = null;
            for (String fomete_boleng : 허용형식) if (서술.startsWith(fomete_boleng, 위치)) { kgetho_boleng = fomete_boleng; break; }
            if (kgetho_boleng == null) throw new Phetolelo_phošo("지원하지 않는 mohuta_wa_data: " + 서술);
            결과.add(kgetho_boleng); 위치 += kgetho_boleng.length();
        }
        return 결과;
    }
    static String leswao(String 종류, String... 부분들) {
        try {
            byte[] haše_faele = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Sengwalwa = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Sengwalwa.append(String.format(Locale.ROOT, "%02x", haše_faele[순번] & 255));
            return Sengwalwa.toString();
        } catch (Exception Phošo) { throw new Phetolelo_phošo(Phošo.toString()); }
    }
    final Map<String, legoro_data> 클래스들 = new TreeMap<>();
    final Map<mokgwa_Dipadišo, setho_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, motšhene_legoro;
    final int 동적기억낱말수;
    final Path mothopo_tsela;
    기계어미리번역(List<Path> tsela_Lenaneo, String nepo, int 낱말수, Path mothopo_boleng) throws IOException {
        if ((!nepo.equals("kernel") && !nepo.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Phetolelo_phošo("phethagatša_taelo nepo 또는 memori_boleng 공간 Bogolo Phošo");
        실행대상 = nepo; 동적기억낱말수 = 낱말수; mothopo_tsela = mothopo_boleng;
        // 이 이름도 국가별 mohlodi_mohlare 생성 시 해당 언어로 옮긴다.
        motšhene_legoro = nepo.equals("kernel") ? "보드" : "mošomiši";
        for (String mothaladi : Files.readAllLines(mothopo_boleng.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = mothaladi.split("\t", -1);
            if (부분들.length != 4) throw new Phetolelo_phošo("motšhene TIRO_boleng data Phošo");
            if (부분들[0].equals(nepo)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Tsejana : tsela_Lenaneo) {
            legoro_data data = new legoro_data(Tsejana);
            if (클래스들.put(data.Leina, data) != null) throw new Phetolelo_phošo("중복 legoro_boleng_55654bf1: " + data.Leina);
            for (setho_data lefelwana_boleng : data.lefelwana_boleng) {
                if ((lefelwana_boleng.fihlelela_go_tsenya_tshedimošo & 8) == 0 || 형식읽기(lefelwana_boleng.서술).equals(Collections.singletonList("V"))) throw new Phetolelo_phošo("ya_go_se_fetoge_boleng_f430d3f5 필드만 Thekgo_boleng");
                if (필드들.put(new mokgwa_Dipadišo(data.Leina, lefelwana_boleng.Leina, lefelwana_boleng.서술), lefelwana_boleng) != null) throw new Phetolelo_phošo("중복 lefelwana_boleng");
            }
            for (setho_data TIRO_boleng : data.TIRO_boleng) {
                if (TIRO_boleng.Leina.equals("<init>")) continue;
                if ((TIRO_boleng.fihlelela_go_tsenya_tshedimošo & 8) == 0 || (TIRO_boleng.fihlelela_go_tsenya_tshedimošo & (0x20 | 0x400)) != 0) throw new Phetolelo_phošo("ya_go_se_fetoge_boleng_f430d3f5 비동기화 함수만 Thekgo_boleng");
                new 함수형식(TIRO_boleng.서술);
                if (함수들.put(new mokgwa_Dipadišo(data.Leina, TIRO_boleng.Leina, TIRO_boleng.서술), TIRO_boleng) != null) throw new Phetolelo_phošo("중복 TIRO_boleng");
            }
        }
    }
    String molokoloko_leswao(String Sengwalwa) { return 문자열들.computeIfAbsent(Sengwalwa, boleng -> "j_text_" + 문자열들.size()); }
    String ya_go_se_fetoge_tlhagišo(legoro_data data, int lokela) {
        if (lokela < 1 || lokela >= data.상수종류.length) throw new Phetolelo_phošo("ya_go_se_fetoge_boleng lokela setsopolwa Phošo");
        if (data.상수종류[lokela] == 3) return "(word)(uint32_t)(" + data.ya_go_se_fetoge_data[lokela] + ")";
        if (data.상수종류[lokela] == 8) return "(word)" + molokoloko_leswao(data.문자((Integer)data.ya_go_se_fetoge_data[lokela]));
        throw new Phetolelo_phošo("정수와 molokoloko_boleng 상수만 Thekgo_boleng");
    }
    String 함수원형(mokgwa_Dipadišo Dipadišo) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Dipadišo.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + leswao("method", Dipadišo.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void lekola_kgauswi(int lokela, int 지역변수수) { if (lokela < 0 || lokela >= 지역변수수) throw new Phetolelo_phošo("kgauswi_skoupo 변수 lokela setsopolwa Phošo"); }
    void 분기넣기(List<String> 출력, Set<Integer> lekala_Lenaneo, int 위치, int 이동량, String seemo) {
        int boyo_boleng = 위치 + 이동량; lekala_Lenaneo.add(boyo_boleng);
        출력.add((seemo == null ? "" : "if (" + seemo + ") ") + "goto b" + boyo_boleng + ";");
    }
    String 함수본문(mokgwa_Dipadišo TIRO_boleng, setho_data data) {
        byte[] 본문자료 = data.tlhaodi_ya_faele_boleng.get("Code"); if (본문자료 == null) throw new Phetolelo_phošo("TIRO_boleng 몸체가 없음: " + TIRO_boleng.Leina);
        data_mmadi mmadi_boleng = new data_mmadi(본문자료); int 쌓임깊이 = mmadi_boleng.두바이트(), 지역변수수 = mmadi_boleng.두바이트();
        data_mmadi taelo_data = new data_mmadi(mmadi_boleng.Bala(mmadi_boleng.네바이트()));
        if (mmadi_boleng.두바이트() != 0) throw new Phetolelo_phošo("try/catch/finally 미지원");
        함수형식 fomete_boleng = new 함수형식(TIRO_boleng.서술); if (지역변수수 < fomete_boleng.인수.size()) throw new Phetolelo_phošo("매개변수보다 적은 kgauswi_skoupo 변수");
        legoro_data legoro_boleng_55654bf1 = 클래스들.get(TIRO_boleng.mong_boleng);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(TIRO_boleng) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < fomete_boleng.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), lekala_Lenaneo = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (taelo_data.위치 < taelo_data.data.length) {
            int 위치 = taelo_data.위치, Taelo = taelo_data.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (Taelo == 0) continue;
            if (Taelo == 1) 출력.add("PUSH(0);");
            else if (Taelo >= 2 && Taelo <= 8) 출력.add("PUSH((uint32_t)(" + (Taelo - 3) + "));");
            else if (Taelo == 16 || Taelo == 17) 출력.add("PUSH((uint32_t)(" + (Taelo == 16 ? taelo_data.부호한바이트() : taelo_data.부호두바이트()) + "));");
            else if (Taelo == 18 || Taelo == 19) 출력.add("PUSH(" + ya_go_se_fetoge_tlhagišo(legoro_boleng_55654bf1, Taelo == 18 ? taelo_data.한바이트() : taelo_data.두바이트()) + ");");
            else if (Taelo == 21 || Taelo == 25 || (Taelo >= 26 && Taelo <= 29) || (Taelo >= 42 && Taelo <= 45)) {
                int lokela = Taelo == 21 || Taelo == 25 ? taelo_data.한바이트() : Taelo - (Taelo <= 29 ? 26 : 42);
                lekola_kgauswi(lokela, 지역변수수); 출력.add("PUSH(l[" + lokela + "]);");
            } else if (Taelo == 54 || Taelo == 58 || (Taelo >= 59 && Taelo <= 62) || (Taelo >= 75 && Taelo <= 78)) {
                int lokela = Taelo == 54 || Taelo == 58 ? taelo_data.한바이트() : Taelo - (Taelo <= 62 ? 59 : 75);
                lekola_kgauswi(lokela, 지역변수수); 출력.add("l[" + lokela + "] = POP();");
            } else if (Taelo == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Taelo == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Taelo == 87 || Taelo == 88) 출력.add(Taelo == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Taelo >= 89 && Taelo <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] thulaganyo_Lenaneo = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Taelo - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char boleng : thulaganyo_Lenaneo[Taelo - 89].toCharArray()) 출력.add("PUSH(" + boleng + ");");
            } else if (Taelo == 96 || Taelo == 100 || Taelo == 104 || Taelo == 126 || Taelo == 128 || Taelo == 130) {
                String tiro_boleng = Taelo == 96 ? "+" : Taelo == 100 ? "-" : Taelo == 104 ? "*" : Taelo == 126 ? "&" : Taelo == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + tiro_boleng + " (uint32_t)b);");
            } else if (Taelo == 108 || Taelo == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Taelo == 112 ? 1 : 0) + "));");
            else if (Taelo == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Taelo == 120 || Taelo == 122 || Taelo == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Taelo == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Taelo == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Taelo == 132) {
                int lokela = taelo_data.한바이트(), 증가량 = taelo_data.부호한바이트(); lekola_kgauswi(lokela, 지역변수수);
                출력.add("l[" + lokela + "] = (uint32_t)l[" + lokela + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Taelo >= 145 && Taelo <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Taelo == 145 ? "int8_t" : Taelo == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Taelo >= 153 && Taelo <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, lekala_Lenaneo, 위치, taelo_data.부호두바이트(), "(int32_t)a " + 비교들[Taelo - 153] + " 0");
            } else if (Taelo >= 159 && Taelo <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, lekala_Lenaneo, 위치, taelo_data.부호두바이트(), Taelo >= 165 ? "a " + 비교들[Taelo - 159] + " b" : "(int32_t)a " + 비교들[Taelo - 159] + " (int32_t)b");
            } else if (Taelo == 167 || Taelo == 200) 분기넣기(출력, lekala_Lenaneo, 위치, Taelo == 167 ? taelo_data.부호두바이트() : taelo_data.네바이트(), null);
            else if (Taelo == 170 || Taelo == 171) {
                while (taelo_data.위치 % 4 != 0) taelo_data.한바이트();
                int setsenywa_sa_tirelwa = taelo_data.네바이트(); 출력.add("a = POP();");
                if (Taelo == 170) {
                    int 아래 = taelo_data.네바이트(), 위 = taelo_data.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (taelo_data.data.length - taelo_data.위치) / 4) throw new Phetolelo_phošo("switch setsopolwa Phošo");
                    for (long boleng = 아래; boleng <= 위; boleng++) 분기넣기(출력, lekala_Lenaneo, 위치, taelo_data.네바이트(), "(int32_t)a == (" + boleng + ")");
                } else {
                    int 개수 = taelo_data.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (taelo_data.data.length - taelo_data.위치) / 8) throw new Phetolelo_phošo("switch Bogolo Phošo");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int boleng = taelo_data.네바이트(); if (순번 > 0 && boleng <= 앞값) throw new Phetolelo_phošo("switch thulaganyo_boleng Phošo"); 앞값 = boleng;
                        분기넣기(출력, lekala_Lenaneo, 위치, taelo_data.네바이트(), "(int32_t)a == (" + boleng + ")");
                    }
                }
                분기넣기(출력, lekala_Lenaneo, 위치, setsenywa_sa_tirelwa, null);
            } else if (Taelo == 172 || Taelo == 176 || Taelo == 177) 출력.add("return " + (Taelo == 177 ? "0" : "POP()") + ";");
            else if (Taelo == 178 || Taelo == 179) {
                mokgwa_Dipadišo Dipadišo = legoro_boleng_55654bf1.Dipadišo(taelo_data.두바이트()); if (!필드들.containsKey(Dipadišo)) throw new Phetolelo_phošo("알 수 없는 lefelwana_boleng");
                출력.add(leswao("init", Dipadišo.mong_boleng) + "();"); String lefelwana_boleng = leswao("field", Dipadišo.부분들());
                출력.add(Taelo == 178 ? "PUSH(" + lefelwana_boleng + ");" : lefelwana_boleng + " = POP();");
            } else if (Taelo == 184) {
                mokgwa_Dipadišo Dipadišo = legoro_boleng_55654bf1.Dipadišo(taelo_data.두바이트()); if (!함수들.containsKey(Dipadišo)) throw new Phetolelo_phošo("알 수 없는 TIRO_boleng");
                함수형식 호출형식 = new 함수형식(Dipadišo.서술); int 개수 = 호출형식.인수.size();
                출력.add(leswao("init", Dipadišo.mong_boleng) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + leswao("method", Dipadišo.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Taelo == 182) {
                mokgwa_Dipadišo Dipadišo = legoro_boleng_55654bf1.Dipadišo(taelo_data.두바이트());
                if (Dipadišo.equals(new mokgwa_Dipadišo("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Dipadišo.equals(new mokgwa_Dipadišo("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Phetolelo_phošo("가상 TIRO_boleng 호출 미지원");
            } else if (Taelo == 188) {
                if (taelo_data.한바이트() != 10) throw new Phetolelo_phošo("new int[]만 Thekgo_boleng"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Taelo == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Taelo == 196) {
                int koketšo_boleng = taelo_data.한바이트(), lokela = taelo_data.두바이트(); lekola_kgauswi(lokela, 지역변수수);
                if (koketšo_boleng == 21 || koketšo_boleng == 25) 출력.add("PUSH(l[" + lokela + "]);");
                else if (koketšo_boleng == 54 || koketšo_boleng == 58) 출력.add("l[" + lokela + "] = POP();");
                else if (koketšo_boleng == 132) 출력.add("l[" + lokela + "] = (uint32_t)l[" + lokela + "] + (uint32_t)(" + taelo_data.부호두바이트() + ");");
                else throw new Phetolelo_phošo("미지원 wide Taelo");
            } else if (Taelo == 198 || Taelo == 199) {
                출력.add("a = POP();"); 분기넣기(출력, lekala_Lenaneo, 위치, taelo_data.부호두바이트(), "a " + (Taelo == 198 ? "==" : "!=") + " 0");
            } else throw new Phetolelo_phošo(TIRO_boleng.mong_boleng + "." + TIRO_boleng.Leina + ", paete_boleng " + 위치 + ": 미지원 Taelo " + Taelo);
        }
        if (!경계들.containsAll(lekala_Lenaneo)) throw new Phetolelo_phošo("Taelo 경계가 아닌 곳으로 lekala");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String Iša_mokgwa(String linke_leswao, String nepo, boolean 진입점여부) {
        int 자리 = nepo.lastIndexOf('.'); if (자리 < 0 || !linke_leswao.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Phetolelo_phošo("내보내기 abela_boleng Phošo");
        String mong_boleng = nepo.substring(0, 자리).replace('.', '/'), Leina = nepo.substring(자리 + 1); mokgwa_Dipadišo kgetho_boleng = null;
        for (mokgwa_Dipadišo Dipadišo : 함수들.keySet()) if (Dipadišo.mong_boleng.equals(mong_boleng) && Dipadišo.Leina.equals(Leina)) {
            if (kgetho_boleng != null) throw new Phetolelo_phošo("겹친 내보내기 nepo"); kgetho_boleng = Dipadišo;
        }
        if (kgetho_boleng == null || (함수들.get(kgetho_boleng).fihlelela_go_tsenya_tshedimošo & 0x100) != 0) throw new Phetolelo_phošo("내보낼 함수가 없음 또는 native TIRO_boleng");
        함수형식 fomete_boleng = new 함수형식(kgetho_boleng.서술);
        if ((진입점여부 && !fomete_boleng.인수.isEmpty()) || !Arrays.asList("V", "I").contains(fomete_boleng.반환)) throw new Phetolelo_phošo("go_tsenya_tshedimošo_ntlha_boleng 또는 C 경계 fomete_boleng Phošo");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < fomete_boleng.인수.size(); 순번++) {
            if (!fomete_boleng.인수.get(순번).equals("I")) throw new Phetolelo_phošo("C 경계는 int 인수만 Thekgo_boleng");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (fomete_boleng.반환.equals("V") ? "void " : "int32_t ") + linke_leswao + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + leswao("init", kgetho_boleng.mong_boleng) + "(); " + (fomete_boleng.반환.equals("V") ? "" : "return (int32_t)") + leswao("method", kgetho_boleng.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String go_tsenya_tshedimošo_ntlha, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<mokgwa_Dipadišo, setho_data> go_tsenya_tshedimošo_boleng : 함수들.entrySet()) {
            mokgwa_Dipadišo Dipadišo = go_tsenya_tshedimošo_boleng.getKey(); setho_data data = go_tsenya_tshedimošo_boleng.getValue(); 선언들.add(함수원형(Dipadišo) + ";");
            if ((data.fihlelela_go_tsenya_tshedimošo & 0x100) != 0) {
                String Ikgokaganye = 기계함수들.get(Dipadišo.Leina + Dipadišo.서술);
                if (!Dipadišo.mong_boleng.equals(motšhene_legoro) || Ikgokaganye == null) throw new Phetolelo_phošo("허용되지 않은 native TIRO_boleng: " + Dipadišo.Leina);
                int 개수 = new 함수형식(Dipadišo.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Ikgokaganye + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Dipadišo) + " { return " + Ikgokaganye + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Dipadišo, data));
        }
        for (Map.Entry<mokgwa_Dipadišo, setho_data> go_tsenya_tshedimošo_boleng : 필드들.entrySet()) {
            mokgwa_Dipadišo Dipadišo = go_tsenya_tshedimošo_boleng.getKey(); byte[] ya_go_se_fetoge_boleng = go_tsenya_tshedimošo_boleng.getValue().tlhaodi_ya_faele_boleng.get("ConstantValue");
            String boleng = ya_go_se_fetoge_boleng == null ? "0" : ya_go_se_fetoge_tlhagišo(클래스들.get(Dipadišo.mong_boleng), new data_mmadi(ya_go_se_fetoge_boleng).두바이트());
            필드선언들.add("static word " + leswao("field", Dipadišo.부분들()) + " = " + boleng + ";");
        }
        for (String Leina : 클래스들.keySet()) {
            String thomiša = leswao("init", Leina), boemo_boleng = leswao("state", Leina);
            선언들.add("static void " + thomiša + "(void);"); 필드선언들.add("static unsigned " + boemo_boleng + ";");
            mokgwa_Dipadišo Dipadišo = new mokgwa_Dipadišo(Leina, "<clinit>", "()V");
            몸체들.add("static void " + thomiša + "(void) { if(" + boemo_boleng + ") return; " + boemo_boleng + " = 1; " + (함수들.containsKey(Dipadišo) ? leswao("method", Dipadišo.부분들()) + "(); " : "") + boemo_boleng + " = 2; }");
        }
        몸체들.add(Iša_mokgwa("java_entry", go_tsenya_tshedimošo_ntlha, true)); Set<String> 공개이름 = new HashSet<>();
        for (String abela_boleng : 내보내기목록) {
            int 자리 = abela_boleng.indexOf('='); if (자리 < 1) throw new Phetolelo_phošo("내보내기 abela_boleng Phošo");
            String Leina = abela_boleng.substring(0, 자리); 공개이름.add(Leina); 몸체들.add(Iša_mokgwa(Leina, abela_boleng.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> go_tsenya_tshedimošo_boleng : 문자열들.entrySet()) {
            String Sengwalwa = go_tsenya_tshedimošo_boleng.getKey(); StringBuilder arei_boleng = new StringBuilder("static const word " + go_tsenya_tshedimošo_boleng.getValue() + "[] = {" + Sengwalwa.length());
            for (int 순번 = 0; 순번 < Sengwalwa.length(); 순번++) arei_boleng.append(", ").append((int)Sengwalwa.charAt(순번));
            문자열선언들.add(arei_boleng.append("};").toString());
        }
        String Thekgo_boleng = Files.readString(mothopo_tsela.resolve("lebakanako_la_polelotlwaelwa_Thekgo.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Thekgo_boleng + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String mohlodi, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> leina_tafola = new HashMap<>();
        for (String mothaladi : Files.readAllLines(mothopo_tsela.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] phera_boleng = mothaladi.split("\t"); leina_tafola.put(phera_boleng[0], phera_boleng[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(mohlodi); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Leina = 찾개.group(), 새이름 = Leina;
            if (!Leina.startsWith("//") && !Leina.startsWith("/*") && !Leina.startsWith("\"") && !Leina.startsWith("'") && !공개이름.contains(Leina)) {
                새이름 = leina_tafola.getOrDefault(Leina, Leina);
                if (Leina.matches("a[0-9]+")) 새이름 = "인수" + Leina.substring(1);
                if (Leina.matches("b[0-9]+")) 새이름 = "lekala" + Leina.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char tlhaka_boleng : 새이름.toCharArray()) 표기.append(tlhaka_boleng < 128 ? Character.toString(tlhaka_boleng) : String.format(Locale.ROOT, "\\u%04x", (int)tlhaka_boleng));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(mokgwa_Dipadišo TIRO_boleng, setho_data data, Map<String,String> motšhene_tafola, String nepo) {
        String 표식 = leswao("method", TIRO_boleng.부분들());
        List<String> mothaladi = new ArrayList<>();
        if ((data.fihlelela_go_tsenya_tshedimošo & 0x100) != 0) {
            String Ikgokaganye = motšhene_tafola.get(TIRO_boleng.Leina + TIRO_boleng.서술);
            if (!TIRO_boleng.mong_boleng.equals(nepo.equals("kernel") ? "sedirišwa_boleng" : "mošomiši") || Ikgokaganye == null) throw new Phetolelo_phošo("허용되지 않은 native TIRO_boleng");
            return ".text\n" + 표식 + ":\njmp " + Ikgokaganye;
        }
        byte[] mmele_wa_sengwalwa = data.tlhaodi_ya_faele_boleng.get("Code"); if (mmele_wa_sengwalwa == null) throw new Phetolelo_phošo("TIRO_boleng 몸체가 없음");
        data_mmadi mmadi_boleng = new data_mmadi(mmele_wa_sengwalwa); mmadi_boleng.두바이트(); int 지역수 = mmadi_boleng.두바이트();
        data_mmadi taelo_data = new data_mmadi(mmadi_boleng.Bala(mmadi_boleng.네바이트()));
        if (mmadi_boleng.두바이트() != 0) throw new Phetolelo_phošo("try/catch/finally 미지원");
        함수형식 fomete_boleng = new 함수형식(TIRO_boleng.서술); if (지역수 < fomete_boleng.인수.size()) throw new Phetolelo_phošo("매개변수보다 적은 kgauswi_skoupo 변수");
        Collections.addAll(mothaladi,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < fomete_boleng.인수.size(); 순번++) Collections.addAll(mothaladi,"movl " + (8 + 4 * (fomete_boleng.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        legoro_data legoro_boleng_55654bf1 = 클래스들.get(TIRO_boleng.mong_boleng); Set<Integer> 경계들 = new HashSet<>(), lekala_Lenaneo = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (taelo_data.위치 < taelo_data.data.length) {
            int 위치 = taelo_data.위치, Taelo = taelo_data.한바이트(); String 자리 = 표식 + "_b" + 위치;
            mothaladi.add(자리 + ":"); 경계들.add(위치);
            if (Taelo == 0) mothaladi.add("nop");
            else if (Taelo == 1) mothaladi.add("pushl $0");
            else if (Taelo >= 2 && Taelo <= 8) mothaladi.add("pushl $" + (Taelo - 3));
            else if (Taelo == 16 || Taelo == 17) mothaladi.add("pushl $" + (Taelo == 16 ? taelo_data.부호한바이트() : taelo_data.부호두바이트()));
            else if (Taelo == 18 || Taelo == 19) {
                int lokela = Taelo == 18 ? taelo_data.한바이트() : taelo_data.두바이트();
                mothaladi.add("pushl $" + 엑스상수(legoro_boleng_55654bf1,lokela));
            } else if (Taelo == 21 || Taelo == 25 || (Taelo >= 26 && Taelo <= 29) || (Taelo >= 42 && Taelo <= 45) || Taelo == 54 || Taelo == 58 || (Taelo >= 59 && Taelo <= 62) || (Taelo >= 75 && Taelo <= 78)) {
                boolean 읽음 = Taelo < 54; int lokela = Taelo == 21 || Taelo == 25 || Taelo == 54 || Taelo == 58 ? taelo_data.한바이트() : Taelo - (Taelo <= 29 ? 26 : Taelo <= 45 ? 42 : Taelo <= 62 ? 59 : 75);
                lekola_kgauswi(lokela,지역수); mothaladi.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (lokela + 1)) + "(%ebp)");
            } else if (Taelo == 46) Collections.addAll(mothaladi,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Taelo == 79) Collections.addAll(mothaladi,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Taelo == 87 || Taelo == 88) mothaladi.add("addl $" + (Taelo == 87 ? 4 : 8) + ", %esp");
            else if (Taelo >= 89 && Taelo <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] thulaganyo_Lenaneo = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Taelo - 89]; 순번++) mothaladi.add("popl " + 저장기들[순번]);
                for (int 순번 : thulaganyo_Lenaneo[Taelo - 89]) mothaladi.add("pushl " + 저장기들[순번]);
            } else if (Taelo == 96 || Taelo == 100 || Taelo == 104 || Taelo == 126 || Taelo == 128 || Taelo == 130) {
                String tiro_boleng = Taelo == 96 ? "addl" : Taelo == 100 ? "subl" : Taelo == 104 ? "imull" : Taelo == 126 ? "andl" : Taelo == 128 ? "orl" : "xorl";
                Collections.addAll(mothaladi,"popl %ecx","popl %eax",tiro_boleng + " %ecx, %eax","pushl %eax");
            } else if (Taelo == 108 || Taelo == 112) Collections.addAll(mothaladi,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Taelo == 108 ? "%eax" : "%edx"));
            else if (Taelo == 116) mothaladi.add("negl (%esp)");
            else if (Taelo == 120 || Taelo == 122 || Taelo == 124) Collections.addAll(mothaladi,"popl %ecx","popl %eax",(Taelo == 120 ? "sall" : Taelo == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Taelo == 132) {
                int lokela = taelo_data.한바이트(), 증가 = taelo_data.부호한바이트(); lekola_kgauswi(lokela,지역수); mothaladi.add("addl $" + 증가 + ", -" + (4 * (lokela + 1)) + "(%ebp)");
            } else if (Taelo >= 145 && Taelo <= 147) Collections.addAll(mothaladi,"popl %eax",Taelo == 145 ? "movsbl %al, %eax" : Taelo == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Taelo >= 153 && Taelo <= 166) {
                if (Taelo <= 158) Collections.addAll(mothaladi,"popl %eax","testl %eax, %eax");
                else Collections.addAll(mothaladi,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int boyo_boleng = 위치 + taelo_data.부호두바이트(); lekala_Lenaneo.add(boyo_boleng); mothaladi.add(비교들[Taelo - (Taelo <= 158 ? 153 : 159)] + " " + 표식 + "_b" + boyo_boleng);
            } else if (Taelo == 167 || Taelo == 200) {
                int boyo_boleng = 위치 + (Taelo == 167 ? taelo_data.부호두바이트() : taelo_data.네바이트()); lekala_Lenaneo.add(boyo_boleng); mothaladi.add("jmp " + 표식 + "_b" + boyo_boleng);
            } else if (Taelo == 170 || Taelo == 171) {
                while (taelo_data.위치 % 4 != 0) taelo_data.한바이트();
                int setsenywa_sa_tirelwa = 위치 + taelo_data.네바이트(); lekala_Lenaneo.add(setsenywa_sa_tirelwa); mothaladi.add("popl %eax");
                int 개수, 아래 = 0;
                if (Taelo == 170) { 아래 = taelo_data.네바이트(); int 위 = taelo_data.네바이트(); long botelele_boleng = (long)위 - 아래 + 1; if (botelele_boleng < 1 || botelele_boleng > (taelo_data.data.length - taelo_data.위치) / 4) throw new Phetolelo_phošo("switch setsopolwa Phošo"); 개수 = (int)botelele_boleng; }
                else { 개수 = taelo_data.네바이트(); if (개수 < 0 || 개수 > (taelo_data.data.length - taelo_data.위치) / 8) throw new Phetolelo_phošo("switch Bogolo Phošo"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int boleng = Taelo == 170 ? 아래 + 순번 : taelo_data.네바이트(), boyo_boleng = 위치 + taelo_data.네바이트(); lekala_Lenaneo.add(boyo_boleng);
                    Collections.addAll(mothaladi,"cmpl $" + boleng + ", %eax","je " + 표식 + "_b" + boyo_boleng);
                }
                mothaladi.add("jmp " + 표식 + "_b" + setsenywa_sa_tirelwa);
            } else if (Taelo == 172 || Taelo == 176 || Taelo == 177) {
                if (Taelo != 177) mothaladi.add("popl %eax"); Collections.addAll(mothaladi,"leave","ret");
            } else if (Taelo == 178 || Taelo == 179) {
                mokgwa_Dipadišo Dipadišo = legoro_boleng_55654bf1.Dipadišo(taelo_data.두바이트()); if (!필드들.containsKey(Dipadišo)) throw new Phetolelo_phošo("알 수 없는 lefelwana_boleng");
                Collections.addAll(mothaladi,"call " + leswao("init",Dipadišo.mong_boleng),(Taelo == 178 ? "pushl " : "popl ") + leswao("field",Dipadišo.부분들()));
            } else if (Taelo == 184) {
                mokgwa_Dipadišo Dipadišo = legoro_boleng_55654bf1.Dipadišo(taelo_data.두바이트()); if (!함수들.containsKey(Dipadišo)) throw new Phetolelo_phošo("알 수 없는 TIRO_boleng");
                함수형식 호출형식 = new 함수형식(Dipadišo.서술); Collections.addAll(mothaladi,"call " + leswao("init",Dipadišo.mong_boleng),"call " + leswao("method",Dipadišo.부분들()));
                if (!호출형식.인수.isEmpty()) mothaladi.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) mothaladi.add("pushl %eax");
            } else if (Taelo == 182) {
                mokgwa_Dipadišo Dipadišo = legoro_boleng_55654bf1.Dipadišo(taelo_data.두바이트());
                if (Dipadišo.equals(new mokgwa_Dipadišo("java/lang/String","length","()I"))) Collections.addAll(mothaladi,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Dipadišo.equals(new mokgwa_Dipadišo("java/lang/String","charAt","(I)C"))) Collections.addAll(mothaladi,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Phetolelo_phošo("가상 TIRO_boleng 호출 미지원");
            } else if (Taelo == 188) {
                if (taelo_data.한바이트() != 10) throw new Phetolelo_phošo("new int[]만 Thekgo_boleng"); Collections.addAll(mothaladi,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Taelo == 190) Collections.addAll(mothaladi,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Taelo == 196) {
                int koketšo_boleng = taelo_data.한바이트(), lokela = taelo_data.두바이트(); lekola_kgauswi(lokela,지역수);
                if (koketšo_boleng == 21 || koketšo_boleng == 25 || koketšo_boleng == 54 || koketšo_boleng == 58) mothaladi.add((koketšo_boleng <= 25 ? "pushl " : "popl ") + "-" + 4 * (lokela + 1) + "(%ebp)");
                else if (koketšo_boleng == 132) mothaladi.add("addl $" + taelo_data.부호두바이트() + ", -" + 4 * (lokela + 1) + "(%ebp)");
                else throw new Phetolelo_phošo("wide Taelo 미지원");
            } else if (Taelo == 198 || Taelo == 199) {
                int boyo_boleng = 위치 + taelo_data.부호두바이트(); lekala_Lenaneo.add(boyo_boleng); Collections.addAll(mothaladi,"popl %eax","testl %eax, %eax",(Taelo == 198 ? "je " : "jne ") + 표식 + "_b" + boyo_boleng);
            } else throw new Phetolelo_phošo("미지원 Taelo: " + Taelo);
        }
        if (!경계들.containsAll(lekala_Lenaneo)) throw new Phetolelo_phošo("Taelo 경계가 아닌 곳으로 lekala");
        mothaladi.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",mothaladi);
    }
    String 엑스상수(legoro_data data, int lokela) {
        if (data.상수종류[lokela] == 3) return data.ya_go_se_fetoge_data[lokela].toString();
        if (data.상수종류[lokela] == 8) return molokoloko_leswao(data.문자((Integer)data.ya_go_se_fetoge_data[lokela]));
        throw new Phetolelo_phošo("정수와 molokoloko_boleng 상수만 Thekgo_boleng");
    }
    String 엑스조립본(String go_tsenya_tshedimošo_ntlha, List<String> 내보냄, String nepo) throws IOException {
        Map<String,String> motšhene_tafola = new HashMap<>();
        for (String mothaladi : Files.readAllLines(mothopo_tsela.resolve("엑스기계함수.tsv"))) { String[] phera_boleng = mothaladi.split("\t"); if (phera_boleng[0].equals(nepo)) motšhene_tafola.put(phera_boleng[1] + phera_boleng[2],phera_boleng[3]); }
        int 자리 = go_tsenya_tshedimošo_ntlha.lastIndexOf('.'); if (자리 < 0) throw new Phetolelo_phošo("go_tsenya_tshedimošo_ntlha abela_boleng Phošo");
        String mong_boleng = go_tsenya_tshedimošo_ntlha.substring(0,자리).replace('.','/'), mokgwa_go_tsenya_tshedimošo_leina = go_tsenya_tshedimošo_ntlha.substring(자리 + 1); mokgwa_Dipadišo go_tsenya_tshedimošo_ntlha_boleng = null;
        for (String 서술 : Arrays.asList("()I","()V")) { mokgwa_Dipadišo Dipadišo = new mokgwa_Dipadišo(mong_boleng,mokgwa_go_tsenya_tshedimošo_leina,서술); if (함수들.containsKey(Dipadišo)) { if (go_tsenya_tshedimošo_ntlha_boleng != null) throw new Phetolelo_phošo("겹친 go_tsenya_tshedimošo_ntlha"); go_tsenya_tshedimošo_ntlha_boleng = Dipadišo; } }
        if (go_tsenya_tshedimošo_ntlha_boleng == null || (함수들.get(go_tsenya_tshedimošo_ntlha_boleng).fihlelela_go_tsenya_tshedimošo & 0x100) != 0) throw new Phetolelo_phošo("go_tsenya_tshedimošo_ntlha_boleng TIRO_boleng fomete_boleng Phošo");
        List<String> mothaladi = new ArrayList<>(); mothaladi.add(".code32");
        for (legoro_data data : 클래스들.values()) {
            String boemo_boleng = leswao("state",data.Leina), thomiša = leswao("init",data.Leina);
            Collections.addAll(mothaladi,".bss",".balign 4",boemo_boleng + ": .long 0",".text",thomiša + ":","cmpl $0, " + boemo_boleng,"jne " + thomiša + "_done","movl $1, " + boemo_boleng);
            mokgwa_Dipadišo 초기화참조 = new mokgwa_Dipadišo(data.Leina,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) mothaladi.add("call " + leswao("method",초기화참조.부분들()));
            Collections.addAll(mothaladi,"movl $2, " + boemo_boleng,thomiša + "_done:","ret");
            for (setho_data lefelwana_boleng : data.lefelwana_boleng) {
                byte[] ya_go_se_fetoge_boleng = lefelwana_boleng.tlhaodi_ya_faele_boleng.get("ConstantValue"); String boleng = ya_go_se_fetoge_boleng == null ? "0" : 엑스상수(data,new data_mmadi(ya_go_se_fetoge_boleng).두바이트());
                Collections.addAll(mothaladi,".data",".balign 4",leswao("field",data.Leina,lefelwana_boleng.Leina,lefelwana_boleng.서술) + ": .long " + boleng);
            }
            for (setho_data TIRO_boleng : data.TIRO_boleng) if (!TIRO_boleng.Leina.equals("<init>")) mothaladi.add(엑스함수본문(new mokgwa_Dipadišo(data.Leina,TIRO_boleng.Leina,TIRO_boleng.서술),TIRO_boleng,motšhene_tafola,nepo));
        }
        Collections.addAll(mothaladi,".text",".globl java_entry","java_entry:","call " + leswao("init",go_tsenya_tshedimošo_ntlha_boleng.mong_boleng),"call " + leswao("method",go_tsenya_tshedimošo_ntlha_boleng.부분들()));
        if (go_tsenya_tshedimošo_ntlha_boleng.서술.equals("()V")) mothaladi.add("xorl %eax, %eax"); mothaladi.add("ret");
        for (String abela_boleng : 내보냄) {
            int searoganyi_boleng_d8ba4873 = abela_boleng.indexOf('='); if (searoganyi_boleng_d8ba4873 < 1) throw new Phetolelo_phošo("내보내기 abela_boleng Phošo");
            String 외부 = abela_boleng.substring(0,searoganyi_boleng_d8ba4873), TIRO_boleng = abela_boleng.substring(searoganyi_boleng_d8ba4873 + 1); int 나눔 = TIRO_boleng.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Phetolelo_phošo("내보내기 leswao Phošo");
            String legoro_boleng_55654bf1 = TIRO_boleng.substring(0,나눔).replace('.','/'), Leina = TIRO_boleng.substring(나눔 + 1); mokgwa_Dipadišo kgetho_boleng = null;
            for (mokgwa_Dipadišo Dipadišo : 함수들.keySet()) if (Dipadišo.mong_boleng.equals(legoro_boleng_55654bf1) && Dipadišo.Leina.equals(Leina)) { if (kgetho_boleng != null) throw new Phetolelo_phošo("겹친 내보내기 nepo"); kgetho_boleng = Dipadišo; }
            if (kgetho_boleng == null) throw new Phetolelo_phošo("내보낼 함수가 없음");
            Collections.addAll(mothaladi,".text",".globl " + 외부,외부 + ":","call " + leswao("init",kgetho_boleng.mong_boleng),"jmp " + leswao("method",kgetho_boleng.부분들()));
        }
        mothaladi.add(".section .rodata");
        for (Map.Entry<String,String> go_tsenya_tshedimošo_boleng : 문자열들.entrySet()) {
            Collections.addAll(mothaladi,".balign 4",go_tsenya_tshedimošo_boleng.getValue() + ":",".long " + go_tsenya_tshedimošo_boleng.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char thutišo_boleng : go_tsenya_tshedimošo_boleng.getKey().toCharArray()) 단위들.add(Integer.toString(thutišo_boleng)); if (!단위들.isEmpty()) mothaladi.add(".long " + String.join(",",단위들));
        }
        mothaladi.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",mothaladi) + "\n";
    }
    static void phethagatša_tholosi(List<String> Taelo) throws Exception {
        if (new ProcessBuilder(Taelo).inheritIO().start().waitFor() != 0) throw new Phetolelo_phošo("aga_mohlodi Phošo: " + Taelo.get(0));
    }
    static String data_molokoloko(String Sengwalwa) { return "\"" + Sengwalwa.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String nepo, String go_tsenya_tshedimošo_ntlha, List<String> 내보냄, Path 출력, Path mothopo_boleng) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), legoro_tsela = 임시.resolve("classes"); Files.createDirectory(legoro_tsela);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",legoro_tsela.toString(),"-sourcepath",legoro_tsela.toString(),"-d",legoro_tsela.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Phetolelo_phošo("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Phetolelo_phošo(".java 또는 .class만 Thekgo_boleng");
            }
            if (원문수 > 0) phethagatša_tholosi(자바명령);
            try (java.util.stream.Stream<Path> tsela_Lenaneo = Files.walk(legoro_tsela)) { tsela_Lenaneo.filter(Tsejana -> Tsejana.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,nepo.equals("user") ? "user" : "kernel",262144,mothopo_boleng);
            String 조립 = 변환.엑스조립본(go_tsenya_tshedimošo_ntlha,내보냄,nepo); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = mothopo_boleng.getParent();
            phethagatša_tholosi(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            phethagatša_tholosi(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("lebakanako_la_polelotlwaelwa_Thekgo.s").toString()));
            List<String> Ikgokaganye = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (nepo.equals("kernel")) Ikgokaganye.add("-r");
            else {
                phethagatša_tholosi(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(nepo.equals("user") ? "Thomišo_mošomiši_tirišo.s" : "리눅스시작.s").toString()));
                Collections.addAll(Ikgokaganye,"-e","_start",임시.resolve("start.o").toString());
                if (nepo.equals("user")) Collections.addAll(Ikgokaganye,"-T",도구위치.resolve("mošomiši_linke_Sebopego.ld").toString());
            }
            Collections.addAll(Ikgokaganye,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); phethagatša_tholosi(Ikgokaganye);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path tšweletša_boleng = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),tšweletša_boleng,StandardCopyOption.REPLACE_EXISTING); Files.move(tšweletša_boleng,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(tšweletša_boleng); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(nepo.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> leswao_data = new ArrayList<>(), data_ya_mothopo = new ArrayList<>();
            for (mokgwa_Dipadišo Dipadišo : 변환.함수들.keySet()) leswao_data.add(data_molokoloko(leswao("method",Dipadišo.부분들())) + ":" + data_molokoloko(Dipadišo.mong_boleng + "." + Dipadišo.Leina + Dipadišo.서술));
            for (Path 입력 : 입력들) {
                byte[] haše_faele = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Sengwalwa = new StringBuilder(); for (byte boleng : haše_faele) Sengwalwa.append(String.format(Locale.ROOT,"%02x",boleng & 255));
                data_ya_mothopo.add(data_molokoloko(입력.toAbsolutePath().toString()) + ":" + data_molokoloko(Sengwalwa.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + data_molokoloko(nepo) + ",\"entry\":" + data_molokoloko(go_tsenya_tshedimošo_ntlha) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",leswao_data) + "},\"sources\":{" + String.join(",",data_ya_mothopo) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> tsela_Lenaneo = Files.walk(임시)) { for (Path Tsejana : (Iterable<Path>)tsela_Lenaneo.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Tsejana); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String go_tsenya_tshedimošo_ntlha = null, nepo = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> tsela_Lenaneo = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String boleng = 인수[순번];
                switch (boleng) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry legoro_boleng_55654bf1.TIRO_boleng -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export leswao=legoro_boleng_55654bf1.TIRO_boleng] 클래스파일 또는 Java원문"); return;
                    case "--entry": go_tsenya_tshedimošo_ntlha = 인수[++순번]; break;
                    case "--profile": nepo = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (boleng.startsWith("-")) throw new Phetolelo_phošo("알 수 없는 옵션: " + boleng); tsela_Lenaneo.add(Paths.get(boleng));
                }
            }
            if (go_tsenya_tshedimošo_ntlha == null || 출력경로 == null || tsela_Lenaneo.isEmpty()) throw new Phetolelo_phošo("--entry, -o, legoro_boleng_55654bf1 파일이 필요합니다");
            Path mothopo_boleng = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Phetolelo_phošo("알 수 없는 phethagatša_taelo nepo");
                엑스번역(tsela_Lenaneo,엑스대상,go_tsenya_tshedimošo_ntlha,내보냄,출력경로,mothopo_boleng); return;
            }
            String mohlodi = new 기계어미리번역(tsela_Lenaneo, nepo, 낱말수, mothopo_boleng).생성(go_tsenya_tshedimošo_ntlha, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, mohlodi, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Phošo) { System.err.println("aga_mohlodi Phošo: " + Phošo.getMessage()); System.exit(1); }
    }
}
