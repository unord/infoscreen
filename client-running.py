#! /usr/bin/env python3
import subprocess


def main():
    while True:
        subprocess.run('infoscreen-client.exe', shell=True)


if __name__ == '__main__':
    main()