// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Sinif_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Tərcümə_səhv extends RuntimeException {
        Tərcümə_səhv(String 설명) { super(설명); }
    }
    static final class verilənlər_oxucu {
        final byte[] verilənlər;
        int yerinə_qoymaq;
        verilənlər_oxucu(byte[] 입력자료) { verilənlər = 입력자료; }
        byte[] Oxuma(int uzunluq_VALUE) {
            if (uzunluq_VALUE < 0 || uzunluq_VALUE > verilənlər.length - yerinə_qoymaq) throw new Tərcümə_səhv("잘린 Sinif_VALUE 또는 Əmr verilənlər");
            byte[] ölçü = Arrays.copyOfRange(verilənlər, yerinə_qoymaq, yerinə_qoymaq + uzunluq_VALUE); yerinə_qoymaq += uzunluq_VALUE; return ölçü;
        }
        int 한바이트() { if (yerinə_qoymaq >= verilənlər.length) throw new Tərcümə_səhv("잘린 Əmr verilənlər"); return verilənlər[yerinə_qoymaq++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class üzv_verilənlər {
        final int müraciət_daxiletmə;
        final String Ad, 서술;
        final Map<String, byte[]> atribut_VALUE;
        üzv_verilənlər(int müraciət_VALUE, String ad_VALUE, String 서술값, Map<String, byte[]> atribut_verilənlər) {
            müraciət_daxiletmə = müraciət_VALUE; Ad = ad_VALUE; 서술 = 서술값; atribut_VALUE = atribut_verilənlər;
        }
    }
    static final class metod_İstinad implements Comparable<metod_İstinad> {
        final String sahib_VALUE, Ad, 서술;
        metod_İstinad(String 소유값, String ad_VALUE, String 서술값) { sahib_VALUE = 소유값; Ad = ad_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{sahib_VALUE, Ad, 서술}; }
        public int compareTo(metod_İstinad eynisəviyyəli_VALUE) {
            int Müqayisə_VALUE = sahib_VALUE.compareTo(eynisəviyyəli_VALUE.sahib_VALUE);
            if (Müqayisə_VALUE == 0) Müqayisə_VALUE = Ad.compareTo(eynisəviyyəli_VALUE.Ad);
            return Müqayisə_VALUE == 0 ? 서술.compareTo(eynisəviyyəli_VALUE.서술) : Müqayisə_VALUE;
        }
        public boolean equals(Object eynisəviyyəli_VALUE) { return eynisəviyyəli_VALUE instanceof metod_İstinad && compareTo((metod_İstinad) eynisəviyyəli_VALUE) == 0; }
        public int hashCode() { return Objects.hash(sahib_VALUE, Ad, 서술); }
    }
    static final class Sinif_verilənlər {
        final int[] 상수종류;
        final Object[] sabit_verilənlər;
        final String Ad;
        final List<üzv_verilənlər> sahə_VALUE_0f39cf1c, FUNCTION_VALUE;
        Sinif_verilənlər(Path Cığır) throws IOException {
            verilənlər_oxucu oxucu_VALUE = new verilənlər_oxucu(Files.readAllBytes(Cığır));
            if (oxucu_VALUE.네바이트() != 0xcafebabe) throw new Tərcümə_səhv("Java Sinif_VALUE 표식이 아님");
            oxucu_VALUE.Oxuma(4);
            int element_COUNT = oxucu_VALUE.두바이트(); 상수종류 = new int[element_COUNT]; sabit_verilənlər = new Object[element_COUNT];
            for (int 순번 = 1; 순번 < element_COUNT; 순번++) {
                int 종류 = oxucu_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int uzunluq_VALUE = oxucu_VALUE.두바이트();
                        byte[] simvol_bufer = oxucu_VALUE.Oxuma(uzunluq_VALUE), 길이붙인자료 = new byte[uzunluq_VALUE + 2];
                        길이붙인자료[0] = (byte)(uzunluq_VALUE >> 8); 길이붙인자료[1] = (byte)uzunluq_VALUE;
                        System.arraycopy(simvol_bufer, 0, 길이붙인자료, 2, uzunluq_VALUE);
                        sabit_verilənlər[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: sabit_verilənlər[순번] = oxucu_VALUE.네바이트(); break;
                    case 4: oxucu_VALUE.Oxuma(4); break;
                    case 5: case 6: oxucu_VALUE.Oxuma(8); 순번++; break;
                    case 7: case 8: case 16: sabit_verilənlər[순번] = oxucu_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        sabit_verilənlər[순번] = new int[]{oxucu_VALUE.두바이트(), oxucu_VALUE.두바이트()}; break;
                    case 15: sabit_verilənlər[순번] = new int[]{oxucu_VALUE.한바이트(), oxucu_VALUE.두바이트()}; break;
                    default: throw new Tərcümə_səhv("지원하지 않는 sabit_VALUE 종류: " + 종류);
                }
            }
            oxucu_VALUE.두바이트(); Ad = Sinif_ad(oxucu_VALUE.두바이트());
            if (!Sinif_ad(oxucu_VALUE.두바이트()).equals("java/lang/Object") || oxucu_VALUE.두바이트() != 0)
                throw new Tərcümə_səhv(Ad + ": 상속 및 인터페이스 미지원");
            sahə_VALUE_0f39cf1c = 멤버읽기(oxucu_VALUE); FUNCTION_VALUE = 멤버읽기(oxucu_VALUE); 속성읽기(oxucu_VALUE);
            if (oxucu_VALUE.yerinə_qoymaq != oxucu_VALUE.verilənlər.length) throw new Tərcümə_səhv("Sinif_VALUE 뒤에 남은 verilənlər");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Tərcümə_səhv("문자 sabit_VALUE INDEX XƏTA");
            return (String) sabit_verilənlər[INDEX];
        }
        String Sinif_ad(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Tərcümə_səhv("Sinif_VALUE İstinad XƏTA");
            return 문자((Integer)sabit_verilənlər[INDEX]);
        }
        metod_İstinad İstinad(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Tərcümə_səhv("멤버 İstinad XƏTA");
            int[] qoşmaq_VALUE = (int[])sabit_verilənlər[INDEX], ad_qoşmaq = (int[])sabit_verilənlər[qoşmaq_VALUE[1]];
            return new metod_İstinad(Sinif_ad(qoşmaq_VALUE[0]), 문자(ad_qoşmaq[0]), 문자(ad_qoşmaq[1]));
        }
        Map<String, byte[]> 속성읽기(verilənlər_oxucu oxucu_VALUE) {
            Map<String, byte[]> ölçü = new LinkedHashMap<>();
            int element_COUNT = oxucu_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                String atribut_ad = 문자(oxucu_VALUE.두바이트()); byte[] VALUE = oxucu_VALUE.Oxuma(oxucu_VALUE.네바이트());
                if (ölçü.put(atribut_ad, VALUE) != null) throw new Tərcümə_səhv("겹친 atribut_VALUE: " + atribut_ad);
            }
            return ölçü;
        }
        List<üzv_verilənlər> 멤버읽기(verilənlər_oxucu oxucu_VALUE) {
            List<üzv_verilənlər> ölçü = new ArrayList<>(); int element_COUNT = oxucu_VALUE.두바이트();
            for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                int müraciət_daxiletmə = oxucu_VALUE.두바이트(); String metod_daxiletmə_ad = 문자(oxucu_VALUE.두바이트()), 서술 = 문자(oxucu_VALUE.두바이트());
                ölçü.add(new üzv_verilənlər(müraciət_daxiletmə, metod_daxiletmə_ad, 서술, 속성읽기(oxucu_VALUE)));
            }
            return ölçü;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String geri_qaytarmaq_ölçü;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Tərcümə_səhv("FUNCTION_VALUE 서술 XƏTA: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Tərcümə_səhv("FUNCTION_VALUE 서술 XƏTA: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Tərcümə_səhv("FUNCTION_VALUE 서술 XƏTA: " + 서술);
            geri_qaytarmaq_ölçü = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> ölçü = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int yerinə_qoymaq = 0; yerinə_qoymaq < 서술.length();) {
            String seçilmiş_sahə_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, yerinə_qoymaq)) { seçilmiş_sahə_VALUE = format_VALUE; break; }
            if (seçilmiş_sahə_VALUE == null) throw new Tərcümə_səhv("지원하지 않는 verilənlər_növü: " + 서술);
            ölçü.add(seçilmiş_sahə_VALUE); yerinə_qoymaq += seçilmiş_sahə_VALUE.length();
        }
        return ölçü;
    }
    static String simvol(String 종류, String... 부분들) {
        try {
            byte[] heş_fayl = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Mətn = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Mətn.append(String.format(Locale.ROOT, "%02x", heş_fayl[순번] & 255));
            return Mətn.toString();
        } catch (Exception XƏTA) { throw new Tərcümə_səhv(XƏTA.toString()); }
    }
    final Map<String, Sinif_verilənlər> 클래스들 = new TreeMap<>();
    final Map<metod_İstinad, üzv_verilənlər> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, maşın_Sinif;
    final int 동적기억낱말수;
    final Path resurs_yol;
    기계어미리번역(List<Path> yol_Siyahı, String hədəf, int 낱말수, Path resurs_VALUE) throws IOException {
        if ((!hədəf.equals("kernel") && !hədəf.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Tərcümə_səhv("icra_etmək_əmr hədəf 또는 Yaddaş_VALUE 공간 Böyüklük XƏTA");
        실행대상 = hədəf; 동적기억낱말수 = 낱말수; resurs_yol = resurs_VALUE;
        // 이 이름도 국가별 mənbə_ağac yarat 시 해당 언어로 옮긴다.
        maşın_Sinif = hədəf.equals("kernel") ? "lövhə" : "istifadəçi";
        for (String Giriş : Files.readAllLines(resurs_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Giriş.split("\t", -1);
            if (부분들.length != 4) throw new Tərcümə_səhv("maşın FUNCTION_VALUE verilənlər XƏTA");
            if (부분들[0].equals(hədəf)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Cığır : yol_Siyahı) {
            Sinif_verilənlər verilənlər = new Sinif_verilənlər(Cığır);
            if (클래스들.put(verilənlər.Ad, verilənlər) != null) throw new Tərcümə_səhv("중복 Sinif_VALUE: " + verilənlər.Ad);
            for (üzv_verilənlər sahə_VALUE_0f39cf1c : verilənlər.sahə_VALUE_0f39cf1c) {
                if ((sahə_VALUE_0f39cf1c.müraciət_daxiletmə & 8) == 0 || 형식읽기(sahə_VALUE_0f39cf1c.서술).equals(Collections.singletonList("V"))) throw new Tərcümə_səhv("statik_VALUE 필드만 Dəstək_VALUE");
                if (필드들.put(new metod_İstinad(verilənlər.Ad, sahə_VALUE_0f39cf1c.Ad, sahə_VALUE_0f39cf1c.서술), sahə_VALUE_0f39cf1c) != null) throw new Tərcümə_səhv("중복 sahə_VALUE_0f39cf1c");
            }
            for (üzv_verilənlər FUNCTION_VALUE : verilənlər.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Ad.equals("<init>")) continue;
                if ((FUNCTION_VALUE.müraciət_daxiletmə & 8) == 0 || (FUNCTION_VALUE.müraciət_daxiletmə & (0x20 | 0x400)) != 0) throw new Tərcümə_səhv("statik_VALUE 비동기화 함수만 Dəstək_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new metod_İstinad(verilənlər.Ad, FUNCTION_VALUE.Ad, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Tərcümə_səhv("중복 FUNCTION_VALUE");
            }
        }
    }
    String sətir_simvol(String Mətn) { return 문자열들.computeIfAbsent(Mətn, VALUE -> "j_text_" + 문자열들.size()); }
    String sabit_ifadə(Sinif_verilənlər verilənlər, int INDEX) {
        if (INDEX < 1 || INDEX >= verilənlər.상수종류.length) throw new Tərcümə_səhv("sabit_VALUE INDEX klip XƏTA");
        if (verilənlər.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + verilənlər.sabit_verilənlər[INDEX] + ")";
        if (verilənlər.상수종류[INDEX] == 8) return "(word)" + sətir_simvol(verilənlər.문자((Integer)verilənlər.sabit_verilənlər[INDEX]));
        throw new Tərcümə_səhv("정수와 sətir_VALUE 상수만 Dəstək_VALUE");
    }
    String 함수원형(metod_İstinad İstinad) {
        List<String> 인수들 = new ArrayList<>(); int element_COUNT = new 함수형식(İstinad.서술).인수.size();
        for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simvol("method", İstinad.부분들()) + "(" + (element_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void çek_lokal(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Tərcümə_səhv("lokal_miqyas 변수 INDEX klip XƏTA"); }
    void 분기넣기(List<String> 출력, Set<Integer> qol_Siyahı, int yerinə_qoymaq, int 이동량, String şərt) {
        int təyinat_VALUE_a0fbc067 = yerinə_qoymaq + 이동량; qol_Siyahı.add(təyinat_VALUE_a0fbc067);
        출력.add((şərt == null ? "" : "if (" + şərt + ") ") + "goto b" + təyinat_VALUE_a0fbc067 + ";");
    }
    String 함수본문(metod_İstinad FUNCTION_VALUE, üzv_verilənlər verilənlər) {
        byte[] 본문자료 = verilənlər.atribut_VALUE.get("Code"); if (본문자료 == null) throw new Tərcümə_səhv("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Ad);
        verilənlər_oxucu oxucu_VALUE = new verilənlər_oxucu(본문자료); int 쌓임깊이 = oxucu_VALUE.두바이트(), 지역변수수 = oxucu_VALUE.두바이트();
        verilənlər_oxucu əmr_verilənlər = new verilənlər_oxucu(oxucu_VALUE.Oxuma(oxucu_VALUE.네바이트()));
        if (oxucu_VALUE.두바이트() != 0) throw new Tərcümə_səhv("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (지역변수수 < format_VALUE.인수.size()) throw new Tərcümə_səhv("매개변수보다 적은 lokal_miqyas 변수");
        Sinif_verilənlər Sinif_VALUE = 클래스들.get(FUNCTION_VALUE.sahib_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(FUNCTION_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), qol_Siyahı = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (əmr_verilənlər.yerinə_qoymaq < əmr_verilənlər.verilənlər.length) {
            int yerinə_qoymaq = əmr_verilənlər.yerinə_qoymaq, Əmr = əmr_verilənlər.한바이트(); 경계들.add(yerinə_qoymaq); 출력.add("b" + yerinə_qoymaq + ":;");
            if (Əmr == 0) continue;
            if (Əmr == 1) 출력.add("PUSH(0);");
            else if (Əmr >= 2 && Əmr <= 8) 출력.add("PUSH((uint32_t)(" + (Əmr - 3) + "));");
            else if (Əmr == 16 || Əmr == 17) 출력.add("PUSH((uint32_t)(" + (Əmr == 16 ? əmr_verilənlər.부호한바이트() : əmr_verilənlər.부호두바이트()) + "));");
            else if (Əmr == 18 || Əmr == 19) 출력.add("PUSH(" + sabit_ifadə(Sinif_VALUE, Əmr == 18 ? əmr_verilənlər.한바이트() : əmr_verilənlər.두바이트()) + ");");
            else if (Əmr == 21 || Əmr == 25 || (Əmr >= 26 && Əmr <= 29) || (Əmr >= 42 && Əmr <= 45)) {
                int INDEX = Əmr == 21 || Əmr == 25 ? əmr_verilənlər.한바이트() : Əmr - (Əmr <= 29 ? 26 : 42);
                çek_lokal(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (Əmr == 54 || Əmr == 58 || (Əmr >= 59 && Əmr <= 62) || (Əmr >= 75 && Əmr <= 78)) {
                int INDEX = Əmr == 54 || Əmr == 58 ? əmr_verilənlər.한바이트() : Əmr - (Əmr <= 62 ? 59 : 75);
                çek_lokal(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (Əmr == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Əmr == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Əmr == 87 || Əmr == 88) 출력.add(Əmr == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Əmr >= 89 && Əmr <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ardıcıllıq_Siyahı = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Əmr - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : ardıcıllıq_Siyahı[Əmr - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (Əmr == 96 || Əmr == 100 || Əmr == 104 || Əmr == 126 || Əmr == 128 || Əmr == 130) {
                String əməliyyat_VALUE = Əmr == 96 ? "+" : Əmr == 100 ? "-" : Əmr == 104 ? "*" : Əmr == 126 ? "&" : Əmr == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + əməliyyat_VALUE + " (uint32_t)b);");
            } else if (Əmr == 108 || Əmr == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Əmr == 112 ? 1 : 0) + "));");
            else if (Əmr == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Əmr == 120 || Əmr == 122 || Əmr == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Əmr == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Əmr == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Əmr == 132) {
                int INDEX = əmr_verilənlər.한바이트(), 증가량 = əmr_verilənlər.부호한바이트(); çek_lokal(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Əmr >= 145 && Əmr <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Əmr == 145 ? "int8_t" : Əmr == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Əmr >= 153 && Əmr <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, qol_Siyahı, yerinə_qoymaq, əmr_verilənlər.부호두바이트(), "(int32_t)a " + 비교들[Əmr - 153] + " 0");
            } else if (Əmr >= 159 && Əmr <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, qol_Siyahı, yerinə_qoymaq, əmr_verilənlər.부호두바이트(), Əmr >= 165 ? "a " + 비교들[Əmr - 159] + " b" : "(int32_t)a " + 비교들[Əmr - 159] + " (int32_t)b");
            } else if (Əmr == 167 || Əmr == 200) 분기넣기(출력, qol_Siyahı, yerinə_qoymaq, Əmr == 167 ? əmr_verilənlər.부호두바이트() : əmr_verilənlər.네바이트(), null);
            else if (Əmr == 170 || Əmr == 171) {
                while (əmr_verilənlər.yerinə_qoymaq % 4 != 0) əmr_verilənlər.한바이트();
                int standart_qiymət = əmr_verilənlər.네바이트(); 출력.add("a = POP();");
                if (Əmr == 170) {
                    int 아래 = əmr_verilənlər.네바이트(), 위 = əmr_verilənlər.네바이트(); long element_COUNT = (long)위 - 아래 + 1;
                    if (element_COUNT < 1 || element_COUNT > (əmr_verilənlər.verilənlər.length - əmr_verilənlər.yerinə_qoymaq) / 4) throw new Tərcümə_səhv("switch klip XƏTA");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, qol_Siyahı, yerinə_qoymaq, əmr_verilənlər.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int element_COUNT = əmr_verilənlər.네바이트(), ön_verilənlər = 0;
                    if (element_COUNT < 0 || element_COUNT > (əmr_verilənlər.verilənlər.length - əmr_verilənlər.yerinə_qoymaq) / 8) throw new Tərcümə_səhv("switch Böyüklük XƏTA");
                    for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                        int VALUE = əmr_verilənlər.네바이트(); if (순번 > 0 && VALUE <= ön_verilənlər) throw new Tərcümə_səhv("switch ardıcıllıq_VALUE XƏTA"); ön_verilənlər = VALUE;
                        분기넣기(출력, qol_Siyahı, yerinə_qoymaq, əmr_verilənlər.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, qol_Siyahı, yerinə_qoymaq, standart_qiymət, null);
            } else if (Əmr == 172 || Əmr == 176 || Əmr == 177) 출력.add("return " + (Əmr == 177 ? "0" : "POP()") + ";");
            else if (Əmr == 178 || Əmr == 179) {
                metod_İstinad İstinad = Sinif_VALUE.İstinad(əmr_verilənlər.두바이트()); if (!필드들.containsKey(İstinad)) throw new Tərcümə_səhv("알 수 없는 sahə_VALUE_0f39cf1c");
                출력.add(simvol("init", İstinad.sahib_VALUE) + "();"); String sahə_VALUE_0f39cf1c = simvol("field", İstinad.부분들());
                출력.add(Əmr == 178 ? "PUSH(" + sahə_VALUE_0f39cf1c + ");" : sahə_VALUE_0f39cf1c + " = POP();");
            } else if (Əmr == 184) {
                metod_İstinad İstinad = Sinif_VALUE.İstinad(əmr_verilənlər.두바이트()); if (!함수들.containsKey(İstinad)) throw new Tərcümə_səhv("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(İstinad.서술); int element_COUNT = 호출형식.인수.size();
                출력.add(simvol("init", İstinad.sahib_VALUE) + "();"); 출력.add("if(sp < " + element_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + element_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < element_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + simvol("method", İstinad.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.geri_qaytarmaq_ölçü.equals("V")) 출력.add("PUSH(a);");
            } else if (Əmr == 182) {
                metod_İstinad İstinad = Sinif_VALUE.İstinad(əmr_verilənlər.두바이트());
                if (İstinad.equals(new metod_İstinad("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (İstinad.equals(new metod_İstinad("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Tərcümə_səhv("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Əmr == 188) {
                if (əmr_verilənlər.한바이트() != 10) throw new Tərcümə_səhv("new int[]만 Dəstək_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Əmr == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Əmr == 196) {
                int genişlənmə_VALUE = əmr_verilənlər.한바이트(), INDEX = əmr_verilənlər.두바이트(); çek_lokal(INDEX, 지역변수수);
                if (genişlənmə_VALUE == 21 || genişlənmə_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (genişlənmə_VALUE == 54 || genişlənmə_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (genişlənmə_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + əmr_verilənlər.부호두바이트() + ");");
                else throw new Tərcümə_səhv("미지원 wide Əmr");
            } else if (Əmr == 198 || Əmr == 199) {
                출력.add("a = POP();"); 분기넣기(출력, qol_Siyahı, yerinə_qoymaq, əmr_verilənlər.부호두바이트(), "a " + (Əmr == 198 ? "==" : "!=") + " 0");
            } else throw new Tərcümə_səhv(FUNCTION_VALUE.sahib_VALUE + "." + FUNCTION_VALUE.Ad + ", bayt_VALUE " + yerinə_qoymaq + ": 미지원 Əmr " + Əmr);
        }
        if (!경계들.containsAll(qol_Siyahı)) throw new Tərcümə_səhv("Əmr 경계가 아닌 곳으로 qol");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String ixrac_etmək_metod(String keçid_simvol, String hədəf, boolean 진입점여부) {
        int yerinə_qoymaq_INDEX = hədəf.lastIndexOf('.'); if (yerinə_qoymaq_INDEX < 0 || !keçid_simvol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tərcümə_səhv("내보내기 təyin_et_VALUE XƏTA");
        String sahib_VALUE = hədəf.substring(0, yerinə_qoymaq_INDEX).replace('.', '/'), Ad = hədəf.substring(yerinə_qoymaq_INDEX + 1); metod_İstinad seçilmiş_sahə_VALUE = null;
        for (metod_İstinad İstinad : 함수들.keySet()) if (İstinad.sahib_VALUE.equals(sahib_VALUE) && İstinad.Ad.equals(Ad)) {
            if (seçilmiş_sahə_VALUE != null) throw new Tərcümə_səhv("겹친 내보내기 hədəf"); seçilmiş_sahə_VALUE = İstinad;
        }
        if (seçilmiş_sahə_VALUE == null || (함수들.get(seçilmiş_sahə_VALUE).müraciət_daxiletmə & 0x100) != 0) throw new Tərcümə_səhv("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 format_VALUE = new 함수형식(seçilmiş_sahə_VALUE.서술);
        if ((진입점여부 && !format_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.geri_qaytarmaq_ölçü)) throw new Tərcümə_səhv("daxiletmə_p_VALUE 또는 C 경계 format_VALUE XƏTA");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) {
            if (!format_VALUE.인수.get(순번).equals("I")) throw new Tərcümə_səhv("C 경계는 int 인수만 Dəstək_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.geri_qaytarmaq_ölçü.equals("V") ? "void " : "int32_t ") + keçid_simvol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simvol("init", seçilmiş_sahə_VALUE.sahib_VALUE) + "(); " + (format_VALUE.geri_qaytarmaq_ölçü.equals("V") ? "" : "return (int32_t)") + simvol("method", seçilmiş_sahə_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String yarat(String daxiletmə_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metod_İstinad, üzv_verilənlər> daxiletmə_VALUE : 함수들.entrySet()) {
            metod_İstinad İstinad = daxiletmə_VALUE.getKey(); üzv_verilənlər verilənlər = daxiletmə_VALUE.getValue(); 선언들.add(함수원형(İstinad) + ";");
            if ((verilənlər.müraciət_daxiletmə & 0x100) != 0) {
                String Bağlan = 기계함수들.get(İstinad.Ad + İstinad.서술);
                if (!İstinad.sahib_VALUE.equals(maşın_Sinif) || Bağlan == null) throw new Tərcümə_səhv("허용되지 않은 native FUNCTION_VALUE: " + İstinad.Ad);
                int element_COUNT = new 함수형식(İstinad.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Bağlan + "(" + (element_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(element_COUNT, "word"))) + ");");
                몸체들.add(함수원형(İstinad) + " { return " + Bağlan + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(İstinad, verilənlər));
        }
        for (Map.Entry<metod_İstinad, üzv_verilənlər> daxiletmə_VALUE : 필드들.entrySet()) {
            metod_İstinad İstinad = daxiletmə_VALUE.getKey(); byte[] sabit_VALUE = daxiletmə_VALUE.getValue().atribut_VALUE.get("ConstantValue");
            String VALUE = sabit_VALUE == null ? "0" : sabit_ifadə(클래스들.get(İstinad.sahib_VALUE), new verilənlər_oxucu(sabit_VALUE).두바이트());
            필드선언들.add("static word " + simvol("field", İstinad.부분들()) + " = " + VALUE + ";");
        }
        for (String Ad : 클래스들.keySet()) {
            String ilkin_qiymət_vermək = simvol("init", Ad), vəziyyət_VALUE = simvol("state", Ad);
            선언들.add("static void " + ilkin_qiymət_vermək + "(void);"); 필드선언들.add("static unsigned " + vəziyyət_VALUE + ";");
            metod_İstinad İstinad = new metod_İstinad(Ad, "<clinit>", "()V");
            몸체들.add("static void " + ilkin_qiymət_vermək + "(void) { if(" + vəziyyət_VALUE + ") return; " + vəziyyət_VALUE + " = 1; " + (함수들.containsKey(İstinad) ? simvol("method", İstinad.부분들()) + "(); " : "") + vəziyyət_VALUE + " = 2; }");
        }
        몸체들.add(ixrac_etmək_metod("java_entry", daxiletmə_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String təyin_et_VALUE : 내보내기목록) {
            int yerinə_qoymaq_INDEX = təyin_et_VALUE.indexOf('='); if (yerinə_qoymaq_INDEX < 1) throw new Tərcümə_səhv("내보내기 təyin_et_VALUE XƏTA");
            String Ad = təyin_et_VALUE.substring(0, yerinə_qoymaq_INDEX); 공개이름.add(Ad); 몸체들.add(ixrac_etmək_metod(Ad, təyin_et_VALUE.substring(yerinə_qoymaq_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> daxiletmə_VALUE : 문자열들.entrySet()) {
            String Mətn = daxiletmə_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + daxiletmə_VALUE.getValue() + "[] = {" + Mətn.length());
            for (int 순번 = 0; 순번 < Mətn.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Mətn.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Dəstək_VALUE = Files.readString(resurs_yol.resolve("ümumi_dil_icrası_Dəstək.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Dəstək_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String QAYNAQ, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ad_cədvəl = new HashMap<>();
        for (String Giriş : Files.readAllLines(resurs_yol.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] qoşmaq_VALUE = Giriş.split("\t"); ad_cədvəl.put(qoşmaq_VALUE[0], qoşmaq_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(QAYNAQ); StringBuffer ölçü = new StringBuffer();
        while (찾개.find()) {
            String Ad = 찾개.group(), 새이름 = Ad;
            if (!Ad.startsWith("//") && !Ad.startsWith("/*") && !Ad.startsWith("\"") && !Ad.startsWith("'") && !공개이름.contains(Ad)) {
                새이름 = ad_cədvəl.getOrDefault(Ad, Ad);
                if (Ad.matches("a[0-9]+")) 새이름 = "인수" + Ad.substring(1);
                if (Ad.matches("b[0-9]+")) 새이름 = "qol" + Ad.substring(1);
                if (범용표기) {
                    StringBuilder notasiya_VALUE = new StringBuilder();
                    for (char simvol_VALUE_068c2631 : 새이름.toCharArray()) notasiya_VALUE.append(simvol_VALUE_068c2631 < 128 ? Character.toString(simvol_VALUE_068c2631) : String.format(Locale.ROOT, "\\u%04x", (int)simvol_VALUE_068c2631));
                    새이름 = notasiya_VALUE.toString();
                }
            }
            찾개.appendReplacement(ölçü, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(ölçü); return ölçü.toString();
    }
    String 엑스함수본문(metod_İstinad FUNCTION_VALUE, üzv_verilənlər verilənlər, Map<String,String> maşın_cədvəl, String hədəf) {
        String 표식 = simvol("method", FUNCTION_VALUE.부분들());
        List<String> Giriş = new ArrayList<>();
        if ((verilənlər.müraciət_daxiletmə & 0x100) != 0) {
            String Bağlan = maşın_cədvəl.get(FUNCTION_VALUE.Ad + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.sahib_VALUE.equals(hədəf.equals("kernel") ? "cihaz_VALUE" : "istifadəçi") || Bağlan == null) throw new Tərcümə_səhv("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Bağlan;
        }
        byte[] əsas_mətn = verilənlər.atribut_VALUE.get("Code"); if (əsas_mətn == null) throw new Tərcümə_səhv("FUNCTION_VALUE 몸체가 없음");
        verilənlər_oxucu oxucu_VALUE = new verilənlər_oxucu(əsas_mətn); oxucu_VALUE.두바이트(); int lokal_COUNT = oxucu_VALUE.두바이트();
        verilənlər_oxucu əmr_verilənlər = new verilənlər_oxucu(oxucu_VALUE.Oxuma(oxucu_VALUE.네바이트()));
        if (oxucu_VALUE.두바이트() != 0) throw new Tərcümə_səhv("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokal_COUNT < format_VALUE.인수.size()) throw new Tərcümə_səhv("매개변수보다 적은 lokal_miqyas 변수");
        Collections.addAll(Giriş,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) Collections.addAll(Giriş,"movl " + (8 + 4 * (format_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Sinif_verilənlər Sinif_VALUE = 클래스들.get(FUNCTION_VALUE.sahib_VALUE); Set<Integer> 경계들 = new HashSet<>(), qol_Siyahı = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (əmr_verilənlər.yerinə_qoymaq < əmr_verilənlər.verilənlər.length) {
            int yerinə_qoymaq = əmr_verilənlər.yerinə_qoymaq, Əmr = əmr_verilənlər.한바이트(); String yerinə_qoymaq_INDEX = 표식 + "_b" + yerinə_qoymaq;
            Giriş.add(yerinə_qoymaq_INDEX + ":"); 경계들.add(yerinə_qoymaq);
            if (Əmr == 0) Giriş.add("nop");
            else if (Əmr == 1) Giriş.add("pushl $0");
            else if (Əmr >= 2 && Əmr <= 8) Giriş.add("pushl $" + (Əmr - 3));
            else if (Əmr == 16 || Əmr == 17) Giriş.add("pushl $" + (Əmr == 16 ? əmr_verilənlər.부호한바이트() : əmr_verilənlər.부호두바이트()));
            else if (Əmr == 18 || Əmr == 19) {
                int INDEX = Əmr == 18 ? əmr_verilənlər.한바이트() : əmr_verilənlər.두바이트();
                Giriş.add("pushl $" + X_86_sabit(Sinif_VALUE,INDEX));
            } else if (Əmr == 21 || Əmr == 25 || (Əmr >= 26 && Əmr <= 29) || (Əmr >= 42 && Əmr <= 45) || Əmr == 54 || Əmr == 58 || (Əmr >= 59 && Əmr <= 62) || (Əmr >= 75 && Əmr <= 78)) {
                boolean 읽음 = Əmr < 54; int INDEX = Əmr == 21 || Əmr == 25 || Əmr == 54 || Əmr == 58 ? əmr_verilənlər.한바이트() : Əmr - (Əmr <= 29 ? 26 : Əmr <= 45 ? 42 : Əmr <= 62 ? 59 : 75);
                çek_lokal(INDEX,lokal_COUNT); Giriş.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Əmr == 46) Collections.addAll(Giriş,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Əmr == 79) Collections.addAll(Giriş,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Əmr == 87 || Əmr == 88) Giriş.add("addl $" + (Əmr == 87 ? 4 : 8) + ", %esp");
            else if (Əmr >= 89 && Əmr <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ardıcıllıq_Siyahı = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Əmr - 89]; 순번++) Giriş.add("popl " + 저장기들[순번]);
                for (int 순번 : ardıcıllıq_Siyahı[Əmr - 89]) Giriş.add("pushl " + 저장기들[순번]);
            } else if (Əmr == 96 || Əmr == 100 || Əmr == 104 || Əmr == 126 || Əmr == 128 || Əmr == 130) {
                String əməliyyat_VALUE = Əmr == 96 ? "addl" : Əmr == 100 ? "subl" : Əmr == 104 ? "imull" : Əmr == 126 ? "andl" : Əmr == 128 ? "orl" : "xorl";
                Collections.addAll(Giriş,"popl %ecx","popl %eax",əməliyyat_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Əmr == 108 || Əmr == 112) Collections.addAll(Giriş,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + yerinə_qoymaq_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + yerinə_qoymaq_INDEX + "_divide","xorl %edx, %edx","jmp " + yerinə_qoymaq_INDEX + "_done",yerinə_qoymaq_INDEX + "_divide:","cltd","idivl %ecx",yerinə_qoymaq_INDEX + "_done:","pushl " + (Əmr == 108 ? "%eax" : "%edx"));
            else if (Əmr == 116) Giriş.add("negl (%esp)");
            else if (Əmr == 120 || Əmr == 122 || Əmr == 124) Collections.addAll(Giriş,"popl %ecx","popl %eax",(Əmr == 120 ? "sall" : Əmr == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Əmr == 132) {
                int INDEX = əmr_verilənlər.한바이트(), 증가 = əmr_verilənlər.부호한바이트(); çek_lokal(INDEX,lokal_COUNT); Giriş.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Əmr >= 145 && Əmr <= 147) Collections.addAll(Giriş,"popl %eax",Əmr == 145 ? "movsbl %al, %eax" : Əmr == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Əmr >= 153 && Əmr <= 166) {
                if (Əmr <= 158) Collections.addAll(Giriş,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Giriş,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int təyinat_VALUE_a0fbc067 = yerinə_qoymaq + əmr_verilənlər.부호두바이트(); qol_Siyahı.add(təyinat_VALUE_a0fbc067); Giriş.add(비교들[Əmr - (Əmr <= 158 ? 153 : 159)] + " " + 표식 + "_b" + təyinat_VALUE_a0fbc067);
            } else if (Əmr == 167 || Əmr == 200) {
                int təyinat_VALUE_a0fbc067 = yerinə_qoymaq + (Əmr == 167 ? əmr_verilənlər.부호두바이트() : əmr_verilənlər.네바이트()); qol_Siyahı.add(təyinat_VALUE_a0fbc067); Giriş.add("jmp " + 표식 + "_b" + təyinat_VALUE_a0fbc067);
            } else if (Əmr == 170 || Əmr == 171) {
                while (əmr_verilənlər.yerinə_qoymaq % 4 != 0) əmr_verilənlər.한바이트();
                int standart_qiymət = yerinə_qoymaq + əmr_verilənlər.네바이트(); qol_Siyahı.add(standart_qiymət); Giriş.add("popl %eax");
                int element_COUNT, 아래 = 0;
                if (Əmr == 170) { 아래 = əmr_verilənlər.네바이트(); int 위 = əmr_verilənlər.네바이트(); long uzunluq_VALUE = (long)위 - 아래 + 1; if (uzunluq_VALUE < 1 || uzunluq_VALUE > (əmr_verilənlər.verilənlər.length - əmr_verilənlər.yerinə_qoymaq) / 4) throw new Tərcümə_səhv("switch klip XƏTA"); element_COUNT = (int)uzunluq_VALUE; }
                else { element_COUNT = əmr_verilənlər.네바이트(); if (element_COUNT < 0 || element_COUNT > (əmr_verilənlər.verilənlər.length - əmr_verilənlər.yerinə_qoymaq) / 8) throw new Tərcümə_səhv("switch Böyüklük XƏTA"); }
                for (int 순번 = 0; 순번 < element_COUNT; 순번++) {
                    int VALUE = Əmr == 170 ? 아래 + 순번 : əmr_verilənlər.네바이트(), təyinat_VALUE_a0fbc067 = yerinə_qoymaq + əmr_verilənlər.네바이트(); qol_Siyahı.add(təyinat_VALUE_a0fbc067);
                    Collections.addAll(Giriş,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + təyinat_VALUE_a0fbc067);
                }
                Giriş.add("jmp " + 표식 + "_b" + standart_qiymət);
            } else if (Əmr == 172 || Əmr == 176 || Əmr == 177) {
                if (Əmr != 177) Giriş.add("popl %eax"); Collections.addAll(Giriş,"leave","ret");
            } else if (Əmr == 178 || Əmr == 179) {
                metod_İstinad İstinad = Sinif_VALUE.İstinad(əmr_verilənlər.두바이트()); if (!필드들.containsKey(İstinad)) throw new Tərcümə_səhv("알 수 없는 sahə_VALUE_0f39cf1c");
                Collections.addAll(Giriş,"call " + simvol("init",İstinad.sahib_VALUE),(Əmr == 178 ? "pushl " : "popl ") + simvol("field",İstinad.부분들()));
            } else if (Əmr == 184) {
                metod_İstinad İstinad = Sinif_VALUE.İstinad(əmr_verilənlər.두바이트()); if (!함수들.containsKey(İstinad)) throw new Tərcümə_səhv("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(İstinad.서술); Collections.addAll(Giriş,"call " + simvol("init",İstinad.sahib_VALUE),"call " + simvol("method",İstinad.부분들()));
                if (!호출형식.인수.isEmpty()) Giriş.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.geri_qaytarmaq_ölçü.equals("V")) Giriş.add("pushl %eax");
            } else if (Əmr == 182) {
                metod_İstinad İstinad = Sinif_VALUE.İstinad(əmr_verilənlər.두바이트());
                if (İstinad.equals(new metod_İstinad("java/lang/String","length","()I"))) Collections.addAll(Giriş,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (İstinad.equals(new metod_İstinad("java/lang/String","charAt","(I)C"))) Collections.addAll(Giriş,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Tərcümə_səhv("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Əmr == 188) {
                if (əmr_verilənlər.한바이트() != 10) throw new Tərcümə_səhv("new int[]만 Dəstək_VALUE"); Collections.addAll(Giriş,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Əmr == 190) Collections.addAll(Giriş,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Əmr == 196) {
                int genişlənmə_VALUE = əmr_verilənlər.한바이트(), INDEX = əmr_verilənlər.두바이트(); çek_lokal(INDEX,lokal_COUNT);
                if (genişlənmə_VALUE == 21 || genişlənmə_VALUE == 25 || genişlənmə_VALUE == 54 || genişlənmə_VALUE == 58) Giriş.add((genişlənmə_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (genişlənmə_VALUE == 132) Giriş.add("addl $" + əmr_verilənlər.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Tərcümə_səhv("wide Əmr 미지원");
            } else if (Əmr == 198 || Əmr == 199) {
                int təyinat_VALUE_a0fbc067 = yerinə_qoymaq + əmr_verilənlər.부호두바이트(); qol_Siyahı.add(təyinat_VALUE_a0fbc067); Collections.addAll(Giriş,"popl %eax","testl %eax, %eax",(Əmr == 198 ? "je " : "jne ") + 표식 + "_b" + təyinat_VALUE_a0fbc067);
            } else throw new Tərcümə_səhv("미지원 Əmr: " + Əmr);
        }
        if (!경계들.containsAll(qol_Siyahı)) throw new Tərcümə_səhv("Əmr 경계가 아닌 곳으로 qol");
        Giriş.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",Giriş);
    }
    String X_86_sabit(Sinif_verilənlər verilənlər, int INDEX) {
        if (verilənlər.상수종류[INDEX] == 3) return verilənlər.sabit_verilənlər[INDEX].toString();
        if (verilənlər.상수종류[INDEX] == 8) return sətir_simvol(verilənlər.문자((Integer)verilənlər.sabit_verilənlər[INDEX]));
        throw new Tərcümə_səhv("정수와 sətir_VALUE 상수만 Dəstək_VALUE");
    }
    String 엑스조립본(String daxiletmə_p, List<String> 내보냄, String hədəf) throws IOException {
        Map<String,String> maşın_cədvəl = new HashMap<>();
        for (String Giriş : Files.readAllLines(resurs_yol.resolve("엑스기계함수.tsv"))) { String[] qoşmaq_VALUE = Giriş.split("\t"); if (qoşmaq_VALUE[0].equals(hədəf)) maşın_cədvəl.put(qoşmaq_VALUE[1] + qoşmaq_VALUE[2],qoşmaq_VALUE[3]); }
        int yerinə_qoymaq_INDEX = daxiletmə_p.lastIndexOf('.'); if (yerinə_qoymaq_INDEX < 0) throw new Tərcümə_səhv("daxiletmə_p təyin_et_VALUE XƏTA");
        String sahib_VALUE = daxiletmə_p.substring(0,yerinə_qoymaq_INDEX).replace('.','/'), metod_daxiletmə_ad = daxiletmə_p.substring(yerinə_qoymaq_INDEX + 1); metod_İstinad daxiletmə_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metod_İstinad İstinad = new metod_İstinad(sahib_VALUE,metod_daxiletmə_ad,서술); if (함수들.containsKey(İstinad)) { if (daxiletmə_p_VALUE != null) throw new Tərcümə_səhv("겹친 daxiletmə_p"); daxiletmə_p_VALUE = İstinad; } }
        if (daxiletmə_p_VALUE == null || (함수들.get(daxiletmə_p_VALUE).müraciət_daxiletmə & 0x100) != 0) throw new Tərcümə_səhv("daxiletmə_p_VALUE FUNCTION_VALUE format_VALUE XƏTA");
        List<String> Giriş = new ArrayList<>(); Giriş.add(".code32");
        for (Sinif_verilənlər verilənlər : 클래스들.values()) {
            String vəziyyət_VALUE = simvol("state",verilənlər.Ad), ilkin_qiymət_vermək = simvol("init",verilənlər.Ad);
            Collections.addAll(Giriş,".bss",".balign 4",vəziyyət_VALUE + ": .long 0",".text",ilkin_qiymət_vermək + ":","cmpl $0, " + vəziyyət_VALUE,"jne " + ilkin_qiymət_vermək + "_done","movl $1, " + vəziyyət_VALUE);
            metod_İstinad 초기화참조 = new metod_İstinad(verilənlər.Ad,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Giriş.add("call " + simvol("method",초기화참조.부분들()));
            Collections.addAll(Giriş,"movl $2, " + vəziyyət_VALUE,ilkin_qiymət_vermək + "_done:","ret");
            for (üzv_verilənlər sahə_VALUE_0f39cf1c : verilənlər.sahə_VALUE_0f39cf1c) {
                byte[] sabit_VALUE = sahə_VALUE_0f39cf1c.atribut_VALUE.get("ConstantValue"); String VALUE = sabit_VALUE == null ? "0" : X_86_sabit(verilənlər,new verilənlər_oxucu(sabit_VALUE).두바이트());
                Collections.addAll(Giriş,".data",".balign 4",simvol("field",verilənlər.Ad,sahə_VALUE_0f39cf1c.Ad,sahə_VALUE_0f39cf1c.서술) + ": .long " + VALUE);
            }
            for (üzv_verilənlər FUNCTION_VALUE : verilənlər.FUNCTION_VALUE) if (!FUNCTION_VALUE.Ad.equals("<init>")) Giriş.add(엑스함수본문(new metod_İstinad(verilənlər.Ad,FUNCTION_VALUE.Ad,FUNCTION_VALUE.서술),FUNCTION_VALUE,maşın_cədvəl,hədəf));
        }
        Collections.addAll(Giriş,".text",".globl java_entry","java_entry:","call " + simvol("init",daxiletmə_p_VALUE.sahib_VALUE),"call " + simvol("method",daxiletmə_p_VALUE.부분들()));
        if (daxiletmə_p_VALUE.서술.equals("()V")) Giriş.add("xorl %eax, %eax"); Giriş.add("ret");
        for (String təyin_et_VALUE : 내보냄) {
            int ayırıcı_VALUE_d8ba4873 = təyin_et_VALUE.indexOf('='); if (ayırıcı_VALUE_d8ba4873 < 1) throw new Tərcümə_səhv("내보내기 təyin_et_VALUE XƏTA");
            String 외부 = təyin_et_VALUE.substring(0,ayırıcı_VALUE_d8ba4873), FUNCTION_VALUE = təyin_et_VALUE.substring(ayırıcı_VALUE_d8ba4873 + 1); int bölmə_ölçü = FUNCTION_VALUE.lastIndexOf('.');
            if (bölmə_ölçü < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tərcümə_səhv("내보내기 simvol XƏTA");
            String Sinif_VALUE = FUNCTION_VALUE.substring(0,bölmə_ölçü).replace('.','/'), Ad = FUNCTION_VALUE.substring(bölmə_ölçü + 1); metod_İstinad seçilmiş_sahə_VALUE = null;
            for (metod_İstinad İstinad : 함수들.keySet()) if (İstinad.sahib_VALUE.equals(Sinif_VALUE) && İstinad.Ad.equals(Ad)) { if (seçilmiş_sahə_VALUE != null) throw new Tərcümə_səhv("겹친 내보내기 hədəf"); seçilmiş_sahə_VALUE = İstinad; }
            if (seçilmiş_sahə_VALUE == null) throw new Tərcümə_səhv("내보낼 함수가 없음");
            Collections.addAll(Giriş,".text",".globl " + 외부,외부 + ":","call " + simvol("init",seçilmiş_sahə_VALUE.sahib_VALUE),"jmp " + simvol("method",seçilmiş_sahə_VALUE.부분들()));
        }
        Giriş.add(".section .rodata");
        for (Map.Entry<String,String> daxiletmə_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Giriş,".balign 4",daxiletmə_VALUE.getValue() + ":",".long " + daxiletmə_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char dərs_VALUE : daxiletmə_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(dərs_VALUE)); if (!단위들.isEmpty()) Giriş.add(".long " + String.join(",",단위들));
        }
        Giriş.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Giriş) + "\n";
    }
    static void icra_etmək_alət(List<String> Əmr) throws Exception {
        if (new ProcessBuilder(Əmr).inheritIO().start().waitFor() != 0) throw new Tərcümə_səhv("qurmaq_mənbə XƏTA: " + Əmr.get(0));
    }
    static String verilənlər_sətir(String Mətn) { return "\"" + Mətn.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Tərcümə(List<Path> 입력들, String hədəf, String daxiletmə_p, List<String> 내보냄, Path 출력, Path resurs_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Sinif_yol = 임시.resolve("classes"); Files.createDirectory(Sinif_yol);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Sinif_yol.toString(),"-sourcepath",Sinif_yol.toString(),"-d",Sinif_yol.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int mənbə_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Tərcümə_səhv("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); mənbə_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Tərcümə_səhv(".java 또는 .class만 Dəstək_VALUE");
            }
            if (mənbə_COUNT > 0) icra_etmək_alət(자바명령);
            try (java.util.stream.Stream<Path> yol_Siyahı = Files.walk(Sinif_yol)) { yol_Siyahı.filter(Cığır -> Cığır.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,hədəf.equals("user") ? "user" : "kernel",262144,resurs_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(daxiletmə_p,내보냄,hədəf); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path alət_yerinə_qoymaq = resurs_VALUE.getParent();
            icra_etmək_alət(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            icra_etmək_alət(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),alət_yerinə_qoymaq.resolve("ümumi_dil_icrası_Dəstək.s").toString()));
            List<String> Bağlan = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (hədəf.equals("kernel")) Bağlan.add("-r");
            else {
                icra_etmək_alət(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),alət_yerinə_qoymaq.resolve(hədəf.equals("user") ? "Başla_istifadəçi_proqram.s" : "리눅스시작.s").toString()));
                Collections.addAll(Bağlan,"-e","_start",임시.resolve("start.o").toString());
                if (hədəf.equals("user")) Collections.addAll(Bağlan,"-T",alət_yerinə_qoymaq.resolve("istifadəçi_keçid_Düzüm.ld").toString());
            }
            Collections.addAll(Bağlan,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); icra_etmək_alət(Bağlan);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path dərc_et_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),dərc_et_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(dərc_et_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(dərc_et_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(hədəf.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simvol_verilənlər = new ArrayList<>(), mənbə_məlumatları = new ArrayList<>();
            for (metod_İstinad İstinad : CONVERT_VALUE.함수들.keySet()) simvol_verilənlər.add(verilənlər_sətir(simvol("method",İstinad.부분들())) + ":" + verilənlər_sətir(İstinad.sahib_VALUE + "." + İstinad.Ad + İstinad.서술));
            for (Path 입력 : 입력들) {
                byte[] heş_fayl = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Mətn = new StringBuilder(); for (byte VALUE : heş_fayl) Mətn.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                mənbə_məlumatları.add(verilənlər_sətir(입력.toAbsolutePath().toString()) + ":" + verilənlər_sətir(Mətn.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + verilənlər_sətir(hədəf) + ",\"entry\":" + verilənlər_sətir(daxiletmə_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simvol_verilənlər) + "},\"sources\":{" + String.join(",",mənbə_məlumatları) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> yol_Siyahı = Files.walk(임시)) { for (Path Cığır : (Iterable<Path>)yol_Siyahı.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Cığır); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String daxiletmə_p = null, hədəf = "kernel", X_86_hədəf = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> yol_Siyahı = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": X_86_hədəf = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Sinif_VALUE.FUNCTION_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export simvol=Sinif_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": daxiletmə_p = 인수[++순번]; break;
                    case "--profile": hədəf = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Tərcümə_səhv("알 수 없는 옵션: " + VALUE); yol_Siyahı.add(Paths.get(VALUE));
                }
            }
            if (daxiletmə_p == null || 출력경로 == null || yol_Siyahı.isEmpty()) throw new Tərcümə_səhv("--entry, -o, Sinif_VALUE 파일이 필요합니다");
            Path resurs_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_hədəf != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_hədəf)) throw new Tərcümə_səhv("알 수 없는 icra_etmək_əmr hədəf");
                X_86_Tərcümə(yol_Siyahı,X_86_hədəf,daxiletmə_p,내보냄,출력경로,resurs_VALUE); return;
            }
            String QAYNAQ = new 기계어미리번역(yol_Siyahı, hədəf, 낱말수, resurs_VALUE).yarat(daxiletmə_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, QAYNAQ, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception XƏTA) { System.err.println("qurmaq_mənbə XƏTA: " + XƏTA.getMessage()); System.exit(1); }
    }
}
