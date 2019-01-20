#!/usr/bin/env python
#coding: utf-8
#author: J0k3r

from app.app_core import CLI

logo = """
\033[33m      __          _______  \033[0m \033[31m _    _             _            \033[0m
\033[33m     /\ \        / /  __ \ \033[0m \033[31m| |  | |           | |           \033[0m
\033[33m    /  \ \  /\  / /| |  | |\033[0m \033[31m| |__| |_   _ _ __ | |_\033[34m ___ \033[0m\033[31m_ __ \033[0m
\033[33m   / /\ \ \/  \/ / | |  | |\033[0m \033[31m|  __  | | | | '_ \| __\033[34m/ _ \\\033[0m\033[31m '__|\033[0m
\033[33m  / ____ \  /\  /  | |__| |\033[0m \033[31m| |  | | |_| | | | | |\033[34m|  __/\033[0m\033[31m |   \033[0m
\033[33m /_/    \_\/  \/   |_____/ \033[0m \033[31m|_|  |_|\__,_|_| |_|\__\033[34m\___|\033[0m\033[31m_|   \033[0m\033[1m{\033[0m\033[4m\033[35mver 1.0\033[0m\033[0m\033[1m}\033[0m

                \033[96m>\033[0m help/h to show help info \033[1m█\033[0m                          
                                                            \033[32m---by J0k3r\033[0m
"""

def main():
   print logo
   interface = CLI()

   while True:
       try:
           interface.cmdloop()
       except KeyboardInterrupt:
           print "Interrupt: use the 'quit/q' command to quit"

if __name__ == "__main__":
   main()
