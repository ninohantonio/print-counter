import threading
import time
import win32print
import tkinter
from tkinter import *


def monitor_print_jobs():
    last_valid_job = None
    while True:
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        for printer in printers:
            printer_handle = win32print.OpenPrinter(printer)
            try:
                jobs = win32print.EnumJobs(printer_handle, 0, -1, 1)
                # Parcourir tous les travaux d'impression
                for job in jobs:
                    # Vérifier si le travail contient des métadonnées valides
                    if job['TotalPages'] > 0 and job['pDocument']:
                        last_valid_job = job  # Mettre à jour le dernier travail valide
            finally:
                win32print.ClosePrinter(printer_handle)

        # Si un dernier travail valide a été trouvé, l'afficher
        if last_valid_job:
            print("Dernier travail valide détecté :")
            print(f"job Id: {last_valid_job['JobId']}")
            print(f"Printer name : {last_valid_job['pPrinterName']}")
            print(f"Document: {last_valid_job['pDocument']}")
            print(f"User: {last_valid_job['pUserName']}")
            print(f"Total Pages: {last_valid_job['TotalPages'] + last_valid_job['PagesPrinted']}")
            print(f"Submitted: {last_valid_job['Submitted']}")
            last_valid_job = None  # Réinitialiser après affichage pour surveiller les prochains jobs

        time.sleep(1)  # Attendre avant de vérifier à nouveau les imprimantes


def start_monitoring():
    monitoring_thread = threading.Thread(target=monitor_print_jobs)
    monitoring_thread.daemon = True
    monitoring_thread.start()


if __name__ == '__main__':
    start_monitoring()
    screen = tkinter.Tk()
    screen.mainloop()
