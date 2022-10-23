from rich.console import Console

console = Console()


def menu():
    console.print("\n---------------Menu---------------")
    console.print("[bold][1] Get all credentials of specific app[/bold]")
    console.print("[bold][2] List apps in database[/bold]")
    console.print("[bold][3] Find accounts using email/phone[/bold]")
    console.print("[bold][4] Add new app to database[/bold]")
    console.print("[bold][5] Update Data[/bold]")
    console.print("[bold][6] Delete app from database[/bold]")
    console.print("[bold][7] Generate password[/bold]")
    console.print("[bold][8] Exit[/bold]")
    console.print("------------------------------------")
