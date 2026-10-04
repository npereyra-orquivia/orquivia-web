# Orquivia · Web bilingüe

Sitio estático para la consultoría de procesos, automatización, aplicaciones a medida e integración de plataformas para despachos de arquitectura.

El dominio configurado en GitHub Pages es `orquivia.com`. Se conserva el archivo CNAME.

## Construcción y comprobación

La fuente está en `tools/build_site.py` y los textos reutilizables en `content/`. No se necesitan dependencias externas para construir.

```powershell
python tools/build_site.py
python tools/check_site.py
python tools/build_site.py --production --output .publish/orquivia-production
python tools/check_seo.py .publish/orquivia-production
node --check script.js
```

La construcción local genera una revisión con `noindex`. El modo de producción exige una carpeta separada y genera páginas indexables, sitemap y robots para el dominio real. El CSS y JavaScript llevan una versión calculada a partir de su contenido para evitar recursos desactualizados en caché.

La carpeta exportada contiene únicamente los archivos públicos necesarios; se publica manteniendo CNAME y `.nojekyll`. La configuración de publicación de Pages se mantiene en la cuenta de Orquivia.

## Agenda y correo de Arsys

El correo sigue en Arsys. El formulario prepara un mensaje para revisar y enviar desde el correo del visitante; no envía datos a un servidor, ni confirma reservas automáticamente.

Se puede proponer fecha y hora de una llamada de 15 minutos, en horario de Barcelona. La cita queda pendiente de confirmación por correo. Si el visitante utiliza Webmail, puede copiar el mensaje y enviarlo a `info@orquivia.com`.

Para ofrecer horarios disponibles, crear una página de reservas en Google Calendar u otro servicio elegido. En Google Calendar: crear una programación de citas de 15 minutos, definir disponibilidad, zona Europe/Madrid y revisar qué agenda bloquea horas ocupadas; después, copiar el enlace público de reserva. Documentación: https://support.google.com/calendar/answer/10729749?hl=es

Añadir ese enlace HTTPS en `booking_url` de `content/site-settings.json` y reconstruir. El sitio mostrará el botón de la agenda externa en lugar de la propuesta de horario. No se carga una agenda incrustada automáticamente. Antes de activar un proveedor, completar en privacidad su identificación y tratamiento de reservas.

## Pendiente antes de publicar

- Completar en `content/site-settings.json` los datos de inscripción de Orquivia Global SL en el Registro Mercantil. El aviso legal los señala como pendientes.
- Confirmar razón social, NIF y domicilio del aviso anterior, reutilizados en esta propuesta.
- Cuando se publique, verificar `orquivia.com` en Google Search Console y enviar `https://orquivia.com/sitemap.xml`. La indexación y posiciones dependen de Google; no se garantizan.

La web no instala analítica ni publicidad. La privacidad describe el formulario, el correo de Arsys y los registros de seguridad de GitHub Pages. Si se añaden nuevas herramientas, revisar la política según el funcionamiento real.

Las tres nuevas imágenes editoriales ilustran automatización documental, apps de seguimiento y sincronización de plataformas. Se generaron con ImageGen; no representan productos implantados ni documentación de clientes. El caso de Value Retail conserva su alcance real de consultoría y estandarización gráfica.
