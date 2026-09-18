from .chat import chat
from colorama import Fore, Style, init
from qlab.core.model import User, test_user

init(autoreset=True)

print(f"{Fore.YELLOW}{'='*40}")
print(f"{Fore.YELLOW}  Welcome to QuizLab AI — Ask Zuri!")
print(f"{Fore.YELLOW}{'='*40}\n")

while True:
    prompt = input(f"{Fore.GREEN}{Style.BRIGHT}{test_user.first_name}: {Style.RESET_ALL}")
    
    if prompt.strip().lower() in ("exit", "quit", "bye"):
        print(f"\n{Fore.YELLOW}Zuri: Goodbye! Good luck with your studies. 👋\n")
        break

    response = chat(user=test_user, prompt=prompt)
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Zuri:{Style.RESET_ALL} {response.content}\n")