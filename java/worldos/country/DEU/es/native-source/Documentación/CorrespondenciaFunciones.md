# engos 기능 대응표

이 표는 기존 `FuentesFundamentales/`의 valorObjeto fundamento JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [datosEfectivo Arranque 기능과 límiteFrontera](../os/Guía.md)를 따로 기록한다.

## Java 관리 valorCapa implementación esTerminado

| engos valorRegión | JDeuOS implementación |
|---|---|
| memorymanager, phymem | `GestorMemoria` valorAlinear asignarMemoriaAlmacenamiento·liberarAlmacenamiento·병합 |
| paging, virtmem | `GestorPágina` dirección regiónDirección·valorPágina conectar·COW·개인 escribir |
| gdt, tss | `TablaDescriptorGlobal`, `SegmentoEstadoValorTarea` |
| interrupt | `GestorInterrumpir` registroEntradaElemento·activar·distribuirValor |
| process, scheduler, thread | `valorProceso`, `Planificador` PID·fork·wait·valorEstadoValor modoConmutar |
| systemcall/POSIX 1단계 | leer·escribir·abrir·cerrar·seek·dup·fcntl·entradaElementoAcceso·작업목록·Usuario/무리 ID·sincronizar·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `AdjuntoTecnologíaAvanzado` 512바이트 valorSección leer·escribir |
| MSDOS partition | `tablaParticiónPrimario` MBR 검증과 네 valorEntradaElemento analizarValor |
| FAT 공개 Archivo valorCapa | `SistemaArchivo`, `tablaDescriptorArchivo` leer 전용 파일과 과정별 FD |
| ELF | ELF32 Comprobaciones, valorSección recortar Comprobaciones, 적재, NOBITS operandoCero inicializar, ponerEnMarcha dirección·argumentoParámetro·entorno 반영 |
| keyboard, mouse | `GestorEntrada`의 손실 계수 Encabezados evento 대기열 |
| timer | `Reloj` 틱과 valorTiempo convertirValor |
| PCI | `GestorBusPeriférico` 검색 결과와 Dispositivo valorSelección |
| VGA/text mode | `presentarCarácter` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `HerramientasRed`, `CapaRed` índiceMarco Comprobaciones·sumaComprobación·valorContrato/puertoEquipoFísico distribuirValor |

## 기존 valorObjeto fundamento 관리 valorNúcleo 전체를 부팅하기 위해 남은 conectar

elementoListaSiguiente 항목은 Java 문법만으로 실행할 númeroValor 없는 CPU/Dispositivo 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot valorPuntoEntradaElemento, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 valorContexto valorAlmacenar
- datosEfectivo PIC/PIT/PS2/ATA/PCI puertoEquipoFísico 및 AMD PCnet DMA valorBucle
- Java valorObjeto·valorArreglo DisposiciónEnlace, excepción, valorEstático inicializar, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT valorEtapa
- FAT 디스크 구역을 datosEfectivo ATA 장치와 연결하는 salidaEntrada 접착 valorCapa

valorExtremoSuperior 관리 계층은 engos 기능의 Java 관리 구현과 Anfitrión 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot valorPuntoEntradaElemento, valorEstático inicializar·EnteroValor valorArreglo, VGA/valorSerie/PS2, IntérpreteComandos, Usuario ELF/ring 3/시스템 invocar, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 Anfitrión 루프백 패킷 왕복을 검증했다. valorExtremoSuperior 표의 valorObjeto fundamento 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
