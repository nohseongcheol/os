// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Genera código fuente C para un núcleo ARM64 autónomo a partir de archivos de clases Java. Se ejecuta en el JDK anfitrión. */
public final class CompilaciónAnticipada {
    static final class ErrorTraducción extends RuntimeException {
        ErrorTraducción(String descripción) { super(descripción); }
    }
    static final class LectorDatos {
        final byte[] Datos;
        int posición;
        LectorDatos(byte[] datosEntrada) { Datos = datosEntrada; }
        byte[] leer(int longitud) {
            if (longitud < 0 || longitud > Datos.length - posición) throw new ErrorTraducción("valorRecortado valorClase 또는 comando Datos");
            byte[] resultado = Arrays.copyOfRange(Datos, posición, posición + longitud); posición += longitud; return resultado;
        }
        int leerByte() { if (posición >= Datos.length) throw new ErrorTraducción("valorRecortado comando Datos"); return Datos[posición++] & 255; }
        int leerCorto() { return (leerByte() << 8) | leerByte(); }
        int leerTipoEntero() { return (leerCorto() << 16) | leerCorto(); }
        int leerByteConSigno() { return (byte) leerByte(); }
        int leerCortoConSigno() { return (short) leerCorto(); }
    }
    static final class DatosMiembro {
        final int entradaElementoAcceso;
        final String nombre, valorDescripción;
        final Map<String, byte[]> valorAtributo;
        DatosMiembro(int valorAcceso, String valorNombre, String datosDescriptor, Map<String, byte[]> datosAtributo) {
            entradaElementoAcceso = valorAcceso; nombre = valorNombre; valorDescripción = datosDescriptor; valorAtributo = datosAtributo;
        }
    }
    static final class ReferenciaMétodo implements Comparable<ReferenciaMétodo> {
        final String valorPropietario, nombre, valorDescripción;
        ReferenciaMétodo(String valorPropioRecurso, String valorNombre, String datosDescriptor) { valorPropietario = valorPropioRecurso; nombre = valorNombre; valorDescripción = datosDescriptor; }
        String[] partes() { return new String[]{valorPropietario, nombre, valorDescripción}; }
        public int compareTo(ReferenciaMétodo valorParRed) {
            int valorComparación = valorPropietario.compareTo(valorParRed.valorPropietario);
            if (valorComparación == 0) valorComparación = nombre.compareTo(valorParRed.nombre);
            return valorComparación == 0 ? valorDescripción.compareTo(valorParRed.valorDescripción) : valorComparación;
        }
        public boolean equals(Object valorParRed) { return valorParRed instanceof ReferenciaMétodo && compareTo((ReferenciaMétodo) valorParRed) == 0; }
        public int hashCode() { return Objects.hash(valorPropietario, nombre, valorDescripción); }
    }
    static final class DatosClase {
        final int[] claseTipoConstante;
        final Object[] datosConstante;
        final String nombre;
        final List<DatosMiembro> valorCampo, Función;
        DatosClase(Path ruta) throws IOException {
            LectorDatos valorLector = new LectorDatos(Files.readAllBytes(ruta));
            if (valorLector.leerTipoEntero() != 0xcafebabe) throw new ErrorTraducción("Java valorClase 표식이 아님");
            valorLector.leer(4);
            int númeroElementosElementoLista = valorLector.leerCorto(); claseTipoConstante = new int[númeroElementosElementoLista]; datosConstante = new Object[númeroElementosElementoLista];
            for (int índiceOrdinal = 1; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) {
                int valorClaseTipo = valorLector.leerByte(); claseTipoConstante[índiceOrdinal] = valorClaseTipo;
                switch (valorClaseTipo) {
                    case 1:
                        int longitud = valorLector.leerCorto();
                        byte[] búferCarácter = valorLector.leer(longitud), datosPrefijadoLongitud = new byte[longitud + 2];
                        datosPrefijadoLongitud[0] = (byte)(longitud >> 8); datosPrefijadoLongitud[1] = (byte)longitud;
                        System.arraycopy(búferCarácter, 0, datosPrefijadoLongitud, 2, longitud);
                        datosConstante[índiceOrdinal] = new DataInputStream(new ByteArrayInputStream(datosPrefijadoLongitud)).readUTF(); break;
                    case 3: datosConstante[índiceOrdinal] = valorLector.leerTipoEntero(); break;
                    case 4: valorLector.leer(4); break;
                    case 5: case 6: valorLector.leer(8); índiceOrdinal++; break;
                    case 7: case 8: case 16: datosConstante[índiceOrdinal] = valorLector.leerCorto(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        datosConstante[índiceOrdinal] = new int[]{valorLector.leerCorto(), valorLector.leerCorto()}; break;
                    case 15: datosConstante[índiceOrdinal] = new int[]{valorLector.leerByte(), valorLector.leerCorto()}; break;
                    default: throw new ErrorTraducción("지원하지 않는 valorConstante valorClaseTipo: " + valorClaseTipo);
                }
            }
            valorLector.leerCorto(); nombre = nombreClase(valorLector.leerCorto());
            if (!nombreClase(valorLector.leerCorto()).equals("java/lang/Object") || valorLector.leerCorto() != 0)
                throw new ErrorTraducción(nombre + ": 상속 및 인터페이스 esNoAdmitido");
            valorCampo = leerMiembros(valorLector); Función = leerMiembros(valorLector); leerAtributos(valorLector);
            if (valorLector.posición != valorLector.Datos.length) throw new ErrorTraducción("valorClase 뒤에 남은 Datos");
        }
        String Caracteres(int número) {
            if (número < 1 || número >= claseTipoConstante.length || claseTipoConstante[número] != 1) throw new ErrorTraducción("Caracteres valorConstante número error");
            return (String) datosConstante[número];
        }
        String nombreClase(int número) {
            if (número < 1 || número >= claseTipoConstante.length || claseTipoConstante[número] != 7) throw new ErrorTraducción("valorClase referencia error");
            return Caracteres((Integer)datosConstante[número]);
        }
        ReferenciaMétodo referencia(int número) {
            if (número < 1 || número >= claseTipoConstante.length || claseTipoConstante[número] < 9 || claseTipoConstante[número] > 11) throw new ErrorTraducción("멤버 referencia error");
            int[] valorPar = (int[])datosConstante[número], parNombre = (int[])datosConstante[valorPar[1]];
            return new ReferenciaMétodo(nombreClase(valorPar[0]), Caracteres(parNombre[0]), Caracteres(parNombre[1]));
        }
        Map<String, byte[]> leerAtributos(LectorDatos valorLector) {
            Map<String, byte[]> resultado = new LinkedHashMap<>();
            int númeroElementosElementoLista = valorLector.leerCorto();
            for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) {
                String nombreAtributo = Caracteres(valorLector.leerCorto()); byte[] valor = valorLector.leer(valorLector.leerTipoEntero());
                if (resultado.put(nombreAtributo, valor) != null) throw new ErrorTraducción("겹친 valorAtributo: " + nombreAtributo);
            }
            return resultado;
        }
        List<DatosMiembro> leerMiembros(LectorDatos valorLector) {
            List<DatosMiembro> resultado = new ArrayList<>(); int númeroElementosElementoLista = valorLector.leerCorto();
            for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) {
                int entradaElementoAcceso = valorLector.leerCorto(); String nombreEntradaElementoMétodo = Caracteres(valorLector.leerCorto()), valorDescripción = Caracteres(valorLector.leerCorto());
                resultado.add(new DatosMiembro(entradaElementoAcceso, nombreEntradaElementoMétodo, valorDescripción, leerAtributos(valorLector)));
            }
            return resultado;
        }
    }
    static final class DescriptorMétodo {
        final List<String> argumentos = new ArrayList<>();
        final String resultadoRetornar;
        DescriptorMétodo(String valorDescripción) {
            if (!valorDescripción.startsWith("(")) throw new ErrorTraducción("Función valorDescripción error: " + valorDescripción);
            int terminación = valorDescripción.indexOf(')'); if (terminación < 0) throw new ErrorTraducción("Función valorDescripción error: " + valorDescripción);
            argumentos.addAll(analizarTipos(valorDescripción.substring(1, terminación)));
            List<String> valoresDevuelto = analizarTipos(valorDescripción.substring(terminación + 1));
            if (argumentos.contains("V") || valoresDevuelto.size() != 1) throw new ErrorTraducción("Función valorDescripción error: " + valorDescripción);
            resultadoRetornar = valoresDevuelto.get(0);
        }
    }
    static List<String> analizarTipos(String valorDescripción) {
        List<String> resultado = new ArrayList<>();
        String[] formatoPermitido = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int posición = 0; posición < valorDescripción.length();) {
            String valorSelección = null;
            for (String valorFormato : formatoPermitido) if (valorDescripción.startsWith(valorFormato, posición)) { valorSelección = valorFormato; break; }
            if (valorSelección == null) throw new ErrorTraducción("지원하지 않는 tipoDatos: " + valorDescripción);
            resultado.add(valorSelección); posición += valorSelección.length();
        }
        return resultado;
    }
    static String símbolo(String valorClaseTipo, String... partes) {
        try {
            byte[] archivoResumenHash = MessageDigest.getInstance("SHA-256").digest(String.join("\0", partes).getBytes(StandardCharsets.UTF_8));
            StringBuilder texto = new StringBuilder("j_" + valorClaseTipo + "_");
            for (int índiceOrdinal = 0; índiceOrdinal < 12; índiceOrdinal++) texto.append(String.format(Locale.ROOT, "%02x", archivoResumenHash[índiceOrdinal] & 255));
            return texto.toString();
        } catch (Exception error) { throw new ErrorTraducción(error.toString()); }
    }
    final Map<String, DatosClase> listaClases = new TreeMap<>();
    final Map<ReferenciaMétodo, DatosMiembro> listaMétodos = new TreeMap<>(), listaCampos = new TreeMap<>();
    final Map<String, String> valoresCadena = new LinkedHashMap<>(), funcionesMáquina = new LinkedHashMap<>();
    final String objetivoEjecución, claseMáquina;
    final int númeroElementosPalabraMontículo;
    final Path rutaRecurso;
    CompilaciónAnticipada(List<Path> listaRuta, String valorObjetivo, int númeroElementosPalabraLéxico, Path valorRecurso) throws IOException {
        if ((!valorObjetivo.equals("kernel") && !valorObjetivo.equals("user")) || númeroElementosPalabraLéxico < 1024 || númeroElementosPalabraLéxico > 1048576) throw new ErrorTraducción("ejecutarComando valorObjetivo 또는 Memoria regiónDirección tamaño error");
        objetivoEjecución = valorObjetivo; númeroElementosPalabraMontículo = númeroElementosPalabraLéxico; rutaRecurso = valorRecurso;
        // Este nombre también se traduce al generar las fuentes de cada país.
        claseMáquina = valorObjetivo.equals("kernel") ? "Placa" : "Usuario";
        for (String línea : Files.readAllLines(valorRecurso.resolve("FuncionesMáquina.tsv"), StandardCharsets.UTF_8)) {
            String[] partes = línea.split("\t", -1);
            if (partes.length != 4) throw new ErrorTraducción("máquina Función Datos error");
            if (partes[0].equals(valorObjetivo)) funcionesMáquina.put(partes[1] + partes[2], partes[3]);
        }
        for (Path ruta : listaRuta) {
            DatosClase Datos = new DatosClase(ruta);
            if (listaClases.put(Datos.nombre, Datos) != null) throw new ErrorTraducción("중복 valorClase: " + Datos.nombre);
            for (DatosMiembro valorCampo : Datos.valorCampo) {
                if ((valorCampo.entradaElementoAcceso & 8) == 0 || analizarTipos(valorCampo.valorDescripción).equals(Collections.singletonList("V"))) throw new ErrorTraducción("valorEstático 필드만 valorSoporte");
                if (listaCampos.put(new ReferenciaMétodo(Datos.nombre, valorCampo.nombre, valorCampo.valorDescripción), valorCampo) != null) throw new ErrorTraducción("중복 valorCampo");
            }
            for (DatosMiembro Función : Datos.Función) {
                if (Función.nombre.equals("<init>")) continue;
                if ((Función.entradaElementoAcceso & 8) == 0 || (Función.entradaElementoAcceso & (0x20 | 0x400)) != 0) throw new ErrorTraducción("valorEstático 비동기화 함수만 valorSoporte");
                new DescriptorMétodo(Función.valorDescripción);
                if (listaMétodos.put(new ReferenciaMétodo(Datos.nombre, Función.nombre, Función.valorDescripción), Función) != null) throw new ErrorTraducción("중복 Función");
            }
        }
    }
    String símboloCadena(String texto) { return valoresCadena.computeIfAbsent(texto, valor -> "j_text_" + valoresCadena.size()); }
    String expresiónConstante(DatosClase Datos, int número) {
        if (número < 1 || número >= Datos.claseTipoConstante.length) throw new ErrorTraducción("valorConstante número recortar error");
        if (Datos.claseTipoConstante[número] == 3) return "(word)(uint32_t)(" + Datos.datosConstante[número] + ")";
        if (Datos.claseTipoConstante[número] == 8) return "(word)" + símboloCadena(Datos.Caracteres((Integer)Datos.datosConstante[número]));
        throw new ErrorTraducción("정수와 Cadena 상수만 valorSoporte");
    }
    String prototipoMétodo(ReferenciaMétodo referencia) {
        List<String> listaArgumentos = new ArrayList<>(); int númeroElementosElementoLista = new DescriptorMétodo(referencia.valorDescripción).argumentos.size();
        for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) listaArgumentos.add("word a" + índiceOrdinal);
        return "static word " + símbolo("method", referencia.partes()) + "(" + (númeroElementosElementoLista == 0 ? "void" : String.join(", ", listaArgumentos)) + ")";
    }
    void comprobarLocal(int número, int númeroElementosVariableLocal) { if (número < 0 || número >= númeroElementosVariableLocal) throw new ErrorTraducción("ámbitoLocal valorVariable número recortar error"); }
    void emitirRama(List<String> Salida, Set<Integer> listaRama, int posición, int importeMovimiento, String condición) {
        int valorDestino = posición + importeMovimiento; listaRama.add(valorDestino);
        Salida.add((condición == null ? "" : "if (" + condición + ") ") + "goto b" + valorDestino + ";");
    }
    String cuerpoMétodo(ReferenciaMétodo Función, DatosMiembro Datos) {
        byte[] datosCuerpo = Datos.valorAtributo.get("Code"); if (datosCuerpo == null) throw new ErrorTraducción("Función 몸체가 métodoAusente: " + Función.nombre);
        LectorDatos valorLector = new LectorDatos(datosCuerpo); int profundidadPila = valorLector.leerCorto(), númeroElementosVariableLocal = valorLector.leerCorto();
        LectorDatos datosComando = new LectorDatos(valorLector.leer(valorLector.leerTipoEntero()));
        if (valorLector.leerCorto() != 0) throw new ErrorTraducción("try/catch/finally esNoAdmitido");
        DescriptorMétodo valorFormato = new DescriptorMétodo(Función.valorDescripción); if (númeroElementosVariableLocal < valorFormato.argumentos.size()) throw new ErrorTraducción("매개변수보다 적은 ámbitoLocal valorVariable");
        DatosClase valorClase = listaClases.get(Función.valorPropietario);
        List<String> Salida = new ArrayList<>(); Salida.add(prototipoMétodo(Función) + " {");
        Salida.add("word s[" + Math.max(profundidadPila, 1) + "], l[" + Math.max(númeroElementosVariableLocal, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int índiceOrdinal = 0; índiceOrdinal < valorFormato.argumentos.size(); índiceOrdinal++) Salida.add("l[" + índiceOrdinal + "] = a" + índiceOrdinal + ";");
        Set<Integer> listaFronteras = new HashSet<>(), listaRama = new HashSet<>();
        String[] listaComparaciones = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (datosComando.posición < datosComando.Datos.length) {
            int posición = datosComando.posición, comando = datosComando.leerByte(); listaFronteras.add(posición); Salida.add("b" + posición + ":;");
            if (comando == 0) continue;
            if (comando == 1) Salida.add("PUSH(0);");
            else if (comando >= 2 && comando <= 8) Salida.add("PUSH((uint32_t)(" + (comando - 3) + "));");
            else if (comando == 16 || comando == 17) Salida.add("PUSH((uint32_t)(" + (comando == 16 ? datosComando.leerByteConSigno() : datosComando.leerCortoConSigno()) + "));");
            else if (comando == 18 || comando == 19) Salida.add("PUSH(" + expresiónConstante(valorClase, comando == 18 ? datosComando.leerByte() : datosComando.leerCorto()) + ");");
            else if (comando == 21 || comando == 25 || (comando >= 26 && comando <= 29) || (comando >= 42 && comando <= 45)) {
                int número = comando == 21 || comando == 25 ? datosComando.leerByte() : comando - (comando <= 29 ? 26 : 42);
                comprobarLocal(número, númeroElementosVariableLocal); Salida.add("PUSH(l[" + número + "]);");
            } else if (comando == 54 || comando == 58 || (comando >= 59 && comando <= 62) || (comando >= 75 && comando <= 78)) {
                int número = comando == 54 || comando == 58 ? datosComando.leerByte() : comando - (comando <= 62 ? 59 : 75);
                comprobarLocal(número, númeroElementosVariableLocal); Salida.add("l[" + número + "] = POP();");
            } else if (comando == 46) Salida.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (comando == 79) Salida.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (comando == 87 || comando == 88) Salida.add(comando == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (comando >= 89 && comando <= 95) {
                int[] conteosElementoLista = {1,2,3,2,3,4,2}; String[] listaOrden = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int índiceOrdinal = 0; índiceOrdinal < conteosElementoLista[comando - 89]; índiceOrdinal++) Salida.add("abcd".charAt(índiceOrdinal) + " = POP();");
                for (char valor : listaOrden[comando - 89].toCharArray()) Salida.add("PUSH(" + valor + ");");
            } else if (comando == 96 || comando == 100 || comando == 104 || comando == 126 || comando == 128 || comando == 130) {
                String valorOperación = comando == 96 ? "+" : comando == 100 ? "-" : comando == 104 ? "*" : comando == 126 ? "&" : comando == 128 ? "|" : "^";
                Salida.add("b = POP(); a = POP(); PUSH((uint32_t)a " + valorOperación + " (uint32_t)b);");
            } else if (comando == 108 || comando == 112) Salida.add("b = POP(); a = POP(); PUSH(divide(a,b," + (comando == 112 ? 1 : 0) + "));");
            else if (comando == 116) Salida.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (comando == 120 || comando == 122 || comando == 124) {
                Salida.add("b = POP(); a = POP();"); Salida.add("PUSH(" + (comando == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (comando == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (comando == 132) {
                int número = datosComando.leerByte(), importeIncremento = datosComando.leerByteConSigno(); comprobarLocal(número, númeroElementosVariableLocal);
                Salida.add("l[" + número + "] = (uint32_t)l[" + número + "] + (uint32_t)(" + importeIncremento + ");");
            } else if (comando >= 145 && comando <= 147) Salida.add("a = POP(); PUSH((uint32_t)(" + (comando == 145 ? "int8_t" : comando == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (comando >= 153 && comando <= 158) {
                Salida.add("a = POP();"); emitirRama(Salida, listaRama, posición, datosComando.leerCortoConSigno(), "(int32_t)a " + listaComparaciones[comando - 153] + " 0");
            } else if (comando >= 159 && comando <= 166) {
                Salida.add("b = POP(); a = POP();"); emitirRama(Salida, listaRama, posición, datosComando.leerCortoConSigno(), comando >= 165 ? "a " + listaComparaciones[comando - 159] + " b" : "(int32_t)a " + listaComparaciones[comando - 159] + " (int32_t)b");
            } else if (comando == 167 || comando == 200) emitirRama(Salida, listaRama, posición, comando == 167 ? datosComando.leerCortoConSigno() : datosComando.leerTipoEntero(), null);
            else if (comando == 170 || comando == 171) {
                while (datosComando.posición % 4 != 0) datosComando.leerByte();
                int valorPredeterminado = datosComando.leerTipoEntero(); Salida.add("a = POP();");
                if (comando == 170) {
                    int valorExtremoInferior = datosComando.leerTipoEntero(), valorExtremoSuperior = datosComando.leerTipoEntero(); long númeroElementosElementoLista = (long)valorExtremoSuperior - valorExtremoInferior + 1;
                    if (númeroElementosElementoLista < 1 || númeroElementosElementoLista > (datosComando.Datos.length - datosComando.posición) / 4) throw new ErrorTraducción("switch recortar error");
                    for (long valor = valorExtremoInferior; valor <= valorExtremoSuperior; valor++) emitirRama(Salida, listaRama, posición, datosComando.leerTipoEntero(), "(int32_t)a == (" + valor + ")");
                } else {
                    int númeroElementosElementoLista = datosComando.leerTipoEntero(), datosLadoDelantero = 0;
                    if (númeroElementosElementoLista < 0 || númeroElementosElementoLista > (datosComando.Datos.length - datosComando.posición) / 8) throw new ErrorTraducción("switch tamaño error");
                    for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) {
                        int valor = datosComando.leerTipoEntero(); if (índiceOrdinal > 0 && valor <= datosLadoDelantero) throw new ErrorTraducción("switch valorOrden error"); datosLadoDelantero = valor;
                        emitirRama(Salida, listaRama, posición, datosComando.leerTipoEntero(), "(int32_t)a == (" + valor + ")");
                    }
                }
                emitirRama(Salida, listaRama, posición, valorPredeterminado, null);
            } else if (comando == 172 || comando == 176 || comando == 177) Salida.add("return " + (comando == 177 ? "0" : "POP()") + ";");
            else if (comando == 178 || comando == 179) {
                ReferenciaMétodo referencia = valorClase.referencia(datosComando.leerCorto()); if (!listaCampos.containsKey(referencia)) throw new ErrorTraducción("알 númeroValor 없는 valorCampo");
                Salida.add(símbolo("init", referencia.valorPropietario) + "();"); String valorCampo = símbolo("field", referencia.partes());
                Salida.add(comando == 178 ? "PUSH(" + valorCampo + ");" : valorCampo + " = POP();");
            } else if (comando == 184) {
                ReferenciaMétodo referencia = valorClase.referencia(datosComando.leerCorto()); if (!listaMétodos.containsKey(referencia)) throw new ErrorTraducción("알 númeroValor 없는 Función");
                DescriptorMétodo tipoInvocación = new DescriptorMétodo(referencia.valorDescripción); int númeroElementosElementoLista = tipoInvocación.argumentos.size();
                Salida.add(símbolo("init", referencia.valorPropietario) + "();"); Salida.add("if(sp < " + númeroElementosElementoLista + ") kernel_panic(\"call stack underflow\"); sp -= " + númeroElementosElementoLista + ";");
                List<String> argumentosInvocación = new ArrayList<>(); for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) argumentosInvocación.add("s[sp + " + índiceOrdinal + "]");
                Salida.add("a = " + símbolo("method", referencia.partes()) + "(" + String.join(",", argumentosInvocación) + ");");
                if (!tipoInvocación.resultadoRetornar.equals("V")) Salida.add("PUSH(a);");
            } else if (comando == 182) {
                ReferenciaMétodo referencia = valorClase.referencia(datosComando.leerCorto());
                if (referencia.equals(new ReferenciaMétodo("java/lang/String", "length", "()I"))) Salida.add("a = POP(); PUSH(length(a));");
                else if (referencia.equals(new ReferenciaMétodo("java/lang/String", "charAt", "(I)C"))) Salida.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new ErrorTraducción("가상 Función invocar esNoAdmitido");
            } else if (comando == 188) {
                if (datosComando.leerByte() != 10) throw new ErrorTraducción("new int[]만 valorSoporte"); Salida.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (comando == 190) Salida.add("a = POP(); PUSH(length(a));");
            else if (comando == 196) {
                int valorExtensión = datosComando.leerByte(), número = datosComando.leerCorto(); comprobarLocal(número, númeroElementosVariableLocal);
                if (valorExtensión == 21 || valorExtensión == 25) Salida.add("PUSH(l[" + número + "]);");
                else if (valorExtensión == 54 || valorExtensión == 58) Salida.add("l[" + número + "] = POP();");
                else if (valorExtensión == 132) Salida.add("l[" + número + "] = (uint32_t)l[" + número + "] + (uint32_t)(" + datosComando.leerCortoConSigno() + ");");
                else throw new ErrorTraducción("esNoAdmitido wide comando");
            } else if (comando == 198 || comando == 199) {
                Salida.add("a = POP();"); emitirRama(Salida, listaRama, posición, datosComando.leerCortoConSigno(), "a " + (comando == 198 ? "==" : "!=") + " 0");
            } else throw new ErrorTraducción(Función.valorPropietario + "." + Función.nombre + ", valorByte " + posición + ": esNoAdmitido comando " + comando);
        }
        if (!listaFronteras.containsAll(listaRama)) throw new ErrorTraducción("comando 경계가 아닌 곳으로 rama");
        Salida.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Salida);
    }
    String métodoExportar(String símboloEnlazar, String valorObjetivo, boolean tienePuntoEntradaElemento) {
        int índicePosición = valorObjetivo.lastIndexOf('.'); if (índicePosición < 0 || !símboloEnlazar.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ErrorTraducción("emitirValor valorAsignar error");
        String valorPropietario = valorObjetivo.substring(0, índicePosición).replace('.', '/'), nombre = valorObjetivo.substring(índicePosición + 1); ReferenciaMétodo valorSelección = null;
        for (ReferenciaMétodo referencia : listaMétodos.keySet()) if (referencia.valorPropietario.equals(valorPropietario) && referencia.nombre.equals(nombre)) {
            if (valorSelección != null) throw new ErrorTraducción("겹친 emitirValor valorObjetivo"); valorSelección = referencia;
        }
        if (valorSelección == null || (listaMétodos.get(valorSelección).entradaElementoAcceso & 0x100) != 0) throw new ErrorTraducción("내보낼 함수가 métodoAusente 또는 native Función");
        DescriptorMétodo valorFormato = new DescriptorMétodo(valorSelección.valorDescripción);
        if ((tienePuntoEntradaElemento && !valorFormato.argumentos.isEmpty()) || !Arrays.asList("V", "I").contains(valorFormato.resultadoRetornar)) throw new ErrorTraducción("valorPuntoEntradaElemento 또는 C valorFrontera valorFormato error");
        List<String> listaArgumentos = new ArrayList<>(), argumentosInvocación = new ArrayList<>();
        for (int índiceOrdinal = 0; índiceOrdinal < valorFormato.argumentos.size(); índiceOrdinal++) {
            if (!valorFormato.argumentos.get(índiceOrdinal).equals("I")) throw new ErrorTraducción("C 경계는 int 인수만 valorSoporte");
            listaArgumentos.add("int32_t a" + índiceOrdinal); argumentosInvocación.add("(uint32_t)a" + índiceOrdinal);
        }
        return (valorFormato.resultadoRetornar.equals("V") ? "void " : "int32_t ") + símboloEnlazar + "(" + (listaArgumentos.isEmpty() ? "void" : String.join(",", listaArgumentos)) + ") { " + símbolo("init", valorSelección.valorPropietario) + "(); " + (valorFormato.resultadoRetornar.equals("V") ? "" : "return (int32_t)") + símbolo("method", valorSelección.partes()) + "(" + String.join(",", argumentosInvocación) + "); }";
    }
    String generar(String puntoEntradaElemento, List<String> entradasExportar, boolean notaciónUniversal) throws IOException {
        List<String> listaDeclaraciones = new ArrayList<>(), listaCuerpos = new ArrayList<>(), declaracionesCampo = new ArrayList<>();
        for (Map.Entry<ReferenciaMétodo, DatosMiembro> valorEntradaElemento : listaMétodos.entrySet()) {
            ReferenciaMétodo referencia = valorEntradaElemento.getKey(); DatosMiembro Datos = valorEntradaElemento.getValue(); listaDeclaraciones.add(prototipoMétodo(referencia) + ";");
            if ((Datos.entradaElementoAcceso & 0x100) != 0) {
                String conectar = funcionesMáquina.get(referencia.nombre + referencia.valorDescripción);
                if (!referencia.valorPropietario.equals(claseMáquina) || conectar == null) throw new ErrorTraducción("허용되지 않은 native Función: " + referencia.nombre);
                int númeroElementosElementoLista = new DescriptorMétodo(referencia.valorDescripción).argumentos.size(); List<String> listaArgumentos = new ArrayList<>();
                for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) listaArgumentos.add("a" + índiceOrdinal);
                listaDeclaraciones.add("extern word " + conectar + "(" + (númeroElementosElementoLista == 0 ? "void" : String.join(",", Collections.nCopies(númeroElementosElementoLista, "word"))) + ");");
                listaCuerpos.add(prototipoMétodo(referencia) + " { return " + conectar + "(" + String.join(",", listaArgumentos) + "); }");
            } else listaCuerpos.add(cuerpoMétodo(referencia, Datos));
        }
        for (Map.Entry<ReferenciaMétodo, DatosMiembro> valorEntradaElemento : listaCampos.entrySet()) {
            ReferenciaMétodo referencia = valorEntradaElemento.getKey(); byte[] valorConstante = valorEntradaElemento.getValue().valorAtributo.get("ConstantValue");
            String valor = valorConstante == null ? "0" : expresiónConstante(listaClases.get(referencia.valorPropietario), new LectorDatos(valorConstante).leerCorto());
            declaracionesCampo.add("static word " + símbolo("field", referencia.partes()) + " = " + valor + ";");
        }
        for (String nombre : listaClases.keySet()) {
            String inicializar = símbolo("init", nombre), valorEstadoValor = símbolo("state", nombre);
            listaDeclaraciones.add("static void " + inicializar + "(void);"); declaracionesCampo.add("static unsigned " + valorEstadoValor + ";");
            ReferenciaMétodo referencia = new ReferenciaMétodo(nombre, "<clinit>", "()V");
            listaCuerpos.add("static void " + inicializar + "(void) { if(" + valorEstadoValor + ") return; " + valorEstadoValor + " = 1; " + (listaMétodos.containsKey(referencia) ? símbolo("method", referencia.partes()) + "(); " : "") + valorEstadoValor + " = 2; }");
        }
        listaCuerpos.add(métodoExportar("java_entry", puntoEntradaElemento, true)); Set<String> nombreExportado = new HashSet<>();
        for (String valorAsignar : entradasExportar) {
            int índicePosición = valorAsignar.indexOf('='); if (índicePosición < 1) throw new ErrorTraducción("emitirValor valorAsignar error");
            String nombre = valorAsignar.substring(0, índicePosición); nombreExportado.add(nombre); listaCuerpos.add(métodoExportar(nombre, valorAsignar.substring(índicePosición + 1), false));
        }
        List<String> declaracionesCadena = new ArrayList<>();
        for (Map.Entry<String, String> valorEntradaElemento : valoresCadena.entrySet()) {
            String texto = valorEntradaElemento.getKey(); StringBuilder valorArreglo = new StringBuilder("static const word " + valorEntradaElemento.getValue() + "[] = {" + texto.length());
            for (int índiceOrdinal = 0; índiceOrdinal < texto.length(); índiceOrdinal++) valorArreglo.append(", ").append((int)texto.charAt(índiceOrdinal));
            declaracionesCadena.add(valorArreglo.append("};").toString());
        }
        String valorSoporte = Files.readString(rutaRecurso.resolve("SoporteEntornoEjecución.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(númeroElementosPalabraMontículo));
        return localizarFuenteGenerado(valorSoporte + String.join("\n", declaracionesCadena) + "\n" + String.join("\n", listaDeclaraciones) + "\n" + String.join("\n", declaracionesCampo) + "\n" + String.join("\n", listaCuerpos) + "\n", nombreExportado, notaciónUniversal);
    }
    String localizarFuenteGenerado(String fuente, Set<String> nombreExportado, boolean notaciónUniversal) throws IOException {
        Map<String, String> tablaNombre = new HashMap<>();
        for (String línea : Files.readAllLines(rutaRecurso.resolve("NombresGenerado.tsv"), StandardCharsets.UTF_8)) {
            String[] valorPar = línea.split("\t"); tablaNombre.put(valorPar[0], valorPar[1]);
        }
        Pattern expresiónFragmentoBloque = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher valorBuscador = expresiónFragmentoBloque.matcher(fuente); StringBuffer resultado = new StringBuffer();
        while (valorBuscador.find()) {
            String nombre = valorBuscador.group(), nombreNuevo = nombre;
            if (!nombre.startsWith("//") && !nombre.startsWith("/*") && !nombre.startsWith("\"") && !nombre.startsWith("'") && !nombreExportado.contains(nombre)) {
                nombreNuevo = tablaNombre.getOrDefault(nombre, nombre);
                if (nombre.matches("a[0-9]+")) nombreNuevo = "argumentos" + nombre.substring(1);
                if (nombre.matches("b[0-9]+")) nombreNuevo = "rama" + nombre.substring(1);
                if (notaciónUniversal) {
                    StringBuilder valorNotación = new StringBuilder();
                    for (char valorCarácter : nombreNuevo.toCharArray()) valorNotación.append(valorCarácter < 128 ? Character.toString(valorCarácter) : String.format(Locale.ROOT, "\\u%04x", (int)valorCarácter));
                    nombreNuevo = valorNotación.toString();
                }
            }
            valorBuscador.appendReplacement(resultado, Matcher.quoteReplacement(nombreNuevo));
        }
        valorBuscador.appendTail(resultado); return resultado.toString();
    }
    String cuerpoMétodoX86(ReferenciaMétodo Función, DatosMiembro Datos, Map<String,String> tablaMáquina, String valorObjetivo) {
        String valorMarcador = símbolo("method", Función.partes());
        List<String> línea = new ArrayList<>();
        if ((Datos.entradaElementoAcceso & 0x100) != 0) {
            String conectar = tablaMáquina.get(Función.nombre + Función.valorDescripción);
            if (!Función.valorPropietario.equals(valorObjetivo.equals("kernel") ? "Dispositivo" : "Usuario") || conectar == null) throw new ErrorTraducción("허용되지 않은 native Función");
            return ".text\n" + valorMarcador + ":\njmp " + conectar;
        }
        byte[] textoCuerpo = Datos.valorAtributo.get("Code"); if (textoCuerpo == null) throw new ErrorTraducción("Función 몸체가 métodoAusente");
        LectorDatos valorLector = new LectorDatos(textoCuerpo); valorLector.leerCorto(); int númeroElementosLocal = valorLector.leerCorto();
        LectorDatos datosComando = new LectorDatos(valorLector.leer(valorLector.leerTipoEntero()));
        if (valorLector.leerCorto() != 0) throw new ErrorTraducción("try/catch/finally esNoAdmitido");
        DescriptorMétodo valorFormato = new DescriptorMétodo(Función.valorDescripción); if (númeroElementosLocal < valorFormato.argumentos.size()) throw new ErrorTraducción("매개변수보다 적은 ámbitoLocal valorVariable");
        Collections.addAll(línea,".text",".globl " + valorMarcador,".type " + valorMarcador + ", @function",valorMarcador + ":","pushl %ebp","movl %esp, %ebp","subl $" + númeroElementosLocal * 4 + ", %esp");
        for (int índiceOrdinal = 0; índiceOrdinal < valorFormato.argumentos.size(); índiceOrdinal++) Collections.addAll(línea,"movl " + (8 + 4 * (valorFormato.argumentos.size() - índiceOrdinal - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (índiceOrdinal + 1)) + "(%ebp)");
        DatosClase valorClase = listaClases.get(Función.valorPropietario); Set<Integer> listaFronteras = new HashSet<>(), listaRama = new HashSet<>();
        String[] listaComparaciones = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (datosComando.posición < datosComando.Datos.length) {
            int posición = datosComando.posición, comando = datosComando.leerByte(); String índicePosición = valorMarcador + "_b" + posición;
            línea.add(índicePosición + ":"); listaFronteras.add(posición);
            if (comando == 0) línea.add("nop");
            else if (comando == 1) línea.add("pushl $0");
            else if (comando >= 2 && comando <= 8) línea.add("pushl $" + (comando - 3));
            else if (comando == 16 || comando == 17) línea.add("pushl $" + (comando == 16 ? datosComando.leerByteConSigno() : datosComando.leerCortoConSigno()));
            else if (comando == 18 || comando == 19) {
                int número = comando == 18 ? datosComando.leerByte() : datosComando.leerCorto();
                línea.add("pushl $" + constanteX86(valorClase,número));
            } else if (comando == 21 || comando == 25 || (comando >= 26 && comando <= 29) || (comando >= 42 && comando <= 45) || comando == 54 || comando == 58 || (comando >= 59 && comando <= 62) || (comando >= 75 && comando <= 78)) {
                boolean leerResultado = comando < 54; int número = comando == 21 || comando == 25 || comando == 54 || comando == 58 ? datosComando.leerByte() : comando - (comando <= 29 ? 26 : comando <= 45 ? 42 : comando <= 62 ? 59 : 75);
                comprobarLocal(número,númeroElementosLocal); línea.add((leerResultado ? "pushl " : "popl ") + "-" + (4 * (número + 1)) + "(%ebp)");
            } else if (comando == 46) Collections.addAll(línea,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (comando == 79) Collections.addAll(línea,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (comando == 87 || comando == 88) línea.add("addl $" + (comando == 87 ? 4 : 8) + ", %esp");
            else if (comando >= 89 && comando <= 95) {
                int[] conteosElementoLista = {1,2,3,2,3,4,2}; int[][] listaOrden = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] registroValores = {"%eax","%ecx","%edx","%ebx"};
                for (int índiceOrdinal = 0; índiceOrdinal < conteosElementoLista[comando - 89]; índiceOrdinal++) línea.add("popl " + registroValores[índiceOrdinal]);
                for (int índiceOrdinal : listaOrden[comando - 89]) línea.add("pushl " + registroValores[índiceOrdinal]);
            } else if (comando == 96 || comando == 100 || comando == 104 || comando == 126 || comando == 128 || comando == 130) {
                String valorOperación = comando == 96 ? "addl" : comando == 100 ? "subl" : comando == 104 ? "imull" : comando == 126 ? "andl" : comando == 128 ? "orl" : "xorl";
                Collections.addAll(línea,"popl %ecx","popl %eax",valorOperación + " %ecx, %eax","pushl %eax");
            } else if (comando == 108 || comando == 112) Collections.addAll(línea,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + índicePosición + "_divide","cmpl $0x80000000, %eax","jne " + índicePosición + "_divide","xorl %edx, %edx","jmp " + índicePosición + "_done",índicePosición + "_divide:","cltd","idivl %ecx",índicePosición + "_done:","pushl " + (comando == 108 ? "%eax" : "%edx"));
            else if (comando == 116) línea.add("negl (%esp)");
            else if (comando == 120 || comando == 122 || comando == 124) Collections.addAll(línea,"popl %ecx","popl %eax",(comando == 120 ? "sall" : comando == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (comando == 132) {
                int número = datosComando.leerByte(), valorIncremento = datosComando.leerByteConSigno(); comprobarLocal(número,númeroElementosLocal); línea.add("addl $" + valorIncremento + ", -" + (4 * (número + 1)) + "(%ebp)");
            } else if (comando >= 145 && comando <= 147) Collections.addAll(línea,"popl %eax",comando == 145 ? "movsbl %al, %eax" : comando == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (comando >= 153 && comando <= 166) {
                if (comando <= 158) Collections.addAll(línea,"popl %eax","testl %eax, %eax");
                else Collections.addAll(línea,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int valorDestino = posición + datosComando.leerCortoConSigno(); listaRama.add(valorDestino); línea.add(listaComparaciones[comando - (comando <= 158 ? 153 : 159)] + " " + valorMarcador + "_b" + valorDestino);
            } else if (comando == 167 || comando == 200) {
                int valorDestino = posición + (comando == 167 ? datosComando.leerCortoConSigno() : datosComando.leerTipoEntero()); listaRama.add(valorDestino); línea.add("jmp " + valorMarcador + "_b" + valorDestino);
            } else if (comando == 170 || comando == 171) {
                while (datosComando.posición % 4 != 0) datosComando.leerByte();
                int valorPredeterminado = posición + datosComando.leerTipoEntero(); listaRama.add(valorPredeterminado); línea.add("popl %eax");
                int númeroElementosElementoLista, valorExtremoInferior = 0;
                if (comando == 170) { valorExtremoInferior = datosComando.leerTipoEntero(); int valorExtremoSuperior = datosComando.leerTipoEntero(); long longitud = (long)valorExtremoSuperior - valorExtremoInferior + 1; if (longitud < 1 || longitud > (datosComando.Datos.length - datosComando.posición) / 4) throw new ErrorTraducción("switch recortar error"); númeroElementosElementoLista = (int)longitud; }
                else { númeroElementosElementoLista = datosComando.leerTipoEntero(); if (númeroElementosElementoLista < 0 || númeroElementosElementoLista > (datosComando.Datos.length - datosComando.posición) / 8) throw new ErrorTraducción("switch tamaño error"); }
                for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) {
                    int valor = comando == 170 ? valorExtremoInferior + índiceOrdinal : datosComando.leerTipoEntero(), valorDestino = posición + datosComando.leerTipoEntero(); listaRama.add(valorDestino);
                    Collections.addAll(línea,"cmpl $" + valor + ", %eax","je " + valorMarcador + "_b" + valorDestino);
                }
                línea.add("jmp " + valorMarcador + "_b" + valorPredeterminado);
            } else if (comando == 172 || comando == 176 || comando == 177) {
                if (comando != 177) línea.add("popl %eax"); Collections.addAll(línea,"leave","ret");
            } else if (comando == 178 || comando == 179) {
                ReferenciaMétodo referencia = valorClase.referencia(datosComando.leerCorto()); if (!listaCampos.containsKey(referencia)) throw new ErrorTraducción("알 númeroValor 없는 valorCampo");
                Collections.addAll(línea,"call " + símbolo("init",referencia.valorPropietario),(comando == 178 ? "pushl " : "popl ") + símbolo("field",referencia.partes()));
            } else if (comando == 184) {
                ReferenciaMétodo referencia = valorClase.referencia(datosComando.leerCorto()); if (!listaMétodos.containsKey(referencia)) throw new ErrorTraducción("알 númeroValor 없는 Función");
                DescriptorMétodo tipoInvocación = new DescriptorMétodo(referencia.valorDescripción); Collections.addAll(línea,"call " + símbolo("init",referencia.valorPropietario),"call " + símbolo("method",referencia.partes()));
                if (!tipoInvocación.argumentos.isEmpty()) línea.add("addl $" + tipoInvocación.argumentos.size() * 4 + ", %esp");
                if (!tipoInvocación.resultadoRetornar.equals("V")) línea.add("pushl %eax");
            } else if (comando == 182) {
                ReferenciaMétodo referencia = valorClase.referencia(datosComando.leerCorto());
                if (referencia.equals(new ReferenciaMétodo("java/lang/String","length","()I"))) Collections.addAll(línea,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (referencia.equals(new ReferenciaMétodo("java/lang/String","charAt","(I)C"))) Collections.addAll(línea,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new ErrorTraducción("가상 Función invocar esNoAdmitido");
            } else if (comando == 188) {
                if (datosComando.leerByte() != 10) throw new ErrorTraducción("new int[]만 valorSoporte"); Collections.addAll(línea,"popl %eax","call rt_new_array","pushl %eax");
            } else if (comando == 190) Collections.addAll(línea,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (comando == 196) {
                int valorExtensión = datosComando.leerByte(), número = datosComando.leerCorto(); comprobarLocal(número,númeroElementosLocal);
                if (valorExtensión == 21 || valorExtensión == 25 || valorExtensión == 54 || valorExtensión == 58) línea.add((valorExtensión <= 25 ? "pushl " : "popl ") + "-" + 4 * (número + 1) + "(%ebp)");
                else if (valorExtensión == 132) línea.add("addl $" + datosComando.leerCortoConSigno() + ", -" + 4 * (número + 1) + "(%ebp)");
                else throw new ErrorTraducción("wide comando esNoAdmitido");
            } else if (comando == 198 || comando == 199) {
                int valorDestino = posición + datosComando.leerCortoConSigno(); listaRama.add(valorDestino); Collections.addAll(línea,"popl %eax","testl %eax, %eax",(comando == 198 ? "je " : "jne ") + valorMarcador + "_b" + valorDestino);
            } else throw new ErrorTraducción("esNoAdmitido comando: " + comando);
        }
        if (!listaFronteras.containsAll(listaRama)) throw new ErrorTraducción("comando 경계가 아닌 곳으로 rama");
        línea.add(".size " + valorMarcador + ", .-" + valorMarcador); return String.join("\n",línea);
    }
    String constanteX86(DatosClase Datos, int número) {
        if (Datos.claseTipoConstante[número] == 3) return Datos.datosConstante[número].toString();
        if (Datos.claseTipoConstante[número] == 8) return símboloCadena(Datos.Caracteres((Integer)Datos.datosConstante[número]));
        throw new ErrorTraducción("정수와 Cadena 상수만 valorSoporte");
    }
    String ensambladorX86(String puntoEntradaElemento, List<String> valorExportado, String valorObjetivo) throws IOException {
        Map<String,String> tablaMáquina = new HashMap<>();
        for (String línea : Files.readAllLines(rutaRecurso.resolve("FuncionesMáquinaX86.tsv"))) { String[] valorPar = línea.split("\t"); if (valorPar[0].equals(valorObjetivo)) tablaMáquina.put(valorPar[1] + valorPar[2],valorPar[3]); }
        int índicePosición = puntoEntradaElemento.lastIndexOf('.'); if (índicePosición < 0) throw new ErrorTraducción("puntoEntradaElemento valorAsignar error");
        String valorPropietario = puntoEntradaElemento.substring(0,índicePosición).replace('.','/'), nombreEntradaElementoMétodo = puntoEntradaElemento.substring(índicePosición + 1); ReferenciaMétodo valorPuntoEntradaElemento = null;
        for (String valorDescripción : Arrays.asList("()I","()V")) { ReferenciaMétodo referencia = new ReferenciaMétodo(valorPropietario,nombreEntradaElementoMétodo,valorDescripción); if (listaMétodos.containsKey(referencia)) { if (valorPuntoEntradaElemento != null) throw new ErrorTraducción("겹친 puntoEntradaElemento"); valorPuntoEntradaElemento = referencia; } }
        if (valorPuntoEntradaElemento == null || (listaMétodos.get(valorPuntoEntradaElemento).entradaElementoAcceso & 0x100) != 0) throw new ErrorTraducción("valorPuntoEntradaElemento Función valorFormato error");
        List<String> línea = new ArrayList<>(); línea.add(".code32");
        for (DatosClase Datos : listaClases.values()) {
            String valorEstadoValor = símbolo("state",Datos.nombre), inicializar = símbolo("init",Datos.nombre);
            Collections.addAll(línea,".bss",".balign 4",valorEstadoValor + ": .long 0",".text",inicializar + ":","cmpl $0, " + valorEstadoValor,"jne " + inicializar + "_done","movl $1, " + valorEstadoValor);
            ReferenciaMétodo referenciaInicializador = new ReferenciaMétodo(Datos.nombre,"<clinit>","()V"); if (listaMétodos.containsKey(referenciaInicializador)) línea.add("call " + símbolo("method",referenciaInicializador.partes()));
            Collections.addAll(línea,"movl $2, " + valorEstadoValor,inicializar + "_done:","ret");
            for (DatosMiembro valorCampo : Datos.valorCampo) {
                byte[] valorConstante = valorCampo.valorAtributo.get("ConstantValue"); String valor = valorConstante == null ? "0" : constanteX86(Datos,new LectorDatos(valorConstante).leerCorto());
                Collections.addAll(línea,".data",".balign 4",símbolo("field",Datos.nombre,valorCampo.nombre,valorCampo.valorDescripción) + ": .long " + valor);
            }
            for (DatosMiembro Función : Datos.Función) if (!Función.nombre.equals("<init>")) línea.add(cuerpoMétodoX86(new ReferenciaMétodo(Datos.nombre,Función.nombre,Función.valorDescripción),Función,tablaMáquina,valorObjetivo));
        }
        Collections.addAll(línea,".text",".globl java_entry","java_entry:","call " + símbolo("init",valorPuntoEntradaElemento.valorPropietario),"call " + símbolo("method",valorPuntoEntradaElemento.partes()));
        if (valorPuntoEntradaElemento.valorDescripción.equals("()V")) línea.add("xorl %eax, %eax"); línea.add("ret");
        for (String valorAsignar : valorExportado) {
            int valorDelimitador = valorAsignar.indexOf('='); if (valorDelimitador < 1) throw new ErrorTraducción("emitirValor valorAsignar error");
            String valorExterno = valorAsignar.substring(0,valorDelimitador), Función = valorAsignar.substring(valorDelimitador + 1); int resultadoDivisión = Función.lastIndexOf('.');
            if (resultadoDivisión < 0 || !valorExterno.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ErrorTraducción("emitirValor símbolo error");
            String valorClase = Función.substring(0,resultadoDivisión).replace('.','/'), nombre = Función.substring(resultadoDivisión + 1); ReferenciaMétodo valorSelección = null;
            for (ReferenciaMétodo referencia : listaMétodos.keySet()) if (referencia.valorPropietario.equals(valorClase) && referencia.nombre.equals(nombre)) { if (valorSelección != null) throw new ErrorTraducción("겹친 emitirValor valorObjetivo"); valorSelección = referencia; }
            if (valorSelección == null) throw new ErrorTraducción("내보낼 함수가 métodoAusente");
            Collections.addAll(línea,".text",".globl " + valorExterno,valorExterno + ":","call " + símbolo("init",valorSelección.valorPropietario),"jmp " + símbolo("method",valorSelección.partes()));
        }
        línea.add(".section .rodata");
        for (Map.Entry<String,String> valorEntradaElemento : valoresCadena.entrySet()) {
            Collections.addAll(línea,".balign 4",valorEntradaElemento.getValue() + ":",".long " + valorEntradaElemento.getKey().length());
            List<String> listaUnidades = new ArrayList<>(); for (char valorUnidad : valorEntradaElemento.getKey().toCharArray()) listaUnidades.add(Integer.toString(valorUnidad)); if (!listaUnidades.isEmpty()) línea.add(".long " + String.join(",",listaUnidades));
        }
        línea.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",línea) + "\n";
    }
    static void ejecutarHerramienta(List<String> comando) throws Exception {
        if (new ProcessBuilder(comando).inheritIO().start().waitFor() != 0) throw new ErrorTraducción("compilarFuente error: " + comando.get(0));
    }
    static String cadenaDatos(String texto) { return "\"" + texto.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void traducciónX86(List<Path> listaEntrada, String valorObjetivo, String puntoEntradaElemento, List<String> valorExportado, Path Salida, Path valorRecurso) throws Exception {
        Path valorTemporal = Files.createTempDirectory("jkoros-java-x86-"), rutaClase = valorTemporal.resolve("classes"); Files.createDirectory(rutaClase);
        try {
            List<String> comandoJava = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",rutaClase.toString(),"-sourcepath",rutaClase.toString(),"-d",rutaClase.toString()));
            List<Path> códigoBytes = new ArrayList<>(); int númeroElementosFuente = 0;
            for (Path valorEntrada : listaEntrada) {
                if (Salida.toAbsolutePath().normalize().equals(valorEntrada.toAbsolutePath().normalize())) throw new ErrorTraducción("Salida 파일과 입력이 textoIgual");
                if (valorEntrada.toString().endsWith(".java")) { comandoJava.add(valorEntrada.toString()); númeroElementosFuente++; }
                else if (valorEntrada.toString().endsWith(".class")) códigoBytes.add(valorEntrada);
                else throw new ErrorTraducción(".java 또는 .class만 valorSoporte");
            }
            if (númeroElementosFuente > 0) ejecutarHerramienta(comandoJava);
            try (java.util.stream.Stream<Path> listaRuta = Files.walk(rutaClase)) { listaRuta.filter(ruta -> ruta.toString().endsWith(".class")).sorted().forEach(códigoBytes::add); }
            CompilaciónAnticipada convertirValor = new CompilaciónAnticipada(códigoBytes,valorObjetivo.equals("user") ? "user" : "kernel",262144,valorRecurso);
            String ensamblarValor = convertirValor.ensambladorX86(puntoEntradaElemento,valorExportado,valorObjetivo); Files.writeString(valorTemporal.resolve("program.s"),ensamblarValor,StandardCharsets.UTF_8);
            Path posiciónHerramienta = valorRecurso.getParent();
            ejecutarHerramienta(Arrays.asList("as","--32","-o",valorTemporal.resolve("program.o").toString(),valorTemporal.resolve("program.s").toString()));
            ejecutarHerramienta(Arrays.asList("as","--32","-o",valorTemporal.resolve("runtime.o").toString(),posiciónHerramienta.resolve("SoporteEntornoEjecución.s").toString()));
            List<String> conectar = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (valorObjetivo.equals("kernel")) conectar.add("-r");
            else {
                ejecutarHerramienta(Arrays.asList("as","--32","-o",valorTemporal.resolve("start.o").toString(),posiciónHerramienta.resolve(valorObjetivo.equals("user") ? "iniciarProgramaUsuario.s" : "inicioSistemaLinux.s").toString()));
                Collections.addAll(conectar,"-e","_start",valorTemporal.resolve("start.o").toString());
                if (valorObjetivo.equals("user")) Collections.addAll(conectar,"-T",posiciónHerramienta.resolve("disposiciónEnlazarUsuario.ld").toString());
            }
            Collections.addAll(conectar,"-o",valorTemporal.resolve("result").toString(),valorTemporal.resolve("program.o").toString(),valorTemporal.resolve("runtime.o").toString()); ejecutarHerramienta(conectar);
            Salida = Salida.toAbsolutePath(); Files.createDirectories(Salida.getParent()); Path valorPublicar = Files.createTempFile(Salida.getParent(),".elf-",".tmp");
            try { Files.copy(valorTemporal.resolve("result"),valorPublicar,StandardCopyOption.REPLACE_EXISTING); Files.move(valorPublicar,Salida,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(valorPublicar); }
            Files.setPosixFilePermissions(Salida,java.nio.file.attribute.PosixFilePermissions.fromString(valorObjetivo.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Salida + ".s"),ensamblarValor,StandardCharsets.UTF_8);
            List<String> datosSímbolo = new ArrayList<>(), datosFuente = new ArrayList<>();
            for (ReferenciaMétodo referencia : convertirValor.listaMétodos.keySet()) datosSímbolo.add(cadenaDatos(símbolo("method",referencia.partes())) + ":" + cadenaDatos(referencia.valorPropietario + "." + referencia.nombre + referencia.valorDescripción));
            for (Path valorEntrada : listaEntrada) {
                byte[] archivoResumenHash = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(valorEntrada)); StringBuilder texto = new StringBuilder(); for (byte valor : archivoResumenHash) texto.append(String.format(Locale.ROOT,"%02x",valor & 255));
                datosFuente.add(cadenaDatos(valorEntrada.toAbsolutePath().toString()) + ":" + cadenaDatos(texto.toString()));
            }
            Files.writeString(Paths.get(Salida + ".json"),"{\"target\":" + cadenaDatos(valorObjetivo) + ",\"entry\":" + cadenaDatos(puntoEntradaElemento) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",datosSímbolo) + "},\"sources\":{" + String.join(",",datosFuente) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> listaRuta = Files.walk(valorTemporal)) { for (Path ruta : (Iterable<Path>)listaRuta.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(ruta); }
        }
    }
    public static void main(String[] argumentos) {
        try {
            String puntoEntradaElemento = null, valorObjetivo = "kernel", objetivoX86 = null; Path rutaSalida = null; int númeroElementosPalabraLéxico = 262144; boolean notaciónUniversal = false;
            List<String> valorExportado = new ArrayList<>(); List<Path> listaRuta = new ArrayList<>();
            for (int índiceOrdinal = 0; índiceOrdinal < argumentos.length; índiceOrdinal++) {
                String valor = argumentos[índiceOrdinal];
                switch (valor) {
                    case "--target": objetivoX86 = argumentos[++índiceOrdinal]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry valorClase.Función -o Salida [--target linux|kernel|user] [--profile kernel|user] [--export símbolo=valorClase.Función] 클래스파일 또는 Java원문"); return;
                    case "--entry": puntoEntradaElemento = argumentos[++índiceOrdinal]; break;
                    case "--profile": valorObjetivo = argumentos[++índiceOrdinal]; break;
                    case "--heap-words": númeroElementosPalabraLéxico = Integer.parseInt(argumentos[++índiceOrdinal]); break;
                    case "--export": valorExportado.add(argumentos[++índiceOrdinal]); break;
                    case "-o": rutaSalida = Paths.get(argumentos[++índiceOrdinal]); break;
                    case "--ucn": notaciónUniversal = true; break;
                    default: if (valor.startsWith("-")) throw new ErrorTraducción("알 númeroValor 없는 옵션: " + valor); listaRuta.add(Paths.get(valor));
                }
            }
            if (puntoEntradaElemento == null || rutaSalida == null || listaRuta.isEmpty()) throw new ErrorTraducción("--entry, -o, valorClase 파일이 필요합니다");
            Path valorRecurso = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (objetivoX86 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(objetivoX86)) throw new ErrorTraducción("알 númeroValor 없는 ejecutarComando valorObjetivo");
                traducciónX86(listaRuta,objetivoX86,puntoEntradaElemento,valorExportado,rutaSalida,valorRecurso); return;
            }
            String fuente = new CompilaciónAnticipada(listaRuta, valorObjetivo, númeroElementosPalabraLéxico, valorRecurso).generar(puntoEntradaElemento, valorExportado, notaciónUniversal);
            rutaSalida = rutaSalida.toAbsolutePath(); Files.createDirectories(rutaSalida.getParent());
            Path valorTemporal = Files.createTempFile(rutaSalida.getParent(), ".aot-", ".tmp");
            try { Files.writeString(valorTemporal, fuente, StandardCharsets.UTF_8); Files.move(valorTemporal, rutaSalida, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(valorTemporal); }
        } catch (Exception error) { System.err.println("compilarFuente error: " + error.getMessage()); System.exit(1); }
    }
}
