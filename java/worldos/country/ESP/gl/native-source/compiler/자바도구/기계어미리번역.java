// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Clase_VALOR 파일에서 독립 ARM64 커널용 C 원문을 만든다. hospedar JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Tradución_erro extends RuntimeException {
        Tradución_erro(String 설명) { super(설명); }
    }
    static final class datos_Lector {
        final byte[] datos;
        int Posición;
        datos_Lector(byte[] 입력자료) { datos = 입력자료; }
        byte[] Lectura(int duración_VALOR) {
            if (duración_VALOR < 0 || duración_VALOR > datos.length - Posición) throw new Tradución_erro("잘린 Clase_VALOR 또는 Orde datos");
            byte[] RESULTANTE = Arrays.copyOfRange(datos, Posición, Posición + duración_VALOR); Posición += duración_VALOR; return RESULTANTE;
        }
        int 한바이트() { if (Posición >= datos.length) throw new Tradución_erro("잘린 Orde datos"); return datos[Posición++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class membro_datos {
        final int acceso_introdución;
        final String Nome, 서술;
        final Map<String, byte[]> atributo_VALOR;
        membro_datos(int acceso_VALOR, String nome_VALOR, String 서술값, Map<String, byte[]> atributo_datos) {
            acceso_introdución = acceso_VALOR; Nome = nome_VALOR; 서술 = 서술값; atributo_VALOR = atributo_datos;
        }
    }
    static final class 함수참조 implements Comparable<함수참조> {
        final String propietario_VALOR, Nome, 서술;
        함수참조(String 소유값, String nome_VALOR, String 서술값) { propietario_VALOR = 소유값; Nome = nome_VALOR; 서술 = 서술값; }
        String[] 부분들() { return new String[]{propietario_VALOR, Nome, 서술}; }
        public int compareTo(함수참조 punto_VALOR) {
            int Comparación_VALOR = propietario_VALOR.compareTo(punto_VALOR.propietario_VALOR);
            if (Comparación_VALOR == 0) Comparación_VALOR = Nome.compareTo(punto_VALOR.Nome);
            return Comparación_VALOR == 0 ? 서술.compareTo(punto_VALOR.서술) : Comparación_VALOR;
        }
        public boolean equals(Object punto_VALOR) { return punto_VALOR instanceof 함수참조 && compareTo((함수참조) punto_VALOR) == 0; }
        public int hashCode() { return Objects.hash(propietario_VALOR, Nome, 서술); }
    }
    static final class Clase_datos {
        final int[] 상수종류;
        final Object[] constante_datos;
        final String Nome;
        final List<membro_datos> campo_VALOR, FUNCIÓN_VALOR;
        Clase_datos(Path CAMIÑO) throws IOException {
            datos_Lector Lector_VALOR = new datos_Lector(Files.readAllBytes(CAMIÑO));
            if (Lector_VALOR.네바이트() != 0xcafebabe) throw new Tradución_erro("Java Clase_VALOR 표식이 아님");
            Lector_VALOR.Lectura(4);
            int elemento_CONTAR = Lector_VALOR.두바이트(); 상수종류 = new int[elemento_CONTAR]; constante_datos = new Object[elemento_CONTAR];
            for (int 순번 = 1; 순번 < elemento_CONTAR; 순번++) {
                int 종류 = Lector_VALOR.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int duración_VALOR = Lector_VALOR.두바이트();
                        byte[] carácter_búfer = Lector_VALOR.Lectura(duración_VALOR), 길이붙인자료 = new byte[duración_VALOR + 2];
                        길이붙인자료[0] = (byte)(duración_VALOR >> 8); 길이붙인자료[1] = (byte)duración_VALOR;
                        System.arraycopy(carácter_búfer, 0, 길이붙인자료, 2, duración_VALOR);
                        constante_datos[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: constante_datos[순번] = Lector_VALOR.네바이트(); break;
                    case 4: Lector_VALOR.Lectura(4); break;
                    case 5: case 6: Lector_VALOR.Lectura(8); 순번++; break;
                    case 7: case 8: case 16: constante_datos[순번] = Lector_VALOR.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        constante_datos[순번] = new int[]{Lector_VALOR.두바이트(), Lector_VALOR.두바이트()}; break;
                    case 15: constante_datos[순번] = new int[]{Lector_VALOR.한바이트(), Lector_VALOR.두바이트()}; break;
                    default: throw new Tradución_erro("지원하지 않는 constante_VALOR 종류: " + 종류);
                }
            }
            Lector_VALOR.두바이트(); Nome = nome_de_clase(Lector_VALOR.두바이트());
            if (!nome_de_clase(Lector_VALOR.두바이트()).equals("java/lang/Object") || Lector_VALOR.두바이트() != 0)
                throw new Tradución_erro(Nome + ": 상속 및 인터페이스 미지원");
            campo_VALOR = 멤버읽기(Lector_VALOR); FUNCIÓN_VALOR = 멤버읽기(Lector_VALOR); 속성읽기(Lector_VALOR);
            if (Lector_VALOR.Posición != Lector_VALOR.datos.length) throw new Tradución_erro("Clase_VALOR 뒤에 남은 datos");
        }
        String 문자(int ÍNDICE) {
            if (ÍNDICE < 1 || ÍNDICE >= 상수종류.length || 상수종류[ÍNDICE] != 1) throw new Tradución_erro("문자 constante_VALOR ÍNDICE ERRO");
            return (String) constante_datos[ÍNDICE];
        }
        String nome_de_clase(int ÍNDICE) {
            if (ÍNDICE < 1 || ÍNDICE >= 상수종류.length || 상수종류[ÍNDICE] != 7) throw new Tradución_erro("Clase_VALOR Material_de_referencia ERRO");
            return 문자((Integer)constante_datos[ÍNDICE]);
        }
        함수참조 Material_de_referencia(int ÍNDICE) {
            if (ÍNDICE < 1 || ÍNDICE >= 상수종류.length || 상수종류[ÍNDICE] < 9 || 상수종류[ÍNDICE] > 11) throw new Tradución_erro("멤버 Material_de_referencia ERRO");
            int[] vincular_VALOR = (int[])constante_datos[ÍNDICE], nome_vincular = (int[])constante_datos[vincular_VALOR[1]];
            return new 함수참조(nome_de_clase(vincular_VALOR[0]), 문자(nome_vincular[0]), 문자(nome_vincular[1]));
        }
        Map<String, byte[]> 속성읽기(datos_Lector Lector_VALOR) {
            Map<String, byte[]> RESULTANTE = new LinkedHashMap<>();
            int elemento_CONTAR = Lector_VALOR.두바이트();
            for (int 순번 = 0; 순번 < elemento_CONTAR; 순번++) {
                String atributo_nome = 문자(Lector_VALOR.두바이트()); byte[] VALOR = Lector_VALOR.Lectura(Lector_VALOR.네바이트());
                if (RESULTANTE.put(atributo_nome, VALOR) != null) throw new Tradución_erro("겹친 atributo_VALOR: " + atributo_nome);
            }
            return RESULTANTE;
        }
        List<membro_datos> 멤버읽기(datos_Lector Lector_VALOR) {
            List<membro_datos> RESULTANTE = new ArrayList<>(); int elemento_CONTAR = Lector_VALOR.두바이트();
            for (int 순번 = 0; 순번 < elemento_CONTAR; 순번++) {
                int acceso_introdución = Lector_VALOR.두바이트(); String 함수이름 = 문자(Lector_VALOR.두바이트()), 서술 = 문자(Lector_VALOR.두바이트());
                RESULTANTE.add(new membro_datos(acceso_introdución, 함수이름, 서술, 속성읽기(Lector_VALOR)));
            }
            return RESULTANTE;
        }
    }
    static final class 함수형식 {
        final List<String> Argumentos = new ArrayList<>();
        final String devolver_medida;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Tradución_erro("FUNCIÓN_VALOR 서술 ERRO: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Tradución_erro("FUNCIÓN_VALOR 서술 ERRO: " + 서술);
            Argumentos.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumentos.contains("V") || 반환들.size() != 1) throw new Tradución_erro("FUNCIÓN_VALOR 서술 ERRO: " + 서술);
            devolver_medida = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> RESULTANTE = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Posición = 0; Posición < 서술.length();) {
            String selección_VALOR = null;
            for (String formato_VALOR : 허용형식) if (서술.startsWith(formato_VALOR, Posición)) { selección_VALOR = formato_VALOR; break; }
            if (selección_VALOR == null) throw new Tradución_erro("지원하지 않는 tipo_de_datos: " + 서술);
            RESULTANTE.add(selección_VALOR); Posición += selección_VALOR.length();
        }
        return RESULTANTE;
    }
    static String símbolo(String 종류, String... 부분들) {
        try {
            byte[] hash_Ficheiro = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Texto = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Texto.append(String.format(Locale.ROOT, "%02x", hash_Ficheiro[순번] & 255));
            return Texto.toString();
        } catch (Exception ERRO) { throw new Tradución_erro(ERRO.toString()); }
    }
    final Map<String, Clase_datos> 클래스들 = new TreeMap<>();
    final Map<함수참조, membro_datos> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), máquina_Funcións_de_Azure_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, máquina_Clase;
    final int 동적기억낱말수;
    final Path Recurso_camiño;
    기계어미리번역(List<Path> camiño_Lista, String obxectivo_VALOR, int 낱말수, Path Recurso_VALOR) throws IOException {
        if ((!obxectivo_VALOR.equals("kernel") && !obxectivo_VALOR.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Tradución_erro("executar_comando obxectivo_VALOR 또는 Memoria_VALOR 공간 Tamaño ERRO");
        실행대상 = obxectivo_VALOR; 동적기억낱말수 = 낱말수; Recurso_camiño = Recurso_VALOR;
        // 이 이름도 국가별 fonte_árbore xerar 시 해당 언어로 옮긴다.
        máquina_Clase = obxectivo_VALOR.equals("kernel") ? "Panel" : "usuario";
        for (String Liña : Files.readAllLines(Recurso_VALOR.resolve("máquina_Funcións_de_Azure.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Liña.split("\t", -1);
            if (부분들.length != 4) throw new Tradución_erro("máquina FUNCIÓN_VALOR datos ERRO");
            if (부분들[0].equals(obxectivo_VALOR)) máquina_Funcións_de_Azure_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path CAMIÑO : camiño_Lista) {
            Clase_datos datos = new Clase_datos(CAMIÑO);
            if (클래스들.put(datos.Nome, datos) != null) throw new Tradución_erro("중복 Clase_VALOR: " + datos.Nome);
            for (membro_datos campo_VALOR : datos.campo_VALOR) {
                if ((campo_VALOR.acceso_introdución & 8) == 0 || 형식읽기(campo_VALOR.서술).equals(Collections.singletonList("V"))) throw new Tradución_erro("estático_VALOR 필드만 soporte_VALOR");
                if (필드들.put(new 함수참조(datos.Nome, campo_VALOR.Nome, campo_VALOR.서술), campo_VALOR) != null) throw new Tradución_erro("중복 campo_VALOR");
            }
            for (membro_datos FUNCIÓN_VALOR : datos.FUNCIÓN_VALOR) {
                if (FUNCIÓN_VALOR.Nome.equals("<init>")) continue;
                if ((FUNCIÓN_VALOR.acceso_introdución & 8) == 0 || (FUNCIÓN_VALOR.acceso_introdución & (0x20 | 0x400)) != 0) throw new Tradución_erro("estático_VALOR 비동기화 함수만 soporte_VALOR");
                new 함수형식(FUNCIÓN_VALOR.서술);
                if (함수들.put(new 함수참조(datos.Nome, FUNCIÓN_VALOR.Nome, FUNCIÓN_VALOR.서술), FUNCIÓN_VALOR) != null) throw new Tradución_erro("중복 FUNCIÓN_VALOR");
            }
        }
    }
    String cadea_símbolo(String Texto) { return 문자열들.computeIfAbsent(Texto, VALOR -> "j_text_" + 문자열들.size()); }
    String constante_expresión(Clase_datos datos, int ÍNDICE) {
        if (ÍNDICE < 1 || ÍNDICE >= datos.상수종류.length) throw new Tradución_erro("constante_VALOR ÍNDICE clip ERRO");
        if (datos.상수종류[ÍNDICE] == 3) return "(word)(uint32_t)(" + datos.constante_datos[ÍNDICE] + ")";
        if (datos.상수종류[ÍNDICE] == 8) return "(word)" + cadea_símbolo(datos.문자((Integer)datos.constante_datos[ÍNDICE]));
        throw new Tradución_erro("정수와 cadea_VALOR 상수만 soporte_VALOR");
    }
    String 함수원형(함수참조 Material_de_referencia) {
        List<String> 인수들 = new ArrayList<>(); int elemento_CONTAR = new 함수형식(Material_de_referencia.서술).Argumentos.size();
        for (int 순번 = 0; 순번 < elemento_CONTAR; 순번++) 인수들.add("word a" + 순번);
        return "static word " + símbolo("method", Material_de_referencia.부분들()) + "(" + (elemento_CONTAR == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void cheque_local(int ÍNDICE, int 지역변수수) { if (ÍNDICE < 0 || ÍNDICE >= 지역변수수) throw new Tradución_erro("local_Ámbito 변수 ÍNDICE clip ERRO"); }
    void 분기넣기(List<String> Saída, Set<Integer> ramificación_Lista, int Posición, int 이동량, String condición) {
        int destino_VALOR = Posición + 이동량; ramificación_Lista.add(destino_VALOR);
        Saída.add((condición == null ? "" : "if (" + condición + ") ") + "goto b" + destino_VALOR + ";");
    }
    String 함수본문(함수참조 FUNCIÓN_VALOR, membro_datos datos) {
        byte[] corpo_datos = datos.atributo_VALOR.get("Code"); if (corpo_datos == null) throw new Tradución_erro("FUNCIÓN_VALOR 몸체가 없음: " + FUNCIÓN_VALOR.Nome);
        datos_Lector Lector_VALOR = new datos_Lector(corpo_datos); int 쌓임깊이 = Lector_VALOR.두바이트(), 지역변수수 = Lector_VALOR.두바이트();
        datos_Lector comando_datos = new datos_Lector(Lector_VALOR.Lectura(Lector_VALOR.네바이트()));
        if (Lector_VALOR.두바이트() != 0) throw new Tradución_erro("try/catch/finally 미지원");
        함수형식 formato_VALOR = new 함수형식(FUNCIÓN_VALOR.서술); if (지역변수수 < formato_VALOR.Argumentos.size()) throw new Tradución_erro("매개변수보다 적은 local_Ámbito 변수");
        Clase_datos Clase_VALOR = 클래스들.get(FUNCIÓN_VALOR.propietario_VALOR);
        List<String> Saída = new ArrayList<>(); Saída.add(함수원형(FUNCIÓN_VALOR) + " {");
        Saída.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formato_VALOR.Argumentos.size(); 순번++) Saída.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ramificación_Lista = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (comando_datos.Posición < comando_datos.datos.length) {
            int Posición = comando_datos.Posición, Orde = comando_datos.한바이트(); 경계들.add(Posición); Saída.add("b" + Posición + ":;");
            if (Orde == 0) continue;
            if (Orde == 1) Saída.add("PUSH(0);");
            else if (Orde >= 2 && Orde <= 8) Saída.add("PUSH((uint32_t)(" + (Orde - 3) + "));");
            else if (Orde == 16 || Orde == 17) Saída.add("PUSH((uint32_t)(" + (Orde == 16 ? comando_datos.부호한바이트() : comando_datos.부호두바이트()) + "));");
            else if (Orde == 18 || Orde == 19) Saída.add("PUSH(" + constante_expresión(Clase_VALOR, Orde == 18 ? comando_datos.한바이트() : comando_datos.두바이트()) + ");");
            else if (Orde == 21 || Orde == 25 || (Orde >= 26 && Orde <= 29) || (Orde >= 42 && Orde <= 45)) {
                int ÍNDICE = Orde == 21 || Orde == 25 ? comando_datos.한바이트() : Orde - (Orde <= 29 ? 26 : 42);
                cheque_local(ÍNDICE, 지역변수수); Saída.add("PUSH(l[" + ÍNDICE + "]);");
            } else if (Orde == 54 || Orde == 58 || (Orde >= 59 && Orde <= 62) || (Orde >= 75 && Orde <= 78)) {
                int ÍNDICE = Orde == 54 || Orde == 58 ? comando_datos.한바이트() : Orde - (Orde <= 62 ? 59 : 75);
                cheque_local(ÍNDICE, 지역변수수); Saída.add("l[" + ÍNDICE + "] = POP();");
            } else if (Orde == 46) Saída.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Orde == 79) Saída.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Orde == 87 || Orde == 88) Saída.add(Orde == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Orde >= 89 && Orde <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] orde_Lista = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Orde - 89]; 순번++) Saída.add("abcd".charAt(순번) + " = POP();");
                for (char VALOR : orde_Lista[Orde - 89].toCharArray()) Saída.add("PUSH(" + VALOR + ");");
            } else if (Orde == 96 || Orde == 100 || Orde == 104 || Orde == 126 || Orde == 128 || Orde == 130) {
                String cirurxía_VALOR = Orde == 96 ? "+" : Orde == 100 ? "-" : Orde == 104 ? "*" : Orde == 126 ? "&" : Orde == 128 ? "|" : "^";
                Saída.add("b = POP(); a = POP(); PUSH((uint32_t)a " + cirurxía_VALOR + " (uint32_t)b);");
            } else if (Orde == 108 || Orde == 112) Saída.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Orde == 112 ? 1 : 0) + "));");
            else if (Orde == 116) Saída.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Orde == 120 || Orde == 122 || Orde == 124) {
                Saída.add("b = POP(); a = POP();"); Saída.add("PUSH(" + (Orde == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Orde == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Orde == 132) {
                int ÍNDICE = comando_datos.한바이트(), 증가량 = comando_datos.부호한바이트(); cheque_local(ÍNDICE, 지역변수수);
                Saída.add("l[" + ÍNDICE + "] = (uint32_t)l[" + ÍNDICE + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Orde >= 145 && Orde <= 147) Saída.add("a = POP(); PUSH((uint32_t)(" + (Orde == 145 ? "int8_t" : Orde == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Orde >= 153 && Orde <= 158) {
                Saída.add("a = POP();"); 분기넣기(Saída, ramificación_Lista, Posición, comando_datos.부호두바이트(), "(int32_t)a " + 비교들[Orde - 153] + " 0");
            } else if (Orde >= 159 && Orde <= 166) {
                Saída.add("b = POP(); a = POP();"); 분기넣기(Saída, ramificación_Lista, Posición, comando_datos.부호두바이트(), Orde >= 165 ? "a " + 비교들[Orde - 159] + " b" : "(int32_t)a " + 비교들[Orde - 159] + " (int32_t)b");
            } else if (Orde == 167 || Orde == 200) 분기넣기(Saída, ramificación_Lista, Posición, Orde == 167 ? comando_datos.부호두바이트() : comando_datos.네바이트(), null);
            else if (Orde == 170 || Orde == 171) {
                while (comando_datos.Posición % 4 != 0) comando_datos.한바이트();
                int valor_predefinido = comando_datos.네바이트(); Saída.add("a = POP();");
                if (Orde == 170) {
                    int 아래 = comando_datos.네바이트(), 위 = comando_datos.네바이트(); long elemento_CONTAR = (long)위 - 아래 + 1;
                    if (elemento_CONTAR < 1 || elemento_CONTAR > (comando_datos.datos.length - comando_datos.Posición) / 4) throw new Tradución_erro("switch clip ERRO");
                    for (long VALOR = 아래; VALOR <= 위; VALOR++) 분기넣기(Saída, ramificación_Lista, Posición, comando_datos.네바이트(), "(int32_t)a == (" + VALOR + ")");
                } else {
                    int elemento_CONTAR = comando_datos.네바이트(), frontal_datos = 0;
                    if (elemento_CONTAR < 0 || elemento_CONTAR > (comando_datos.datos.length - comando_datos.Posición) / 8) throw new Tradución_erro("switch Tamaño ERRO");
                    for (int 순번 = 0; 순번 < elemento_CONTAR; 순번++) {
                        int VALOR = comando_datos.네바이트(); if (순번 > 0 && VALOR <= frontal_datos) throw new Tradución_erro("switch orde_VALOR ERRO"); frontal_datos = VALOR;
                        분기넣기(Saída, ramificación_Lista, Posición, comando_datos.네바이트(), "(int32_t)a == (" + VALOR + ")");
                    }
                }
                분기넣기(Saída, ramificación_Lista, Posición, valor_predefinido, null);
            } else if (Orde == 172 || Orde == 176 || Orde == 177) Saída.add("return " + (Orde == 177 ? "0" : "POP()") + ";");
            else if (Orde == 178 || Orde == 179) {
                함수참조 Material_de_referencia = Clase_VALOR.Material_de_referencia(comando_datos.두바이트()); if (!필드들.containsKey(Material_de_referencia)) throw new Tradución_erro("알 수 없는 campo_VALOR");
                Saída.add(símbolo("init", Material_de_referencia.propietario_VALOR) + "();"); String campo_VALOR = símbolo("field", Material_de_referencia.부분들());
                Saída.add(Orde == 178 ? "PUSH(" + campo_VALOR + ");" : campo_VALOR + " = POP();");
            } else if (Orde == 184) {
                함수참조 Material_de_referencia = Clase_VALOR.Material_de_referencia(comando_datos.두바이트()); if (!함수들.containsKey(Material_de_referencia)) throw new Tradución_erro("알 수 없는 FUNCIÓN_VALOR");
                함수형식 호출형식 = new 함수형식(Material_de_referencia.서술); int elemento_CONTAR = 호출형식.Argumentos.size();
                Saída.add(símbolo("init", Material_de_referencia.propietario_VALOR) + "();"); Saída.add("if(sp < " + elemento_CONTAR + ") kernel_panic(\"call stack underflow\"); sp -= " + elemento_CONTAR + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < elemento_CONTAR; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Saída.add("a = " + símbolo("method", Material_de_referencia.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.devolver_medida.equals("V")) Saída.add("PUSH(a);");
            } else if (Orde == 182) {
                함수참조 Material_de_referencia = Clase_VALOR.Material_de_referencia(comando_datos.두바이트());
                if (Material_de_referencia.equals(new 함수참조("java/lang/String", "length", "()I"))) Saída.add("a = POP(); PUSH(length(a));");
                else if (Material_de_referencia.equals(new 함수참조("java/lang/String", "charAt", "(I)C"))) Saída.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Tradución_erro("가상 FUNCIÓN_VALOR 호출 미지원");
            } else if (Orde == 188) {
                if (comando_datos.한바이트() != 10) throw new Tradución_erro("new int[]만 soporte_VALOR"); Saída.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Orde == 190) Saída.add("a = POP(); PUSH(length(a));");
            else if (Orde == 196) {
                int extensión_VALOR = comando_datos.한바이트(), ÍNDICE = comando_datos.두바이트(); cheque_local(ÍNDICE, 지역변수수);
                if (extensión_VALOR == 21 || extensión_VALOR == 25) Saída.add("PUSH(l[" + ÍNDICE + "]);");
                else if (extensión_VALOR == 54 || extensión_VALOR == 58) Saída.add("l[" + ÍNDICE + "] = POP();");
                else if (extensión_VALOR == 132) Saída.add("l[" + ÍNDICE + "] = (uint32_t)l[" + ÍNDICE + "] + (uint32_t)(" + comando_datos.부호두바이트() + ");");
                else throw new Tradución_erro("미지원 wide Orde");
            } else if (Orde == 198 || Orde == 199) {
                Saída.add("a = POP();"); 분기넣기(Saída, ramificación_Lista, Posición, comando_datos.부호두바이트(), "a " + (Orde == 198 ? "==" : "!=") + " 0");
            } else throw new Tradución_erro(FUNCIÓN_VALOR.propietario_VALOR + "." + FUNCIÓN_VALOR.Nome + ", byte_VALOR " + Posición + ": 미지원 Orde " + Orde);
        }
        if (!경계들.containsAll(ramificación_Lista)) throw new Tradución_erro("Orde 경계가 아닌 곳으로 ramificación");
        Saída.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Saída);
    }
    String 내보낼함수(String Ligar_símbolo, String obxectivo_VALOR, boolean 진입점여부) {
        int cargo_ÍNDICE = obxectivo_VALOR.lastIndexOf('.'); if (cargo_ÍNDICE < 0 || !Ligar_símbolo.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tradución_erro("내보내기 Asignar_VALOR ERRO");
        String propietario_VALOR = obxectivo_VALOR.substring(0, cargo_ÍNDICE).replace('.', '/'), Nome = obxectivo_VALOR.substring(cargo_ÍNDICE + 1); 함수참조 selección_VALOR = null;
        for (함수참조 Material_de_referencia : 함수들.keySet()) if (Material_de_referencia.propietario_VALOR.equals(propietario_VALOR) && Material_de_referencia.Nome.equals(Nome)) {
            if (selección_VALOR != null) throw new Tradución_erro("겹친 내보내기 obxectivo_VALOR"); selección_VALOR = Material_de_referencia;
        }
        if (selección_VALOR == null || (함수들.get(selección_VALOR).acceso_introdución & 0x100) != 0) throw new Tradución_erro("내보낼 함수가 없음 또는 native FUNCIÓN_VALOR");
        함수형식 formato_VALOR = new 함수형식(selección_VALOR.서술);
        if ((진입점여부 && !formato_VALOR.Argumentos.isEmpty()) || !Arrays.asList("V", "I").contains(formato_VALOR.devolver_medida)) throw new Tradución_erro("introdución_p_VALOR 또는 C 경계 formato_VALOR ERRO");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formato_VALOR.Argumentos.size(); 순번++) {
            if (!formato_VALOR.Argumentos.get(순번).equals("I")) throw new Tradución_erro("C 경계는 int 인수만 soporte_VALOR");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formato_VALOR.devolver_medida.equals("V") ? "void " : "int32_t ") + Ligar_símbolo + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + símbolo("init", selección_VALOR.propietario_VALOR) + "(); " + (formato_VALOR.devolver_medida.equals("V") ? "" : "return (int32_t)") + símbolo("method", selección_VALOR.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String xerar(String introdución_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<함수참조, membro_datos> introdución_VALOR : 함수들.entrySet()) {
            함수참조 Material_de_referencia = introdución_VALOR.getKey(); membro_datos datos = introdución_VALOR.getValue(); 선언들.add(함수원형(Material_de_referencia) + ";");
            if ((datos.acceso_introdución & 0x100) != 0) {
                String Conectar = máquina_Funcións_de_Azure_c3a8e64a.get(Material_de_referencia.Nome + Material_de_referencia.서술);
                if (!Material_de_referencia.propietario_VALOR.equals(máquina_Clase) || Conectar == null) throw new Tradución_erro("허용되지 않은 native FUNCIÓN_VALOR: " + Material_de_referencia.Nome);
                int elemento_CONTAR = new 함수형식(Material_de_referencia.서술).Argumentos.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < elemento_CONTAR; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Conectar + "(" + (elemento_CONTAR == 0 ? "void" : String.join(",", Collections.nCopies(elemento_CONTAR, "word"))) + ");");
                몸체들.add(함수원형(Material_de_referencia) + " { return " + Conectar + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Material_de_referencia, datos));
        }
        for (Map.Entry<함수참조, membro_datos> introdución_VALOR : 필드들.entrySet()) {
            함수참조 Material_de_referencia = introdución_VALOR.getKey(); byte[] constante_VALOR = introdución_VALOR.getValue().atributo_VALOR.get("ConstantValue");
            String VALOR = constante_VALOR == null ? "0" : constante_expresión(클래스들.get(Material_de_referencia.propietario_VALOR), new datos_Lector(constante_VALOR).두바이트());
            필드선언들.add("static word " + símbolo("field", Material_de_referencia.부분들()) + " = " + VALOR + ";");
        }
        for (String Nome : 클래스들.keySet()) {
            String iniciar = símbolo("init", Nome), Estado_VALOR = símbolo("state", Nome);
            선언들.add("static void " + iniciar + "(void);"); 필드선언들.add("static unsigned " + Estado_VALOR + ";");
            함수참조 Material_de_referencia = new 함수참조(Nome, "<clinit>", "()V");
            몸체들.add("static void " + iniciar + "(void) { if(" + Estado_VALOR + ") return; " + Estado_VALOR + " = 1; " + (함수들.containsKey(Material_de_referencia) ? símbolo("method", Material_de_referencia.부분들()) + "(); " : "") + Estado_VALOR + " = 2; }");
        }
        몸체들.add(내보낼함수("java_entry", introdución_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Asignar_VALOR : 내보내기목록) {
            int cargo_ÍNDICE = Asignar_VALOR.indexOf('='); if (cargo_ÍNDICE < 1) throw new Tradución_erro("내보내기 Asignar_VALOR ERRO");
            String Nome = Asignar_VALOR.substring(0, cargo_ÍNDICE); 공개이름.add(Nome); 몸체들.add(내보낼함수(Nome, Asignar_VALOR.substring(cargo_ÍNDICE + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> introdución_VALOR : 문자열들.entrySet()) {
            String Texto = introdución_VALOR.getKey(); StringBuilder MATRIZ_VALOR = new StringBuilder("static const word " + introdución_VALOR.getValue() + "[] = {" + Texto.length());
            for (int 순번 = 0; 순번 < Texto.length(); 순번++) MATRIZ_VALOR.append(", ").append((int)Texto.charAt(순번));
            문자열선언들.add(MATRIZ_VALOR.append("};").toString());
        }
        String soporte_VALOR = Files.readString(Recurso_camiño.resolve("실행지원.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(soporte_VALOR + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String FONTE, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nome_táboa = new HashMap<>();
        for (String Liña : Files.readAllLines(Recurso_camiño.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] vincular_VALOR = Liña.split("\t"); nome_táboa.put(vincular_VALOR[0], vincular_VALOR[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(FONTE); StringBuffer RESULTANTE = new StringBuffer();
        while (찾개.find()) {
            String Nome = 찾개.group(), 새이름 = Nome;
            if (!Nome.startsWith("//") && !Nome.startsWith("/*") && !Nome.startsWith("\"") && !Nome.startsWith("'") && !공개이름.contains(Nome)) {
                새이름 = nome_táboa.getOrDefault(Nome, Nome);
                if (Nome.matches("a[0-9]+")) 새이름 = "Argumentos" + Nome.substring(1);
                if (Nome.matches("b[0-9]+")) 새이름 = "ramificación" + Nome.substring(1);
                if (범용표기) {
                    StringBuilder notación_VALOR = new StringBuilder();
                    for (char carácter_VALOR : 새이름.toCharArray()) notación_VALOR.append(carácter_VALOR < 128 ? Character.toString(carácter_VALOR) : String.format(Locale.ROOT, "\\u%04x", (int)carácter_VALOR));
                    새이름 = notación_VALOR.toString();
                }
            }
            찾개.appendReplacement(RESULTANTE, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(RESULTANTE); return RESULTANTE.toString();
    }
    String 엑스함수본문(함수참조 FUNCIÓN_VALOR, membro_datos datos, Map<String,String> máquina_táboa, String obxectivo_VALOR) {
        String 표식 = símbolo("method", FUNCIÓN_VALOR.부분들());
        List<String> Liña = new ArrayList<>();
        if ((datos.acceso_introdución & 0x100) != 0) {
            String Conectar = máquina_táboa.get(FUNCIÓN_VALOR.Nome + FUNCIÓN_VALOR.서술);
            if (!FUNCIÓN_VALOR.propietario_VALOR.equals(obxectivo_VALOR.equals("kernel") ? "dispositivo_VALOR" : "usuario") || Conectar == null) throw new Tradución_erro("허용되지 않은 native FUNCIÓN_VALOR");
            return ".text\n" + 표식 + ":\njmp " + Conectar;
        }
        byte[] corpo_do_texto = datos.atributo_VALOR.get("Code"); if (corpo_do_texto == null) throw new Tradución_erro("FUNCIÓN_VALOR 몸체가 없음");
        datos_Lector Lector_VALOR = new datos_Lector(corpo_do_texto); Lector_VALOR.두바이트(); int local_CONTAR = Lector_VALOR.두바이트();
        datos_Lector comando_datos = new datos_Lector(Lector_VALOR.Lectura(Lector_VALOR.네바이트()));
        if (Lector_VALOR.두바이트() != 0) throw new Tradución_erro("try/catch/finally 미지원");
        함수형식 formato_VALOR = new 함수형식(FUNCIÓN_VALOR.서술); if (local_CONTAR < formato_VALOR.Argumentos.size()) throw new Tradución_erro("매개변수보다 적은 local_Ámbito 변수");
        Collections.addAll(Liña,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + local_CONTAR * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formato_VALOR.Argumentos.size(); 순번++) Collections.addAll(Liña,"movl " + (8 + 4 * (formato_VALOR.Argumentos.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Clase_datos Clase_VALOR = 클래스들.get(FUNCIÓN_VALOR.propietario_VALOR); Set<Integer> 경계들 = new HashSet<>(), ramificación_Lista = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (comando_datos.Posición < comando_datos.datos.length) {
            int Posición = comando_datos.Posición, Orde = comando_datos.한바이트(); String cargo_ÍNDICE = 표식 + "_b" + Posición;
            Liña.add(cargo_ÍNDICE + ":"); 경계들.add(Posición);
            if (Orde == 0) Liña.add("nop");
            else if (Orde == 1) Liña.add("pushl $0");
            else if (Orde >= 2 && Orde <= 8) Liña.add("pushl $" + (Orde - 3));
            else if (Orde == 16 || Orde == 17) Liña.add("pushl $" + (Orde == 16 ? comando_datos.부호한바이트() : comando_datos.부호두바이트()));
            else if (Orde == 18 || Orde == 19) {
                int ÍNDICE = Orde == 18 ? comando_datos.한바이트() : comando_datos.두바이트();
                Liña.add("pushl $" + X_86_constante(Clase_VALOR,ÍNDICE));
            } else if (Orde == 21 || Orde == 25 || (Orde >= 26 && Orde <= 29) || (Orde >= 42 && Orde <= 45) || Orde == 54 || Orde == 58 || (Orde >= 59 && Orde <= 62) || (Orde >= 75 && Orde <= 78)) {
                boolean 읽음 = Orde < 54; int ÍNDICE = Orde == 21 || Orde == 25 || Orde == 54 || Orde == 58 ? comando_datos.한바이트() : Orde - (Orde <= 29 ? 26 : Orde <= 45 ? 42 : Orde <= 62 ? 59 : 75);
                cheque_local(ÍNDICE,local_CONTAR); Liña.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (ÍNDICE + 1)) + "(%ebp)");
            } else if (Orde == 46) Collections.addAll(Liña,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Orde == 79) Collections.addAll(Liña,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Orde == 87 || Orde == 88) Liña.add("addl $" + (Orde == 87 ? 4 : 8) + ", %esp");
            else if (Orde >= 89 && Orde <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] orde_Lista = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Orde - 89]; 순번++) Liña.add("popl " + 저장기들[순번]);
                for (int 순번 : orde_Lista[Orde - 89]) Liña.add("pushl " + 저장기들[순번]);
            } else if (Orde == 96 || Orde == 100 || Orde == 104 || Orde == 126 || Orde == 128 || Orde == 130) {
                String cirurxía_VALOR = Orde == 96 ? "addl" : Orde == 100 ? "subl" : Orde == 104 ? "imull" : Orde == 126 ? "andl" : Orde == 128 ? "orl" : "xorl";
                Collections.addAll(Liña,"popl %ecx","popl %eax",cirurxía_VALOR + " %ecx, %eax","pushl %eax");
            } else if (Orde == 108 || Orde == 112) Collections.addAll(Liña,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + cargo_ÍNDICE + "_divide","cmpl $0x80000000, %eax","jne " + cargo_ÍNDICE + "_divide","xorl %edx, %edx","jmp " + cargo_ÍNDICE + "_done",cargo_ÍNDICE + "_divide:","cltd","idivl %ecx",cargo_ÍNDICE + "_done:","pushl " + (Orde == 108 ? "%eax" : "%edx"));
            else if (Orde == 116) Liña.add("negl (%esp)");
            else if (Orde == 120 || Orde == 122 || Orde == 124) Collections.addAll(Liña,"popl %ecx","popl %eax",(Orde == 120 ? "sall" : Orde == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Orde == 132) {
                int ÍNDICE = comando_datos.한바이트(), 증가 = comando_datos.부호한바이트(); cheque_local(ÍNDICE,local_CONTAR); Liña.add("addl $" + 증가 + ", -" + (4 * (ÍNDICE + 1)) + "(%ebp)");
            } else if (Orde >= 145 && Orde <= 147) Collections.addAll(Liña,"popl %eax",Orde == 145 ? "movsbl %al, %eax" : Orde == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Orde >= 153 && Orde <= 166) {
                if (Orde <= 158) Collections.addAll(Liña,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Liña,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int destino_VALOR = Posición + comando_datos.부호두바이트(); ramificación_Lista.add(destino_VALOR); Liña.add(비교들[Orde - (Orde <= 158 ? 153 : 159)] + " " + 표식 + "_b" + destino_VALOR);
            } else if (Orde == 167 || Orde == 200) {
                int destino_VALOR = Posición + (Orde == 167 ? comando_datos.부호두바이트() : comando_datos.네바이트()); ramificación_Lista.add(destino_VALOR); Liña.add("jmp " + 표식 + "_b" + destino_VALOR);
            } else if (Orde == 170 || Orde == 171) {
                while (comando_datos.Posición % 4 != 0) comando_datos.한바이트();
                int valor_predefinido = Posición + comando_datos.네바이트(); ramificación_Lista.add(valor_predefinido); Liña.add("popl %eax");
                int elemento_CONTAR, 아래 = 0;
                if (Orde == 170) { 아래 = comando_datos.네바이트(); int 위 = comando_datos.네바이트(); long duración_VALOR = (long)위 - 아래 + 1; if (duración_VALOR < 1 || duración_VALOR > (comando_datos.datos.length - comando_datos.Posición) / 4) throw new Tradución_erro("switch clip ERRO"); elemento_CONTAR = (int)duración_VALOR; }
                else { elemento_CONTAR = comando_datos.네바이트(); if (elemento_CONTAR < 0 || elemento_CONTAR > (comando_datos.datos.length - comando_datos.Posición) / 8) throw new Tradución_erro("switch Tamaño ERRO"); }
                for (int 순번 = 0; 순번 < elemento_CONTAR; 순번++) {
                    int VALOR = Orde == 170 ? 아래 + 순번 : comando_datos.네바이트(), destino_VALOR = Posición + comando_datos.네바이트(); ramificación_Lista.add(destino_VALOR);
                    Collections.addAll(Liña,"cmpl $" + VALOR + ", %eax","je " + 표식 + "_b" + destino_VALOR);
                }
                Liña.add("jmp " + 표식 + "_b" + valor_predefinido);
            } else if (Orde == 172 || Orde == 176 || Orde == 177) {
                if (Orde != 177) Liña.add("popl %eax"); Collections.addAll(Liña,"leave","ret");
            } else if (Orde == 178 || Orde == 179) {
                함수참조 Material_de_referencia = Clase_VALOR.Material_de_referencia(comando_datos.두바이트()); if (!필드들.containsKey(Material_de_referencia)) throw new Tradución_erro("알 수 없는 campo_VALOR");
                Collections.addAll(Liña,"call " + símbolo("init",Material_de_referencia.propietario_VALOR),(Orde == 178 ? "pushl " : "popl ") + símbolo("field",Material_de_referencia.부분들()));
            } else if (Orde == 184) {
                함수참조 Material_de_referencia = Clase_VALOR.Material_de_referencia(comando_datos.두바이트()); if (!함수들.containsKey(Material_de_referencia)) throw new Tradución_erro("알 수 없는 FUNCIÓN_VALOR");
                함수형식 호출형식 = new 함수형식(Material_de_referencia.서술); Collections.addAll(Liña,"call " + símbolo("init",Material_de_referencia.propietario_VALOR),"call " + símbolo("method",Material_de_referencia.부분들()));
                if (!호출형식.Argumentos.isEmpty()) Liña.add("addl $" + 호출형식.Argumentos.size() * 4 + ", %esp");
                if (!호출형식.devolver_medida.equals("V")) Liña.add("pushl %eax");
            } else if (Orde == 182) {
                함수참조 Material_de_referencia = Clase_VALOR.Material_de_referencia(comando_datos.두바이트());
                if (Material_de_referencia.equals(new 함수참조("java/lang/String","length","()I"))) Collections.addAll(Liña,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Material_de_referencia.equals(new 함수참조("java/lang/String","charAt","(I)C"))) Collections.addAll(Liña,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Tradución_erro("가상 FUNCIÓN_VALOR 호출 미지원");
            } else if (Orde == 188) {
                if (comando_datos.한바이트() != 10) throw new Tradución_erro("new int[]만 soporte_VALOR"); Collections.addAll(Liña,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Orde == 190) Collections.addAll(Liña,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Orde == 196) {
                int extensión_VALOR = comando_datos.한바이트(), ÍNDICE = comando_datos.두바이트(); cheque_local(ÍNDICE,local_CONTAR);
                if (extensión_VALOR == 21 || extensión_VALOR == 25 || extensión_VALOR == 54 || extensión_VALOR == 58) Liña.add((extensión_VALOR <= 25 ? "pushl " : "popl ") + "-" + 4 * (ÍNDICE + 1) + "(%ebp)");
                else if (extensión_VALOR == 132) Liña.add("addl $" + comando_datos.부호두바이트() + ", -" + 4 * (ÍNDICE + 1) + "(%ebp)");
                else throw new Tradución_erro("wide Orde 미지원");
            } else if (Orde == 198 || Orde == 199) {
                int destino_VALOR = Posición + comando_datos.부호두바이트(); ramificación_Lista.add(destino_VALOR); Collections.addAll(Liña,"popl %eax","testl %eax, %eax",(Orde == 198 ? "je " : "jne ") + 표식 + "_b" + destino_VALOR);
            } else throw new Tradución_erro("미지원 Orde: " + Orde);
        }
        if (!경계들.containsAll(ramificación_Lista)) throw new Tradución_erro("Orde 경계가 아닌 곳으로 ramificación");
        Liña.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",Liña);
    }
    String X_86_constante(Clase_datos datos, int ÍNDICE) {
        if (datos.상수종류[ÍNDICE] == 3) return datos.constante_datos[ÍNDICE].toString();
        if (datos.상수종류[ÍNDICE] == 8) return cadea_símbolo(datos.문자((Integer)datos.constante_datos[ÍNDICE]));
        throw new Tradución_erro("정수와 cadea_VALOR 상수만 soporte_VALOR");
    }
    String X_86_ensamblado(String introdución_p, List<String> 내보냄, String obxectivo_VALOR) throws IOException {
        Map<String,String> máquina_táboa = new HashMap<>();
        for (String Liña : Files.readAllLines(Recurso_camiño.resolve("_86_máquina_Funcións_de_Azure.tsv"))) { String[] vincular_VALOR = Liña.split("\t"); if (vincular_VALOR[0].equals(obxectivo_VALOR)) máquina_táboa.put(vincular_VALOR[1] + vincular_VALOR[2],vincular_VALOR[3]); }
        int cargo_ÍNDICE = introdución_p.lastIndexOf('.'); if (cargo_ÍNDICE < 0) throw new Tradución_erro("introdución_p Asignar_VALOR ERRO");
        String propietario_VALOR = introdución_p.substring(0,cargo_ÍNDICE).replace('.','/'), 함수이름 = introdución_p.substring(cargo_ÍNDICE + 1); 함수참조 introdución_p_VALOR = null;
        for (String 서술 : Arrays.asList("()I","()V")) { 함수참조 Material_de_referencia = new 함수참조(propietario_VALOR,함수이름,서술); if (함수들.containsKey(Material_de_referencia)) { if (introdución_p_VALOR != null) throw new Tradución_erro("겹친 introdución_p"); introdución_p_VALOR = Material_de_referencia; } }
        if (introdución_p_VALOR == null || (함수들.get(introdución_p_VALOR).acceso_introdución & 0x100) != 0) throw new Tradución_erro("introdución_p_VALOR FUNCIÓN_VALOR formato_VALOR ERRO");
        List<String> Liña = new ArrayList<>(); Liña.add(".code32");
        for (Clase_datos datos : 클래스들.values()) {
            String Estado_VALOR = símbolo("state",datos.Nome), iniciar = símbolo("init",datos.Nome);
            Collections.addAll(Liña,".bss",".balign 4",Estado_VALOR + ": .long 0",".text",iniciar + ":","cmpl $0, " + Estado_VALOR,"jne " + iniciar + "_done","movl $1, " + Estado_VALOR);
            함수참조 초기화참조 = new 함수참조(datos.Nome,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Liña.add("call " + símbolo("method",초기화참조.부분들()));
            Collections.addAll(Liña,"movl $2, " + Estado_VALOR,iniciar + "_done:","ret");
            for (membro_datos campo_VALOR : datos.campo_VALOR) {
                byte[] constante_VALOR = campo_VALOR.atributo_VALOR.get("ConstantValue"); String VALOR = constante_VALOR == null ? "0" : X_86_constante(datos,new datos_Lector(constante_VALOR).두바이트());
                Collections.addAll(Liña,".data",".balign 4",símbolo("field",datos.Nome,campo_VALOR.Nome,campo_VALOR.서술) + ": .long " + VALOR);
            }
            for (membro_datos FUNCIÓN_VALOR : datos.FUNCIÓN_VALOR) if (!FUNCIÓN_VALOR.Nome.equals("<init>")) Liña.add(엑스함수본문(new 함수참조(datos.Nome,FUNCIÓN_VALOR.Nome,FUNCIÓN_VALOR.서술),FUNCIÓN_VALOR,máquina_táboa,obxectivo_VALOR));
        }
        Collections.addAll(Liña,".text",".globl java_entry","java_entry:","call " + símbolo("init",introdución_p_VALOR.propietario_VALOR),"call " + símbolo("method",introdución_p_VALOR.부분들()));
        if (introdución_p_VALOR.서술.equals("()V")) Liña.add("xorl %eax, %eax"); Liña.add("ret");
        for (String Asignar_VALOR : 내보냄) {
            int delimitador_VALOR = Asignar_VALOR.indexOf('='); if (delimitador_VALOR < 1) throw new Tradución_erro("내보내기 Asignar_VALOR ERRO");
            String externo_VALOR = Asignar_VALOR.substring(0,delimitador_VALOR), FUNCIÓN_VALOR = Asignar_VALOR.substring(delimitador_VALOR + 1); int división_medida = FUNCIÓN_VALOR.lastIndexOf('.');
            if (división_medida < 0 || !externo_VALOR.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tradución_erro("내보내기 símbolo ERRO");
            String Clase_VALOR = FUNCIÓN_VALOR.substring(0,división_medida).replace('.','/'), Nome = FUNCIÓN_VALOR.substring(división_medida + 1); 함수참조 selección_VALOR = null;
            for (함수참조 Material_de_referencia : 함수들.keySet()) if (Material_de_referencia.propietario_VALOR.equals(Clase_VALOR) && Material_de_referencia.Nome.equals(Nome)) { if (selección_VALOR != null) throw new Tradución_erro("겹친 내보내기 obxectivo_VALOR"); selección_VALOR = Material_de_referencia; }
            if (selección_VALOR == null) throw new Tradución_erro("내보낼 함수가 없음");
            Collections.addAll(Liña,".text",".globl " + externo_VALOR,externo_VALOR + ":","call " + símbolo("init",selección_VALOR.propietario_VALOR),"jmp " + símbolo("method",selección_VALOR.부분들()));
        }
        Liña.add(".section .rodata");
        for (Map.Entry<String,String> introdución_VALOR : 문자열들.entrySet()) {
            Collections.addAll(Liña,".balign 4",introdución_VALOR.getValue() + ":",".long " + introdución_VALOR.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lección_VALOR : introdución_VALOR.getKey().toCharArray()) 단위들.add(Integer.toString(lección_VALOR)); if (!단위들.isEmpty()) Liña.add(".long " + String.join(",",단위들));
        }
        Liña.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Liña) + "\n";
    }
    static void executar_ferramenta(List<String> Orde) throws Exception {
        if (new ProcessBuilder(Orde).inheritIO().start().waitFor() != 0) throw new Tradución_erro("compilar_fonte ERRO: " + Orde.get(0));
    }
    static String datos_cadea(String Texto) { return "\"" + Texto.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Tradución(List<Path> 입력들, String obxectivo_VALOR, String introdución_p, List<String> 내보냄, Path Saída, Path Recurso_VALOR) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Clase_camiño = 임시.resolve("classes"); Files.createDirectory(Clase_camiño);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Clase_camiño.toString(),"-sourcepath",Clase_camiño.toString(),"-d",Clase_camiño.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int fonte_CONTAR = 0;
            for (Path 입력 : 입력들) {
                if (Saída.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Tradución_erro("Saída 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); fonte_CONTAR++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Tradución_erro(".java 또는 .class만 soporte_VALOR");
            }
            if (fonte_CONTAR > 0) executar_ferramenta(자바명령);
            try (java.util.stream.Stream<Path> camiño_Lista = Files.walk(Clase_camiño)) { camiño_Lista.filter(CAMIÑO -> CAMIÑO.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERTER_VALOR = new 기계어미리번역(바이트코드,obxectivo_VALOR.equals("user") ? "user" : "kernel",262144,Recurso_VALOR);
            String 조립 = CONVERTER_VALOR.X_86_ensamblado(introdución_p,내보냄,obxectivo_VALOR); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path ferramenta_cargo = Recurso_VALOR.getParent();
            executar_ferramenta(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            executar_ferramenta(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),ferramenta_cargo.resolve("실행지원.s").toString()));
            List<String> Conectar = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (obxectivo_VALOR.equals("kernel")) Conectar.add("-r");
            else {
                executar_ferramenta(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),ferramenta_cargo.resolve(obxectivo_VALOR.equals("user") ? "START_usuario_apl.s" : "리눅스시작.s").toString()));
                Collections.addAll(Conectar,"-e","_start",임시.resolve("start.o").toString());
                if (obxectivo_VALOR.equals("user")) Collections.addAll(Conectar,"-T",ferramenta_cargo.resolve("usuario_Ligar_deseño.ld").toString());
            }
            Collections.addAll(Conectar,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); executar_ferramenta(Conectar);
            Saída = Saída.toAbsolutePath(); Files.createDirectories(Saída.getParent()); Path publicar_VALOR = Files.createTempFile(Saída.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publicar_VALOR,StandardCopyOption.REPLACE_EXISTING); Files.move(publicar_VALOR,Saída,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publicar_VALOR); }
            Files.setPosixFilePermissions(Saída,java.nio.file.attribute.PosixFilePermissions.fromString(obxectivo_VALOR.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Saída + ".s"),조립,StandardCharsets.UTF_8);
            List<String> símbolo_datos = new ArrayList<>(), datos_de_orixe = new ArrayList<>();
            for (함수참조 Material_de_referencia : CONVERTER_VALOR.함수들.keySet()) símbolo_datos.add(datos_cadea(símbolo("method",Material_de_referencia.부분들())) + ":" + datos_cadea(Material_de_referencia.propietario_VALOR + "." + Material_de_referencia.Nome + Material_de_referencia.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_Ficheiro = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Texto = new StringBuilder(); for (byte VALOR : hash_Ficheiro) Texto.append(String.format(Locale.ROOT,"%02x",VALOR & 255));
                datos_de_orixe.add(datos_cadea(입력.toAbsolutePath().toString()) + ":" + datos_cadea(Texto.toString()));
            }
            Files.writeString(Paths.get(Saída + ".json"),"{\"target\":" + datos_cadea(obxectivo_VALOR) + ",\"entry\":" + datos_cadea(introdución_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",símbolo_datos) + "},\"sources\":{" + String.join(",",datos_de_orixe) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> camiño_Lista = Files.walk(임시)) { for (Path CAMIÑO : (Iterable<Path>)camiño_Lista.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(CAMIÑO); }
        }
    }
    public static void main(String[] Argumentos) {
        try {
            String introdución_p = null, obxectivo_VALOR = "kernel", X_86_obxectivo = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> camiño_Lista = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumentos.length; 순번++) {
                String VALOR = Argumentos[순번];
                switch (VALOR) {
                    case "--target": X_86_obxectivo = Argumentos[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Clase_VALOR.FUNCIÓN_VALOR -o Saída [--target linux|kernel|user] [--profile kernel|user] [--export símbolo=Clase_VALOR.FUNCIÓN_VALOR] 클래스파일 또는 Java원문"); return;
                    case "--entry": introdución_p = Argumentos[++순번]; break;
                    case "--profile": obxectivo_VALOR = Argumentos[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumentos[++순번]); break;
                    case "--export": 내보냄.add(Argumentos[++순번]); break;
                    case "-o": 출력경로 = Paths.get(Argumentos[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALOR.startsWith("-")) throw new Tradución_erro("알 수 없는 옵션: " + VALOR); camiño_Lista.add(Paths.get(VALOR));
                }
            }
            if (introdución_p == null || 출력경로 == null || camiño_Lista.isEmpty()) throw new Tradución_erro("--entry, -o, Clase_VALOR 파일이 필요합니다");
            Path Recurso_VALOR = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_obxectivo != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_obxectivo)) throw new Tradución_erro("알 수 없는 executar_comando obxectivo_VALOR");
                X_86_Tradución(camiño_Lista,X_86_obxectivo,introdución_p,내보냄,출력경로,Recurso_VALOR); return;
            }
            String FONTE = new 기계어미리번역(camiño_Lista, obxectivo_VALOR, 낱말수, Recurso_VALOR).xerar(introdución_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, FONTE, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception ERRO) { System.err.println("compilar_fonte ERRO: " + ERRO.getMessage()); System.exit(1); }
    }
}
