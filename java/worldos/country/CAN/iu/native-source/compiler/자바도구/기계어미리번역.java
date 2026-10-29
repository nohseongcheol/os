// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java naliannuungavik_atuutilik 파일에서 독립 ARM64 커널용 C 원문을 만든다. tuttarvik JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class 번역오류 extends RuntimeException {
        번역오류(String 설명) { super(설명); }
    }
    static final class titiqqat_Uqalimaarut {
        final byte[] titiqqat;
        int 위치;
        titiqqat_Uqalimaarut(byte[] 입력자료) { titiqqat = 입력자료; }
        byte[] 읽기(int takininga_atuutilik) {
            if (takininga_atuutilik < 0 || takininga_atuutilik > titiqqat.length - 위치) throw new 번역오류("잘린 naliannuungavik_atuutilik 또는 piqujijjut titiqqat");
            byte[] 결과 = Arrays.copyOfRange(titiqqat, 위치, 위치 + takininga_atuutilik); 위치 += takininga_atuutilik; return 결과;
        }
        int 한바이트() { if (위치 >= titiqqat.length) throw new 번역오류("잘린 piqujijjut titiqqat"); return titiqqat[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class ilagijaujuq_titiqqat {
        final int pili_Iliniku;
        final String atiq, 서술;
        final Map<String, byte[]> piuluqqutit_atuutilik;
        ilagijaujuq_titiqqat(int pili_atuutilik, String atiq_atuutilik, String 서술값, Map<String, byte[]> piuluqqutit_titiqqat) {
            pili_Iliniku = pili_atuutilik; atiq = atiq_atuutilik; 서술 = 서술값; piuluqqutit_atuutilik = piuluqqutit_titiqqat;
        }
    }
    static final class 함수참조 implements Comparable<함수참조> {
        final String 소유, atiq, 서술;
        함수참조(String 소유값, String atiq_atuutilik, String 서술값) { 소유 = 소유값; atiq = atiq_atuutilik; 서술 = 서술값; }
        String[] 부분들() { return new String[]{소유, atiq, 서술}; }
        public int compareTo(함수참조 ilagijaujuq_atuutilik) {
            int 비교값 = 소유.compareTo(ilagijaujuq_atuutilik.소유);
            if (비교값 == 0) 비교값 = atiq.compareTo(ilagijaujuq_atuutilik.atiq);
            return 비교값 == 0 ? 서술.compareTo(ilagijaujuq_atuutilik.서술) : 비교값;
        }
        public boolean equals(Object ilagijaujuq_atuutilik) { return ilagijaujuq_atuutilik instanceof 함수참조 && compareTo((함수참조) ilagijaujuq_atuutilik) == 0; }
        public int hashCode() { return Objects.hash(소유, atiq, 서술); }
    }
    static final class naliannuungavik_titiqqat {
        final int[] 상수종류;
        final Object[] surragunnangittuq_titiqqat;
        final String atiq;
        final List<ilagijaujuq_titiqqat> kisumuungavik_atuutilik, sugiakkannirut_atuutilik;
        naliannuungavik_titiqqat(Path aqqut) throws IOException {
            titiqqat_Uqalimaarut Uqalimaarut_atuutilik = new titiqqat_Uqalimaarut(Files.readAllBytes(aqqut));
            if (Uqalimaarut_atuutilik.네바이트() != 0xcafebabe) throw new 번역오류("Java naliannuungavik_atuutilik 표식이 아님");
            Uqalimaarut_atuutilik.읽기(4);
            int 개수 = Uqalimaarut_atuutilik.두바이트(); 상수종류 = new int[개수]; surragunnangittuq_titiqqat = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = Uqalimaarut_atuutilik.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int takininga_atuutilik = Uqalimaarut_atuutilik.두바이트();
                        byte[] immikkuuqtuq_Tuqquikkannirvik = Uqalimaarut_atuutilik.읽기(takininga_atuutilik), 길이붙인자료 = new byte[takininga_atuutilik + 2];
                        길이붙인자료[0] = (byte)(takininga_atuutilik >> 8); 길이붙인자료[1] = (byte)takininga_atuutilik;
                        System.arraycopy(immikkuuqtuq_Tuqquikkannirvik, 0, 길이붙인자료, 2, takininga_atuutilik);
                        surragunnangittuq_titiqqat[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: surragunnangittuq_titiqqat[순번] = Uqalimaarut_atuutilik.네바이트(); break;
                    case 4: Uqalimaarut_atuutilik.읽기(4); break;
                    case 5: case 6: Uqalimaarut_atuutilik.읽기(8); 순번++; break;
                    case 7: case 8: case 16: surragunnangittuq_titiqqat[순번] = Uqalimaarut_atuutilik.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        surragunnangittuq_titiqqat[순번] = new int[]{Uqalimaarut_atuutilik.두바이트(), Uqalimaarut_atuutilik.두바이트()}; break;
                    case 15: surragunnangittuq_titiqqat[순번] = new int[]{Uqalimaarut_atuutilik.한바이트(), Uqalimaarut_atuutilik.두바이트()}; break;
                    default: throw new 번역오류("지원하지 않는 surragunnangittuq_atuutilik 종류: " + 종류);
                }
            }
            Uqalimaarut_atuutilik.두바이트(); atiq = naliannuungavik_atiq(Uqalimaarut_atuutilik.두바이트());
            if (!naliannuungavik_atiq(Uqalimaarut_atuutilik.두바이트()).equals("java/lang/Object") || Uqalimaarut_atuutilik.두바이트() != 0)
                throw new 번역오류(atiq + ": 상속 및 인터페이스 미지원");
            kisumuungavik_atuutilik = 멤버읽기(Uqalimaarut_atuutilik); sugiakkannirut_atuutilik = 멤버읽기(Uqalimaarut_atuutilik); 속성읽기(Uqalimaarut_atuutilik);
            if (Uqalimaarut_atuutilik.위치 != Uqalimaarut_atuutilik.titiqqat.length) throw new 번역오류("naliannuungavik_atuutilik 뒤에 남은 titiqqat");
        }
        String 문자(int nalunaiqsimavik) {
            if (nalunaiqsimavik < 1 || nalunaiqsimavik >= 상수종류.length || 상수종류[nalunaiqsimavik] != 1) throw new 번역오류("문자 surragunnangittuq_atuutilik nalunaiqsimavik tammarniq");
            return (String) surragunnangittuq_titiqqat[nalunaiqsimavik];
        }
        String naliannuungavik_atiq(int nalunaiqsimavik) {
            if (nalunaiqsimavik < 1 || nalunaiqsimavik >= 상수종류.length || 상수종류[nalunaiqsimavik] != 7) throw new 번역오류("naliannuungavik_atuutilik 참조 tammarniq");
            return 문자((Integer)surragunnangittuq_titiqqat[nalunaiqsimavik]);
        }
        함수참조 참조(int nalunaiqsimavik) {
            if (nalunaiqsimavik < 1 || nalunaiqsimavik >= 상수종류.length || 상수종류[nalunaiqsimavik] < 9 || 상수종류[nalunaiqsimavik] > 11) throw new 번역오류("멤버 참조 tammarniq");
            int[] igluanuarli_atuutilik = (int[])surragunnangittuq_titiqqat[nalunaiqsimavik], atiq_igluanuarli = (int[])surragunnangittuq_titiqqat[igluanuarli_atuutilik[1]];
            return new 함수참조(naliannuungavik_atiq(igluanuarli_atuutilik[0]), 문자(atiq_igluanuarli[0]), 문자(atiq_igluanuarli[1]));
        }
        Map<String, byte[]> 속성읽기(titiqqat_Uqalimaarut Uqalimaarut_atuutilik) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = Uqalimaarut_atuutilik.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String piuluqqutit_atiq = 문자(Uqalimaarut_atuutilik.두바이트()); byte[] atuutilik = Uqalimaarut_atuutilik.읽기(Uqalimaarut_atuutilik.네바이트());
                if (결과.put(piuluqqutit_atiq, atuutilik) != null) throw new 번역오류("겹친 piuluqqutit_atuutilik: " + piuluqqutit_atiq);
            }
            return 결과;
        }
        List<ilagijaujuq_titiqqat> 멤버읽기(titiqqat_Uqalimaarut Uqalimaarut_atuutilik) {
            List<ilagijaujuq_titiqqat> 결과 = new ArrayList<>(); int 개수 = Uqalimaarut_atuutilik.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int pili_Iliniku = Uqalimaarut_atuutilik.두바이트(); String 함수이름 = 문자(Uqalimaarut_atuutilik.두바이트()), 서술 = 문자(Uqalimaarut_atuutilik.두바이트());
                결과.add(new ilagijaujuq_titiqqat(pili_Iliniku, 함수이름, 서술, 속성읽기(Uqalimaarut_atuutilik)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new 번역오류("sugiakkannirut_atuutilik 서술 tammarniq: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new 번역오류("sugiakkannirut_atuutilik 서술 tammarniq: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new 번역오류("sugiakkannirut_atuutilik 서술 tammarniq: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String nirulussimaniq_atuutilik = null;
            for (String aaqqisurli_atuutilik : 허용형식) if (서술.startsWith(aaqqisurli_atuutilik, 위치)) { nirulussimaniq_atuutilik = aaqqisurli_atuutilik; break; }
            if (nirulussimaniq_atuutilik == null) throw new 번역오류("지원하지 않는 titiqqat_qanuittut: " + 서술);
            결과.add(nirulussimaniq_atuutilik); 위치 += nirulussimaniq_atuutilik.length();
        }
        return 결과;
    }
    static String 기호(String 종류, String... 부분들) {
        try {
            byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder titiqqaq = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) titiqqaq.append(String.format(Locale.ROOT, "%02x", 해시[순번] & 255));
            return titiqqaq.toString();
        } catch (Exception tammarniq) { throw new 번역오류(tammarniq.toString()); }
    }
    final Map<String, naliannuungavik_titiqqat> 클래스들 = new TreeMap<>();
    final Map<함수참조, ilagijaujuq_titiqqat> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, 기계클래스;
    final int 동적기억낱말수;
    final Path qarasaujalirijjutiit_aqqut;
    기계어미리번역(List<Path> aqqut_Titiqpalliagaq, String turaagaq, int 낱말수, Path qarasaujalirijjutiit_atuutilik) throws IOException {
        if ((!turaagaq.equals("kernel") && !turaagaq.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new 번역오류("실행 turaagaq 또는 puigujjaikkut_atuutilik 공간 anininga tammarniq");
        실행대상 = turaagaq; 동적기억낱말수 = 낱말수; qarasaujalirijjutiit_aqqut = qarasaujalirijjutiit_atuutilik;
        // 이 이름도 국가별 pivviujuq_attavigiit 생성 시 해당 언어로 옮긴다.
        기계클래스 = turaagaq.equals("kernel") ? "보드" : "atuqtuq";
        for (String titikutaak : Files.readAllLines(qarasaujalirijjutiit_atuutilik.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = titikutaak.split("\t", -1);
            if (부분들.length != 4) throw new 번역오류("기계 sugiakkannirut_atuutilik titiqqat tammarniq");
            if (부분들[0].equals(turaagaq)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path aqqut : aqqut_Titiqpalliagaq) {
            naliannuungavik_titiqqat titiqqat = new naliannuungavik_titiqqat(aqqut);
            if (클래스들.put(titiqqat.atiq, titiqqat) != null) throw new 번역오류("중복 naliannuungavik_atuutilik: " + titiqqat.atiq);
            for (ilagijaujuq_titiqqat kisumuungavik_atuutilik : titiqqat.kisumuungavik_atuutilik) {
                if ((kisumuungavik_atuutilik.pili_Iliniku & 8) == 0 || 형식읽기(kisumuungavik_atuutilik.서술).equals(Collections.singletonList("V"))) throw new 번역오류("surravviqanngittuq_atuutilik 필드만 ikajuqsuiniq_atuutilik");
                if (필드들.put(new 함수참조(titiqqat.atiq, kisumuungavik_atuutilik.atiq, kisumuungavik_atuutilik.서술), kisumuungavik_atuutilik) != null) throw new 번역오류("중복 kisumuungavik_atuutilik");
            }
            for (ilagijaujuq_titiqqat sugiakkannirut_atuutilik : titiqqat.sugiakkannirut_atuutilik) {
                if (sugiakkannirut_atuutilik.atiq.equals("<init>")) continue;
                if ((sugiakkannirut_atuutilik.pili_Iliniku & 8) == 0 || (sugiakkannirut_atuutilik.pili_Iliniku & (0x20 | 0x400)) != 0) throw new 번역오류("surravviqanngittuq_atuutilik 비동기화 함수만 ikajuqsuiniq_atuutilik");
                new 함수형식(sugiakkannirut_atuutilik.서술);
                if (함수들.put(new 함수참조(titiqqat.atiq, sugiakkannirut_atuutilik.atiq, sugiakkannirut_atuutilik.서술), sugiakkannirut_atuutilik) != null) throw new 번역오류("중복 sugiakkannirut_atuutilik");
            }
        }
    }
    String 문자열기호(String titiqqaq) { return 문자열들.computeIfAbsent(titiqqaq, atuutilik -> "j_text_" + 문자열들.size()); }
    String surragunnangittuq_uqarusiq(naliannuungavik_titiqqat titiqqat, int nalunaiqsimavik) {
        if (nalunaiqsimavik < 1 || nalunaiqsimavik >= titiqqat.상수종류.length) throw new 번역오류("surragunnangittuq_atuutilik nalunaiqsimavik Nakatigat tammarniq");
        if (titiqqat.상수종류[nalunaiqsimavik] == 3) return "(word)(uint32_t)(" + titiqqat.surragunnangittuq_titiqqat[nalunaiqsimavik] + ")";
        if (titiqqat.상수종류[nalunaiqsimavik] == 8) return "(word)" + 문자열기호(titiqqat.문자((Integer)titiqqat.surragunnangittuq_titiqqat[nalunaiqsimavik]));
        throw new 번역오류("정수와 qimiaq_atuutilik 상수만 ikajuqsuiniq_atuutilik");
    }
    String 함수원형(함수참조 참조) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(참조.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + 기호("method", 참조.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void qaujigiarli_tamaani(int nalunaiqsimavik, int 지역변수수) { if (nalunaiqsimavik < 0 || nalunaiqsimavik >= 지역변수수) throw new 번역오류("tamaani_qinirvik 변수 nalunaiqsimavik Nakatigat tammarniq"); }
    void 분기넣기(List<String> 출력, Set<Integer> avalangajuq_Titiqpalliagaq, int 위치, int 이동량, String qanuinniq) {
        int namunngarvik_atuutilik = 위치 + 이동량; avalangajuq_Titiqpalliagaq.add(namunngarvik_atuutilik);
        출력.add((qanuinniq == null ? "" : "if (" + qanuinniq + ") ") + "goto b" + namunngarvik_atuutilik + ";");
    }
    String 함수본문(함수참조 sugiakkannirut_atuutilik, ilagijaujuq_titiqqat titiqqat) {
        byte[] 본문자료 = titiqqat.piuluqqutit_atuutilik.get("Code"); if (본문자료 == null) throw new 번역오류("sugiakkannirut_atuutilik 몸체가 없음: " + sugiakkannirut_atuutilik.atiq);
        titiqqat_Uqalimaarut Uqalimaarut_atuutilik = new titiqqat_Uqalimaarut(본문자료); int 쌓임깊이 = Uqalimaarut_atuutilik.두바이트(), 지역변수수 = Uqalimaarut_atuutilik.두바이트();
        titiqqat_Uqalimaarut piqujijjut_titiqqat = new titiqqat_Uqalimaarut(Uqalimaarut_atuutilik.읽기(Uqalimaarut_atuutilik.네바이트()));
        if (Uqalimaarut_atuutilik.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 aaqqisurli_atuutilik = new 함수형식(sugiakkannirut_atuutilik.서술); if (지역변수수 < aaqqisurli_atuutilik.인수.size()) throw new 번역오류("매개변수보다 적은 tamaani_qinirvik 변수");
        naliannuungavik_titiqqat naliannuungavik_atuutilik = 클래스들.get(sugiakkannirut_atuutilik.소유);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(sugiakkannirut_atuutilik) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < aaqqisurli_atuutilik.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), avalangajuq_Titiqpalliagaq = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (piqujijjut_titiqqat.위치 < piqujijjut_titiqqat.titiqqat.length) {
            int 위치 = piqujijjut_titiqqat.위치, piqujijjut = piqujijjut_titiqqat.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (piqujijjut == 0) continue;
            if (piqujijjut == 1) 출력.add("PUSH(0);");
            else if (piqujijjut >= 2 && piqujijjut <= 8) 출력.add("PUSH((uint32_t)(" + (piqujijjut - 3) + "));");
            else if (piqujijjut == 16 || piqujijjut == 17) 출력.add("PUSH((uint32_t)(" + (piqujijjut == 16 ? piqujijjut_titiqqat.부호한바이트() : piqujijjut_titiqqat.부호두바이트()) + "));");
            else if (piqujijjut == 18 || piqujijjut == 19) 출력.add("PUSH(" + surragunnangittuq_uqarusiq(naliannuungavik_atuutilik, piqujijjut == 18 ? piqujijjut_titiqqat.한바이트() : piqujijjut_titiqqat.두바이트()) + ");");
            else if (piqujijjut == 21 || piqujijjut == 25 || (piqujijjut >= 26 && piqujijjut <= 29) || (piqujijjut >= 42 && piqujijjut <= 45)) {
                int nalunaiqsimavik = piqujijjut == 21 || piqujijjut == 25 ? piqujijjut_titiqqat.한바이트() : piqujijjut - (piqujijjut <= 29 ? 26 : 42);
                qaujigiarli_tamaani(nalunaiqsimavik, 지역변수수); 출력.add("PUSH(l[" + nalunaiqsimavik + "]);");
            } else if (piqujijjut == 54 || piqujijjut == 58 || (piqujijjut >= 59 && piqujijjut <= 62) || (piqujijjut >= 75 && piqujijjut <= 78)) {
                int nalunaiqsimavik = piqujijjut == 54 || piqujijjut == 58 ? piqujijjut_titiqqat.한바이트() : piqujijjut - (piqujijjut <= 62 ? 59 : 75);
                qaujigiarli_tamaani(nalunaiqsimavik, 지역변수수); 출력.add("l[" + nalunaiqsimavik + "] = POP();");
            } else if (piqujijjut == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (piqujijjut == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (piqujijjut == 87 || piqujijjut == 88) 출력.add(piqujijjut == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (piqujijjut >= 89 && piqujijjut <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] agguijjut_Titiqpalliagaq = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[piqujijjut - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char atuutilik : agguijjut_Titiqpalliagaq[piqujijjut - 89].toCharArray()) 출력.add("PUSH(" + atuutilik + ");");
            } else if (piqujijjut == 96 || piqujijjut == 100 || piqujijjut == 104 || piqujijjut == 126 || piqujijjut == 128 || piqujijjut == 130) {
                String aulattiniq_atuutilik = piqujijjut == 96 ? "+" : piqujijjut == 100 ? "-" : piqujijjut == 104 ? "*" : piqujijjut == 126 ? "&" : piqujijjut == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + aulattiniq_atuutilik + " (uint32_t)b);");
            } else if (piqujijjut == 108 || piqujijjut == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (piqujijjut == 112 ? 1 : 0) + "));");
            else if (piqujijjut == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (piqujijjut == 120 || piqujijjut == 122 || piqujijjut == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (piqujijjut == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (piqujijjut == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (piqujijjut == 132) {
                int nalunaiqsimavik = piqujijjut_titiqqat.한바이트(), 증가량 = piqujijjut_titiqqat.부호한바이트(); qaujigiarli_tamaani(nalunaiqsimavik, 지역변수수);
                출력.add("l[" + nalunaiqsimavik + "] = (uint32_t)l[" + nalunaiqsimavik + "] + (uint32_t)(" + 증가량 + ");");
            } else if (piqujijjut >= 145 && piqujijjut <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (piqujijjut == 145 ? "int8_t" : piqujijjut == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (piqujijjut >= 153 && piqujijjut <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, avalangajuq_Titiqpalliagaq, 위치, piqujijjut_titiqqat.부호두바이트(), "(int32_t)a " + 비교들[piqujijjut - 153] + " 0");
            } else if (piqujijjut >= 159 && piqujijjut <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, avalangajuq_Titiqpalliagaq, 위치, piqujijjut_titiqqat.부호두바이트(), piqujijjut >= 165 ? "a " + 비교들[piqujijjut - 159] + " b" : "(int32_t)a " + 비교들[piqujijjut - 159] + " (int32_t)b");
            } else if (piqujijjut == 167 || piqujijjut == 200) 분기넣기(출력, avalangajuq_Titiqpalliagaq, 위치, piqujijjut == 167 ? piqujijjut_titiqqat.부호두바이트() : piqujijjut_titiqqat.네바이트(), null);
            else if (piqujijjut == 170 || piqujijjut == 171) {
                while (piqujijjut_titiqqat.위치 % 4 != 0) piqujijjut_titiqqat.한바이트();
                int Aturniliuvagiiqtut = piqujijjut_titiqqat.네바이트(); 출력.add("a = POP();");
                if (piqujijjut == 170) {
                    int 아래 = piqujijjut_titiqqat.네바이트(), 위 = piqujijjut_titiqqat.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (piqujijjut_titiqqat.titiqqat.length - piqujijjut_titiqqat.위치) / 4) throw new 번역오류("switch Nakatigat tammarniq");
                    for (long atuutilik = 아래; atuutilik <= 위; atuutilik++) 분기넣기(출력, avalangajuq_Titiqpalliagaq, 위치, piqujijjut_titiqqat.네바이트(), "(int32_t)a == (" + atuutilik + ")");
                } else {
                    int 개수 = piqujijjut_titiqqat.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (piqujijjut_titiqqat.titiqqat.length - piqujijjut_titiqqat.위치) / 8) throw new 번역오류("switch anininga tammarniq");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int atuutilik = piqujijjut_titiqqat.네바이트(); if (순번 > 0 && atuutilik <= 앞값) throw new 번역오류("switch agguijjut_atuutilik tammarniq"); 앞값 = atuutilik;
                        분기넣기(출력, avalangajuq_Titiqpalliagaq, 위치, piqujijjut_titiqqat.네바이트(), "(int32_t)a == (" + atuutilik + ")");
                    }
                }
                분기넣기(출력, avalangajuq_Titiqpalliagaq, 위치, Aturniliuvagiiqtut, null);
            } else if (piqujijjut == 172 || piqujijjut == 176 || piqujijjut == 177) 출력.add("return " + (piqujijjut == 177 ? "0" : "POP()") + ";");
            else if (piqujijjut == 178 || piqujijjut == 179) {
                함수참조 참조 = naliannuungavik_atuutilik.참조(piqujijjut_titiqqat.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 kisumuungavik_atuutilik");
                출력.add(기호("init", 참조.소유) + "();"); String kisumuungavik_atuutilik = 기호("field", 참조.부분들());
                출력.add(piqujijjut == 178 ? "PUSH(" + kisumuungavik_atuutilik + ");" : kisumuungavik_atuutilik + " = POP();");
            } else if (piqujijjut == 184) {
                함수참조 참조 = naliannuungavik_atuutilik.참조(piqujijjut_titiqqat.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 sugiakkannirut_atuutilik");
                함수형식 호출형식 = new 함수형식(참조.서술); int 개수 = 호출형식.인수.size();
                출력.add(기호("init", 참조.소유) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + 기호("method", 참조.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (piqujijjut == 182) {
                함수참조 참조 = naliannuungavik_atuutilik.참조(piqujijjut_titiqqat.두바이트());
                if (참조.equals(new 함수참조("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (참조.equals(new 함수참조("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 번역오류("가상 sugiakkannirut_atuutilik 호출 미지원");
            } else if (piqujijjut == 188) {
                if (piqujijjut_titiqqat.한바이트() != 10) throw new 번역오류("new int[]만 ikajuqsuiniq_atuutilik"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (piqujijjut == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (piqujijjut == 196) {
                int uigu_atuutilik = piqujijjut_titiqqat.한바이트(), nalunaiqsimavik = piqujijjut_titiqqat.두바이트(); qaujigiarli_tamaani(nalunaiqsimavik, 지역변수수);
                if (uigu_atuutilik == 21 || uigu_atuutilik == 25) 출력.add("PUSH(l[" + nalunaiqsimavik + "]);");
                else if (uigu_atuutilik == 54 || uigu_atuutilik == 58) 출력.add("l[" + nalunaiqsimavik + "] = POP();");
                else if (uigu_atuutilik == 132) 출력.add("l[" + nalunaiqsimavik + "] = (uint32_t)l[" + nalunaiqsimavik + "] + (uint32_t)(" + piqujijjut_titiqqat.부호두바이트() + ");");
                else throw new 번역오류("미지원 wide piqujijjut");
            } else if (piqujijjut == 198 || piqujijjut == 199) {
                출력.add("a = POP();"); 분기넣기(출력, avalangajuq_Titiqpalliagaq, 위치, piqujijjut_titiqqat.부호두바이트(), "a " + (piqujijjut == 198 ? "==" : "!=") + " 0");
            } else throw new 번역오류(sugiakkannirut_atuutilik.소유 + "." + sugiakkannirut_atuutilik.atiq + ", byte_atuutilik " + 위치 + ": 미지원 piqujijjut " + piqujijjut);
        }
        if (!경계들.containsAll(avalangajuq_Titiqpalliagaq)) throw new 번역오류("piqujijjut 경계가 아닌 곳으로 avalangajuq");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String 내보낼함수(String 연결기호, String turaagaq, boolean 진입점여부) {
        int 자리 = turaagaq.lastIndexOf('.'); if (자리 < 0 || !연결기호.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 지정 tammarniq");
        String 소유 = turaagaq.substring(0, 자리).replace('.', '/'), atiq = turaagaq.substring(자리 + 1); 함수참조 nirulussimaniq_atuutilik = null;
        for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(소유) && 참조.atiq.equals(atiq)) {
            if (nirulussimaniq_atuutilik != null) throw new 번역오류("겹친 내보내기 turaagaq"); nirulussimaniq_atuutilik = 참조;
        }
        if (nirulussimaniq_atuutilik == null || (함수들.get(nirulussimaniq_atuutilik).pili_Iliniku & 0x100) != 0) throw new 번역오류("내보낼 함수가 없음 또는 native sugiakkannirut_atuutilik");
        함수형식 aaqqisurli_atuutilik = new 함수형식(nirulussimaniq_atuutilik.서술);
        if ((진입점여부 && !aaqqisurli_atuutilik.인수.isEmpty()) || !Arrays.asList("V", "I").contains(aaqqisurli_atuutilik.반환)) throw new 번역오류("Iliniku_puinti_atuutilik 또는 C 경계 aaqqisurli_atuutilik tammarniq");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < aaqqisurli_atuutilik.인수.size(); 순번++) {
            if (!aaqqisurli_atuutilik.인수.get(순번).equals("I")) throw new 번역오류("C 경계는 int 인수만 ikajuqsuiniq_atuutilik");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (aaqqisurli_atuutilik.반환.equals("V") ? "void " : "int32_t ") + 연결기호 + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + 기호("init", nirulussimaniq_atuutilik.소유) + "(); " + (aaqqisurli_atuutilik.반환.equals("V") ? "" : "return (int32_t)") + 기호("method", nirulussimaniq_atuutilik.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String Iliniku_puinti, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<함수참조, ilagijaujuq_titiqqat> Iliniku_atuutilik : 함수들.entrySet()) {
            함수참조 참조 = Iliniku_atuutilik.getKey(); ilagijaujuq_titiqqat titiqqat = Iliniku_atuutilik.getValue(); 선언들.add(함수원형(참조) + ";");
            if ((titiqqat.pili_Iliniku & 0x100) != 0) {
                String kasurli = 기계함수들.get(참조.atiq + 참조.서술);
                if (!참조.소유.equals(기계클래스) || kasurli == null) throw new 번역오류("허용되지 않은 native sugiakkannirut_atuutilik: " + 참조.atiq);
                int 개수 = new 함수형식(참조.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + kasurli + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(참조) + " { return " + kasurli + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(참조, titiqqat));
        }
        for (Map.Entry<함수참조, ilagijaujuq_titiqqat> Iliniku_atuutilik : 필드들.entrySet()) {
            함수참조 참조 = Iliniku_atuutilik.getKey(); byte[] surragunnangittuq_atuutilik = Iliniku_atuutilik.getValue().piuluqqutit_atuutilik.get("ConstantValue");
            String atuutilik = surragunnangittuq_atuutilik == null ? "0" : surragunnangittuq_uqarusiq(클래스들.get(참조.소유), new titiqqat_Uqalimaarut(surragunnangittuq_atuutilik).두바이트());
            필드선언들.add("static word " + 기호("field", 참조.부분들()) + " = " + atuutilik + ";");
        }
        for (String atiq : 클래스들.keySet()) {
            String aturunnaqsili = 기호("init", atiq), qanuilinganiq_atuutilik = 기호("state", atiq);
            선언들.add("static void " + aturunnaqsili + "(void);"); 필드선언들.add("static unsigned " + qanuilinganiq_atuutilik + ";");
            함수참조 참조 = new 함수참조(atiq, "<clinit>", "()V");
            몸체들.add("static void " + aturunnaqsili + "(void) { if(" + qanuilinganiq_atuutilik + ") return; " + qanuilinganiq_atuutilik + " = 1; " + (함수들.containsKey(참조) ? 기호("method", 참조.부분들()) + "(); " : "") + qanuilinganiq_atuutilik + " = 2; }");
        }
        몸체들.add(내보낼함수("java_entry", Iliniku_puinti, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new 번역오류("내보내기 지정 tammarniq");
            String atiq = 지정.substring(0, 자리); 공개이름.add(atiq); 몸체들.add(내보낼함수(atiq, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> Iliniku_atuutilik : 문자열들.entrySet()) {
            String titiqqaq = Iliniku_atuutilik.getKey(); StringBuilder array_atuutilik = new StringBuilder("static const word " + Iliniku_atuutilik.getValue() + "[] = {" + titiqqaq.length());
            for (int 순번 = 0; 순번 < titiqqaq.length(); 순번++) array_atuutilik.append(", ").append((int)titiqqaq.charAt(순번));
            문자열선언들.add(array_atuutilik.append("};").toString());
        }
        String ikajuqsuiniq_atuutilik = Files.readString(qarasaujalirijjutiit_aqqut.resolve("실행지원.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(ikajuqsuiniq_atuutilik + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String pivviujuq, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> atiq_kipu = new HashMap<>();
        for (String titikutaak : Files.readAllLines(qarasaujalirijjutiit_aqqut.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] igluanuarli_atuutilik = titikutaak.split("\t"); atiq_kipu.put(igluanuarli_atuutilik[0], igluanuarli_atuutilik[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(pivviujuq); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String atiq = 찾개.group(), 새이름 = atiq;
            if (!atiq.startsWith("//") && !atiq.startsWith("/*") && !atiq.startsWith("\"") && !atiq.startsWith("'") && !공개이름.contains(atiq)) {
                새이름 = atiq_kipu.getOrDefault(atiq, atiq);
                if (atiq.matches("a[0-9]+")) 새이름 = "인수" + atiq.substring(1);
                if (atiq.matches("b[0-9]+")) 새이름 = "avalangajuq" + atiq.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char immikkuuqtuq_atuutilik : 새이름.toCharArray()) 표기.append(immikkuuqtuq_atuutilik < 128 ? Character.toString(immikkuuqtuq_atuutilik) : String.format(Locale.ROOT, "\\u%04x", (int)immikkuuqtuq_atuutilik));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(함수참조 sugiakkannirut_atuutilik, ilagijaujuq_titiqqat titiqqat, Map<String,String> 기계표, String turaagaq) {
        String 표식 = 기호("method", sugiakkannirut_atuutilik.부분들());
        List<String> titikutaak = new ArrayList<>();
        if ((titiqqat.pili_Iliniku & 0x100) != 0) {
            String kasurli = 기계표.get(sugiakkannirut_atuutilik.atiq + sugiakkannirut_atuutilik.서술);
            if (!sugiakkannirut_atuutilik.소유.equals(turaagaq.equals("kernel") ? "sunakkutaaq_atuutilik" : "atuqtuq") || kasurli == null) throw new 번역오류("허용되지 않은 native sugiakkannirut_atuutilik");
            return ".text\n" + 표식 + ":\njmp " + kasurli;
        }
        byte[] Titiqqaup_ilulilluataa = titiqqat.piuluqqutit_atuutilik.get("Code"); if (Titiqqaup_ilulilluataa == null) throw new 번역오류("sugiakkannirut_atuutilik 몸체가 없음");
        titiqqat_Uqalimaarut Uqalimaarut_atuutilik = new titiqqat_Uqalimaarut(Titiqqaup_ilulilluataa); Uqalimaarut_atuutilik.두바이트(); int 지역수 = Uqalimaarut_atuutilik.두바이트();
        titiqqat_Uqalimaarut piqujijjut_titiqqat = new titiqqat_Uqalimaarut(Uqalimaarut_atuutilik.읽기(Uqalimaarut_atuutilik.네바이트()));
        if (Uqalimaarut_atuutilik.두바이트() != 0) throw new 번역오류("try/catch/finally 미지원");
        함수형식 aaqqisurli_atuutilik = new 함수형식(sugiakkannirut_atuutilik.서술); if (지역수 < aaqqisurli_atuutilik.인수.size()) throw new 번역오류("매개변수보다 적은 tamaani_qinirvik 변수");
        Collections.addAll(titikutaak,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < aaqqisurli_atuutilik.인수.size(); 순번++) Collections.addAll(titikutaak,"movl " + (8 + 4 * (aaqqisurli_atuutilik.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        naliannuungavik_titiqqat naliannuungavik_atuutilik = 클래스들.get(sugiakkannirut_atuutilik.소유); Set<Integer> 경계들 = new HashSet<>(), avalangajuq_Titiqpalliagaq = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (piqujijjut_titiqqat.위치 < piqujijjut_titiqqat.titiqqat.length) {
            int 위치 = piqujijjut_titiqqat.위치, piqujijjut = piqujijjut_titiqqat.한바이트(); String 자리 = 표식 + "_b" + 위치;
            titikutaak.add(자리 + ":"); 경계들.add(위치);
            if (piqujijjut == 0) titikutaak.add("nop");
            else if (piqujijjut == 1) titikutaak.add("pushl $0");
            else if (piqujijjut >= 2 && piqujijjut <= 8) titikutaak.add("pushl $" + (piqujijjut - 3));
            else if (piqujijjut == 16 || piqujijjut == 17) titikutaak.add("pushl $" + (piqujijjut == 16 ? piqujijjut_titiqqat.부호한바이트() : piqujijjut_titiqqat.부호두바이트()));
            else if (piqujijjut == 18 || piqujijjut == 19) {
                int nalunaiqsimavik = piqujijjut == 18 ? piqujijjut_titiqqat.한바이트() : piqujijjut_titiqqat.두바이트();
                titikutaak.add("pushl $" + 엑스상수(naliannuungavik_atuutilik,nalunaiqsimavik));
            } else if (piqujijjut == 21 || piqujijjut == 25 || (piqujijjut >= 26 && piqujijjut <= 29) || (piqujijjut >= 42 && piqujijjut <= 45) || piqujijjut == 54 || piqujijjut == 58 || (piqujijjut >= 59 && piqujijjut <= 62) || (piqujijjut >= 75 && piqujijjut <= 78)) {
                boolean 읽음 = piqujijjut < 54; int nalunaiqsimavik = piqujijjut == 21 || piqujijjut == 25 || piqujijjut == 54 || piqujijjut == 58 ? piqujijjut_titiqqat.한바이트() : piqujijjut - (piqujijjut <= 29 ? 26 : piqujijjut <= 45 ? 42 : piqujijjut <= 62 ? 59 : 75);
                qaujigiarli_tamaani(nalunaiqsimavik,지역수); titikutaak.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (nalunaiqsimavik + 1)) + "(%ebp)");
            } else if (piqujijjut == 46) Collections.addAll(titikutaak,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (piqujijjut == 79) Collections.addAll(titikutaak,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (piqujijjut == 87 || piqujijjut == 88) titikutaak.add("addl $" + (piqujijjut == 87 ? 4 : 8) + ", %esp");
            else if (piqujijjut >= 89 && piqujijjut <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] agguijjut_Titiqpalliagaq = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[piqujijjut - 89]; 순번++) titikutaak.add("popl " + 저장기들[순번]);
                for (int 순번 : agguijjut_Titiqpalliagaq[piqujijjut - 89]) titikutaak.add("pushl " + 저장기들[순번]);
            } else if (piqujijjut == 96 || piqujijjut == 100 || piqujijjut == 104 || piqujijjut == 126 || piqujijjut == 128 || piqujijjut == 130) {
                String aulattiniq_atuutilik = piqujijjut == 96 ? "addl" : piqujijjut == 100 ? "subl" : piqujijjut == 104 ? "imull" : piqujijjut == 126 ? "andl" : piqujijjut == 128 ? "orl" : "xorl";
                Collections.addAll(titikutaak,"popl %ecx","popl %eax",aulattiniq_atuutilik + " %ecx, %eax","pushl %eax");
            } else if (piqujijjut == 108 || piqujijjut == 112) Collections.addAll(titikutaak,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (piqujijjut == 108 ? "%eax" : "%edx"));
            else if (piqujijjut == 116) titikutaak.add("negl (%esp)");
            else if (piqujijjut == 120 || piqujijjut == 122 || piqujijjut == 124) Collections.addAll(titikutaak,"popl %ecx","popl %eax",(piqujijjut == 120 ? "sall" : piqujijjut == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (piqujijjut == 132) {
                int nalunaiqsimavik = piqujijjut_titiqqat.한바이트(), 증가 = piqujijjut_titiqqat.부호한바이트(); qaujigiarli_tamaani(nalunaiqsimavik,지역수); titikutaak.add("addl $" + 증가 + ", -" + (4 * (nalunaiqsimavik + 1)) + "(%ebp)");
            } else if (piqujijjut >= 145 && piqujijjut <= 147) Collections.addAll(titikutaak,"popl %eax",piqujijjut == 145 ? "movsbl %al, %eax" : piqujijjut == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (piqujijjut >= 153 && piqujijjut <= 166) {
                if (piqujijjut <= 158) Collections.addAll(titikutaak,"popl %eax","testl %eax, %eax");
                else Collections.addAll(titikutaak,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int namunngarvik_atuutilik = 위치 + piqujijjut_titiqqat.부호두바이트(); avalangajuq_Titiqpalliagaq.add(namunngarvik_atuutilik); titikutaak.add(비교들[piqujijjut - (piqujijjut <= 158 ? 153 : 159)] + " " + 표식 + "_b" + namunngarvik_atuutilik);
            } else if (piqujijjut == 167 || piqujijjut == 200) {
                int namunngarvik_atuutilik = 위치 + (piqujijjut == 167 ? piqujijjut_titiqqat.부호두바이트() : piqujijjut_titiqqat.네바이트()); avalangajuq_Titiqpalliagaq.add(namunngarvik_atuutilik); titikutaak.add("jmp " + 표식 + "_b" + namunngarvik_atuutilik);
            } else if (piqujijjut == 170 || piqujijjut == 171) {
                while (piqujijjut_titiqqat.위치 % 4 != 0) piqujijjut_titiqqat.한바이트();
                int Aturniliuvagiiqtut = 위치 + piqujijjut_titiqqat.네바이트(); avalangajuq_Titiqpalliagaq.add(Aturniliuvagiiqtut); titikutaak.add("popl %eax");
                int 개수, 아래 = 0;
                if (piqujijjut == 170) { 아래 = piqujijjut_titiqqat.네바이트(); int 위 = piqujijjut_titiqqat.네바이트(); long takininga_atuutilik = (long)위 - 아래 + 1; if (takininga_atuutilik < 1 || takininga_atuutilik > (piqujijjut_titiqqat.titiqqat.length - piqujijjut_titiqqat.위치) / 4) throw new 번역오류("switch Nakatigat tammarniq"); 개수 = (int)takininga_atuutilik; }
                else { 개수 = piqujijjut_titiqqat.네바이트(); if (개수 < 0 || 개수 > (piqujijjut_titiqqat.titiqqat.length - piqujijjut_titiqqat.위치) / 8) throw new 번역오류("switch anininga tammarniq"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int atuutilik = piqujijjut == 170 ? 아래 + 순번 : piqujijjut_titiqqat.네바이트(), namunngarvik_atuutilik = 위치 + piqujijjut_titiqqat.네바이트(); avalangajuq_Titiqpalliagaq.add(namunngarvik_atuutilik);
                    Collections.addAll(titikutaak,"cmpl $" + atuutilik + ", %eax","je " + 표식 + "_b" + namunngarvik_atuutilik);
                }
                titikutaak.add("jmp " + 표식 + "_b" + Aturniliuvagiiqtut);
            } else if (piqujijjut == 172 || piqujijjut == 176 || piqujijjut == 177) {
                if (piqujijjut != 177) titikutaak.add("popl %eax"); Collections.addAll(titikutaak,"leave","ret");
            } else if (piqujijjut == 178 || piqujijjut == 179) {
                함수참조 참조 = naliannuungavik_atuutilik.참조(piqujijjut_titiqqat.두바이트()); if (!필드들.containsKey(참조)) throw new 번역오류("알 수 없는 kisumuungavik_atuutilik");
                Collections.addAll(titikutaak,"call " + 기호("init",참조.소유),(piqujijjut == 178 ? "pushl " : "popl ") + 기호("field",참조.부분들()));
            } else if (piqujijjut == 184) {
                함수참조 참조 = naliannuungavik_atuutilik.참조(piqujijjut_titiqqat.두바이트()); if (!함수들.containsKey(참조)) throw new 번역오류("알 수 없는 sugiakkannirut_atuutilik");
                함수형식 호출형식 = new 함수형식(참조.서술); Collections.addAll(titikutaak,"call " + 기호("init",참조.소유),"call " + 기호("method",참조.부분들()));
                if (!호출형식.인수.isEmpty()) titikutaak.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) titikutaak.add("pushl %eax");
            } else if (piqujijjut == 182) {
                함수참조 참조 = naliannuungavik_atuutilik.참조(piqujijjut_titiqqat.두바이트());
                if (참조.equals(new 함수참조("java/lang/String","length","()I"))) Collections.addAll(titikutaak,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (참조.equals(new 함수참조("java/lang/String","charAt","(I)C"))) Collections.addAll(titikutaak,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 번역오류("가상 sugiakkannirut_atuutilik 호출 미지원");
            } else if (piqujijjut == 188) {
                if (piqujijjut_titiqqat.한바이트() != 10) throw new 번역오류("new int[]만 ikajuqsuiniq_atuutilik"); Collections.addAll(titikutaak,"popl %eax","call rt_new_array","pushl %eax");
            } else if (piqujijjut == 190) Collections.addAll(titikutaak,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (piqujijjut == 196) {
                int uigu_atuutilik = piqujijjut_titiqqat.한바이트(), nalunaiqsimavik = piqujijjut_titiqqat.두바이트(); qaujigiarli_tamaani(nalunaiqsimavik,지역수);
                if (uigu_atuutilik == 21 || uigu_atuutilik == 25 || uigu_atuutilik == 54 || uigu_atuutilik == 58) titikutaak.add((uigu_atuutilik <= 25 ? "pushl " : "popl ") + "-" + 4 * (nalunaiqsimavik + 1) + "(%ebp)");
                else if (uigu_atuutilik == 132) titikutaak.add("addl $" + piqujijjut_titiqqat.부호두바이트() + ", -" + 4 * (nalunaiqsimavik + 1) + "(%ebp)");
                else throw new 번역오류("wide piqujijjut 미지원");
            } else if (piqujijjut == 198 || piqujijjut == 199) {
                int namunngarvik_atuutilik = 위치 + piqujijjut_titiqqat.부호두바이트(); avalangajuq_Titiqpalliagaq.add(namunngarvik_atuutilik); Collections.addAll(titikutaak,"popl %eax","testl %eax, %eax",(piqujijjut == 198 ? "je " : "jne ") + 표식 + "_b" + namunngarvik_atuutilik);
            } else throw new 번역오류("미지원 piqujijjut: " + piqujijjut);
        }
        if (!경계들.containsAll(avalangajuq_Titiqpalliagaq)) throw new 번역오류("piqujijjut 경계가 아닌 곳으로 avalangajuq");
        titikutaak.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",titikutaak);
    }
    String 엑스상수(naliannuungavik_titiqqat titiqqat, int nalunaiqsimavik) {
        if (titiqqat.상수종류[nalunaiqsimavik] == 3) return titiqqat.surragunnangittuq_titiqqat[nalunaiqsimavik].toString();
        if (titiqqat.상수종류[nalunaiqsimavik] == 8) return 문자열기호(titiqqat.문자((Integer)titiqqat.surragunnangittuq_titiqqat[nalunaiqsimavik]));
        throw new 번역오류("정수와 qimiaq_atuutilik 상수만 ikajuqsuiniq_atuutilik");
    }
    String 엑스조립본(String Iliniku_puinti, List<String> 내보냄, String turaagaq) throws IOException {
        Map<String,String> 기계표 = new HashMap<>();
        for (String titikutaak : Files.readAllLines(qarasaujalirijjutiit_aqqut.resolve("엑스기계함수.tsv"))) { String[] igluanuarli_atuutilik = titikutaak.split("\t"); if (igluanuarli_atuutilik[0].equals(turaagaq)) 기계표.put(igluanuarli_atuutilik[1] + igluanuarli_atuutilik[2],igluanuarli_atuutilik[3]); }
        int 자리 = Iliniku_puinti.lastIndexOf('.'); if (자리 < 0) throw new 번역오류("Iliniku_puinti 지정 tammarniq");
        String 소유 = Iliniku_puinti.substring(0,자리).replace('.','/'), 함수이름 = Iliniku_puinti.substring(자리 + 1); 함수참조 Iliniku_puinti_atuutilik = null;
        for (String 서술 : Arrays.asList("()I","()V")) { 함수참조 참조 = new 함수참조(소유,함수이름,서술); if (함수들.containsKey(참조)) { if (Iliniku_puinti_atuutilik != null) throw new 번역오류("겹친 Iliniku_puinti"); Iliniku_puinti_atuutilik = 참조; } }
        if (Iliniku_puinti_atuutilik == null || (함수들.get(Iliniku_puinti_atuutilik).pili_Iliniku & 0x100) != 0) throw new 번역오류("Iliniku_puinti_atuutilik sugiakkannirut_atuutilik aaqqisurli_atuutilik tammarniq");
        List<String> titikutaak = new ArrayList<>(); titikutaak.add(".code32");
        for (naliannuungavik_titiqqat titiqqat : 클래스들.values()) {
            String qanuilinganiq_atuutilik = 기호("state",titiqqat.atiq), aturunnaqsili = 기호("init",titiqqat.atiq);
            Collections.addAll(titikutaak,".bss",".balign 4",qanuilinganiq_atuutilik + ": .long 0",".text",aturunnaqsili + ":","cmpl $0, " + qanuilinganiq_atuutilik,"jne " + aturunnaqsili + "_done","movl $1, " + qanuilinganiq_atuutilik);
            함수참조 초기화참조 = new 함수참조(titiqqat.atiq,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) titikutaak.add("call " + 기호("method",초기화참조.부분들()));
            Collections.addAll(titikutaak,"movl $2, " + qanuilinganiq_atuutilik,aturunnaqsili + "_done:","ret");
            for (ilagijaujuq_titiqqat kisumuungavik_atuutilik : titiqqat.kisumuungavik_atuutilik) {
                byte[] surragunnangittuq_atuutilik = kisumuungavik_atuutilik.piuluqqutit_atuutilik.get("ConstantValue"); String atuutilik = surragunnangittuq_atuutilik == null ? "0" : 엑스상수(titiqqat,new titiqqat_Uqalimaarut(surragunnangittuq_atuutilik).두바이트());
                Collections.addAll(titikutaak,".data",".balign 4",기호("field",titiqqat.atiq,kisumuungavik_atuutilik.atiq,kisumuungavik_atuutilik.서술) + ": .long " + atuutilik);
            }
            for (ilagijaujuq_titiqqat sugiakkannirut_atuutilik : titiqqat.sugiakkannirut_atuutilik) if (!sugiakkannirut_atuutilik.atiq.equals("<init>")) titikutaak.add(엑스함수본문(new 함수참조(titiqqat.atiq,sugiakkannirut_atuutilik.atiq,sugiakkannirut_atuutilik.서술),sugiakkannirut_atuutilik,기계표,turaagaq));
        }
        Collections.addAll(titikutaak,".text",".globl java_entry","java_entry:","call " + 기호("init",Iliniku_puinti_atuutilik.소유),"call " + 기호("method",Iliniku_puinti_atuutilik.부분들()));
        if (Iliniku_puinti_atuutilik.서술.equals("()V")) titikutaak.add("xorl %eax, %eax"); titikutaak.add("ret");
        for (String 지정 : 내보냄) {
            int isuaguurut_atuutilik = 지정.indexOf('='); if (isuaguurut_atuutilik < 1) throw new 번역오류("내보내기 지정 tammarniq");
            String 외부 = 지정.substring(0,isuaguurut_atuutilik), sugiakkannirut_atuutilik = 지정.substring(isuaguurut_atuutilik + 1); int 나눔 = sugiakkannirut_atuutilik.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 번역오류("내보내기 기호 tammarniq");
            String naliannuungavik_atuutilik = sugiakkannirut_atuutilik.substring(0,나눔).replace('.','/'), atiq = sugiakkannirut_atuutilik.substring(나눔 + 1); 함수참조 nirulussimaniq_atuutilik = null;
            for (함수참조 참조 : 함수들.keySet()) if (참조.소유.equals(naliannuungavik_atuutilik) && 참조.atiq.equals(atiq)) { if (nirulussimaniq_atuutilik != null) throw new 번역오류("겹친 내보내기 turaagaq"); nirulussimaniq_atuutilik = 참조; }
            if (nirulussimaniq_atuutilik == null) throw new 번역오류("내보낼 함수가 없음");
            Collections.addAll(titikutaak,".text",".globl " + 외부,외부 + ":","call " + 기호("init",nirulussimaniq_atuutilik.소유),"jmp " + 기호("method",nirulussimaniq_atuutilik.부분들()));
        }
        titikutaak.add(".section .rodata");
        for (Map.Entry<String,String> Iliniku_atuutilik : 문자열들.entrySet()) {
            Collections.addAll(titikutaak,".balign 4",Iliniku_atuutilik.getValue() + ":",".long " + Iliniku_atuutilik.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char atauttimiittut_atuutilik : Iliniku_atuutilik.getKey().toCharArray()) 단위들.add(Integer.toString(atauttimiittut_atuutilik)); if (!단위들.isEmpty()) titikutaak.add(".long " + String.join(",",단위들));
        }
        titikutaak.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",titikutaak) + "\n";
    }
    static void 도구실행(List<String> piqujijjut) throws Exception {
        if (new ProcessBuilder(piqujijjut).inheritIO().start().waitFor() != 0) throw new 번역오류("sanali_pivviujuq tammarniq: " + piqujijjut.get(0));
    }
    static String titiqqat_qimiaq(String titiqqaq) { return "\"" + titiqqaq.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String turaagaq, String Iliniku_puinti, List<String> 내보냄, Path 출력, Path qarasaujalirijjutiit_atuutilik) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), naliannuungavik_aqqut = 임시.resolve("classes"); Files.createDirectory(naliannuungavik_aqqut);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",naliannuungavik_aqqut.toString(),"-sourcepath",naliannuungavik_aqqut.toString(),"-d",naliannuungavik_aqqut.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new 번역오류("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new 번역오류(".java 또는 .class만 ikajuqsuiniq_atuutilik");
            }
            if (원문수 > 0) 도구실행(자바명령);
            try (java.util.stream.Stream<Path> aqqut_Titiqpalliagaq = Files.walk(naliannuungavik_aqqut)) { aqqut_Titiqpalliagaq.filter(aqqut -> aqqut.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,turaagaq.equals("user") ? "user" : "kernel",262144,qarasaujalirijjutiit_atuutilik);
            String 조립 = 변환.엑스조립본(Iliniku_puinti,내보냄,turaagaq); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = qarasaujalirijjutiit_atuutilik.getParent();
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            도구실행(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("실행지원.s").toString()));
            List<String> kasurli = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (turaagaq.equals("kernel")) kasurli.add("-r");
            else {
                도구실행(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(turaagaq.equals("user") ? "pigiarli_atuqtuq_pilirijjut.s" : "리눅스시작.s").toString()));
                Collections.addAll(kasurli,"-e","_start",임시.resolve("start.o").toString());
                if (turaagaq.equals("user")) Collections.addAll(kasurli,"-T",도구위치.resolve("atuqtuq_kasurvik_ilinganinga.ld").toString());
            }
            Collections.addAll(kasurli,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); 도구실행(kasurli);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path saqqitilli_atuutilik = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),saqqitilli_atuutilik,StandardCopyOption.REPLACE_EXISTING); Files.move(saqqitilli_atuutilik,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(saqqitilli_atuutilik); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(turaagaq.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> 기호자료 = new ArrayList<>(), titiqqanik_nakinngaarvik = new ArrayList<>();
            for (함수참조 참조 : 변환.함수들.keySet()) 기호자료.add(titiqqat_qimiaq(기호("method",참조.부분들())) + ":" + titiqqat_qimiaq(참조.소유 + "." + 참조.atiq + 참조.서술));
            for (Path 입력 : 입력들) {
                byte[] 해시 = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder titiqqaq = new StringBuilder(); for (byte atuutilik : 해시) titiqqaq.append(String.format(Locale.ROOT,"%02x",atuutilik & 255));
                titiqqanik_nakinngaarvik.add(titiqqat_qimiaq(입력.toAbsolutePath().toString()) + ":" + titiqqat_qimiaq(titiqqaq.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + titiqqat_qimiaq(turaagaq) + ",\"entry\":" + titiqqat_qimiaq(Iliniku_puinti) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",기호자료) + "},\"sources\":{" + String.join(",",titiqqanik_nakinngaarvik) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> aqqut_Titiqpalliagaq = Files.walk(임시)) { for (Path aqqut : (Iterable<Path>)aqqut_Titiqpalliagaq.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(aqqut); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String Iliniku_puinti = null, turaagaq = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> aqqut_Titiqpalliagaq = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String atuutilik = 인수[순번];
                switch (atuutilik) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry naliannuungavik_atuutilik.sugiakkannirut_atuutilik -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export 기호=naliannuungavik_atuutilik.sugiakkannirut_atuutilik] 클래스파일 또는 Java원문"); return;
                    case "--entry": Iliniku_puinti = 인수[++순번]; break;
                    case "--profile": turaagaq = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (atuutilik.startsWith("-")) throw new 번역오류("알 수 없는 옵션: " + atuutilik); aqqut_Titiqpalliagaq.add(Paths.get(atuutilik));
                }
            }
            if (Iliniku_puinti == null || 출력경로 == null || aqqut_Titiqpalliagaq.isEmpty()) throw new 번역오류("--entry, -o, naliannuungavik_atuutilik 파일이 필요합니다");
            Path qarasaujalirijjutiit_atuutilik = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new 번역오류("알 수 없는 실행 turaagaq");
                엑스번역(aqqut_Titiqpalliagaq,엑스대상,Iliniku_puinti,내보냄,출력경로,qarasaujalirijjutiit_atuutilik); return;
            }
            String pivviujuq = new 기계어미리번역(aqqut_Titiqpalliagaq, turaagaq, 낱말수, qarasaujalirijjutiit_atuutilik).생성(Iliniku_puinti, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, pivviujuq, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception tammarniq) { System.err.println("sanali_pivviujuq tammarniq: " + tammarniq.getMessage()); System.exit(1); }
    }
}
