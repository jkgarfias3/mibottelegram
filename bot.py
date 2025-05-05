import asyncio
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token de tu bot
TOKEN = '7856798577:AAGzCAJxbf6-jkUYMlZGVwkpQ8m-R6oIgqI'

# Diccionario para rastrear tareas activas por usuario (chat_id)
usuarios_activos = {}

# Lista de mensajes con botones y firma
mensajes = [
    {
        "texto": "📚 ¿Necesitas hacer cambios en tus notas o en tu documentación? Conozco los procesos y puedo ayudarte a facilitar ese trámite de manera segura. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    },
    {
        "texto": "📝 Si quieres gestionar modificaciones en tu calificación o certificados, puedo orientarte y ofrecerte soluciones rápidas y confiables. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    },
    {
        "texto": "🎯 ¿Buscas resolver temas relacionados con tus notas o documentación académica? Aquí estoy para ayudarte a gestionar todo de forma efectiva. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    },
    {
        "texto": "💻 ¿Requieres realizar ajustes en tus registros o certificados? Con experiencia en el tema, puedo ayudarte a gestionar esos cambios de manera discreta. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    },
    {
        "texto": "🎉 Si necesitas gestionar modificaciones en tus registros académicos, te puedo apoyar en cada paso para que el proceso sea sencillo y seguro. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    },
    {
        "texto": "🤓 ¿Quieres solucionar temas relacionados con tus calificaciones o certificados? Tengo las habilidades para ayudarte a gestionar todo eficazmente. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    },
    {
        "texto": "💥 Si necesitas hacer cambios en tus notas o en tus registros, puedo facilitarte la gestión y asesorarte en todo momento. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    },
    {
        "texto": "📈 Quiero ayudarte a gestionar cambios en tu documentación académica, ofreciéndote soluciones rápidas y confiables. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    },
    {
        "texto": "🚀 Mi experiencia me permite apoyarte en la gestión de cambios en tus registros sin complicaciones ni riesgos. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    },
    {
        "texto": "🎓 ¿Necesitas realizar ajustes en tus calificaciones o certificados? Estoy aquí para ayudarte a gestionar todo de forma profesional y discreta. ",
        "enlace": "https://t.me/BOBNOTASPERU"
    }
]

# Autoeliminar mensaje después de unos segundos
async def eliminar_mensaje(chat_id, message_id, context, retraso=5):
    await asyncio.sleep(retraso)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

# Ciclo individual por usuario
async def ciclo_mensajes_individual(chat_id, context):
    while usuarios_activos.get(chat_id):
        mensaje_obj = random.choice(mensajes)
        texto = mensaje_obj["texto"] + "\n\n@PROFEBOB"
        boton = InlineKeyboardButton("📎 Ver Referencias", url=mensaje_obj["enlace"])
        teclado = InlineKeyboardMarkup([[boton]])

        try:
            msg = await context.bot.send_message(
                chat_id=chat_id,
                text=texto,
                reply_markup=teclado,
                parse_mode='Markdown'
            )
            asyncio.create_task(eliminar_mensaje(chat_id, msg.message_id, context, retraso=5))
        except Exception as e:
            print(f"Error al enviar mensaje a {chat_id}: {e}")
            break  # Salir del ciclo si falla

        await asyncio.sleep(5)

# Comando /start para iniciar el ciclo por usuario
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await update.message.reply_text(
        "🔰 *BIENVENID@ A PROFEBOB PERÚ* 🔐\n\n"
        "📍 *Servicios discretos y seguros:*\n"
        "📚 Cambios de notas académicos\n"
        "🧾 Certificados títulos actualizados\n"
        "💸 Descuentos en pensiones\n"
        "🔒 Opciones tech personalizadas\n\n"
        "📌 *CONTÁCTAME:* @profebob\n"
        "📎 *Revisa las referencias y únete a los que ya confiaron* 🔍",
        parse_mode='Markdown'
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text="📝 *Menú:*",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📞 Contactarme con Bob", url="https://t.me/PROFEBOB")],
            [InlineKeyboardButton("🔗 Ver referencias", url="https://t.me/BOBNOTASPERU")]
        ]),
        parse_mode='Markdown'
    )

    # Solo iniciar si el usuario no tiene un ciclo activo
    if not usuarios_activos.get(chat_id):
        usuarios_activos[chat_id] = True
        asyncio.create_task(ciclo_mensajes_individual(chat_id, context))

# Comando /stop para detener el ciclo
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if usuarios_activos.get(chat_id):
        usuarios_activos[chat_id] = False
        await update.message.reply_text("🚫 El ciclo ha sido detenido.")
    else:
        await update.message.reply_text("ℹ️ No hay ningún ciclo activo para ti.")

# Inicializar el bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    print("✅ BOT INICIADO Y LISTO")
    app.run_polling()