# Orquivia · Web bilingüe

Sitio estático para despachos de arquitectura y project managers: procesos y documentación, coordinación de actuaciones concretas y aplicaciones de gestión a medida. Las experiencias con pequeños negocios y equipos de postventa se mencionan como recorrido profesional en Sobre Orquivia.

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

- Los datos de inscripción se contrastaron con el BORME del 18 de marzo de 2026: Registro Mercantil de Barcelona, sección 8, hoja B 652730, inscripción 1. La fuente oficial se enlaza desde el aviso legal.
- Confirmar razón social, NIF y domicilio del aviso anterior, reutilizados en esta propuesta.
- Cuando se publique, verificar `orquivia.com` en Google Search Console y enviar `https://orquivia.com/sitemap.xml`. La indexación y posiciones dependen de Google; no se garantizan.

La web no instala analítica ni publicidad. La privacidad describe el formulario, el correo de Arsys y los registros de seguridad de GitHub Pages. Si se añaden nuevas herramientas, revisar la política según el funcionamiento real.

Los servicios y artículos utilizan cinco escenas de trabajo ilustrativas generadas con ImageGen. Sus WebP y prompts están en `assets/photography/` y el mapa de uso en `content/photo-assets.json`. Las imágenes tienen variantes de 768 px para móvil y el pie identifica las escenas generadas. No se presentan como fotografías de clientes. Se mantiene el retrato seleccionado de Nicole. El caso de Value Retail conserva su esquema y su alcance real de consultoría y estandarización gráfica.

Las aplicaciones se muestran mediante versiones anonimizadas de las capturas aportadas por Nicole: consultas sobre un plano, control de trabajos y presupuestos. Se conserva la distribución y el detalle de las interfaces; ImageGen sustituye datos identificativos y privados por datos de muestra, sin simplificar las pantallas. Los originales privados no forman parte del sitio ni del repositorio. Los WebP revisados están en `assets/mockups/` y el proceso de edición se documenta en `assets/mockups/orquivia-capturas-v2-prompts.json`. El mapa de uso y los textos están en `content/app-mockups.json`. Las capturas se presentan a mayor ancho en la propia página, sin enlaces de ampliación ni recortes verticales; sus cifras son datos de muestra y no resultados comerciales.

La oferta se resume en tres servicios. Los ejemplos se basan en trabajos descritos por Nicole y no atribuyen ahorros, ingresos ni funcionalidades no aportadas. La aplicación para project managers permite crear y seguir consultas visualmente desde un plano. La coordinación de actuaciones tiene una página propia: `gestion-operativa.html` / `operational-coordination.html`.

El público comercial es despachos de arquitectura y project managers. Los otros negocios son experiencia previa, mencionada en Sobre Orquivia, y no segmentos de captación.

La portada parte del beneficio para arquitectura y project managers: control del proyecto, avance de entregas y capacidad para nuevos encargos. Explica después los servicios y utiliza el caso de planos como experiencia concreta; no promete porcentajes de ahorro ni ingresos.
