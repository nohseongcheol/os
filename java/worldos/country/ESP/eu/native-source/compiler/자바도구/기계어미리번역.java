// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Gela_balio 파일에서 독립 ARM64 커널용 C 원문을 만든다. Ostalari JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Itzulpena_errore extends RuntimeException {
        Itzulpena_errore(String 설명) { super(설명); }
    }
    static final class datuak_irakurle {
        final byte[] datuak;
        int Posizioa;
        datuak_irakurle(byte[] 입력자료) { datuak = 입력자료; }
        byte[] Irakurri(int luzera_balio) {
            if (luzera_balio < 0 || luzera_balio > datuak.length - Posizioa) throw new Itzulpena_errore("잘린 Gela_balio 또는 Komandoa datuak");
            byte[] EMAITZA = Arrays.copyOfRange(datuak, Posizioa, Posizioa + luzera_balio); Posizioa += luzera_balio; return EMAITZA;
        }
        int 한바이트() { if (Posizioa >= datuak.length) throw new Itzulpena_errore("잘린 Komandoa datuak"); return datuak[Posizioa++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class kide_datuak {
        final int atzitu_sarrera;
        final String Izena, 서술;
        final Map<String, byte[]> atributu_balio;
        kide_datuak(int atzitu_balio, String izen_balio, String 서술값, Map<String, byte[]> atributu_datuak) {
            atzitu_sarrera = atzitu_balio; Izena = izen_balio; 서술 = 서술값; atributu_balio = atributu_datuak;
        }
    }
    static final class 함수참조 implements Comparable<함수참조> {
        final String jabe_balio, Izena, 서술;
        함수참조(String 소유값, String izen_balio, String 서술값) { jabe_balio = 소유값; Izena = izen_balio; 서술 = 서술값; }
        String[] 부분들() { return new String[]{jabe_balio, Izena, 서술}; }
        public int compareTo(함수참조 pareko_balio) {
            int Konparazioa_balio = jabe_balio.compareTo(pareko_balio.jabe_balio);
            if (Konparazioa_balio == 0) Konparazioa_balio = Izena.compareTo(pareko_balio.Izena);
            return Konparazioa_balio == 0 ? 서술.compareTo(pareko_balio.서술) : Konparazioa_balio;
        }
        public boolean equals(Object pareko_balio) { return pareko_balio instanceof 함수참조 && compareTo((함수참조) pareko_balio) == 0; }
        public int hashCode() { return Objects.hash(jabe_balio, Izena, 서술); }
    }
    static final class Gela_datuak {
        final int[] 상수종류;
        final Object[] konstante_datuak;
        final String Izena;
        final List<kide_datuak> eremu_balio, FUNTZIOA_balio;
        Gela_datuak(Path Bide_izena) throws IOException {
            datuak_irakurle irakurle_balio = new datuak_irakurle(Files.readAllBytes(Bide_izena));
            if (irakurle_balio.네바이트() != 0xcafebabe) throw new Itzulpena_errore("Java Gela_balio 표식이 아님");
            irakurle_balio.Irakurri(4);
            int elementu_ZENBATU = irakurle_balio.두바이트(); 상수종류 = new int[elementu_ZENBATU]; konstante_datuak = new Object[elementu_ZENBATU];
            for (int 순번 = 1; 순번 < elementu_ZENBATU; 순번++) {
                int 종류 = irakurle_balio.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int luzera_balio = irakurle_balio.두바이트();
                        byte[] karaktere_buffer = irakurle_balio.Irakurri(luzera_balio), 길이붙인자료 = new byte[luzera_balio + 2];
                        길이붙인자료[0] = (byte)(luzera_balio >> 8); 길이붙인자료[1] = (byte)luzera_balio;
                        System.arraycopy(karaktere_buffer, 0, 길이붙인자료, 2, luzera_balio);
                        konstante_datuak[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstante_datuak[순번] = irakurle_balio.네바이트(); break;
                    case 4: irakurle_balio.Irakurri(4); break;
                    case 5: case 6: irakurle_balio.Irakurri(8); 순번++; break;
                    case 7: case 8: case 16: konstante_datuak[순번] = irakurle_balio.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstante_datuak[순번] = new int[]{irakurle_balio.두바이트(), irakurle_balio.두바이트()}; break;
                    case 15: konstante_datuak[순번] = new int[]{irakurle_balio.한바이트(), irakurle_balio.두바이트()}; break;
                    default: throw new Itzulpena_errore("지원하지 않는 konstante_balio 종류: " + 종류);
                }
            }
            irakurle_balio.두바이트(); Izena = klasearen_izen(irakurle_balio.두바이트());
            if (!klasearen_izen(irakurle_balio.두바이트()).equals("java/lang/Object") || irakurle_balio.두바이트() != 0)
                throw new Itzulpena_errore(Izena + ": 상속 및 인터페이스 미지원");
            eremu_balio = 멤버읽기(irakurle_balio); FUNTZIOA_balio = 멤버읽기(irakurle_balio); 속성읽기(irakurle_balio);
            if (irakurle_balio.Posizioa != irakurle_balio.datuak.length) throw new Itzulpena_errore("Gela_balio 뒤에 남은 datuak");
        }
        String 문자(int INDIZE) {
            if (INDIZE < 1 || INDIZE >= 상수종류.length || 상수종류[INDIZE] != 1) throw new Itzulpena_errore("문자 konstante_balio INDIZE errorea");
            return (String) konstante_datuak[INDIZE];
        }
        String klasearen_izen(int INDIZE) {
            if (INDIZE < 1 || INDIZE >= 상수종류.length || 상수종류[INDIZE] != 7) throw new Itzulpena_errore("Gela_balio Erreferentzia_materiala errorea");
            return 문자((Integer)konstante_datuak[INDIZE]);
        }
        함수참조 Erreferentzia_materiala(int INDIZE) {
            if (INDIZE < 1 || INDIZE >= 상수종류.length || 상수종류[INDIZE] < 9 || 상수종류[INDIZE] > 11) throw new Itzulpena_errore("멤버 Erreferentzia_materiala errorea");
            int[] parekatu_balio = (int[])konstante_datuak[INDIZE], izen_parekatu = (int[])konstante_datuak[parekatu_balio[1]];
            return new 함수참조(klasearen_izen(parekatu_balio[0]), 문자(izen_parekatu[0]), 문자(izen_parekatu[1]));
        }
        Map<String, byte[]> 속성읽기(datuak_irakurle irakurle_balio) {
            Map<String, byte[]> EMAITZA = new LinkedHashMap<>();
            int elementu_ZENBATU = irakurle_balio.두바이트();
            for (int 순번 = 0; 순번 < elementu_ZENBATU; 순번++) {
                String atributu_izen = 문자(irakurle_balio.두바이트()); byte[] balio = irakurle_balio.Irakurri(irakurle_balio.네바이트());
                if (EMAITZA.put(atributu_izen, balio) != null) throw new Itzulpena_errore("겹친 atributu_balio: " + atributu_izen);
            }
            return EMAITZA;
        }
        List<kide_datuak> 멤버읽기(datuak_irakurle irakurle_balio) {
            List<kide_datuak> EMAITZA = new ArrayList<>(); int elementu_ZENBATU = irakurle_balio.두바이트();
            for (int 순번 = 0; 순번 < elementu_ZENBATU; 순번++) {
                int atzitu_sarrera = irakurle_balio.두바이트(); String 함수이름 = 문자(irakurle_balio.두바이트()), 서술 = 문자(irakurle_balio.두바이트());
                EMAITZA.add(new kide_datuak(atzitu_sarrera, 함수이름, 서술, 속성읽기(irakurle_balio)));
            }
            return EMAITZA;
        }
    }
    static final class 함수형식 {
        final List<String> Argumentuak = new ArrayList<>();
        final String itzuli_neurria;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Itzulpena_errore("FUNTZIOA_balio 서술 errorea: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Itzulpena_errore("FUNTZIOA_balio 서술 errorea: " + 서술);
            Argumentuak.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumentuak.contains("V") || 반환들.size() != 1) throw new Itzulpena_errore("FUNTZIOA_balio 서술 errorea: " + 서술);
            itzuli_neurria = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> EMAITZA = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Posizioa = 0; Posizioa < 서술.length();) {
            String hautapen_balio = null;
            for (String formatu_balio : 허용형식) if (서술.startsWith(formatu_balio, Posizioa)) { hautapen_balio = formatu_balio; break; }
            if (hautapen_balio == null) throw new Itzulpena_errore("지원하지 않는 datu_mota: " + 서술);
            EMAITZA.add(hautapen_balio); Posizioa += hautapen_balio.length();
        }
        return EMAITZA;
    }
    static String ikur(String 종류, String... 부분들) {
        try {
            byte[] hash_fitxategi = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Testua = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Testua.append(String.format(Locale.ROOT, "%02x", hash_fitxategi[순번] & 255));
            return Testua.toString();
        } catch (Exception errorea) { throw new Itzulpena_errore(errorea.toString()); }
    }
    final Map<String, Gela_datuak> 클래스들 = new TreeMap<>();
    final Map<함수참조, kide_datuak> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), gailu_Azure_Funtzioak_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, gailu_Gela;
    final int 동적기억낱말수;
    final Path baliabide_bide_izen;
    기계어미리번역(List<Path> bide_izen_Zerrenda, String helburu_balio, int 낱말수, Path baliabide_balio) throws IOException {
        if ((!helburu_balio.equals("kernel") && !helburu_balio.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Itzulpena_errore("exekutatu_komando helburu_balio 또는 Memoria_balio 공간 Tamaina errorea");
        실행대상 = helburu_balio; 동적기억낱말수 = 낱말수; baliabide_bide_izen = baliabide_balio;
        // 이 이름도 국가별 iturburu_zuhaitz sortu 시 해당 언어로 옮긴다.
        gailu_Gela = helburu_balio.equals("kernel") ? "arbel" : "erabiltzaile";
        for (String Marra : Files.readAllLines(baliabide_balio.resolve("gailu_Azure_Funtzioak.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Marra.split("\t", -1);
            if (부분들.length != 4) throw new Itzulpena_errore("gailu FUNTZIOA_balio datuak errorea");
            if (부분들[0].equals(helburu_balio)) gailu_Azure_Funtzioak_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Bide_izena : bide_izen_Zerrenda) {
            Gela_datuak datuak = new Gela_datuak(Bide_izena);
            if (클래스들.put(datuak.Izena, datuak) != null) throw new Itzulpena_errore("중복 Gela_balio: " + datuak.Izena);
            for (kide_datuak eremu_balio : datuak.eremu_balio) {
                if ((eremu_balio.atzitu_sarrera & 8) == 0 || 형식읽기(eremu_balio.서술).equals(Collections.singletonList("V"))) throw new Itzulpena_errore("estatiko_balio 필드만 Laguntza_balio");
                if (필드들.put(new 함수참조(datuak.Izena, eremu_balio.Izena, eremu_balio.서술), eremu_balio) != null) throw new Itzulpena_errore("중복 eremu_balio");
            }
            for (kide_datuak FUNTZIOA_balio : datuak.FUNTZIOA_balio) {
                if (FUNTZIOA_balio.Izena.equals("<init>")) continue;
                if ((FUNTZIOA_balio.atzitu_sarrera & 8) == 0 || (FUNTZIOA_balio.atzitu_sarrera & (0x20 | 0x400)) != 0) throw new Itzulpena_errore("estatiko_balio 비동기화 함수만 Laguntza_balio");
                new 함수형식(FUNTZIOA_balio.서술);
                if (함수들.put(new 함수참조(datuak.Izena, FUNTZIOA_balio.Izena, FUNTZIOA_balio.서술), FUNTZIOA_balio) != null) throw new Itzulpena_errore("중복 FUNTZIOA_balio");
            }
        }
    }
    String kate_ikur(String Testua) { return 문자열들.computeIfAbsent(Testua, balio -> "j_text_" + 문자열들.size()); }
    String konstante_adierazpen(Gela_datuak datuak, int INDIZE) {
        if (INDIZE < 1 || INDIZE >= datuak.상수종류.length) throw new Itzulpena_errore("konstante_balio INDIZE klip errorea");
        if (datuak.상수종류[INDIZE] == 3) return "(word)(uint32_t)(" + datuak.konstante_datuak[INDIZE] + ")";
        if (datuak.상수종류[INDIZE] == 8) return "(word)" + kate_ikur(datuak.문자((Integer)datuak.konstante_datuak[INDIZE]));
        throw new Itzulpena_errore("정수와 kate_balio 상수만 Laguntza_balio");
    }
    String 함수원형(함수참조 Erreferentzia_materiala) {
        List<String> 인수들 = new ArrayList<>(); int elementu_ZENBATU = new 함수형식(Erreferentzia_materiala.서술).Argumentuak.size();
        for (int 순번 = 0; 순번 < elementu_ZENBATU; 순번++) 인수들.add("word a" + 순번);
        return "static word " + ikur("method", Erreferentzia_materiala.부분들()) + "(" + (elementu_ZENBATU == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void txeke_lokal(int INDIZE, int 지역변수수) { if (INDIZE < 0 || INDIZE >= 지역변수수) throw new Itzulpena_errore("lokal_esparru 변수 INDIZE klip errorea"); }
    void 분기넣기(List<String> Irteera, Set<Integer> adar_Zerrenda, int Posizioa, int 이동량, String baldintza) {
        int helburu_balio_a0fbc067 = Posizioa + 이동량; adar_Zerrenda.add(helburu_balio_a0fbc067);
        Irteera.add((baldintza == null ? "" : "if (" + baldintza + ") ") + "goto b" + helburu_balio_a0fbc067 + ";");
    }
    String 함수본문(함수참조 FUNTZIOA_balio, kide_datuak datuak) {
        byte[] gorputz_datuak = datuak.atributu_balio.get("Code"); if (gorputz_datuak == null) throw new Itzulpena_errore("FUNTZIOA_balio 몸체가 없음: " + FUNTZIOA_balio.Izena);
        datuak_irakurle irakurle_balio = new datuak_irakurle(gorputz_datuak); int 쌓임깊이 = irakurle_balio.두바이트(), 지역변수수 = irakurle_balio.두바이트();
        datuak_irakurle komando_datuak = new datuak_irakurle(irakurle_balio.Irakurri(irakurle_balio.네바이트()));
        if (irakurle_balio.두바이트() != 0) throw new Itzulpena_errore("try/catch/finally 미지원");
        함수형식 formatu_balio = new 함수형식(FUNTZIOA_balio.서술); if (지역변수수 < formatu_balio.Argumentuak.size()) throw new Itzulpena_errore("매개변수보다 적은 lokal_esparru 변수");
        Gela_datuak Gela_balio = 클래스들.get(FUNTZIOA_balio.jabe_balio);
        List<String> Irteera = new ArrayList<>(); Irteera.add(함수원형(FUNTZIOA_balio) + " {");
        Irteera.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formatu_balio.Argumentuak.size(); 순번++) Irteera.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), adar_Zerrenda = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (komando_datuak.Posizioa < komando_datuak.datuak.length) {
            int Posizioa = komando_datuak.Posizioa, Komandoa = komando_datuak.한바이트(); 경계들.add(Posizioa); Irteera.add("b" + Posizioa + ":;");
            if (Komandoa == 0) continue;
            if (Komandoa == 1) Irteera.add("PUSH(0);");
            else if (Komandoa >= 2 && Komandoa <= 8) Irteera.add("PUSH((uint32_t)(" + (Komandoa - 3) + "));");
            else if (Komandoa == 16 || Komandoa == 17) Irteera.add("PUSH((uint32_t)(" + (Komandoa == 16 ? komando_datuak.부호한바이트() : komando_datuak.부호두바이트()) + "));");
            else if (Komandoa == 18 || Komandoa == 19) Irteera.add("PUSH(" + konstante_adierazpen(Gela_balio, Komandoa == 18 ? komando_datuak.한바이트() : komando_datuak.두바이트()) + ");");
            else if (Komandoa == 21 || Komandoa == 25 || (Komandoa >= 26 && Komandoa <= 29) || (Komandoa >= 42 && Komandoa <= 45)) {
                int INDIZE = Komandoa == 21 || Komandoa == 25 ? komando_datuak.한바이트() : Komandoa - (Komandoa <= 29 ? 26 : 42);
                txeke_lokal(INDIZE, 지역변수수); Irteera.add("PUSH(l[" + INDIZE + "]);");
            } else if (Komandoa == 54 || Komandoa == 58 || (Komandoa >= 59 && Komandoa <= 62) || (Komandoa >= 75 && Komandoa <= 78)) {
                int INDIZE = Komandoa == 54 || Komandoa == 58 ? komando_datuak.한바이트() : Komandoa - (Komandoa <= 62 ? 59 : 75);
                txeke_lokal(INDIZE, 지역변수수); Irteera.add("l[" + INDIZE + "] = POP();");
            } else if (Komandoa == 46) Irteera.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Komandoa == 79) Irteera.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Komandoa == 87 || Komandoa == 88) Irteera.add(Komandoa == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Komandoa >= 89 && Komandoa <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ordena_Zerrenda = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Komandoa - 89]; 순번++) Irteera.add("abcd".charAt(순번) + " = POP();");
                for (char balio : ordena_Zerrenda[Komandoa - 89].toCharArray()) Irteera.add("PUSH(" + balio + ");");
            } else if (Komandoa == 96 || Komandoa == 100 || Komandoa == 104 || Komandoa == 126 || Komandoa == 128 || Komandoa == 130) {
                String kirurgia_balio = Komandoa == 96 ? "+" : Komandoa == 100 ? "-" : Komandoa == 104 ? "*" : Komandoa == 126 ? "&" : Komandoa == 128 ? "|" : "^";
                Irteera.add("b = POP(); a = POP(); PUSH((uint32_t)a " + kirurgia_balio + " (uint32_t)b);");
            } else if (Komandoa == 108 || Komandoa == 112) Irteera.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Komandoa == 112 ? 1 : 0) + "));");
            else if (Komandoa == 116) Irteera.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Komandoa == 120 || Komandoa == 122 || Komandoa == 124) {
                Irteera.add("b = POP(); a = POP();"); Irteera.add("PUSH(" + (Komandoa == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Komandoa == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Komandoa == 132) {
                int INDIZE = komando_datuak.한바이트(), 증가량 = komando_datuak.부호한바이트(); txeke_lokal(INDIZE, 지역변수수);
                Irteera.add("l[" + INDIZE + "] = (uint32_t)l[" + INDIZE + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Komandoa >= 145 && Komandoa <= 147) Irteera.add("a = POP(); PUSH((uint32_t)(" + (Komandoa == 145 ? "int8_t" : Komandoa == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Komandoa >= 153 && Komandoa <= 158) {
                Irteera.add("a = POP();"); 분기넣기(Irteera, adar_Zerrenda, Posizioa, komando_datuak.부호두바이트(), "(int32_t)a " + 비교들[Komandoa - 153] + " 0");
            } else if (Komandoa >= 159 && Komandoa <= 166) {
                Irteera.add("b = POP(); a = POP();"); 분기넣기(Irteera, adar_Zerrenda, Posizioa, komando_datuak.부호두바이트(), Komandoa >= 165 ? "a " + 비교들[Komandoa - 159] + " b" : "(int32_t)a " + 비교들[Komandoa - 159] + " (int32_t)b");
            } else if (Komandoa == 167 || Komandoa == 200) 분기넣기(Irteera, adar_Zerrenda, Posizioa, Komandoa == 167 ? komando_datuak.부호두바이트() : komando_datuak.네바이트(), null);
            else if (Komandoa == 170 || Komandoa == 171) {
                while (komando_datuak.Posizioa % 4 != 0) komando_datuak.한바이트();
                int balio_lehenetsi = komando_datuak.네바이트(); Irteera.add("a = POP();");
                if (Komandoa == 170) {
                    int 아래 = komando_datuak.네바이트(), 위 = komando_datuak.네바이트(); long elementu_ZENBATU = (long)위 - 아래 + 1;
                    if (elementu_ZENBATU < 1 || elementu_ZENBATU > (komando_datuak.datuak.length - komando_datuak.Posizioa) / 4) throw new Itzulpena_errore("switch klip errorea");
                    for (long balio = 아래; balio <= 위; balio++) 분기넣기(Irteera, adar_Zerrenda, Posizioa, komando_datuak.네바이트(), "(int32_t)a == (" + balio + ")");
                } else {
                    int elementu_ZENBATU = komando_datuak.네바이트(), aurrekoa_datuak = 0;
                    if (elementu_ZENBATU < 0 || elementu_ZENBATU > (komando_datuak.datuak.length - komando_datuak.Posizioa) / 8) throw new Itzulpena_errore("switch Tamaina errorea");
                    for (int 순번 = 0; 순번 < elementu_ZENBATU; 순번++) {
                        int balio = komando_datuak.네바이트(); if (순번 > 0 && balio <= aurrekoa_datuak) throw new Itzulpena_errore("switch ordena_balio errorea"); aurrekoa_datuak = balio;
                        분기넣기(Irteera, adar_Zerrenda, Posizioa, komando_datuak.네바이트(), "(int32_t)a == (" + balio + ")");
                    }
                }
                분기넣기(Irteera, adar_Zerrenda, Posizioa, balio_lehenetsi, null);
            } else if (Komandoa == 172 || Komandoa == 176 || Komandoa == 177) Irteera.add("return " + (Komandoa == 177 ? "0" : "POP()") + ";");
            else if (Komandoa == 178 || Komandoa == 179) {
                함수참조 Erreferentzia_materiala = Gela_balio.Erreferentzia_materiala(komando_datuak.두바이트()); if (!필드들.containsKey(Erreferentzia_materiala)) throw new Itzulpena_errore("알 수 없는 eremu_balio");
                Irteera.add(ikur("init", Erreferentzia_materiala.jabe_balio) + "();"); String eremu_balio = ikur("field", Erreferentzia_materiala.부분들());
                Irteera.add(Komandoa == 178 ? "PUSH(" + eremu_balio + ");" : eremu_balio + " = POP();");
            } else if (Komandoa == 184) {
                함수참조 Erreferentzia_materiala = Gela_balio.Erreferentzia_materiala(komando_datuak.두바이트()); if (!함수들.containsKey(Erreferentzia_materiala)) throw new Itzulpena_errore("알 수 없는 FUNTZIOA_balio");
                함수형식 호출형식 = new 함수형식(Erreferentzia_materiala.서술); int elementu_ZENBATU = 호출형식.Argumentuak.size();
                Irteera.add(ikur("init", Erreferentzia_materiala.jabe_balio) + "();"); Irteera.add("if(sp < " + elementu_ZENBATU + ") kernel_panic(\"call stack underflow\"); sp -= " + elementu_ZENBATU + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < elementu_ZENBATU; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Irteera.add("a = " + ikur("method", Erreferentzia_materiala.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.itzuli_neurria.equals("V")) Irteera.add("PUSH(a);");
            } else if (Komandoa == 182) {
                함수참조 Erreferentzia_materiala = Gela_balio.Erreferentzia_materiala(komando_datuak.두바이트());
                if (Erreferentzia_materiala.equals(new 함수참조("java/lang/String", "length", "()I"))) Irteera.add("a = POP(); PUSH(length(a));");
                else if (Erreferentzia_materiala.equals(new 함수참조("java/lang/String", "charAt", "(I)C"))) Irteera.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Itzulpena_errore("가상 FUNTZIOA_balio 호출 미지원");
            } else if (Komandoa == 188) {
                if (komando_datuak.한바이트() != 10) throw new Itzulpena_errore("new int[]만 Laguntza_balio"); Irteera.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Komandoa == 190) Irteera.add("a = POP(); PUSH(length(a));");
            else if (Komandoa == 196) {
                int luzapen_balio = komando_datuak.한바이트(), INDIZE = komando_datuak.두바이트(); txeke_lokal(INDIZE, 지역변수수);
                if (luzapen_balio == 21 || luzapen_balio == 25) Irteera.add("PUSH(l[" + INDIZE + "]);");
                else if (luzapen_balio == 54 || luzapen_balio == 58) Irteera.add("l[" + INDIZE + "] = POP();");
                else if (luzapen_balio == 132) Irteera.add("l[" + INDIZE + "] = (uint32_t)l[" + INDIZE + "] + (uint32_t)(" + komando_datuak.부호두바이트() + ");");
                else throw new Itzulpena_errore("미지원 wide Komandoa");
            } else if (Komandoa == 198 || Komandoa == 199) {
                Irteera.add("a = POP();"); 분기넣기(Irteera, adar_Zerrenda, Posizioa, komando_datuak.부호두바이트(), "a " + (Komandoa == 198 ? "==" : "!=") + " 0");
            } else throw new Itzulpena_errore(FUNTZIOA_balio.jabe_balio + "." + FUNTZIOA_balio.Izena + ", byte_balio " + Posizioa + ": 미지원 Komandoa " + Komandoa);
        }
        if (!경계들.containsAll(adar_Zerrenda)) throw new Itzulpena_errore("Komandoa 경계가 아닌 곳으로 adar");
        Irteera.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Irteera);
    }
    String 내보낼함수(String lotu_ikur, String helburu_balio, boolean 진입점여부) {
        int kargu_INDIZE = helburu_balio.lastIndexOf('.'); if (kargu_INDIZE < 0 || !lotu_ikur.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Itzulpena_errore("내보내기 Esleitu_balio errorea");
        String jabe_balio = helburu_balio.substring(0, kargu_INDIZE).replace('.', '/'), Izena = helburu_balio.substring(kargu_INDIZE + 1); 함수참조 hautapen_balio = null;
        for (함수참조 Erreferentzia_materiala : 함수들.keySet()) if (Erreferentzia_materiala.jabe_balio.equals(jabe_balio) && Erreferentzia_materiala.Izena.equals(Izena)) {
            if (hautapen_balio != null) throw new Itzulpena_errore("겹친 내보내기 helburu_balio"); hautapen_balio = Erreferentzia_materiala;
        }
        if (hautapen_balio == null || (함수들.get(hautapen_balio).atzitu_sarrera & 0x100) != 0) throw new Itzulpena_errore("내보낼 함수가 없음 또는 native FUNTZIOA_balio");
        함수형식 formatu_balio = new 함수형식(hautapen_balio.서술);
        if ((진입점여부 && !formatu_balio.Argumentuak.isEmpty()) || !Arrays.asList("V", "I").contains(formatu_balio.itzuli_neurria)) throw new Itzulpena_errore("sarrera_p_balio 또는 C 경계 formatu_balio errorea");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formatu_balio.Argumentuak.size(); 순번++) {
            if (!formatu_balio.Argumentuak.get(순번).equals("I")) throw new Itzulpena_errore("C 경계는 int 인수만 Laguntza_balio");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formatu_balio.itzuli_neurria.equals("V") ? "void " : "int32_t ") + lotu_ikur + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + ikur("init", hautapen_balio.jabe_balio) + "(); " + (formatu_balio.itzuli_neurria.equals("V") ? "" : "return (int32_t)") + ikur("method", hautapen_balio.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String sortu(String sarrera_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<함수참조, kide_datuak> sarrera_balio : 함수들.entrySet()) {
            함수참조 Erreferentzia_materiala = sarrera_balio.getKey(); kide_datuak datuak = sarrera_balio.getValue(); 선언들.add(함수원형(Erreferentzia_materiala) + ";");
            if ((datuak.atzitu_sarrera & 0x100) != 0) {
                String Konektatu = gailu_Azure_Funtzioak_c3a8e64a.get(Erreferentzia_materiala.Izena + Erreferentzia_materiala.서술);
                if (!Erreferentzia_materiala.jabe_balio.equals(gailu_Gela) || Konektatu == null) throw new Itzulpena_errore("허용되지 않은 native FUNTZIOA_balio: " + Erreferentzia_materiala.Izena);
                int elementu_ZENBATU = new 함수형식(Erreferentzia_materiala.서술).Argumentuak.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < elementu_ZENBATU; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Konektatu + "(" + (elementu_ZENBATU == 0 ? "void" : String.join(",", Collections.nCopies(elementu_ZENBATU, "word"))) + ");");
                몸체들.add(함수원형(Erreferentzia_materiala) + " { return " + Konektatu + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Erreferentzia_materiala, datuak));
        }
        for (Map.Entry<함수참조, kide_datuak> sarrera_balio : 필드들.entrySet()) {
            함수참조 Erreferentzia_materiala = sarrera_balio.getKey(); byte[] konstante_balio = sarrera_balio.getValue().atributu_balio.get("ConstantValue");
            String balio = konstante_balio == null ? "0" : konstante_adierazpen(클래스들.get(Erreferentzia_materiala.jabe_balio), new datuak_irakurle(konstante_balio).두바이트());
            필드선언들.add("static word " + ikur("field", Erreferentzia_materiala.부분들()) + " = " + balio + ";");
        }
        for (String Izena : 클래스들.keySet()) {
            String hasieratu = ikur("init", Izena), Egoera_balio = ikur("state", Izena);
            선언들.add("static void " + hasieratu + "(void);"); 필드선언들.add("static unsigned " + Egoera_balio + ";");
            함수참조 Erreferentzia_materiala = new 함수참조(Izena, "<clinit>", "()V");
            몸체들.add("static void " + hasieratu + "(void) { if(" + Egoera_balio + ") return; " + Egoera_balio + " = 1; " + (함수들.containsKey(Erreferentzia_materiala) ? ikur("method", Erreferentzia_materiala.부분들()) + "(); " : "") + Egoera_balio + " = 2; }");
        }
        몸체들.add(내보낼함수("java_entry", sarrera_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Esleitu_balio : 내보내기목록) {
            int kargu_INDIZE = Esleitu_balio.indexOf('='); if (kargu_INDIZE < 1) throw new Itzulpena_errore("내보내기 Esleitu_balio errorea");
            String Izena = Esleitu_balio.substring(0, kargu_INDIZE); 공개이름.add(Izena); 몸체들.add(내보낼함수(Izena, Esleitu_balio.substring(kargu_INDIZE + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> sarrera_balio : 문자열들.entrySet()) {
            String Testua = sarrera_balio.getKey(); StringBuilder matrize_balio = new StringBuilder("static const word " + sarrera_balio.getValue() + "[] = {" + Testua.length());
            for (int 순번 = 0; 순번 < Testua.length(); 순번++) matrize_balio.append(", ").append((int)Testua.charAt(순번));
            문자열선언들.add(matrize_balio.append("};").toString());
        }
        String Laguntza_balio = Files.readString(baliabide_bide_izen.resolve("실행지원.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Laguntza_balio + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ITURBURUA, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> izen_taula = new HashMap<>();
        for (String Marra : Files.readAllLines(baliabide_bide_izen.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] parekatu_balio = Marra.split("\t"); izen_taula.put(parekatu_balio[0], parekatu_balio[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(ITURBURUA); StringBuffer EMAITZA = new StringBuffer();
        while (찾개.find()) {
            String Izena = 찾개.group(), 새이름 = Izena;
            if (!Izena.startsWith("//") && !Izena.startsWith("/*") && !Izena.startsWith("\"") && !Izena.startsWith("'") && !공개이름.contains(Izena)) {
                새이름 = izen_taula.getOrDefault(Izena, Izena);
                if (Izena.matches("a[0-9]+")) 새이름 = "Argumentuak" + Izena.substring(1);
                if (Izena.matches("b[0-9]+")) 새이름 = "adar" + Izena.substring(1);
                if (범용표기) {
                    StringBuilder notazio_balio = new StringBuilder();
                    for (char karaktere_balio : 새이름.toCharArray()) notazio_balio.append(karaktere_balio < 128 ? Character.toString(karaktere_balio) : String.format(Locale.ROOT, "\\u%04x", (int)karaktere_balio));
                    새이름 = notazio_balio.toString();
                }
            }
            찾개.appendReplacement(EMAITZA, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(EMAITZA); return EMAITZA.toString();
    }
    String 엑스함수본문(함수참조 FUNTZIOA_balio, kide_datuak datuak, Map<String,String> gailu_taula, String helburu_balio) {
        String 표식 = ikur("method", FUNTZIOA_balio.부분들());
        List<String> Marra = new ArrayList<>();
        if ((datuak.atzitu_sarrera & 0x100) != 0) {
            String Konektatu = gailu_taula.get(FUNTZIOA_balio.Izena + FUNTZIOA_balio.서술);
            if (!FUNTZIOA_balio.jabe_balio.equals(helburu_balio.equals("kernel") ? "gailu_balio" : "erabiltzaile") || Konektatu == null) throw new Itzulpena_errore("허용되지 않은 native FUNTZIOA_balio");
            return ".text\n" + 표식 + ":\njmp " + Konektatu;
        }
        byte[] testu_nagusi = datuak.atributu_balio.get("Code"); if (testu_nagusi == null) throw new Itzulpena_errore("FUNTZIOA_balio 몸체가 없음");
        datuak_irakurle irakurle_balio = new datuak_irakurle(testu_nagusi); irakurle_balio.두바이트(); int lokal_ZENBATU = irakurle_balio.두바이트();
        datuak_irakurle komando_datuak = new datuak_irakurle(irakurle_balio.Irakurri(irakurle_balio.네바이트()));
        if (irakurle_balio.두바이트() != 0) throw new Itzulpena_errore("try/catch/finally 미지원");
        함수형식 formatu_balio = new 함수형식(FUNTZIOA_balio.서술); if (lokal_ZENBATU < formatu_balio.Argumentuak.size()) throw new Itzulpena_errore("매개변수보다 적은 lokal_esparru 변수");
        Collections.addAll(Marra,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_ZENBATU * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formatu_balio.Argumentuak.size(); 순번++) Collections.addAll(Marra,"movl " + (8 + 4 * (formatu_balio.Argumentuak.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Gela_datuak Gela_balio = 클래스들.get(FUNTZIOA_balio.jabe_balio); Set<Integer> 경계들 = new HashSet<>(), adar_Zerrenda = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (komando_datuak.Posizioa < komando_datuak.datuak.length) {
            int Posizioa = komando_datuak.Posizioa, Komandoa = komando_datuak.한바이트(); String kargu_INDIZE = 표식 + "_b" + Posizioa;
            Marra.add(kargu_INDIZE + ":"); 경계들.add(Posizioa);
            if (Komandoa == 0) Marra.add("nop");
            else if (Komandoa == 1) Marra.add("pushl $0");
            else if (Komandoa >= 2 && Komandoa <= 8) Marra.add("pushl $" + (Komandoa - 3));
            else if (Komandoa == 16 || Komandoa == 17) Marra.add("pushl $" + (Komandoa == 16 ? komando_datuak.부호한바이트() : komando_datuak.부호두바이트()));
            else if (Komandoa == 18 || Komandoa == 19) {
                int INDIZE = Komandoa == 18 ? komando_datuak.한바이트() : komando_datuak.두바이트();
                Marra.add("pushl $" + X_86_konstante(Gela_balio,INDIZE));
            } else if (Komandoa == 21 || Komandoa == 25 || (Komandoa >= 26 && Komandoa <= 29) || (Komandoa >= 42 && Komandoa <= 45) || Komandoa == 54 || Komandoa == 58 || (Komandoa >= 59 && Komandoa <= 62) || (Komandoa >= 75 && Komandoa <= 78)) {
                boolean 읽음 = Komandoa < 54; int INDIZE = Komandoa == 21 || Komandoa == 25 || Komandoa == 54 || Komandoa == 58 ? komando_datuak.한바이트() : Komandoa - (Komandoa <= 29 ? 26 : Komandoa <= 45 ? 42 : Komandoa <= 62 ? 59 : 75);
                txeke_lokal(INDIZE,lokal_ZENBATU); Marra.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDIZE + 1)) + "(%ebp)");
            } else if (Komandoa == 46) Collections.addAll(Marra,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Komandoa == 79) Collections.addAll(Marra,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Komandoa == 87 || Komandoa == 88) Marra.add("addl $" + (Komandoa == 87 ? 4 : 8) + ", %esp");
            else if (Komandoa >= 89 && Komandoa <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ordena_Zerrenda = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Komandoa - 89]; 순번++) Marra.add("popl " + 저장기들[순번]);
                for (int 순번 : ordena_Zerrenda[Komandoa - 89]) Marra.add("pushl " + 저장기들[순번]);
            } else if (Komandoa == 96 || Komandoa == 100 || Komandoa == 104 || Komandoa == 126 || Komandoa == 128 || Komandoa == 130) {
                String kirurgia_balio = Komandoa == 96 ? "addl" : Komandoa == 100 ? "subl" : Komandoa == 104 ? "imull" : Komandoa == 126 ? "andl" : Komandoa == 128 ? "orl" : "xorl";
                Collections.addAll(Marra,"popl %ecx","popl %eax",kirurgia_balio + " %ecx, %eax","pushl %eax");
            } else if (Komandoa == 108 || Komandoa == 112) Collections.addAll(Marra,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + kargu_INDIZE + "_divide","cmpl $0x80000000, %eax","jne " + kargu_INDIZE + "_divide","xorl %edx, %edx","jmp " + kargu_INDIZE + "_done",kargu_INDIZE + "_divide:","cltd","idivl %ecx",kargu_INDIZE + "_done:","pushl " + (Komandoa == 108 ? "%eax" : "%edx"));
            else if (Komandoa == 116) Marra.add("negl (%esp)");
            else if (Komandoa == 120 || Komandoa == 122 || Komandoa == 124) Collections.addAll(Marra,"popl %ecx","popl %eax",(Komandoa == 120 ? "sall" : Komandoa == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Komandoa == 132) {
                int INDIZE = komando_datuak.한바이트(), 증가 = komando_datuak.부호한바이트(); txeke_lokal(INDIZE,lokal_ZENBATU); Marra.add("addl $" + 증가 + ", -" + (4 * (INDIZE + 1)) + "(%ebp)");
            } else if (Komandoa >= 145 && Komandoa <= 147) Collections.addAll(Marra,"popl %eax",Komandoa == 145 ? "movsbl %al, %eax" : Komandoa == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Komandoa >= 153 && Komandoa <= 166) {
                if (Komandoa <= 158) Collections.addAll(Marra,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Marra,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int helburu_balio_a0fbc067 = Posizioa + komando_datuak.부호두바이트(); adar_Zerrenda.add(helburu_balio_a0fbc067); Marra.add(비교들[Komandoa - (Komandoa <= 158 ? 153 : 159)] + " " + 표식 + "_b" + helburu_balio_a0fbc067);
            } else if (Komandoa == 167 || Komandoa == 200) {
                int helburu_balio_a0fbc067 = Posizioa + (Komandoa == 167 ? komando_datuak.부호두바이트() : komando_datuak.네바이트()); adar_Zerrenda.add(helburu_balio_a0fbc067); Marra.add("jmp " + 표식 + "_b" + helburu_balio_a0fbc067);
            } else if (Komandoa == 170 || Komandoa == 171) {
                while (komando_datuak.Posizioa % 4 != 0) komando_datuak.한바이트();
                int balio_lehenetsi = Posizioa + komando_datuak.네바이트(); adar_Zerrenda.add(balio_lehenetsi); Marra.add("popl %eax");
                int elementu_ZENBATU, 아래 = 0;
                if (Komandoa == 170) { 아래 = komando_datuak.네바이트(); int 위 = komando_datuak.네바이트(); long luzera_balio = (long)위 - 아래 + 1; if (luzera_balio < 1 || luzera_balio > (komando_datuak.datuak.length - komando_datuak.Posizioa) / 4) throw new Itzulpena_errore("switch klip errorea"); elementu_ZENBATU = (int)luzera_balio; }
                else { elementu_ZENBATU = komando_datuak.네바이트(); if (elementu_ZENBATU < 0 || elementu_ZENBATU > (komando_datuak.datuak.length - komando_datuak.Posizioa) / 8) throw new Itzulpena_errore("switch Tamaina errorea"); }
                for (int 순번 = 0; 순번 < elementu_ZENBATU; 순번++) {
                    int balio = Komandoa == 170 ? 아래 + 순번 : komando_datuak.네바이트(), helburu_balio_a0fbc067 = Posizioa + komando_datuak.네바이트(); adar_Zerrenda.add(helburu_balio_a0fbc067);
                    Collections.addAll(Marra,"cmpl $" + balio + ", %eax","je " + 표식 + "_b" + helburu_balio_a0fbc067);
                }
                Marra.add("jmp " + 표식 + "_b" + balio_lehenetsi);
            } else if (Komandoa == 172 || Komandoa == 176 || Komandoa == 177) {
                if (Komandoa != 177) Marra.add("popl %eax"); Collections.addAll(Marra,"leave","ret");
            } else if (Komandoa == 178 || Komandoa == 179) {
                함수참조 Erreferentzia_materiala = Gela_balio.Erreferentzia_materiala(komando_datuak.두바이트()); if (!필드들.containsKey(Erreferentzia_materiala)) throw new Itzulpena_errore("알 수 없는 eremu_balio");
                Collections.addAll(Marra,"call " + ikur("init",Erreferentzia_materiala.jabe_balio),(Komandoa == 178 ? "pushl " : "popl ") + ikur("field",Erreferentzia_materiala.부분들()));
            } else if (Komandoa == 184) {
                함수참조 Erreferentzia_materiala = Gela_balio.Erreferentzia_materiala(komando_datuak.두바이트()); if (!함수들.containsKey(Erreferentzia_materiala)) throw new Itzulpena_errore("알 수 없는 FUNTZIOA_balio");
                함수형식 호출형식 = new 함수형식(Erreferentzia_materiala.서술); Collections.addAll(Marra,"call " + ikur("init",Erreferentzia_materiala.jabe_balio),"call " + ikur("method",Erreferentzia_materiala.부분들()));
                if (!호출형식.Argumentuak.isEmpty()) Marra.add("addl $" + 호출형식.Argumentuak.size() * 4 + ", %esp");
                if (!호출형식.itzuli_neurria.equals("V")) Marra.add("pushl %eax");
            } else if (Komandoa == 182) {
                함수참조 Erreferentzia_materiala = Gela_balio.Erreferentzia_materiala(komando_datuak.두바이트());
                if (Erreferentzia_materiala.equals(new 함수참조("java/lang/String","length","()I"))) Collections.addAll(Marra,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Erreferentzia_materiala.equals(new 함수참조("java/lang/String","charAt","(I)C"))) Collections.addAll(Marra,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Itzulpena_errore("가상 FUNTZIOA_balio 호출 미지원");
            } else if (Komandoa == 188) {
                if (komando_datuak.한바이트() != 10) throw new Itzulpena_errore("new int[]만 Laguntza_balio"); Collections.addAll(Marra,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Komandoa == 190) Collections.addAll(Marra,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Komandoa == 196) {
                int luzapen_balio = komando_datuak.한바이트(), INDIZE = komando_datuak.두바이트(); txeke_lokal(INDIZE,lokal_ZENBATU);
                if (luzapen_balio == 21 || luzapen_balio == 25 || luzapen_balio == 54 || luzapen_balio == 58) Marra.add((luzapen_balio <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDIZE + 1) + "(%ebp)");
                else if (luzapen_balio == 132) Marra.add("addl $" + komando_datuak.부호두바이트() + ", -" + 4 * (INDIZE + 1) + "(%ebp)");
                else throw new Itzulpena_errore("wide Komandoa 미지원");
            } else if (Komandoa == 198 || Komandoa == 199) {
                int helburu_balio_a0fbc067 = Posizioa + komando_datuak.부호두바이트(); adar_Zerrenda.add(helburu_balio_a0fbc067); Collections.addAll(Marra,"popl %eax","testl %eax, %eax",(Komandoa == 198 ? "je " : "jne ") + 표식 + "_b" + helburu_balio_a0fbc067);
            } else throw new Itzulpena_errore("미지원 Komandoa: " + Komandoa);
        }
        if (!경계들.containsAll(adar_Zerrenda)) throw new Itzulpena_errore("Komandoa 경계가 아닌 곳으로 adar");
        Marra.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",Marra);
    }
    String X_86_konstante(Gela_datuak datuak, int INDIZE) {
        if (datuak.상수종류[INDIZE] == 3) return datuak.konstante_datuak[INDIZE].toString();
        if (datuak.상수종류[INDIZE] == 8) return kate_ikur(datuak.문자((Integer)datuak.konstante_datuak[INDIZE]));
        throw new Itzulpena_errore("정수와 kate_balio 상수만 Laguntza_balio");
    }
    String X_86_mihiztatze(String sarrera_p, List<String> 내보냄, String helburu_balio) throws IOException {
        Map<String,String> gailu_taula = new HashMap<>();
        for (String Marra : Files.readAllLines(baliabide_bide_izen.resolve("_86_gailu_Azure_Funtzioak.tsv"))) { String[] parekatu_balio = Marra.split("\t"); if (parekatu_balio[0].equals(helburu_balio)) gailu_taula.put(parekatu_balio[1] + parekatu_balio[2],parekatu_balio[3]); }
        int kargu_INDIZE = sarrera_p.lastIndexOf('.'); if (kargu_INDIZE < 0) throw new Itzulpena_errore("sarrera_p Esleitu_balio errorea");
        String jabe_balio = sarrera_p.substring(0,kargu_INDIZE).replace('.','/'), 함수이름 = sarrera_p.substring(kargu_INDIZE + 1); 함수참조 sarrera_p_balio = null;
        for (String 서술 : Arrays.asList("()I","()V")) { 함수참조 Erreferentzia_materiala = new 함수참조(jabe_balio,함수이름,서술); if (함수들.containsKey(Erreferentzia_materiala)) { if (sarrera_p_balio != null) throw new Itzulpena_errore("겹친 sarrera_p"); sarrera_p_balio = Erreferentzia_materiala; } }
        if (sarrera_p_balio == null || (함수들.get(sarrera_p_balio).atzitu_sarrera & 0x100) != 0) throw new Itzulpena_errore("sarrera_p_balio FUNTZIOA_balio formatu_balio errorea");
        List<String> Marra = new ArrayList<>(); Marra.add(".code32");
        for (Gela_datuak datuak : 클래스들.values()) {
            String Egoera_balio = ikur("state",datuak.Izena), hasieratu = ikur("init",datuak.Izena);
            Collections.addAll(Marra,".bss",".balign 4",Egoera_balio + ": .long 0",".text",hasieratu + ":","cmpl $0, " + Egoera_balio,"jne " + hasieratu + "_done","movl $1, " + Egoera_balio);
            함수참조 초기화참조 = new 함수참조(datuak.Izena,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Marra.add("call " + ikur("method",초기화참조.부분들()));
            Collections.addAll(Marra,"movl $2, " + Egoera_balio,hasieratu + "_done:","ret");
            for (kide_datuak eremu_balio : datuak.eremu_balio) {
                byte[] konstante_balio = eremu_balio.atributu_balio.get("ConstantValue"); String balio = konstante_balio == null ? "0" : X_86_konstante(datuak,new datuak_irakurle(konstante_balio).두바이트());
                Collections.addAll(Marra,".data",".balign 4",ikur("field",datuak.Izena,eremu_balio.Izena,eremu_balio.서술) + ": .long " + balio);
            }
            for (kide_datuak FUNTZIOA_balio : datuak.FUNTZIOA_balio) if (!FUNTZIOA_balio.Izena.equals("<init>")) Marra.add(엑스함수본문(new 함수참조(datuak.Izena,FUNTZIOA_balio.Izena,FUNTZIOA_balio.서술),FUNTZIOA_balio,gailu_taula,helburu_balio));
        }
        Collections.addAll(Marra,".text",".globl java_entry","java_entry:","call " + ikur("init",sarrera_p_balio.jabe_balio),"call " + ikur("method",sarrera_p_balio.부분들()));
        if (sarrera_p_balio.서술.equals("()V")) Marra.add("xorl %eax, %eax"); Marra.add("ret");
        for (String Esleitu_balio : 내보냄) {
            int mugatzaile_balio = Esleitu_balio.indexOf('='); if (mugatzaile_balio < 1) throw new Itzulpena_errore("내보내기 Esleitu_balio errorea");
            String 외부 = Esleitu_balio.substring(0,mugatzaile_balio), FUNTZIOA_balio = Esleitu_balio.substring(mugatzaile_balio + 1); int zatiketa_neurria = FUNTZIOA_balio.lastIndexOf('.');
            if (zatiketa_neurria < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Itzulpena_errore("내보내기 ikur errorea");
            String Gela_balio = FUNTZIOA_balio.substring(0,zatiketa_neurria).replace('.','/'), Izena = FUNTZIOA_balio.substring(zatiketa_neurria + 1); 함수참조 hautapen_balio = null;
            for (함수참조 Erreferentzia_materiala : 함수들.keySet()) if (Erreferentzia_materiala.jabe_balio.equals(Gela_balio) && Erreferentzia_materiala.Izena.equals(Izena)) { if (hautapen_balio != null) throw new Itzulpena_errore("겹친 내보내기 helburu_balio"); hautapen_balio = Erreferentzia_materiala; }
            if (hautapen_balio == null) throw new Itzulpena_errore("내보낼 함수가 없음");
            Collections.addAll(Marra,".text",".globl " + 외부,외부 + ":","call " + ikur("init",hautapen_balio.jabe_balio),"jmp " + ikur("method",hautapen_balio.부분들()));
        }
        Marra.add(".section .rodata");
        for (Map.Entry<String,String> sarrera_balio : 문자열들.entrySet()) {
            Collections.addAll(Marra,".balign 4",sarrera_balio.getValue() + ":",".long " + sarrera_balio.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char unitate_balio : sarrera_balio.getKey().toCharArray()) 단위들.add(Integer.toString(unitate_balio)); if (!단위들.isEmpty()) Marra.add(".long " + String.join(",",단위들));
        }
        Marra.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Marra) + "\n";
    }
    static void exekutatu_tresna(List<String> Komandoa) throws Exception {
        if (new ProcessBuilder(Komandoa).inheritIO().start().waitFor() != 0) throw new Itzulpena_errore("eraiki_iturburu errorea: " + Komandoa.get(0));
    }
    static String datuak_kate(String Testua) { return "\"" + Testua.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Itzulpena(List<Path> 입력들, String helburu_balio, String sarrera_p, List<String> 내보냄, Path Irteera, Path baliabide_balio) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Gela_bide_izen = 임시.resolve("classes"); Files.createDirectory(Gela_bide_izen);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Gela_bide_izen.toString(),"-sourcepath",Gela_bide_izen.toString(),"-d",Gela_bide_izen.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int iturburu_ZENBATU = 0;
            for (Path 입력 : 입력들) {
                if (Irteera.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Itzulpena_errore("Irteera 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); iturburu_ZENBATU++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Itzulpena_errore(".java 또는 .class만 Laguntza_balio");
            }
            if (iturburu_ZENBATU > 0) exekutatu_tresna(자바명령);
            try (java.util.stream.Stream<Path> bide_izen_Zerrenda = Files.walk(Gela_bide_izen)) { bide_izen_Zerrenda.filter(Bide_izena -> Bide_izena.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 BIHURTU_balio = new 기계어미리번역(바이트코드,helburu_balio.equals("user") ? "user" : "kernel",262144,baliabide_balio);
            String 조립 = BIHURTU_balio.X_86_mihiztatze(sarrera_p,내보냄,helburu_balio); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path tresna_kargu = baliabide_balio.getParent();
            exekutatu_tresna(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            exekutatu_tresna(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),tresna_kargu.resolve("실행지원.s").toString()));
            List<String> Konektatu = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (helburu_balio.equals("kernel")) Konektatu.add("-r");
            else {
                exekutatu_tresna(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),tresna_kargu.resolve(helburu_balio.equals("user") ? "HASI_erabiltzaile_aplik.s" : "리눅스시작.s").toString()));
                Collections.addAll(Konektatu,"-e","_start",임시.resolve("start.o").toString());
                if (helburu_balio.equals("user")) Collections.addAll(Konektatu,"-T",tresna_kargu.resolve("erabiltzaile_lotu_diseinu.ld").toString());
            }
            Collections.addAll(Konektatu,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); exekutatu_tresna(Konektatu);
            Irteera = Irteera.toAbsolutePath(); Files.createDirectories(Irteera.getParent()); Path argitaratu_balio = Files.createTempFile(Irteera.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),argitaratu_balio,StandardCopyOption.REPLACE_EXISTING); Files.move(argitaratu_balio,Irteera,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(argitaratu_balio); }
            Files.setPosixFilePermissions(Irteera,java.nio.file.attribute.PosixFilePermissions.fromString(helburu_balio.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Irteera + ".s"),조립,StandardCharsets.UTF_8);
            List<String> ikur_datuak = new ArrayList<>(), iturburu_datu = new ArrayList<>();
            for (함수참조 Erreferentzia_materiala : BIHURTU_balio.함수들.keySet()) ikur_datuak.add(datuak_kate(ikur("method",Erreferentzia_materiala.부분들())) + ":" + datuak_kate(Erreferentzia_materiala.jabe_balio + "." + Erreferentzia_materiala.Izena + Erreferentzia_materiala.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_fitxategi = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Testua = new StringBuilder(); for (byte balio : hash_fitxategi) Testua.append(String.format(Locale.ROOT,"%02x",balio & 255));
                iturburu_datu.add(datuak_kate(입력.toAbsolutePath().toString()) + ":" + datuak_kate(Testua.toString()));
            }
            Files.writeString(Paths.get(Irteera + ".json"),"{\"target\":" + datuak_kate(helburu_balio) + ",\"entry\":" + datuak_kate(sarrera_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",ikur_datuak) + "},\"sources\":{" + String.join(",",iturburu_datu) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> bide_izen_Zerrenda = Files.walk(임시)) { for (Path Bide_izena : (Iterable<Path>)bide_izen_Zerrenda.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Bide_izena); }
        }
    }
    public static void main(String[] Argumentuak) {
        try {
            String sarrera_p = null, helburu_balio = "kernel", X_86_helburu = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> bide_izen_Zerrenda = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumentuak.length; 순번++) {
                String balio = Argumentuak[순번];
                switch (balio) {
                    case "--target": X_86_helburu = Argumentuak[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Gela_balio.FUNTZIOA_balio -o Irteera [--target linux|kernel|user] [--profile kernel|user] [--export ikur=Gela_balio.FUNTZIOA_balio] 클래스파일 또는 Java원문"); return;
                    case "--entry": sarrera_p = Argumentuak[++순번]; break;
                    case "--profile": helburu_balio = Argumentuak[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumentuak[++순번]); break;
                    case "--export": 내보냄.add(Argumentuak[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argumentuak[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (balio.startsWith("-")) throw new Itzulpena_errore("알 수 없는 옵션: " + balio); bide_izen_Zerrenda.add(Paths.get(balio));
                }
            }
            if (sarrera_p == null || 출력경로 == null || bide_izen_Zerrenda.isEmpty()) throw new Itzulpena_errore("--entry, -o, Gela_balio 파일이 필요합니다");
            Path baliabide_balio = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_helburu != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_helburu)) throw new Itzulpena_errore("알 수 없는 exekutatu_komando helburu_balio");
                X_86_Itzulpena(bide_izen_Zerrenda,X_86_helburu,sarrera_p,내보냄,출력경로,baliabide_balio); return;
            }
            String ITURBURUA = new 기계어미리번역(bide_izen_Zerrenda, helburu_balio, 낱말수, baliabide_balio).sortu(sarrera_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ITURBURUA, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception errorea) { System.err.println("eraiki_iturburu errorea: " + errorea.getMessage()); System.exit(1); }
    }
}
