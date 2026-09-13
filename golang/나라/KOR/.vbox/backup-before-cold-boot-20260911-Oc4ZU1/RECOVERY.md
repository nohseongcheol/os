# KOR 저장 상태 백업 후 새 부팅 기록

- 작업일: 2026-09-11 (Asia/Seoul)
- 대상: `worldos KOR`, UUID `12edc548-ca02-4c78-bd6e-6ed5850af279`
- 사용자 승인: 저장 상태를 백업하고 기존 디스크를 유지한 채 새로 부팅
- 결과: 저장 상태 해제 후 기존 VM을 GUI로 새 부팅, `running` 확인
- 부팅 검증: 직렬 출력에서 `=== KOR BOOT ===`, `WORLDOS-SHELL:READY` 확인

이 폴더에는 원래 `.sav` 저장 상태, `.vbox` 및 `.vbox-prev` 설정, 실행기 `state.json`, 디스크 VDI, 부팅 ISO, 기존 직렬 로그를 백업했다. 각 복사본은 원본과 바이트 단위로 비교했으며 SHA-256은 `SHA256SUMS`에 기록했다. `vm-before.txt`는 작업 직전 VirtualBox의 상태와 원래 파일 경로를 담는다.

백업 이후 `VBoxManage discardstate`로 저장된 메모리 상태만 해제했다. 이어서 `VBoxManage startvm ... --type gui`로 부팅했으며, 커널/셸 재빌드, 미디어 교체, 새 VM 생성은 하지 않았다. 디스크·ISO·실행기 상태 파일의 해시는 새 부팅 후 검사 시에도 아래와 같았다.

| 파일 | SHA-256 |
| --- | --- |
| 기존 VDI | `09ceaca64f7f996816ca0e938723fdf1b2711efdbc97b5610d94f2f48af5171c` |
| 기존 ISO | `b88077e9b378cb35c7ab219fb28a81f491aff468861bc81c42a68ac95af631a2` |
| 실행기 state.json | `a5b7904256fcb65b9122ee7b112e1d950db08dda18100ca24a392e57055bbbc0` |

백업한 저장 상태는 `2026-09-10T12-28-12-922601000Z.sav`다. 새 부팅은 메모리 안의 이전 실행 작업을 이어받지 않는다. 이번 조치는 VirtualBox의 `VERR_PGM_NO_HYPERVISOR_ADDRESS` 복원 오류 자체를 수정한 것은 아니며, 저장 상태 복원을 다시 시도하면 오류가 재발할 수 있다. 백업 복원은 현재 VM과 디스크의 변경 사항을 먼저 보존한 다음 별도로 검토해야 한다. 실행 중인 VM에 백업 설정이나 디스크를 덮어쓰지 않는다.
