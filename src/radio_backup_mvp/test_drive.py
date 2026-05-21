from conexion import autenticar_drive


def probar_conexion():
    service = autenticar_drive()

    info = service.about().get(
        fields="user,storageQuota"
    ).execute()

    usuario = info["user"]
    quota = info["storageQuota"]

    print("Conectado a Google Drive")
    print("Usuario:", usuario.get("emailAddress"))

    usado_gb = int(quota.get("usage", 0)) / (1024 ** 3)
    print(f"Usado: {usado_gb:.2f} GB")

    if "limit" in quota:
        limite_gb = int(quota.get("limit", 0)) / (1024 ** 3)
        print(f"Límite: {limite_gb:.2f} GB")
    else:
        print("Límite: No disponible")


if __name__ == "__main__":
    probar_conexion()