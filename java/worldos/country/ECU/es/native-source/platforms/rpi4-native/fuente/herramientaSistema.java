// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Órdenes de gestión de IPv4, ICMP, tareas, memoria y almacenamiento RAM que leen el estado real del núcleo. */
public final class herramientaSistema {
    static int valorDirección;
    static boolean textoIgual(int número, String textoPalabra) { return IntérpreteComandos.textoIgual(número, textoPalabra); }
    static int númeroElementosElementoLista() { return IntérpreteComandos.númeroElementosTokenLéxico; }
    static void valorFallo(String Guía) { IntérpreteComandos.resultado=2; EntradaSalidaTerminal.escribir(Guía); EntradaSalidaTerminal.Caracteres(10); }
    static void error(int valor) { IntérpreteComandos.error(valor); }
    static void entradaElementoNúmero(String nombre, int valor) { EntradaSalidaTerminal.escribir(nombre); EntradaSalidaTerminal.númeroValor(valor); EntradaSalidaTerminal.Caracteres(10); }
    static int valorDígito(int número, int límiteCapacidad) {
        if (número>=númeroElementosElementoLista() || IntérpreteComandos.longitud[número]==0) return -1;
        int valor=0;
        for (int índiceOrdinal=0; índiceOrdinal<IntérpreteComandos.longitud[número]; índiceOrdinal++) {
            int valorCarácter=IntérpreteComandos.valorTokenLéxico[IntérpreteComandos.puntoInicial[número]+índiceOrdinal]-'0';
            if (valorCarácter<0 || valorCarácter>9 || valor>(límiteCapacidad-valorCarácter)/10) return -1;
            valor=valor*10+valorCarácter;
        }
        return valor<=límiteCapacidad?valor:-1;
    }
    static boolean leerDirección(int número) {
        if (número>=númeroElementosElementoLista()) return false;
        int valor=0, valorFragmentoBloque=0, númeroElementosDígito=0, númeroElementosPunto=0;
        for (int índiceOrdinal=0; índiceOrdinal<IntérpreteComandos.longitud[número]; índiceOrdinal++) {
            int valorCarácter=IntérpreteComandos.valorTokenLéxico[IntérpreteComandos.puntoInicial[número]+índiceOrdinal];
            if (valorCarácter=='.') { if (númeroElementosDígito==0 || ++númeroElementosPunto>3) return false; valor=(valor<<8)|valorFragmentoBloque; valorFragmentoBloque=númeroElementosDígito=0; }
            else { if (valorCarácter<'0' || valorCarácter>'9' || ++númeroElementosDígito>3) return false; valorFragmentoBloque=valorFragmentoBloque*10+valorCarácter-'0'; if(valorFragmentoBloque>255)return false; }
        }
        if (númeroElementosPunto!=3 || númeroElementosDígito==0) return false;
        valorDirección=(valor<<8)|valorFragmentoBloque; return true;
    }
    static void escribirDirección(int valor) {
        EntradaSalidaTerminal.númeroValor((valor>>>24)&255); EntradaSalidaTerminal.Caracteres('.'); EntradaSalidaTerminal.númeroValor((valor>>>16)&255); EntradaSalidaTerminal.Caracteres('.');
        EntradaSalidaTerminal.númeroValor((valor>>>8)&255); EntradaSalidaTerminal.Caracteres('.'); EntradaSalidaTerminal.númeroValor(valor&255);
    }
    static void mostrarEstadoRed() {
        EntradaSalidaTerminal.escribir(Placa.estadoRed(20,0)!=0?"en0: ":"sl0: "); EntradaSalidaTerminal.escribir(Placa.estadoRed(3,0)!=0?"UP":"DOWN");
        EntradaSalidaTerminal.escribir(Placa.estadoRed(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        EntradaSalidaTerminal.escribir(Placa.estadoRed(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); escribirDirección(Placa.estadoRed(0,0));
        EntradaSalidaTerminal.escribir(" netmask "); escribirDirección(Placa.estadoRed(1,0)); EntradaSalidaTerminal.escribir(" gateway "); escribirDirección(Placa.estadoRed(2,0)); EntradaSalidaTerminal.Caracteres(10);
        EntradaSalidaTerminal.escribir("  RX packets "); EntradaSalidaTerminal.númeroValor(Placa.estadoRed(4,0)); EntradaSalidaTerminal.escribir(" bytes "); EntradaSalidaTerminal.númeroValor(Placa.estadoRed(6,0));
        EntradaSalidaTerminal.escribir(" TX packets "); EntradaSalidaTerminal.númeroValor(Placa.estadoRed(5,0)); EntradaSalidaTerminal.escribir(" bytes "); EntradaSalidaTerminal.númeroValor(Placa.estadoRed(7,0)); EntradaSalidaTerminal.Caracteres(10);
        entradaElementoNúmero("  dropped ",Placa.estadoRed(8,0));
    }
    static void establecerDirección(int ponerEnMarcha) {
        if (númeroElementosElementoLista()!=ponerEnMarcha+3 || !leerDirección(ponerEnMarcha)) { valorFallo("사용법: ipconfig set dirección 주소가림 valorPasarela"); return; }
        int dirección=valorDirección;
        if(!leerDirección(ponerEnMarcha+1)){valorFallo("Invalid IPv4 netmask");return;} int valorMáscara=valorDirección;
        if(!leerDirección(ponerEnMarcha+2)){valorFallo("Invalid IPv4 gateway");return;}
        int resultado=Placa.ajustesRed(0,dirección,valorMáscara,valorDirección);
        if(resultado<0) { error(resultado); if(resultado==-16)EntradaSalidaTerminal.escribir("Close sockets and stop ftpd before changing address.\n"); }
        else { EntradaSalidaTerminal.escribir("IPv4 configuration applied (until reboot)\n"); mostrarEstadoRed(); }
    }
    static void comandoRed(boolean direcciónIP) {
        if (númeroElementosElementoLista()==1 || númeroElementosElementoLista()==2 && (textoIgual(1,"show") || textoIgual(1,"addr") || textoIgual(1,"address") || textoIgual(1,"sl0") || textoIgual(1,"en0")) || númeroElementosElementoLista()==3 && (textoIgual(1,"addr") || textoIgual(1,"address")) && textoIgual(2,"show")) { mostrarEstadoRed();return; }
        if (direcciónIP && textoIgual(1,"route") && (númeroElementosElementoLista()==2 || númeroElementosElementoLista()==3&&textoIgual(2,"show"))) { mostrarRuta();return; }
        if (textoIgual(1,"set")) { establecerDirección(2);return; }
        if (númeroElementosElementoLista()==2 && (textoIgual(1,"up") || textoIgual(1,"down"))) { Placa.ajustesRed(textoIgual(1,"up")?1:2,0,0,0);mostrarEstadoRed();return; }
        if (direcciónIP && númeroElementosElementoLista()==6 && textoIgual(1,"link") && textoIgual(2,"set") && textoIgual(3,"dev") && (textoIgual(4,"sl0")||textoIgual(4,"en0")) && (textoIgual(5,"up") || textoIgual(5,"down"))) { Placa.ajustesRed(textoIgual(5,"up")?1:2,0,0,0);mostrarEstadoRed();return; }
        valorFallo("사용법: ip [addr show|route show|set dirección 주소가림 valorPasarela|link set dev sl0 up|down]");
    }
    static void mostrarRuta() {
        EntradaSalidaTerminal.escribir("Destination Netmask Gateway Interface\n");
        escribirDirección(Placa.estadoRed(0,0)&Placa.estadoRed(1,0));EntradaSalidaTerminal.Caracteres(' ');escribirDirección(Placa.estadoRed(1,0));EntradaSalidaTerminal.escribir(Placa.estadoRed(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Placa.estadoRed(2,0)!=0) {EntradaSalidaTerminal.escribir("0.0.0.0 0.0.0.0 ");escribirDirección(Placa.estadoRed(2,0));EntradaSalidaTerminal.escribir(Placa.estadoRed(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void mostrarRed() {
        EntradaSalidaTerminal.escribir("Proto Local Remote State Queued\n");
        for(int número=0;número<32;número++) {
            int categoríaTipo=Placa.estadoRed(10,número);if(categoríaTipo==0)continue;
            EntradaSalidaTerminal.escribir(categoríaTipo==1?"TCP ":"UDP ");escribirDirección(Placa.estadoRed(16,número));EntradaSalidaTerminal.Caracteres(':');EntradaSalidaTerminal.númeroValor(Placa.estadoRed(11,número));EntradaSalidaTerminal.Caracteres(' ');
            escribirDirección(Placa.estadoRed(12,número));EntradaSalidaTerminal.Caracteres(':');EntradaSalidaTerminal.númeroValor(Placa.estadoRed(13,número));EntradaSalidaTerminal.Caracteres(' ');
            int valorEstadoValor=Placa.estadoRed(14,número);EntradaSalidaTerminal.escribir(categoríaTipo==2?"DATAGRAM":valorEstadoValor==1?"LISTEN":valorEstadoValor==2?"ESTABLISHED":valorEstadoValor==3?"CLOSE_WAIT":valorEstadoValor==4?"ERROR":"UNCONNECTED");
            EntradaSalidaTerminal.Caracteres(' ');EntradaSalidaTerminal.númeroValor(Placa.estadoRed(15,número));EntradaSalidaTerminal.Caracteres(10);
        }
        EntradaSalidaTerminal.escribir("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean esperarEstadoValor(int milisegundos) {
        int ponerEnMarcha=Placa.milisegundos();
        while(Placa.milisegundos()-ponerEnMarcha<milisegundos) {
            if(EntradaSalidaIntérpreteComandos.esInteractivo()!=0){int valorCarácter=Placa.leerSerie();if(valorCarácter==3 || valorCarácter=='q' || valorCarácter=='Q' || valorCarácter==27 || valorCarácter==-4096)return false;}
            Placa.cederProcesador();
        }
        return true;
    }
    static void pruebaRespuestaRetorno() {
        int númeroElementosRepetición=4, valorLímite=1000, valorObjetivo=-1;
        for(int índicePosición=1;índicePosición<númeroElementosElementoLista();índicePosición++) {
            if(textoIgual(índicePosición,"-c")){númeroElementosRepetición=valorDígito(++índicePosición,100);if(númeroElementosRepetición<1){valorFallo("ping: -c 1..100");return;}}
            else if(textoIgual(índicePosición,"-W")){valorLímite=valorDígito(++índicePosición,10);if(valorLímite<1){valorFallo("ping: -W 1..10 seconds");return;}valorLímite*=1000;}
            else if(valorObjetivo<0)valorObjetivo=índicePosición;else{valorFallo("사용법: ping [-c númeroElementosRepetición] [-W valorSegundos] IPv4");return;}
        }
        if(valorObjetivo<0 || !leerDirección(valorObjetivo)){valorFallo("ping: an IPv4 address is required (DNS is not configured)");return;}
        int dirección=valorDirección, númeroElementosEnviado=0, númeroElementosRecibido=0, valorAcumulado=0, límiteMínimo=100000, límiteMáximo=0;
        EntradaSalidaTerminal.escribir("PING ");escribirDirección(dirección);EntradaSalidaTerminal.escribir(" 32 ICMP bytes\n");
        boolean procesamientoContinuar=true;
        for(int valorOrden=1;valorOrden<=númeroElementosRepetición && procesamientoContinuar;valorOrden++) {
            int valorProcesado=Placa.enviarRespuestaRetorno(dirección,valorOrden);
            if(valorProcesado<0){error(valorProcesado);break;}númeroElementosEnviado++;
            int ponerEnMarcha=Placa.milisegundos();
            while(Placa.leerRespuestaRetorno(0)==-11 && Placa.milisegundos()-ponerEnMarcha<valorLímite)if(!esperarEstadoValor(1)){procesamientoContinuar=false;break;}
            if(!procesamientoContinuar)break;
            if(Placa.leerRespuestaRetorno(0)==0){
                int valorTiempo=Placa.leerRespuestaRetorno(1);númeroElementosRecibido++;valorAcumulado+=valorTiempo;if(valorTiempo<límiteMínimo)límiteMínimo=valorTiempo;if(valorTiempo>límiteMáximo)límiteMáximo=valorTiempo;
                EntradaSalidaTerminal.escribir("32 bytes from ");escribirDirección(dirección);EntradaSalidaTerminal.escribir(" seq=");EntradaSalidaTerminal.númeroValor(valorOrden);EntradaSalidaTerminal.escribir(" ttl=");EntradaSalidaTerminal.númeroValor(Placa.leerRespuestaRetorno(2));EntradaSalidaTerminal.escribir(" time=");EntradaSalidaTerminal.númeroValor(valorTiempo);EntradaSalidaTerminal.escribir(" ms\n");
            }else{EntradaSalidaTerminal.escribir("Request timeout seq=");EntradaSalidaTerminal.númeroValor(valorOrden);EntradaSalidaTerminal.Caracteres(10);}
            if(valorOrden<númeroElementosRepetición)procesamientoContinuar=esperarEstadoValor(200);
        }
        EntradaSalidaTerminal.númeroValor(númeroElementosEnviado);EntradaSalidaTerminal.escribir(" transmitted, ");EntradaSalidaTerminal.númeroValor(númeroElementosRecibido);EntradaSalidaTerminal.escribir(" received, ");EntradaSalidaTerminal.númeroValor(númeroElementosEnviado==0?100:(númeroElementosEnviado-númeroElementosRecibido)*100/númeroElementosEnviado);EntradaSalidaTerminal.escribir("% packet loss\n");
        if(númeroElementosRecibido>0){EntradaSalidaTerminal.escribir("rtt min/avg/max = ");EntradaSalidaTerminal.númeroValor(límiteMínimo);EntradaSalidaTerminal.Caracteres('/');EntradaSalidaTerminal.númeroValor(valorAcumulado/númeroElementosRecibido);EntradaSalidaTerminal.Caracteres('/');EntradaSalidaTerminal.númeroValor(límiteMáximo);EntradaSalidaTerminal.escribir(" ms\n");}
        IntérpreteComandos.resultado=procesamientoContinuar?(númeroElementosRecibido==0?1:0):130;
    }
    static void mostrarActividad() { EntradaSalidaTerminal.escribir("up ");EntradaSalidaTerminal.númeroValor(Placa.milisegundos()/1000);EntradaSalidaTerminal.escribir(" seconds\n"); }
    static void mostrarMemoria() {
        entradaElementoNúmero("ARM RAM KiB (firmware): ",Placa.sistemaConsultar(0,0));
        entradaElementoNúmero("Kernel image+BSS+stack KiB: ",Placa.sistemaConsultar(1,0));
        int capacidadTotal=Placa.sistemaConsultar(2,0), capacidadUsado=Placa.sistemaConsultar(3,0);
        EntradaSalidaTerminal.escribir("AOT heap KiB total/used/free: ");EntradaSalidaTerminal.númeroValor(capacidadTotal);EntradaSalidaTerminal.Caracteres('/');EntradaSalidaTerminal.númeroValor(capacidadUsado);EntradaSalidaTerminal.Caracteres('/');EntradaSalidaTerminal.númeroValor(capacidadTotal-capacidadUsado);EntradaSalidaTerminal.Caracteres(10);
        entradaElementoNúmero("Framebuffer KiB: ",Placa.sistemaConsultar(4,0));
        entradaElementoNúmero("EL0 arena+session reserve KiB: ",Placa.sistemaConsultar(5,0));
        int valorAsociado=0;for(int número=0;número<4;número++)valorAsociado+=Placa.sistemaConsultar(22,número);
        entradaElementoNúmero("EL0 mapped KiB: ",valorAsociado);
        EntradaSalidaTerminal.escribir("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void mostrarTareas() {
        EntradaSalidaTerminal.escribir("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        EntradaSalidaTerminal.escribir("1 - RUN - - ");EntradaSalidaTerminal.númeroValor(Placa.milisegundos());EntradaSalidaTerminal.escribir(" kernel/shell\n");
        for(int número=1;número<3;número++)if(Placa.estadoValorTarea(número)>0){EntradaSalidaTerminal.númeroValor(número+1);EntradaSalidaTerminal.escribir(" - READY 64 - - kernel-task\n");}
        for(int número=0;número<4;número++){
            int valorEstadoValor=Placa.sistemaConsultar(20,número);if(valorEstadoValor==0)continue;
            EntradaSalidaTerminal.númeroValor(Placa.sistemaConsultar(21,número));EntradaSalidaTerminal.Caracteres(' ');EntradaSalidaTerminal.númeroValor(número);EntradaSalidaTerminal.escribir(valorEstadoValor==1?" RUN ":" SUSPENDED ");
            EntradaSalidaTerminal.númeroValor(Placa.sistemaConsultar(22,número));EntradaSalidaTerminal.Caracteres(' ');EntradaSalidaTerminal.númeroValor(Placa.sistemaConsultar(24,número));EntradaSalidaTerminal.Caracteres(' ');EntradaSalidaTerminal.númeroValor(Placa.sistemaConsultar(23,número));EntradaSalidaTerminal.Caracteres(' ');
            for(int índicePosición=0;índicePosición<288;índicePosición++){int valorByte=Placa.sistemaConsultar(25,número+índicePosición*4);if(valorByte==0)break;Placa.escribirSerie(valorByte);}EntradaSalidaTerminal.Caracteres(10);
        }
    }
    static void mostrarAlmacenamiento() {
        int númeroElementosRanura=0, númeroElementosDatos=0;
        for(int número=0;número<ArchivosMemoria.númeroElementosArchivo;número++)if(ArchivosMemoria.longitudNombre[número]>0 || ArchivosMemoria.númeroElementosReferencia[número]>0){númeroElementosRanura++;númeroElementosDatos+=ArchivosMemoria.longitud[número];}
        EntradaSalidaTerminal.escribir("Filesystem Total Reserved Available Data Files Mount\nramfs ");EntradaSalidaTerminal.númeroValor(ArchivosMemoria.númeroElementosArchivo*16384);EntradaSalidaTerminal.Caracteres(' ');EntradaSalidaTerminal.númeroValor(númeroElementosRanura*16384);EntradaSalidaTerminal.Caracteres(' ');EntradaSalidaTerminal.númeroValor((ArchivosMemoria.númeroElementosArchivo-númeroElementosRanura)*16384);EntradaSalidaTerminal.Caracteres(' ');EntradaSalidaTerminal.númeroValor(númeroElementosDatos);EntradaSalidaTerminal.Caracteres(' ');EntradaSalidaTerminal.númeroValor(númeroElementosRanura);EntradaSalidaTerminal.Caracteres('/');EntradaSalidaTerminal.númeroValor(ArchivosMemoria.númeroElementosArchivo);EntradaSalidaTerminal.escribir(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void mostrarEstado() {
        int númeroElementosRepetición=EntradaSalidaIntérpreteComandos.esInteractivo()!=0?0:1;
        if(númeroElementosElementoLista()>1){if(númeroElementosElementoLista()!=3 || !textoIgual(1,"-n") || (númeroElementosRepetición=valorDígito(2,1000))<1){valorFallo("사용법: top [-n 1..1000]; q/Ctrl+C로 programaTerminarSesión");return;}}
        for(int valorSecuencia=0;númeroElementosRepetición==0 || valorSecuencia<númeroElementosRepetición;valorSecuencia++){
            if(EntradaSalidaIntérpreteComandos.esInteractivo()!=0 && númeroElementosRepetición==0)EntradaSalidaTerminal.escribir("\u001b[2J\u001b[H");
            mostrarActividad();mostrarMemoria();mostrarTareas();
            if(númeroElementosRepetición!=0 && valorSecuencia+1>=númeroElementosRepetición)break;
            if(!esperarEstadoValor(1000))break;
        }
    }
    static String palabraEstándar(int número) {
        if(número==0)return "ipconfig";if(número==1)return "ip";if(número==2)return "ping";if(número==3)return "route";if(número==4)return "netstat";
        if(número==5)return "ps";if(número==6)return "top";if(número==7)return "free";if(número==8)return "df";if(número==9)return "uptime";if(número==10)return "poweroff";return "help";
    }
    static void mostrarAyuda() {
        EntradaSalidaTerminal.escribir("--- Network / system commands ---\n");
        for(int número=0;número<12;número++){EntradaSalidaTerminal.escribir(palabraEstándar(número));EntradaSalidaTerminal.escribir(" / ");EntradaSalidaTerminal.escribir(ComandosAdministración.textoPalabra(número));EntradaSalidaTerminal.escribir(" : ");EntradaSalidaTerminal.escribir(ComandosAdministración.descripción(número));EntradaSalidaTerminal.Caracteres(10);}
        EntradaSalidaTerminal.escribir("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        EntradaSalidaTerminal.escribir("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        EntradaSalidaTerminal.escribir("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean ejecutarComando() {
        int comando=-1;
        for(int número=0;número<12;número++)if(textoIgual(0,palabraEstándar(número)) || textoIgual(0,ComandosAdministración.textoPalabra(número)))comando=número;
        if(textoIgual(0,"ifconfig"))comando=0;if(textoIgual(0,"ss"))comando=4;
        if(comando<0)return false;
        if(comando==11){if(textoIgual(1,"net") || textoIgual(1,"system"))mostrarAyuda();else if(textoIgual(1,"ko") || textoIgual(1,"input"))IntérpreteComandos.ayudaHangul();else IntérpreteComandos.mostrarAyuda();return true;}
        if(comando==0 || comando==1)comandoRed(comando==1);
        else if(comando==2)pruebaRespuestaRetorno();
        else if(comando==6)mostrarEstado();
        else if(númeroElementosElementoLista()!=1){valorFallo("This command takes no arguments; help system");}
        else if(comando==3)mostrarRuta();else if(comando==4)mostrarRed();else if(comando==5)mostrarTareas();else if(comando==7)mostrarMemoria();else if(comando==8)mostrarAlmacenamiento();else if(comando==9)mostrarActividad();
        else if(comando==10)Placa.desactivadoAlimentación();
        return true;
    }
}
