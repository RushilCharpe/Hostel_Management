import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
DATA_FILE = "hostel_records.json"

def load_records():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_records(records):
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=4)

hostel_records = load_records()

def add_record(student_id, student_name):
    hostel_records[student_id] = {
        "Name": student_name,
        "Out Time": None,
        "In Time": None,
        "Reason": None
    }
    save_records(hostel_records)
    console.print(f"[green]✔ Record created for {student_name} (ID: {student_id})[/]")

def log_out(student_id, reason, out_time):
    if student_id in hostel_records:
        hostel_records[student_id]["Out Time"] = out_time
        hostel_records[student_id]["Reason"] = reason
        hostel_records[student_id]["In Time"] = None
        save_records(hostel_records)
        console.print(f"[yellow]↘ {hostel_records[student_id]['Name']} (ID: {student_id}) logged OUT at {out_time} for: {reason}[/]")
    else:
        console.print("[red]⚠ No record found for that ID. Use Add Record first.[/]")

def log_in(student_id, in_time):
    if student_id in hostel_records and hostel_records[student_id]["In Time"] is None:
        hostel_records[student_id]["In Time"] = in_time
        save_records(hostel_records)
        console.print(f"[cyan]↗ {hostel_records[student_id]['Name']} (ID: {student_id}) logged IN at {in_time}[/]")
    else:
        console.print("[red]⚠ No OUT record found or already logged IN.[/]")

def delete_record(student_id):
    if student_id in hostel_records:
        removed = hostel_records.pop(student_id)
        save_records(hostel_records)
        console.print(f"[red]🗑 Deleted record for {removed['Name']} (ID: {student_id})[/]")
    else:
        console.print("[red]⚠ No record found with that ID.[/]")

def show_records():
    if not hostel_records:
        console.print("[bold red]No records available.[/]")
        return

    table = Table(title="🏠 Hostel Records", style="bold magenta")
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Name", justify="center", style="green")
    table.add_column("Out Time", justify="center", style="yellow")
    table.add_column("In Time", justify="center", style="cyan")
    table.add_column("Reason", justify="center", style="white")

    for sid, record in hostel_records.items():
        table.add_row(
            sid,
            record["Name"],
            record["Out Time"] or "-",
            record["In Time"] or "-",
            record["Reason"] or "-"
        )
    console.print(table)

while True:
    console.print(Panel.fit("🏠 [bold cyan]Hostel Management System[/]", style="bold blue"))
    console.print("[1] Add Record\n[2] Log OUT\n[3] Log IN\n[4] Show Records\n[5] Delete Record\n[6] Exit", style="bold white")
    choice = input("Enter choice: ")

    if choice == "1":
        sid = input("Enter Student ID: ")
        name = input("Enter Student Name: ")
        add_record(sid, name)

    elif choice == "2":
        sid = input("Enter Student ID: ")
        reason = input("Reason for going out: ")
        out_time = input("Enter OUT time: ")
        log_out(sid, reason, out_time)

    elif choice == "3":
        sid = input("Enter Student ID: ")
        in_time = input("Enter IN time: ")
        log_in(sid, in_time)

    elif choice == "4":
        show_records()

    elif choice == "5":
        sid = input("Enter Student ID to delete: ")
        delete_record(sid)

    elif choice == "6":
        console.print("[bold green]Exiting system... Goodbye![/]")
        break

    else:
        console.print("[red]Invalid choice. Try again.[/]")
