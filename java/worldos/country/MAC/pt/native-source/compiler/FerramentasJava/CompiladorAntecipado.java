// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java aula_VALOR 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class CompiladorAntecipado {
    static final class Tradução_erro extends RuntimeException {
        Tradução_erro(String 설명) { super(설명); }
    }
    static final class dados_Leitor {
        final byte[] dados;
        int posição;
        dados_Leitor(byte[] entrada_dados) { dados = entrada_dados; }
        byte[] Leitura(int duração_VALOR) {
            if (duração_VALOR < 0 || duração_VALOR > dados.length - posição) throw new Tradução_erro("잘린 aula_VALOR 또는 comando dados");
            byte[] resultado = Arrays.copyOfRange(dados, posição, posição + duração_VALOR); posição += duração_VALOR; return resultado;
        }
        int leitura_byte() { if (posição >= dados.length) throw new Tradução_erro("잘린 comando dados"); return dados[posição++] & 255; }
        int 두바이트() { return (leitura_byte() << 8) | leitura_byte(); }
        int leitura_INT() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) leitura_byte(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class membro_dados {
        final int acesso_entrada;
        final String Nome, 서술;
        final Map<String, byte[]> valor_do_atributo;
        membro_dados(int acesso_VALOR, String nome_VALOR, String descritor_dados, Map<String, byte[]> atributo_dados) {
            acesso_entrada = acesso_VALOR; Nome = nome_VALOR; 서술 = descritor_dados; valor_do_atributo = atributo_dados;
        }
    }
    static final class método_Referência implements Comparable<método_Referência> {
        final String proprietário_VALOR, Nome, 서술;
        método_Referência(String 소유값, String nome_VALOR, String descritor_dados) { proprietário_VALOR = 소유값; Nome = nome_VALOR; 서술 = descritor_dados; }
        String[] 부분들() { return new String[]{proprietário_VALOR, Nome, 서술}; }
        public int compareTo(método_Referência par_VALOR) {
            int Comparação_VALOR = proprietário_VALOR.compareTo(par_VALOR.proprietário_VALOR);
            if (Comparação_VALOR == 0) Comparação_VALOR = Nome.compareTo(par_VALOR.Nome);
            return Comparação_VALOR == 0 ? 서술.compareTo(par_VALOR.서술) : Comparação_VALOR;
        }
        public boolean equals(Object par_VALOR) { return par_VALOR instanceof método_Referência && compareTo((método_Referência) par_VALOR) == 0; }
        public int hashCode() { return Objects.hash(proprietário_VALOR, Nome, 서술); }
    }
    static final class aula_dados {
        final int[] constante_Tipo;
        final Object[] constante_dados;
        final String Nome;
        final List<membro_dados> valor_do_campo, FUNÇÃO_VALOR;
        aula_dados(Path caminho) throws IOException {
            dados_Leitor Leitor_VALOR = new dados_Leitor(Files.readAllBytes(caminho));
            if (Leitor_VALOR.leitura_INT() != 0xcafebabe) throw new Tradução_erro("Java aula_VALOR 표식이 아님");
            Leitor_VALOR.Leitura(4);
            int item_CONT_NÚM = Leitor_VALOR.두바이트(); constante_Tipo = new int[item_CONT_NÚM]; constante_dados = new Object[item_CONT_NÚM];
            for (int 순번 = 1; 순번 < item_CONT_NÚM; 순번++) {
                int Tipo_VALOR = Leitor_VALOR.leitura_byte(); constante_Tipo[순번] = Tipo_VALOR;
                switch (Tipo_VALOR) {
                    case 1:
                        int duração_VALOR = Leitor_VALOR.두바이트();
                        byte[] caractere_buffer = Leitor_VALOR.Leitura(duração_VALOR), 길이붙인자료 = new byte[duração_VALOR + 2];
                        길이붙인자료[0] = (byte)(duração_VALOR >> 8); 길이붙인자료[1] = (byte)duração_VALOR;
                        System.arraycopy(caractere_buffer, 0, 길이붙인자료, 2, duração_VALOR);
                        constante_dados[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: constante_dados[순번] = Leitor_VALOR.leitura_INT(); break;
                    case 4: Leitor_VALOR.Leitura(4); break;
                    case 5: case 6: Leitor_VALOR.Leitura(8); 순번++; break;
                    case 7: case 8: case 16: constante_dados[순번] = Leitor_VALOR.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        constante_dados[순번] = new int[]{Leitor_VALOR.두바이트(), Leitor_VALOR.두바이트()}; break;
                    case 15: constante_dados[순번] = new int[]{Leitor_VALOR.leitura_byte(), Leitor_VALOR.두바이트()}; break;
                    default: throw new Tradução_erro("지원하지 않는 constante_VALOR Tipo_VALOR: " + Tipo_VALOR);
                }
            }
            Leitor_VALOR.두바이트(); Nome = nome_da_classe(Leitor_VALOR.두바이트());
            if (!nome_da_classe(Leitor_VALOR.두바이트()).equals("java/lang/Object") || Leitor_VALOR.두바이트() != 0)
                throw new Tradução_erro(Nome + ": 상속 및 인터페이스 미지원");
            valor_do_campo = 멤버읽기(Leitor_VALOR); FUNÇÃO_VALOR = 멤버읽기(Leitor_VALOR); leitura_características(Leitor_VALOR);
            if (Leitor_VALOR.posição != Leitor_VALOR.dados.length) throw new Tradução_erro("aula_VALOR 뒤에 남은 dados");
        }
        String 문자(int ÍNDICE) {
            if (ÍNDICE < 1 || ÍNDICE >= constante_Tipo.length || constante_Tipo[ÍNDICE] != 1) throw new Tradução_erro("문자 constante_VALOR ÍNDICE erro");
            return (String) constante_dados[ÍNDICE];
        }
        String nome_da_classe(int ÍNDICE) {
            if (ÍNDICE < 1 || ÍNDICE >= constante_Tipo.length || constante_Tipo[ÍNDICE] != 7) throw new Tradução_erro("aula_VALOR Referência erro");
            return 문자((Integer)constante_dados[ÍNDICE]);
        }
        método_Referência Referência(int ÍNDICE) {
            if (ÍNDICE < 1 || ÍNDICE >= constante_Tipo.length || constante_Tipo[ÍNDICE] < 9 || constante_Tipo[ÍNDICE] > 11) throw new Tradução_erro("멤버 Referência erro");
            int[] emparelhar_VALOR = (int[])constante_dados[ÍNDICE], nome_emparelhar = (int[])constante_dados[emparelhar_VALOR[1]];
            return new método_Referência(nome_da_classe(emparelhar_VALOR[0]), 문자(nome_emparelhar[0]), 문자(nome_emparelhar[1]));
        }
        Map<String, byte[]> leitura_características(dados_Leitor Leitor_VALOR) {
            Map<String, byte[]> resultado = new LinkedHashMap<>();
            int item_CONT_NÚM = Leitor_VALOR.두바이트();
            for (int 순번 = 0; 순번 < item_CONT_NÚM; 순번++) {
                String atributo_nome = 문자(Leitor_VALOR.두바이트()); byte[] VALOR = Leitor_VALOR.Leitura(Leitor_VALOR.leitura_INT());
                if (resultado.put(atributo_nome, VALOR) != null) throw new Tradução_erro("겹친 valor_do_atributo: " + atributo_nome);
            }
            return resultado;
        }
        List<membro_dados> 멤버읽기(dados_Leitor Leitor_VALOR) {
            List<membro_dados> resultado = new ArrayList<>(); int item_CONT_NÚM = Leitor_VALOR.두바이트();
            for (int 순번 = 0; 순번 < item_CONT_NÚM; 순번++) {
                int acesso_entrada = Leitor_VALOR.두바이트(); String método_entrada_nome = 문자(Leitor_VALOR.두바이트()), 서술 = 문자(Leitor_VALOR.두바이트());
                resultado.add(new membro_dados(acesso_entrada, método_entrada_nome, 서술, leitura_características(Leitor_VALOR)));
            }
            return resultado;
        }
    }
    static final class método_descritor {
        final List<String> argumentos = new ArrayList<>();
        final String devolver_RC;
        método_descritor(String 서술) {
            if (!서술.startsWith("(")) throw new Tradução_erro("FUNÇÃO_VALOR 서술 erro: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Tradução_erro("FUNÇÃO_VALOR 서술 erro: " + 서술);
            argumentos.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (argumentos.contains("V") || 반환들.size() != 1) throw new Tradução_erro("FUNÇÃO_VALOR 서술 erro: " + 서술);
            devolver_RC = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> resultado = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int posição = 0; posição < 서술.length();) {
            String seleção_VALOR = null;
            for (String formato_VALOR : 허용형식) if (서술.startsWith(formato_VALOR, posição)) { seleção_VALOR = formato_VALOR; break; }
            if (seleção_VALOR == null) throw new Tradução_erro("지원하지 않는 tipo_de_dados: " + 서술);
            resultado.add(seleção_VALOR); posição += seleção_VALOR.length();
        }
        return resultado;
    }
    static String símbolo(String Tipo_VALOR, String... 부분들) {
        try {
            byte[] hash_Arquivo = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder texto = new StringBuilder("j_" + Tipo_VALOR + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) texto.append(String.format(Locale.ROOT, "%02x", hash_Arquivo[순번] & 255));
            return texto.toString();
        } catch (Exception erro) { throw new Tradução_erro(erro.toString()); }
    }
    final Map<String, aula_dados> 클래스들 = new TreeMap<>();
    final Map<método_Referência, membro_dados> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), computador_Functions = new LinkedHashMap<>();
    final String execução_alvo, computador_aula;
    final int heap_Contagem_de_Palavras;
    final Path recurso_caminho;
    CompiladorAntecipado(List<Path> caminho_Lista, String meta, int 낱말수, Path recurso_VALOR) throws IOException {
        if ((!meta.equals("kernel") && !meta.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Tradução_erro("Executar_comando meta 또는 Memória_VALOR email_região Tamanho erro");
        execução_alvo = meta; heap_Contagem_de_Palavras = 낱말수; recurso_caminho = recurso_VALOR;
        // 이 이름도 국가별 fonte_árvore gerar 시 해당 언어로 옮긴다.
        computador_aula = meta.equals("kernel") ? "Quadro" : "espaço_do_utilizador";
        for (String linha_de_entrada : Files.readAllLines(recurso_VALOR.resolve("FunçõesMáquina.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = linha_de_entrada.split("\t", -1);
            if (부분들.length != 4) throw new Tradução_erro("computador FUNÇÃO_VALOR dados erro");
            if (부분들[0].equals(meta)) computador_Functions.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path caminho : caminho_Lista) {
            aula_dados dados = new aula_dados(caminho);
            if (클래스들.put(dados.Nome, dados) != null) throw new Tradução_erro("중복 aula_VALOR: " + dados.Nome);
            for (membro_dados valor_do_campo : dados.valor_do_campo) {
                if ((valor_do_campo.acesso_entrada & 8) == 0 || 형식읽기(valor_do_campo.서술).equals(Collections.singletonList("V"))) throw new Tradução_erro("estático_VALOR 필드만 Suporte_VALOR");
                if (필드들.put(new método_Referência(dados.Nome, valor_do_campo.Nome, valor_do_campo.서술), valor_do_campo) != null) throw new Tradução_erro("중복 valor_do_campo");
            }
            for (membro_dados FUNÇÃO_VALOR : dados.FUNÇÃO_VALOR) {
                if (FUNÇÃO_VALOR.Nome.equals("<init>")) continue;
                if ((FUNÇÃO_VALOR.acesso_entrada & 8) == 0 || (FUNÇÃO_VALOR.acesso_entrada & (0x20 | 0x400)) != 0) throw new Tradução_erro("estático_VALOR 비동기화 함수만 Suporte_VALOR");
                new método_descritor(FUNÇÃO_VALOR.서술);
                if (함수들.put(new método_Referência(dados.Nome, FUNÇÃO_VALOR.Nome, FUNÇÃO_VALOR.서술), FUNÇÃO_VALOR) != null) throw new Tradução_erro("중복 FUNÇÃO_VALOR");
            }
        }
    }
    String cadeia_símbolo(String texto) { return 문자열들.computeIfAbsent(texto, VALOR -> "j_text_" + 문자열들.size()); }
    String expressão_de_constante(aula_dados dados, int ÍNDICE) {
        if (ÍNDICE < 1 || ÍNDICE >= dados.constante_Tipo.length) throw new Tradução_erro("constante_VALOR ÍNDICE recortar erro");
        if (dados.constante_Tipo[ÍNDICE] == 3) return "(word)(uint32_t)(" + dados.constante_dados[ÍNDICE] + ")";
        if (dados.constante_Tipo[ÍNDICE] == 8) return "(word)" + cadeia_símbolo(dados.문자((Integer)dados.constante_dados[ÍNDICE]));
        throw new Tradução_erro("정수와 cadeia_VALOR 상수만 Suporte_VALOR");
    }
    String método_protótipo(método_Referência Referência) {
        List<String> 인수들 = new ArrayList<>(); int item_CONT_NÚM = new método_descritor(Referência.서술).argumentos.size();
        for (int 순번 = 0; 순번 < item_CONT_NÚM; 순번++) 인수들.add("word a" + 순번);
        return "static word " + símbolo("method", Referência.부분들()) + "(" + (item_CONT_NÚM == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void cheque_local(int ÍNDICE, int variável_local_CONT_NÚM) { if (ÍNDICE < 0 || ÍNDICE >= variável_local_CONT_NÚM) throw new Tradução_erro("local_Scope variável_VALOR ÍNDICE recortar erro"); }
    void 분기넣기(List<String> saídaTexto, Set<Integer> branch_Lista, int posição, int 이동량, String doença) {
        int destino_VALOR = posição + 이동량; branch_Lista.add(destino_VALOR);
        saídaTexto.add((doença == null ? "" : "if (" + doença + ") ") + "goto b" + destino_VALOR + ";");
    }
    String corpo_do_método(método_Referência FUNÇÃO_VALOR, membro_dados dados) {
        byte[] corpo_dados = dados.valor_do_atributo.get("Code"); if (corpo_dados == null) throw new Tradução_erro("FUNÇÃO_VALOR 몸체가 없음: " + FUNÇÃO_VALOR.Nome);
        dados_Leitor Leitor_VALOR = new dados_Leitor(corpo_dados); int 쌓임깊이 = Leitor_VALOR.두바이트(), variável_local_CONT_NÚM = Leitor_VALOR.두바이트();
        dados_Leitor comando_dados = new dados_Leitor(Leitor_VALOR.Leitura(Leitor_VALOR.leitura_INT()));
        if (Leitor_VALOR.두바이트() != 0) throw new Tradução_erro("try/catch/finally 미지원");
        método_descritor formato_VALOR = new método_descritor(FUNÇÃO_VALOR.서술); if (variável_local_CONT_NÚM < formato_VALOR.argumentos.size()) throw new Tradução_erro("매개변수보다 적은 local_Scope variável_VALOR");
        aula_dados aula_VALOR = 클래스들.get(FUNÇÃO_VALOR.proprietário_VALOR);
        List<String> saídaTexto = new ArrayList<>(); saídaTexto.add(método_protótipo(FUNÇÃO_VALOR) + " {");
        saídaTexto.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(variável_local_CONT_NÚM, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formato_VALOR.argumentos.size(); 순번++) saídaTexto.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), branch_Lista = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (comando_dados.posição < comando_dados.dados.length) {
            int posição = comando_dados.posição, comando = comando_dados.leitura_byte(); 경계들.add(posição); saídaTexto.add("b" + posição + ":;");
            if (comando == 0) continue;
            if (comando == 1) saídaTexto.add("PUSH(0);");
            else if (comando >= 2 && comando <= 8) saídaTexto.add("PUSH((uint32_t)(" + (comando - 3) + "));");
            else if (comando == 16 || comando == 17) saídaTexto.add("PUSH((uint32_t)(" + (comando == 16 ? comando_dados.부호한바이트() : comando_dados.부호두바이트()) + "));");
            else if (comando == 18 || comando == 19) saídaTexto.add("PUSH(" + expressão_de_constante(aula_VALOR, comando == 18 ? comando_dados.leitura_byte() : comando_dados.두바이트()) + ");");
            else if (comando == 21 || comando == 25 || (comando >= 26 && comando <= 29) || (comando >= 42 && comando <= 45)) {
                int ÍNDICE = comando == 21 || comando == 25 ? comando_dados.leitura_byte() : comando - (comando <= 29 ? 26 : 42);
                cheque_local(ÍNDICE, variável_local_CONT_NÚM); saídaTexto.add("PUSH(l[" + ÍNDICE + "]);");
            } else if (comando == 54 || comando == 58 || (comando >= 59 && comando <= 62) || (comando >= 75 && comando <= 78)) {
                int ÍNDICE = comando == 54 || comando == 58 ? comando_dados.leitura_byte() : comando - (comando <= 62 ? 59 : 75);
                cheque_local(ÍNDICE, variável_local_CONT_NÚM); saídaTexto.add("l[" + ÍNDICE + "] = POP();");
            } else if (comando == 46) saídaTexto.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (comando == 79) saídaTexto.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (comando == 87 || comando == 88) saídaTexto.add(comando == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (comando >= 89 && comando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ordem_Lista = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[comando - 89]; 순번++) saídaTexto.add("abcd".charAt(순번) + " = POP();");
                for (char VALOR : ordem_Lista[comando - 89].toCharArray()) saídaTexto.add("PUSH(" + VALOR + ");");
            } else if (comando == 96 || comando == 100 || comando == 104 || comando == 126 || comando == 128 || comando == 130) {
                String cirurgia_VALOR = comando == 96 ? "+" : comando == 100 ? "-" : comando == 104 ? "*" : comando == 126 ? "&" : comando == 128 ? "|" : "^";
                saídaTexto.add("b = POP(); a = POP(); PUSH((uint32_t)a " + cirurgia_VALOR + " (uint32_t)b);");
            } else if (comando == 108 || comando == 112) saídaTexto.add("b = POP(); a = POP(); PUSH(divide(a,b," + (comando == 112 ? 1 : 0) + "));");
            else if (comando == 116) saídaTexto.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (comando == 120 || comando == 122 || comando == 124) {
                saídaTexto.add("b = POP(); a = POP();"); saídaTexto.add("PUSH(" + (comando == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (comando == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (comando == 132) {
                int ÍNDICE = comando_dados.leitura_byte(), incremento_valor = comando_dados.부호한바이트(); cheque_local(ÍNDICE, variável_local_CONT_NÚM);
                saídaTexto.add("l[" + ÍNDICE + "] = (uint32_t)l[" + ÍNDICE + "] + (uint32_t)(" + incremento_valor + ");");
            } else if (comando >= 145 && comando <= 147) saídaTexto.add("a = POP(); PUSH((uint32_t)(" + (comando == 145 ? "int8_t" : comando == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (comando >= 153 && comando <= 158) {
                saídaTexto.add("a = POP();"); 분기넣기(saídaTexto, branch_Lista, posição, comando_dados.부호두바이트(), "(int32_t)a " + 비교들[comando - 153] + " 0");
            } else if (comando >= 159 && comando <= 166) {
                saídaTexto.add("b = POP(); a = POP();"); 분기넣기(saídaTexto, branch_Lista, posição, comando_dados.부호두바이트(), comando >= 165 ? "a " + 비교들[comando - 159] + " b" : "(int32_t)a " + 비교들[comando - 159] + " (int32_t)b");
            } else if (comando == 167 || comando == 200) 분기넣기(saídaTexto, branch_Lista, posição, comando == 167 ? comando_dados.부호두바이트() : comando_dados.leitura_INT(), null);
            else if (comando == 170 || comando == 171) {
                while (comando_dados.posição % 4 != 0) comando_dados.leitura_byte();
                int valor_padrão = comando_dados.leitura_INT(); saídaTexto.add("a = POP();");
                if (comando == 170) {
                    int 아래 = comando_dados.leitura_INT(), 위 = comando_dados.leitura_INT(); long item_CONT_NÚM = (long)위 - 아래 + 1;
                    if (item_CONT_NÚM < 1 || item_CONT_NÚM > (comando_dados.dados.length - comando_dados.posição) / 4) throw new Tradução_erro("switch recortar erro");
                    for (long VALOR = 아래; VALOR <= 위; VALOR++) 분기넣기(saídaTexto, branch_Lista, posição, comando_dados.leitura_INT(), "(int32_t)a == (" + VALOR + ")");
                } else {
                    int item_CONT_NÚM = comando_dados.leitura_INT(), câmera_frontal_dados = 0;
                    if (item_CONT_NÚM < 0 || item_CONT_NÚM > (comando_dados.dados.length - comando_dados.posição) / 8) throw new Tradução_erro("switch Tamanho erro");
                    for (int 순번 = 0; 순번 < item_CONT_NÚM; 순번++) {
                        int VALOR = comando_dados.leitura_INT(); if (순번 > 0 && VALOR <= câmera_frontal_dados) throw new Tradução_erro("switch ordem_VALOR erro"); câmera_frontal_dados = VALOR;
                        분기넣기(saídaTexto, branch_Lista, posição, comando_dados.leitura_INT(), "(int32_t)a == (" + VALOR + ")");
                    }
                }
                분기넣기(saídaTexto, branch_Lista, posição, valor_padrão, null);
            } else if (comando == 172 || comando == 176 || comando == 177) saídaTexto.add("return " + (comando == 177 ? "0" : "POP()") + ";");
            else if (comando == 178 || comando == 179) {
                método_Referência Referência = aula_VALOR.Referência(comando_dados.두바이트()); if (!필드들.containsKey(Referência)) throw new Tradução_erro("알 número 없는 valor_do_campo");
                saídaTexto.add(símbolo("init", Referência.proprietário_VALOR) + "();"); String valor_do_campo = símbolo("field", Referência.부분들());
                saídaTexto.add(comando == 178 ? "PUSH(" + valor_do_campo + ");" : valor_do_campo + " = POP();");
            } else if (comando == 184) {
                método_Referência Referência = aula_VALOR.Referência(comando_dados.두바이트()); if (!함수들.containsKey(Referência)) throw new Tradução_erro("알 número 없는 FUNÇÃO_VALOR");
                método_descritor 호출형식 = new método_descritor(Referência.서술); int item_CONT_NÚM = 호출형식.argumentos.size();
                saídaTexto.add(símbolo("init", Referência.proprietário_VALOR) + "();"); saídaTexto.add("if(sp < " + item_CONT_NÚM + ") kernel_panic(\"call stack underflow\"); sp -= " + item_CONT_NÚM + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < item_CONT_NÚM; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                saídaTexto.add("a = " + símbolo("method", Referência.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.devolver_RC.equals("V")) saídaTexto.add("PUSH(a);");
            } else if (comando == 182) {
                método_Referência Referência = aula_VALOR.Referência(comando_dados.두바이트());
                if (Referência.equals(new método_Referência("java/lang/String", "length", "()I"))) saídaTexto.add("a = POP(); PUSH(length(a));");
                else if (Referência.equals(new método_Referência("java/lang/String", "charAt", "(I)C"))) saídaTexto.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Tradução_erro("가상 FUNÇÃO_VALOR 호출 미지원");
            } else if (comando == 188) {
                if (comando_dados.leitura_byte() != 10) throw new Tradução_erro("new int[]만 Suporte_VALOR"); saídaTexto.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (comando == 190) saídaTexto.add("a = POP(); PUSH(length(a));");
            else if (comando == 196) {
                int extensão_VALOR = comando_dados.leitura_byte(), ÍNDICE = comando_dados.두바이트(); cheque_local(ÍNDICE, variável_local_CONT_NÚM);
                if (extensão_VALOR == 21 || extensão_VALOR == 25) saídaTexto.add("PUSH(l[" + ÍNDICE + "]);");
                else if (extensão_VALOR == 54 || extensão_VALOR == 58) saídaTexto.add("l[" + ÍNDICE + "] = POP();");
                else if (extensão_VALOR == 132) saídaTexto.add("l[" + ÍNDICE + "] = (uint32_t)l[" + ÍNDICE + "] + (uint32_t)(" + comando_dados.부호두바이트() + ");");
                else throw new Tradução_erro("미지원 wide comando");
            } else if (comando == 198 || comando == 199) {
                saídaTexto.add("a = POP();"); 분기넣기(saídaTexto, branch_Lista, posição, comando_dados.부호두바이트(), "a " + (comando == 198 ? "==" : "!=") + " 0");
            } else throw new Tradução_erro(FUNÇÃO_VALOR.proprietário_VALOR + "." + FUNÇÃO_VALOR.Nome + ", byte_VALOR " + posição + ": 미지원 comando " + comando);
        }
        if (!경계들.containsAll(branch_Lista)) throw new Tradução_erro("comando 경계가 아닌 곳으로 branch");
        saídaTexto.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", saídaTexto);
    }
    String exportar_método(String Link_símbolo, String meta, boolean 진입점여부) {
        int cargo_ÍNDICE = meta.lastIndexOf('.'); if (cargo_ÍNDICE < 0 || !Link_símbolo.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tradução_erro("내보내기 ceder_VALOR erro");
        String proprietário_VALOR = meta.substring(0, cargo_ÍNDICE).replace('.', '/'), Nome = meta.substring(cargo_ÍNDICE + 1); método_Referência seleção_VALOR = null;
        for (método_Referência Referência : 함수들.keySet()) if (Referência.proprietário_VALOR.equals(proprietário_VALOR) && Referência.Nome.equals(Nome)) {
            if (seleção_VALOR != null) throw new Tradução_erro("겹친 내보내기 meta"); seleção_VALOR = Referência;
        }
        if (seleção_VALOR == null || (함수들.get(seleção_VALOR).acesso_entrada & 0x100) != 0) throw new Tradução_erro("내보낼 함수가 없음 또는 native FUNÇÃO_VALOR");
        método_descritor formato_VALOR = new método_descritor(seleção_VALOR.서술);
        if ((진입점여부 && !formato_VALOR.argumentos.isEmpty()) || !Arrays.asList("V", "I").contains(formato_VALOR.devolver_RC)) throw new Tradução_erro("ponto_de_entrada_VALOR 또는 C limite_VALOR formato_VALOR erro");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formato_VALOR.argumentos.size(); 순번++) {
            if (!formato_VALOR.argumentos.get(순번).equals("I")) throw new Tradução_erro("C 경계는 int 인수만 Suporte_VALOR");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formato_VALOR.devolver_RC.equals("V") ? "void " : "int32_t ") + Link_símbolo + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + símbolo("init", seleção_VALOR.proprietário_VALOR) + "(); " + (formato_VALOR.devolver_RC.equals("V") ? "" : "return (int32_t)") + símbolo("method", seleção_VALOR.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String gerar(String ponto_de_entrada, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<método_Referência, membro_dados> entrada_VALOR_962f286b : 함수들.entrySet()) {
            método_Referência Referência = entrada_VALOR_962f286b.getKey(); membro_dados dados = entrada_VALOR_962f286b.getValue(); 선언들.add(método_protótipo(Referência) + ";");
            if ((dados.acesso_entrada & 0x100) != 0) {
                String Ligar = computador_Functions.get(Referência.Nome + Referência.서술);
                if (!Referência.proprietário_VALOR.equals(computador_aula) || Ligar == null) throw new Tradução_erro("허용되지 않은 native FUNÇÃO_VALOR: " + Referência.Nome);
                int item_CONT_NÚM = new método_descritor(Referência.서술).argumentos.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < item_CONT_NÚM; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Ligar + "(" + (item_CONT_NÚM == 0 ? "void" : String.join(",", Collections.nCopies(item_CONT_NÚM, "word"))) + ");");
                몸체들.add(método_protótipo(Referência) + " { return " + Ligar + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(corpo_do_método(Referência, dados));
        }
        for (Map.Entry<método_Referência, membro_dados> entrada_VALOR_962f286b : 필드들.entrySet()) {
            método_Referência Referência = entrada_VALOR_962f286b.getKey(); byte[] constante_VALOR = entrada_VALOR_962f286b.getValue().valor_do_atributo.get("ConstantValue");
            String VALOR = constante_VALOR == null ? "0" : expressão_de_constante(클래스들.get(Referência.proprietário_VALOR), new dados_Leitor(constante_VALOR).두바이트());
            필드선언들.add("static word " + símbolo("field", Referência.부분들()) + " = " + VALOR + ";");
        }
        for (String Nome : 클래스들.keySet()) {
            String inicializar = símbolo("init", Nome), Estado_VALOR = símbolo("state", Nome);
            선언들.add("static void " + inicializar + "(void);"); 필드선언들.add("static unsigned " + Estado_VALOR + ";");
            método_Referência Referência = new método_Referência(Nome, "<clinit>", "()V");
            몸체들.add("static void " + inicializar + "(void) { if(" + Estado_VALOR + ") return; " + Estado_VALOR + " = 1; " + (함수들.containsKey(Referência) ? símbolo("method", Referência.부분들()) + "(); " : "") + Estado_VALOR + " = 2; }");
        }
        몸체들.add(exportar_método("java_entry", ponto_de_entrada, true)); Set<String> 공개이름 = new HashSet<>();
        for (String ceder_VALOR : 내보내기목록) {
            int cargo_ÍNDICE = ceder_VALOR.indexOf('='); if (cargo_ÍNDICE < 1) throw new Tradução_erro("내보내기 ceder_VALOR erro");
            String Nome = ceder_VALOR.substring(0, cargo_ÍNDICE); 공개이름.add(Nome); 몸체들.add(exportar_método(Nome, ceder_VALOR.substring(cargo_ÍNDICE + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> entrada_VALOR_962f286b : 문자열들.entrySet()) {
            String texto = entrada_VALOR_962f286b.getKey(); StringBuilder MATRIZ_VALOR = new StringBuilder("static const word " + entrada_VALOR_962f286b.getValue() + "[] = {" + texto.length());
            for (int 순번 = 0; 순번 < texto.length(); 순번++) MATRIZ_VALOR.append(", ").append((int)texto.charAt(순번));
            문자열선언들.add(MATRIZ_VALOR.append("};").toString());
        }
        String Suporte_VALOR = Files.readString(recurso_caminho.resolve("SuporteExecução.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(heap_Contagem_de_Palavras));
        return 기계원문한국어화(Suporte_VALOR + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String códigoFonte, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nome_tabela = new HashMap<>();
        for (String linha_de_entrada : Files.readAllLines(recurso_caminho.resolve("NomesGerados.tsv"), StandardCharsets.UTF_8)) {
            String[] emparelhar_VALOR = linha_de_entrada.split("\t"); nome_tabela.put(emparelhar_VALOR[0], emparelhar_VALOR[1]);
        }
        Pattern parte_expressão = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = parte_expressão.matcher(códigoFonte); StringBuffer resultado = new StringBuffer();
        while (찾개.find()) {
            String Nome = 찾개.group(), 새이름 = Nome;
            if (!Nome.startsWith("//") && !Nome.startsWith("/*") && !Nome.startsWith("\"") && !Nome.startsWith("'") && !공개이름.contains(Nome)) {
                새이름 = nome_tabela.getOrDefault(Nome, Nome);
                if (Nome.matches("a[0-9]+")) 새이름 = "argumentos" + Nome.substring(1);
                if (Nome.matches("b[0-9]+")) 새이름 = "branch" + Nome.substring(1);
                if (범용표기) {
                    StringBuilder notação_VALOR = new StringBuilder();
                    for (char caractere_VALOR : 새이름.toCharArray()) notação_VALOR.append(caractere_VALOR < 128 ? Character.toString(caractere_VALOR) : String.format(Locale.ROOT, "\\u%04x", (int)caractere_VALOR));
                    새이름 = notação_VALOR.toString();
                }
            }
            찾개.appendReplacement(resultado, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(resultado); return resultado.toString();
    }
    String X_86_corpo_do_método(método_Referência FUNÇÃO_VALOR, membro_dados dados, Map<String,String> computador_tabela, String meta) {
        String favorito_VALOR = símbolo("method", FUNÇÃO_VALOR.부분들());
        List<String> linha_de_entrada = new ArrayList<>();
        if ((dados.acesso_entrada & 0x100) != 0) {
            String Ligar = computador_tabela.get(FUNÇÃO_VALOR.Nome + FUNÇÃO_VALOR.서술);
            if (!FUNÇÃO_VALOR.proprietário_VALOR.equals(meta.equals("kernel") ? "celular_VALOR" : "espaço_do_utilizador") || Ligar == null) throw new Tradução_erro("허용되지 않은 native FUNÇÃO_VALOR");
            return ".text\n" + favorito_VALOR + ":\njmp " + Ligar;
        }
        byte[] corpo_de_texto = dados.valor_do_atributo.get("Code"); if (corpo_de_texto == null) throw new Tradução_erro("FUNÇÃO_VALOR 몸체가 없음");
        dados_Leitor Leitor_VALOR = new dados_Leitor(corpo_de_texto); Leitor_VALOR.두바이트(); int local_CONT_NÚM = Leitor_VALOR.두바이트();
        dados_Leitor comando_dados = new dados_Leitor(Leitor_VALOR.Leitura(Leitor_VALOR.leitura_INT()));
        if (Leitor_VALOR.두바이트() != 0) throw new Tradução_erro("try/catch/finally 미지원");
        método_descritor formato_VALOR = new método_descritor(FUNÇÃO_VALOR.서술); if (local_CONT_NÚM < formato_VALOR.argumentos.size()) throw new Tradução_erro("매개변수보다 적은 local_Scope variável_VALOR");
        Collections.addAll(linha_de_entrada,".text",".globl " + favorito_VALOR,".type " + favorito_VALOR + ", @function",favorito_VALOR + ":","pushl %ebp","movl %esp, %ebp","subl $" + local_CONT_NÚM * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formato_VALOR.argumentos.size(); 순번++) Collections.addAll(linha_de_entrada,"movl " + (8 + 4 * (formato_VALOR.argumentos.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        aula_dados aula_VALOR = 클래스들.get(FUNÇÃO_VALOR.proprietário_VALOR); Set<Integer> 경계들 = new HashSet<>(), branch_Lista = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (comando_dados.posição < comando_dados.dados.length) {
            int posição = comando_dados.posição, comando = comando_dados.leitura_byte(); String cargo_ÍNDICE = favorito_VALOR + "_b" + posição;
            linha_de_entrada.add(cargo_ÍNDICE + ":"); 경계들.add(posição);
            if (comando == 0) linha_de_entrada.add("nop");
            else if (comando == 1) linha_de_entrada.add("pushl $0");
            else if (comando >= 2 && comando <= 8) linha_de_entrada.add("pushl $" + (comando - 3));
            else if (comando == 16 || comando == 17) linha_de_entrada.add("pushl $" + (comando == 16 ? comando_dados.부호한바이트() : comando_dados.부호두바이트()));
            else if (comando == 18 || comando == 19) {
                int ÍNDICE = comando == 18 ? comando_dados.leitura_byte() : comando_dados.두바이트();
                linha_de_entrada.add("pushl $" + X_86_constante(aula_VALOR,ÍNDICE));
            } else if (comando == 21 || comando == 25 || (comando >= 26 && comando <= 29) || (comando >= 42 && comando <= 45) || comando == 54 || comando == 58 || (comando >= 59 && comando <= 62) || (comando >= 75 && comando <= 78)) {
                boolean leitura_RC = comando < 54; int ÍNDICE = comando == 21 || comando == 25 || comando == 54 || comando == 58 ? comando_dados.leitura_byte() : comando - (comando <= 29 ? 26 : comando <= 45 ? 42 : comando <= 62 ? 59 : 75);
                cheque_local(ÍNDICE,local_CONT_NÚM); linha_de_entrada.add((leitura_RC ? "pushl " : "popl ") + "-" + (4 * (ÍNDICE + 1)) + "(%ebp)");
            } else if (comando == 46) Collections.addAll(linha_de_entrada,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (comando == 79) Collections.addAll(linha_de_entrada,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (comando == 87 || comando == 88) linha_de_entrada.add("addl $" + (comando == 87 ? 4 : 8) + ", %esp");
            else if (comando >= 89 && comando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ordem_Lista = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[comando - 89]; 순번++) linha_de_entrada.add("popl " + 저장기들[순번]);
                for (int 순번 : ordem_Lista[comando - 89]) linha_de_entrada.add("pushl " + 저장기들[순번]);
            } else if (comando == 96 || comando == 100 || comando == 104 || comando == 126 || comando == 128 || comando == 130) {
                String cirurgia_VALOR = comando == 96 ? "addl" : comando == 100 ? "subl" : comando == 104 ? "imull" : comando == 126 ? "andl" : comando == 128 ? "orl" : "xorl";
                Collections.addAll(linha_de_entrada,"popl %ecx","popl %eax",cirurgia_VALOR + " %ecx, %eax","pushl %eax");
            } else if (comando == 108 || comando == 112) Collections.addAll(linha_de_entrada,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + cargo_ÍNDICE + "_divide","cmpl $0x80000000, %eax","jne " + cargo_ÍNDICE + "_divide","xorl %edx, %edx","jmp " + cargo_ÍNDICE + "_done",cargo_ÍNDICE + "_divide:","cltd","idivl %ecx",cargo_ÍNDICE + "_done:","pushl " + (comando == 108 ? "%eax" : "%edx"));
            else if (comando == 116) linha_de_entrada.add("negl (%esp)");
            else if (comando == 120 || comando == 122 || comando == 124) Collections.addAll(linha_de_entrada,"popl %ecx","popl %eax",(comando == 120 ? "sall" : comando == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (comando == 132) {
                int ÍNDICE = comando_dados.leitura_byte(), incremento_VALOR = comando_dados.부호한바이트(); cheque_local(ÍNDICE,local_CONT_NÚM); linha_de_entrada.add("addl $" + incremento_VALOR + ", -" + (4 * (ÍNDICE + 1)) + "(%ebp)");
            } else if (comando >= 145 && comando <= 147) Collections.addAll(linha_de_entrada,"popl %eax",comando == 145 ? "movsbl %al, %eax" : comando == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (comando >= 153 && comando <= 166) {
                if (comando <= 158) Collections.addAll(linha_de_entrada,"popl %eax","testl %eax, %eax");
                else Collections.addAll(linha_de_entrada,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int destino_VALOR = posição + comando_dados.부호두바이트(); branch_Lista.add(destino_VALOR); linha_de_entrada.add(비교들[comando - (comando <= 158 ? 153 : 159)] + " " + favorito_VALOR + "_b" + destino_VALOR);
            } else if (comando == 167 || comando == 200) {
                int destino_VALOR = posição + (comando == 167 ? comando_dados.부호두바이트() : comando_dados.leitura_INT()); branch_Lista.add(destino_VALOR); linha_de_entrada.add("jmp " + favorito_VALOR + "_b" + destino_VALOR);
            } else if (comando == 170 || comando == 171) {
                while (comando_dados.posição % 4 != 0) comando_dados.leitura_byte();
                int valor_padrão = posição + comando_dados.leitura_INT(); branch_Lista.add(valor_padrão); linha_de_entrada.add("popl %eax");
                int item_CONT_NÚM, 아래 = 0;
                if (comando == 170) { 아래 = comando_dados.leitura_INT(); int 위 = comando_dados.leitura_INT(); long duração_VALOR = (long)위 - 아래 + 1; if (duração_VALOR < 1 || duração_VALOR > (comando_dados.dados.length - comando_dados.posição) / 4) throw new Tradução_erro("switch recortar erro"); item_CONT_NÚM = (int)duração_VALOR; }
                else { item_CONT_NÚM = comando_dados.leitura_INT(); if (item_CONT_NÚM < 0 || item_CONT_NÚM > (comando_dados.dados.length - comando_dados.posição) / 8) throw new Tradução_erro("switch Tamanho erro"); }
                for (int 순번 = 0; 순번 < item_CONT_NÚM; 순번++) {
                    int VALOR = comando == 170 ? 아래 + 순번 : comando_dados.leitura_INT(), destino_VALOR = posição + comando_dados.leitura_INT(); branch_Lista.add(destino_VALOR);
                    Collections.addAll(linha_de_entrada,"cmpl $" + VALOR + ", %eax","je " + favorito_VALOR + "_b" + destino_VALOR);
                }
                linha_de_entrada.add("jmp " + favorito_VALOR + "_b" + valor_padrão);
            } else if (comando == 172 || comando == 176 || comando == 177) {
                if (comando != 177) linha_de_entrada.add("popl %eax"); Collections.addAll(linha_de_entrada,"leave","ret");
            } else if (comando == 178 || comando == 179) {
                método_Referência Referência = aula_VALOR.Referência(comando_dados.두바이트()); if (!필드들.containsKey(Referência)) throw new Tradução_erro("알 número 없는 valor_do_campo");
                Collections.addAll(linha_de_entrada,"call " + símbolo("init",Referência.proprietário_VALOR),(comando == 178 ? "pushl " : "popl ") + símbolo("field",Referência.부분들()));
            } else if (comando == 184) {
                método_Referência Referência = aula_VALOR.Referência(comando_dados.두바이트()); if (!함수들.containsKey(Referência)) throw new Tradução_erro("알 número 없는 FUNÇÃO_VALOR");
                método_descritor 호출형식 = new método_descritor(Referência.서술); Collections.addAll(linha_de_entrada,"call " + símbolo("init",Referência.proprietário_VALOR),"call " + símbolo("method",Referência.부분들()));
                if (!호출형식.argumentos.isEmpty()) linha_de_entrada.add("addl $" + 호출형식.argumentos.size() * 4 + ", %esp");
                if (!호출형식.devolver_RC.equals("V")) linha_de_entrada.add("pushl %eax");
            } else if (comando == 182) {
                método_Referência Referência = aula_VALOR.Referência(comando_dados.두바이트());
                if (Referência.equals(new método_Referência("java/lang/String","length","()I"))) Collections.addAll(linha_de_entrada,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Referência.equals(new método_Referência("java/lang/String","charAt","(I)C"))) Collections.addAll(linha_de_entrada,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Tradução_erro("가상 FUNÇÃO_VALOR 호출 미지원");
            } else if (comando == 188) {
                if (comando_dados.leitura_byte() != 10) throw new Tradução_erro("new int[]만 Suporte_VALOR"); Collections.addAll(linha_de_entrada,"popl %eax","call rt_new_array","pushl %eax");
            } else if (comando == 190) Collections.addAll(linha_de_entrada,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (comando == 196) {
                int extensão_VALOR = comando_dados.leitura_byte(), ÍNDICE = comando_dados.두바이트(); cheque_local(ÍNDICE,local_CONT_NÚM);
                if (extensão_VALOR == 21 || extensão_VALOR == 25 || extensão_VALOR == 54 || extensão_VALOR == 58) linha_de_entrada.add((extensão_VALOR <= 25 ? "pushl " : "popl ") + "-" + 4 * (ÍNDICE + 1) + "(%ebp)");
                else if (extensão_VALOR == 132) linha_de_entrada.add("addl $" + comando_dados.부호두바이트() + ", -" + 4 * (ÍNDICE + 1) + "(%ebp)");
                else throw new Tradução_erro("wide comando 미지원");
            } else if (comando == 198 || comando == 199) {
                int destino_VALOR = posição + comando_dados.부호두바이트(); branch_Lista.add(destino_VALOR); Collections.addAll(linha_de_entrada,"popl %eax","testl %eax, %eax",(comando == 198 ? "je " : "jne ") + favorito_VALOR + "_b" + destino_VALOR);
            } else throw new Tradução_erro("미지원 comando: " + comando);
        }
        if (!경계들.containsAll(branch_Lista)) throw new Tradução_erro("comando 경계가 아닌 곳으로 branch");
        linha_de_entrada.add(".size " + favorito_VALOR + ", .-" + favorito_VALOR); return String.join("\n",linha_de_entrada);
    }
    String X_86_constante(aula_dados dados, int ÍNDICE) {
        if (dados.constante_Tipo[ÍNDICE] == 3) return dados.constante_dados[ÍNDICE].toString();
        if (dados.constante_Tipo[ÍNDICE] == 8) return cadeia_símbolo(dados.문자((Integer)dados.constante_dados[ÍNDICE]));
        throw new Tradução_erro("정수와 cadeia_VALOR 상수만 Suporte_VALOR");
    }
    String X_86_assembly(String ponto_de_entrada, List<String> 내보냄, String meta) throws IOException {
        Map<String,String> computador_tabela = new HashMap<>();
        for (String linha_de_entrada : Files.readAllLines(recurso_caminho.resolve("_86_computador_Functions.tsv"))) { String[] emparelhar_VALOR = linha_de_entrada.split("\t"); if (emparelhar_VALOR[0].equals(meta)) computador_tabela.put(emparelhar_VALOR[1] + emparelhar_VALOR[2],emparelhar_VALOR[3]); }
        int cargo_ÍNDICE = ponto_de_entrada.lastIndexOf('.'); if (cargo_ÍNDICE < 0) throw new Tradução_erro("ponto_de_entrada ceder_VALOR erro");
        String proprietário_VALOR = ponto_de_entrada.substring(0,cargo_ÍNDICE).replace('.','/'), método_entrada_nome = ponto_de_entrada.substring(cargo_ÍNDICE + 1); método_Referência ponto_de_entrada_VALOR = null;
        for (String 서술 : Arrays.asList("()I","()V")) { método_Referência Referência = new método_Referência(proprietário_VALOR,método_entrada_nome,서술); if (함수들.containsKey(Referência)) { if (ponto_de_entrada_VALOR != null) throw new Tradução_erro("겹친 ponto_de_entrada"); ponto_de_entrada_VALOR = Referência; } }
        if (ponto_de_entrada_VALOR == null || (함수들.get(ponto_de_entrada_VALOR).acesso_entrada & 0x100) != 0) throw new Tradução_erro("ponto_de_entrada_VALOR FUNÇÃO_VALOR formato_VALOR erro");
        List<String> linha_de_entrada = new ArrayList<>(); linha_de_entrada.add(".code32");
        for (aula_dados dados : 클래스들.values()) {
            String Estado_VALOR = símbolo("state",dados.Nome), inicializar = símbolo("init",dados.Nome);
            Collections.addAll(linha_de_entrada,".bss",".balign 4",Estado_VALOR + ": .long 0",".text",inicializar + ":","cmpl $0, " + Estado_VALOR,"jne " + inicializar + "_done","movl $1, " + Estado_VALOR);
            método_Referência inicializador_Referência = new método_Referência(dados.Nome,"<clinit>","()V"); if (함수들.containsKey(inicializador_Referência)) linha_de_entrada.add("call " + símbolo("method",inicializador_Referência.부분들()));
            Collections.addAll(linha_de_entrada,"movl $2, " + Estado_VALOR,inicializar + "_done:","ret");
            for (membro_dados valor_do_campo : dados.valor_do_campo) {
                byte[] constante_VALOR = valor_do_campo.valor_do_atributo.get("ConstantValue"); String VALOR = constante_VALOR == null ? "0" : X_86_constante(dados,new dados_Leitor(constante_VALOR).두바이트());
                Collections.addAll(linha_de_entrada,".data",".balign 4",símbolo("field",dados.Nome,valor_do_campo.Nome,valor_do_campo.서술) + ": .long " + VALOR);
            }
            for (membro_dados FUNÇÃO_VALOR : dados.FUNÇÃO_VALOR) if (!FUNÇÃO_VALOR.Nome.equals("<init>")) linha_de_entrada.add(X_86_corpo_do_método(new método_Referência(dados.Nome,FUNÇÃO_VALOR.Nome,FUNÇÃO_VALOR.서술),FUNÇÃO_VALOR,computador_tabela,meta));
        }
        Collections.addAll(linha_de_entrada,".text",".globl java_entry","java_entry:","call " + símbolo("init",ponto_de_entrada_VALOR.proprietário_VALOR),"call " + símbolo("method",ponto_de_entrada_VALOR.부분들()));
        if (ponto_de_entrada_VALOR.서술.equals("()V")) linha_de_entrada.add("xorl %eax, %eax"); linha_de_entrada.add("ret");
        for (String ceder_VALOR : 내보냄) {
            int delimitador_VALOR = ceder_VALOR.indexOf('='); if (delimitador_VALOR < 1) throw new Tradução_erro("내보내기 ceder_VALOR erro");
            String externo_VALOR = ceder_VALOR.substring(0,delimitador_VALOR), FUNÇÃO_VALOR = ceder_VALOR.substring(delimitador_VALOR + 1); int Divisão_RC = FUNÇÃO_VALOR.lastIndexOf('.');
            if (Divisão_RC < 0 || !externo_VALOR.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tradução_erro("내보내기 símbolo erro");
            String aula_VALOR = FUNÇÃO_VALOR.substring(0,Divisão_RC).replace('.','/'), Nome = FUNÇÃO_VALOR.substring(Divisão_RC + 1); método_Referência seleção_VALOR = null;
            for (método_Referência Referência : 함수들.keySet()) if (Referência.proprietário_VALOR.equals(aula_VALOR) && Referência.Nome.equals(Nome)) { if (seleção_VALOR != null) throw new Tradução_erro("겹친 내보내기 meta"); seleção_VALOR = Referência; }
            if (seleção_VALOR == null) throw new Tradução_erro("내보낼 함수가 없음");
            Collections.addAll(linha_de_entrada,".text",".globl " + externo_VALOR,externo_VALOR + ":","call " + símbolo("init",seleção_VALOR.proprietário_VALOR),"jmp " + símbolo("method",seleção_VALOR.부분들()));
        }
        linha_de_entrada.add(".section .rodata");
        for (Map.Entry<String,String> entrada_VALOR_962f286b : 문자열들.entrySet()) {
            Collections.addAll(linha_de_entrada,".balign 4",entrada_VALOR_962f286b.getValue() + ":",".long " + entrada_VALOR_962f286b.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lição_VALOR : entrada_VALOR_962f286b.getKey().toCharArray()) 단위들.add(Integer.toString(lição_VALOR)); if (!단위들.isEmpty()) linha_de_entrada.add(".long " + String.join(",",단위들));
        }
        linha_de_entrada.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",linha_de_entrada) + "\n";
    }
    static void Executar_ferramenta(List<String> comando) throws Exception {
        if (new ProcessBuilder(comando).inheritIO().start().waitFor() != 0) throw new Tradução_erro("compilar_fonte erro: " + comando.get(0));
    }
    static String dados_cadeia(String texto) { return "\"" + texto.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Tradução(List<Path> entrada_Lista, String meta, String ponto_de_entrada, List<String> 내보냄, Path saídaTexto, Path recurso_VALOR) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), aula_caminho = 임시.resolve("classes"); Files.createDirectory(aula_caminho);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",aula_caminho.toString(),"-sourcepath",aula_caminho.toString(),"-d",aula_caminho.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int fonte_CONT_NÚM = 0;
            for (Path entrada_VALOR : entrada_Lista) {
                if (saídaTexto.toAbsolutePath().normalize().equals(entrada_VALOR.toAbsolutePath().normalize())) throw new Tradução_erro("saídaTexto 파일과 입력이 같음");
                if (entrada_VALOR.toString().endsWith(".java")) { 자바명령.add(entrada_VALOR.toString()); fonte_CONT_NÚM++; }
                else if (entrada_VALOR.toString().endsWith(".class")) 바이트코드.add(entrada_VALOR);
                else throw new Tradução_erro(".java 또는 .class만 Suporte_VALOR");
            }
            if (fonte_CONT_NÚM > 0) Executar_ferramenta(자바명령);
            try (java.util.stream.Stream<Path> caminho_Lista = Files.walk(aula_caminho)) { caminho_Lista.filter(caminho -> caminho.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            CompiladorAntecipado CONVERTER_VALOR = new CompiladorAntecipado(바이트코드,meta.equals("user") ? "user" : "kernel",262144,recurso_VALOR);
            String montar_VALOR = CONVERTER_VALOR.X_86_assembly(ponto_de_entrada,내보냄,meta); Files.writeString(임시.resolve("program.s"),montar_VALOR,StandardCharsets.UTF_8);
            Path ferramenta_cargo = recurso_VALOR.getParent();
            Executar_ferramenta(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Executar_ferramenta(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),ferramenta_cargo.resolve("SuporteExecução.s").toString()));
            List<String> Ligar = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (meta.equals("kernel")) Ligar.add("-r");
            else {
                Executar_ferramenta(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),ferramenta_cargo.resolve(meta.equals("user") ? "START_usuário_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Ligar,"-e","_start",임시.resolve("start.o").toString());
                if (meta.equals("user")) Collections.addAll(Ligar,"-T",ferramenta_cargo.resolve("usuário_Link_Layout.ld").toString());
            }
            Collections.addAll(Ligar,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Executar_ferramenta(Ligar);
            saídaTexto = saídaTexto.toAbsolutePath(); Files.createDirectories(saídaTexto.getParent()); Path publicar_VALOR = Files.createTempFile(saídaTexto.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publicar_VALOR,StandardCopyOption.REPLACE_EXISTING); Files.move(publicar_VALOR,saídaTexto,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publicar_VALOR); }
            Files.setPosixFilePermissions(saídaTexto,java.nio.file.attribute.PosixFilePermissions.fromString(meta.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(saídaTexto + ".s"),montar_VALOR,StandardCharsets.UTF_8);
            List<String> símbolo_dados = new ArrayList<>(), dados_de_origem = new ArrayList<>();
            for (método_Referência Referência : CONVERTER_VALOR.함수들.keySet()) símbolo_dados.add(dados_cadeia(símbolo("method",Referência.부분들())) + ":" + dados_cadeia(Referência.proprietário_VALOR + "." + Referência.Nome + Referência.서술));
            for (Path entrada_VALOR : entrada_Lista) {
                byte[] hash_Arquivo = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(entrada_VALOR)); StringBuilder texto = new StringBuilder(); for (byte VALOR : hash_Arquivo) texto.append(String.format(Locale.ROOT,"%02x",VALOR & 255));
                dados_de_origem.add(dados_cadeia(entrada_VALOR.toAbsolutePath().toString()) + ":" + dados_cadeia(texto.toString()));
            }
            Files.writeString(Paths.get(saídaTexto + ".json"),"{\"target\":" + dados_cadeia(meta) + ",\"entry\":" + dados_cadeia(ponto_de_entrada) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",símbolo_dados) + "},\"sources\":{" + String.join(",",dados_de_origem) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> caminho_Lista = Files.walk(임시)) { for (Path caminho : (Iterable<Path>)caminho_Lista.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(caminho); }
        }
    }
    public static void main(String[] argumentos) {
        try {
            String ponto_de_entrada = null, meta = "kernel", X_86_alvo = null; Path saída_caminho = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> caminho_Lista = new ArrayList<>();
            for (int 순번 = 0; 순번 < argumentos.length; 순번++) {
                String VALOR = argumentos[순번];
                switch (VALOR) {
                    case "--target": X_86_alvo = argumentos[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry aula_VALOR.FUNÇÃO_VALOR -o saídaTexto [--target linux|kernel|user] [--profile kernel|user] [--export símbolo=aula_VALOR.FUNÇÃO_VALOR] 클래스파일 또는 Java원문"); return;
                    case "--entry": ponto_de_entrada = argumentos[++순번]; break;
                    case "--profile": meta = argumentos[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(argumentos[++순번]); break;
                    case "--export": 내보냄.add(argumentos[++순번]); break;
                    case "-o": saída_caminho = Paths.get(argumentos[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALOR.startsWith("-")) throw new Tradução_erro("알 número 없는 옵션: " + VALOR); caminho_Lista.add(Paths.get(VALOR));
                }
            }
            if (ponto_de_entrada == null || saída_caminho == null || caminho_Lista.isEmpty()) throw new Tradução_erro("--entry, -o, aula_VALOR 파일이 필요합니다");
            Path recurso_VALOR = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_alvo != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_alvo)) throw new Tradução_erro("알 número 없는 Executar_comando meta");
                X_86_Tradução(caminho_Lista,X_86_alvo,ponto_de_entrada,내보냄,saída_caminho,recurso_VALOR); return;
            }
            String códigoFonte = new CompiladorAntecipado(caminho_Lista, meta, 낱말수, recurso_VALOR).gerar(ponto_de_entrada, 내보냄, 범용표기);
            saída_caminho = saída_caminho.toAbsolutePath(); Files.createDirectories(saída_caminho.getParent());
            Path 임시 = Files.createTempFile(saída_caminho.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, códigoFonte, StandardCharsets.UTF_8); Files.move(임시, saída_caminho, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception erro) { System.err.println("compilar_fonte erro: " + erro.getMessage()); System.exit(1); }
    }
}
