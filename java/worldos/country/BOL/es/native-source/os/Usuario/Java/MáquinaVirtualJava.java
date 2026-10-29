// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** JVM restringida que se ejecuta en ring 3. Comprueba límites de archivos, pila, referencias y saltos durante la ejecución. */
public final class MáquinaVirtualJava {
    static int[] Archivo = new int[16384], textoNombreArchivo = new int[64];
    static int[] etiquetaMarcadorConstante = new int[512], valorPrimeroConstante = new int[512], valorSegundoConstante = new int[512], referenciaCadena = new int[512];
    static int[] textoNombreMétodo = new int[32], tipoMétodo = new int[32], accesoMétodo = new int[32];
    static int[] iniciarMétodo = new int[32], finMétodo = new int[32], pilaMétodo = new int[32], variablesLocalesMétodo = new int[32];
    static int[] númeroElementosArgumentoMétodo = new int[32], tipoArgumentoMétodo = new int[512], retornarMétodo = new int[32];
    static int[] valorFrontera = new int[16384];
    static int[] valorLocal = new int[4096], tipoLocal = new int[4096], valorPilaOperando = new int[4096], tipoPilaOperando = new int[4096];
    static int[] métodoMarco = new int[32], posiciónMarco = new int[32], pilaMarco = new int[32];
    static int[] valorMontículo = new int[8192];
    static int tamaño, leerPosición, númeroElementosConstante, númeroElementosMétodo, nombreClase, índiceMarco = -1, posiciónFinMontículo = 1, tipoRetornar;
    static boolean error;

