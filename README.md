# VPN FIXER

La VPN de la Digital Factory se cae a cada rato, es por eso que he creado este script que reinicia la conexión cuando esta se cae. Esto lo hace emulando una aplicación de autenticación como Google Authenticator, generando el código antes de ingresar las credenciales.

## Como Correrlo

Para correr esto vamos a necesitar setear un poco nuestro mac

### Instalar libs

Lo primero que vamos a necesitar son los binarios `openvpn` y `zbar` que podemos conseguir de `brew` con

```bash
brew install openvpn zbar
```

`zbar` no necesita nada mas, pero como `openvpn` es una herramienta de sistema, `brew` no crea un `symlink` a `/usr/local/bin` así que tenemos que crearlo nosotros:

```bash
ln -s /usr/local/opt/openvpn/sbin/openvpn /usr/local/bin
```

Con esto deberíamos poder correr:

```bash
openvpn --version
```

### Setear Python

Lo segundo que necesitamos es Python. Este repo fue construido con Python 3.13.5 pero como tenemos muy pocas dependencias puede que sirva con otra versión.

Necesitamos instalar las dependencias para eso corremos

```bash
pip install -r requirements.txt
```

Y luego podemos correr la aplicación como super user con

```bash
sudo python main.py
```

Deberíamos ver:

```
QR not found in .configs/qr.png
```

Y es porque nos faltan los archivos de configuración

### Archivos de configuración

Vamos a crear un directorio `.configs` y añadiremos tres (3) archivos de configuración: `client.ovpn`, `credentials.txt` y `qr.png`. Todos con dicho nombre.

#### client.ovpn

Este es el archivo de configuración de la vpn. Es el mismo con el que configuraste en un inicio la vpn de Falabella. Sin exponer nada importante, este es el formato que debe tener:

```
client
dev tun
proto udp
remote vpn.fif.tech 1194
resolv-retry infinite
nobind
persist-key
persist-tun
cipher AES-256-CBC
verb 3
auth-user-pass
auth-nocache
dhcp-option DNS 10.145.15.198
dhcp-option DNS 10.145.15.197
dhcp-option DNS 10.145.15.196
dhcp-option DNS 1.1.1.1
dhcp-option DOMAIN srv.fif.tech
auth-user-pass .configs/vpn-auth.txt # Añadir esta linea

<ca>
-----BEGIN CERTIFICATE-----
YOUR CERTIFICATE
-----END CERTIFICATE-----
</ca>
```

Es muy importante que añadamos la linea de autenticación ya que no viene por defecto.
```
auth-user-pass .configs/vpn-auth.txt # Añadir esta linea
```

Si queremos que los logs funcionen bien, no puede existir una linea que sea del estilo
```
mute 20
```

#### credentials.txt

En este archivo vamos a colocar nuestras credenciales de la siguiente forma:

```
LDAP-username
LDAP-password
```
Importante colocar la solo la contraseña, sin el código de authenticator.

### qr.png

Necesitamos es el QR que nos envía la digital factory para el segundo factor de autenticación. Para eso ingresamos a [portal](https://portal.fif.tech/profile) y presionamos el botón que dice "**Solicitar segundo factor de de Autenticación vpn FIFTech**".

Vamos a Teams y descargamos la imagen QR que nos acaba de llegar con **Bender** fumando un puro y la pegamos en `.configs/` con el nombre `qr.png`
