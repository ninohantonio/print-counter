import threading
import time
import win32print

def monitor_print_jobs():
    while True:
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        # print(f"Get printer = {printers}")
        for printer in printers:
            printer_handle = win32print.OpenPrinter(printer)
            try:
                jobs = win32print.EnumJobs(printer_handle, 0, -1, 1)
                if len(jobs) != 0:
                    print(f"jobs  = {jobs}")
                # for job in jobs:
                #     print(f"Document: {job['pDocument']}")
                #     print(f"User: {job['pUserName']}")
                #     print(f"Total Pages: {job['TotalPages']}")
                #     print(f"Pages Printed: {job['PagesPrinted']}")
                #     print(f"Submitted: {job['Submitted']}")
            finally:
                win32print.ClosePrinter(printer_handle)

        time.sleep(1)
        # pass

def start_monitoring():
    monitoring_thread = threading.Thread(target=monitor_print_jobs)
    monitoring_thread.daemon = True
    monitoring_thread.start()

if __name__ == '__main__':
    start_monitoring()
    while True:
        time.sleep(1)

