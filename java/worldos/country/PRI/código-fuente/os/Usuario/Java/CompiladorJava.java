// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Compilador Java restringido que se ejecuta en el invitado y genera archivos de clase estándar de versión 49. */
public final class CompiladorJava {
    static int[] fuente = new int[16384], Salida = new int[16384], valorCódigo = new int[4096];
    static int[] claseTipoTokenLéxico = new int[2048], posiciónTokenLéxico = new int[2048], longitudTokenLéxico = new int[2048];
    static int[] valorConstante = new int[4096], desfaseConstante = new int[512];
    static int[] Caracteres = new int[512], textoNombreArchivo = new int[64];
    static int[] códigoInsertado = new int[16];
    static int tamañoFuente, númeroElementosTokenLéxico, posición, tamañoCódigo, tamañoConstante, númeroElementosConstante = 1, tamañoSalida, longitudCarácter;
    static boolean error;
    static int tokenLéxicoClase, constanteClase, constantePadre, constanteCódigo;
    static int[] nombreEntradaElementoMétodo = new int[32], retornarMétodo = new int[32], númeroElementosArgumentoMétodo = new int[32];
    static int[] nombreArgumentoMétodo = new int[512], tipoArgumentoMétodo = new int[512];
    static int[] cuerpoMétodo = new int[32], finMétodo = new int[32], códigoMétodo = new int[32];
    static int[] longitudMétodo = new int[32], variablesLocalesMétodo = new int[32], constanteNombreMétodo = new int[32], constanteDescriptorMétodo = new int[32];
    static int[] accesoMétodo = new int[32];
    static int númeroElementosMétodo, métodoActual, númeroElementosLocal, valorProfundidad, profundidadExpresión;
    static int[] nombreLocal = new int[128], tipoLocal = new int[128], profundidadLocal = new int[128];

