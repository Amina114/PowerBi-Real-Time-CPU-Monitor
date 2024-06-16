import psutil
import time
import pyodbc

def connect_to_database():
    try:
        con = pyodbc.connect('Driver={SQL Server};'
                             'Server=AMINA_CHABCHOUB;'
                             'Database=System_Information;'
                             'Trusted_connection=yes;')
        print("Connection to database established")
        return con
    except pyodbc.Error as e:
        print("Error connecting to SQL Server:", e)
        return None

def table_exists(cursor, table_name):
    try:
        cursor.execute(f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
        exists = cursor.fetchone() is not None
        print(f"Table '{table_name}' exists: {exists}")
        return exists
    except pyodbc.Error as e:
        print(f"Error checking for table {table_name}:", e)
        return False

def main():
    con = connect_to_database()
    if con is None:
        return
    
    cursor = con.cursor()

    table_name = 'Performances'
    if not table_exists(cursor, table_name):
        print(f"Table '{table_name}' does not exist.")
        return

    while True:
        try:
            # Collect system information
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            cpu_interrupts = psutil.cpu_stats().interrupts
            cpu_syscalls = psutil.cpu_stats().syscalls
            memory_used = psutil.virtual_memory().used
            memory_free = psutil.virtual_memory().available
            bytes_sent = psutil.net_io_counters().bytes_sent
            bytes_received = psutil.net_io_counters().bytes_recv
            disk_usage = psutil.disk_usage('/').percent
       # Print collected values for debugging
            print(f"CPU Usage: {cpu_usage}%")
            print(f"Memory Usage: {memory_usage}%")
            print(f"CPU Interrupts: {cpu_interrupts}")
            print(f"CPU Syscalls: {cpu_syscalls}")
            print(f"Memory Used: {memory_used}")
            print(f"Memory Free: {memory_free}")
            print(f"Bytes Sent: {bytes_sent}")
            print(f"Bytes Received: {bytes_received}")
            print(f"Disk Usage: {disk_usage}%")
            # Insert data into the database
            cursor.execute('''
                INSERT INTO Performances (
                    time, cpu_usage, Memory_Usage, CPU_Interrupts, cpu_calls, 
                    Memory_Used, Memory_Free, Bytes_Sent, Bytes_Received, Disk_Usage
                ) VALUES (
                    GETDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', (cpu_usage, memory_usage, cpu_interrupts, cpu_syscalls, 
                  memory_used, memory_free, bytes_sent, bytes_received, disk_usage))
            con.commit()

            print(f"CPU Usage: {cpu_usage}%")
            time.sleep(1)
        except pyodbc.Error as e:
            print("Error executing SQL command:", e)
            break
        except Exception as e:
            print("An error occurred:", e)
            break

    # Close the connection
    con.close()

if __name__ == "__main__":
    main()
