# 1. Příprava

Ověřeno na Kali Linuxu s Pythonem 3.13 a mtkclientem 2.1.4. Na jiném Debianu/Ubuntu by to mělo jít stejně.

> [!NOTE]
> Na Windows to nedoporučujeme. mtkclient tam budík hlásil jen na okamžik a pak zmizel, SP Flash Tool při čtení padal s `STATUS_READ_DATA_EXCEPTION`. Na Linuxu to prošlo napoprvé. Windows 10 je potřeba jen pro jeden krok převodu globální verze — SP Flash Tool ([04](04-x04g-na-lx04.md)). Další globální kusy už jdou klonováním čistě na Linuxu.

## mtkclient

```bash
sudo apt update
sudo apt install -y git python3-venv python3-pip libusb-1.0-0 adb
cd ~
git clone https://github.com/bkerler/mtkclient.git
cd mtkclient
python3 -m venv mtk_venv
source mtk_venv/bin/activate
pip install -r requirements.txt
pip install .
```

Pravidla pro USB, aby mtkclient viděl zařízení bez roota:

```bash
sudo cp ~/mtkclient/Setup/Linux/*.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo usermod -aG plugdev,dialout $USER
```

Po přidání do skupin se odhlas a znovu přihlas.

Na rozbalení firmwaru a kontrolu souborů:

```bash
sudo apt install -y p7zip-full xxd
```

## Před každou prací

```bash
cd ~/mtkclient
source mtk_venv/bin/activate
```

Zapomenuté `source` je nejčastější chyba — projeví se jako `ModuleNotFoundError: No module named 'usb'`.

## Tlačítkové sekvence

| Režim | Jak na něj |
|---|---|
| **BROM** (pro mtkclient a SP Flash Tool) | budík vypnutý → podrž **hlasitost +** → zapoj USB kabel → drž pár vteřin |
| **Recovery** | budík vypnutý → podrž **hlasitost + a −** současně → zapoj kabel |
| Menu recovery | na obrazovce „No command" podrž **Mute + hlasitost +** |

V BROM režimu zůstane displej černý. Že se spojil, poznáš podle výpisu mtkclientu (`Port - Device detected :)`).

Nejdřív spusť příkaz mtkclientu, ten začne čekat na zařízení — a pak teprve připoj budík v BROM režimu.

## Kabel

Budík má jediný USB port, přes který se i napájí. Použij kvalitní datový kabel. Nabíjecí kabely bez datových vodičů se projeví tak, že mtkclient zařízení vůbec nezaznamená.
