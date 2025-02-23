import os
import json
import time
import requests
from pathlib import Path
from urllib.parse import unquote, parse_qs
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

# Banner PocketFi
BANNER = """
╔══════════════════════════════════════════════╗
║       🌟 POCKETFI BOT - Automated Mining     ║
║ Automate your PocketFi mining and tasks!     ║
║  Developed by: https://t.me/sentineldiscus   ║
╚══════════════════════════════════════════════╝
"""

# Setup logging dengan RichHandler
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%H:%M:%S]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("PocketFi")

# Inisialisasi console rich
console = Console()

class PocketFi:
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://pocketfi.app",
            "Referer": "https://pocketfi.app/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
            ),
            "X-Paf-T": "Abvx2NzMTM==",
        }
        self.max_workers = self.get_thread_count()
        # Dictionary untuk menyimpan data mining dari setiap akun
        self.mining_data = {}

    def get_thread_count(self):
        """Meminta input jumlah thread dari pengguna dengan validasi"""
        while True:
            try:
                console.print("[bold yellow]Masukkan jumlah thread yang diinginkan (1-50):[/]")
                thread_count = int(input("> "))
                if 1 <= thread_count <= 50:
                    logger.info(f"Jumlah thread yang dipilih: {thread_count}")
                    return thread_count
                else:
                    console.print("[bold red]Masukkan angka antara 1 dan 50![/]")
            except ValueError:
                console.print("[bold red]Input tidak valid, masukkan angka![/]")

    def countdown(self, seconds):
        """Menampilkan countdown dengan tqdm"""
        with tqdm(total=seconds, desc="Menunggu", unit="s") as pbar:
            for _ in range(seconds):
                time.sleep(1)
                pbar.update(1)

    def get_user_mining(self, init_data):
        url = "https://gm.pocketfi.org/mining/getUserMining"
        headers = self.headers.copy()
        headers["Telegramrawdata"] = init_data

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json().get("userMining")
        except (requests.RequestException, TimeoutError) as e:
            logger.error(f"Gagal mendapatkan data mining: {str(e)}")
            return None

    def claim_mining(self, init_data):
        url = "https://gm.pocketfi.org/mining/claimMining"
        headers = self.headers.copy()
        headers["Telegramrawdata"] = init_data

        try:
            response = requests.post(url, headers=headers, timeout=10)
            response.raise_for_status()
            # Menyembunyikan log "Claim berhasil | Saldo: [nilai]"
            pass  # Tidak ada log untuk claim saldo
        except (requests.RequestException, TimeoutError) as e:
            logger.error(f"Gagal claim: {str(e)}")

    def get_tasks(self, boost_type, init_data):
        url = f"https://bot.pocketfi.org/boost/tasks?boostType={boost_type}"
        headers = self.headers.copy()
        headers["Telegramrawdata"] = init_data

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, TimeoutError) as e:
            logger.error(f"Gagal mendapatkan tugas {boost_type}: {str(e)}")
            return None

    def do_task(self, task_id, init_data):
        url = "https://bot.pocketfi.org/confirmSubscription"
        headers = self.headers.copy()
        headers["Telegramrawdata"] = init_data
        data = {"subscriptionType": task_id}

        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code == 500:
                # Menyembunyikan log warning untuk tugas manual
                pass  # Tidak ada log untuk "Harus menyelesaikan tugas secara manual"
            else:
                response.raise_for_status()
                logger.info(f"Misi {task_id} selesai")
        except (requests.RequestException, TimeoutError) as e:
            logger.error(f"Gagal menjalankan tugas: {str(e)}")

    def activate_daily_boost(self, init_data):
        url = "https://bot.pocketfi.org/boost/activateDailyBoost"
        headers = self.headers.copy()
        headers["telegramRawData"] = init_data

        try:
            response = requests.post(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            updated_for_day = data.get("updatedForDay")
            pass  # Tidak ada log untuk boost harian
        except (requests.RequestException, TimeoutError) as e:
            logger.error(f"Gagal klaim harian: {str(e)}")

    def manage_task(self, init_data):
        pump_task = self.get_tasks("pump", init_data)
        general_task = self.get_tasks("general", init_data)
        partner_task = self.get_tasks("partner", init_data)

        if not all([pump_task, general_task, partner_task]):
            logger.error("Gagal mendapatkan info quest")
            return

        try:
            all_tasks = (
                pump_task.get("tasks", {}).get("pump", [])
                + general_task.get("tasks", {}).get("connect", [])
                + general_task.get("tasks", {}).get("daily", [])
                + general_task.get("tasks", {}).get("subscriptions", [])
                + general_task.get("tasks", {}).get("trade", [])
                + partner_task.get("tasks", {}).get("partner", [])
            )
        except AttributeError as e:
            logger.error(f"Error menggabungkan tugas: {str(e)}")
            return

        total_tasks = len([task for task in all_tasks if task.get("doneAmount") == 0])
        if total_tasks == 0:
            pass  # Tidak ada log untuk "Tidak ada tugas yang perlu dilakukan"
            return

        for task_count, task in enumerate(all_tasks, 1):
            if task.get("doneAmount") == 0:
                task_code = task.get("code", "Unknown")
                console.print(f"[yellow]Memulai tugas {task_count}/{total_tasks}[/]", end="\r")
                self.do_task(task_code, init_data)
        console.print(" " * 50, end="\r")

    def process_account(self, index, init_data):
        """Memproses satu akun dan menyimpan data ke self.mining_data"""
        try:
            parsed_data = parse_qs(init_data)
            user_encoded = parsed_data.get("user", [None])[0]
            if not user_encoded:
                logger.error(f"Akun {index}: Informasi user tidak ditemukan")
                self.mining_data[index] = {
                    "username": f"Akun {index}",
                    "saldo": "Error: User tidak ditemukan",
                    "kecepatan": "-"
                }
                return

            user_data = json.loads(unquote(user_encoded))
            user_name = user_data.get("username", "Unknown")
            
            user_mining = self.get_user_mining(init_data)
            if user_mining:
                self.mining_data[index] = {
                    "username": user_name,
                    "saldo": str(user_mining.get("gotAmount", "0")),
                    "kecepatan": str(user_mining.get("speed", "0"))
                }
                self.activate_daily_boost(init_data)
                self.claim_mining(init_data)
                self.manage_task(init_data)
            else:
                logger.error(f"Akun {index}: Gagal mendapatkan info mining")
                self.mining_data[index] = {
                    "username": user_name,
                    "saldo": "Error: Gagal mining",
                    "kecepatan": "-"
                }

        except Exception as e:
            logger.error(f"Akun {index}: Error - {str(e)}")
            self.mining_data[index] = {
                "username": f"Akun {index}",
                "saldo": f"Error: {str(e)}",
                "kecepatan": "-"
            }
        logger.debug(f"Data untuk Akun {index} disimpan: {self.mining_data[index]}")

    def display_mining_table(self):
        """Menampilkan tabel dengan format: akun menurun, username, saldo, dan kecepatan memanjang"""
        if not self.mining_data:
            console.print("[bold red]Tidak ada data untuk ditampilkan[/]")
            logger.error("Data mining kosong, periksa koneksi atau file data.txt")
            return

        table = Table(title="Informasi akun", title_style="green on black", style="orange1", border_style="orange1")
        table.add_column("Akun", style="green on black", justify="left")
        table.add_column("Username", style="orange1 on black", justify="center")
        table.add_column("Saldo", style="orange1 on black", justify="center")
        table.add_column("Kecepatan", style="orange1 on black", justify="center")

        for index in sorted(self.mining_data.keys()):
            data = self.mining_data[index]
            username = data["username"]
            saldo = data["saldo"]
            kecepatan = data["kecepatan"]
            table.add_row(f"Akun {index}", username, saldo, kecepatan)

        console.print(table)

    def main(self):
        console.print(BANNER)  # Tampilkan banner di awal
        data_file = Path(__file__).parent / "data.txt"
        if not data_file.exists():
            logger.error("File data.txt tidak ditemukan")
            return

        with data_file.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            logger.error("File data.txt kosong")
            return

        while True:
            self.mining_data.clear()  # Reset data sebelum proses baru
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [
                    executor.submit(self.process_account, index, init_data)
                    for index, init_data in enumerate(lines, start=1)
                ]
                for future in futures:
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"Thread error: {str(e)}")

            logger.info("Menampilkan tabel hasil mining...")
            self.display_mining_table()

            logger.info("Menunggu 4 jam untuk melanjutkan...")
            self.countdown(4 * 60 * 60)  # 4 jam dalam detik (disesuaikan dari 5 jam)

if __name__ == "__main__":
    pocket_fi = PocketFi()
    try:
        pocket_fi.main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Bot dimatikan oleh pengguna.[/]")
    except Exception as e:
        logger.error(f"Error utama: {str(e)}")
