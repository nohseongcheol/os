// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** JVM restringida que se ejecuta en ARM64 EL0. Comprueba límites de archivos, pila, referencias y saltos durante la ejecución. */
public final class MáquinaVirtualJava {
    static int[] Archivo = new int[16 * 16384], archivoTemporal = new int[16384], textoNombreArchivo = new int[512];
    static int[] etiquetaMarcadorConstante = new int[8192], valorPrimeroConstante = new int[8192], valorSegundoConstante = new int[8192], referenciaCadena = new int[8192];
    static int[] textoNombreMétodo = new int[512], tipoMétodo = new int[512], accesoMétodo = new int[512], propietarioMétodo = new int[512];
    static int[] iniciarMétodo = new int[512], finMétodo = new int[512], pilaMétodo = new int[512], variablesLocalesMétodo = new int[512];
    static int[] númeroElementosArgumentoMétodo = new int[512], tipoArgumentoMétodo = new int[8192], retornarMétodo = new int[512];
    static int[] valorFrontera = new int[16 * 16384];
    static int[] valorLocal = new int[16384], tipoLocal = new int[16384], valorPilaOperando = new int[16384], tipoPilaOperando = new int[16384];
    static int[] métodoMarco = new int[128], posiciónMarco = new int[128], pilaMarco = new int[128], instrucciónMáquinaMarco = new int[128], inicializarMarco = new int[128];
    static int[] nombreDefiniciónClase = new int[16], tamañoDefiniciónClase = new int[16], padreDefiniciónClase = new int[16], estadoValorDefiniciónClase = new int[16], númeroElementosRanuraClase = new int[16], inicializarDefiniciónClase = new int[16];
    static int[] interfazClase = new int[16 * 16], númeroElementosInterfazClase = new int[16];
    static int[] nombreRanura = new int[512], tipoRanura = new int[512], propietarioRanura = new int[512], permisosRanura = new int[512], posiciónRanura = new int[512], datosRanura = new int[512];
    static int[] capturarIniciar = new int[1024], capturarFin = new int[1024], capturarPosición = new int[1024], capturarClase = new int[1024], capturarMétodo = new int[1024];
    static int[] valorMontículo = new int[32768], anchuraMontículo = new int[32768], marcaMontículo = new int[32768], referenciaMontículo = new int[32768], esperarPresentarPara = new int[32768];
    static int[] referenciaTemporal = new int[256], elementoArreglo = new int[32768], enteroValorAlmacenar = new int[256];
    static int tamaño, leerPosición, númeroElementosMétodo, nombreClase, índiceMarco = -1, posiciónFinMontículo = 1, tipoRetornar;
    static int númeroElementosDefiniciónClase, númeroElementosRanura, capturarNúmeroElementos, claseAnalizadoActual, objetoLanzado, númeroElementosTemporal, númeroElementosPresentar, númeroElementosColección;
    static int hiloEjecuciónActual, númeroElementosHiloEjecución = 1, definiciónClaseEntradaElemento;
    static int[] marcoHiloEjecución = new int[4], estadoValorHiloEjecución = new int[4], objetoHiloEjecución = new int[4], objetivoHiloEjecución = new int[4], esperarHiloEjecuciónPara = new int[4];
    static boolean error, cambiarPetición;
    static int[] propietarioCerrojo = new int[32768], profundidadCerrojo = new int[32768], cerrojoMarco = new int[128], cerrojoClase = new int[16], hiloEjecuciónClase = new int[16];

