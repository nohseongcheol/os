// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·compilar_sistema·실행을 맡는 hospedar Java Ferramentas. */
public final class 국가실행기 {
    static final class datos_analizador {
        final String FONTE; int Posición;
        datos_analizador(String Texto) { FONTE = Texto; }
        void 빈칸() { while (Posición < FONTE.length() && Character.isWhitespace(FONTE.charAt(Posición))) Posición++; }
        Object Lectura() {
            빈칸(); char carácter_VALOR = FONTE.charAt(Posición++);
            if (carácter_VALOR == '{') {
                Map<String,Object> RESULTANTE = new LinkedHashMap<>(); 빈칸();
                if (FONTE.charAt(Posición) == '}') { Posición++; return RESULTANTE; }
                while (true) {
                    String Nome = (String)Lectura(); 빈칸(); if (FONTE.charAt(Posición++) != ':') throw new IllegalArgumentException("datos delimitador_VALOR ERRO");
                    RESULTANTE.put(Nome, Lectura()); 빈칸(); char delimitador_VALOR = FONTE.charAt(Posición++);
                    if (delimitador_VALOR == '}') return RESULTANTE; if (delimitador_VALOR != ',') throw new IllegalArgumentException("datos delimitador_VALOR ERRO");
                }
            }
            if (carácter_VALOR == '[') {
                List<Object> RESULTANTE = new ArrayList<>(); 빈칸();
                if (FONTE.charAt(Posición) == ']') { Posición++; return RESULTANTE; }
                while (true) {
                    RESULTANTE.add(Lectura()); 빈칸(); char delimitador_VALOR = FONTE.charAt(Posición++);
                    if (delimitador_VALOR == ']') return RESULTANTE; if (delimitador_VALOR != ',') throw new IllegalArgumentException("datos delimitador_VALOR ERRO");
                }
            }
            if (carácter_VALOR == '"') {
                StringBuilder RESULTANTE = new StringBuilder();
                while (true) {
                    char Seguinte_elemento = FONTE.charAt(Posición++); if (Seguinte_elemento == '"') return RESULTANTE.toString();
                    if (Seguinte_elemento == '\\') {
                        Seguinte_elemento = FONTE.charAt(Posición++);
                        if (Seguinte_elemento == 'u') { RESULTANTE.append((char)Integer.parseInt(FONTE.substring(Posición, Posición + 4),16)); Posición += 4; continue; }
                        if (Seguinte_elemento == 'n') Seguinte_elemento = '\n'; else if (Seguinte_elemento == 'r') Seguinte_elemento = '\r'; else if (Seguinte_elemento == 't') Seguinte_elemento = '\t';
                        else if (Seguinte_elemento == 'b') Seguinte_elemento = '\b'; else if (Seguinte_elemento == 'f') Seguinte_elemento = '\f';
                        else if (Seguinte_elemento != '"' && Seguinte_elemento != '\\' && Seguinte_elemento != '/') throw new IllegalArgumentException("문자 이스케이프 ERRO");
                    }
                    RESULTANTE.append(Seguinte_elemento);
                }
            }
            int Executar_2 = Posición - 1;
            while (Posición < FONTE.length() && ",]} \t\r\n".indexOf(FONTE.charAt(Posición)) < 0) Posición++;
            String VALOR = FONTE.substring(Executar_2, Posición);
            if (VALOR.equals("true")) return Boolean.TRUE; if (VALOR.equals("false")) return Boolean.FALSE; if (VALOR.equals("null")) return null;
            return Double.valueOf(VALOR);
        }
    }
    static String hash_Ficheiro(Path CAMIÑO) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] datos = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(CAMIÑO)) { for (int duración_VALOR; (duración_VALOR = 입력.read(datos)) >= 0;) 계산.update(datos,0,duración_VALOR); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] datos) {
        StringBuilder Texto = new StringBuilder(); for (byte VALOR : datos) Texto.append(String.format(Locale.ROOT,"%02x",VALOR & 255)); return Texto.toString();
    }
    static Path 내부경로(Path Project_raíz, String Nome) {
        Path RESULTANTE = Project_raíz.resolve(Nome).normalize();
        if (Nome.isEmpty() || Paths.get(Nome).isAbsolute() || !RESULTANTE.startsWith(Project_raíz) || Nome.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 CAMIÑO: " + Nome);
        for (Path 부분 : Paths.get(Nome)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 CAMIÑO 금지: " + Nome);
        for (Path ao_corrente_elemento = RESULTANTE; ao_corrente_elemento != null && ao_corrente_elemento.startsWith(Project_raíz); ao_corrente_elemento = ao_corrente_elemento.getParent())
            if (Files.isSymbolicLink(ao_corrente_elemento)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nome);
        return RESULTANTE;
    }
    static String 명령출력(List<String> Orde) throws Exception {
        Process Proceso_VALOR = new ProcessBuilder(Orde).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String RESULTANTE = new String(Proceso_VALOR.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proceso_VALOR.waitFor() != 0) throw new IOException("Orde erro_VALOR: " + Orde.get(0)); return RESULTANTE;
    }
    static void extraer(Path Arquivo_VALOR, Path destino_VALOR) throws Exception {
        for (String Nome : 명령출력(Arrays.asList("tar","-tzf",Arquivo_VALOR.toString())).split("\n")) 내부경로(destino_VALOR, Nome);
        for (String Liña : 명령출력(Arrays.asList("tar","-tvzf",Arquivo_VALOR.toString())).split("\n"))
            if (!Liña.isEmpty() && Liña.charAt(0) != '-' && Liña.charAt(0) != 'd') throw new IOException("externo_VALOR 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(destino_VALOR);
        int Estado_VALOR = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arquivo_VALOR.toString(),"-C",destino_VALOR.toString()).inheritIO().start().waitFor();
        if (Estado_VALOR != 0) throw new IOException("의존성 Arquivo_VALOR liberar_Almacenamento erro_VALOR");
    }
    static void 호출(Path 작업경로, Path Ferramentas, List<String> Argumentos, Map<String,String> 환경) throws Exception {
        List<String> Orde = new ArrayList<>(Arrays.asList("python3", Ferramentas.toString())); Orde.addAll(Argumentos);
        ProcessBuilder executar_comando = new ProcessBuilder(Orde).directory(작업경로.toFile()).inheritIO(); executar_comando.environment().putAll(환경);
        int Estado_VALOR = executar_comando.start().waitFor(); if (Estado_VALOR != 0) throw new IOException("Ferramentas erro_VALOR: " + Ferramentas + " (" + Estado_VALOR + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumentos) throws Exception {
        if (Argumentos.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Acción = Argumentos[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Acción)) throw new IllegalArgumentException("알 수 없는 Acción");
        Path Project_raíz = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Configuración = (Map<String,Object>)new datos_analizador(Files.readString(Project_raíz.resolve("native.json"),StandardCharsets.UTF_8)).Lectura();
        Path fonte_árbore = 내부경로(Project_raíz,(String)Configuración.get("source")), kernel_VALOR = 내부경로(fonte_árbore,(String)Configuración.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Configuración.get("owned_files");
        for (String Nome : 소유파일들) if (!Files.isRegularFile(내부경로(fonte_árbore,Nome))) throw new IOException("fonte_árbore 없음: " + Nome);
        if (Acción.equals("check")) { System.out.println(Configuración.get("country") + " " + Configuración.get("language") + " 독립 fonte_árbore verificar 완료"); return; }
        String 자원상대 = (String)Configuración.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Project_raíz CAMIÑO ERRO");
        Path Recurso_VALOR = Project_raíz.resolve(자원상대).normalize(); Path Arquivo_VALOR = Recurso_VALOR.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Configuración.get("vendor_sha256");
        if (!hash_Ficheiro(Arquivo_VALOR).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = fonte_árbore.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { extraer(Arquivo_VALOR, fonte_árbore); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_raíz; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = fonte_árbore.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Acción) && !환경.containsKey("QEMU_AARCH64")) {
            Path apl_iniciador = Recurso_VALOR.resolve("host/qemu"), 실행기표식 = Recurso_VALOR.resolve("host/.qemu-sha256");
            String iniciador_hash = (String)Configuración.get("qemu_sha256");
            if (!Files.isRegularFile(apl_iniciador) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(iniciador_hash)) {
                Path iniciador_Arquivo = Recurso_VALOR.resolve("qemu-host.tar.gz"); if (!hash_Ficheiro(iniciador_Arquivo).equals(iniciador_hash)) throw new IOException("QEMU SHA-256 불일치");
                extraer(iniciador_Arquivo,Recurso_VALOR.resolve("host")); Files.writeString(실행기표식,iniciador_hash + "\n");
            }
            환경.put("QEMU_AARCH64",apl_iniciador.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nome : 소유파일들) { 계산.update(Nome.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(fonte_árbore,Nome))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String fonte_hash = hash_SMS(계산.digest()); Path 빌드표식 = kernel_VALOR.resolve("build/worldos-source.sha256");
        if (Acción.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(fonte_hash)) {
            호출(kernel_VALOR,내부경로(kernel_VALOR,(String)Configuración.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,fonte_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumentos).subList(1,Argumentos.length));
        if (Acción.equals("run") || Acción.equals("desktop")) {
            if (Acción.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_VALOR,내부경로(kernel_VALOR,(String)Configuración.get("runner")),추가인수,환경);
        } else if (Acción.equals("image")) 호출(kernel_VALOR,내부경로(kernel_VALOR,(String)Configuración.get("image_builder")),추가인수,환경);
        else if (Acción.equals("test-system")) {
            추가인수.add(0,Project_raíz.toString()); 추가인수.add(0,"--edition");
            호출(kernel_VALOR,내부경로(kernel_VALOR,(String)Configuración.get("system_tester")),추가인수,환경);
        }
    }
}
