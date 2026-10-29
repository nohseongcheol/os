// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Línea de órdenes UTF-8 por UART, con comillas, Backspace, Ctrl-U, Ctrl-C y editor en RAM. */
public final class IntérpreteComandos {
    static int[] línea = new int[4096], valorTokenLéxico = new int[4096], puntoInicial = new int[32], longitud = new int[32];
    static int[] contenidoEditado = new int[16384], nombreEditar = new int[63];
    static int númeroElementosTokenLéxico, longitudNombreEditar, resultado;
    static boolean líneaElementoPrevio;
    static void byteOriginal(int valor) { Placa.escribirSerie(valor); }
    static int leerLíneaEntrada() { return EditorLínea.leer(); }
    static boolean valoresDividir(int tamaño) {
        int posición = 0, terminación = 0; númeroElementosTokenLéxico = 0;
        while (posición < tamaño) {
            while (posición < tamaño && (línea[posición] == 32 || línea[posición] == 9)) posición++;
            if (posición == tamaño) break;
            if (númeroElementosTokenLéxico == 16) { EntradaSalidaTerminal.escribir("comando analizarValor: 인수가 너무 많습니다\n"); return false; }
            puntoInicial[númeroElementosTokenLéxico] = terminación; int valorComilla = 0;
            while (posición < tamaño) {
                int valor = línea[posición++];
                if (valorComilla == 0 && (valor == 32 || valor == 9)) break;
                if (valor == valorComilla) { valorComilla = 0; continue; }
                if (valorComilla == 0 && (valor == 39 || valor == 34)) { valorComilla = valor; continue; }
                valorTokenLéxico[terminación++] = valor;
            }
            if (valorComilla != 0) { EntradaSalidaTerminal.escribir("comando analizarValor: 따옴표가 닫히지 않았습니다\n"); return false; }
            longitud[númeroElementosTokenLéxico] = terminación - puntoInicial[númeroElementosTokenLéxico]; númeroElementosTokenLéxico++;
        }
        return true;
    }
    static boolean textoIgual(int número, String textoPalabra) {
        if (número >= númeroElementosTokenLéxico) return false;
        int índicePosición=0;
        for (int índiceOrdinal=0; índiceOrdinal<textoPalabra.length(); índiceOrdinal++) {
            int códigoCarácter=textoPalabra.charAt(índiceOrdinal);
            if (códigoCarácter>=0xd800 && códigoCarácter<=0xdbff && índiceOrdinal+1<textoPalabra.length()) códigoCarácter=0x10000+((códigoCarácter-0xd800)<<10)+textoPalabra.charAt(++índiceOrdinal)-0xdc00;
            int númeroElementosByte=códigoCarácter<128?1:códigoCarácter<2048?2:códigoCarácter<65536?3:4;
            for (int valorSecuencia=númeroElementosByte-1; valorSecuencia>=0; valorSecuencia--) {
                int valor=númeroElementosByte==1?códigoCarácter:valorSecuencia==númeroElementosByte-1?(númeroElementosByte==2?0xc0:númeroElementosByte==3?0xe0:0xf0)|(códigoCarácter>>(6*valorSecuencia)):0x80|((códigoCarácter>>(6*valorSecuencia))&63);
                if (índicePosición>=longitud[número] || valorTokenLéxico[puntoInicial[número]+índicePosición++]!=valor) return false;
            }
        }
        return índicePosición==longitud[número];
    }
    static int ruta(int número) {
        if (número >= númeroElementosTokenLéxico) return -22;
        int resultado = ArchivosMemoria.iniciarRuta(longitud[número]); if (resultado < 0) return resultado;
        for (int índiceBucle = 0; índiceBucle < longitud[número]; índiceBucle++) {
            resultado = ArchivosMemoria.byteRuta(índiceBucle, valorTokenLéxico[puntoInicial[número] + índiceBucle]); if (resultado < 0) return resultado;
        }
        return 0;
    }
    static void error(int número) { resultado = 1; EntradaSalidaTerminal.escribir("error "); EntradaSalidaTerminal.númeroValor(número); EntradaSalidaTerminal.Caracteres(10); }
    static void valorVista() {
        if (númeroElementosTokenLéxico != 2) { EntradaSalidaTerminal.escribir("사용법: cat Archivo\n"); return; }
        int resultado = ruta(1); if (resultado < 0) { error(resultado); return; }
        int Archivo = ArchivosMemoria.abrir(0); if (Archivo < 0) { error(Archivo); return; }
        while (true) { int valor = ArchivosMemoria.leer(Archivo); if (valor == 256) break; if (valor < 0) { error(valor); break; } byteOriginal(valor); }
        ArchivosMemoria.cerrar(Archivo); EntradaSalidaTerminal.Caracteres(10);
    }
    static void valorEditar() {
        if (númeroElementosTokenLéxico != 2) { EntradaSalidaTerminal.escribir("사용법: edit Archivo\n"); return; }
        int resultado = ruta(1); if (resultado < 0) { error(resultado); return; }
        longitudNombreEditar = longitud[1];
        for (int índiceBucle = 0; índiceBucle < longitudNombreEditar; índiceBucle++) nombreEditar[índiceBucle] = valorTokenLéxico[puntoInicial[1] + índiceBucle];
        EntradaSalidaTerminal.escribir("EDIT: Archivo 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(valorMáximo 16384바이트)\n");
        int tamaño = 0;
        while (true) {
            EntradaSalidaTerminal.escribir("edit> "); int valorEntrada = leerLíneaEntrada();
            if (valorEntrada < 0) { EntradaSalidaTerminal.escribir("EDIT CANCELLED\n"); return; }
            if (valorEntrada == 1 && línea[0] == '.') break;
            if (valorEntrada + 1 > contenidoEditado.length - tamaño) { EntradaSalidaTerminal.escribir("EDIT CANCELLED: file too large\n"); return; }
            for (int índiceBucle = 0; índiceBucle < valorEntrada; índiceBucle++) contenidoEditado[tamaño++] = línea[índiceBucle];
            contenidoEditado[tamaño++] = 10;
        }
        ArchivosMemoria.iniciarRuta(longitudNombreEditar);
        for (int índiceBucle = 0; índiceBucle < longitudNombreEditar; índiceBucle++) ArchivosMemoria.byteRuta(índiceBucle, nombreEditar[índiceBucle]);
        int Archivo = ArchivosMemoria.abrir(577); if (Archivo < 0) { error(Archivo); return; }
        for (int índiceBucle = 0; índiceBucle < tamaño; índiceBucle++) ArchivosMemoria.escribir(Archivo, contenidoEditado[índiceBucle]);
        ArchivosMemoria.cerrar(Archivo); EntradaSalidaTerminal.escribir("SAVED "); EntradaSalidaTerminal.númeroValor(tamaño); EntradaSalidaTerminal.escribir("valorByte(주기억 Archivo)\n");
    }
    static int valorHexadecimal(int valor) {
        if (valor >= '0' && valor <= '9') return valor - '0';
        if (valor >= 'a' && valor <= 'f') return valor - 'a' + 10;
        if (valor >= 'A' && valor <= 'F') return valor - 'A' + 10;
        return -1;
    }
    static void entradaSalidaBinario(boolean ponerValor) {
        if (númeroElementosTokenLéxico != 2) { EntradaSalidaTerminal.escribir("사용법: load Archivo | hex Archivo\n"); return; }
        int resultado = ruta(1); if (resultado < 0) { error(resultado); return; }
        if (!ponerValor) {
            int Archivo = ArchivosMemoria.abrir(0); if (Archivo < 0) { error(Archivo); return; }
            EntradaSalidaTerminal.escribir("HEX BEGIN "); EntradaSalidaTerminal.númeroValor(ArchivosMemoria.tamaño(Archivo)); EntradaSalidaTerminal.Caracteres(10);
            int númeroElementosEntradaElemento = 0;
            while (true) {
                int valor = ArchivosMemoria.leer(Archivo); if (valor < 0 || valor == 256) break;
                EntradaSalidaTerminal.Caracteres("0123456789abcdef".charAt(valor >> 4)); EntradaSalidaTerminal.Caracteres("0123456789abcdef".charAt(valor & 15));
                if (++númeroElementosEntradaElemento % 32 == 0) EntradaSalidaTerminal.Caracteres(10);
            }
            if (númeroElementosEntradaElemento % 32 != 0) EntradaSalidaTerminal.Caracteres(10);
            ArchivosMemoria.cerrar(Archivo); EntradaSalidaTerminal.escribir("HEX END\n"); return;
        }
        longitudNombreEditar = longitud[1];
        for (int índiceBucle = 0; índiceBucle < longitudNombreEditar; índiceBucle++) nombreEditar[índiceBucle] = valorTokenLéxico[puntoInicial[1] + índiceBucle];
        EntradaSalidaTerminal.escribir("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int tamaño = 0;
        while (true) {
            EntradaSalidaTerminal.escribir("hex> "); int valorEntrada = leerLíneaEntrada();
            if (valorEntrada < 0) { EntradaSalidaTerminal.escribir("LOAD CANCELLED\n"); return; }
            if (valorEntrada == 1 && línea[0] == '.') break;
            int valorLadoDelantero = -1;
            for (int índiceBucle = 0; índiceBucle < valorEntrada; índiceBucle++) {
                if (línea[índiceBucle] == 32 || línea[índiceBucle] == 9) continue;
                int valor = valorHexadecimal(línea[índiceBucle]);
                if (valor < 0 || tamaño >= contenidoEditado.length) { EntradaSalidaTerminal.escribir("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (valorLadoDelantero < 0) valorLadoDelantero = valor; else { contenidoEditado[tamaño++] = valorLadoDelantero * 16 + valor; valorLadoDelantero = -1; }
            }
            if (valorLadoDelantero >= 0) { EntradaSalidaTerminal.escribir("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        ArchivosMemoria.iniciarRuta(longitudNombreEditar);
        for (int índiceBucle = 0; índiceBucle < longitudNombreEditar; índiceBucle++) ArchivosMemoria.byteRuta(índiceBucle, nombreEditar[índiceBucle]);
        int Archivo = ArchivosMemoria.abrir(577); if (Archivo < 0) { error(Archivo); return; }
        for (int índiceBucle = 0; índiceBucle < tamaño; índiceBucle++) ArchivosMemoria.escribir(Archivo, contenidoEditado[índiceBucle]);
        ArchivosMemoria.cerrar(Archivo); EntradaSalidaTerminal.escribir("LOADED "); EntradaSalidaTerminal.númeroValor(tamaño); EntradaSalidaTerminal.escribir("valorByte(주기억 Archivo)\n");
    }
    static int Herramientas(int número) {
        return EntradaElementoHerramienta(número, 1);
    }
    static int EntradaElementoHerramienta(int número, int ponerEnMarcha) {
        if (númeroElementosTokenLéxico - ponerEnMarcha > 8) return -22;
        Placa.prepararArgumentos(númeroElementosTokenLéxico - ponerEnMarcha);
        for (int datosPrimero = ponerEnMarcha; datosPrimero < númeroElementosTokenLéxico; datosPrimero++) {
            if (longitud[datosPrimero] > 255) return -36;
            for (int índiceBucle = 0; índiceBucle < longitud[datosPrimero]; índiceBucle++) Placa.byteArgumento(datosPrimero - ponerEnMarcha, índiceBucle, valorTokenLéxico[puntoInicial[datosPrimero] + índiceBucle]);
        }
        return número == -2 ? Placa.ejecutarArchivoLinux() : número < 0 ? Placa.ejecutarArchivoUsuario() : Placa.ponerEnMarchaProgramaUsuario(número);
    }
    static int PaquetePython() {
        if (númeroElementosTokenLéxico > 8) return -22;
        Placa.prepararArgumentos(númeroElementosTokenLéxico);
        String ruta = "/lib/Paquete.py";
        // Escribir una cadena Java en el búfer de argumentos UTF-8 del intérprete.
        int índicePosición = 0;
        for (int índiceOrdinal = 0; índiceOrdinal < ruta.length(); índiceOrdinal++) {
            int valorCarácter = ruta.charAt(índiceOrdinal);
            if (valorCarácter < 128) Placa.byteArgumento(0, índicePosición++, valorCarácter);
            else { Placa.byteArgumento(0, índicePosición++, 0xe0 | (valorCarácter >> 12)); Placa.byteArgumento(0, índicePosición++, 0x80 | ((valorCarácter >> 6) & 63)); Placa.byteArgumento(0, índicePosición++, 0x80 | (valorCarácter & 63)); }
        }
        for (int índiceOrdinal = 1; índiceOrdinal < númeroElementosTokenLéxico; índiceOrdinal++) {
            if (longitud[índiceOrdinal] > 255) return -36;
            for (int valorCarácter = 0; valorCarácter < longitud[índiceOrdinal]; valorCarácter++) Placa.byteArgumento(índiceOrdinal, valorCarácter, valorTokenLéxico[puntoInicial[índiceOrdinal] + valorCarácter]);
        }
        return Placa.ponerEnMarchaProgramaUsuario(12);
    }
    static int formatoEjecución() {
        int valorProcesado = ruta(0); if (valorProcesado < 0) return valorProcesado;
        int Archivo = ArchivosMemoria.abrir(0); if (Archivo < 0) return Archivo;
        int datosPrimero = ArchivosMemoria.leer(Archivo), datosByte = ArchivosMemoria.leer(Archivo), códigoCarácter = ArchivosMemoria.leer(Archivo), valorPosiciónFinal = ArchivosMemoria.leer(Archivo);
        ArchivosMemoria.cerrar(Archivo);
        if (datosPrimero == 127 && datosByte == 'E' && códigoCarácter == 'L' && valorPosiciónFinal == 'F') return 1;
        if (datosPrimero == 'P' && datosByte == 'K' && códigoCarácter == 3 && valorPosiciónFinal == 4) return 2;
        return 0;
    }
    static int ponerEnMarchaEjemplo(int número, String argumentos) {
        Placa.prepararArgumentos(1);
        for (int índiceBucle = 0; índiceBucle < argumentos.length(); índiceBucle++) Placa.byteArgumento(0, índiceBucle, argumentos.charAt(índiceBucle));
        return Placa.ponerEnMarchaProgramaUsuario(número);
    }
    static void byteTexto(int Archivo, int valor) { ArchivosMemoria.escribir(Archivo, valor); }
    static void archivoEstático(String nombre, String valorContenidoValor) {
        // Los nombres de archivo del paquete usan ASCII; el contenido se guarda como UTF-8.
        ArchivosMemoria.iniciarRuta(nombre.length());
        for (int índiceBucle = 0; índiceBucle < nombre.length(); índiceBucle++) ArchivosMemoria.byteRuta(índiceBucle, nombre.charAt(índiceBucle));
        int Archivo = ArchivosMemoria.abrir(193); if (Archivo < 0) return;
        for (int índiceBucle = 0; índiceBucle < valorContenidoValor.length(); índiceBucle++) {
            int códigoCarácter = valorContenidoValor.charAt(índiceBucle);
            if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdbff && índiceBucle + 1 < valorContenidoValor.length()) códigoCarácter = 0x10000 + ((códigoCarácter - 0xd800) << 10) + valorContenidoValor.charAt(++índiceBucle) - 0xdc00;
            if (códigoCarácter < 128) byteTexto(Archivo, códigoCarácter);
            else {
                int númeroValor = códigoCarácter < 2048 ? 2 : códigoCarácter < 65536 ? 3 : 4;
                byteTexto(Archivo, (númeroValor == 2 ? 0xc0 : númeroValor == 3 ? 0xe0 : 0xf0) | (códigoCarácter >> (6 * (númeroValor - 1))));
                for (int númeroElementosEntradaElemento = númeroValor - 1; númeroElementosEntradaElemento > 0; númeroElementosEntradaElemento--) byteTexto(Archivo, 0x80 | ((códigoCarácter >> (6 * (númeroElementosEntradaElemento - 1))) & 63));
            }
        }
        ArchivosMemoria.cerrar(Archivo);
    }
    static void ayudaHangul() {
        EntradaSalidaTerminal.escribir("F9 o Shift+Space activa la escritura en español.\n");
        EntradaSalidaTerminal.escribir("  [ES] keyboard; [EN] ASCII\n");
        EntradaSalidaTerminal.escribir("  # → ·\n");
        EntradaSalidaTerminal.escribir("  F9: EN ↔ Español | Ctrl+Shift+V: UTF-8\n");
        EntradaSalidaTerminal.escribir("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        EntradaSalidaTerminal.escribir("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int rutaEjemplo(String nombre) {
        int númeroElementosByte = 0;
        for (int índiceBucle = 0; índiceBucle < nombre.length(); índiceBucle++) { int códigoCarácter = nombre.charAt(índiceBucle); if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdfff) return -22; númeroElementosByte += códigoCarácter < 128 ? 1 : códigoCarácter < 2048 ? 2 : 3; }
        int valorProcesado = ArchivosMemoria.iniciarRuta(númeroElementosByte); if (valorProcesado < 0) return valorProcesado;
        int índicePosición = 0;
        for (int índiceBucle = 0; índiceBucle < nombre.length(); índiceBucle++) {
            int códigoCarácter = nombre.charAt(índiceBucle);
            if (códigoCarácter < 128) ArchivosMemoria.byteRuta(índicePosición++, códigoCarácter);
            else if (códigoCarácter < 2048) { ArchivosMemoria.byteRuta(índicePosición++, 0xc0 | (códigoCarácter >> 6)); ArchivosMemoria.byteRuta(índicePosición++, 0x80 | (códigoCarácter & 63)); }
            else { ArchivosMemoria.byteRuta(índicePosición++, 0xe0 | (códigoCarácter >> 12)); ArchivosMemoria.byteRuta(índicePosición++, 0x80 | ((códigoCarácter >> 6) & 63)); ArchivosMemoria.byteRuta(índicePosición++, 0x80 | (códigoCarácter & 63)); }
        }
        return 0;
    }
    static int directorioEjemplo(String nombre) {
        int valorProcesado = rutaEjemplo(nombre); if (valorProcesado < 0) return valorProcesado;
        valorProcesado = ArchivosMemoria.crearDirectorio(); return valorProcesado == -17 ? 0 : valorProcesado;
    }
    static int archivoEjemplo(String nombre, String Datos) {
        int valorProcesado = rutaEjemplo(nombre); if (valorProcesado < 0) return valorProcesado;
        int Archivo = ArchivosMemoria.abrir(193); if (Archivo == -17) return 0; if (Archivo < 0) return Archivo;
        for (int índiceBucle = 0; índiceBucle < Datos.length(); índiceBucle += 2) {
            valorProcesado = ArchivosMemoria.escribir(Archivo, valorHexadecimal(Datos.charAt(índiceBucle)) * 16 + valorHexadecimal(Datos.charAt(índiceBucle + 1)));
            if (valorProcesado < 0) { ArchivosMemoria.cerrar(Archivo); return valorProcesado; }
        }
        return ArchivosMemoria.cerrar(Archivo);
    }
    static void mostrarAyuda() {
        herramientaSistema.mostrarAyuda();
        EntradaSalidaTerminal.escribir("sshd / intérpreteComandosAsegurar start|stop|status: SSH :22 (user, 장치별 valorContraseña)\n");
        EntradaSalidaTerminal.escribir("vncd / PresentarRemoto start|stop|status: VNC :5900 (장치별 valorContraseña)\n");
        EntradaSalidaTerminal.escribir("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        EntradaSalidaTerminal.escribir("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        EntradaSalidaTerminal.escribir("wc grep head tail tee env export unset history sh source true false exit\n");
        EntradaSalidaTerminal.escribir("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        EntradaSalidaTerminal.escribir("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        EntradaSalidaTerminal.escribir("valorEsquina + ladoIzquierdo 버튼 valorArrastrar: terminal tamaño cambiarValor; terminal size: valorColumna/valorFila\n");
        EntradaSalidaTerminal.escribir("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        EntradaSalidaTerminal.escribir("vi FILE: i to insert; Esc then :wq to save and quit\n");
        EntradaSalidaTerminal.escribir("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        EntradaSalidaTerminal.escribir("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        EntradaSalidaTerminal.escribir("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        EntradaSalidaTerminal.escribir("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        EntradaSalidaTerminal.escribir("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        EntradaSalidaTerminal.escribir("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        EntradaSalidaTerminal.escribir("python FILE.py | python -c 'CODE' (MicroPython)\n");
        EntradaSalidaTerminal.escribir("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        EntradaSalidaTerminal.escribir("pip: MicroPython árbolFuente instalarValor; Anfitrión --network --pip valorNecesario; /lib는 RAM\n");
        EntradaSalidaTerminal.escribir("gui | run cpp | net test | tasks | selftest | samples\n");
        EntradaSalidaTerminal.escribir("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        EntradaSalidaTerminal.escribir("/example/java /example/c /example/python: examples ready at boot\n");
        EntradaSalidaTerminal.escribir("example java|c|python: restore missing examples (keeps existing files)\n");
        ayudaHangul();
    }
    static void terminal(boolean conmutadoEra) {
        if (conmutadoEra && Placa.terminal(2) != 0) { Placa.terminal(0); EntradaSalidaTerminal.escribir("TERMINAL CLOSED\n"); }
        else if (Placa.terminal(1) < 0) error(-19);
        else EntradaSalidaTerminal.escribir("TERMINAL READY — Español terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void comando() {
        if (númeroElementosTokenLéxico == 0) return;
        if (herramientaSistema.ejecutarComando()) return;
        if (textoIgual(0,"sshd") || textoIgual(0,"intérpreteComandosAsegurar") || textoIgual(0,"vncd") || textoIgual(0,"PresentarRemoto")) {
            int valorClaseTipo=textoIgual(0,"vncd")||textoIgual(0,"PresentarRemoto")?1:0;
            int acción=textoIgual(1,"start")||textoIgual(1,"ponerEnMarcha")?1:textoIgual(1,"stop")||textoIgual(1,"detener")?0:2;
            int valorEstadoValor=Placa.controlRemoto(valorClaseTipo,acción);
            if(valorEstadoValor<0)error(valorEstadoValor);else EntradaSalidaTerminal.escribir(Placa.controlRemoto(valorClaseTipo,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (textoIgual(0, "help") || textoIgual(0, "h")) { if (textoIgual(1, "ko") || textoIgual(1, "input")) ayudaHangul(); else mostrarAyuda(); }
        else if (textoIgual(0, "info") || textoIgual(0, "i")) Núcleo.informaciónSistema();
        else if (textoIgual(0, "pwd")) { ArchivosMemoria.escribirActual(); EntradaSalidaTerminal.Caracteres(10); }
        else if (textoIgual(0, "cd")) {
            int valorProcesado;
            if (númeroElementosTokenLéxico == 1) { ArchivosMemoria.iniciarRuta(1); valorProcesado = ArchivosMemoria.byteRuta(0, '/'); } else valorProcesado = númeroElementosTokenLéxico == 2 ? ruta(1) : -22;
            if (valorProcesado >= 0) valorProcesado = ArchivosMemoria.cambiarDirectorio(); if (valorProcesado < 0) error(valorProcesado);
        }
        else if (textoIgual(0, "ls") || textoIgual(0, "f")) {
            int índiceArgumento = textoIgual(1, "-l") ? 2 : 1, valorProcesado;
            if (númeroElementosTokenLéxico == índiceArgumento) { ArchivosMemoria.iniciarRuta(1); valorProcesado = ArchivosMemoria.byteRuta(0, '.'); } else valorProcesado = númeroElementosTokenLéxico == índiceArgumento + 1 ? ruta(índiceArgumento) : -22;
            if (valorProcesado >= 0) valorProcesado = ArchivosMemoria.entradasRuta(); if (valorProcesado < 0) error(valorProcesado);
        }
        else if (textoIgual(0, "mkdir") || textoIgual(0, "rmdir") || textoIgual(0, "touch")) HerramientasIntérpreteComandos.trabajoUnidadArchivo(textoIgual(0, "mkdir") ? "mkdir" : textoIgual(0, "rmdir") ? "rmdir" : "touch");
        else if (textoIgual(0, "cp") || textoIgual(0, "mv")) HerramientasIntérpreteComandos.copiarValor(textoIgual(0, "mv"));
        else if (textoIgual(0, "cat")) HerramientasIntérpreteComandos.valorVista();
        else if (textoIgual(0, "wc")) HerramientasIntérpreteComandos.valorConteoEnCurso();
        else if (textoIgual(0, "grep")) HerramientasIntérpreteComandos.encontrarEntradaElemento();
        else if (textoIgual(0, "head") || textoIgual(0, "tail")) HerramientasIntérpreteComandos.valorCabecera(textoIgual(0, "tail"));
        else if (textoIgual(0, "tee")) HerramientasIntérpreteComandos.escribirJuntos();
        else if (textoIgual(0, "env")) SintaxisIntérpreteComandos.mostrarEntorno();
        else if (textoIgual(0, "export") || textoIgual(0, "unset")) {
            if (númeroElementosTokenLéxico == 1) SintaxisIntérpreteComandos.mostrarEntorno();
            for (int índiceBucle = 1; índiceBucle < númeroElementosTokenLéxico; índiceBucle++) { int valorProcesado = SintaxisIntérpreteComandos.ajustesEntorno(índiceBucle, textoIgual(0, "unset")); if (valorProcesado != 0) { resultado = valorProcesado; EntradaSalidaTerminal.escribir("comando analizarValor: valorVariable 이름이 잘못되었거나 예약된 이름이거나 entorno 공간이 가득 찼습니다\n"); } }
        }
        else if (textoIgual(0, "sh") || textoIgual(0, "source")) SintaxisIntérpreteComandos.ejecutarArchivo();
        else if (textoIgual(0, "true")) resultado = 0;
        else if (textoIgual(0, "false")) resultado = 1;
        else if (textoIgual(0, "history")) EditorLínea.mostrarDiario();
        else if (textoIgual(0, "exit")) {
            if (SintaxisIntérpreteComandos.valorProfundidad > 0) { resultado = númeroElementosTokenLéxico == 1 ? SintaxisIntérpreteComandos.valorEstadoValor : HerramientasIntérpreteComandos.valorDígito(1); if (resultado < 0 || resultado > 255) resultado = 2; SintaxisIntérpreteComandos.finGuion = true; }
            else if (Placa.terminal(2) != 0) terminal(true);
            else EntradaSalidaTerminal.escribir("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (textoIgual(0, "edit")) valorEditar();
        else if (textoIgual(0, "load") || textoIgual(0, "hex")) entradaSalidaBinario(textoIgual(0, "load"));
        else if (textoIgual(0, "rm")) {
            if (númeroElementosTokenLéxico < 2) { resultado = 2; EntradaSalidaTerminal.escribir("사용법: rm Archivo...\n"); }
            for (int índiceBucle = 1; índiceBucle < númeroElementosTokenLéxico; índiceBucle++) { int valorProcesado = ruta(índiceBucle); if (valorProcesado == 0) valorProcesado = ArchivosMemoria.borrarEntradaElemento(); if (valorProcesado < 0) error(valorProcesado); }
        }
        else if (textoIgual(0, "echo")) {
            int iniciarPosición = textoIgual(1, "-n") ? 2 : 1;
            for (int datosPrimero = iniciarPosición; datosPrimero < númeroElementosTokenLéxico; datosPrimero++) { if (datosPrimero > iniciarPosición) EntradaSalidaTerminal.Caracteres(32); for (int índiceBucle = 0; índiceBucle < longitud[datosPrimero]; índiceBucle++) Placa.escribirSerie(valorTokenLéxico[puntoInicial[datosPrimero] + índiceBucle]); }
            if (iniciarPosición == 1) EntradaSalidaTerminal.Caracteres(10);
        }
        else if (textoIgual(0, "clear")) EntradaSalidaTerminal.escribir("\u001b[2J\u001b[H");
        else if (textoIgual(0, "javac") || textoIgual(0, "java") || textoIgual(0, "python") || textoIgual(0, "pip")) {
            int valorProcesado = textoIgual(0, "pip") ? PaquetePython() : Herramientas(textoIgual(0, "javac") ? 10 : textoIgual(0, "java") ? 11 : 12); resultado = valorProcesado == -1005 ? -1005 : valorProcesado < 0 ? 126 : valorProcesado;
            if (valorProcesado != -1005 && !SintaxisIntérpreteComandos.esConexiónEnCurso) { EntradaSalidaTerminal.escribir("exit "); EntradaSalidaTerminal.númeroValor(valorProcesado); EntradaSalidaTerminal.Caracteres(10); }
        }
        else if (textoIgual(0, "vi")) { int valorProcesado = Herramientas(13); resultado = valorProcesado == -1005 ? -1005 : valorProcesado < 0 ? 126 : valorProcesado; }
        else if (textoIgual(0, "cc") || textoIgual(0, "tcc")) { int valorProcesado = Herramientas(15); resultado = valorProcesado < 0 ? 126 : valorProcesado; if (!SintaxisIntérpreteComandos.esConexiónEnCurso) { EntradaSalidaTerminal.escribir("exit "); EntradaSalidaTerminal.númeroValor(valorProcesado); EntradaSalidaTerminal.Caracteres(10); } }
        else if (textoIgual(0, "jaot")) { int valorProcesado = Herramientas(16); resultado = valorProcesado < 0 ? 126 : valorProcesado; if (!SintaxisIntérpreteComandos.esConexiónEnCurso) { EntradaSalidaTerminal.escribir("exit "); EntradaSalidaTerminal.númeroValor(valorProcesado); EntradaSalidaTerminal.Caracteres(10); } }
        else if (textoIgual(0, "terminal")) {
            if (textoIgual(1, "size")) { int tamaño = Placa.terminal(13); EntradaSalidaTerminal.escribir("TERMINAL SIZE "); EntradaSalidaTerminal.númeroValor(tamaño & 65535); EntradaSalidaTerminal.Caracteres('x'); EntradaSalidaTerminal.númeroValor(tamaño >>> 16); EntradaSalidaTerminal.Caracteres(10); }
            else terminal(false);
        }
        else if (textoIgual(0, "gui") || textoIgual(0, "v")) { Placa.terminal(9); Escritorio.ejecutarComando(); }
        else if (textoIgual(0, "c")) Núcleo.pruebaC();
        else if (textoIgual(0, "tasks") || textoIgual(0, "t")) Núcleo.pruebaTareas();
        else if (textoIgual(0, "g")) Núcleo.Pantalla();
        else if (textoIgual(0, "selftest") || textoIgual(0, "u")) Núcleo.pruebaProgramasUsuario();
        else if (textoIgual(0, "e") || (textoIgual(0, "run") && textoIgual(1, "cpp"))) {
            int valorProcesado = Placa.ponerEnMarchaProgramaUsuario(0); if (valorProcesado == 0) EntradaSalidaTerminal.escribir("ELF DEMO PASS\n"); else error(valorProcesado);
        }
        else if (textoIgual(0, "run")) { int valorProcesado = textoIgual(1, "--linux") ? EntradaElementoHerramienta(-2, 2) : Herramientas(-1); resultado = valorProcesado == -1005 ? -1005 : valorProcesado < 0 ? 126 : valorProcesado; if (valorProcesado != -1005 && !SintaxisIntérpreteComandos.esConexiónEnCurso) { EntradaSalidaTerminal.escribir("exit "); EntradaSalidaTerminal.númeroValor(valorProcesado); EntradaSalidaTerminal.Caracteres(10); } }
        else if (textoIgual(0, "n") || (textoIgual(0, "net") && textoIgual(1, "test"))) Núcleo.pruebaConexiónRed();
        else if (textoIgual(0, "ftpd")) {
            if (textoIgual(1, "start")) { int valorProcesado = Placa.servicioTransferenciaArchivo(1); if (valorProcesado < 0) error(valorProcesado); else { EntradaSalidaTerminal.escribir("FTP listening "); herramientaSistema.escribirDirección(Placa.estadoRed(0,0)); EntradaSalidaTerminal.escribir(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (textoIgual(1, "stop")) { Placa.servicioTransferenciaArchivo(0); EntradaSalidaTerminal.escribir("FTP stopped\n"); }
            else EntradaSalidaTerminal.escribir(Placa.servicioTransferenciaArchivo(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (textoIgual(0, "samples")) { Paquete.preparar(); EntradaSalidaTerminal.escribir("SAMPLES READY (existing files kept)\n"); }
        else if (textoIgual(0, "example")) {
            int Lengua = textoIgual(1, "java") ? 0 : textoIgual(1, "c") ? 1 : textoIgual(1, "python") ? 2 : -1;
            if (númeroElementosTokenLéxico != 2 || Lengua < 0) EntradaSalidaTerminal.escribir("example java|c|python: Salida, Archivo, 네트워크, 그래픽, Java Swing ventana Ejemplos\n");
            else { int valorProcesado = PaqueteEjemplo.instalarValor(Lengua); if (valorProcesado < 0) { error(valorProcesado); if (valorProcesado == -28) EntradaSalidaTerminal.escribir("RAM full: remove unused files, then retry example\n"); } else EntradaSalidaTerminal.escribir("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int valorFormato = formatoEjecución();
            if (valorFormato == 1 || valorFormato == 2) {
                int valorProcesado = EntradaElementoHerramienta(valorFormato == 1 ? -1 : 14, 0); resultado = valorProcesado == -1005 ? -1005 : valorProcesado < 0 ? 126 : valorProcesado;
                if (valorProcesado != -1005 && !SintaxisIntérpreteComandos.esConexiónEnCurso) { EntradaSalidaTerminal.escribir("exit "); EntradaSalidaTerminal.númeroValor(valorProcesado); EntradaSalidaTerminal.Caracteres(10); }
            } else if (valorFormato == 0) { resultado = 126; EntradaSalidaTerminal.escribir("실행할 númeroValor 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { resultado = 127; EntradaSalidaTerminal.escribir("Unknown command. help: commands\n"); }
        }
    }
    public static void ejecutarComando() {
        Paquete.preparar();
        for (int Lengua = 0; Lengua < 3; Lengua++) { int valorProcesado = PaqueteEjemplo.instalarValor(Lengua); if (valorProcesado < 0) error(valorProcesado); }
        mostrarAyuda();
        while (true) {
            sesiónVentana.entradaElementoValorProceso(); if (sesiónVentana.ejecuciónReanudar()) continue;
            if (!sesiónVentana.leerContinuación) EntradaSalidaTerminal.escribir("jkoros-native> "); EditorLínea.líneaComando = true; Placa.esperarRemoto(1); int tamaño = leerLíneaEntrada(); Placa.esperarRemoto(0); EditorLínea.líneaComando = false;
            if (tamaño == -3) continue;
            if (tamaño == -2) EntradaSalidaTerminal.escribir("comando analizarValor: 명령줄이 너무 깁니다\n");
            if (tamaño >= 0) { SintaxisIntérpreteComandos.finGuion = false; SintaxisIntérpreteComandos.ejecutarComando(línea, 0, tamaño, 0); } else SintaxisIntérpreteComandos.valorEstadoValor = 130;
            Placa.comandoRemotoFin(SintaxisIntérpreteComandos.valorEstadoValor);
            EditorLínea.tamaño = EditorLínea.valorCursor = EditorLínea.iniciarVentana = 0;
        }
    }
}
