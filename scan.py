import argparse
import socket
import time
import json


def main():
    parser = argparse.ArgumentParser(
        prog="Scan port",
        description="Scan de port",
        epilog="dev: WezerClear  GitHub: https://github.com/WezerClear ",
    )

    parser.add_argument(
        "-i", "--ip", required=True, type=str, help="Addresse ip ou hostname target"
    )
    parser.add_argument(
        "-p",
        "--port",
        required=True,
        type=str,
        help="Port target. Exemple: 80,12 | all for all | fast pour les plus utilisés ",
    )
    parser.add_argument(
        "-t",
        "--temps",
        required=False,
        type=str,
        help="Temps entre chaque port | RECOMMANDE 1",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        help="Activer le mode verbose",
    )

    args = parser.parse_args()

    #    liste = args.port.split(",")
    #    for p in list:
    #        if int(p) < 0 or int(p) > 65535:
    #            return print("Saisir port valide")
    if args.port and args.port.lower() == "fast":
        print("fast")
        return scanFast(args.ip, args.temps, args.verbose)
    if args.port and args.port.lower() == "all":
        print("all")
        return scanAll(args.ip, args.temps, args.verbose)
    else:
        return scanSpé(args.ip, args.port, args.temps, args.verbose)


def scanAll(ip: str, temps: str, verbose: str):
    print("----------------Scan All Port----------------")
    if temps == None:
        temps = 0
    resultat = {}
    for p in range(1, 65536):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        time.sleep(int(temps))
        try:
            sock.connect((ip, int(p)))
            if verbose:
                print(p, "ouvert")
            resultat[p] = {"status": "ouvert", "service": getService(int(p))}
        except (socket.timeout, socket.error):
            if verbose:
                print(p, "fermé")
        finally:
            sock.close()
    json_resultat = json.dumps(resultat, indent=2)

    return print(json_resultat)


def scanFast(ip: str, temps: str, verbose: str):
    print("----------------Scan Most used Port----------------")
    if temps == None:
        temps = 0
    resultat = {}
    portListe = []
    with open("portConnuListe.txt", "r") as fichier:
        for ligne in fichier:
            portListe.append(ligne)
    fichier.close
    for p in portListe:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        time.sleep(int(temps))
        try:
            sock.connect((ip, int(p)))
            if verbose:
                print(p, "ouvert")
            resultat[p] = {"status": "ouvert", "service": getService(int(p))}
        except (socket.timeout, socket.error):
            if verbose:
                print(p, "fermé")
        finally:
            sock.close()
    json_resultat = json.dumps(resultat, indent=2)

    return print(json_resultat)


def scanSpé(ip: str, port: str, temps: str, verbose: str):
    print("----------------Scan", port, "Port----------------")
    if temps == None:
        temps = 0
    resultat = {}
    liste = port.split(",")
    for p in liste:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        time.sleep(int(temps))
        try:
            sock.connect((ip, int(p)))
            if verbose:
                print(p, "ouvert")
            resultat[p] = {"status": "ouvert", "service": getService(int(p))}
        except (socket.timeout, socket.error):
            if verbose:
                print(p, "fermé")
        finally:
            sock.close()
    json_resultat = json.dumps(resultat, indent=2)

    return print(json_resultat)


def getService(port: str):
    try:
        with open("portsConnu.txt", "r") as fichier:
            for ligne in fichier:
                if f"Port {port} :" in ligne:
                    return ligne.strip()
            return "Pas de service"
    except FileNotFoundError:
        return "Fichier non trouvé"


if __name__ == "__main__":
    main()
