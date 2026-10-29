// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java klasë_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. pritës JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Përkthimi_gabim extends RuntimeException {
        Përkthimi_gabim(String 설명) { super(설명); }
    }
    static final class të_dhëna_lexues {
        final byte[] të_dhëna;
        int Pozicioni;
        të_dhëna_lexues(byte[] 입력자료) { të_dhëna = 입력자료; }
        byte[] Leximi(int gjatësi_VALUE) {
            if (gjatësi_VALUE < 0 || gjatësi_VALUE > të_dhëna.length - Pozicioni) throw new Përkthimi_gabim("잘린 klasë_VALUE 또는 Komanda të_dhëna");
            byte[] llogaritje = Arrays.copyOfRange(të_dhëna, Pozicioni, Pozicioni + gjatësi_VALUE); Pozicioni += gjatësi_VALUE; return llogaritje;
        }
        int 한바이트() { if (Pozicioni >= të_dhëna.length) throw new Përkthimi_gabim("잘린 Komanda të_dhëna"); return të_dhëna[Pozicioni++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class anëtar_të_dhëna {
        final int qasem_futje;
        final String Emër, 서술;
        final Map<String, byte[]> atribut_VALUE;
        anëtar_të_dhëna(int qasem_VALUE, String emër_VALUE, String 서술값, Map<String, byte[]> atribut_të_dhëna) {
            qasem_futje = qasem_VALUE; Emër = emër_VALUE; 서술 = 서술값; atribut_VALUE = atribut_të_dhëna;
        }
    }
    static final class metoda_Referencë implements Comparable<metoda_Referencë> {
        final String pronari_VALUE, Emër, 서술;
        metoda_Referencë(String 소유값, String emër_VALUE, String 서술값) { pronari_VALUE = 소유값; Emër = emër_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{pronari_VALUE, Emër, 서술}; }
        public int compareTo(metoda_Referencë homolog_VALUE) {
            int Krahasim_VALUE = pronari_VALUE.compareTo(homolog_VALUE.pronari_VALUE);
            if (Krahasim_VALUE == 0) Krahasim_VALUE = Emër.compareTo(homolog_VALUE.Emër);
            return Krahasim_VALUE == 0 ? 서술.compareTo(homolog_VALUE.서술) : Krahasim_VALUE;
        }
        public boolean equals(Object homolog_VALUE) { return homolog_VALUE instanceof metoda_Referencë && compareTo((metoda_Referencë) homolog_VALUE) == 0; }
        public int hashCode() { return Objects.hash(pronari_VALUE, Emër, 서술); }
    }
    static final class klasë_të_dhëna {
        final int[] 상수종류;
        final Object[] konstante_të_dhëna;
        final String Emër;
        final List<anëtar_të_dhëna> fushë_VALUE, FUNCTION_VALUE;
        klasë_të_dhëna(Path POZICIONI) throws IOException {
            të_dhëna_lexues lexues_VALUE = new të_dhëna_lexues(Files.readAllBytes(POZICIONI));
            if (lexues_VALUE.네바이트() != 0xcafebabe) throw new Përkthimi_gabim("Java klasë_VALUE 표식이 아님");
            lexues_VALUE.Leximi(4);
            int njësi_COUNT = lexues_VALUE.두바이트(); 상수종류 = new int[njësi_COUNT]; konstante_të_dhëna = new Object[njësi_COUNT];
            for (int 순번 = 1; 순번 < njësi_COUNT; 순번++) {
                int 종류 = lexues_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int gjatësi_VALUE = lexues_VALUE.두바이트();
                        byte[] karakter_ndërmemorie = lexues_VALUE.Leximi(gjatësi_VALUE), 길이붙인자료 = new byte[gjatësi_VALUE + 2];
                        길이붙인자료[0] = (byte)(gjatësi_VALUE >> 8); 길이붙인자료[1] = (byte)gjatësi_VALUE;
                        System.arraycopy(karakter_ndërmemorie, 0, 길이붙인자료, 2, gjatësi_VALUE);
                        konstante_të_dhëna[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstante_të_dhëna[순번] = lexues_VALUE.네바이트(); break;
                    case 4: lexues_VALUE.Leximi(4); break;
                    case 5: case 6: lexues_VALUE.Leximi(8); 순번++; break;
                    case 7: case 8: case 16: konstante_të_dhëna[순번] = lexues_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstante_të_dhëna[순번] = new int[]{lexues_VALUE.두바이트(), lexues_VALUE.두바이트()}; break;
                    case 15: konstante_të_dhëna[순번] = new int[]{lexues_VALUE.한바이트(), lexues_VALUE.두바이트()}; break;
                    default: throw new Përkthimi_gabim("지원하지 않는 konstante_VALUE 종류: " + 종류);
                }
            }
            lexues_VALUE.두바이트(); Emër = klasë_emër(lexues_VALUE.두바이트());
            if (!klasë_emër(lexues_VALUE.두바이트()).equals("java/lang/Object") || lexues_VALUE.두바이트() != 0)
                throw new Përkthimi_gabim(Emër + ": 상속 및 인터페이스 미지원");
            fushë_VALUE = 멤버읽기(lexues_VALUE); FUNCTION_VALUE = 멤버읽기(lexues_VALUE); 속성읽기(lexues_VALUE);
            if (lexues_VALUE.Pozicioni != lexues_VALUE.të_dhëna.length) throw new Përkthimi_gabim("klasë_VALUE 뒤에 남은 të_dhëna");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Përkthimi_gabim("문자 konstante_VALUE INDEX GABIM");
            return (String) konstante_të_dhëna[INDEX];
        }
        String klasë_emër(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Përkthimi_gabim("klasë_VALUE Referencë GABIM");
            return 문자((Integer)konstante_të_dhëna[INDEX]);
        }
        metoda_Referencë Referencë(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Përkthimi_gabim("멤버 Referencë GABIM");
            int[] çifto_VALUE = (int[])konstante_të_dhëna[INDEX], emër_çifto = (int[])konstante_të_dhëna[çifto_VALUE[1]];
            return new metoda_Referencë(klasë_emër(çifto_VALUE[0]), 문자(emër_çifto[0]), 문자(emër_çifto[1]));
        }
        Map<String, byte[]> 속성읽기(të_dhëna_lexues lexues_VALUE) {
            Map<String, byte[]> llogaritje = new LinkedHashMap<>();
            int njësi_COUNT = lexues_VALUE.두바이트();
            for (int 순번 = 0; 순번 < njësi_COUNT; 순번++) {
                String atribut_emër = 문자(lexues_VALUE.두바이트()); byte[] VALUE = lexues_VALUE.Leximi(lexues_VALUE.네바이트());
                if (llogaritje.put(atribut_emër, VALUE) != null) throw new Përkthimi_gabim("겹친 atribut_VALUE: " + atribut_emër);
            }
            return llogaritje;
        }
        List<anëtar_të_dhëna> 멤버읽기(të_dhëna_lexues lexues_VALUE) {
            List<anëtar_të_dhëna> llogaritje = new ArrayList<>(); int njësi_COUNT = lexues_VALUE.두바이트();
            for (int 순번 = 0; 순번 < njësi_COUNT; 순번++) {
                int qasem_futje = lexues_VALUE.두바이트(); String metoda_futje_emër = 문자(lexues_VALUE.두바이트()), 서술 = 문자(lexues_VALUE.두바이트());
                llogaritje.add(new anëtar_të_dhëna(qasem_futje, metoda_futje_emër, 서술, 속성읽기(lexues_VALUE)));
            }
            return llogaritje;
        }
    }
    static final class 함수형식 {
        final List<String> Argumente = new ArrayList<>();
        final String Kthe_llogaritje;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Përkthimi_gabim("FUNCTION_VALUE 서술 GABIM: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Përkthimi_gabim("FUNCTION_VALUE 서술 GABIM: " + 서술);
            Argumente.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumente.contains("V") || 반환들.size() != 1) throw new Përkthimi_gabim("FUNCTION_VALUE 서술 GABIM: " + 서술);
            Kthe_llogaritje = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> llogaritje = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Pozicioni = 0; Pozicioni < 서술.length();) {
            String përzgjedhje_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, Pozicioni)) { përzgjedhje_VALUE = format_VALUE; break; }
            if (përzgjedhje_VALUE == null) throw new Përkthimi_gabim("지원하지 않는 tipi_i_të_dhënave: " + 서술);
            llogaritje.add(përzgjedhje_VALUE); Pozicioni += përzgjedhje_VALUE.length();
        }
        return llogaritje;
    }
    static String simbol(String 종류, String... 부분들) {
        try {
            byte[] hash_skedar = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Teksti = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Teksti.append(String.format(Locale.ROOT, "%02x", hash_skedar[순번] & 255));
            return Teksti.toString();
        } catch (Exception GABIM) { throw new Përkthimi_gabim(GABIM.toString()); }
    }
    final Map<String, klasë_të_dhëna> 클래스들 = new TreeMap<>();
    final Map<metoda_Referencë, anëtar_të_dhëna> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, makinë_klasë;
    final int 동적기억낱말수;
    final Path burim_shteg;
    기계어미리번역(List<Path> shteg_Listë, String objektiv, int 낱말수, Path burim_VALUE) throws IOException {
        if ((!objektiv.equals("kernel") && !objektiv.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Përkthimi_gabim("zbatoj_komandë objektiv 또는 Memorie_VALUE 공간 Madhësi GABIM");
        실행대상 = objektiv; 동적기억낱말수 = 낱말수; burim_shteg = burim_VALUE;
        // 이 이름도 국가별 burim_degëzim gjeneroj 시 해당 언어로 옮긴다.
        makinë_klasë = objektiv.equals("kernel") ? "panel" : "përdorues";
        for (String linjë : Files.readAllLines(burim_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = linjë.split("\t", -1);
            if (부분들.length != 4) throw new Përkthimi_gabim("makinë FUNCTION_VALUE të_dhëna GABIM");
            if (부분들[0].equals(objektiv)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path POZICIONI : shteg_Listë) {
            klasë_të_dhëna të_dhëna = new klasë_të_dhëna(POZICIONI);
            if (클래스들.put(të_dhëna.Emër, të_dhëna) != null) throw new Përkthimi_gabim("중복 klasë_VALUE: " + të_dhëna.Emër);
            for (anëtar_të_dhëna fushë_VALUE : të_dhëna.fushë_VALUE) {
                if ((fushë_VALUE.qasem_futje & 8) == 0 || 형식읽기(fushë_VALUE.서술).equals(Collections.singletonList("V"))) throw new Përkthimi_gabim("statik_VALUE 필드만 Mbështetje_VALUE");
                if (필드들.put(new metoda_Referencë(të_dhëna.Emër, fushë_VALUE.Emër, fushë_VALUE.서술), fushë_VALUE) != null) throw new Përkthimi_gabim("중복 fushë_VALUE");
            }
            for (anëtar_të_dhëna FUNCTION_VALUE : të_dhëna.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Emër.equals("<init>")) continue;
                if ((FUNCTION_VALUE.qasem_futje & 8) == 0 || (FUNCTION_VALUE.qasem_futje & (0x20 | 0x400)) != 0) throw new Përkthimi_gabim("statik_VALUE 비동기화 함수만 Mbështetje_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new metoda_Referencë(të_dhëna.Emër, FUNCTION_VALUE.Emër, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Përkthimi_gabim("중복 FUNCTION_VALUE");
            }
        }
    }
    String varg_simbol(String Teksti) { return 문자열들.computeIfAbsent(Teksti, VALUE -> "j_text_" + 문자열들.size()); }
    String konstante_shprehje(klasë_të_dhëna të_dhëna, int INDEX) {
        if (INDEX < 1 || INDEX >= të_dhëna.상수종류.length) throw new Përkthimi_gabim("konstante_VALUE INDEX fragment GABIM");
        if (të_dhëna.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + të_dhëna.konstante_të_dhëna[INDEX] + ")";
        if (të_dhëna.상수종류[INDEX] == 8) return "(word)" + varg_simbol(të_dhëna.문자((Integer)të_dhëna.konstante_të_dhëna[INDEX]));
        throw new Përkthimi_gabim("정수와 varg_VALUE 상수만 Mbështetje_VALUE");
    }
    String 함수원형(metoda_Referencë Referencë) {
        List<String> 인수들 = new ArrayList<>(); int njësi_COUNT = new 함수형식(Referencë.서술).Argumente.size();
        for (int 순번 = 0; 순번 < njësi_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbol("method", Referencë.부분들()) + "(" + (njësi_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void çek_lokal(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Përkthimi_gabim("lokal_fushë 변수 INDEX fragment GABIM"); }
    void 분기넣기(List<String> 출력, Set<Integer> degë_Listë, int Pozicioni, int 이동량, String kusht) {
        int vendmbërritje_VALUE = Pozicioni + 이동량; degë_Listë.add(vendmbërritje_VALUE);
        출력.add((kusht == null ? "" : "if (" + kusht + ") ") + "goto b" + vendmbërritje_VALUE + ";");
    }
    String metoda_trupi(metoda_Referencë FUNCTION_VALUE, anëtar_të_dhëna të_dhëna) {
        byte[] trupi_të_dhëna = të_dhëna.atribut_VALUE.get("Code"); if (trupi_të_dhëna == null) throw new Përkthimi_gabim("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Emër);
        të_dhëna_lexues lexues_VALUE = new të_dhëna_lexues(trupi_të_dhëna); int 쌓임깊이 = lexues_VALUE.두바이트(), 지역변수수 = lexues_VALUE.두바이트();
        të_dhëna_lexues komandë_të_dhëna = new të_dhëna_lexues(lexues_VALUE.Leximi(lexues_VALUE.네바이트()));
        if (lexues_VALUE.두바이트() != 0) throw new Përkthimi_gabim("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (지역변수수 < format_VALUE.Argumente.size()) throw new Përkthimi_gabim("매개변수보다 적은 lokal_fushë 변수");
        klasë_të_dhëna klasë_VALUE = 클래스들.get(FUNCTION_VALUE.pronari_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(FUNCTION_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.Argumente.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), degë_Listë = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (komandë_të_dhëna.Pozicioni < komandë_të_dhëna.të_dhëna.length) {
            int Pozicioni = komandë_të_dhëna.Pozicioni, Komanda = komandë_të_dhëna.한바이트(); 경계들.add(Pozicioni); 출력.add("b" + Pozicioni + ":;");
            if (Komanda == 0) continue;
            if (Komanda == 1) 출력.add("PUSH(0);");
            else if (Komanda >= 2 && Komanda <= 8) 출력.add("PUSH((uint32_t)(" + (Komanda - 3) + "));");
            else if (Komanda == 16 || Komanda == 17) 출력.add("PUSH((uint32_t)(" + (Komanda == 16 ? komandë_të_dhëna.부호한바이트() : komandë_të_dhëna.부호두바이트()) + "));");
            else if (Komanda == 18 || Komanda == 19) 출력.add("PUSH(" + konstante_shprehje(klasë_VALUE, Komanda == 18 ? komandë_të_dhëna.한바이트() : komandë_të_dhëna.두바이트()) + ");");
            else if (Komanda == 21 || Komanda == 25 || (Komanda >= 26 && Komanda <= 29) || (Komanda >= 42 && Komanda <= 45)) {
                int INDEX = Komanda == 21 || Komanda == 25 ? komandë_të_dhëna.한바이트() : Komanda - (Komanda <= 29 ? 26 : 42);
                çek_lokal(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (Komanda == 54 || Komanda == 58 || (Komanda >= 59 && Komanda <= 62) || (Komanda >= 75 && Komanda <= 78)) {
                int INDEX = Komanda == 54 || Komanda == 58 ? komandë_të_dhëna.한바이트() : Komanda - (Komanda <= 62 ? 59 : 75);
                çek_lokal(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (Komanda == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Komanda == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Komanda == 87 || Komanda == 88) 출력.add(Komanda == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Komanda >= 89 && Komanda <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] renditja_Listë = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Komanda - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : renditja_Listë[Komanda - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (Komanda == 96 || Komanda == 100 || Komanda == 104 || Komanda == 126 || Komanda == 128 || Komanda == 130) {
                String operim_VALUE = Komanda == 96 ? "+" : Komanda == 100 ? "-" : Komanda == 104 ? "*" : Komanda == 126 ? "&" : Komanda == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operim_VALUE + " (uint32_t)b);");
            } else if (Komanda == 108 || Komanda == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Komanda == 112 ? 1 : 0) + "));");
            else if (Komanda == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Komanda == 120 || Komanda == 122 || Komanda == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Komanda == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Komanda == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Komanda == 132) {
                int INDEX = komandë_të_dhëna.한바이트(), 증가량 = komandë_të_dhëna.부호한바이트(); çek_lokal(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Komanda >= 145 && Komanda <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Komanda == 145 ? "int8_t" : Komanda == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Komanda >= 153 && Komanda <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, degë_Listë, Pozicioni, komandë_të_dhëna.부호두바이트(), "(int32_t)a " + 비교들[Komanda - 153] + " 0");
            } else if (Komanda >= 159 && Komanda <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, degë_Listë, Pozicioni, komandë_të_dhëna.부호두바이트(), Komanda >= 165 ? "a " + 비교들[Komanda - 159] + " b" : "(int32_t)a " + 비교들[Komanda - 159] + " (int32_t)b");
            } else if (Komanda == 167 || Komanda == 200) 분기넣기(출력, degë_Listë, Pozicioni, Komanda == 167 ? komandë_të_dhëna.부호두바이트() : komandë_të_dhëna.네바이트(), null);
            else if (Komanda == 170 || Komanda == 171) {
                while (komandë_të_dhëna.Pozicioni % 4 != 0) komandë_të_dhëna.한바이트();
                int vlerë_e_parazgjedhur = komandë_të_dhëna.네바이트(); 출력.add("a = POP();");
                if (Komanda == 170) {
                    int 아래 = komandë_të_dhëna.네바이트(), 위 = komandë_të_dhëna.네바이트(); long njësi_COUNT = (long)위 - 아래 + 1;
                    if (njësi_COUNT < 1 || njësi_COUNT > (komandë_të_dhëna.të_dhëna.length - komandë_të_dhëna.Pozicioni) / 4) throw new Përkthimi_gabim("switch fragment GABIM");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, degë_Listë, Pozicioni, komandë_të_dhëna.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int njësi_COUNT = komandë_të_dhëna.네바이트(), e_përparme_të_dhëna = 0;
                    if (njësi_COUNT < 0 || njësi_COUNT > (komandë_të_dhëna.të_dhëna.length - komandë_të_dhëna.Pozicioni) / 8) throw new Përkthimi_gabim("switch Madhësi GABIM");
                    for (int 순번 = 0; 순번 < njësi_COUNT; 순번++) {
                        int VALUE = komandë_të_dhëna.네바이트(); if (순번 > 0 && VALUE <= e_përparme_të_dhëna) throw new Përkthimi_gabim("switch renditja_VALUE GABIM"); e_përparme_të_dhëna = VALUE;
                        분기넣기(출력, degë_Listë, Pozicioni, komandë_të_dhëna.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, degë_Listë, Pozicioni, vlerë_e_parazgjedhur, null);
            } else if (Komanda == 172 || Komanda == 176 || Komanda == 177) 출력.add("return " + (Komanda == 177 ? "0" : "POP()") + ";");
            else if (Komanda == 178 || Komanda == 179) {
                metoda_Referencë Referencë = klasë_VALUE.Referencë(komandë_të_dhëna.두바이트()); if (!필드들.containsKey(Referencë)) throw new Përkthimi_gabim("알 수 없는 fushë_VALUE");
                출력.add(simbol("init", Referencë.pronari_VALUE) + "();"); String fushë_VALUE = simbol("field", Referencë.부분들());
                출력.add(Komanda == 178 ? "PUSH(" + fushë_VALUE + ");" : fushë_VALUE + " = POP();");
            } else if (Komanda == 184) {
                metoda_Referencë Referencë = klasë_VALUE.Referencë(komandë_të_dhëna.두바이트()); if (!함수들.containsKey(Referencë)) throw new Përkthimi_gabim("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Referencë.서술); int njësi_COUNT = 호출형식.Argumente.size();
                출력.add(simbol("init", Referencë.pronari_VALUE) + "();"); 출력.add("if(sp < " + njësi_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + njësi_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < njësi_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + simbol("method", Referencë.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.Kthe_llogaritje.equals("V")) 출력.add("PUSH(a);");
            } else if (Komanda == 182) {
                metoda_Referencë Referencë = klasë_VALUE.Referencë(komandë_të_dhëna.두바이트());
                if (Referencë.equals(new metoda_Referencë("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Referencë.equals(new metoda_Referencë("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Përkthimi_gabim("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Komanda == 188) {
                if (komandë_të_dhëna.한바이트() != 10) throw new Përkthimi_gabim("new int[]만 Mbështetje_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Komanda == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Komanda == 196) {
                int shtesë_VALUE = komandë_të_dhëna.한바이트(), INDEX = komandë_të_dhëna.두바이트(); çek_lokal(INDEX, 지역변수수);
                if (shtesë_VALUE == 21 || shtesë_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (shtesë_VALUE == 54 || shtesë_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (shtesë_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + komandë_të_dhëna.부호두바이트() + ");");
                else throw new Përkthimi_gabim("미지원 wide Komanda");
            } else if (Komanda == 198 || Komanda == 199) {
                출력.add("a = POP();"); 분기넣기(출력, degë_Listë, Pozicioni, komandë_të_dhëna.부호두바이트(), "a " + (Komanda == 198 ? "==" : "!=") + " 0");
            } else throw new Përkthimi_gabim(FUNCTION_VALUE.pronari_VALUE + "." + FUNCTION_VALUE.Emër + ", bajt_VALUE " + Pozicioni + ": 미지원 Komanda " + Komanda);
        }
        if (!경계들.containsAll(degë_Listë)) throw new Përkthimi_gabim("Komanda 경계가 아닌 곳으로 degë");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String eksportoj_metoda(String lidh_simbol, String objektiv, boolean 진입점여부) {
        int pozicioni_INDEX = objektiv.lastIndexOf('.'); if (pozicioni_INDEX < 0 || !lidh_simbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Përkthimi_gabim("내보내기 cakto_VALUE GABIM");
        String pronari_VALUE = objektiv.substring(0, pozicioni_INDEX).replace('.', '/'), Emër = objektiv.substring(pozicioni_INDEX + 1); metoda_Referencë përzgjedhje_VALUE = null;
        for (metoda_Referencë Referencë : 함수들.keySet()) if (Referencë.pronari_VALUE.equals(pronari_VALUE) && Referencë.Emër.equals(Emër)) {
            if (përzgjedhje_VALUE != null) throw new Përkthimi_gabim("겹친 내보내기 objektiv"); përzgjedhje_VALUE = Referencë;
        }
        if (përzgjedhje_VALUE == null || (함수들.get(përzgjedhje_VALUE).qasem_futje & 0x100) != 0) throw new Përkthimi_gabim("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 format_VALUE = new 함수형식(përzgjedhje_VALUE.서술);
        if ((진입점여부 && !format_VALUE.Argumente.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.Kthe_llogaritje)) throw new Përkthimi_gabim("futje_p_VALUE 또는 C 경계 format_VALUE GABIM");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.Argumente.size(); 순번++) {
            if (!format_VALUE.Argumente.get(순번).equals("I")) throw new Përkthimi_gabim("C 경계는 int 인수만 Mbështetje_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.Kthe_llogaritje.equals("V") ? "void " : "int32_t ") + lidh_simbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbol("init", përzgjedhje_VALUE.pronari_VALUE) + "(); " + (format_VALUE.Kthe_llogaritje.equals("V") ? "" : "return (int32_t)") + simbol("method", përzgjedhje_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String gjeneroj(String futje_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metoda_Referencë, anëtar_të_dhëna> futje_VALUE : 함수들.entrySet()) {
            metoda_Referencë Referencë = futje_VALUE.getKey(); anëtar_të_dhëna të_dhëna = futje_VALUE.getValue(); 선언들.add(함수원형(Referencë) + ";");
            if ((të_dhëna.qasem_futje & 0x100) != 0) {
                String Lidhu = 기계함수들.get(Referencë.Emër + Referencë.서술);
                if (!Referencë.pronari_VALUE.equals(makinë_klasë) || Lidhu == null) throw new Përkthimi_gabim("허용되지 않은 native FUNCTION_VALUE: " + Referencë.Emër);
                int njësi_COUNT = new 함수형식(Referencë.서술).Argumente.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < njësi_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Lidhu + "(" + (njësi_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(njësi_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Referencë) + " { return " + Lidhu + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metoda_trupi(Referencë, të_dhëna));
        }
        for (Map.Entry<metoda_Referencë, anëtar_të_dhëna> futje_VALUE : 필드들.entrySet()) {
            metoda_Referencë Referencë = futje_VALUE.getKey(); byte[] konstante_VALUE = futje_VALUE.getValue().atribut_VALUE.get("ConstantValue");
            String VALUE = konstante_VALUE == null ? "0" : konstante_shprehje(클래스들.get(Referencë.pronari_VALUE), new të_dhëna_lexues(konstante_VALUE).두바이트());
            필드선언들.add("static word " + simbol("field", Referencë.부분들()) + " = " + VALUE + ";");
        }
        for (String Emër : 클래스들.keySet()) {
            String filloj = simbol("init", Emër), status_VALUE = simbol("state", Emër);
            선언들.add("static void " + filloj + "(void);"); 필드선언들.add("static unsigned " + status_VALUE + ";");
            metoda_Referencë Referencë = new metoda_Referencë(Emër, "<clinit>", "()V");
            몸체들.add("static void " + filloj + "(void) { if(" + status_VALUE + ") return; " + status_VALUE + " = 1; " + (함수들.containsKey(Referencë) ? simbol("method", Referencë.부분들()) + "(); " : "") + status_VALUE + " = 2; }");
        }
        몸체들.add(eksportoj_metoda("java_entry", futje_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String cakto_VALUE : 내보내기목록) {
            int pozicioni_INDEX = cakto_VALUE.indexOf('='); if (pozicioni_INDEX < 1) throw new Përkthimi_gabim("내보내기 cakto_VALUE GABIM");
            String Emër = cakto_VALUE.substring(0, pozicioni_INDEX); 공개이름.add(Emër); 몸체들.add(eksportoj_metoda(Emër, cakto_VALUE.substring(pozicioni_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> futje_VALUE : 문자열들.entrySet()) {
            String Teksti = futje_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + futje_VALUE.getValue() + "[] = {" + Teksti.length());
            for (int 순번 = 0; 순번 < Teksti.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Teksti.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Mbështetje_VALUE = Files.readString(burim_shteg.resolve("koha_e_ekzekutimit_të_gjuhës_së_zakonshme_Mbështetje.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Mbështetje_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String BURIMI, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> emër_tabelë = new HashMap<>();
        for (String linjë : Files.readAllLines(burim_shteg.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] çifto_VALUE = linjë.split("\t"); emër_tabelë.put(çifto_VALUE[0], çifto_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(BURIMI); StringBuffer llogaritje = new StringBuffer();
        while (찾개.find()) {
            String Emër = 찾개.group(), 새이름 = Emër;
            if (!Emër.startsWith("//") && !Emër.startsWith("/*") && !Emër.startsWith("\"") && !Emër.startsWith("'") && !공개이름.contains(Emër)) {
                새이름 = emër_tabelë.getOrDefault(Emër, Emër);
                if (Emër.matches("a[0-9]+")) 새이름 = "Argumente" + Emër.substring(1);
                if (Emër.matches("b[0-9]+")) 새이름 = "degë" + Emër.substring(1);
                if (범용표기) {
                    StringBuilder simbolet_VALUE = new StringBuilder();
                    for (char karakter_VALUE : 새이름.toCharArray()) simbolet_VALUE.append(karakter_VALUE < 128 ? Character.toString(karakter_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)karakter_VALUE));
                    새이름 = simbolet_VALUE.toString();
                }
            }
            찾개.appendReplacement(llogaritje, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(llogaritje); return llogaritje.toString();
    }
    String X_86_metoda_trupi(metoda_Referencë FUNCTION_VALUE, anëtar_të_dhëna të_dhëna, Map<String,String> makinë_tabelë, String objektiv) {
        String 표식 = simbol("method", FUNCTION_VALUE.부분들());
        List<String> linjë = new ArrayList<>();
        if ((të_dhëna.qasem_futje & 0x100) != 0) {
            String Lidhu = makinë_tabelë.get(FUNCTION_VALUE.Emër + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.pronari_VALUE.equals(objektiv.equals("kernel") ? "pajisje_VALUE" : "përdorues") || Lidhu == null) throw new Përkthimi_gabim("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Lidhu;
        }
        byte[] trupi_i_tekstit = të_dhëna.atribut_VALUE.get("Code"); if (trupi_i_tekstit == null) throw new Përkthimi_gabim("FUNCTION_VALUE 몸체가 없음");
        të_dhëna_lexues lexues_VALUE = new të_dhëna_lexues(trupi_i_tekstit); lexues_VALUE.두바이트(); int lokal_COUNT = lexues_VALUE.두바이트();
        të_dhëna_lexues komandë_të_dhëna = new të_dhëna_lexues(lexues_VALUE.Leximi(lexues_VALUE.네바이트()));
        if (lexues_VALUE.두바이트() != 0) throw new Përkthimi_gabim("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokal_COUNT < format_VALUE.Argumente.size()) throw new Përkthimi_gabim("매개변수보다 적은 lokal_fushë 변수");
        Collections.addAll(linjë,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.Argumente.size(); 순번++) Collections.addAll(linjë,"movl " + (8 + 4 * (format_VALUE.Argumente.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        klasë_të_dhëna klasë_VALUE = 클래스들.get(FUNCTION_VALUE.pronari_VALUE); Set<Integer> 경계들 = new HashSet<>(), degë_Listë = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (komandë_të_dhëna.Pozicioni < komandë_të_dhëna.të_dhëna.length) {
            int Pozicioni = komandë_të_dhëna.Pozicioni, Komanda = komandë_të_dhëna.한바이트(); String pozicioni_INDEX = 표식 + "_b" + Pozicioni;
            linjë.add(pozicioni_INDEX + ":"); 경계들.add(Pozicioni);
            if (Komanda == 0) linjë.add("nop");
            else if (Komanda == 1) linjë.add("pushl $0");
            else if (Komanda >= 2 && Komanda <= 8) linjë.add("pushl $" + (Komanda - 3));
            else if (Komanda == 16 || Komanda == 17) linjë.add("pushl $" + (Komanda == 16 ? komandë_të_dhëna.부호한바이트() : komandë_të_dhëna.부호두바이트()));
            else if (Komanda == 18 || Komanda == 19) {
                int INDEX = Komanda == 18 ? komandë_të_dhëna.한바이트() : komandë_të_dhëna.두바이트();
                linjë.add("pushl $" + X_86_konstante(klasë_VALUE,INDEX));
            } else if (Komanda == 21 || Komanda == 25 || (Komanda >= 26 && Komanda <= 29) || (Komanda >= 42 && Komanda <= 45) || Komanda == 54 || Komanda == 58 || (Komanda >= 59 && Komanda <= 62) || (Komanda >= 75 && Komanda <= 78)) {
                boolean 읽음 = Komanda < 54; int INDEX = Komanda == 21 || Komanda == 25 || Komanda == 54 || Komanda == 58 ? komandë_të_dhëna.한바이트() : Komanda - (Komanda <= 29 ? 26 : Komanda <= 45 ? 42 : Komanda <= 62 ? 59 : 75);
                çek_lokal(INDEX,lokal_COUNT); linjë.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Komanda == 46) Collections.addAll(linjë,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Komanda == 79) Collections.addAll(linjë,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Komanda == 87 || Komanda == 88) linjë.add("addl $" + (Komanda == 87 ? 4 : 8) + ", %esp");
            else if (Komanda >= 89 && Komanda <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] renditja_Listë = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Komanda - 89]; 순번++) linjë.add("popl " + 저장기들[순번]);
                for (int 순번 : renditja_Listë[Komanda - 89]) linjë.add("pushl " + 저장기들[순번]);
            } else if (Komanda == 96 || Komanda == 100 || Komanda == 104 || Komanda == 126 || Komanda == 128 || Komanda == 130) {
                String operim_VALUE = Komanda == 96 ? "addl" : Komanda == 100 ? "subl" : Komanda == 104 ? "imull" : Komanda == 126 ? "andl" : Komanda == 128 ? "orl" : "xorl";
                Collections.addAll(linjë,"popl %ecx","popl %eax",operim_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Komanda == 108 || Komanda == 112) Collections.addAll(linjë,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + pozicioni_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + pozicioni_INDEX + "_divide","xorl %edx, %edx","jmp " + pozicioni_INDEX + "_done",pozicioni_INDEX + "_divide:","cltd","idivl %ecx",pozicioni_INDEX + "_done:","pushl " + (Komanda == 108 ? "%eax" : "%edx"));
            else if (Komanda == 116) linjë.add("negl (%esp)");
            else if (Komanda == 120 || Komanda == 122 || Komanda == 124) Collections.addAll(linjë,"popl %ecx","popl %eax",(Komanda == 120 ? "sall" : Komanda == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Komanda == 132) {
                int INDEX = komandë_të_dhëna.한바이트(), 증가 = komandë_të_dhëna.부호한바이트(); çek_lokal(INDEX,lokal_COUNT); linjë.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Komanda >= 145 && Komanda <= 147) Collections.addAll(linjë,"popl %eax",Komanda == 145 ? "movsbl %al, %eax" : Komanda == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Komanda >= 153 && Komanda <= 166) {
                if (Komanda <= 158) Collections.addAll(linjë,"popl %eax","testl %eax, %eax");
                else Collections.addAll(linjë,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int vendmbërritje_VALUE = Pozicioni + komandë_të_dhëna.부호두바이트(); degë_Listë.add(vendmbërritje_VALUE); linjë.add(비교들[Komanda - (Komanda <= 158 ? 153 : 159)] + " " + 표식 + "_b" + vendmbërritje_VALUE);
            } else if (Komanda == 167 || Komanda == 200) {
                int vendmbërritje_VALUE = Pozicioni + (Komanda == 167 ? komandë_të_dhëna.부호두바이트() : komandë_të_dhëna.네바이트()); degë_Listë.add(vendmbërritje_VALUE); linjë.add("jmp " + 표식 + "_b" + vendmbërritje_VALUE);
            } else if (Komanda == 170 || Komanda == 171) {
                while (komandë_të_dhëna.Pozicioni % 4 != 0) komandë_të_dhëna.한바이트();
                int vlerë_e_parazgjedhur = Pozicioni + komandë_të_dhëna.네바이트(); degë_Listë.add(vlerë_e_parazgjedhur); linjë.add("popl %eax");
                int njësi_COUNT, 아래 = 0;
                if (Komanda == 170) { 아래 = komandë_të_dhëna.네바이트(); int 위 = komandë_të_dhëna.네바이트(); long gjatësi_VALUE = (long)위 - 아래 + 1; if (gjatësi_VALUE < 1 || gjatësi_VALUE > (komandë_të_dhëna.të_dhëna.length - komandë_të_dhëna.Pozicioni) / 4) throw new Përkthimi_gabim("switch fragment GABIM"); njësi_COUNT = (int)gjatësi_VALUE; }
                else { njësi_COUNT = komandë_të_dhëna.네바이트(); if (njësi_COUNT < 0 || njësi_COUNT > (komandë_të_dhëna.të_dhëna.length - komandë_të_dhëna.Pozicioni) / 8) throw new Përkthimi_gabim("switch Madhësi GABIM"); }
                for (int 순번 = 0; 순번 < njësi_COUNT; 순번++) {
                    int VALUE = Komanda == 170 ? 아래 + 순번 : komandë_të_dhëna.네바이트(), vendmbërritje_VALUE = Pozicioni + komandë_të_dhëna.네바이트(); degë_Listë.add(vendmbërritje_VALUE);
                    Collections.addAll(linjë,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + vendmbërritje_VALUE);
                }
                linjë.add("jmp " + 표식 + "_b" + vlerë_e_parazgjedhur);
            } else if (Komanda == 172 || Komanda == 176 || Komanda == 177) {
                if (Komanda != 177) linjë.add("popl %eax"); Collections.addAll(linjë,"leave","ret");
            } else if (Komanda == 178 || Komanda == 179) {
                metoda_Referencë Referencë = klasë_VALUE.Referencë(komandë_të_dhëna.두바이트()); if (!필드들.containsKey(Referencë)) throw new Përkthimi_gabim("알 수 없는 fushë_VALUE");
                Collections.addAll(linjë,"call " + simbol("init",Referencë.pronari_VALUE),(Komanda == 178 ? "pushl " : "popl ") + simbol("field",Referencë.부분들()));
            } else if (Komanda == 184) {
                metoda_Referencë Referencë = klasë_VALUE.Referencë(komandë_të_dhëna.두바이트()); if (!함수들.containsKey(Referencë)) throw new Përkthimi_gabim("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Referencë.서술); Collections.addAll(linjë,"call " + simbol("init",Referencë.pronari_VALUE),"call " + simbol("method",Referencë.부분들()));
                if (!호출형식.Argumente.isEmpty()) linjë.add("addl $" + 호출형식.Argumente.size() * 4 + ", %esp");
                if (!호출형식.Kthe_llogaritje.equals("V")) linjë.add("pushl %eax");
            } else if (Komanda == 182) {
                metoda_Referencë Referencë = klasë_VALUE.Referencë(komandë_të_dhëna.두바이트());
                if (Referencë.equals(new metoda_Referencë("java/lang/String","length","()I"))) Collections.addAll(linjë,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Referencë.equals(new metoda_Referencë("java/lang/String","charAt","(I)C"))) Collections.addAll(linjë,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Përkthimi_gabim("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Komanda == 188) {
                if (komandë_të_dhëna.한바이트() != 10) throw new Përkthimi_gabim("new int[]만 Mbështetje_VALUE"); Collections.addAll(linjë,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Komanda == 190) Collections.addAll(linjë,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Komanda == 196) {
                int shtesë_VALUE = komandë_të_dhëna.한바이트(), INDEX = komandë_të_dhëna.두바이트(); çek_lokal(INDEX,lokal_COUNT);
                if (shtesë_VALUE == 21 || shtesë_VALUE == 25 || shtesë_VALUE == 54 || shtesë_VALUE == 58) linjë.add((shtesë_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (shtesë_VALUE == 132) linjë.add("addl $" + komandë_të_dhëna.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Përkthimi_gabim("wide Komanda 미지원");
            } else if (Komanda == 198 || Komanda == 199) {
                int vendmbërritje_VALUE = Pozicioni + komandë_të_dhëna.부호두바이트(); degë_Listë.add(vendmbërritje_VALUE); Collections.addAll(linjë,"popl %eax","testl %eax, %eax",(Komanda == 198 ? "je " : "jne ") + 표식 + "_b" + vendmbërritje_VALUE);
            } else throw new Përkthimi_gabim("미지원 Komanda: " + Komanda);
        }
        if (!경계들.containsAll(degë_Listë)) throw new Përkthimi_gabim("Komanda 경계가 아닌 곳으로 degë");
        linjë.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",linjë);
    }
    String X_86_konstante(klasë_të_dhëna të_dhëna, int INDEX) {
        if (të_dhëna.상수종류[INDEX] == 3) return të_dhëna.konstante_të_dhëna[INDEX].toString();
        if (të_dhëna.상수종류[INDEX] == 8) return varg_simbol(të_dhëna.문자((Integer)të_dhëna.konstante_të_dhëna[INDEX]));
        throw new Përkthimi_gabim("정수와 varg_VALUE 상수만 Mbështetje_VALUE");
    }
    String 엑스조립본(String futje_p, List<String> 내보냄, String objektiv) throws IOException {
        Map<String,String> makinë_tabelë = new HashMap<>();
        for (String linjë : Files.readAllLines(burim_shteg.resolve("엑스기계함수.tsv"))) { String[] çifto_VALUE = linjë.split("\t"); if (çifto_VALUE[0].equals(objektiv)) makinë_tabelë.put(çifto_VALUE[1] + çifto_VALUE[2],çifto_VALUE[3]); }
        int pozicioni_INDEX = futje_p.lastIndexOf('.'); if (pozicioni_INDEX < 0) throw new Përkthimi_gabim("futje_p cakto_VALUE GABIM");
        String pronari_VALUE = futje_p.substring(0,pozicioni_INDEX).replace('.','/'), metoda_futje_emër = futje_p.substring(pozicioni_INDEX + 1); metoda_Referencë futje_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metoda_Referencë Referencë = new metoda_Referencë(pronari_VALUE,metoda_futje_emër,서술); if (함수들.containsKey(Referencë)) { if (futje_p_VALUE != null) throw new Përkthimi_gabim("겹친 futje_p"); futje_p_VALUE = Referencë; } }
        if (futje_p_VALUE == null || (함수들.get(futje_p_VALUE).qasem_futje & 0x100) != 0) throw new Përkthimi_gabim("futje_p_VALUE FUNCTION_VALUE format_VALUE GABIM");
        List<String> linjë = new ArrayList<>(); linjë.add(".code32");
        for (klasë_të_dhëna të_dhëna : 클래스들.values()) {
            String status_VALUE = simbol("state",të_dhëna.Emër), filloj = simbol("init",të_dhëna.Emër);
            Collections.addAll(linjë,".bss",".balign 4",status_VALUE + ": .long 0",".text",filloj + ":","cmpl $0, " + status_VALUE,"jne " + filloj + "_done","movl $1, " + status_VALUE);
            metoda_Referencë 초기화참조 = new metoda_Referencë(të_dhëna.Emër,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) linjë.add("call " + simbol("method",초기화참조.부분들()));
            Collections.addAll(linjë,"movl $2, " + status_VALUE,filloj + "_done:","ret");
            for (anëtar_të_dhëna fushë_VALUE : të_dhëna.fushë_VALUE) {
                byte[] konstante_VALUE = fushë_VALUE.atribut_VALUE.get("ConstantValue"); String VALUE = konstante_VALUE == null ? "0" : X_86_konstante(të_dhëna,new të_dhëna_lexues(konstante_VALUE).두바이트());
                Collections.addAll(linjë,".data",".balign 4",simbol("field",të_dhëna.Emër,fushë_VALUE.Emër,fushë_VALUE.서술) + ": .long " + VALUE);
            }
            for (anëtar_të_dhëna FUNCTION_VALUE : të_dhëna.FUNCTION_VALUE) if (!FUNCTION_VALUE.Emër.equals("<init>")) linjë.add(X_86_metoda_trupi(new metoda_Referencë(të_dhëna.Emër,FUNCTION_VALUE.Emër,FUNCTION_VALUE.서술),FUNCTION_VALUE,makinë_tabelë,objektiv));
        }
        Collections.addAll(linjë,".text",".globl java_entry","java_entry:","call " + simbol("init",futje_p_VALUE.pronari_VALUE),"call " + simbol("method",futje_p_VALUE.부분들()));
        if (futje_p_VALUE.서술.equals("()V")) linjë.add("xorl %eax, %eax"); linjë.add("ret");
        for (String cakto_VALUE : 내보냄) {
            int kufizues_VALUE = cakto_VALUE.indexOf('='); if (kufizues_VALUE < 1) throw new Përkthimi_gabim("내보내기 cakto_VALUE GABIM");
            String 외부 = cakto_VALUE.substring(0,kufizues_VALUE), FUNCTION_VALUE = cakto_VALUE.substring(kufizues_VALUE + 1); int pjesëtim_llogaritje = FUNCTION_VALUE.lastIndexOf('.');
            if (pjesëtim_llogaritje < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Përkthimi_gabim("내보내기 simbol GABIM");
            String klasë_VALUE = FUNCTION_VALUE.substring(0,pjesëtim_llogaritje).replace('.','/'), Emër = FUNCTION_VALUE.substring(pjesëtim_llogaritje + 1); metoda_Referencë përzgjedhje_VALUE = null;
            for (metoda_Referencë Referencë : 함수들.keySet()) if (Referencë.pronari_VALUE.equals(klasë_VALUE) && Referencë.Emër.equals(Emër)) { if (përzgjedhje_VALUE != null) throw new Përkthimi_gabim("겹친 내보내기 objektiv"); përzgjedhje_VALUE = Referencë; }
            if (përzgjedhje_VALUE == null) throw new Përkthimi_gabim("내보낼 함수가 없음");
            Collections.addAll(linjë,".text",".globl " + 외부,외부 + ":","call " + simbol("init",përzgjedhje_VALUE.pronari_VALUE),"jmp " + simbol("method",përzgjedhje_VALUE.부분들()));
        }
        linjë.add(".section .rodata");
        for (Map.Entry<String,String> futje_VALUE : 문자열들.entrySet()) {
            Collections.addAll(linjë,".balign 4",futje_VALUE.getValue() + ":",".long " + futje_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char mësim_VALUE : futje_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(mësim_VALUE)); if (!단위들.isEmpty()) linjë.add(".long " + String.join(",",단위들));
        }
        linjë.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",linjë) + "\n";
    }
    static void zbatoj_vegël(List<String> Komanda) throws Exception {
        if (new ProcessBuilder(Komanda).inheritIO().start().waitFor() != 0) throw new Përkthimi_gabim("ndërtoj_burim GABIM: " + Komanda.get(0));
    }
    static String të_dhëna_varg(String Teksti) { return "\"" + Teksti.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Përkthimi(List<Path> 입력들, String objektiv, String futje_p, List<String> 내보냄, Path 출력, Path burim_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), klasë_shteg = 임시.resolve("classes"); Files.createDirectory(klasë_shteg);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",klasë_shteg.toString(),"-sourcepath",klasë_shteg.toString(),"-d",klasë_shteg.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int burim_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Përkthimi_gabim("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); burim_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Përkthimi_gabim(".java 또는 .class만 Mbështetje_VALUE");
            }
            if (burim_COUNT > 0) zbatoj_vegël(자바명령);
            try (java.util.stream.Stream<Path> shteg_Listë = Files.walk(klasë_shteg)) { shteg_Listë.filter(POZICIONI -> POZICIONI.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,objektiv.equals("user") ? "user" : "kernel",262144,burim_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(futje_p,내보냄,objektiv); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path vegël_pozicioni = burim_VALUE.getParent();
            zbatoj_vegël(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            zbatoj_vegël(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),vegël_pozicioni.resolve("koha_e_ekzekutimit_të_gjuhës_së_zakonshme_Mbështetje.s").toString()));
            List<String> Lidhu = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (objektiv.equals("kernel")) Lidhu.add("-r");
            else {
                zbatoj_vegël(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),vegël_pozicioni.resolve(objektiv.equals("user") ? "nis_përdorues_program.s" : "리눅스시작.s").toString()));
                Collections.addAll(Lidhu,"-e","_start",임시.resolve("start.o").toString());
                if (objektiv.equals("user")) Collections.addAll(Lidhu,"-T",vegël_pozicioni.resolve("përdorues_lidh_Navigimi.ld").toString());
            }
            Collections.addAll(Lidhu,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); zbatoj_vegël(Lidhu);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path publikoj_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publikoj_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(publikoj_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publikoj_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(objektiv.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbol_të_dhëna = new ArrayList<>(), të_dhëna_burimore = new ArrayList<>();
            for (metoda_Referencë Referencë : CONVERT_VALUE.함수들.keySet()) simbol_të_dhëna.add(të_dhëna_varg(simbol("method",Referencë.부분들())) + ":" + të_dhëna_varg(Referencë.pronari_VALUE + "." + Referencë.Emër + Referencë.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_skedar = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Teksti = new StringBuilder(); for (byte VALUE : hash_skedar) Teksti.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                të_dhëna_burimore.add(të_dhëna_varg(입력.toAbsolutePath().toString()) + ":" + të_dhëna_varg(Teksti.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + të_dhëna_varg(objektiv) + ",\"entry\":" + të_dhëna_varg(futje_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbol_të_dhëna) + "},\"sources\":{" + String.join(",",të_dhëna_burimore) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> shteg_Listë = Files.walk(임시)) { for (Path POZICIONI : (Iterable<Path>)shteg_Listë.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(POZICIONI); }
        }
    }
    public static void main(String[] Argumente) {
        try {
            String futje_p = null, objektiv = "kernel", X_86_objektiv = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> shteg_Listë = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumente.length; 순번++) {
                String VALUE = Argumente[순번];
                switch (VALUE) {
                    case "--target": X_86_objektiv = Argumente[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry klasë_VALUE.FUNCTION_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export simbol=klasë_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": futje_p = Argumente[++순번]; break;
                    case "--profile": objektiv = Argumente[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumente[++순번]); break;
                    case "--export": 내보냄.add(Argumente[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argumente[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Përkthimi_gabim("알 수 없는 옵션: " + VALUE); shteg_Listë.add(Paths.get(VALUE));
                }
            }
            if (futje_p == null || 출력경로 == null || shteg_Listë.isEmpty()) throw new Përkthimi_gabim("--entry, -o, klasë_VALUE 파일이 필요합니다");
            Path burim_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_objektiv != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_objektiv)) throw new Përkthimi_gabim("알 수 없는 zbatoj_komandë objektiv");
                X_86_Përkthimi(shteg_Listë,X_86_objektiv,futje_p,내보냄,출력경로,burim_VALUE); return;
            }
            String BURIMI = new 기계어미리번역(shteg_Listë, objektiv, 낱말수, burim_VALUE).gjeneroj(futje_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, BURIMI, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception GABIM) { System.err.println("ndërtoj_burim GABIM: " + GABIM.getMessage()); System.exit(1); }
    }
}
