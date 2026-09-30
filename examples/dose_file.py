# -*- coding: utf-8 -*-
"""
Luotu Ke 28.1.2026
Tekijä: Sanni Sinisalo

Koodi RTDose tiedoston visualisoimiseen.
"""

import pydicom
import matplotlib.pyplot as plt
from pathlib import Path

# Potilaan doseds-kansion polku
doseds_polku = Path(
    r"C:\Users\User01\GRADU\Aineisto\VN0ds\Patient10_VN0\doseds"
)

# Etsitään RD-alkuinen tiedosto vain suoraan doseds-kansiosta
rd_tiedostot = [
    tiedosto for tiedosto in doseds_polku.glob("RD*")
    if tiedosto.is_file()
]

# Tarkistetaan, että tiedostoja löytyy täsmälleen yksi
if len(rd_tiedostot) == 0:
    raise FileNotFoundError(
        f"RD-alkuista tiedostoa ei löytynyt kansiosta: {doseds_polku}"
    )
elif len(rd_tiedostot) > 1:
    raise RuntimeError(
        f"Kansiosta löytyi useampi RD-alkuinen tiedosto: {rd_tiedostot}"
    )

# Valitaan löydetty tiedosto
dose_polku = rd_tiedostot[0]
ds = pydicom.dcmread(dose_polku)

# Luetaan annosdata
dose_raw = ds.pixel_array  # muoto: (z, y, x)
scaling = float(ds.DoseGridScaling)

dose = dose_raw * scaling  # Gy

print("Dose-matriisin muoto:", dose.shape)
print("Annoksen min/max (Gy):", dose.min(), dose.max())

# Näytetään viipaleet
for i in range(dose.shape[0]):
    plt.figure(figsize=(6, 6))
    plt.imshow(dose[i, :, :], cmap="inferno")
    plt.colorbar(label="Dose (Gy)")
    plt.title(f"RT Dose slice {i}")
    plt.axis("off")
    plt.show()