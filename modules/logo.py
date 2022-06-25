import datetime

def logo():
	print(""" __  __                                
|  \/  |_   _ _ __  ___  ___  ___ _ __ 
| |\/| | | | | '_ \/ __|/ _ \/ _ \ '__|
| |  | | |_| | | | \__ \  __/  __/ |   
|_|  |_|\__,_|_| |_|___/\___|\___|_|  """)

	# printing date and time
	x = datetime.datetime.now().strftime("%H:%M:%S %b %d %Y")
	print(x)
