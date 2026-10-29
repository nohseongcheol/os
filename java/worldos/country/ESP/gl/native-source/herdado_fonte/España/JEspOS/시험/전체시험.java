// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import España.JEspOS.기억공간.Memoria_xefe;
import España.JEspOS.기억공간.páxina_xefe;
import España.JEspOS.입력.입력사건;
import España.JEspOS.작업.Proceso_VALOR;
import España.JEspOS.체계호출.체계호출;
import España.JEspOS.sistema_de_ficheiros.실행파일적재기;
import España.JEspOS.kernel.kernel;
import España.JEspOS.hospedar.호스트하드웨어;
import España.JEspOS.IRQ.IRQ_xefe;
import España.JEspOS.서술자.전역서술자표;
import España.JEspOS.Almacenamento_dispositivo.고급기술결합장치;
import España.JEspOS.dispositivo_VALOR.accesorio_bus_xefe;
import España.JEspOS.Rede_Montón.Rede_Ferramentas;
import España.JEspOS.Rede_Montón.Rede_capa;
import España.JEspOS.dispositivo_VALOR.Reloxo;
import España.JEspOS.서술자.tarefa_Estado_segmento;
import España.JEspOS.화면.carácter_mostrar;
import España.JEspOS.sistema_de_ficheiros.기본분할영역표;

public final class 전체시험 {
    private static int pass_CONTAR;

    private 전체시험() {
    }

    public static void main(String[] parámetro_argumento) {
        호스트하드웨어 dispositivo_VALOR = new 호스트하드웨어();
        kernel kernel_VALOR = new kernel(dispositivo_VALOR);
        kernel_VALOR.Executar_2();

        기억공간시험(kernel_VALOR);
        쪽관리시험(kernel_VALOR);
        파일과과정시험(kernel_VALOR);
        실행파일시험(kernel_VALOR);
        입력시험(kernel_VALOR);
        하드웨어시험(dispositivo_VALOR);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JEspOS 시험 pass_VALOR: " + pass_CONTAR);
    }

