// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Klass_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. Host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Iwwersetzung_Feeler extends RuntimeException {
        Iwwersetzung_Feeler(String 설명) { super(설명); }
    }
    static final class Daten_Lieser {
        final byte[] Daten;
        int positionéieren;
        Daten_Lieser(byte[] 입력자료) { Daten = 입력자료; }
        byte[] 읽기(int Längt_VALUE) {
            if (Längt_VALUE < 0 || Längt_VALUE > Daten.length - positionéieren) throw new Iwwersetzung_Feeler("잘린 Klass_VALUE 또는 Befeel Daten");
            byte[] Mooss = Arrays.copyOfRange(Daten, positionéieren, positionéieren + Längt_VALUE); positionéieren += Längt_VALUE; return Mooss;
        }
        int 한바이트() { if (positionéieren >= Daten.length) throw new Iwwersetzung_Feeler("잘린 Befeel Daten"); return Daten[positionéieren++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class Member_Daten {
        final int Zougrëff_Agab;
        final String Numm, 서술;
        final Map<String, byte[]> Attribut_VALUE;
        Member_Daten(int Zougrëff_VALUE, String Numm_VALUE, String 서술값, Map<String, byte[]> Attribut_Daten) {
            Zougrëff_Agab = Zougrëff_VALUE; Numm = Numm_VALUE; 서술 = 서술값; Attribut_VALUE = Attribut_Daten;
        }
    }
    static final class Method_Referenzen implements Comparable<Method_Referenzen> {
        final String Besëtzer_VALUE, Numm, 서술;
        Method_Referenzen(String 소유값, String Numm_VALUE, String 서술값) { Besëtzer_VALUE = 소유값; Numm = Numm_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{Besëtzer_VALUE, Numm, 서술}; }
        public int compareTo(Method_Referenzen Peer_VALUE) {
            int 비교값 = Besëtzer_VALUE.compareTo(Peer_VALUE.Besëtzer_VALUE);
            if (비교값 == 0) 비교값 = Numm.compareTo(Peer_VALUE.Numm);
            return 비교값 == 0 ? 서술.compareTo(Peer_VALUE.서술) : 비교값;
        }
        public boolean equals(Object Peer_VALUE) { return Peer_VALUE instanceof Method_Referenzen && compareTo((Method_Referenzen) Peer_VALUE) == 0; }
        public int hashCode() { return Objects.hash(Besëtzer_VALUE, Numm, 서술); }
    }
    static final class Klass_Daten {
        final int[] 상수종류;
        final Object[] Konstant_Daten;
        final String Numm;
        final List<Member_Daten> Feld_VALUE, FUNCTION_VALUE;
        Klass_Daten(Path Wee) throws IOException {
            Daten_Lieser Lieser_VALUE = new Daten_Lieser(Files.readAllBytes(Wee));
            if (Lieser_VALUE.네바이트() != 0xcafebabe) throw new Iwwersetzung_Feeler("Java Klass_VALUE 표식이 아님");
            Lieser_VALUE.읽기(4);
            int Element_COUNT = Lieser_VALUE.두바이트(); 상수종류 = new int[Element_COUNT]; Konstant_Daten = new Object[Element_COUNT];
            for (int 순번 = 1; 순번 < Element_COUNT; 순번++) {
                int 종류 = Lieser_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int Längt_VALUE = Lieser_VALUE.두바이트();
                        byte[] Zeechen_Puffer = Lieser_VALUE.읽기(Längt_VALUE), 길이붙인자료 = new byte[Längt_VALUE + 2];
                        길이붙인자료[0] = (byte)(Längt_VALUE >> 8); 길이붙인자료[1] = (byte)Längt_VALUE;
                        System.arraycopy(Zeechen_Puffer, 0, 길이붙인자료, 2, Längt_VALUE);
                        Konstant_Daten[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: Konstant_Daten[순번] = Lieser_VALUE.네바이트(); break;
                    case 4: Lieser_VALUE.읽기(4); break;
                    case 5: case 6: Lieser_VALUE.읽기(8); 순번++; break;
                    case 7: case 8: case 16: Konstant_Daten[순번] = Lieser_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        Konstant_Daten[순번] = new int[]{Lieser_VALUE.두바이트(), Lieser_VALUE.두바이트()}; break;
                    case 15: Konstant_Daten[순번] = new int[]{Lieser_VALUE.한바이트(), Lieser_VALUE.두바이트()}; break;
                    default: throw new Iwwersetzung_Feeler("지원하지 않는 Konstant_VALUE 종류: " + 종류);
                }
            }
            Lieser_VALUE.두바이트(); Numm = Klass_Numm(Lieser_VALUE.두바이트());
            if (!Klass_Numm(Lieser_VALUE.두바이트()).equals("java/lang/Object") || Lieser_VALUE.두바이트() != 0)
                throw new Iwwersetzung_Feeler(Numm + ": 상속 및 인터페이스 미지원");
            Feld_VALUE = 멤버읽기(Lieser_VALUE); FUNCTION_VALUE = 멤버읽기(Lieser_VALUE); 속성읽기(Lieser_VALUE);
            if (Lieser_VALUE.positionéieren != Lieser_VALUE.Daten.length) throw new Iwwersetzung_Feeler("Klass_VALUE 뒤에 남은 Daten");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Iwwersetzung_Feeler("문자 Konstant_VALUE INDEX Feeler");
            return (String) Konstant_Daten[INDEX];
        }
        String Klass_Numm(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Iwwersetzung_Feeler("Klass_VALUE Referenzen Feeler");
            return 문자((Integer)Konstant_Daten[INDEX]);
        }
        Method_Referenzen Referenzen(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Iwwersetzung_Feeler("멤버 Referenzen Feeler");
            int[] ukoppelen_VALUE = (int[])Konstant_Daten[INDEX], Numm_ukoppelen = (int[])Konstant_Daten[ukoppelen_VALUE[1]];
            return new Method_Referenzen(Klass_Numm(ukoppelen_VALUE[0]), 문자(Numm_ukoppelen[0]), 문자(Numm_ukoppelen[1]));
        }
        Map<String, byte[]> 속성읽기(Daten_Lieser Lieser_VALUE) {
            Map<String, byte[]> Mooss = new LinkedHashMap<>();
            int Element_COUNT = Lieser_VALUE.두바이트();
            for (int 순번 = 0; 순번 < Element_COUNT; 순번++) {
                String Attribut_Numm = 문자(Lieser_VALUE.두바이트()); byte[] VALUE = Lieser_VALUE.읽기(Lieser_VALUE.네바이트());
                if (Mooss.put(Attribut_Numm, VALUE) != null) throw new Iwwersetzung_Feeler("겹친 Attribut_VALUE: " + Attribut_Numm);
            }
            return Mooss;
        }
        List<Member_Daten> 멤버읽기(Daten_Lieser Lieser_VALUE) {
            List<Member_Daten> Mooss = new ArrayList<>(); int Element_COUNT = Lieser_VALUE.두바이트();
            for (int 순번 = 0; 순번 < Element_COUNT; 순번++) {
                int Zougrëff_Agab = Lieser_VALUE.두바이트(); String Method_Agab_Numm = 문자(Lieser_VALUE.두바이트()), 서술 = 문자(Lieser_VALUE.두바이트());
                Mooss.add(new Member_Daten(Zougrëff_Agab, Method_Agab_Numm, 서술, 속성읽기(Lieser_VALUE)));
            }
            return Mooss;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Iwwersetzung_Feeler("FUNCTION_VALUE 서술 Feeler: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Iwwersetzung_Feeler("FUNCTION_VALUE 서술 Feeler: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Iwwersetzung_Feeler("FUNCTION_VALUE 서술 Feeler: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> Mooss = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int positionéieren = 0; positionéieren < 서술.length();) {
            String Auswiel_VALUE = null;
            for (String Format_VALUE : 허용형식) if (서술.startsWith(Format_VALUE, positionéieren)) { Auswiel_VALUE = Format_VALUE; break; }
            if (Auswiel_VALUE == null) throw new Iwwersetzung_Feeler("지원하지 않는 Datentyp: " + 서술);
            Mooss.add(Auswiel_VALUE); positionéieren += Auswiel_VALUE.length();
        }
        return Mooss;
    }
    static String Symbol(String 종류, String... 부분들) {
        try {
            byte[] Hash_Fichier = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", Hash_Fichier[순번] & 255));
            return SMS.toString();
        } catch (Exception Feeler) { throw new Iwwersetzung_Feeler(Feeler.toString()); }
    }
    final Map<String, Klass_Daten> 클래스들 = new TreeMap<>();
    final Map<Method_Referenzen, Member_Daten> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, Computer_Klass;
    final int 동적기억낱말수;
    final Path Ressource_Wee;
    기계어미리번역(List<Path> Wee_Lëscht, String Zil, int 낱말수, Path Ressource_VALUE) throws IOException {
        if ((!Zil.equals("kernel") && !Zil.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Iwwersetzung_Feeler("ausféieren_Befeel Zil 또는 Späicher_VALUE 공간 d_Gréisst_veränneren Feeler");
        실행대상 = Zil; 동적기억낱말수 = 낱말수; Ressource_Wee = Ressource_VALUE;
        // 이 이름도 국가별 Quell_Bamstruktur generéieren 시 해당 언어로 옮긴다.
        Computer_Klass = Zil.equals("kernel") ? "Board" : "Benotzer";
        for (String Zeil : Files.readAllLines(Ressource_VALUE.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Zeil.split("\t", -1);
            if (부분들.length != 4) throw new Iwwersetzung_Feeler("Computer FUNCTION_VALUE Daten Feeler");
            if (부분들[0].equals(Zil)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Wee : Wee_Lëscht) {
            Klass_Daten Daten = new Klass_Daten(Wee);
            if (클래스들.put(Daten.Numm, Daten) != null) throw new Iwwersetzung_Feeler("중복 Klass_VALUE: " + Daten.Numm);
            for (Member_Daten Feld_VALUE : Daten.Feld_VALUE) {
                if ((Feld_VALUE.Zougrëff_Agab & 8) == 0 || 형식읽기(Feld_VALUE.서술).equals(Collections.singletonList("V"))) throw new Iwwersetzung_Feeler("statesch_VALUE 필드만 Support_VALUE");
                if (필드들.put(new Method_Referenzen(Daten.Numm, Feld_VALUE.Numm, Feld_VALUE.서술), Feld_VALUE) != null) throw new Iwwersetzung_Feeler("중복 Feld_VALUE");
            }
            for (Member_Daten FUNCTION_VALUE : Daten.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Numm.equals("<init>")) continue;
                if ((FUNCTION_VALUE.Zougrëff_Agab & 8) == 0 || (FUNCTION_VALUE.Zougrëff_Agab & (0x20 | 0x400)) != 0) throw new Iwwersetzung_Feeler("statesch_VALUE 비동기화 함수만 Support_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new Method_Referenzen(Daten.Numm, FUNCTION_VALUE.Numm, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Iwwersetzung_Feeler("중복 FUNCTION_VALUE");
            }
        }
    }
    String Zeechefolleg_Symbol(String SMS) { return 문자열들.computeIfAbsent(SMS, VALUE -> "j_text_" + 문자열들.size()); }
    String Konstant_Ausdrock(Klass_Daten Daten, int INDEX) {
        if (INDEX < 1 || INDEX >= Daten.상수종류.length) throw new Iwwersetzung_Feeler("Konstant_VALUE INDEX Clip Feeler");
        if (Daten.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + Daten.Konstant_Daten[INDEX] + ")";
        if (Daten.상수종류[INDEX] == 8) return "(word)" + Zeechefolleg_Symbol(Daten.문자((Integer)Daten.Konstant_Daten[INDEX]));
        throw new Iwwersetzung_Feeler("정수와 Zeechefolleg_VALUE 상수만 Support_VALUE");
    }
    String 함수원형(Method_Referenzen Referenzen) {
        List<String> 인수들 = new ArrayList<>(); int Element_COUNT = new 함수형식(Referenzen.서술).인수.size();
        for (int 순번 = 0; 순번 < Element_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + Symbol("method", Referenzen.부분들()) + "(" + (Element_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void Scheck_lokal(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Iwwersetzung_Feeler("lokal_Beräich 변수 INDEX Clip Feeler"); }
    void 분기넣기(List<String> 출력, Set<Integer> Branche_Lëscht, int positionéieren, int 이동량, String Bedéngung) {
        int Zil_VALUE = positionéieren + 이동량; Branche_Lëscht.add(Zil_VALUE);
        출력.add((Bedéngung == null ? "" : "if (" + Bedéngung + ") ") + "goto b" + Zil_VALUE + ";");
    }
    String 함수본문(Method_Referenzen FUNCTION_VALUE, Member_Daten Daten) {
        byte[] 본문자료 = Daten.Attribut_VALUE.get("Code"); if (본문자료 == null) throw new Iwwersetzung_Feeler("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Numm);
        Daten_Lieser Lieser_VALUE = new Daten_Lieser(본문자료); int 쌓임깊이 = Lieser_VALUE.두바이트(), 지역변수수 = Lieser_VALUE.두바이트();
        Daten_Lieser Befeel_Daten = new Daten_Lieser(Lieser_VALUE.읽기(Lieser_VALUE.네바이트()));
        if (Lieser_VALUE.두바이트() != 0) throw new Iwwersetzung_Feeler("try/catch/finally 미지원");
        함수형식 Format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (지역변수수 < Format_VALUE.인수.size()) throw new Iwwersetzung_Feeler("매개변수보다 적은 lokal_Beräich 변수");
        Klass_Daten Klass_VALUE = 클래스들.get(FUNCTION_VALUE.Besëtzer_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(FUNCTION_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < Format_VALUE.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), Branche_Lëscht = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (Befeel_Daten.positionéieren < Befeel_Daten.Daten.length) {
            int positionéieren = Befeel_Daten.positionéieren, Befeel = Befeel_Daten.한바이트(); 경계들.add(positionéieren); 출력.add("b" + positionéieren + ":;");
            if (Befeel == 0) continue;
            if (Befeel == 1) 출력.add("PUSH(0);");
            else if (Befeel >= 2 && Befeel <= 8) 출력.add("PUSH((uint32_t)(" + (Befeel - 3) + "));");
            else if (Befeel == 16 || Befeel == 17) 출력.add("PUSH((uint32_t)(" + (Befeel == 16 ? Befeel_Daten.부호한바이트() : Befeel_Daten.부호두바이트()) + "));");
            else if (Befeel == 18 || Befeel == 19) 출력.add("PUSH(" + Konstant_Ausdrock(Klass_VALUE, Befeel == 18 ? Befeel_Daten.한바이트() : Befeel_Daten.두바이트()) + ");");
            else if (Befeel == 21 || Befeel == 25 || (Befeel >= 26 && Befeel <= 29) || (Befeel >= 42 && Befeel <= 45)) {
                int INDEX = Befeel == 21 || Befeel == 25 ? Befeel_Daten.한바이트() : Befeel - (Befeel <= 29 ? 26 : 42);
                Scheck_lokal(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (Befeel == 54 || Befeel == 58 || (Befeel >= 59 && Befeel <= 62) || (Befeel >= 75 && Befeel <= 78)) {
                int INDEX = Befeel == 54 || Befeel == 58 ? Befeel_Daten.한바이트() : Befeel - (Befeel <= 62 ? 59 : 75);
                Scheck_lokal(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (Befeel == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Befeel == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Befeel == 87 || Befeel == 88) 출력.add(Befeel == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Befeel >= 89 && Befeel <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] Reiefolleg_Lëscht = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Befeel - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : Reiefolleg_Lëscht[Befeel - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (Befeel == 96 || Befeel == 100 || Befeel == 104 || Befeel == 126 || Befeel == 128 || Befeel == 130) {
                String Operatioun_VALUE = Befeel == 96 ? "+" : Befeel == 100 ? "-" : Befeel == 104 ? "*" : Befeel == 126 ? "&" : Befeel == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + Operatioun_VALUE + " (uint32_t)b);");
            } else if (Befeel == 108 || Befeel == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Befeel == 112 ? 1 : 0) + "));");
            else if (Befeel == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Befeel == 120 || Befeel == 122 || Befeel == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Befeel == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Befeel == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Befeel == 132) {
                int INDEX = Befeel_Daten.한바이트(), 증가량 = Befeel_Daten.부호한바이트(); Scheck_lokal(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Befeel >= 145 && Befeel <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Befeel == 145 ? "int8_t" : Befeel == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Befeel >= 153 && Befeel <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, Branche_Lëscht, positionéieren, Befeel_Daten.부호두바이트(), "(int32_t)a " + 비교들[Befeel - 153] + " 0");
            } else if (Befeel >= 159 && Befeel <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, Branche_Lëscht, positionéieren, Befeel_Daten.부호두바이트(), Befeel >= 165 ? "a " + 비교들[Befeel - 159] + " b" : "(int32_t)a " + 비교들[Befeel - 159] + " (int32_t)b");
            } else if (Befeel == 167 || Befeel == 200) 분기넣기(출력, Branche_Lëscht, positionéieren, Befeel == 167 ? Befeel_Daten.부호두바이트() : Befeel_Daten.네바이트(), null);
            else if (Befeel == 170 || Befeel == 171) {
                while (Befeel_Daten.positionéieren % 4 != 0) Befeel_Daten.한바이트();
                int Standardwäert = Befeel_Daten.네바이트(); 출력.add("a = POP();");
                if (Befeel == 170) {
                    int 아래 = Befeel_Daten.네바이트(), 위 = Befeel_Daten.네바이트(); long Element_COUNT = (long)위 - 아래 + 1;
                    if (Element_COUNT < 1 || Element_COUNT > (Befeel_Daten.Daten.length - Befeel_Daten.positionéieren) / 4) throw new Iwwersetzung_Feeler("switch Clip Feeler");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, Branche_Lëscht, positionéieren, Befeel_Daten.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int Element_COUNT = Befeel_Daten.네바이트(), 앞값 = 0;
                    if (Element_COUNT < 0 || Element_COUNT > (Befeel_Daten.Daten.length - Befeel_Daten.positionéieren) / 8) throw new Iwwersetzung_Feeler("switch d_Gréisst_veränneren Feeler");
                    for (int 순번 = 0; 순번 < Element_COUNT; 순번++) {
                        int VALUE = Befeel_Daten.네바이트(); if (순번 > 0 && VALUE <= 앞값) throw new Iwwersetzung_Feeler("switch Reiefolleg_VALUE Feeler"); 앞값 = VALUE;
                        분기넣기(출력, Branche_Lëscht, positionéieren, Befeel_Daten.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, Branche_Lëscht, positionéieren, Standardwäert, null);
            } else if (Befeel == 172 || Befeel == 176 || Befeel == 177) 출력.add("return " + (Befeel == 177 ? "0" : "POP()") + ";");
            else if (Befeel == 178 || Befeel == 179) {
                Method_Referenzen Referenzen = Klass_VALUE.Referenzen(Befeel_Daten.두바이트()); if (!필드들.containsKey(Referenzen)) throw new Iwwersetzung_Feeler("알 수 없는 Feld_VALUE");
                출력.add(Symbol("init", Referenzen.Besëtzer_VALUE) + "();"); String Feld_VALUE = Symbol("field", Referenzen.부분들());
                출력.add(Befeel == 178 ? "PUSH(" + Feld_VALUE + ");" : Feld_VALUE + " = POP();");
            } else if (Befeel == 184) {
                Method_Referenzen Referenzen = Klass_VALUE.Referenzen(Befeel_Daten.두바이트()); if (!함수들.containsKey(Referenzen)) throw new Iwwersetzung_Feeler("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Referenzen.서술); int Element_COUNT = 호출형식.인수.size();
                출력.add(Symbol("init", Referenzen.Besëtzer_VALUE) + "();"); 출력.add("if(sp < " + Element_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + Element_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < Element_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + Symbol("method", Referenzen.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Befeel == 182) {
                Method_Referenzen Referenzen = Klass_VALUE.Referenzen(Befeel_Daten.두바이트());
                if (Referenzen.equals(new Method_Referenzen("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Referenzen.equals(new Method_Referenzen("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Iwwersetzung_Feeler("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Befeel == 188) {
                if (Befeel_Daten.한바이트() != 10) throw new Iwwersetzung_Feeler("new int[]만 Support_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Befeel == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Befeel == 196) {
                int Extensioun_VALUE = Befeel_Daten.한바이트(), INDEX = Befeel_Daten.두바이트(); Scheck_lokal(INDEX, 지역변수수);
                if (Extensioun_VALUE == 21 || Extensioun_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (Extensioun_VALUE == 54 || Extensioun_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (Extensioun_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + Befeel_Daten.부호두바이트() + ");");
                else throw new Iwwersetzung_Feeler("미지원 wide Befeel");
            } else if (Befeel == 198 || Befeel == 199) {
                출력.add("a = POP();"); 분기넣기(출력, Branche_Lëscht, positionéieren, Befeel_Daten.부호두바이트(), "a " + (Befeel == 198 ? "==" : "!=") + " 0");
            } else throw new Iwwersetzung_Feeler(FUNCTION_VALUE.Besëtzer_VALUE + "." + FUNCTION_VALUE.Numm + ", Byte_VALUE " + positionéieren + ": 미지원 Befeel " + Befeel);
        }
        if (!경계들.containsAll(Branche_Lëscht)) throw new Iwwersetzung_Feeler("Befeel 경계가 아닌 곳으로 Branche");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String exportéieren_Method(String Link_Symbol, String Zil, boolean 진입점여부) {
        int positionéieren_INDEX = Zil.lastIndexOf('.'); if (positionéieren_INDEX < 0 || !Link_Symbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Iwwersetzung_Feeler("내보내기 지정 Feeler");
        String Besëtzer_VALUE = Zil.substring(0, positionéieren_INDEX).replace('.', '/'), Numm = Zil.substring(positionéieren_INDEX + 1); Method_Referenzen Auswiel_VALUE = null;
        for (Method_Referenzen Referenzen : 함수들.keySet()) if (Referenzen.Besëtzer_VALUE.equals(Besëtzer_VALUE) && Referenzen.Numm.equals(Numm)) {
            if (Auswiel_VALUE != null) throw new Iwwersetzung_Feeler("겹친 내보내기 Zil"); Auswiel_VALUE = Referenzen;
        }
        if (Auswiel_VALUE == null || (함수들.get(Auswiel_VALUE).Zougrëff_Agab & 0x100) != 0) throw new Iwwersetzung_Feeler("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 Format_VALUE = new 함수형식(Auswiel_VALUE.서술);
        if ((진입점여부 && !Format_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(Format_VALUE.반환)) throw new Iwwersetzung_Feeler("Agab_Punkt_VALUE 또는 C 경계 Format_VALUE Feeler");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < Format_VALUE.인수.size(); 순번++) {
            if (!Format_VALUE.인수.get(순번).equals("I")) throw new Iwwersetzung_Feeler("C 경계는 int 인수만 Support_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (Format_VALUE.반환.equals("V") ? "void " : "int32_t ") + Link_Symbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + Symbol("init", Auswiel_VALUE.Besëtzer_VALUE) + "(); " + (Format_VALUE.반환.equals("V") ? "" : "return (int32_t)") + Symbol("method", Auswiel_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generéieren(String Agab_Punkt, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<Method_Referenzen, Member_Daten> Agab_VALUE : 함수들.entrySet()) {
            Method_Referenzen Referenzen = Agab_VALUE.getKey(); Member_Daten Daten = Agab_VALUE.getValue(); 선언들.add(함수원형(Referenzen) + ";");
            if ((Daten.Zougrëff_Agab & 0x100) != 0) {
                String Verbannen = 기계함수들.get(Referenzen.Numm + Referenzen.서술);
                if (!Referenzen.Besëtzer_VALUE.equals(Computer_Klass) || Verbannen == null) throw new Iwwersetzung_Feeler("허용되지 않은 native FUNCTION_VALUE: " + Referenzen.Numm);
                int Element_COUNT = new 함수형식(Referenzen.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < Element_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Verbannen + "(" + (Element_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(Element_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Referenzen) + " { return " + Verbannen + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Referenzen, Daten));
        }
        for (Map.Entry<Method_Referenzen, Member_Daten> Agab_VALUE : 필드들.entrySet()) {
            Method_Referenzen Referenzen = Agab_VALUE.getKey(); byte[] Konstant_VALUE = Agab_VALUE.getValue().Attribut_VALUE.get("ConstantValue");
            String VALUE = Konstant_VALUE == null ? "0" : Konstant_Ausdrock(클래스들.get(Referenzen.Besëtzer_VALUE), new Daten_Lieser(Konstant_VALUE).두바이트());
            필드선언들.add("static word " + Symbol("field", Referenzen.부분들()) + " = " + VALUE + ";");
        }
        for (String Numm : 클래스들.keySet()) {
            String initialiséieren = Symbol("init", Numm), Status_VALUE = Symbol("state", Numm);
            선언들.add("static void " + initialiséieren + "(void);"); 필드선언들.add("static unsigned " + Status_VALUE + ";");
            Method_Referenzen Referenzen = new Method_Referenzen(Numm, "<clinit>", "()V");
            몸체들.add("static void " + initialiséieren + "(void) { if(" + Status_VALUE + ") return; " + Status_VALUE + " = 1; " + (함수들.containsKey(Referenzen) ? Symbol("method", Referenzen.부분들()) + "(); " : "") + Status_VALUE + " = 2; }");
        }
        몸체들.add(exportéieren_Method("java_entry", Agab_Punkt, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int positionéieren_INDEX = 지정.indexOf('='); if (positionéieren_INDEX < 1) throw new Iwwersetzung_Feeler("내보내기 지정 Feeler");
            String Numm = 지정.substring(0, positionéieren_INDEX); 공개이름.add(Numm); 몸체들.add(exportéieren_Method(Numm, 지정.substring(positionéieren_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> Agab_VALUE : 문자열들.entrySet()) {
            String SMS = Agab_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + Agab_VALUE.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) ARRAY_VALUE.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Support_VALUE = Files.readString(Ressource_Wee.resolve("Common_Language_Runtime_Support.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Support_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String Quell, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> Numm_Tabell = new HashMap<>();
        for (String Zeil : Files.readAllLines(Ressource_Wee.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] ukoppelen_VALUE = Zeil.split("\t"); Numm_Tabell.put(ukoppelen_VALUE[0], ukoppelen_VALUE[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(Quell); StringBuffer Mooss = new StringBuffer();
        while (찾개.find()) {
            String Numm = 찾개.group(), 새이름 = Numm;
            if (!Numm.startsWith("//") && !Numm.startsWith("/*") && !Numm.startsWith("\"") && !Numm.startsWith("'") && !공개이름.contains(Numm)) {
                새이름 = Numm_Tabell.getOrDefault(Numm, Numm);
                if (Numm.matches("a[0-9]+")) 새이름 = "인수" + Numm.substring(1);
                if (Numm.matches("b[0-9]+")) 새이름 = "Branche" + Numm.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char Zeechen_VALUE : 새이름.toCharArray()) 표기.append(Zeechen_VALUE < 128 ? Character.toString(Zeechen_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)Zeechen_VALUE));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(Mooss, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(Mooss); return Mooss.toString();
    }
    String 엑스함수본문(Method_Referenzen FUNCTION_VALUE, Member_Daten Daten, Map<String,String> Computer_Tabell, String Zil) {
        String Markéierung_VALUE = Symbol("method", FUNCTION_VALUE.부분들());
        List<String> Zeil = new ArrayList<>();
        if ((Daten.Zougrëff_Agab & 0x100) != 0) {
            String Verbannen = Computer_Tabell.get(FUNCTION_VALUE.Numm + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.Besëtzer_VALUE.equals(Zil.equals("kernel") ? "Mobil_VALUE" : "Benotzer") || Verbannen == null) throw new Iwwersetzung_Feeler("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + Markéierung_VALUE + ":\njmp " + Verbannen;
        }
        byte[] Textkierper = Daten.Attribut_VALUE.get("Code"); if (Textkierper == null) throw new Iwwersetzung_Feeler("FUNCTION_VALUE 몸체가 없음");
        Daten_Lieser Lieser_VALUE = new Daten_Lieser(Textkierper); Lieser_VALUE.두바이트(); int lokal_COUNT = Lieser_VALUE.두바이트();
        Daten_Lieser Befeel_Daten = new Daten_Lieser(Lieser_VALUE.읽기(Lieser_VALUE.네바이트()));
        if (Lieser_VALUE.두바이트() != 0) throw new Iwwersetzung_Feeler("try/catch/finally 미지원");
        함수형식 Format_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (lokal_COUNT < Format_VALUE.인수.size()) throw new Iwwersetzung_Feeler("매개변수보다 적은 lokal_Beräich 변수");
        Collections.addAll(Zeil,".text",".globl " + Markéierung_VALUE,".type " + Markéierung_VALUE + ", @function",Markéierung_VALUE + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < Format_VALUE.인수.size(); 순번++) Collections.addAll(Zeil,"movl " + (8 + 4 * (Format_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Klass_Daten Klass_VALUE = 클래스들.get(FUNCTION_VALUE.Besëtzer_VALUE); Set<Integer> 경계들 = new HashSet<>(), Branche_Lëscht = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (Befeel_Daten.positionéieren < Befeel_Daten.Daten.length) {
            int positionéieren = Befeel_Daten.positionéieren, Befeel = Befeel_Daten.한바이트(); String positionéieren_INDEX = Markéierung_VALUE + "_b" + positionéieren;
            Zeil.add(positionéieren_INDEX + ":"); 경계들.add(positionéieren);
            if (Befeel == 0) Zeil.add("nop");
            else if (Befeel == 1) Zeil.add("pushl $0");
            else if (Befeel >= 2 && Befeel <= 8) Zeil.add("pushl $" + (Befeel - 3));
            else if (Befeel == 16 || Befeel == 17) Zeil.add("pushl $" + (Befeel == 16 ? Befeel_Daten.부호한바이트() : Befeel_Daten.부호두바이트()));
            else if (Befeel == 18 || Befeel == 19) {
                int INDEX = Befeel == 18 ? Befeel_Daten.한바이트() : Befeel_Daten.두바이트();
                Zeil.add("pushl $" + 엑스상수(Klass_VALUE,INDEX));
            } else if (Befeel == 21 || Befeel == 25 || (Befeel >= 26 && Befeel <= 29) || (Befeel >= 42 && Befeel <= 45) || Befeel == 54 || Befeel == 58 || (Befeel >= 59 && Befeel <= 62) || (Befeel >= 75 && Befeel <= 78)) {
                boolean 읽음 = Befeel < 54; int INDEX = Befeel == 21 || Befeel == 25 || Befeel == 54 || Befeel == 58 ? Befeel_Daten.한바이트() : Befeel - (Befeel <= 29 ? 26 : Befeel <= 45 ? 42 : Befeel <= 62 ? 59 : 75);
                Scheck_lokal(INDEX,lokal_COUNT); Zeil.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Befeel == 46) Collections.addAll(Zeil,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Befeel == 79) Collections.addAll(Zeil,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Befeel == 87 || Befeel == 88) Zeil.add("addl $" + (Befeel == 87 ? 4 : 8) + ", %esp");
            else if (Befeel >= 89 && Befeel <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] Reiefolleg_Lëscht = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Befeel - 89]; 순번++) Zeil.add("popl " + 저장기들[순번]);
                for (int 순번 : Reiefolleg_Lëscht[Befeel - 89]) Zeil.add("pushl " + 저장기들[순번]);
            } else if (Befeel == 96 || Befeel == 100 || Befeel == 104 || Befeel == 126 || Befeel == 128 || Befeel == 130) {
                String Operatioun_VALUE = Befeel == 96 ? "addl" : Befeel == 100 ? "subl" : Befeel == 104 ? "imull" : Befeel == 126 ? "andl" : Befeel == 128 ? "orl" : "xorl";
                Collections.addAll(Zeil,"popl %ecx","popl %eax",Operatioun_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Befeel == 108 || Befeel == 112) Collections.addAll(Zeil,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + positionéieren_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + positionéieren_INDEX + "_divide","xorl %edx, %edx","jmp " + positionéieren_INDEX + "_done",positionéieren_INDEX + "_divide:","cltd","idivl %ecx",positionéieren_INDEX + "_done:","pushl " + (Befeel == 108 ? "%eax" : "%edx"));
            else if (Befeel == 116) Zeil.add("negl (%esp)");
            else if (Befeel == 120 || Befeel == 122 || Befeel == 124) Collections.addAll(Zeil,"popl %ecx","popl %eax",(Befeel == 120 ? "sall" : Befeel == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Befeel == 132) {
                int INDEX = Befeel_Daten.한바이트(), 증가 = Befeel_Daten.부호한바이트(); Scheck_lokal(INDEX,lokal_COUNT); Zeil.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Befeel >= 145 && Befeel <= 147) Collections.addAll(Zeil,"popl %eax",Befeel == 145 ? "movsbl %al, %eax" : Befeel == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Befeel >= 153 && Befeel <= 166) {
                if (Befeel <= 158) Collections.addAll(Zeil,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Zeil,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int Zil_VALUE = positionéieren + Befeel_Daten.부호두바이트(); Branche_Lëscht.add(Zil_VALUE); Zeil.add(비교들[Befeel - (Befeel <= 158 ? 153 : 159)] + " " + Markéierung_VALUE + "_b" + Zil_VALUE);
            } else if (Befeel == 167 || Befeel == 200) {
                int Zil_VALUE = positionéieren + (Befeel == 167 ? Befeel_Daten.부호두바이트() : Befeel_Daten.네바이트()); Branche_Lëscht.add(Zil_VALUE); Zeil.add("jmp " + Markéierung_VALUE + "_b" + Zil_VALUE);
            } else if (Befeel == 170 || Befeel == 171) {
                while (Befeel_Daten.positionéieren % 4 != 0) Befeel_Daten.한바이트();
                int Standardwäert = positionéieren + Befeel_Daten.네바이트(); Branche_Lëscht.add(Standardwäert); Zeil.add("popl %eax");
                int Element_COUNT, 아래 = 0;
                if (Befeel == 170) { 아래 = Befeel_Daten.네바이트(); int 위 = Befeel_Daten.네바이트(); long Längt_VALUE = (long)위 - 아래 + 1; if (Längt_VALUE < 1 || Längt_VALUE > (Befeel_Daten.Daten.length - Befeel_Daten.positionéieren) / 4) throw new Iwwersetzung_Feeler("switch Clip Feeler"); Element_COUNT = (int)Längt_VALUE; }
                else { Element_COUNT = Befeel_Daten.네바이트(); if (Element_COUNT < 0 || Element_COUNT > (Befeel_Daten.Daten.length - Befeel_Daten.positionéieren) / 8) throw new Iwwersetzung_Feeler("switch d_Gréisst_veränneren Feeler"); }
                for (int 순번 = 0; 순번 < Element_COUNT; 순번++) {
                    int VALUE = Befeel == 170 ? 아래 + 순번 : Befeel_Daten.네바이트(), Zil_VALUE = positionéieren + Befeel_Daten.네바이트(); Branche_Lëscht.add(Zil_VALUE);
                    Collections.addAll(Zeil,"cmpl $" + VALUE + ", %eax","je " + Markéierung_VALUE + "_b" + Zil_VALUE);
                }
                Zeil.add("jmp " + Markéierung_VALUE + "_b" + Standardwäert);
            } else if (Befeel == 172 || Befeel == 176 || Befeel == 177) {
                if (Befeel != 177) Zeil.add("popl %eax"); Collections.addAll(Zeil,"leave","ret");
            } else if (Befeel == 178 || Befeel == 179) {
                Method_Referenzen Referenzen = Klass_VALUE.Referenzen(Befeel_Daten.두바이트()); if (!필드들.containsKey(Referenzen)) throw new Iwwersetzung_Feeler("알 수 없는 Feld_VALUE");
                Collections.addAll(Zeil,"call " + Symbol("init",Referenzen.Besëtzer_VALUE),(Befeel == 178 ? "pushl " : "popl ") + Symbol("field",Referenzen.부분들()));
            } else if (Befeel == 184) {
                Method_Referenzen Referenzen = Klass_VALUE.Referenzen(Befeel_Daten.두바이트()); if (!함수들.containsKey(Referenzen)) throw new Iwwersetzung_Feeler("알 수 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Referenzen.서술); Collections.addAll(Zeil,"call " + Symbol("init",Referenzen.Besëtzer_VALUE),"call " + Symbol("method",Referenzen.부분들()));
                if (!호출형식.인수.isEmpty()) Zeil.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) Zeil.add("pushl %eax");
            } else if (Befeel == 182) {
                Method_Referenzen Referenzen = Klass_VALUE.Referenzen(Befeel_Daten.두바이트());
                if (Referenzen.equals(new Method_Referenzen("java/lang/String","length","()I"))) Collections.addAll(Zeil,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Referenzen.equals(new Method_Referenzen("java/lang/String","charAt","(I)C"))) Collections.addAll(Zeil,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Iwwersetzung_Feeler("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Befeel == 188) {
                if (Befeel_Daten.한바이트() != 10) throw new Iwwersetzung_Feeler("new int[]만 Support_VALUE"); Collections.addAll(Zeil,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Befeel == 190) Collections.addAll(Zeil,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Befeel == 196) {
                int Extensioun_VALUE = Befeel_Daten.한바이트(), INDEX = Befeel_Daten.두바이트(); Scheck_lokal(INDEX,lokal_COUNT);
                if (Extensioun_VALUE == 21 || Extensioun_VALUE == 25 || Extensioun_VALUE == 54 || Extensioun_VALUE == 58) Zeil.add((Extensioun_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (Extensioun_VALUE == 132) Zeil.add("addl $" + Befeel_Daten.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Iwwersetzung_Feeler("wide Befeel 미지원");
            } else if (Befeel == 198 || Befeel == 199) {
                int Zil_VALUE = positionéieren + Befeel_Daten.부호두바이트(); Branche_Lëscht.add(Zil_VALUE); Collections.addAll(Zeil,"popl %eax","testl %eax, %eax",(Befeel == 198 ? "je " : "jne ") + Markéierung_VALUE + "_b" + Zil_VALUE);
            } else throw new Iwwersetzung_Feeler("미지원 Befeel: " + Befeel);
        }
        if (!경계들.containsAll(Branche_Lëscht)) throw new Iwwersetzung_Feeler("Befeel 경계가 아닌 곳으로 Branche");
        Zeil.add(".size " + Markéierung_VALUE + ", .-" + Markéierung_VALUE); return String.join("\n",Zeil);
    }
    String 엑스상수(Klass_Daten Daten, int INDEX) {
        if (Daten.상수종류[INDEX] == 3) return Daten.Konstant_Daten[INDEX].toString();
        if (Daten.상수종류[INDEX] == 8) return Zeechefolleg_Symbol(Daten.문자((Integer)Daten.Konstant_Daten[INDEX]));
        throw new Iwwersetzung_Feeler("정수와 Zeechefolleg_VALUE 상수만 Support_VALUE");
    }
    String 엑스조립본(String Agab_Punkt, List<String> 내보냄, String Zil) throws IOException {
        Map<String,String> Computer_Tabell = new HashMap<>();
        for (String Zeil : Files.readAllLines(Ressource_Wee.resolve("엑스기계함수.tsv"))) { String[] ukoppelen_VALUE = Zeil.split("\t"); if (ukoppelen_VALUE[0].equals(Zil)) Computer_Tabell.put(ukoppelen_VALUE[1] + ukoppelen_VALUE[2],ukoppelen_VALUE[3]); }
        int positionéieren_INDEX = Agab_Punkt.lastIndexOf('.'); if (positionéieren_INDEX < 0) throw new Iwwersetzung_Feeler("Agab_Punkt 지정 Feeler");
        String Besëtzer_VALUE = Agab_Punkt.substring(0,positionéieren_INDEX).replace('.','/'), Method_Agab_Numm = Agab_Punkt.substring(positionéieren_INDEX + 1); Method_Referenzen Agab_Punkt_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { Method_Referenzen Referenzen = new Method_Referenzen(Besëtzer_VALUE,Method_Agab_Numm,서술); if (함수들.containsKey(Referenzen)) { if (Agab_Punkt_VALUE != null) throw new Iwwersetzung_Feeler("겹친 Agab_Punkt"); Agab_Punkt_VALUE = Referenzen; } }
        if (Agab_Punkt_VALUE == null || (함수들.get(Agab_Punkt_VALUE).Zougrëff_Agab & 0x100) != 0) throw new Iwwersetzung_Feeler("Agab_Punkt_VALUE FUNCTION_VALUE Format_VALUE Feeler");
        List<String> Zeil = new ArrayList<>(); Zeil.add(".code32");
        for (Klass_Daten Daten : 클래스들.values()) {
            String Status_VALUE = Symbol("state",Daten.Numm), initialiséieren = Symbol("init",Daten.Numm);
            Collections.addAll(Zeil,".bss",".balign 4",Status_VALUE + ": .long 0",".text",initialiséieren + ":","cmpl $0, " + Status_VALUE,"jne " + initialiséieren + "_done","movl $1, " + Status_VALUE);
            Method_Referenzen 초기화참조 = new Method_Referenzen(Daten.Numm,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Zeil.add("call " + Symbol("method",초기화참조.부분들()));
            Collections.addAll(Zeil,"movl $2, " + Status_VALUE,initialiséieren + "_done:","ret");
            for (Member_Daten Feld_VALUE : Daten.Feld_VALUE) {
                byte[] Konstant_VALUE = Feld_VALUE.Attribut_VALUE.get("ConstantValue"); String VALUE = Konstant_VALUE == null ? "0" : 엑스상수(Daten,new Daten_Lieser(Konstant_VALUE).두바이트());
                Collections.addAll(Zeil,".data",".balign 4",Symbol("field",Daten.Numm,Feld_VALUE.Numm,Feld_VALUE.서술) + ": .long " + VALUE);
            }
            for (Member_Daten FUNCTION_VALUE : Daten.FUNCTION_VALUE) if (!FUNCTION_VALUE.Numm.equals("<init>")) Zeil.add(엑스함수본문(new Method_Referenzen(Daten.Numm,FUNCTION_VALUE.Numm,FUNCTION_VALUE.서술),FUNCTION_VALUE,Computer_Tabell,Zil));
        }
        Collections.addAll(Zeil,".text",".globl java_entry","java_entry:","call " + Symbol("init",Agab_Punkt_VALUE.Besëtzer_VALUE),"call " + Symbol("method",Agab_Punkt_VALUE.부분들()));
        if (Agab_Punkt_VALUE.서술.equals("()V")) Zeil.add("xorl %eax, %eax"); Zeil.add("ret");
        for (String 지정 : 내보냄) {
            int Trennzeechen_VALUE_d8ba4873 = 지정.indexOf('='); if (Trennzeechen_VALUE_d8ba4873 < 1) throw new Iwwersetzung_Feeler("내보내기 지정 Feeler");
            String 외부 = 지정.substring(0,Trennzeechen_VALUE_d8ba4873), FUNCTION_VALUE = 지정.substring(Trennzeechen_VALUE_d8ba4873 + 1); int Divisioun_Mooss = FUNCTION_VALUE.lastIndexOf('.');
            if (Divisioun_Mooss < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Iwwersetzung_Feeler("내보내기 Symbol Feeler");
            String Klass_VALUE = FUNCTION_VALUE.substring(0,Divisioun_Mooss).replace('.','/'), Numm = FUNCTION_VALUE.substring(Divisioun_Mooss + 1); Method_Referenzen Auswiel_VALUE = null;
            for (Method_Referenzen Referenzen : 함수들.keySet()) if (Referenzen.Besëtzer_VALUE.equals(Klass_VALUE) && Referenzen.Numm.equals(Numm)) { if (Auswiel_VALUE != null) throw new Iwwersetzung_Feeler("겹친 내보내기 Zil"); Auswiel_VALUE = Referenzen; }
            if (Auswiel_VALUE == null) throw new Iwwersetzung_Feeler("내보낼 함수가 없음");
            Collections.addAll(Zeil,".text",".globl " + 외부,외부 + ":","call " + Symbol("init",Auswiel_VALUE.Besëtzer_VALUE),"jmp " + Symbol("method",Auswiel_VALUE.부분들()));
        }
        Zeil.add(".section .rodata");
        for (Map.Entry<String,String> Agab_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Zeil,".balign 4",Agab_VALUE.getValue() + ":",".long " + Agab_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char Lektioun_VALUE : Agab_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(Lektioun_VALUE)); if (!단위들.isEmpty()) Zeil.add(".long " + String.join(",",단위들));
        }
        Zeil.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Zeil) + "\n";
    }
    static void ausféieren_Tool(List<String> Befeel) throws Exception {
        if (new ProcessBuilder(Befeel).inheritIO().start().waitFor() != 0) throw new Iwwersetzung_Feeler("erstellen_Quell Feeler: " + Befeel.get(0));
    }
    static String Daten_Zeechefolleg(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String Zil, String Agab_Punkt, List<String> 내보냄, Path 출력, Path Ressource_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Klass_Wee = 임시.resolve("classes"); Files.createDirectory(Klass_Wee);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Klass_Wee.toString(),"-sourcepath",Klass_Wee.toString(),"-d",Klass_Wee.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int Quell_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Iwwersetzung_Feeler("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); Quell_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Iwwersetzung_Feeler(".java 또는 .class만 Support_VALUE");
            }
            if (Quell_COUNT > 0) ausféieren_Tool(자바명령);
            try (java.util.stream.Stream<Path> Wee_Lëscht = Files.walk(Klass_Wee)) { Wee_Lëscht.filter(Wee -> Wee.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,Zil.equals("user") ? "user" : "kernel",262144,Ressource_VALUE);
            String 조립 = CONVERT_VALUE.엑스조립본(Agab_Punkt,내보냄,Zil); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path Tool_positionéieren = Ressource_VALUE.getParent();
            ausféieren_Tool(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            ausféieren_Tool(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),Tool_positionéieren.resolve("Common_Language_Runtime_Support.s").toString()));
            List<String> Verbannen = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (Zil.equals("kernel")) Verbannen.add("-r");
            else {
                ausféieren_Tool(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),Tool_positionéieren.resolve(Zil.equals("user") ? "Start_Benotzer_App.s" : "리눅스시작.s").toString()));
                Collections.addAll(Verbannen,"-e","_start",임시.resolve("start.o").toString());
                if (Zil.equals("user")) Collections.addAll(Verbannen,"-T",Tool_positionéieren.resolve("Benotzer_Link_Layout.ld").toString());
            }
            Collections.addAll(Verbannen,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); ausféieren_Tool(Verbannen);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path publizéieren_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publizéieren_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(publizéieren_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publizéieren_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(Zil.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> Symbol_Daten = new ArrayList<>(), Quelldaten = new ArrayList<>();
            for (Method_Referenzen Referenzen : CONVERT_VALUE.함수들.keySet()) Symbol_Daten.add(Daten_Zeechefolleg(Symbol("method",Referenzen.부분들())) + ":" + Daten_Zeechefolleg(Referenzen.Besëtzer_VALUE + "." + Referenzen.Numm + Referenzen.서술));
            for (Path 입력 : 입력들) {
                byte[] Hash_Fichier = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte VALUE : Hash_Fichier) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                Quelldaten.add(Daten_Zeechefolleg(입력.toAbsolutePath().toString()) + ":" + Daten_Zeechefolleg(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + Daten_Zeechefolleg(Zil) + ",\"entry\":" + Daten_Zeechefolleg(Agab_Punkt) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",Symbol_Daten) + "},\"sources\":{" + String.join(",",Quelldaten) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> Wee_Lëscht = Files.walk(임시)) { for (Path Wee : (Iterable<Path>)Wee_Lëscht.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Wee); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String Agab_Punkt = null, Zil = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> Wee_Lëscht = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Klass_VALUE.FUNCTION_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export Symbol=Klass_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": Agab_Punkt = 인수[++순번]; break;
                    case "--profile": Zil = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Iwwersetzung_Feeler("알 수 없는 옵션: " + VALUE); Wee_Lëscht.add(Paths.get(VALUE));
                }
            }
            if (Agab_Punkt == null || 출력경로 == null || Wee_Lëscht.isEmpty()) throw new Iwwersetzung_Feeler("--entry, -o, Klass_VALUE 파일이 필요합니다");
            Path Ressource_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Iwwersetzung_Feeler("알 수 없는 ausféieren_Befeel Zil");
                엑스번역(Wee_Lëscht,엑스대상,Agab_Punkt,내보냄,출력경로,Ressource_VALUE); return;
            }
            String Quell = new 기계어미리번역(Wee_Lëscht, Zil, 낱말수, Ressource_VALUE).generéieren(Agab_Punkt, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, Quell, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Feeler) { System.err.println("erstellen_Quell Feeler: " + Feeler.getMessage()); System.exit(1); }
    }
}
