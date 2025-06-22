from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI(title="FASTAPI DI APP")

def dapatkan_biji_kopi(jenis_biji: str = "Arabica"):
    print(f"\n[DEBUG] --> DI Step (Level 1): Menyediakan biji kopi '{jenis_biji}'.")
    return jenis_biji

class CoffeeMachine:
    def __init__(self, biji: str):
        self.biji_terisi = biji
        self.is_on = False
        print(f"[DEBUG] --> DI Step (Kelas Level 2): CoffeeMachine diinisialisasi dengan biji {self.biji_terisi}.")

    def hidupkan(self):
        if not self.is_on:
            self.is_on = True
            print("[DEBUG] --> CoffeeMachine sekarang ON.")
    
    def buat_espresso(self) -> str:
        self.hidupkan()
        return f"Sebuah espresso shot yang kaya rasa dibuat dari biji {self.biji_terisi}!"


def dapatkan_coffee_machine(
    biji_used: Annotated[str, Depends(dapatkan_biji_kopi)]
) -> CoffeeMachine:
    print("[DEBUG] --> DI Step (Fungsi Level 2): Menyediakan instance CoffeeMachine.")
    return CoffeeMachine(biji=biji_used)

class Barista:
    def __init__(self, mesin: CoffeeMachine):
        self.mesin_kopi = mesin
        print("[DEBUG] --> DI Step (Kelas Level 3): Barista siap dengan CoffeeMachine-nya.")

    def siapkan_latte(self, nama_pelanggan: str) -> str:
        espresso = self.mesin_kopi.buat_espresso()
        return f"Halo {nama_pelanggan}! Latte creamy Anda, dibuat dengan {espresso}!"


def dapatkan_barista(
    mesin: Annotated[CoffeeMachine, Depends(dapatkan_coffee_machine)]
) -> Barista:
    print("[DEBUG] --> DI Step (Fungsi Level 3): Menyediakan instance Barista.")
    return Barista(mesin=mesin)

@app.get("/pesan_latte/{nama_pelanggan}")
async def pesan_latte(
    nama_pelanggan: str,
    barista: Annotated[Barista, Depends(dapatkan_barista)]
):
    """Endpoint untuk memesan latte."""
    print(f"\n[DEBUG] --> Endpoint: 'pesan_latte_endpoint' dipanggil untuk {nama_pelanggan}.")
    pesan_latte = barista.siapkan_latte(nama_pelanggan)
    return {"status_pesanan": "Sukses", "minuman_anda": pesan_latte}