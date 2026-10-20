# 3. Čínský LX04 → SP6

Pro čínský budík, který už běží na upravené ROM (官改) nebo na originálním systému. SP6 je novější verze upravené ROM s funkční instalací vlastních aplikací.

## Firmware

| | |
|---|---|
| Název | 官改 SP6 pro LX04 |
| Verze systému | 2.31.31 (vývojová) |
| Verze úprav | 2.99.99 |
| Datum | 20. 6. 2021 |

Balíček `Image sp6.zip` je ke stažení na komunitním webu [小爱音箱资源站](https://xiaoai.qgmzmy.me/), složka `lx04/rom/官改`.

> [!NOTE]
> Autor ROM ji dává zdarma a zakazuje její prodej i další šíření. Proto ji tady nenajdeš. Prosíme, respektuj jeho podmínky.

Po rozbalení bys měl mít:

```
boot-verified.img      lk-verified.img        odmdtbo-verified.img
tee-verified.img       logo-verified.bin      system.img
system_other.img       vendor.img             userdata.img
preloader_mi_lx04.bin  MT8167_Android_scatter.txt
MI_AllInOne_DA-resign.bin   hwparam.json
```

## Než začneš

- [Záloha](02-zaloha.md) hotová, včetně boot1.
- Bootloader musí být odemčený. Na upravené ROM bývá, když si nejsi jistý:
  ```bash
  python3 mtk.py da seccfg unlock
  ```

## Nahrání

Přejdi do složky s rozbaleným firmwarem a zapisuj oddíl po oddílu. U každého příkazu: spusť → připoj budík v BROM → počkej na 100 %.

```bash
source ~/mtkclient/mtk_venv/bin/activate
cd "cesta/k/Image sp6"

python3 ~/mtkclient/mtk.py w lk_a lk-verified.img
python3 ~/mtkclient/mtk.py w boot_a boot-verified.img
python3 ~/mtkclient/mtk.py w tee_a tee-verified.img
python3 ~/mtkclient/mtk.py w odmdtbo_a odmdtbo-verified.img
python3 ~/mtkclient/mtk.py w logo logo-verified.bin
python3 ~/mtkclient/mtk.py w system_a system.img
python3 ~/mtkclient/mtk.py w system_b system_other.img
python3 ~/mtkclient/mtk.py w vendor_a vendor.img
python3 ~/mtkclient/mtk.py w userdata userdata.img
```

Nakonec vymaž uživatelská data, aby systém naběhl čistý:

```bash
cd ~/mtkclient
python3 mtk.py e userdata,metadata
```

Odpoj kabel a budík zapni. První start trvá déle.

## Co se nezapisuje — a proč

- **Preloader** (`preloader_mi_lx04.bin`). Zůstává ten stávající. mtkclient ho zapisuje bez hlavičky, kterou boot oblast potřebuje, a budík by zůstal úplně mrtvý. Podrobně v [Řešení problémů](07-problemy.md).
- **Identita zařízení** (`nvram`, `proinfo`, `protect1/2`, `persist`). Zůstává původní, budíku patří a je to tak správně — sériové číslo, MAC adresy i `mi.did` se nemění.

## Ověření

Po startu by mělo fungovat ADB rovnou, bez zapínání ladění:

```bash
adb devices
```

Pokračuj na [Po instalaci](05-po-instalaci.md).
