// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Classe_VALOR 파일에서 독립 ARM64 커널용 C 원문을 만든다. allotjar JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Traducció_error extends RuntimeException {
        Traducció_error(String 설명) { super(설명); }
    }
    static final class dades_Lector {
        final byte[] dades;
        int Posició;
        dades_Lector(byte[] 입력자료) { dades = 입력자료; }
        byte[] Lectura(int durada_VALOR) {
            if (durada_VALOR < 0 || durada_VALOR > dades.length - Posició) throw new Traducció_error("잘린 Classe_VALOR 또는 Ordre dades");
            byte[] RESULTAT = Arrays.copyOfRange(dades, Posició, Posició + durada_VALOR); Posició += durada_VALOR; return RESULTAT;
        }
        int tancar_byte() { if (Posició >= dades.length) throw new Traducció_error("잘린 Ordre dades"); return dades[Posició++] & 255; }
        int 두바이트() { return (tancar_byte() << 8) | tancar_byte(); }
        int tancar_ENTER() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) tancar_byte(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class membre_dades {
        final int accés_introducció;
        final String Nom, 서술;
        final Map<String, byte[]> valor_d_atribut;
        membre_dades(int accés_VALOR, String nom_VALOR, String 서술값, Map<String, byte[]> atribut_dades) {
            accés_introducció = accés_VALOR; Nom = nom_VALOR; 서술 = 서술값; valor_d_atribut = atribut_dades;
        }
    }
    static final class 함수참조 implements Comparable<함수참조> {
        final String propietari_VALOR, Nom, 서술;
        함수참조(String 소유값, String nom_VALOR, String 서술값) { propietari_VALOR = 소유값; Nom = nom_VALOR; 서술 = 서술값; }
        String[] 부분들() { return new String[]{propietari_VALOR, Nom, 서술}; }
        public int compareTo(함수참조 homòleg_VALOR) {
            int Comparació_VALOR = propietari_VALOR.compareTo(homòleg_VALOR.propietari_VALOR);
            if (Comparació_VALOR == 0) Comparació_VALOR = Nom.compareTo(homòleg_VALOR.Nom);
            return Comparació_VALOR == 0 ? 서술.compareTo(homòleg_VALOR.서술) : Comparació_VALOR;
        }
        public boolean equals(Object homòleg_VALOR) { return homòleg_VALOR instanceof 함수참조 && compareTo((함수참조) homòleg_VALOR) == 0; }
        public int hashCode() { return Objects.hash(propietari_VALOR, Nom, 서술); }
    }
    static final class Classe_dades {
        final int[] 상수종류;
        final Object[] 상수값;
        final String Nom;
        final List<membre_dades> camp_VALOR, FUNCIÓ_VALOR;
        Classe_dades(Path Camí) throws IOException {
            dades_Lector Lector_VALOR = new dades_Lector(Files.readAllBytes(Camí));
            if (Lector_VALOR.tancar_ENTER() != 0xcafebabe) throw new Traducció_error("Java Classe_VALOR 표식이 아님");
            Lector_VALOR.Lectura(4);
            int element_COMPT = Lector_VALOR.두바이트(); 상수종류 = new int[element_COMPT]; 상수값 = new Object[element_COMPT];
            for (int 순번 = 1; 순번 < element_COMPT; 순번++) {
                int 종류 = Lector_VALOR.tancar_byte(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int durada_VALOR = Lector_VALOR.두바이트();
                        byte[] caràcter_memòria_intermèdia = Lector_VALOR.Lectura(durada_VALOR), 길이붙인자료 = new byte[durada_VALOR + 2];
                        길이붙인자료[0] = (byte)(durada_VALOR >> 8); 길이붙인자료[1] = (byte)durada_VALOR;
                        System.arraycopy(caràcter_memòria_intermèdia, 0, 길이붙인자료, 2, durada_VALOR);
                        상수값[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: 상수값[순번] = Lector_VALOR.tancar_ENTER(); break;
                    case 4: Lector_VALOR.Lectura(4); break;
                    case 5: case 6: Lector_VALOR.Lectura(8); 순번++; break;
                    case 7: case 8: case 16: 상수값[순번] = Lector_VALOR.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        상수값[순번] = new int[]{Lector_VALOR.두바이트(), Lector_VALOR.두바이트()}; break;
                    case 15: 상수값[순번] = new int[]{Lector_VALOR.tancar_byte(), Lector_VALOR.두바이트()}; break;
                    default: throw new Traducció_error("지원하지 않는 상수 종류: " + 종류);
                }
            }
            Lector_VALOR.두바이트(); Nom = nom_de_classe(Lector_VALOR.두바이트());
            if (!nom_de_classe(Lector_VALOR.두바이트()).equals("java/lang/Object") || Lector_VALOR.두바이트() != 0)
                throw new Traducció_error(Nom + ": 상속 및 인터페이스 미지원");
            camp_VALOR = 멤버읽기(Lector_VALOR); FUNCIÓ_VALOR = 멤버읽기(Lector_VALOR); tancar_atributs(Lector_VALOR);
            if (Lector_VALOR.Posició != Lector_VALOR.dades.length) throw new Traducció_error("Classe_VALOR 뒤에 남은 dades");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Traducció_error("문자 상수 INDEX s_ha_produït_un_error");
            return (String) 상수값[INDEX];
        }
        String nom_de_classe(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Traducció_error("Classe_VALOR Referència s_ha_produït_un_error");
            return 문자((Integer)상수값[INDEX]);
        }
        함수참조 Referència(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Traducció_error("멤버 Referència s_ha_produït_un_error");
            int[] enllaçar_VALOR = (int[])상수값[INDEX], nom_enllaçar = (int[])상수값[enllaçar_VALOR[1]];
            return new 함수참조(nom_de_classe(enllaçar_VALOR[0]), 문자(nom_enllaçar[0]), 문자(nom_enllaçar[1]));
        }
        Map<String, byte[]> tancar_atributs(dades_Lector Lector_VALOR) {
            Map<String, byte[]> RESULTAT = new LinkedHashMap<>();
            int element_COMPT = Lector_VALOR.두바이트();
            for (int 순번 = 0; 순번 < element_COMPT; 순번++) {
                String atribut_nom = 문자(Lector_VALOR.두바이트()); byte[] VALOR = Lector_VALOR.Lectura(Lector_VALOR.tancar_ENTER());
                if (RESULTAT.put(atribut_nom, VALOR) != null) throw new Traducció_error("겹친 valor_d_atribut: " + atribut_nom);
            }
            return RESULTAT;
        }
        List<membre_dades> 멤버읽기(dades_Lector Lector_VALOR) {
            List<membre_dades> RESULTAT = new ArrayList<>(); int element_COMPT = Lector_VALOR.두바이트();
            for (int 순번 = 0; 순번 < element_COMPT; 순번++) {
                int accés_introducció = Lector_VALOR.두바이트(); String 함수이름 = 문자(Lector_VALOR.두바이트()), 서술 = 문자(Lector_VALOR.두바이트());
                RESULTAT.add(new membre_dades(accés_introducció, 함수이름, 서술, tancar_atributs(Lector_VALOR)));
            }
            return RESULTAT;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String tornar_les_tasques_mesura;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Traducció_error("FUNCIÓ_VALOR 서술 s_ha_produït_un_error: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Traducció_error("FUNCIÓ_VALOR 서술 s_ha_produït_un_error: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Traducció_error("FUNCIÓ_VALOR 서술 s_ha_produït_un_error: " + 서술);
            tornar_les_tasques_mesura = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> RESULTAT = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Posició = 0; Posició < 서술.length();) {
            String selecció_VALOR = null;
            for (String format_VALOR : 허용형식) if (서술.startsWith(format_VALOR, Posició)) { selecció_VALOR = format_VALOR; break; }
            if (selecció_VALOR == null) throw new Traducció_error("지원하지 않는 tipus_de_dades: " + 서술);
            RESULTAT.add(selecció_VALOR); Posició += selecció_VALOR.length();
        }
        return RESULTAT;
    }
    static String símbol(String 종류, String... 부분들) {
        try {
            byte[] hash_arxiu = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", hash_arxiu[순번] & 255));
            return SMS.toString();
        } catch (Exception s_ha_produït_un_error) { throw new Traducció_error(s_ha_produït_un_error.toString()); }
    }
    final Map<String, Classe_dades> 클래스들 = new TreeMap<>();
    final Map<함수참조, membre_dades> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), màquina_Azure_Functions_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, màquina_Classe;
    final int 동적기억낱말수;
    final Path recurs_camí;
    기계어미리번역(List<Path> camí_Llista, String objectiu, int 낱말수, Path recurs_VALOR) throws IOException {
        if ((!objectiu.equals("kernel") && !objectiu.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Traducció_error("Executa_ordre objectiu 또는 Memòria_VALOR 공간 Mida s_ha_produït_un_error");
        실행대상 = objectiu; 동적기억낱말수 = 낱말수; recurs_camí = recurs_VALOR;
        // 이 이름도 국가별 font_arbre generar 시 해당 언어로 옮긴다.
        màquina_Classe = objectiu.equals("kernel") ? "Tauler" : "usuari";
        for (String línia : Files.readAllLines(recurs_VALOR.resolve("màquina_Azure_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = línia.split("\t", -1);
            if (부분들.length != 4) throw new Traducció_error("màquina FUNCIÓ_VALOR dades s_ha_produït_un_error");
            if (부분들[0].equals(objectiu)) màquina_Azure_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path Camí : camí_Llista) {
            Classe_dades dades = new Classe_dades(Camí);
            if (클래스들.put(dades.Nom, dades) != null) throw new Traducció_error("중복 Classe_VALOR: " + dades.Nom);
            for (membre_dades camp_VALOR : dades.camp_VALOR) {
                if ((camp_VALOR.accés_introducció & 8) == 0 || 형식읽기(camp_VALOR.서술).equals(Collections.singletonList("V"))) throw new Traducció_error("estàtic_VALOR 필드만 suport_VALOR");
                if (필드들.put(new 함수참조(dades.Nom, camp_VALOR.Nom, camp_VALOR.서술), camp_VALOR) != null) throw new Traducció_error("중복 camp_VALOR");
            }
            for (membre_dades FUNCIÓ_VALOR : dades.FUNCIÓ_VALOR) {
                if (FUNCIÓ_VALOR.Nom.equals("<init>")) continue;
                if ((FUNCIÓ_VALOR.accés_introducció & 8) == 0 || (FUNCIÓ_VALOR.accés_introducció & (0x20 | 0x400)) != 0) throw new Traducció_error("estàtic_VALOR 비동기화 함수만 suport_VALOR");
                new 함수형식(FUNCIÓ_VALOR.서술);
                if (함수들.put(new 함수참조(dades.Nom, FUNCIÓ_VALOR.Nom, FUNCIÓ_VALOR.서술), FUNCIÓ_VALOR) != null) throw new Traducció_error("중복 FUNCIÓ_VALOR");
            }
        }
    }
    String cadena_símbol(String SMS) { return 문자열들.computeIfAbsent(SMS, VALOR -> "j_text_" + 문자열들.size()); }
    String 상수표현(Classe_dades dades, int INDEX) {
        if (INDEX < 1 || INDEX >= dades.상수종류.length) throw new Traducció_error("상수 INDEX clip s_ha_produït_un_error");
        if (dades.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + dades.상수값[INDEX] + ")";
        if (dades.상수종류[INDEX] == 8) return "(word)" + cadena_símbol(dades.문자((Integer)dades.상수값[INDEX]));
        throw new Traducció_error("정수와 cadena_VALOR 상수만 suport_VALOR");
    }
    String 함수원형(함수참조 Referència) {
        List<String> 인수들 = new ArrayList<>(); int element_COMPT = new 함수형식(Referència.서술).인수.size();
        for (int 순번 = 0; 순번 < element_COMPT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + símbol("method", Referència.부분들()) + "(" + (element_COMPT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void xec_local(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Traducció_error("local_Àmbit 변수 INDEX clip s_ha_produït_un_error"); }
    void 분기넣기(List<String> Sortida, Set<Integer> branca_Llista, int Posició, int 이동량, String condició) {
        int destinació_VALOR = Posició + 이동량; branca_Llista.add(destinació_VALOR);
        Sortida.add((condició == null ? "" : "if (" + condició + ") ") + "goto b" + destinació_VALOR + ";");
    }
    String 함수본문(함수참조 FUNCIÓ_VALOR, membre_dades dades) {
        byte[] text_dades = dades.valor_d_atribut.get("Code"); if (text_dades == null) throw new Traducció_error("FUNCIÓ_VALOR 몸체가 없음: " + FUNCIÓ_VALOR.Nom);
        dades_Lector Lector_VALOR = new dades_Lector(text_dades); int 쌓임깊이 = Lector_VALOR.두바이트(), 지역변수수 = Lector_VALOR.두바이트();
        dades_Lector ordre_dades = new dades_Lector(Lector_VALOR.Lectura(Lector_VALOR.tancar_ENTER()));
        if (Lector_VALOR.두바이트() != 0) throw new Traducció_error("try/catch/finally 미지원");
        함수형식 format_VALOR = new 함수형식(FUNCIÓ_VALOR.서술); if (지역변수수 < format_VALOR.인수.size()) throw new Traducció_error("매개변수보다 적은 local_Àmbit 변수");
        Classe_dades Classe_VALOR = 클래스들.get(FUNCIÓ_VALOR.propietari_VALOR);
        List<String> Sortida = new ArrayList<>(); Sortida.add(함수원형(FUNCIÓ_VALOR) + " {");
        Sortida.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALOR.인수.size(); 순번++) Sortida.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), branca_Llista = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (ordre_dades.Posició < ordre_dades.dades.length) {
            int Posició = ordre_dades.Posició, Ordre = ordre_dades.tancar_byte(); 경계들.add(Posició); Sortida.add("b" + Posició + ":;");
            if (Ordre == 0) continue;
            if (Ordre == 1) Sortida.add("PUSH(0);");
            else if (Ordre >= 2 && Ordre <= 8) Sortida.add("PUSH((uint32_t)(" + (Ordre - 3) + "));");
            else if (Ordre == 16 || Ordre == 17) Sortida.add("PUSH((uint32_t)(" + (Ordre == 16 ? ordre_dades.부호한바이트() : ordre_dades.부호두바이트()) + "));");
            else if (Ordre == 18 || Ordre == 19) Sortida.add("PUSH(" + 상수표현(Classe_VALOR, Ordre == 18 ? ordre_dades.tancar_byte() : ordre_dades.두바이트()) + ");");
            else if (Ordre == 21 || Ordre == 25 || (Ordre >= 26 && Ordre <= 29) || (Ordre >= 42 && Ordre <= 45)) {
                int INDEX = Ordre == 21 || Ordre == 25 ? ordre_dades.tancar_byte() : Ordre - (Ordre <= 29 ? 26 : 42);
                xec_local(INDEX, 지역변수수); Sortida.add("PUSH(l[" + INDEX + "]);");
            } else if (Ordre == 54 || Ordre == 58 || (Ordre >= 59 && Ordre <= 62) || (Ordre >= 75 && Ordre <= 78)) {
                int INDEX = Ordre == 54 || Ordre == 58 ? ordre_dades.tancar_byte() : Ordre - (Ordre <= 62 ? 59 : 75);
                xec_local(INDEX, 지역변수수); Sortida.add("l[" + INDEX + "] = POP();");
            } else if (Ordre == 46) Sortida.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Ordre == 79) Sortida.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Ordre == 87 || Ordre == 88) Sortida.add(Ordre == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Ordre >= 89 && Ordre <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] comanda_Llista = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Ordre - 89]; 순번++) Sortida.add("abcd".charAt(순번) + " = POP();");
                for (char VALOR : comanda_Llista[Ordre - 89].toCharArray()) Sortida.add("PUSH(" + VALOR + ");");
            } else if (Ordre == 96 || Ordre == 100 || Ordre == 104 || Ordre == 126 || Ordre == 128 || Ordre == 130) {
                String cirurgia_VALOR = Ordre == 96 ? "+" : Ordre == 100 ? "-" : Ordre == 104 ? "*" : Ordre == 126 ? "&" : Ordre == 128 ? "|" : "^";
                Sortida.add("b = POP(); a = POP(); PUSH((uint32_t)a " + cirurgia_VALOR + " (uint32_t)b);");
            } else if (Ordre == 108 || Ordre == 112) Sortida.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Ordre == 112 ? 1 : 0) + "));");
            else if (Ordre == 116) Sortida.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Ordre == 120 || Ordre == 122 || Ordre == 124) {
                Sortida.add("b = POP(); a = POP();"); Sortida.add("PUSH(" + (Ordre == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Ordre == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Ordre == 132) {
                int INDEX = ordre_dades.tancar_byte(), 증가량 = ordre_dades.부호한바이트(); xec_local(INDEX, 지역변수수);
                Sortida.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Ordre >= 145 && Ordre <= 147) Sortida.add("a = POP(); PUSH((uint32_t)(" + (Ordre == 145 ? "int8_t" : Ordre == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Ordre >= 153 && Ordre <= 158) {
                Sortida.add("a = POP();"); 분기넣기(Sortida, branca_Llista, Posició, ordre_dades.부호두바이트(), "(int32_t)a " + 비교들[Ordre - 153] + " 0");
            } else if (Ordre >= 159 && Ordre <= 166) {
                Sortida.add("b = POP(); a = POP();"); 분기넣기(Sortida, branca_Llista, Posició, ordre_dades.부호두바이트(), Ordre >= 165 ? "a " + 비교들[Ordre - 159] + " b" : "(int32_t)a " + 비교들[Ordre - 159] + " (int32_t)b");
            } else if (Ordre == 167 || Ordre == 200) 분기넣기(Sortida, branca_Llista, Posició, Ordre == 167 ? ordre_dades.부호두바이트() : ordre_dades.tancar_ENTER(), null);
            else if (Ordre == 170 || Ordre == 171) {
                while (ordre_dades.Posició % 4 != 0) ordre_dades.tancar_byte();
                int valor_per_defecte = ordre_dades.tancar_ENTER(); Sortida.add("a = POP();");
                if (Ordre == 170) {
                    int 아래 = ordre_dades.tancar_ENTER(), 위 = ordre_dades.tancar_ENTER(); long element_COMPT = (long)위 - 아래 + 1;
                    if (element_COMPT < 1 || element_COMPT > (ordre_dades.dades.length - ordre_dades.Posició) / 4) throw new Traducció_error("switch clip s_ha_produït_un_error");
                    for (long VALOR = 아래; VALOR <= 위; VALOR++) 분기넣기(Sortida, branca_Llista, Posició, ordre_dades.tancar_ENTER(), "(int32_t)a == (" + VALOR + ")");
                } else {
                    int element_COMPT = ordre_dades.tancar_ENTER(), frontal_dades = 0;
                    if (element_COMPT < 0 || element_COMPT > (ordre_dades.dades.length - ordre_dades.Posició) / 8) throw new Traducció_error("switch Mida s_ha_produït_un_error");
                    for (int 순번 = 0; 순번 < element_COMPT; 순번++) {
                        int VALOR = ordre_dades.tancar_ENTER(); if (순번 > 0 && VALOR <= frontal_dades) throw new Traducció_error("switch comanda_VALOR s_ha_produït_un_error"); frontal_dades = VALOR;
                        분기넣기(Sortida, branca_Llista, Posició, ordre_dades.tancar_ENTER(), "(int32_t)a == (" + VALOR + ")");
                    }
                }
                분기넣기(Sortida, branca_Llista, Posició, valor_per_defecte, null);
            } else if (Ordre == 172 || Ordre == 176 || Ordre == 177) Sortida.add("return " + (Ordre == 177 ? "0" : "POP()") + ";");
            else if (Ordre == 178 || Ordre == 179) {
                함수참조 Referència = Classe_VALOR.Referència(ordre_dades.두바이트()); if (!필드들.containsKey(Referència)) throw new Traducció_error("알 수 없는 camp_VALOR");
                Sortida.add(símbol("init", Referència.propietari_VALOR) + "();"); String camp_VALOR = símbol("field", Referència.부분들());
                Sortida.add(Ordre == 178 ? "PUSH(" + camp_VALOR + ");" : camp_VALOR + " = POP();");
            } else if (Ordre == 184) {
                함수참조 Referència = Classe_VALOR.Referència(ordre_dades.두바이트()); if (!함수들.containsKey(Referència)) throw new Traducció_error("알 수 없는 FUNCIÓ_VALOR");
                함수형식 호출형식 = new 함수형식(Referència.서술); int element_COMPT = 호출형식.인수.size();
                Sortida.add(símbol("init", Referència.propietari_VALOR) + "();"); Sortida.add("if(sp < " + element_COMPT + ") kernel_panic(\"call stack underflow\"); sp -= " + element_COMPT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < element_COMPT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Sortida.add("a = " + símbol("method", Referència.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.tornar_les_tasques_mesura.equals("V")) Sortida.add("PUSH(a);");
            } else if (Ordre == 182) {
                함수참조 Referència = Classe_VALOR.Referència(ordre_dades.두바이트());
                if (Referència.equals(new 함수참조("java/lang/String", "length", "()I"))) Sortida.add("a = POP(); PUSH(length(a));");
                else if (Referència.equals(new 함수참조("java/lang/String", "charAt", "(I)C"))) Sortida.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Traducció_error("가상 FUNCIÓ_VALOR 호출 미지원");
            } else if (Ordre == 188) {
                if (ordre_dades.tancar_byte() != 10) throw new Traducció_error("new int[]만 suport_VALOR"); Sortida.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Ordre == 190) Sortida.add("a = POP(); PUSH(length(a));");
            else if (Ordre == 196) {
                int extensió_VALOR = ordre_dades.tancar_byte(), INDEX = ordre_dades.두바이트(); xec_local(INDEX, 지역변수수);
                if (extensió_VALOR == 21 || extensió_VALOR == 25) Sortida.add("PUSH(l[" + INDEX + "]);");
                else if (extensió_VALOR == 54 || extensió_VALOR == 58) Sortida.add("l[" + INDEX + "] = POP();");
                else if (extensió_VALOR == 132) Sortida.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + ordre_dades.부호두바이트() + ");");
                else throw new Traducció_error("미지원 wide Ordre");
            } else if (Ordre == 198 || Ordre == 199) {
                Sortida.add("a = POP();"); 분기넣기(Sortida, branca_Llista, Posició, ordre_dades.부호두바이트(), "a " + (Ordre == 198 ? "==" : "!=") + " 0");
            } else throw new Traducció_error(FUNCIÓ_VALOR.propietari_VALOR + "." + FUNCIÓ_VALOR.Nom + ", byte_VALOR " + Posició + ": 미지원 Ordre " + Ordre);
        }
        if (!경계들.containsAll(branca_Llista)) throw new Traducció_error("Ordre 경계가 아닌 곳으로 branca");
        Sortida.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Sortida);
    }
    String 내보낼함수(String enllaç_símbol, String objectiu, boolean 진입점여부) {
        int càrrec_INDEX = objectiu.lastIndexOf('.'); if (càrrec_INDEX < 0 || !enllaç_símbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Traducció_error("내보내기 cedir_VALOR s_ha_produït_un_error");
        String propietari_VALOR = objectiu.substring(0, càrrec_INDEX).replace('.', '/'), Nom = objectiu.substring(càrrec_INDEX + 1); 함수참조 selecció_VALOR = null;
        for (함수참조 Referència : 함수들.keySet()) if (Referència.propietari_VALOR.equals(propietari_VALOR) && Referència.Nom.equals(Nom)) {
            if (selecció_VALOR != null) throw new Traducció_error("겹친 내보내기 objectiu"); selecció_VALOR = Referència;
        }
        if (selecció_VALOR == null || (함수들.get(selecció_VALOR).accés_introducció & 0x100) != 0) throw new Traducció_error("내보낼 함수가 없음 또는 native FUNCIÓ_VALOR");
        함수형식 format_VALOR = new 함수형식(selecció_VALOR.서술);
        if ((진입점여부 && !format_VALOR.인수.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALOR.tornar_les_tasques_mesura)) throw new Traducció_error("introducció_p_VALOR 또는 C 경계 format_VALOR s_ha_produït_un_error");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALOR.인수.size(); 순번++) {
            if (!format_VALOR.인수.get(순번).equals("I")) throw new Traducció_error("C 경계는 int 인수만 suport_VALOR");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALOR.tornar_les_tasques_mesura.equals("V") ? "void " : "int32_t ") + enllaç_símbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + símbol("init", selecció_VALOR.propietari_VALOR) + "(); " + (format_VALOR.tornar_les_tasques_mesura.equals("V") ? "" : "return (int32_t)") + símbol("method", selecció_VALOR.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generar(String introducció_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<함수참조, membre_dades> introducció_VALOR : 함수들.entrySet()) {
            함수참조 Referència = introducció_VALOR.getKey(); membre_dades dades = introducció_VALOR.getValue(); 선언들.add(함수원형(Referència) + ";");
            if ((dades.accés_introducció & 0x100) != 0) {
                String Connecta = màquina_Azure_Functions_c3a8e64a.get(Referència.Nom + Referència.서술);
                if (!Referència.propietari_VALOR.equals(màquina_Classe) || Connecta == null) throw new Traducció_error("허용되지 않은 native FUNCIÓ_VALOR: " + Referència.Nom);
                int element_COMPT = new 함수형식(Referència.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < element_COMPT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Connecta + "(" + (element_COMPT == 0 ? "void" : String.join(",", Collections.nCopies(element_COMPT, "word"))) + ");");
                몸체들.add(함수원형(Referència) + " { return " + Connecta + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Referència, dades));
        }
        for (Map.Entry<함수참조, membre_dades> introducció_VALOR : 필드들.entrySet()) {
            함수참조 Referència = introducció_VALOR.getKey(); byte[] 상수 = introducció_VALOR.getValue().valor_d_atribut.get("ConstantValue");
            String VALOR = 상수 == null ? "0" : 상수표현(클래스들.get(Referència.propietari_VALOR), new dades_Lector(상수).두바이트());
            필드선언들.add("static word " + símbol("field", Referència.부분들()) + " = " + VALOR + ";");
        }
        for (String Nom : 클래스들.keySet()) {
            String inicialitzar = símbol("init", Nom), Estat_VALOR = símbol("state", Nom);
            선언들.add("static void " + inicialitzar + "(void);"); 필드선언들.add("static unsigned " + Estat_VALOR + ";");
            함수참조 Referència = new 함수참조(Nom, "<clinit>", "()V");
            몸체들.add("static void " + inicialitzar + "(void) { if(" + Estat_VALOR + ") return; " + Estat_VALOR + " = 1; " + (함수들.containsKey(Referència) ? símbol("method", Referència.부분들()) + "(); " : "") + Estat_VALOR + " = 2; }");
        }
        몸체들.add(내보낼함수("java_entry", introducció_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String cedir_VALOR : 내보내기목록) {
            int càrrec_INDEX = cedir_VALOR.indexOf('='); if (càrrec_INDEX < 1) throw new Traducció_error("내보내기 cedir_VALOR s_ha_produït_un_error");
            String Nom = cedir_VALOR.substring(0, càrrec_INDEX); 공개이름.add(Nom); 몸체들.add(내보낼함수(Nom, cedir_VALOR.substring(càrrec_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> introducció_VALOR : 문자열들.entrySet()) {
            String SMS = introducció_VALOR.getKey(); StringBuilder MATRIU_VALOR = new StringBuilder("static const word " + introducció_VALOR.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) MATRIU_VALOR.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(MATRIU_VALOR.append("};").toString());
        }
        String suport_VALOR = Files.readString(recurs_camí.resolve("실행지원.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(suport_VALOR + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String FONT, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nom_taula = new HashMap<>();
        for (String línia : Files.readAllLines(recurs_camí.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] enllaçar_VALOR = línia.split("\t"); nom_taula.put(enllaçar_VALOR[0], enllaçar_VALOR[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(FONT); StringBuffer RESULTAT = new StringBuffer();
        while (찾개.find()) {
            String Nom = 찾개.group(), 새이름 = Nom;
            if (!Nom.startsWith("//") && !Nom.startsWith("/*") && !Nom.startsWith("\"") && !Nom.startsWith("'") && !공개이름.contains(Nom)) {
                새이름 = nom_taula.getOrDefault(Nom, Nom);
                if (Nom.matches("a[0-9]+")) 새이름 = "인수" + Nom.substring(1);
                if (Nom.matches("b[0-9]+")) 새이름 = "branca" + Nom.substring(1);
                if (범용표기) {
                    StringBuilder notació_VALOR = new StringBuilder();
                    for (char caràcter_VALOR : 새이름.toCharArray()) notació_VALOR.append(caràcter_VALOR < 128 ? Character.toString(caràcter_VALOR) : String.format(Locale.ROOT, "\\u%04x", (int)caràcter_VALOR));
                    새이름 = notació_VALOR.toString();
                }
            }
            찾개.appendReplacement(RESULTAT, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(RESULTAT); return RESULTAT.toString();
    }
    String 엑스함수본문(함수참조 FUNCIÓ_VALOR, membre_dades dades, Map<String,String> màquina_taula, String objectiu) {
        String 표식 = símbol("method", FUNCIÓ_VALOR.부분들());
        List<String> línia = new ArrayList<>();
        if ((dades.accés_introducció & 0x100) != 0) {
            String Connecta = màquina_taula.get(FUNCIÓ_VALOR.Nom + FUNCIÓ_VALOR.서술);
            if (!FUNCIÓ_VALOR.propietari_VALOR.equals(objectiu.equals("kernel") ? "dispositiu_VALOR" : "usuari") || Connecta == null) throw new Traducció_error("허용되지 않은 native FUNCIÓ_VALOR");
            return ".text\n" + 표식 + ":\njmp " + Connecta;
        }
        byte[] text_del_cos = dades.valor_d_atribut.get("Code"); if (text_del_cos == null) throw new Traducció_error("FUNCIÓ_VALOR 몸체가 없음");
        dades_Lector Lector_VALOR = new dades_Lector(text_del_cos); Lector_VALOR.두바이트(); int local_COMPT = Lector_VALOR.두바이트();
        dades_Lector ordre_dades = new dades_Lector(Lector_VALOR.Lectura(Lector_VALOR.tancar_ENTER()));
        if (Lector_VALOR.두바이트() != 0) throw new Traducció_error("try/catch/finally 미지원");
        함수형식 format_VALOR = new 함수형식(FUNCIÓ_VALOR.서술); if (local_COMPT < format_VALOR.인수.size()) throw new Traducció_error("매개변수보다 적은 local_Àmbit 변수");
        Collections.addAll(línia,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + local_COMPT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALOR.인수.size(); 순번++) Collections.addAll(línia,"movl " + (8 + 4 * (format_VALOR.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Classe_dades Classe_VALOR = 클래스들.get(FUNCIÓ_VALOR.propietari_VALOR); Set<Integer> 경계들 = new HashSet<>(), branca_Llista = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (ordre_dades.Posició < ordre_dades.dades.length) {
            int Posició = ordre_dades.Posició, Ordre = ordre_dades.tancar_byte(); String càrrec_INDEX = 표식 + "_b" + Posició;
            línia.add(càrrec_INDEX + ":"); 경계들.add(Posició);
            if (Ordre == 0) línia.add("nop");
            else if (Ordre == 1) línia.add("pushl $0");
            else if (Ordre >= 2 && Ordre <= 8) línia.add("pushl $" + (Ordre - 3));
            else if (Ordre == 16 || Ordre == 17) línia.add("pushl $" + (Ordre == 16 ? ordre_dades.부호한바이트() : ordre_dades.부호두바이트()));
            else if (Ordre == 18 || Ordre == 19) {
                int INDEX = Ordre == 18 ? ordre_dades.tancar_byte() : ordre_dades.두바이트();
                línia.add("pushl $" + 엑스상수(Classe_VALOR,INDEX));
            } else if (Ordre == 21 || Ordre == 25 || (Ordre >= 26 && Ordre <= 29) || (Ordre >= 42 && Ordre <= 45) || Ordre == 54 || Ordre == 58 || (Ordre >= 59 && Ordre <= 62) || (Ordre >= 75 && Ordre <= 78)) {
                boolean tancar_mesura = Ordre < 54; int INDEX = Ordre == 21 || Ordre == 25 || Ordre == 54 || Ordre == 58 ? ordre_dades.tancar_byte() : Ordre - (Ordre <= 29 ? 26 : Ordre <= 45 ? 42 : Ordre <= 62 ? 59 : 75);
                xec_local(INDEX,local_COMPT); línia.add((tancar_mesura ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Ordre == 46) Collections.addAll(línia,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Ordre == 79) Collections.addAll(línia,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Ordre == 87 || Ordre == 88) línia.add("addl $" + (Ordre == 87 ? 4 : 8) + ", %esp");
            else if (Ordre >= 89 && Ordre <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] comanda_Llista = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Ordre - 89]; 순번++) línia.add("popl " + 저장기들[순번]);
                for (int 순번 : comanda_Llista[Ordre - 89]) línia.add("pushl " + 저장기들[순번]);
            } else if (Ordre == 96 || Ordre == 100 || Ordre == 104 || Ordre == 126 || Ordre == 128 || Ordre == 130) {
                String cirurgia_VALOR = Ordre == 96 ? "addl" : Ordre == 100 ? "subl" : Ordre == 104 ? "imull" : Ordre == 126 ? "andl" : Ordre == 128 ? "orl" : "xorl";
                Collections.addAll(línia,"popl %ecx","popl %eax",cirurgia_VALOR + " %ecx, %eax","pushl %eax");
            } else if (Ordre == 108 || Ordre == 112) Collections.addAll(línia,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + càrrec_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + càrrec_INDEX + "_divide","xorl %edx, %edx","jmp " + càrrec_INDEX + "_done",càrrec_INDEX + "_divide:","cltd","idivl %ecx",càrrec_INDEX + "_done:","pushl " + (Ordre == 108 ? "%eax" : "%edx"));
            else if (Ordre == 116) línia.add("negl (%esp)");
            else if (Ordre == 120 || Ordre == 122 || Ordre == 124) Collections.addAll(línia,"popl %ecx","popl %eax",(Ordre == 120 ? "sall" : Ordre == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Ordre == 132) {
                int INDEX = ordre_dades.tancar_byte(), 증가 = ordre_dades.부호한바이트(); xec_local(INDEX,local_COMPT); línia.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Ordre >= 145 && Ordre <= 147) Collections.addAll(línia,"popl %eax",Ordre == 145 ? "movsbl %al, %eax" : Ordre == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Ordre >= 153 && Ordre <= 166) {
                if (Ordre <= 158) Collections.addAll(línia,"popl %eax","testl %eax, %eax");
                else Collections.addAll(línia,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int destinació_VALOR = Posició + ordre_dades.부호두바이트(); branca_Llista.add(destinació_VALOR); línia.add(비교들[Ordre - (Ordre <= 158 ? 153 : 159)] + " " + 표식 + "_b" + destinació_VALOR);
            } else if (Ordre == 167 || Ordre == 200) {
                int destinació_VALOR = Posició + (Ordre == 167 ? ordre_dades.부호두바이트() : ordre_dades.tancar_ENTER()); branca_Llista.add(destinació_VALOR); línia.add("jmp " + 표식 + "_b" + destinació_VALOR);
            } else if (Ordre == 170 || Ordre == 171) {
                while (ordre_dades.Posició % 4 != 0) ordre_dades.tancar_byte();
                int valor_per_defecte = Posició + ordre_dades.tancar_ENTER(); branca_Llista.add(valor_per_defecte); línia.add("popl %eax");
                int element_COMPT, 아래 = 0;
                if (Ordre == 170) { 아래 = ordre_dades.tancar_ENTER(); int 위 = ordre_dades.tancar_ENTER(); long durada_VALOR = (long)위 - 아래 + 1; if (durada_VALOR < 1 || durada_VALOR > (ordre_dades.dades.length - ordre_dades.Posició) / 4) throw new Traducció_error("switch clip s_ha_produït_un_error"); element_COMPT = (int)durada_VALOR; }
                else { element_COMPT = ordre_dades.tancar_ENTER(); if (element_COMPT < 0 || element_COMPT > (ordre_dades.dades.length - ordre_dades.Posició) / 8) throw new Traducció_error("switch Mida s_ha_produït_un_error"); }
                for (int 순번 = 0; 순번 < element_COMPT; 순번++) {
                    int VALOR = Ordre == 170 ? 아래 + 순번 : ordre_dades.tancar_ENTER(), destinació_VALOR = Posició + ordre_dades.tancar_ENTER(); branca_Llista.add(destinació_VALOR);
                    Collections.addAll(línia,"cmpl $" + VALOR + ", %eax","je " + 표식 + "_b" + destinació_VALOR);
                }
                línia.add("jmp " + 표식 + "_b" + valor_per_defecte);
            } else if (Ordre == 172 || Ordre == 176 || Ordre == 177) {
                if (Ordre != 177) línia.add("popl %eax"); Collections.addAll(línia,"leave","ret");
            } else if (Ordre == 178 || Ordre == 179) {
                함수참조 Referència = Classe_VALOR.Referència(ordre_dades.두바이트()); if (!필드들.containsKey(Referència)) throw new Traducció_error("알 수 없는 camp_VALOR");
                Collections.addAll(línia,"call " + símbol("init",Referència.propietari_VALOR),(Ordre == 178 ? "pushl " : "popl ") + símbol("field",Referència.부분들()));
            } else if (Ordre == 184) {
                함수참조 Referència = Classe_VALOR.Referència(ordre_dades.두바이트()); if (!함수들.containsKey(Referència)) throw new Traducció_error("알 수 없는 FUNCIÓ_VALOR");
                함수형식 호출형식 = new 함수형식(Referència.서술); Collections.addAll(línia,"call " + símbol("init",Referència.propietari_VALOR),"call " + símbol("method",Referència.부분들()));
                if (!호출형식.인수.isEmpty()) línia.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.tornar_les_tasques_mesura.equals("V")) línia.add("pushl %eax");
            } else if (Ordre == 182) {
                함수참조 Referència = Classe_VALOR.Referència(ordre_dades.두바이트());
                if (Referència.equals(new 함수참조("java/lang/String","length","()I"))) Collections.addAll(línia,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Referència.equals(new 함수참조("java/lang/String","charAt","(I)C"))) Collections.addAll(línia,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Traducció_error("가상 FUNCIÓ_VALOR 호출 미지원");
            } else if (Ordre == 188) {
                if (ordre_dades.tancar_byte() != 10) throw new Traducció_error("new int[]만 suport_VALOR"); Collections.addAll(línia,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Ordre == 190) Collections.addAll(línia,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Ordre == 196) {
                int extensió_VALOR = ordre_dades.tancar_byte(), INDEX = ordre_dades.두바이트(); xec_local(INDEX,local_COMPT);
                if (extensió_VALOR == 21 || extensió_VALOR == 25 || extensió_VALOR == 54 || extensió_VALOR == 58) línia.add((extensió_VALOR <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (extensió_VALOR == 132) línia.add("addl $" + ordre_dades.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Traducció_error("wide Ordre 미지원");
            } else if (Ordre == 198 || Ordre == 199) {
                int destinació_VALOR = Posició + ordre_dades.부호두바이트(); branca_Llista.add(destinació_VALOR); Collections.addAll(línia,"popl %eax","testl %eax, %eax",(Ordre == 198 ? "je " : "jne ") + 표식 + "_b" + destinació_VALOR);
            } else throw new Traducció_error("미지원 Ordre: " + Ordre);
        }
        if (!경계들.containsAll(branca_Llista)) throw new Traducció_error("Ordre 경계가 아닌 곳으로 branca");
        línia.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",línia);
    }
    String 엑스상수(Classe_dades dades, int INDEX) {
        if (dades.상수종류[INDEX] == 3) return dades.상수값[INDEX].toString();
        if (dades.상수종류[INDEX] == 8) return cadena_símbol(dades.문자((Integer)dades.상수값[INDEX]));
        throw new Traducció_error("정수와 cadena_VALOR 상수만 suport_VALOR");
    }
    String X_86_assemblatge(String introducció_p, List<String> 내보냄, String objectiu) throws IOException {
        Map<String,String> màquina_taula = new HashMap<>();
        for (String línia : Files.readAllLines(recurs_camí.resolve("_86_màquina_Azure_Functions.tsv"))) { String[] enllaçar_VALOR = línia.split("\t"); if (enllaçar_VALOR[0].equals(objectiu)) màquina_taula.put(enllaçar_VALOR[1] + enllaçar_VALOR[2],enllaçar_VALOR[3]); }
        int càrrec_INDEX = introducció_p.lastIndexOf('.'); if (càrrec_INDEX < 0) throw new Traducció_error("introducció_p cedir_VALOR s_ha_produït_un_error");
        String propietari_VALOR = introducció_p.substring(0,càrrec_INDEX).replace('.','/'), 함수이름 = introducció_p.substring(càrrec_INDEX + 1); 함수참조 introducció_p_VALOR = null;
        for (String 서술 : Arrays.asList("()I","()V")) { 함수참조 Referència = new 함수참조(propietari_VALOR,함수이름,서술); if (함수들.containsKey(Referència)) { if (introducció_p_VALOR != null) throw new Traducció_error("겹친 introducció_p"); introducció_p_VALOR = Referència; } }
        if (introducció_p_VALOR == null || (함수들.get(introducció_p_VALOR).accés_introducció & 0x100) != 0) throw new Traducció_error("introducció_p_VALOR FUNCIÓ_VALOR format_VALOR s_ha_produït_un_error");
        List<String> línia = new ArrayList<>(); línia.add(".code32");
        for (Classe_dades dades : 클래스들.values()) {
            String Estat_VALOR = símbol("state",dades.Nom), inicialitzar = símbol("init",dades.Nom);
            Collections.addAll(línia,".bss",".balign 4",Estat_VALOR + ": .long 0",".text",inicialitzar + ":","cmpl $0, " + Estat_VALOR,"jne " + inicialitzar + "_done","movl $1, " + Estat_VALOR);
            함수참조 초기화참조 = new 함수참조(dades.Nom,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) línia.add("call " + símbol("method",초기화참조.부분들()));
            Collections.addAll(línia,"movl $2, " + Estat_VALOR,inicialitzar + "_done:","ret");
            for (membre_dades camp_VALOR : dades.camp_VALOR) {
                byte[] 상수 = camp_VALOR.valor_d_atribut.get("ConstantValue"); String VALOR = 상수 == null ? "0" : 엑스상수(dades,new dades_Lector(상수).두바이트());
                Collections.addAll(línia,".data",".balign 4",símbol("field",dades.Nom,camp_VALOR.Nom,camp_VALOR.서술) + ": .long " + VALOR);
            }
            for (membre_dades FUNCIÓ_VALOR : dades.FUNCIÓ_VALOR) if (!FUNCIÓ_VALOR.Nom.equals("<init>")) línia.add(엑스함수본문(new 함수참조(dades.Nom,FUNCIÓ_VALOR.Nom,FUNCIÓ_VALOR.서술),FUNCIÓ_VALOR,màquina_taula,objectiu));
        }
        Collections.addAll(línia,".text",".globl java_entry","java_entry:","call " + símbol("init",introducció_p_VALOR.propietari_VALOR),"call " + símbol("method",introducció_p_VALOR.부분들()));
        if (introducció_p_VALOR.서술.equals("()V")) línia.add("xorl %eax, %eax"); línia.add("ret");
        for (String cedir_VALOR : 내보냄) {
            int 구분 = cedir_VALOR.indexOf('='); if (구분 < 1) throw new Traducció_error("내보내기 cedir_VALOR s_ha_produït_un_error");
            String extern_VALOR = cedir_VALOR.substring(0,구분), FUNCIÓ_VALOR = cedir_VALOR.substring(구분 + 1); int divisió_mesura = FUNCIÓ_VALOR.lastIndexOf('.');
            if (divisió_mesura < 0 || !extern_VALOR.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Traducció_error("내보내기 símbol s_ha_produït_un_error");
            String Classe_VALOR = FUNCIÓ_VALOR.substring(0,divisió_mesura).replace('.','/'), Nom = FUNCIÓ_VALOR.substring(divisió_mesura + 1); 함수참조 selecció_VALOR = null;
            for (함수참조 Referència : 함수들.keySet()) if (Referència.propietari_VALOR.equals(Classe_VALOR) && Referència.Nom.equals(Nom)) { if (selecció_VALOR != null) throw new Traducció_error("겹친 내보내기 objectiu"); selecció_VALOR = Referència; }
            if (selecció_VALOR == null) throw new Traducció_error("내보낼 함수가 없음");
            Collections.addAll(línia,".text",".globl " + extern_VALOR,extern_VALOR + ":","call " + símbol("init",selecció_VALOR.propietari_VALOR),"jmp " + símbol("method",selecció_VALOR.부분들()));
        }
        línia.add(".section .rodata");
        for (Map.Entry<String,String> introducció_VALOR : 문자열들.entrySet()) {
            Collections.addAll(línia,".balign 4",introducció_VALOR.getValue() + ":",".long " + introducció_VALOR.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lliçó_VALOR : introducció_VALOR.getKey().toCharArray()) 단위들.add(Integer.toString(lliçó_VALOR)); if (!단위들.isEmpty()) línia.add(".long " + String.join(",",단위들));
        }
        línia.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",línia) + "\n";
    }
    static void Executa_eina(List<String> Ordre) throws Exception {
        if (new ProcessBuilder(Ordre).inheritIO().start().waitFor() != 0) throw new Traducció_error("generar_font s_ha_produït_un_error: " + Ordre.get(0));
    }
    static String dades_cadena(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Traducció(List<Path> 입력들, String objectiu, String introducció_p, List<String> 내보냄, Path Sortida, Path recurs_VALOR) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Classe_camí = 임시.resolve("classes"); Files.createDirectory(Classe_camí);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Classe_camí.toString(),"-sourcepath",Classe_camí.toString(),"-d",Classe_camí.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int font_COMPT = 0;
            for (Path 입력 : 입력들) {
                if (Sortida.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Traducció_error("Sortida 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); font_COMPT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Traducció_error(".java 또는 .class만 suport_VALOR");
            }
            if (font_COMPT > 0) Executa_eina(자바명령);
            try (java.util.stream.Stream<Path> camí_Llista = Files.walk(Classe_camí)) { camí_Llista.filter(Camí -> Camí.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALOR = new 기계어미리번역(바이트코드,objectiu.equals("user") ? "user" : "kernel",262144,recurs_VALOR);
            String 조립 = CONVERT_VALOR.X_86_assemblatge(introducció_p,내보냄,objectiu); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path eina_càrrec = recurs_VALOR.getParent();
            Executa_eina(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Executa_eina(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),eina_càrrec.resolve("실행지원.s").toString()));
            List<String> Connecta = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (objectiu.equals("kernel")) Connecta.add("-r");
            else {
                Executa_eina(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),eina_càrrec.resolve(objectiu.equals("user") ? "Inici_usuari_programa.s" : "리눅스시작.s").toString()));
                Collections.addAll(Connecta,"-e","_start",임시.resolve("start.o").toString());
                if (objectiu.equals("user")) Collections.addAll(Connecta,"-T",eina_càrrec.resolve("usuari_enllaç_disseny.ld").toString());
            }
            Collections.addAll(Connecta,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Executa_eina(Connecta);
            Sortida = Sortida.toAbsolutePath(); Files.createDirectories(Sortida.getParent()); Path publicar_VALOR = Files.createTempFile(Sortida.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publicar_VALOR,StandardCopyOption.REPLACE_EXISTING); Files.move(publicar_VALOR,Sortida,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publicar_VALOR); }
            Files.setPosixFilePermissions(Sortida,java.nio.file.attribute.PosixFilePermissions.fromString(objectiu.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Sortida + ".s"),조립,StandardCharsets.UTF_8);
            List<String> símbol_dades = new ArrayList<>(), font_dades = new ArrayList<>();
            for (함수참조 Referència : CONVERT_VALOR.함수들.keySet()) símbol_dades.add(dades_cadena(símbol("method",Referència.부분들())) + ":" + dades_cadena(Referència.propietari_VALOR + "." + Referència.Nom + Referència.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_arxiu = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte VALOR : hash_arxiu) SMS.append(String.format(Locale.ROOT,"%02x",VALOR & 255));
                font_dades.add(dades_cadena(입력.toAbsolutePath().toString()) + ":" + dades_cadena(SMS.toString()));
            }
            Files.writeString(Paths.get(Sortida + ".json"),"{\"target\":" + dades_cadena(objectiu) + ",\"entry\":" + dades_cadena(introducció_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",símbol_dades) + "},\"sources\":{" + String.join(",",font_dades) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> camí_Llista = Files.walk(임시)) { for (Path Camí : (Iterable<Path>)camí_Llista.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(Camí); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String introducció_p = null, objectiu = "kernel", X_86_objectiu = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> camí_Llista = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALOR = 인수[순번];
                switch (VALOR) {
                    case "--target": X_86_objectiu = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Classe_VALOR.FUNCIÓ_VALOR -o Sortida [--target linux|kernel|user] [--profile kernel|user] [--export símbol=Classe_VALOR.FUNCIÓ_VALOR] 클래스파일 또는 Java원문"); return;
                    case "--entry": introducció_p = 인수[++순번]; break;
                    case "--profile": objectiu = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALOR.startsWith("-")) throw new Traducció_error("알 수 없는 옵션: " + VALOR); camí_Llista.add(Paths.get(VALOR));
                }
            }
            if (introducció_p == null || 출력경로 == null || camí_Llista.isEmpty()) throw new Traducció_error("--entry, -o, Classe_VALOR 파일이 필요합니다");
            Path recurs_VALOR = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_objectiu != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_objectiu)) throw new Traducció_error("알 수 없는 Executa_ordre objectiu");
                X_86_Traducció(camí_Llista,X_86_objectiu,introducció_p,내보냄,출력경로,recurs_VALOR); return;
            }
            String FONT = new 기계어미리번역(camí_Llista, objectiu, 낱말수, recurs_VALOR).generar(introducció_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, FONT, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception s_ha_produït_un_error) { System.err.println("generar_font s_ha_produït_un_error: " + s_ha_produït_un_error.getMessage()); System.exit(1); }
    }
}
