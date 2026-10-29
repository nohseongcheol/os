# JBrnOS seni_bina

아래는 objek_VALUE 기반 관리 kernel_VALUE 전체의 sasaran_objek 구조다. 현재 sebenar_data permulaan_mesin 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 sistem_pengendalian README_eb81d7d9](../os/README_eb81d7d9.md)에 pelaksanaan 범위를 명시한다. 아래의 GC·konteks_VALUE tukar_mod·sistem_fail 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 lapisan_VALUE
  ↓
Java AOT 실행기와 objek_VALUE·ARRAY_VALUE·GC 런타임
  ↓
하드웨어 경계
  ↓
Java 관리 kernel_VALUE
  ├─ Memori_rantau/쪽관리/COW
  ├─ Proses_VALUE/배정/wait
  ├─ sistem_fail/ELF/POSIX
  └─ 입력/Storan_peranti/rangkaian_tindan
```

OpenJDK 자체는 이미 운영체제가 제공하는 Fail, 스레드, 가상 기억공간을 전제로 한다. 따라서 kernel_VALUE 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, konteks_VALUE 저장처럼 Java로 표현할 수 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