    private static void 기억공간시험(kernel kernel_VALOR) {
        Memoria_xefe xefe_VALOR = kernel_VALOR.기억공간();
        int 첫주소 = xefe_VALOR.정렬할당(100, 64);
        verificar((첫주소 & 63) == 0, "aliñar_VALOR atribuír_Almacenamento");
        xefe_VALOR.escribir_byte_VALOR(첫주소, (byte) 0x5a);
        verificar(xefe_VALOR.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Escritura");
        int 사용전 = xefe_VALOR.사용크기();
        xefe_VALOR.liberar_Almacenamento(첫주소);
        verificar(xefe_VALOR.사용크기() < 사용전, "기억공간 liberar_Almacenamento");
    }

    private static void 쪽관리시험(kernel kernel_VALOR) {
        páxina_xefe xefe_VALOR = kernel_VALOR.쪽관리();
        páxina_xefe.ENDEREZO_espazo 부모공간 = xefe_VALOR.새주소공간();
        xefe_VALOR.MAP_páxina(부모공간, 0x1000, true);
        xefe_VALOR.escribir_byte_VALOR(부모공간, 0x1010, (byte) 7);
        páxina_xefe.ENDEREZO_espazo neno_espazo = xefe_VALOR.쓰기시복사복제(부모공간);
        xefe_VALOR.escribir_byte_VALOR(neno_espazo, 0x1010, (byte) 9);
        verificar(xefe_VALOR.바이트읽기(부모공간, 0x1010) == 7, "Escritura 시 copiar_VALOR 부모 격리");
        verificar(xefe_VALOR.바이트읽기(neno_espazo, 0x1010) == 9, "Escritura 시 copiar_VALOR neno_VALOR Escritura");
    }

    private static void 파일과과정시험(kernel kernel_VALOR) {
        byte[] Contido_VALOR = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_VALOR.sistema_de_ficheiros().Anexar_Ficheiro("시험", Contido_VALOR);
        Proceso_VALOR 부모 = kernel_VALOR.첫과정();
        체계호출 호출 = kernel_VALOR.체계호출();
        int 서술자 = 호출.Abrir(부모, "/시험", 체계호출.só_de_lectura_marca);
        verificar(서술자 >= 3, "Ficheiro Abrir");

        byte[] 받을곳 = new byte[Contido_VALOR.length];
        verificar(호출.Lectura(부모, 서술자, 받을곳, 받을곳.length) == Contido_VALOR.length, "Ficheiro Lectura");
        verificar(Arrays.equals(Contido_VALOR, 받을곳), "Ficheiro Contido_VALOR");
        verificar(호출.mover_cargo(부모, 서술자, 0, 체계호출.ACHAR_START) == 0, "Ficheiro Posición mover_VALOR");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        verificar(복제서술자 >= 0, "서술자 clon_VALOR");
        Proceso_VALOR neno_VALOR = 호출.clon_Proceso(부모);
        verificar(neno_VALOR.식별자() != 부모.식별자(), "Proceso_VALOR 식별자 분리");
        verificar(neno_VALOR.부모식별자() == 부모.식별자(), "부모 Proceso_VALOR 식별자");
        verificar(호출.Pechar(neno_VALOR, 서술자) == 0 && 부모.파일서술자().Tecnoloxía_da_información_TI_abrir(서술자), "neno_VALOR Pechar 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        verificar(이전끝 == 0x06000000, "apl_f5044b9b 끝 늘리기");
        verificar(부모.apl_pausa() == 0x06002000, "apl_f5044b9b 끝 반영");
        verificar(neno_VALOR.apl_pausa() == 0x06000000, "과정별 apl_f5044b9b 끝 격리");

        neno_VALOR.saír_apl(7);
        verificar(호출.자식기다리기(부모, neno_VALOR.식별자(), false) == (7 << 8), "neno_VALOR saír_apl 기다리기");
        verificar(호출.접근가능("시험", 1) == -13, "executar_comando permiso_VALOR rexeitar_VALOR_e3ecc00b");
        verificar(호출.사용자식별자() == 0 && 호출.무리식별자() == 0, "사용자와 무리 식별자");
        verificar("/".equals(호출.ao_corrente_lista_de_tarefas(2)) && 호출.mudar_lista_de_tarefas("/") == 0, "ao_corrente_elemento 작업 introdución_Lista");
        verificar(호출.Tecnoloxía_da_información_TI_Terminal(부모, 1), "표준 Saída 단말");
        verificar("JEspOS".equals(호출.sistema_Detalles().sistema_nome()), "sistema_operativo_VALOR msinfo32_exe");
    }

    private static void 실행파일시험(kernel kernel_VALOR) {
        byte[] datos = new byte[92];
        datos[0] = 0x7f;
        datos[1] = 'E';
        datos[2] = 'L';
        datos[3] = 'F';
        datos[4] = 1;
        datos[5] = 1;
        escribir_número_enteiro_VALOR(datos, 24, 0x04001000);
        escribir_número_enteiro_VALOR(datos, 32, 52);
        짧은정수쓰기(datos, 46, 40);
        짧은정수쓰기(datos, 48, 1);
        escribir_número_enteiro_VALOR(datos, 56, 8);
        escribir_número_enteiro_VALOR(datos, 60, 2);
        escribir_número_enteiro_VALOR(datos, 64, 0x04002000);
        escribir_número_enteiro_VALOR(datos, 72, 64);

        실행파일적재기.IMAXE IMAXE_VALOR = new 실행파일적재기().검사(datos);
        verificar(IMAXE_VALOR.START_ENDEREZO() == 0x04001000, "ELF Executar_2 ENDEREZO");
        verificar(IMAXE_VALOR.구역들().size() == 1 && IMAXE_VALOR.구역들().get(0).종류() == 8, "ELF 빈 datos sección_VALOR");
        int 서술자 = kernel_VALOR.체계호출().Abrir(kernel_VALOR.첫과정(), "시험", 체계호출.só_de_lectura_marca);
        verificar(kernel_VALOR.체계호출().Ficheiro_control(kernel_VALOR.첫과정(), 서술자, 2, 1) == 0, "executar_comando 시 Pechar Configuración");
        verificar(kernel_VALOR.체계호출().executar_comando(kernel_VALOR.첫과정(), datos, new String[] {"시험", "값"}, new String[] {"Idioma=Galego"}) == 0, "ELF executar_comando IMAXE_VALOR 적재");
        verificar(kernel_VALOR.첫과정().실행시작주소() == 0x04001000, "executar_comando Executar_2 ENDEREZO 반영");
        verificar(kernel_VALOR.첫과정().실행인자().length == 2 && kernel_VALOR.첫과정().환경값().length == 1, "executar_comando 인자와 환경");
        verificar(!kernel_VALOR.첫과정().파일서술자().Tecnoloxía_da_información_TI_abrir(서술자), "executar_comando 시 서술자 Pechar");
        verificar(kernel_VALOR.쪽관리().바이트읽기(kernel_VALOR.첫과정().ENDEREZO_espazo(), 0x04002000) == 0, "빈 datos sección_VALOR 영 iniciar");
    }

    private static void 입력시험(kernel kernel_VALOR) {
        kernel_VALOR.입력관리().키누름('가');
        kernel_VALOR.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kernel_VALOR.입력관리().Seguinte_evento();
        입력사건 SEGUNDO_evento = kernel_VALOR.입력관리().Seguinte_evento();
        verificar(첫사건.사건종류() == 입력사건.종류.키누름, "자판 Evento");
        verificar(SEGUNDO_evento.첫째값() == 3 && SEGUNDO_evento.SEGUNDO_VALOR() == -2, "쥐 mover_VALOR Evento");
    }

    private static void 하드웨어시험(호스트하드웨어 dispositivo_VALOR) {
        dispositivo_VALOR.escribir_porto_byte(0x3f8, 0xab);
        verificar(dispositivo_VALOR.포트바이트읽기(0x3f8) == 0xab, "포트 E_S 경계");
        verificar(dispositivo_VALOR.직렬기록().contains("JEspOS"), "직렬 LOG_fila");
    }

    private static void 개입중단과서술자시험() {
        IRQ_xefe xefe_VALOR = new IRQ_xefe();
        xefe_VALOR.rexistrarse_introdución(0x21, Almacenamento_ENDEREZO -> Almacenamento_ENDEREZO + 4);
        xefe_VALOR.activar();
        verificar(xefe_VALOR.distribuír_VALOR(0x21, 100) == 104, "IRQ distribuír_VALOR");
        xefe_VALOR.desactivar();
        verificar(xefe_VALOR.distribuír_VALOR(0x21, 100) == 100, "IRQ desactivar");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.conxunto_valor_predefinido();
        verificar(서술자표.조각들().size() == 5, "전역 서술자표");
        tarefa_Estado_segmento tarefa_Estado = new tarefa_Estado_segmento();
        tarefa_Estado.특권쌓임공간설정(0x10, 0x800000);
        verificar(tarefa_Estado.영번쌓임조각() == 0x10 && tarefa_Estado.영번쌓임주소() == 0x800000, "작업 Estado_VALOR sección_VALOR");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Almacenamento_dispositivo = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.구역크기];
        byte[] 읽은자료 = new byte[고급기술결합장치.구역크기];
        쓸자료[17] = 42;
        Almacenamento_dispositivo.Escritura(2, 쓸자료);
        Almacenamento_dispositivo.Lectura(2, 읽은자료);
        verificar(읽은자료[17] == 42, "ATA sección_VALOR 읽고 Escritura");

        accesorio_bus_xefe accesorio = new accesorio_bus_xefe();
        accesorio.발견(new accesorio_bus_xefe.dispositivo_VALOR(0x1022, 0x2000, 0xc000, 11));
        verificar(accesorio.Busca_introdución(0x1022, 0x2000) != null, "주변 dispositivo_VALOR Busca_introdución");

        byte[] Ethernet_marco = new byte[34];
        Ethernet_marco[12] = 0x08;
        Ethernet_marco[13] = 0x00;
        Ethernet_marco[14] = 0x45;
        verificar(Rede_Ferramentas.Ethernet_MAIÚSCULA_protocolo(Ethernet_marco) == 0x0800, "이더넷 상위 caso_VALOR");
        verificar(Rede_Ferramentas.상호통신망규약사판인가(Ethernet_marco, 14), "상호통신망규약 4판");
        verificar(Rede_Ferramentas.nube_suma_de_comprobación(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 suma_de_comprobación");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        escribir_número_enteiro_VALOR(첫구역, 454, 63);
        escribir_número_enteiro_VALOR(첫구역, 458, 1024);
        verificar(new 기본분할영역표().Lectura(첫구역).size() == 1, "valor_predefinido 분할 영역표");

        Rede_capa capa_VALOR = new Rede_capa();
        int[] RECIBIDO_CONTAR = new int[1];
        capa_VALOR.rexistrarse_usuario_datos_lección(7, (datos, Executar_2, duración_VALOR) -> RECIBIDO_CONTAR[0]++);
        byte[] marco_ÍNDICE = new byte[14 + 20 + 8];
        marco_ÍNDICE[12] = 0x08;
        marco_ÍNDICE[13] = 0x00;
        marco_ÍNDICE[14] = 0x45;
        marco_ÍNDICE[16] = 0;
        marco_ÍNDICE[17] = 28;
        marco_ÍNDICE[23] = 17;
        marco_ÍNDICE[36] = 0;
        marco_ÍNDICE[37] = 7;
        verificar(capa_VALOR.이더넷받기(marco_ÍNDICE) && RECIBIDO_CONTAR[0] == 1, "usuario datos lección_VALOR distribuír_VALOR");
    }

    private static void 화면과시계시험() {
        carácter_mostrar 화면 = new carácter_mostrar();
        화면.Saída("가나\n다");
        verificar(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Saída");
        Reloxo Reloxo = new Reloxo(100);
        for (int ÍNDICE = 0; ÍNDICE < 10; ÍNDICE++) {
            Reloxo.틱();
        }
        verificar(Reloxo.지난밀리초() == 100, "Reloxo 틱 CONVERTER_VALOR");
    }

    private static void escribir_número_enteiro_VALOR(byte[] datos, int Posición, int VALOR) {
        datos[Posición] = (byte) VALOR;
        datos[Posición + 1] = (byte) (VALOR >>> 8);
        datos[Posición + 2] = (byte) (VALOR >>> 16);
        datos[Posición + 3] = (byte) (VALOR >>> 24);
    }

    private static void 짧은정수쓰기(byte[] datos, int Posición, int VALOR) {
        datos[Posición] = (byte) VALOR;
        datos[Posición + 1] = (byte) (VALOR >>> 8);
    }

    private static void verificar(boolean condición, String Nome) {
        if (!condición) {
            throw new AssertionError("erro_VALOR: " + Nome);
        }
        pass_CONTAR++;
        System.out.println("pass_VALOR: " + Nome);
    }
}
