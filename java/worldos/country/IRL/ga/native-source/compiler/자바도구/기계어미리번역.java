// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java aicme_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. óstach JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Aistriúchán_earráid extends RuntimeException {
        Aistriúchán_earráid(String 설명) { super(설명); }
    }
    static final class sonraí_Léitheoir {
        final byte[] sonraí;
        int suíomh;
        sonraí_Léitheoir(byte[] 입력자료) { sonraí = 입력자료; }
        byte[] Léigh(int fad_VALUE) {
            if (fad_VALUE < 0 || fad_VALUE > sonraí.length - suíomh) throw new Aistriúchán_earráid("잘린 aicme_VALUE 또는 Ordú sonraí");
            byte[] tomhas = Arrays.copyOfRange(sonraí, suíomh, suíomh + fad_VALUE); suíomh += fad_VALUE; return tomhas;
        }
        int 한바이트() { if (suíomh >= sonraí.length) throw new Aistriúchán_earráid("잘린 Ordú sonraí"); return sonraí[suíomh++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class ball_sonraí {
        final int rochtain_iontráil;
        final String Ainm, 서술;
        final Map<String, byte[]> tréith_VALUE;
        ball_sonraí(int rochtain_VALUE, String ainm_VALUE, String 서술값, Map<String, byte[]> tréith_sonraí) {
            rochtain_iontráil = rochtain_VALUE; Ainm = ainm_VALUE; 서술 = 서술값; tréith_VALUE = tréith_sonraí;
        }
    }
    static final class modh_Leabhair_thagartha implements Comparable<modh_Leabhair_thagartha> {
        final String úinéir_VALUE, Ainm, 서술;
        modh_Leabhair_thagartha(String 소유값, String ainm_VALUE, String 서술값) { úinéir_VALUE = 소유값; Ainm = ainm_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{úinéir_VALUE, Ainm, 서술}; }
        public int compareTo(modh_Leabhair_thagartha piara_VALUE) {
            int 비교값 = úinéir_VALUE.compareTo(piara_VALUE.úinéir_VALUE);
            if (비교값 == 0) 비교값 = Ainm.compareTo(piara_VALUE.Ainm);
            return 비교값 == 0 ? 서술.compareTo(piara_VALUE.서술) : 비교값;
        }
        public boolean equals(Object piara_VALUE) { return piara_VALUE instanceof modh_Leabhair_thagartha && compareTo((modh_Leabhair_thagartha) piara_VALUE) == 0; }
        public int hashCode() { return Objects.hash(úinéir_VALUE, Ainm, 서술); }
    }
    static final class aicme_sonraí {
        final int[] 상수종류;
        final Object[] tairiseach_sonraí;
        final String Ainm;
        final List<ball_sonraí> réimse_VALUE, feidhm_VALUE;
        aicme_sonraí(Path CONAIR) throws IOException {
            sonraí_Léitheoir Léitheoir_VALUE = new sonraí_Léitheoir(Files.readAllBytes(CONAIR));
            if (Léitheoir_VALUE.네바이트() != 0xcafebabe) throw new Aistriúchán_earráid("Java aicme_VALUE 표식이 아님");
            Léitheoir_VALUE.Léigh(4);
            int mír_COUNT = Léitheoir_VALUE.두바이트(); 상수종류 = new int[mír_COUNT]; tairiseach_sonraí = new Object[mír_COUNT];
            for (int 순번 = 1; 순번 < mír_COUNT; 순번++) {
                int 종류 = Léitheoir_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int fad_VALUE = Léitheoir_VALUE.두바이트();
                        byte[] carachtar_maolán = Léitheoir_VALUE.Léigh(fad_VALUE), 길이붙인자료 = new byte[fad_VALUE + 2];
                        길이붙인자료[0] = (byte)(fad_VALUE >> 8); 길이붙인자료[1] = (byte)fad_VALUE;
                        System.arraycopy(carachtar_maolán, 0, 길이붙인자료, 2, fad_VALUE);
                        tairiseach_sonraí[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: tairiseach_sonraí[순번] = Léitheoir_VALUE.네바이트(); break;
                    case 4: Léitheoir_VALUE.Léigh(4); break;
                    case 5: case 6: Léitheoir_VALUE.Léigh(8); 순번++; break;
                    case 7: case 8: case 16: tairiseach_sonraí[순번] = Léitheoir_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        tairiseach_sonraí[순번] = new int[]{Léitheoir_VALUE.두바이트(), Léitheoir_VALUE.두바이트()}; break;
                    case 15: tairiseach_sonraí[순번] = new int[]{Léitheoir_VALUE.한바이트(), Léitheoir_VALUE.두바이트()}; break;
                    default: throw new Aistriúchán_earráid("지원하지 않는 tairiseach_VALUE 종류: " + 종류);
                }
            }
            Léitheoir_VALUE.두바이트(); Ainm = aicme_ainm(Léitheoir_VALUE.두바이트());
            if (!aicme_ainm(Léitheoir_VALUE.두바이트()).equals("java/lang/Object") || Léitheoir_VALUE.두바이트() != 0)
                throw new Aistriúchán_earráid(Ainm + ": 상속 및 인터페이스 미지원");
            réimse_VALUE = 멤버읽기(Léitheoir_VALUE); feidhm_VALUE = 멤버읽기(Léitheoir_VALUE); 속성읽기(Léitheoir_VALUE);
            if (Léitheoir_VALUE.suíomh != Léitheoir_VALUE.sonraí.length) throw new Aistriúchán_earráid("aicme_VALUE 뒤에 남은 sonraí");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Aistriúchán_earráid("문자 tairiseach_VALUE INDEX ERREÁID");
            return (String) tairiseach_sonraí[INDEX];
        }
        String aicme_ainm(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Aistriúchán_earráid("aicme_VALUE Leabhair_thagartha ERREÁID");
            return 문자((Integer)tairiseach_sonraí[INDEX]);
        }
        modh_Leabhair_thagartha Leabhair_thagartha(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Aistriúchán_earráid("멤버 Leabhair_thagartha ERREÁID");
            int[] péireáil_VALUE = (int[])tairiseach_sonraí[INDEX], ainm_péireáil = (int[])tairiseach_sonraí[péireáil_VALUE[1]];
            return new modh_Leabhair_thagartha(aicme_ainm(péireáil_VALUE[0]), 문자(ainm_péireáil[0]), 문자(ainm_péireáil[1]));
        }
        Map<String, byte[]> 속성읽기(sonraí_Léitheoir Léitheoir_VALUE) {
            Map<String, byte[]> tomhas = new LinkedHashMap<>();
            int mír_COUNT = Léitheoir_VALUE.두바이트();
            for (int 순번 = 0; 순번 < mír_COUNT; 순번++) {
                String tréith_ainm = 문자(Léitheoir_VALUE.두바이트()); byte[] VALUE = Léitheoir_VALUE.Léigh(Léitheoir_VALUE.네바이트());
                if (tomhas.put(tréith_ainm, VALUE) != null) throw new Aistriúchán_earráid("겹친 tréith_VALUE: " + tréith_ainm);
            }
            return tomhas;
        }
        List<ball_sonraí> 멤버읽기(sonraí_Léitheoir Léitheoir_VALUE) {
            List<ball_sonraí> tomhas = new ArrayList<>(); int mír_COUNT = Léitheoir_VALUE.두바이트();
            for (int 순번 = 0; 순번 < mír_COUNT; 순번++) {
                int rochtain_iontráil = Léitheoir_VALUE.두바이트(); String modh_iontráil_ainm = 문자(Léitheoir_VALUE.두바이트()), 서술 = 문자(Léitheoir_VALUE.두바이트());
                tomhas.add(new ball_sonraí(rochtain_iontráil, modh_iontráil_ainm, 서술, 속성읽기(Léitheoir_VALUE)));
            }
            return tomhas;
        }
    }
    static final class 함수형식 {
        final List<String> Argóintí = new ArrayList<>();
        final String return_tomhas;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Aistriúchán_earráid("feidhm_VALUE 서술 ERREÁID: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Aistriúchán_earráid("feidhm_VALUE 서술 ERREÁID: " + 서술);
            Argóintí.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argóintí.contains("V") || 반환들.size() != 1) throw new Aistriúchán_earráid("feidhm_VALUE 서술 ERREÁID: " + 서술);
            return_tomhas = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> tomhas = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int suíomh = 0; suíomh < 서술.length();) {
            String roghnú_VALUE = null;
            for (String formáid_VALUE : 허용형식) if (서술.startsWith(formáid_VALUE, suíomh)) { roghnú_VALUE = formáid_VALUE; break; }
            if (roghnú_VALUE == null) throw new Aistriúchán_earráid("지원하지 않는 cineál_sonraí: " + 서술);
            tomhas.add(roghnú_VALUE); suíomh += roghnú_VALUE.length();
        }
        return tomhas;
    }
    static String siombail(String 종류, String... 부분들) {
        try {
            byte[] hais_comhad = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Téacs = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Téacs.append(String.format(Locale.ROOT, "%02x", hais_comhad[순번] & 255));
            return Téacs.toString();
        } catch (Exception ERREÁID) { throw new Aistriúchán_earráid(ERREÁID.toString()); }
    }
    final Map<String, aicme_sonraí> 클래스들 = new TreeMap<>();
    final Map<modh_Leabhair_thagartha, ball_sonraí> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, meaisín_aicme;
    final int 동적기억낱말수;
    final Path acmhainn_cosán;
    기계어미리번역(List<Path> cosán_Liosta, String sprioc, int 낱말수, Path acmhainn_VALUE) throws IOException {
        if ((!sprioc.equals("kernel") && !sprioc.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Aistriúchán_earráid("Rith_ordú sprioc 또는 Cuimhne_VALUE 공간 Méid ERREÁID");
        실행대상 = sprioc; 동적기억낱말수 = 낱말수; acmhainn_cosán = acmhainn_VALUE;
        // 이 이름도 국가별 foinse_crann giniúint 시 해당 언어로 옮긴다.
        meaisín_aicme = sprioc.equals("kernel") ? "clár" : "úsáideoir";
        for (String Líne : Files.readAllLines(acmhainn_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Líne.split("\t", -1);
            if (부분들.length != 4) throw new Aistriúchán_earráid("meaisín feidhm_VALUE sonraí ERREÁID");
            if (부분들[0].equals(sprioc)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path CONAIR : cosán_Liosta) {
            aicme_sonraí sonraí = new aicme_sonraí(CONAIR);
            if (클래스들.put(sonraí.Ainm, sonraí) != null) throw new Aistriúchán_earráid("중복 aicme_VALUE: " + sonraí.Ainm);
            for (ball_sonraí réimse_VALUE : sonraí.réimse_VALUE) {
                if ((réimse_VALUE.rochtain_iontráil & 8) == 0 || 형식읽기(réimse_VALUE.서술).equals(Collections.singletonList("V"))) throw new Aistriúchán_earráid("statach_VALUE 필드만 Tacaíocht_VALUE");
                if (필드들.put(new modh_Leabhair_thagartha(sonraí.Ainm, réimse_VALUE.Ainm, réimse_VALUE.서술), réimse_VALUE) != null) throw new Aistriúchán_earráid("중복 réimse_VALUE");
            }
            for (ball_sonraí feidhm_VALUE : sonraí.feidhm_VALUE) {
                if (feidhm_VALUE.Ainm.equals("<init>")) continue;
                if ((feidhm_VALUE.rochtain_iontráil & 8) == 0 || (feidhm_VALUE.rochtain_iontráil & (0x20 | 0x400)) != 0) throw new Aistriúchán_earráid("statach_VALUE 비동기화 함수만 Tacaíocht_VALUE");
                new 함수형식(feidhm_VALUE.서술);
                if (함수들.put(new modh_Leabhair_thagartha(sonraí.Ainm, feidhm_VALUE.Ainm, feidhm_VALUE.서술), feidhm_VALUE) != null) throw new Aistriúchán_earráid("중복 feidhm_VALUE");
            }
        }
    }
    String teaghrán_siombail(String Téacs) { return 문자열들.computeIfAbsent(Téacs, VALUE -> "j_text_" + 문자열들.size()); }
    String tairiseach_slonn(aicme_sonraí sonraí, int INDEX) {
        if (INDEX < 1 || INDEX >= sonraí.상수종류.length) throw new Aistriúchán_earráid("tairiseach_VALUE INDEX gearrthóg ERREÁID");
        if (sonraí.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + sonraí.tairiseach_sonraí[INDEX] + ")";
        if (sonraí.상수종류[INDEX] == 8) return "(word)" + teaghrán_siombail(sonraí.문자((Integer)sonraí.tairiseach_sonraí[INDEX]));
        throw new Aistriúchán_earráid("정수와 teaghrán_VALUE 상수만 Tacaíocht_VALUE");
    }
    String 함수원형(modh_Leabhair_thagartha Leabhair_thagartha) {
        List<String> 인수들 = new ArrayList<>(); int mír_COUNT = new 함수형식(Leabhair_thagartha.서술).Argóintí.size();
        for (int 순번 = 0; 순번 < mír_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + siombail("method", Leabhair_thagartha.부분들()) + "(" + (mír_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void seic_logánta(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Aistriúchán_earráid("logánta_scóip 변수 INDEX gearrthóg ERREÁID"); }
    void 분기넣기(List<String> Aschur, Set<Integer> craobh_Liosta, int suíomh, int 이동량, String coinníoll) {
        int sprioc_VALUE = suíomh + 이동량; craobh_Liosta.add(sprioc_VALUE);
        Aschur.add((coinníoll == null ? "" : "if (" + coinníoll + ") ") + "goto b" + sprioc_VALUE + ";");
    }
    String modh_corp(modh_Leabhair_thagartha feidhm_VALUE, ball_sonraí sonraí) {
        byte[] corp_sonraí = sonraí.tréith_VALUE.get("Code"); if (corp_sonraí == null) throw new Aistriúchán_earráid("feidhm_VALUE 몸체가 없음: " + feidhm_VALUE.Ainm);
        sonraí_Léitheoir Léitheoir_VALUE = new sonraí_Léitheoir(corp_sonraí); int 쌓임깊이 = Léitheoir_VALUE.두바이트(), 지역변수수 = Léitheoir_VALUE.두바이트();
        sonraí_Léitheoir ordú_sonraí = new sonraí_Léitheoir(Léitheoir_VALUE.Léigh(Léitheoir_VALUE.네바이트()));
        if (Léitheoir_VALUE.두바이트() != 0) throw new Aistriúchán_earráid("try/catch/finally 미지원");
        함수형식 formáid_VALUE = new 함수형식(feidhm_VALUE.서술); if (지역변수수 < formáid_VALUE.Argóintí.size()) throw new Aistriúchán_earráid("매개변수보다 적은 logánta_scóip 변수");
        aicme_sonraí aicme_VALUE = 클래스들.get(feidhm_VALUE.úinéir_VALUE);
        List<String> Aschur = new ArrayList<>(); Aschur.add(함수원형(feidhm_VALUE) + " {");
        Aschur.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formáid_VALUE.Argóintí.size(); 순번++) Aschur.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), craobh_Liosta = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (ordú_sonraí.suíomh < ordú_sonraí.sonraí.length) {
            int suíomh = ordú_sonraí.suíomh, Ordú = ordú_sonraí.한바이트(); 경계들.add(suíomh); Aschur.add("b" + suíomh + ":;");
            if (Ordú == 0) continue;
            if (Ordú == 1) Aschur.add("PUSH(0);");
            else if (Ordú >= 2 && Ordú <= 8) Aschur.add("PUSH((uint32_t)(" + (Ordú - 3) + "));");
            else if (Ordú == 16 || Ordú == 17) Aschur.add("PUSH((uint32_t)(" + (Ordú == 16 ? ordú_sonraí.부호한바이트() : ordú_sonraí.부호두바이트()) + "));");
            else if (Ordú == 18 || Ordú == 19) Aschur.add("PUSH(" + tairiseach_slonn(aicme_VALUE, Ordú == 18 ? ordú_sonraí.한바이트() : ordú_sonraí.두바이트()) + ");");
            else if (Ordú == 21 || Ordú == 25 || (Ordú >= 26 && Ordú <= 29) || (Ordú >= 42 && Ordú <= 45)) {
                int INDEX = Ordú == 21 || Ordú == 25 ? ordú_sonraí.한바이트() : Ordú - (Ordú <= 29 ? 26 : 42);
                seic_logánta(INDEX, 지역변수수); Aschur.add("PUSH(l[" + INDEX + "]);");
            } else if (Ordú == 54 || Ordú == 58 || (Ordú >= 59 && Ordú <= 62) || (Ordú >= 75 && Ordú <= 78)) {
                int INDEX = Ordú == 54 || Ordú == 58 ? ordú_sonraí.한바이트() : Ordú - (Ordú <= 62 ? 59 : 75);
                seic_logánta(INDEX, 지역변수수); Aschur.add("l[" + INDEX + "] = POP();");
            } else if (Ordú == 46) Aschur.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Ordú == 79) Aschur.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Ordú == 87 || Ordú == 88) Aschur.add(Ordú == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Ordú >= 89 && Ordú <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ord_Liosta = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Ordú - 89]; 순번++) Aschur.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : ord_Liosta[Ordú - 89].toCharArray()) Aschur.add("PUSH(" + VALUE + ");");
            } else if (Ordú == 96 || Ordú == 100 || Ordú == 104 || Ordú == 126 || Ordú == 128 || Ordú == 130) {
                String oibríocht_VALUE = Ordú == 96 ? "+" : Ordú == 100 ? "-" : Ordú == 104 ? "*" : Ordú == 126 ? "&" : Ordú == 128 ? "|" : "^";
                Aschur.add("b = POP(); a = POP(); PUSH((uint32_t)a " + oibríocht_VALUE + " (uint32_t)b);");
            } else if (Ordú == 108 || Ordú == 112) Aschur.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Ordú == 112 ? 1 : 0) + "));");
            else if (Ordú == 116) Aschur.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Ordú == 120 || Ordú == 122 || Ordú == 124) {
                Aschur.add("b = POP(); a = POP();"); Aschur.add("PUSH(" + (Ordú == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Ordú == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Ordú == 132) {
                int INDEX = ordú_sonraí.한바이트(), 증가량 = ordú_sonraí.부호한바이트(); seic_logánta(INDEX, 지역변수수);
                Aschur.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Ordú >= 145 && Ordú <= 147) Aschur.add("a = POP(); PUSH((uint32_t)(" + (Ordú == 145 ? "int8_t" : Ordú == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Ordú >= 153 && Ordú <= 158) {
                Aschur.add("a = POP();"); 분기넣기(Aschur, craobh_Liosta, suíomh, ordú_sonraí.부호두바이트(), "(int32_t)a " + 비교들[Ordú - 153] + " 0");
            } else if (Ordú >= 159 && Ordú <= 166) {
                Aschur.add("b = POP(); a = POP();"); 분기넣기(Aschur, craobh_Liosta, suíomh, ordú_sonraí.부호두바이트(), Ordú >= 165 ? "a " + 비교들[Ordú - 159] + " b" : "(int32_t)a " + 비교들[Ordú - 159] + " (int32_t)b");
            } else if (Ordú == 167 || Ordú == 200) 분기넣기(Aschur, craobh_Liosta, suíomh, Ordú == 167 ? ordú_sonraí.부호두바이트() : ordú_sonraí.네바이트(), null);
            else if (Ordú == 170 || Ordú == 171) {
                while (ordú_sonraí.suíomh % 4 != 0) ordú_sonraí.한바이트();
                int luach_réamhshocraithe = ordú_sonraí.네바이트(); Aschur.add("a = POP();");
                if (Ordú == 170) {
                    int 아래 = ordú_sonraí.네바이트(), 위 = ordú_sonraí.네바이트(); long mír_COUNT = (long)위 - 아래 + 1;
                    if (mír_COUNT < 1 || mír_COUNT > (ordú_sonraí.sonraí.length - ordú_sonraí.suíomh) / 4) throw new Aistriúchán_earráid("switch gearrthóg ERREÁID");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Aschur, craobh_Liosta, suíomh, ordú_sonraí.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int mír_COUNT = ordú_sonraí.네바이트(), 앞값 = 0;
                    if (mír_COUNT < 0 || mír_COUNT > (ordú_sonraí.sonraí.length - ordú_sonraí.suíomh) / 8) throw new Aistriúchán_earráid("switch Méid ERREÁID");
                    for (int 순번 = 0; 순번 < mír_COUNT; 순번++) {
                        int VALUE = ordú_sonraí.네바이트(); if (순번 > 0 && VALUE <= 앞값) throw new Aistriúchán_earráid("switch ord_VALUE ERREÁID"); 앞값 = VALUE;
                        분기넣기(Aschur, craobh_Liosta, suíomh, ordú_sonraí.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Aschur, craobh_Liosta, suíomh, luach_réamhshocraithe, null);
            } else if (Ordú == 172 || Ordú == 176 || Ordú == 177) Aschur.add("return " + (Ordú == 177 ? "0" : "POP()") + ";");
            else if (Ordú == 178 || Ordú == 179) {
                modh_Leabhair_thagartha Leabhair_thagartha = aicme_VALUE.Leabhair_thagartha(ordú_sonraí.두바이트()); if (!필드들.containsKey(Leabhair_thagartha)) throw new Aistriúchán_earráid("알 수 없는 réimse_VALUE");
                Aschur.add(siombail("init", Leabhair_thagartha.úinéir_VALUE) + "();"); String réimse_VALUE = siombail("field", Leabhair_thagartha.부분들());
                Aschur.add(Ordú == 178 ? "PUSH(" + réimse_VALUE + ");" : réimse_VALUE + " = POP();");
            } else if (Ordú == 184) {
                modh_Leabhair_thagartha Leabhair_thagartha = aicme_VALUE.Leabhair_thagartha(ordú_sonraí.두바이트()); if (!함수들.containsKey(Leabhair_thagartha)) throw new Aistriúchán_earráid("알 수 없는 feidhm_VALUE");
                함수형식 호출형식 = new 함수형식(Leabhair_thagartha.서술); int mír_COUNT = 호출형식.Argóintí.size();
                Aschur.add(siombail("init", Leabhair_thagartha.úinéir_VALUE) + "();"); Aschur.add("if(sp < " + mír_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + mír_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < mír_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Aschur.add("a = " + siombail("method", Leabhair_thagartha.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.return_tomhas.equals("V")) Aschur.add("PUSH(a);");
            } else if (Ordú == 182) {
                modh_Leabhair_thagartha Leabhair_thagartha = aicme_VALUE.Leabhair_thagartha(ordú_sonraí.두바이트());
                if (Leabhair_thagartha.equals(new modh_Leabhair_thagartha("java/lang/String", "length", "()I"))) Aschur.add("a = POP(); PUSH(length(a));");
                else if (Leabhair_thagartha.equals(new modh_Leabhair_thagartha("java/lang/String", "charAt", "(I)C"))) Aschur.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Aistriúchán_earráid("가상 feidhm_VALUE 호출 미지원");
            } else if (Ordú == 188) {
                if (ordú_sonraí.한바이트() != 10) throw new Aistriúchán_earráid("new int[]만 Tacaíocht_VALUE"); Aschur.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Ordú == 190) Aschur.add("a = POP(); PUSH(length(a));");
            else if (Ordú == 196) {
                int breisiú_VALUE = ordú_sonraí.한바이트(), INDEX = ordú_sonraí.두바이트(); seic_logánta(INDEX, 지역변수수);
                if (breisiú_VALUE == 21 || breisiú_VALUE == 25) Aschur.add("PUSH(l[" + INDEX + "]);");
                else if (breisiú_VALUE == 54 || breisiú_VALUE == 58) Aschur.add("l[" + INDEX + "] = POP();");
                else if (breisiú_VALUE == 132) Aschur.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + ordú_sonraí.부호두바이트() + ");");
                else throw new Aistriúchán_earráid("미지원 wide Ordú");
            } else if (Ordú == 198 || Ordú == 199) {
                Aschur.add("a = POP();"); 분기넣기(Aschur, craobh_Liosta, suíomh, ordú_sonraí.부호두바이트(), "a " + (Ordú == 198 ? "==" : "!=") + " 0");
            } else throw new Aistriúchán_earráid(feidhm_VALUE.úinéir_VALUE + "." + feidhm_VALUE.Ainm + ", beart_VALUE " + suíomh + ": 미지원 Ordú " + Ordú);
        }
        if (!경계들.containsAll(craobh_Liosta)) throw new Aistriúchán_earráid("Ordú 경계가 아닌 곳으로 craobh");
        Aschur.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Aschur);
    }
    String easportáil_modh(String Nasc_siombail, String sprioc, boolean 진입점여부) {
        int suíomh_INDEX = sprioc.lastIndexOf('.'); if (suíomh_INDEX < 0 || !Nasc_siombail.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Aistriúchán_earráid("내보내기 지정 ERREÁID");
        String úinéir_VALUE = sprioc.substring(0, suíomh_INDEX).replace('.', '/'), Ainm = sprioc.substring(suíomh_INDEX + 1); modh_Leabhair_thagartha roghnú_VALUE = null;
        for (modh_Leabhair_thagartha Leabhair_thagartha : 함수들.keySet()) if (Leabhair_thagartha.úinéir_VALUE.equals(úinéir_VALUE) && Leabhair_thagartha.Ainm.equals(Ainm)) {
            if (roghnú_VALUE != null) throw new Aistriúchán_earráid("겹친 내보내기 sprioc"); roghnú_VALUE = Leabhair_thagartha;
        }
        if (roghnú_VALUE == null || (함수들.get(roghnú_VALUE).rochtain_iontráil & 0x100) != 0) throw new Aistriúchán_earráid("내보낼 함수가 없음 또는 native feidhm_VALUE");
        함수형식 formáid_VALUE = new 함수형식(roghnú_VALUE.서술);
        if ((진입점여부 && !formáid_VALUE.Argóintí.isEmpty()) || !Arrays.asList("V", "I").contains(formáid_VALUE.return_tomhas)) throw new Aistriúchán_earráid("iontráil_pointe_VALUE 또는 C 경계 formáid_VALUE ERREÁID");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formáid_VALUE.Argóintí.size(); 순번++) {
            if (!formáid_VALUE.Argóintí.get(순번).equals("I")) throw new Aistriúchán_earráid("C 경계는 int 인수만 Tacaíocht_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formáid_VALUE.return_tomhas.equals("V") ? "void " : "int32_t ") + Nasc_siombail + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + siombail("init", roghnú_VALUE.úinéir_VALUE) + "(); " + (formáid_VALUE.return_tomhas.equals("V") ? "" : "return (int32_t)") + siombail("method", roghnú_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String giniúint(String iontráil_pointe, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<modh_Leabhair_thagartha, ball_sonraí> iontráil_VALUE : 함수들.entrySet()) {
            modh_Leabhair_thagartha Leabhair_thagartha = iontráil_VALUE.getKey(); ball_sonraí sonraí = iontráil_VALUE.getValue(); 선언들.add(함수원형(Leabhair_thagartha) + ";");
            if ((sonraí.rochtain_iontráil & 0x100) != 0) {
                String Nasc = 기계함수들.get(Leabhair_thagartha.Ainm + Leabhair_thagartha.서술);
                if (!Leabhair_thagartha.úinéir_VALUE.equals(meaisín_aicme) || Nasc == null) throw new Aistriúchán_earráid("허용되지 않은 native feidhm_VALUE: " + Leabhair_thagartha.Ainm);
                int mír_COUNT = new 함수형식(Leabhair_thagartha.서술).Argóintí.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < mír_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Nasc + "(" + (mír_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(mír_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Leabhair_thagartha) + " { return " + Nasc + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(modh_corp(Leabhair_thagartha, sonraí));
        }
        for (Map.Entry<modh_Leabhair_thagartha, ball_sonraí> iontráil_VALUE : 필드들.entrySet()) {
            modh_Leabhair_thagartha Leabhair_thagartha = iontráil_VALUE.getKey(); byte[] tairiseach_VALUE = iontráil_VALUE.getValue().tréith_VALUE.get("ConstantValue");
            String VALUE = tairiseach_VALUE == null ? "0" : tairiseach_slonn(클래스들.get(Leabhair_thagartha.úinéir_VALUE), new sonraí_Léitheoir(tairiseach_VALUE).두바이트());
            필드선언들.add("static word " + siombail("field", Leabhair_thagartha.부분들()) + " = " + VALUE + ";");
        }
        for (String Ainm : 클래스들.keySet()) {
            String túsaigh = siombail("init", Ainm), staid_VALUE = siombail("state", Ainm);
            선언들.add("static void " + túsaigh + "(void);"); 필드선언들.add("static unsigned " + staid_VALUE + ";");
            modh_Leabhair_thagartha Leabhair_thagartha = new modh_Leabhair_thagartha(Ainm, "<clinit>", "()V");
            몸체들.add("static void " + túsaigh + "(void) { if(" + staid_VALUE + ") return; " + staid_VALUE + " = 1; " + (함수들.containsKey(Leabhair_thagartha) ? siombail("method", Leabhair_thagartha.부분들()) + "(); " : "") + staid_VALUE + " = 2; }");
        }
        몸체들.add(easportáil_modh("java_entry", iontráil_pointe, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int suíomh_INDEX = 지정.indexOf('='); if (suíomh_INDEX < 1) throw new Aistriúchán_earráid("내보내기 지정 ERREÁID");
            String Ainm = 지정.substring(0, suíomh_INDEX); 공개이름.add(Ainm); 몸체들.add(easportáil_modh(Ainm, 지정.substring(suíomh_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> iontráil_VALUE : 문자열들.entrySet()) {
            String Téacs = iontráil_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + iontráil_VALUE.getValue() + "[] = {" + Téacs.length());
            for (int 순번 = 0; 순번 < Téacs.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Téacs.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Tacaíocht_VALUE = Files.readString(acmhainn_cosán.resolve("am_rite_teanga_coiteann_Tacaíocht.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Tacaíocht_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String FOINSE, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ainm_tábla = new HashMap<>();
        for (String Líne : Files.readAllLines(acmhainn_cosán.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] péireáil_VALUE = Líne.split("\t"); ainm_tábla.put(péireáil_VALUE[0], péireáil_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(FOINSE); StringBuffer tomhas = new StringBuffer();
        while (찾개.find()) {
            String Ainm = 찾개.group(), 새이름 = Ainm;
            if (!Ainm.startsWith("//") && !Ainm.startsWith("/*") && !Ainm.startsWith("\"") && !Ainm.startsWith("'") && !공개이름.contains(Ainm)) {
                새이름 = ainm_tábla.getOrDefault(Ainm, Ainm);
                if (Ainm.matches("a[0-9]+")) 새이름 = "Argóintí" + Ainm.substring(1);
                if (Ainm.matches("b[0-9]+")) 새이름 = "craobh" + Ainm.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char carachtar_VALUE : 새이름.toCharArray()) 표기.append(carachtar_VALUE < 128 ? Character.toString(carachtar_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)carachtar_VALUE));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(tomhas, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(tomhas); return tomhas.toString();
    }
    String 엑스함수본문(modh_Leabhair_thagartha feidhm_VALUE, ball_sonraí sonraí, Map<String,String> meaisín_tábla, String sprioc) {
        String 표식 = siombail("method", feidhm_VALUE.부분들());
        List<String> Líne = new ArrayList<>();
        if ((sonraí.rochtain_iontráil & 0x100) != 0) {
            String Nasc = meaisín_tábla.get(feidhm_VALUE.Ainm + feidhm_VALUE.서술);
            if (!feidhm_VALUE.úinéir_VALUE.equals(sprioc.equals("kernel") ? "gléas_VALUE" : "úsáideoir") || Nasc == null) throw new Aistriúchán_earráid("허용되지 않은 native feidhm_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Nasc;
        }
        byte[] corpthéacs = sonraí.tréith_VALUE.get("Code"); if (corpthéacs == null) throw new Aistriúchán_earráid("feidhm_VALUE 몸체가 없음");
        sonraí_Léitheoir Léitheoir_VALUE = new sonraí_Léitheoir(corpthéacs); Léitheoir_VALUE.두바이트(); int logánta_COUNT = Léitheoir_VALUE.두바이트();
        sonraí_Léitheoir ordú_sonraí = new sonraí_Léitheoir(Léitheoir_VALUE.Léigh(Léitheoir_VALUE.네바이트()));
        if (Léitheoir_VALUE.두바이트() != 0) throw new Aistriúchán_earráid("try/catch/finally 미지원");
        함수형식 formáid_VALUE = new 함수형식(feidhm_VALUE.서술); if (logánta_COUNT < formáid_VALUE.Argóintí.size()) throw new Aistriúchán_earráid("매개변수보다 적은 logánta_scóip 변수");
        Collections.addAll(Líne,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + logánta_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formáid_VALUE.Argóintí.size(); 순번++) Collections.addAll(Líne,"movl " + (8 + 4 * (formáid_VALUE.Argóintí.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        aicme_sonraí aicme_VALUE = 클래스들.get(feidhm_VALUE.úinéir_VALUE); Set<Integer> 경계들 = new HashSet<>(), craobh_Liosta = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (ordú_sonraí.suíomh < ordú_sonraí.sonraí.length) {
            int suíomh = ordú_sonraí.suíomh, Ordú = ordú_sonraí.한바이트(); String suíomh_INDEX = 표식 + "_b" + suíomh;
            Líne.add(suíomh_INDEX + ":"); 경계들.add(suíomh);
            if (Ordú == 0) Líne.add("nop");
            else if (Ordú == 1) Líne.add("pushl $0");
            else if (Ordú >= 2 && Ordú <= 8) Líne.add("pushl $" + (Ordú - 3));
            else if (Ordú == 16 || Ordú == 17) Líne.add("pushl $" + (Ordú == 16 ? ordú_sonraí.부호한바이트() : ordú_sonraí.부호두바이트()));
            else if (Ordú == 18 || Ordú == 19) {
                int INDEX = Ordú == 18 ? ordú_sonraí.한바이트() : ordú_sonraí.두바이트();
                Líne.add("pushl $" + 엑스상수(aicme_VALUE,INDEX));
            } else if (Ordú == 21 || Ordú == 25 || (Ordú >= 26 && Ordú <= 29) || (Ordú >= 42 && Ordú <= 45) || Ordú == 54 || Ordú == 58 || (Ordú >= 59 && Ordú <= 62) || (Ordú >= 75 && Ordú <= 78)) {
                boolean 읽음 = Ordú < 54; int INDEX = Ordú == 21 || Ordú == 25 || Ordú == 54 || Ordú == 58 ? ordú_sonraí.한바이트() : Ordú - (Ordú <= 29 ? 26 : Ordú <= 45 ? 42 : Ordú <= 62 ? 59 : 75);
                seic_logánta(INDEX,logánta_COUNT); Líne.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Ordú == 46) Collections.addAll(Líne,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Ordú == 79) Collections.addAll(Líne,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Ordú == 87 || Ordú == 88) Líne.add("addl $" + (Ordú == 87 ? 4 : 8) + ", %esp");
            else if (Ordú >= 89 && Ordú <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ord_Liosta = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Ordú - 89]; 순번++) Líne.add("popl " + 저장기들[순번]);
                for (int 순번 : ord_Liosta[Ordú - 89]) Líne.add("pushl " + 저장기들[순번]);
            } else if (Ordú == 96 || Ordú == 100 || Ordú == 104 || Ordú == 126 || Ordú == 128 || Ordú == 130) {
                String oibríocht_VALUE = Ordú == 96 ? "addl" : Ordú == 100 ? "subl" : Ordú == 104 ? "imull" : Ordú == 126 ? "andl" : Ordú == 128 ? "orl" : "xorl";
                Collections.addAll(Líne,"popl %ecx","popl %eax",oibríocht_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Ordú == 108 || Ordú == 112) Collections.addAll(Líne,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + suíomh_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + suíomh_INDEX + "_divide","xorl %edx, %edx","jmp " + suíomh_INDEX + "_done",suíomh_INDEX + "_divide:","cltd","idivl %ecx",suíomh_INDEX + "_done:","pushl " + (Ordú == 108 ? "%eax" : "%edx"));
            else if (Ordú == 116) Líne.add("negl (%esp)");
            else if (Ordú == 120 || Ordú == 122 || Ordú == 124) Collections.addAll(Líne,"popl %ecx","popl %eax",(Ordú == 120 ? "sall" : Ordú == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Ordú == 132) {
                int INDEX = ordú_sonraí.한바이트(), 증가 = ordú_sonraí.부호한바이트(); seic_logánta(INDEX,logánta_COUNT); Líne.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Ordú >= 145 && Ordú <= 147) Collections.addAll(Líne,"popl %eax",Ordú == 145 ? "movsbl %al, %eax" : Ordú == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Ordú >= 153 && Ordú <= 166) {
                if (Ordú <= 158) Collections.addAll(Líne,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Líne,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int sprioc_VALUE = suíomh + ordú_sonraí.부호두바이트(); craobh_Liosta.add(sprioc_VALUE); Líne.add(비교들[Ordú - (Ordú <= 158 ? 153 : 159)] + " " + 표식 + "_b" + sprioc_VALUE);
            } else if (Ordú == 167 || Ordú == 200) {
                int sprioc_VALUE = suíomh + (Ordú == 167 ? ordú_sonraí.부호두바이트() : ordú_sonraí.네바이트()); craobh_Liosta.add(sprioc_VALUE); Líne.add("jmp " + 표식 + "_b" + sprioc_VALUE);
            } else if (Ordú == 170 || Ordú == 171) {
                while (ordú_sonraí.suíomh % 4 != 0) ordú_sonraí.한바이트();
                int luach_réamhshocraithe = suíomh + ordú_sonraí.네바이트(); craobh_Liosta.add(luach_réamhshocraithe); Líne.add("popl %eax");
                int mír_COUNT, 아래 = 0;
                if (Ordú == 170) { 아래 = ordú_sonraí.네바이트(); int 위 = ordú_sonraí.네바이트(); long fad_VALUE = (long)위 - 아래 + 1; if (fad_VALUE < 1 || fad_VALUE > (ordú_sonraí.sonraí.length - ordú_sonraí.suíomh) / 4) throw new Aistriúchán_earráid("switch gearrthóg ERREÁID"); mír_COUNT = (int)fad_VALUE; }
                else { mír_COUNT = ordú_sonraí.네바이트(); if (mír_COUNT < 0 || mír_COUNT > (ordú_sonraí.sonraí.length - ordú_sonraí.suíomh) / 8) throw new Aistriúchán_earráid("switch Méid ERREÁID"); }
                for (int 순번 = 0; 순번 < mír_COUNT; 순번++) {
                    int VALUE = Ordú == 170 ? 아래 + 순번 : ordú_sonraí.네바이트(), sprioc_VALUE = suíomh + ordú_sonraí.네바이트(); craobh_Liosta.add(sprioc_VALUE);
                    Collections.addAll(Líne,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + sprioc_VALUE);
                }
                Líne.add("jmp " + 표식 + "_b" + luach_réamhshocraithe);
            } else if (Ordú == 172 || Ordú == 176 || Ordú == 177) {
                if (Ordú != 177) Líne.add("popl %eax"); Collections.addAll(Líne,"leave","ret");
            } else if (Ordú == 178 || Ordú == 179) {
                modh_Leabhair_thagartha Leabhair_thagartha = aicme_VALUE.Leabhair_thagartha(ordú_sonraí.두바이트()); if (!필드들.containsKey(Leabhair_thagartha)) throw new Aistriúchán_earráid("알 수 없는 réimse_VALUE");
                Collections.addAll(Líne,"call " + siombail("init",Leabhair_thagartha.úinéir_VALUE),(Ordú == 178 ? "pushl " : "popl ") + siombail("field",Leabhair_thagartha.부분들()));
            } else if (Ordú == 184) {
                modh_Leabhair_thagartha Leabhair_thagartha = aicme_VALUE.Leabhair_thagartha(ordú_sonraí.두바이트()); if (!함수들.containsKey(Leabhair_thagartha)) throw new Aistriúchán_earráid("알 수 없는 feidhm_VALUE");
                함수형식 호출형식 = new 함수형식(Leabhair_thagartha.서술); Collections.addAll(Líne,"call " + siombail("init",Leabhair_thagartha.úinéir_VALUE),"call " + siombail("method",Leabhair_thagartha.부분들()));
                if (!호출형식.Argóintí.isEmpty()) Líne.add("addl $" + 호출형식.Argóintí.size() * 4 + ", %esp");
                if (!호출형식.return_tomhas.equals("V")) Líne.add("pushl %eax");
            } else if (Ordú == 182) {
                modh_Leabhair_thagartha Leabhair_thagartha = aicme_VALUE.Leabhair_thagartha(ordú_sonraí.두바이트());
                if (Leabhair_thagartha.equals(new modh_Leabhair_thagartha("java/lang/String","length","()I"))) Collections.addAll(Líne,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Leabhair_thagartha.equals(new modh_Leabhair_thagartha("java/lang/String","charAt","(I)C"))) Collections.addAll(Líne,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Aistriúchán_earráid("가상 feidhm_VALUE 호출 미지원");
            } else if (Ordú == 188) {
                if (ordú_sonraí.한바이트() != 10) throw new Aistriúchán_earráid("new int[]만 Tacaíocht_VALUE"); Collections.addAll(Líne,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Ordú == 190) Collections.addAll(Líne,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Ordú == 196) {
                int breisiú_VALUE = ordú_sonraí.한바이트(), INDEX = ordú_sonraí.두바이트(); seic_logánta(INDEX,logánta_COUNT);
                if (breisiú_VALUE == 21 || breisiú_VALUE == 25 || breisiú_VALUE == 54 || breisiú_VALUE == 58) Líne.add((breisiú_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (breisiú_VALUE == 132) Líne.add("addl $" + ordú_sonraí.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Aistriúchán_earráid("wide Ordú 미지원");
            } else if (Ordú == 198 || Ordú == 199) {
                int sprioc_VALUE = suíomh + ordú_sonraí.부호두바이트(); craobh_Liosta.add(sprioc_VALUE); Collections.addAll(Líne,"popl %eax","testl %eax, %eax",(Ordú == 198 ? "je " : "jne ") + 표식 + "_b" + sprioc_VALUE);
            } else throw new Aistriúchán_earráid("미지원 Ordú: " + Ordú);
        }
        if (!경계들.containsAll(craobh_Liosta)) throw new Aistriúchán_earráid("Ordú 경계가 아닌 곳으로 craobh");
        Líne.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",Líne);
    }
    String 엑스상수(aicme_sonraí sonraí, int INDEX) {
        if (sonraí.상수종류[INDEX] == 3) return sonraí.tairiseach_sonraí[INDEX].toString();
        if (sonraí.상수종류[INDEX] == 8) return teaghrán_siombail(sonraí.문자((Integer)sonraí.tairiseach_sonraí[INDEX]));
        throw new Aistriúchán_earráid("정수와 teaghrán_VALUE 상수만 Tacaíocht_VALUE");
    }
    String 엑스조립본(String iontráil_pointe, List<String> 내보냄, String sprioc) throws IOException {
        Map<String,String> meaisín_tábla = new HashMap<>();
        for (String Líne : Files.readAllLines(acmhainn_cosán.resolve("엑스기계함수.tsv"))) { String[] péireáil_VALUE = Líne.split("\t"); if (péireáil_VALUE[0].equals(sprioc)) meaisín_tábla.put(péireáil_VALUE[1] + péireáil_VALUE[2],péireáil_VALUE[3]); }
        int suíomh_INDEX = iontráil_pointe.lastIndexOf('.'); if (suíomh_INDEX < 0) throw new Aistriúchán_earráid("iontráil_pointe 지정 ERREÁID");
        String úinéir_VALUE = iontráil_pointe.substring(0,suíomh_INDEX).replace('.','/'), modh_iontráil_ainm = iontráil_pointe.substring(suíomh_INDEX + 1); modh_Leabhair_thagartha iontráil_pointe_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { modh_Leabhair_thagartha Leabhair_thagartha = new modh_Leabhair_thagartha(úinéir_VALUE,modh_iontráil_ainm,서술); if (함수들.containsKey(Leabhair_thagartha)) { if (iontráil_pointe_VALUE != null) throw new Aistriúchán_earráid("겹친 iontráil_pointe"); iontráil_pointe_VALUE = Leabhair_thagartha; } }
        if (iontráil_pointe_VALUE == null || (함수들.get(iontráil_pointe_VALUE).rochtain_iontráil & 0x100) != 0) throw new Aistriúchán_earráid("iontráil_pointe_VALUE feidhm_VALUE formáid_VALUE ERREÁID");
        List<String> Líne = new ArrayList<>(); Líne.add(".code32");
        for (aicme_sonraí sonraí : 클래스들.values()) {
            String staid_VALUE = siombail("state",sonraí.Ainm), túsaigh = siombail("init",sonraí.Ainm);
            Collections.addAll(Líne,".bss",".balign 4",staid_VALUE + ": .long 0",".text",túsaigh + ":","cmpl $0, " + staid_VALUE,"jne " + túsaigh + "_done","movl $1, " + staid_VALUE);
            modh_Leabhair_thagartha 초기화참조 = new modh_Leabhair_thagartha(sonraí.Ainm,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Líne.add("call " + siombail("method",초기화참조.부분들()));
            Collections.addAll(Líne,"movl $2, " + staid_VALUE,túsaigh + "_done:","ret");
            for (ball_sonraí réimse_VALUE : sonraí.réimse_VALUE) {
                byte[] tairiseach_VALUE = réimse_VALUE.tréith_VALUE.get("ConstantValue"); String VALUE = tairiseach_VALUE == null ? "0" : 엑스상수(sonraí,new sonraí_Léitheoir(tairiseach_VALUE).두바이트());
                Collections.addAll(Líne,".data",".balign 4",siombail("field",sonraí.Ainm,réimse_VALUE.Ainm,réimse_VALUE.서술) + ": .long " + VALUE);
            }
            for (ball_sonraí feidhm_VALUE : sonraí.feidhm_VALUE) if (!feidhm_VALUE.Ainm.equals("<init>")) Líne.add(엑스함수본문(new modh_Leabhair_thagartha(sonraí.Ainm,feidhm_VALUE.Ainm,feidhm_VALUE.서술),feidhm_VALUE,meaisín_tábla,sprioc));
        }
        Collections.addAll(Líne,".text",".globl java_entry","java_entry:","call " + siombail("init",iontráil_pointe_VALUE.úinéir_VALUE),"call " + siombail("method",iontráil_pointe_VALUE.부분들()));
        if (iontráil_pointe_VALUE.서술.equals("()V")) Líne.add("xorl %eax, %eax"); Líne.add("ret");
        for (String 지정 : 내보냄) {
            int teormharcóir_VALUE = 지정.indexOf('='); if (teormharcóir_VALUE < 1) throw new Aistriúchán_earráid("내보내기 지정 ERREÁID");
            String 외부 = 지정.substring(0,teormharcóir_VALUE), feidhm_VALUE = 지정.substring(teormharcóir_VALUE + 1); int roinnt_tomhas = feidhm_VALUE.lastIndexOf('.');
            if (roinnt_tomhas < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Aistriúchán_earráid("내보내기 siombail ERREÁID");
            String aicme_VALUE = feidhm_VALUE.substring(0,roinnt_tomhas).replace('.','/'), Ainm = feidhm_VALUE.substring(roinnt_tomhas + 1); modh_Leabhair_thagartha roghnú_VALUE = null;
            for (modh_Leabhair_thagartha Leabhair_thagartha : 함수들.keySet()) if (Leabhair_thagartha.úinéir_VALUE.equals(aicme_VALUE) && Leabhair_thagartha.Ainm.equals(Ainm)) { if (roghnú_VALUE != null) throw new Aistriúchán_earráid("겹친 내보내기 sprioc"); roghnú_VALUE = Leabhair_thagartha; }
            if (roghnú_VALUE == null) throw new Aistriúchán_earráid("내보낼 함수가 없음");
            Collections.addAll(Líne,".text",".globl " + 외부,외부 + ":","call " + siombail("init",roghnú_VALUE.úinéir_VALUE),"jmp " + siombail("method",roghnú_VALUE.부분들()));
        }
        Líne.add(".section .rodata");
        for (Map.Entry<String,String> iontráil_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Líne,".balign 4",iontráil_VALUE.getValue() + ":",".long " + iontráil_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char aonaid_VALUE : iontráil_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(aonaid_VALUE)); if (!단위들.isEmpty()) Líne.add(".long " + String.join(",",단위들));
        }
        Líne.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Líne) + "\n";
    }
    static void Rith_uirlis(List<String> Ordú) throws Exception {
        if (new ProcessBuilder(Ordú).inheritIO().start().waitFor() != 0) throw new Aistriúchán_earráid("tóg_foinse ERREÁID: " + Ordú.get(0));
    }
    static String sonraí_teaghrán(String Téacs) { return "\"" + Téacs.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String sprioc, String iontráil_pointe, List<String> 내보냄, Path Aschur, Path acmhainn_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), aicme_cosán = 임시.resolve("classes"); Files.createDirectory(aicme_cosán);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",aicme_cosán.toString(),"-sourcepath",aicme_cosán.toString(),"-d",aicme_cosán.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int foinse_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Aschur.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Aistriúchán_earráid("Aschur 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); foinse_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Aistriúchán_earráid(".java 또는 .class만 Tacaíocht_VALUE");
            }
            if (foinse_COUNT > 0) Rith_uirlis(자바명령);
            try (java.util.stream.Stream<Path> cosán_Liosta = Files.walk(aicme_cosán)) { cosán_Liosta.filter(CONAIR -> CONAIR.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,sprioc.equals("user") ? "user" : "kernel",262144,acmhainn_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(iontráil_pointe,내보냄,sprioc); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path uirlis_suíomh = acmhainn_VALUE.getParent();
            Rith_uirlis(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Rith_uirlis(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),uirlis_suíomh.resolve("am_rite_teanga_coiteann_Tacaíocht.s").toString()));
            List<String> Nasc = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (sprioc.equals("kernel")) Nasc.add("-r");
            else {
                Rith_uirlis(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),uirlis_suíomh.resolve(sprioc.equals("user") ? "Start_úsáideoir_clár.s" : "리눅스시작.s").toString()));
                Collections.addAll(Nasc,"-e","_start",임시.resolve("start.o").toString());
                if (sprioc.equals("user")) Collections.addAll(Nasc,"-T",uirlis_suíomh.resolve("úsáideoir_Nasc_dáileadh.ld").toString());
            }
            Collections.addAll(Nasc,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Rith_uirlis(Nasc);
            Aschur = Aschur.toAbsolutePath(); Files.createDirectories(Aschur.getParent()); Path foilsigh_VALUE = Files.createTempFile(Aschur.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),foilsigh_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(foilsigh_VALUE,Aschur,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(foilsigh_VALUE); }
            Files.setPosixFilePermissions(Aschur,java.nio.file.attribute.PosixFilePermissions.fromString(sprioc.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Aschur + ".s"),조립,StandardCharsets.UTF_8);
            List<String> siombail_sonraí = new ArrayList<>(), sonraí_foinseacha = new ArrayList<>();
            for (modh_Leabhair_thagartha Leabhair_thagartha : CONVERT_VALUE.함수들.keySet()) siombail_sonraí.add(sonraí_teaghrán(siombail("method",Leabhair_thagartha.부분들())) + ":" + sonraí_teaghrán(Leabhair_thagartha.úinéir_VALUE + "." + Leabhair_thagartha.Ainm + Leabhair_thagartha.서술));
            for (Path 입력 : 입력들) {
                byte[] hais_comhad = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Téacs = new StringBuilder(); for (byte VALUE : hais_comhad) Téacs.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                sonraí_foinseacha.add(sonraí_teaghrán(입력.toAbsolutePath().toString()) + ":" + sonraí_teaghrán(Téacs.toString()));
            }
            Files.writeString(Paths.get(Aschur + ".json"),"{\"target\":" + sonraí_teaghrán(sprioc) + ",\"entry\":" + sonraí_teaghrán(iontráil_pointe) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",siombail_sonraí) + "},\"sources\":{" + String.join(",",sonraí_foinseacha) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> cosán_Liosta = Files.walk(임시)) { for (Path CONAIR : (Iterable<Path>)cosán_Liosta.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(CONAIR); }
        }
    }
    public static void main(String[] Argóintí) {
        try {
            String iontráil_pointe = null, sprioc = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> cosán_Liosta = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argóintí.length; 순번++) {
                String VALUE = Argóintí[순번];
                switch (VALUE) {
                    case "--target": 엑스대상 = Argóintí[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry aicme_VALUE.feidhm_VALUE -o Aschur [--target linux|kernel|user] [--profile kernel|user] [--export siombail=aicme_VALUE.feidhm_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": iontráil_pointe = Argóintí[++순번]; break;
                    case "--profile": sprioc = Argóintí[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argóintí[++순번]); break;
                    case "--export": 내보냄.add(Argóintí[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argóintí[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Aistriúchán_earráid("알 수 없는 옵션: " + VALUE); cosán_Liosta.add(Paths.get(VALUE));
                }
            }
            if (iontráil_pointe == null || 출력경로 == null || cosán_Liosta.isEmpty()) throw new Aistriúchán_earráid("--entry, -o, aicme_VALUE 파일이 필요합니다");
            Path acmhainn_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Aistriúchán_earráid("알 수 없는 Rith_ordú sprioc");
                엑스번역(cosán_Liosta,엑스대상,iontráil_pointe,내보냄,출력경로,acmhainn_VALUE); return;
            }
            String FOINSE = new 기계어미리번역(cosán_Liosta, sprioc, 낱말수, acmhainn_VALUE).giniúint(iontráil_pointe, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, FOINSE, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception ERREÁID) { System.err.println("tóg_foinse ERREÁID: " + ERREÁID.getMessage()); System.exit(1); }
    }
}