    static void valorFallo(String textoPalabra) {
        if (!error) { Usuario.escribir("JVM error: "); Usuario.escribir(textoPalabra); Usuario.escribirValorCarácter(10); }
        error = true;
    }
    static boolean recortar(int ponerEnMarcha, int longitud) { return ponerEnMarcha >= 0 && longitud >= 0 && ponerEnMarcha <= tamaño - longitud; }
    static int valorByte() {
        if (!recortar(leerPosición, 1)) { valorFallo("truncated class file"); return 0; }
        return Archivo[leerPosición++];
    }
    static int valorCorto() { return valorByte() << 8 | valorByte(); }
    static int EnteroValor() { return valorCorto() << 16 | valorCorto(); }
    static void saltarBytes(int longitud) { if (!recortar(leerPosición, longitud)) valorFallo("invalid attribute size"); else leerPosición += longitud; }
    static boolean comprobarConstante(int númeroValor, int valorClaseTipo) {
        if (númeroValor <= 0 || númeroValor >= númeroElementosConstante || etiquetaMarcadorConstante[númeroValor] != valorClaseTipo) { valorFallo("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean rangoTexto(int ponerEnMarcha, int longitud, String textoPalabra) {
        if (!recortar(ponerEnMarcha, longitud) || longitud != textoPalabra.length()) return false;
        for (int númeroValor = 0; númeroValor < longitud; númeroValor++) if (Archivo[ponerEnMarcha + númeroValor] != textoPalabra.charAt(númeroValor)) return false;
        return true;
    }
    static boolean textoPalabra(int valorConstante, String textoPalabra) { return comprobarConstante(valorConstante, 1) && rangoTexto(valorPrimeroConstante[valorConstante], valorSegundoConstante[valorConstante], textoPalabra); }
    static boolean palabraConcordante(int operandoPrimero, int operandoSegundo) {
        if (!comprobarConstante(operandoPrimero, 1) || !comprobarConstante(operandoSegundo, 1) || valorSegundoConstante[operandoPrimero] != valorSegundoConstante[operandoSegundo]) return false;
        for (int númeroValor = 0; númeroValor < valorSegundoConstante[operandoPrimero]; númeroValor++) if (Archivo[valorPrimeroConstante[operandoPrimero] + númeroValor] != Archivo[valorPrimeroConstante[operandoSegundo] + númeroValor]) return false;
        return true;
    }
    static int textoNombreClase(int númeroValor) { return comprobarConstante(númeroValor, 7) && comprobarConstante(valorPrimeroConstante[númeroValor], 1) ? valorPrimeroConstante[númeroValor] : 0; }
    static int nombreReferencia(int númeroValor) { return comprobarConstante(númeroValor, 12) && comprobarConstante(valorPrimeroConstante[númeroValor], 1) ? valorPrimeroConstante[númeroValor] : 0; }
    static int tipoReferencia(int númeroValor) { return comprobarConstante(númeroValor, 12) && comprobarConstante(valorSegundoConstante[númeroValor], 1) ? valorSegundoConstante[númeroValor] : 0; }
    static int tipoDescriptor(int terminación, boolean tipoVacíoEstado) {
        if (leerPosición >= terminación) { valorFallo("invalid descriptor"); return 0; }
        int valor = valorByte();
        if (valor == 'V' && tipoVacíoEstado) return 0;
        if (valor == 'I' || valor == 'B' || valor == 'C' || valor == 'S' || valor == 'Z') return 1;
        if (valor == '[') { tipoDescriptor(terminación, false); return 2; }
        if (valor == 'L') {
            int ponerEnMarcha = leerPosición;
            while (leerPosición < terminación && Archivo[leerPosición] != ';') leerPosición++;
            if (leerPosición == terminación || leerPosición == ponerEnMarcha) valorFallo("invalid reference descriptor");
            else leerPosición++;
            return 2;
        }
        valorFallo("unsupported descriptor type"); return 0;
    }
    static void leerDescriptor(int Función) {
        int elementoListaElementoPrevio = leerPosición, númeroValor = tipoMétodo[Función];
        if (!comprobarConstante(númeroValor, 1)) return;
        leerPosición = valorPrimeroConstante[númeroValor]; int terminación = leerPosición + valorSegundoConstante[númeroValor];
        if (valorByte() != '(') valorFallo("invalid method descriptor");
        int númeroElementosElementoLista = 0;
        while (!error && leerPosición < terminación && Archivo[leerPosición] != ')') {
            if (númeroElementosElementoLista == 16) { valorFallo("too many method arguments"); break; }
            tipoArgumentoMétodo[Función * 16 + númeroElementosElementoLista++] = tipoDescriptor(terminación, false);
        }
        if (leerPosición >= terminación || valorByte() != ')') valorFallo("invalid method descriptor");
        retornarMétodo[Función] = tipoDescriptor(terminación, true); númeroElementosArgumentoMétodo[Función] = númeroElementosElementoLista;
        if (leerPosición != terminación) valorFallo("invalid method descriptor");
        leerPosición = elementoListaElementoPrevio;
    }
    static void saltarAtributo() {
        int númeroElementosElementoLista = valorCorto();
        for (int númeroValor = 0; númeroValor < númeroElementosElementoLista && !error; númeroValor++) { comprobarConstante(valorCorto(), 1); saltarBytes(EnteroValor()); }
    }
    static int longitudComando(int valor) {
        if (valor == 16 || valor == 18 || valor == 21 || valor == 25 || valor == 54 || valor == 58 || valor == 188) return 2;
        if (valor == 17 || valor == 19 || valor == 132 || valor >= 153 && valor <= 167
            || valor >= 178 && valor <= 184 || valor == 187 || valor == 189 || valor == 192 || valor == 198 || valor == 199) return 3;
        if (valor >= 0 && valor <= 8 || valor >= 26 && valor <= 29 || valor >= 42 && valor <= 46 || valor == 50
            || valor >= 59 && valor <= 62 || valor >= 75 && valor <= 79 || valor == 83 || valor == 87 || valor == 89 || valor == 95
            || valor == 96 || valor == 100 || valor == 104 || valor == 108 || valor == 112 || valor == 116
            || valor == 120 || valor == 122 || valor == 124 || valor == 126 || valor == 128 || valor == 130
            || valor >= 145 && valor <= 147 || valor == 172 || valor == 176 || valor == 177 || valor == 190) return 1;
        return 0;
    }
    static void leerClase() {
        if (EnteroValor() != 0xcafebabe) valorFallo("not a class file");
        int revisiónMenor = valorCorto(), valorVersión = valorCorto();
        if (valorVersión < 45 || valorVersión > 52 || revisiónMenor != 0) valorFallo("supported class versions: 45..52, minor 0");
        númeroElementosConstante = valorCorto();
        if (númeroElementosConstante < 1 || númeroElementosConstante > 512) { valorFallo("constant pool limit (511)"); return; }
        for (int númeroValor = 1; númeroValor < númeroElementosConstante && !error; númeroValor++) {
            int valorClaseTipo = valorByte(); etiquetaMarcadorConstante[númeroValor] = valorClaseTipo;
            if (valorClaseTipo == 1) { valorSegundoConstante[númeroValor] = valorCorto(); valorPrimeroConstante[númeroValor] = leerPosición; saltarBytes(valorSegundoConstante[númeroValor]); }
            else if (valorClaseTipo == 3) valorPrimeroConstante[númeroValor] = EnteroValor();
            else if (valorClaseTipo == 7 || valorClaseTipo == 8) valorPrimeroConstante[númeroValor] = valorCorto();
            else if (valorClaseTipo == 9 || valorClaseTipo == 10 || valorClaseTipo == 12) { valorPrimeroConstante[númeroValor] = valorCorto(); valorSegundoConstante[númeroValor] = valorCorto(); }
            else valorFallo("unsupported constant type");
        }
        int valorPermiso = valorCorto();
        if ((valorPermiso & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) valorFallo("unsupported class flags");
        nombreClase = textoNombreClase(valorCorto());
        if (!textoPalabra(textoNombreClase(valorCorto()), "java/lang/Object")) valorFallo("inheritance unsupported");
        if (valorCorto() != 0) valorFallo("interfaces unsupported");
        if (valorCorto() != 0) valorFallo("fields unsupported");
        númeroElementosMétodo = valorCorto();
        if (númeroElementosMétodo < 1 || númeroElementosMétodo > 32) { valorFallo("method count limit (32)"); return; }
        for (int númeroValor = 0; númeroValor < númeroElementosMétodo && !error; númeroValor++) {
            accesoMétodo[númeroValor] = valorCorto(); textoNombreMétodo[númeroValor] = valorCorto(); tipoMétodo[númeroValor] = valorCorto();
            comprobarConstante(textoNombreMétodo[númeroValor], 1); leerDescriptor(númeroValor);
            if ((accesoMétodo[númeroValor] & (0x100 | 0x400 | 0x20)) != 0) valorFallo("native, abstract and synchronized methods unsupported");
            if ((accesoMétodo[númeroValor] & 8) == 0 && !textoPalabra(textoNombreMétodo[númeroValor], "<init>")) valorFallo("instance methods unsupported");
            if (textoPalabra(textoNombreMétodo[númeroValor], "<clinit>")) valorFallo("class initializers unsupported");
            for (int valorLadoDelantero = 0; valorLadoDelantero < númeroValor; valorLadoDelantero++) if (palabraConcordante(textoNombreMétodo[valorLadoDelantero], textoNombreMétodo[númeroValor]) && palabraConcordante(tipoMétodo[valorLadoDelantero], tipoMétodo[númeroValor])) valorFallo("duplicate method");
            int númeroElementosElementoLista = valorCorto();
            for (int valorAtributo = 0; valorAtributo < númeroElementosElementoLista && !error; valorAtributo++) {
                int nombre = valorCorto(), longitud = EnteroValor(), ponerEnMarcha = leerPosición;
                if (!recortar(ponerEnMarcha, longitud)) { valorFallo("truncated method attribute"); break; }
                if (textoPalabra(nombre, "Code")) {
                    if (iniciarMétodo[númeroValor] != 0) valorFallo("duplicate Code attribute");
                    pilaMétodo[númeroValor] = valorCorto(); variablesLocalesMétodo[númeroValor] = valorCorto(); int longitudCódigo = EnteroValor();
                    if (pilaMétodo[númeroValor] > 128 || variablesLocalesMétodo[númeroValor] > 128 || variablesLocalesMétodo[númeroValor] < númeroElementosArgumentoMétodo[númeroValor]
                        || longitudCódigo < 1 || longitudCódigo > 8192) valorFallo("method memory limits exceeded");
                    iniciarMétodo[númeroValor] = leerPosición; saltarBytes(longitudCódigo); finMétodo[númeroValor] = leerPosición;
                    if (valorCorto() != 0) valorFallo("exception handlers unsupported");
                    saltarAtributo();
                    if (leerPosición != ponerEnMarcha + longitud) valorFallo("Code attribute size mismatch");
                } else saltarBytes(longitud);
            }
            if (iniciarMétodo[númeroValor] == 0) valorFallo("missing Code attribute");
            int entradaElementoRanura = iniciarMétodo[númeroValor];
            while (entradaElementoRanura < finMétodo[númeroValor] && !error) {
                int longitud = longitudComando(Archivo[entradaElementoRanura]);
                if (longitud == 0 || longitud > finMétodo[númeroValor] - entradaElementoRanura) { valorFallo("unsupported or truncated bytecode"); break; }
                valorFrontera[entradaElementoRanura] = númeroValor + 1; entradaElementoRanura += longitud;
            }
            // Rechazar destinos de salto no válidos incluso en rutas que nunca se ejecutan.
            entradaElementoRanura = iniciarMétodo[númeroValor];
            while (entradaElementoRanura < finMétodo[númeroValor] && !error) {
                int valor = Archivo[entradaElementoRanura];
                if (valor >= 153 && valor <= 167 || valor == 198 || valor == 199) {
                    int valorDestino = entradaElementoRanura + (short)(Archivo[entradaElementoRanura + 1] << 8 | Archivo[entradaElementoRanura + 2]);
                    if (valorDestino < iniciarMétodo[númeroValor] || valorDestino >= finMétodo[númeroValor] || valorFrontera[valorDestino] != númeroValor + 1) valorFallo("invalid branch target");
                }
                entradaElementoRanura += longitudComando(valor);
            }
        }
        if (!error) saltarAtributo();
        if (leerPosición != tamaño) valorFallo("extra class file data");
    }
    static int asignarMemoriaAlmacenamiento(int valorClaseTipo, int longitud) {
        if (longitud < 0 || longitud > valorMontículo.length - posiciónFinMontículo - 2) { valorFallo("object heap exhausted or negative array size"); return 0; }
        int referencia = posiciónFinMontículo; posiciónFinMontículo += longitud + 2; valorMontículo[referencia] = valorClaseTipo; valorMontículo[referencia + 1] = longitud;
        return referencia;
    }
    static boolean valorObjeto(int referencia, int valorClaseTipo) {
        if (referencia < 1 || referencia >= posiciónFinMontículo - 1 || valorMontículo[referencia] != valorClaseTipo) { valorFallo("null or invalid object reference"); return false; }
        return true;
    }
    static int textoConstante(int número) {
        if (!comprobarConstante(número, 1)) return 0;
        if (referenciaCadena[número] != 0) return referenciaCadena[número];
        int referencia = asignarMemoriaAlmacenamiento(1, valorSegundoConstante[número]); if (error) return 0;
        int terminación = valorPrimeroConstante[número] + valorSegundoConstante[número], númeroValor = valorPrimeroConstante[número], longitud = 0;
        while (númeroValor < terminación && !error) {
            int valor = Archivo[númeroValor++];
            if (valor == 0) valorFallo("invalid modified UTF-8");
            else if (valor >= 192 && valor <= 223 && númeroValor < terminación) {
                int elementoListaSiguiente = Archivo[númeroValor++];
                if ((elementoListaSiguiente & 192) != 128) valorFallo("invalid modified UTF-8");
                valor = (valor & 31) << 6 | elementoListaSiguiente & 63;
                if (valor != 0 && valor < 128) valorFallo("overlong modified UTF-8");
            } else if (valor >= 224 && valor <= 239 && númeroValor + 1 < terminación) {
                int operandoPrimero = Archivo[númeroValor++], operandoSegundo = Archivo[númeroValor++];
                if ((operandoPrimero & 192) != 128 || (operandoSegundo & 192) != 128) valorFallo("invalid modified UTF-8");
                valor = (valor & 15) << 12 | (operandoPrimero & 63) << 6 | operandoSegundo & 63;
                if (valor < 2048) valorFallo("overlong modified UTF-8");
            } else if (valor >= 128) valorFallo("invalid modified UTF-8");
            valorMontículo[referencia + 2 + longitud++] = valor;
        }
        valorMontículo[referencia + 1] = longitud; referenciaCadena[número] = referencia; return referencia;
    }
    static int carácterAnfitrión(String valor) {
        int referencia = asignarMemoriaAlmacenamiento(1, valor.length()); if (error) return 0;
        for (int númeroValor = 0; númeroValor < valor.length(); númeroValor++) valorMontículo[referencia + 2 + númeroValor] = valor.charAt(númeroValor);
        return referencia;
    }
    static void escribirTexto(int referencia) {
        if (referencia == 0) { Usuario.escribir("null"); return; }
        if (!valorObjeto(referencia, 1)) return;
        for (int númeroValor = 0; númeroValor < valorMontículo[referencia + 1]; númeroValor++) Usuario.escribirValorCarácter(valorMontículo[referencia + 2 + númeroValor]);
    }
    static int carácterDígito(int valor) {
        int referencia = asignarMemoriaAlmacenamiento(1, 11); if (error) return 0;
        int longitud = 0;
        if (valor < 0) valorMontículo[referencia + 2 + longitud++] = '-'; else valor = -valor;
        int índicePosición = 1000000000; boolean ponerEnMarcha = false;
        while (índicePosición != 0) {
            int númeroValor = -(valor / índicePosición);
            if (númeroValor != 0 || ponerEnMarcha || índicePosición == 1) { valorMontículo[referencia + 2 + longitud++] = '0' + númeroValor; ponerEnMarcha = true; }
            valor %= índicePosición; índicePosición /= 10;
        }
        valorMontículo[referencia + 1] = longitud; return referencia;
    }
    static int decodificarEnteroValor(int referencia) {
        if (!valorObjeto(referencia, 1)) return 0;
        int longitud = valorMontículo[referencia + 1], númeroValor = 0, valor = 0; boolean valorNegativo = false;
        if (longitud > 0 && (valorMontículo[referencia + 2] == '-' || valorMontículo[referencia + 2] == '+')) { valorNegativo = valorMontículo[referencia + 2] == '-'; númeroValor++; }
        if (númeroValor == longitud) valorFallo("NumberFormatException");
        for (; númeroValor < longitud && !error; númeroValor++) {
            int valorDígito = valorMontículo[referencia + 2 + númeroValor] - '0';
            if (valorDígito < 0 || valorDígito > 9 || valor < -214748364 || valor == -214748364 && valorDígito > (valorNegativo ? 8 : 7)) valorFallo("NumberFormatException");
            valor = valor * 10 - valorDígito;
        }
        return valorNegativo ? valor : -valor;
    }
    static void ponerValor(int valor, int valorTipo) {
        if (error) return;
        if (índiceMarco < 0 || pilaMarco[índiceMarco] >= pilaMétodo[métodoMarco[índiceMarco]]) { valorFallo("operand stack overflow"); return; }
        int entradaElementoRanura = índiceMarco * 128 + pilaMarco[índiceMarco]++; valorPilaOperando[entradaElementoRanura] = valor; tipoPilaOperando[entradaElementoRanura] = valorTipo;
    }
    static int restarValores(int valorTipo) {
        if (error) return 0;
        if (índiceMarco < 0 || pilaMarco[índiceMarco] < 1) { valorFallo("operand stack underflow"); return 0; }
        int entradaElementoRanura = índiceMarco * 128 + --pilaMarco[índiceMarco]; tipoRetornar = tipoPilaOperando[entradaElementoRanura];
        if (valorTipo != 0 && tipoRetornar != valorTipo) valorFallo("operand type mismatch");
        return valorPilaOperando[entradaElementoRanura];
    }
    static void leerLocal(int número, int valorTipo) {
        if (número >= variablesLocalesMétodo[métodoMarco[índiceMarco]] || número < 0 || tipoLocal[índiceMarco * 128 + número] != valorTipo) { valorFallo("invalid or uninitialized local"); return; }
        ponerValor(valorLocal[índiceMarco * 128 + número], valorTipo);
    }
    static void escribirLocal(int número, int valorTipo) {
        if (número >= variablesLocalesMétodo[métodoMarco[índiceMarco]] || número < 0) { valorFallo("local index out of range"); return; }
        int valor = restarValores(valorTipo); valorLocal[índiceMarco * 128 + número] = valor; tipoLocal[índiceMarco * 128 + número] = valorTipo;
    }
    static int leerByteCódigoOperación() {
        int posición = posiciónMarco[índiceMarco];
        if (posición < iniciarMétodo[métodoMarco[índiceMarco]] || posición >= finMétodo[métodoMarco[índiceMarco]]) { valorFallo("instruction pointer out of range"); return 0; }
        posiciónMarco[índiceMarco]++; return Archivo[posición];
    }
    static int leerCortoCódigoOperación() { return leerByteCódigoOperación() << 8 | leerByteCódigoOperación(); }
    static void valorMover(int posición) {
        int Función = métodoMarco[índiceMarco];
        if (posición < iniciarMétodo[Función] || posición >= finMétodo[Función] || valorFrontera[posición] != Función + 1) valorFallo("invalid branch target");
        else posiciónMarco[índiceMarco] = posición;
    }
    static void invocar(int Función) {
        if (índiceMarco == 31) { valorFallo("call stack limit (32)"); return; }
        int elementoListaSiguiente = índiceMarco + 1;
        for (int númeroValor = 0; númeroValor < 128; númeroValor++) tipoLocal[elementoListaSiguiente * 128 + númeroValor] = 0;
        for (int númeroValor = númeroElementosArgumentoMétodo[Función] - 1; númeroValor >= 0; númeroValor--) {
            valorLocal[elementoListaSiguiente * 128 + númeroValor] = restarValores(tipoArgumentoMétodo[Función * 16 + númeroValor]); tipoLocal[elementoListaSiguiente * 128 + númeroValor] = tipoArgumentoMétodo[Función * 16 + númeroValor];
        }
        índiceMarco = elementoListaSiguiente; métodoMarco[índiceMarco] = Función; posiciónMarco[índiceMarco] = iniciarMétodo[Función]; pilaMarco[índiceMarco] = 0;
    }
    static void resultadoRetornar(int valorTipo) {
        if (valorTipo != retornarMétodo[métodoMarco[índiceMarco]]) { valorFallo("return type mismatch"); return; }
        int valor = valorTipo == 0 ? 0 : restarValores(valorTipo);
        índiceMarco--; if (índiceMarco >= 0 && valorTipo != 0) ponerValor(valor, valorTipo);
    }
    static int[] nombreArchivoFlujo = new int[64];
    static void llamadaFlujoArchivo(int valorPropietario, int nombre, int valorFormato, int comando) {
        boolean Salida = textoPalabra(valorPropietario, "java/io/FileOutputStream");
        int valorClaseTipo = Salida ? 6 : 5;
        if (comando == 183 && textoPalabra(nombre, "<init>")) {
            boolean valorContinuación = false;
            if (Salida && textoPalabra(valorFormato, "(Ljava/lang/String;Z)V")) valorContinuación = restarValores(1) != 0;
            else if (!textoPalabra(valorFormato, "(Ljava/lang/String;)V")) { valorFallo("unsupported file stream constructor"); return; }
            int nombreEntradaElementoArchivo = restarValores(2), valorFlujo = restarValores(2);
            if (!valorObjeto(nombreEntradaElementoArchivo, 1) || !valorObjeto(valorFlujo, valorClaseTipo) || error) return;
            if (valorMontículo[valorFlujo + 3] != 0) { valorFallo("file stream already initialized"); return; }
            int longitud = valorMontículo[nombreEntradaElementoArchivo + 1];
            if (longitud < 1 || longitud > 63) { valorFallo("invalid file name length"); return; }
            for (int entradaElementoRanura = 0; entradaElementoRanura < longitud; entradaElementoRanura++) {
                int valor = valorMontículo[nombreEntradaElementoArchivo + 2 + entradaElementoRanura];
                if (valor < 1 || valor > 127) { valorFallo("file stream paths currently require ASCII"); return; }
                nombreArchivoFlujo[entradaElementoRanura] = valor;
            }
            nombreArchivoFlujo[longitud] = 0;
            int entradaElementoDescriptor = Usuario.abrirDescriptorArchivo(nombreArchivoFlujo, Salida ? (valorContinuación ? 1089 : 577) : 0);
            if (entradaElementoDescriptor < 0) { valorFallo("FileNotFoundException: file open failed"); return; }
            valorMontículo[valorFlujo + 2] = entradaElementoDescriptor; valorMontículo[valorFlujo + 3] = 1;
            return;
        }
        if (comando != 182) { valorFallo("invalid file stream invocation"); return; }
        int acción = -1, valor = 0;
        if (textoPalabra(nombre, "close") && textoPalabra(valorFormato, "()V")) acción = 0;
        if (!Salida && textoPalabra(nombre, "read") && textoPalabra(valorFormato, "()I")) acción = 1;
        if (Salida && textoPalabra(nombre, "write") && textoPalabra(valorFormato, "(I)V")) { acción = 2; valor = restarValores(1); }
        if (acción < 0) { valorFallo("unsupported file stream method"); return; }
        int valorFlujo = restarValores(2);
        if (!valorObjeto(valorFlujo, valorClaseTipo) || error) return;
        if (valorMontículo[valorFlujo + 3] == 0) { valorFallo("uninitialized file stream"); return; }
        int entradaElementoDescriptor = valorMontículo[valorFlujo + 2];
        if (acción == 0) {
            if (entradaElementoDescriptor >= 0 && Usuario.cerrarDescriptorArchivo(entradaElementoDescriptor) < 0) valorFallo("IOException: close failed");
            valorMontículo[valorFlujo + 2] = -1; return;
        }
        if (entradaElementoDescriptor < 0) { valorFallo("IOException: stream closed"); return; }
        if (acción == 1) {
            int resultado = Usuario.leerByteArchivoUno(entradaElementoDescriptor);
            if (resultado < -1) valorFallo("IOException: read failed"); else ponerValor(resultado, 1);
        } else if (Usuario.escribirByteArchivoUno(entradaElementoDescriptor, valor) != 1) valorFallo("IOException: write failed");
    }
    static void llamadaMétodo(int número, int comando) {
        if (!comprobarConstante(número, 10)) return;
        int valorPropietario = textoNombreClase(valorPrimeroConstante[número]), nombre = nombreReferencia(valorSegundoConstante[número]), valorFormato = tipoReferencia(valorSegundoConstante[número]);
        if (error) return;
        if (palabraConcordante(valorPropietario, nombreClase)) {
            if (comando != 184) { valorFallo("only static user methods are supported"); return; }
            for (int númeroValor = 0; númeroValor < númeroElementosMétodo; númeroValor++) if (palabraConcordante(nombre, textoNombreMétodo[númeroValor]) && palabraConcordante(valorFormato, tipoMétodo[númeroValor])) {
                if ((accesoMétodo[númeroValor] & 8) == 0) valorFallo("method is not static"); else invocar(númeroValor);
                return;
            }
            valorFallo("NoSuchMethodError"); return;
        }
        if (textoPalabra(valorPropietario, "java/io/FileInputStream") || textoPalabra(valorPropietario, "java/io/FileOutputStream")) {
            llamadaFlujoArchivo(valorPropietario, nombre, valorFormato, comando); return;
        }
        if (comando == 184 && textoPalabra(valorPropietario, "java/lang/Integer") && textoPalabra(nombre, "parseInt") && textoPalabra(valorFormato, "(Ljava/lang/String;)I")) {
            ponerValor(decodificarEnteroValor(restarValores(2)), 1); return;
        }
        if (comando == 182 && textoPalabra(valorPropietario, "java/io/PrintStream") && (textoPalabra(nombre, "println") || textoPalabra(nombre, "print"))) {
            int valorTipo = 0, valor = 0;
            if (textoPalabra(valorFormato, "(I)V")) { valorTipo = 1; valor = restarValores(1); }
            else if (textoPalabra(valorFormato, "(Z)V")) { valorTipo = 2; valor = restarValores(1); }
            else if (textoPalabra(valorFormato, "(C)V")) { valorTipo = 3; valor = restarValores(1); }
            else if (textoPalabra(valorFormato, "(Ljava/lang/String;)V")) { valorTipo = 4; valor = restarValores(2); }
            else if (!textoPalabra(valorFormato, "()V") || !textoPalabra(nombre, "println")) valorFallo("unsupported print descriptor");
            if (restarValores(2) != -1) valorFallo("invalid PrintStream receiver");
            if (error) return;
            if (valorTipo == 1) HerramientaJava.escribirNúmero(valor);
            if (valorTipo == 2) Usuario.escribir(valor == 0 ? "false" : "true");
            if (valorTipo == 3) Usuario.escribirValorCarácter(valor & 65535);
            if (valorTipo == 4) escribirTexto(valor);
            if (textoPalabra(nombre, "println")) Usuario.escribirValorCarácter(10);
            return;
        }
        if (comando == 182 && textoPalabra(valorPropietario, "java/lang/String")) {
            if (textoPalabra(nombre, "length") && textoPalabra(valorFormato, "()I")) {
                int referencia = restarValores(2); if (valorObjeto(referencia, 1)) ponerValor(valorMontículo[referencia + 1], 1); return;
            }
            if (textoPalabra(nombre, "charAt") && textoPalabra(valorFormato, "(I)C")) {
                int valorÍndiceArreglo = restarValores(1), referencia = restarValores(2);
                if (valorObjeto(referencia, 1)) {
                    if (valorÍndiceArreglo < 0 || valorÍndiceArreglo >= valorMontículo[referencia + 1]) valorFallo("StringIndexOutOfBoundsException"); else ponerValor(valorMontículo[referencia + 2 + valorÍndiceArreglo], 1);
                }
                return;
            }
        }
        if (textoPalabra(valorPropietario, "java/lang/StringBuilder")) {
            if (comando == 183 && textoPalabra(nombre, "<init>") && textoPalabra(valorFormato, "()V")) { valorObjeto(restarValores(2), 4); return; }
            if (comando == 182 && textoPalabra(nombre, "toString") && textoPalabra(valorFormato, "()Ljava/lang/String;")) {
                int referencia = restarValores(2); if (valorObjeto(referencia, 4)) ponerValor(valorMontículo[referencia + 2] == 0 ? carácterAnfitrión("") : valorMontículo[referencia + 2], 2); return;
            }
            if (comando == 182 && textoPalabra(nombre, "append")) {
                int texto = 0;
                if (textoPalabra(valorFormato, "(I)Ljava/lang/StringBuilder;")) texto = carácterDígito(restarValores(1));
                else if (textoPalabra(valorFormato, "(Z)Ljava/lang/StringBuilder;")) texto = carácterAnfitrión(restarValores(1) == 0 ? "false" : "true");
                else if (textoPalabra(valorFormato, "(C)Ljava/lang/StringBuilder;")) {
                    int valor = restarValores(1); texto = asignarMemoriaAlmacenamiento(1, 1); if (!error) valorMontículo[texto + 2] = valor & 65535;
                }
                else if (textoPalabra(valorFormato, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { texto = restarValores(2); if (texto == 0) texto = carácterAnfitrión("null"); }
                else { valorFallo("unsupported StringBuilder append"); return; }
                int referencia = restarValores(2); if (!valorObjeto(referencia, 4) || !valorObjeto(texto, 1)) return;
                int valorLadoDelantero = valorMontículo[referencia + 2], longitudValorLadoDelantero = valorLadoDelantero == 0 ? 0 : valorMontículo[valorLadoDelantero + 1], longitudValorLadoPosterior = valorMontículo[texto + 1];
                int textoNuevo = asignarMemoriaAlmacenamiento(1, longitudValorLadoDelantero + longitudValorLadoPosterior); if (error) return;
                for (int númeroValor = 0; númeroValor < longitudValorLadoDelantero; númeroValor++) valorMontículo[textoNuevo + 2 + númeroValor] = valorMontículo[valorLadoDelantero + 2 + númeroValor];
                for (int númeroValor = 0; númeroValor < longitudValorLadoPosterior; númeroValor++) valorMontículo[textoNuevo + 2 + longitudValorLadoDelantero + númeroValor] = valorMontículo[texto + 2 + númeroValor];
                valorMontículo[referencia + 2] = textoNuevo; ponerValor(referencia, 2); return;
            }
        }
        valorFallo("unsupported library method");
    }
    static int ranuraArreglo(int referencia, int valorÍndiceArreglo, int valorTipo) {
        if (!valorObjeto(referencia, valorTipo)) return 0;
        if (valorÍndiceArreglo < 0 || valorÍndiceArreglo >= valorMontículo[referencia + 1]) { valorFallo("ArrayIndexOutOfBoundsException"); return 0; }
        return referencia + 2 + valorÍndiceArreglo;
    }
    static void ejecutarComando() {
        int datosRestoDivisión = 500000;
        while (índiceMarco >= 0 && !error) {
            if (--datosRestoDivisión == 0) { valorFallo("instruction limit (500000)"); break; }
            int ponerEnMarcha = posiciónMarco[índiceMarco], valor = leerByteCódigoOperación();
            if (error) break;
            if (valor == 0) continue;
            if (valor == 1) { ponerValor(0, 2); continue; }
            if (valor >= 2 && valor <= 8) { ponerValor(valor - 3, 1); continue; }
            if (valor == 16) { ponerValor((byte)leerByteCódigoOperación(), 1); continue; }
            if (valor == 17) { ponerValor((short)leerCortoCódigoOperación(), 1); continue; }
            if (valor == 18 || valor == 19) {
                int númeroValor = valor == 18 ? leerByteCódigoOperación() : leerCortoCódigoOperación();
                if (númeroValor <= 0 || númeroValor >= númeroElementosConstante) valorFallo("invalid ldc constant");
                else if (etiquetaMarcadorConstante[númeroValor] == 3) ponerValor(valorPrimeroConstante[númeroValor], 1);
                else if (etiquetaMarcadorConstante[númeroValor] == 8) ponerValor(textoConstante(valorPrimeroConstante[númeroValor]), 2);
                else valorFallo("unsupported ldc constant");
                continue;
            }
            if (valor == 21 || valor == 25) { leerLocal(leerByteCódigoOperación(), valor == 21 ? 1 : 2); continue; }
            if (valor >= 26 && valor <= 29) { leerLocal(valor - 26, 1); continue; }
            if (valor >= 42 && valor <= 45) { leerLocal(valor - 42, 2); continue; }
            if (valor == 54 || valor == 58) { escribirLocal(leerByteCódigoOperación(), valor == 54 ? 1 : 2); continue; }
            if (valor >= 59 && valor <= 62) { escribirLocal(valor - 59, 1); continue; }
            if (valor >= 75 && valor <= 78) { escribirLocal(valor - 75, 2); continue; }
            if (valor == 46 || valor == 50) {
                int valorÍndiceArreglo = restarValores(1), referencia = restarValores(2), entradaElementoRanura = ranuraArreglo(referencia, valorÍndiceArreglo, valor == 46 ? 2 : 3);
                if (!error) ponerValor(valorMontículo[entradaElementoRanura], valor == 46 ? 1 : 2); continue;
            }
            if (valor == 79 || valor == 83) {
                int elementoElementoLista = restarValores(valor == 79 ? 1 : 2), valorÍndiceArreglo = restarValores(1), referencia = restarValores(2), entradaElementoRanura = ranuraArreglo(referencia, valorÍndiceArreglo, valor == 79 ? 2 : 3);
                if (valor == 83 && elementoElementoLista != 0) valorObjeto(elementoElementoLista, 1);
                if (!error) valorMontículo[entradaElementoRanura] = elementoElementoLista; continue;
            }
            if (valor == 87) { restarValores(0); continue; }
            if (valor == 89) { int operandoPrimero = restarValores(0), valorTipo = tipoRetornar; ponerValor(operandoPrimero, valorTipo); ponerValor(operandoPrimero, valorTipo); continue; }
            if (valor == 95) { int operandoPrimero = restarValores(0), tipoOperandoPrimero = tipoRetornar, operandoSegundo = restarValores(0), tipoOperandoSegundo = tipoRetornar; ponerValor(operandoPrimero, tipoOperandoPrimero); ponerValor(operandoSegundo, tipoOperandoSegundo); continue; }
            if (valor == 96 || valor == 100 || valor == 104 || valor == 108 || valor == 112 || valor == 120
                || valor == 122 || valor == 124 || valor == 126 || valor == 128 || valor == 130) {
                int operandoSegundo = restarValores(1), operandoPrimero = restarValores(1), resultado = 0;
                if ((valor == 108 || valor == 112) && operandoSegundo == 0) { valorFallo("ArithmeticException: / by zero"); continue; }
                if (valor == 96) resultado = operandoPrimero + operandoSegundo;
                if (valor == 100) resultado = operandoPrimero - operandoSegundo;
                if (valor == 104) resultado = operandoPrimero * operandoSegundo;
                if (valor == 108) resultado = operandoPrimero / operandoSegundo;
                if (valor == 112) resultado = operandoPrimero % operandoSegundo;
                if (valor == 120) resultado = operandoPrimero << operandoSegundo;
                if (valor == 122) resultado = operandoPrimero >> operandoSegundo;
                if (valor == 124) resultado = operandoPrimero >>> operandoSegundo;
                if (valor == 126) resultado = operandoPrimero & operandoSegundo;
                if (valor == 128) resultado = operandoPrimero | operandoSegundo;
                if (valor == 130) resultado = operandoPrimero ^ operandoSegundo;
                ponerValor(resultado, 1); continue;
            }
            if (valor == 116) { ponerValor(-restarValores(1), 1); continue; }
            if (valor == 132) {
                int ámbitoLocal = leerByteCódigoOperación(), pasoUnidadIncremento = (byte)leerByteCódigoOperación(); leerLocal(ámbitoLocal, 1); ponerValor(restarValores(1) + pasoUnidadIncremento, 1); escribirLocal(ámbitoLocal, 1); continue;
            }
            if (valor >= 145 && valor <= 147) {
                int númeroValor = restarValores(1); ponerValor(valor == 145 ? (byte)númeroValor : valor == 146 ? (char)númeroValor : (short)númeroValor, 1); continue;
            }
            if (valor >= 153 && valor <= 167 || valor == 198 || valor == 199) {
                int valorDestino = ponerEnMarcha + (short)leerCortoCódigoOperación(); boolean deberíaProseguir = valor == 167;
                if (valor >= 153 && valor <= 158) {
                    int númeroValor = restarValores(1); deberíaProseguir = valor == 153 ? númeroValor == 0 : valor == 154 ? númeroValor != 0 : valor == 155 ? númeroValor < 0 : valor == 156 ? númeroValor >= 0 : valor == 157 ? númeroValor > 0 : númeroValor <= 0;
                } else if (valor >= 159 && valor <= 166) {
                    int operandoSegundo = restarValores(valor >= 165 ? 2 : 1), operandoPrimero = restarValores(valor >= 165 ? 2 : 1);
                    deberíaProseguir = valor == 159 || valor == 165 ? operandoPrimero == operandoSegundo : valor == 160 || valor == 166 ? operandoPrimero != operandoSegundo : valor == 161 ? operandoPrimero < operandoSegundo : valor == 162 ? operandoPrimero >= operandoSegundo : valor == 163 ? operandoPrimero > operandoSegundo : operandoPrimero <= operandoSegundo;
                } else if (valor == 198 || valor == 199) { int númeroValor = restarValores(2); deberíaProseguir = valor == 198 ? númeroValor == 0 : númeroValor != 0; }
                if (deberíaProseguir) valorMover(valorDestino); continue;
            }
            if (valor == 172 || valor == 176 || valor == 177) { resultadoRetornar(valor == 172 ? 1 : valor == 176 ? 2 : 0); continue; }
            if (valor == 178) {
                int númeroValor = leerCortoCódigoOperación(); if (!comprobarConstante(númeroValor, 9)) continue;
                if (!textoPalabra(textoNombreClase(valorPrimeroConstante[númeroValor]), "java/lang/System") || !textoPalabra(nombreReferencia(valorSegundoConstante[númeroValor]), "out")
                    || !textoPalabra(tipoReferencia(valorSegundoConstante[númeroValor]), "Ljava/io/PrintStream;")) valorFallo("unsupported static field");
                else ponerValor(-1, 2); continue;
            }
            if (valor == 182 || valor == 183 || valor == 184) { llamadaMétodo(leerCortoCódigoOperación(), valor); continue; }
            if (valor == 187) {
                int nombre = textoNombreClase(leerCortoCódigoOperación());
                if (textoPalabra(nombre, "java/lang/StringBuilder")) ponerValor(asignarMemoriaAlmacenamiento(4, 1), 2);
                else if (textoPalabra(nombre, "java/io/FileInputStream") || textoPalabra(nombre, "java/io/FileOutputStream")) {
                    int referencia = asignarMemoriaAlmacenamiento(textoPalabra(nombre, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!error) { valorMontículo[referencia + 2] = -1; ponerValor(referencia, 2); }
                } else valorFallo("unsupported object construction");
                continue;
            }
            if (valor == 188 || valor == 189) {
                if (valor == 188) { if (leerByteCódigoOperación() != 10) valorFallo("only int[] newarray is supported"); }
                else if (!textoPalabra(textoNombreClase(leerCortoCódigoOperación()), "java/lang/String")) valorFallo("only String[] anewarray is supported");
                int longitud = restarValores(1); ponerValor(asignarMemoriaAlmacenamiento(valor == 188 ? 2 : 3, longitud), 2); continue;
            }
            if (valor == 190) {
                int referencia = restarValores(2);
                if (referencia < 1 || referencia >= posiciónFinMontículo - 1 || (valorMontículo[referencia] != 2 && valorMontículo[referencia] != 3)) valorFallo("null or invalid array");
                else ponerValor(valorMontículo[referencia + 1], 1); continue;
            }
            if (valor == 192) {
                int nombre = textoNombreClase(leerCortoCódigoOperación()), referencia = restarValores(2);
                if (!textoPalabra(nombre, "java/lang/String")) valorFallo("unsupported checkcast");
                else if (referencia != 0) valorObjeto(referencia, 1);
                ponerValor(referencia, 2); continue;
            }
            valorFallo("unsupported bytecode");
        }
    }
    public static int ponerEnMarcha() {
        if (Usuario.númeroElementosArgumentos() == 1 && HerramientaJava.textoIgual(Usuario.argumentos(0), "-version")) {
            Usuario.escribir("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (Usuario.númeroElementosArgumentos() < 1) { Usuario.escribir("Usage: java CLASS [ARGS]\n"); return 2; }
        int longitud = HerramientaJava.nombre(textoNombreArchivo, Usuario.argumentos(0));
        if (longitud < 1 || longitud > 57) { Usuario.escribir("java: invalid class name\n"); return 2; }
        textoNombreArchivo[longitud] = '.'; textoNombreArchivo[longitud + 1] = 'c'; textoNombreArchivo[longitud + 2] = 'l'; textoNombreArchivo[longitud + 3] = 'a'; textoNombreArchivo[longitud + 4] = 's'; textoNombreArchivo[longitud + 5] = 's';
        tamaño = Usuario.leerArchivo(textoNombreArchivo, Archivo);
        if (tamaño < 0) { Usuario.escribir("java: cannot read class: "); HerramientaJava.escribirNúmero(tamaño); Usuario.escribirValorCarácter(10); return 1; }
        leerClase(); if (error) return 1;
        int nombreCarácter = textoConstante(nombreClase);
        if (!error && valorMontículo[nombreCarácter + 1] != longitud) valorFallo("class name does not match file");
        for (int númeroValor = 0; númeroValor < longitud && !error; númeroValor++) if (valorMontículo[nombreCarácter + 2 + númeroValor] != textoNombreArchivo[númeroValor]) valorFallo("class name does not match file");
        int valorPuntoEntradaElemento = -1;
        for (int númeroValor = 0; númeroValor < númeroElementosMétodo; númeroValor++) if (textoPalabra(textoNombreMétodo[númeroValor], "main") && textoPalabra(tipoMétodo[númeroValor], "([Ljava/lang/String;)V") && (accesoMétodo[númeroValor] & 9) == 9) valorPuntoEntradaElemento = númeroValor;
        if (valorPuntoEntradaElemento < 0) valorFallo("public static void main(String[] args) required");
        if (error) return 1;
        int argumentos = asignarMemoriaAlmacenamiento(3, Usuario.númeroElementosArgumentos() - 1);
        for (int númeroValor = 1; númeroValor < Usuario.númeroElementosArgumentos() && !error; númeroValor++) valorMontículo[argumentos + 1 + númeroValor] = carácterAnfitrión(Usuario.argumentos(númeroValor));
        índiceMarco = 0; métodoMarco[0] = valorPuntoEntradaElemento; posiciónMarco[0] = iniciarMétodo[valorPuntoEntradaElemento]; valorLocal[0] = argumentos; tipoLocal[0] = 2;
        ejecutarComando(); return error ? 1 : 0;
    }
}
