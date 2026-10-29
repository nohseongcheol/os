# koros 현행 구현

`현행/`은 `/home/user/engos`의 현재 커널 기능을 한글 독음 방식의 함수·변수 이름으로 옮긴 독립 빌드 트리다.

- 예: `CloneAddressSpaceCOW` → `C클론어드레스스페이스카우`
- Go는 한글 첫 글자를 공개 식별자로 처리하지 않으므로 공개 이름에는 원래 영문 대문자 한 글자를 표지로 유지한다.
- `main`, `init`, `K핵심` 및 런타임/어셈블리 ABI 이름은 부팅 호환성을 위해 유지한다.
- 전체 원래 이름과 변환 이름은 `현행/이름대응표.tsv`에 기록된다.

빌드:

```sh
make current
make current-iso
make current-qemu
```

`current-qemu`는 시험 디스크를 `snapshot=on`으로 연결하므로 원본 VDI를 변경하지 않는다.

현행판에는 POSIX 파일·과정 호출, FAT 읽기, ELF 실행과 IPv4 UDP 로컬 소켓 호출이 포함된다. 외부 NIC와 TCP는 아직 구현 단계다.

`현행/`을 다시 생성하려면:

```sh
go run /home/user/localize_engos.go koros /home/user/engos /home/user/koros/현행
```
