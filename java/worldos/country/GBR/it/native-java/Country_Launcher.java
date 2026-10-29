// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·costruire·실행을 맡는 host Java strumenti. */
public final class Country_Launcher {
    static final class dati_parser {
        final String codiceSorgente; int posizione;
        dati_parser(String testo) { codiceSorgente = testo; }
        void 빈칸() { while (posizione < codiceSorgente.length() && Character.isWhitespace(codiceSorgente.charAt(posizione))) posizione++; }
        Object Lettura() {
            빈칸(); char carattere_VALORE = codiceSorgente.charAt(posizione++);
            if (carattere_VALORE == '{') {
                Map<String,Object> risultato = new LinkedHashMap<>(); 빈칸();
                if (codiceSorgente.charAt(posizione) == '}') { posizione++; return risultato; }
                while (true) {
                    String Nome = (String)Lettura(); 빈칸(); if (codiceSorgente.charAt(posizione++) != ':') throw new IllegalArgumentException("dati delimitatore_VALORE errore");
                    risultato.put(Nome, Lettura()); 빈칸(); char delimitatore_VALORE = codiceSorgente.charAt(posizione++);
                    if (delimitatore_VALORE == '}') return risultato; if (delimitatore_VALORE != ',') throw new IllegalArgumentException("dati delimitatore_VALORE errore");
                }
            }
            if (carattere_VALORE == '[') {
                List<Object> risultato = new ArrayList<>(); 빈칸();
                if (codiceSorgente.charAt(posizione) == ']') { posizione++; return risultato; }
                while (true) {
                    risultato.add(Lettura()); 빈칸(); char delimitatore_VALORE = codiceSorgente.charAt(posizione++);
                    if (delimitatore_VALORE == ']') return risultato; if (delimitatore_VALORE != ',') throw new IllegalArgumentException("dati delimitatore_VALORE errore");
                }
            }
            if (carattere_VALORE == '"') {
                StringBuilder risultato = new StringBuilder();
                while (true) {
                    char Avanti_articolo = codiceSorgente.charAt(posizione++); if (Avanti_articolo == '"') return risultato.toString();
                    if (Avanti_articolo == '\\') {
                        Avanti_articolo = codiceSorgente.charAt(posizione++);
                        if (Avanti_articolo == 'u') { risultato.append((char)Integer.parseInt(codiceSorgente.substring(posizione, posizione + 4),16)); posizione += 4; continue; }
                        if (Avanti_articolo == 'n') Avanti_articolo = '\n'; else if (Avanti_articolo == 'r') Avanti_articolo = '\r'; else if (Avanti_articolo == 't') Avanti_articolo = '\t';
                        else if (Avanti_articolo == 'b') Avanti_articolo = '\b'; else if (Avanti_articolo == 'f') Avanti_articolo = '\f';
                        else if (Avanti_articolo != '"' && Avanti_articolo != '\\' && Avanti_articolo != '/') throw new IllegalArgumentException("문자 이스케이프 errore");
                    }
                    risultato.append(Avanti_articolo);
                }
            }
            int avvia = posizione - 1;
            while (posizione < codiceSorgente.length() && ",]} \t\r\n".indexOf(codiceSorgente.charAt(posizione)) < 0) posizione++;
            String VALORE = codiceSorgente.substring(avvia, posizione);
            if (VALORE.equals("true")) return Boolean.TRUE; if (VALORE.equals("false")) return Boolean.FALSE; if (VALORE.equals("null")) return null;
            return Double.valueOf(VALORE);
        }
    }
    static String hash_File(Path percorso) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] dati = new byte[1024 * 1024];
        try (InputStream input_VALORE = Files.newInputStream(percorso)) { for (int durata_VALORE; (durata_VALORE = input_VALORE.read(dati)) >= 0;) 계산.update(dati,0,durata_VALORE); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] dati) {
        StringBuilder testo = new StringBuilder(); for (byte VALORE : dati) testo.append(String.format(Locale.ROOT,"%02x",VALORE & 255)); return testo.toString();
    }
    static Path interno_percorso(Path azione_radice, String Nome) {
        Path risultato = azione_radice.resolve(Nome).normalize();
        if (Nome.isEmpty() || Paths.get(Nome).isAbsolute() || !risultato.startsWith(azione_radice) || Nome.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 percorso: " + Nome);
        for (Path 부분 : Paths.get(Nome)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 percorso 금지: " + Nome);
        for (Path Regolari_articolo = risultato; Regolari_articolo != null && Regolari_articolo.startsWith(azione_radice); Regolari_articolo = Regolari_articolo.getParent())
            if (Files.isSymbolicLink(Regolari_articolo)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nome);
        return risultato;
    }
    static String comando_output(List<String> comando) throws Exception {
        Process Processi_VALORE = new ProcessBuilder(comando).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String risultato = new String(Processi_VALORE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Processi_VALORE.waitFor() != 0) throw new IOException("comando errore_VALORE: " + comando.get(0)); return risultato;
    }
    static void estrarre(Path Archivio_VALORE, Path meta_VALORE) throws Exception {
        for (String Nome : comando_output(Arrays.asList("tar","-tzf",Archivio_VALORE.toString())).split("\n")) interno_percorso(meta_VALORE, Nome);
        for (String riga_di_ingresso : comando_output(Arrays.asList("tar","-tvzf",Archivio_VALORE.toString())).split("\n"))
            if (!riga_di_ingresso.isEmpty() && riga_di_ingresso.charAt(0) != '-' && riga_di_ingresso.charAt(0) != 'd') throw new IOException("esterno_VALORE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(meta_VALORE);
        int Stato_VALORE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Archivio_VALORE.toString(),"-C",meta_VALORE.toString()).inheritIO().start().waitFor();
        if (Stato_VALORE != 0) throw new IOException("의존성 Archivio_VALORE release_Memoria errore_VALORE");
    }
    static void 호출(Path 작업경로, Path strumenti, List<String> argomenti, Map<String,String> ambiente) throws Exception {
        List<String> comando = new ArrayList<>(Arrays.asList("python3", strumenti.toString())); comando.addAll(argomenti);
        ProcessBuilder Esegui_comando = new ProcessBuilder(comando).directory(작업경로.toFile()).inheritIO(); Esegui_comando.environment().putAll(ambiente);
        int Stato_VALORE = Esegui_comando.start().waitFor(); if (Stato_VALORE != 0) throw new IOException("strumenti errore_VALORE: " + strumenti + " (" + Stato_VALORE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argomenti) throws Exception {
        if (argomenti.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Azione = argomenti[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Azione)) throw new IllegalArgumentException("알 numero 없는 Azione");
        Path azione_radice = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Impostazioni = (Map<String,Object>)new dati_parser(Files.readString(azione_radice.resolve("native.json"),StandardCharsets.UTF_8)).Lettura();
        Path fonte_albero = interno_percorso(azione_radice,(String)Impostazioni.get("source")), kernel_VALORE = interno_percorso(fonte_albero,(String)Impostazioni.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Impostazioni.get("owned_files");
        for (String Nome : 소유파일들) if (!Files.isRegularFile(interno_percorso(fonte_albero,Nome))) throw new IOException("fonte_albero 없음: " + Nome);
        if (Azione.equals("check")) { System.out.println(Impostazioni.get("country") + " " + Impostazioni.get("language") + " 독립 fonte_albero verificare 완료"); return; }
        String risorsa_percorso_relativo = (String)Impostazioni.getOrDefault("resource_root", ".");
        if (!risorsa_percorso_relativo.equals(".") && !risorsa_percorso_relativo.equals("..")) throw new IllegalArgumentException("의존성 azione_radice percorso errore");
        Path risorsa_VALORE = azione_radice.resolve(risorsa_percorso_relativo).normalize(); Path Archivio_VALORE = risorsa_VALORE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Impostazioni.get("vendor_sha256");
        if (!hash_File(Archivio_VALORE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path marcatore_VALORE = fonte_albero.resolve(".vendor-sha256");
        if (!Files.isRegularFile(marcatore_VALORE) || !Files.readString(marcatore_VALORE).trim().equals(기대해시)) { estrarre(Archivio_VALORE, fonte_albero); Files.writeString(marcatore_VALORE,기대해시 + "\n"); }
        Map<String,String> ambiente = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (ambiente.containsKey("IP_CONFIG")) ipConfig = Paths.get(ambiente.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = azione_radice; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = fonte_albero.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        ambiente.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Azione) && !ambiente.containsKey("QEMU_AARCH64")) {
            Path app_Launcher = risorsa_VALORE.resolve("host/qemu"), Launcher_marcatore = risorsa_VALORE.resolve("host/.qemu-sha256");
            String Launcher_hash = (String)Impostazioni.get("qemu_sha256");
            if (!Files.isRegularFile(app_Launcher) || !Files.isRegularFile(Launcher_marcatore) || !Files.readString(Launcher_marcatore).trim().equals(Launcher_hash)) {
                Path Launcher_Archivio = risorsa_VALORE.resolve("qemu-host.tar.gz"); if (!hash_File(Launcher_Archivio).equals(Launcher_hash)) throw new IOException("QEMU SHA-256 불일치");
                estrarre(Launcher_Archivio,risorsa_VALORE.resolve("host")); Files.writeString(Launcher_marcatore,Launcher_hash + "\n");
            }
            ambiente.put("QEMU_AARCH64",app_Launcher.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nome : 소유파일들) { 계산.update(Nome.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(interno_percorso(fonte_albero,Nome))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String fonte_hash = hash_SMS(계산.digest()); Path BLD_marcatore = kernel_VALORE.resolve("build/worldos-source.sha256");
        if (Azione.equals("build") || !Files.isRegularFile(BLD_marcatore) || !Files.readString(BLD_marcatore).trim().equals(fonte_hash)) {
            호출(kernel_VALORE,interno_percorso(kernel_VALORE,(String)Impostazioni.get("builder")),Collections.emptyList(),ambiente);
            Files.writeString(BLD_marcatore,fonte_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(argomenti).subList(1,argomenti.length));
        if (Azione.equals("run") || Azione.equals("desktop")) {
            if (Azione.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_VALORE,interno_percorso(kernel_VALORE,(String)Impostazioni.get("runner")),추가인수,ambiente);
        } else if (Azione.equals("image")) 호출(kernel_VALORE,interno_percorso(kernel_VALORE,(String)Impostazioni.get("image_builder")),추가인수,ambiente);
        else if (Azione.equals("test-system")) {
            추가인수.add(0,azione_radice.toString()); 추가인수.add(0,"--edition");
            호출(kernel_VALORE,interno_percorso(kernel_VALORE,(String)Impostazioni.get("system_tester")),추가인수,ambiente);
        }
    }
}
