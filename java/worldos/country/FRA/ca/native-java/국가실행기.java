// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·generar_sistema·실행을 맡는 allotjar Java Eines. */
public final class 국가실행기 {
    static final class dades_analitzador {
        final String FONT; int Posició;
        dades_analitzador(String SMS) { FONT = SMS; }
        void 빈칸() { while (Posició < FONT.length() && Character.isWhitespace(FONT.charAt(Posició))) Posició++; }
        Object Lectura() {
            빈칸(); char caràcter_VALOR = FONT.charAt(Posició++);
            if (caràcter_VALOR == '{') {
                Map<String,Object> RESULTAT = new LinkedHashMap<>(); 빈칸();
                if (FONT.charAt(Posició) == '}') { Posició++; return RESULTAT; }
                while (true) {
                    String Nom = (String)Lectura(); 빈칸(); if (FONT.charAt(Posició++) != ':') throw new IllegalArgumentException("dades 구분 s_ha_produït_un_error");
                    RESULTAT.put(Nom, Lectura()); 빈칸(); char 구분 = FONT.charAt(Posició++);
                    if (구분 == '}') return RESULTAT; if (구분 != ',') throw new IllegalArgumentException("dades 구분 s_ha_produït_un_error");
                }
            }
            if (caràcter_VALOR == '[') {
                List<Object> RESULTAT = new ArrayList<>(); 빈칸();
                if (FONT.charAt(Posició) == ']') { Posició++; return RESULTAT; }
                while (true) {
                    RESULTAT.add(Lectura()); 빈칸(); char 구분 = FONT.charAt(Posició++);
                    if (구분 == ']') return RESULTAT; if (구분 != ',') throw new IllegalArgumentException("dades 구분 s_ha_produït_un_error");
                }
            }
            if (caràcter_VALOR == '"') {
                StringBuilder RESULTAT = new StringBuilder();
                while (true) {
                    char Següent_element = FONT.charAt(Posició++); if (Següent_element == '"') return RESULTAT.toString();
                    if (Següent_element == '\\') {
                        Següent_element = FONT.charAt(Posició++);
                        if (Següent_element == 'u') { RESULTAT.append((char)Integer.parseInt(FONT.substring(Posició, Posició + 4),16)); Posició += 4; continue; }
                        if (Següent_element == 'n') Següent_element = '\n'; else if (Següent_element == 'r') Següent_element = '\r'; else if (Següent_element == 't') Següent_element = '\t';
                        else if (Següent_element == 'b') Següent_element = '\b'; else if (Següent_element == 'f') Següent_element = '\f';
                        else if (Següent_element != '"' && Següent_element != '\\' && Següent_element != '/') throw new IllegalArgumentException("문자 이스케이프 s_ha_produït_un_error");
                    }
                    RESULTAT.append(Següent_element);
                }
            }
            int Executa_2 = Posició - 1;
            while (Posició < FONT.length() && ",]} \t\r\n".indexOf(FONT.charAt(Posició)) < 0) Posició++;
            String VALOR = FONT.substring(Executa_2, Posició);
            if (VALOR.equals("true")) return Boolean.TRUE; if (VALOR.equals("false")) return Boolean.FALSE; if (VALOR.equals("null")) return null;
            return Double.valueOf(VALOR);
        }
    }
    static String hash_arxiu(Path Camí) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] dades = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Camí)) { for (int durada_VALOR; (durada_VALOR = 입력.read(dades)) >= 0;) 계산.update(dades,0,durada_VALOR); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] dades) {
        StringBuilder SMS = new StringBuilder(); for (byte VALOR : dades) SMS.append(String.format(Locale.ROOT,"%02x",VALOR & 255)); return SMS.toString();
    }
    static Path intern_camí(Path Project_rel, String Nom) {
        Path RESULTAT = Project_rel.resolve(Nom).normalize();
        if (Nom.isEmpty() || Paths.get(Nom).isAbsolute() || !RESULTAT.startsWith(Project_rel) || Nom.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Camí: " + Nom);
        for (Path 부분 : Paths.get(Nom)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Camí 금지: " + Nom);
        for (Path 현재 = RESULTAT; 현재 != null && 현재.startsWith(Project_rel); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nom);
        return RESULTAT;
    }
    static String 명령출력(List<String> Ordre) throws Exception {
        Process Procés_VALOR = new ProcessBuilder(Ordre).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String RESULTAT = new String(Procés_VALOR.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Procés_VALOR.waitFor() != 0) throw new IOException("Ordre error_VALOR: " + Ordre.get(0)); return RESULTAT;
    }
    static void extreure(Path Arxiu_VALOR, Path destinació_VALOR) throws Exception {
        for (String Nom : 명령출력(Arrays.asList("tar","-tzf",Arxiu_VALOR.toString())).split("\n")) intern_camí(destinació_VALOR, Nom);
        for (String línia : 명령출력(Arrays.asList("tar","-tvzf",Arxiu_VALOR.toString())).split("\n"))
            if (!línia.isEmpty() && línia.charAt(0) != '-' && línia.charAt(0) != 'd') throw new IOException("extern_VALOR 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(destinació_VALOR);
        int Estat_VALOR = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arxiu_VALOR.toString(),"-C",destinació_VALOR.toString()).inheritIO().start().waitFor();
        if (Estat_VALOR != 0) throw new IOException("의존성 Arxiu_VALOR versió_Emmagatzematge error_VALOR");
    }
    static void 호출(Path 작업경로, Path Eines, List<String> 인수, Map<String,String> entorn) throws Exception {
        List<String> Ordre = new ArrayList<>(Arrays.asList("python3", Eines.toString())); Ordre.addAll(인수);
        ProcessBuilder Executa_ordre = new ProcessBuilder(Ordre).directory(작업경로.toFile()).inheritIO(); Executa_ordre.environment().putAll(entorn);
        int Estat_VALOR = Executa_ordre.start().waitFor(); if (Estat_VALOR != 0) throw new IOException("Eines error_VALOR: " + Eines + " (" + Estat_VALOR + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Acció = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Acció)) throw new IllegalArgumentException("알 수 없는 Acció");
        Path Project_rel = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Ajusts = (Map<String,Object>)new dades_analitzador(Files.readString(Project_rel.resolve("native.json"),StandardCharsets.UTF_8)).Lectura();
        Path font_arbre = intern_camí(Project_rel,(String)Ajusts.get("source")), nucli_VALOR = intern_camí(font_arbre,(String)Ajusts.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Ajusts.get("owned_files");
        for (String Nom : 소유파일들) if (!Files.isRegularFile(intern_camí(font_arbre,Nom))) throw new IOException("font_arbre 없음: " + Nom);
        if (Acció.equals("check")) { System.out.println(Ajusts.get("country") + " " + Ajusts.get("language") + " 독립 font_arbre verificar 완료"); return; }
        String 자원상대 = (String)Ajusts.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Project_rel Camí s_ha_produït_un_error");
        Path recurs_VALOR = Project_rel.resolve(자원상대).normalize(); Path Arxiu_VALOR = recurs_VALOR.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Ajusts.get("vendor_sha256");
        if (!hash_arxiu(Arxiu_VALOR).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = font_arbre.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { extreure(Arxiu_VALOR, font_arbre); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> entorn = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (entorn.containsKey("IP_CONFIG")) ipConfig = Paths.get(entorn.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_rel; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = font_arbre.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        entorn.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Acció) && !entorn.containsKey("QEMU_AARCH64")) {
            Path programa_iniciador = recurs_VALOR.resolve("host/qemu"), 실행기표식 = recurs_VALOR.resolve("host/.qemu-sha256");
            String iniciador_hash = (String)Ajusts.get("qemu_sha256");
            if (!Files.isRegularFile(programa_iniciador) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(iniciador_hash)) {
                Path iniciador_Arxiu = recurs_VALOR.resolve("qemu-host.tar.gz"); if (!hash_arxiu(iniciador_Arxiu).equals(iniciador_hash)) throw new IOException("QEMU SHA-256 불일치");
                extreure(iniciador_Arxiu,recurs_VALOR.resolve("host")); Files.writeString(실행기표식,iniciador_hash + "\n");
            }
            entorn.put("QEMU_AARCH64",programa_iniciador.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nom : 소유파일들) { 계산.update(Nom.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(intern_camí(font_arbre,Nom))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String font_hash = hash_SMS(계산.digest()); Path 빌드표식 = nucli_VALOR.resolve("build/worldos-source.sha256");
        if (Acció.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(font_hash)) {
            호출(nucli_VALOR,intern_camí(nucli_VALOR,(String)Ajusts.get("builder")),Collections.emptyList(),entorn);
            Files.writeString(빌드표식,font_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Acció.equals("run") || Acció.equals("desktop")) {
            if (Acció.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(nucli_VALOR,intern_camí(nucli_VALOR,(String)Ajusts.get("runner")),추가인수,entorn);
        } else if (Acció.equals("image")) 호출(nucli_VALOR,intern_camí(nucli_VALOR,(String)Ajusts.get("image_builder")),추가인수,entorn);
        else if (Acció.equals("test-system")) {
            추가인수.add(0,Project_rel.toString()); 추가인수.add(0,"--edition");
            호출(nucli_VALOR,intern_camí(nucli_VALOR,(String)Ajusts.get("system_tester")),추가인수,entorn);
        }
    }
}
