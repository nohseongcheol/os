# engos 기능 대응표

이 표는 기존 `herdado_fonte/`의 objeto_VALOR 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [real_dados arranque_da_máquina 기능과 한계](../os/LEIAME_eb81d7d9.md)를 따로 기록한다.

## Java 관리 camada_VALOR implementação 완료

| engos região_VALOR | JCheOS implementação |
|---|---|
| memorymanager, phymem | `Memória_gerente` alinhar_VALOR alocar_Armazenamento·lançar_Armazenamento·병합 |
| paging, virtmem | `Gerenciador_de_Páginas` Endereço email_região·página_VALOR Ligar·COW·개인 Escrita |
| gdt, tss | `Global_descritor_tabela`, `Tarefa_Estado_segmento` |
| interrupt | `IRQ_gerente` registro_entrada·ligar·distribuir_VALOR |
| process, scheduler, thread | `Processo_VALOR`, `Agendador` PID·fork·wait·Estado_VALOR mudar_MODO |
| systemcall/POSIX 1단계 | Leitura·Escrita·Abrir·Fechar·seek·dup·fcntl·acesso_entrada·작업목록·espaço_do_utilizador/무리 ID·sincronizar·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 seção_VALOR Leitura·Escrita |
| MSDOS partition | `partição_primária_tabela` MBR 검증과 네 entrada_VALOR_962f286b analisar_VALOR |
| FAT 공개 ficheiro camada_VALOR | `sistema_de_arquivos`, `Arquivo_descritor_tabela` Leitura 전용 파일과 과정별 FD |
| ELF | ELF32 검사, seção_VALOR recortar 검사, 적재, NOBITS zero_operando inicializar, iniciar Endereço·parâmetro_argumento·ambiente 반영 |
| keyboard, mouse | `entrada_gerente`의 손실 계수 declarações Evento 대기열 |
| timer | `Relógio` 틱과 valor_temporal CONVERTER_VALOR |
| PCI | `acessório_barramento_gerente` 검색 결과와 celular_VALOR seleção_VALOR |
| VGA/text mode | `caractere_visor` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `rede_Ferramentas`, `camada_de_rede` quadro_ÍNDICE 검사·soma_de_verificação·valor_do_contrato/hardware_porta distribuir_VALOR |

## 기존 objeto_VALOR 기반 관리 kernel_VALOR 전체를 부팅하기 위해 남은 Ligar

Avançar_item 항목은 Java 문법만으로 실행할 número 없는 CPU/celular_VALOR 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot ponto_de_entrada_VALOR, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 contexto_VALOR Store_VALOR
- real_dados PIC/PIT/PS2/ATA/PCI hardware_porta 및 AMD PCnet DMA Loop_VALOR
- Java objeto_VALOR·MATRIZ_VALOR disposição_de_ligação, exceção, estático_VALOR inicializar, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT fase_VALOR
- FAT 디스크 구역을 real_dados ATA 장치와 연결하는 E_S 접착 camada_VALOR

위 관리 계층은 engos 기능의 Java 관리 구현과 host 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot ponto_de_entrada_VALOR, estático_VALOR inicializar·inteiro MATRIZ_VALOR, VGA/직렬/PS2, InterpretadorComandos, espaço_do_utilizador ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 host 루프백 패킷 왕복을 검증했다. 위 표의 objeto_VALOR 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
