// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java klasė_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. organizuoti JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class 번역오류 extends RuntimeException {
        번역오류(String aprašas) { super(aprašas); }
    }
    static final class duomenys_Skaitytuvė {
        final byte[] duomenys;
        int Pozicija;
        duomenys_Skaitytuvė(byte[] 입력자료) { duomenys = 입력자료; }
        byte[] Skaitymas(int 길이) {
            if (길이 < 0 || 길이 > duomenys.length - Pozicija) throw new 번역오류("잘린 klasė_VALUE 또는 Komanda duomenys");
            byte[] REZULTATAS = Arrays.copyOfRange(duomenys, Pozicija, Pozicija + 길이); Pozicija += 길이; return REZULTATAS;
        }
        int 한바이트() { if (Pozicija >= duomenys.length) throw new 번역오류("잘린 Komanda duomenys"); return duomenys[Pozicija++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class narys_duomenys {
        final int prieiga_įrašas;
        final String Pavadinimas_2, aprašas_VALUE;
        final Map<String, byte[]> atributas_VALUE;
        narys_duomenys(int prieiga_VALUE, String pavadinimas_VALUE, String 서술값, Map<String, byte[]> atributas_duomenys) {
            prieiga_įrašas = prieiga_VALUE; Pavadinimas_2 = pavadinimas_VALUE; aprašas_VALUE = 서술값; atributas_VALUE = atributas_duomenys;
        }
    }
    static final class metodas_nuoroda implements Comparable<metodas_nuoroda> {
        final String savininkas_VALUE, Pavadinimas_2, aprašas_VALUE;
        metodas_nuoroda(String 소유값, String pavadinimas_VALUE, String 서술값) { savininkas_VALUE = 소유값; Pavadinimas_2 = pavadinimas_VALUE; aprašas_VALUE = 서술값; }
        String[] 부분들() { return new String[]{savininkas_VALUE, Pavadinimas_2, aprašas_VALUE}; }
        public int compareTo(metodas_nuoroda lygiavertis_mazgas_VALUE) {
            int Palyginimas_VALUE = savininkas_VALUE.compareTo(lygiavertis_mazgas_VALUE.savininkas_VALUE);
            if (Palyginimas_VALUE == 0) Palyginimas_VALUE = Pavadinimas_2.compareTo(lygiavertis_mazgas_VALUE.Pavadinimas_2);
            return Palyginimas_VALUE == 0 ? aprašas_VALUE.compareTo(lygiavertis_mazgas_VALUE.aprašas_VALUE) : Palyginimas_VALUE;
        }
        public boolean equals(Object lygiavertis_mazgas_VALUE) { return lygiavertis_mazgas_VALUE instanceof metodas_nuoroda && compareTo((metodas_nuoroda) lygiavertis_mazgas_VALUE) == 0; }
        public int hashCode() { return Objects.hash(savininkas_VALUE, Pavadinimas_2, aprašas_VALUE); }
    }
    static final class klasė_duomenys {
        final int[] 상수종류;
        final Object[] konstanta_duomenys;
        final String Pavadinimas_2;
        final List<narys_duomenys> lauko_reikšmė, FUNCTION_VALUE;
        klasė_duomenys(Path KELIAS) throws IOException {
            duomenys_Skaitytuvė Skaitytuvė_VALUE = new duomenys_Skaitytuvė(Files.readAllBytes(KELIAS));
            if (Skaitytuvė_VALUE.네바이트() != 0xcafebabe) throw new 번역오류("Java klasė_VALUE 표식이 아님");
            Skaitytuvė_VALUE.Skaitymas(4);
            int prekė_COUNT = Skaitytuvė_VALUE.두바이트(); 상수종류 = new int[prekė_COUNT]; konstanta_duomenys = new Object[prekė_COUNT];
            for (int 순번 = 1; 순번 < prekė_COUNT; 순번++) {
                int 종류 = Skaitytuvė_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int 길이 = Skaitytuvė_VALUE.두바이트();
                        byte[] simbolis_kaupti = Skaitytuvė_VALUE.Skaitymas(길이), 길이붙인자료 = new byte[길이 + 2];
                        길이붙인자료[0] = (byte)(길이 >> 8); 길이붙인자료[1] = (byte)길이;
                        System.arraycopy(simbolis_kaupti, 0, 길이붙인자료, 2, 길이);
                        konstanta_duomenys[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstanta_duomenys[순번] = Skaitytuvė_VALUE.네바이트(); break;
                    case 4: Skaitytuvė_VALUE.Skaitymas(4); break;
                    case 5: case 6: Skaitytuvė_VALUE.Skaitymas(8); 순번++; break;
                    case 7: case 8: case 16: konstanta_duomenys[순번] = Skaitytuvė_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstanta_duomenys[순번] = new int[]{Skaitytuvė_VALUE.두바이트(), Skaitytuvė_VALUE.두바이트()}; break;
                    case 15: konstanta_duomenys[순번] = new int[]{Skaitytuvė_VALUE.한바이트(), Skaitytuvė_VALUE.두바이트()}; break;
                    default: throw new 번역오류("지원하지 않는 konstanta_VALUE 종류: " + 종류);
                }
            }
            Skaitytuvė_VALUE.두바이트(); Pavadinimas_2 = klasės_pavadinimas(Skaitytuvė_VALUE.두바이트());
            if (!klasės_pavadinimas(Skaitytuvė_VALUE.두바이트()).equals("java/lang/Object") || Skaitytuvė_VALUE.두바이트() != 0)
                throw new 번역오류(Pavadinimas_2 + ": 상속 및 인터페이스 미지원");
            lauko_reikšmė = 멤버읽기(Skaitytuvė_VALUE); FUNCTION_VALUE = 멤버읽기(Skaitytuvė_VALUE); 속성읽기(Skaitytuvė_VALUE);
            if (Skaitytuvė_VALUE.Pozicija != Skaitytuvė_VALUE.duomenys.length) throw new 번역오류("klasė_VALUE 뒤에 남은 duomenys");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new 번역오류("문자 konstanta_VALUE INDEX KLAIDA");
            return (String) konstanta_duomenys[INDEX];
        }
        String klasės_pavadinimas(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new 번역오류("klasė_VALUE nuoroda KLAIDA");
            return 문자((Integer)konstanta_duomenys[INDEX]);
        }
        metodas_nuoroda nuoroda(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new 번역오류("멤버 nuoroda KLAIDA");
            int[] susieti_VALUE = (int[])konstanta_duomenys[INDEX], pavadinimas_susieti = (int[])konstanta_duomenys[susieti_VALUE[1]];
            return new metodas_nuoroda(klasės_pavadinimas(susieti_VALUE[0]), 문자(pavadinimas_susieti[0]), 문자(pavadinimas_susieti[1]));
        }
        Map<String, byte[]> 속성읽기(duomenys_Skaitytuvė Skaitytuvė_VALUE) {
            Map<String, byte[]> REZULTATAS = new LinkedHashMap<>();
            int prekė_COUNT = Skaitytuvė_VALUE.두바이트();
            for (int 순번 = 0; 순번 < prekė_COUNT; 순번++) {
                String atributas_pavadinimas = 문자(Skaitytuvė_VALUE.두바이트()); byte[] VALUE = Skaitytuvė_VALUE.Skaitymas(Skaitytuvė_VALUE.네바이트());
                if (REZULTATAS.put(atributas_pavadinimas, VALUE) != null) throw new 번역오류("겹친 atributas_VALUE: " + atributas_pavadinimas);
            }
            return REZULTATAS;
        }
        List<narys_duomenys> 멤버읽기(duomenys_Skaitytuvė Skaitytuvė_VALUE) {
            List<narys_duomenys> REZULTATAS = new ArrayList<>(); int prekė_COUNT = Skaitytuvė_VALUE.두바이트();
            for (int 순번 = 0; 순번 < prekė_COUNT; 순번++) {
                int prieiga_įrašas = Skaitytuvė_VALUE.두바이트(); String metodas_įrašas_pavadinimas = 문자(Skaitytuvė_VALUE.두바이트()), aprašas_VALUE = 문자(Skaitytuvė_VALUE.두바이트());
                REZULTATAS.add(new narys_duomenys(prieiga_įrašas, metodas_įrašas_pavadinimas, aprašas_VALUE, 속성읽기(Skaitytuvė_VALUE)));
            }
            return REZULTATAS;
        }
    }
    static final class 함수형식 {
        final List<String> Argumentai = new ArrayList<>();
        final String grąžinti_KR;
        함수형식(String aprašas_VALUE) {
            if (!aprašas_VALUE.startsWith("(")) throw new 번역오류("FUNCTION_VALUE aprašas_VALUE KLAIDA: " + aprašas_VALUE);
            int 끝 = aprašas_VALUE.indexOf(')'); if (끝 < 0) throw new 번역오류("FUNCTION_VALUE aprašas_VALUE KLAIDA: " + aprašas_VALUE);
            Argumentai.addAll(형식읽기(aprašas_VALUE.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(aprašas_VALUE.substring(끝 + 1));
            if (Argumentai.contains("V") || 반환들.size() != 1) throw new 번역오류("FUNCTION_VALUE aprašas_VALUE KLAIDA: " + aprašas_VALUE);
            grąžinti_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String aprašas_VALUE) {
        List<String> REZULTATAS = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Pozicija = 0; Pozicija < aprašas_VALUE.length();) {
            String žymėjimas_VALUE = null;
            for (String formatas_VALUE : 허용형식) if (aprašas_VALUE.startsWith(formatas_VALUE, Pozicija)) { žymėjimas_VALUE = formatas_VALUE; break; }
            if (žymėjimas_VALUE == null) throw new 번역오류("지원하지 않는 duomenų_tipas: " + aprašas_VALUE);
            REZULTATAS.add(žymėjimas_VALUE); Pozicija += žymėjimas_VALUE.length();
        }
        return REZULTATAS;
    }
    static String simbolis(String 종류, String... 부분들) {
        try {
            byte[] maiša_Failas = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Tekstas = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Tekstas.append(String.format(Locale.ROOT, "%02x", maiša_Failas[순번] & 255));
            return Tekstas.toString();
        } catch (Exception KLAIDA) { throw new 번역오류(KLAIDA.toString()); }
    }
    final Map<String, klasė_duomenys> 클래스들 = new TreeMap<>();
    final Map<metodas_nuoroda, narys_duomenys> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), mašina_Azure_funkcijos_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, mašina_klasė;
    final int 동적기억낱말수;
    final Path ištekliai_kelias;
    기계어미리번역(List<Path> kelias_Sąrašas, String tikslas, int 낱말수, Path ištekliai_VALUE) throws IOException {
        if ((!tikslas.equals("kernel") && !tikslas.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new 번역오류("Vykdyti_komanda tikslas 또는 atmintis_VALUE ADDRESS_sritis Dydis KLAIDA");
        실행대상 = tikslas; 동적기억낱말수 = 낱말수; ištekliai_kelias = ištekliai_VALUE;
        // 이 이름도 국가별 šaltinis_medis generuoti 시 해당 언어로 옮긴다.
        mašina_klasė = tikslas.equals("kernel") ? "Lenta" : "naudotojas";
        for (String Eilutė : Files.readAllLines(ištekliai_VALUE.resolve("mašina_Azure_funkcijos.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Eilutė.split("\t", -1);
            if (부분들.length != 4) throw new 번역오류("mašina FUNCTION_VALUE duomenys KLAIDA");
            if (부분들[0].equals(tikslas)) mašina_Azure_funkcijos_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path KELIAS : kelias_Sąrašas) {
            klasė_duomenys duomenys = new klasė_duomenys(KELIAS);
            if (클래스들.put(duomenys.Pavadinimas_2, duomenys) != null) throw new 번역오류("중복 klasė_VALUE: " + duomenys.Pavadinimas_2);
            for (narys_duomenys lauko_reikšmė : duomenys.lauko_reikšmė) {
                if ((lauko_reikšmė.prieiga_įrašas & 8) == 0 || 형식읽기(lauko_reikšmė.aprašas_VALUE).equals(Collections.singletonList("V"))) throw new 번역오류("정적 필드만 pagalba_VALUE");
                if (필드들.put(new metodas_nuoroda(duomenys.Pavadinimas_2, lauko_reikšmė.Pavadinimas_2, lauko_reikšmė.aprašas_VALUE), lauko_reikšmė) != null) throw new 번역오류("중복 lauko_reikšmė");
            }
            for (narys_duomenys FUNCTION_VALUE : duomenys.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Pavadinimas_2.equals("<init>")) continue;
                if ((FUNCTION_VALUE.prieiga_įrašas & 8) == 0 || (FUNCTION_VALUE.prieiga_įrašas & (0x20 | 0x400)) != 0) throw new 번역오류("정적 비동기화 함수만 pagalba_VALUE");
                new 함수형식(FUNCTION_VALUE.aprašas_VALUE);
                if (함수들.put(new metodas_nuoroda(duomenys.Pavadinimas_2, FUNCTION_VALUE.Pavadinimas_2, FUNCTION_VALUE.aprašas_VALUE), FUNCTION_VALUE) != null) throw new 번역오류("중복 FUNCTION_VALUE");
            }
        }
    }
    String eilutė_simbolis(String Tekstas) { return 문자열들.computeIfAbsent(Tekstas, VALUE -> "j_text_" + 문자열들.size()); }
    String konstanta_reiškinys(klasė_duomenys duomenys, int INDEX) {
        if (INDEX < 1 || INDEX >= duomenys.상수종류.length) throw new 번역오류("konstanta_VALUE INDEX klipas KLAIDA");
        if (duomenys.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + duomenys.konstanta_duomenys[INDEX] + ")";
        if (duomenys.상수종류[INDEX] == 8) return "(word)" + eilutė_simbolis(duomenys.문자((Integer)duomenys.konstanta_duomenys[INDEX]));
        throw new 번역오류("정수와 eilutė_VALUE 상수만 pagalba_VALUE");
    }
    String 함수원형(metodas_nuoroda nuoroda) {
        List<String> 인수들 = new ArrayList<>(); int prekė_COUNT = new 함수형식(nuoroda.aprašas_VALUE).Argumentai.size();
        for (int 순번 = 0; 순번 < prekė_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbolis("method", nuoroda.부분들()) + "(" + (prekė_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void čekis_vietinis(int INDEX, int vietinis_kintamasis_COUNT) { if (INDEX < 0 || INDEX >= vietinis_kintamasis_COUNT) throw new 번역오류("vietinis_Aprėptis kintamasis_VALUE INDEX klipas KLAIDA"); }
    void 분기넣기(List<String> Išvestis, Set<Integer> šaka_Sąrašas, int Pozicija, int 이동량, String sąlyga) {
        int vieta_VALUE = Pozicija + 이동량; šaka_Sąrašas.add(vieta_VALUE);
        Išvestis.add((sąlyga == null ? "" : "if (" + sąlyga + ") ") + "goto b" + vieta_VALUE + ";");
    }
    String metodas_pranešimo_tekstas(metodas_nuoroda FUNCTION_VALUE, narys_duomenys duomenys) {
        byte[] pranešimo_tekstas_duomenys = duomenys.atributas_VALUE.get("Code"); if (pranešimo_tekstas_duomenys == null) throw new 번역오류("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Pavadinimas_2);
        duomenys_Skaitytuvė Skaitytuvė_VALUE = new duomenys_Skaitytuvė(pranešimo_tekstas_duomenys); int 쌓임깊이 = Skaitytuvė_VALUE.두바이트(), vietinis_kintamasis_COUNT = Skaitytuvė_VALUE.두바이트();
        duomenys_Skaitytuvė komanda_duomenys = new duomenys_Skaitytuvė(Skaitytuvė_VALUE.Skaitymas(Skaitytuvė_VALUE.네바이트()));
        if (Skaitytuvė_VALUE.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 formatas_VALUE = new 함수형식(FUNCTION_VALUE.aprašas_VALUE); if (vietinis_kintamasis_COUNT < formatas_VALUE.Argumentai.size()) throw new 번역오류("매개변수보다 적은 vietinis_Aprėptis kintamasis_VALUE");
        klasė_duomenys klasė_VALUE = 클래스들.get(FUNCTION_VALUE.savininkas_VALUE);
        List<String> Išvestis = new ArrayList<>(); Išvestis.add(함수원형(FUNCTION_VALUE) + " {");
        Išvestis.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(vietinis_kintamasis_COUNT, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formatas_VALUE.Argumentai.size(); 순번++) Išvestis.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), šaka_Sąrašas = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (komanda_duomenys.Pozicija < komanda_duomenys.duomenys.length) {
            int Pozicija = komanda_duomenys.Pozicija, Komanda = komanda_duomenys.한바이트(); 경계들.add(Pozicija); Išvestis.add("b" + Pozicija + ":;");
            if (Komanda == 0) continue;
            if (Komanda == 1) Išvestis.add("PUSH(0);");
            else if (Komanda >= 2 && Komanda <= 8) Išvestis.add("PUSH((uint32_t)(" + (Komanda - 3) + "));");
            else if (Komanda == 16 || Komanda == 17) Išvestis.add("PUSH((uint32_t)(" + (Komanda == 16 ? komanda_duomenys.부호한바이트() : komanda_duomenys.부호두바이트()) + "));");
            else if (Komanda == 18 || Komanda == 19) Išvestis.add("PUSH(" + konstanta_reiškinys(klasė_VALUE, Komanda == 18 ? komanda_duomenys.한바이트() : komanda_duomenys.두바이트()) + ");");
            else if (Komanda == 21 || Komanda == 25 || (Komanda >= 26 && Komanda <= 29) || (Komanda >= 42 && Komanda <= 45)) {
                int INDEX = Komanda == 21 || Komanda == 25 ? komanda_duomenys.한바이트() : Komanda - (Komanda <= 29 ? 26 : 42);
                čekis_vietinis(INDEX, vietinis_kintamasis_COUNT); Išvestis.add("PUSH(l[" + INDEX + "]);");
            } else if (Komanda == 54 || Komanda == 58 || (Komanda >= 59 && Komanda <= 62) || (Komanda >= 75 && Komanda <= 78)) {
                int INDEX = Komanda == 54 || Komanda == 58 ? komanda_duomenys.한바이트() : Komanda - (Komanda <= 62 ? 59 : 75);
                čekis_vietinis(INDEX, vietinis_kintamasis_COUNT); Išvestis.add("l[" + INDEX + "] = POP();");
            } else if (Komanda == 46) Išvestis.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Komanda == 79) Išvestis.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Komanda == 87 || Komanda == 88) Išvestis.add(Komanda == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Komanda >= 89 && Komanda <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] tvarka_Sąrašas = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Komanda - 89]; 순번++) Išvestis.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : tvarka_Sąrašas[Komanda - 89].toCharArray()) Išvestis.add("PUSH(" + VALUE + ");");
            } else if (Komanda == 96 || Komanda == 100 || Komanda == 104 || Komanda == 126 || Komanda == 128 || Komanda == 130) {
                String operacija_VALUE = Komanda == 96 ? "+" : Komanda == 100 ? "-" : Komanda == 104 ? "*" : Komanda == 126 ? "&" : Komanda == 128 ? "|" : "^";
                Išvestis.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operacija_VALUE + " (uint32_t)b);");
            } else if (Komanda == 108 || Komanda == 112) Išvestis.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Komanda == 112 ? 1 : 0) + "));");
            else if (Komanda == 116) Išvestis.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Komanda == 120 || Komanda == 122 || Komanda == 124) {
                Išvestis.add("b = POP(); a = POP();"); Išvestis.add("PUSH(" + (Komanda == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Komanda == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Komanda == 132) {
                int INDEX = komanda_duomenys.한바이트(), padidinimas_suma = komanda_duomenys.부호한바이트(); čekis_vietinis(INDEX, vietinis_kintamasis_COUNT);
                Išvestis.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + padidinimas_suma + ");");
            } else if (Komanda >= 145 && Komanda <= 147) Išvestis.add("a = POP(); PUSH((uint32_t)(" + (Komanda == 145 ? "int8_t" : Komanda == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Komanda >= 153 && Komanda <= 158) {
                Išvestis.add("a = POP();"); 분기넣기(Išvestis, šaka_Sąrašas, Pozicija, komanda_duomenys.부호두바이트(), "(int32_t)a " + 비교들[Komanda - 153] + " 0");
            } else if (Komanda >= 159 && Komanda <= 166) {
                Išvestis.add("b = POP(); a = POP();"); 분기넣기(Išvestis, šaka_Sąrašas, Pozicija, komanda_duomenys.부호두바이트(), Komanda >= 165 ? "a " + 비교들[Komanda - 159] + " b" : "(int32_t)a " + 비교들[Komanda - 159] + " (int32_t)b");
            } else if (Komanda == 167 || Komanda == 200) 분기넣기(Išvestis, šaka_Sąrašas, Pozicija, Komanda == 167 ? komanda_duomenys.부호두바이트() : komanda_duomenys.네바이트(), null);
            else if (Komanda == 170 || Komanda == 171) {
                while (komanda_duomenys.Pozicija % 4 != 0) komanda_duomenys.한바이트();
                int numatytoji_reikšmė = komanda_duomenys.네바이트(); Išvestis.add("a = POP();");
                if (Komanda == 170) {
                    int 아래 = komanda_duomenys.네바이트(), 위 = komanda_duomenys.네바이트(); long prekė_COUNT = (long)위 - 아래 + 1;
                    if (prekė_COUNT < 1 || prekė_COUNT > (komanda_duomenys.duomenys.length - komanda_duomenys.Pozicija) / 4) throw new 번역오류("switch klipas KLAIDA");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Išvestis, šaka_Sąrašas, Pozicija, komanda_duomenys.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int prekė_COUNT = komanda_duomenys.네바이트(), priekinis_duomenys = 0;
                    if (prekė_COUNT < 0 || prekė_COUNT > (komanda_duomenys.duomenys.length - komanda_duomenys.Pozicija) / 8) throw new 번역오류("switch Dydis KLAIDA");
                    for (int 순번 = 0; 순번 < prekė_COUNT; 순번++) {
                        int VALUE = komanda_duomenys.네바이트(); if (순번 > 0 && VALUE <= priekinis_duomenys) throw new 번역오류("switch tvarka_VALUE KLAIDA"); priekinis_duomenys = VALUE;
                        분기넣기(Išvestis, šaka_Sąrašas, Pozicija, komanda_duomenys.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Išvestis, šaka_Sąrašas, Pozicija, numatytoji_reikšmė, null);
            } else if (Komanda == 172 || Komanda == 176 || Komanda == 177) Išvestis.add("return " + (Komanda == 177 ? "0" : "POP()") + ";");
            else if (Komanda == 178 || Komanda == 179) {
                metodas_nuoroda nuoroda = klasė_VALUE.nuoroda(komanda_duomenys.두바이트()); if (!필드들.containsKey(nuoroda)) throw new 번역오류("알 numeris 없는 lauko_reikšmė");
                Išvestis.add(simbolis("init", nuoroda.savininkas_VALUE) + "();"); String lauko_reikšmė = simbolis("field", nuoroda.부분들());
                Išvestis.add(Komanda == 178 ? "PUSH(" + lauko_reikšmė + ");" : lauko_reikšmė + " = POP();");
            } else if (Komanda == 184) {
                metodas_nuoroda nuoroda = klasė_VALUE.nuoroda(komanda_duomenys.두바이트()); if (!함수들.containsKey(nuoroda)) throw new 번역오류("알 numeris 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(nuoroda.aprašas_VALUE); int prekė_COUNT = 호출형식.Argumentai.size();
                Išvestis.add(simbolis("init", nuoroda.savininkas_VALUE) + "();"); Išvestis.add("if(sp < " + prekė_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + prekė_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < prekė_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Išvestis.add("a = " + simbolis("method", nuoroda.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.grąžinti_KR.equals("V")) Išvestis.add("PUSH(a);");
            } else if (Komanda == 182) {
                metodas_nuoroda nuoroda = klasė_VALUE.nuoroda(komanda_duomenys.두바이트());
                if (nuoroda.equals(new metodas_nuoroda("java/lang/String", "length", "()I"))) Išvestis.add("a = POP(); PUSH(length(a));");
                else if (nuoroda.equals(new metodas_nuoroda("java/lang/String", "charAt", "(I)C"))) Išvestis.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 번역오류("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Komanda == 188) {
                if (komanda_duomenys.한바이트() != 10) throw new 번역오류("new int[]만 pagalba_VALUE"); Išvestis.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Komanda == 190) Išvestis.add("a = POP(); PUSH(length(a));");
            else if (Komanda == 196) {
                int plėtinys_VALUE = komanda_duomenys.한바이트(), INDEX = komanda_duomenys.두바이트(); čekis_vietinis(INDEX, vietinis_kintamasis_COUNT);
                if (plėtinys_VALUE == 21 || plėtinys_VALUE == 25) Išvestis.add("PUSH(l[" + INDEX + "]);");
                else if (plėtinys_VALUE == 54 || plėtinys_VALUE == 58) Išvestis.add("l[" + INDEX + "] = POP();");
                else if (plėtinys_VALUE == 132) Išvestis.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + komanda_duomenys.부호두바이트() + ");");
                else throw new 번역오류("미지원 wide Komanda");
            } else if (Komanda == 198 || Komanda == 199) {
                Išvestis.add("a = POP();"); 분기넣기(Išvestis, šaka_Sąrašas, Pozicija, komanda_duomenys.부호두바이트(), "a " + (Komanda == 198 ? "==" : "!=") + " 0");
            } else throw new 번역오류(FUNCTION_VALUE.savininkas_VALUE + "." + FUNCTION_VALUE.Pavadinimas_2 + ", baitas_VALUE " + Pozicija + ": 미지원 Komanda " + Komanda);
        }
        if (!경계들.containsAll(šaka_Sąrašas)) throw new 번역오류("Komanda 경계가 아닌 곳으로 šaka");
        Išvestis.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Išvestis);
    }
    String eksportuoti_metodas(String sieti_simbolis, String tikslas, boolean 진입점여부) {
        int vietos_rodyklė = tikslas.lastIndexOf('.'); if (vietos_rodyklė < 0 || !sieti_simbolis.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 Priskirti_VALUE KLAIDA");
        String savininkas_VALUE = tikslas.substring(0, vietos_rodyklė).replace('.', '/'), Pavadinimas_2 = tikslas.substring(vietos_rodyklė + 1); metodas_nuoroda žymėjimas_VALUE = null;
        for (metodas_nuoroda nuoroda : 함수들.keySet()) if (nuoroda.savininkas_VALUE.equals(savininkas_VALUE) && nuoroda.Pavadinimas_2.equals(Pavadinimas_2)) {
            if (žymėjimas_VALUE != null) throw new 번역오류("겹친 내보내기 tikslas"); žymėjimas_VALUE = nuoroda;
        }
        if (žymėjimas_VALUE == null || (함수들.get(žymėjimas_VALUE).prieiga_įrašas & 0x100) != 0) throw new 번역오류("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 formatas_VALUE = new 함수형식(žymėjimas_VALUE.aprašas_VALUE);
        if ((진입점여부 && !formatas_VALUE.Argumentai.isEmpty()) || !Arrays.asList("V", "I").contains(formatas_VALUE.grąžinti_KR)) throw new 번역오류("įrašas_p_VALUE 또는 C 경계 formatas_VALUE KLAIDA");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formatas_VALUE.Argumentai.size(); 순번++) {
            if (!formatas_VALUE.Argumentai.get(순번).equals("I")) throw new 번역오류("C 경계는 int 인수만 pagalba_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formatas_VALUE.grąžinti_KR.equals("V") ? "void " : "int32_t ") + sieti_simbolis + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbolis("init", žymėjimas_VALUE.savininkas_VALUE) + "(); " + (formatas_VALUE.grąžinti_KR.equals("V") ? "" : "return (int32_t)") + simbolis("method", žymėjimas_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generuoti(String įrašas_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metodas_nuoroda, narys_duomenys> įrašas_VALUE : 함수들.entrySet()) {
            metodas_nuoroda nuoroda = įrašas_VALUE.getKey(); narys_duomenys duomenys = įrašas_VALUE.getValue(); 선언들.add(함수원형(nuoroda) + ";");
            if ((duomenys.prieiga_įrašas & 0x100) != 0) {
                String Prisijungti = mašina_Azure_funkcijos_c3a8e64a.get(nuoroda.Pavadinimas_2 + nuoroda.aprašas_VALUE);
                if (!nuoroda.savininkas_VALUE.equals(mašina_klasė) || Prisijungti == null) throw new 번역오류("허용되지 않은 native FUNCTION_VALUE: " + nuoroda.Pavadinimas_2);
                int prekė_COUNT = new 함수형식(nuoroda.aprašas_VALUE).Argumentai.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < prekė_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Prisijungti + "(" + (prekė_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(prekė_COUNT, "word"))) + ");");
                몸체들.add(함수원형(nuoroda) + " { return " + Prisijungti + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metodas_pranešimo_tekstas(nuoroda, duomenys));
        }
        for (Map.Entry<metodas_nuoroda, narys_duomenys> įrašas_VALUE : 필드들.entrySet()) {
            metodas_nuoroda nuoroda = įrašas_VALUE.getKey(); byte[] konstanta_VALUE = įrašas_VALUE.getValue().atributas_VALUE.get("ConstantValue");
            String VALUE = konstanta_VALUE == null ? "0" : konstanta_reiškinys(클래스들.get(nuoroda.savininkas_VALUE), new duomenys_Skaitytuvė(konstanta_VALUE).두바이트());
            필드선언들.add("static word " + simbolis("field", nuoroda.부분들()) + " = " + VALUE + ";");
        }
        for (String Pavadinimas_2 : 클래스들.keySet()) {
            String 초기화 = simbolis("init", Pavadinimas_2), Būsena_VALUE = simbolis("state", Pavadinimas_2);
            선언들.add("static void " + 초기화 + "(void);"); 필드선언들.add("static unsigned " + Būsena_VALUE + ";");
            metodas_nuoroda nuoroda = new metodas_nuoroda(Pavadinimas_2, "<clinit>", "()V");
            몸체들.add("static void " + 초기화 + "(void) { if(" + Būsena_VALUE + ") return; " + Būsena_VALUE + " = 1; " + (함수들.containsKey(nuoroda) ? simbolis("method", nuoroda.부분들()) + "(); " : "") + Būsena_VALUE + " = 2; }");
        }
        몸체들.add(eksportuoti_metodas("java_entry", įrašas_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Priskirti_VALUE : 내보내기목록) {
            int vietos_rodyklė = Priskirti_VALUE.indexOf('='); if (vietos_rodyklė < 1) throw new 번역오류("내보내기 Priskirti_VALUE KLAIDA");
            String Pavadinimas_2 = Priskirti_VALUE.substring(0, vietos_rodyklė); 공개이름.add(Pavadinimas_2); 몸체들.add(eksportuoti_metodas(Pavadinimas_2, Priskirti_VALUE.substring(vietos_rodyklė + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> įrašas_VALUE : 문자열들.entrySet()) {
            String Tekstas = įrašas_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + įrašas_VALUE.getValue() + "[] = {" + Tekstas.length());
            for (int 순번 = 0; 순번 < Tekstas.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Tekstas.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String pagalba_VALUE = Files.readString(ištekliai_kelias.resolve("CLR_pagalba.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(pagalba_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ŠALTINIS, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> pavadinimas_lentelė = new HashMap<>();
        for (String Eilutė : Files.readAllLines(ištekliai_kelias.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] susieti_VALUE = Eilutė.split("\t"); pavadinimas_lentelė.put(susieti_VALUE[0], susieti_VALUE[1]);
        }
        Pattern segmentas_reiškinys = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = segmentas_reiškinys.matcher(ŠALTINIS); StringBuffer REZULTATAS = new StringBuffer();
        while (찾개.find()) {
            String Pavadinimas_2 = 찾개.group(), 새이름 = Pavadinimas_2;
            if (!Pavadinimas_2.startsWith("//") && !Pavadinimas_2.startsWith("/*") && !Pavadinimas_2.startsWith("\"") && !Pavadinimas_2.startsWith("'") && !공개이름.contains(Pavadinimas_2)) {
                새이름 = pavadinimas_lentelė.getOrDefault(Pavadinimas_2, Pavadinimas_2);
                if (Pavadinimas_2.matches("a[0-9]+")) 새이름 = "Argumentai" + Pavadinimas_2.substring(1);
                if (Pavadinimas_2.matches("b[0-9]+")) 새이름 = "šaka" + Pavadinimas_2.substring(1);
                if (범용표기) {
                    StringBuilder notacija_VALUE = new StringBuilder();
                    for (char simbolis_VALUE_068c2631 : 새이름.toCharArray()) notacija_VALUE.append(simbolis_VALUE_068c2631 < 128 ? Character.toString(simbolis_VALUE_068c2631) : String.format(Locale.ROOT, "\\u%04x", (int)simbolis_VALUE_068c2631));
                    새이름 = notacija_VALUE.toString();
                }
            }
            찾개.appendReplacement(REZULTATAS, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(REZULTATAS); return REZULTATAS.toString();
    }
    String X_86_metodas_pranešimo_tekstas(metodas_nuoroda FUNCTION_VALUE, narys_duomenys duomenys, Map<String,String> mašina_lentelė, String tikslas) {
        String žymeklis_VALUE = simbolis("method", FUNCTION_VALUE.부분들());
        List<String> Eilutė = new ArrayList<>();
        if ((duomenys.prieiga_įrašas & 0x100) != 0) {
            String Prisijungti = mašina_lentelė.get(FUNCTION_VALUE.Pavadinimas_2 + FUNCTION_VALUE.aprašas_VALUE);
            if (!FUNCTION_VALUE.savininkas_VALUE.equals(tikslas.equals("kernel") ? "įrenginys_VALUE" : "naudotojas") || Prisijungti == null) throw new 번역오류("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + žymeklis_VALUE + ":\njmp " + Prisijungti;
        }
        byte[] pagrindinis_tekstas = duomenys.atributas_VALUE.get("Code"); if (pagrindinis_tekstas == null) throw new 번역오류("FUNCTION_VALUE 몸체가 없음");
        duomenys_Skaitytuvė Skaitytuvė_VALUE = new duomenys_Skaitytuvė(pagrindinis_tekstas); Skaitytuvė_VALUE.두바이트(); int vietinis_COUNT = Skaitytuvė_VALUE.두바이트();
        duomenys_Skaitytuvė komanda_duomenys = new duomenys_Skaitytuvė(Skaitytuvė_VALUE.Skaitymas(Skaitytuvė_VALUE.네바이트()));
        if (Skaitytuvė_VALUE.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 formatas_VALUE = new 함수형식(FUNCTION_VALUE.aprašas_VALUE); if (vietinis_COUNT < formatas_VALUE.Argumentai.size()) throw new 번역오류("매개변수보다 적은 vietinis_Aprėptis kintamasis_VALUE");
        Collections.addAll(Eilutė,".text",".globl " + žymeklis_VALUE,".type " + žymeklis_VALUE + ", @function",žymeklis_VALUE + ":","pushl %ebp","movl %esp, %ebp","subl $" + vietinis_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formatas_VALUE.Argumentai.size(); 순번++) Collections.addAll(Eilutė,"movl " + (8 + 4 * (formatas_VALUE.Argumentai.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        klasė_duomenys klasė_VALUE = 클래스들.get(FUNCTION_VALUE.savininkas_VALUE); Set<Integer> 경계들 = new HashSet<>(), šaka_Sąrašas = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (komanda_duomenys.Pozicija < komanda_duomenys.duomenys.length) {
            int Pozicija = komanda_duomenys.Pozicija, Komanda = komanda_duomenys.한바이트(); String vietos_rodyklė = žymeklis_VALUE + "_b" + Pozicija;
            Eilutė.add(vietos_rodyklė + ":"); 경계들.add(Pozicija);
            if (Komanda == 0) Eilutė.add("nop");
            else if (Komanda == 1) Eilutė.add("pushl $0");
            else if (Komanda >= 2 && Komanda <= 8) Eilutė.add("pushl $" + (Komanda - 3));
            else if (Komanda == 16 || Komanda == 17) Eilutė.add("pushl $" + (Komanda == 16 ? komanda_duomenys.부호한바이트() : komanda_duomenys.부호두바이트()));
            else if (Komanda == 18 || Komanda == 19) {
                int INDEX = Komanda == 18 ? komanda_duomenys.한바이트() : komanda_duomenys.두바이트();
                Eilutė.add("pushl $" + X_86_konstanta(klasė_VALUE,INDEX));
            } else if (Komanda == 21 || Komanda == 25 || (Komanda >= 26 && Komanda <= 29) || (Komanda >= 42 && Komanda <= 45) || Komanda == 54 || Komanda == 58 || (Komanda >= 59 && Komanda <= 62) || (Komanda >= 75 && Komanda <= 78)) {
                boolean 읽음 = Komanda < 54; int INDEX = Komanda == 21 || Komanda == 25 || Komanda == 54 || Komanda == 58 ? komanda_duomenys.한바이트() : Komanda - (Komanda <= 29 ? 26 : Komanda <= 45 ? 42 : Komanda <= 62 ? 59 : 75);
                čekis_vietinis(INDEX,vietinis_COUNT); Eilutė.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Komanda == 46) Collections.addAll(Eilutė,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Komanda == 79) Collections.addAll(Eilutė,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Komanda == 87 || Komanda == 88) Eilutė.add("addl $" + (Komanda == 87 ? 4 : 8) + ", %esp");
            else if (Komanda >= 89 && Komanda <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] tvarka_Sąrašas = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Komanda - 89]; 순번++) Eilutė.add("popl " + 저장기들[순번]);
                for (int 순번 : tvarka_Sąrašas[Komanda - 89]) Eilutė.add("pushl " + 저장기들[순번]);
            } else if (Komanda == 96 || Komanda == 100 || Komanda == 104 || Komanda == 126 || Komanda == 128 || Komanda == 130) {
                String operacija_VALUE = Komanda == 96 ? "addl" : Komanda == 100 ? "subl" : Komanda == 104 ? "imull" : Komanda == 126 ? "andl" : Komanda == 128 ? "orl" : "xorl";
                Collections.addAll(Eilutė,"popl %ecx","popl %eax",operacija_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Komanda == 108 || Komanda == 112) Collections.addAll(Eilutė,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + vietos_rodyklė + "_divide","cmpl $0x80000000, %eax","jne " + vietos_rodyklė + "_divide","xorl %edx, %edx","jmp " + vietos_rodyklė + "_done",vietos_rodyklė + "_divide:","cltd","idivl %ecx",vietos_rodyklė + "_done:","pushl " + (Komanda == 108 ? "%eax" : "%edx"));
            else if (Komanda == 116) Eilutė.add("negl (%esp)");
            else if (Komanda == 120 || Komanda == 122 || Komanda == 124) Collections.addAll(Eilutė,"popl %ecx","popl %eax",(Komanda == 120 ? "sall" : Komanda == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Komanda == 132) {
                int INDEX = komanda_duomenys.한바이트(), padidinimas_VALUE = komanda_duomenys.부호한바이트(); čekis_vietinis(INDEX,vietinis_COUNT); Eilutė.add("addl $" + padidinimas_VALUE + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Komanda >= 145 && Komanda <= 147) Collections.addAll(Eilutė,"popl %eax",Komanda == 145 ? "movsbl %al, %eax" : Komanda == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Komanda >= 153 && Komanda <= 166) {
                if (Komanda <= 158) Collections.addAll(Eilutė,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Eilutė,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int vieta_VALUE = Pozicija + komanda_duomenys.부호두바이트(); šaka_Sąrašas.add(vieta_VALUE); Eilutė.add(비교들[Komanda - (Komanda <= 158 ? 153 : 159)] + " " + žymeklis_VALUE + "_b" + vieta_VALUE);
            } else if (Komanda == 167 || Komanda == 200) {
                int vieta_VALUE = Pozicija + (Komanda == 167 ? komanda_duomenys.부호두바이트() : komanda_duomenys.네바이트()); šaka_Sąrašas.add(vieta_VALUE); Eilutė.add("jmp " + žymeklis_VALUE + "_b" + vieta_VALUE);
            } else if (Komanda == 170 || Komanda == 171) {
                while (komanda_duomenys.Pozicija % 4 != 0) komanda_duomenys.한바이트();
                int numatytoji_reikšmė = Pozicija + komanda_duomenys.네바이트(); šaka_Sąrašas.add(numatytoji_reikšmė); Eilutė.add("popl %eax");
                int prekė_COUNT, 아래 = 0;
                if (Komanda == 170) { 아래 = komanda_duomenys.네바이트(); int 위 = komanda_duomenys.네바이트(); long 길이 = (long)위 - 아래 + 1; if (길이 < 1 || 길이 > (komanda_duomenys.duomenys.length - komanda_duomenys.Pozicija) / 4) throw new 번역오류("switch klipas KLAIDA"); prekė_COUNT = (int)길이; }
                else { prekė_COUNT = komanda_duomenys.네바이트(); if (prekė_COUNT < 0 || prekė_COUNT > (komanda_duomenys.duomenys.length - komanda_duomenys.Pozicija) / 8) throw new 번역오류("switch Dydis KLAIDA"); }
                for (int 순번 = 0; 순번 < prekė_COUNT; 순번++) {
                    int VALUE = Komanda == 170 ? 아래 + 순번 : komanda_duomenys.네바이트(), vieta_VALUE = Pozicija + komanda_duomenys.네바이트(); šaka_Sąrašas.add(vieta_VALUE);
                    Collections.addAll(Eilutė,"cmpl $" + VALUE + ", %eax","je " + žymeklis_VALUE + "_b" + vieta_VALUE);
                }
                Eilutė.add("jmp " + žymeklis_VALUE + "_b" + numatytoji_reikšmė);
            } else if (Komanda == 172 || Komanda == 176 || Komanda == 177) {
                if (Komanda != 177) Eilutė.add("popl %eax"); Collections.addAll(Eilutė,"leave","ret");
            } else if (Komanda == 178 || Komanda == 179) {
                metodas_nuoroda nuoroda = klasė_VALUE.nuoroda(komanda_duomenys.두바이트()); if (!필드들.containsKey(nuoroda)) throw new 번역오류("알 numeris 없는 lauko_reikšmė");
                Collections.addAll(Eilutė,"call " + simbolis("init",nuoroda.savininkas_VALUE),(Komanda == 178 ? "pushl " : "popl ") + simbolis("field",nuoroda.부분들()));
            } else if (Komanda == 184) {
                metodas_nuoroda nuoroda = klasė_VALUE.nuoroda(komanda_duomenys.두바이트()); if (!함수들.containsKey(nuoroda)) throw new 번역오류("알 numeris 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(nuoroda.aprašas_VALUE); Collections.addAll(Eilutė,"call " + simbolis("init",nuoroda.savininkas_VALUE),"call " + simbolis("method",nuoroda.부분들()));
                if (!호출형식.Argumentai.isEmpty()) Eilutė.add("addl $" + 호출형식.Argumentai.size() * 4 + ", %esp");
                if (!호출형식.grąžinti_KR.equals("V")) Eilutė.add("pushl %eax");
            } else if (Komanda == 182) {
                metodas_nuoroda nuoroda = klasė_VALUE.nuoroda(komanda_duomenys.두바이트());
                if (nuoroda.equals(new metodas_nuoroda("java/lang/String","length","()I"))) Collections.addAll(Eilutė,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (nuoroda.equals(new metodas_nuoroda("java/lang/String","charAt","(I)C"))) Collections.addAll(Eilutė,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 번역오류("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Komanda == 188) {
                if (komanda_duomenys.한바이트() != 10) throw new 번역오류("new int[]만 pagalba_VALUE"); Collections.addAll(Eilutė,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Komanda == 190) Collections.addAll(Eilutė,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Komanda == 196) {
                int plėtinys_VALUE = komanda_duomenys.한바이트(), INDEX = komanda_duomenys.두바이트(); čekis_vietinis(INDEX,vietinis_COUNT);
                if (plėtinys_VALUE == 21 || plėtinys_VALUE == 25 || plėtinys_VALUE == 54 || plėtinys_VALUE == 58) Eilutė.add((plėtinys_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (plėtinys_VALUE == 132) Eilutė.add("addl $" + komanda_duomenys.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new 번역오류("wide Komanda 미지원");
            } else if (Komanda == 198 || Komanda == 199) {
                int vieta_VALUE = Pozicija + komanda_duomenys.부호두바이트(); šaka_Sąrašas.add(vieta_VALUE); Collections.addAll(Eilutė,"popl %eax","testl %eax, %eax",(Komanda == 198 ? "je " : "jne ") + žymeklis_VALUE + "_b" + vieta_VALUE);
            } else throw new 번역오류("미지원 Komanda: " + Komanda);
        }
        if (!경계들.containsAll(šaka_Sąrašas)) throw new 번역오류("Komanda 경계가 아닌 곳으로 šaka");
        Eilutė.add(".size " + žymeklis_VALUE + ", .-" + žymeklis_VALUE); return String.join("\n",Eilutė);
    }
    String X_86_konstanta(klasė_duomenys duomenys, int INDEX) {
        if (duomenys.상수종류[INDEX] == 3) return duomenys.konstanta_duomenys[INDEX].toString();
        if (duomenys.상수종류[INDEX] == 8) return eilutė_simbolis(duomenys.문자((Integer)duomenys.konstanta_duomenys[INDEX]));
        throw new 번역오류("정수와 eilutė_VALUE 상수만 pagalba_VALUE");
    }
    String X_86_rinkinys(String įrašas_p, List<String> 내보냄, String tikslas) throws IOException {
        Map<String,String> mašina_lentelė = new HashMap<>();
        for (String Eilutė : Files.readAllLines(ištekliai_kelias.resolve("_86_mašina_Azure_funkcijos.tsv"))) { String[] susieti_VALUE = Eilutė.split("\t"); if (susieti_VALUE[0].equals(tikslas)) mašina_lentelė.put(susieti_VALUE[1] + susieti_VALUE[2],susieti_VALUE[3]); }
        int vietos_rodyklė = įrašas_p.lastIndexOf('.'); if (vietos_rodyklė < 0) throw new 번역오류("įrašas_p Priskirti_VALUE KLAIDA");
        String savininkas_VALUE = įrašas_p.substring(0,vietos_rodyklė).replace('.','/'), metodas_įrašas_pavadinimas = įrašas_p.substring(vietos_rodyklė + 1); metodas_nuoroda įrašas_p_VALUE = null;
        for (String aprašas_VALUE : Arrays.asList("()I","()V")) { metodas_nuoroda nuoroda = new metodas_nuoroda(savininkas_VALUE,metodas_įrašas_pavadinimas,aprašas_VALUE); if (함수들.containsKey(nuoroda)) { if (įrašas_p_VALUE != null) throw new 번역오류("겹친 įrašas_p"); įrašas_p_VALUE = nuoroda; } }
        if (įrašas_p_VALUE == null || (함수들.get(įrašas_p_VALUE).prieiga_įrašas & 0x100) != 0) throw new 번역오류("įrašas_p_VALUE FUNCTION_VALUE formatas_VALUE KLAIDA");
        List<String> Eilutė = new ArrayList<>(); Eilutė.add(".code32");
        for (klasė_duomenys duomenys : 클래스들.values()) {
            String Būsena_VALUE = simbolis("state",duomenys.Pavadinimas_2), 초기화 = simbolis("init",duomenys.Pavadinimas_2);
            Collections.addAll(Eilutė,".bss",".balign 4",Būsena_VALUE + ": .long 0",".text",초기화 + ":","cmpl $0, " + Būsena_VALUE,"jne " + 초기화 + "_done","movl $1, " + Būsena_VALUE);
            metodas_nuoroda 초기화참조 = new metodas_nuoroda(duomenys.Pavadinimas_2,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Eilutė.add("call " + simbolis("method",초기화참조.부분들()));
            Collections.addAll(Eilutė,"movl $2, " + Būsena_VALUE,초기화 + "_done:","ret");
            for (narys_duomenys lauko_reikšmė : duomenys.lauko_reikšmė) {
                byte[] konstanta_VALUE = lauko_reikšmė.atributas_VALUE.get("ConstantValue"); String VALUE = konstanta_VALUE == null ? "0" : X_86_konstanta(duomenys,new duomenys_Skaitytuvė(konstanta_VALUE).두바이트());
                Collections.addAll(Eilutė,".data",".balign 4",simbolis("field",duomenys.Pavadinimas_2,lauko_reikšmė.Pavadinimas_2,lauko_reikšmė.aprašas_VALUE) + ": .long " + VALUE);
            }
            for (narys_duomenys FUNCTION_VALUE : duomenys.FUNCTION_VALUE) if (!FUNCTION_VALUE.Pavadinimas_2.equals("<init>")) Eilutė.add(X_86_metodas_pranešimo_tekstas(new metodas_nuoroda(duomenys.Pavadinimas_2,FUNCTION_VALUE.Pavadinimas_2,FUNCTION_VALUE.aprašas_VALUE),FUNCTION_VALUE,mašina_lentelė,tikslas));
        }
        Collections.addAll(Eilutė,".text",".globl java_entry","java_entry:","call " + simbolis("init",įrašas_p_VALUE.savininkas_VALUE),"call " + simbolis("method",įrašas_p_VALUE.부분들()));
        if (įrašas_p_VALUE.aprašas_VALUE.equals("()V")) Eilutė.add("xorl %eax, %eax"); Eilutė.add("ret");
        for (String Priskirti_VALUE : 내보냄) {
            int skyriklis_VALUE_d8ba4873 = Priskirti_VALUE.indexOf('='); if (skyriklis_VALUE_d8ba4873 < 1) throw new 번역오류("내보내기 Priskirti_VALUE KLAIDA");
            String išorinis_VALUE = Priskirti_VALUE.substring(0,skyriklis_VALUE_d8ba4873), FUNCTION_VALUE = Priskirti_VALUE.substring(skyriklis_VALUE_d8ba4873 + 1); int dalyba_KR = FUNCTION_VALUE.lastIndexOf('.');
            if (dalyba_KR < 0 || !išorinis_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 simbolis KLAIDA");
            String klasė_VALUE = FUNCTION_VALUE.substring(0,dalyba_KR).replace('.','/'), Pavadinimas_2 = FUNCTION_VALUE.substring(dalyba_KR + 1); metodas_nuoroda žymėjimas_VALUE = null;
            for (metodas_nuoroda nuoroda : 함수들.keySet()) if (nuoroda.savininkas_VALUE.equals(klasė_VALUE) && nuoroda.Pavadinimas_2.equals(Pavadinimas_2)) { if (žymėjimas_VALUE != null) throw new 번역오류("겹친 내보내기 tikslas"); žymėjimas_VALUE = nuoroda; }
            if (žymėjimas_VALUE == null) throw new 번역오류("내보낼 함수가 없음");
            Collections.addAll(Eilutė,".text",".globl " + išorinis_VALUE,išorinis_VALUE + ":","call " + simbolis("init",žymėjimas_VALUE.savininkas_VALUE),"jmp " + simbolis("method",žymėjimas_VALUE.부분들()));
        }
        Eilutė.add(".section .rodata");
        for (Map.Entry<String,String> įrašas_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Eilutė,".balign 4",įrašas_VALUE.getValue() + ":",".long " + įrašas_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char pamoka_VALUE : įrašas_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(pamoka_VALUE)); if (!단위들.isEmpty()) Eilutė.add(".long " + String.join(",",단위들));
        }
        Eilutė.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Eilutė) + "\n";
    }
    static void Vykdyti_įrankis(List<String> Komanda) throws Exception {
        if (new ProcessBuilder(Komanda).inheritIO().start().waitFor() != 0) throw new 번역오류("kompiliuoti_šaltinis KLAIDA: " + Komanda.get(0));
    }
    static String duomenys_eilutė(String Tekstas) { return "\"" + Tekstas.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Vertimas(List<Path> 입력들, String tikslas, String įrašas_p, List<String> 내보냄, Path Išvestis, Path ištekliai_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), klasė_kelias = 임시.resolve("classes"); Files.createDirectory(klasė_kelias);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",klasė_kelias.toString(),"-sourcepath",klasė_kelias.toString(),"-d",klasė_kelias.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int šaltinis_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Išvestis.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new 번역오류("Išvestis 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); šaltinis_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new 번역오류(".java 또는 .class만 pagalba_VALUE");
            }
            if (šaltinis_COUNT > 0) Vykdyti_įrankis(자바명령);
            try (java.util.stream.Stream<Path> kelias_Sąrašas = Files.walk(klasė_kelias)) { kelias_Sąrašas.filter(KELIAS -> KELIAS.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,tikslas.equals("user") ? "user" : "kernel",262144,ištekliai_VALUE);
            String 조립 = CONVERT_VALUE.X_86_rinkinys(įrašas_p,내보냄,tikslas); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path įrankis_padėtis = ištekliai_VALUE.getParent();
            Vykdyti_įrankis(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Vykdyti_įrankis(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),įrankis_padėtis.resolve("CLR_pagalba.s").toString()));
            List<String> Prisijungti = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (tikslas.equals("kernel")) Prisijungti.add("-r");
            else {
                Vykdyti_įrankis(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),įrankis_padėtis.resolve(tikslas.equals("user") ? "Start_naudotojas_programa.s" : "리눅스시작.s").toString()));
                Collections.addAll(Prisijungti,"-e","_start",임시.resolve("start.o").toString());
                if (tikslas.equals("user")) Collections.addAll(Prisijungti,"-T",įrankis_padėtis.resolve("naudotojas_sieti_schema.ld").toString());
            }
            Collections.addAll(Prisijungti,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Vykdyti_įrankis(Prisijungti);
            Išvestis = Išvestis.toAbsolutePath(); Files.createDirectories(Išvestis.getParent()); Path publikuoti_VALUE = Files.createTempFile(Išvestis.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publikuoti_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(publikuoti_VALUE,Išvestis,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publikuoti_VALUE); }
            Files.setPosixFilePermissions(Išvestis,java.nio.file.attribute.PosixFilePermissions.fromString(tikslas.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Išvestis + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbolis_duomenys = new ArrayList<>(), šaltinis_duomenys = new ArrayList<>();
            for (metodas_nuoroda nuoroda : CONVERT_VALUE.함수들.keySet()) simbolis_duomenys.add(duomenys_eilutė(simbolis("method",nuoroda.부분들())) + ":" + duomenys_eilutė(nuoroda.savininkas_VALUE + "." + nuoroda.Pavadinimas_2 + nuoroda.aprašas_VALUE));
            for (Path 입력 : 입력들) {
                byte[] maiša_Failas = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Tekstas = new StringBuilder(); for (byte VALUE : maiša_Failas) Tekstas.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                šaltinis_duomenys.add(duomenys_eilutė(입력.toAbsolutePath().toString()) + ":" + duomenys_eilutė(Tekstas.toString()));
            }
            Files.writeString(Paths.get(Išvestis + ".json"),"{\"target\":" + duomenys_eilutė(tikslas) + ",\"entry\":" + duomenys_eilutė(įrašas_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbolis_duomenys) + "},\"sources\":{" + String.join(",",šaltinis_duomenys) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> kelias_Sąrašas = Files.walk(임시)) { for (Path KELIAS : (Iterable<Path>)kelias_Sąrašas.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(KELIAS); }
        }
    }
    public static void main(String[] Argumentai) {
        try {
            String įrašas_p = null, tikslas = "kernel", X_86_tikslas = null; Path išeiga_kelias = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> kelias_Sąrašas = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumentai.length; 순번++) {
                String VALUE = Argumentai[순번];
                switch (VALUE) {
                    case "--target": X_86_tikslas = Argumentai[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry klasė_VALUE.FUNCTION_VALUE -o Išvestis [--target linux|kernel|user] [--profile kernel|user] [--export simbolis=klasė_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": įrašas_p = Argumentai[++순번]; break;
                    case "--profile": tikslas = Argumentai[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumentai[++순번]); break;
                    case "--export": 내보냄.add(Argumentai[++순번]); break;
                    case "-o": išeiga_kelias = Paths.get(Argumentai[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new 번역오류("알 numeris 없는 옵션: " + VALUE); kelias_Sąrašas.add(Paths.get(VALUE));
                }
            }
            if (įrašas_p == null || išeiga_kelias == null || kelias_Sąrašas.isEmpty()) throw new 번역오류("--entry, -o, klasė_VALUE 파일이 필요합니다");
            Path ištekliai_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_tikslas != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_tikslas)) throw new 번역오류("알 numeris 없는 Vykdyti_komanda tikslas");
                X_86_Vertimas(kelias_Sąrašas,X_86_tikslas,įrašas_p,내보냄,išeiga_kelias,ištekliai_VALUE); return;
            }
            String ŠALTINIS = new 기계어미리번역(kelias_Sąrašas, tikslas, 낱말수, ištekliai_VALUE).generuoti(įrašas_p, 내보냄, 범용표기);
            išeiga_kelias = išeiga_kelias.toAbsolutePath(); Files.createDirectories(išeiga_kelias.getParent());
            Path 임시 = Files.createTempFile(išeiga_kelias.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ŠALTINIS, StandardCharsets.UTF_8); Files.move(임시, išeiga_kelias, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception KLAIDA) { System.err.println("kompiliuoti_šaltinis KLAIDA: " + KLAIDA.getMessage()); System.exit(1); }
    }
}