    static void valorFallo(String valorRazón) {
        if (!error) {
            Usuario.escribir("javac error: "); Usuario.escribir(valorRazón);
            Usuario.escribir(" at line ");
            int línea = 1, terminación = posición < númeroElementosTokenLéxico ? posiciónTokenLéxico[posición] : tamañoFuente;
            for (int númeroValor = 0; númeroValor < terminación; númeroValor++) if (fuente[númeroValor] == 10) línea++;
            HerramientaJava.escribirNúmero(línea); Usuario.escribirValorCarácter(10);
        }
        error = true;
    }
    static boolean valorCarácter(int valor) { return ReglasCaracteresIdentificadores.carácterPrimero(valor); }
    static boolean valorDígito(int valor) { return valor >= '0' && valor <= '9'; }
    static boolean igualNombres(int operandoPrimero, int operandoSegundo) {
        if (operandoPrimero < 0 || operandoSegundo < 0 || operandoPrimero >= númeroElementosTokenLéxico || operandoSegundo >= númeroElementosTokenLéxico || longitudTokenLéxico[operandoPrimero] != longitudTokenLéxico[operandoSegundo]) return false;
        for (int númeroValor = 0; númeroValor < longitudTokenLéxico[operandoPrimero]; númeroValor++) if (fuente[posiciónTokenLéxico[operandoPrimero] + númeroValor] != fuente[posiciónTokenLéxico[operandoSegundo] + númeroValor]) return false;
        return true;
    }
    static boolean valorPalabra(int valorTokenLéxico, String textoPalabra) {
        if (valorTokenLéxico < 0 || valorTokenLéxico >= númeroElementosTokenLéxico || longitudTokenLéxico[valorTokenLéxico] != textoPalabra.length()) return false;
        for (int númeroValor = 0; númeroValor < textoPalabra.length(); númeroValor++) if (fuente[posiciónTokenLéxico[valorTokenLéxico] + númeroValor] != textoPalabra.charAt(númeroValor)) return false;
        return true;
    }
    static int valorClaseTipo() { return posición < númeroElementosTokenLéxico ? claseTipoTokenLéxico[posición] : 0; }
    static boolean recibir(int valor) { if (valorClaseTipo() != valor) return false; posición++; return true; }
    static void valorRequisito(int valor) { if (!recibir(valor)) valorFallo("unexpected token"); }
    static boolean palabraTomar(String textoPalabra) { if (!valorPalabra(posición, textoPalabra)) return false; posición++; return true; }
    static void palabraExigir(String textoPalabra) { if (!palabraTomar(textoPalabra)) valorFallo(textoPalabra); }
    static int valorIdentificador() {
        int resultado = posición;
        if (valorClaseTipo() != 256) valorFallo("identifier required"); else posición++;
        String palabrasReservado = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int ponerEnMarcha = 0;
        for (int númeroValor = 0; númeroValor <= palabrasReservado.length(); númeroValor++) {
            if (númeroValor == palabrasReservado.length() || palabrasReservado.charAt(númeroValor) == ' ') {
                boolean textoIgual = númeroValor - ponerEnMarcha == longitudTokenLéxico[resultado];
                for (int entradaElementoRanura = ponerEnMarcha; textoIgual && entradaElementoRanura < númeroValor; entradaElementoRanura++) if (palabrasReservado.charAt(entradaElementoRanura) != fuente[posiciónTokenLéxico[resultado] + entradaElementoRanura - ponerEnMarcha]) textoIgual = false;
                if (textoIgual) valorFallo("reserved word cannot be an identifier");
                ponerEnMarcha = númeroValor + 1;
            }
        }
        return resultado;
    }
    static void valorCortar() {
        int númeroValor = 0;
        while (númeroValor < tamañoFuente && !error) {
            int valor = fuente[númeroValor], ponerEnMarcha = númeroValor, valorClaseTipo = valor;
            if (valor == 32 || valor == 9 || valor == 10 || valor == 13) { númeroValor++; continue; }
            if (valor == '/' && númeroValor + 1 < tamañoFuente && fuente[númeroValor + 1] == '/') {
                while (númeroValor < tamañoFuente && fuente[númeroValor] != 10) númeroValor++;
                continue;
            }
            if (valor == '/' && númeroValor + 1 < tamañoFuente && fuente[númeroValor + 1] == '*') {
                númeroValor += 2;
                while (númeroValor + 1 < tamañoFuente && !(fuente[númeroValor] == '*' && fuente[númeroValor + 1] == '/')) númeroValor++;
                if (númeroValor + 1 >= tamañoFuente) { valorFallo("unterminated comment"); break; }
                númeroValor += 2; continue;
            }
            if (valorCarácter(valor)) { valorClaseTipo = 256; while (númeroValor < tamañoFuente && ReglasCaracteresIdentificadores.carácterContinuación(fuente[númeroValor])) númeroValor++; }
            else if (valorDígito(valor)) { valorClaseTipo = 257; while (númeroValor < tamañoFuente && valorDígito(fuente[númeroValor])) númeroValor++; }
            else if (valor == '"' || valor == '\'') {
                valorClaseTipo = valor == '"' ? 258 : 259; númeroValor++;
                while (númeroValor < tamañoFuente && fuente[númeroValor] != valor && fuente[númeroValor] != 10 && fuente[númeroValor] != 13) {
                    if (fuente[númeroValor] == '\\') númeroValor++;
                    númeroValor++;
                }
                if (númeroValor >= tamañoFuente || fuente[númeroValor] != valor) { valorFallo("unterminated literal"); break; }
                númeroValor++;
            } else {
                númeroValor++;
                if (númeroValor < tamañoFuente) {
                    int elementoListaSiguiente = fuente[númeroValor];
                    if (valor == '=' && elementoListaSiguiente == '=') valorClaseTipo = 300;
                    if (valor == '!' && elementoListaSiguiente == '=') valorClaseTipo = 301;
                    if (valor == '<' && elementoListaSiguiente == '=') valorClaseTipo = 302;
                    if (valor == '>' && elementoListaSiguiente == '=') valorClaseTipo = 303;
                    if (valor == '&' && elementoListaSiguiente == '&') valorClaseTipo = 304;
                    if (valor == '|' && elementoListaSiguiente == '|') valorClaseTipo = 305;
                    if (valor == '+' && elementoListaSiguiente == '+') valorClaseTipo = 306;
                    if (valor == '-' && elementoListaSiguiente == '-') valorClaseTipo = 307;
                    if (valor == '+' && elementoListaSiguiente == '=') valorClaseTipo = 308;
                    if (valor == '-' && elementoListaSiguiente == '=') valorClaseTipo = 309;
                    if (valor == '*' && elementoListaSiguiente == '=') valorClaseTipo = 310;
                    if (valor == '/' && elementoListaSiguiente == '=') valorClaseTipo = 311;
                    if (valor == '%' && elementoListaSiguiente == '=') valorClaseTipo = 312;
                    if (valorClaseTipo >= 300) númeroValor++;
                }
            }
            if (númeroElementosTokenLéxico == claseTipoTokenLéxico.length - 1) { valorFallo("too many tokens (2047 maximum)"); break; }
            claseTipoTokenLéxico[númeroElementosTokenLéxico] = valorClaseTipo; posiciónTokenLéxico[númeroElementosTokenLéxico] = ponerEnMarcha; longitudTokenLéxico[númeroElementosTokenLéxico++] = númeroValor - ponerEnMarcha;
        }
    }
    static void escribirByteConstante(int valor) {
        if (tamañoConstante == valorConstante.length) { valorFallo("constant pool too large"); return; }
        valorConstante[tamañoConstante++] = valor & 255;
    }
    static void escribirCortoConstante(int valor) { escribirByteConstante(valor >> 8); escribirByteConstante(valor); }
    static int registroConstante(int ponerEnMarcha) {
        for (int númeroValor = 1; númeroValor < númeroElementosConstante; númeroValor++) {
            int valorLadoDelantero = desfaseConstante[númeroValor], longitud = (númeroValor + 1 < númeroElementosConstante ? desfaseConstante[númeroValor + 1] : ponerEnMarcha) - valorLadoDelantero;
            if (longitud != tamañoConstante - ponerEnMarcha) continue;
            boolean textoIgual = true;
            for (int entradaElementoRanura = 0; entradaElementoRanura < longitud; entradaElementoRanura++) if (valorConstante[valorLadoDelantero + entradaElementoRanura] != valorConstante[ponerEnMarcha + entradaElementoRanura]) textoIgual = false;
            if (textoIgual) { tamañoConstante = ponerEnMarcha; return númeroValor; }
        }
        if (númeroElementosConstante == desfaseConstante.length) { valorFallo("too many constants"); return 0; }
        desfaseConstante[númeroElementosConstante] = ponerEnMarcha;
        return númeroElementosConstante++;
    }
    static void añadirFinalTexto(int valor) {
        if (longitudCarácter == Caracteres.length) { valorFallo("text too long"); return; }
        Caracteres[longitudCarácter++] = valor;
    }
    static void añadirFinalPalabra(String textoPalabra) { for (int númeroValor = 0; númeroValor < textoPalabra.length(); númeroValor++) añadirFinalTexto(textoPalabra.charAt(númeroValor)); }
    static int constanteCarácter() {
        int ponerEnMarcha = tamañoConstante; escribirByteConstante(1); escribirCortoConstante(0);
        for (int númeroValor = 0; númeroValor < longitudCarácter; númeroValor++) {
            int valor = Caracteres[númeroValor];
            if (valor > 0 && valor < 128) escribirByteConstante(valor);
            else if (valor < 2048) { escribirByteConstante(192 | valor >> 6); escribirByteConstante(128 | valor & 63); }
            else { escribirByteConstante(224 | valor >> 12); escribirByteConstante(128 | valor >> 6 & 63); escribirByteConstante(128 | valor & 63); }
        }
        if (error) return 0;
        int longitud = tamañoConstante - ponerEnMarcha - 3;
        valorConstante[ponerEnMarcha + 1] = longitud >> 8; valorConstante[ponerEnMarcha + 2] = longitud & 255;
        return registroConstante(ponerEnMarcha);
    }
    static int constantePalabra(String textoPalabra) { longitudCarácter = 0; añadirFinalPalabra(textoPalabra); return constanteCarácter(); }
    static int constanteTokenLéxico(int valorTokenLéxico) {
        longitudCarácter = 0;
        for (int númeroValor = 0; númeroValor < longitudTokenLéxico[valorTokenLéxico]; númeroValor++) añadirFinalTexto(fuente[posiciónTokenLéxico[valorTokenLéxico] + númeroValor]);
        return constanteCarácter();
    }
    static int referencia(int valorClaseTipo, int operandoPrimero, int operandoSegundo) {
        int ponerEnMarcha = tamañoConstante; escribirByteConstante(valorClaseTipo); escribirCortoConstante(operandoPrimero);
        if (valorClaseTipo == 9 || valorClaseTipo == 10 || valorClaseTipo == 12) escribirCortoConstante(operandoSegundo);
        return registroConstante(ponerEnMarcha);
    }
    static int referenciaExterno(int valorClaseTipo, String valorPropietario, String nombre, String valorDescripción) {
        int identificadorPropietario = referencia(7, constantePalabra(valorPropietario), 0);
        int númeroElementosNombre = constantePalabra(nombre), númeroElementosFormato = constantePalabra(valorDescripción);
        return referencia(valorClaseTipo, identificadorPropietario, referencia(12, númeroElementosNombre, númeroElementosFormato));
    }
    static void emitirValor(int valor) {
        if (tamañoCódigo == valorCódigo.length) { valorFallo("bytecode too large"); return; }
        valorCódigo[tamañoCódigo++] = valor & 255;
    }
    static void comando(int valor, int argumentos) { emitirValor(valor); emitirValor(argumentos >> 8); emitirValor(argumentos); }
    static void constanteNumérico(int valor) {
        if (valor >= -1 && valor <= 5) { emitirValor(valor + 3); return; }
        int ponerEnMarcha = tamañoConstante; escribirByteConstante(3); escribirCortoConstante(valor >>> 16); escribirCortoConstante(valor);
        comando(19, registroConstante(ponerEnMarcha));
    }
    static int rama(int comando) { int resultado = tamañoCódigo; comando(comando, 0); return resultado; }
    static void valorEnlazar(int rama, int objetoObjetivo) {
        if (error) return;
        int valorDistancia = objetoObjetivo - rama;
        if (valorDistancia < -32768 || valorDistancia > 32767 || rama < 0 || rama + 2 >= tamañoCódigo) { valorFallo("invalid branch"); return; }
        valorCódigo[rama + 1] = valorDistancia >> 8 & 255; valorCódigo[rama + 2] = valorDistancia & 255;
    }
    static void valorComparación(int comando) {
        int valorVerdadero = rama(comando); emitirValor(3); int terminación = rama(167);
        valorEnlazar(valorVerdadero, tamañoCódigo); emitirValor(4); valorEnlazar(terminación, tamañoCódigo);
    }
    static int valorFormato() {
        if (palabraTomar("void")) return 0;
        if (palabraTomar("int")) return 1;
        if (palabraTomar("boolean")) return 2;
        if (palabraTomar("char")) return 5;
        if (palabraTomar("FileInputStream")) return 6;
        if (palabraTomar("FileOutputStream")) return 7;
        if (palabraTomar("String")) { if (recibir('[')) { valorRequisito(']'); return 4; } return 3; }
        valorFallo("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void añadirFormato(int valorTipo) {
        if (valorTipo == 0) añadirFinalTexto('V');
        if (valorTipo == 1) añadirFinalTexto('I');
        if (valorTipo == 2) añadirFinalTexto('Z');
        if (valorTipo == 3) añadirFinalPalabra("Ljava/lang/String;");
        if (valorTipo == 4) añadirFinalPalabra("[Ljava/lang/String;");
        if (valorTipo == 5) añadirFinalTexto('C');
        if (valorTipo == 6) añadirFinalPalabra("Ljava/io/FileInputStream;");
        if (valorTipo == 7) añadirFinalPalabra("Ljava/io/FileOutputStream;");
    }
    // El compilador restringido admite declaraciones throws. Los cuerpos de manejo de excepciones requieren javac en el anfitrión.
    static void leerNombreExcepción() {
        boolean PaqueteCoreano = palabraTomar("español");
        if (PaqueteCoreano) { valorRequisito('.'); palabraExigir("propio"); valorRequisito('.'); }
        if (!PaqueteCoreano && (palabraTomar("Exception") || palabraTomar("IOException"))) return;
        if (palabraTomar("excepción") || palabraTomar("ExcepciónEjecución") || palabraTomar("ExcepciónSalidaEntrada") || palabraTomar("ExcepciónTiempoEsperaEsperar") || palabraTomar("ExcepciónBuscarDirección") || palabraTomar("ExcepciónArchivoAusente") || palabraTomar("ExcepciónComunicación") || palabraTomar("ExcepciónArgumentoInválido") || palabraTomar("FalloFormatoNúmero") || palabraTomar("ExcepciónLímites") || palabraTomar("ExcepciónLímitesArreglo") || palabraTomar("ExcepciónLímitesCadena") || palabraTomar("ExcepciónReferenciaReferenciaNula") || palabraTomar("FalloAritmética") || palabraTomar("ExcepciónEstadoValor") || palabraTomar("ExcepciónConversiónTipoTipo") || palabraTomar("FalloTamañoArregloNegativo") || palabraTomar("FalloAlmacenarArreglo") || palabraTomar("ExcepciónEstadoValorHiloEjecución") || palabraTomar("ExcepciónInterrumpidoEsperar")) return;
        valorFallo("unsupported throws type");
    }
    static void leerDeclaración() {
        while (palabraTomar("import")) {
            if (valorPalabra(posición, "español")) leerNombreExcepción();
            else {
                palabraExigir("java"); valorRequisito('.'); palabraExigir("io"); valorRequisito('.');
                if (!(palabraTomar("FileInputStream") || palabraTomar("FileOutputStream") || palabraTomar("IOException"))) valorFallo("unsupported import");
            }
            valorRequisito(';');
        }
        palabraTomar("public"); palabraTomar("final"); palabraExigir("class"); tokenLéxicoClase = valorIdentificador();
        constanteClase = referencia(7, constanteTokenLéxico(tokenLéxicoClase), 0);
        constantePadre = referencia(7, constantePalabra("java/lang/Object"), 0); constanteCódigo = constantePalabra("Code"); valorRequisito('{');
        while (!error && valorClaseTipo() != '}') {
            if (númeroElementosMétodo == 32) { valorFallo("too many methods"); break; }
            int entradaElementoAcceso = palabraTomar("public") ? 1 : palabraTomar("private") ? 2 : 0; palabraExigir("static");
            int Función = númeroElementosMétodo++;
            accesoMétodo[Función] = entradaElementoAcceso | 8;
            retornarMétodo[Función] = valorFormato(); nombreEntradaElementoMétodo[Función] = valorIdentificador(); valorRequisito('(');
            for (int valorLadoDelantero = 0; valorLadoDelantero < Función; valorLadoDelantero++) if (igualNombres(nombreEntradaElementoMétodo[valorLadoDelantero], nombreEntradaElementoMétodo[Función])) valorFallo("duplicate method (overloading unsupported)");
            while (!error && valorClaseTipo() != ')') {
                int númeroValor = númeroElementosArgumentoMétodo[Función];
                if (númeroValor == 16) { valorFallo("too many parameters"); break; }
                int valorTipo = valorFormato(); if (valorTipo == 0) valorFallo("void parameter");
                tipoArgumentoMétodo[Función * 16 + númeroValor] = valorTipo; nombreArgumentoMétodo[Función * 16 + númeroValor] = valorIdentificador();
                númeroElementosArgumentoMétodo[Función]++;
                if (!recibir(',')) break;
            }
            valorRequisito(')');
            if (palabraTomar("throws")) {
                do { leerNombreExcepción(); } while (!error && recibir(','));
            }
            cuerpoMétodo[Función] = posición; valorRequisito('{');
            int valorAnidamiento = 1;
            while (posición < númeroElementosTokenLéxico && valorAnidamiento > 0) {
                if (valorClaseTipo() == '{') valorAnidamiento++;
                if (valorClaseTipo() == '}') valorAnidamiento--;
                posición++;
            }
            if (valorAnidamiento != 0) valorFallo("unclosed method body");
            finMétodo[Función] = posición;
            constanteNombreMétodo[Función] = constanteTokenLéxico(nombreEntradaElementoMétodo[Función]);
            longitudCarácter = 0; añadirFinalTexto('(');
            for (int númeroValor = 0; númeroValor < númeroElementosArgumentoMétodo[Función]; númeroValor++) añadirFormato(tipoArgumentoMétodo[Función * 16 + númeroValor]);
            añadirFinalTexto(')'); añadirFormato(retornarMétodo[Función]); constanteDescriptorMétodo[Función] = constanteCarácter();
        }
        valorRequisito('}'); if (posición != númeroElementosTokenLéxico) valorFallo("extra input after class");
    }
    static int encontrarLocal(int nombre) {
        for (int númeroValor = númeroElementosLocal - 1; númeroValor >= 0; númeroValor--) if (profundidadLocal[númeroValor] >= 0 && igualNombres(nombreLocal[númeroValor], nombre)) return númeroValor;
        valorFallo("unknown variable"); return 0;
    }
    static int añadirLocal(int nombre, int valorTipo) {
        for (int númeroValor = 0; númeroValor < númeroElementosLocal; númeroValor++) if (profundidadLocal[númeroValor] >= 0 && igualNombres(nombreLocal[númeroValor], nombre)) valorFallo("duplicate local variable");
        if (númeroElementosLocal == 128) { valorFallo("too many locals"); return 0; }
        nombreLocal[númeroElementosLocal] = nombre; tipoLocal[númeroElementosLocal] = valorTipo; profundidadLocal[númeroElementosLocal] = valorProfundidad;
        return númeroElementosLocal++;
    }
    static boolean tipoEnteroValor(int valorTipo) { return valorTipo == 1 || valorTipo == 5; }
    static void leerLocal(int númeroValor) { emitirValor(tipoLocal[númeroValor] <= 2 || tipoLocal[númeroValor] == 5 ? 21 : 25); emitirValor(númeroValor); }
    static void escribirLocal(int númeroValor) { emitirValor(tipoLocal[númeroValor] <= 2 || tipoLocal[númeroValor] == 5 ? 54 : 58); emitirValor(númeroValor); }
    static void verificarTipo(int datosEfectivo, int expectativa) { if (datosEfectivo != expectativa && !(datosEfectivo == 5 && expectativa == 1)) valorFallo("type mismatch"); }
    static void leerValorCarácter(int valorTokenLéxico) {
        longitudCarácter = 0; int ponerEnMarcha = posiciónTokenLéxico[valorTokenLéxico] + 1, terminación = posiciónTokenLéxico[valorTokenLéxico] + longitudTokenLéxico[valorTokenLéxico] - 1;
        while (ponerEnMarcha < terminación && !error) {
            int valor = fuente[ponerEnMarcha++];
            if (valor == '\\') {
                if (ponerEnMarcha == terminación) { valorFallo("invalid escape"); break; }
                valor = fuente[ponerEnMarcha++];
                if (valor == 'n') valor = 10;
                else if (valor == 'r') valor = 13;
                else if (valor == 't') valor = 9;
                else if (valor == 'b') valor = 8;
                else if (valor == 'f') valor = 12;
                else if (valor != '\\' && valor != '"' && valor != '\'') valorFallo("unsupported escape");
            }
            añadirFinalTexto(valor);
        }
    }
    static int analizarEnteroValor(int valorTokenLéxico, boolean valorNegativo) {
        if (longitudTokenLéxico[valorTokenLéxico] > 1 && fuente[posiciónTokenLéxico[valorTokenLéxico]] == '0') valorFallo("octal literals unsupported");
        int valor = 0;
        for (int númeroValor = 0; númeroValor < longitudTokenLéxico[valorTokenLéxico]; númeroValor++) {
            int elementoListaDígito = fuente[posiciónTokenLéxico[valorTokenLéxico] + númeroValor] - '0';
            if (valor < -214748364 || valor == -214748364 && elementoListaDígito > (valorNegativo ? 8 : 7)) valorFallo("integer literal out of range");
            valor = valor * 10 - elementoListaDígito;
        }
        return valorNegativo ? valor : -valor;
    }
    static int expresiónPrimario() {
        if (palabraTomar("new")) {
            int valorTipo = valorFormato();
            if (valorTipo != 6 && valorTipo != 7) { valorFallo("only file streams supported by new in source"); return 0; }
            String valorPropietario = valorTipo == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            comando(187, referencia(7, constantePalabra(valorPropietario), 0)); emitirValor(89);
            valorRequisito('('); verificarTipo(valorExpresión(), 3); boolean valorContinuación = false;
            if (recibir(',')) { if (valorTipo != 7) valorFallo("input stream constructor arguments"); verificarTipo(valorExpresión(), 2); valorContinuación = true; }
            valorRequisito(')');
            comando(183, referenciaExterno(10, valorPropietario, "<init>", valorContinuación ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return valorTipo;
        }
        if (recibir('(')) { int valorTipo = valorExpresión(); valorRequisito(')'); return valorTipo; }
        if (valorClaseTipo() == 257) { constanteNumérico(analizarEnteroValor(posición++, false)); return 1; }
        if (valorClaseTipo() == 258) { leerValorCarácter(posición++); comando(19, referencia(8, constanteCarácter(), 0)); return 3; }
        if (valorClaseTipo() == 259) { leerValorCarácter(posición++); if (longitudCarácter != 1) valorFallo("character literal length"); constanteNumérico(Caracteres[0]); return 5; }
        if (palabraTomar("true")) { emitirValor(4); return 2; }
        if (palabraTomar("false")) { emitirValor(3); return 2; }
        if (palabraTomar("español")) {
            valorRequisito('.'); palabraExigir("propio"); valorRequisito('.');
            String valorPropietario = "", valorMétodo = "", valorDescripción = ""; int operandoPrimero = 0, operandoSegundo = 0, operandoTercero = 0, operandoCuarto = 0, operandoQuinto = 0, resultado = 0;
            if (palabraTomar("Salida")) {
                valorPropietario = "español/propio/Salida"; valorRequisito('.');
                if (palabraTomar("escribirLínea")) { valorMétodo = "escribirLínea"; valorDescripción = "(Ljava/lang/String;)V"; operandoPrimero = 3; }
                else if (palabraTomar("escribir")) { valorMétodo = "escribir"; valorDescripción = "(Ljava/lang/String;)V"; operandoPrimero = 3; }
                else if (palabraTomar("escribirNúmero")) { valorMétodo = "escribirNúmero"; valorDescripción = "(I)V"; operandoPrimero = 1; }
                else valorFallo("unknown Korean output method");
            } else if (palabraTomar("Caracteres")) {
                valorPropietario = "español/propio/Caracteres"; valorRequisito('.'); operandoPrimero = 3;
                if (palabraTomar("longitud")) { valorMétodo = "longitud"; valorDescripción = "(Ljava/lang/String;)I"; resultado = 1; }
                else if (palabraTomar("númeroElementosPuntoCódigo")) { valorMétodo = "númeroElementosPuntoCódigo"; valorDescripción = "(Ljava/lang/String;)I"; resultado = 1; }
                else if (palabraTomar("analizarEnteroValor")) { valorMétodo = "analizarEnteroValor"; valorDescripción = "(Ljava/lang/String;)I"; resultado = 1; }
                else if (palabraTomar("escribirValorEnteroValor")) { valorMétodo = "escribirValorEnteroValor"; valorDescripción = "(I)Ljava/lang/String;"; operandoPrimero = 1; resultado = 3; }
                else if (palabraTomar("textoIgual")) { valorMétodo = "textoIgual"; valorDescripción = "(Ljava/lang/String;Ljava/lang/String;)Z"; operandoSegundo = 3; resultado = 2; }
                else if (palabraTomar("textoPegar")) { valorMétodo = "textoPegar"; valorDescripción = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; operandoSegundo = 3; resultado = 3; }
                else if (palabraTomar("valorCortar")) { valorMétodo = "valorCortar"; valorDescripción = "(Ljava/lang/String;II)Ljava/lang/String;"; operandoSegundo = 1; operandoTercero = 1; resultado = 3; }
                else valorFallo("unknown Korean text method");
            } else if (palabraTomar("Archivo")) {
                valorPropietario = "español/propio/Archivo"; valorRequisito('.'); operandoPrimero = 3;
                if (palabraTomar("leer")) { valorMétodo = "leer"; valorDescripción = "(Ljava/lang/String;)Ljava/lang/String;"; resultado = 3; }
                else if (palabraTomar("escribir")) { valorMétodo = "escribir"; valorDescripción = "(Ljava/lang/String;Ljava/lang/String;)V"; operandoSegundo = 3; }
                else valorFallo("unknown Korean file method");
            } else if (palabraTomar("Pantalla")) {
                valorPropietario = "español/propio/Pantalla"; valorRequisito('.');
                if (palabraTomar("valorAnchura")) { valorMétodo = "valorAnchura"; valorDescripción = "()I"; resultado = 1; }
                else if (palabraTomar("valorAltura")) { valorMétodo = "valorAltura"; valorDescripción = "()I"; resultado = 1; }
                else if (palabraTomar("rectángulo")) { valorMétodo = "rectángulo"; valorDescripción = "(IIIII)V"; operandoPrimero = 1; operandoSegundo = 1; operandoTercero = 1; operandoCuarto = 1; operandoQuinto = 1; }
                else if (palabraTomar("borrarEntradaElemento")) { valorMétodo = "borrarEntradaElemento"; valorDescripción = "(I)V"; operandoPrimero = 1; }
                else if (palabraTomar("esperarFin")) { valorMétodo = "esperarFin"; valorDescripción = "()V"; }
                else valorFallo("unknown Korean framebuffer method");
            } else valorFallo("unsupported Korean library class");
            valorRequisito('('); if (operandoPrimero != 0) verificarTipo(valorExpresión(), operandoPrimero);
            if (operandoSegundo != 0) { valorRequisito(','); verificarTipo(valorExpresión(), operandoSegundo); }
            if (operandoTercero != 0) { valorRequisito(','); verificarTipo(valorExpresión(), operandoTercero); }
            if (operandoCuarto != 0) { valorRequisito(','); verificarTipo(valorExpresión(), operandoCuarto); }
            if (operandoQuinto != 0) { valorRequisito(','); verificarTipo(valorExpresión(), operandoQuinto); }
            valorRequisito(')'); comando(184, referenciaExterno(10, valorPropietario, valorMétodo, valorDescripción)); return resultado;
        }
        if (palabraTomar("Integer")) {
            valorRequisito('.'); palabraExigir("parseInt"); valorRequisito('('); verificarTipo(valorExpresión(), 3); valorRequisito(')');
            comando(184, referenciaExterno(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int nombre = valorIdentificador();
        if (recibir('(')) {
            int Función = -1;
            for (int númeroValor = 0; númeroValor < númeroElementosMétodo; númeroValor++) if (igualNombres(nombre, nombreEntradaElementoMétodo[númeroValor])) Función = númeroValor;
            if (Función < 0) { valorFallo("unknown static method"); return 0; }
            int númeroValor = 0;
            while (!error && valorClaseTipo() != ')') {
                if (númeroValor >= númeroElementosArgumentoMétodo[Función]) { valorFallo("too many arguments"); break; }
                verificarTipo(valorExpresión(), tipoArgumentoMétodo[Función * 16 + númeroValor++]); if (!recibir(',')) break;
            }
            valorRequisito(')'); if (númeroValor != númeroElementosArgumentoMétodo[Función]) valorFallo("argument count mismatch");
            comando(184, referencia(10, constanteClase, referencia(12, constanteNombreMétodo[Función], constanteDescriptorMétodo[Función])));
            return retornarMétodo[Función];
        }
        int ámbitoLocal = encontrarLocal(nombre), valorTipo = tipoLocal[ámbitoLocal]; leerLocal(ámbitoLocal);
        while (!error) {
            if (recibir('[')) { verificarTipo(valorTipo, 4); verificarTipo(valorExpresión(), 1); valorRequisito(']'); emitirValor(50); valorTipo = 3; }
            else if (recibir('.')) {
                if (valorTipo == 6 || valorTipo == 7) {
                    String valorPropietario = valorTipo == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (palabraTomar("close")) { valorRequisito('('); valorRequisito(')'); comando(182, referenciaExterno(10, valorPropietario, "close", "()V")); valorTipo = 0; }
                    else if (valorTipo == 6 && palabraTomar("read")) { valorRequisito('('); valorRequisito(')'); comando(182, referenciaExterno(10, valorPropietario, "read", "()I")); valorTipo = 1; }
                    else if (valorTipo == 7 && palabraTomar("write")) { valorRequisito('('); verificarTipo(valorExpresión(), 1); valorRequisito(')'); comando(182, referenciaExterno(10, valorPropietario, "write", "(I)V")); valorTipo = 0; }
                    else { valorFallo("unsupported file stream method"); }
                    continue;
                }
                palabraExigir("length");
                if (valorTipo == 4) { emitirValor(190); valorTipo = 1; }
                else { verificarTipo(valorTipo, 3); valorRequisito('('); valorRequisito(')'); comando(182, referenciaExterno(10, "java/lang/String", "length", "()I")); valorTipo = 1; }
            } else break;
        }
        return valorTipo;
    }
    static int valorUnario() {
        if (++profundidadExpresión > 64) { valorFallo("expression nesting too deep"); profundidadExpresión--; return 0; }
        int valorTipo;
        if (recibir('!')) { verificarTipo(valorUnario(), 2); valorComparación(153); valorTipo = 2; }
        else if (recibir('-')) {
            if (valorClaseTipo() == 257) constanteNumérico(analizarEnteroValor(posición++, true));
            else { verificarTipo(valorUnario(), 1); emitirValor(116); }
            valorTipo = 1;
        } else if (recibir('+')) { verificarTipo(valorUnario(), 1); valorTipo = 1; }
        else valorTipo = expresiónPrimario();
        profundidadExpresión--; return valorTipo;
    }
    static int expresiónMultiplicación() {
        int valorTipo = valorUnario();
        while (!error && (valorClaseTipo() == '*' || valorClaseTipo() == '/' || valorClaseTipo() == '%')) {
            int valorCodificaciónEstado = valorClaseTipo(); posición++; verificarTipo(valorTipo, 1); verificarTipo(valorUnario(), 1);
            emitirValor(valorCodificaciónEstado == '*' ? 104 : valorCodificaciónEstado == '/' ? 108 : 112); valorTipo = 1;
        }
        return valorTipo;
    }
    static int expresiónSuma() {
        int valorTipo = expresiónMultiplicación();
        while (!error && (valorClaseTipo() == '+' || valorClaseTipo() == '-')) {
            int valorCodificaciónEstado = valorClaseTipo(); posición++; int valorFrontera = tamañoCódigo, tipoValorLadoPosterior = expresiónMultiplicación();
            if (valorCodificaciónEstado == '+' && (valorTipo == 3 || tipoValorLadoPosterior == 3)) { valoresCombinar(valorFrontera, valorTipo, tipoValorLadoPosterior); valorTipo = 3; }
            else { verificarTipo(valorTipo, 1); verificarTipo(tipoValorLadoPosterior, 1); emitirValor(valorCodificaciónEstado == '+' ? 96 : 100); valorTipo = 1; }
        }
        return valorTipo;
    }
    static int referenciaAdjuntado(int valorTipo) {
        if (valorTipo != 1 && valorTipo != 2 && valorTipo != 3 && valorTipo != 5) valorFallo("unsupported concatenation type");
        return referenciaExterno(10, "java/lang/StringBuilder", "append", valorTipo == 1 ? "(I)Ljava/lang/StringBuilder;"
            : valorTipo == 2 ? "(Z)Ljava/lang/StringBuilder;" : valorTipo == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void valoresCombinar(int valorFrontera, int tipoValorLadoDelantero, int tipoValorLadoPosterior) {
        // Insertar el código generado antes del código del operando derecho para añadir primero con append el valor izquierdo ya calculado.
        // Las distancias de los saltos relativos dentro de la expresión derecha se conservan porque toda la región se desplaza junta.
        int terminación = tamañoCódigo;
        comando(187, referencia(7, constantePalabra("java/lang/StringBuilder"), 0)); emitirValor(89);
        comando(183, referenciaExterno(10, "java/lang/StringBuilder", "<init>", "()V")); emitirValor(95); comando(182, referenciaAdjuntado(tipoValorLadoDelantero));
        if (error) return;
        int longitud = tamañoCódigo - terminación;
        for (int númeroValor = 0; númeroValor < longitud; númeroValor++) códigoInsertado[númeroValor] = valorCódigo[terminación + númeroValor];
        for (int númeroValor = terminación - 1; númeroValor >= valorFrontera; númeroValor--) valorCódigo[númeroValor + longitud] = valorCódigo[númeroValor];
        for (int númeroValor = 0; númeroValor < longitud; númeroValor++) valorCódigo[valorFrontera + númeroValor] = códigoInsertado[númeroValor];
        comando(182, referenciaAdjuntado(tipoValorLadoPosterior)); comando(182, referenciaExterno(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int expresiónComparación() {
        int valorTipo = expresiónSuma();
        while (!error && (valorClaseTipo() == '<' || valorClaseTipo() == '>' || valorClaseTipo() == 302 || valorClaseTipo() == 303)) {
            int valorCodificaciónEstado = valorClaseTipo(); posición++; verificarTipo(valorTipo, 1); verificarTipo(expresiónSuma(), 1);
            valorComparación(valorCodificaciónEstado == '<' ? 161 : valorCodificaciónEstado == '>' ? 163 : valorCodificaciónEstado == 302 ? 164 : 162); valorTipo = 2;
        }
        return valorTipo;
    }
    static int expresiónIgualdad() {
        int valorTipo = expresiónComparación();
        while (!error && (valorClaseTipo() == 300 || valorClaseTipo() == 301)) {
            int valorCodificaciónEstado = valorClaseTipo(); posición++; int tipoValorLadoPosterior = expresiónComparación();
            if (valorTipo == 0 || tipoValorLadoPosterior == 0) valorFallo("void expression");
            if (!(tipoEnteroValor(valorTipo) && tipoEnteroValor(tipoValorLadoPosterior))) verificarTipo(tipoValorLadoPosterior, valorTipo);
            valorComparación((valorTipo <= 2 || valorTipo == 5 ? 159 : 165) + (valorCodificaciónEstado == 301 ? 1 : 0)); valorTipo = 2;
        }
        return valorTipo;
    }
    static int yLógico() {
        int valorTipo = expresiónIgualdad();
        while (!error && recibir(304)) {
            verificarTipo(valorTipo, 2); int operandoPrimero = rama(153); verificarTipo(expresiónIgualdad(), 2); int operandoSegundo = rama(153);
            emitirValor(4); int terminación = rama(167); valorEnlazar(operandoPrimero, tamañoCódigo); valorEnlazar(operandoSegundo, tamañoCódigo); emitirValor(3); valorEnlazar(terminación, tamañoCódigo); valorTipo = 2;
        }
        return valorTipo;
    }
    static int valorExpresión() {
        int valorTipo = yLógico();
        while (!error && recibir(305)) {
            verificarTipo(valorTipo, 2); int operandoPrimero = rama(154); verificarTipo(yLógico(), 2); int operandoSegundo = rama(154);
            emitirValor(3); int terminación = rama(167); valorEnlazar(operandoPrimero, tamañoCódigo); valorEnlazar(operandoSegundo, tamañoCódigo); emitirValor(4); valorEnlazar(terminación, tamañoCódigo); valorTipo = 2;
        }
        return valorTipo;
    }
    static void valorAsignación(boolean permitirDeclaración) {
        if (valorPalabra(posición, "int") || valorPalabra(posición, "boolean") || valorPalabra(posición, "String") || valorPalabra(posición, "char")
            || valorPalabra(posición, "FileInputStream") || valorPalabra(posición, "FileOutputStream")) {
            if (!permitirDeclaración) valorFallo("declaration not allowed here");
            int valorTipo = valorFormato(), nombre = valorIdentificador(); valorRequisito('='); verificarTipo(valorExpresión(), valorTipo);
            escribirLocal(añadirLocal(nombre, valorTipo)); return;
        }
        int nombre = valorIdentificador(), ámbitoLocal = encontrarLocal(nombre);
        if (recibir('=')) { verificarTipo(valorExpresión(), tipoLocal[ámbitoLocal]); escribirLocal(ámbitoLocal); }
        else if (valorClaseTipo() >= 308 && valorClaseTipo() <= 312) {
            int valorCodificaciónEstado = valorClaseTipo(); posición++; leerLocal(ámbitoLocal); int valorFrontera = tamañoCódigo, tipoValorLadoPosterior = valorExpresión();
            if (valorCodificaciónEstado == 308 && tipoLocal[ámbitoLocal] == 3) valoresCombinar(valorFrontera, 3, tipoValorLadoPosterior);
            else {
                verificarTipo(tipoLocal[ámbitoLocal], 1); verificarTipo(tipoValorLadoPosterior, 1);
                emitirValor(valorCodificaciónEstado == 308 ? 96 : valorCodificaciónEstado == 309 ? 100 : valorCodificaciónEstado == 310 ? 104 : valorCodificaciónEstado == 311 ? 108 : 112);
                if (tipoLocal[ámbitoLocal] == 5) emitirValor(146);
            }
            escribirLocal(ámbitoLocal);
        }
        else if (valorClaseTipo() == 306 || valorClaseTipo() == 307) {
            verificarTipo(tipoLocal[ámbitoLocal], 1); emitirValor(132); emitirValor(ámbitoLocal); emitirValor(valorClaseTipo() == 306 ? 1 : 255); posición++;
            if (tipoLocal[ámbitoLocal] == 5) { leerLocal(ámbitoLocal); emitirValor(146); escribirLocal(ámbitoLocal); }
        } else valorFallo("assignment or postfix increment required");
    }
    static void salidaPantalla() {
        palabraExigir("System"); valorRequisito('.'); palabraExigir("out"); valorRequisito('.');
        boolean nuevaLínea = palabraTomar("println"); if (!nuevaLínea) palabraExigir("print"); valorRequisito('(');
        comando(178, referenciaExterno(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean argumentoVacíoEstado = valorClaseTipo() == ')';
        int valorTipo = argumentoVacíoEstado ? 0 : valorExpresión(); valorRequisito(')'); valorRequisito(';');
        String valorDescripción = valorTipo == 0 ? "()V" : valorTipo == 1 ? "(I)V" : valorTipo == 2 ? "(Z)V" : valorTipo == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (valorTipo == 4 || valorTipo >= 6 || valorTipo == 0 && (!nuevaLínea || !argumentoVacíoEstado)) valorFallo("unsupported print argument");
        comando(182, referenciaExterno(10, "java/io/PrintStream", nuevaLínea ? "println" : "print", valorDescripción));
    }
    static boolean valorInstrucción() {
        if (error) return false;
        if (valorProfundidad > 32) { valorFallo("statement nesting too deep"); return false; }
        if (recibir('{')) {
            valorProfundidad++; boolean resultadoRetornar = false;
            while (!error && valorClaseTipo() != '}') { if (resultadoRetornar) valorFallo("unreachable statement"); resultadoRetornar = valorInstrucción(); }
            valorRequisito('}'); for (int númeroValor = 0; númeroValor < númeroElementosLocal; númeroValor++) if (profundidadLocal[númeroValor] == valorProfundidad) profundidadLocal[númeroValor] = -1;
            valorProfundidad--; return resultadoRetornar;
        }
        if (recibir(';')) return false;
        if (palabraTomar("return")) {
            int valorTipo = valorClaseTipo() == ';' ? 0 : valorExpresión(); verificarTipo(valorTipo, retornarMétodo[métodoActual]); valorRequisito(';');
            emitirValor(valorTipo == 0 ? 177 : valorTipo <= 2 || valorTipo == 5 ? 172 : 176); return true;
        }
        if (palabraTomar("if")) {
            valorRequisito('('); verificarTipo(valorExpresión(), 2); valorRequisito(')'); int valorFalso = rama(153);
            valorProfundidad++; boolean operandoPrimero = instrucciónControl(); valorProfundidad--;
            if (palabraTomar("else")) { int terminación = rama(167); valorEnlazar(valorFalso, tamañoCódigo); valorProfundidad++; boolean operandoSegundo = instrucciónControl(); valorProfundidad--; valorEnlazar(terminación, tamañoCódigo); return operandoPrimero && operandoSegundo; }
            valorEnlazar(valorFalso, tamañoCódigo); return false;
        }
        if (palabraTomar("while")) {
            int ponerEnMarcha = tamañoCódigo; valorRequisito('('); verificarTipo(valorExpresión(), 2); valorRequisito(')'); int terminación = rama(153);
            valorProfundidad++; instrucciónControl(); valorProfundidad--; valorEnlazar(rama(167), ponerEnMarcha); valorEnlazar(terminación, tamañoCódigo); return false;
        }
        if (palabraTomar("for")) {
            valorProfundidad++; valorRequisito('('); if (valorClaseTipo() != ';') valorAsignación(true); valorRequisito(';');
            int condición = tamañoCódigo; if (valorClaseTipo() == ';') emitirValor(4); else verificarTipo(valorExpresión(), 2); valorRequisito(';');
            int terminación = rama(153), textoCuerpo = rama(167), actualizar = tamañoCódigo;
            if (valorClaseTipo() != ')') valorAsignación(false); valorRequisito(')'); valorEnlazar(rama(167), condición); valorEnlazar(textoCuerpo, tamañoCódigo);
            instrucciónControl(); valorEnlazar(rama(167), actualizar); valorEnlazar(terminación, tamañoCódigo);
            for (int númeroValor = 0; númeroValor < númeroElementosLocal; númeroValor++) if (profundidadLocal[númeroValor] == valorProfundidad) profundidadLocal[númeroValor] = -1;
            valorProfundidad--; return false;
        }
        if (valorPalabra(posición, "System")) { salidaPantalla(); return false; }
        if (valorClaseTipo() == 256 && posición + 1 < númeroElementosTokenLéxico && (claseTipoTokenLéxico[posición + 1] == '(' || claseTipoTokenLéxico[posición + 1] == '.')) {
            int valorTipo = valorExpresión(); if (valorTipo != 0) emitirValor(87); valorRequisito(';'); return false;
        }
        valorAsignación(true); valorRequisito(';'); return false;
    }
    static boolean instrucciónControl() {
        if (valorPalabra(posición, "int") || valorPalabra(posición, "boolean") || valorPalabra(posición, "char") || valorPalabra(posición, "String")
            || valorPalabra(posición, "FileInputStream") || valorPalabra(posición, "FileOutputStream")) valorFallo("local declaration requires braces");
        return valorInstrucción();
    }
    static void emitirByteClase(int valor) { if (tamañoSalida == Salida.length) valorFallo("class file too large"); else Salida[tamañoSalida++] = valor & 255; }
    static void emitirCortoClase(int valor) { emitirByteClase(valor >> 8); emitirByteClase(valor); }
    static void emitirEnteroValorClase(int valor) { emitirCortoClase(valor >>> 16); emitirCortoClase(valor); }
    static void escribirClase() {
        emitirEnteroValorClase(0xcafebabe); emitirCortoClase(0); emitirCortoClase(49); emitirCortoClase(númeroElementosConstante);
        for (int númeroValor = 0; númeroValor < tamañoConstante; númeroValor++) emitirByteClase(valorConstante[númeroValor]);
        emitirCortoClase(0x21); emitirCortoClase(constanteClase); emitirCortoClase(constantePadre); emitirCortoClase(0); emitirCortoClase(0); emitirCortoClase(númeroElementosMétodo);
        for (int númeroValor = 0; númeroValor < númeroElementosMétodo; númeroValor++) {
            emitirCortoClase(accesoMétodo[númeroValor]); emitirCortoClase(constanteNombreMétodo[númeroValor]); emitirCortoClase(constanteDescriptorMétodo[númeroValor]); emitirCortoClase(1); emitirCortoClase(constanteCódigo);
            emitirEnteroValorClase(12 + longitudMétodo[númeroValor]); emitirCortoClase(128); emitirCortoClase(variablesLocalesMétodo[númeroValor]); emitirEnteroValorClase(longitudMétodo[númeroValor]);
            for (int entradaElementoRanura = 0; entradaElementoRanura < longitudMétodo[númeroValor]; entradaElementoRanura++) emitirByteClase(valorCódigo[códigoMétodo[númeroValor] + entradaElementoRanura]);
            emitirCortoClase(0); emitirCortoClase(0);
        }
        emitirCortoClase(0);
    }
    public static int ponerEnMarcha() {
        if (Usuario.númeroElementosArgumentos() == 1 && HerramientaJava.textoIgual(Usuario.argumentos(0), "-version")) {
            Usuario.escribir("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (Usuario.númeroElementosArgumentos() != 1) { Usuario.escribir("Usage: javac FILE.java\n"); return 2; }
        int tamañoNombre = HerramientaJava.nombre(textoNombreArchivo, Usuario.argumentos(0));
        if (tamañoNombre < 6 || tamañoNombre > 62 || textoNombreArchivo[tamañoNombre - 5] != '.' || textoNombreArchivo[tamañoNombre - 4] != 'j'
            || textoNombreArchivo[tamañoNombre - 3] != 'a' || textoNombreArchivo[tamañoNombre - 2] != 'v' || textoNombreArchivo[tamañoNombre - 1] != 'a') {
            Usuario.escribir("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        tamañoFuente = Usuario.leerArchivo(textoNombreArchivo, fuente);
        if (tamañoFuente < 0) { Usuario.escribir("javac: cannot read source: "); HerramientaJava.escribirNúmero(tamañoFuente); Usuario.escribirValorCarácter(10); return 1; }
        tamañoFuente = HerramientaJava.decodificarFuente(fuente, tamañoFuente);
        if (tamañoFuente < 0) { Usuario.escribir("javac error: invalid UTF-8 source\n"); return 1; }
        valorCortar(); if (!error) leerDeclaración();
        if (!error) {
            if (longitudTokenLéxico[tokenLéxicoClase] != tamañoNombre - 5) valorFallo("class name must match file name");
            for (int númeroValor = 0; númeroValor < tamañoNombre - 5; númeroValor++) if (fuente[posiciónTokenLéxico[tokenLéxicoClase] + númeroValor] != textoNombreArchivo[númeroValor]) valorFallo("class name must match file name");
        }
        for (métodoActual = 0; métodoActual < númeroElementosMétodo && !error; métodoActual++) {
            posición = cuerpoMétodo[métodoActual]; códigoMétodo[métodoActual] = tamañoCódigo; númeroElementosLocal = 0; valorProfundidad = 0;
            for (int númeroValor = 0; númeroValor < númeroElementosArgumentoMétodo[métodoActual]; númeroValor++) añadirLocal(nombreArgumentoMétodo[métodoActual * 16 + númeroValor], tipoArgumentoMétodo[métodoActual * 16 + númeroValor]);
            boolean resultadoRetornar = valorInstrucción();
            if (!resultadoRetornar && retornarMétodo[métodoActual] != 0) valorFallo("missing return");
            // El punto de unión tras un salto debe ser una instrucción real, según el verificador de versión 49.
            if (retornarMétodo[métodoActual] == 0) emitirValor(177);
            else { boolean EnteroValor = retornarMétodo[métodoActual] <= 2 || retornarMétodo[métodoActual] == 5; emitirValor(EnteroValor ? 3 : 1); emitirValor(EnteroValor ? 172 : 176); }
            if (posición != finMétodo[métodoActual]) valorFallo("invalid method body");
            variablesLocalesMétodo[métodoActual] = númeroElementosLocal; longitudMétodo[métodoActual] = tamañoCódigo - códigoMétodo[métodoActual];
        }
        if (error) return 1;
        escribirClase(); if (error) return 1;
        textoNombreArchivo[tamañoNombre - 4] = 'c'; textoNombreArchivo[tamañoNombre - 3] = 'l'; textoNombreArchivo[tamañoNombre - 2] = 'a';
        textoNombreArchivo[tamañoNombre - 1] = 's'; textoNombreArchivo[tamañoNombre] = 's'; textoNombreArchivo[tamañoNombre + 1] = 0;
        int resultado = Usuario.escribirArchivo(textoNombreArchivo, Salida, tamañoSalida);
        if (resultado < 0) { Usuario.escribir("javac: cannot save class: "); HerramientaJava.escribirNúmero(resultado); Usuario.escribirValorCarácter(10); return 1; }
        Usuario.escribir("Compiled: "); for (int númeroValor = 0; textoNombreArchivo[númeroValor] != 0; númeroValor++) Usuario.escribirValorCarácter(textoNombreArchivo[númeroValor]);
        Usuario.escribir(" (JVM class version 49)\n"); return 0;
    }
}
