// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Herramienta Java anfitriona para comprobar y restaurar dependencias, construir y ejecutar una edición nacional independiente. */
public final class LanzadorNacional {
    static final class AnalizadorDatos {
        final String fuente; int posición;
        AnalizadorDatos(String texto) { fuente = texto; }
        void saltarEspaciosBlancos() { while (posición < fuente.length() && Character.isWhitespace(fuente.charAt(posición))) posición++; }
        Object leer() {
            saltarEspaciosBlancos(); char valorCarácter = fuente.charAt(posición++);
            if (valorCarácter == '{') {
                Map<String,Object> resultado = new LinkedHashMap<>(); saltarEspaciosBlancos();
                if (fuente.charAt(posición) == '}') { posición++; return resultado; }
                while (true) {
                    String nombre = (String)leer(); saltarEspaciosBlancos(); if (fuente.charAt(posición++) != ':') throw new IllegalArgumentException("Datos valorDelimitador error");
                    resultado.put(nombre, leer()); saltarEspaciosBlancos(); char valorDelimitador = fuente.charAt(posición++);
                    if (valorDelimitador == '}') return resultado; if (valorDelimitador != ',') throw new IllegalArgumentException("Datos valorDelimitador error");
                }
            }
            if (valorCarácter == '[') {
                List<Object> resultado = new ArrayList<>(); saltarEspaciosBlancos();
                if (fuente.charAt(posición) == ']') { posición++; return resultado; }
                while (true) {
                    resultado.add(leer()); saltarEspaciosBlancos(); char valorDelimitador = fuente.charAt(posición++);
                    if (valorDelimitador == ']') return resultado; if (valorDelimitador != ',') throw new IllegalArgumentException("Datos valorDelimitador error");
                }
            }
            if (valorCarácter == '"') {
                StringBuilder resultado = new StringBuilder();
                while (true) {
                    char elementoListaSiguiente = fuente.charAt(posición++); if (elementoListaSiguiente == '"') return resultado.toString();
                    if (elementoListaSiguiente == '\\') {
                        elementoListaSiguiente = fuente.charAt(posición++);
                        if (elementoListaSiguiente == 'u') { resultado.append((char)Integer.parseInt(fuente.substring(posición, posición + 4),16)); posición += 4; continue; }
                        if (elementoListaSiguiente == 'n') elementoListaSiguiente = '\n'; else if (elementoListaSiguiente == 'r') elementoListaSiguiente = '\r'; else if (elementoListaSiguiente == 't') elementoListaSiguiente = '\t';
                        else if (elementoListaSiguiente == 'b') elementoListaSiguiente = '\b'; else if (elementoListaSiguiente == 'f') elementoListaSiguiente = '\f';
                        else if (elementoListaSiguiente != '"' && elementoListaSiguiente != '\\' && elementoListaSiguiente != '/') throw new IllegalArgumentException("Caracteres 이스케이프 error");
                    }
                    resultado.append(elementoListaSiguiente);
                }
            }
            int ponerEnMarcha = posición - 1;
            while (posición < fuente.length() && ",]} \t\r\n".indexOf(fuente.charAt(posición)) < 0) posición++;
            String valor = fuente.substring(ponerEnMarcha, posición);
            if (valor.equals("true")) return Boolean.TRUE; if (valor.equals("false")) return Boolean.FALSE; if (valor.equals("null")) return null;
            return Double.valueOf(valor);
        }
    }
    static String archivoResumenHash(Path ruta) throws Exception {
        MessageDigest resultadoCálculo = MessageDigest.getInstance("SHA-256"); byte[] Datos = new byte[1024 * 1024];
        try (InputStream valorEntrada = Files.newInputStream(ruta)) { for (int longitud; (longitud = valorEntrada.read(Datos)) >= 0;) resultadoCálculo.update(Datos,0,longitud); }
        return textoResumenHash(resultadoCálculo.digest());
    }
    static String textoResumenHash(byte[] Datos) {
        StringBuilder texto = new StringBuilder(); for (byte valor : Datos) texto.append(String.format(Locale.ROOT,"%02x",valor & 255)); return texto.toString();
    }
    static Path rutaInterno(Path raízProyecto, String nombre) {
        Path resultado = raízProyecto.resolve(nombre).normalize();
        if (nombre.isEmpty() || Paths.get(nombre).isAbsolute() || !resultado.startsWith(raízProyecto) || nombre.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ruta: " + nombre);
        for (Path valorSubparte : Paths.get(nombre)) if (valorSubparte.toString().equals("..")) throw new IllegalArgumentException("상위 ruta valorVedado: " + nombre);
        for (Path elementoListaActual = resultado; elementoListaActual != null && elementoListaActual.startsWith(raízProyecto); elementoListaActual = elementoListaActual.getParent())
            if (Files.isSymbolicLink(elementoListaActual)) throw new IllegalArgumentException("dependencias 경로의 링크 valorVedado: " + nombre);
        return resultado;
    }
    static String salidaComando(List<String> comando) throws Exception {
        Process valorProceso = new ProcessBuilder(comando).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String resultado = new String(valorProceso.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (valorProceso.waitFor() != 0) throw new IOException("comando valorFallo: " + comando.get(0)); return resultado;
    }
    static void extraer(Path valorArchivoComprimido, Path valorDestino) throws Exception {
        for (String nombre : salidaComando(Arrays.asList("tar","-tzf",valorArchivoComprimido.toString())).split("\n")) rutaInterno(valorDestino, nombre);
        for (String línea : salidaComando(Arrays.asList("tar","-tvzf",valorArchivoComprimido.toString())).split("\n"))
            if (!línea.isEmpty() && línea.charAt(0) != '-' && línea.charAt(0) != 'd') throw new IOException("valorExterno 링크 또는 valorEspecial 파일을 포함한 dependencias");
        Files.createDirectories(valorDestino);
        int valorEstadoValor = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",valorArchivoComprimido.toString(),"-C",valorDestino.toString()).inheritIO().start().waitFor();
        if (valorEstadoValor != 0) throw new IOException("dependencias valorArchivoComprimido liberarAlmacenamiento valorFallo");
    }
    static void invocar(Path rutaTrabajoEnCurso, Path Herramientas, List<String> argumentos, Map<String,String> entorno) throws Exception {
        List<String> comando = new ArrayList<>(Arrays.asList("python3", Herramientas.toString())); comando.addAll(argumentos);
        ProcessBuilder ejecutarComando = new ProcessBuilder(comando).directory(rutaTrabajoEnCurso.toFile()).inheritIO(); ejecutarComando.environment().putAll(entorno);
        int valorEstadoValor = ejecutarComando.start().waitFor(); if (valorEstadoValor != 0) throw new IOException("Herramientas valorFallo: " + Herramientas + " (" + valorEstadoValor + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argumentos) throws Exception {
        if (argumentos.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String acción = argumentos[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(acción)) throw new IllegalArgumentException("알 númeroValor 없는 acción");
        Path raízProyecto = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ajustes = (Map<String,Object>)new AnalizadorDatos(Files.readString(raízProyecto.resolve("native.json"),StandardCharsets.UTF_8)).leer();
        Path árbolFuente = rutaInterno(raízProyecto,(String)ajustes.get("source")), valorNúcleo = rutaInterno(árbolFuente,(String)ajustes.get("native"));
        List<String> archivosPropioRecurso = (List<String>)(List<?>)ajustes.get("owned_files");
        for (String nombre : archivosPropioRecurso) if (!Files.isRegularFile(rutaInterno(árbolFuente,nombre))) throw new IOException("árbolFuente métodoAusente: " + nombre);
        if (acción.equals("check")) { System.out.println(ajustes.get("country") + " " + ajustes.get("language") + " 독립 árbolFuente verificar esTerminado"); return; }
        String rutaRelativoRecurso = (String)ajustes.getOrDefault("resource_root", ".");
        if (!rutaRelativoRecurso.equals(".") && !rutaRelativoRecurso.equals("..")) throw new IllegalArgumentException("dependencias raízProyecto ruta error");
        Path valorRecurso = raízProyecto.resolve(rutaRelativoRecurso).normalize(); Path valorArchivoComprimido = valorRecurso.resolve("native-vendor.tar.gz");
        String resumenHashEsperado = (String)ajustes.get("vendor_sha256");
        if (!archivoResumenHash(valorArchivoComprimido).equals(resumenHashEsperado)) throw new IOException("dependencias SHA-256 불일치");
        Path valorMarcador = árbolFuente.resolve(".vendor-sha256");
        if (!Files.isRegularFile(valorMarcador) || !Files.readString(valorMarcador).trim().equals(resumenHashEsperado)) { extraer(valorArchivoComprimido, árbolFuente); Files.writeString(valorMarcador,resumenHashEsperado + "\n"); }
        Map<String,String> entorno = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (entorno.containsKey("IP_CONFIG")) ipConfig = Paths.get(entorno.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = raízProyecto; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = árbolFuente.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        entorno.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(acción) && !entorno.containsKey("QEMU_AARCH64")) {
            Path LanzadorPrograma = valorRecurso.resolve("host/qemu"), marcadorLanzador = valorRecurso.resolve("host/.qemu-sha256");
            String resumenHashLanzador = (String)ajustes.get("qemu_sha256");
            if (!Files.isRegularFile(LanzadorPrograma) || !Files.isRegularFile(marcadorLanzador) || !Files.readString(marcadorLanzador).trim().equals(resumenHashLanzador)) {
                Path archivoComprimidoLanzador = valorRecurso.resolve("qemu-host.tar.gz"); if (!archivoResumenHash(archivoComprimidoLanzador).equals(resumenHashLanzador)) throw new IOException("QEMU SHA-256 불일치");
                extraer(archivoComprimidoLanzador,valorRecurso.resolve("host")); Files.writeString(marcadorLanzador,resumenHashLanzador + "\n");
            }
            entorno.put("QEMU_AARCH64",LanzadorPrograma.toString());
        }
        MessageDigest resultadoCálculo = MessageDigest.getInstance("SHA-256"); Collections.sort(archivosPropioRecurso);
        for (String nombre : archivosPropioRecurso) { resultadoCálculo.update(nombre.getBytes(StandardCharsets.UTF_8)); resultadoCálculo.update(Files.readAllBytes(rutaInterno(árbolFuente,nombre))); }
        resultadoCálculo.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); resultadoCálculo.update(Files.readAllBytes(ipConfig));
        String resumenHashFuente = textoResumenHash(resultadoCálculo.digest()); Path construirMarcador = valorNúcleo.resolve("build/worldos-source.sha256");
        if (acción.equals("build") || !Files.isRegularFile(construirMarcador) || !Files.readString(construirMarcador).trim().equals(resumenHashFuente)) {
            invocar(valorNúcleo,rutaInterno(valorNúcleo,(String)ajustes.get("builder")),Collections.emptyList(),entorno);
            Files.writeString(construirMarcador,resumenHashFuente + "\n");
        }
        List<String> argumentosLanzador = new ArrayList<>(Arrays.asList(argumentos).subList(1,argumentos.length));
        if (acción.equals("run") || acción.equals("desktop")) {
            if (acción.equals("desktop")) argumentosLanzador.add(0,"--desktop");
            invocar(valorNúcleo,rutaInterno(valorNúcleo,(String)ajustes.get("runner")),argumentosLanzador,entorno);
        } else if (acción.equals("image")) invocar(valorNúcleo,rutaInterno(valorNúcleo,(String)ajustes.get("image_builder")),argumentosLanzador,entorno);
        else if (acción.equals("test-system")) {
            argumentosLanzador.add(0,raízProyecto.toString()); argumentosLanzador.add(0,"--edition");
            invocar(valorNúcleo,rutaInterno(valorNúcleo,(String)ajustes.get("system_tester")),argumentosLanzador,entorno);
        }
    }
}
