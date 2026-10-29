// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java les_WAARDE 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Vertaling_fout extends RuntimeException {
        Vertaling_fout(String 설명) { super(설명); }
    }
    static final class gegevens_Lezer {
        final byte[] gegevens;
        int positie;
        gegevens_Lezer(byte[] invoer_gegevens) { gegevens = invoer_gegevens; }
        byte[] Lezen(int tijdsduur_WAARDE) {
            if (tijdsduur_WAARDE < 0 || tijdsduur_WAARDE > gegevens.length - positie) throw new Vertaling_fout("잘린 les_WAARDE 또는 opdracht gegevens");
            byte[] resultaat = Arrays.copyOfRange(gegevens, positie, positie + tijdsduur_WAARDE); positie += tijdsduur_WAARDE; return resultaat;
        }
        int 한바이트() { if (positie >= gegevens.length) throw new Vertaling_fout("잘린 opdracht gegevens"); return gegevens[positie++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class lid_gegevens {
        final int toegang_invoer;
        final String Naam, 서술;
        final Map<String, byte[]> kenmerkwaarde;
        lid_gegevens(int toegang_WAARDE, String naam_WAARDE, String 서술값, Map<String, byte[]> kenmerk_gegevens) {
            toegang_invoer = toegang_WAARDE; Naam = naam_WAARDE; 서술 = 서술값; kenmerkwaarde = kenmerk_gegevens;
        }
    }
    static final class methode_verwijzen implements Comparable<methode_verwijzen> {
        final String eigenaar_WAARDE, Naam, 서술;
        methode_verwijzen(String 소유값, String naam_WAARDE, String 서술값) { eigenaar_WAARDE = 소유값; Naam = naam_WAARDE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{eigenaar_WAARDE, Naam, 서술}; }
        public int compareTo(methode_verwijzen peer_WAARDE) {
            int Vergelijking_WAARDE = eigenaar_WAARDE.compareTo(peer_WAARDE.eigenaar_WAARDE);
            if (Vergelijking_WAARDE == 0) Vergelijking_WAARDE = Naam.compareTo(peer_WAARDE.Naam);
            return Vergelijking_WAARDE == 0 ? 서술.compareTo(peer_WAARDE.서술) : Vergelijking_WAARDE;
        }
        public boolean equals(Object peer_WAARDE) { return peer_WAARDE instanceof methode_verwijzen && compareTo((methode_verwijzen) peer_WAARDE) == 0; }
        public int hashCode() { return Objects.hash(eigenaar_WAARDE, Naam, 서술); }
    }
    static final class les_gegevens {
        final int[] constante_soort;
        final Object[] constante_gegevens;
        final String Naam;
        final List<lid_gegevens> veldwaarde, FUNCTIE_WAARDE;
        les_gegevens(Path pad) throws IOException {
            gegevens_Lezer Lezer_WAARDE = new gegevens_Lezer(Files.readAllBytes(pad));
            if (Lezer_WAARDE.네바이트() != 0xcafebabe) throw new Vertaling_fout("Java les_WAARDE 표식이 아님");
            Lezer_WAARDE.Lezen(4);
            int item_AANTAL = Lezer_WAARDE.두바이트(); constante_soort = new int[item_AANTAL]; constante_gegevens = new Object[item_AANTAL];
            for (int 순번 = 1; 순번 < item_AANTAL; 순번++) {
                int soort_WAARDE = Lezer_WAARDE.한바이트(); constante_soort[순번] = soort_WAARDE;
                switch (soort_WAARDE) {
                    case 1:
                        int tijdsduur_WAARDE = Lezer_WAARDE.두바이트();
                        byte[] teken_buffer = Lezer_WAARDE.Lezen(tijdsduur_WAARDE), 길이붙인자료 = new byte[tijdsduur_WAARDE + 2];
                        길이붙인자료[0] = (byte)(tijdsduur_WAARDE >> 8); 길이붙인자료[1] = (byte)tijdsduur_WAARDE;
                        System.arraycopy(teken_buffer, 0, 길이붙인자료, 2, tijdsduur_WAARDE);
                        constante_gegevens[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: constante_gegevens[순번] = Lezer_WAARDE.네바이트(); break;
                    case 4: Lezer_WAARDE.Lezen(4); break;
                    case 5: case 6: Lezer_WAARDE.Lezen(8); 순번++; break;
                    case 7: case 8: case 16: constante_gegevens[순번] = Lezer_WAARDE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        constante_gegevens[순번] = new int[]{Lezer_WAARDE.두바이트(), Lezer_WAARDE.두바이트()}; break;
                    case 15: constante_gegevens[순번] = new int[]{Lezer_WAARDE.한바이트(), Lezer_WAARDE.두바이트()}; break;
                    default: throw new Vertaling_fout("지원하지 않는 constante_WAARDE soort_WAARDE: " + soort_WAARDE);
                }
            }
            Lezer_WAARDE.두바이트(); Naam = klassenaam(Lezer_WAARDE.두바이트());
            if (!klassenaam(Lezer_WAARDE.두바이트()).equals("java/lang/Object") || Lezer_WAARDE.두바이트() != 0)
                throw new Vertaling_fout(Naam + ": 상속 및 인터페이스 미지원");
            veldwaarde = 멤버읽기(Lezer_WAARDE); FUNCTIE_WAARDE = 멤버읽기(Lezer_WAARDE); 속성읽기(Lezer_WAARDE);
            if (Lezer_WAARDE.positie != Lezer_WAARDE.gegevens.length) throw new Vertaling_fout("les_WAARDE 뒤에 남은 gegevens");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= constante_soort.length || constante_soort[INDEX] != 1) throw new Vertaling_fout("문자 constante_WAARDE INDEX fout");
            return (String) constante_gegevens[INDEX];
        }
        String klassenaam(int INDEX) {
            if (INDEX < 1 || INDEX >= constante_soort.length || constante_soort[INDEX] != 7) throw new Vertaling_fout("les_WAARDE verwijzen fout");
            return 문자((Integer)constante_gegevens[INDEX]);
        }
        methode_verwijzen verwijzen(int INDEX) {
            if (INDEX < 1 || INDEX >= constante_soort.length || constante_soort[INDEX] < 9 || constante_soort[INDEX] > 11) throw new Vertaling_fout("멤버 verwijzen fout");
            int[] koppelen_WAARDE = (int[])constante_gegevens[INDEX], naam_koppelen = (int[])constante_gegevens[koppelen_WAARDE[1]];
            return new methode_verwijzen(klassenaam(koppelen_WAARDE[0]), 문자(naam_koppelen[0]), 문자(naam_koppelen[1]));
        }
        Map<String, byte[]> 속성읽기(gegevens_Lezer Lezer_WAARDE) {
            Map<String, byte[]> resultaat = new LinkedHashMap<>();
            int item_AANTAL = Lezer_WAARDE.두바이트();
            for (int 순번 = 0; 순번 < item_AANTAL; 순번++) {
                String kenmerk_naam = 문자(Lezer_WAARDE.두바이트()); byte[] WAARDE = Lezer_WAARDE.Lezen(Lezer_WAARDE.네바이트());
                if (resultaat.put(kenmerk_naam, WAARDE) != null) throw new Vertaling_fout("겹친 kenmerkwaarde: " + kenmerk_naam);
            }
            return resultaat;
        }
        List<lid_gegevens> 멤버읽기(gegevens_Lezer Lezer_WAARDE) {
            List<lid_gegevens> resultaat = new ArrayList<>(); int item_AANTAL = Lezer_WAARDE.두바이트();
            for (int 순번 = 0; 순번 < item_AANTAL; 순번++) {
                int toegang_invoer = Lezer_WAARDE.두바이트(); String methode_invoer_naam = 문자(Lezer_WAARDE.두바이트()), 서술 = 문자(Lezer_WAARDE.두바이트());
                resultaat.add(new lid_gegevens(toegang_invoer, methode_invoer_naam, 서술, 속성읽기(Lezer_WAARDE)));
            }
            return resultaat;
        }
    }
    static final class 함수형식 {
        final List<String> argumenten = new ArrayList<>();
        final String Retour_HR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Vertaling_fout("FUNCTIE_WAARDE 서술 fout: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Vertaling_fout("FUNCTIE_WAARDE 서술 fout: " + 서술);
            argumenten.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (argumenten.contains("V") || 반환들.size() != 1) throw new Vertaling_fout("FUNCTIE_WAARDE 서술 fout: " + 서술);
            Retour_HR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> resultaat = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int positie = 0; positie < 서술.length();) {
            String selectie_WAARDE = null;
            for (String opmaak_WAARDE : 허용형식) if (서술.startsWith(opmaak_WAARDE, positie)) { selectie_WAARDE = opmaak_WAARDE; break; }
            if (selectie_WAARDE == null) throw new Vertaling_fout("지원하지 않는 gegevenstype: " + 서술);
            resultaat.add(selectie_WAARDE); positie += selectie_WAARDE.length();
        }
        return resultaat;
    }
    static String symbool(String soort_WAARDE, String... 부분들) {
        try {
            byte[] hash_Bestand = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder tekst = new StringBuilder("j_" + soort_WAARDE + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) tekst.append(String.format(Locale.ROOT, "%02x", hash_Bestand[순번] & 255));
            return tekst.toString();
        } catch (Exception fout) { throw new Vertaling_fout(fout.toString()); }
    }
    final Map<String, les_gegevens> 클래스들 = new TreeMap<>();
    final Map<methode_verwijzen, lid_gegevens> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), machine_Functions_c3a8e64a = new LinkedHashMap<>();
    final String uitvoerbewerking_doel, machine_les;
    final int heap_Aantal_woorden;
    final Path bron_pad;
    기계어미리번역(List<Path> pad_Lijst, String doel, int 낱말수, Path bron_WAARDE) throws IOException {
        if ((!doel.equals("kernel") && !doel.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Vertaling_fout("Uitvoeren_opdracht doel 또는 Geheugen_WAARDE ADRES_regio Grootte fout");
        uitvoerbewerking_doel = doel; heap_Aantal_woorden = 낱말수; bron_pad = bron_WAARDE;
        // 이 이름도 국가별 bron_structuur genereren 시 해당 언어로 옮긴다.
        machine_les = doel.equals("kernel") ? "Bord" : "gebruikersruimte";
        for (String invoerregel : Files.readAllLines(bron_WAARDE.resolve("machine_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = invoerregel.split("\t", -1);
            if (부분들.length != 4) throw new Vertaling_fout("machine FUNCTIE_WAARDE gegevens fout");
            if (부분들[0].equals(doel)) machine_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path pad : pad_Lijst) {
            les_gegevens gegevens = new les_gegevens(pad);
            if (클래스들.put(gegevens.Naam, gegevens) != null) throw new Vertaling_fout("중복 les_WAARDE: " + gegevens.Naam);
            for (lid_gegevens veldwaarde : gegevens.veldwaarde) {
                if ((veldwaarde.toegang_invoer & 8) == 0 || 형식읽기(veldwaarde.서술).equals(Collections.singletonList("V"))) throw new Vertaling_fout("statisch_WAARDE 필드만 steun_WAARDE");
                if (필드들.put(new methode_verwijzen(gegevens.Naam, veldwaarde.Naam, veldwaarde.서술), veldwaarde) != null) throw new Vertaling_fout("중복 veldwaarde");
            }
            for (lid_gegevens FUNCTIE_WAARDE : gegevens.FUNCTIE_WAARDE) {
                if (FUNCTIE_WAARDE.Naam.equals("<init>")) continue;
                if ((FUNCTIE_WAARDE.toegang_invoer & 8) == 0 || (FUNCTIE_WAARDE.toegang_invoer & (0x20 | 0x400)) != 0) throw new Vertaling_fout("statisch_WAARDE 비동기화 함수만 steun_WAARDE");
                new 함수형식(FUNCTIE_WAARDE.서술);
                if (함수들.put(new methode_verwijzen(gegevens.Naam, FUNCTIE_WAARDE.Naam, FUNCTIE_WAARDE.서술), FUNCTIE_WAARDE) != null) throw new Vertaling_fout("중복 FUNCTIE_WAARDE");
            }
        }
    }
    String tekenreeks_symbool(String tekst) { return 문자열들.computeIfAbsent(tekst, WAARDE -> "j_text_" + 문자열들.size()); }
    String constante_expressie(les_gegevens gegevens, int INDEX) {
        if (INDEX < 1 || INDEX >= gegevens.constante_soort.length) throw new Vertaling_fout("constante_WAARDE INDEX clip fout");
        if (gegevens.constante_soort[INDEX] == 3) return "(word)(uint32_t)(" + gegevens.constante_gegevens[INDEX] + ")";
        if (gegevens.constante_soort[INDEX] == 8) return "(word)" + tekenreeks_symbool(gegevens.문자((Integer)gegevens.constante_gegevens[INDEX]));
        throw new Vertaling_fout("정수와 tekenreeks_WAARDE 상수만 steun_WAARDE");
    }
    String 함수원형(methode_verwijzen verwijzen) {
        List<String> 인수들 = new ArrayList<>(); int item_AANTAL = new 함수형식(verwijzen.서술).argumenten.size();
        for (int 순번 = 0; 순번 < item_AANTAL; 순번++) 인수들.add("word a" + 순번);
        return "static word " + symbool("method", verwijzen.부분들()) + "(" + (item_AANTAL == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void cheque_lokaal(int INDEX, int lokaal_variabele_AANTAL) { if (INDEX < 0 || INDEX >= lokaal_variabele_AANTAL) throw new Vertaling_fout("lokaal_scope variabele_WAARDE INDEX clip fout"); }
    void 분기넣기(List<String> tekstuitvoer, Set<Integer> branch_Lijst, int positie, int 이동량, String toestand) {
        int doel_WAARDE = positie + 이동량; branch_Lijst.add(doel_WAARDE);
        tekstuitvoer.add((toestand == null ? "" : "if (" + toestand + ") ") + "goto b" + doel_WAARDE + ";");
    }
    String methode_hoofdtekst(methode_verwijzen FUNCTIE_WAARDE, lid_gegevens gegevens) {
        byte[] hoofdtekst_gegevens = gegevens.kenmerkwaarde.get("Code"); if (hoofdtekst_gegevens == null) throw new Vertaling_fout("FUNCTIE_WAARDE 몸체가 없음: " + FUNCTIE_WAARDE.Naam);
        gegevens_Lezer Lezer_WAARDE = new gegevens_Lezer(hoofdtekst_gegevens); int 쌓임깊이 = Lezer_WAARDE.두바이트(), lokaal_variabele_AANTAL = Lezer_WAARDE.두바이트();
        gegevens_Lezer opdracht_gegevens = new gegevens_Lezer(Lezer_WAARDE.Lezen(Lezer_WAARDE.네바이트()));
        if (Lezer_WAARDE.두바이트() != 0) throw new Vertaling_fout("try/catch/finally 미지원");
        함수형식 opmaak_WAARDE = new 함수형식(FUNCTIE_WAARDE.서술); if (lokaal_variabele_AANTAL < opmaak_WAARDE.argumenten.size()) throw new Vertaling_fout("매개변수보다 적은 lokaal_scope variabele_WAARDE");
        les_gegevens les_WAARDE = 클래스들.get(FUNCTIE_WAARDE.eigenaar_WAARDE);
        List<String> tekstuitvoer = new ArrayList<>(); tekstuitvoer.add(함수원형(FUNCTIE_WAARDE) + " {");
        tekstuitvoer.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(lokaal_variabele_AANTAL, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < opmaak_WAARDE.argumenten.size(); 순번++) tekstuitvoer.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), branch_Lijst = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (opdracht_gegevens.positie < opdracht_gegevens.gegevens.length) {
            int positie = opdracht_gegevens.positie, opdracht = opdracht_gegevens.한바이트(); 경계들.add(positie); tekstuitvoer.add("b" + positie + ":;");
            if (opdracht == 0) continue;
            if (opdracht == 1) tekstuitvoer.add("PUSH(0);");
            else if (opdracht >= 2 && opdracht <= 8) tekstuitvoer.add("PUSH((uint32_t)(" + (opdracht - 3) + "));");
            else if (opdracht == 16 || opdracht == 17) tekstuitvoer.add("PUSH((uint32_t)(" + (opdracht == 16 ? opdracht_gegevens.부호한바이트() : opdracht_gegevens.부호두바이트()) + "));");
            else if (opdracht == 18 || opdracht == 19) tekstuitvoer.add("PUSH(" + constante_expressie(les_WAARDE, opdracht == 18 ? opdracht_gegevens.한바이트() : opdracht_gegevens.두바이트()) + ");");
            else if (opdracht == 21 || opdracht == 25 || (opdracht >= 26 && opdracht <= 29) || (opdracht >= 42 && opdracht <= 45)) {
                int INDEX = opdracht == 21 || opdracht == 25 ? opdracht_gegevens.한바이트() : opdracht - (opdracht <= 29 ? 26 : 42);
                cheque_lokaal(INDEX, lokaal_variabele_AANTAL); tekstuitvoer.add("PUSH(l[" + INDEX + "]);");
            } else if (opdracht == 54 || opdracht == 58 || (opdracht >= 59 && opdracht <= 62) || (opdracht >= 75 && opdracht <= 78)) {
                int INDEX = opdracht == 54 || opdracht == 58 ? opdracht_gegevens.한바이트() : opdracht - (opdracht <= 62 ? 59 : 75);
                cheque_lokaal(INDEX, lokaal_variabele_AANTAL); tekstuitvoer.add("l[" + INDEX + "] = POP();");
            } else if (opdracht == 46) tekstuitvoer.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (opdracht == 79) tekstuitvoer.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (opdracht == 87 || opdracht == 88) tekstuitvoer.add(opdracht == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (opdracht >= 89 && opdracht <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] order_Lijst = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[opdracht - 89]; 순번++) tekstuitvoer.add("abcd".charAt(순번) + " = POP();");
                for (char WAARDE : order_Lijst[opdracht - 89].toCharArray()) tekstuitvoer.add("PUSH(" + WAARDE + ");");
            } else if (opdracht == 96 || opdracht == 100 || opdracht == 104 || opdracht == 126 || opdracht == 128 || opdracht == 130) {
                String operatie_WAARDE = opdracht == 96 ? "+" : opdracht == 100 ? "-" : opdracht == 104 ? "*" : opdracht == 126 ? "&" : opdracht == 128 ? "|" : "^";
                tekstuitvoer.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operatie_WAARDE + " (uint32_t)b);");
            } else if (opdracht == 108 || opdracht == 112) tekstuitvoer.add("b = POP(); a = POP(); PUSH(divide(a,b," + (opdracht == 112 ? 1 : 0) + "));");
            else if (opdracht == 116) tekstuitvoer.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (opdracht == 120 || opdracht == 122 || opdracht == 124) {
                tekstuitvoer.add("b = POP(); a = POP();"); tekstuitvoer.add("PUSH(" + (opdracht == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (opdracht == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (opdracht == 132) {
                int INDEX = opdracht_gegevens.한바이트(), toename_aantal = opdracht_gegevens.부호한바이트(); cheque_lokaal(INDEX, lokaal_variabele_AANTAL);
                tekstuitvoer.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + toename_aantal + ");");
            } else if (opdracht >= 145 && opdracht <= 147) tekstuitvoer.add("a = POP(); PUSH((uint32_t)(" + (opdracht == 145 ? "int8_t" : opdracht == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (opdracht >= 153 && opdracht <= 158) {
                tekstuitvoer.add("a = POP();"); 분기넣기(tekstuitvoer, branch_Lijst, positie, opdracht_gegevens.부호두바이트(), "(int32_t)a " + 비교들[opdracht - 153] + " 0");
            } else if (opdracht >= 159 && opdracht <= 166) {
                tekstuitvoer.add("b = POP(); a = POP();"); 분기넣기(tekstuitvoer, branch_Lijst, positie, opdracht_gegevens.부호두바이트(), opdracht >= 165 ? "a " + 비교들[opdracht - 159] + " b" : "(int32_t)a " + 비교들[opdracht - 159] + " (int32_t)b");
            } else if (opdracht == 167 || opdracht == 200) 분기넣기(tekstuitvoer, branch_Lijst, positie, opdracht == 167 ? opdracht_gegevens.부호두바이트() : opdracht_gegevens.네바이트(), null);
            else if (opdracht == 170 || opdracht == 171) {
                while (opdracht_gegevens.positie % 4 != 0) opdracht_gegevens.한바이트();
                int standaardwaarde = opdracht_gegevens.네바이트(); tekstuitvoer.add("a = POP();");
                if (opdracht == 170) {
                    int 아래 = opdracht_gegevens.네바이트(), 위 = opdracht_gegevens.네바이트(); long item_AANTAL = (long)위 - 아래 + 1;
                    if (item_AANTAL < 1 || item_AANTAL > (opdracht_gegevens.gegevens.length - opdracht_gegevens.positie) / 4) throw new Vertaling_fout("switch clip fout");
                    for (long WAARDE = 아래; WAARDE <= 위; WAARDE++) 분기넣기(tekstuitvoer, branch_Lijst, positie, opdracht_gegevens.네바이트(), "(int32_t)a == (" + WAARDE + ")");
                } else {
                    int item_AANTAL = opdracht_gegevens.네바이트(), voorkant_gegevens = 0;
                    if (item_AANTAL < 0 || item_AANTAL > (opdracht_gegevens.gegevens.length - opdracht_gegevens.positie) / 8) throw new Vertaling_fout("switch Grootte fout");
                    for (int 순번 = 0; 순번 < item_AANTAL; 순번++) {
                        int WAARDE = opdracht_gegevens.네바이트(); if (순번 > 0 && WAARDE <= voorkant_gegevens) throw new Vertaling_fout("switch order_WAARDE fout"); voorkant_gegevens = WAARDE;
                        분기넣기(tekstuitvoer, branch_Lijst, positie, opdracht_gegevens.네바이트(), "(int32_t)a == (" + WAARDE + ")");
                    }
                }
                분기넣기(tekstuitvoer, branch_Lijst, positie, standaardwaarde, null);
            } else if (opdracht == 172 || opdracht == 176 || opdracht == 177) tekstuitvoer.add("return " + (opdracht == 177 ? "0" : "POP()") + ";");
            else if (opdracht == 178 || opdracht == 179) {
                methode_verwijzen verwijzen = les_WAARDE.verwijzen(opdracht_gegevens.두바이트()); if (!필드들.containsKey(verwijzen)) throw new Vertaling_fout("알 nummer 없는 veldwaarde");
                tekstuitvoer.add(symbool("init", verwijzen.eigenaar_WAARDE) + "();"); String veldwaarde = symbool("field", verwijzen.부분들());
                tekstuitvoer.add(opdracht == 178 ? "PUSH(" + veldwaarde + ");" : veldwaarde + " = POP();");
            } else if (opdracht == 184) {
                methode_verwijzen verwijzen = les_WAARDE.verwijzen(opdracht_gegevens.두바이트()); if (!함수들.containsKey(verwijzen)) throw new Vertaling_fout("알 nummer 없는 FUNCTIE_WAARDE");
                함수형식 호출형식 = new 함수형식(verwijzen.서술); int item_AANTAL = 호출형식.argumenten.size();
                tekstuitvoer.add(symbool("init", verwijzen.eigenaar_WAARDE) + "();"); tekstuitvoer.add("if(sp < " + item_AANTAL + ") kernel_panic(\"call stack underflow\"); sp -= " + item_AANTAL + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < item_AANTAL; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                tekstuitvoer.add("a = " + symbool("method", verwijzen.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.Retour_HR.equals("V")) tekstuitvoer.add("PUSH(a);");
            } else if (opdracht == 182) {
                methode_verwijzen verwijzen = les_WAARDE.verwijzen(opdracht_gegevens.두바이트());
                if (verwijzen.equals(new methode_verwijzen("java/lang/String", "length", "()I"))) tekstuitvoer.add("a = POP(); PUSH(length(a));");
                else if (verwijzen.equals(new methode_verwijzen("java/lang/String", "charAt", "(I)C"))) tekstuitvoer.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Vertaling_fout("가상 FUNCTIE_WAARDE 호출 미지원");
            } else if (opdracht == 188) {
                if (opdracht_gegevens.한바이트() != 10) throw new Vertaling_fout("new int[]만 steun_WAARDE"); tekstuitvoer.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (opdracht == 190) tekstuitvoer.add("a = POP(); PUSH(length(a));");
            else if (opdracht == 196) {
                int extensie_WAARDE = opdracht_gegevens.한바이트(), INDEX = opdracht_gegevens.두바이트(); cheque_lokaal(INDEX, lokaal_variabele_AANTAL);
                if (extensie_WAARDE == 21 || extensie_WAARDE == 25) tekstuitvoer.add("PUSH(l[" + INDEX + "]);");
                else if (extensie_WAARDE == 54 || extensie_WAARDE == 58) tekstuitvoer.add("l[" + INDEX + "] = POP();");
                else if (extensie_WAARDE == 132) tekstuitvoer.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + opdracht_gegevens.부호두바이트() + ");");
                else throw new Vertaling_fout("미지원 wide opdracht");
            } else if (opdracht == 198 || opdracht == 199) {
                tekstuitvoer.add("a = POP();"); 분기넣기(tekstuitvoer, branch_Lijst, positie, opdracht_gegevens.부호두바이트(), "a " + (opdracht == 198 ? "==" : "!=") + " 0");
            } else throw new Vertaling_fout(FUNCTIE_WAARDE.eigenaar_WAARDE + "." + FUNCTIE_WAARDE.Naam + ", byte_WAARDE " + positie + ": 미지원 opdracht " + opdracht);
        }
        if (!경계들.containsAll(branch_Lijst)) throw new Vertaling_fout("opdracht 경계가 아닌 곳으로 branch");
        tekstuitvoer.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", tekstuitvoer);
    }
    String exporteren_methode(String link_symbool, String doel, boolean 진입점여부) {
        int plaatsingsindex = doel.lastIndexOf('.'); if (plaatsingsindex < 0 || !link_symbool.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Vertaling_fout("내보내기 Toewijzen_WAARDE fout");
        String eigenaar_WAARDE = doel.substring(0, plaatsingsindex).replace('.', '/'), Naam = doel.substring(plaatsingsindex + 1); methode_verwijzen selectie_WAARDE = null;
        for (methode_verwijzen verwijzen : 함수들.keySet()) if (verwijzen.eigenaar_WAARDE.equals(eigenaar_WAARDE) && verwijzen.Naam.equals(Naam)) {
            if (selectie_WAARDE != null) throw new Vertaling_fout("겹친 내보내기 doel"); selectie_WAARDE = verwijzen;
        }
        if (selectie_WAARDE == null || (함수들.get(selectie_WAARDE).toegang_invoer & 0x100) != 0) throw new Vertaling_fout("내보낼 함수가 없음 또는 native FUNCTIE_WAARDE");
        함수형식 opmaak_WAARDE = new 함수형식(selectie_WAARDE.서술);
        if ((진입점여부 && !opmaak_WAARDE.argumenten.isEmpty()) || !Arrays.asList("V", "I").contains(opmaak_WAARDE.Retour_HR)) throw new Vertaling_fout("beginpunt_WAARDE 또는 C grens_WAARDE opmaak_WAARDE fout");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < opmaak_WAARDE.argumenten.size(); 순번++) {
            if (!opmaak_WAARDE.argumenten.get(순번).equals("I")) throw new Vertaling_fout("C 경계는 int 인수만 steun_WAARDE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (opmaak_WAARDE.Retour_HR.equals("V") ? "void " : "int32_t ") + link_symbool + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + symbool("init", selectie_WAARDE.eigenaar_WAARDE) + "(); " + (opmaak_WAARDE.Retour_HR.equals("V") ? "" : "return (int32_t)") + symbool("method", selectie_WAARDE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String genereren(String beginpunt, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<methode_verwijzen, lid_gegevens> invoer_WAARDE_962f286b : 함수들.entrySet()) {
            methode_verwijzen verwijzen = invoer_WAARDE_962f286b.getKey(); lid_gegevens gegevens = invoer_WAARDE_962f286b.getValue(); 선언들.add(함수원형(verwijzen) + ";");
            if ((gegevens.toegang_invoer & 0x100) != 0) {
                String Verbinden = machine_Functions_c3a8e64a.get(verwijzen.Naam + verwijzen.서술);
                if (!verwijzen.eigenaar_WAARDE.equals(machine_les) || Verbinden == null) throw new Vertaling_fout("허용되지 않은 native FUNCTIE_WAARDE: " + verwijzen.Naam);
                int item_AANTAL = new 함수형식(verwijzen.서술).argumenten.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < item_AANTAL; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Verbinden + "(" + (item_AANTAL == 0 ? "void" : String.join(",", Collections.nCopies(item_AANTAL, "word"))) + ");");
                몸체들.add(함수원형(verwijzen) + " { return " + Verbinden + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(methode_hoofdtekst(verwijzen, gegevens));
        }
        for (Map.Entry<methode_verwijzen, lid_gegevens> invoer_WAARDE_962f286b : 필드들.entrySet()) {
            methode_verwijzen verwijzen = invoer_WAARDE_962f286b.getKey(); byte[] constante_WAARDE = invoer_WAARDE_962f286b.getValue().kenmerkwaarde.get("ConstantValue");
            String WAARDE = constante_WAARDE == null ? "0" : constante_expressie(클래스들.get(verwijzen.eigenaar_WAARDE), new gegevens_Lezer(constante_WAARDE).두바이트());
            필드선언들.add("static word " + symbool("field", verwijzen.부분들()) + " = " + WAARDE + ";");
        }
        for (String Naam : 클래스들.keySet()) {
            String initialiseren = symbool("init", Naam), Status_WAARDE = symbool("state", Naam);
            선언들.add("static void " + initialiseren + "(void);"); 필드선언들.add("static unsigned " + Status_WAARDE + ";");
            methode_verwijzen verwijzen = new methode_verwijzen(Naam, "<clinit>", "()V");
            몸체들.add("static void " + initialiseren + "(void) { if(" + Status_WAARDE + ") return; " + Status_WAARDE + " = 1; " + (함수들.containsKey(verwijzen) ? symbool("method", verwijzen.부분들()) + "(); " : "") + Status_WAARDE + " = 2; }");
        }
        몸체들.add(exporteren_methode("java_entry", beginpunt, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Toewijzen_WAARDE : 내보내기목록) {
            int plaatsingsindex = Toewijzen_WAARDE.indexOf('='); if (plaatsingsindex < 1) throw new Vertaling_fout("내보내기 Toewijzen_WAARDE fout");
            String Naam = Toewijzen_WAARDE.substring(0, plaatsingsindex); 공개이름.add(Naam); 몸체들.add(exporteren_methode(Naam, Toewijzen_WAARDE.substring(plaatsingsindex + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> invoer_WAARDE_962f286b : 문자열들.entrySet()) {
            String tekst = invoer_WAARDE_962f286b.getKey(); StringBuilder MATRIX_WAARDE = new StringBuilder("static const word " + invoer_WAARDE_962f286b.getValue() + "[] = {" + tekst.length());
            for (int 순번 = 0; 순번 < tekst.length(); 순번++) MATRIX_WAARDE.append(", ").append((int)tekst.charAt(순번));
            문자열선언들.add(MATRIX_WAARDE.append("};").toString());
        }
        String steun_WAARDE = Files.readString(bron_pad.resolve("CLR_steun.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(heap_Aantal_woorden));
        return 기계원문한국어화(steun_WAARDE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String broncode, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> naam_tabel = new HashMap<>();
        for (String invoerregel : Files.readAllLines(bron_pad.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] koppelen_WAARDE = invoerregel.split("\t"); naam_tabel.put(koppelen_WAARDE[0], koppelen_WAARDE[1]);
        }
        Pattern chunk_expressie = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = chunk_expressie.matcher(broncode); StringBuffer resultaat = new StringBuffer();
        while (찾개.find()) {
            String Naam = 찾개.group(), 새이름 = Naam;
            if (!Naam.startsWith("//") && !Naam.startsWith("/*") && !Naam.startsWith("\"") && !Naam.startsWith("'") && !공개이름.contains(Naam)) {
                새이름 = naam_tabel.getOrDefault(Naam, Naam);
                if (Naam.matches("a[0-9]+")) 새이름 = "argumenten" + Naam.substring(1);
                if (Naam.matches("b[0-9]+")) 새이름 = "branch" + Naam.substring(1);
                if (범용표기) {
                    StringBuilder notatie_WAARDE = new StringBuilder();
                    for (char teken_WAARDE : 새이름.toCharArray()) notatie_WAARDE.append(teken_WAARDE < 128 ? Character.toString(teken_WAARDE) : String.format(Locale.ROOT, "\\u%04x", (int)teken_WAARDE));
                    새이름 = notatie_WAARDE.toString();
                }
            }
            찾개.appendReplacement(resultaat, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(resultaat); return resultaat.toString();
    }
    String X_86_methode_hoofdtekst(methode_verwijzen FUNCTIE_WAARDE, lid_gegevens gegevens, Map<String,String> machine_tabel, String doel) {
        String markering_WAARDE = symbool("method", FUNCTIE_WAARDE.부분들());
        List<String> invoerregel = new ArrayList<>();
        if ((gegevens.toegang_invoer & 0x100) != 0) {
            String Verbinden = machine_tabel.get(FUNCTIE_WAARDE.Naam + FUNCTIE_WAARDE.서술);
            if (!FUNCTIE_WAARDE.eigenaar_WAARDE.equals(doel.equals("kernel") ? "mobiel_WAARDE" : "gebruikersruimte") || Verbinden == null) throw new Vertaling_fout("허용되지 않은 native FUNCTIE_WAARDE");
            return ".text\n" + markering_WAARDE + ":\njmp " + Verbinden;
        }
        byte[] hoofdtekst = gegevens.kenmerkwaarde.get("Code"); if (hoofdtekst == null) throw new Vertaling_fout("FUNCTIE_WAARDE 몸체가 없음");
        gegevens_Lezer Lezer_WAARDE = new gegevens_Lezer(hoofdtekst); Lezer_WAARDE.두바이트(); int lokaal_AANTAL = Lezer_WAARDE.두바이트();
        gegevens_Lezer opdracht_gegevens = new gegevens_Lezer(Lezer_WAARDE.Lezen(Lezer_WAARDE.네바이트()));
        if (Lezer_WAARDE.두바이트() != 0) throw new Vertaling_fout("try/catch/finally 미지원");
        함수형식 opmaak_WAARDE = new 함수형식(FUNCTIE_WAARDE.서술); if (lokaal_AANTAL < opmaak_WAARDE.argumenten.size()) throw new Vertaling_fout("매개변수보다 적은 lokaal_scope variabele_WAARDE");
        Collections.addAll(invoerregel,".text",".globl " + markering_WAARDE,".type " + markering_WAARDE + ", @function",markering_WAARDE + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokaal_AANTAL * 4 + ", %esp");
        for (int 순번 = 0; 순번 < opmaak_WAARDE.argumenten.size(); 순번++) Collections.addAll(invoerregel,"movl " + (8 + 4 * (opmaak_WAARDE.argumenten.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        les_gegevens les_WAARDE = 클래스들.get(FUNCTIE_WAARDE.eigenaar_WAARDE); Set<Integer> 경계들 = new HashSet<>(), branch_Lijst = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (opdracht_gegevens.positie < opdracht_gegevens.gegevens.length) {
            int positie = opdracht_gegevens.positie, opdracht = opdracht_gegevens.한바이트(); String plaatsingsindex = markering_WAARDE + "_b" + positie;
            invoerregel.add(plaatsingsindex + ":"); 경계들.add(positie);
            if (opdracht == 0) invoerregel.add("nop");
            else if (opdracht == 1) invoerregel.add("pushl $0");
            else if (opdracht >= 2 && opdracht <= 8) invoerregel.add("pushl $" + (opdracht - 3));
            else if (opdracht == 16 || opdracht == 17) invoerregel.add("pushl $" + (opdracht == 16 ? opdracht_gegevens.부호한바이트() : opdracht_gegevens.부호두바이트()));
            else if (opdracht == 18 || opdracht == 19) {
                int INDEX = opdracht == 18 ? opdracht_gegevens.한바이트() : opdracht_gegevens.두바이트();
                invoerregel.add("pushl $" + X_86_constante(les_WAARDE,INDEX));
            } else if (opdracht == 21 || opdracht == 25 || (opdracht >= 26 && opdracht <= 29) || (opdracht >= 42 && opdracht <= 45) || opdracht == 54 || opdracht == 58 || (opdracht >= 59 && opdracht <= 62) || (opdracht >= 75 && opdracht <= 78)) {
                boolean 읽음 = opdracht < 54; int INDEX = opdracht == 21 || opdracht == 25 || opdracht == 54 || opdracht == 58 ? opdracht_gegevens.한바이트() : opdracht - (opdracht <= 29 ? 26 : opdracht <= 45 ? 42 : opdracht <= 62 ? 59 : 75);
                cheque_lokaal(INDEX,lokaal_AANTAL); invoerregel.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (opdracht == 46) Collections.addAll(invoerregel,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (opdracht == 79) Collections.addAll(invoerregel,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (opdracht == 87 || opdracht == 88) invoerregel.add("addl $" + (opdracht == 87 ? 4 : 8) + ", %esp");
            else if (opdracht >= 89 && opdracht <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] order_Lijst = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[opdracht - 89]; 순번++) invoerregel.add("popl " + 저장기들[순번]);
                for (int 순번 : order_Lijst[opdracht - 89]) invoerregel.add("pushl " + 저장기들[순번]);
            } else if (opdracht == 96 || opdracht == 100 || opdracht == 104 || opdracht == 126 || opdracht == 128 || opdracht == 130) {
                String operatie_WAARDE = opdracht == 96 ? "addl" : opdracht == 100 ? "subl" : opdracht == 104 ? "imull" : opdracht == 126 ? "andl" : opdracht == 128 ? "orl" : "xorl";
                Collections.addAll(invoerregel,"popl %ecx","popl %eax",operatie_WAARDE + " %ecx, %eax","pushl %eax");
            } else if (opdracht == 108 || opdracht == 112) Collections.addAll(invoerregel,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + plaatsingsindex + "_divide","cmpl $0x80000000, %eax","jne " + plaatsingsindex + "_divide","xorl %edx, %edx","jmp " + plaatsingsindex + "_done",plaatsingsindex + "_divide:","cltd","idivl %ecx",plaatsingsindex + "_done:","pushl " + (opdracht == 108 ? "%eax" : "%edx"));
            else if (opdracht == 116) invoerregel.add("negl (%esp)");
            else if (opdracht == 120 || opdracht == 122 || opdracht == 124) Collections.addAll(invoerregel,"popl %ecx","popl %eax",(opdracht == 120 ? "sall" : opdracht == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (opdracht == 132) {
                int INDEX = opdracht_gegevens.한바이트(), toename_WAARDE = opdracht_gegevens.부호한바이트(); cheque_lokaal(INDEX,lokaal_AANTAL); invoerregel.add("addl $" + toename_WAARDE + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (opdracht >= 145 && opdracht <= 147) Collections.addAll(invoerregel,"popl %eax",opdracht == 145 ? "movsbl %al, %eax" : opdracht == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (opdracht >= 153 && opdracht <= 166) {
                if (opdracht <= 158) Collections.addAll(invoerregel,"popl %eax","testl %eax, %eax");
                else Collections.addAll(invoerregel,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int doel_WAARDE = positie + opdracht_gegevens.부호두바이트(); branch_Lijst.add(doel_WAARDE); invoerregel.add(비교들[opdracht - (opdracht <= 158 ? 153 : 159)] + " " + markering_WAARDE + "_b" + doel_WAARDE);
            } else if (opdracht == 167 || opdracht == 200) {
                int doel_WAARDE = positie + (opdracht == 167 ? opdracht_gegevens.부호두바이트() : opdracht_gegevens.네바이트()); branch_Lijst.add(doel_WAARDE); invoerregel.add("jmp " + markering_WAARDE + "_b" + doel_WAARDE);
            } else if (opdracht == 170 || opdracht == 171) {
                while (opdracht_gegevens.positie % 4 != 0) opdracht_gegevens.한바이트();
                int standaardwaarde = positie + opdracht_gegevens.네바이트(); branch_Lijst.add(standaardwaarde); invoerregel.add("popl %eax");
                int item_AANTAL, 아래 = 0;
                if (opdracht == 170) { 아래 = opdracht_gegevens.네바이트(); int 위 = opdracht_gegevens.네바이트(); long tijdsduur_WAARDE = (long)위 - 아래 + 1; if (tijdsduur_WAARDE < 1 || tijdsduur_WAARDE > (opdracht_gegevens.gegevens.length - opdracht_gegevens.positie) / 4) throw new Vertaling_fout("switch clip fout"); item_AANTAL = (int)tijdsduur_WAARDE; }
                else { item_AANTAL = opdracht_gegevens.네바이트(); if (item_AANTAL < 0 || item_AANTAL > (opdracht_gegevens.gegevens.length - opdracht_gegevens.positie) / 8) throw new Vertaling_fout("switch Grootte fout"); }
                for (int 순번 = 0; 순번 < item_AANTAL; 순번++) {
                    int WAARDE = opdracht == 170 ? 아래 + 순번 : opdracht_gegevens.네바이트(), doel_WAARDE = positie + opdracht_gegevens.네바이트(); branch_Lijst.add(doel_WAARDE);
                    Collections.addAll(invoerregel,"cmpl $" + WAARDE + ", %eax","je " + markering_WAARDE + "_b" + doel_WAARDE);
                }
                invoerregel.add("jmp " + markering_WAARDE + "_b" + standaardwaarde);
            } else if (opdracht == 172 || opdracht == 176 || opdracht == 177) {
                if (opdracht != 177) invoerregel.add("popl %eax"); Collections.addAll(invoerregel,"leave","ret");
            } else if (opdracht == 178 || opdracht == 179) {
                methode_verwijzen verwijzen = les_WAARDE.verwijzen(opdracht_gegevens.두바이트()); if (!필드들.containsKey(verwijzen)) throw new Vertaling_fout("알 nummer 없는 veldwaarde");
                Collections.addAll(invoerregel,"call " + symbool("init",verwijzen.eigenaar_WAARDE),(opdracht == 178 ? "pushl " : "popl ") + symbool("field",verwijzen.부분들()));
            } else if (opdracht == 184) {
                methode_verwijzen verwijzen = les_WAARDE.verwijzen(opdracht_gegevens.두바이트()); if (!함수들.containsKey(verwijzen)) throw new Vertaling_fout("알 nummer 없는 FUNCTIE_WAARDE");
                함수형식 호출형식 = new 함수형식(verwijzen.서술); Collections.addAll(invoerregel,"call " + symbool("init",verwijzen.eigenaar_WAARDE),"call " + symbool("method",verwijzen.부분들()));
                if (!호출형식.argumenten.isEmpty()) invoerregel.add("addl $" + 호출형식.argumenten.size() * 4 + ", %esp");
                if (!호출형식.Retour_HR.equals("V")) invoerregel.add("pushl %eax");
            } else if (opdracht == 182) {
                methode_verwijzen verwijzen = les_WAARDE.verwijzen(opdracht_gegevens.두바이트());
                if (verwijzen.equals(new methode_verwijzen("java/lang/String","length","()I"))) Collections.addAll(invoerregel,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (verwijzen.equals(new methode_verwijzen("java/lang/String","charAt","(I)C"))) Collections.addAll(invoerregel,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Vertaling_fout("가상 FUNCTIE_WAARDE 호출 미지원");
            } else if (opdracht == 188) {
                if (opdracht_gegevens.한바이트() != 10) throw new Vertaling_fout("new int[]만 steun_WAARDE"); Collections.addAll(invoerregel,"popl %eax","call rt_new_array","pushl %eax");
            } else if (opdracht == 190) Collections.addAll(invoerregel,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (opdracht == 196) {
                int extensie_WAARDE = opdracht_gegevens.한바이트(), INDEX = opdracht_gegevens.두바이트(); cheque_lokaal(INDEX,lokaal_AANTAL);
                if (extensie_WAARDE == 21 || extensie_WAARDE == 25 || extensie_WAARDE == 54 || extensie_WAARDE == 58) invoerregel.add((extensie_WAARDE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (extensie_WAARDE == 132) invoerregel.add("addl $" + opdracht_gegevens.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Vertaling_fout("wide opdracht 미지원");
            } else if (opdracht == 198 || opdracht == 199) {
                int doel_WAARDE = positie + opdracht_gegevens.부호두바이트(); branch_Lijst.add(doel_WAARDE); Collections.addAll(invoerregel,"popl %eax","testl %eax, %eax",(opdracht == 198 ? "je " : "jne ") + markering_WAARDE + "_b" + doel_WAARDE);
            } else throw new Vertaling_fout("미지원 opdracht: " + opdracht);
        }
        if (!경계들.containsAll(branch_Lijst)) throw new Vertaling_fout("opdracht 경계가 아닌 곳으로 branch");
        invoerregel.add(".size " + markering_WAARDE + ", .-" + markering_WAARDE); return String.join("\n",invoerregel);
    }
    String X_86_constante(les_gegevens gegevens, int INDEX) {
        if (gegevens.constante_soort[INDEX] == 3) return gegevens.constante_gegevens[INDEX].toString();
        if (gegevens.constante_soort[INDEX] == 8) return tekenreeks_symbool(gegevens.문자((Integer)gegevens.constante_gegevens[INDEX]));
        throw new Vertaling_fout("정수와 tekenreeks_WAARDE 상수만 steun_WAARDE");
    }
    String X_86_assembly(String beginpunt, List<String> 내보냄, String doel) throws IOException {
        Map<String,String> machine_tabel = new HashMap<>();
        for (String invoerregel : Files.readAllLines(bron_pad.resolve("_86_machine_Functions.tsv"))) { String[] koppelen_WAARDE = invoerregel.split("\t"); if (koppelen_WAARDE[0].equals(doel)) machine_tabel.put(koppelen_WAARDE[1] + koppelen_WAARDE[2],koppelen_WAARDE[3]); }
        int plaatsingsindex = beginpunt.lastIndexOf('.'); if (plaatsingsindex < 0) throw new Vertaling_fout("beginpunt Toewijzen_WAARDE fout");
        String eigenaar_WAARDE = beginpunt.substring(0,plaatsingsindex).replace('.','/'), methode_invoer_naam = beginpunt.substring(plaatsingsindex + 1); methode_verwijzen beginpunt_WAARDE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { methode_verwijzen verwijzen = new methode_verwijzen(eigenaar_WAARDE,methode_invoer_naam,서술); if (함수들.containsKey(verwijzen)) { if (beginpunt_WAARDE != null) throw new Vertaling_fout("겹친 beginpunt"); beginpunt_WAARDE = verwijzen; } }
        if (beginpunt_WAARDE == null || (함수들.get(beginpunt_WAARDE).toegang_invoer & 0x100) != 0) throw new Vertaling_fout("beginpunt_WAARDE FUNCTIE_WAARDE opmaak_WAARDE fout");
        List<String> invoerregel = new ArrayList<>(); invoerregel.add(".code32");
        for (les_gegevens gegevens : 클래스들.values()) {
            String Status_WAARDE = symbool("state",gegevens.Naam), initialiseren = symbool("init",gegevens.Naam);
            Collections.addAll(invoerregel,".bss",".balign 4",Status_WAARDE + ": .long 0",".text",initialiseren + ":","cmpl $0, " + Status_WAARDE,"jne " + initialiseren + "_done","movl $1, " + Status_WAARDE);
            methode_verwijzen 초기화참조 = new methode_verwijzen(gegevens.Naam,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) invoerregel.add("call " + symbool("method",초기화참조.부분들()));
            Collections.addAll(invoerregel,"movl $2, " + Status_WAARDE,initialiseren + "_done:","ret");
            for (lid_gegevens veldwaarde : gegevens.veldwaarde) {
                byte[] constante_WAARDE = veldwaarde.kenmerkwaarde.get("ConstantValue"); String WAARDE = constante_WAARDE == null ? "0" : X_86_constante(gegevens,new gegevens_Lezer(constante_WAARDE).두바이트());
                Collections.addAll(invoerregel,".data",".balign 4",symbool("field",gegevens.Naam,veldwaarde.Naam,veldwaarde.서술) + ": .long " + WAARDE);
            }
            for (lid_gegevens FUNCTIE_WAARDE : gegevens.FUNCTIE_WAARDE) if (!FUNCTIE_WAARDE.Naam.equals("<init>")) invoerregel.add(X_86_methode_hoofdtekst(new methode_verwijzen(gegevens.Naam,FUNCTIE_WAARDE.Naam,FUNCTIE_WAARDE.서술),FUNCTIE_WAARDE,machine_tabel,doel));
        }
        Collections.addAll(invoerregel,".text",".globl java_entry","java_entry:","call " + symbool("init",beginpunt_WAARDE.eigenaar_WAARDE),"call " + symbool("method",beginpunt_WAARDE.부분들()));
        if (beginpunt_WAARDE.서술.equals("()V")) invoerregel.add("xorl %eax, %eax"); invoerregel.add("ret");
        for (String Toewijzen_WAARDE : 내보냄) {
            int scheidingsteken_WAARDE = Toewijzen_WAARDE.indexOf('='); if (scheidingsteken_WAARDE < 1) throw new Vertaling_fout("내보내기 Toewijzen_WAARDE fout");
            String extern_WAARDE = Toewijzen_WAARDE.substring(0,scheidingsteken_WAARDE), FUNCTIE_WAARDE = Toewijzen_WAARDE.substring(scheidingsteken_WAARDE + 1); int deling_HR = FUNCTIE_WAARDE.lastIndexOf('.');
            if (deling_HR < 0 || !extern_WAARDE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Vertaling_fout("내보내기 symbool fout");
            String les_WAARDE = FUNCTIE_WAARDE.substring(0,deling_HR).replace('.','/'), Naam = FUNCTIE_WAARDE.substring(deling_HR + 1); methode_verwijzen selectie_WAARDE = null;
            for (methode_verwijzen verwijzen : 함수들.keySet()) if (verwijzen.eigenaar_WAARDE.equals(les_WAARDE) && verwijzen.Naam.equals(Naam)) { if (selectie_WAARDE != null) throw new Vertaling_fout("겹친 내보내기 doel"); selectie_WAARDE = verwijzen; }
            if (selectie_WAARDE == null) throw new Vertaling_fout("내보낼 함수가 없음");
            Collections.addAll(invoerregel,".text",".globl " + extern_WAARDE,extern_WAARDE + ":","call " + symbool("init",selectie_WAARDE.eigenaar_WAARDE),"jmp " + symbool("method",selectie_WAARDE.부분들()));
        }
        invoerregel.add(".section .rodata");
        for (Map.Entry<String,String> invoer_WAARDE_962f286b : 문자열들.entrySet()) {
            Collections.addAll(invoerregel,".balign 4",invoer_WAARDE_962f286b.getValue() + ":",".long " + invoer_WAARDE_962f286b.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char les_WAARDE_7c611f50 : invoer_WAARDE_962f286b.getKey().toCharArray()) 단위들.add(Integer.toString(les_WAARDE_7c611f50)); if (!단위들.isEmpty()) invoerregel.add(".long " + String.join(",",단위들));
        }
        invoerregel.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",invoerregel) + "\n";
    }
    static void Uitvoeren_hulpmiddel(List<String> opdracht) throws Exception {
        if (new ProcessBuilder(opdracht).inheritIO().start().waitFor() != 0) throw new Vertaling_fout("compileren_bron fout: " + opdracht.get(0));
    }
    static String gegevens_tekenreeks(String tekst) { return "\"" + tekst.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Vertaling(List<Path> invoer_Lijst, String doel, String beginpunt, List<String> 내보냄, Path tekstuitvoer, Path bron_WAARDE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), les_pad = 임시.resolve("classes"); Files.createDirectory(les_pad);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",les_pad.toString(),"-sourcepath",les_pad.toString(),"-d",les_pad.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int bron_AANTAL = 0;
            for (Path invoer_WAARDE : invoer_Lijst) {
                if (tekstuitvoer.toAbsolutePath().normalize().equals(invoer_WAARDE.toAbsolutePath().normalize())) throw new Vertaling_fout("tekstuitvoer 파일과 입력이 같음");
                if (invoer_WAARDE.toString().endsWith(".java")) { 자바명령.add(invoer_WAARDE.toString()); bron_AANTAL++; }
                else if (invoer_WAARDE.toString().endsWith(".class")) 바이트코드.add(invoer_WAARDE);
                else throw new Vertaling_fout(".java 또는 .class만 steun_WAARDE");
            }
            if (bron_AANTAL > 0) Uitvoeren_hulpmiddel(자바명령);
            try (java.util.stream.Stream<Path> pad_Lijst = Files.walk(les_pad)) { pad_Lijst.filter(pad -> pad.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERTEREN_WAARDE = new 기계어미리번역(바이트코드,doel.equals("user") ? "user" : "kernel",262144,bron_WAARDE);
            String 조립 = CONVERTEREN_WAARDE.X_86_assembly(beginpunt,내보냄,doel); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path hulpmiddel_functie = bron_WAARDE.getParent();
            Uitvoeren_hulpmiddel(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Uitvoeren_hulpmiddel(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),hulpmiddel_functie.resolve("CLR_steun.s").toString()));
            List<String> Verbinden = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (doel.equals("kernel")) Verbinden.add("-r");
            else {
                Uitvoeren_hulpmiddel(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),hulpmiddel_functie.resolve(doel.equals("user") ? "START_gebruiker_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Verbinden,"-e","_start",임시.resolve("start.o").toString());
                if (doel.equals("user")) Collections.addAll(Verbinden,"-T",hulpmiddel_functie.resolve("gebruiker_link_Indeling.ld").toString());
            }
            Collections.addAll(Verbinden,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Uitvoeren_hulpmiddel(Verbinden);
            tekstuitvoer = tekstuitvoer.toAbsolutePath(); Files.createDirectories(tekstuitvoer.getParent()); Path publiceren_WAARDE = Files.createTempFile(tekstuitvoer.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publiceren_WAARDE,StandardCopyOption.REPLACE_EXISTING); Files.move(publiceren_WAARDE,tekstuitvoer,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publiceren_WAARDE); }
            Files.setPosixFilePermissions(tekstuitvoer,java.nio.file.attribute.PosixFilePermissions.fromString(doel.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(tekstuitvoer + ".s"),조립,StandardCharsets.UTF_8);
            List<String> symbool_gegevens = new ArrayList<>(), brongegevens = new ArrayList<>();
            for (methode_verwijzen verwijzen : CONVERTEREN_WAARDE.함수들.keySet()) symbool_gegevens.add(gegevens_tekenreeks(symbool("method",verwijzen.부분들())) + ":" + gegevens_tekenreeks(verwijzen.eigenaar_WAARDE + "." + verwijzen.Naam + verwijzen.서술));
            for (Path invoer_WAARDE : invoer_Lijst) {
                byte[] hash_Bestand = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(invoer_WAARDE)); StringBuilder tekst = new StringBuilder(); for (byte WAARDE : hash_Bestand) tekst.append(String.format(Locale.ROOT,"%02x",WAARDE & 255));
                brongegevens.add(gegevens_tekenreeks(invoer_WAARDE.toAbsolutePath().toString()) + ":" + gegevens_tekenreeks(tekst.toString()));
            }
            Files.writeString(Paths.get(tekstuitvoer + ".json"),"{\"target\":" + gegevens_tekenreeks(doel) + ",\"entry\":" + gegevens_tekenreeks(beginpunt) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbool_gegevens) + "},\"sources\":{" + String.join(",",brongegevens) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> pad_Lijst = Files.walk(임시)) { for (Path pad : (Iterable<Path>)pad_Lijst.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(pad); }
        }
    }
    public static void main(String[] argumenten) {
        try {
            String beginpunt = null, doel = "kernel", X_86_doel = null; Path uitvoer_pad = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> pad_Lijst = new ArrayList<>();
            for (int 순번 = 0; 순번 < argumenten.length; 순번++) {
                String WAARDE = argumenten[순번];
                switch (WAARDE) {
                    case "--target": X_86_doel = argumenten[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry les_WAARDE.FUNCTIE_WAARDE -o tekstuitvoer [--target linux|kernel|user] [--profile kernel|user] [--export symbool=les_WAARDE.FUNCTIE_WAARDE] 클래스파일 또는 Java원문"); return;
                    case "--entry": beginpunt = argumenten[++순번]; break;
                    case "--profile": doel = argumenten[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(argumenten[++순번]); break;
                    case "--export": 내보냄.add(argumenten[++순번]); break;
                    case "-o": uitvoer_pad = Paths.get(argumenten[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (WAARDE.startsWith("-")) throw new Vertaling_fout("알 nummer 없는 옵션: " + WAARDE); pad_Lijst.add(Paths.get(WAARDE));
                }
            }
            if (beginpunt == null || uitvoer_pad == null || pad_Lijst.isEmpty()) throw new Vertaling_fout("--entry, -o, les_WAARDE 파일이 필요합니다");
            Path bron_WAARDE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_doel != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_doel)) throw new Vertaling_fout("알 nummer 없는 Uitvoeren_opdracht doel");
                X_86_Vertaling(pad_Lijst,X_86_doel,beginpunt,내보냄,uitvoer_pad,bron_WAARDE); return;
            }
            String broncode = new 기계어미리번역(pad_Lijst, doel, 낱말수, bron_WAARDE).genereren(beginpunt, 내보냄, 범용표기);
            uitvoer_pad = uitvoer_pad.toAbsolutePath(); Files.createDirectories(uitvoer_pad.getParent());
            Path 임시 = Files.createTempFile(uitvoer_pad.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, broncode, StandardCharsets.UTF_8); Files.move(임시, uitvoer_pad, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception fout) { System.err.println("compileren_bron fout: " + fout.getMessage()); System.exit(1); }
    }
}