    static void valorFallo(String textoPalabra) {
        if (error) return;
        int códigoCategoría = 0;
        if (HerramientaJava.textoIgual(textoPalabra, "ArithmeticException: / by zero")) códigoCategoría = 4;
        if (HerramientaJava.textoIgual(textoPalabra, "NullPointerException") || HerramientaJava.textoIgual(textoPalabra, "null or invalid array")) códigoCategoría = 5;
        if (HerramientaJava.textoIgual(textoPalabra, "ArrayIndexOutOfBoundsException")) códigoCategoría = 7;
        if (HerramientaJava.textoIgual(textoPalabra, "StringIndexOutOfBoundsException")) códigoCategoría = 8;
        if (HerramientaJava.textoIgual(textoPalabra, "NumberFormatException")) códigoCategoría = 10;
        if (HerramientaJava.textoIgual(textoPalabra, "FileNotFoundException: file open failed")) códigoCategoría = 12;
        if (HerramientaJava.textoIgual(textoPalabra, "IOException: stream closed") || HerramientaJava.textoIgual(textoPalabra, "IOException: read failed") || HerramientaJava.textoIgual(textoPalabra, "IOException: write failed")) códigoCategoría = 11;
        if (HerramientaJava.textoIgual(textoPalabra, "ClassCastException")) códigoCategoría = 14;
        if (HerramientaJava.textoIgual(textoPalabra, "NegativeArraySizeException")) códigoCategoría = 15;
        if (códigoCategoría != 0 && índiceMarco >= 0) { lanzarExcepción(códigoCategoría, textoPalabra); return; }
        Usuario.escribir("JVM error: "); Usuario.escribir(textoPalabra); Usuario.escribirValorCarácter(10); error = true;
    }
    static boolean recortar(int ponerEnMarcha, int longitud) {
        if (ponerEnMarcha < 0 || ponerEnMarcha >= Archivo.length || longitud < 0) return false;
        int definiciónClase = ponerEnMarcha / 16384;
        return ponerEnMarcha % 16384 <= tamañoDefiniciónClase[definiciónClase] && longitud <= tamañoDefiniciónClase[definiciónClase] - ponerEnMarcha % 16384;
    }
    static int valorByte() {
        if (!recortar(leerPosición, 1)) { valorFallo("truncated class file"); return 0; }
        return Archivo[leerPosición++];
    }
    static int valorCorto() { return valorByte() << 8 | valorByte(); }
    static int EnteroValor() { return valorCorto() << 16 | valorCorto(); }
    static void saltarBytes(int longitud) { if (!recortar(leerPosición, longitud)) valorFallo("invalid attribute size"); else leerPosición += longitud; }
    static boolean comprobarConstante(int númeroValor, int valorClaseTipo) {
        if (númeroValor <= 0 || númeroValor >= etiquetaMarcadorConstante.length || etiquetaMarcadorConstante[númeroValor] != valorClaseTipo) { valorFallo("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean rangoTexto(int ponerEnMarcha, int longitud, String textoPalabra) {
        if (!recortar(ponerEnMarcha, longitud)) return false;
        int leerCursor = ponerEnMarcha, terminación = ponerEnMarcha + longitud;
        for (int índiceBucle = 0; índiceBucle < textoPalabra.length(); índiceBucle++) {
            int códigoCarácter = textoPalabra.charAt(índiceBucle);
            if (códigoCarácter > 0 && códigoCarácter < 128) { if (leerCursor >= terminación || Archivo[leerCursor++] != códigoCarácter) return false; }
            else if (códigoCarácter < 2048) {
                if (leerCursor + 2 > terminación || Archivo[leerCursor++] != (192 | (códigoCarácter >> 6)) || Archivo[leerCursor++] != (128 | (códigoCarácter & 63))) return false;
            } else if (leerCursor + 3 > terminación || Archivo[leerCursor++] != (224 | (códigoCarácter >> 12)) || Archivo[leerCursor++] != (128 | ((códigoCarácter >> 6) & 63)) || Archivo[leerCursor++] != (128 | (códigoCarácter & 63))) return false;
        }
        return leerCursor == terminación;
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
    static int leerÍndiceConstante() { int valor = valorCorto(); return valor == 0 ? 0 : claseAnalizadoActual * 512 + valor; }
    static int leerConstanteCódigoOperación() { return propietarioMétodo[métodoMarco[índiceMarco]] * 512 + leerCortoCódigoOperación(); }
    static void saltarAtributo() {
        int númeroElementosElementoLista = valorCorto();
        for (int númeroValor = 0; númeroValor < númeroElementosElementoLista && !error; númeroValor++) { comprobarConstante(leerÍndiceConstante(), 1); saltarBytes(EnteroValor()); }
    }
    static int longitudComando(int valor) {
        if (valor == 16 || valor == 18 || valor == 21 || valor == 25 || valor == 54 || valor == 58 || valor == 188) return 2;
        if (valor == 17 || valor == 19 || valor == 132 || valor >= 153 && valor <= 167
            || valor >= 178 && valor <= 184 || valor == 187 || valor == 189 || valor == 192 || valor == 193 || valor == 198 || valor == 199) return 3;
        if (valor == 185 || valor == 200) return 5;
        if (valor >= 0 && valor <= 8 || valor >= 26 && valor <= 29 || valor >= 42 && valor <= 46 || valor >= 50 && valor <= 53
            || valor >= 59 && valor <= 62 || valor >= 75 && valor <= 79 || valor >= 83 && valor <= 95
            || valor == 96 || valor == 100 || valor == 104 || valor == 108 || valor == 112 || valor == 116
            || valor == 120 || valor == 122 || valor == 124 || valor == 126 || valor == 128 || valor == 130
            || valor >= 145 && valor <= 147 || valor == 172 || valor == 176 || valor == 177 || valor == 190 || valor == 191
            || valor == 194 || valor == 195) return 1;
        return 0;
    }
    static int enteroValorPosición(int leerCursor) {
        if (!recortar(leerCursor, 4)) { valorFallo("truncated bytecode operand"); return 0; }
        return Archivo[leerCursor] << 24 | Archivo[leerCursor + 1] << 16 | Archivo[leerCursor + 2] << 8 | Archivo[leerCursor + 3];
    }
    static int leerLongitud(int leerCursor, int ponerEnMarcha, int terminación) {
        int valor = Archivo[leerCursor], longitud = longitudComando(valor);
        if (valor == 170 || valor == 171) {
            int posiciónBase = leerCursor + 1;
            while ((posiciónBase - ponerEnMarcha) % 4 != 0) posiciónBase++;
            if (terminación - posiciónBase < (valor == 170 ? 12 : 8)) return 0;
            int númeroElementosEntradaElemento = valor == 170 ? enteroValorPosición(posiciónBase + 8) - enteroValorPosición(posiciónBase + 4) + 1 : enteroValorPosición(posiciónBase + 4);
            if (númeroElementosEntradaElemento < 0 || númeroElementosEntradaElemento > 2048) return 0;
            longitud = posiciónBase - leerCursor + (valor == 170 ? 12 + 4 * númeroElementosEntradaElemento : 8 + 8 * númeroElementosEntradaElemento);
        }
        if (valor == 196 && leerCursor + 1 < terminación) {
            int datosPalabra = Archivo[leerCursor + 1]; longitud = datosPalabra == 132 ? 6 : (datosPalabra == 21 || datosPalabra == 25 || datosPalabra == 54 || datosPalabra == 58) ? 4 : 0;
        }
        return longitud > 0 && longitud <= terminación - leerCursor ? longitud : 0;
    }
    static void comprobarValorDestino(int valorDestino, int Función) {
        if (valorDestino < iniciarMétodo[Función] || valorDestino >= finMétodo[Función] || valorFrontera[valorDestino] != Función + 1) valorFallo("invalid branch target");
    }
    static void leerClase(int definiciónClase) {
        claseAnalizadoActual = definiciónClase; leerPosición = definiciónClase * 16384; tamaño = leerPosición + tamañoDefiniciónClase[definiciónClase];
        if (EnteroValor() != 0xcafebabe) { valorFallo("not a class file"); return; }
        int revisiónMenor = valorCorto(), valorVersión = valorCorto();
        if (valorVersión < 45 || valorVersión > 52 || revisiónMenor != 0) { valorFallo("supported class versions: 45..52, minor 0"); return; }
        int númeroElementosConstante = valorCorto(), posiciónBase = definiciónClase * 512;
        if (númeroElementosConstante < 1 || númeroElementosConstante > 512) { valorFallo("constant pool limit (511)"); return; }
        for (int númeroElementosEntradaElemento = 1; númeroElementosEntradaElemento < númeroElementosConstante && !error; númeroElementosEntradaElemento++) {
            int númeroValor = posiciónBase + númeroElementosEntradaElemento, valorClaseTipo = valorByte(); etiquetaMarcadorConstante[númeroValor] = valorClaseTipo;
            if (valorClaseTipo == 1) { valorSegundoConstante[númeroValor] = valorCorto(); valorPrimeroConstante[númeroValor] = leerPosición; saltarBytes(valorSegundoConstante[númeroValor]); }
            else if (valorClaseTipo == 3) valorPrimeroConstante[númeroValor] = EnteroValor();
            else if (valorClaseTipo == 7 || valorClaseTipo == 8) valorPrimeroConstante[númeroValor] = leerÍndiceConstante();
            else if (valorClaseTipo == 9 || valorClaseTipo == 10 || valorClaseTipo == 11 || valorClaseTipo == 12) { valorPrimeroConstante[númeroValor] = leerÍndiceConstante(); valorSegundoConstante[númeroValor] = leerÍndiceConstante(); }
            else valorFallo("unsupported constant type");
        }
        int valorPermiso = valorCorto();
        if ((valorPermiso & (0x2000 | 0x4000)) != 0) valorFallo("annotation/enum class unsupported");
        nombreDefiniciónClase[definiciónClase] = textoNombreClase(leerÍndiceConstante());
        padreDefiniciónClase[definiciónClase] = textoNombreClase(leerÍndiceConstante());
        int númeroElementosInterfaz = valorCorto(); if (númeroElementosInterfaz > 16) { valorFallo("interface count limit"); return; }
        númeroElementosInterfazClase[definiciónClase] = númeroElementosInterfaz;
        for (int índiceBucle = 0; índiceBucle < númeroElementosInterfaz; índiceBucle++) interfazClase[definiciónClase * 16 + índiceBucle] = textoNombreClase(leerÍndiceConstante());
        int númeroElementosCampo = valorCorto();
        if (númeroElementosCampo > 512 - númeroElementosRanura) { valorFallo("field count limit (512)"); return; }
        for (int índiceBucle = 0; índiceBucle < númeroElementosCampo && !error; índiceBucle++) {
            int índiceArchivo = númeroElementosRanura++; propietarioRanura[índiceArchivo] = definiciónClase; permisosRanura[índiceArchivo] = valorCorto(); nombreRanura[índiceArchivo] = leerÍndiceConstante(); tipoRanura[índiceArchivo] = leerÍndiceConstante();
            comprobarConstante(nombreRanura[índiceArchivo], 1); comprobarConstante(tipoRanura[índiceArchivo], 1);
            int valorPreservado = leerPosición; leerPosición = valorPrimeroConstante[tipoRanura[índiceArchivo]]; int códigoCategoría = tipoDescriptor(leerPosición + valorSegundoConstante[tipoRanura[índiceArchivo]], false); leerPosición = valorPreservado;
            if ((permisosRanura[índiceArchivo] & 8) == 0) posiciónRanura[índiceArchivo] = númeroElementosRanuraClase[definiciónClase]++;
            int datosAtributo = valorCorto();
            for (int posiciónInterior = 0; posiciónInterior < datosAtributo && !error; posiciónInterior++) {
                int constanteNombre = leerÍndiceConstante(), longitudVálido = EnteroValor();
                if (textoPalabra(constanteNombre, "ConstantValue") && longitudVálido == 2) {
                    int valorDatos = leerÍndiceConstante();
                    if (códigoCategoría == 1 && comprobarConstante(valorDatos, 3)) datosRanura[índiceArchivo] = valorPrimeroConstante[valorDatos];
                    else if (códigoCategoría == 2 && comprobarConstante(valorDatos, 8)) datosRanura[índiceArchivo] = textoConstante(valorPrimeroConstante[valorDatos]);
                } else saltarBytes(longitudVálido);
            }
        }
        int númeroElementosElementoLista = valorCorto();
        if (númeroElementosElementoLista > 512 - númeroElementosMétodo) { valorFallo("method count limit (512)"); return; }
        for (int índiceBucle = 0; índiceBucle < númeroElementosElementoLista && !error; índiceBucle++) {
            int númeroValor = númeroElementosMétodo++; propietarioMétodo[númeroValor] = definiciónClase;
            accesoMétodo[númeroValor] = valorCorto(); textoNombreMétodo[númeroValor] = leerÍndiceConstante(); tipoMétodo[númeroValor] = leerÍndiceConstante();
            comprobarConstante(textoNombreMétodo[númeroValor], 1); leerDescriptor(númeroValor);
            if ((accesoMétodo[númeroValor] & 8) == 0) {
                if (númeroElementosArgumentoMétodo[númeroValor] == 16) { valorFallo("too many instance method arguments"); return; }
                for (int posiciónComparación = númeroElementosArgumentoMétodo[númeroValor]; posiciónComparación > 0; posiciónComparación--) tipoArgumentoMétodo[númeroValor * 16 + posiciónComparación] = tipoArgumentoMétodo[númeroValor * 16 + posiciónComparación - 1];
                tipoArgumentoMétodo[númeroValor * 16] = 2; númeroElementosArgumentoMétodo[númeroValor]++;
            }
            if ((accesoMétodo[númeroValor] & 0x100) != 0) valorFallo("user native method unsupported");
            if (textoPalabra(textoNombreMétodo[númeroValor], "<clinit>")) inicializarDefiniciónClase[definiciónClase] = númeroValor + 1;
            for (int valorLadoDelantero = 0; valorLadoDelantero < númeroValor; valorLadoDelantero++) if (propietarioMétodo[valorLadoDelantero] == definiciónClase && palabraConcordante(textoNombreMétodo[valorLadoDelantero], textoNombreMétodo[númeroValor]) && palabraConcordante(tipoMétodo[valorLadoDelantero], tipoMétodo[númeroValor])) valorFallo("duplicate method");
            int númeroElementosAtributo = valorCorto();
            for (int valorAtributo = 0; valorAtributo < númeroElementosAtributo && !error; valorAtributo++) {
                int nombre = leerÍndiceConstante(), longitud = EnteroValor(), ponerEnMarcha = leerPosición;
                if (!recortar(ponerEnMarcha, longitud)) { valorFallo("truncated method attribute"); break; }
                if (textoPalabra(nombre, "Code")) {
                    if (iniciarMétodo[númeroValor] != 0) valorFallo("duplicate Code attribute");
                    pilaMétodo[númeroValor] = valorCorto(); variablesLocalesMétodo[númeroValor] = valorCorto(); int longitudCódigo = EnteroValor();
                    if (pilaMétodo[númeroValor] > 128 || variablesLocalesMétodo[númeroValor] > 128 || variablesLocalesMétodo[númeroValor] < númeroElementosArgumentoMétodo[númeroValor]
                        || longitudCódigo < 1 || longitudCódigo > 8192) valorFallo("method memory limits exceeded");
                    iniciarMétodo[númeroValor] = leerPosición; saltarBytes(longitudCódigo); finMétodo[númeroValor] = leerPosición;
                    int númeroElementosCapturaEnCurso = valorCorto();
                    if (númeroElementosCapturaEnCurso > 1024 - capturarNúmeroElementos) { valorFallo("exception table limit"); return; }
                    for (int posiciónInterior = 0; posiciónInterior < númeroElementosCapturaEnCurso; posiciónInterior++) {
                        int referenciaError = capturarNúmeroElementos++; capturarMétodo[referenciaError] = númeroValor;
                        capturarIniciar[referenciaError] = iniciarMétodo[númeroValor] + valorCorto(); capturarFin[referenciaError] = iniciarMétodo[númeroValor] + valorCorto();
                        capturarPosición[referenciaError] = iniciarMétodo[númeroValor] + valorCorto(); int valorCodificado = leerÍndiceConstante(); capturarClase[referenciaError] = valorCodificado == 0 ? 0 : textoNombreClase(valorCodificado);
                    }
                    saltarAtributo();
                    if (leerPosición != ponerEnMarcha + longitud) valorFallo("Code attribute size mismatch");
                } else saltarBytes(longitud);
            }
            if ((accesoMétodo[númeroValor] & 0x400) != 0) continue;
            if (iniciarMétodo[númeroValor] == 0) valorFallo("missing Code attribute");
            int entradaElementoRanura = iniciarMétodo[númeroValor];
            while (entradaElementoRanura < finMétodo[númeroValor] && !error) {
                int longitud = leerLongitud(entradaElementoRanura, iniciarMétodo[númeroValor], finMétodo[númeroValor]);
                if (longitud == 0) { valorFallo("unsupported or truncated bytecode"); break; }
                valorFrontera[entradaElementoRanura] = númeroValor + 1; entradaElementoRanura += longitud;
            }
            entradaElementoRanura = iniciarMétodo[númeroValor];
            while (entradaElementoRanura < finMétodo[númeroValor] && !error) {
                int valor = Archivo[entradaElementoRanura];
                if (valor >= 153 && valor <= 167 || valor == 198 || valor == 199) comprobarValorDestino(entradaElementoRanura + (short)(Archivo[entradaElementoRanura + 1] << 8 | Archivo[entradaElementoRanura + 2]), númeroValor);
                if (valor == 200) comprobarValorDestino(entradaElementoRanura + enteroValorPosición(entradaElementoRanura + 1), númeroValor);
                if (valor == 170 || valor == 171) {
                    int leerCursor = entradaElementoRanura + 1; while ((leerCursor - iniciarMétodo[númeroValor]) % 4 != 0) leerCursor++;
                    comprobarValorDestino(entradaElementoRanura + enteroValorPosición(leerCursor), númeroValor);
                    int númeroElementosEntradaElemento = valor == 170 ? enteroValorPosición(leerCursor + 8) - enteroValorPosición(leerCursor + 4) + 1 : enteroValorPosición(leerCursor + 4);
                    leerCursor += valor == 170 ? 12 : 8;
                    for (int posiciónInterior = 0; posiciónInterior < númeroElementosEntradaElemento; posiciónInterior++) comprobarValorDestino(entradaElementoRanura + enteroValorPosición(leerCursor + posiciónInterior * (valor == 170 ? 4 : 8) + (valor == 170 ? 0 : 4)), númeroValor);
                }
                entradaElementoRanura += leerLongitud(entradaElementoRanura, iniciarMétodo[númeroValor], finMétodo[númeroValor]);
            }
            for (int posiciónInterior = 0; posiciónInterior < capturarNúmeroElementos; posiciónInterior++) if (capturarMétodo[posiciónInterior] == númeroValor) {
                comprobarValorDestino(capturarIniciar[posiciónInterior], númeroValor); comprobarValorDestino(capturarPosición[posiciónInterior], númeroValor);
                if (capturarFin[posiciónInterior] != finMétodo[númeroValor]) comprobarValorDestino(capturarFin[posiciónInterior], númeroValor);
                if (capturarIniciar[posiciónInterior] >= capturarFin[posiciónInterior]) valorFallo("invalid exception range");
            }
        }
        if (!error) saltarAtributo();
        if (leerPosición != tamaño) valorFallo("extra class file data");
    }
    static int asignarMemoriaAlmacenamiento(int valorClaseTipo, int longitud) { return memoriaNuevo(valorClaseTipo, longitud); }
    static boolean valorObjeto(int referencia, int valorClaseTipo) {
        if (!esObjetoVálido(referencia)) return false;
        if (valorMontículo[referencia] != valorClaseTipo) { valorFallo("object type mismatch"); return false; }
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
        if (tipoRetornar == 2) protegerValor(valorPilaOperando[entradaElementoRanura]);
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
        if (índiceMarco % 32 == 31) { valorFallo("call stack limit (32)"); return; }
        int elementoListaSiguiente = índiceMarco + 1;
        for (int númeroValor = 0; númeroValor < 128; númeroValor++) tipoLocal[elementoListaSiguiente * 128 + númeroValor] = 0;
        for (int númeroValor = númeroElementosArgumentoMétodo[Función] - 1; númeroValor >= 0; númeroValor--) {
            valorLocal[elementoListaSiguiente * 128 + númeroValor] = restarValores(tipoArgumentoMétodo[Función * 16 + númeroValor]); tipoLocal[elementoListaSiguiente * 128 + númeroValor] = tipoArgumentoMétodo[Función * 16 + númeroValor];
        }
        if (error) return;
        índiceMarco = elementoListaSiguiente; inicializarMarco[índiceMarco] = 0; métodoMarco[índiceMarco] = Función; posiciónMarco[índiceMarco] = iniciarMétodo[Función]; pilaMarco[índiceMarco] = 0;
    }
    static void resultadoRetornar(int valorTipo) {
        if (valorTipo != retornarMétodo[métodoMarco[índiceMarco]]) { valorFallo("return type mismatch"); return; }
        int valor = valorTipo == 0 ? 0 : restarValores(valorTipo);
        if (inicializarMarco[índiceMarco] != 0) estadoValorDefiniciónClase[inicializarMarco[índiceMarco] - 1] = 2;
        if (cerrojoMarco[índiceMarco] != 0) { liberarCerrojo(cerrojoMarco[índiceMarco]); cerrojoMarco[índiceMarco] = 0; }
        índiceMarco--; if (índiceMarco >= hiloEjecuciónActual * 32 && valorTipo != 0) ponerValor(valor, valorTipo);
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
                if (valor < 1) { valorFallo("invalid file stream path"); return; }
                nombreArchivoFlujo[entradaElementoRanura] = valor;
            }
            nombreArchivoFlujo[longitud] = 0;
            int entradaElementoDescriptor = Usuario.abrirDescriptorArchivo(nombreArchivoFlujo, Salida ? (valorContinuación ? 1089 : 577) : 0);
            if (entradaElementoDescriptor < 0) { valorFallo("FileNotFoundException: file open failed"); return; }
            valorMontículo[valorFlujo + 2] = entradaElementoDescriptor; valorMontículo[valorFlujo + 3] = 1;
            return;
        }
        if (comando != 182) { valorFallo("invalid file stream invocation"); return; }
        if ((Salida && textoPalabra(nombre, "write") || !Salida && textoPalabra(nombre, "read"))
            && (textoPalabra(valorFormato, Salida ? "([B)V" : "([B)I") || textoPalabra(valorFormato, Salida ? "([BII)V" : "([BII)I"))) {
            boolean valorRecortar = textoPalabra(valorFormato, Salida ? "([BII)V" : "([BII)I");
            int númeroElementosEntradaElemento = valorRecortar ? restarValores(1) : 0, puntoInicial = valorRecortar ? restarValores(1) : 0, arregloDatos = restarValores(2), referenciaObjeto = restarValores(2);
            if (!valorObjeto(arregloDatos, 20) || !valorObjeto(referenciaObjeto, valorClaseTipo)) return;
            if (!valorRecortar) númeroElementosEntradaElemento = valorMontículo[arregloDatos + 1];
            if (puntoInicial < 0 || númeroElementosEntradaElemento < 0 || puntoInicial > valorMontículo[arregloDatos + 1] - númeroElementosEntradaElemento) { lanzarExcepción(6, "file buffer bounds"); return; }
            if (valorMontículo[referenciaObjeto + 3] == 0 || valorMontículo[referenciaObjeto + 2] < 0) { valorFallo("IOException: stream closed"); return; }
            int númeroElementosCompletado = 0;
            while (númeroElementosCompletado < númeroElementosEntradaElemento && !error) {
                int valorDevuelto = Salida ? Usuario.escribirByteArchivoUno(valorMontículo[referenciaObjeto + 2], valorMontículo[arregloDatos + 2 + puntoInicial + númeroElementosCompletado]) : Usuario.leerByteArchivoUno(valorMontículo[referenciaObjeto + 2]);
                if (valorDevuelto < 0) { valorFallo(Salida ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Salida && valorDevuelto == 256) break;
                if (!Salida) valorMontículo[arregloDatos + 2 + puntoInicial + númeroElementosCompletado] = (byte)valorDevuelto;
                númeroElementosCompletado++;
            }
            if (!Salida) ponerValor(númeroElementosEntradaElemento != 0 && númeroElementosCompletado == 0 ? -1 : númeroElementosCompletado, 1);
            return;
        }
        if (Salida && textoPalabra(nombre, "flush") && textoPalabra(valorFormato, "()V")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, valorClaseTipo) && valorMontículo[referenciaObjeto + 2] < 0) valorFallo("IOException: stream closed"); return; }
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
            if (resultado < -1) valorFallo("IOException: read failed"); else ponerValor(resultado == 256 ? -1 : resultado, 1);
        } else if (Usuario.escribirByteArchivoUno(entradaElementoDescriptor, valor) != 1) valorFallo("IOException: write failed");
    }
    static void llamadaMétodo(int número, int comando) {
        if (número <= 0 || número >= etiquetaMarcadorConstante.length || (etiquetaMarcadorConstante[número] != 10 && etiquetaMarcadorConstante[número] != 11)) { valorFallo("invalid method reference"); return; }
        int valorPropietario = textoNombreClase(valorPrimeroConstante[número]), nombre = nombreReferencia(valorSegundoConstante[número]), valorFormato = tipoReferencia(valorSegundoConstante[número]);
        if (error) return;
        if (invocarPredeterminado(valorPropietario, nombre, valorFormato, comando)) return;
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
        int definiciónClase = encontrarDefiniciónClase(valorPropietario); if (definiciónClase < 0 || error) return;
        int índiceArchivo = encontrarMétodo(definiciónClase, nombre, valorFormato);
        if (índiceArchivo < 0) {
            for (int códigoCarácter = definiciónClase, númeroElementosEntradaElemento = 0; códigoCarácter >= 0 && númeroElementosEntradaElemento < 16; númeroElementosEntradaElemento++, códigoCarácter = clasePadre(códigoCarácter))
                if (textoPalabra(padreDefiniciónClase[códigoCarácter], "java/lang/Thread")) { invocarHiloEjecución(nombre, valorFormato, comando); return; }
            valorFallo("NoSuchMethodError"); return;
        }
        if (((accesoMétodo[índiceArchivo] & 8) != 0) != (comando == 184)) { valorFallo("method static/instance mismatch"); return; }
        if (comando == 184) { if (!inicializar(propietarioMétodo[índiceArchivo], instrucciónMáquinaMarco[índiceMarco])) return; }
        else {
            int leerCursor = pilaMarco[índiceMarco] - númeroElementosArgumentoMétodo[índiceArchivo];
            if (leerCursor < 0 || tipoPilaOperando[índiceMarco * 128 + leerCursor] != 2) { valorFallo("invalid method receiver"); return; }
            int referenciaObjeto = valorPilaOperando[índiceMarco * 128 + leerCursor];
            if (!esObjetoVálido(referenciaObjeto)) return;
            if (valorMontículo[referenciaObjeto] < 32 || !claseContiene(valorMontículo[referenciaObjeto] - 32, valorPropietario)) { valorFallo("method receiver type mismatch"); return; }
            if (comando != 183) índiceArchivo = encontrarMétodo(valorMontículo[referenciaObjeto] - 32, nombre, valorFormato);
        }
        if (índiceArchivo < 0 || (accesoMétodo[índiceArchivo] & 0x400) != 0) { valorFallo("AbstractMethodError"); return; }
        int referenciaCerrojo = 0;
        if ((accesoMétodo[índiceArchivo] & 32) != 0) {
            if (comando == 184) { int códigoCarácter = propietarioMétodo[índiceArchivo]; if (cerrojoClase[códigoCarácter] == 0) cerrojoClase[códigoCarácter] = asignarMemoriaAlmacenamiento(8, 0); referenciaCerrojo = cerrojoClase[códigoCarácter]; }
            else referenciaCerrojo = valorPilaOperando[índiceMarco * 128 + pilaMarco[índiceMarco] - númeroElementosArgumentoMétodo[índiceArchivo]];
            if (!adquirirCerrojo(referenciaCerrojo)) { if (!error) posiciónMarco[índiceMarco] = instrucciónMáquinaMarco[índiceMarco]; return; }
        }
        invocar(índiceArchivo); if (!error) cerrojoMarco[índiceMarco] = referenciaCerrojo;
    }
    static boolean puedeArregloAlmacenar(int referenciaArreglo, int valorDatos) {
        if (valorDatos == 0 || elementoArreglo[referenciaArreglo] == 0) return true;
        boolean esExitoso = elementoArreglo[referenciaArreglo] == -1 ? (valorDatos > 0 && valorDatos < posiciónFinMontículo && valorMontículo[valorDatos] == 1) : objetoConcordante(valorDatos, elementoArreglo[referenciaArreglo]);
        if (!esExitoso && !error) lanzarExcepción(17, "array element type mismatch");
        return esExitoso;
    }
    static int ranuraArreglo(int referencia, int valorÍndiceArreglo, int valorTipo) {
        if (!valorObjeto(referencia, valorTipo)) return 0;
        if (valorÍndiceArreglo < 0 || valorÍndiceArreglo >= valorMontículo[referencia + 1]) { valorFallo("ArrayIndexOutOfBoundsException"); return 0; }
        return referencia + 2 + valorÍndiceArreglo;
    }
    static void ejecutarComando() {
        int datosRestoDivisión = 500000, valorFragmento = 100;
        while (true) {
            if (error) { if (objetoLanzado != 0) excepciónManejador(); if (error || índiceMarco < hiloEjecuciónActual * 32) break; }
            if (índiceMarco < hiloEjecuciónActual * 32 || cambiarPetición || --valorFragmento == 0) { if (!hiloEjecuciónConmutar()) break; valorFragmento = 100; }
            if (índiceMarco == 0 && estadoValorDefiniciónClase[definiciónClaseEntradaElemento] != 2 && !inicializar(definiciónClaseEntradaElemento, posiciónMarco[índiceMarco])) continue;
            if (índiceMarco == hiloEjecuciónActual * 32 && hiloEjecuciónActual != 0 && (accesoMétodo[métodoMarco[índiceMarco]] & 32) != 0 && cerrojoMarco[índiceMarco] == 0) {
                int referenciaObjeto = objetivoHiloEjecución[hiloEjecuciónActual]; if (!adquirirCerrojo(referenciaObjeto)) { if (error) break; continue; } cerrojoMarco[índiceMarco] = referenciaObjeto;
            }
            númeroElementosTemporal = 0;
            if (--datosRestoDivisión == 0) { valorFallo("instruction limit (500000)"); break; }
            int ponerEnMarcha = posiciónMarco[índiceMarco]; instrucciónMáquinaMarco[índiceMarco] = ponerEnMarcha; int valor = leerByteCódigoOperación();
            if (error) break;
            if (valor == 0) continue;
            if (valor == 1) { ponerValor(0, 2); continue; }
            if (valor >= 2 && valor <= 8) { ponerValor(valor - 3, 1); continue; }
            if (valor == 16) { ponerValor((byte)leerByteCódigoOperación(), 1); continue; }
            if (valor == 17) { ponerValor((short)leerCortoCódigoOperación(), 1); continue; }
            if (valor == 18 || valor == 19) {
                int númeroValor = propietarioMétodo[métodoMarco[índiceMarco]] * 512 + (valor == 18 ? leerByteCódigoOperación() : leerCortoCódigoOperación());
                if (númeroValor <= 0 || númeroValor >= etiquetaMarcadorConstante.length) valorFallo("invalid ldc constant");
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
            if (valor == 46 || valor >= 50 && valor <= 53) {
                int posiciónEntradaElemento = restarValores(1), referenciaObjeto = restarValores(2), códigoCategoría = valor == 46 ? 2 : valor == 50 ? 3 : valor == 51 ? 20 : valor == 52 ? 22 : 23;
                if (valor == 51 && referenciaObjeto > 0 && referenciaObjeto < posiciónFinMontículo && valorMontículo[referenciaObjeto] == 21) códigoCategoría = 21;
                int leerCursor = ranuraArreglo(referenciaObjeto, posiciónEntradaElemento, códigoCategoría); if (!error) ponerValor(valorMontículo[leerCursor], valor == 50 ? 2 : 1); continue;
            }
            if (valor == 79 || valor >= 83 && valor <= 86) {
                int referenciaEntradaElemento = restarValores(valor == 83 ? 2 : 1), posiciónEntradaElemento = restarValores(1), referenciaObjeto = restarValores(2), códigoCategoría = valor == 79 ? 2 : valor == 83 ? 3 : valor == 84 ? 20 : valor == 85 ? 22 : 23;
                if (valor == 84 && referenciaObjeto > 0 && referenciaObjeto < posiciónFinMontículo && valorMontículo[referenciaObjeto] == 21) códigoCategoría = 21;
                int leerCursor = ranuraArreglo(referenciaObjeto, posiciónEntradaElemento, códigoCategoría);
                if (!error && códigoCategoría == 3 && !puedeArregloAlmacenar(referenciaObjeto, referenciaEntradaElemento)) continue;
                if (!error) valorMontículo[leerCursor] = códigoCategoría == 20 ? (byte)referenciaEntradaElemento : códigoCategoría == 21 ? referenciaEntradaElemento & 1 : códigoCategoría == 22 ? (char)referenciaEntradaElemento : códigoCategoría == 23 ? (short)referenciaEntradaElemento : referenciaEntradaElemento;
                continue;
            }
            if (valor >= 87 && valor <= 95) { instrucciónMáquinaPila(valor); continue; }
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
            if (valor >= 178 && valor <= 181) { invocarCampo(leerConstanteCódigoOperación(), valor, ponerEnMarcha); continue; }
            if (valor >= 182 && valor <= 185) {
                int valorCodificado = leerConstanteCódigoOperación();
                if (valor == 185) { int númeroElementosTotal = leerByteCódigoOperación(); if (númeroElementosTotal == 0 || leerByteCódigoOperación() != 0) { valorFallo("invalid invokeinterface operands"); continue; } }
                llamadaMétodo(valorCodificado, valor); continue;
            }
            if (valor == 187) { objetoNuevo(textoNombreClase(leerConstanteCódigoOperación()), ponerEnMarcha); continue; }
            if (valor == 188 || valor == 189) {
                int códigoCategoría = 3, componente = 0;
                if (valor == 188) { int datosTemporal = leerByteCódigoOperación(); códigoCategoría = datosTemporal == 10 ? 2 : datosTemporal == 8 ? 20 : datosTemporal == 4 ? 21 : datosTemporal == 5 ? 22 : datosTemporal == 9 ? 23 : 0; }
                else componente = textoNombreClase(leerConstanteCódigoOperación());
                if (códigoCategoría == 0) { valorFallo("unsupported primitive array type"); continue; }
                int longitudVálido = restarValores(1), referenciaObjeto = asignarMemoriaAlmacenamiento(códigoCategoría, longitudVálido); if (!error) elementoArreglo[referenciaObjeto] = componente; ponerValor(referenciaObjeto, 2); continue;
            }
            if (valor == 190) {
                int referenciaObjeto = restarValores(2);
                if (esObjetoVálido(referenciaObjeto)) { int posiciónComparación = valorMontículo[referenciaObjeto]; if (posiciónComparación != 2 && posiciónComparación != 3 && (posiciónComparación < 20 || posiciónComparación > 23)) valorFallo("not an array"); else ponerValor(valorMontículo[referenciaObjeto + 1], 1); }
                continue;
            }
            if (valor == 191) {
                int referenciaObjeto = restarValores(2); if (esObjetoVálido(referenciaObjeto)) { if (valorMontículo[referenciaObjeto] != 9) valorFallo("athrow requires supported Throwable"); else { objetoLanzado = referenciaObjeto; error = true; } }
                continue;
            }
            if (valor == 192 || valor == 193) {
                int constanteNombre = textoNombreClase(leerConstanteCódigoOperación()), referenciaObjeto = restarValores(2); boolean coincide = objetoConcordante(referenciaObjeto, constanteNombre);
                if (valor == 193) ponerValor(referenciaObjeto != 0 && coincide ? 1 : 0, 1);
                else { if (!coincide && !error) valorFallo("ClassCastException"); ponerValor(referenciaObjeto, 2); }
                continue;
            }
            if (valor == 170 || valor == 171) {
                int leerCursor = ponerEnMarcha + 1, índiceArchivo = métodoMarco[índiceMarco], referenciaTecla = restarValores(1);
                while ((leerCursor - iniciarMétodo[índiceArchivo]) % 4 != 0) leerCursor++;
                int direcciónObjetivo = enteroValorPosición(leerCursor);
                if (valor == 170) { int valorBajo = enteroValorPosición(leerCursor + 4), valorAlto = enteroValorPosición(leerCursor + 8); if (referenciaTecla >= valorBajo && referenciaTecla <= valorAlto) direcciónObjetivo = enteroValorPosición(leerCursor + 12 + (referenciaTecla - valorBajo) * 4); }
                else { int númeroElementosTotal = enteroValorPosición(leerCursor + 4); for (int índiceBucle = 0; índiceBucle < númeroElementosTotal; índiceBucle++) if (enteroValorPosición(leerCursor + 8 + índiceBucle * 8) == referenciaTecla) direcciónObjetivo = enteroValorPosición(leerCursor + 12 + índiceBucle * 8); }
                valorMover(ponerEnMarcha + direcciónObjetivo); continue;
            }
            if (valor == 200) { valorMover(ponerEnMarcha + enteroValorPosición(ponerEnMarcha + 1)); continue; }
            if (valor == 194 || valor == 195) {
                int referenciaObjeto = restarValores(2);
                if (valor == 195) liberarCerrojo(referenciaObjeto);
                else if (!adquirirCerrojo(referenciaObjeto) && !error) { ponerValor(referenciaObjeto, 2); posiciónMarco[índiceMarco] = ponerEnMarcha; }
                continue;
            }
            if (valor == 196) {
                int códigoComando = leerByteCódigoOperación(), posiciónEntradaElemento = leerCortoCódigoOperación();
                if (códigoComando == 21 || códigoComando == 25) leerLocal(posiciónEntradaElemento, códigoComando == 21 ? 1 : 2);
                else if (códigoComando == 54 || códigoComando == 58) escribirLocal(posiciónEntradaElemento, códigoComando == 54 ? 1 : 2);
                else if (códigoComando == 132) { int valorVariación = (short)leerCortoCódigoOperación(); leerLocal(posiciónEntradaElemento, 1); ponerValor(restarValores(1) + valorVariación, 1); escribirLocal(posiciónEntradaElemento, 1); }
                else valorFallo("unsupported wide opcode");
                continue;
            }
            valorFallo("unsupported bytecode");
        }
    }
    static int encontrarDefiniciónClase(int nombre) {
        for (int índiceBucle = 0; índiceBucle < númeroElementosDefiniciónClase; índiceBucle++) if (nombreDefiniciónClase[índiceBucle] != 0 && palabraConcordante(nombreDefiniciónClase[índiceBucle], nombre)) return índiceBucle;
        return cargarDefiniciónClase(textoConstante(nombre));
    }
    static int cargarDefiniciónClase(int cadenaNombre) {
        if (!valorObjeto(cadenaNombre, 1)) return -1;
        int longitud = valorMontículo[cadenaNombre + 1];
        if (longitud < 1 || longitud > 505 || númeroElementosDefiniciónClase == 16) { valorFallo("class name/count limit"); return -1; }
        for (int índiceBucle = 0; índiceBucle < longitud; índiceBucle++) { int códigoCarácter = valorMontículo[cadenaNombre + 2 + índiceBucle]; textoNombreArchivo[índiceBucle] = códigoCarácter == '/' ? '.' : códigoCarácter; }
        textoNombreArchivo[longitud] = '.'; textoNombreArchivo[longitud + 1] = 'c'; textoNombreArchivo[longitud + 2] = 'l'; textoNombreArchivo[longitud + 3] = 'a'; textoNombreArchivo[longitud + 4] = 's'; textoNombreArchivo[longitud + 5] = 's'; textoNombreArchivo[longitud + 6] = 0;
        int tamaño = Usuario.leerArchivo(textoNombreArchivo, archivoTemporal);
        if (tamaño < 0) { valorFallo("ClassNotFoundException"); return -1; }
        int definiciónClase = númeroElementosDefiniciónClase++; tamañoDefiniciónClase[definiciónClase] = tamaño;
        for (int índiceBucle = 0; índiceBucle < tamaño; índiceBucle++) Archivo[definiciónClase * 16384 + índiceBucle] = archivoTemporal[índiceBucle];
        leerClase(definiciónClase); if (error) return -1;
        int datosEfectivo = textoConstante(nombreDefiniciónClase[definiciónClase]);
        if (!igualTextos(datosEfectivo, cadenaNombre, true)) { valorFallo("class name does not match file"); return -1; }
        int valorPadre = padreDefiniciónClase[definiciónClase];
        if (valorPadre != 0 && !textoPalabra(valorPadre, "java/lang/Object") && !textoPalabra(valorPadre, "java/lang/Thread")) {
            // No vuelve a cargar clases ya registradas, pero rechaza explícitamente los ciclos de herencia.
            int valorExtremoSuperior = encontrarDefiniciónClase(valorPadre);
            if (error || valorExtremoSuperior < 0) return -1;
            int leerCursor = valorExtremoSuperior, númeroElementosEtapa = 0;
            while (leerCursor >= 0 && númeroElementosEtapa++ < 16) {
                if (leerCursor == definiciónClase) { valorFallo("cyclic inheritance"); return -1; }
                leerCursor = clasePadre(leerCursor);
            }
            int iniciarDesplazamiento = númeroElementosRanuraClase[valorExtremoSuperior];
            for (int índiceArchivo = 0; índiceArchivo < númeroElementosRanura; índiceArchivo++) if (propietarioRanura[índiceArchivo] == definiciónClase && (permisosRanura[índiceArchivo] & 8) == 0) posiciónRanura[índiceArchivo] += iniciarDesplazamiento;
            númeroElementosRanuraClase[definiciónClase] += iniciarDesplazamiento;
        }
        return definiciónClase;
    }
    static int clasePadre(int definiciónClase) {
        int nombre = padreDefiniciónClase[definiciónClase];
        for (int índiceBucle = 0; índiceBucle < númeroElementosDefiniciónClase; índiceBucle++) if (nombre != 0 && nombreDefiniciónClase[índiceBucle] != 0 && palabraConcordante(nombreDefiniciónClase[índiceBucle], nombre)) return índiceBucle;
        return -1;
    }
    static int encontrarMétodo(int definiciónClase, int nombre, int valorFormato) {
        for (int valorProfundidad = 0; definiciónClase >= 0 && valorProfundidad < 16; valorProfundidad++, definiciónClase = clasePadre(definiciónClase)) {
            for (int índiceBucle = 0; índiceBucle < númeroElementosMétodo; índiceBucle++) if (propietarioMétodo[índiceBucle] == definiciónClase && palabraConcordante(textoNombreMétodo[índiceBucle], nombre) && palabraConcordante(tipoMétodo[índiceBucle], valorFormato)) return índiceBucle;
        }
        return -1;
    }
    static int métodoNombre(int definiciónClase, String nombre, String valorFormato) {
        for (int valorProfundidad = 0; definiciónClase >= 0 && valorProfundidad < 16; valorProfundidad++, definiciónClase = clasePadre(definiciónClase))
            for (int índiceBucle = 0; índiceBucle < númeroElementosMétodo; índiceBucle++) if (propietarioMétodo[índiceBucle] == definiciónClase && textoPalabra(textoNombreMétodo[índiceBucle], nombre) && textoPalabra(tipoMétodo[índiceBucle], valorFormato)) return índiceBucle;
        return -1;
    }
    static int claseTipoTipo(int nombre) { return Archivo[valorPrimeroConstante[nombre]] == 'L' || Archivo[valorPrimeroConstante[nombre]] == '[' ? 2 : 1; }
    static boolean inicializar(int definiciónClase, int iniciarComando) {
        if (definiciónClase < 0 || error) return false;
        if (estadoValorDefiniciónClase[definiciónClase] == 3) { valorFallo("NoClassDefFoundError: initialization failed"); return false; }
        if (estadoValorDefiniciónClase[definiciónClase] == 1 && hiloEjecuciónClase[definiciónClase] != hiloEjecuciónActual) { posiciónMarco[índiceMarco] = iniciarComando; cambiarPetición = true; return false; }
        if (estadoValorDefiniciónClase[definiciónClase] != 0) return true;
        int valorExtremoSuperior = clasePadre(definiciónClase);
        if (valorExtremoSuperior >= 0 && !inicializar(valorExtremoSuperior, iniciarComando)) return false;
        estadoValorDefiniciónClase[definiciónClase] = 1; hiloEjecuciónClase[definiciónClase] = hiloEjecuciónActual;
        if (inicializarDefiniciónClase[definiciónClase] != 0) {
            posiciónMarco[índiceMarco] = iniciarComando;
            invocar(inicializarDefiniciónClase[definiciónClase] - 1); if (!error) inicializarMarco[índiceMarco] = definiciónClase + 1;
            return false;
        }
        estadoValorDefiniciónClase[definiciónClase] = 2; return true;
    }
    static void invocarCampo(int número, int comando, int ponerEnMarcha) {
        if (!comprobarConstante(número, 9)) return;
        int valorPropietario = textoNombreClase(valorPrimeroConstante[número]), nombre = nombreReferencia(valorSegundoConstante[número]), valorFormato = tipoReferencia(valorSegundoConstante[número]);
        if (textoPalabra(valorPropietario, "java/lang/System") && (textoPalabra(nombre, "out") || textoPalabra(nombre, "err")) && textoPalabra(valorFormato, "Ljava/io/PrintStream;") && comando == 178) { ponerValor(-1, 2); return; }
        int definiciónClase = encontrarDefiniciónClase(valorPropietario); if (definiciónClase < 0 || error) return;
        int valorEncontrado = -1;
        for (int leerCursor = definiciónClase, valorProfundidad = 0; leerCursor >= 0 && valorProfundidad < 16 && valorEncontrado < 0; valorProfundidad++, leerCursor = clasePadre(leerCursor))
            for (int índiceArchivo = 0; índiceArchivo < númeroElementosRanura; índiceArchivo++) if (propietarioRanura[índiceArchivo] == leerCursor && palabraConcordante(nombreRanura[índiceArchivo], nombre) && palabraConcordante(tipoRanura[índiceArchivo], valorFormato)) valorEncontrado = índiceArchivo;
        if (valorEncontrado < 0) { valorFallo("NoSuchFieldError"); return; }
        boolean valorEstático = comando == 178 || comando == 179;
        if (valorEstático != ((permisosRanura[valorEncontrado] & 8) != 0)) { valorFallo("field static/instance mismatch"); return; }
        if (valorEstático && !inicializar(propietarioRanura[valorEncontrado], ponerEnMarcha)) return;
        int valorTipo = claseTipoTipo(valorFormato), valor = 0;
        if (comando == 179 || comando == 181) valor = restarValores(valorTipo);
        if (valorEstático) { if (comando == 178) ponerValor(datosRanura[valorEncontrado], valorTipo); else if (!error) datosRanura[valorEncontrado] = valor; return; }
        int referenciaObjeto = restarValores(2);
        if (!esObjetoVálido(referenciaObjeto)) return;
        if (valorMontículo[referenciaObjeto] < 32 || !claseContiene(valorMontículo[referenciaObjeto] - 32, valorPropietario)) { valorFallo("field receiver type mismatch"); return; }
        int ranuraPreservado = referenciaObjeto + 2 + posiciónRanura[valorEncontrado];
        if (comando == 180) ponerValor(valorMontículo[ranuraPreservado], valorTipo);
        else if (!error) { valorMontículo[ranuraPreservado] = valor; referenciaMontículo[ranuraPreservado] = valorTipo == 2 ? 1 : 0; }
    }
    static boolean claseContiene(int definiciónClase, int nombre) {
        for (int profundidad = 0; definiciónClase >= 0 && profundidad < 16; profundidad++, definiciónClase = clasePadre(definiciónClase)) {
            if (palabraConcordante(nombreDefiniciónClase[definiciónClase], nombre) || (padreDefiniciónClase[definiciónClase] != 0 && palabraConcordante(padreDefiniciónClase[definiciónClase], nombre))) return true;
            for (int posiciónInterior = 0; posiciónInterior < númeroElementosInterfazClase[definiciónClase]; posiciónInterior++) if (palabraConcordante(interfazClase[definiciónClase * 16 + posiciónInterior], nombre)) return true;
        }
        return false;
    }
    static boolean igualTextos(int datosPrimero, int datosByte, boolean ruta) {
        if (datosPrimero == datosByte) return true;
        if (datosPrimero <= 0 || datosByte <= 0 || valorMontículo[datosPrimero] != 1 || valorMontículo[datosByte] != 1 || valorMontículo[datosPrimero + 1] != valorMontículo[datosByte + 1]) return false;
        for (int índiceBucle = 0; índiceBucle < valorMontículo[datosPrimero + 1]; índiceBucle++) {
            int coordenadaCoordenadaHorizontal = valorMontículo[datosPrimero + 2 + índiceBucle], coordenadaCoordenadaVertical = valorMontículo[datosByte + 2 + índiceBucle];
            if (ruta) { if (coordenadaCoordenadaHorizontal == '.') coordenadaCoordenadaHorizontal = '/'; if (coordenadaCoordenadaVertical == '.') coordenadaCoordenadaVertical = '/'; }
            if (coordenadaCoordenadaHorizontal != coordenadaCoordenadaVertical) return false;
        }
        return true;
    }
    static boolean esObjetoVálido(int referenciaObjeto) {
        if (referenciaObjeto == 0) { valorFallo("NullPointerException"); return false; }
        if (referenciaObjeto < 1 || referenciaObjeto >= posiciónFinMontículo || anchuraMontículo[referenciaObjeto] < 2 || valorMontículo[referenciaObjeto] == 0) { valorFallo("invalid object reference"); return false; }
        return true;
    }
    static void protegerValor(int referenciaObjeto) {
        if (referenciaObjeto > 0 && referenciaObjeto < posiciónFinMontículo && anchuraMontículo[referenciaObjeto] >= 2 && númeroElementosTemporal < referenciaTemporal.length) referenciaTemporal[númeroElementosTemporal++] = referenciaObjeto;
    }
    static void mostrarValor(int referenciaObjeto) {
        if (referenciaObjeto > 0 && referenciaObjeto < posiciónFinMontículo && anchuraMontículo[referenciaObjeto] >= 2 && valorMontículo[referenciaObjeto] != 0 && marcaMontículo[referenciaObjeto] == 0) {
            marcaMontículo[referenciaObjeto] = 1; esperarPresentarPara[númeroElementosPresentar++] = referenciaObjeto;
        }
    }
    static void recolectarBasura() {
        númeroElementosPresentar = 0; númeroElementosColección++;
        for (int comprobarPosición = 1; comprobarPosición < posiciónFinMontículo; comprobarPosición += anchuraMontículo[comprobarPosición]) marcaMontículo[comprobarPosición] = 0;
        for (int índiceBucle = 0; índiceBucle < referenciaCadena.length; índiceBucle++) mostrarValor(referenciaCadena[índiceBucle]);
        for (int índiceBucle = 0; índiceBucle < númeroElementosRanura; índiceBucle++) if ((permisosRanura[índiceBucle] & 8) != 0 && claseTipoTipo(tipoRanura[índiceBucle]) == 2) mostrarValor(datosRanura[índiceBucle]);
        for (int datosTemporal = 0; datosTemporal < númeroElementosHiloEjecución; datosTemporal++) {
            mostrarValor(objetoHiloEjecución[datosTemporal]); mostrarValor(objetivoHiloEjecución[datosTemporal]);
            int posiciónExtremoSuperior = datosTemporal == hiloEjecuciónActual ? índiceMarco : marcoHiloEjecución[datosTemporal];
            for (int índiceArchivo = datosTemporal * 32; índiceArchivo <= posiciónExtremoSuperior; índiceArchivo++) {
                for (int posiciónInterior = 0; posiciónInterior < variablesLocalesMétodo[métodoMarco[índiceArchivo]]; posiciónInterior++) if (tipoLocal[índiceArchivo * 128 + posiciónInterior] == 2) mostrarValor(valorLocal[índiceArchivo * 128 + posiciónInterior]);
                for (int posiciónInterior = 0; posiciónInterior < pilaMarco[índiceArchivo]; posiciónInterior++) if (tipoPilaOperando[índiceArchivo * 128 + posiciónInterior] == 2) mostrarValor(valorPilaOperando[índiceArchivo * 128 + posiciónInterior]);
            }
        }
        for (int índiceBucle = 0; índiceBucle < referenciaPantalla.length; índiceBucle++) mostrarValor(referenciaPantalla[índiceBucle]);
        for (int índiceBucle = 0; índiceBucle < númeroElementosPosterior; índiceBucle++) mostrarValor(posteriorPlanificación[índiceBucle]);
        for (int índiceBucle = 0; índiceBucle < enteroValorAlmacenar.length; índiceBucle++) mostrarValor(enteroValorAlmacenar[índiceBucle]);
        for (int índiceBucle = 0; índiceBucle < númeroElementosDefiniciónClase; índiceBucle++) mostrarValor(cerrojoClase[índiceBucle]);
        for (int comprobarPosición = 1; comprobarPosición < posiciónFinMontículo; comprobarPosición += anchuraMontículo[comprobarPosición]) if (profundidadCerrojo[comprobarPosición] > 0) mostrarValor(comprobarPosición);
        mostrarValor(objetoLanzado);
        for (int índiceBucle = 0; índiceBucle < númeroElementosTemporal; índiceBucle++) mostrarValor(referenciaTemporal[índiceBucle]);
        while (númeroElementosPresentar > 0) {
            int referenciaObjeto = esperarPresentarPara[--númeroElementosPresentar], códigoCategoría = valorMontículo[referenciaObjeto];
            for (int índiceBucle = referenciaObjeto + 2; índiceBucle < referenciaObjeto + anchuraMontículo[referenciaObjeto]; índiceBucle++) if (códigoCategoría == 3 || códigoCategoría == 4 || referenciaMontículo[índiceBucle] != 0) mostrarValor(valorMontículo[índiceBucle]);
        }
        for (int comprobarPosición = 1; comprobarPosición < posiciónFinMontículo; comprobarPosición += anchuraMontículo[comprobarPosición]) if (marcaMontículo[comprobarPosición] == 0) valorMontículo[comprobarPosición] = 0;
        for (int comprobarPosición = 1; comprobarPosición < posiciónFinMontículo; comprobarPosición += anchuraMontículo[comprobarPosición]) if (valorMontículo[comprobarPosición] == 0) {
            while (comprobarPosición + anchuraMontículo[comprobarPosición] < posiciónFinMontículo && valorMontículo[comprobarPosición + anchuraMontículo[comprobarPosición]] == 0) { int posiciónSiguiente = comprobarPosición + anchuraMontículo[comprobarPosición]; anchuraMontículo[comprobarPosición] += anchuraMontículo[posiciónSiguiente]; anchuraMontículo[posiciónSiguiente] = 0; }
            if (comprobarPosición + anchuraMontículo[comprobarPosición] == posiciónFinMontículo) { posiciónFinMontículo = comprobarPosición; break; }
        }
    }
    static int memoriaNuevo(int valorClaseTipo, int longitud) {
        if (longitud < 0) { valorFallo("NegativeArraySizeException"); return 0; }
        if (longitud > valorMontículo.length - 3) { valorFallo("object heap exhausted"); return 0; }
        int númeroElementosRequerido = longitud + 2, referenciaObjeto = 0;
        if (númeroElementosRequerido <= valorMontículo.length - posiciónFinMontículo) { referenciaObjeto = posiciónFinMontículo; posiciónFinMontículo += númeroElementosRequerido; }
        else {
            recolectarBasura();
            for (int leerCursor = 1; leerCursor < posiciónFinMontículo; leerCursor += anchuraMontículo[leerCursor]) if (valorMontículo[leerCursor] == 0 && anchuraMontículo[leerCursor] >= númeroElementosRequerido) { referenciaObjeto = leerCursor; break; }
            if (referenciaObjeto != 0) {
                int longitudRestante = anchuraMontículo[referenciaObjeto] - númeroElementosRequerido;
                if (longitudRestante >= 2) { anchuraMontículo[referenciaObjeto + númeroElementosRequerido] = longitudRestante; valorMontículo[referenciaObjeto + númeroElementosRequerido] = 0; }
                else númeroElementosRequerido += longitudRestante;
            } else if (númeroElementosRequerido <= valorMontículo.length - posiciónFinMontículo) { referenciaObjeto = posiciónFinMontículo; posiciónFinMontículo += númeroElementosRequerido; }
        }
        if (referenciaObjeto == 0) { valorFallo("object heap exhausted"); return 0; }
        for (int índiceBucle = 0; índiceBucle < númeroElementosRequerido; índiceBucle++) { valorMontículo[referenciaObjeto + índiceBucle] = 0; referenciaMontículo[referenciaObjeto + índiceBucle] = 0; anchuraMontículo[referenciaObjeto + índiceBucle] = 0; }
        elementoArreglo[referenciaObjeto] = 0;
        anchuraMontículo[referenciaObjeto] = númeroElementosRequerido; valorMontículo[referenciaObjeto] = valorClaseTipo; valorMontículo[referenciaObjeto + 1] = longitud; protegerValor(referenciaObjeto); return referenciaObjeto;
    }
    static int claseExcepción(String constanteNombre) {
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/Throwable")) return 1;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/Exception")) return 2;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/RuntimeException")) return 3;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/ArithmeticException")) return 4;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/NullPointerException")) return 5;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/IndexOutOfBoundsException")) return 6;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/IllegalArgumentException")) return 9;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/NumberFormatException")) return 10;
        if (HerramientaJava.textoIgual(constanteNombre, "java/io/IOException")) return 11;
        if (HerramientaJava.textoIgual(constanteNombre, "java/io/FileNotFoundException")) return 12;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/IllegalStateException")) return 13;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/ClassCastException")) return 14;
        if (HerramientaJava.textoIgual(constanteNombre, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int constanteExcepción(int nombre) {
        for (int índiceBucle = 1; índiceBucle <= 41; índiceBucle++) if (textoPalabra(nombre, nombreExcepción(índiceBucle))) return índiceBucle;
        return 0;
    }
    static String nombreExcepción(int valorIdentidad) {
        if (valorIdentidad == 40) return "java/lang/InterruptedException";
        if (valorIdentidad == 41) return "español/propio/ExcepciónInterrumpidoEsperar";
        if (valorIdentidad == 39) return "java/net/SocketException";
        if (valorIdentidad == 20) return "español/propio/excepción";
        if (valorIdentidad == 21) return "español/propio/ExcepciónEjecución";
        if (valorIdentidad == 22) return "español/propio/ExcepciónSalidaEntrada";
        if (valorIdentidad == 23) return "español/propio/ExcepciónTiempoEsperaEsperar";
        if (valorIdentidad == 24) return "español/propio/ExcepciónBuscarDirección";
        if (valorIdentidad == 25) return "español/propio/ExcepciónArchivoAusente";
        if (valorIdentidad == 26) return "español/propio/ExcepciónComunicación";
        if (valorIdentidad == 27) return "español/propio/ExcepciónArgumentoInválido";
        if (valorIdentidad == 28) return "español/propio/FalloFormatoNúmero";
        if (valorIdentidad == 29) return "español/propio/ExcepciónLímites";
        if (valorIdentidad == 30) return "español/propio/ExcepciónLímitesArreglo";
        if (valorIdentidad == 31) return "español/propio/ExcepciónLímitesCadena";
        if (valorIdentidad == 32) return "español/propio/ExcepciónReferenciaReferenciaNula";
        if (valorIdentidad == 33) return "español/propio/FalloAritmética";
        if (valorIdentidad == 34) return "español/propio/ExcepciónEstadoValor";
        if (valorIdentidad == 35) return "español/propio/ExcepciónConversiónTipoTipo";
        if (valorIdentidad == 36) return "español/propio/FalloTamañoArregloNegativo";
        if (valorIdentidad == 37) return "español/propio/FalloAlmacenarArreglo";
        if (valorIdentidad == 38) return "español/propio/ExcepciónEstadoValorHiloEjecución";
        if (valorIdentidad == 1) return "java/lang/Throwable"; if (valorIdentidad == 2) return "java/lang/Exception";
        if (valorIdentidad == 3) return "java/lang/RuntimeException"; if (valorIdentidad == 4) return "java/lang/ArithmeticException";
        if (valorIdentidad == 5) return "java/lang/NullPointerException"; if (valorIdentidad == 6) return "java/lang/IndexOutOfBoundsException";
        if (valorIdentidad == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (valorIdentidad == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (valorIdentidad == 9) return "java/lang/IllegalArgumentException"; if (valorIdentidad == 10) return "java/lang/NumberFormatException";
        if (valorIdentidad == 11) return "java/io/IOException"; if (valorIdentidad == 12) return "java/io/FileNotFoundException";
        if (valorIdentidad == 17) return "java/lang/ArrayStoreException";
        if (valorIdentidad == 18) return "java/net/UnknownHostException";
        if (valorIdentidad == 19) return "java/net/SocketTimeoutException";
        if (valorIdentidad == 16) return "java/lang/IllegalThreadStateException";
        if (valorIdentidad == 13) return "java/lang/IllegalStateException"; if (valorIdentidad == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int padreExcepción(int valorIdentidad) {
        if (valorIdentidad == 40) return 2;
        if (valorIdentidad == 41) return 40;
        if (valorIdentidad == 39) return 11;
        if (valorIdentidad == 1) return 0;
        if (valorIdentidad == 2) return 1;
        if (valorIdentidad == 3) return 2;
        if (valorIdentidad == 4) return 3;
        if (valorIdentidad == 5) return 3;
        if (valorIdentidad == 6) return 3;
        if (valorIdentidad == 7) return 6;
        if (valorIdentidad == 8) return 6;
        if (valorIdentidad == 9) return 3;
        if (valorIdentidad == 10) return 9;
        if (valorIdentidad == 11) return 2;
        if (valorIdentidad == 12) return 11;
        if (valorIdentidad == 13) return 3;
        if (valorIdentidad == 14) return 3;
        if (valorIdentidad == 15) return 3;
        if (valorIdentidad == 16) return 9;
        if (valorIdentidad == 17) return 3;
        if (valorIdentidad == 18) return 11;
        if (valorIdentidad == 19) return 11;
        if (valorIdentidad == 20) return 2;
        if (valorIdentidad == 21) return 3;
        if (valorIdentidad == 22) return 11;
        if (valorIdentidad == 23) return 22;
        if (valorIdentidad == 24) return 22;
        if (valorIdentidad == 25) return 22;
        if (valorIdentidad == 26) return 22;
        if (valorIdentidad == 27) return 9;
        if (valorIdentidad == 28) return 27;
        if (valorIdentidad == 29) return 6;
        if (valorIdentidad == 30) return 29;
        if (valorIdentidad == 31) return 29;
        if (valorIdentidad == 32) return 5;
        if (valorIdentidad == 33) return 4;
        if (valorIdentidad == 34) return 13;
        if (valorIdentidad == 35) return 14;
        if (valorIdentidad == 36) return 15;
        if (valorIdentidad == 37) return 17;
        if (valorIdentidad == 38) return 16;
        return 0;
    }
    static boolean excepciónContiene(int valorEfectivo, int deseado) {
        for (int valorProfundidad = 0; valorEfectivo != 0 && valorProfundidad < 16; valorProfundidad++, valorEfectivo = padreExcepción(valorEfectivo))
            if (valorEfectivo == deseado) return true;
        return false;
    }
    static void lanzarExcepción(int valorIdentidad, String referenciaLéame) {
        int referenciaObjeto = memoriaNuevo(9, 2); if (error) return;
        valorMontículo[referenciaObjeto + 2] = valorIdentidad; valorMontículo[referenciaObjeto + 3] = carácterAnfitrión(referenciaLéame); referenciaMontículo[referenciaObjeto + 3] = 1;
        objetoLanzado = referenciaObjeto; error = true;
    }
    static boolean objetoConcordante(int referenciaObjeto, int nombre) {
        if (referenciaObjeto == 0) return true;
        if (!esObjetoVálido(referenciaObjeto)) return false;
        int códigoCategoría = valorMontículo[referenciaObjeto];
        if (textoPalabra(nombre, "java/lang/Object")) return true;
        if (códigoCategoría >= 32) return claseContiene(códigoCategoría - 32, nombre);
        if (códigoCategoría == 9) { int direcciónObjetivo = constanteExcepción(nombre); return direcciónObjetivo != 0 && excepciónContiene(valorMontículo[referenciaObjeto + 2], direcciónObjetivo); }
        if (códigoCategoría == 1) return textoPalabra(nombre, "java/lang/String") || textoPalabra(nombre, "java/lang/CharSequence");
        if (códigoCategoría == 4) return textoPalabra(nombre, "java/lang/StringBuilder") || textoPalabra(nombre, "java/lang/CharSequence");
        if (códigoCategoría == 10) return textoPalabra(nombre, "java/util/ArrayList") || textoPalabra(nombre, "java/util/List");
        if (códigoCategoría == 11) return textoPalabra(nombre, "java/util/HashMap") || textoPalabra(nombre, "java/util/Map");
        if (códigoCategoría == 12) return textoPalabra(nombre, "java/lang/Integer") || textoPalabra(nombre, "java/lang/Number");
        if (códigoCategoría >= 24 && códigoCategoría <= 28 && valorMontículo[referenciaObjeto + 13] != 0) return clasePantallaCoreano(nombre) == códigoCategoría || textoPalabra(nombre, "español/propio/ElementoPantalla");
        if (códigoCategoría >= 24 && códigoCategoría <= 28) return (clasePantallaCoreano(nombre) == 0 && clasePantalla(nombre) == códigoCategoría) || textoPalabra(nombre, "java/awt/Component") || textoPalabra(nombre, "java/awt/Container") || textoPalabra(nombre, "javax/swing/JComponent");
        if (códigoCategoría == 29) return textoPalabra(nombre, valorMontículo[referenciaObjeto + 3] != 0 ? "español/propio/NotificaciónAcción" : "java/awt/event/ActionEvent");
        if (códigoCategoría == 30) return textoPalabra(nombre, "java/awt/FlowLayout") || textoPalabra(nombre, "java/awt/LayoutManager");
        if (códigoCategoría == 17) return textoPalabra(nombre, "java/net/Socket");
        if (códigoCategoría == 18) return textoPalabra(nombre, "java/net/ServerSocket");
        if (códigoCategoría == 19) return textoPalabra(nombre, valorMontículo[referenciaObjeto + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (códigoCategoría == 14) return textoPalabra(nombre, "java/net/InetAddress");
        if (códigoCategoría == 15) return textoPalabra(nombre, "java/net/DatagramSocket");
        if (códigoCategoría == 16) return textoPalabra(nombre, "java/net/DatagramPacket");
        if (códigoCategoría == 13) return textoPalabra(nombre, valorMontículo[referenciaObjeto + 3] != 0 ? "español/propio/tareaFondo" : "java/lang/Thread");
        if (códigoCategoría == 2) return textoPalabra(nombre, "[I"); if (códigoCategoría == 20) return textoPalabra(nombre, "[B"); if (códigoCategoría == 21) return textoPalabra(nombre, "[Z");
        if (códigoCategoría == 22) return textoPalabra(nombre, "[C"); if (códigoCategoría == 23) return textoPalabra(nombre, "[S");
        if (códigoCategoría != 3) return false;
        if (textoPalabra(nombre, "[Ljava/lang/Object;")) return true;
        int componente = elementoArreglo[referenciaObjeto];
        if (componente == -1) return textoPalabra(nombre, "[Ljava/lang/String;") || textoPalabra(nombre, "[Ljava/lang/CharSequence;");
        if (componente == 0) return false;
        if (compararClasesArreglo(componente, nombre)) return true;
        if ((textoPalabra(componente, "java/lang/String") || textoPalabra(componente, "java/lang/StringBuilder")) && textoPalabra(nombre, "[Ljava/lang/CharSequence;")) return true;
        for (int índiceBucle = 0; índiceBucle < númeroElementosDefiniciónClase; índiceBucle++) if (palabraConcordante(nombreDefiniciónClase[índiceBucle], componente)) {
            for (int códigoCarácter = índiceBucle, profundidad = 0; códigoCarácter >= 0 && profundidad < 16; profundidad++, códigoCarácter = clasePadre(códigoCarácter)) {
                if (compararClasesArreglo(padreDefiniciónClase[códigoCarácter], nombre)) return true;
                for (int posiciónInterior = 0; posiciónInterior < númeroElementosInterfazClase[códigoCarácter]; posiciónInterior++) if (compararClasesArreglo(interfazClase[códigoCarácter * 16 + posiciónInterior], nombre)) return true;
            }
        }
        return false;
    }
    static boolean compararClasesArreglo(int constanteNombre, int descriptor) {
        int comprobarPosición = valorPrimeroConstante[descriptor], númeroElementosEntradaElemento = valorSegundoConstante[descriptor];
        if (constanteNombre == 0 || númeroElementosEntradaElemento < 4 || Archivo[comprobarPosición] != '[' || Archivo[comprobarPosición + 1] != 'L' || Archivo[comprobarPosición + númeroElementosEntradaElemento - 1] != ';' || valorSegundoConstante[constanteNombre] != númeroElementosEntradaElemento - 3) return false;
        for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento - 3; índiceBucle++) if (Archivo[valorPrimeroConstante[constanteNombre] + índiceBucle] != Archivo[comprobarPosición + 2 + índiceBucle]) return false;
        return true;
    }
    static void excepciónManejador() {
        if (objetoLanzado == 0) return;
        error = false;
        while (índiceMarco >= hiloEjecuciónActual * 32) {
            int índiceArchivo = métodoMarco[índiceMarco], leerCursor = instrucciónMáquinaMarco[índiceMarco];
            for (int índiceBucle = 0; índiceBucle < capturarNúmeroElementos; índiceBucle++) if (capturarMétodo[índiceBucle] == índiceArchivo && leerCursor >= capturarIniciar[índiceBucle] && leerCursor < capturarFin[índiceBucle]
                && (capturarClase[índiceBucle] == 0 || objetoConcordante(objetoLanzado, capturarClase[índiceBucle]))) {
                posiciónMarco[índiceMarco] = capturarPosición[índiceBucle]; pilaMarco[índiceMarco] = 0; ponerValor(objetoLanzado, 2); objetoLanzado = 0; return;
            }
            if (inicializarMarco[índiceMarco] != 0) estadoValorDefiniciónClase[inicializarMarco[índiceMarco] - 1] = 3;
            if (cerrojoMarco[índiceMarco] != 0) { liberarCerrojo(cerrojoMarco[índiceMarco]); cerrojoMarco[índiceMarco] = 0; }
            índiceMarco--;
        }
        Usuario.escribir("Uncaught ");
        if (valorMontículo[objetoLanzado] == 9) { Usuario.escribir(nombreExcepción(valorMontículo[objetoLanzado + 2])); Usuario.escribir(": "); escribirTexto(valorMontículo[objetoLanzado + 3]); }
        else Usuario.escribir("user exception");
        Usuario.escribirValorCarácter(10); objetoLanzado = 0; error = true;
    }
    // Esta JVM solo admite actualmente elementos de pila category-1 (int/reference).
    static void instrucciónMáquinaPila(int códigoComando) {
        int datosPrimero = restarValores(0), formatoPrimero = tipoRetornar;
        if (códigoComando == 87) return;
        if (códigoComando == 89) { ponerValor(datosPrimero, formatoPrimero); ponerValor(datosPrimero, formatoPrimero); return; }
        int datosByte = restarValores(0), formatoSegundo = tipoRetornar;
        if (códigoComando == 88) return;
        if (códigoComando == 90) { ponerValor(datosPrimero, formatoPrimero); ponerValor(datosByte, formatoSegundo); ponerValor(datosPrimero, formatoPrimero); return; }
        if (códigoComando == 92) { ponerValor(datosByte, formatoSegundo); ponerValor(datosPrimero, formatoPrimero); ponerValor(datosByte, formatoSegundo); ponerValor(datosPrimero, formatoPrimero); return; }
        if (códigoComando == 95) { ponerValor(datosPrimero, formatoPrimero); ponerValor(datosByte, formatoSegundo); return; }
        int códigoCarácter = restarValores(0), formatoTercero = tipoRetornar;
        if (códigoComando == 91) { ponerValor(datosPrimero, formatoPrimero); ponerValor(códigoCarácter, formatoTercero); ponerValor(datosByte, formatoSegundo); ponerValor(datosPrimero, formatoPrimero); return; }
        if (códigoComando == 93) { ponerValor(datosByte, formatoSegundo); ponerValor(datosPrimero, formatoPrimero); ponerValor(códigoCarácter, formatoTercero); ponerValor(datosByte, formatoSegundo); ponerValor(datosPrimero, formatoPrimero); return; }
        int valorPosiciónFinal = restarValores(0), formatoCuarto = tipoRetornar;
        ponerValor(datosByte, formatoSegundo); ponerValor(datosPrimero, formatoPrimero); ponerValor(valorPosiciónFinal, formatoCuarto); ponerValor(códigoCarácter, formatoTercero); ponerValor(datosByte, formatoSegundo); ponerValor(datosPrimero, formatoPrimero);
    }
    static void objetoNuevo(int constanteNombre, int puntoInicial) {
        int códigoCategoría = 0, longitudVálido = 0, referenciaExcepción = constanteExcepción(constanteNombre);
        if (textoPalabra(constanteNombre, "java/lang/StringBuilder")) { códigoCategoría = 4; longitudVálido = 1; }
        if (textoPalabra(constanteNombre, "java/io/FileInputStream")) { códigoCategoría = 5; longitudVálido = 2; }
        if (textoPalabra(constanteNombre, "java/io/FileOutputStream")) { códigoCategoría = 6; longitudVálido = 2; }
        if (referenciaExcepción != 0) { códigoCategoría = 9; longitudVálido = 2; }
        if (textoPalabra(constanteNombre, "java/util/ArrayList")) { códigoCategoría = 10; longitudVálido = 2; }
        if (textoPalabra(constanteNombre, "java/util/HashMap")) { códigoCategoría = 11; longitudVálido = 2; }
        if (textoPalabra(constanteNombre, "java/lang/Integer")) { códigoCategoría = 12; longitudVálido = 1; }
        if (textoPalabra(constanteNombre, "java/net/Socket")) { códigoCategoría = 17; longitudVálido = 5; }
        if (textoPalabra(constanteNombre, "java/net/ServerSocket")) { códigoCategoría = 18; longitudVálido = 5; }
        if (textoPalabra(constanteNombre, "java/net/DatagramSocket")) { códigoCategoría = 15; longitudVálido = 3; }
        if (textoPalabra(constanteNombre, "java/net/DatagramPacket")) { códigoCategoría = 16; longitudVálido = 4; }
        if (textoPalabra(constanteNombre, "java/lang/Thread") || textoPalabra(constanteNombre, "español/propio/tareaFondo")) { códigoCategoría = 13; longitudVálido = 2; }
        if (textoPalabra(constanteNombre, "java/lang/Object")) { códigoCategoría = 8; }
        if (códigoCategoría == 0 && clasePantalla(constanteNombre) != 0) { códigoCategoría = clasePantalla(constanteNombre); longitudVálido = 12; }
        if (códigoCategoría == 0) {
            int códigoCarácter = encontrarDefiniciónClase(constanteNombre); if (códigoCarácter < 0 || error || !inicializar(códigoCarácter, puntoInicial)) return;
            códigoCategoría = 32 + códigoCarácter; longitudVálido = númeroElementosRanuraClase[códigoCarácter];
        }
        int referenciaObjeto = asignarMemoriaAlmacenamiento(códigoCategoría, longitudVálido); if (error) return;
        if (códigoCategoría == 13 && textoPalabra(constanteNombre, "español/propio/tareaFondo")) valorMontículo[referenciaObjeto + 3] = 1;
        if (códigoCategoría >= 24 && códigoCategoría <= 28 && clasePantallaCoreano(constanteNombre) != 0) valorMontículo[referenciaObjeto + 13] = 1;
        if (códigoCategoría == 5 || códigoCategoría == 6 || códigoCategoría == 15 || códigoCategoría == 17 || códigoCategoría == 18) valorMontículo[referenciaObjeto + 2] = -1;
        if (códigoCategoría == 9) valorMontículo[referenciaObjeto + 2] = referenciaExcepción;
        ponerValor(referenciaObjeto, 2);
    }
    static boolean igualValores(int datosPrimero, int datosByte) {
        if (datosPrimero == datosByte) return true;
        if (datosPrimero == 0 || datosByte == 0 || datosPrimero < 0 || datosByte < 0 || datosPrimero >= posiciónFinMontículo || datosByte >= posiciónFinMontículo) return false;
        if (valorMontículo[datosPrimero] == 1 && valorMontículo[datosByte] == 1) return igualTextos(datosPrimero, datosByte, false);
        return valorMontículo[datosPrimero] == 12 && valorMontículo[datosByte] == 12 && valorMontículo[datosPrimero + 2] == valorMontículo[datosByte + 2];
    }
    static int fragmentoTexto(int referenciaObjeto, int iniciarPosición, int posiciónFin) {
        if (!valorObjeto(referenciaObjeto, 1)) return 0;
        if (iniciarPosición < 0 || posiciónFin < iniciarPosición || posiciónFin > valorMontículo[referenciaObjeto + 1]) { valorFallo("StringIndexOutOfBoundsException"); return 0; }
        int valorDevuelto = asignarMemoriaAlmacenamiento(1, posiciónFin - iniciarPosición); if (error) return 0;
        for (int índiceBucle = iniciarPosición; índiceBucle < posiciónFin; índiceBucle++) valorMontículo[valorDevuelto + 2 + índiceBucle - iniciarPosición] = valorMontículo[referenciaObjeto + 2 + índiceBucle];
        return valorDevuelto;
    }
    static int unirTexto(int datosPrimero, int datosByte) {
        if (!valorObjeto(datosPrimero, 1) || !valorObjeto(datosByte, 1)) return 0;
        int númeroElementosEntradaElemento = valorMontículo[datosPrimero + 1], índiceMétodo = valorMontículo[datosByte + 1], valorDevuelto = asignarMemoriaAlmacenamiento(1, númeroElementosEntradaElemento + índiceMétodo); if (error) return 0;
        for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) valorMontículo[valorDevuelto + 2 + índiceBucle] = valorMontículo[datosPrimero + 2 + índiceBucle];
        for (int índiceBucle = 0; índiceBucle < índiceMétodo; índiceBucle++) valorMontículo[valorDevuelto + 2 + númeroElementosEntradaElemento + índiceBucle] = valorMontículo[datosByte + 2 + índiceBucle];
        return valorDevuelto;
    }
    static boolean invocarPredeterminado(int propietario, int constanteNombre, int constanteDescriptor, int códigoComando) {
        if (textoPalabra(propietario, "español/propio/Argumentos") && códigoComando == 184) {
            if (textoPalabra(constanteNombre, "númeroElementosElementoLista") && textoPalabra(constanteDescriptor, "()I")) { ponerValor(Usuario.númeroElementosArgumentos() - 1, 1); return true; }
            if (textoPalabra(constanteNombre, "texto") && textoPalabra(constanteDescriptor, "(I)Ljava/lang/String;")) {
                int índiceOrdinal = restarValores(1);
                if (índiceOrdinal < 0 || índiceOrdinal >= Usuario.númeroElementosArgumentos() - 1) lanzarExcepción(29, "ejecutarComando argumentos 범위를 벗어났습니다");
                else ponerValor(carácterAnfitrión(Usuario.argumentos(índiceOrdinal + 1)), 2);
                return true;
            }
            valorFallo("지원하지 않는 español ejecutarComando argumentos invocar"); return true;
        }
        if (textoPalabra(propietario, "español/propio/tareaFondo")) { hiloEjecuciónProceso(constanteNombre, constanteDescriptor, códigoComando, true); return true; }
        if (propietarioPantallaCoreano(propietario)) { invocarPantallaCoreano(propietario, constanteNombre, constanteDescriptor, códigoComando); return true; }
        if (propietarioPantalla(propietario)) { invocarPantalla(propietario, constanteNombre, constanteDescriptor, códigoComando); return true; }
        if (textoPalabra(propietario, "java/net/Socket") || textoPalabra(propietario, "java/net/ServerSocket") || textoPalabra(propietario, "java/io/InputStream") || textoPalabra(propietario, "java/io/OutputStream")) { invocarFlujo(propietario, constanteNombre, constanteDescriptor, códigoComando); return true; }
        if (textoPalabra(propietario, "español/propio/valorNúcleo") && códigoComando == 184) {
            if (textoPalabra(constanteNombre, "anchuraPantalla") && textoPalabra(constanteDescriptor, "()I")) { ponerValor(Usuario.anchuraPantalla(), 1); return true; }
            if (textoPalabra(constanteNombre, "alturaPantalla") && textoPalabra(constanteDescriptor, "()I")) { ponerValor(Usuario.alturaPantalla(), 1); return true; }
            if (textoPalabra(constanteNombre, "milisegundos") && textoPalabra(constanteDescriptor, "()I")) { ponerValor(Usuario.milisegundos(), 1); return true; }
            if (textoPalabra(constanteNombre, "esperarImagenPara") && textoPalabra(constanteDescriptor, "()I")) { ponerValor(Usuario.esperarImagenPara(), 1); return true; }
            if (textoPalabra(constanteNombre, "rectángulo") && textoPalabra(constanteDescriptor, "(IIIII)I")) { int colorPíxel = restarValores(1), valorAltura = restarValores(1), valorAnchura = restarValores(1), coordenadaCoordenadaVertical = restarValores(1), coordenadaCoordenadaHorizontal = restarValores(1); ponerValor(Usuario.rectángulo(coordenadaCoordenadaHorizontal, coordenadaCoordenadaVertical, valorAnchura, valorAltura, colorPíxel), 1); return true; }
        }
        if (textoPalabra(propietario, "java/net/InetAddress") || textoPalabra(propietario, "java/net/DatagramPacket") || textoPalabra(propietario, "java/net/DatagramSocket")) { invocarRed(propietario, constanteNombre, constanteDescriptor, códigoComando); return true; }
        if (textoPalabra(propietario, "java/lang/Thread")) { invocarHiloEjecución(constanteNombre, constanteDescriptor, códigoComando); return true; }
        if (textoPalabra(propietario, "java/lang/Object")) {
            if (textoPalabra(constanteNombre, "<init>") && textoPalabra(constanteDescriptor, "()V") && códigoComando == 183) { esObjetoVálido(restarValores(2)); return true; }
            if (textoPalabra(constanteNombre, "equals") && textoPalabra(constanteDescriptor, "(Ljava/lang/Object;)Z")) { int datosByte = restarValores(2), datosPrimero = restarValores(2); if (esObjetoVálido(datosPrimero)) ponerValor(datosPrimero == datosByte ? 1 : 0, 1); return true; }
        }
        if (constanteExcepción(propietario) != 0) {
            if (textoPalabra(constanteNombre, "<init>") && códigoComando == 183 && (textoPalabra(constanteDescriptor, "()V") || textoPalabra(constanteDescriptor, "(Ljava/lang/String;)V"))) {
                int indicadorEntrada = textoPalabra(constanteDescriptor, "()V") ? 0 : restarValores(2), referenciaObjeto = restarValores(2);
                if (valorObjeto(referenciaObjeto, 9)) { valorMontículo[referenciaObjeto + 3] = indicadorEntrada; referenciaMontículo[referenciaObjeto + 3] = 1; } return true;
            }
            if ((textoPalabra(constanteNombre, "getMessage") || textoPalabra(constanteNombre, "descripción")) && textoPalabra(constanteDescriptor, "()Ljava/lang/String;")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, 9)) ponerValor(valorMontículo[referenciaObjeto + 3], 2); return true; }
        }
        if (textoPalabra(propietario, "java/lang/String")) {
            if (códigoComando == 182 && textoPalabra(constanteNombre, "getBytes") && (textoPalabra(constanteDescriptor, "()[B") || textoPalabra(constanteDescriptor, "(Ljava/lang/String;)[B"))) {
                int nombreCodificaciónEstado = textoPalabra(constanteDescriptor, "()[B") ? 0 : restarValores(2), referenciaObjeto = restarValores(2);
                if (!valorObjeto(referenciaObjeto, 1)) return true;
                if (nombreCodificaciónEstado != 0 && !igualTextos(nombreCodificaciónEstado, carácterAnfitrión("UTF-8"), false) && !igualTextos(nombreCodificaciónEstado, carácterAnfitrión("UTF8"), false) && !igualTextos(nombreCodificaciónEstado, carácterAnfitrión("utf-8"), false)) { lanzarExcepción(11, "only UTF-8 encoding is supported"); return true; }
                int númeroElementosEntradaElemento = valorMontículo[referenciaObjeto + 1], valorDevuelto = asignarMemoriaAlmacenamiento(20, númeroElementosEntradaElemento * 3), númeroElementosUsado = 0; if (error) return true;
                for (int posiciónInterior = 0; posiciónInterior < númeroElementosEntradaElemento; posiciónInterior++) {
                    int códigoCarácter = valorMontículo[referenciaObjeto + 2 + posiciónInterior];
                    if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdbff && posiciónInterior + 1 < númeroElementosEntradaElemento && valorMontículo[referenciaObjeto + 3 + posiciónInterior] >= 0xdc00 && valorMontículo[referenciaObjeto + 3 + posiciónInterior] <= 0xdfff) códigoCarácter = 0x10000 + ((códigoCarácter - 0xd800) << 10) + valorMontículo[referenciaObjeto + 2 + ++posiciónInterior] - 0xdc00;
                    else if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdfff) códigoCarácter = '?';
                    if (códigoCarácter < 128) valorMontículo[valorDevuelto + 2 + númeroElementosUsado++] = códigoCarácter;
                    else { int númeroElementosByte = códigoCarácter < 2048 ? 2 : códigoCarácter < 65536 ? 3 : 4; valorMontículo[valorDevuelto + 2 + númeroElementosUsado++] = (byte)((númeroElementosByte == 2 ? 192 : númeroElementosByte == 3 ? 224 : 240) | códigoCarácter >> (6 * (númeroElementosByte - 1))); for (int posiciónComparación = númeroElementosByte - 1; posiciónComparación > 0; posiciónComparación--) valorMontículo[valorDevuelto + 2 + númeroElementosUsado++] = (byte)(128 | códigoCarácter >> (6 * (posiciónComparación - 1)) & 63); }
                }
                valorMontículo[valorDevuelto + 1] = númeroElementosUsado; ponerValor(valorDevuelto, 2); return true;
            }
            if (códigoComando == 184 && textoPalabra(constanteNombre, "valueOf") && textoPalabra(constanteDescriptor, "(I)Ljava/lang/String;")) { ponerValor(carácterDígito(restarValores(1)), 2); return true; }
            if (códigoComando != 182) return false;
            if (textoPalabra(constanteNombre, "equals") && textoPalabra(constanteDescriptor, "(Ljava/lang/Object;)Z")) { int datosByte = restarValores(2), datosPrimero = restarValores(2); if (valorObjeto(datosPrimero, 1)) ponerValor(igualTextos(datosPrimero, datosByte, false) ? 1 : 0, 1); return true; }
            if (textoPalabra(constanteNombre, "isEmpty") && textoPalabra(constanteDescriptor, "()Z")) { int datosPrimero = restarValores(2); if (valorObjeto(datosPrimero, 1)) ponerValor(valorMontículo[datosPrimero + 1] == 0 ? 1 : 0, 1); return true; }
            if (textoPalabra(constanteNombre, "substring") && (textoPalabra(constanteDescriptor, "(I)Ljava/lang/String;") || textoPalabra(constanteDescriptor, "(II)Ljava/lang/String;"))) {
                boolean valorSegundo = textoPalabra(constanteDescriptor, "(II)Ljava/lang/String;"); int posiciónFin = valorSegundo ? restarValores(1) : 0, puntoInicial = restarValores(1), datosPrimero = restarValores(2);
                if (valorObjeto(datosPrimero, 1)) ponerValor(fragmentoTexto(datosPrimero, puntoInicial, valorSegundo ? posiciónFin : valorMontículo[datosPrimero + 1]), 2); return true;
            }
            if (textoPalabra(constanteNombre, "concat") && textoPalabra(constanteDescriptor, "(Ljava/lang/String;)Ljava/lang/String;")) { int datosByte = restarValores(2), datosPrimero = restarValores(2); ponerValor(unirTexto(datosPrimero, datosByte), 2); return true; }
            if (textoPalabra(constanteNombre, "hashCode") && textoPalabra(constanteDescriptor, "()I")) { int datosPrimero = restarValores(2), valorResumenHash = 0; if (valorObjeto(datosPrimero, 1)) { for (int índiceBucle = 0; índiceBucle < valorMontículo[datosPrimero + 1]; índiceBucle++) valorResumenHash = valorResumenHash * 31 + valorMontículo[datosPrimero + 2 + índiceBucle]; ponerValor(valorResumenHash, 1); } return true; }
            if (textoPalabra(constanteNombre, "toString") && textoPalabra(constanteDescriptor, "()Ljava/lang/String;")) { int datosPrimero = restarValores(2); if (valorObjeto(datosPrimero, 1)) ponerValor(datosPrimero, 2); return true; }
        }
        if (textoPalabra(propietario, "java/lang/Integer")) {
            if (códigoComando == 184 && textoPalabra(constanteNombre, "valueOf") && textoPalabra(constanteDescriptor, "(I)Ljava/lang/Integer;")) { int valorDatos = restarValores(1), referenciaObjeto = valorDatos >= -128 && valorDatos <= 127 ? enteroValorAlmacenar[valorDatos + 128] : 0; if (referenciaObjeto == 0) { referenciaObjeto = asignarMemoriaAlmacenamiento(12, 1); if (!error) { valorMontículo[referenciaObjeto + 2] = valorDatos; if (valorDatos >= -128 && valorDatos <= 127) enteroValorAlmacenar[valorDatos + 128] = referenciaObjeto; } } ponerValor(referenciaObjeto, 2); return true; }
            if (códigoComando == 183 && textoPalabra(constanteNombre, "<init>") && textoPalabra(constanteDescriptor, "(I)V")) { int valorDatos = restarValores(1), referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, 12)) valorMontículo[referenciaObjeto + 2] = valorDatos; return true; }
            if (códigoComando == 182 && textoPalabra(constanteNombre, "intValue") && textoPalabra(constanteDescriptor, "()I")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, 12)) ponerValor(valorMontículo[referenciaObjeto + 2], 1); return true; }
            if (códigoComando == 184 && textoPalabra(constanteNombre, "toString") && textoPalabra(constanteDescriptor, "(I)Ljava/lang/String;")) { ponerValor(carácterDígito(restarValores(1)), 2); return true; }
        }
        if (textoPalabra(propietario, "java/lang/Math") && códigoComando == 184) {
            if (textoPalabra(constanteNombre, "abs") && textoPalabra(constanteDescriptor, "(I)I")) { int leerValor = restarValores(1); ponerValor(leerValor < 0 ? -leerValor : leerValor, 1); return true; }
            if ((textoPalabra(constanteNombre, "min") || textoPalabra(constanteNombre, "max")) && textoPalabra(constanteDescriptor, "(II)I")) { int datosByte = restarValores(1), datosPrimero = restarValores(1); ponerValor(textoPalabra(constanteNombre, "min") ? (datosPrimero < datosByte ? datosPrimero : datosByte) : (datosPrimero > datosByte ? datosPrimero : datosByte), 1); return true; }
        }
        if (textoPalabra(propietario, "java/lang/System") && códigoComando == 184) {
            if (textoPalabra(constanteNombre, "gc") && textoPalabra(constanteDescriptor, "()V")) { recolectarBasura(); return true; }
            if (textoPalabra(constanteNombre, "arraycopy") && textoPalabra(constanteDescriptor, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int númeroElementosEntradaElemento = restarValores(1), índiceValorDestino = restarValores(1), datosByte = restarValores(2), iniciarPosición = restarValores(1), datosPrimero = restarValores(2);
                if (esObjetoVálido(datosPrimero) && esObjetoVálido(datosByte)) {
                    int códigoCategoría = valorMontículo[datosPrimero];
                    if (valorMontículo[datosByte] != códigoCategoría || (códigoCategoría != 2 && códigoCategoría != 3 && (códigoCategoría < 20 || códigoCategoría > 23))) valorFallo("arraycopy type mismatch");
                    else if (númeroElementosEntradaElemento < 0 || iniciarPosición < 0 || índiceValorDestino < 0 || iniciarPosición > valorMontículo[datosPrimero + 1] - númeroElementosEntradaElemento || índiceValorDestino > valorMontículo[datosByte + 1] - númeroElementosEntradaElemento) valorFallo("ArrayIndexOutOfBoundsException");
                    else if (datosPrimero == datosByte && índiceValorDestino > iniciarPosición) { for (int índiceBucle = númeroElementosEntradaElemento - 1; índiceBucle >= 0; índiceBucle--) valorMontículo[datosByte + 2 + índiceValorDestino + índiceBucle] = valorMontículo[datosPrimero + 2 + iniciarPosición + índiceBucle]; }
                    else { for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento && !error; índiceBucle++) { int valorDatos = valorMontículo[datosPrimero + 2 + iniciarPosición + índiceBucle]; if (códigoCategoría != 3 || puedeArregloAlmacenar(datosByte, valorDatos)) valorMontículo[datosByte + 2 + índiceValorDestino + índiceBucle] = valorDatos; } }
                }
                return true;
            }
        }
        if (textoPalabra(propietario, "java/util/ArrayList") || textoPalabra(propietario, "java/util/List") || textoPalabra(propietario, "java/util/HashMap") || textoPalabra(propietario, "java/util/Map")) {
            invocarColección(propietario, constanteNombre, constanteDescriptor, códigoComando); return true;
        }
        return false;
    }
    static void ampliarColección(int referenciaObjeto, int númeroElementosRequerido) {
        int valorElementoPrevio = valorMontículo[referenciaObjeto + 2], datosCapacidad = valorElementoPrevio == 0 ? 0 : valorMontículo[valorElementoPrevio + 1];
        if (datosCapacidad >= númeroElementosRequerido) return;
        int posiciónSiguiente = datosCapacidad < 8 ? 8 : datosCapacidad * 2; if (posiciónSiguiente < númeroElementosRequerido) posiciónSiguiente = númeroElementosRequerido;
        int arregloDatos = asignarMemoriaAlmacenamiento(3, posiciónSiguiente); if (error) return;
        for (int índiceBucle = 0; índiceBucle < datosCapacidad; índiceBucle++) valorMontículo[arregloDatos + 2 + índiceBucle] = valorMontículo[valorElementoPrevio + 2 + índiceBucle];
        valorMontículo[referenciaObjeto + 2] = arregloDatos; referenciaMontículo[referenciaObjeto + 2] = 1;
    }
    static void invocarColección(int propietario, int constanteNombre, int constanteDescriptor, int códigoComando) {
        boolean referenciaAsociado = textoPalabra(propietario, "java/util/HashMap") || textoPalabra(propietario, "java/util/Map"); int códigoCategoría = referenciaAsociado ? 11 : 10;
        if (textoPalabra(constanteNombre, "<init>") && códigoComando == 183 && textoPalabra(constanteDescriptor, "()V")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, códigoCategoría)) ampliarColección(referenciaObjeto, 8); return; }
        if (códigoComando != 182 && códigoComando != 185) { valorFallo("invalid collection invocation"); return; }
        if (textoPalabra(constanteNombre, "size") && textoPalabra(constanteDescriptor, "()I") || textoPalabra(constanteNombre, "isEmpty") && textoPalabra(constanteDescriptor, "()Z")) {
            int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, códigoCategoría)) ponerValor(textoPalabra(constanteNombre, "size") ? valorMontículo[referenciaObjeto + 3] : valorMontículo[referenciaObjeto + 3] == 0 ? 1 : 0, 1); return;
        }
        if (textoPalabra(constanteNombre, "clear") && textoPalabra(constanteDescriptor, "()V")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, códigoCategoría)) { int arregloDatos = valorMontículo[referenciaObjeto + 2]; for (int índiceBucle = 0; índiceBucle < valorMontículo[arregloDatos + 1]; índiceBucle++) valorMontículo[arregloDatos + 2 + índiceBucle] = 0; valorMontículo[referenciaObjeto + 3] = 0; } return; }
        if (!referenciaAsociado && textoPalabra(constanteNombre, "add") && textoPalabra(constanteDescriptor, "(Ljava/lang/Object;)Z")) {
            int valorDatos = restarValores(2), referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, 10)) return;
            int númeroElementosEntradaElemento = valorMontículo[referenciaObjeto + 3]; ampliarColección(referenciaObjeto, númeroElementosEntradaElemento + 1); if (!error) { valorMontículo[valorMontículo[referenciaObjeto + 2] + 2 + númeroElementosEntradaElemento] = valorDatos; valorMontículo[referenciaObjeto + 3] = númeroElementosEntradaElemento + 1; ponerValor(1, 1); } return;
        }
        if (!referenciaAsociado && (textoPalabra(constanteNombre, "get") || textoPalabra(constanteNombre, "remove")) && textoPalabra(constanteDescriptor, "(I)Ljava/lang/Object;") || !referenciaAsociado && textoPalabra(constanteNombre, "set") && textoPalabra(constanteDescriptor, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean esAsignado = textoPalabra(constanteNombre, "set"); int valorDatos = esAsignado ? restarValores(2) : 0, posiciónEntradaElemento = restarValores(1), referenciaObjeto = restarValores(2);
            if (!valorObjeto(referenciaObjeto, 10)) return;
            int númeroElementosEntradaElemento = valorMontículo[referenciaObjeto + 3], arregloDatos = valorMontículo[referenciaObjeto + 2];
            if (posiciónEntradaElemento < 0 || posiciónEntradaElemento >= númeroElementosEntradaElemento) { lanzarExcepción(6, "list index"); return; }
            int valorElementoPrevio = valorMontículo[arregloDatos + 2 + posiciónEntradaElemento];
            if (esAsignado) valorMontículo[arregloDatos + 2 + posiciónEntradaElemento] = valorDatos;
            if (textoPalabra(constanteNombre, "remove")) { for (int índiceBucle = posiciónEntradaElemento + 1; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) valorMontículo[arregloDatos + 1 + índiceBucle] = valorMontículo[arregloDatos + 2 + índiceBucle]; valorMontículo[arregloDatos + 1 + númeroElementosEntradaElemento] = 0; valorMontículo[referenciaObjeto + 3] = númeroElementosEntradaElemento - 1; }
            ponerValor(valorElementoPrevio, 2); return;
        }
        if (referenciaAsociado && (textoPalabra(constanteNombre, "get") || textoPalabra(constanteNombre, "remove")) && textoPalabra(constanteDescriptor, "(Ljava/lang/Object;)Ljava/lang/Object;") || referenciaAsociado && textoPalabra(constanteNombre, "put") && textoPalabra(constanteDescriptor, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || referenciaAsociado && textoPalabra(constanteNombre, "containsKey") && textoPalabra(constanteDescriptor, "(Ljava/lang/Object;)Z")) {
            boolean esInserción = textoPalabra(constanteNombre, "put"), eliminar = textoPalabra(constanteNombre, "remove");
            int valorDatos = esInserción ? restarValores(2) : 0, referenciaTecla = restarValores(2), referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, 11)) return;
            int númeroElementosEntradaElemento = valorMontículo[referenciaObjeto + 3], arregloDatos = valorMontículo[referenciaObjeto + 2], encontradoEra = -1;
            for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) if (igualValores(referenciaTecla, valorMontículo[arregloDatos + 2 + 2 * índiceBucle])) { encontradoEra = índiceBucle; break; }
            int valorElementoPrevio = encontradoEra < 0 ? 0 : valorMontículo[arregloDatos + 3 + 2 * encontradoEra];
            if (esInserción) {
                if (encontradoEra < 0) { ampliarColección(referenciaObjeto, (númeroElementosEntradaElemento + 1) * 2); arregloDatos = valorMontículo[referenciaObjeto + 2]; encontradoEra = númeroElementosEntradaElemento; if (!error) valorMontículo[referenciaObjeto + 3] = númeroElementosEntradaElemento + 1; }
                if (!error) { valorMontículo[arregloDatos + 2 + 2 * encontradoEra] = referenciaTecla; valorMontículo[arregloDatos + 3 + 2 * encontradoEra] = valorDatos; }
            }
            if (eliminar && encontradoEra >= 0) { for (int índiceBucle = encontradoEra + 1; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) { valorMontículo[arregloDatos + 2 * índiceBucle] = valorMontículo[arregloDatos + 2 + 2 * índiceBucle]; valorMontículo[arregloDatos + 1 + 2 * índiceBucle] = valorMontículo[arregloDatos + 3 + 2 * índiceBucle]; } valorMontículo[arregloDatos + 2 * númeroElementosEntradaElemento] = 0; valorMontículo[arregloDatos + 1 + 2 * númeroElementosEntradaElemento] = 0; valorMontículo[referenciaObjeto + 3] = númeroElementosEntradaElemento - 1; }
            if (textoPalabra(constanteNombre, "containsKey")) ponerValor(encontradoEra >= 0 ? 1 : 0, 1); else ponerValor(valorElementoPrevio, 2);
            return;
        }
        valorFallo("unsupported collection method");
    }
    static boolean adquirirCerrojo(int referenciaObjeto) {
        if (!esObjetoVálido(referenciaObjeto)) return false;
        if (profundidadCerrojo[referenciaObjeto] != 0 && propietarioCerrojo[referenciaObjeto] != hiloEjecuciónActual + 1) { cambiarPetición = true; return false; }
        propietarioCerrojo[referenciaObjeto] = hiloEjecuciónActual + 1; profundidadCerrojo[referenciaObjeto]++; return true;
    }
    static void liberarCerrojo(int referenciaObjeto) {
        if (!esObjetoVálido(referenciaObjeto)) return;
        if (profundidadCerrojo[referenciaObjeto] == 0 || propietarioCerrojo[referenciaObjeto] != hiloEjecuciónActual + 1) { lanzarExcepción(13, "monitor not owned"); return; }
        if (--profundidadCerrojo[referenciaObjeto] == 0) propietarioCerrojo[referenciaObjeto] = 0;
    }
    static boolean hiloEjecuciónConmutar() {
        marcoHiloEjecución[hiloEjecuciónActual] = índiceMarco;
        if (índiceMarco < hiloEjecuciónActual * 32) estadoValorHiloEjecución[hiloEjecuciónActual] = 3;
        for (int índiceBucle = 0; índiceBucle < númeroElementosHiloEjecución; índiceBucle++) if (estadoValorHiloEjecución[índiceBucle] == 2 && estadoValorHiloEjecución[esperarHiloEjecuciónPara[índiceBucle]] == 3) estadoValorHiloEjecución[índiceBucle] = 1;
        for (int índiceBucle = 1; índiceBucle <= númeroElementosHiloEjecución; índiceBucle++) {
            int posiciónSiguiente = (hiloEjecuciónActual + índiceBucle) % númeroElementosHiloEjecución;
            if (estadoValorHiloEjecución[posiciónSiguiente] == 1) { hiloEjecuciónActual = posiciónSiguiente; índiceMarco = marcoHiloEjecución[posiciónSiguiente]; cambiarPetición = false; return true; }
        }
        for (int índiceBucle = 0; índiceBucle < númeroElementosHiloEjecución; índiceBucle++) if (estadoValorHiloEjecución[índiceBucle] != 3) { valorFallo("thread deadlock"); return false; }
        return false;
    }
    static void invocarHiloEjecución(int constanteNombre, int constanteDescriptor, int códigoComando) { hiloEjecuciónProceso(constanteNombre, constanteDescriptor, códigoComando, false); }
    static void hiloEjecuciónProceso(int constanteNombre, int constanteDescriptor, int códigoComando, boolean español) {
        if (códigoComando == 184 && textoPalabra(constanteNombre, español ? "cederTarea" : "yield") && textoPalabra(constanteDescriptor, "()V")) { cambiarPetición = true; return; }
        if (códigoComando == 184 && textoPalabra(constanteNombre, "currentThread") && textoPalabra(constanteDescriptor, "()Ljava/lang/Thread;")) { ponerValor(objetoHiloEjecución[hiloEjecuciónActual], 2); return; }
        if (códigoComando == 183 && textoPalabra(constanteNombre, "<init>") && (textoPalabra(constanteDescriptor, "()V") || textoPalabra(constanteDescriptor, español ? "(Lespañol/propio/TareaTareaEjecutable;)V" : "(Ljava/lang/Runnable;)V"))) {
            int direcciónObjetivo = textoPalabra(constanteDescriptor, "()V") ? 0 : restarValores(2), referenciaObjeto = restarValores(2);
            if (!esObjetoVálido(referenciaObjeto)) return;
            if (valorMontículo[referenciaObjeto] == 13) { valorMontículo[referenciaObjeto + 2] = direcciónObjetivo; referenciaMontículo[referenciaObjeto + 2] = 1; }
            else if (direcciónObjetivo != 0) valorFallo("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (códigoComando == 182 && (textoPalabra(constanteNombre, español ? "iniciarTarea" : "start") || textoPalabra(constanteNombre, español ? "esperarFin" : "join")) && textoPalabra(constanteDescriptor, "()V") || códigoComando == 182 && textoPalabra(constanteNombre, español ? "esVivo" : "isAlive") && textoPalabra(constanteDescriptor, "()Z")) {
            int referenciaObjeto = restarValores(2); if (!esObjetoVálido(referenciaObjeto)) return;
            int valorIdentidad = -1; for (int índiceBucle = 0; índiceBucle < númeroElementosHiloEjecución; índiceBucle++) if (objetoHiloEjecución[índiceBucle] == referenciaObjeto) valorIdentidad = índiceBucle;
            if (textoPalabra(constanteNombre, español ? "esVivo" : "isAlive")) { ponerValor(valorIdentidad >= 0 && estadoValorHiloEjecución[valorIdentidad] != 3 ? 1 : 0, 1); return; }
            if (textoPalabra(constanteNombre, español ? "esperarFin" : "join")) { if (valorIdentidad >= 0 && estadoValorHiloEjecución[valorIdentidad] != 3) { esperarHiloEjecuciónPara[hiloEjecuciónActual] = valorIdentidad; estadoValorHiloEjecución[hiloEjecuciónActual] = 2; cambiarPetición = true; } return; }
            if (valorIdentidad >= 0) { lanzarExcepción(español ? 38 : 16, "thread already started"); return; }
            if (númeroElementosHiloEjecución == 4) { valorFallo("thread limit (4 including main)"); return; }
            int direcciónObjetivo = valorMontículo[referenciaObjeto] == 13 ? valorMontículo[referenciaObjeto + 2] : referenciaObjeto;
            int índiceArchivo = direcciónObjetivo > 0 && valorMontículo[direcciónObjetivo] >= 32 ? métodoNombre(valorMontículo[direcciónObjetivo] - 32, español ? "ejecutarTarea" : "run", "()V") : -1;
            if (direcciónObjetivo != 0 && índiceArchivo < 0) { valorFallo("Runnable.run required"); return; }
            valorIdentidad = númeroElementosHiloEjecución++; objetoHiloEjecución[valorIdentidad] = referenciaObjeto; objetivoHiloEjecución[valorIdentidad] = direcciónObjetivo;
            int marco = valorIdentidad * 32; marcoHiloEjecución[valorIdentidad] = índiceArchivo < 0 ? marco - 1 : marco; estadoValorHiloEjecución[valorIdentidad] = índiceArchivo < 0 ? 3 : 1;
            if (índiceArchivo >= 0) { métodoMarco[marco] = índiceArchivo; posiciónMarco[marco] = iniciarMétodo[índiceArchivo]; valorLocal[marco * 128] = direcciónObjetivo; tipoLocal[marco * 128] = 2; }
            return;
        }
        valorFallo("unsupported Thread method");
    }
    static int[] valorTemporalRed = new int[514], textoDirección = new int[16];
    static int direcciónLocal() { return objetoDirección(0x7f000001); }
    static int objetoDirección(int valor) { int referenciaObjeto = asignarMemoriaAlmacenamiento(14, 1); if (!error) valorMontículo[referenciaObjeto + 2] = valor; return referenciaObjeto; }
    static int decodificarDirección(int referenciaObjeto) {
        if (referenciaObjeto == 0 || igualTextos(referenciaObjeto, carácterAnfitrión("localhost"), false)) return 0x7f000001;
        if (!valorObjeto(referenciaObjeto, 1)) return 0;
        int valorDatos = 0, númeroElementosTotal = 0, byteDirección = 0, dígitos = 0, númeroElementosEntradaElemento = valorMontículo[referenciaObjeto + 1];
        for (int índiceBucle = 0; índiceBucle <= númeroElementosEntradaElemento; índiceBucle++) {
            int códigoCarácter = índiceBucle == númeroElementosEntradaElemento ? '.' : valorMontículo[referenciaObjeto + 2 + índiceBucle];
            if (códigoCarácter == '.') { if (dígitos == 0 || númeroElementosTotal == 4) { lanzarExcepción(18, "numeric IPv4 address required; DNS unavailable"); return 0; } valorDatos = valorDatos << 8 | byteDirección; númeroElementosTotal++; byteDirección = dígitos = 0; }
            else { if (códigoCarácter < '0' || códigoCarácter > '9' || ++dígitos > 3 || (byteDirección = byteDirección * 10 + códigoCarácter - '0') > 255) { lanzarExcepción(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (númeroElementosTotal != 4) { lanzarExcepción(18, "invalid IPv4 address"); return 0; } return valorDatos;
    }
    static int carácterDirección(int valorDatos) {
        int númeroElementosEntradaElemento = 0;
        for (int desplazar = 24; desplazar >= 0; desplazar -= 8) {
            int byteDirección = valorDatos >>> desplazar & 255;
            if (byteDirección >= 100) textoDirección[númeroElementosEntradaElemento++] = '0' + byteDirección / 100;
            if (byteDirección >= 10) textoDirección[númeroElementosEntradaElemento++] = '0' + byteDirección / 10 % 10;
            textoDirección[númeroElementosEntradaElemento++] = '0' + byteDirección % 10; if (desplazar != 0) textoDirección[númeroElementosEntradaElemento++] = '.';
        }
        int referenciaObjeto = asignarMemoriaAlmacenamiento(1, númeroElementosEntradaElemento); if (!error) for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) valorMontículo[referenciaObjeto + 2 + índiceBucle] = textoDirección[índiceBucle]; return referenciaObjeto;
    }
    static void invocarRed(int propietario, int constanteNombre, int constanteDescriptor, int códigoComando) {
        if (textoPalabra(propietario, "java/net/InetAddress")) {
            if (códigoComando == 184 && textoPalabra(constanteNombre, "getLoopbackAddress") && textoPalabra(constanteDescriptor, "()Ljava/net/InetAddress;")) { ponerValor(direcciónLocal(), 2); return; }
            if (códigoComando == 184 && textoPalabra(constanteNombre, "getByName") && textoPalabra(constanteDescriptor, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int valorDatos = decodificarDirección(restarValores(2)); if (objetoLanzado == 0 && !error) ponerValor(objetoDirección(valorDatos), 2); return;
            }
            if (códigoComando == 182 && textoPalabra(constanteNombre, "getHostAddress") && textoPalabra(constanteDescriptor, "()Ljava/lang/String;")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, 14)) ponerValor(carácterDirección(valorMontículo[referenciaObjeto + 2]), 2); return; }
        }
        if (textoPalabra(propietario, "java/net/DatagramPacket")) {
            if (códigoComando == 183 && textoPalabra(constanteNombre, "<init>") && (textoPalabra(constanteDescriptor, "([BI)V") || textoPalabra(constanteDescriptor, "([BILjava/net/InetAddress;I)V"))) {
                boolean referenciaValorDestino = textoPalabra(constanteDescriptor, "([BILjava/net/InetAddress;I)V"); int númeroPuerto = referenciaValorDestino ? restarValores(1) : 0, referenciaDirección = referenciaValorDestino ? restarValores(2) : 0;
                int númeroElementosEntradaElemento = restarValores(1), arregloDatos = restarValores(2), referenciaObjeto = restarValores(2);
                if (!valorObjeto(referenciaObjeto, 16) || !valorObjeto(arregloDatos, 20)) return;
                if (númeroElementosEntradaElemento < 0 || númeroElementosEntradaElemento > valorMontículo[arregloDatos + 1] || númeroPuerto < 0 || númeroPuerto > 65535) { lanzarExcepción(9, "invalid datagram length/port"); return; }
                if (referenciaDirección != 0 && !valorObjeto(referenciaDirección, 14)) return;
                valorMontículo[referenciaObjeto + 2] = arregloDatos; referenciaMontículo[referenciaObjeto + 2] = 1; valorMontículo[referenciaObjeto + 3] = númeroElementosEntradaElemento;
                valorMontículo[referenciaObjeto + 4] = referenciaDirección; referenciaMontículo[referenciaObjeto + 4] = 1; valorMontículo[referenciaObjeto + 5] = númeroPuerto; return;
            }
            if (códigoComando == 182 && textoPalabra(constanteNombre, "setLength") && textoPalabra(constanteDescriptor, "(I)V")) {
                int númeroElementosEntradaElemento = restarValores(1), referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, 16)) return;
                if (númeroElementosEntradaElemento < 0 || númeroElementosEntradaElemento > valorMontículo[valorMontículo[referenciaObjeto + 2] + 1]) lanzarExcepción(9, "invalid datagram length"); else valorMontículo[referenciaObjeto + 3] = númeroElementosEntradaElemento; return;
            }
            if (códigoComando == 182 && (textoPalabra(constanteNombre, "getData") && textoPalabra(constanteDescriptor, "()[B") || textoPalabra(constanteNombre, "getLength") && textoPalabra(constanteDescriptor, "()I") || textoPalabra(constanteNombre, "getAddress") && textoPalabra(constanteDescriptor, "()Ljava/net/InetAddress;") || textoPalabra(constanteNombre, "getPort") && textoPalabra(constanteDescriptor, "()I"))) {
                int referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, 16)) return;
                int posiciónEntradaElemento = textoPalabra(constanteNombre, "getData") ? 2 : textoPalabra(constanteNombre, "getLength") ? 3 : textoPalabra(constanteNombre, "getAddress") ? 4 : 5;
                ponerValor(valorMontículo[referenciaObjeto + posiciónEntradaElemento], posiciónEntradaElemento == 2 || posiciónEntradaElemento == 4 ? 2 : 1); return;
            }
        }
        if (textoPalabra(propietario, "java/net/DatagramSocket")) {
            if (códigoComando == 183 && textoPalabra(constanteNombre, "<init>") && (textoPalabra(constanteDescriptor, "()V") || textoPalabra(constanteDescriptor, "(I)V"))) {
                int númeroPuerto = textoPalabra(constanteDescriptor, "()V") ? 0 : restarValores(1), referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, 15)) return;
                if (númeroPuerto < 0 || númeroPuerto > 65535) { lanzarExcepción(9, "invalid port"); return; }
                int númeroArchivoAbierto = Usuario.abrirRed(númeroPuerto); if (númeroArchivoAbierto < 0) lanzarExcepción(39, "UDP socket/bind failed"); else valorMontículo[referenciaObjeto + 2] = númeroArchivoAbierto; return;
            }
            if (códigoComando == 182 && textoPalabra(constanteNombre, "setSoTimeout") && textoPalabra(constanteDescriptor, "(I)V")) {
                int valorMilisegundos = restarValores(1), referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, 15)) return;
                if (valorMilisegundos < 0) lanzarExcepción(9, "negative timeout"); else valorMontículo[referenciaObjeto + 3] = valorMilisegundos; return;
            }
            if (códigoComando == 182 && textoPalabra(constanteNombre, "getLocalPort") && textoPalabra(constanteDescriptor, "()I")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, 15)) ponerValor(valorMontículo[referenciaObjeto + 2] < 0 ? -1 : Usuario.puertoRed(valorMontículo[referenciaObjeto + 2]), 1); return; }
            if (códigoComando == 182 && textoPalabra(constanteNombre, "isClosed") && textoPalabra(constanteDescriptor, "()Z")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, 15)) ponerValor(valorMontículo[referenciaObjeto + 2] < 0 ? 1 : 0, 1); return; }
            if (códigoComando == 182 && textoPalabra(constanteNombre, "close") && textoPalabra(constanteDescriptor, "()V")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, 15) && valorMontículo[referenciaObjeto + 2] >= 0) { Usuario.cerrarDescriptorArchivo(valorMontículo[referenciaObjeto + 2]); valorMontículo[referenciaObjeto + 2] = -1; } return; }
            if (códigoComando == 182 && (textoPalabra(constanteNombre, "send") || textoPalabra(constanteNombre, "receive")) && textoPalabra(constanteDescriptor, "(Ljava/net/DatagramPacket;)V")) {
                int paqueteDatos = restarValores(2), referenciaObjeto = restarValores(2); if (!valorObjeto(paqueteDatos, 16) || !valorObjeto(referenciaObjeto, 15)) return;
                int arregloDatos = valorMontículo[paqueteDatos + 2], longitudVálido = valorMontículo[paqueteDatos + 3], númeroArchivoAbierto = valorMontículo[referenciaObjeto + 2];
                if (númeroArchivoAbierto < 0) { lanzarExcepción(39, "socket closed"); return; }
                if (textoPalabra(constanteNombre, "send")) {
                    if (!valorObjeto(valorMontículo[paqueteDatos + 4], 14)) return;
                    if (longitudVálido > 512) { lanzarExcepción(11, "datagram limit (512 bytes)"); return; }
                    for (int índiceBucle = 0; índiceBucle < longitudVálido; índiceBucle++) valorTemporalRed[índiceBucle] = valorMontículo[arregloDatos + 2 + índiceBucle];
                    if (Usuario.enviarRed(númeroArchivoAbierto, valorMontículo[valorMontículo[paqueteDatos + 4] + 2], valorMontículo[paqueteDatos + 5], valorTemporalRed, longitudVálido) < 0) lanzarExcepción(11, "UDP send failed");
                } else {
                    int númeroElementosEntradaElemento = Usuario.recibirRed(númeroArchivoAbierto, valorTemporalRed, longitudVálido > 512 ? 512 : longitudVálido);
                    if (númeroElementosEntradaElemento == -11) {
                        int tiempoActual = Usuario.milisegundos();
                        if (valorMontículo[referenciaObjeto + 4] == 0) valorMontículo[referenciaObjeto + 4] = tiempoActual + 1;
                        if (valorMontículo[referenciaObjeto + 3] > 0 && tiempoActual - (valorMontículo[referenciaObjeto + 4] - 1) >= valorMontículo[referenciaObjeto + 3]) { valorMontículo[referenciaObjeto + 4] = 0; lanzarExcepción(19, "receive timed out"); return; }
                        ponerValor(referenciaObjeto, 2); ponerValor(paqueteDatos, 2); posiciónMarco[índiceMarco] = instrucciónMáquinaMarco[índiceMarco]; cambiarPetición = true; return;
                    }
                    valorMontículo[referenciaObjeto + 4] = 0;
                    if (númeroElementosEntradaElemento < 0) { lanzarExcepción(11, "UDP receive failed"); return; }
                    for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) valorMontículo[arregloDatos + 2 + índiceBucle] = (byte)valorTemporalRed[índiceBucle];
                    valorMontículo[paqueteDatos + 3] = númeroElementosEntradaElemento; valorMontículo[paqueteDatos + 4] = objetoDirección(valorTemporalRed[513]); referenciaMontículo[paqueteDatos + 4] = 1; valorMontículo[paqueteDatos + 5] = valorTemporalRed[512];
                }
                return;
            }
        }
        valorFallo("unsupported java.net method");
    }
    static boolean esperarFlujoPara(int referenciaObjeto) {
        int tiempoActual = Usuario.milisegundos();
        if (valorMontículo[referenciaObjeto + 5] == 0) valorMontículo[referenciaObjeto + 5] = tiempoActual + 1;
        if (valorMontículo[referenciaObjeto + 3] > 0 && tiempoActual - (valorMontículo[referenciaObjeto + 5] - 1) >= valorMontículo[referenciaObjeto + 3]) { valorMontículo[referenciaObjeto + 5] = 0; lanzarExcepción(19, "stream wait timed out"); return false; }
        posiciónMarco[índiceMarco] = instrucciónMáquinaMarco[índiceMarco]; cambiarPetición = true; return true;
    }
    static void invocarFlujo(int propietario, int constanteNombre, int constanteDescriptor, int códigoComando) {
        boolean recibirPágina = textoPalabra(propietario, "java/net/ServerSocket"), flujo = textoPalabra(propietario, "java/io/InputStream") || textoPalabra(propietario, "java/io/OutputStream");
        if (!flujo && códigoComando == 183 && textoPalabra(constanteNombre, "<init>")) {
            boolean esEstadoValorVacíoEstado = textoPalabra(constanteDescriptor, "()V"), nombrado = textoPalabra(constanteDescriptor, "(Ljava/lang/String;I)V"), direccionado = textoPalabra(constanteDescriptor, "(Ljava/net/InetAddress;I)V");
            if (!(esEstadoValorVacíoEstado || recibirPágina && textoPalabra(constanteDescriptor, "(I)V") || !recibirPágina && (nombrado || direccionado))) { valorFallo("unsupported socket constructor"); return; }
            int númeroPuerto = esEstadoValorVacíoEstado ? 0 : restarValores(1), referenciaDirección = nombrado || direccionado ? restarValores(2) : 0, referenciaObjeto = restarValores(2);
            if (!valorObjeto(referenciaObjeto, recibirPágina ? 18 : 17)) return;
            if (númeroPuerto < 0 || númeroPuerto > 65535) { lanzarExcepción(9, "invalid port"); return; }
            if (direccionado && !valorObjeto(referenciaDirección, 14)) return;
            int direcciónRed = nombrado ? decodificarDirección(referenciaDirección) : direccionado ? valorMontículo[referenciaDirección + 2] : 0x7f000001;
            if (error || objetoLanzado != 0) return;
            int númeroArchivoAbierto = Usuario.controlFlujo(0, 0, 0); if (númeroArchivoAbierto < 0) { lanzarExcepción(39, "socket slots exhausted"); return; }
            int valorProcesado = esEstadoValorVacíoEstado ? 0 : recibirPágina ? Usuario.controlFlujo(1, númeroArchivoAbierto, númeroPuerto) : Usuario.conectarFlujo(númeroArchivoAbierto, direcciónRed, númeroPuerto);
            if (valorProcesado < 0) { Usuario.cerrarDescriptorArchivo(númeroArchivoAbierto); lanzarExcepción(39, "socket bind/connect failed"); return; }
            valorMontículo[referenciaObjeto + 2] = númeroArchivoAbierto; valorMontículo[referenciaObjeto + 4] = númeroPuerto; valorMontículo[referenciaObjeto + 6] = esEstadoValorVacíoEstado ? 0 : 1; return;
        }
        if (!flujo && textoPalabra(constanteNombre, "setSoTimeout") && textoPalabra(constanteDescriptor, "(I)V")) { int valorMilisegundos = restarValores(1), referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, recibirPágina ? 18 : 17)) return; if (valorMilisegundos < 0) lanzarExcepción(9, "negative timeout"); else valorMontículo[referenciaObjeto + 3] = valorMilisegundos; return; }
        if (!flujo && textoPalabra(constanteNombre, "close") && textoPalabra(constanteDescriptor, "()V")) { int referenciaObjeto = restarValores(2); if (valorObjeto(referenciaObjeto, recibirPágina ? 18 : 17) && valorMontículo[referenciaObjeto + 2] >= 0) { Usuario.cerrarDescriptorArchivo(valorMontículo[referenciaObjeto + 2]); valorMontículo[referenciaObjeto + 2] = -1; } return; }
        if (!flujo && (textoPalabra(constanteNombre, "getLocalPort") || textoPalabra(constanteNombre, "getPort") || textoPalabra(constanteNombre, "isClosed") || textoPalabra(constanteNombre, "isConnected"))) {
            int referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, recibirPágina ? 18 : 17)) return;
            ponerValor(textoPalabra(constanteNombre, "isClosed") ? valorMontículo[referenciaObjeto + 2] < 0 ? 1 : 0 : textoPalabra(constanteNombre, "isConnected") ? valorMontículo[referenciaObjeto + 6] : textoPalabra(constanteNombre, "getPort") ? valorMontículo[referenciaObjeto + 4] : valorMontículo[referenciaObjeto + 2] < 0 ? -1 : Usuario.controlFlujo(4, valorMontículo[referenciaObjeto + 2], 0), 1); return;
        }
        if (recibirPágina && textoPalabra(constanteNombre, "accept") && textoPalabra(constanteDescriptor, "()Ljava/net/Socket;")) {
            int referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, 18)) return; int númeroArchivoAbierto = Usuario.controlFlujo(3, valorMontículo[referenciaObjeto + 2], 0);
            if (númeroArchivoAbierto == -11) { if (esperarFlujoPara(referenciaObjeto)) ponerValor(referenciaObjeto, 2); return; }
            valorMontículo[referenciaObjeto + 5] = 0; if (númeroArchivoAbierto < 0) { lanzarExcepción(11, "accept failed"); return; }
            int valorDevuelto = asignarMemoriaAlmacenamiento(17, 5); if (error) { Usuario.cerrarDescriptorArchivo(númeroArchivoAbierto); return; } valorMontículo[valorDevuelto + 2] = númeroArchivoAbierto; valorMontículo[valorDevuelto + 4] = Usuario.controlFlujo(5, númeroArchivoAbierto, 0); valorMontículo[valorDevuelto + 6] = 1; ponerValor(valorDevuelto, 2); return;
        }
        if (!recibirPágina && !flujo && ((textoPalabra(constanteNombre, "getInputStream") && textoPalabra(constanteDescriptor, "()Ljava/io/InputStream;")) || (textoPalabra(constanteNombre, "getOutputStream") && textoPalabra(constanteDescriptor, "()Ljava/io/OutputStream;")))) {
            int referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, 17)) return; if (valorMontículo[referenciaObjeto + 2] < 0 || valorMontículo[referenciaObjeto + 6] == 0) { lanzarExcepción(39, "socket is not connected"); return; }
            int valorDevuelto = asignarMemoriaAlmacenamiento(19, 4); if (error) return; valorMontículo[valorDevuelto + 2] = referenciaObjeto; referenciaMontículo[valorDevuelto + 2] = 1; valorMontículo[valorDevuelto + 3] = textoPalabra(constanteNombre, "getInputStream") ? 0 : 1; ponerValor(valorDevuelto, 2); return;
        }
        if (flujo) {
            boolean tieneLeer = textoPalabra(constanteNombre, "read"), esOperaciónEscribir = textoPalabra(constanteNombre, "write"), bloque = textoPalabra(constanteDescriptor, "([B)I") || textoPalabra(constanteDescriptor, "([B)V"), esSubarreglo = textoPalabra(constanteDescriptor, "([BII)I") || textoPalabra(constanteDescriptor, "([BII)V");
            int númeroElementosEntradaElemento = esSubarreglo ? restarValores(1) : 0, iniciarDesplazamiento = esSubarreglo ? restarValores(1) : 0, arregloDatos = bloque || esSubarreglo ? restarValores(2) : 0;
            int valorDatos = esOperaciónEscribir && textoPalabra(constanteDescriptor, "(I)V") ? restarValores(1) : 0, referenciaObjeto = restarValores(2);
            if (!valorObjeto(referenciaObjeto, 19)) return; int referenciaPadre = valorMontículo[referenciaObjeto + 2], númeroArchivoAbierto = valorMontículo[referenciaPadre + 2];
            if (númeroArchivoAbierto < 0) { lanzarExcepción(11, "stream closed"); return; }
            if (textoPalabra(constanteNombre, "close") && textoPalabra(constanteDescriptor, "()V")) { Usuario.cerrarDescriptorArchivo(númeroArchivoAbierto); valorMontículo[referenciaPadre + 2] = -1; return; }
            if (textoPalabra(constanteNombre, "flush") && textoPalabra(constanteDescriptor, "()V")) return;
            if ((!tieneLeer && !esOperaciónEscribir) || tieneLeer != (valorMontículo[referenciaObjeto + 3] == 0)) { valorFallo("unsupported stream operation"); return; }
            if (bloque || esSubarreglo) { if (!valorObjeto(arregloDatos, 20)) return; if (bloque) númeroElementosEntradaElemento = valorMontículo[arregloDatos + 1]; if (iniciarDesplazamiento < 0 || númeroElementosEntradaElemento < 0 || iniciarDesplazamiento > valorMontículo[arregloDatos + 1] - númeroElementosEntradaElemento) { lanzarExcepción(6, "stream array bounds"); return; } }
            else númeroElementosEntradaElemento = 1;
            if (númeroElementosEntradaElemento == 0) { if (tieneLeer) ponerValor(0, 1); return; }
            int númeroElementosCompletado = esOperaciónEscribir ? valorMontículo[referenciaObjeto + 4] : 0, valorProcesado = 0;
            while (númeroElementosCompletado < númeroElementosEntradaElemento) {
                valorProcesado = tieneLeer ? Usuario.leerByteArchivoUno(númeroArchivoAbierto) : Usuario.escribirByteArchivoUno(númeroArchivoAbierto, bloque || esSubarreglo ? valorMontículo[arregloDatos + 2 + iniciarDesplazamiento + númeroElementosCompletado] : valorDatos);
                if (valorProcesado < 0 || tieneLeer && valorProcesado == 256) break;
                if (tieneLeer && (bloque || esSubarreglo)) valorMontículo[arregloDatos + 2 + iniciarDesplazamiento + númeroElementosCompletado] = (byte)valorProcesado;
                númeroElementosCompletado++; if (tieneLeer && !(bloque || esSubarreglo)) break;
            }
            if (valorProcesado == -11 && (esOperaciónEscribir || númeroElementosCompletado == 0)) {
                valorMontículo[referenciaObjeto + 4] = númeroElementosCompletado;
                if (esperarFlujoPara(referenciaPadre)) { ponerValor(referenciaObjeto, 2); if (bloque || esSubarreglo) ponerValor(arregloDatos, 2); if (esSubarreglo) { ponerValor(iniciarDesplazamiento, 1); ponerValor(númeroElementosEntradaElemento, 1); } if (esOperaciónEscribir && !(bloque || esSubarreglo)) ponerValor(valorDatos, 1); } return;
            }
            valorMontículo[referenciaObjeto + 4] = 0; valorMontículo[referenciaPadre + 5] = 0;
            if (valorProcesado < 0 && valorProcesado != -11) { lanzarExcepción(11, "stream I/O failed"); return; }
            if (tieneLeer) ponerValor(númeroElementosCompletado == 0 && valorProcesado == 256 ? -1 : bloque || esSubarreglo ? númeroElementosCompletado : valorProcesado, 1); return;
        }
        valorFallo("unsupported Socket/ServerSocket method");
    }
    static int[] referenciaPantalla = new int[32], textoPantallaTemporal = new int[256], posteriorPlanificación = new int[8];
    static int númeroElementosPosterior;
    static int[] valorCoreanoPosterior = new int[8];
    static boolean esEventoEstadoTratamiento;
    static int clasePantallaCoreano(int constanteNombre) {
        if (textoPalabra(constanteNombre, "español/propio/ventana")) return 24;
        if (textoPalabra(constanteNombre, "español/propio/etiqueta")) return 26;
        if (textoPalabra(constanteNombre, "español/propio/botón")) return 27;
        if (textoPalabra(constanteNombre, "español/propio/CampoTexto")) return 28;
        if (textoPalabra(constanteNombre, "español/propio/NotificaciónAcción")) return 29;
        return 0;
    }
    static boolean propietarioPantallaCoreano(int constanteNombre) {
        return clasePantallaCoreano(constanteNombre) != 0 || textoPalabra(constanteNombre, "español/propio/ElementoPantalla") || textoPalabra(constanteNombre, "español/propio/ColaEvento");
    }
    static int clasePantalla(int constanteNombre) {
        int ClaseCoreano = clasePantallaCoreano(constanteNombre); if (ClaseCoreano != 0) return ClaseCoreano;
        if (textoPalabra(constanteNombre, "javax/swing/JFrame")) return 24;
        if (textoPalabra(constanteNombre, "javax/swing/JPanel")) return 25;
        if (textoPalabra(constanteNombre, "javax/swing/JLabel")) return 26;
        if (textoPalabra(constanteNombre, "javax/swing/JButton")) return 27;
        if (textoPalabra(constanteNombre, "javax/swing/JTextField")) return 28;
        if (textoPalabra(constanteNombre, "java/awt/event/ActionEvent")) return 29;
        if (textoPalabra(constanteNombre, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean propietarioPantalla(int constanteNombre) {
        return clasePantalla(constanteNombre) != 0 || textoPalabra(constanteNombre, "java/awt/Component") || textoPalabra(constanteNombre, "java/awt/Container") || textoPalabra(constanteNombre, "javax/swing/JComponent") || textoPalabra(constanteNombre, "javax/swing/AbstractButton") || textoPalabra(constanteNombre, "javax/swing/text/JTextComponent") || textoPalabra(constanteNombre, "javax/swing/SwingUtilities");
    }
    static boolean objetoPantalla(int referenciaObjeto) { if (!esObjetoVálido(referenciaObjeto)) return false; if (valorMontículo[referenciaObjeto] < 24 || valorMontículo[referenciaObjeto] > 28) { valorFallo("unsupported Swing receiver"); return false; } return true; }
    static void establecerCarácterPantalla(int referenciaObjeto, int referenciaTexto) {
        if (referenciaTexto != 0 && !valorObjeto(referenciaTexto, 1)) return;
        int númeroElementosEntradaElemento = referenciaTexto == 0 ? 0 : valorMontículo[referenciaTexto + 1]; if (númeroElementosEntradaElemento > 254) { lanzarExcepción(9, "GUI text limit"); return; }
        for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) textoPantallaTemporal[índiceBucle] = valorMontículo[referenciaTexto + 2 + índiceBucle];
        if (Usuario.textoPantalla(valorMontículo[referenciaObjeto + 2], textoPantallaTemporal, númeroElementosEntradaElemento) < 0) { lanzarExcepción(9, "GUI text too long/invalid"); return; }
        valorMontículo[referenciaObjeto + 3] = referenciaTexto; referenciaMontículo[referenciaObjeto + 3] = 1;
    }
    static int leerCarácterPantalla(int referenciaObjeto) {
        int valorIdentidad = valorMontículo[referenciaObjeto + 2], númeroElementosEntradaElemento = Usuario.conexiónPantalla(8, valorIdentidad, 0, 0, 0, 0), númeroElementosUsado = 0;
        if (númeroElementosEntradaElemento < 0) { valorFallo("GUI text read failed"); return 0; }
        for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) { int valorCodificado = Usuario.conexiónPantalla(9, valorIdentidad, índiceBucle, 0, 0, 0); if (valorCodificado >= 65536) { valorCodificado -= 65536; textoPantallaTemporal[númeroElementosUsado++] = 0xd800 | valorCodificado >> 10; textoPantallaTemporal[númeroElementosUsado++] = 0xdc00 | valorCodificado & 1023; } else textoPantallaTemporal[númeroElementosUsado++] = valorCodificado; }
        int valorDevuelto = asignarMemoriaAlmacenamiento(1, númeroElementosUsado); if (!error) for (int índiceBucle = 0; índiceBucle < númeroElementosUsado; índiceBucle++) valorMontículo[valorDevuelto + 2 + índiceBucle] = textoPantallaTemporal[índiceBucle]; return valorDevuelto;
    }
    /* Crea directamente objetos de la API en español y los conecta con los gráficos del núcleo, sin objetos ni adaptadores Swing. */
    static void invocarPantallaCoreano(int propietario, int constanteNombre, int constanteDescriptor, int códigoComando) {
        if (textoPalabra(propietario, "español/propio/ColaEvento")) {
            if (códigoComando == 184 && textoPalabra(constanteNombre, "invocarPosterior") && textoPalabra(constanteDescriptor, "(Lespañol/propio/TareaTareaEjecutable;)V")) {
                int AcciónTarea = restarValores(2); if (!esObjetoVálido(AcciónTarea)) return;
                if (númeroElementosPosterior == 8) { valorFallo("Pantalla Tarea 대기열이 가득 찼습니다"); return; }
                valorCoreanoPosterior[númeroElementosPosterior] = 1; posteriorPlanificación[númeroElementosPosterior++] = AcciónTarea; return;
            }
            if (códigoComando == 184 && textoPalabra(constanteNombre, "esDespachoEnCursoEvento") && textoPalabra(constanteDescriptor, "()Z")) { ponerValor(esEventoEstadoTratamiento ? 1 : 0, 1); return; }
            valorFallo("지원하지 않는 español Pantalla 일정 invocar"); return;
        }
        if (textoPalabra(propietario, "español/propio/NotificaciónAcción")) {
            int notificación = restarValores(2); if (!valorObjeto(notificación, 29) || valorMontículo[notificación + 3] == 0) return;
            if (textoPalabra(constanteNombre, "fuenteEvento") && textoPalabra(constanteDescriptor, "()Lespañol/propio/ElementoPantalla;")) ponerValor(valorMontículo[notificación + 2], 2);
            else if (textoPalabra(constanteNombre, "textoComando") && textoPalabra(constanteDescriptor, "()Ljava/lang/String;")) ponerValor(leerCarácterPantalla(valorMontículo[notificación + 2]), 2);
            else if (textoPalabra(constanteNombre, "número") && textoPalabra(constanteDescriptor, "()I")) ponerValor(1001, 1);
            else valorFallo("지원하지 않는 español acción notificación invocar"); return;
        }
        if (códigoComando == 183 && textoPalabra(constanteNombre, "<init>")) {
            int valorClaseTipo = clasePantallaCoreano(propietario), valorReceptor = 0, posiciónHorizontal = 0, posiciónVertical = 0, extensiónRangoAnchura = 0, valorAltura = 0;
            if (valorClaseTipo == 24 && textoPalabra(constanteDescriptor, "(Ljava/lang/String;II)V")) {
                valorAltura = restarValores(1); extensiónRangoAnchura = restarValores(1); posiciónHorizontal = (Usuario.anchuraPantalla() - extensiónRangoAnchura) / 2; posiciónVertical = (Usuario.alturaPantalla() - valorAltura) / 2;
            } else if ((valorClaseTipo == 26 || valorClaseTipo == 28) && textoPalabra(constanteDescriptor, "(Ljava/lang/String;IIII)V") || valorClaseTipo == 27 && textoPalabra(constanteDescriptor, "(Ljava/lang/String;IIIILespañol/propio/ReceptorAcción;)V")) {
                if (valorClaseTipo == 27) valorReceptor = restarValores(2);
                valorAltura = restarValores(1); extensiónRangoAnchura = restarValores(1); posiciónVertical = restarValores(1); posiciónHorizontal = restarValores(1);
            } else { valorFallo("지원하지 않는 español Pantalla 생성자"); return; }
            int texto = restarValores(2), valorElemento = restarValores(2); if (!objetoPantalla(valorElemento)) return;
            if (extensiónRangoAnchura < 1 || valorAltura < 1 || posiciónHorizontal < 0 || posiciónVertical < 0 || extensiónRangoAnchura > Usuario.anchuraPantalla() - posiciónHorizontal || valorAltura > Usuario.alturaPantalla() - posiciónVertical) { lanzarExcepción(27, "Pantalla 영역을 벗어난 크기입니다"); return; }
            int número = Usuario.conexiónPantalla(0, valorClaseTipo - 23, 0, 0, 0, 0);
            if (número < 1 || número > 32) { valorFallo("Pantalla valorElemento 자리가 가득 찼습니다"); return; }
            valorMontículo[valorElemento + 2] = número; referenciaPantalla[número - 1] = valorElemento;
            valorMontículo[valorElemento + 5] = posiciónHorizontal; valorMontículo[valorElemento + 6] = posiciónVertical; valorMontículo[valorElemento + 7] = extensiónRangoAnchura; valorMontículo[valorElemento + 8] = valorAltura; valorMontículo[valorElemento + 10] = 2;
            valorMontículo[valorElemento + 4] = valorReceptor; referenciaMontículo[valorElemento + 4] = 1; valorMontículo[valorElemento + 12] = 1;
            Usuario.conexiónPantalla(1, número, posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, valorAltura);
            if (valorClaseTipo == 24) Usuario.conexiónPantalla(7, número, 2, 0, 0, 0);
            establecerCarácterPantalla(valorElemento, texto); return;
        }
        if (códigoComando != 182) { valorFallo("잘못된 español Pantalla invocar comando"); return; }
        if (textoPalabra(constanteNombre, "escribirTexto") && textoPalabra(constanteDescriptor, "(Ljava/lang/String;)V")) {
            int texto = restarValores(2), valorElemento = restarValores(2); if (objetoPantalla(valorElemento)) establecerCarácterPantalla(valorElemento, texto); return;
        }
        if (textoPalabra(constanteNombre, "leerTexto") && textoPalabra(constanteDescriptor, "()Ljava/lang/String;")) {
            int valorElemento = restarValores(2); if (objetoPantalla(valorElemento)) ponerValor(leerCarácterPantalla(valorElemento), 2); return;
        }
        if (textoPalabra(constanteNombre, "establecerReceptorAcción") && textoPalabra(constanteDescriptor, "(Lespañol/propio/ReceptorAcción;)V")) {
            int valorReceptor = restarValores(2), valorElemento = restarValores(2);
            if (objetoPantalla(valorElemento)) { valorMontículo[valorElemento + 4] = valorReceptor; referenciaMontículo[valorElemento + 4] = 1; valorMontículo[valorElemento + 12] = 1; } return;
        }
        if (textoPalabra(constanteNombre, "añadirElemento") && textoPalabra(constanteDescriptor, "(Lespañol/propio/ElementoPantalla;)V")) {
            int valorHijo = restarValores(2), valorPadre = restarValores(2); if (!objetoPantalla(valorHijo) || !objetoPantalla(valorPadre)) return;
            if (Usuario.conexiónPantalla(2, valorMontículo[valorPadre + 2], valorMontículo[valorHijo + 2], 0, 0, 0) < 0) { lanzarExcepción(27, "잘못된 Pantalla 부모입니다"); return; }
            valorMontículo[valorHijo + 11] = valorPadre; referenciaMontículo[valorHijo + 11] = 1; return;
        }
        if (textoPalabra(constanteNombre, "establecerLímites") && textoPalabra(constanteDescriptor, "(IIII)V")) {
            int valorAltura = restarValores(1), extensiónRangoAnchura = restarValores(1), posiciónVertical = restarValores(1), posiciónHorizontal = restarValores(1), valorElemento = restarValores(2); if (!objetoPantalla(valorElemento)) return;
            if (Usuario.conexiónPantalla(1, valorMontículo[valorElemento + 2], posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, valorAltura) < 0) { lanzarExcepción(27, "Pantalla 영역을 벗어난 자리입니다"); return; }
            valorMontículo[valorElemento + 5] = posiciónHorizontal; valorMontículo[valorElemento + 6] = posiciónVertical; valorMontículo[valorElemento + 7] = extensiónRangoAnchura; valorMontículo[valorElemento + 8] = valorAltura; return;
        }
        if ((textoPalabra(constanteNombre, "mostrarVentana") || textoPalabra(constanteNombre, "cerrar")) && textoPalabra(constanteDescriptor, "()V")) {
            boolean valorVisibilidad = textoPalabra(constanteNombre, "mostrarVentana"); int valorElemento = restarValores(2); if (!objetoPantalla(valorElemento)) return;
            if (Usuario.conexiónPantalla(valorVisibilidad ? 3 : 4, valorMontículo[valorElemento + 2], valorVisibilidad ? 1 : 0, 0, 0, 0) < 0) { valorFallo("화면은 interactivo 명령에서 실행해야 합니다"); return; }
            valorMontículo[valorElemento + 9] = valorVisibilidad ? 1 : 0; return;
        }
        if (textoPalabra(constanteNombre, "esVisible") && textoPalabra(constanteDescriptor, "()Z")) { int valorElemento = restarValores(2); if (objetoPantalla(valorElemento)) ponerValor(valorMontículo[valorElemento + 9], 1); return; }
        valorFallo("지원하지 않는 español Pantalla valorMétodo");
    }
    static void invocarPantalla(int propietario, int constanteNombre, int constanteDescriptor, int códigoComando) {
        if (textoPalabra(propietario, "javax/swing/SwingUtilities")) {
            if (códigoComando == 184 && textoPalabra(constanteNombre, "invokeLater") && textoPalabra(constanteDescriptor, "(Ljava/lang/Runnable;)V")) { int referenciaObjeto = restarValores(2); if (!esObjetoVálido(referenciaObjeto)) return; if (númeroElementosPosterior == 8) { valorFallo("invokeLater queue full"); return; } posteriorPlanificación[númeroElementosPosterior++] = referenciaObjeto; return; }
            if (códigoComando == 184 && textoPalabra(constanteNombre, "isEventDispatchThread") && textoPalabra(constanteDescriptor, "()Z")) { ponerValor(esEventoEstadoTratamiento ? 1 : 0, 1); return; }
            valorFallo("unsupported SwingUtilities method"); return;
        }
        if (textoPalabra(propietario, "java/awt/event/ActionEvent")) {
            int referenciaObjeto = restarValores(2); if (!valorObjeto(referenciaObjeto, 29)) return;
            if (textoPalabra(constanteNombre, "getSource") && textoPalabra(constanteDescriptor, "()Ljava/lang/Object;")) ponerValor(valorMontículo[referenciaObjeto + 2], 2);
            else if (textoPalabra(constanteNombre, "getActionCommand") && textoPalabra(constanteDescriptor, "()Ljava/lang/String;")) ponerValor(leerCarácterPantalla(valorMontículo[referenciaObjeto + 2]), 2);
            else if (textoPalabra(constanteNombre, "getID") && textoPalabra(constanteDescriptor, "()I")) ponerValor(1001, 1);
            else valorFallo("unsupported ActionEvent method"); return;
        }
        if (códigoComando == 183 && textoPalabra(constanteNombre, "<init>")) {
            int columnas = 0, referenciaTexto = 0;
            if (textoPalabra(constanteDescriptor, "(I)V")) columnas = restarValores(1);
            else if (textoPalabra(constanteDescriptor, "(Ljava/lang/String;I)V")) { columnas = restarValores(1); referenciaTexto = restarValores(2); }
            else if (textoPalabra(constanteDescriptor, "(Ljava/lang/String;)V")) referenciaTexto = restarValores(2);
            else if (textoPalabra(constanteDescriptor, "(Ljava/awt/LayoutManager;)V")) restarValores(2);
            else if (!textoPalabra(constanteDescriptor, "()V")) { valorFallo("unsupported Swing constructor"); return; }
            int referenciaObjeto = restarValores(2); if (!esObjetoVálido(referenciaObjeto)) return;
            if (valorMontículo[referenciaObjeto] == 30) { valorFallo("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!objetoPantalla(referenciaObjeto) || columnas < 0) return;
            int valorIdentidad = Usuario.conexiónPantalla(0, valorMontículo[referenciaObjeto] - 23, 0, 0, 0, 0);
            if (valorIdentidad < 1 || valorIdentidad > 32) { valorFallo("GUI widget slots exhausted"); return; }
            valorMontículo[referenciaObjeto + 2] = valorIdentidad; referenciaPantalla[valorIdentidad - 1] = referenciaObjeto; valorMontículo[referenciaObjeto + 5] = valorMontículo[referenciaObjeto] == 24 ? 130 : 16; valorMontículo[referenciaObjeto + 6] = valorMontículo[referenciaObjeto] == 24 ? 110 : 16;
            valorMontículo[referenciaObjeto + 7] = valorMontículo[referenciaObjeto] == 24 ? 380 : 220; valorMontículo[referenciaObjeto + 8] = valorMontículo[referenciaObjeto] == 24 ? 240 : 28; valorMontículo[referenciaObjeto + 10] = 1;
            establecerCarácterPantalla(referenciaObjeto, referenciaTexto); return;
        }
        if (textoPalabra(constanteNombre, "setText") || textoPalabra(constanteNombre, "setTitle")) { int referenciaTexto = restarValores(2), referenciaObjeto = restarValores(2); if (objetoPantalla(referenciaObjeto) && textoPalabra(constanteDescriptor, "(Ljava/lang/String;)V")) establecerCarácterPantalla(referenciaObjeto, referenciaTexto); return; }
        if (textoPalabra(constanteNombre, "getText") || textoPalabra(constanteNombre, "getTitle")) { int referenciaObjeto = restarValores(2); if (objetoPantalla(referenciaObjeto) && textoPalabra(constanteDescriptor, "()Ljava/lang/String;")) ponerValor(leerCarácterPantalla(referenciaObjeto), 2); return; }
        if (textoPalabra(constanteNombre, "addActionListener") && textoPalabra(constanteDescriptor, "(Ljava/awt/event/ActionListener;)V")) { int recibirReferencia = restarValores(2), referenciaObjeto = restarValores(2); if (objetoPantalla(referenciaObjeto)) { valorMontículo[referenciaObjeto + 4] = recibirReferencia; referenciaMontículo[referenciaObjeto + 4] = 1; } return; }
        if (textoPalabra(constanteNombre, "getContentPane") && textoPalabra(constanteDescriptor, "()Ljava/awt/Container;")) { int referenciaObjeto = restarValores(2); if (objetoPantalla(referenciaObjeto)) ponerValor(referenciaObjeto, 2); return; }
        if (textoPalabra(constanteNombre, "setLayout") && textoPalabra(constanteDescriptor, "(Ljava/awt/LayoutManager;)V")) { int referenciaDisposición = restarValores(2), referenciaObjeto = restarValores(2); if (objetoPantalla(referenciaObjeto) && referenciaDisposición != 0) valorFallo("only absolute layout (null) is supported"); return; }
        if (textoPalabra(constanteNombre, "add") && (textoPalabra(constanteDescriptor, "(Ljava/awt/Component;)Ljava/awt/Component;") || textoPalabra(constanteDescriptor, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean condiciónDisposición = textoPalabra(constanteDescriptor, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (condiciónDisposición) restarValores(2);
            int referenciaHijo = restarValores(2), referenciaObjeto = restarValores(2); if (!objetoPantalla(referenciaHijo) || !objetoPantalla(referenciaObjeto)) return;
            if (Usuario.conexiónPantalla(2, valorMontículo[referenciaObjeto + 2], valorMontículo[referenciaHijo + 2], 0, 0, 0) < 0) { lanzarExcepción(9, "invalid GUI parent"); return; }
            valorMontículo[referenciaHijo + 11] = referenciaObjeto; referenciaMontículo[referenciaHijo + 11] = 1; if (!condiciónDisposición) ponerValor(referenciaHijo, 2); return;
        }
        if (textoPalabra(constanteNombre, "setBounds") && textoPalabra(constanteDescriptor, "(IIII)V")) {
            int valorAltura = restarValores(1), valorAnchura = restarValores(1), coordenadaCoordenadaVertical = restarValores(1), coordenadaCoordenadaHorizontal = restarValores(1), referenciaObjeto = restarValores(2); if (!objetoPantalla(referenciaObjeto)) return;
            if (Usuario.conexiónPantalla(1, valorMontículo[referenciaObjeto + 2], coordenadaCoordenadaHorizontal, coordenadaCoordenadaVertical, valorAnchura, valorAltura) < 0) { lanzarExcepción(9, "GUI bounds"); return; }
            valorMontículo[referenciaObjeto + 5] = coordenadaCoordenadaHorizontal; valorMontículo[referenciaObjeto + 6] = coordenadaCoordenadaVertical; valorMontículo[referenciaObjeto + 7] = valorAnchura; valorMontículo[referenciaObjeto + 8] = valorAltura; return;
        }
        if (textoPalabra(constanteNombre, "setSize") && textoPalabra(constanteDescriptor, "(II)V")) {
            int valorAltura = restarValores(1), valorAnchura = restarValores(1), referenciaObjeto = restarValores(2); if (!objetoPantalla(referenciaObjeto)) return;
            if (Usuario.conexiónPantalla(1, valorMontículo[referenciaObjeto + 2], valorMontículo[referenciaObjeto + 5], valorMontículo[referenciaObjeto + 6], valorAnchura, valorAltura) < 0) lanzarExcepción(9, "GUI size"); else { valorMontículo[referenciaObjeto + 7] = valorAnchura; valorMontículo[referenciaObjeto + 8] = valorAltura; } return;
        }
        if (textoPalabra(constanteNombre, "setLocationRelativeTo") && textoPalabra(constanteDescriptor, "(Ljava/awt/Component;)V")) { int relativo = restarValores(2), referenciaObjeto = restarValores(2); if (!objetoPantalla(referenciaObjeto)) return; if (relativo != 0) { valorFallo("only screen centering supported"); return; } valorMontículo[referenciaObjeto + 5] = (Usuario.anchuraPantalla() - valorMontículo[referenciaObjeto + 7]) / 2; valorMontículo[referenciaObjeto + 6] = (Usuario.alturaPantalla() - valorMontículo[referenciaObjeto + 8]) / 2; Usuario.conexiónPantalla(1, valorMontículo[referenciaObjeto + 2], valorMontículo[referenciaObjeto + 5], valorMontículo[referenciaObjeto + 6], valorMontículo[referenciaObjeto + 7], valorMontículo[referenciaObjeto + 8]); return; }
        if (textoPalabra(constanteNombre, "setDefaultCloseOperation") && textoPalabra(constanteDescriptor, "(I)V")) { int política = restarValores(1), referenciaObjeto = restarValores(2); if (objetoPantalla(referenciaObjeto)) { if (política < 0 || política > 3) lanzarExcepción(9, "close policy"); else { valorMontículo[referenciaObjeto + 10] = política; Usuario.conexiónPantalla(7, valorMontículo[referenciaObjeto + 2], política, 0, 0, 0); } } return; }
        if (textoPalabra(constanteNombre, "setVisible") && textoPalabra(constanteDescriptor, "(Z)V")) { int valorDatos = restarValores(1), referenciaObjeto = restarValores(2); if (objetoPantalla(referenciaObjeto)) { int valorProcesado = Usuario.conexiónPantalla(3, valorMontículo[referenciaObjeto + 2], valorDatos, 0, 0, 0); if (valorProcesado < 0) valorFallo("Swing requires a standalone interactive command"); else valorMontículo[referenciaObjeto + 9] = valorDatos; } return; }
        if (textoPalabra(constanteNombre, "dispose") && textoPalabra(constanteDescriptor, "()V")) { int referenciaObjeto = restarValores(2); if (objetoPantalla(referenciaObjeto)) { Usuario.conexiónPantalla(4, valorMontículo[referenciaObjeto + 2], 0, 0, 0, 0); valorMontículo[referenciaObjeto + 9] = 0; } return; }
        if (textoPalabra(constanteNombre, "repaint") || textoPalabra(constanteNombre, "validate")) { int referenciaObjeto = restarValores(2); if (!objetoPantalla(referenciaObjeto) || !textoPalabra(constanteDescriptor, "()V")) return; Usuario.conexiónPantalla(1, valorMontículo[referenciaObjeto + 2], valorMontículo[referenciaObjeto + 5], valorMontículo[referenciaObjeto + 6], valorMontículo[referenciaObjeto + 7], valorMontículo[referenciaObjeto + 8]); return; }
        if (textoPalabra(constanteNombre, "isVisible") && textoPalabra(constanteDescriptor, "()Z")) { int referenciaObjeto = restarValores(2); if (objetoPantalla(referenciaObjeto)) ponerValor(valorMontículo[referenciaObjeto + 9], 1); return; }
        valorFallo("unsupported Swing method (native subset)");
    }
    static void eventoDespachar(int direcciónObjetivo, int númeroEvento, boolean español) {
        if (direcciónObjetivo < 1 || valorMontículo[direcciónObjetivo] < 32) { valorFallo("Java event listener required"); return; }
        int índiceArchivo = métodoNombre(valorMontículo[direcciónObjetivo] - 32, númeroEvento == 0 ? (español ? "ejecutarTarea" : "run") : (español ? "recibirAcción" : "actionPerformed"), númeroEvento == 0 ? "()V" : (español ? "(Lespañol/propio/NotificaciónAcción;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (índiceArchivo < 0) { valorFallo("event callback missing"); return; }
        hiloEjecuciónActual = 0; númeroElementosHiloEjecución = 1; índiceMarco = 0; estadoValorHiloEjecución[0] = 1; pilaMarco[0] = 0; cerrojoMarco[0] = inicializarMarco[0] = 0; cambiarPetición = false;
        for (int índiceBucle = 0; índiceBucle < 128; índiceBucle++) { valorLocal[índiceBucle] = tipoLocal[índiceBucle] = 0; }
        métodoMarco[0] = índiceArchivo; posiciónMarco[0] = iniciarMétodo[índiceArchivo]; valorLocal[0] = direcciónObjetivo; tipoLocal[0] = 2;
        if (númeroEvento != 0) { valorLocal[1] = númeroEvento; tipoLocal[1] = 2; }
        esEventoEstadoTratamiento = true; ejecutarComando(); esEventoEstadoTratamiento = false;
    }
    static void eventosPantalla() {
        while (!error) {
            if (númeroElementosPosterior > 0) { int direcciónObjetivo = posteriorPlanificación[0], español = valorCoreanoPosterior[0]; for (int índiceBucle = 1; índiceBucle < númeroElementosPosterior; índiceBucle++) { posteriorPlanificación[índiceBucle - 1] = posteriorPlanificación[índiceBucle]; valorCoreanoPosterior[índiceBucle - 1] = valorCoreanoPosterior[índiceBucle]; } posteriorPlanificación[--númeroElementosPosterior] = 0; valorCoreanoPosterior[númeroElementosPosterior] = 0; eventoDespachar(direcciónObjetivo, 0, español != 0); continue; }
            if (Usuario.conexiónPantalla(6, 0, 0, 0, 0, 0) == 0) return;
            int númeroEvento = Usuario.conexiónPantalla(5, 0, 0, 0, 0, 0); if (númeroEvento == 0) continue;
            if (númeroEvento < 0) { valorFallo("GUI event I/O failed"); return; }
            int valorIdentidad = númeroEvento & 65535; if (valorIdentidad < 1 || valorIdentidad > 32) continue; int referenciaObjeto = referenciaPantalla[valorIdentidad - 1]; if (referenciaObjeto == 0) continue;
            if ((númeroEvento & 65536) != 0) {
                if (valorMontículo[referenciaObjeto + 10] != 0) valorMontículo[referenciaObjeto + 9] = 0;
                if (valorMontículo[referenciaObjeto + 10] == 3) for (int índiceBucle = 0; índiceBucle < 32; índiceBucle++) if (referenciaPantalla[índiceBucle] != 0 && valorMontículo[referenciaPantalla[índiceBucle]] == 24) Usuario.conexiónPantalla(4, índiceBucle + 1, 0, 0, 0, 0);
            } else if (valorMontículo[referenciaObjeto + 4] != 0) {
                int referenciaLéame = asignarMemoriaAlmacenamiento(29, 2); if (error) return; valorMontículo[referenciaLéame + 2] = referenciaObjeto; valorMontículo[referenciaLéame + 3] = valorMontículo[referenciaObjeto + 12]; referenciaMontículo[referenciaLéame + 2] = 1; eventoDespachar(valorMontículo[referenciaObjeto + 4], referenciaLéame, valorMontículo[referenciaObjeto + 12] != 0);
            }
        }
    }
    public static int ponerEnMarcha() {
        if (Usuario.númeroElementosArgumentos() == 1 && HerramientaJava.textoIgual(Usuario.argumentos(0), "-version")) {
            Usuario.escribir("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (Usuario.númeroElementosArgumentos() < 1) { Usuario.escribir("Usage: java CLASS [ARGS]\n"); return 2; }
        definiciónClaseEntradaElemento = cargarDefiniciónClase(carácterAnfitrión(Usuario.argumentos(0))); if (error || definiciónClaseEntradaElemento < 0) return 1;
        int valorPuntoEntradaElemento = métodoNombre(definiciónClaseEntradaElemento, "ponerEnMarcha", "()V");
        boolean entradaElementoCoreano = valorPuntoEntradaElemento >= 0 && (accesoMétodo[valorPuntoEntradaElemento] & 9) == 9;
        if (!entradaElementoCoreano) valorPuntoEntradaElemento = métodoNombre(definiciónClaseEntradaElemento, "main", "([Ljava/lang/String;)V");
        if (valorPuntoEntradaElemento < 0 || (accesoMétodo[valorPuntoEntradaElemento] & 9) != 9) valorFallo("public static void ponerEnMarcha() or main(String[] args) required");
        if (error) return 1;
        int argumentos = asignarMemoriaAlmacenamiento(3, Usuario.númeroElementosArgumentos() - 1); elementoArreglo[argumentos] = -1;
        for (int númeroValor = 1; númeroValor < Usuario.númeroElementosArgumentos() && !error; númeroValor++) valorMontículo[argumentos + 1 + númeroValor] = carácterAnfitrión(Usuario.argumentos(númeroValor));
        índiceMarco = 0; métodoMarco[0] = valorPuntoEntradaElemento; posiciónMarco[0] = iniciarMétodo[valorPuntoEntradaElemento]; valorLocal[0] = entradaElementoCoreano ? 0 : argumentos; tipoLocal[0] = entradaElementoCoreano ? 0 : 2;
        estadoValorHiloEjecución[0] = 1; objetoHiloEjecución[0] = asignarMemoriaAlmacenamiento(13, 2);
        ejecutarComando(); if (!error) eventosPantalla(); return error ? 1 : 0;
    }
}
