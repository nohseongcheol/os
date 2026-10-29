// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·construir·실행을 맡는 host Java ferramentas. */
public final class IniciadorPaís {
    static final class dados_analisador {
        final String códigoFonte; int posição;
        dados_analisador(String texto) { códigoFonte = texto; }
        void 빈칸() { while (posição < códigoFonte.length() && Character.isWhitespace(códigoFonte.charAt(posição))) posição++; }
        Object Leitura() {
            빈칸(); char caractere_VALOR = códigoFonte.charAt(posição++);
            if (caractere_VALOR == '{') {
                Map<String,Object> resultado = new LinkedHashMap<>(); 빈칸();
                if (códigoFonte.charAt(posição) == '}') { posição++; return resultado; }
                while (true) {
                    String Nome = (String)Leitura(); 빈칸(); if (códigoFonte.charAt(posição++) != ':') throw new IllegalArgumentException("dados delimitador_VALOR erro");
                    resultado.put(Nome, Leitura()); 빈칸(); char delimitador_VALOR = códigoFonte.charAt(posição++);
                    if (delimitador_VALOR == '}') return resultado; if (delimitador_VALOR != ',') throw new IllegalArgumentException("dados delimitador_VALOR erro");
                }
            }
            if (caractere_VALOR == '[') {
                List<Object> resultado = new ArrayList<>(); 빈칸();
                if (códigoFonte.charAt(posição) == ']') { posição++; return resultado; }
                while (true) {
                    resultado.add(Leitura()); 빈칸(); char delimitador_VALOR = códigoFonte.charAt(posição++);
                    if (delimitador_VALOR == ']') return resultado; if (delimitador_VALOR != ',') throw new IllegalArgumentException("dados delimitador_VALOR erro");
                }
            }
            if (caractere_VALOR == '"') {
                StringBuilder resultado = new StringBuilder();
                while (true) {
                    char Avançar_item = códigoFonte.charAt(posição++); if (Avançar_item == '"') return resultado.toString();
                    if (Avançar_item == '\\') {
                        Avançar_item = códigoFonte.charAt(posição++);
                        if (Avançar_item == 'u') { resultado.append((char)Integer.parseInt(códigoFonte.substring(posição, posição + 4),16)); posição += 4; continue; }
                        if (Avançar_item == 'n') Avançar_item = '\n'; else if (Avançar_item == 'r') Avançar_item = '\r'; else if (Avançar_item == 't') Avançar_item = '\t';
                        else if (Avançar_item == 'b') Avançar_item = '\b'; else if (Avançar_item == 'f') Avançar_item = '\f';
                        else if (Avançar_item != '"' && Avançar_item != '\\' && Avançar_item != '/') throw new IllegalArgumentException("문자 이스케이프 erro");
                    }
                    resultado.append(Avançar_item);
                }
            }
            int iniciar = posição - 1;
            while (posição < códigoFonte.length() && ",]} \t\r\n".indexOf(códigoFonte.charAt(posição)) < 0) posição++;
            String VALOR = códigoFonte.substring(iniciar, posição);
            if (VALOR.equals("true")) return Boolean.TRUE; if (VALOR.equals("false")) return Boolean.FALSE; if (VALOR.equals("null")) return null;
            return Double.valueOf(VALOR);
        }
    }
    static String hash_Arquivo(Path caminho) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] dados = new byte[1024 * 1024];
        try (InputStream entrada_VALOR = Files.newInputStream(caminho)) { for (int duração_VALOR; (duração_VALOR = entrada_VALOR.read(dados)) >= 0;) 계산.update(dados,0,duração_VALOR); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] dados) {
        StringBuilder texto = new StringBuilder(); for (byte VALOR : dados) texto.append(String.format(Locale.ROOT,"%02x",VALOR & 255)); return texto.toString();
    }
    static Path interno_caminho(Path ação_raiz, String Nome) {
        Path resultado = ação_raiz.resolve(Nome).normalize();
        if (Nome.isEmpty() || Paths.get(Nome).isAbsolute() || !resultado.startsWith(ação_raiz) || Nome.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 caminho: " + Nome);
        for (Path 부분 : Paths.get(Nome)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 caminho 금지: " + Nome);
        for (Path em_dia_item = resultado; em_dia_item != null && em_dia_item.startsWith(ação_raiz); em_dia_item = em_dia_item.getParent())
            if (Files.isSymbolicLink(em_dia_item)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nome);
        return resultado;
    }
    static String comando_saída(List<String> comando) throws Exception {
        Process Processo_VALOR = new ProcessBuilder(comando).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String resultado = new String(Processo_VALOR.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Processo_VALOR.waitFor() != 0) throw new IOException("comando falha_VALOR: " + comando.get(0)); return resultado;
    }
    static void extrair(Path arquivo_VALOR, Path destino_VALOR) throws Exception {
        for (String Nome : comando_saída(Arrays.asList("tar","-tzf",arquivo_VALOR.toString())).split("\n")) interno_caminho(destino_VALOR, Nome);
        for (String linha_de_entrada : comando_saída(Arrays.asList("tar","-tvzf",arquivo_VALOR.toString())).split("\n"))
            if (!linha_de_entrada.isEmpty() && linha_de_entrada.charAt(0) != '-' && linha_de_entrada.charAt(0) != 'd') throw new IOException("externo_VALOR 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(destino_VALOR);
        int Estado_VALOR = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",arquivo_VALOR.toString(),"-C",destino_VALOR.toString()).inheritIO().start().waitFor();
        if (Estado_VALOR != 0) throw new IOException("의존성 arquivo_VALOR lançar_Armazenamento falha_VALOR");
    }
    static void 호출(Path 작업경로, Path ferramentas, List<String> argumentos, Map<String,String> ambiente) throws Exception {
        List<String> comando = new ArrayList<>(Arrays.asList("python3", ferramentas.toString())); comando.addAll(argumentos);
        ProcessBuilder Executar_comando = new ProcessBuilder(comando).directory(작업경로.toFile()).inheritIO(); Executar_comando.environment().putAll(ambiente);
        int Estado_VALOR = Executar_comando.start().waitFor(); if (Estado_VALOR != 0) throw new IOException("ferramentas falha_VALOR: " + ferramentas + " (" + Estado_VALOR + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argumentos) throws Exception {
        if (argumentos.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Acção = argumentos[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Acção)) throw new IllegalArgumentException("알 número 없는 Acção");
        Path ação_raiz = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Definições = (Map<String,Object>)new dados_analisador(Files.readString(ação_raiz.resolve("native.json"),StandardCharsets.UTF_8)).Leitura();
        Path fonte_árvore = interno_caminho(ação_raiz,(String)Definições.get("source")), kernel_VALOR = interno_caminho(fonte_árvore,(String)Definições.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Definições.get("owned_files");
        for (String Nome : 소유파일들) if (!Files.isRegularFile(interno_caminho(fonte_árvore,Nome))) throw new IOException("fonte_árvore 없음: " + Nome);
        if (Acção.equals("check")) { System.out.println(Definições.get("country") + " " + Definições.get("language") + " 독립 fonte_árvore verificar 완료"); return; }
        String recurso_caminho_relativo = (String)Definições.getOrDefault("resource_root", ".");
        if (!recurso_caminho_relativo.equals(".") && !recurso_caminho_relativo.equals("..")) throw new IllegalArgumentException("의존성 ação_raiz caminho erro");
        Path recurso_VALOR = ação_raiz.resolve(recurso_caminho_relativo).normalize(); Path arquivo_VALOR = recurso_VALOR.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Definições.get("vendor_sha256");
        if (!hash_Arquivo(arquivo_VALOR).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path favorito_VALOR = fonte_árvore.resolve(".vendor-sha256");
        if (!Files.isRegularFile(favorito_VALOR) || !Files.readString(favorito_VALOR).trim().equals(기대해시)) { extrair(arquivo_VALOR, fonte_árvore); Files.writeString(favorito_VALOR,기대해시 + "\n"); }
        Map<String,String> ambiente = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (ambiente.containsKey("IP_CONFIG")) ipConfig = Paths.get(ambiente.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = ação_raiz; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = fonte_árvore.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        ambiente.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Acção) && !ambiente.containsKey("QEMU_AARCH64")) {
            Path app_Launcher = recurso_VALOR.resolve("host/qemu"), Launcher_favorito = recurso_VALOR.resolve("host/.qemu-sha256");
            String Launcher_hash = (String)Definições.get("qemu_sha256");
            if (!Files.isRegularFile(app_Launcher) || !Files.isRegularFile(Launcher_favorito) || !Files.readString(Launcher_favorito).trim().equals(Launcher_hash)) {
                Path Launcher_arquivo = recurso_VALOR.resolve("qemu-host.tar.gz"); if (!hash_Arquivo(Launcher_arquivo).equals(Launcher_hash)) throw new IOException("QEMU SHA-256 불일치");
                extrair(Launcher_arquivo,recurso_VALOR.resolve("host")); Files.writeString(Launcher_favorito,Launcher_hash + "\n");
            }
            ambiente.put("QEMU_AARCH64",app_Launcher.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nome : 소유파일들) { 계산.update(Nome.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(interno_caminho(fonte_árvore,Nome))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String fonte_hash = hash_SMS(계산.digest()); Path BLD_favorito = kernel_VALOR.resolve("build/worldos-source.sha256");
        if (Acção.equals("build") || !Files.isRegularFile(BLD_favorito) || !Files.readString(BLD_favorito).trim().equals(fonte_hash)) {
            호출(kernel_VALOR,interno_caminho(kernel_VALOR,(String)Definições.get("builder")),Collections.emptyList(),ambiente);
            Files.writeString(BLD_favorito,fonte_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(argumentos).subList(1,argumentos.length));
        if (Acção.equals("run") || Acção.equals("desktop")) {
            if (Acção.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_VALOR,interno_caminho(kernel_VALOR,(String)Definições.get("runner")),추가인수,ambiente);
        } else if (Acção.equals("image")) 호출(kernel_VALOR,interno_caminho(kernel_VALOR,(String)Definições.get("image_builder")),추가인수,ambiente);
        else if (Acção.equals("test-system")) {
            추가인수.add(0,ação_raiz.toString()); 추가인수.add(0,"--edition");
            호출(kernel_VALOR,interno_caminho(kernel_VALOR,(String)Definições.get("system_tester")),추가인수,ambiente);
        }
    }
}
